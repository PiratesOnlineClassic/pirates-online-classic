from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.directnotify import DirectNotifyGlobal

WRECK_ACTIVE = 0
WRECK_EMPTY = 1
WRECK_SUNK = 2


class DistributedWreckAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWreckAI')

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)

        self.modelPath = 'models/shipparts/merchantL2-geometry_High'
        self.status = WRECK_ACTIVE
        self.value = 0

    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    def getModelPath(self):
        return self.modelPath

    def setStatus(self, status):
        self.status = status

    def d_setStatus(self, status):
        self.sendUpdate('setStatus', [status])

    def b_setStatus(self, status):
        self.setStatus(status)
        self.d_setStatus(status)

    def getStatus(self):
        return self.status

    def setValue(self, value):
        self.value = max(0, value)

    def d_setValue(self, value):
        self.sendUpdate('setValue', [value])

    def b_setValue(self, value):
        self.setValue(value)
        self.d_setValue(self.value)

    def getValue(self):
        return self.value

    def takeValue(self, amount):
        # removes up to amount of treasure from the wreck,
        # returning how much was actually taken...
        if self.status != WRECK_ACTIVE:
            return 0

        amount = min(amount, self.value)
        self.b_setValue(self.value - amount)
        if self.value <= 0:
            self.b_setStatus(WRECK_EMPTY)

        return amount

    def d_sink(self):
        self.sendUpdate('sink', [])

    def sink(self):
        self.b_setStatus(WRECK_SUNK)
        self.d_sink()
