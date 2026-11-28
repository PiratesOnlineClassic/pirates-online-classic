from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta

from otp.avatar.DistributedAvatarAI import DistributedAvatarAI

from pirates.battle.WeaponBaseBase import WeaponBaseBase
from pirates.battle import WeaponGlobals
from pirates.battle import EnemyGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI


class WeaponBaseAI(WeaponBaseBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('WeaponBaseAI')

    # the client only warns it's player about targets beyond 4/3 of a skill's
    # range (see CombatTray.trySkill), and the positions we know of lag behind
    # the client's. targets are only out of range once they are well beyond that...
    AttackRangeTolerance = 1.5
    AttackRangeLeeway = 10.0

    def __init__(self, air):
        self.air = air

    def isTargetInAttackRange(self, avatar, target, skillId, ammoSkillId):
        if not hasattr(target, 'getParentObj') or not hasattr(target, 'getPos'):
            return True

        attackRange = self.air.battleMgr.getModifiedAttackRange(avatar, skillId, ammoSkillId)
        if not attackRange or attackRange == WeaponGlobals.INF_RANGE:
            return True

        # big creatures (crabs, stumps...) can be hit anywhere along their battle tube,
        # the client takes the size of the tube off the distance (BattleManager.targetInRange)...
        tolerance = self.AttackRangeLeeway
        if getattr(target, 'isNpc', False) and getattr(target, 'avatarType', None) is not None:
            try:
                tolerance += EnemyGlobals.getBattleTubeRadius(target.avatarType) or 0
            except (KeyError, IndexError, TypeError, AttributeError):
                pass

        maxDistance = attackRange * self.AttackRangeTolerance + tolerance
        return self.air.battleMgr.getRelativePosition(avatar, target) <= maxDistance

    def syncCurrentTarget(self, avatar, target):
        # the other clients play the avatar's attack against the avatar's current
        # target (DistributedTargetableObject.useTargetedSkill), make sure they know
        # which target the avatar is attacking before they hear of the attack...
        if target is None or target is avatar or getattr(avatar, 'isNpc', True):
            return

        if avatar.getCurrentTarget() != target.doId:
            avatar.b_setCurrentTarget(target.doId)

    def requestTargetedSkill(self, skillId, ammoSkillId, clientResult, targetId, areaIdList, timestamp, pos, charge):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        # skills used with the avatar's own weapons are validated, and their costs
        # spent, once per request no matter how many targets the skill effects...
        if self is avatar and not self.air.battleMgr.requestSkillUse(avatar, skillId, ammoSkillId):
            self.notify.debug('Avatar %d cannot use targeted skill %d, ammo skill %d!' % (
                avatar.doId, skillId, ammoSkillId))

            # the client still rolled this attack with a new seed...
            self.air.battleMgr.advanceAttackSeed(avatar)
            return

        # this will handle the attackers targeted skill request, however we will not check if the target
        # specified in this update is valid. because, if their is no target then the client is
        # just requesting targeted skill for no target. the skill's result includes the result
        # for every target in the area of the skill, the client predicts all of them at once...
        target = self.air.doId2do.get(targetId) if targetId else None
        if target is not None and self is avatar and not self.air.battleMgr.isPlayerSkillHandledElsewhere(skillId):
            # never land an attack on a target the avatar couldn't have reached,
            # the attack's swing is still shown to everyone...
            if not self.isTargetInAttackRange(avatar, target, skillId, ammoSkillId):
                self.notify.debug('Avatar %d target %d is out of range of skill %d!' % (
                    avatar.doId, targetId, skillId))

                clientResult = WeaponGlobals.RESULT_OUT_OF_RANGE

            self.syncCurrentTarget(avatar, target)

        self.useTargetedSkill(avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge, clientResult)

    def requestShipSkill(self, skillId, ammoSkillId, clientResult, targetId, timestamp):
        # the helmsman's sailing skills are sent by the avatar, the target
        # is always the ship it is steering (see LocalPirate.composeRequestShipSkill)...
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar or avatar is not self:
            return

        # the client rolled the ship skill with a new seed, see BattleManager.doAttack...
        if getattr(avatar, 'battleRandom', None):
            avatar.battleRandom.advanceAttackSeed()

        from pirates.ship.DistributedShipAI import DistributedShipAI
        ship = self.air.doId2do.get(targetId)
        if not isinstance(ship, DistributedShipAI) or not ship.hasCrewMember(avatar.doId):
            self.notify.debug('Avatar %d cannot use ship skill %d on ship %d they are not crew of!' % (
                avatar.doId, skillId, targetId))

            return

        ship.useShipSkill(avatar, skillId, ammoSkillId)

    def requestProjectileSkill(self, skillId, ammoSkillId, posHpr, timestamp, power):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if self is avatar and not self.air.battleMgr.requestSkillUse(avatar, skillId, ammoSkillId):
            self.notify.debug('Avatar %d cannot use projectile skill %d, ammo skill %d!' % (
                avatar.doId, skillId, ammoSkillId))

            return

        # the skill's recharge (or the cannon's reload) limits how often a projectile
        # may be used. an earlier one may still be in the air, or have landed in the
        # water which the client never tells us about (WeaponBase.__waterHit)...
        timestamp = globalClockDelta.getRealNetworkTime(bits=32)
        self.air.targetMgr.removeProjectile(avatar.doId, skillId, ammoSkillId)
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
            # the result includes every target in the area of the projectile's impact...
            self.useProjectileSkill(avatar, target, skillId, ammoSkillId, result, targetId, areaIdList, pos, normal, codes, timestamp)
        else:
            # handle projectile skill results for ships and shipparts:
            cannonCode, hullCode, sailCode = codes
            if WeaponGlobals.getIsGrappleSkill(skillId, ammoSkillId):
                # grappling hooks don't do any damage, they land on one of the
                # grapple targets of a crippled flagship (the sail code is the target index):
                if hasattr(target, 'handleGrappleHit'):
                    target.handleGrappleHit(avatar, sailCode)

                self.air.targetMgr.removeProjectile(avatar.doId, skillId, ammoSkillId)
                return

            # the client rolled the hit with a new seed, see WeaponBase.__shippartHit...
            self.air.battleMgr.advanceAttackSeed(avatar)
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

    def useTargetedSkill(self, avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge, clientResult=None):
        targetResult = self.air.battleMgr.getTargetedSkillResult(avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge,
            clientResult=clientResult)

        if not targetResult:
            self.notify.debug('Cannot get targeted skill, no valid result was given; '
                'avatarId=%d, skillId=%d!' % (avatar.doId, skillId))

            return

        self.sendUpdate('useTargetedSkill', targetResult)

    def useProjectileSkill(self, avatar, target, skillId, ammoSkillId, result, targetId, areaIdList, pos, normal, codes, timestamp):
        targetResult = self.air.battleMgr.getTargetedSkillResult(avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos,
            clientResult=result)

        if not targetResult:
            self.notify.debug('Cannot get projectile targeted skill, '
                'no valid result was given; avatarId=%d, skillId=%d!' % (avatar.doId, skillId))

            return

        skillId, ammoSkillId, skillResult, targetDoId, areaIdList, attackerEffects, targetEffects, \
            areaIdEffects, timestamp, pos, charge = targetResult

        self.sendUpdate('setProjectileSkillResult', [skillId, ammoSkillId, skillResult, targetId if not target else target.doId,
            areaIdList, attackerEffects, targetEffects, areaIdEffects, pos, normal, codes, avatar.doId, timestamp])
