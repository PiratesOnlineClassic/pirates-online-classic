
from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
from pirates.npc.BossAI import BossAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBossCreatureAI(DistributedCreatureAI, BossAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossCreatureAI')

    def __init__(self, air):
        DistributedCreatureAI.__init__(self, air)
        BossAI.__init__(self, air)



