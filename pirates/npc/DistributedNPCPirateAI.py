from direct.directnotify import DirectNotifyGlobal

from pirates.battle.DistributedBattleNPCAI import DistributedBattleNPCAI


class DistributedNPCPirateAI(DistributedBattleNPCAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCPirateAI')

    def __init__(self, air):
        DistributedBattleNPCAI.__init__(self, air)
