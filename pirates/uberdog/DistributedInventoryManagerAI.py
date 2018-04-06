from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType

class DistributedInventoryManagerAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryManagerAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

        self.inventories = {}
        self.inventoryTasks = {}

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
        avatarId = self.air.getAvatarIdFromSender()

        if not avatarId:
            return

        def queryResponse(dclass, fields):
            if not dclass or not fields:
                self.notify.warning('Failed to query avatar %d!' % avatarId)
                return

            inventoryId, = fields.get('setInventoryId', (0,))

            if not inventoryId:
                self.notify.warning('Invalid inventory found for avatar %d!' % avatarId)
                return

            self.__sendInventory(avatarId, inventoryId)

        self.air.dbInterface.queryObject(self.air.dbId, avatarId, callback=queryResponse, dclass=\
            self.air.dclassesByName['DistributedPlayerPirateAI'])

    def __waitForInventory(self, avatarId, inventoryId, task):
        inventory = self.inventories.get(inventoryId)

        if not inventory:
            return task.cont

        self.__sendInventory(avatarId, inventory.doId)
        return task.done

    def __cleanupInventory(self, avatarId, inventoryId):
        if avatarId in self.inventoryTasks:
            taskMgr.remove(self.inventoryTasks[avatarId])
            del self.inventoryTasks[avatarId]

        inventory = self.inventories.get(inventoryId)

        if not inventory:
            return

        self.removeInventory(inventory.doId)

    def __sendInventory(self, avatarId, inventoryId):
        inventory = self.inventories.get(inventoryId)

        self.acceptOnce('distObjDelete-%d' % (avatarId), lambda: self.__cleanupInventory(
            avatarId, inventoryId))

        if not inventory:
            if avatarId in self.inventoryTasks:
                self.notify.debug('Cannot retrieve inventory avatar %d, already trying to get inventory!' % (
                    avatarId))

                return

            self.inventoryTasks[avatarId] = taskMgr.doMethodLater(1.0, self.__waitForInventory, 'waitForInventory-%d-%s' % (
                avatarId, id(self)), appendTask=True, extraArgs=[avatarId, inventoryId])

            return

        inventory.d_requestInventoryComplete()
