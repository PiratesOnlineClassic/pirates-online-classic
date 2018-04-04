
from pirates.npc.DistributedNPCNavySailorAI import DistributedNPCNavySailorAI
from pirates.npc.BossAI import BossAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBossNavySailorAI(DistributedNPCNavySailorAI, BossAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossNavySailorAI')

    def __init__(self, air):
        DistributedNPCNavySailorAI.__init__(self, air)
        BossAI.__init__(self, air)



