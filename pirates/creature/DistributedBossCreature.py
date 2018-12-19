from pandac.PandaModules import Vec4
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.DistributedCreature import DistributedCreature
from pirates.pirate import AvatarTypes
from pirates.npc.Boss import Boss
CreatureTypes = {
    AvatarTypes.Crab: AvatarTypes.Crab,
    AvatarTypes.RockCrab: AvatarTypes.Crab,
    AvatarTypes.GiantCrab: AvatarTypes.Crab,
    AvatarTypes.Stump: AvatarTypes.Stump,
    AvatarTypes.FlyTrap: AvatarTypes.FlyTrap,
    AvatarTypes.Scorpion: AvatarTypes.Scorpion,
    AvatarTypes.DreadScorpion: AvatarTypes.Scorpion,
    AvatarTypes.Alligator: AvatarTypes.Alligator,
    AvatarTypes.BigGator: AvatarTypes.Alligator,
    AvatarTypes.HugeGator: AvatarTypes.Alligator,
    AvatarTypes.Bat: AvatarTypes.Bat,
    AvatarTypes.VampireBat: AvatarTypes.Bat,
    AvatarTypes.Wasp: AvatarTypes.Wasp,
    AvatarTypes.AngryWasp: AvatarTypes.Wasp}

class DistributedBossCreature(DistributedCreature, Boss):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossCreature')
    
    def __init__(self, cr):
        DistributedCreature.__init__(self, cr)
        Boss.__init__(self, cr)
    
    def setupCreature(self, avatarType):
        self.loadBossData(self.getUniqueId(), avatarType)
        DistributedCreature.setupCreature(self, avatarType)
    
    def announceGenerate(self):
        DistributedCreature.announceGenerate(self)
        avType = CreatureTypes[self.avatarType.getNonBossType()]
        self.addBossEffect(avType)
    
    def disable(self):
        self.removeBossEffect()
        DistributedCreature.disable(self)
    
    def getEnemyScale(self):
        return Boss.getEnemyScale(self)
    
    def getBossEffect(self):
        return Boss.getBossEffect(self)

    def getBossHighlightColor(self):
        return Boss.getBossHighlightColor(self)


