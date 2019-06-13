from panda3d.core import *

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI

from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI


# give us some room so we don't allocate a interest context
# with the same context that of the client's interest handles...
GRID_INTEREST_CONTEXT_MIN = 10000
GRID_INTEREST_CONTEXT_MAX = 25000

# this constant defines the number of zones we want to get
# from the getConcentricZones function based on the client's current cell...
GRID_INTEREST_ZONES_COUNT = 3


class GridInterestHandle(object):

    def __init__(self, interestId, interestZone):
        self.interestId = interestId
        self.interestZone = interestZone


class GridInterestHandler(object):

    def __init__(self, air, parentObj, avatar):
        self.air = air
        self.parentObj = parentObj
        self.avatar = avatar

        self.contextAllocator = UniqueIdAllocator(GRID_INTEREST_CONTEXT_MIN, GRID_INTEREST_CONTEXT_MAX)
        self.interestHandles = []

    def GetPuppetConnectionChannel(self, doId):
        return doId + (1001 << 32)

    def getInterestHandleFromZoneId(self, zoneId):
        for interestHandle in self.interestHandles:
            if interestHandle.interestZone == zoneId:
                return interestHandle

        return None

    def hasInterestHandleByZoneId(self, zoneId):
        return self.getInterestHandleFromZoneId(zoneId) is not None

    def addInterestHandle(self, zoneId):
        if self.hasInterestHandleByZoneId(zoneId):
            return

        interestId = zoneId#self.contextAllocator.allocate()
        interestHandle = GridInterestHandle(interestId, zoneId)

        clientChannel = self.GetPuppetConnectionChannel(self.avatar.doId)
        self.air.clientAddInterest(clientChannel, interestHandle.interestId,
            self.parentObj.doId, interestHandle.interestZone)

        self.interestHandles.append(interestHandle)

    def removeInterestHandle(self, interestHandle):
        if interestHandle not in self.interestHandles:
            return

        clientChannel = self.GetPuppetConnectionChannel(self.avatar.doId)
        self.air.clientRemoveInterest(clientChannel, interestHandle.interestZone)

        #self.contextAllocator.free(interestHandle.interestId)
        self.interestHandles.remove(interestHandle)

    def handleLocationChanged(self, zoneId):
        previousZones = set([interestHandle.interestZone for interestHandle in self.interestHandles])
        newZones = set()
        for x in xrange(1, GRID_INTEREST_ZONES_COUNT + 1):
            newZones.update(self.parentObj.getConcentricZones(zoneId, x))

        # get the difference between the old zones and remove interest
        # to any zones we should no longer have interest in...
        oldZones = newZones.difference(previousZones)
        for zoneId in oldZones:
            interestHandle = self.getInterestHandleFromZoneId(zoneId)
            if not interestHandle:
                continue

            self.removeInterestHandle(interestHandle)

        #if not isinstance(self.parentObj, DistributedGAInteriorAI):
        #    parentObj = self.parentObj.getParentObj()
        #    parentObj.d_sendAutoInterest(self.avatar.doId, list(newZones))

        # add interest to the new zones we should now have interest in...
        for zoneId in newZones:
            self.addInterestHandle(zoneId)

    def clearInterestZones(self):
        clientChannel = self.GetPuppetConnectionChannel(self.avatar.doId)
        for interestHandle in self.interestHandles:
            self.air.clientRemoveInterest(clientChannel, interestHandle.interestZone)

        self.interestHandles = []

    def destroy(self):
        self.lastInterestId = 0
        self.interestHandles = []


class WorldGridManagerAI(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('WorldGridManagerAI')

    def __init__(self, air):
        self.air = air
        self.gridInterestHandlers = {}

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
