
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.distributed.DistributedTargetableObjectAI import DistributedTargetableObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedInteractivePropAI(DistributedInteractiveAI, DistributedTargetableObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteractivePropAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        DistributedTargetableObjectAI.__init__(self, air)
        self.modelPath = ''
        self.parentObjId = 0
        self.interactAble = ''
        self.interactType = ''


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

    # setMovie(uint32) broadcast ram

    def setMovie(self, movie):
        self.sendUpdate('setMovie', [movie])

    # setInteractAble(string) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setInteractAble(self, interactAble):
        self.interactAble = interactAble

    def d_setInteractAble(self, interactAble):
        self.sendUpdate('setInteractAble', [interactAble])

    def b_setInteractAble(self, interactAble):
        self.setInteractAble(interactAble)
        self.d_setInteractAble(interactAble)

    def getInteractAble(self):
        return self.interactAble

    # setInteractType(string) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setInteractType(self, interactType):
        self.interactType = interactType

    def d_setInteractType(self, interactType):
        self.sendUpdate('setInteractType', [interactType])

    def b_setInteractType(self, interactType):
        self.setInteractType(interactType)
        self.d_setInteractType(interactType)

    def getInteractType(self):
        return self.interactType

    # propSlashed() broadcast

    def propSlashed(self, propSlashed):
        self.sendUpdate('propSlashed', [propSlashed])


