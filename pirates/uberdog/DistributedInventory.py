from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObject import DistributedObject
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType


class DistributedInventory(DistributedInventoryBase, DistributedObject):
    notify = directNotify.newCategory('Inventory')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        DistributedInventoryBase.__init__(self, cr)

    def announceGenerate(self):
        self.invInterest = self.addInterest(2, self.uniqueName('inventory'))
        self.cr.inventoryManager.sendRequestInventory()
        DistributedObject.announceGenerate(self)

    def disable(self):
        if self.invInterest:
            self.removeInterest(self.invInterest)

        DistributedObject.disable(self)
        DistributedInventoryBase.delete(self)

    def delete(self):
        DistributedObject.delete(self)

    def stackLimit(self, stackType, limit):
        if stackType == InventoryType.Hp:
            if stackType in self.stackLimits:
                oldHp = self.stackLimits[stackType]
            else:
                oldHp = limit

        self.stackLimits[stackType] = limit
        messenger.send('inventoryLimit-%s-%s' % (self.doId,stackType), [limit])
        messenger.send('inventoryChanged-%s' % self.doId)
        if stackType == InventoryType.Hp:
            base.localAvatar.setMaxHp(limit)
            base.localAvatar.toonUp(limit - oldHp)
            avId = base.localAvatar.getDoId()
            self.sendUpdate('sendMaxHp', [limit, avId])

        if stackType == InventoryType.Mojo:
            base.localAvatar.setMaxMojo(limit)
            avId = base.localAvatar.getDoId()
            self.sendUpdate('sendMaxMojo', [limit, avId])

    def stack(self, stackType, quantity):
        self.stacks[stackType] = quantity
        categoryId = InventoryId.getCategory(stackType)
        category = self.stacksInCategory.setdefault(categoryId, {})
        if quantity:
            category[stackType] = quantity
        else:
            category.pop(stackType, None)

        messenger.send('inventoryQuantity-%s-%s' % (self.doId, stackType), [quantity])
        messenger.send('inventoryChanged-%s' % self.doId)
        if stackType == InventoryType.Vitae_Level or stackType == InventoryType.Vitae_Cost or stackType == InventoryType.Vitae_Left:
            localAvatar.guiMgr.gameGui.updateVitae(self.getStackQuantity(InventoryType.Vitae_Level), self.getStackQuantity(InventoryType.Vitae_Cost),
                self.getStackQuantity(InventoryType.Vitae_Left))

        if stackType == InventoryType.DollToken or stackType == InventoryType.WandToken or stackType == InventoryType.DaggerToken or \
            stackType == InventoryType.GrenadeToken:

            if self.ownerId == localAvatar.getDoId():
                localAvatar.gotWeaponReward(stackType)

    def requestInventoryComplete(self):
        self.stacksReady = True
        self.checkIsReady()

    def accumulator(self, accumulatorType, quantity):
        self.accumulators[accumulatorType] = quantity
        messenger.send('inventoryAccumulator-%s-%s' % (self.doId, accumulatorType), [quantity])
        messenger.send('inventoryChanged-%s' % self.doId)

    def sendRequestDestroy(self, category, doId, context):
        pass
