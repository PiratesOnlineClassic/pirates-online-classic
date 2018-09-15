from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal
from otp.distributed import OtpDoGlobals
from direct.distributed.MsgTypes import *
from direct.distributed.PyDatagram import PyDatagram
from direct.fsm.FSM import FSM
from pirates.uberdog import InventoryInit


class InventoryOperationFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('InventoryOperationFSM')

    def __init__(self, air, avatarId, callback=None):
        FSM.__init__(self, self.__class__.__name__)

        self.air = air
        self.avatarId = avatarId
        self.callback = callback

    def enterOff(self):
        pass

    def exitOff(Self):
        pass

    def cleanup(self, *args, **kwargs):
        del self.air.inventoryManager.avatar2fsm[self.avatarId]
        self.ignoreAll()
        self.demand('Off')

        if self.callback:
            self.callback(*args, **kwargs)

class InventoryQueryFSM(InventoryOperationFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('InventoryQueryFSM')

    def enterStart(self):

        def avatarQueryCallback(dclass, fields):
            if not dclass and not fields:
                self.notify.warning('Failed to query avatar %d for inventory!' % self.avatarId)
                self.cleanup(None)
                return

            inventoryId, = fields.get('setInventoryId', (0,))
            self.cleanup(inventoryId)

        self.air.dbInterface.queryObject(self.air.dbId,
            self.avatarId,
            avatarQueryCallback,
            dclass=self.air.dclassesByName['DistributedPlayerPirateUD'])

    def exitStart(self):
        pass

class InventoryCreateFSM(InventoryOperationFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('InventoryCreateFSM')

    def enterStart(self):
        categoryLimits = []
        for key, limit in InventoryInit.CategoryLimits.iteritems():
            categoryLimits.append((key, limit))

        accumulators = []
        for key, limit in InventoryInit.AccumulatorLimits.iteritems():
            accumulators.append((key, 0))

        stackLimits = []
        for key, limit in InventoryInit.StackLimits.iteritems():
            stackLimits.append((key, limit))

        startStacks = []
        for key, amount in InventoryInit.StartingStacks.iteritems():
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

        self.air.dbInterface.createObject(self.air.dbId,
            self.air.dclassesByName['PirateInventoryUD'],
            fields=fields,
            callback=self.__inventoryCreatedCallback)

    def __inventoryCreatedCallback(self, inventoryId):
        if not inventoryId:
            self.notify.warning('Failed to create inventory for avatar %d!' % (
                self.avatarId))

            self.cleanup(None)
            return

        self.inventoryId = inventoryId

        fields = {
            'setInventoryId': (inventoryId,),
        }

        self.air.dbInterface.updateObject(self.air.dbId,
            self.avatarId,
            self.air.dclassesByName['DistributedPlayerPirateUD'],
            fields,
            callback=self.__inventorySetCallback)

    def __inventorySetCallback(self, fields):
        if fields is not None:
            self.notify.warning('Failed to update inventory %d for avatar %d' % (
                self.inventoryId, self.avatarId))

            self.cleanup(None)
            return

        self.cleanup(self.inventoryId)

    def exitStart(self):
        pass

class InventoryLoadFSM(InventoryOperationFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('InventoryLoadFSM')

    def enterStart(self, inventoryId):
        self.air.sendActivate(inventoryId,
            self.avatarId,
            OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT,
            dclass=self.air.dclassesByName['PirateInventoryUD'])

        self.callback(inventoryId)

    def exitLoad(self):
        pass

class DistributedInventoryManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

        self.avatar2fsm = {}

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        self.air.netMessenger.accept('hasInventoryResponse', self, self.proccessCallbackResponse)
        self.air.netMessenger.accept('getInventoryResponse', self, self.proccessCallbackResponse)

    def runInventoryFSM(self, fsmtype, avatarId, *args, **kwargs):
        if avatarId in self.avatar2fsm:
            self.notify.debug('Failed to run inventory FSM for avatar %d, '
                'an FSM already running!' % avatarId)

            return

        callback = kwargs.pop('callback', None)

        self.avatar2fsm[avatarId] = fsmtype(self.air, avatarId, callback)
        self.avatar2fsm[avatarId].request('Start', *args, **kwargs)

    def hasInventory(self, inventoryId, callback):
        self.air.netMessenger.send('hasInventory', [inventoryId, callback])

    def addInventory(self, inventory):
        if inventory and inventory.doId:
            self.air.netMessenger.send('addInventory', [inventory])

    def removeInventory(self, inventory):
        if inventory and inventory.doId:
            self.air.netMessenger.send('removeInventory', [inventory])

    def getInventory(self, avatarId, callback):
        self.air.netMessenger.send('getInventory', [avatarId, callback])

    def initiateInventory(self, avatarId, callback=None):

        def inventoryLoadedCallback(inventoryId):
            if not inventoryId:
                self.notify.warning('Failed to load inventory for avatar %d' % avatarId)
                callback(0)
            else:
                callback(inventoryId)

        def inventoryCreatedCallback(inventoryId):
            if not inventory:
                self.notify.warning('Failed to create inventory for avatar %d' % avatarId)
                callback(0)
            else:
                self.runInventoryFSM(InventoryLoadFSM, avatarId,
                    inventoryId, callback=inventoryLoadedCallback)

        def inventoryQueryCallback(inventoryId):
            if not inventoryId:
                self.runInventoryFSM(InventoryCreateFSM, avatarId,
                    callback=inventoryCreatedCallback)
            else:
                self.runInventoryFSM(InventoryLoadFSM, avatarId,
                    inventoryId, callback=inventoryLoadedCallback)

        self.runInventoryFSM(InventoryQueryFSM, avatarId,
            callback=inventoryQueryCallback)

    def proccessCallbackResponse(self, callback, *args, **kwargs):
        if callback and callable(callback):
            callback(*args, **kwargs)
            return

        self.notify.warning('No valid callback for a callback response!'
            'What was the purpose of that?')
