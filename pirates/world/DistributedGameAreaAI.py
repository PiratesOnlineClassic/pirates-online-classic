from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedNodeAI import DistributedNodeAI

from otp.avatar.DistributedPlayerAI import DistributedPlayerAI

from pirates.piratesbase import PLocalizer
from pirates.world.GameAreaBuilderAI import GameAreaBuilderAI
from pirates.piratesbase import PLocalizer


class DistributedGameAreaAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGameAreaAI')

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)

        self.modelPath = ''
        self.links = []
        self.uniqueId = ''
        self.name = PLocalizer.Unknown
        self.fileName = ''
        self.jailInterior = None
        self.builder = GameAreaBuilderAI(self.air, self)

    def handleChildArrive(self, childObj, zoneId):
        if isinstance(childObj, DistributedPlayerAI):
            self.air.worldGridManager.handleLocationChanged(self, childObj, zoneId)

        DistributedNodeAI.handleChildArrive(self, childObj, zoneId)

    def handleChildArriveZone(self, childObj, zoneId):
        if isinstance(childObj, DistributedPlayerAI):
            self.air.worldGridManager.handleLocationChanged(self, childObj, zoneId)

        DistributedNodeAI.handleChildArriveZone(self, childObj, zoneId)

    def handleChildLeave(self, childObj, zoneId):
        if isinstance(childObj, DistributedPlayerAI):
            self.air.worldGridManager.clearAvatarInterest(self, childObj)

        DistributedNodeAI.handleChildLeave(self, childObj, zoneId)

    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    def d_setModelPath(self, modelPath):
        self.sendUpdate('setModelPath', [modelPath])

    def b_setModelPath(self, modelPath):
        self.setModelPath(modelPath)
        self.d_setModelPath(modelPath)

    def getModelPath(self):
        return self.modelPath

    def setLinks(self, links):
        self.links = links

    def d_setLinks(self, links):
        self.sendUpdate('setLinks', [links])

    def b_setLinks(self, links):
        self.setLinks(links)
        self.d_setLinks(links)

    def getLinks(self):
        return self.links

    def setUniqueId(self, uniqueId):
        self.uniqueId = uniqueId

    def d_setUniqueId(self, uniqueId):
        self.sendUpdate('setUniqueId', [uniqueId])

    def b_setUniqueId(self, uniqueId):
        self.setUniqueId(uniqueId)
        self.d_setUniqueId(uniqueId)

    def getUniqueId(self):
        return self.uniqueId

    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    def setFileName(self, fileName):
        self.fileName = fileName

    def getFileName(self):
        return self.fileName

    def getLocalizerName(self):
        return PLocalizer.LocationNames.get(self.uniqueId, self.name)

    def isInterior(self):
        return 'interior' in self.modelPath

    def d_addSpawnTriggers(self, triggerSpheres):
        self.sendUpdate('addSpawnTriggers', [triggerSpheres])

    def spawnNPC(self, spawnPtId, doId):
        pass

    def setJailInterior(self, jailInterior):
        self.jailInterior = jailInterior

    def getJailInterior(self):
        return self.jailInterior

    def generateChildWithRequired(self, do, zoneId, optionalFields=[]):
        self.generateChildWithRequiredAndId(do, self.air.allocateChannel(), self.doId, zoneId, optionalFields)

    def generateChildWithRequiredAndId(self, do, doId, parentId, zoneId, optionalFields=[]):
        do.generateWithRequiredAndId(doId, parentId, zoneId, optionalFields)
