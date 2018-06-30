# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.npc.DistributedBossSkeleton
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import Vec4
from pirates.npc.Boss import Boss
from pirates.npc.DistributedNPCSkeleton import DistributedNPCSkeleton
from pirates.pirate import AvatarTypes


class DistributedBossSkeleton(DistributedNPCSkeleton, Boss):

    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedBossSkeleton')

    def __init__(self, cr):
        DistributedNPCSkeleton.__init__(self, cr)
        Boss.__init__(self, cr)

    def generate(self):
        DistributedNPCSkeleton.generate(self)

    def announceGenerate(self):
        DistributedNPCSkeleton.announceGenerate(self)
        self.addBossEffect(AvatarTypes.Undead)

    def disable(self):
        self.removeBossEffect()
        DistributedNPCSkeleton.disable(self)

    def setAvatarType(self, avatarType):
        DistributedNPCSkeleton.setAvatarType(self, avatarType)
        self.loadBossData(self.getUniqueId(), avatarType)

    def getEnemyScale(self):
        return Boss.getEnemyScale(self)

    def getBossEffect(self):
        return Boss.getBossEffect(self)

    def getBossHighlightColor(self):
        return Boss.getBossHighlightColor(self)


# okay decompiling .\pirates\npc\DistributedBossSkeleton.pyc
