import random

from panda3d.core import *

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta

from pirates.battle.BattleManagerBase import BattleManagerBase
from pirates.piratesbase import FreebooterAI
from pirates.piratesbase import PiratesGlobals
from pirates.battle import WeaponGlobals
from pirates.battle import EnemyGlobals
from pirates.battle import LootGlobals
from pirates.uberdog import UberDogGlobals
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType, InventoryCategory
from pirates.battle.ComboDiaryAI import ComboDiaryAI
from pirates.pirate import AvatarTypes
from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI
from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from pirates.interact.DistributedInteractivePropAI import DistributedInteractivePropAI


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
        # stunned avatars cannot use any skill, see CombatTray.trySkill...
        if WeaponGlobals.C_STUN in self.getSkillEffectIds(avatar):
            self.notify.debug('Avatar %d cannot use skill %d while stunned!' % (avatar.doId, skillId))
            return False

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

        for usedSkillId in (skillId, ammoSkillId):
            if not self.isRankedSkill(usedSkillId):
                continue

            if inventory.getStackQuantity(usedSkillId) < 2:
                self.notify.debug('Avatar %d cannot use skill %d, skill was never learned!' % (
                    avatar.doId, usedSkillId))

                return False

            if not FreebooterAI.canUseSkill(avatar, usedSkillId):
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
        # one of them has been cursed undead, see TeamUtils.friendOrFoe:
        # players on pvp or siege teams only fight the other team though...
        friendlyFire = config.GetBool('want-friendly-fire', False)
        for teamGetter in ('getPVPTeam', 'getSiegeTeam'):
            try:
                avatarTeam = getattr(avatar, teamGetter)()
                targetTeam = getattr(target, teamGetter)()
            except AttributeError:
                continue

            if avatarTeam and targetTeam:
                return avatarTeam != targetTeam or friendlyFire

        if avatar.getZombie() or target.getZombie():
            return True

        return friendlyFire

    def advanceAttackSeed(self, avatar):
        # the attacking client advances the attacker's battle random once for every
        # attack it predicts (see BattleManager.doAttack) and then rolls the attack's
        # accuracy and damage in a fixed order. advancing it once per request here
        # as well gives the exact same rolls, so the damage the client displays is
        # the damage we deal...
        battleRandom = getattr(avatar, 'battleRandom', None)
        if battleRandom:
            battleRandom.advanceAttackSeed()

    def resyncBattleRandom(self, avatar):
        # the client advances it's battle random for attacks it never sends us
        # (e.g. on friendly targets), once the results we roll differ from the
        # client's both sides are reset to the avatar's initial seed...
        battleRandom = getattr(avatar, 'battleRandom', None)
        if not battleRandom:
            return

        battleRandom.resync()
        if isinstance(avatar, DistributedPlayerPirateAI):
            avatar.sendUpdateToAvatarId(avatar.doId, 'battleRandomSync', [])

    def getTargetedSkillResult(self, avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge=0,
                               clientResult=None):
        if not avatar:
            return None

        # every attack the client requests was rolled with a newly advanced seed...
        self.advanceAttackSeed(avatar)

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

        # the client requested a valid skill result, calculate the result for
        # the skill's target and all of it's area targets and send it back...
        return self._skillResult(avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge, clientResult)

    def canAttackTarget(self, avatar, target, skillId, ammoSkillId):
        # ensure the avatar that has sent this skill request obeys
        # the pirate code and can use the weapon on the target...
        if not self.obeysPirateCode(avatar, target):
            self.notify.debug('Cannot get skill result for avatar %d, '
                'does not obey pirate code!' % (avatar.doId))

            return False

        # pvp instances decide which players may damage one another...
        if isinstance(avatar, DistributedPlayerPirateAI) and isinstance(target, DistributedPlayerPirateAI):
            world = target.getWorld()
            if world and world.getType() == PiratesGlobals.INSTANCE_PVP:
                if not WeaponGlobals.isFriendlyFire(skillId, ammoSkillId):
                    if not world.isDamageAllowed(avatar, target):
                        return False

                    world.avatarAttacked(avatar, target)
            elif not WeaponGlobals.isFriendlyFire(skillId, ammoSkillId):
                if not self.isPlayerDamageAllowed(avatar, target):
                    self.notify.debug('Cannot get skill result for avatar %d, '
                        'cannot damage player %d outside of pvp!' % (avatar.doId, target.doId))

                    return False

        return True

    def isAreaTargetValid(self, avatar, target, skillId, ammoSkillId):
        # the client only lists the targets around the skill's target, see
        # WeaponBaseBase.getAreaList; the attacker is only listed when the
        # skill damages it's own user...
        if target is avatar:
            return bool(WeaponGlobals.isAttackAreaSelfDamaging(skillId, ammoSkillId))

        if isinstance(target, DistributedInteractivePropAI):
            return True

        if target.getHp()[0] <= 0:
            return False

        if WeaponGlobals.getIsDollAttackSkill(skillId):
            # hexes only effect the targets the doll is attuned to...
            if isinstance(avatar, DistributedPlayerPirateAI) and not avatar.hasStickyTarget(target.doId):
                return False
        elif not self.isInSkillArea(avatar, target, skillId, ammoSkillId):
            return False

        return self.canAttackTarget(avatar, target, skillId, ammoSkillId)

    # the leeway given to the area of a skill, positions are not exact...
    AreaTolerance = WeaponGlobals.AI_AOE_RANGE_TOLERANCE * 2

    def isInSkillArea(self, avatar, target, skillId, ammoSkillId):
        if WeaponGlobals.getAttackAreaShape(skillId, ammoSkillId) == WeaponGlobals.AREA_OFF:
            return False

        attackRange = self.getModifiedAttackRange(avatar, skillId, ammoSkillId)
        if attackRange == WeaponGlobals.INF_RANGE:
            return True

        # the area is centered around the skill's target which is within the skill's
        # range, or spans the skill's range for tubes and cones...
        maxDistance = attackRange + self.getModifiedAttackAreaRadius(avatar, skillId, ammoSkillId) + self.AreaTolerance
        return self.getRelativePosition(avatar, target) <= maxDistance

    def getAttackResult(self, avatar, target, skillId, ammoSkillId, areaIdList, charge):
        # mirrors the client's prediction, see BattleManager.doAttack...
        spawnProtected = target is not None and WeaponGlobals.C_SPAWN in self.getSkillEffectIds(target)
        if spawnProtected and not WeaponGlobals.getIsShipSkill(skillId) and not WeaponGlobals.getIsDollAttackSkill(skillId):
            return WeaponGlobals.RESULT_MISS

        skillResult = self.willWeaponHit(avatar, target, skillId, ammoSkillId, charge)
        if skillResult == WeaponGlobals.RESULT_NOT_AVAILABLE:
            return skillResult

        if not WeaponGlobals.getNeedTarget(skillId, ammoSkillId):
            return WeaponGlobals.RESULT_HIT

        if not target and not areaIdList:
            return WeaponGlobals.RESULT_MISS

        if target is not None:
            # enemies breaking combat are returning to their spawn and cannot be hit...
            gameFSM = getattr(target, 'gameFSM', None)
            if getattr(target, 'isNpc', False) and gameFSM and gameFSM.getCurrentOrNextState() == 'BreakCombat':
                return WeaponGlobals.RESULT_MISS

            if spawnProtected:
                return WeaponGlobals.RESULT_MISS

        return skillResult

    # the results the client predicts by rolling the battle random...
    RolledResults = (
        WeaponGlobals.RESULT_MISS,
        WeaponGlobals.RESULT_HIT,
        WeaponGlobals.RESULT_PARRY,
        WeaponGlobals.RESULT_DODGE,
        WeaponGlobals.RESULT_RESIST)

    # the results of attacks the client already knows never landed...
    ClientMissedResults = (
        WeaponGlobals.RESULT_OUT_OF_RANGE,
        WeaponGlobals.RESULT_AGAINST_PIRATE_CODE)

    def _skillResult(self, avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge, clientResult=None):
        currentWeaponId, isWeaponDrawn = avatar.getCurrentWeapon()
        if not isWeaponDrawn:
            self.notify.debug('Cannot get skill result for avatar %d, '
                'weapon %d was never drawn!' % (avatar.doId, currentWeaponId))

            return None

        # ensure the user has access to the requested weapon before
        # running result calculations
        repId = WeaponGlobals.getRepId(currentWeaponId)
        if not FreebooterAI.canUseWeapon(avatar, repId):
            self.notify.warning('Freebooter (%d) attempted to use paid weapon (%d)' % (avatar.doId, currentWeaponId))
            return None

        if target is not None and not self.canAttackTarget(avatar, target, skillId, ammoSkillId):
            return None

        # the client lists at most MAX_AREA_TARGETS area targets, see WeaponBaseBase.getAreaList...
        areaTargets = []
        for areaId in list(areaIdList)[:WeaponGlobals.MAX_AREA_TARGETS]:
            if target is not None and areaId == target.doId:
                continue

            areaTarget = self.air.doId2do.get(areaId)
            if isinstance(areaTarget, (DistributedBattleAvatarAI, DistributedInteractivePropAI)):
                areaTargets.append(areaTarget)

        # this is just the client requesting an action for the skill used,
        # they are not actually attacking any kind of target...
        if target is None and not areaTargets:
            return self._otherSkillResult(avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge)

        # roll the attack in the same order the attacking client does, see
        # BattleManager.doAttack and LocalPirate.composeRequestTargetedSkill...
        skillResult = self.getAttackResult(avatar, target, skillId, ammoSkillId, areaTargets, charge)
        if skillResult == WeaponGlobals.RESULT_NOT_AVAILABLE:
            self.notify.debug('Cannot get skill result for avatar %d, '
                'skill %d result was not available!' % (avatar.doId, skillId))

            return None

        primaryTarget = target
        if primaryTarget is None and isinstance(getattr(avatar, 'currentTarget', None), DistributedBattleAvatarAI):
            primaryTarget = avatar.currentTarget

        attackerEffects, targetEffects = self.getModifiedSkillEffects(avatar, primaryTarget, skillId, ammoSkillId, charge)
        if target is None:
            targetEffects = [0, 0, 0, 0, 0]

        resultAreaIdList = []
        areaIdEffects = []
        areaHits = []
        for areaTarget in areaTargets:
            areaEffects = self.getModifiedSkillEffects(avatar, areaTarget, skillId, ammoSkillId, charge)[1]
            if not self.isAreaTargetValid(avatar, areaTarget, skillId, ammoSkillId):
                continue

            resultAreaIdList.append(areaTarget.doId)
            areaIdEffects.append(areaEffects)
            areaHits.append((areaTarget, areaEffects))

        if clientResult in self.RolledResults and skillResult in self.RolledResults and clientResult != skillResult:
            self.notify.debug('Avatar %d rolled %d for skill %d, we rolled %d!' % (
                avatar.doId, clientResult, skillId, skillResult))

            self.resyncBattleRandom(avatar)
        elif clientResult in self.ClientMissedResults:
            # the client never displayed the attack landing...
            skillResult = clientResult

        timestamp = globalClockDelta.getRealNetworkTime(bits=32)
        hitTargets = [target] if target is not None else []
        hitTargets += [areaTarget for areaTarget, areaEffects in areaHits]
        for hitTarget in hitTargets:
            # check to see if our dictionary of target to attacker data contains this attacker,
            # if not we will assume this is a new attacker to the target and assign them accordingly...
            if hitTarget is avatar or isinstance(hitTarget, DistributedInteractivePropAI):
                continue

            if not self.air.targetMgr.hasTarget(avatar.doId) and not self.air.targetMgr.hasAttacker(avatar.doId, hitTarget.doId):
                self.air.targetMgr.addAttacker(avatar, hitTarget)

        # add the skill info to the attackers battle skill diary to track
        # what skills they have used and when...
        if not avatar.battleSkillDiary.hasSkill(skillId):
            avatar.battleSkillDiary.addSkill(timestamp, skillId, ammoSkillId)

        if skillResult in (WeaponGlobals.RESULT_HIT, WeaponGlobals.RESULT_PARRY, WeaponGlobals.RESULT_RESIST):
            # update this skills current reputation, this will eventually add up
            # and all skills used will be rewarded reputation...
            skillData = avatar.battleSkillDiary.getSkill(skillId)
            if not skillData:
                return None

            # only update the experience for avatar's, enemies do not need experience...
            if isinstance(avatar, DistributedPlayerPirateAI) and hitTargets:
                experience = self.getModifiedAttackReputation(avatar, hitTargets[0], skillId, ammoSkillId)
                if self.air.newsManager.isHolidayActive(PiratesGlobals.DOUBLEXPHOLIDAY) or avatar.hasTempDoubleXPReward():
                    experience *= 2
                elif self.air.newsManager.isHolidayActive(PiratesGlobals.DOUBLEXPHOLIDAYPAID) and avatar.isPaid():
                    experience *= 2

                skillData[2] += experience

        if skillResult == WeaponGlobals.RESULT_HIT:
            if target is not None:
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

                self.applySkillHit(avatar, target, targetEffects, skillId, ammoSkillId)

            for areaTarget, areaEffects in areaHits:
                self.applySkillHit(avatar, areaTarget, areaEffects, skillId, ammoSkillId)

        # the attacking client displays the skill's effects on it's user no matter
        # the result (see LocalPirate.composeRequestTargetedSkill), players have
        # already spent the mojo this skill costs when the skill was requested...
        appliedAttackerEffects = list(attackerEffects)
        if isinstance(avatar, DistributedPlayerPirateAI) and appliedAttackerEffects[3] < 0:
            appliedAttackerEffects[3] = 0

        if skillResult in self.RolledResults and avatar.getHp()[0] > 0:
            self.applyTargetEffects(avatar, appliedAttackerEffects)

        return [skillId, ammoSkillId, skillResult, target.doId if target is not None else 0, resultAreaIdList,
            attackerEffects, targetEffects, areaIdEffects, timestamp, pos, charge]

    def applySkillHit(self, avatar, target, targetEffects, skillId, ammoSkillId):
        # handle interactive props
        if isinstance(target, DistributedInteractivePropAI):
            target.d_propSlashed()
            return

        self.applyTargetEffects(target, targetEffects)

        effectId = targetEffects[2]
        if effectId == WeaponGlobals.C_ATTUNE:
            # check to see if the skill used by the avatar was the doll attuning effect,
            # and that the avatar's current weapon is infact an doll weapon...
            if skillId == InventoryType.DollAttune and WeaponGlobals.isVoodooWeapon(avatar.currentWeaponId):
                self.attuneTarget(avatar, target)
        elif effectId == WeaponGlobals.C_BUFF_BREAK:
            self.breakHostileSkillEffects(target)
        else:
            self.applySkillEffect(target, effectId, avatar, skillId, ammoSkillId)

        # some skills shatter the target's voodoo attunements...
        if WeaponGlobals.getSkillUnattune(skillId):
            self.shatterAttunements(avatar, target, skillId, ammoSkillId)

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

        return [skillId, ammoSkillId, WeaponGlobals.RESULT_HIT, 0, [], attackerEffects, targetEffects,
            [], timestamp, pos, charge]

    def applyTargetEffects(self, target, targetEffects):
        if not target.getDamagable():
            return

        # Jack is immortal, cannot kill an already dead monkey D:
        if target.getAvatarType() == AvatarTypes.Monkey:
            return

        # the third effect is the skill's effect id (see WeaponGlobals.getAttackEffects),
        # luck is never changed by a skill...
        hp, power, effectId, mojo, swiftness = targetEffects
        if hp:
            target.b_setHp(max(0, min(target.getHp()[0] + int(hp), target.getMaxHp())))

        if power:
            target.b_setPower(max(0, min(target.getPower() + int(power), target.getMaxPower())))

        if mojo:
            target.b_setMojo(max(0, min(target.getMojo() + int(mojo), target.getMaxMojo())))

        if swiftness:
            target.b_setSwiftness(max(0, min(target.getSwiftness() + int(swiftness), target.getMaxSwiftness())))

    # the skill effect flags which are status effects the client's buff tray
    # and status visuals know of (see BuffIcon.buffTable), the other flags
    # only modify the attack itself (see BattleManagerBase.getModifiedSkillEffects)...
    StatusEffects = (
        WeaponGlobals.C_FLAMING,
        WeaponGlobals.C_ON_FIRE,
        WeaponGlobals.C_WOUND,
        WeaponGlobals.C_POISON,
        WeaponGlobals.C_ACID,
        WeaponGlobals.C_REGEN,
        WeaponGlobals.C_STUN,
        WeaponGlobals.C_UNSTUN,
        WeaponGlobals.C_SLOW,
        WeaponGlobals.C_PAIN,
        WeaponGlobals.C_HOLD,
        WeaponGlobals.C_BLIND,
        WeaponGlobals.C_DIRT,
        WeaponGlobals.C_TAUNT,
        WeaponGlobals.C_CURSE,
        WeaponGlobals.C_HASTEN,
        WeaponGlobals.C_WEAKEN)

    # the status effects which deal their effects every time they recur,
    # see WeaponGlobals.getEffects and getAttackRecur...
    RecurringEffects = (
        WeaponGlobals.C_FLAMING,
        WeaponGlobals.C_ON_FIRE,
        WeaponGlobals.C_WOUND,
        WeaponGlobals.C_POISON,
        WeaponGlobals.C_ACID,
        WeaponGlobals.C_REGEN)

    # the status effects a cure removes from it's target, everything but the
    # defensive buffs (see WeaponGlobals.getIsDefensiveBuff)...
    HostileEffects = (
        WeaponGlobals.C_FLAMING,
        WeaponGlobals.C_ON_FIRE,
        WeaponGlobals.C_WOUND,
        WeaponGlobals.C_POISON,
        WeaponGlobals.C_ACID,
        WeaponGlobals.C_STUN,
        WeaponGlobals.C_SLOW,
        WeaponGlobals.C_PAIN,
        WeaponGlobals.C_HOLD,
        WeaponGlobals.C_BLIND,
        WeaponGlobals.C_DIRT,
        WeaponGlobals.C_TAUNT,
        WeaponGlobals.C_CURSE,
        WeaponGlobals.C_WEAKEN)

    # the effect durations shortened by the grenade's ignore pain passive,
    # see the skill's description in PLocalizer.SkillDescriptions...
    IgnorePainEffects = (WeaponGlobals.C_STUN, WeaponGlobals.C_SLOW)

    def getSkillRank(self, avatar, skillId):
        if not skillId or not isinstance(avatar, DistributedPlayerPirateAI):
            return 0

        inventory = avatar.getInventory()
        if not inventory:
            return 0

        # an avatar's skill rank is it's skill point stack minus one, see SkillPage...
        return max(0, inventory.getStackQuantity(skillId) - 1)

    def getSkillEffectDuration(self, attacker, target, effectId, skillId, ammoSkillId):
        duration = WeaponGlobals.getAttackDuration(skillId, ammoSkillId)
        if duration <= 0:
            return duration

        # every rank past the first lengthens the effect by a quarter of it's
        # duration (see SkillButton.createHelpFrame). the ammo's effect replaces
        # the skill's effect, see WeaponGlobals.getAttackEffects...
        rank = self.getSkillRank(attacker, ammoSkillId or skillId)
        if rank > 1:
            duration += duration * (rank - 1) / 4.0

        if effectId in self.IgnorePainEffects:
            rank = self.getSkillRank(target, InventoryType.GrenadeIgnorePain)
            if rank:
                reduction = WeaponGlobals.getAttackDuration(InventoryType.GrenadeIgnorePain)
                reduction += reduction * (rank - 1) / 4.0
                duration *= max(0.0, 1.0 - reduction)

        return duration

    def applySkillEffect(self, target, effectId, attacker, skillId, ammoSkillId):
        if effectId not in self.StatusEffects:
            return

        if isinstance(target, DistributedInteractivePropAI):
            # Dont apply skill effects for props
            return

        # cannot apply a skill effect to the monkey
        if target.getAvatarType() == AvatarTypes.Monkey:
            return

        if not target.getDamagable() or target.getHp()[0] <= 0:
            return

        # stun immunity
        if effectId == WeaponGlobals.C_STUN and target.hasSkillEffect(WeaponGlobals.C_UNSTUN):
            return

        duration = self.getSkillEffectDuration(attacker, target, effectId, skillId, ammoSkillId)
        if duration <= 0:
            return

        # the client shows one buff per effect and attacker, the same attacker
        # renews it's effect. make sure the avatar does not already have too many
        # of these skill effects applied...
        attackerIds = target.getSkillEffectAttackers(effectId)
        if attacker.doId not in attackerIds and len(attackerIds) >= WeaponGlobals.getBuffStackNumber(effectId):
            return

        recur = 0
        if effectId in self.RecurringEffects:
            recur = WeaponGlobals.getAttackRecur(skillId, ammoSkillId)

        target.addSkillEffect(effectId, duration, attacker.doId, recur)

    def applySkillEffectTick(self, target, effectId, attackerId):
        # damage over time effects deal their effects every time they recur...
        effects = WeaponGlobals.getEffects(effectId)
        if effects and target.getHp()[0] > 0:
            self.applyTargetEffects(target, effects)

    def breakHostileSkillEffects(self, target):
        if not hasattr(target, 'removeSkillEffect'):
            return

        for effectId in self.HostileEffects:
            target.removeSkillEffect(effectId)

    def getMaxAttunedTargets(self, avatar):
        # every rank of attune allows the doll to be attuned to another target,
        # see the skill's description in PLocalizer.SkillDescriptions...
        return max(1, self.getSkillRank(avatar, InventoryType.DollAttune))

    def attuneTarget(self, avatar, target):
        if isinstance(avatar, DistributedPlayerPirateAI) and not avatar.hasStickyTarget(target.doId):
            stickyTargets = list(avatar.getStickyTargets())
            while stickyTargets and len(stickyTargets) >= self.getMaxAttunedTargets(avatar):
                self.unattuneTarget(avatar, stickyTargets.pop(0))

        if hasattr(avatar, 'addStickyTarget'):
            avatar.addStickyTarget(target.doId)

        # set the target's skill effect so that the attuning effect is
        # present, this will also set the avatar's local attune list...
        target.addSkillEffect(WeaponGlobals.C_ATTUNE, 0, avatar.doId)

    def unattuneTarget(self, avatar, targetDoId):
        if hasattr(avatar, 'removeStickyTarget'):
            avatar.removeStickyTarget(targetDoId)

        target = self.air.doId2do.get(targetDoId)
        if target and hasattr(target, 'removeSkillEffect'):
            target.removeSkillEffect(WeaponGlobals.C_ATTUNE, avatar.doId)

    def shatterAttunements(self, attacker, target, skillId, ammoSkillId):
        if not isinstance(target, DistributedPlayerPirateAI) or not target.getStickyTargets():
            return

        if target.hasSkillEffect(WeaponGlobals.C_VOODOO_STUN_LOCK):
            return

        for targetDoId in list(target.getStickyTargets()):
            self.unattuneTarget(target, targetDoId)

        # the client shows the attunements shattering, see DistributedBattleAvatar.addStatusEffect...
        duration = max(1, WeaponGlobals.getAttackDuration(skillId, ammoSkillId))
        target.addSkillEffect(WeaponGlobals.C_VOODOO_STUN, duration, attacker.doId)

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
        if hasattr(attacker, 'hasStickyTarget') and attacker.hasStickyTarget(target.doId):
            self.unattuneTarget(attacker, target.doId)

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
        if FreebooterAI.isAtOverallLevelCap(attacker):
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
