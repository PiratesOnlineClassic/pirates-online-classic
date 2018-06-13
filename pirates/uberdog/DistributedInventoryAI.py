from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedInventoryAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.ownerId = 0
        self.categoryLimits = []
        self.categoriesAndDoIds = []
        self.accumulators = []
        self.stackLimits = []
        self.stacks = []

    def generate(self):
        self.air.inventoryManager.addInventory(self)

        DistributedObjectAI.generate(self)

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        self.air.netMessenger.accept('b_setAccumulators', self, self.b_setAccumulators)
        self.air.netMessenger.accept('b_setAccumulator', self, self.b_setAccumulator)
        self.air.netMessenger.accept('b_setStackLimits', self, self.b_setStackLimits)
        self.air.netMessenger.accept('b_setStacks', self, self.b_setStacks)
        self.air.netMessenger.accept('b_setStack', self, self.b_setStack)
        self.air.netMessenger.accept('b_setOwnerId', self, self.b_setOwnerId)
        self.air.netMessenger.accept('getAccumulators', self, self.sendAccumulators)
        self.air.netMessenger.accept('getAccumulator', self, self.sendAccumulator)
        self.air.netMessenger.accept('getStackLimit', self, self.sendStackLimit)
        self.air.netMessenger.accept('getStack', self, self.sendStack)
        self.air.netMessenger.accept('getOwnerId', self, self.sendOwnerId)

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def d_setOwnerId(self, ownerId):
        self.sendUpdate('setOwnerId', [ownerId])

    def b_setOwnerId(self, ownerId):
        self.setOwnerId(ownerId)
        self.d_setOwnerId(ownerId)

    def getOwnerId(self):
        return self.ownerId

    def sendOwnerId(self, callback):
        self.air.netMessenger.send('getOwnerIdResponse', [callback, self.ownerId])

    def setCategoryLimits(self, categoryLimits):
        self.categoryLimits = categoryLimits

    def d_setCategoryLimits(self, categoryLimits):
        self.sendUpdate('setCategoryLimits', [categoryLimits])

    def b_setCategoryLimits(self, categoryLimits):
        self.setCategoryLimits(categoryLimits)
        self.d_setCategoryLimits(categoryLimits)

    def getCategoryLimits(self):
        return self.categoryLimits

    def setDoIds(self, categoriesAndDoIds):
        self.categoriesAndDoIds = categoriesAndDoIds

    def d_setDoIds(self, categoriesAndDoIds):
        self.sendUpdate('setDoIds', [categoriesAndDoIds])

    def b_setDoIds(self, categoriesAndDoIds):
        self.setDoIds(categoriesAndDoIds)
        self.d_setDoIds(categoriesAndDoIds)

    def getDoIds(self):
        return self.categoriesAndDoIds

    def setAccumulators(self, accumulators):
        self.accumulators = accumulators

    def d_setAccumulators(self, accumulators):
        self.sendUpdate('setAccumulators', [accumulators])

    def b_setAccumulators(self, accumulators):
        self.setAccumulators(accumulators)
        self.d_setAccumulators(accumulators)

    def getAccumulators(self):
        return self.accumulators

    def sendAccumulators(self, callback):
        self.air.netMessenger.send('getAccumulatorsResponse', [callback, self.accumulators])

    def setStackLimits(self, stackLimits):
        self.stackLimits = stackLimits

    def d_setStackLimits(self, stackLimits):
        self.sendUpdate('setStackLimits', [stackLimits])

    def b_setStackLimits(self, stackLimits):
        self.setStackLimits(stackLimits)
        self.d_setStackLimits(stackLimits)

    def getStackLimits(self):
        return self.stackLimits

    def setStacks(self, stacks):
        self.stacks = stacks

    def d_setStacks(self, stacks):
        self.sendUpdate('setStacks', [stacks])

    def b_setStacks(self, stacks):
        self.setStacks(stacks)
        self.d_setStacks(stacks)

    def getStacks(self):
        return self.stacks

    def getCategoryLimit(self, category):
        for categoryLimit in self.categoryLimits:

            if categoryLimit[0] == category:
                return categoryLimit[1]

        return 0

    def setCategoryAndDoId(self, category, doId):
        categoryDoIds = self.getCategoryDoIds(category)
        categoryLimit = self.getCategoryLimit(category)

        if len(categoryDoIds) >= categoryLimit:
            self.notify.warning('Cannot add category %d, number of categories and doIds exceed the maximum allowed %d!' % (
                category, categoryLimit))

            return

        self.categoriesAndDoIds.append([category, doId])

    def d_setCategoryAndDoId(self, category, doId):
        self.d_setDoIds(self.categoriesAndDoIds)

    def b_setCategoryAndDoId(self, category, doId):
        self.setCategoryAndDoId(category, doId)
        self.d_setCategoryAndDoId(category, doId)

    def getCategoryDoIds(self, category):
        categoryDoIds = []

        for categoryAndDoId in self.categoriesAndDoIds:

            if categoryAndDoId[0] == category:
                categoryDoIds.append(categoryAndDoId[1])

        return categoryDoIds

    def setAccumulator(self, accumulatorType, quantity):
        accumulator = self.getAccumulator(accumulatorType)

        if accumulator:
            self.accumulators[self.accumulators.index(accumulator)] = [accumulatorType, quantity]
        else:
            self.accumulators.append([accumulatorType, quantity])

        self.d_setAccumulators(self.accumulators)

    def d_setAccumulator(self, accumulatorType, quantity):
        self.sendUpdateToAvatarId(self.ownerId, 'accumulator', [accumulatorType, quantity])

    def b_setAccumulator(self, accumulatorType, quantity):
        self.setAccumulator(accumulatorType, quantity)
        self.d_setAccumulator(accumulatorType, quantity)

    def getAccumulator(self, accumulatorType):
        for accumulator in self.accumulators:

            if accumulator[0] == accumulatorType:
                return accumulator

        return None

    def sendAccumulator(self, accumulatorType, callback):
        self.air.netMessenger.send('getAccumulatorResponse', [callback, self.getAccumulator(accumulatorType)])

    def setStackLimit(self, stackType, limit):
        stackLimit = self.getStackLimit(stackType)

        if stackLimit:
            self.stackLimits[self.stackLimits.index(stackLimit)] = [stackType, limit]
        else:
            self.stackLimits.append([stackType, limit])

        self.d_setStackLimits(self.stackLimits)

    def d_setStackLimit(self, stackType, limit):
        self.sendUpdateToAvatarId(self.ownerId, 'stackLimit', [stackType, limit])

    def b_setStackLimit(self, stackType, limit):
        self.setStackLimit(stackType, limit)
        self.d_setStackLimit(stackType, limit)

    def getStackLimit(self, stackType):
        for stackLimit in self.stackLimits:

            if stackLimit[0] == stackType:
                return stackLimit

        return None

    def hasStackSpace(self, stackType, amount=0):
        limit = self.getStackLimit(stackType)
        _, stored = self.getStack(stackType) or (stackType, 0)
        return limit > (stored + amount)

    def sendStackLimit(self, stackType, callback):
        self.air.netMessenger.send('getStackLimitResponse', [callback, self.getStackLimit(stackType)])

    def setStack(self, stackType, quantity):
        stack = self.getStack(stackType)

        if stack:
            self.stacks[self.stacks.index(stack)] = [stackType, quantity]
        else:
            self.stacks.append([stackType, quantity])

        self.d_setStacks(self.stacks)

    def d_setStack(self, stackType, quantity):
        self.sendUpdateToAvatarId(self.ownerId, 'stack', [stackType, quantity])

    def b_setStack(self, stackType, quantity):
        self.setStack(stackType, quantity)
        self.d_setStack(stackType, quantity)

    def getStack(self, stackType):
        for stack in self.stacks:

            if stack[0] == stackType:
                return stack

        return None

    def sendStack(self, stackType, callback):
        self.air.netMessenger.send('getStackResponse', [callback, self.getStack(stackType)])

    def getItem(self, itemGetter, itemType):
        item = itemGetter(itemType)

        if not item:
            return 0

        return item[1]

    def d_setTemporaryInventory(self, temporaryInventory):
        self.sendUpdateToAvatarId(self.ownerId, 'setTemporaryInventory', [temporaryInventory])

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

    def delete(self):
        self.air.inventoryManager.removeInventory(self)

        DistributedObjectAI.delete(self)

    def getTonics(self):
        return dict(((tonicId, self.getStack(tonicId)[1]) for tonicId in InventoryType.Potions))

    def proccessCallbackResponse(self, callback, *args, **kwargs):
        if callback and callable(callback):
            callback(*args, **kwargs)
            return

        self.notify.warning('No valid callback for a callback response!'
            'What was the purpose of that?')
