
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTownAI(DistributedGameAreaAI, DistributedCartesianGridAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTownAI')

    def __init__(self, air):
        DistributedGameAreaAI.__init__(self, air)
        DistributedCartesianGridAI.__init__(self, air)
        self.modelPath = ''


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


