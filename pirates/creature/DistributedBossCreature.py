# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.DistributedBossCreature
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import Vec4
from pirates.creature.DistributedCreature import DistributedCreature
from pirates.npc.Boss import Boss
from pirates.pirate import AvatarTypes

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
    AvatarTypes.AngryWasp: AvatarTypes.Wasp
}


class DistributedBossCreature(DistributedCreature, Boss):

    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedBossCreature')

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


# okay decompiling .\pirates\creature\DistributedBossCreature.pyc
