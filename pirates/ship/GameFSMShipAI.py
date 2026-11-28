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

    def _initWorldRefs(self):
        if self.oceanGrid is None:
            self.oceanGrid = self.ship.getParentObj()

        if self.world is None and self.oceanGrid:
            self.world = self.oceanGrid.getParentObj()

    def cleanup(self):
        self._stopAllTasks()
        self.targetShip = None
        self.targetDoId = 0
        self.threatList = {}

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
        return (target.getPos() - self.ship.getPos()).length()

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

    def onDamageReceived(self, attackerDoId, damage):
        self.addThreat(attackerDoId, damage)
        if self.getCurrentOrNextState() in self.EngageStates:
            self.engageTarget(self.air.doId2do.get(attackerDoId))

    # Navigation:

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

    def _localIslandPointToOcean(self, island, localX, localY):
        islandTransform = island.getIslandTransform()
        angle = math.radians(islandTransform[3] if len(islandTransform) > 3 else 0.0)
        return (islandTransform[0] + localX * math.cos(angle) - localY * math.sin(angle),
            islandTransform[1] + localX * math.sin(angle) + localY * math.cos(angle))

    def _getIslandCollisionSpheres(self):
        # islands don't move, so we only need to work these out once:
        if self._islandSpheres is not None:
            return self._islandSpheres

        self._initWorldRefs()
        if not self.world or not hasattr(self.world, 'builder'):
            return []

        self._islandSpheres = []
        for island in self.world.builder.getIslands():
            for sphere in island.getPortCollisionSpheres() or []:
                pos, radius = sphere.get('pos', (0, 0, 0)), sphere.get('radius', 0)
                if radius:
                    x, y = self._localIslandPointToOcean(island, pos[0], pos[1])
                    self._islandSpheres.append((x, y, float(radius)))

            # the island's inner sphere covers the island itself, the same
            # radius the ship deployer uses for it's minimum radius:
            sphereRadii = getattr(island, 'sphereRadii', None)
            if sphereRadii and sphereRadii[0] > 0:
                sphereCenter = getattr(island, 'sphereCenter', None) or [0, 0]
                x, y = self._localIslandPointToOcean(island, sphereCenter[0], sphereCenter[1])
                self._islandSpheres.append((x, y, float(sphereRadii[0])))

        return self._islandSpheres

    def _getBlockingIsland(self, x, y):
        for centerX, centerY, radius in self._getIslandCollisionSpheres():
            radius += self.IslandBuffer
            if (x - centerX) ** 2 + (y - centerY) ** 2 < radius * radius:
                return centerX, centerY, radius

        return None

    def _isPositionSafe(self, pos):
        return self._isWithinGridBounds(pos[0], pos[1]) and not self._getBlockingIsland(pos[0], pos[1])

    def _getRandomPatrolPos(self):
        homeX, homeY = self.homePos[0], self.homePos[1]
        for _ in range(10):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(self.WaypointRadius, self.PatrolRadius)
            x, y = self._clampToGridBounds(homeX + math.cos(angle) * dist, homeY + math.sin(angle) * dist)
            if self._isPositionSafe((x, y)):
                return Point3(x, y, 0)

        return Point3(homeX, homeY, 0)

    def _calculateHeadingTo(self, destination):
        pos = self.ship.getPos()
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
        heading = self._calculateHeadingTo(self._currentDestination)
        target = self._broadsideTarget
        if target and self._isValidTarget(target) and self._getDistanceToTarget(target) < self.BroadsideRange:
            # once in range the ship sails alongside the target, putting
            # whichever beam needs the least amount of turning toward it:
            bearing = self._calculateHeadingTo(target.getPos())
            leftBeam = self._normalizeAngle(bearing - 90.0)
            rightBeam = self._normalizeAngle(bearing + 90.0)
            if abs(self._normalizeAngle(leftBeam - self.ship.getH())) < abs(self._normalizeAngle(rightBeam - self.ship.getH())):
                heading = leftBeam
            else:
                heading = rightBeam

        x, y = self.ship.getX(), self.ship.getY()
        blocking = self._getBlockingIsland(x + -math.sin(math.radians(heading)) * self.IslandBuffer,
            y + math.cos(math.radians(heading)) * self.IslandBuffer)
        if blocking:
            # steer around the island by sailing along it's edge:
            awayHeading = -math.degrees(math.atan2(x - blocking[0], y - blocking[1]))
            leftEdge = self._normalizeAngle(awayHeading + 90.0)
            rightEdge = self._normalizeAngle(awayHeading - 90.0)
            if abs(self._normalizeAngle(leftEdge - heading)) < abs(self._normalizeAngle(rightEdge - heading)):
                heading = leftEdge
            else:
                heading = rightEdge

        return heading

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
        x = self.ship.getX() + -math.sin(math.radians(heading)) * distance
        y = self.ship.getY() + math.cos(math.radians(heading)) * distance
        x, y = self._clampToGridBounds(x, y)
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
            self.homePos = self.ship.getPos()

        self.targetShip = None
        self.targetDoId = 0
        self.ship.setSailAnimState('Idle')
        self._startMovementTo(self._getRandomPatrolPos(), self._getShipSpeed())
        self._startThinking(self.__patrolThink)

    def __patrolThink(self, task):
        target = self._selectBestTarget() or self._findNearestEnemy()
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
        self.ship.setSailAnimState('Idle')
        if not self._isValidTarget(self.targetShip):
            self.targetShip = self._selectBestTarget()

        self._startThinking(self.__chaseThink)

    def __chaseThink(self, task):
        if not self._isValidTarget(self.targetShip) or self._getDistanceToTarget(self.targetShip) > self.LoseTargetRadius:
            self.threatList.pop(self.targetDoId, None)
            self.targetShip = self._selectBestTarget()
            if not self.targetShip:
                self.ship.b_setGameState('Patrol', 0)
                return Task.done

            self.targetDoId = self.targetShip.doId

        self._startMovementTo(self.targetShip.getPos(), self._getShipSpeed(combatMode=True))
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
