from direct.directnotify import DirectNotifyGlobal

from pirates.npc.BossAI import BossAI
from pirates.npc.BossNPCGameFSMAI import BossNPCGameFSMAI
from pirates.npc.DistributedNPCNavySailorAI import DistributedNPCNavySailorAI


class DistributedBossNavySailorAI(DistributedNPCNavySailorAI, BossAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossNavySailorAI')

    def __init__(self, air):
        DistributedNPCNavySailorAI.__init__(self, air)
        BossAI.__init__(self, air)

    def createGameFSM(self):
        return BossNPCGameFSMAI(self.air, self)

    def getMonsterDmg(self):
        return BossAI.getMonsterDmg(self)
