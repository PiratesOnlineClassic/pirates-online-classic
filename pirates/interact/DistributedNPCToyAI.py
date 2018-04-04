
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal

class DistributedNPCToyAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCToyAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.uniqueId = ''
        self.modelPath = ''
        self.parentObjId = 0
        self.movie = 0


    # setUniqueId(string) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setUniqueId(self, uniqueId):
        self.uniqueId = uniqueId

    def d_setUniqueId(self, uniqueId):
        self.sendUpdate('setUniqueId', [uniqueId])

    def b_setUniqueId(self, uniqueId):
        self.setUniqueId(uniqueId)
        self.d_setUniqueId(uniqueId)

    def getUniqueId(self):
        return self.uniqueId

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

    # setMovie(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setMovie(self, movie):
        self.movie = movie

    def d_setMovie(self, movie):
        self.sendUpdate('setMovie', [movie])

    def b_setMovie(self, movie):
        self.setMovie(movie)
        self.d_setMovie(movie)

    def getMovie(self):
        return self.movie


