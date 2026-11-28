from direct.directnotify import DirectNotifyGlobal

from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.ship import ShipGlobals
from pirates.tutorial import TutorialGlobals


class TutorialShipAI(DistributedShipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TutorialShipAI')

    # once Beck sets sail an undead ship turns up to the left of the ship
    # wreck (as seen from the tutorial cannon), the new pirate has to sink it
    # before the Jolly Roger shows up. it's only level 1, idles where it is and
    # never fires back...
    TargetShipClass = ShipGlobals.SKEL_PHANTOM
    TargetShipLevel = 1
    TargetShipHp = 1000
    TargetShipPos = (110, 540, 0)
    TargetShipH = 80

    def __init__(self, air):
        DistributedShipAI.__init__(self, air)
        self.tutorialStumpy = None
        self.tutorialBuilder = None
        self._tutorialSailing = False
        self._tutorialSailingRoute = []
        self._tutorialSailingIndex = 0
        self.tutorialOceanGrid = None
        self.tutorialAuthoredPos = None
        self.tutorialAuthoredHpr = None
        self.tutorialAuthoredState = None
        self.tutorialTarget = None
        self.tutorialTargetSunk = False

    def setGameState(self, stateName, avId, timeStamp=0):
        # remember the level editor start state, the tutorial ship is
        # shared by every new pirate and must be restored after each one...
        if stateName and self.tutorialAuthoredState is None:
            self.tutorialAuthoredState = stateName

        DistributedShipAI.setGameState(self, stateName, avId, timeStamp)

    def setTutorialStumpy(self, stumpy, builder):
        self.tutorialStumpy = stumpy
        self.tutorialBuilder = builder

    def _sendBoardingMovie(self, avatar):
        # The tutorial client already places the avatar on board after the cutscene.
        pass

    def setTutorialAuthoredPose(self, oceanGrid, pos, hpr):
        self.tutorialOceanGrid = oceanGrid
        self.tutorialAuthoredPos = tuple(pos)
        self.tutorialAuthoredHpr = tuple(hpr)

    def _buildAuthoredRoute(self, direction1First):
        creator = getattr(self.air, 'worldCreator', None)
        linkManager = getattr(creator, 'movementLinkManager', None)
        if not creator or not linkManager:
            return None

        outgoing = {}
        for links in linkManager.movementLinkData.values():
            for link in links:
                if len(link) < 3:
                    continue

                first, second, direction = link[:3]
                if direction == 'Bi-directional':
                    outgoing.setdefault(first, set()).add(second)
                    outgoing.setdefault(second, set()).add(first)
                elif direction in ('Direction 1', 'Direction 2'):
                    firstToSecond = (direction == 'Direction 1') == direction1First
                    source, destination = (first, second) if firstToSecond else (second, first)
                    outgoing.setdefault(source, set()).add(destination)

        startUid = self.getUniqueId()
        visited = {startUid}
        currentUid = startUid
        route = []
        while True:
            destinations = outgoing.get(currentUid, set())
            if len(destinations) != 1:
                return None

            nextUid = next(iter(destinations))
            if nextUid in visited:
                return route if route and nextUid == route[0][0] else None

            nodeData = creator.getObjectDataByUid(nextUid)
            if not nodeData or nodeData.get('Type') != 'Ship Movement Node':
                return None

            route.append((nextUid, nodeData.get('Pos')))
            visited.add(nextUid)
            currentUid = nextUid

    def _getTutorialSailingRoute(self):
        routes = [
            self._buildAuthoredRoute(direction1First=True),
            self._buildAuthoredRoute(direction1First=False),
        ]
        routes = [route for route in routes if route]
        if not routes:
            return None

        longestLength = max(len(route) for route in routes)
        longestRoutes = [route for route in routes if len(route) == longestLength]
        if len(longestRoutes) != 1:
            return None

        return longestRoutes[0]

    def startSailing(self):
        if self._tutorialSailing:
            return True

        route = self._getTutorialSailingRoute()
        if not route:
            self.notify.warning('Cannot start tutorial ship sailing without an unambiguous authored route!')
            return False

        self._tutorialSailing = True
        self._tutorialSailingRoute = route
        self._tutorialSailingIndex = 0
        return self._sailToNextWaypoint()

    def _sailToNextWaypoint(self):
        if not self._tutorialSailing or not self._tutorialSailingRoute:
            return False

        gameFSM = getattr(self, 'gameFSM', None)
        if not gameFSM:
            self.stopSailing()
            return False

        waypointUid, destination = self._tutorialSailingRoute[self._tutorialSailingIndex]
        self._tutorialSailingIndex = (self._tutorialSailingIndex + 1) % len(self._tutorialSailingRoute)
        gameFSM._initWorldRefs()

        x, y, z = destination
        if not gameFSM._isWithinGridBounds(x, y):
            self.notify.warning('Stopping tutorial ship at unsafe authored waypoint %s!' % waypointUid)
            self.stopSailing()
            return False

        speed = gameFSM._getShipSpeed()
        if speed <= 0:
            self.stopSailing()
            return False

        return self._startAuthoredMovementTo(
            destination, speed, onComplete=self._sailToNextWaypoint)

    def _startAuthoredMovementTo(self, destination, speed, onComplete=None):
        from panda3d.core import Point3

        gameFSM = self.gameFSM
        gameFSM._stopMovement()
        destination = Point3(destination)
        shipPos = Point3(self.getPos())
        distance = (destination - shipPos).length()
        if distance < 50:
            if onComplete:
                onComplete()
            return True

        oceanGrid = gameFSM.oceanGrid
        destNode = oceanGrid.attachNewNode('tutorial-route-dest-%d' % self.doId)
        destNode.setPos(destination)
        self.lookAt(destNode)
        destNode.removeNode()

        gameFSM._currentDestination = destination
        gameFSM._movementCallback = onComplete
        gameFSM._moveInterval = self.posInterval(
            distance / max(speed, 1.0),
            (destination.getX(), destination.getY(), destination.getZ()),
            other=oceanGrid)
        movementDone = gameFSM._getMovementDoneName()
        gameFSM._moveInterval.setDoneEvent(movementDone)
        self.acceptOnce(movementDone, gameFSM._onMovementComplete)
        gameFSM._moveInterval.start()
        return True

    def stopSailing(self):
        wasSailing = self._tutorialSailing
        self._tutorialSailing = False
        self._tutorialSailingRoute = []
        self._tutorialSailingIndex = 0
        if wasSailing and getattr(self, 'gameFSM', None):
            self.gameFSM._stopMovement()

    def spawnTutorialTarget(self):
        if self.tutorialTarget and not self.tutorialTarget.isDeleted():
            return self.tutorialTarget

        oceanGrid = self.tutorialOceanGrid
        if not oceanGrid:
            self.notify.warning('Cannot spawn the tutorial target without an ocean grid!')
            return None

        from pirates.piratesbase.PLocalizer import ShipClassNames
        from pirates.ship.NPCShipAI import NPCShipAI

        shipClass = self.TargetShipClass
        shipConfig = ShipGlobals.getShipConfig(shipClass)
        hullConfig = ShipGlobals.getHullConfig(shipClass)
        if not shipConfig or not hullConfig:
            self.notify.warning('Cannot spawn the tutorial target without ship configuration!')
            return None

        ship = NPCShipAI(self.air)
        ship.setUniqueId(TutorialGlobals.UNDEAD_SHIP_UID)
        ship.setBaseTeam(ShipGlobals.getShipTeam(shipClass))
        ship.setLevel(self.TargetShipLevel)
        ship.setShipClass(shipClass)
        ship.setName(ShipClassNames.get(shipClass, ''))
        ship.setNPCship(1)
        ship.setIsBoardable(0)
        ship.setMaxHp(self.TargetShipHp)
        ship.setHp(self.TargetShipHp)
        ship.setMaxSp(hullConfig['setMaxSp'][0])
        ship.setSp(hullConfig['setSp'][0])
        ship.setHullCondition(1 << 7)

        zoneId = oceanGrid.getZoneFromXYZ(self.TargetShipPos)
        oceanGrid.generateChildWithRequired(ship, zoneId)
        ship.setPos(oceanGrid, *self.TargetShipPos)
        ship.setHpr(oceanGrid, self.TargetShipH, 0, 0)
        oceanGrid.addObjectToOceanGrid(ship)
        ship.sendCurrentPosition()
        ship.startPosHprBroadcast()

        # Idle isn't one of the states the ship's AI engages from, so it
        # just sits there and takes it...
        ship.b_setGameState('Idle', 0)

        self.tutorialTarget = ship
        self.tutorialTargetSunk = False
        self.acceptOnce(ship.uniqueName('shipSinking'), self.__tutorialTargetSinking)
        return ship

    def __tutorialTargetSinking(self, ship):
        if ship is not self.tutorialTarget:
            return

        self.tutorialTargetSunk = True
        self.notify.info('Tutorial target %d has been sunk' % ship.doId)

    def isTutorialTargetSunk(self):
        return self.tutorialTargetSunk

    def removeTutorialTarget(self):
        target = getattr(self, 'tutorialTarget', None)
        self.tutorialTarget = None
        self.tutorialTargetSunk = False
        if not target:
            return

        self.ignore(target.uniqueName('shipSinking'))
        if not target.isDeleted():
            target.requestDelete()

    def resetSailingToAuthoredPose(self):
        self.stopSailing()
        self.removeTutorialTarget()
        if self.tutorialAuthoredPos is None or self.tutorialAuthoredHpr is None:
            return False

        oceanGrid = self.tutorialOceanGrid
        if not oceanGrid:
            return False

        zoneId = oceanGrid.getZoneFromXYZ(self.tutorialAuthoredPos)
        self.setPos(oceanGrid, *self.tutorialAuthoredPos)
        self.setHpr(oceanGrid, *self.tutorialAuthoredHpr)
        if self.parentId != oceanGrid.doId or self.zoneId != zoneId:
            self.b_setLocation(oceanGrid.doId, zoneId)

        # the last crew member leaving puts the ship away, bring it back
        # to it's authored state for the next pirate's tutorial...
        authoredState = getattr(self, 'tutorialAuthoredState', None)
        if authoredState and self.getGameState()[0] != authoredState:
            self.b_setGameState(authoredState, 0)

        self.sendCurrentPosition()
        return True

    def delete(self):
        self.stopSailing()
        self.removeTutorialTarget()

        if self.tutorialStumpy:
            if (self.tutorialBuilder
                    and self.tutorialBuilder.objectList.get(self.tutorialStumpy.doId) is self.tutorialStumpy):
                self.tutorialBuilder.removeObject(self.tutorialStumpy)

            self.tutorialStumpy.requestDelete()
            self.tutorialStumpy = None

        if (self.tutorialBuilder
                and self.tutorialBuilder.objectList.get(self.doId) is self):
            self.tutorialBuilder.removeObject(self)

        self.tutorialBuilder = None
        self.tutorialOceanGrid = None
        DistributedShipAI.delete(self)
