from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.pirate.BattleAvatarGameFSMAI import BattleAvatarGameFSMAI


class BodyGameFSMAI(BattleAvatarGameFSMAI):
    notify = directNotify.newCategory('BodyGameFSMAI')

    def enterDeath(self):
        self.avatar.processDeath()

    def exitDeath(self):
        pass
