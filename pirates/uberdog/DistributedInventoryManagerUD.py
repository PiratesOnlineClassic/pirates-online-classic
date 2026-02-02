from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal
from otp.distributed.MsgTypes import *
from direct.distributed.PyDatagram import PyDatagram
from direct.fsm.FSM import FSM
from direct.task import Task

from otp.distributed import OtpDoGlobals

from pirates.uberdog import InventoryInit


class InventoryOperationFSM(FSM):
    """
    Base FSM for inventory database operations.
    
    Provides guaranteed cleanup, timeout handling, and safe callback invocation.
    All subclasses should call _finish() to complete operations.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('InventoryOperationFSM')
    TIMEOUT_SECONDS = 30.0

    def __init__(self, manager, avatarId, callback=None):
        FSM.__init__(self, self.__class__.__name__)

        self.manager = manager
        self.air = manager.air
        self.avatarId = avatarId
        self.callback = callback
        self._finished = False
        self._timeoutTaskName = 'InventoryFSM-timeout-%d-%d' % (id(self), avatarId)

    def getAvatarClassName(self):
        return 'DistributedPlayerPirateUD'

    def getInventoryClassName(self):
        return 'PirateInventoryUD'

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterStart(self):
        # Start timeout timer
        taskMgr.doMethodLater(
            self.TIMEOUT_SECONDS,
            self._onTimeout,
            self._timeoutTaskName
        )

    def exitStart(self):
        pass

    def _onTimeout(self, task):
        """Called when operation times out."""
        if not self._finished:
            self.notify.warning('Operation timed out for entity %d' % self.avatarId)
            self._finish(0)
        return Task.done

    def _finish(self, *args, **kwargs):
        """
        Guaranteed cleanup path. Always call this to complete the operation.
        Replaces the old cleanup() method with proper guards.
        """
        if self._finished:
            return
        self._finished = True

        # Cancel timeout task
        taskMgr.remove(self._timeoutTaskName)

        # Clean up any event listeners
        self.ignoreAll()

        # Unregister from manager safely
        if hasattr(self, 'manager') and self.manager:
            self.manager.avatar2fsm.pop(self.avatarId, None)

        # Transition to Off state
        try:
            self.demand('Off')
        except Exception:
            pass

        # Invoke callback safely
        if self.callback:
            try:
                self.callback(*args, **kwargs)
            except Exception:
                self.notify.exception('Callback failed for entity %d' % self.avatarId)

    def cleanup(self, *args, **kwargs):
        """Legacy method - redirects to _finish for backwards compatibility."""
        self._finish(*args, **kwargs)


class QueryInventoryFSM(InventoryOperationFSM):
    """Queries the database for an avatar's inventory ID."""
    notify = DirectNotifyGlobal.directNotify.newCategory('QueryInventoryFSM')

    def enterStart(self):
        InventoryOperationFSM.enterStart(self)
        try:
            self.air.dbInterface.queryObject(self.air.dbId,
                self.avatarId,
                self.avatarQueryCallback,
                dclass=self.air.dclassesByName[self.getAvatarClassName()])
        except Exception:
            self.notify.exception('Failed to query avatar %d' % self.avatarId)
            self._finish(0)

    def avatarQueryCallback(self, dclass, fields):
        if self._finished:
            return
            
        if not dclass and not fields:
            self.notify.warning('Failed to query avatar %d for inventory!' % self.avatarId)
            self._finish(0)
            return

        inventoryId = 0
        try:
            inventoryId, = fields.get('setInventoryId', (0,))
        except (ValueError, TypeError):
            inventoryId = 0
        self._finish(inventoryId)

    def exitStart(self):
        pass


class QueryShipInventoryFSM(QueryInventoryFSM):

    def getAvatarClassName(self):
        return 'PlayerShipUD'

    def getInventoryClassName(self):
        return 'DistributedInventoryUD'


class CreateInventoryFSM(InventoryOperationFSM):
    """Creates a new inventory in the database and links it to an avatar."""
    notify = DirectNotifyGlobal.directNotify.newCategory('CreateInventoryFSM')

    def __init__(self, manager, avatarId, callback=None):
        InventoryOperationFSM.__init__(self, manager, avatarId, callback)
        self.inventoryId = 0

    def enterStart(self):
        InventoryOperationFSM.enterStart(self)
        
        categoryLimits = []
        for key, limit in InventoryInit.CategoryLimits.items():
            categoryLimits.append((key, limit))

        accumulators = []
        for key, limit in InventoryInit.AccumulatorLimits.items():
            accumulators.append((key, 0))

        stackLimits = []
        for key, limit in InventoryInit.StackLimits.items():
            stackLimits.append((key, limit))

        startStacks = []
        for key, amount in InventoryInit.StartingStacks.items():
            startStacks.append((key, amount))

        fields = {
            'setOwnerId': (self.avatarId,),
            'setInventoryVersion': (InventoryInit.UberDogRevision,),
            'setCategoryLimits': (categoryLimits,),
            'setDoIds': ([],),
            'setAccumulators': (accumulators,),
            'setStackLimits': (stackLimits,),
            'setStacks': (startStacks,)
        }

        try:
            self.air.dbInterface.createObject(self.air.dbId,
                self.air.dclassesByName[self.getInventoryClassName()],
                fields=fields,
                callback=self.inventoryCreatedCallback)
        except Exception:
            self.notify.exception('Failed to create inventory for %d' % self.avatarId)
            self._finish(0)

    def inventoryCreatedCallback(self, inventoryId):
        if self._finished:
            return
            
        self.inventoryId = inventoryId
        if not inventoryId:
            self.notify.warning('Failed to create inventory for avatar %d, '
                'inventory database creation failed!' % (self.avatarId))
            self._finish(0)
            return

        fields = {
            'setInventoryId': (inventoryId,),
        }

        try:
            self.air.dbInterface.updateObject(self.air.dbId,
                self.avatarId,
                self.air.dclassesByName[self.getAvatarClassName()],
                fields,
                callback=self.inventorySetCallback)
        except Exception:
            self.notify.exception('Failed to update avatar %d with inventory %d' % (self.avatarId, inventoryId))
            self._finish(inventoryId)

    def inventorySetCallback(self, fields):
        if self._finished:
            return
            
        if fields is not None:
            self.notify.warning('Failed to update inventory %d for avatar %d, '
                'invalid database response!' % (self.inventoryId, self.avatarId))
            self._finish(0)
            return

        self._finish(self.inventoryId)

    def exitStart(self):
        pass


class CreateShipInventoryFSM(CreateInventoryFSM):

    def getAvatarClassName(self):
        return 'PlayerShipUD'

    def getInventoryClassName(self):
        return 'DistributedInventoryUD'


class ActivateInventoryFSM(InventoryOperationFSM):
    """Activates an inventory as a distributed object."""
    notify = DirectNotifyGlobal.directNotify.newCategory('ActivateInventoryFSM')

    def enterStart(self, inventoryId):
        InventoryOperationFSM.enterStart(self)
        
        if not inventoryId:
            self.notify.warning('Failed to activate inventory for avatar %d, '
                'no inventory found!' % self.avatarId)
            self._finish(0)
            return

        try:
            self.air.sendActivate(inventoryId,
                self.avatarId,
                OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT,
                dclass=self.air.dclassesByName[self.getInventoryClassName()])
            self._finish(inventoryId)
        except Exception:
            self.notify.exception('Failed to activate inventory %d' % inventoryId)
            self._finish(0)

    def exitStart(self):
        pass


class ActivateShipInventoryFSM(ActivateInventoryFSM):
    """Activates a ship's inventory as a distributed object."""

    def getAvatarClassName(self):
        return 'PlayerShipUD'

    def getInventoryClassName(self):
        return 'DistributedInventoryUD'

    def enterStart(self, parentId, inventoryId):
        # Start timeout timer
        taskMgr.doMethodLater(
            self.TIMEOUT_SECONDS,
            self._onTimeout,
            self._timeoutTaskName
        )
        
        if not parentId:
            self.notify.warning('Failed to activate inventory for avatar %d, '
                'invalid parent id specified' % self.avatarId)
            self._finish(0)
            return

        if not inventoryId:
            self.notify.warning('Failed to activate inventory for avatar %d, '
                'no inventory found!' % self.avatarId)
            self._finish(0)
            return

        try:
            self.air.sendActivate(inventoryId,
                parentId,
                OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT,
                dclass=self.air.dclassesByName[self.getInventoryClassName()])
            self._finish(inventoryId)
        except Exception:
            self.notify.exception('Failed to activate ship inventory %d' % inventoryId)
            self._finish(0)

    def exitStart(self):
        pass


class DistributedInventoryManagerUD(DistributedObjectGlobalUD):
    """
    UberDog-side inventory manager.
    
    Manages inventory database operations using FSMs for async handling.
    Provides a clean interface for querying, creating, and activating inventories.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        self.avatar2fsm = {}

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.air.netMessenger.accept('hasInventoryResponse', self, self.processCallbackResponse)
        self.air.netMessenger.accept('getInventoryResponse', self, self.processCallbackResponse)

    def delete(self):
        # Clean up any pending FSMs
        for fsm in list(self.avatar2fsm.values()):
            try:
                fsm._finish(0)
            except Exception:
                pass
        self.avatar2fsm.clear()
        DistributedObjectGlobalUD.delete(self)

    def hasPendingOperation(self, entityId):
        """Check if an operation is already running for this entity."""
        return entityId in self.avatar2fsm

    def hasInventory(self, inventoryId, callback):
        self.air.netMessenger.send('hasInventory', [inventoryId, callback])

    def addInventory(self, inventory):
        if inventory is None or inventory.doId == 0:
            return
        self.air.netMessenger.send('addInventory', [inventory])

    def removeInventory(self, inventory):
        if inventory is None or inventory.doId == 0:
            return
        self.air.netMessenger.send('removeInventory', [inventory])

    def getInventory(self, avatarId, callback):
        self.air.netMessenger.send('getInventory', [avatarId, callback])

    def runInventoryFSM(self, fsmtype, avatarId, *args, **kwargs):
        if avatarId in self.avatar2fsm:
            self.notify.debug('Failed to run inventory FSM for avatar %d, '
                'an inventory FSM is already running!' % avatarId)
            # Call the callback with failure to avoid leaving caller hanging
            callback = kwargs.get('callback')
            if callback:
                try:
                    callback(0)
                except Exception:
                    pass
            return False

        callback = kwargs.pop('callback', None)
        fsm = fsmtype(self, avatarId, callback)
        self.avatar2fsm[avatarId] = fsm
        fsm.request('Start', *args, **kwargs)
        return True

    def queryInventory(self, avatarId, callback=None):
        def inventoryQueryCallback(inventoryId):
            if not inventoryId:
                self.runInventoryFSM(CreateInventoryFSM, avatarId, callback=callback)
            elif callback:
                try:
                    callback(inventoryId)
                except Exception:
                    self.notify.exception('Callback failed in queryInventory')

        self.runInventoryFSM(QueryInventoryFSM, avatarId, callback=inventoryQueryCallback)

    def activateInventory(self, avatarId, inventoryId, callback=None):
        self.runInventoryFSM(ActivateInventoryFSM, avatarId, inventoryId, callback=callback)

    def queryShipInventory(self, shipId, callback=None):
        self.runInventoryFSM(QueryShipInventoryFSM, shipId, callback=callback)

    def createShipInventory(self, shipId, callback=None):
        self.runInventoryFSM(CreateShipInventoryFSM, shipId, callback=callback)

    def activateShipInventory(self, avatarId, shipId, inventoryId, callback=None):
        self.runInventoryFSM(ActivateShipInventoryFSM, shipId, avatarId, inventoryId, callback=callback)

    def processCallbackResponse(self, callback, *args, **kwargs):
        """Safely invoke callbacks delivered via netMessenger.

        This prevents exceptions in callbacks from bubbling into the
        messenger task system and logs any errors encountered.
        """
        if callable(callback):
            try:
                callback(*args, **kwargs)
            except Exception:
                try:
                    self.notify.exception('Exception while running callback')
                except Exception:
                    pass
            return

        self.notify.warning('No valid callback for a callback response! What was the purpose of that?')
