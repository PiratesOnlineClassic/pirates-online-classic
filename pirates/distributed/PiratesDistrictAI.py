
from otp.distributed.DistributedDistrictAI import DistributedDistrictAI
from direct.directnotify import DirectNotifyGlobal

class PiratesDistrictAI(DistributedDistrictAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesDistrictAI')

    def __init__(self, air):
        DistributedDistrictAI.__init__(self, air)
        self.avatarCount = 0
        self.newAvatarCount = 0
        self.mainWorld = ''
        self.shardType = 0


    # setAvatarCount(uint32) broadcast required
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setAvatarCount(self, avatarCount):
        self.avatarCount = avatarCount

    def d_setAvatarCount(self, avatarCount):
        self.sendUpdate('setAvatarCount', [avatarCount])

    def b_setAvatarCount(self, avatarCount):
        self.setAvatarCount(avatarCount)
        self.d_setAvatarCount(avatarCount)

    def getAvatarCount(self):
        return self.avatarCount

    # setNewAvatarCount(uint32) broadcast required
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setNewAvatarCount(self, newAvatarCount):
        self.newAvatarCount = newAvatarCount

    def d_setNewAvatarCount(self, newAvatarCount):
        self.sendUpdate('setNewAvatarCount', [newAvatarCount])

    def b_setNewAvatarCount(self, newAvatarCount):
        self.setNewAvatarCount(newAvatarCount)
        self.d_setNewAvatarCount(newAvatarCount)

    def getNewAvatarCount(self):
        return self.newAvatarCount

    # setMainWorld(string) broadcast required
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setMainWorld(self, mainWorld):
        self.mainWorld = mainWorld

    def d_setMainWorld(self, mainWorld):
        self.sendUpdate('setMainWorld', [mainWorld])

    def b_setMainWorld(self, mainWorld):
        self.setMainWorld(mainWorld)
        self.d_setMainWorld(mainWorld)

    def getMainWorld(self):
        return self.mainWorld

    # setShardType(uint8) broadcast required ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setShardType(self, shardType):
        self.shardType = shardType

    def d_setShardType(self, shardType):
        self.sendUpdate('setShardType', [shardType])

    def b_setShardType(self, shardType):
        self.setShardType(shardType)
        self.d_setShardType(shardType)

    def getShardType(self):
        return self.shardType

    # setPopulationLimits(uint16, uint16)

    def setPopulationLimits(self, populationLimits, todo_uint16_1):
        self.sendUpdate('setPopulationLimits', [populationLimits, todo_uint16_1])


