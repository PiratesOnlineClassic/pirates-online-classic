from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta

from pirates.battle.DistributedShipCannonAI import DistributedShipCannonAI
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import InventoryType


class DistributedTutorialShipCannonAI(DistributedShipCannonAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTutorialShipCannonAI')

    def __init__(self, air):
        DistributedShipCannonAI.__init__(self, air)

    def requestProjectileSkill(self, skillId, ammoSkillId, posHpr, timestamp, power):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if (not avatar or avatar.doId != self.userId or avatar.doId != self.avatarId
                or self.mode != WeaponGlobals.WEAPON_MOVIE_START
                or skillId != InventoryType.CannonShoot
                or ammoSkillId != InventoryType.CannonRoundShot):
            self.notify.warning('Rejected invalid tutorial cannon projectile request')
            return

        # Wreck hits are client-local and never send a projectile result to clear tracking.
        timestamp = globalClockDelta.getRealNetworkTime(bits=32)
        self.sendUpdate('useProjectileSkill', [skillId, ammoSkillId, posHpr, timestamp, power])
