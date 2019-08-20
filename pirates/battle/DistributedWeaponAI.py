from direct.directnotify import DirectNotifyGlobal

from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.battle.WeaponBaseAI import WeaponBaseAI
from pirates.battle import WeaponGlobals


class DistributedWeaponAI(DistributedInteractiveAI, WeaponBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWeaponAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        WeaponBaseAI.__init__(self, air)

        self.mode = WeaponGlobals.WEAPON_MOVIE_CLEAR
        self.avatarId = 0

    def setMovie(self, mode, avatarId):
        self.mode = mode
        self.avatarId = avatarId

    def d_setMovie(self, mode, avatarId):
        self.sendUpdateToAvatarId(avatarId, 'setMovie', [mode, avatarId])

    def b_setMovie(self, mode, avatarId):
        self.setMovie(mode, avatarId)
        self.d_setMovie(mode, avatarId)

    def getMovie(self):
        return [self.mode, self.avatarId]

    def startWeapon(self, avatarId):
        if self.mode == WeaponGlobals.WEAPON_MOVIE_START:
            return

        self.b_setMovie(WeaponGlobals.WEAPON_MOVIE_START, avatarId)

    def stopWeapon(self, avatarId):
        if self.mode == WeaponGlobals.WEAPON_MOVIE_STOP:
            return

        self.b_setMovie(WeaponGlobals.WEAPON_MOVIE_STOP, avatarId)
