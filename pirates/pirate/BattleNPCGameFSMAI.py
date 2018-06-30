from pirates.pirate.BattleAvatarGameFSMAI import BattleAvatarGameFSMAI
from direct.directnotify.DirectNotifyGlobal import directNotify


class BattleNPCGameFSMAI(BattleAvatarGameFSMAI):
    notify = directNotify.newCategory('BattleNPCGameFSMAI')

    def __init__(self, air, avatar):
        BattleAvatarGameFSMAI.__init__(self, air, avatar)

    def enterDeath(self):
        self.air.battleMgr.rewardAttackers(self.avatar)
        self.avatar.spawnerNode.processDeath()

    def exitDeath(self):
        pass
