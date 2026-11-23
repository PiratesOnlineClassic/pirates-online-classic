from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal


class DistributedInventoryUD(DistributedObjectUD):
    """
    UberDog-side inventory proxy.
    
    Forwards inventory operations to the AI via netMessenger.
    This class acts as a bridge between the database layer and the AI-side
    inventory that holds the actual data.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryUD')

    # -------------------------------------------------------------------------
    # Setters - Forward to AI via netMessenger
    # -------------------------------------------------------------------------
    def b_setAccumulators(self, accumulators):
        self.air.netMessenger.send('b_setAccumulators', [self.doId, accumulators])

    def b_setAccumulator(self, accumulatorType, quantity):
        self.air.netMessenger.send('b_setAccumulator', [self.doId, accumulatorType, quantity])

    def b_setStackLimits(self, stackLimits):
        self.air.netMessenger.send('b_setStackLimits', [self.doId, stackLimits])

    def b_setStacks(self, stacks):
        self.air.netMessenger.send('b_setStacks', [self.doId, stacks])

    def b_setStack(self, stackType, quantity):
        self.air.netMessenger.send('b_setStack', [self.doId, stackType, quantity])

    def b_setOwnerId(self, ownerId):
        self.air.netMessenger.send('b_setOwnerId', [self.doId, ownerId])

    # -------------------------------------------------------------------------
    # Getters - Request from AI via netMessenger with callback
    # -------------------------------------------------------------------------
    def getAccumulators(self, callback):
        if callback is None:
            return
        self.air.netMessenger.send('getAccumulators', [self.doId, callback])

    def getAccumulator(self, accumulatorType, callback):
        if callback is None:
            return
        self.air.netMessenger.send('getAccumulator', [self.doId, accumulatorType, callback])

    def getStackLimit(self, stackType, callback):
        if callback is None:
            return
        self.air.netMessenger.send('getStackLimit', [self.doId, stackType, callback])

    def getStack(self, stackType, callback):
        if callback is None:
            return
        self.air.netMessenger.send('getStack', [self.doId, stackType, callback])

    def getOwnerId(self, callback):
        if callback is None:
            return
        self.air.netMessenger.send('getOwnerId', [self.doId, callback])
