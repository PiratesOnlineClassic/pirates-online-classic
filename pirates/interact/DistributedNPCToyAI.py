from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI

class DistributedNPCToyAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCToyAI')

    MULTIUSE = True

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.modelPath = ''
        self.parentObjId = 0
        self.movie = 0

    def handleRequestInteraction(self, avatar, interactType, instant):
        return self.ACCEPT

    def handlePostRequestInteraction(self, avatar):
        # play the kick/punch movie for everyone that can see the toy; we do not
        # store it, otherwise new viewers would replay the movie on generate...
        self.d_setMovie(avatar.doId)

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

    def setParentObjId(self, parentObjId):
        self.parentObjId = parentObjId

    def d_setParentObjId(self, parentObjId):
        self.sendUpdate('setParentObjId', [parentObjId])

    def b_setParentObjId(self, parentObjId):
        self.setParentObjId(parentObjId)
        self.d_setParentObjId(parentObjId)

    def getParentObjId(self):
        return self.parentObjId

    def setMovie(self, movie):
        self.movie = movie

    def d_setMovie(self, movie):
        self.sendUpdate('setMovie', [movie])

    def b_setMovie(self, movie):
        self.setMovie(movie)
        self.d_setMovie(movie)

    def getMovie(self):
        return self.movie
