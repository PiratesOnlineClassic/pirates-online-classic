from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class DistributedInventoryUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryUD')

    def announceGenerate(self):
        DistributedObjectUD.announceGenerate(self)

        self.air.netMessenger.accept('getAccumulatorsResponse', self, self.proccessCallbackResponse)
        self.air.netMessenger.accept('getAccumulatorResponse', self, self.proccessCallbackResponse)
        self.air.netMessenger.accept('getStackLimitResponse', self, self.proccessCallbackResponse)
        self.air.netMessenger.accept('getStackResponse', self, self.proccessCallbackResponse)
        self.air.netMessenger.accept('getOwnerIdResponse', self, self.proccessCallbackResponse)

    def b_setAccumulators(self, accumulators):
        self.air.netMessenger.send('b_setAccumulators', [accumulators])

    def b_setAccumulator(self, accumulatorType, quantity):
        self.air.netMessenger.send('b_setAccumulator', [accumulatorType, quantity])

    def b_setStackLimits(self, stackLimits):
        self.air.netMessenger.send('b_setStackLimits', [stackLimits])

    def b_setStacks(self, stacks):
        self.air.netMessenger.send('b_setStacks', [stacks])

    def b_setStack(self, stackType, quantity):
        self.air.netMessenger.send('b_setStack', [stackType, quantity])

    def b_setOwnerId(self, ownerId):
        self.air.netMessenger.send('b_setOwnerId', [ownerId])

    def getAccumulators(self, callback):
        self.air.netMessenger.send('getAccumulators', [callback])

    def getAccumulator(self, accumulatorType, callback):
        self.air.netMessenger.send('getAccumulator', [accumulatorType, callback])

    def getStackLimit(self, stackType, callback):
        self.air.netMessenger.send('getStackLimit', [stackType, callback])

    def getStack(self, stackType, callback):
        self.air.netMessenger.send('getStack', [stackType, callback])

    def getOwnerId(self, callback):
        self.air.netMessenger.send('getOwnerId', [callback])

    def proccessCallbackResponse(self, callback, *args, **kwargs):
        if callback and callable(callback):
            callback(*args, **kwargs)
            return

        self.notify.warning('No valid callback for a callback response! '
            'What was the purpose of that?')
