from panda3d.core import *

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI

# this constant defines the number of zones we want to get
# from the getConcentricZones function based on the client's current cell...
GRID_INTEREST_ZONES_COUNT = 3


class GridInterestHandle(object):

    def __init__(self, interestId, interestZone):
        self.interestId = interestId
        self.interestZone = interestZone


class GridInterestHandler(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('GridInterestHandler')

    def __init__(self, air, parentObj, avatar):
        self.air = air
        self.parentObj = parentObj
        self.avatar = avatar

        self.interestHandles = []
        self.pendingInterestHandles = []

        self.oldZoneId = 0

    def getInterestHandleFromZoneId(self, zoneId):
        for interestHandle in self.interestHandles:
            if interestHandle.interestZone == zoneId:
                return interestHandle

        return None

    def hasInterestHandleByZoneId(self, zoneId):
        return self.getInterestHandleFromZoneId(zoneId) is not None

    def addInterestHandle(self, context, newZoneId):
        if self.hasInterestHandleByZoneId(newZoneId):
            return

        interestHandle = GridInterestHandle(context, newZoneId)
        self.interestHandles.append(interestHandle)

    def removeInterestHandle(self, interestHandle):
        if interestHandle not in self.interestHandles:
            return

        clientChannel = self.avatar.GetPuppetConnectionChannel(self.avatar.doId)
        self.air.clientRemoveInterest(clientChannel, interestHandle.interestId)
        self.interestHandles.remove(interestHandle)

    def handleGotInterestContext(self, zoneId, context):
        if zoneId not in self.pendingInterestHandles:
            self.notify.debug('Failed to handle interest context %d for zone %d, '
                'zone is not a pending interest handle!' % (context, zoneId))

            return

        self.addInterestHandle(context, zoneId)
        self.pendingInterestHandles.remove(zoneId)

    def handleLocationChanged(self, zoneId):
        if zoneId == self.oldZoneId:
            return

        # we don't want to force the client to have to tell us about all of
        # the interest requests, the client will handle adding it's own interest
        # for the pending zones, and we will handle removal of interest...
        self.pendingInterestHandles = []
        previousZones = set([interestHandle.interestZone for interestHandle in self.interestHandles])
        newZones = set()
        for x in xrange(1, GRID_INTEREST_ZONES_COUNT + 1):
            newZones.update(self.parentObj.getConcentricZones(zoneId, x))

        oldConcentricZones = previousZones.difference(newZones)
        for oldZoneId in oldConcentricZones:
            interestHandle = self.getInterestHandleFromZoneId(oldZoneId)
            if not interestHandle:
                continue

            self.removeInterestHandle(interestHandle)

        newConcentricZones = newZones.difference(previousZones)
        self.pendingInterestHandles = list(newConcentricZones)
        for newZoneId in newConcentricZones:
            self.avatar.d_addZoneInterest(self.parentObj.doId, newZoneId)

        previousZones.clear()
        newZones.clear()

        oldConcentricZones.clear()
        newConcentricZones.clear()

        self.oldZoneId = zoneId

    def clearInterestZones(self):
        clientChannel = self.avatar.GetPuppetConnectionChannel(self.avatar.doId)
        for interestHandle in self.interestHandles:
            self.air.clientRemoveInterest(clientChannel, interestHandle.interestZone)

        self.interestHandles = []
        self.pendingInterestHandles = []

    def destroy(self):
        self.lastInterestId = 0
        self.interestHandles = []
        self.pendingInterestHandles = []
        self.oldZoneId = 0


class WorldGridManagerAI(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('WorldGridManagerAI')

    def __init__(self, air):
        self.air = air
        self.gridInterestHandlers = {}

    def addZoneInterestDone(self, avatar, zoneId, context):
        gridHandler = self.gridInterestHandlers.get(avatar.doId)
        if not gridHandler:
            return

        gridHandler.handleGotInterestContext(zoneId, context)

    def handleLocationChanged(self, parentObj, avatar, zoneId):
        if not isinstance(parentObj, DistributedCartesianGridAI):
            return

        if not parentObj.isValidZone(zoneId):
            self.notify.warning('Failed to handle avatar %d grid location change, '
                'invalid zone %d for parent with doId %d!' % (avatar.doId, zoneId, parentObj.doId))

            return

        gridHandler = self.gridInterestHandlers.get(avatar.doId)
        if gridHandler is not None:
            if gridHandler.parentObj != parentObj:
                self.clearAvatarInterests(avatar)
                gridHandler = None

        if not gridHandler:
            gridHandler = GridInterestHandler(self.air, parentObj, avatar)
            self.gridInterestHandlers[avatar.doId] = gridHandler

        gridHandler.handleLocationChanged(zoneId)

    def clearAvatarInterests(self, avatar):
        gridHandler = self.gridInterestHandlers.pop(avatar.doId, None)
        if not gridHandler:
            return

        gridHandler.clearInterestZones()
        gridHandler.destroy()
        del gridHandler
