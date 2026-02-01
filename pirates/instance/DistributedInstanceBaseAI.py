import random

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from pirates.piratesbase import PiratesGlobals
from pirates.world.WorldNodeAI import WorldNodeAI
from pirates.world.ClientAreaBuilderAI import ClientAreaBuilderAI


class DistributedInstanceBaseAI(DistributedObjectAI, WorldNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInstanceBaseAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        WorldNodeAI.__init__(self, air)

        self.uniqueId = ''
        self.name = ''
        self.fileName = ''
        self.type = PiratesGlobals.INSTANCE_NONE
        self.canBePrivate = False
        self.spawnPts = {}
        self.builder = ClientAreaBuilderAI(self.air, self)

    def getParentingRules(self):
        return ['', '']

    def getParentInstance(self):
        return None

    def getSubInstances(self):
        return []

    def setUniqueId(self, uniqueId):
        self.uniqueId = uniqueId

    def getUniqueId(self):
        return self.uniqueId

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setFileName(self, fileName):
        self.fileName = fileName

    def getFileName(self):
        return self.fileName

    def setType(self, type):
        self.type = type

    def d_setType(self, type):
        self.sendUpdate('setType', [type])

    def b_setType(self, type):
        self.setType(type)
        self.d_setType(type)

    def getType(self):
        return self.type

    def setCanBePrivate(self, canBePrivate):
        self.canBePrivate = canBePrivate

    def getCanBePrivate(self):
        return self.canBePrivate

    def d_setSpawnInfo(self, avatarId, xPos, yPos, zPos, h, spawnZone, parents):
        self.sendUpdateToAvatarId(avatarId, 'setSpawnInfo', [xPos, yPos, zPos, h, spawnZone, parents])

    def addSpawnPt(self, area, spawnPt, index=None):
        self.spawnPts[area] = self.spawnPts.setdefault(area, {})
        self.spawnPts[area][index or len(self.spawnPts[area])] = spawnPt

    def removeSpawnPt(self, area, index):
        if area not in self.spawnPts:
            return

        if index not in self.spawnPts[area]:
            return

        del self.spawnPts[area][index]

    def getSpawnPt(self, area, index=None):
        if area not in self.spawnPts:
            return (0, 0, 0, 0)

        if not index:
            index = random.choice(list(self.spawnPts[area].keys()))

        if index not in self.spawnPts[area]:
            return (0, 0, 0, 0)

        return self.spawnPts[area][index]

    def avatarDied(self):
        pass

    def d_sendLocalAvatarToJail(self, avatarId, jailDoId, jailWorldParentId, jailWorldZone):
        self.sendUpdateToAvatarId(avatarId, 'sendLocalAvatarToJail', [jailDoId, jailWorldParentId, jailWorldZone])

    def d_sendAutoInterest(self, avatarId, zoneList):
        self.sendUpdateToAvatarId(avatarId, 'AutoInterest', zoneList)

    def generateChildWithRequired(self, do, zoneId, optionalFields=[]):
        self.generateChildWithRequiredAndId(do, self.air.allocateChannel(), self.doId, zoneId, optionalFields)

    def generateChildWithRequiredAndId(self, do, doId, parentId, zoneId, optionalFields=[]):
        do.generateWithRequiredAndId(doId, parentId, zoneId, optionalFields)
