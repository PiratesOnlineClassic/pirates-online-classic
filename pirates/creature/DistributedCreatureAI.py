
from pirates.battle.DistributedBattleNPCAI import DistributedBattleNPCAI
from direct.directnotify import DirectNotifyGlobal

class DistributedCreatureAI(DistributedBattleNPCAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCreatureAI')

    def __init__(self, air):
        DistributedBattleNPCAI.__init__(self, air)



