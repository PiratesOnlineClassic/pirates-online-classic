from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal
from pirates.battle.WeaponBaseAI import WeaponBaseAI


class DistributedWeaponAI(DistributedInteractiveAI, WeaponBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWeaponAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        WeaponBaseAI.__init__(self, air)

    def d_setMovie(self, mode, avId):
        self.sendUpdateToAvatarId(avId, 'setMovie', [mode, avId])
