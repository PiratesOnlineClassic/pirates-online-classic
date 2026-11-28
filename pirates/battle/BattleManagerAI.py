import random
import time
import collections

from panda3d.core import *

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta

from pirates.battle.BattleManagerBase import BattleManagerBase
from pirates.piratesbase import PiratesGlobals
from pirates.battle import WeaponGlobals
from pirates.battle import EnemyGlobals
from pirates.battle import LootGlobals
from pirates.battle import WeaponConstants
from pirates.uberdog import UberDogGlobals
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType, InventoryCategory
from pirates.battle.ComboDiaryAI import ComboDiaryAI
from pirates.piratesbase import Freebooter
from pirates.pirate import AvatarTypes
from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI
from pirates.piratesbase import Freebooter
from pirates.interact.DistributedInteractivePropAI import DistributedInteractivePropAI


class PendingSkillEffect(object):

    def __init__(self, effectId, skillId, ammoSkillId, duration, attacker, target):
        self.effectId = effectId
        self.skillId = skillId
        self.ammoSkillId = ammoSkillId
        self.duration = duration
        self.timestamp = time.time()

        self.attacker = attacker
        self.target = target


class BattleManagerAI(BattleManagerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleManagerAI')

    # an attacker is only removed from it's target once it has moved this
    # far beyond the range of the last skill it used on the target. melee
    # weapons have a very short range, so without this leeway an attacker
    # stepping back from it's target would lose all it's earned reputation...
    AttackerDisengageRange = WeaponGlobals.LONG_RANGE

    # the skill ranges that are ranked through the avatar's inventory,
    # a skill must be learned before the avatar may use it...
    RankedSkillRanges = (
        (InventoryType.begin_WeaponSkillMelee, InventoryType.end_WeaponSkillMelee),
        (InventoryType.begin_WeaponSkillCutlass, InventoryType.end_WeaponSkillCutlass),
        (InventoryType.begin_WeaponSkillPistol, InventoryType.end_WeaponSkillPistol),
        (InventoryType.begin_WeaponSkillMusket, InventoryType.end_WeaponSkillMusket),
        (InventoryType.begin_WeaponSkillDagger, InventoryType.end_WeaponSkillDagger),
        (InventoryType.begin_WeaponSkillGrenade, InventoryType.end_WeaponSkillGrenade),
        (InventoryType.begin_WeaponSkillDoll, InventoryType.end_WeaponSkillDoll),
        (InventoryType.begin_WeaponSkillWand, InventoryType.end_WeaponSkillWand),
        (InventoryType.begin_WeaponSkillBayonet, InventoryType.end_WeaponSkillBayonet))

    # skills which are always available to the avatar's weapon,
    # the combat tray uses these without the skill ever being learned...
    UnrankedSkills = (InventoryType.MeleePunch,)

    def __init__(self, air):
        self.air = air

        self._pendingSkillEffects = collections.deque()
        self._removedPendingSkillEffects = collections.deque()

        self.__updateSkillEffectsTask = taskMgr.doMethodLater(1.0, self._updateSkillEffects,
            'BattleManagerAI-updateSkillEffects')

    def getTargetInRange(self, attacker, target, skillId, ammoSkillId):
        tolerance = 0
        attackRange = self.getModifiedAttackRange(attacker, skillId, ammoSkillId)
        if attackRange == WeaponGlobals.INF_RANGE:
            return True

        distance = self.getRelativePosition(attacker, target)
        if distance <= attackRange + tolerance:
            return True

        return False

    def getRelativePosition(self, attacker, target):
        targetParent = target.getParentObj()
        if not targetParent:
            return 0

        targetNP = NodePath('psuedo-target-%d' % target.doId)
        targetNP.setPosHpr(targetParent, target.getPos(), target.getHpr())

        attackerNP = NodePath('psuedo-attacker-%d' % attacker.doId)
        attackerNP.setPosHpr(targetParent, attacker.getPos(), attacker.getHpr())

        return attackerNP.getDistance(targetNP)

    def getIsWeaponAmmo(self, ammoId):
        if not ammoId:
            return False

        if ammoId >= InventoryType.begin_WeaponPistolAmmo and ammoId <= InventoryType.end_WeaponPistolAmmo:
            return True
        elif ammoId >= InventoryType.begin_WeaponGrenadeAmmo and ammoId <= InventoryType.end_WeaponGrenadeAmmo:
            return True
        elif ammoId >= InventoryType.begin_WeaponCannonAmmo and ammoId <= InventoryType.end_WeaponCannonAmmo:
            return True
        elif ammoId >= InventoryType.begin_WeaponDaggerAmmo and ammoId <= InventoryType.end_WeaponDaggerAmmo:
            return True

        return False

    def isRankedSkill(self, skillId):
        if not skillId or skillId in self.UnrankedSkills:
            return False

        for begin, end in self.RankedSkillRanges:
            if skillId >= begin and skillId < end:
                return True

        return False

    def isPlayerSkillHandledElsewhere(self, skillId):
        # ship and cannon skills are validated by the ship and cannon objects,
        # items are validated when the item itself is used...
        return skillId == InventoryType.UseItem or WeaponGlobals.getIsShipSkill(skillId) or \
            WeaponGlobals.getIsCannonSkill(skillId)

    def canUseSkill(self, avatar, skillId, ammoSkillId):
        if self.isPlayerSkillHandledElsewhere(skillId):
            return True

        if avatar.getHp()[0] <= 0:
            self.notify.debug('Avatar %d cannot use skill %d while defeated!' % (avatar.doId, skillId))
            return False

        currentWeaponId, isWeaponDrawn = avatar.getCurrentWeapon()
        if not isWeaponDrawn or not avatar.hasWeapon(currentWeaponId):
            self.notify.debug('Avatar %d cannot use skill %d, weapon %d is not drawn!' % (
                avatar.doId, skillId, currentWeaponId))

            return False

        repId = WeaponGlobals.getRepId(currentWeaponId)
        if not WeaponGlobals.isValidSkill(skillId, currentWeaponId, repId) or \
                not WeaponGlobals.isValidAttack(skillId, ammoSkillId, currentWeaponId, repId):
            self.notify.debug('Avatar %d cannot use skill %d, ammo skill %d with weapon %d!' % (
                avatar.doId, skillId, ammoSkillId, currentWeaponId))

            return False

        inventory = avatar.getInventory()
        if not inventory:
            self.notify.debug('Avatar %d cannot use skill %d, no inventory present!' % (avatar.doId, skillId))
            return False

        isPaid = avatar.isPaid()
        for usedSkillId in (skillId, ammoSkillId):
            if not self.isRankedSkill(usedSkillId):
                continue

            if inventory.getStackQuantity(usedSkillId) < 2:
                self.notify.debug('Avatar %d cannot use skill %d, skill was never learned!' % (
                    avatar.doId, usedSkillId))

                return False

            if not isPaid and not WeaponGlobals.canFreeUse(usedSkillId):
                self.notify.debug('Freebooter %d cannot use paid skill %d!' % (avatar.doId, usedSkillId))
                return False

        for usedSkillId in (skillId, ammoSkillId):
            if not usedSkillId or WeaponGlobals.isInfiniteAmmo(usedSkillId):
                continue

            ammoId = WeaponGlobals.getSkillAmmoInventoryId(usedSkillId)
            if ammoId and inventory.getStackQuantity(ammoId) < 1:
                self.notify.debug('Avatar %d cannot use skill %d, out of ammo %d!' % (
                    avatar.doId, usedSkillId, ammoId))

                return False

        mojoCost = -1 * WeaponGlobals.getMojoCost(skillId)
        if mojoCost > 0 and avatar.getMojo() < mojoCost:
            self.notify.debug('Avatar %d cannot use skill %d, not enough mojo!' % (avatar.doId, skillId))
            return False

        if avatar.isSkillRecharging(skillId, ammoSkillId):
            self.notify.debug('Avatar %d cannot use skill %d, skill is still recharging!' % (
                avatar.doId, skillId))

            return False

        return True

    def getSkillMojoCost(self, avatar, skillId, ammoSkillId):
        mojo = WeaponGlobals.getAttackEffects(skillId, ammoSkillId)[0][3]
        if mojo >= 0:
            return 0

        # voodoo users which have trained conservation spend less mojo,
        # see BattleManagerBase.getModifiedSkillEffects...
        inventory = avatar.getInventory()
        if inventory and WeaponGlobals.isVoodooWeapon(avatar.currentWeaponId):
            amt = max(0, inventory.getStackQuantity(InventoryType.StaffConservation) - 1) * \
                WeaponGlobals.getAttackSelfMojo(InventoryType.StaffConservation)

            mojo = min(mojo - mojo * amt, 0)

        return int(-mojo)

    def useSkillCosts(self, avatar, skillId, ammoSkillId):
        if self.isPlayerSkillHandledElsewhere(skillId):
            return

        inventory = avatar.getInventory()
        if inventory:
            for usedSkillId in (skillId, ammoSkillId):
                if not usedSkillId or WeaponGlobals.isInfiniteAmmo(usedSkillId):
                    continue

                ammoId = WeaponGlobals.getSkillAmmoInventoryId(usedSkillId)
                if not self.getIsWeaponAmmo(ammoId):
                    continue

                ammoAmt = inventory.getStackQuantity(ammoId)
                if ammoAmt > 0:
                    inventory.b_setStackQuantity(ammoId, ammoAmt - 1)

        mojoCost = self.getSkillMojoCost(avatar, skillId, ammoSkillId)
        if mojoCost:
            avatar.b_setMojo(max(0, avatar.getMojo() - mojoCost))

        avatar.startSkillRecharge(skillId)

    def requestSkillUse(self, avatar, skillId, ammoSkillId):
        # only player avatars have their skill usage validated, enemies
        # decide which skills they use themselves...
        if not isinstance(avatar, DistributedPlayerPirateAI):
            return True

        if not self.canUseSkill(avatar, skillId, ammoSkillId):
            return False

        self.useSkillCosts(avatar, skillId, ammoSkillId)
        return True

    def isPlayerDamageAllowed(self, avatar, target):
        # outside of pvp instances players cannot harm one another, unless
        # one of them has been cursed undead, see TeamUtils.friendOrFoe...
        if avatar.getZombie() or target.getZombie():
            return True

        return config.GetBool('want-friendly-fire', False)

    def getTargetedSkillResult(self, avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge=0):
        if not avatar:
            return None

        # tonics are used on the avatar itself and may be used without
        # any weapon drawn, they never effect the avatar's area targets...
        if skillId == InventoryType.UseItem and ammoSkillId in InventoryType.Potions:
            if target:
                return None

            return self._otherSkillResult(avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge)

        # ship repair kits are only available to privateers, the siege manager handles them...
        if skillId == InventoryType.UseItem and ammoSkillId == InventoryType.ShipRepairKit:
            if not self.air.siegeManager.useShipRepairKit(avatar, target):
                return None

            return self._otherSkillResult(avatar, None, skillId, ammoSkillId, areaIdList, timestamp, pos, charge)

        currentWeaponId, isWeaponDrawn = avatar.getCurrentWeapon()
        if not isWeaponDrawn:
            self.notify.debug('Cannot get skill result for avatar %d, '
                'weapon %d was never drawn!' % (avatar.doId, currentWeaponId))

            return None

        repId = WeaponGlobals.getRepId(currentWeaponId)
        if not WeaponGlobals.isValidSkill(skillId, currentWeaponId, repId):
            self.notify.debug('Cannot get skill result for avatar %d, '
                'invalid skill %d used for weapon %d!' % (avatar.doId, skillId, currentWeaponId))

            return None

        if not WeaponGlobals.isValidAttack(skillId, ammoSkillId, currentWeaponId, repId):
            self.notify.debug('Cannot get skill result for avatar %d, '
                'invalid attack skill %d, ammo skill: %d used for weapon %d!' % (avatar.doId, skillId, ammoSkillId, currentWeaponId))

            return None

        # the skill's ammo and mojo were spent when the skill was requested,
        # see requestSkillUse...

        # this is just the client requesting an action for the skill used,
        # they are not actually attacking any kind of target...
        if not target:
            return self._otherSkillResult(avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge)

        # the client requested a valid skill result, attempt to calculate
        # the result for the client and send the result back...
        return self._skillResult(avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge)

    def _skillResult(self, avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge):
        currentWeaponId, isWeaponDrawn = avatar.getCurrentWeapon()
        if not isWeaponDrawn:
            self.notify.debug('Cannot get skill result for avatar %d, '
                'weapon %d was never drawn!' % (avatar.doId, currentWeaponId))

            return None

        # ensure the user has access to the requested weapon before
        # running result calculations
        repId = WeaponGlobals.getRepId(currentWeaponId)
        if hasattr(avatar, 'isPaid'):
            if not avatar.isPaid() and not Freebooter.allowedFreebooterWeapon(repId):
                self.notify.warning('Freebooter (%d) attempted to use paid weapon (%d)' % (avatar.doId, currentWeaponId))
                return None

        # ensure the avatar that has sent this skill request obeys
        # the pirate code and can use the weapon on the target...
        obeysPirateCode = self.obeysPirateCode(avatar, target)
        if not obeysPirateCode:
            self.notify.debug('Cannot get skill result for avatar %d, '
                'does not obey pirate code!' % (avatar.doId))

            return None

        # pvp instances decide which players may damage one another...
        if isinstance(avatar, DistributedPlayerPirateAI) and isinstance(target, DistributedPlayerPirateAI):
            world = target.getWorld()
            if world and world.getType() == PiratesGlobals.INSTANCE_PVP:
                if not WeaponGlobals.isFriendlyFire(skillId, ammoSkillId):
                    if not world.isDamageAllowed(avatar, target):
                        return None

                    world.avatarAttacked(avatar, target)
            elif not WeaponGlobals.isFriendlyFire(skillId, ammoSkillId):
                if not self.isPlayerDamageAllowed(avatar, target):
                    self.notify.debug('Cannot get skill result for avatar %d, '
                        'cannot damage player %d outside of pvp!' % (avatar.doId, target.doId))

                    return None

        skillResult = self.willWeaponHit(avatar, target, skillId, ammoSkillId, charge)
        distance = self.getRelativePosition(avatar, target)
        timestamp = globalClockDelta.getRealNetworkTime(bits=32)

        # check to see if our dictionary of target to attacker data contains this attacker,
        # if not we will assume this is a new attacker to the target and assign them accordingly...
        if not self.air.targetMgr.hasTarget(avatar.doId) and not self.air.targetMgr.hasAttacker(avatar.doId, target.doId):
            self.air.targetMgr.addAttacker(avatar, target)

        # add the skill info to the attackers battle skill diary to track
        # what skills they have used and when...
        if not avatar.battleSkillDiary.hasSkill(skillId):
            avatar.battleSkillDiary.addSkill(timestamp, skillId, ammoSkillId)

        # calculate the moddified skill result for this skill, add this including
        # the attack data according to which ever weapon the avatar is using...
        if WeaponGlobals.isBladedWeapon(currentWeaponId):
            attackerEffects, targetEffects = self.getModifiedSkillEffectsSword(avatar, target, skillId, ammoSkillId, charge, distance)
        else:
            attackerEffects, targetEffects = self.getModifiedSkillEffects(avatar, target, skillId, ammoSkillId, charge, distance)

        areaIdEffects = [
            attackerEffects,
            targetEffects
        ]

        if skillResult == WeaponGlobals.RESULT_NOT_AVAILABLE:
            self.notify.debug('Cannot get skill result for avatar %d, '
                'skill %d result was not available!' % (avatar.doId, skillId))

            return None
        elif skillResult == WeaponGlobals.RESULT_MISS:
            pass
        elif skillResult == WeaponGlobals.RESULT_DODGE:
            pass
        elif skillResult in [WeaponGlobals.RESULT_HIT, WeaponGlobals.RESULT_PARRY, WeaponGlobals.RESULT_RESIST]:
            # update this skills current reputation, this will eventually add up
            # and all skills used will be rewarded reputation...
            skillData = avatar.battleSkillDiary.getSkill(skillId)
            if not skillData:
                return None

            # only update the experience for avatar's, enemies do not need experience...
            if isinstance(avatar, DistributedPlayerPirateAI):
                experience = self.getModifiedAttackReputation(avatar, target, skillId, ammoSkillId)
                if self.air.newsManager.isHolidayActive(PiratesGlobals.DOUBLEXPHOLIDAY) or avatar.hasTempDoubleXPReward():
                    experience *= 2
                elif self.air.newsManager.isHolidayActive(PiratesGlobals.DOUBLEXPHOLIDAYPAID) and avatar.isPaid():
                    experience *= 2

                skillData[2] += experience

            # check to see if the avatar knows of any skills that are valid combos,
            # recent attacks are measured within a certain time frame...
            totalCombo, totalDamage, numAttackers = avatar.comboDiary.getCombo()
            if totalCombo and numAttackers > 1:
                # apply the combo damage including the combo bonus damage to the
                # target, then broadcast the combo info to all targets with interest...
                targetEffects[0] = totalDamage + WeaponGlobals.getComboBonus(numAttackers)
                target.b_setCombo(totalCombo, numAttackers, targetEffects[0], avatar.doId)

            # update the avatar's combo diary so we can determine if any other attacks
            # made by avatars attacking the avatar's current target is a combo...
            for attackerDoId in self.air.targetMgr.getAttackers(target.doId):
                attacker = self.air.doId2do.get(attackerDoId)
                if not attacker:
                    continue

                attacker.comboDiary.recordAttack(avatar.doId, skillId, targetEffects[0])

            # players have already spent the mojo this skill costs, when the
            # skill was requested. don't charge them for it a second time...
            appliedAttackerEffects = attackerEffects
            if isinstance(avatar, DistributedPlayerPirateAI) and attackerEffects[3] < 0:
                appliedAttackerEffects = list(attackerEffects)
                appliedAttackerEffects[3] = 0

            # when the skill result is parry, this means that we've reversed the
            # attack our attacker has done to us onto them
            appliedTargetEffects = targetEffects
            if skillResult == WeaponGlobals.RESULT_PARRY:
                prevTargetEffects = targetEffects
                prevAttackerEffects = attackerEffects

                targetEffects = prevAttackerEffects
                attackerEffects = prevTargetEffects

                appliedTargetEffects = appliedAttackerEffects
                appliedAttackerEffects = prevTargetEffects

            # apply the target effects to both the target and attacker
            self.applyTargetEffects(target, appliedTargetEffects)
            self.applyTargetEffects(avatar, appliedAttackerEffects)

            # add skill effects for both attacker and target, this will also
            # check to see if the attacker or target can be damaged...
            self.applySkillEffect(target, targetEffects, avatar, skillId, ammoSkillId)
            self.applySkillEffect(avatar, attackerEffects, avatar, skillId, ammoSkillId)

            # check to see if the skill used by the avatar was the doll attuning effect,
            # and that the avatar's current weapon is infact an doll weapon...
            if WeaponGlobals.isVoodooWeapon(currentWeaponId) and skillId == InventoryType.DollAttune:
                avatar.addStickyTarget(target.doId)

                # set the target's skill effect so that the attuning effect is
                # present, this will also set the avatar's local attune list...
                target.addSkillEffect(WeaponGlobals.C_ATTUNE, 0, avatar.doId)

            # handle interactive props
            if isinstance(target, DistributedInteractivePropAI):
                target.d_propSlashed()
        else:
            self.notify.debug('Cannot get skill result for avatar %d, '
                'unknown skill result %d for skill %d!' % (avatar.doId, skillResult, skillId))

            return None

        return [skillId, ammoSkillId, skillResult, target.doId, areaIdList, attackerEffects, targetEffects,
            areaIdEffects, timestamp, pos, charge]

    def _otherSkillResult(self, avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge):
        # since this skill doesn't have a target we cannot set an effect for it,
        # just send some "place holder" data to satisfy the dc field...
        attackerEffects = [
            0,
            0,
            0,
            0,
            0]

        targetEffects = [
            0,
            0,
            0,
            0,
            0]

        areaIdEffects = [
            attackerEffects,
            targetEffects
        ]

        if skillId == InventoryType.UseItem:
            if ammoSkillId in UberDogGlobals.InventoryType.Potions:
                if not avatar.useTonic(ammoSkillId):
                    return None
        else:
            currentWeaponId, isWeaponDrawn = avatar.getCurrentWeapon()
            if not isWeaponDrawn:
                self.notify.debug('Cannot get other skill result for avatar %d, '
                    'weapon %d was never drawn!' % (avatar.doId, currentWeaponId))

                return None

        return [skillId, ammoSkillId, WeaponGlobals.RESULT_HIT, 0, areaIdList, attackerEffects, targetEffects,
            areaIdEffects, timestamp, pos, charge]

    def applyTargetEffects(self, target, targetEffects):
        if not target.getDamagable():
            return

        # Jack is immortal, cannot kill an already dead monkey D:
        if target.getAvatarType() == AvatarTypes.Monkey:
            return

        target.b_setHp(max(0, min(target.getHp()[0] + targetEffects[0], target.getMaxHp())))
        target.b_setPower(max(0, min(target.getPower() + targetEffects[1], target.getMaxPower())))
        target.b_setLuck(max(0, min(target.getLuck() + targetEffects[2], target.getMaxLuck())))
        target.b_setMojo(max(0, min(target.getMojo() + targetEffects[3], target.getMaxMojo())))
        target.b_setSwiftness(max(0, min(target.getSwiftness() + targetEffects[4], target.getMaxSwiftness())))

    def appendSkillEffect(self, pendingSkillEffect):
        if pendingSkillEffect in self._pendingSkillEffects:
            return

        self._pendingSkillEffects.append(pendingSkillEffect)

    def removePendingSkillEffect(self, effectId):
        if effectId in self._removedPendingSkillEffects:
            return

        if effectId == WeaponGlobals.C_ATTUNE:
            return

        self._removedPendingSkillEffects.append(effectId)

    def getPendingSkillEffect(self, effectId):
        for pendingSkillEffect in list(self._pendingSkillEffects):
            if pendingSkillEffect.effectId == effectId:
                return pendingSkillEffect

        return None

    def applySkillEffect(self, target, targetEffects, attacker, skillId, ammoSkillId):
        targetEffectId = targetEffects[2]
        if not targetEffectId or targetEffectId == WeaponGlobals.C_ATTUNE:
            return

        if isinstance(target, DistributedInteractivePropAI):
            # Dont apply skill effects for props
            return

        # cannot apply a skill effect to the monkey
        if target.getAvatarType() == AvatarTypes.Monkey:
            return

        effectAttackDuration = WeaponGlobals.getAttackDuration(skillId, ammoSkillId)
        maxEffectStack = WeaponGlobals.getBuffStackNumber(targetEffectId)
        if not target.getDamagable():
            return

        # make sure the avatar does not already have too many of these skill effects applied
        if target.getSkillEffectCount(targetEffectId) >= maxEffectStack:
            return

        # add the skill effect to the avatar's list of skill effects which will be sent to the client
        target.addSkillEffect(targetEffectId, effectAttackDuration, attacker.doId)

        # store a pending skill effect so we can apply it's effects to the target,
        # and remove the skill effect from the target when it expires:
        pendingSkillEffect = PendingSkillEffect(targetEffectId, skillId, ammoSkillId, effectAttackDuration, attacker, target)
        self.appendSkillEffect(pendingSkillEffect)

    def _updateSkillEffect(self, pendingSkillEffect):
        assert(pendingSkillEffect is not None)

        attacker = pendingSkillEffect.attacker
        assert(attacker is not None)

        target = pendingSkillEffect.target
        assert(target is not None)

        if target.getHp()[0] <= 0:
            target.b_setSkillEffects([])
            return False

        # check to see if the skill effect has expired
        currentTime = globalClockDelta.getFrameNetworkTime()
        if time.time() - pendingSkillEffect.timestamp >= pendingSkillEffect.duration:
            target.removeSkillEffect(pendingSkillEffect.effectId)
            return False

        if pendingSkillEffect.effectId in [WeaponConstants.C_FLAMING,
                                           WeaponConstants.C_ON_FIRE,
                                           WeaponConstants.C_WOUND,
                                           WeaponConstants.C_ACID,
                                           WeaponConstants.C_POISON,
                                           WeaponConstants.C_REGEN,
                                           WeaponConstants.C_STUN,
                                           WeaponConstants.C_HOLD]:

            skillEffects = WeaponGlobals.getEffects(pendingSkillEffect.effectId)
            self.applyTargetEffects(target, skillEffects)
        else:
            try:
                skillEffects = self.getModifiedSkillEffects(attacker, target, pendingSkillEffect.skillId, pendingSkillEffect.ammoSkillId)
            except:
                return False

            if skillEffects is not None:
                self.applyTargetEffects(target, skillEffects[0])

        return True

    def _updateSkillEffects(self, task):
        for _ in range(len(self._removedPendingSkillEffects)):
            effectId = self._removedPendingSkillEffects.popleft()
            assert(effectId != WeaponGlobals.C_ATTUNE)

            pendingSkillEffect = self.getPendingSkillEffect(effectId)
            if pendingSkillEffect is not None:
                target = pendingSkillEffect.target
                assert(target is not None)

                if pendingSkillEffect in self._pendingSkillEffects:
                    self._pendingSkillEffects.remove(pendingSkillEffect)
                    target.removeSkillEffect(pendingSkillEffect.effectId)

        for _ in range(len(self._pendingSkillEffects)):
            pendingSkillEffect = self._pendingSkillEffects.popleft()
            assert(pendingSkillEffect is not None)

            if self._updateSkillEffect(pendingSkillEffect):
                self._pendingSkillEffects.append(pendingSkillEffect)

        return task.again

    def updateTarget(self, targetId, attackers):
        target = self.air.doId2do.get(targetId)
        if not target:
            return

        for attackerId in list(attackers):
            attacker = self.air.doId2do.get(attackerId)
            if not attacker:
                continue

            self.__checkAttacker(attacker, target)

    def __checkAttacker(self, attacker, target):
        # check to see if the avatar's recent recorded combos are expired,
        # if they are removed them from the combo diary...
        combos = attacker.comboDiary.getCombos(attacker.doId)
        for combo in combos:
            skillId = combo[ComboDiaryAI.SKILLID_INDEX]
            if attacker.comboDiary.checkComboExpired(attacker.doId, skillId):
                attacker.comboDiary.removeCombo(attacker.doId, skillId)

        # check to see if the avatar doesn't have anymore combos
        # that are not expired, if so clear the combo diary...
        if len(combos) == 0:
            attacker.comboDiary.clear()

        # check the current weapon skill and determine if the avatar is still in
        # range that they may still be able to use that weapon in battle...
        skillId = attacker.battleSkillDiary.getCurrentSkill()
        if not skillId:
            return

        skillData = attacker.battleSkillDiary.getSkill(skillId)
        if not skillData:
            return

        # now that we have the avatar's current skill, check the range of,
        # that specific weapon. the attacker is only considered to have left
        # the battle once it is well beyond the range of it's weapon...
        ammoSkillId, timestamp, reputation = skillData
        attackRange = self.getModifiedAttackRange(attacker, skillId, ammoSkillId)
        if attackRange == WeaponGlobals.INF_RANGE:
            return

        distance = self.getRelativePosition(attacker, target)
        if distance > attackRange + self.AttackerDisengageRange:
            self.air.targetMgr.removeAttacker(attacker, target)

    def clearAttacker(self, target, attacker):
        assert(target is not None)
        assert(attacker is not None)

        # remove the doll attuning when out of range.
        if attacker.hasStickyTarget(target.doId):
            attacker.removeSkillEffect(WeaponGlobals.C_ATTUNE)
            attacker.removeStickyTarget(target.doId)

        # clear the avatar's skill diaries
        attacker.battleSkillDiary.clear()
        attacker.comboDiary.clear()

    def rewardAttackers(self, target):
        attackers = self.air.targetMgr.getAttackers(target.doId)
        for attackerId in list(attackers):
            attacker = self.air.doId2do.get(attackerId)
            if not attacker:
                # the attacker has since left the district
                continue

            self.rewardAttacker(attacker, target)

    def rewardAttacker(self, attacker, target):
        if not isinstance(attacker, DistributedPlayerPirateAI):
            # only players are rewarded for defeating an enemy
            return

        inventory = attacker.getInventory()
        if not inventory:
            self.notify.warning('Cannot reward attacker %d for defeating %d, '
                'no inventory present!' % (attacker.doId, target.doId))

            return

        # Verify the user has not exceeded the level cap
        if hasattr(attacker, 'isPaid'):
            if not attacker.isPaid() and attacker.getLevel() >= Freebooter.FreeOverallLevelCap:
                return

        overallReputation = 0
        reputationCategories = {}
        dropMultiplier = 1
        if hasattr(target, 'getGoldScale'):
            dropMultiplier = target.getGoldScale()

        goldReward = EnemyGlobals.getGoldDrop(target.getAvatarType(), target.getLevel(), dropMultiplier)

        for skillId in attacker.battleSkillDiary.getSkills():
            ammoSkillId, timestamp, reputation = attacker.battleSkillDiary.getSkill(skillId)
            reputationCategoryId = WeaponGlobals.getSkillReputationCategoryId(skillId)
            reputation = int(reputation)

            # update the avatar's skill reputation for each skill it used to kill the target,
            # adding onto the overall reputation rewarded
            overallReputation += reputation
            inventory.setReputation(reputationCategoryId, inventory.getReputation(reputationCategoryId) + reputation)
            reputationCategories[reputationCategoryId] = reputationCategories.get(reputationCategoryId, 0) + reputation

        # update the avatar's overall reputation based on all the skills they
        # used to kill the target
        inventory.setOverallRep(inventory.getOverallRep() + overallReputation)
        inventory.addGoldInPocket(goldReward)

        # let the client know how much reputation they've earned so they can
        # display the reputation text above the defeated enemy...
        if overallReputation > 0:
            categories = [categoryId for categoryId in reputationCategories if categoryId]
            reputationList = [min(reputationCategories[categoryId], 65535) for categoryId in categories]
            attacker.d_sendReputationMessage(target.doId, categories, reputationList, 0, 0, 0, 0)

        if random.random() < LootGlobals.CARD_DROP_CHANCE:
            cardId = random.randint(InventoryType.begin_Cards, InventoryType.end_Cards - 1)
            inventory.giveCards(cardId, 1)

        # enemies also carry the pieces of the treasure collections the
        # avatar has started, see CollectionMap.Collection_Found...
        if random.random() < LootGlobals.COLLECTION_DROP_CHANCE:
            itemId = LootGlobals.getCollectionDrop(target.getAvatarType(), inventory)
            if itemId:
                inventory.giveCollectionItem(itemId)

        # attempt to update the avatar's active task progress...
        self.air.questMgr.enemyDefeated(attacker, target)
