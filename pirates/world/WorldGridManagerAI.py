from panda3d.core import *

from direct.directnotify import DirectNotifyGlobal
from direct.showbase import PythonUtil
from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI


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

        self.pendingCallbackContexts = set()
        self.pendingCallback = None

        self.interestHandles = set()
        self.oldZoneId = 0

    def getInterestHandleFromZoneId(self, zoneId):
        """
        Gets an interest handle by it's zoneId from the list
        """

        for interestHandle in list(self.interestHandles):
            if interestHandle.zoneId == zoneId:
                return interestHandle

        return None

    def hasInterestHandleByZoneId(self, zoneId):
        """
        Returns True if there is an interest handle by zoneId in the list otherwise False
        """

        return self.getInterestHandleFromZoneId(zoneId) is not None

    def addInterestHandle(self, newZoneId):
        """
        Adds a client agent specific interest handle via the CLIENTAGENT_ADD_INTEREST message,
        this event does not exist on the client and the client does not know about this interest handle...
        """

        if self.hasInterestHandleByZoneId(newZoneId):
            return

        interestHandle = GridInterestHandle(newZoneId, newZoneId)
        self.interestHandles.add(interestHandle)

        clientChannel = self.avatar.GetPuppetConnectionChannel(self.avatar.doId)
        self.air.clientAddInterest(clientChannel, interestHandle.context, self.parentObj.doId, interestHandle.zoneId, False)

    def removeInterestHandle(self, interestHandle):
        """
        Removes a client agent specific interest handle via the CLIENTAGENT_REMOVE_INTEREST message
        """

        if interestHandle not in self.interestHandles:
            return

        clientChannel = self.avatar.GetPuppetConnectionChannel(self.avatar.doId)
        self.air.clientRemoveInterest(clientChannel, interestHandle.context, False)
        self.interestHandles.remove(interestHandle)

    def removeInterestHandleByZoneId(self, zoneId):
        """
        Removes an interest handle using it's zoneId which it's indexed as
        """

        interestHandle = self.getInterestHandleFromZoneId(zoneId)
        if not interestHandle:
            self.notify.warning('Cannot remove interest handle by zoneId: %d, '
                'interest handle does not exist!' % zoneId)

            return

        self.removeInterestHandle(interestHandle)

    def hasPendingContext(self, context):
        """
        Returns True if there is a pending interest handle callback by context else False
        """

        return context in self.pendingCallbackContexts

    def _callbackInterestContext(self):
        """
        Calls back the interest handle(s) callback when the client agent has told us
        that all of our interest handles have been added and the objects sent for generate on the client
        """

        assert(len(self.pendingCallbackContexts) == 0)
        assert(self.pendingCallback is not None)
        self.pendingCallback.finish()

        self.pendingCallbackContexts = set()
        self.pendingCallback = None

    def handleInterestContextDone(self, context):
        """
        Handles the interest context done event for an interest handle via the CLIENTAGENT_DONE_INTEREST_RESP message
        """

        if context not in self.pendingCallbackContexts:
            return

        self.pendingCallbackContexts.remove(context)
        if len(self.pendingCallbackContexts) == 0:
            self._callbackInterestContext()

    def _setInterestContextDoneCallback(self, contexts, callback):
        assert(len(contexts) > 0)
        assert(callback is not None)

        self.pendingCallbackContexts.update(contexts)
        self.pendingCallback = PythonUtil.FrameDelayedCall('interest-context-callback-%d' % self.avatar.doId, callback)

    def handleLocationChanged(self, zoneId, callback):
        """
        Adds interest to a new set of concentric zones based on the zoneId provided which would be
        the center of the circle and the radius being the cartesian grid parent's radius value.
        We add interest only to cells we didn't see before and only remove interest from cells we cannot see now...
        """

        previousZones = set([interestHandle.zoneId for interestHandle in list(self.interestHandles)])
        newZones = set([zoneId])

        # determine how many zones we want to see ahead of us based on
        # the cartesian grid radius set by constants for the parent object
        for x in range(1, self.parentObj.gridRadius + 1):
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
            self._setInterestContextDoneCallback(newConcentricZones, callback)

        for newZoneId in newConcentricZones:
            self.addInterestHandle(newZoneId)

        previousZones.clear()
        newZones.clear()

        oldConcentricZones.clear()
        newConcentricZones.clear()

    def clearInterestZones(self):
        """
        Clears all of our interest handles that we currently have opened, this will
        also clear any pending interest callbacks...
        """

        for interestHandle in list(self.interestHandles):
            self.removeInterestHandle(interestHandle)

        self.interestHandles.clear()

        self.pendingCallback = None
        self.pendingCallbackContexts.clear()

    def destroy(self):
        """
        Destroys the interest handle and it's values
        """

        self.lastInterestId = 0
        self.interestHandles.clear()
        self.oldZoneId = 0

        self.pendingCallback = None
        self.pendingCallbackContexts.clear()


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

        for parentId in dict(gridInterests):
            gridInterestHandler = gridInterests.get(parentId)
            assert(gridInterestHandler is not None)

            # find an interest handler with the pending context and handle it,
            # assuming we only have a single grid interest handler with that pending context...
            if gridInterestHandler.hasPendingContext(context):
                gridInterestHandler.handleInterestContextDone(context)
                break

    def hasInterestHandleByZoneId(self, parentObj, avatar, zoneId):
        """
        Returns True if we have a set of interests for the avatar under the parentObj otherwise False
        """

        assert(parentObj is not None)
        assert(avatar is not None)

        gridInterests = self.gridInterestHandlers.get(avatar.doId)
        if not gridInterests:
            return False

        gridInterestHandler = gridInterests.get(parentObj.doId)
        if not gridInterestHandler:
            return False

        return gridInterestHandler.hasInterestHandleByZoneId(zoneId)

    def addInterestHandle(self, parentObj, avatar, newZoneId):
        """
        Explicitly calls addInterestHandle function on the grid interest handler
        """

        assert(parentObj is not None)
        assert(avatar is not None)

        gridInterests = self.gridInterestHandlers.get(avatar.doId)
        if not gridInterests:
            return

        gridInterestHandler = gridInterests.get(parentObj.doId)
        if not gridInterestHandler:
            return

        gridInterestHandler.addInterestHandle(newZones)

    def removeInterestHandle(self, parentObj, avatar, interestHandle):
        """
        Explicitly calls removeInterestHandle function on the grid interest handler
        associated with the provided cartesian grid parentObj
        """

        assert(parentObj is not None)
        assert(avatar is not None)
        assert(interestHandle is not None)

        gridInterests = self.gridInterestHandlers.get(avatar.doId)
        if not gridInterests:
            return

        gridInterestHandler = gridInterests.get(parentObj.doId)
        if not gridInterestHandler:
            return

        gridInterestHandler.removeInterestHandle(interestHandle)

    def removeInterestHandleByZoneId(self, parentObj, avatar, zoneId):
        """
        Explicitly calls removeInterestHandle function on the grid interest handler
        associated with the provided cartesian grid parentObj
        """

        assert(parentObj is not None)
        assert(avatar is not None)

        gridInterests = self.gridInterestHandlers.get(avatar.doId)
        if not gridInterests:
            return

        gridInterestHandler = gridInterests.get(parentObj.doId)
        if not gridInterestHandler:
            return

        gridInterestHandler.removeInterestHandleByZoneId(zoneId)

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

        gridInterests = self.gridInterestHandlers.get(avatar.doId)
        if not gridInterests:
            return

        for parentId in dict(gridInterests):
            parentObj = self.air.doId2do.get(parentId)
            assert(parentObj is not None)
            self.clearAvatarInterest(parentObj, avatar)

        assert(avatar.doId in self.gridInterestHandlers)
        del self.gridInterestHandlers[avatar.doId]
