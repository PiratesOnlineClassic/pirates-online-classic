from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class DistributedInventoryUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryUD')

    def announceGenerate(self):
        DistributedObjectUD.announceGenerate(self)

        # Listen for async callback responses from the manager/AI.
        self.air.netMessenger.accept('getAccumulatorsResponse', self, self.processCallbackResponse)
        self.air.netMessenger.accept('getAccumulatorResponse', self, self.processCallbackResponse)
        self.air.netMessenger.accept('getStackLimitResponse', self, self.processCallbackResponse)
        self.air.netMessenger.accept('getStackResponse', self, self.processCallbackResponse)
        self.air.netMessenger.accept('getOwnerIdResponse', self, self.processCallbackResponse)

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

    def processCallbackResponse(self, callback, *args, **kwargs):
        """Safely invoke a callback delivered via netMessenger.

        Provides exception handling and logs failures instead of
        letting them propagate into the netMessenger task.
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
