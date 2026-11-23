from direct.directnotify import DirectNotifyGlobal

from pirates.ship.DistributedShipAI import DistributedShipAI


class TutorialShipAI(DistributedShipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TutorialShipAI')

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

    def resetSailingToAuthoredPose(self):
        self.stopSailing()
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

        self.sendCurrentPosition()
        return True

    def delete(self):
        self.stopSailing()

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
