from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedNodeAI import DistributedNodeAI
from pirates.piratesbase import PLocalizer
from pirates.piratesbase.UniqueIdManager import UniqueIdManager
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

        self.uidMgr = UniqueIdManager(self.air)
        self.builder = GameAreaBuilderAI(self.air, self)

    def handleAvatarZoneChange(self, av, useZoneId=-1):
        pos = av.getPos(self)
        zoneId = self.getZoneFromXYZ(pos)

        def resetConcentricZones():
            avatar.setConcentricZones(self.getConcentricZones(zoneId,
                self.gridRadius))

        # if the avatar doesn't already have a set of concentric zones
        # calculated, calculate a new set of zones...
        if not avatar.getConcentricZones():
            resetConcentricZones()

        for concentricZoneId in avatar.getConcentricZones():

            # check to see if the avatar has gone out of range of the available
            # concentric zones
            if zoneId < concentricZoneId or zoneId > concentricZoneId:

                # set the grid parent of the avatar to the new zone which is out
                # of range of the concentric zones
                avatar.b_setLocation(self.doId, zoneId)

                # the avatar has gone past it's previous set of concentric zones,
                # calculate a new set of zones...
                resetConcentricZones()
                break

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

    def getLocalizerName(self):
        return PLocalizer.LocationNames.get(self.uniqueId, self.name)

    def isInterior(self):
        return 'interior' in self.modelPath

    def d_addSpawnTriggers(self, triggerSpheres):
        self.sendUpdate('addSpawnTriggers', [triggerSpheres])

    def spawnNPC(self, spawnPtId, doId):
        pass

    def generateChildWithRequired(self, do, zoneId, optionalFields=[]):
        do.generateWithRequiredAndId(self.air.allocateChannel(), self.doId, zoneId, optionalFields)
