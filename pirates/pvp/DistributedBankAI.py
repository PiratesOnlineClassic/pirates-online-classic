
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBankAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBankAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.modelPath = ''
        self.parentObjId = 0


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

    # setBelongsToTeam(int16) broadcast ram

    def setBelongsToTeam(self, belongsToTeam):
        self.sendUpdate('setBelongsToTeam', [belongsToTeam])

    # startLooting(uint8)

    def startLooting(self, startLooting):
        self.sendUpdate('startLooting', [startLooting])

    # stopLooting()

    def stopLooting(self, stopLooting):
        self.sendUpdate('stopLooting', [stopLooting])

    # setValue(int16) broadcast ram

    def setValue(self, value):
        self.sendUpdate('setValue', [value])

    # setMaxValue(uint16) broadcast ram

    def setMaxValue(self, maxValue):
        self.sendUpdate('setMaxValue', [maxValue])

    # setParentObjId(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setParentObjId(self, parentObjId):
        self.parentObjId = parentObjId

    def d_setParentObjId(self, parentObjId):
        self.sendUpdate('setParentObjId', [parentObjId])

    def b_setParentObjId(self, parentObjId):
        self.setParentObjId(parentObjId)
        self.d_setParentObjId(parentObjId)

    def getParentObjId(self):
        return self.parentObjId


