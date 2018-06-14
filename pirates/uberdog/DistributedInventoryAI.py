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

    def setCategoryLimits(self, categoriesAndLimits):
        self.categoryLimits = {category: limit for category, limit in categoriesAndLimits}

    def d_setCategoryLimits(self, categoriesAndLimits):
        self.sendUpdate('setCategoryLimits', [categoriesAndLimits])

    def b_setCategoryLimits(self, categoriesAndLimits):
        self.setCategoryLimits(categoriesAndLimits)
        self.d_setCategoryLimits(self.getCategoryLimits())

    def getCategoryLimits(self):
        return [[category, limit] for category, limit in self.categoryLimits.items()]

    def setDoIds(self, categoriesAndDoIds):
        self.doIds = {doId: category for category, doId in categoriesAndDoIds}

        for category, doId in categoriesAndDoIds:
            category = self.doIdsInCategory.setdefault(category, [])

            # TODO FIXME: why is the shipId list sent more times than once????
            if doId in category:
                continue

            category.append(doId)

    def d_setDoIds(self, categoriesAndDoIds):
        self.sendUpdate('setDoIds', [categoriesAndDoIds])

    def b_setDoIds(self, categoriesAndDoIds):
        self.setDoIds(categoriesAndDoIds)
        self.d_setDoIds(self.getDoIds())

    def getDoIds(self):
        return [[category, doId] for doId, category in self.doIds.items()]

    def setAccumulators(self, accumulatorTypesAndQuantities):
        for accumulatorType, quantity in accumulatorTypesAndQuantities:
            self.accumulators[accumulatorType] = quantity

    def d_setAccumulators(self, accumulatorTypesAndQuantities):
        self.sendUpdate('setAccumulators', [accumulatorTypesAndQuantities])

    def b_setAccumulators(self, accumulatorTypesAndQuantities):
        self.setAccumulators(accumulatorTypesAndQuantities)
        self.d_setAccumulators(self.getAccumulators())

    def getAccumulators(self):
        return [[accumulatorType, quantity] for accumulatorType, quantity in self.accumulators.items()]

    def setStackLimits(self, stackTypesAndLimits):
        self.stackLimits = {stackType: limit for stackType, limit in stackTypesAndLimits}

    def d_setStackLimits(self, stackTypesAndLimits):
        self.sendUpdate('setStackLimits', [stackTypesAndLimits])

    def b_setStackLimits(self, stackTypesAndLimits):
        self.setStackLimits(stackTypesAndLimits)
        self.d_setStackLimits(self.getStackLimits())

    def getStackLimits(self):
        return [[stackType, limit] for stackType, limit in self.stackLimits.items()]

    def setStacks(self, stackTypesAndQuantities):
        self.stacks = {stackType: quantity for stackType, quantity in stackTypesAndQuantities}

        for stackType, quantity in stackTypesAndQuantities:
            category = InventoryId.getCategory(stackType)
            categoryList = self.stacksInCategory.setdefault(category, {})
            categoryList[stackType] = quantity

    def d_setStacks(self, stackTypesAndQuantities):
        self.sendUpdate('setStacks', [stackTypesAndQuantities])

    def b_setStacks(self, stackTypesAndQuantities):
        self.setStacks(stackTypesAndQuantities)
        self.d_setStacks(self.getStacks())

    def getStacks(self):
        return [[stackType, quantity] for stackType, quantity in self.stacks.items()]

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
        self.stacks[stackType] = quantity
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
        self.doIdsInCategory[category] = doIdList

        for doId in doIdList:
            self.doIds[doId] = category

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
        _, stored = self.getStack(stackType) or (stackType, 0)
        return limit > (stored + amount)

    def d_setTemporaryInventory(self, temporaryInventory):
        self.sendUpdateToAvatarId(self.ownerId, 'setTemporaryInventory', [temporaryInventory])

    def d_setTemporaryStack(self, stackType, amount):
        self.sendUpdateToAvatarId(self.ownerId, 'setTemporaryStack', [stackType, amount])

    def sendMaxHp(self, limit, avId):
        avatar = self.air.doId2do.get(self.ownerId)

        if not avatar:
            return

        avatar.b_setHp(avatar.getMaxHp(), 0)

    def sendMaxMojo(self, limit, avId):
        avatar = self.air.doId2do.get(self.ownerId)

        if not avatar:
            return

        avatar.b_setMojo(avatar.getMaxMojo())

    def d_requestInventoryComplete(self):
        self.sendUpdateToAvatarId(self.ownerId, 'requestInventoryComplete', [])

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
