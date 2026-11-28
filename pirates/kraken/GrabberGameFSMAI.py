from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.pirate.BattleAvatarGameFSMAI import BattleAvatarGameFSMAI


class GrabberGameFSMAI(BattleAvatarGameFSMAI):
    notify = directNotify.newCategory('GrabberGameFSMAI')

    def enterDeath(self):
        self.avatar.processDeath()

    def exitDeath(self):
        pass
