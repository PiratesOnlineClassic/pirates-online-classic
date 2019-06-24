from panda3d.core import *

from direct.directnotify import DirectNotifyGlobal
from direct.showbase import PythonUtil
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

        self.pendingCallbackContexts = []
        self.pendingCallback = None

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

    def hasPendingContext(self, context):
        return context in self.pendingCallbackContexts

    def _callbackInterestContext(self):
        assert(len(self.pendingCallbackContexts) == 0)
        assert(self.pendingCallback is not None)
        self.pendingCallback()

        self.pendingCallbackContexts = []
        self.pendingCallback = None

    def handleInterestContextDone(self, context):
        if context not in self.pendingCallbackContexts:
            return

        self.pendingCallbackContexts.remove(context)
        if len(self.pendingCallbackContexts) == 0:
            self._callbackInterestContext()

    def handleLocationChanged(self, zoneId, callback):
        previousZones = set([interestHandle.zoneId for interestHandle in self.interestHandles])
        newZones = set([zoneId])

        # determine how many zones we want to see ahead of us based on
        # the cartesian grid radius set by constants for the parent object
        for x in xrange(1, self.parentObj.gridRadius + 1):
            concentricZones = set(self.parentObj.getConcentricZones(zoneId, x))
            newZones.update(concentricZones)

        oldConcentricZones = previousZones.difference(newZones)
        for oldZoneId in oldConcentricZones:
            interestHandle = self.getInterestHandleFromZoneId(oldZoneId)
            if not interestHandle:
                continue

            self.removeInterestHandle(interestHandle)

        newConcentricZones = newZones.difference(previousZones)
        if callback is not None:
            self.pendingCallbackContexts = list(newConcentricZones)
            self.pendingCallback = PythonUtil.DelayedFunctor(callback, 'interest-context-callback-%d' % self.avatar.doId, 0.2)

        for newZoneId in newConcentricZones:
            self.addInterestHandle(newZoneId)

        previousZones.clear()
        newZones.clear()

        oldConcentricZones.clear()
        newConcentricZones.clear()

    def clearInterestZones(self):
        for interestHandle in list(self.interestHandles):
            self.removeInterestHandle(interestHandle)

        self.interestHandles = []

    def destroy(self):
        self.lastInterestId = 0
        self.interestHandles = []
        self.oldZoneId = 0

        self.pendingCallback = None
        self.pendingCallbackContexts = []


class WorldGridManagerAI(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('WorldGridManagerAI')

    def __init__(self, air):
        self.air = air
        self.gridInterestHandlers = {}

    def handleInterestContextDone(self, avatarId, context):
        """
        Handles interest done callback from the ClientAgent via the msgtype CLIENTAGENT_DONE_INTEREST_RESP
        we wait for the ClientAgent to tell us that all of our interest zone events have been handled,
        then call the callback specified by the caller
        """

        gridInterests = self.gridInterestHandlers.get(avatarId)
        if not gridInterests:
            return

        for parentId in gridInterests:
            gridInterestHandler = gridInterests.get(parentId)
            assert(gridInterestHandler is not None)

            # find an interest handler with the pending context and handle it,
            # assuming we only have a single grid interest handler with that pending context...
            if gridInterestHandler.hasPendingContext(context):
                gridInterestHandler.handleInterestContextDone(context)
                break

    def handleLocationChanged(self, parentObj, avatar, zoneId, callback=None):
        """
        Updates the avatar's interest sets for a particular parent cartesian object
        based on the center of the radius which is subject to the zoneId
        """

        assert(parentObj is not None)
        assert(avatar is not None)

        if not isinstance(parentObj, DistributedCartesianGridAI):
            return

        if not parentObj.isValidZone(zoneId):
            self.notify.warning('Failed to handle avatar %d grid location change, '
                'invalid zone %d for parent with doId %d!' % (avatar.doId, zoneId, parentObj.doId))

            return

        gridInterests = self.gridInterestHandlers.setdefault(avatar.doId, {})
        gridInterestHandler = gridInterests.get(parentObj.doId)
        if not gridInterestHandler:
            gridInterestHandler = GridInterestHandler(self.air, parentObj, avatar)
            gridInterests[parentObj.doId] = gridInterestHandler

        assert(gridInterestHandler is not None)
        gridInterestHandler.handleLocationChanged(zoneId, callback)

    def clearAvatarInterest(self, parentObj, avatar):
        """
        Clears an avatar's interest set which is specific to a parent cartesian object
        """

        assert(parentObj is not None)
        assert(avatar is not None)

        gridInterests = self.gridInterestHandlers.get(avatar.doId)
        if not gridInterests:
            return

        gridInterestHandler = gridInterests.pop(parentObj.doId, None)
        if not gridInterestHandler:
            return

        gridInterestHandler.clearInterestZones()
        gridInterestHandler.destroy()
        del gridInterestHandler

    def clearAvatarInterests(self, avatar):
        """
        Clears all of the avatar's current grid interests
        """

        assert(avatar is not None)

        gridInterests = self.gridInterestHandlers.pop(avatar.doId, None)
        if not gridInterests:
            return

        for parentId in gridInterests:
            self.clearAvatarInterest(avatar, parentId)
