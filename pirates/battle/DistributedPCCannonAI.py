from direct.directnotify import DirectNotifyGlobal

from pirates.battle.DistributedWeaponAI import DistributedWeaponAI


class DistributedPCCannonAI(DistributedWeaponAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPCCannonAI')
