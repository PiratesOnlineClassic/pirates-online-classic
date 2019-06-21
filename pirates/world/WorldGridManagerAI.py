from panda3d.core import *

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI

from pirates.ship.DistributedShipAI import DistributedShipAI


class GridInterestHandle(object):

    def __init__(self, context, zoneId):
        self.context = context
        self.zoneId = zoneId


class GridInterestHandler(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('GridInterestHandler')

    def __init__(self, air, parentObj, avatar):
        self.air = air
        self.parentObj = parentObj
        self.avatar = avatar

        self.interestHandles = []
        self.oldZoneId = 0

    def getInterestHandleFromZoneId(self, zoneId):
        for interestHandle in list(self.interestHandles):
            if interestHandle.zoneId == zoneId:
                return interestHandle

        return None

    def hasInterestHandleByZoneId(self, zoneId):
        return self.getInterestHandleFromZoneId(zoneId) is not None

    def addInterestHandle(self, newZoneId):
        if self.hasInterestHandleByZoneId(newZoneId):
            return

        interestHandle = GridInterestHandle(newZoneId, newZoneId)
        self.interestHandles.append(interestHandle)

        clientChannel = self.avatar.GetPuppetConnectionChannel(self.avatar.doId)
        self.air.clientAddInterest(clientChannel, interestHandle.context, self.parentObj.doId, interestHandle.zoneId, False)

    def removeInterestHandle(self, interestHandle):
        if interestHandle not in self.interestHandles:
            return

        clientChannel = self.avatar.GetPuppetConnectionChannel(self.avatar.doId)
        self.air.clientRemoveInterest(clientChannel, interestHandle.context, False)
        self.interestHandles.remove(interestHandle)

    def handleLocationChanged(self, zoneId):
        if zoneId == self.oldZoneId:
            return

        previousZones = set([interestHandle.zoneId for interestHandle in self.interestHandles])
        newZones = set()

        # determine how many zones we want to see ahead of us based on
        # the cartesian grid radius set by constants for the parent object
        for x in xrange(1, self.parentObj.gridRadius + 1):
            newZones.update(self.parentObj.getConcentricZones(zoneId, x))

        oldConcentricZones = previousZones.difference(newZones)
        for oldZoneId in oldConcentricZones:
            interestHandle = self.getInterestHandleFromZoneId(oldZoneId)
            if not interestHandle:
                continue

            self.removeInterestHandle(interestHandle)

        newConcentricZones = newZones.difference(previousZones)
        for newZoneId in newConcentricZones:
            self.addInterestHandle(newZoneId)

        previousZones.clear()
        newZones.clear()

        oldConcentricZones.clear()
        newConcentricZones.clear()

        self.oldZoneId = zoneId

    def clearInterestZones(self):
        for interestHandle in list(self.interestHandles):
            self.removeInterestHandle(interestHandle)

        self.interestHandles = []

    def destroy(self):
        self.lastInterestId = 0
        self.interestHandles = []
        self.oldZoneId = 0


class WorldGridManagerAI(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('WorldGridManagerAI')

    def __init__(self, air):
        self.air = air
        self.gridInterestHandlers = {}

    def handleLocationChanged(self, parentObj, avatar, zoneId):
        if isinstance(parentObj, DistributedShipAI):
            shipParentObj = parentObj
            parentObj = shipParentObj.getParentObj()
            zoneId = parentObj.getZoneFromXYZ(shipParentObj.getPos())
        else:
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
