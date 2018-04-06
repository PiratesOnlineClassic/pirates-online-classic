from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType

class DistributedInventoryManagerAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryManagerAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

        self.inventories = {}

    def hasInventory(self, inventoryId):
        return inventoryId in self.inventories

    def addInventory(self, inventory):
        if self.hasInventory(inventory.doId):
            self.notify.warning('Tried to add an already existing inventory %d!' % inventory.doId)
            return

        self.inventories[inventory.doId] = inventory

    def removeInventory(self, inventory):
        if not self.hasInventory(inventory.doId):
            self.notify.warning('Tried to remove a non-existant inventory %d!' % inventory.doId)
            return

        del self.inventories[inventory.doId]
        inventory.requestDelete()

    def getInventory(self, avatarId):
        for inventory in self.inventories.values():

            if inventory.getOwnerId() == avatarId:
                return inventory

        return None

    def requestInventory(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        def queryResponse(dclass, fields):
            if not dclass or not fields:
                self.notify.warning('Failed to query avatar %d!' % avatar.doId)
                return

            inventoryId, = fields.get('setInventoryId', (0,))

            if not inventoryId:
                self.notify.warning('Invalid inventory found for avatar %d!' % avatar.doId)
                return

            self.__sendInventory(avatar, self.inventories.get(inventoryId))

        self.air.dbInterface.queryObject(self.air.dbId, avatar.doId, callback=queryResponse, dclass=\
            self.air.dclassesByName['DistributedPlayerPirateAI'])

    def __sendInventory(self, avatar, inventory):
        if not inventory:
            self.notify.warning('Failed to retrieve inventory for avatar %d!' % avatar.doId)
            return

        #inventory.b_setStackLimit(InventoryType.Hp, avatar.getMaxHp())
        #inventory.b_setStackLimit(InventoryType.Mojo, avatar.getMaxMojo())

        #for index in xrange(len(inventory.accumulators)):
        #    inventory.d_setAccumulator(*inventory.accumulators[index])

        #for index in xrange(len(inventory.stackLimits)):
        #    inventory.d_setStackLimit(*inventory.stackLimits[index])

        #for index in xrange(len(inventory.stacks)):
        #    inventory.d_setStack(*inventory.stacks[index])

        inventory.d_requestInventoryComplete()
