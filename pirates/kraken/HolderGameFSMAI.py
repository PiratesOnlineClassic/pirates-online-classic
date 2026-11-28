from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.pirate.BattleAvatarGameFSMAI import BattleAvatarGameFSMAI


class HolderGameFSMAI(BattleAvatarGameFSMAI):
    notify = directNotify.newCategory('HolderGameFSMAI')

    def enterDeath(self):
        self.avatar.processDeath()

    def exitDeath(self):
        pass
