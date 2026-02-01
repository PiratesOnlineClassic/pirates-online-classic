from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta

from otp.avatar.DistributedAvatarAI import DistributedAvatarAI

from pirates.battle.WeaponBaseBase import WeaponBaseBase
from pirates.piratesbase import PiratesGlobals
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI


class WeaponBaseAI(WeaponBaseBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('WeaponBaseAI')

    def __init__(self, air):
        self.air = air

    def requestTargetedSkill(self, skillId, ammoSkillId, clientResult, targetId, areaIdList, timestamp, pos, charge):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        target = self.air.doId2do.get(targetId)

        # this will handle the attackers targeted skill request, however we will not check if the target
        # specified in this update is valid. because, if their is no target then the client is
        # just requesting targeted skill for no target...
        self.useTargetedSkill(avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge)

        # this will handle the targeted skill for any targets in the range of the attacker,
        # for example if an attacker uses a skill that effects enemies around it...
        for targetId in areaIdList:

            # ignore the avatar if it is in the area list,
            # no reason to handle it here...
            if targetId == avatar.doId:
                continue

            target = self.air.doId2do.get(targetId)
            if not target:
                self.notify.debug('Cannot request targeted skill, unknown areaId target; '
                    'avatarId=%d skillId=%d!' % (avatar.doId, skillId))

                continue

            self.useTargetedSkill(avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge)

    def requestProjectileSkill(self, skillId, ammoSkillId, posHpr, timestamp, power):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        print(("requestProjectileSkill", skillId, ammoSkillId, posHpr, timestamp, power))

        if self.air.targetMgr.hasProjectile(avatar.doId, skillId, ammoSkillId):
            self.notify.debug('Avatar %d tried to request projectile skill for already used skill; '
                'skillId=%d ammoSkillId=%d!' % (avatar.doId, skillId, ammoSkillId))

            return

        # TODO FIXME: calculate the air time of the projectile and store the current,
        # timestamp so we know when the projectile request expires...
        timestamp = globalClockDelta.getRealNetworkTime(bits=32)
        self.air.targetMgr.addProjectile(avatar.doId, skillId, ammoSkillId, timestamp)

        # send the projectile skill update so everyone in the same zone
        # will see the projectile...
        self.sendUpdate('useProjectileSkill', [skillId, ammoSkillId, posHpr, timestamp, power])

    def suggestProjectileSkillResult(self, skillId, ammoSkillId, result, targetId, areaIdList, pos, normal, codes, timestamp):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        target = self.air.doId2do.get(targetId)
        from pirates.movement.DistributedMovingObjectAI import DistributedMovingObjectAI
        if not isinstance(target, DistributedMovingObjectAI):
            target = None

        #if not self.air.targetMgr.hasProjectile(avatar.doId, skillId, ammoSkillId):
        #    self.notify.warning('Avatar %d tried to request projectile skill for skill never used; '
        #        'skillId=%d ammoSkillId=%d!' % (avatar.doId, skillId, ammoSkillId))
        #
        #    return

        # handle projectile skill results for non ship objects:
        from pirates.ship.DistributedShipAI import DistributedShipAI
        if not isinstance(target, DistributedShipAI):
            self.useProjectileSkill(avatar, target, skillId, ammoSkillId, result, targetId, areaIdList, pos, normal, codes, timestamp)
            for targetId in areaIdList:
                target = self.air.doId2do.get(targetId)
                if not target:
                    self.notify.debug('Cannot request projectil skill, unknown areaId target; '
                        'avatarId=%d skillId=%d!' % (avatar.doId, skillId))

                    continue

                self.useProjectileSkill(avatar, target, skillId, ammoSkillId, result, targetId, areaIdList, pos, normal, codes, timestamp)
        else:
            # handle projectile skill results for ships and shipparts:
            cannonCode, hullCode, sailCode = codes
            skillResult = self.air.battleMgr.willWeaponHit(avatar, target, skillId, ammoSkillId, 0)

            attackerEffects = [0, 0, 0, 0, 0]
            targetEffects = [0, 0, 0, 0, 0]
            areaIdEffects = [attackerEffects, targetEffects]

            timestamp = globalClockDelta.getRealNetworkTime(bits=32)
            if skillResult:
                if hullCode > 0:
                    target.hull.projectileWeaponHit(skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, avatar)

                if sailCode > 0:
                    for sail in target.sails:
                        if sail.hp > 0:
                            sail.projectileWeaponHit(skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, avatar)

            self.sendUpdate('setProjectileSkillResult', [skillId, ammoSkillId, skillResult, target.doId, [], attackerEffects, targetEffects, areaIdEffects, pos, normal, codes, avatar.doId, timestamp])

        # the projectile has been successfully used, remove the projectile
        # from the target manager so the avatar can use the skill again...
        self.air.targetMgr.removeProjectile(avatar.doId, skillId, ammoSkillId)

    def useTargetedSkill(self, avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge):
        targetResult = self.air.battleMgr.getTargetedSkillResult(avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge)
        if not targetResult:
            self.notify.debug('Cannot get targeted skill, no valid result was given; '
                'avatarId=%d, skillId=%d!' % (avatar.doId, skillId))

            return

        self.sendUpdate('useTargetedSkill', targetResult)

    def useProjectileSkill(self, avatar, target, skillId, ammoSkillId, result, targetId, areaIdList, pos, normal, codes, timestamp):
        targetResult = self.air.battleMgr.getTargetedSkillResult(avatar, target, skillId, ammoSkillId, result, areaIdList, timestamp, pos)
        if not targetResult:
            self.notify.debug('Cannot get projectile targeted skill, '
                'no valid result was given; avatarId=%d, skillId=%d!' % (avatar.doId, skillId))

            return

        skillId, ammoSkillId, skillResult, targetDoId, areaIdList, attackerEffects, targetEffects, \
            areaIdEffects, timestamp, pos, charge = targetResult

        self.sendUpdate('setProjectileSkillResult', [skillId, ammoSkillId, skillResult, targetId if not target else target.doId,
            areaIdList, attackerEffects, targetEffects, areaIdEffects, pos, normal, codes, avatar.doId, timestamp])
