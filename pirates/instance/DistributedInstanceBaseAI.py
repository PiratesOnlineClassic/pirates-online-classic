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

    def getAvatarArea(self, avatar):
        # returns the game area within this instance that the avatar
        # is currently in, or None when the avatar is somewhere else...
        from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI

        area = avatar.getParentObj()
        if not isinstance(area, DistributedGameAreaAI):
            return None

        if area.getParentObj() is not self:
            return None

        return area

    def requestSpawnLoc(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        area = self.getAvatarArea(avatar)
        if not area:
            self.notify.warning('Cannot send spawn location for avatar %d, '
                'avatar is not in instance %d!' % (avatar.doId, self.doId))

            return

        xPos, yPos, zPos, h = self.getSpawnPt(area.getUniqueId())
        self.d_setSpawnInfo(avatar.doId, xPos, yPos, zPos, h, 0, [area.doId,
            area.zoneId, area.parentId])

    def avatarDied(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if not self.getAvatarArea(avatar):
            self.notify.warning('Received avatarDied for avatar %d, '
                'avatar is not in instance %d!' % (avatar.doId, self.doId))

            return

        # the avatar's Death state sends it to jail as soon as it's hp reaches
        # zero, if that was not possible then the client would wait in it's
        # death state forever, so release it back into the world instead...
        if avatar.gameFSM.getCurrentOrNextState() != 'Death':
            return

        if avatar.getJailCellIndex() < 100:
            return

        self.notify.warning('Avatar %d died but could not be sent to jail, '
            'releasing avatar!' % avatar.doId)

        avatar.b_setHp(avatar.getMaxHp())
        avatar.b_setGameState('LandRoam')
        self.d_sendLocalAvatarToJail(avatar.doId, 0, 0, 0)

    def d_sendLocalAvatarToJail(self, avatarId, jailDoId, jailWorldParentId, jailWorldZone):
        self.sendUpdateToAvatarId(avatarId, 'sendLocalAvatarToJail', [jailDoId, jailWorldParentId, jailWorldZone])

    def d_sendAutoInterest(self, avatarId, zoneList):
        self.sendUpdateToAvatarId(avatarId, 'AutoInterest', zoneList)

    def generateChildWithRequired(self, do, zoneId, optionalFields=[]):
        self.generateChildWithRequiredAndId(do, self.air.allocateChannel(), self.doId, zoneId, optionalFields)

    def generateChildWithRequiredAndId(self, do, doId, parentId, zoneId, optionalFields=[]):
        do.generateWithRequiredAndId(doId, parentId, zoneId, optionalFields)
