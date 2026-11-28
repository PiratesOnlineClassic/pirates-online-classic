import math
import random

from panda3d.core import *

from direct.directnotify import DirectNotifyGlobal
from direct.fsm import FSM
from direct.task import Task

from pirates.ship import ShipGlobals
from pirates.ship import ShipBalance
from pirates.battle import EnemyGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.world import WorldGlobals

def _localIslandPointToOcean(island, localX, localY):
    islandTransform = island.getIslandTransform()
    angle = math.radians(islandTransform[3] if len(islandTransform) > 3 else 0.0)
    return (islandTransform[0] + localX * math.cos(angle) - localY * math.sin(angle),
        islandTransform[1] + localX * math.sin(angle) + localY * math.cos(angle))


def getIslandAvoidSpheres(world):
    """
    The (x, y, radius) spheres NPC ships keep out of, in ocean grid space: each island's
    inner LOD sphere, which covers the whole island, and the island's port collision spheres.
    """

    spheres = []
    for island in world.builder.getIslands():
        for sphere in island.getPortCollisionSpheres() or []:
            pos, radius = sphere.get('pos', (0, 0, 0)), sphere.get('radius', 0)
            if radius:
                x, y = _localIslandPointToOcean(island, pos[0], pos[1])
                spheres.append((x, y, float(radius)))

        # the island's inner sphere covers the island itself, the same
        # radius the ship deployer uses for it's minimum radius:
        sphereRadii = getattr(island, 'sphereRadii', None)
        if sphereRadii and sphereRadii[0] > 0:
            sphereCenter = getattr(island, 'sphereCenter', None) or [0, 0]
            x, y = _localIslandPointToOcean(island, sphereCenter[0], sphereCenter[1])
            spheres.append((x, y, float(sphereRadii[0])))

    return spheres


class GameFSMShipAI(FSM.FSM):
    """
    The AI side game state of a ship. The states mirror the client's GameFSMShip,
    NPC ships additionally sail themselves while in the Patrol and AttackChase states.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('GameFSMShipAI')

    # how often the ship's course is updated and how often it looks for targets:
    MovePeriod = PiratesGlobals.AI_MOVEMENT_PERIOD
    ThinkPeriod = 1.0

    # patrolling ships stay within the search radius of where they first started patrolling:
    PatrolRadius = EnemyGlobals.SHIP_SEARCH_RADIUS
    WaypointRadius = 200.0

    # ships give up on targets that sail far enough away from them:
    LoseTargetRadius = EnemyGlobals.SHIP_SEARCH_RADIUS * 1.5

    # broadsides are fired when the target is within range and within the
    # cannon heading range of either beam of the ship:
    BroadsideRange = ShipGlobals.BROADSIDE_MAX_AUTOAIM_DIST
    BroadsideHeadingRange = PiratesGlobals.AI_CANNON_HEADING_RANGE
    BroadsideReloadTime = 10.0

    # ships kept to a sea lane stop this close to their target:
    HoldRange = 600.0

    # ships keep this far away from islands and the edge of the ocean grid:
    IslandBuffer = 200.0
    GridMargin = WorldGlobals.OCEAN_CELL_SIZE

    # default AI speed and turn rate for ships without AI speed data in ShipGlobals:
    DefaultSpeeds = ([50, 100, 115, 135], [10, 10])

    SinkingStates = ('Sinking', 'Sunk', 'Off', 'PutAway')

    # the states from which a ship will go after a target that attacks or aggros it:
    EngageStates = ('Patrol', 'AISteering', 'Neutral')

    def __init__(self, air, ship):
        FSM.FSM.__init__(self, 'GameFSMShipAI')

        self.air = air
        self.ship = ship

        self.oceanGrid = None
        self.world = None

        self.targetShip = None
        self.targetDoId = 0
        self.threatList = {}
        self.homePos = None
        self.lastBroadsideTime = [0.0, 0.0]

        self._shipLevel = None
        self._sinkingTask = None
        self._thinkTask = None
        self._moveInterval = None
        self._currentDestination = None
        self._movementCallback = None
        self._movementSpeed = 0.0
        self._broadsideTarget = None
        self._islandSpheres = None

        # ships may be kept to a sea lane, a list of (x, y, radius) points the
        # ship sails along without straying further than the radius from it,
        # (used where the islands can't be avoided by their collision spheres)...
        self.seaLane = None

        # a ship that is hunting a target never gives up on it:
        self.huntTarget = None

        # ships spawned at a ship spawn node patrol back and forth along the route
        # the world data links the node to (see ShipManagerAI.getShipSpawnNodes):
        self.patrolRoute = None
        self._routeIndex = None
        self._routeStep = 1

    def _initWorldRefs(self):
        if self.oceanGrid is None:
            self.oceanGrid = self.ship.getParentObj()

        if self.world is None and self.oceanGrid:
            self.world = self.oceanGrid.getParentObj()

    def _getGridPos(self, obj):
        # ships sit under the ocean grid's cell origins, so their own position is
        # relative to the cell they're in. The ai works in ocean grid space...
        self._initWorldRefs()
        if self.oceanGrid is not None and not self.oceanGrid.isEmpty():
            return obj.getPos(self.oceanGrid)

        return obj.getPos()

    def cleanup(self):
        self._stopAllTasks()
        self.targetShip = None
        self.targetDoId = 0
        self.threatList = {}
        self.huntTarget = None

    def _stopAllTasks(self):
        self._stopThinking()
        self._stopMovement()

    def _startThinking(self, method):
        self._stopThinking()
        self._thinkTask = taskMgr.doMethodLater(self.ThinkPeriod, method,
            self.ship.uniqueName('ship-ai-think'))

    def _stopThinking(self):
        if self._thinkTask:
            taskMgr.remove(self._thinkTask)
            self._thinkTask = None

    # Ship stats:

    def _getSpeedData(self):
        speeds, turnRates = ShipGlobals.getAIShipSpeed(self.ship.shipClass)
        if not speeds or not turnRates:
            speeds, turnRates = self.DefaultSpeeds

        return speeds, turnRates

    def _getShipSpeed(self, combatMode=False):
        # AI ship speeds are [min, cruise, max, boost] feet per second:
        speeds, turnRates = self._getSpeedData()
        speed = speeds[2] if combatMode else speeds[1]
        return speed * ShipBalance.SpeedModifier.getValue()

    def _getTurnRate(self):
        speeds, turnRates = self._getSpeedData()
        return turnRates[0]

    def _getShipLevel(self):
        if self._shipLevel is None:
            self._shipLevel = ShipGlobals.getShipLevel(self.ship.shipClass) or 1

        return self._shipLevel

    def _getTargetLevel(self, target):
        if target.getCrew():
            return target.getCrewLevel()

        return target.getLevel()

    def _getAggroRadius(self, target):
        # this matches the aggro sphere the client uses for NPC ships (DistributedShip.getAggroSphereSize):
        levelDiff = max(1, abs(self._getTargetLevel(target) - self._getShipLevel()) - EnemyGlobals.AGGRO_RADIUS_LEVEL_BUFFER)
        return max(EnemyGlobals.SHIP_SEARCH_RADIUS / max(1.0, levelDiff / EnemyGlobals.AGGRO_RADIUS_FALLOFF_RATE),
            EnemyGlobals.SHIP_MIN_SEARCH_RADIUS)

    # Targeting:

    def _getDistanceToTarget(self, target):
        return (self._getGridPos(target) - self._getGridPos(self.ship)).length()

    def _isValidTarget(self, target):
        # NPC ships only ever fight player ships, they leave each other alone...
        if not target or target.isEmpty() or target.isDeleted():
            return False

        if target.getBaseTeam() != ShipGlobals.PLAYER_TEAM:
            return False

        if target.getParentObj() is not self.ship.getParentObj():
            return False

        if hasattr(target, 'gameFSM') and target.gameFSM.getCurrentOrNextState() in self.SinkingStates:
            return False

        return True

    def addThreat(self, attackerDoId, damage=0):
        self.threatList[attackerDoId] = self.threatList.get(attackerDoId, 0) + damage

    def _selectBestTarget(self):
        # the ship goes after whoever has done the most damage to it:
        bestTarget = None
        bestThreat = -1
        for attackerDoId, threat in list(self.threatList.items()):
            attacker = self.air.doId2do.get(attackerDoId)
            if not self._isValidTarget(attacker):
                del self.threatList[attackerDoId]
                continue

            if threat > bestThreat:
                bestTarget = attacker
                bestThreat = threat

        return bestTarget

    def _findNearestEnemy(self):
        nearest = None
        nearestDist = None
        for target in self.air.shipManager.getPlayerShips():
            if not self._isValidTarget(target):
                continue

            dist = self._getDistanceToTarget(target)
            if dist > self._getAggroRadius(target):
                continue

            if nearestDist is None or dist < nearestDist:
                nearest = target
                nearestDist = dist

        return nearest

    def engageTarget(self, target):
        if not self._isValidTarget(target):
            return False

        self.targetShip = target
        self.targetDoId = target.doId
        if self.getCurrentOrNextState() in self.EngageStates:
            self.ship.b_setGameState('AttackChase', 0)

        return True

    def setPatrolRoute(self, patrolRoute):
        self.patrolRoute = [Point3(point[0], point[1], 0) for point in patrolRoute] if patrolRoute else None
        self._routeIndex = None
        self._routeStep = 1

    def _getNextRoutePoint(self):
        route = self.patrolRoute
        if self._routeIndex is None:
            # start (or after a chase, carry on) from whichever point is nearest:
            pos = self._getGridPos(self.ship)
            self._routeIndex = min(range(len(route)), key=lambda index: (route[index] - pos).length())
            return route[self._routeIndex]

        if len(route) > 1:
            if not 0 <= self._routeIndex + self._routeStep < len(route):
                self._routeStep = -self._routeStep

            self._routeIndex += self._routeStep

        return route[self._routeIndex]

    def setSeaLane(self, seaLane):
        self.seaLane = list(seaLane) if seaLane else None

    def hunt(self, target):
        # the ship goes after the target and keeps after it until it's sunk:
        self.huntTarget = target
        return self.engageTarget(target)

    def stopHunting(self):
        self.huntTarget = None

    def _getHuntTarget(self):
        if self.huntTarget is not None and not self._isValidTarget(self.huntTarget):
            self.huntTarget = None

        return self.huntTarget

    def onDamageReceived(self, attackerDoId, damage):
        self.addThreat(attackerDoId, damage)
        if self.getCurrentOrNextState() in self.EngageStates:
            self.engageTarget(self.air.doId2do.get(attackerDoId))

    # Navigation:

    def _getLaneSegments(self):
        points = self.seaLane or []
        if len(points) == 1:
            return [(points[0], points[0])]

        return list(zip(points, points[1:]))

    def _projectOnLaneSegment(self, x, y, a, b):
        # returns how far along the segment the closest point to (x, y) is (0 - 1),
        # and the distance to that point:
        dx, dy = b[0] - a[0], b[1] - a[1]
        lengthSq = dx * dx + dy * dy
        t = 0.0
        if lengthSq > 0:
            t = max(0.0, min(1.0, ((x - a[0]) * dx + (y - a[1]) * dy) / lengthSq))

        px, py = a[0] + dx * t, a[1] + dy * t
        return t, math.hypot(x - px, y - py)

    def _getLanePosition(self, x, y):
        # the distance along the lane of the closest point on the lane to (x, y),
        # and how far (x, y) strays from the lane past the lane's radius:
        bestAlong = 0.0
        bestStray = None
        along = 0.0
        for a, b in self._getLaneSegments():
            t, dist = self._projectOnLaneSegment(x, y, a, b)
            radius = a[2] + (b[2] - a[2]) * t
            stray = dist - radius
            if bestStray is None or stray < bestStray:
                bestAlong = along + math.hypot(b[0] - a[0], b[1] - a[1]) * t
                bestStray = stray

            along += math.hypot(b[0] - a[0], b[1] - a[1])

        return bestAlong, bestStray or 0.0

    def _getLanePoint(self, along):
        for a, b in self._getLaneSegments():
            length = math.hypot(b[0] - a[0], b[1] - a[1])
            if along <= length or (a, b) == self._getLaneSegments()[-1]:
                t = max(0.0, min(1.0, along / length)) if length else 0.0
                return Point3(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, 0)

            along -= length

        return Point3(self.seaLane[0][0], self.seaLane[0][1], 0)

    def _isInLane(self, x, y):
        return not self.seaLane or self._getLanePosition(x, y)[1] <= 0

    def _isHolding(self):
        # in the narrow waters of a lane the ship holds it's position once it is
        # close enough to it's target to trade broadsides, turning to bring it's guns to bear:
        target = self._broadsideTarget
        return bool(self.seaLane and target is not None and self._isValidTarget(target) and
                    self._getDistanceToTarget(target) < self.HoldRange)

    def _clampToLane(self, x, y):
        # the point in the lane closest to (x, y):
        best = None
        for a, b in self._getLaneSegments():
            t, dist = self._projectOnLaneSegment(x, y, a, b)
            radius = a[2] + (b[2] - a[2]) * t
            if best is None or dist - radius < best[0]:
                best = (dist - radius, a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, dist, radius)

        stray, px, py, dist, radius = best
        if stray <= 0 or not dist:
            return Point3(x, y, 0)

        scale = radius * 0.9 / dist
        return Point3(px + (x - px) * scale, py + (y - py) * scale, 0)

    def _getLaneWaypoint(self, destination):
        # ships follow the lane to their destination, aiming for a point a little
        # further along the lane until the destination is just ahead of them:
        shipPos = self._getGridPos(self.ship)
        shipAlong, shipStray = self._getLanePosition(shipPos[0], shipPos[1])
        destAlong, destStray = self._getLanePosition(destination[0], destination[1])
        if abs(destAlong - shipAlong) <= self.WaypointRadius:
            return self._clampToLane(destination[0], destination[1])

        if shipStray > 0:
            # get back onto the lane before going anywhere else:
            return self._getLanePoint(shipAlong)

        step = min(self.WaypointRadius * 1.5, abs(destAlong - shipAlong))
        return self._getLanePoint(shipAlong + (step if destAlong > shipAlong else -step))

    def _getGridBounds(self):
        halfSize = (WorldGlobals.OCEAN_GRID_SIZE * WorldGlobals.OCEAN_CELL_SIZE) / 2.0
        return (-halfSize + self.GridMargin, halfSize - self.GridMargin,
            -halfSize + self.GridMargin, halfSize - self.GridMargin)

    def _isWithinGridBounds(self, x, y):
        minX, maxX, minY, maxY = self._getGridBounds()
        return minX <= x <= maxX and minY <= y <= maxY

    def _clampToGridBounds(self, x, y):
        minX, maxX, minY, maxY = self._getGridBounds()
        return max(minX, min(maxX, x)), max(minY, min(maxY, y))

    def _getIslandCollisionSpheres(self):
        # islands don't move, so we only need to work these out once:
        if self._islandSpheres is not None:
            return self._islandSpheres

        self._initWorldRefs()
        if not self.world or not hasattr(self.world, 'builder'):
            return []

        self._islandSpheres = getIslandAvoidSpheres(self.world)
        return self._islandSpheres

    def _getBlockingIsland(self, x, y):
        # a sea lane keeps the ship clear of the islands by itself:
        if self.seaLane:
            return None

        for centerX, centerY, radius in self._getIslandCollisionSpheres():
            radius += self.IslandBuffer
            if (x - centerX) ** 2 + (y - centerY) ** 2 < radius * radius:
                return centerX, centerY, radius

        return None

    def _getTurningRadius(self):
        # how wide a circle the ship sails when turning as hard as it can:
        speed = max(self._movementSpeed, 1.0)
        return speed / math.radians(max(self._getTurnRate(), 1.0))

    def _getAvoidRange(self):
        # far enough ahead to turn clear of an island at the ship's current speed...
        return self.IslandBuffer + self._getTurningRadius() * 2.0

    def _getAvoidSphere(self, x, y, heading, distance):
        """
        Returns the nearest island avoid sphere (grown by the island buffer) the ship sails
        into within the distance along the heading, or the one the ship is already within.
        """

        if self.seaLane:
            return None

        dirX, dirY = -math.sin(math.radians(heading)), math.cos(math.radians(heading))
        nearest = None
        for centerX, centerY, radius in self._getIslandCollisionSpheres():
            radius += self.IslandBuffer
            offsetX, offsetY = centerX - x, centerY - y
            distSq = offsetX * offsetX + offsetY * offsetY
            if distSq < radius * radius:
                return centerX, centerY, radius

            along = offsetX * dirX + offsetY * dirY
            perpSq = distSq - along * along
            if along <= 0 or perpSq >= radius * radius:
                continue

            hitDist = along - math.sqrt(radius * radius - perpSq)
            if hitDist <= distance and (nearest is None or hitDist < nearest[0]):
                nearest = (hitDist, centerX, centerY, radius)

        if nearest:
            return nearest[1:]

        return None

    def _getAvoidHeading(self, heading):
        """
        Steers the ship around the island avoid spheres in it's path, the ship sails along
        whichever tangent of the sphere turns it the least from the heading it wants...
        """

        x, y = self._getGridPos(self.ship).getXy()
        avoidRange = self._getAvoidRange()
        sphere = self._getAvoidSphere(x, y, heading, avoidRange)
        if not sphere:
            return heading

        centerX, centerY, radius = sphere
        dist = math.hypot(x - centerX, y - centerY)
        awayHeading = -math.degrees(math.atan2(x - centerX, y - centerY))
        if dist <= radius:
            # already too close, get back out to open water first:
            return awayHeading

        toCenter = self._normalizeAngle(awayHeading + 180.0)
        offset = math.degrees(math.asin(min(1.0, radius / dist)))
        tangents = sorted((self._normalizeAngle(toCenter + offset), self._normalizeAngle(toCenter - offset)),
            key=lambda tangent: abs(self._normalizeAngle(tangent - heading)))
        for tangent in tangents:
            blocking = self._getAvoidSphere(x, y, tangent, avoidRange)
            if not blocking or blocking == sphere:
                return tangent

        return awayHeading

    def _isRunningAground(self, fromX, fromY, toX, toY):
        # a ship never sails any further into an island than it already is:
        if self.seaLane:
            return False

        for centerX, centerY, radius in self._getIslandCollisionSpheres():
            toDistSq = (toX - centerX) ** 2 + (toY - centerY) ** 2
            if toDistSq < radius * radius and toDistSq < (fromX - centerX) ** 2 + (fromY - centerY) ** 2:
                return True

        return False

    def _isPositionSafe(self, pos):
        return self._isWithinGridBounds(pos[0], pos[1]) and not self._getBlockingIsland(pos[0], pos[1])

    def _getRandomPatrolPos(self):
        if self.patrolRoute:
            return self._getNextRoutePoint()

        homeX, homeY = self.homePos[0], self.homePos[1]
        if self.seaLane:
            homeAlong = self._getLanePosition(homeX, homeY)[0]
            return self._getLanePoint(max(0.0, homeAlong + random.uniform(-self.PatrolRadius, self.PatrolRadius) / 4.0))

        for _ in range(10):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(self.WaypointRadius, self.PatrolRadius)
            x, y = self._clampToGridBounds(homeX + math.cos(angle) * dist, homeY + math.sin(angle) * dist)
            if self._isPositionSafe((x, y)):
                return Point3(x, y, 0)

        return Point3(homeX, homeY, 0)

    def _calculateHeadingTo(self, destination):
        pos = self._getGridPos(self.ship)
        return -math.degrees(math.atan2(destination[0] - pos[0], destination[1] - pos[1]))

    def _normalizeAngle(self, angle):
        return (angle + 180.0) % 360.0 - 180.0

    def _getMovementDoneName(self):
        return 'ai-move-done-%d' % self.ship.doId

    def _startMovementTo(self, destination, speed, onComplete=None):
        self._initWorldRefs()
        self._currentDestination = Point3(destination[0], destination[1], 0)
        self._movementSpeed = speed
        self._movementCallback = onComplete
        if not self._moveInterval:
            self._moveInterval = taskMgr.doMethodLater(self.MovePeriod, self._moveTask,
                self.ship.uniqueName('ship-ai-move'))

    def _stopMovement(self):
        if self._moveInterval:
            if isinstance(self._moveInterval, Task.Task):
                taskMgr.remove(self._moveInterval)
            else:
                self._moveInterval.pause()

            self._moveInterval = None

        self.ship.ignore(self._getMovementDoneName())
        self._currentDestination = None
        self._movementCallback = None
        self._broadsideTarget = None

    def _isMoving(self):
        return self._currentDestination is not None

    def _onMovementComplete(self):
        self._moveInterval = None
        self._currentDestination = None
        callback = self._movementCallback
        self._movementCallback = None
        if callback:
            callback()

    def _getDesiredHeading(self):
        destination = self._currentDestination
        if self.seaLane:
            destination = self._getLaneWaypoint(destination)

        heading = self._calculateHeadingTo(destination)
        target = self._broadsideTarget
        if target and self._isValidTarget(target) and self._getDistanceToTarget(target) < self.BroadsideRange:
            # once in range the ship sails alongside the target, putting
            # whichever beam needs the least amount of turning toward it:
            bearing = self._calculateHeadingTo(self._getGridPos(target))
            leftBeam = self._normalizeAngle(bearing - 90.0)
            rightBeam = self._normalizeAngle(bearing + 90.0)
            if abs(self._normalizeAngle(leftBeam - self.ship.getH())) < abs(self._normalizeAngle(rightBeam - self.ship.getH())):
                beamHeading = leftBeam
            else:
                beamHeading = rightBeam

            # a ship kept to a lane only turns broadside where there's room to:
            x, y = self._getGridPos(self.ship).getXy()
            if self._isHolding() or self._isInLane(x + -math.sin(math.radians(beamHeading)) * self.WaypointRadius,
                                                   y + math.cos(math.radians(beamHeading)) * self.WaypointRadius):
                heading = beamHeading

        return self._getAvoidHeading(heading)

    def _moveTask(self, task):
        if self._currentDestination is None:
            self._moveInterval = None
            return Task.done

        dt = self.MovePeriod
        heading = self.ship.getH()
        turn = self._normalizeAngle(self._getDesiredHeading() - heading)
        maxTurn = self._getTurnRate() * dt
        heading += max(-maxTurn, min(maxTurn, turn))

        distance = self._movementSpeed * dt
        if self._isHolding():
            distance = 0

        shipX, shipY = self._getGridPos(self.ship).getXy()
        x = shipX + -math.sin(math.radians(heading)) * distance
        y = shipY + math.cos(math.radians(heading)) * distance
        if self.seaLane and not self._isInLane(x, y) and self._isInLane(shipX, shipY):
            # don't run aground, turn without making way until the ship can carry on:
            x, y = shipX, shipY
        elif self._isRunningAground(shipX, shipY, x, y):
            x, y = shipX, shipY

        x, y = self._clampToGridBounds(x, y)
        grid = self.ship.getParentObj()
        if grid is not None:
            self.ship.setPosHpr(grid, x, y, 0, heading, 0, 0)
        else:
            self.ship.setPosHpr(x, y, 0, heading, 0, 0)

        if self._broadsideTarget is None:
            if (self._currentDestination - Point3(x, y, 0)).length() < self.WaypointRadius:
                self._onMovementComplete()
                return Task.done

        return Task.again

    # Broadsides:

    def _getBroadsideFacing(self, target):
        pos = target.getPos(self.ship)
        angle = math.degrees(math.atan2(pos[0], pos[1]))
        if abs(angle + 90.0) < self.BroadsideHeadingRange:
            return ShipGlobals.BROADSIDE_LEFT
        elif abs(angle - 90.0) < self.BroadsideHeadingRange:
            return ShipGlobals.BROADSIDE_RIGHT

        return -1

    def _attemptBroadside(self, target):
        if not self.ship.broadside:
            return False

        if self._getDistanceToTarget(target) > self.BroadsideRange:
            return False

        side = self._getBroadsideFacing(target)
        if side < 0:
            return False

        now = globalClock.getFrameTime()
        if now - self.lastBroadsideTime[side] < self.BroadsideReloadTime:
            return False

        if not self.ship.broadside.fireAtTarget(target, side):
            return False

        self.lastBroadsideTime[side] = now
        return True

    # States:

    def enterOff(self):
        self._stopAllTasks()

    def enterSpawn(self):
        taskMgr.doMethodLater(2.0, self.__spawnDone, self.ship.uniqueName('spawn-to-patrol'))

    def __spawnDone(self, task):
        self.ship.b_setGameState('Patrol', 0)
        return Task.done

    def exitSpawn(self):
        taskMgr.remove(self.ship.uniqueName('spawn-to-patrol'))

    def enterPatrol(self):
        self._initWorldRefs()
        if self.homePos is None:
            self.homePos = self._getGridPos(self.ship)

        self.targetShip = None
        self.targetDoId = 0
        self.ship.setSailAnimState('Idle')
        self._startMovementTo(self._getRandomPatrolPos(), self._getShipSpeed())
        self._startThinking(self.__patrolThink)

    def __patrolThink(self, task):
        target = self._getHuntTarget() or self._selectBestTarget() or self._findNearestEnemy()
        if target:
            self.engageTarget(target)
            return Task.done

        if not self._isMoving():
            self._startMovementTo(self._getRandomPatrolPos(), self._getShipSpeed())

        return Task.again

    def exitPatrol(self):
        self._stopAllTasks()

    def enterAttackChase(self):
        self._initWorldRefs()
        self._routeIndex = None
        self.ship.setSailAnimState('Idle')
        if not self._isValidTarget(self.targetShip):
            self.targetShip = self._getHuntTarget() or self._selectBestTarget()

        self._startThinking(self.__chaseThink)

    def __chaseThink(self, task):
        if not self._isValidTarget(self.targetShip) or (self.targetShip is not self._getHuntTarget() and
                self._getDistanceToTarget(self.targetShip) > self.LoseTargetRadius):
            self.threatList.pop(self.targetDoId, None)
            self.targetShip = self._getHuntTarget() or self._selectBestTarget()
            if not self.targetShip:
                self.ship.b_setGameState('Patrol', 0)
                return Task.done

            self.targetDoId = self.targetShip.doId

        self._startMovementTo(self._getGridPos(self.targetShip), self._getShipSpeed(combatMode=True))
        self._broadsideTarget = self.targetShip
        self._attemptBroadside(self.targetShip)
        return Task.again

    def exitAttackChase(self):
        self._stopAllTasks()

    def enterSinking(self):
        self._stopAllTasks()
        self.targetShip = None
        self._sinkingTask = taskMgr.doMethodLater(self.ship.getSinkDuration(), self.__shipSunk,
            self.ship.uniqueName('shipSunk'))

    def __shipSunk(self, task):
        self._sinkingTask = None
        self.ship.handleShipSunk()
        return Task.done

    def exitSinking(self):
        if self._sinkingTask is not None:
            taskMgr.remove(self._sinkingTask)
            self._sinkingTask = None

    def defaultEnter(self, *args):
        # the rest of the states (Docked, Adrift, ClientSteering, PutAway, the
        # flagship boarding states etc.) are not driven by the ship's AI:
        self._stopAllTasks()

    def defaultExit(self):
        pass
