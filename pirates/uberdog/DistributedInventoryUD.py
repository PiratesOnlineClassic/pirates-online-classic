
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class DistributedInventoryUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
        self.inventoryVersion = 0
        self.ownerId = 0
        self.categoryLimits = []
        self.doIds = []
        self.accumulators = []
        self.stackLimits = []
        self.stacks = []


    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setInventoryVersion(self, inventoryVersion):
        self.inventoryVersion = inventoryVersion

    def d_setInventoryVersion(self, inventoryVersion):
        self.sendUpdate('setInventoryVersion', [inventoryVersion])

    def b_setInventoryVersion(self, inventoryVersion):
        self.setInventoryVersion(inventoryVersion)
        self.d_setInventoryVersion(inventoryVersion)

    def getInventoryVersion(self):
        return self.inventoryVersion

    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def d_setOwnerId(self, ownerId):
        self.sendUpdate('setOwnerId', [ownerId])

    def b_setOwnerId(self, ownerId):
        self.setOwnerId(ownerId)
        self.d_setOwnerId(ownerId)

    def getOwnerId(self):
        return self.ownerId

    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setCategoryLimits(self, categoryLimits):
        self.categoryLimits = categoryLimits

    def d_setCategoryLimits(self, categoryLimits):
        self.sendUpdate('setCategoryLimits', [categoryLimits])

    def b_setCategoryLimits(self, categoryLimits):
        self.setCategoryLimits(categoryLimits)
        self.d_setCategoryLimits(categoryLimits)

    def getCategoryLimits(self):
        return self.categoryLimits

    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setDoIds(self, doIds):
        self.doIds = doIds

    def d_setDoIds(self, doIds):
        self.sendUpdate('setDoIds', [doIds])

    def b_setDoIds(self, doIds):
        self.setDoIds(doIds)
        self.d_setDoIds(doIds)

    def getDoIds(self):
        return self.doIds

    # accumulator(uint16, uint32)

    def accumulator(self, accumulator, todo_uint32_1):
        self.sendUpdate('accumulator', [accumulator, todo_uint32_1])

    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setAccumulators(self, accumulators):
        self.accumulators = accumulators

    def d_setAccumulators(self, accumulators):
        self.sendUpdate('setAccumulators', [accumulators])

    def b_setAccumulators(self, accumulators):
        self.setAccumulators(accumulators)
        self.d_setAccumulators(accumulators)

    def getAccumulators(self):
        return self.accumulators

    # stackLimit(uint16, uint16)

    def stackLimit(self, stackLimit, todo_uint16_1):
        self.sendUpdate('stackLimit', [stackLimit, todo_uint16_1])

    # stack(uint16, uint16)

    def stack(self, stack, todo_uint16_1):
        self.sendUpdate('stack', [stack, todo_uint16_1])

    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setStackLimits(self, stackLimits):
        self.stackLimits = stackLimits

    def d_setStackLimits(self, stackLimits):
        self.sendUpdate('setStackLimits', [stackLimits])

    def b_setStackLimits(self, stackLimits):
        self.setStackLimits(stackLimits)
        self.d_setStackLimits(stackLimits)

    def getStackLimits(self):
        return self.stackLimits

    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setStacks(self, stacks):
        self.stacks = stacks

    def d_setStacks(self, stacks):
        self.sendUpdate('setStacks', [stacks])

    def b_setStacks(self, stacks):
        self.setStacks(stacks)
        self.d_setStacks(stacks)

    def getStacks(self):
        return self.stacks

    # setTemporaryInventory(bool)

    def setTemporaryInventory(self, temporaryInventory):
        self.sendUpdate('setTemporaryInventory', [temporaryInventory])

    # setTemporaryStack(uint16, uint16)

    def setTemporaryStack(self, temporaryStack, todo_uint16_1):
        self.sendUpdate('setTemporaryStack', [temporaryStack, todo_uint16_1])



    # requestInventoryComplete()

    def requestInventoryComplete(self, requestInventoryComplete):
        self.sendUpdate('requestInventoryComplete', [requestInventoryComplete])



