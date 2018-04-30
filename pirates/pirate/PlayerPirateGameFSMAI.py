from pirates.pirate.BattleAvatarGameFSMAI import BattleAvatarGameFSMAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class PlayerPirateGameFSMAI(BattleAvatarGameFSMAI):
    notify = directNotify.newCategory('PlayerPirateGameFSMAI')

    def __init__(self, air, avatar):
        BattleAvatarGameFSMAI.__init__(self, air, avatar)
