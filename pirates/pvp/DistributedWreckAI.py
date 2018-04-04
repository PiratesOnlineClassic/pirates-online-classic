
from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.directnotify import DirectNotifyGlobal

class DistributedWreckAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWreckAI')

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)
        self.modelPath = ''
        self.status = 0
        self.value = 0


    # setModelPath(string) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    def d_setModelPath(self, modelPath):
        self.sendUpdate('setModelPath', [modelPath])

    def b_setModelPath(self, modelPath):
        self.setModelPath(modelPath)
        self.d_setModelPath(modelPath)

    def getModelPath(self):
        return self.modelPath

    # setStatus(int8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setStatus(self, status):
        self.status = status

    def d_setStatus(self, status):
        self.sendUpdate('setStatus', [status])

    def b_setStatus(self, status):
        self.setStatus(status)
        self.d_setStatus(status)

    def getStatus(self):
        return self.status

    # setValue(int8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setValue(self, value):
        self.value = value

    def d_setValue(self, value):
        self.sendUpdate('setValue', [value])

    def b_setValue(self, value):
        self.setValue(value)
        self.d_setValue(value)

    def getValue(self):
        return self.value

    # sink() broadcast ram

    def sink(self, sink):
        self.sendUpdate('sink', [sink])


