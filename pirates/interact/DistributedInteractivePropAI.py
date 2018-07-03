from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.distributed.DistributedTargetableObjectAI import DistributedTargetableObjectAI

class DistributedInteractivePropAI(DistributedInteractiveAI, DistributedTargetableObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteractivePropAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        DistributedTargetableObjectAI.__init__(self, air)

    def handleRequestInteraction(self, avatar, interactType, instant):
        return self.ACCEPT

    def handleRequestExit(self, avatar):
        return self.ACCEPT

    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    def d_setModelPath(self, modelPath):
        self.sendUpdate('setModelPath', [modelPath])

    def b_setModelPath(self, modelPath):
        self.setModelPath(modelPath)
        self.d_setModelPath(modelPath)

    def getModelPath(self):
        return self.modelPath

    def setParentObjId(self, parentId):
        self.parentId = parentId

    def d_setParentObjId(self, parentId):
        self.sendUpdate('setParentId', [parentId])

    def b_setParentObjId(self, parentId):
        self.setParentObjId(parentId)
        self.d_setParentObjId(parentId)

    def getParentObjId(self):
        return self.parentId

    def d_setMovie(self, movie):
        self.sendUpdate('setMovie', [movie])

    def setInteractAble(self, interactAble):
        self.interactAble = interactAble

    def d_setInteractAble(self, interactAble):
        self.sendUpdate('setInteractAble', [interactAble])

    def b_setInteractAble(self, interactAble):
        self.setInteractAble(interactAble)
        self.d_setInteractAble(interactAble)

    def getInteractAble(self):
        return self.interactAble

    def setInteractType(self, interactType):
        self.interactType = interactType

    def d_setInteractType(self, interactType):
        self.sendUpdate('setInteractType', [interactType])

    def b_setInteractType(self, interactType):
        self.setInteractType(interactType)
        self.d_setInteractType(interactType)

    def getInteractType(self):
        return self.interactType

    def d_propSlashed(self):
        self.sendUpdate('propSlashed', [])

    def getDamagable(self):
        return False

    def getTeam(self):
        return PiratesGlobals.TUTORIAL_ENEMY_TEAM

    def getLevel(self):
        return 1
