from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal
from otp.distributed import OtpDoGlobals
from direct.distributed.MsgTypes import *
from direct.distributed.PyDatagram import PyDatagram
from direct.fsm.FSM import FSM
from pirates.uberdog import InventoryInit


class InventoryFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('InventoryFSM')

    def __init__(self, manager, avatarId, callback):
        self.manager = manager
        self.avatarId = avatarId
        self.callback = callback

        FSM.__init__(self, 'InventoryFSM')

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterStart(self):
        self.manager.air.dbInterface.queryObject(
            self.manager.air.dbId,
            self.avatarId,
            self.__avatarQueryCallback,
            dclass=self.manager.air.dclassesByName['DistributedPlayerPirateUD'])

    def __avatarQueryCallback(self, dclass, fields):
        if not dclass and not fields:
            self.notify.warning(
                'Failed to query avatar %d for inventory!' % (self.avatarId))

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

        self.manager.air.dbInterface.createObject(
            self.manager.air.dbId,
            self.manager.air.dclassesByName['PirateInventoryUD'],
            fields=fields,
            callback=self.__inventoryCreatedCallback)

    def __inventoryCreatedCallback(self, inventoryId):
        if not inventoryId:
            self.notify.warning(
                'Failed to create inventory for avatar %d!' % (self.avatarId))

            return

        self.inventoryId = inventoryId

        fields = {
            'setInventoryId': (inventoryId,),
        }

        self.manager.air.dbInterface.updateObject(
            self.manager.air.dbId,
            self.avatarId,
            self.manager.air.dclassesByName['DistributedPlayerPirateUD'],
            fields,
            callback=self.__inventorySetCallback)

    def __inventorySetCallback(self, fields):
        if fields is not None:
            self.notify.warning('Failed to update inventory %d for avatar %d' %
                                (self.inventoryId, self.avatarId))

            return

        self.request('Load')

    def exitCreate(self):
        pass

    def enterLoad(self):
        self.manager.air.sendActivate(
            self.inventoryId,
            self.avatarId,
            OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT,
            dclass=self.manager.air.dclassesByName['PirateInventoryUD'])

        if self.callback:
            self.callback(self.inventoryId)

        del self.manager.avatar2fsm[self.avatarId]
        self.demand('Off')

    def exitLoad(self):
        pass


class DistributedInventoryManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedInventoryManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

        self.avatar2fsm = {}

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        self.air.netMessenger.accept('hasInventoryResponse', self,
                                     self.proccessCallbackResponse)
        self.air.netMessenger.accept('getInventoryResponse', self,
                                     self.proccessCallbackResponse)

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
        if avatarId in self.avatar2fsm:
            self.notify.warning(
                'Failed to initiate inventory for avatar %d, an operation is already running!'
                % (avatarId))

            return

        self.avatar2fsm[avatarId] = InventoryFSM(self, avatarId, callback)
        self.avatar2fsm[avatarId].request('Start')

    def proccessCallbackResponse(self, callback, *args, **kwargs):
        if callback and callable(callback):
            callback(*args, **kwargs)
            return

        self.notify.warning('No valid callback for a callback response!'
                            'What was the purpose of that?')
