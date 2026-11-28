from otp.distributed.DistributedDistrictAI import DistributedDistrictAI
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals

class PiratesDistrictAI(DistributedDistrictAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesDistrictAI')

    def __init__(self, air):
        DistributedDistrictAI.__init__(self, air)
        self.avatarCount = 0
        self.newAvatarCount = 0
        self.mainWorldFile = ''
        self.shardType = PiratesGlobals.SHARD_MAIN
        self.populationLimits = [0, 0]

    def getParentingRules(self):
        return ['', '']

    def setAvatarCount(self, avatarCount):
        self.avatarCount = avatarCount

    def d_setAvatarCount(self, avatarCount):
        self.sendUpdate('setAvatarCount', [avatarCount])

    def b_setAvatarCount(self, avatarCount):
        self.d_setAvatarCount(avatarCount)
        self.setAvatarCount(avatarCount)

    def getAvatarCount(self):
        return self.avatarCount

    def setNewAvatarCount(self, newAvatarCount):
        self.newAvatarCount = newAvatarCount

    def d_setNewAvatarCount(self, newAvatarCount):
        self.sendUpdate('setNewAvatarCount', [newAvatarCount])

    def b_setNewAvatarCount(self, newAvatarCount):
        self.d_setNewAvatarCount(newAvatarCount)
        self.setNewAvatarCount(newAvatarCount)

    def getNewAvatarCount(self):
        return self.newAvatarCount

    def setMainWorld(self, mainWorldFile):
        self.mainWorldFile = mainWorldFile

    def d_setMainWorld(self, mainWorldFile):
        self.sendUpdate('setMainWorld', [mainWorldFile])

    def b_setMainWorld(self, mainWorldFile):
        self.setMainWorld(mainWorldFile)
        self.d_setMainWorld(mainWorldFile)

    def getMainWorld(self):
        return self.mainWorldFile

    def setShardType(self, shardType):
        self.shardType = shardType

    def d_setShardType(self, shardType):
        self.sendUpdate('setShardType', [shardType])

    def b_setShardType(self, shardType):
        self.setShardType(shardType)
        self.d_setShardType(shardType)

    def getShardType(self):
        return self.shardType

    def setPopulationLimits(self, lowLimit, highLimit):
        self.populationLimits = [lowLimit, highLimit]

    def getPopulationLimits(self):
        return self.populationLimits

    def d_setStats(self, avatarCount, newAvatarCount):
        self.sendUpdate('setStats', [avatarCount, newAvatarCount])

    def b_setStats(self, avatarCount, newAvatarCount):
        self.setAvatarCount(avatarCount)
        self.setNewAvatarCount(newAvatarCount)
        self.d_setStats(avatarCount, newAvatarCount)

    def isFull(self):
        # a district is considered full once it reaches it's high population limit,
        # a limit of zero means the district has no population limit...
        highLimit = self.populationLimits[1]
        return bool(highLimit) and self.avatarCount >= highLimit
