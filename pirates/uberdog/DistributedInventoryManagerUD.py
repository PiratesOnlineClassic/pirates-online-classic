from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.MsgTypes import *
from direct.distributed.PyDatagram import PyDatagram
from direct.fsm.FSM import FSM

from otp.distributed import OtpDoGlobals

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


class InventoryFSM(InventoryOperationFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('InventoryFSM')

    def enterStart(self):
        self.air.dbInterface.queryObject(self.air.dbId,
            self.avatarId,
            self.avatarQueryCallback,
            dclass=self.air.dclassesByName['DistributedPlayerPirateUD'])

    def avatarQueryCallback(self, dclass, fields):
        if not dclass and not fields:
            self.notify.warning('Failed to query avatar %d for inventory!' % (
                self.avatarId))

            self.cleanup(0)
            return

        self.inventoryId, = fields.get('setInventoryId', (0,))
        if not self.inventoryId:
            self.request('Create')
        else:
            self.request('Load')

    def exitStart(self):
        pass

    def enterCreate(self):
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
            callback=self.inventoryCreatedCallback)

    def inventoryCreatedCallback(self, inventoryId):
        self.inventoryId = inventoryId
        if not inventoryId:
            self.notify.warning('Failed to create inventory for avatar %d!' % (
                self.avatarId))

            self.cleanup(0)
            return

        fields = {
            'setInventoryId': (inventoryId,),
        }

        self.air.dbInterface.updateObject(self.air.dbId,
            self.avatarId,
            self.air.dclassesByName['DistributedPlayerPirateUD'],
            fields,
            callback=self.inventorySetCallback)

    def inventorySetCallback(self, fields):
        if fields is not None:
            self.notify.warning('Failed to update inventory %d for avatar %d' % (
                self.inventoryId, self.avatarId))

            self.cleanup(0)
            return

        self.request('Load')

    def exitCreate(self):
        pass

    def enterLoad(self):
        self.air.sendActivate(self.inventoryId,
            self.avatarId,
            OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT,
            dclass=self.air.dclassesByName['PirateInventoryUD'])

        self.cleanup(self.inventoryId)

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

    def runInventoryFSM(self, fsmtype, avatarId, *args, **kwargs):
        if avatarId in self.avatar2fsm:
            self.notify.debug('Failed to run inventory FSM for avatar %d, '
                'an FSM already running!' % avatarId)

            return

        callback = kwargs.pop('callback', None)

        self.avatar2fsm[avatarId] = fsmtype(self.air, avatarId, callback)
        self.avatar2fsm[avatarId].request('Start', *args, **kwargs)

    def initiateInventory(self, avatarId, callback=None):
        self.runInventoryFSM(InventoryFSM, avatarId, callback=callback)

    def proccessCallbackResponse(self, callback, *args, **kwargs):
        if callback and callable(callback):
            callback(*args, **kwargs)
            return

        self.notify.warning('No valid callback for a callback response!'
            'What was the purpose of that?')
