from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
from pirates.uberdog.UberDogGlobals import (InventoryCategory, InventoryId,
    InventoryType, getSkillCategory)

class DistributedInventoryAI(DistributedObjectAI, DistributedInventoryBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        DistributedInventoryBase.__init__(self, air)

    def generate(self):
        self.air.inventoryManager.addInventory(self)
        DistributedObjectAI.generate(self)

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

    def d_setCategoryLimits(self, categoriesAndLimits):
        self.sendUpdate('setCategoryLimits', [categoriesAndLimits])

    def b_setCategoryLimits(self, categoriesAndLimits):
        self.setCategoryLimits(categoriesAndLimits)
        self.d_setCategoryLimits(self.getCategoryLimits())

    def getCategoryLimits(self):
        return [[category, limit] for category, limit in list(self.categoryLimits.items())]

    def d_setDoIds(self, categoriesAndDoIds):
        self.sendUpdate('setDoIds', [categoriesAndDoIds])

    def b_setDoIds(self, categoriesAndDoIds):
        self.setDoIds(categoriesAndDoIds)
        self.d_setDoIds(self.getDoIds())

    def getDoIds(self):
        return [[category, doId] for doId, category in list(self.doIds.items())]

    def d_setAccumulators(self, accumulatorTypesAndQuantities):
        self.sendUpdate('setAccumulators', [accumulatorTypesAndQuantities])

    def b_setAccumulators(self, accumulatorTypesAndQuantities):
        self.setAccumulators(accumulatorTypesAndQuantities)
        self.d_setAccumulators(self.getAccumulators())

    def getAccumulators(self):
        return [[accumulatorType, quantity] for accumulatorType, quantity in list(self.accumulators.items())]

    def d_setStackLimits(self, stackTypesAndLimits):
        self.sendUpdate('setStackLimits', [stackTypesAndLimits])

    def b_setStackLimits(self, stackTypesAndLimits):
        self.setStackLimits(stackTypesAndLimits)
        self.d_setStackLimits(self.getStackLimits())

    def getStackLimits(self):
        return [[stackType, limit] for stackType, limit in list(self.stackLimits.items())]

    def d_setStacks(self, stackTypesAndQuantities):
        self.sendUpdate('setStacks', [stackTypesAndQuantities])

    def b_setStacks(self, stackTypesAndQuantities):
        self.setStacks(stackTypesAndQuantities)
        self.d_setStacks(self.getStacks())

    def getStacks(self):
        return [[stackType, quantity] for stackType, quantity in list(self.stacks.items())]

    def setAccumulator(self, accumulatorType, quantity):
        self.accumulators[accumulatorType] = quantity
        self.d_setAccumulators(self.getAccumulators())

    def d_setAccumulator(self, accumulatorType, quantity):
        self.sendUpdateToAvatarId(self.ownerId, 'accumulator', [accumulatorType, quantity])

    def b_setAccumulator(self, accumulatorType, quantity):
        self.setAccumulator(accumulatorType, quantity)
        self.d_setAccumulator(accumulatorType, quantity)

    def setStackLimit(self, stackType, limit):
        self.stackLimits[stackType] = limit
        self.d_setStackLimits(self.getStackLimits())

    def d_setStackLimit(self, stackType, limit):
        self.sendUpdateToAvatarId(self.ownerId, 'stackLimit', [stackType, limit])

    def b_setStackLimit(self, stackType, limit):
        self.setStackLimit(stackType, limit)
        self.d_setStackLimit(stackType, limit)

    def setStackQuantity(self, stackType, quantity):
        self.stacks[stackType] = min(quantity, self.getStackLimit(stackType))
        self.d_setStacks(self.getStacks())

    def d_setStackQuantity(self, stackType, quantity):
        self.sendUpdateToAvatarId(self.ownerId, 'stack', [stackType, quantity])

    def b_setStackQuantity(self, stackType, quantity):
        self.setStackQuantity(stackType, quantity)
        self.d_setStackQuantity(stackType, quantity)

    def setStacksInCategory(self, stackType, quantity):
        category = InventoryId.getCategory(stackType)
        self.stacksInCategory[category] = {stackType: quantity}
        self.setStackQuantity(stackType, quantity)

    def d_setStacksInCategory(self, stackType, quantity):
        self.d_setStacks(self.getStacks())

    def b_setStacksInCategory(self, stackType, quantity):
        self.setStacksInCategory(stackType, quantity)
        self.d_setStacksInCategory(stackType, quantity)

    def setDoIdListCategory(self, category, doIdList):
        self.doIdsInCategory[category] = list(doIdList)
        for doId in doIdList:
            self.doIds[doId] = category

        for doId in list(self.doIds.keys()):
            if self.doIds[doId] == category and doId not in doIdList:
                del self.doIds[doId]

    def d_setDoIdListCategory(self, category, doIdList):
        self.d_setDoIds(self.getDoIds())

    def b_setDoIdListCategory(self, category, doIdList):
        self.setDoIdListCategory(category, doIdList)
        self.d_setDoIdListCategory(category, doIdList)

    def setCategoryLimit(self, category, limit):
        self.categoryLimits[category] = limit

    def d_setCategoryLimit(self, category, limit):
        self.d_setCategoryLimits(self.getCategoryLimits())

    def b_setCategoryLimit(self, category, limit):
        self.setCategoryLimit(category, limit)
        self.d_setCategoryLimit(category, limit)

    def hasStackSpace(self, stackType, amount=0):
        limit = self.getStackLimit(stackType)
        _, stored = self.getStackQuantity(stackType) or (stackType, 0)
        return limit > (stored + amount)

    def d_setTemporaryInventory(self, temporaryInventory):
        self.sendUpdateToAvatarId(self.ownerId, 'setTemporaryInventory', [temporaryInventory])

    def d_setTemporaryStack(self, stackType, amount):
        self.sendUpdateToAvatarId(self.ownerId, 'setTemporaryStack', [stackType, amount])

    def sendMaxHp(self, limit, avId):
        pass

    def sendMaxMojo(self, limit, avId):
        pass

    def d_requestInventoryComplete(self):
        self.sendUpdateToAvatarId(self.ownerId, 'requestInventoryComplete', [])

    def populateInventory(self):
        self.d_requestInventoryComplete()

    def proccessCallbackResponse(self, callback, *args, **kwargs):
        if callback and callable(callback):
            callback(*args, **kwargs)
            return

        self.notify.warning('No valid callback for a callback response!'
            'What was the purpose of that?')

    def delete(self):
        self.air.inventoryManager.removeInventory(self)
        DistributedObjectAI.delete(self)
        DistributedInventoryBase.delete(self)
