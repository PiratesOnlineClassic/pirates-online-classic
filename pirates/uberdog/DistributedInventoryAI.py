from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
from pirates.uberdog.UberDogGlobals import (InventoryCategory, InventoryId,
    InventoryType, getSkillCategory)


class DistributedInventoryAI(DistributedObjectAI, DistributedInventoryBase):
    """
    AI-side inventory implementation.
    
    Stores inventory data and synchronizes changes to the client via sendUpdate.
    Follows the b_set/d_set/set pattern matching the Base class design.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        DistributedInventoryBase.__init__(self, air)

    def generate(self):
        try:
            self.air.inventoryManager.addInventory(self)
        except Exception:
            self.notify.exception('Failed to register inventory with manager')
        DistributedObjectAI.generate(self)

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        # Stacks are set from the DB before announceGenerate fires, so mark
        # them as ready and check whether the inventory is fully initialised.
        self.stacksReady = True
        self.checkIsReady()

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
        # Local state update only.  The targeted network send is done by
        # d_setAccumulator; b_setAccumulator combines both.
        self.accumulators[accumulatorType] = quantity

    def d_setAccumulator(self, accumulatorType, quantity):
        self.sendUpdateToAvatarId(self.ownerId, 'accumulator', [accumulatorType, quantity])

    def b_setAccumulator(self, accumulatorType, quantity):
        self.setAccumulator(accumulatorType, quantity)
        self.d_setAccumulator(accumulatorType, quantity)

    def setStackLimit(self, stackType, limit):
        # Local state update only.  The targeted network send is done by
        # d_setStackLimit; b_setStackLimit combines both.
        self.stackLimits[stackType] = limit

    def d_setStackLimit(self, stackType, limit):
        self.sendUpdateToAvatarId(self.ownerId, 'stackLimit', [stackType, limit])

    def b_setStackLimit(self, stackType, limit):
        self.setStackLimit(stackType, limit)
        self.d_setStackLimit(stackType, limit)

    def setStackQuantity(self, stackType, quantity):
        # Apply the stack cap only when a positive limit exists.  A missing
        # limit defaults to 0, which would otherwise silently zero every stack
        # that has no explicit limit configured.
        limit = self.getStackLimit(stackType)
        if limit > 0:
            quantity = min(quantity, limit)
        self.stacks[stackType] = quantity
        # Keep stacksInCategory in sync so getStacksInCategory / getWeapons
        # etc. return current values after individual stack changes.
        categoryId = InventoryId.getCategory(stackType)
        if categoryId:
            self.stacksInCategory.setdefault(categoryId, {})[stackType] = quantity

    def d_setStackQuantity(self, stackType, quantity):
        self.sendUpdateToAvatarId(self.ownerId, 'stack', [stackType, quantity])

    def b_setStackQuantity(self, stackType, quantity):
        self.setStackQuantity(stackType, quantity)
        self.d_setStackQuantity(stackType, quantity)

    def setStacksInCategory(self, stackType, quantity):
        category = InventoryId.getCategory(stackType)
        # Merge into the existing category dict rather than replacing it, so
        # other stacks in the same category are not lost.
        self.stacksInCategory.setdefault(category, {})[stackType] = quantity
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
        stored = self.getStackQuantity(stackType)
        return limit > (stored + amount)

    def d_setTemporaryInventory(self, temporaryInventory):
        if self.ownerId:
            self.sendUpdateToAvatarId(self.ownerId, 'setTemporaryInventory', [temporaryInventory])

    def d_setTemporaryStack(self, stackType, amount):
        if self.ownerId:
            self.sendUpdateToAvatarId(self.ownerId, 'setTemporaryStack', [stackType, amount])

    def sendMaxHp(self, limit, avId):
        pass

    def sendMaxMojo(self, limit, avId):
        pass

    def d_requestInventoryComplete(self):
        if self.ownerId:
            self.sendUpdateToAvatarId(self.ownerId, 'requestInventoryComplete', [])

    def populateInventory(self):
        self.d_requestInventoryComplete()

    def processCallbackResponse(self, callback, *args, **kwargs):
        """Safely invoke a callback delivered via netMessenger.

        This wraps the callback invocation with error handling and
        accepts any callable. If the callback is not callable, a
        warning is logged.
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

    def delete(self):
        try:
            self.air.inventoryManager.removeInventory(self)
        except Exception:
            self.notify.exception('Failed to unregister inventory from manager')
        DistributedObjectAI.delete(self)
        DistributedInventoryBase.delete(self)
