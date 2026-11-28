from direct.directnotify import DirectNotifyGlobal

from pirates.battle.DistributedWeaponAI import DistributedWeaponAI
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import InventoryType


class DistributedPCCannonAI(DistributedWeaponAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPCCannonAI')

    # the client starts reloading as soon as it fires, allow for some latency
    # before the next shot is requested (see DistributedPCCannon.startReload)...
    ReloadTolerance = 0.5

    def __init__(self, air):
        DistributedWeaponAI.__init__(self, air)

        self.lastFireTimes = {}

    def gainSkill(self, skillId):
        # cannon skills are only ever earned through reputation, the client never sends this...
        avatarId = self.air.getAvatarIdFromSender()
        self.air.writeServerEvent('suspicious', avId=avatarId,
            issue='Tried to gain cannon skill %d from cannon %d!' % (skillId, self.doId))

    def canFireCannon(self, avatar, skillId, ammoSkillId):
        if avatar.doId != self.userId:
            self.notify.debug('Avatar %d tried to fire cannon %d they are not using!' % (
                avatar.doId, self.doId))

            return False

        if skillId != InventoryType.CannonShoot or not WeaponGlobals.getIsCannonSkill(ammoSkillId) or \
                ammoSkillId == InventoryType.CannonShoot:
            self.air.writeServerEvent('suspicious', avId=avatar.doId,
                issue='Tried to fire cannon %d with skill %d, ammo %d!' % (self.doId, skillId, ammoSkillId))

            return False

        inventory = avatar.getInventory()
        if not inventory:
            return False

        # the ammo the cannon may fire are the ammo skills the avatar has learned,
        # or the round shot and grapple hooks everyone may fire (see DistributedPCCannon.changeAmmo)...
        if not WeaponGlobals.isInfiniteAmmo(ammoSkillId) and inventory.getStackQuantity(ammoSkillId) < 2:
            self.notify.debug('Avatar %d cannot fire ammo %d, ammo skill was never learned!' % (
                avatar.doId, ammoSkillId))

            return False

        if hasattr(avatar, 'isPaid') and not avatar.isPaid() and not WeaponGlobals.canFreeUse(ammoSkillId):
            self.notify.debug('Freebooter %d cannot fire paid ammo %d!' % (avatar.doId, ammoSkillId))
            return False

        if not WeaponGlobals.isInfiniteAmmo(ammoSkillId):
            ammoId = WeaponGlobals.getSkillAmmoInventoryId(ammoSkillId)
            if ammoId and inventory.getStackQuantity(ammoId) < 1:
                self.notify.debug('Avatar %d cannot fire ammo %d, out of ammo!' % (avatar.doId, ammoSkillId))
                return False

        # a volley of shots may be fired before the cannon has to be reloaded, the
        # client reloads the whole volley once it stops firing for the reload time
        # (see DistributedPCCannon.startReload and finishReload)...
        lastFired, shotsFired = self.lastFireTimes.get(avatar.doId, (None, 0))
        if lastFired is not None:
            reloadTime = self.air.battleMgr.getModifiedReloadTime(avatar, skillId, ammoSkillId)
            if globalClock.getRealTime() - lastFired >= reloadTime - self.ReloadTolerance:
                shotsFired = 0

            volley = max(1, int(WeaponGlobals.getAttackVolley(skillId, ammoSkillId)))
            if shotsFired >= volley:
                self.notify.debug('Avatar %d fired cannon %d before it was reloaded!' % (
                    avatar.doId, self.doId))

                return False

        self.lastFireTimes[avatar.doId] = (lastFired, shotsFired)
        return True

    def useCannonAmmo(self, avatar, ammoSkillId):
        lastFired, shotsFired = self.lastFireTimes.get(avatar.doId, (None, 0))
        self.lastFireTimes[avatar.doId] = (globalClock.getRealTime(), shotsFired + 1)
        if WeaponGlobals.isInfiniteAmmo(ammoSkillId) or config.GetBool('infinite-ammo', False):
            return

        inventory = avatar.getInventory()
        ammoId = WeaponGlobals.getSkillAmmoInventoryId(ammoSkillId)
        if inventory and ammoId:
            inventory.b_setStackQuantity(ammoId, max(0, inventory.getStackQuantity(ammoId) - 1))

    def requestProjectileSkill(self, skillId, ammoSkillId, posHpr, timestamp, power):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if not self.canFireCannon(avatar, skillId, ammoSkillId):
            return

        self.useCannonAmmo(avatar, ammoSkillId)
        DistributedWeaponAI.requestProjectileSkill(self, skillId, ammoSkillId, posHpr, timestamp, power)
