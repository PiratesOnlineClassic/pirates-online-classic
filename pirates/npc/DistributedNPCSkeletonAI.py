from direct.directnotify import DirectNotifyGlobal

from pirates.battle.DistributedBattleNPCAI import DistributedBattleNPCAI
from pirates.piratesbase import PLocalizerEnglish


class DistributedNPCSkeletonAI(DistributedBattleNPCAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCSkeletonAI')

    def __init__(self, air):
        DistributedBattleNPCAI.__init__(self, air)

    def handleClientAggro(self, avatar):
        DistributedBattleNPCAI.handleClientAggro(self, avatar)
        self.d_setChat(PLocalizerEnglish.getUndeadAggroPhrase())
