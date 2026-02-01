from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal
from otp.distributed.MsgTypes import *
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

    def getAvatarClassName(self):
        return 'DistributedPlayerPirateUD'

    def getInventoryClassName(self):
        return 'PirateInventoryUD'

    def enterOff(self):
        pass

    def exitOff(Self):
        pass

    def enterStart(self):
        pass

    def exitStart(self):
        pass

    def cleanup(self, *args, **kwargs):
        del self.air.inventoryManager.avatar2fsm[self.avatarId]
        self.ignoreAll()
        self.demand('Off')

        if self.callback:
            self.callback(*args, **kwargs)


class QueryInventoryFSM(InventoryOperationFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('QueryInventoryFSM')

    def enterStart(self):
        self.air.dbInterface.queryObject(self.air.dbId,
            self.avatarId,
            self.avatarQueryCallback,
            dclass=self.air.dclassesByName[self.getAvatarClassName()])

    def avatarQueryCallback(self, dclass, fields):
        if not dclass and not fields:
            self.notify.warning('Failed to query avatar %d for inventory!' % self.avatarId)
            self.cleanup(0)
            return

        self.inventoryId, = fields.get('setInventoryId', (0,))
        self.cleanup(self.inventoryId)

    def exitStart(self):
        pass


class QueryShipInventoryFSM(QueryInventoryFSM):

    def getAvatarClassName(self):
        return 'PlayerShipUD'

    def getInventoryClassName(self):
        return 'DistributedInventoryUD'


class CreateInventoryFSM(InventoryOperationFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('CreateInventoryFSM')

    def enterStart(self):
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

        self.air.dbInterface.createObject(self.air.dbId,
            self.air.dclassesByName[self.getInventoryClassName()],
            fields=fields,
            callback=self.inventoryCreatedCallback)

    def inventoryCreatedCallback(self, inventoryId):
        self.inventoryId = inventoryId
        if not inventoryId:
            self.notify.warning('Failed to create inventory for avatar %d, '
                'inventory database creation failed!' % (self.avatarId))

            self.cleanup(0)
            return

        fields = {
            'setInventoryId': (inventoryId,),
        }

        self.air.dbInterface.updateObject(self.air.dbId,
            self.avatarId,
            self.air.dclassesByName[self.getAvatarClassName()],
            fields,
            callback=self.inventorySetCallback)

    def inventorySetCallback(self, fields):
        if fields is not None:
            self.notify.warning('Failed to update inventory %d for avatar %d, '
                'invalid database response!' % (self.inventoryId, self.avatarId))

            self.cleanup(0)
            return

        self.cleanup(self.inventoryId)

    def exitStart(self):
        pass


class CreateShipInventoryFSM(CreateInventoryFSM):

    def getAvatarClassName(self):
        return 'PlayerShipUD'

    def getInventoryClassName(self):
        return 'DistributedInventoryUD'


class ActivateInventoryFSM(InventoryOperationFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('ActivateInventoryFSM')

    def enterStart(self, inventoryId):
        if not inventoryId:
            self.notify.warning('Failed to activate inventory for avatar %d, '
                'no inventory found!' % self.avatarId)

            self.cleanup(0)
            return

        self.air.sendActivate(inventoryId,
            self.avatarId,
            OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT,
            dclass=self.air.dclassesByName[self.getInventoryClassName()])

        self.cleanup(inventoryId)

    def exitStart(self):
        pass


class ActivateShipInventoryFSM(ActivateInventoryFSM):

    def getAvatarClassName(self):
        return 'PlayerShipUD'

    def getInventoryClassName(self):
        return 'DistributedInventoryUD'

    def enterStart(self, parentId, inventoryId):
        if not parentId:
            self.notify.warning('Failed to activate inventory for avatar %d, '
                'invalid parent id specified' % self.avatarId)

            self.cleanup(0)
            return

        if not inventoryId:
            self.notify.warning('Failed to activate inventory for avatar %d, '
                'no inventory found!' % self.avatarId)

            self.cleanup(0)
            return

        self.air.sendActivate(inventoryId,
            parentId,
            OtpDoGlobals.OTP_ZONE_ID_MANAGEMENT,
            dclass=self.air.dclassesByName[self.getInventoryClassName()])

        self.cleanup(inventoryId)

    def exitStart(self):
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
        if inventory == None or inventory.doId == 0:
            return

        self.air.netMessenger.send('addInventory', [inventory])

    def removeInventory(self, inventory):
        if inventory == None or inventory.doId == 0:
            return

        self.air.netMessenger.send('removeInventory', [inventory])

    def getInventory(self, avatarId, callback):
        self.air.netMessenger.send('getInventory', [avatarId, callback])

    def runInventoryFSM(self, fsmtype, avatarId, *args, **kwargs):
        if avatarId in list(self.avatar2fsm.keys()):
            self.notify.debug('Failed to run inventory FSM for avatar %d, '
                'an inventory FSM is already running!' % avatarId)

            return

        callback = kwargs.pop('callback', None)

        self.avatar2fsm[avatarId] = fsmtype(self.air, avatarId, callback)
        self.avatar2fsm[avatarId].request('Start', *args, **kwargs)

    def queryInventory(self, avatarId, callback=None):

        def inventoryQueryCallback(inventoryId):
            if not inventoryId:
                self.runInventoryFSM(CreateInventoryFSM, avatarId, callback=callback)
            else:
                callback(inventoryId)

        self.runInventoryFSM(QueryInventoryFSM, avatarId, callback=inventoryQueryCallback)

    def activateInventory(self, avatarId, inventoryId, callback=None):
        self.runInventoryFSM(ActivateInventoryFSM, avatarId, inventoryId, callback=callback)

    def queryShipInventory(self, shipId, callback=None):
        self.runInventoryFSM(QueryShipInventoryFSM, shipId, callback=callback)

    def createShipInventory(self, shipId, callback=None):
        self.runInventoryFSM(CreateShipInventoryFSM, shipId, callback=callback)

    def activateShipInventory(self, avatarId, shipId, inventoryId, callback=None):
        self.runInventoryFSM(ActivateShipInventoryFSM, shipId, avatarId, inventoryId, callback=callback)

    def proccessCallbackResponse(self, callback, *args, **kwargs):
        if callback and callable(callback):
            callback(*args, **kwargs)
            return

        self.notify.warning('No valid callback for a callback response!'
            'What was the purpose of that?')
