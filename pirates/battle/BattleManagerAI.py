import random
import math

from panda3d.core import *
from pirates.battle.BattleManagerBase import BattleManagerBase
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals
from pirates.battle import WeaponGlobals
from pirates.battle import EnemyGlobals
from pirates.battle import WeaponConstants
from direct.distributed.ClockDelta import globalClockDelta
from pirates.uberdog import UberDogGlobals
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType, InventoryCategory

class BattleManagerAI(BattleManagerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleManagerAI')

    def __init__(self, air):
        self.air = air
        self.enemySpawner = self.air.enemySpawner

        self.__updateTask = None
        self.__targets = {}
        self.__removingAttackers = {}

    def startup(self):
        self.__updateTask = taskMgr.add(self.__update, '%s-update-task-%s' % (
            self.__class__.__name__, id(self)))

    def __update(self, task):
        for targetId, attackers in self.__targets.items():
            self.__checkTarget(targetId, attackers)

        return task.cont

    def hasTarget(self, targetId):
        return targetId in self.__targets

    def addTarget(self, target):
        if target.doId in self.__targets:
            return

        self.__targets[target.doId] = []

    def removeTarget(self, target):
        if target.doId not in self.__targets:
            return

        del self.__targets[target.doId]

    def hasAttacker(self, attackerId, targetId):
        if targetId not in self.__targets:
            return False

        return attackerId in self.__targets[targetId]

    def addAttacker(self, attackerId, targetId):
        if targetId not in self.__targets:
            return

        if attackerId in self.__targets[targetId]:
            return

        self.__targets[targetId].append(attackerId)

    def removeAttacker(self, attackerId, targetId):
        if targetId not in self.__targets:
            return

        if attackerId not in self.__targets[targetId]:
            return

        attacker.battleSkillDiary.reset()
        self.__targets[targetId].remove(attackerId)

    def getAttackers(self, targetId):
        return self.__targets.get(targetId)

    def targetInRange(self, attacker, target, skillId, ammoSkillId):
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

    def getTargetedSkillResult(self, avatar, target, skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge):
        if not avatar:
            self.notify.warning('Cannot get targeted skill result for an unknown avatar!')
            return None

        # this is just the client requesting an action for the skill used,
        # they are not actually attacking any kind of target...
        if not target:
            return self.__otherSkillResult(avatar, target, skillId, ammoSkillId, clientResult, areaIdList,
                timestamp, pos, charge)

        # the client requested a valid skill result, attempt to calculate
        # the result for the client and send the result back...
        return self.__skillResult(avatar, target, skillId, ammoSkillId, clientResult, areaIdList,
            timestamp, pos, charge)

    def __skillResult(self, avatar, target, skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge):
        currentWeaponId, isWeaponDrawn = avatar.getCurrentWeapon()

        # ensure the avatar that has sent this skill request actually
        # has their weapon drawn...
        if not isWeaponDrawn:
            self.notify.debug('Cannot get skill result for avatar %d, weapon %d was now drawn!' % (
                avatar.doId, currentWeaponId))

            return None

        obeysPirateCode = self.obeysPirateCode(avatar, target)

        # ensure the avatar that has sent this skill request obeys
        # the pirate code and can use the weapon on the target...
        if not obeysPirateCode:
            self.notify.debug('Cannot get skill result for avatar %d, does not obey pirate code!' % (
                avatar.doId))

            return None

        skillResult = self.willWeaponHit(avatar, target, skillId, ammoSkillId, charge)
        distance = self.getRelativePosition(avatar, target)
        timestamp = globalClockDelta.getRealNetworkTime(bits=32)

        # check to see if our dictionary of target to attacker data contains this attacker,
        # if not we will assume this is a new attacker to the target and assign them accordingly...
        if not self.hasAttacker(avatar.doId, target.doId):
            self.addAttacker(avatar.doId, target.doId)

        # add the skill info to the attackers battle skill diary to track
        # what skills they have used and when...
        if not avatar.battleSkillDiary.hasSkill(skillId):
            avatar.battleSkillDiary.addSkill(skillId, ammoSkillId)

        # calculate the moddified skill result for this skill, add this including
        # the attack data according to which ever weapon the avatar is using...
        if WeaponGlobals.isBladedWeapon(currentWeaponId):
            attackerEffects, targetEffects = self.getModifiedSkillEffectsSword(avatar, target, skillId,
                ammoSkillId, charge, distance)
        else:
            attackerEffects, targetEffects = self.getModifiedSkillEffects(avatar, target, skillId,
                ammoSkillId, charge, distance)

        areaIdEffects = [
            attackerEffects,
            targetEffects
        ]

        if skillResult == WeaponGlobals.RESULT_NOT_AVAILABLE:
            self.notify.debug('Cannot get skill result for avatar %d, skill %d not available for avatar!' % (
                avatar.doId, skillId))

            return None
        elif skillResult == WeaponGlobals.RESULT_HIT:

            # check to see if the skill used by the avatar was either a hurting effect,
            # or a healing effect like the doll heal, cure skills...
            if WeaponGlobals.isHealingSkill(skillId):
                self.__healTarget(target, targetEffects)
                self.__healTarget(avatar, attackerEffects)
            else:
                self.__hurtTarget(target, targetEffects)
                self.__hurtTarget(avatar, attackerEffects)

            # update this skills current reputation, this will eventually add up
            # and all skills used will be rewarded reputation...
            skillData = avatar.battleSkillDiary.getSkill(skillId)

            if not skillData:
                return None

            skillData[2] += self.getModifiedAttackReputation(avatar, target,
                skillId, ammoSkillId)

        elif skillResult == WeaponGlobals.RESULT_MISS:
            pass
        elif skillResult == WeaponGlobals.RESULT_DODGE:
            raise NotImplemented
        elif skillResult == WeaponGlobals.RESULT_PARRY:
            raise NotImplemented
        elif skillResult == WeaponGlobals.RESULT_RESIST:
            raise NotImplemented
        else:
            self.notify.debug('Cannot get skill result for avatar %d, unknown skill result %d for skill %d!' % (
                avatar.doId, skillResult, skillId))

            return None

        return [skillId, ammoSkillId, skillResult, target.doId, areaIdList, attackerEffects, targetEffects,
            areaIdEffects, timestamp, pos, charge]

    def __otherSkillResult(self, avatar, target, skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge):
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
                avatar.useTonic(ammoSkillId)
        else:
            currentWeaponId, isWeaponDrawn = avatar.getCurrentWeapon()

            # ensure the avatar that has sent this skill request actually
            # has their weapon drawn...
            if not isWeaponDrawn:
                self.notify.debug('Cannot get other skill result for avatar %d, weapon %d was now drawn!' % (
                    avatar.doId, currentWeaponId))

                return None

        return [skillId, ammoSkillId, WeaponGlobals.RESULT_HIT, 0, areaIdList, attackerEffects, targetEffects,
            areaIdEffects, timestamp, pos, charge]

    def __healTarget(self, target, targetEffects):
        target.b_setHp(max(0, min(target.getHp()[0] - targetEffects[0], target.getMaxHp())))
        target.b_setPower(max(0, min(target.getPower() - targetEffects[1], target.getMaxPower())))
        target.b_setLuck(max(0, min(target.getLuck() - targetEffects[2], target.getMaxLuck())))
        target.b_setMojo(max(0, min(target.getMojo() - targetEffects[3], target.getMaxMojo())))
        target.b_setSwiftness(max(0, min(target.getSwiftness() - targetEffects[4], target.getMaxSwiftness())))

    def __hurtTarget(self, target, targetEffects):
        target.b_setHp(max(0, min(target.getHp()[0] + targetEffects[0], target.getMaxHp())))
        target.b_setPower(max(0, min(target.getPower() + targetEffects[1], target.getMaxPower())))
        target.b_setLuck(max(0, min(target.getLuck() + targetEffects[2], target.getMaxLuck())))
        target.b_setMojo(max(0, min(target.getMojo() + targetEffects[3], target.getMaxMojo())))
        target.b_setSwiftness(max(0, min(target.getSwiftness() + targetEffects[4], target.getMaxSwiftness())))

    def __checkTarget(self, targetId, attackers):
        target = self.air.doId2do.get(targetId)

        if not target:
            return

        for attackerId in attackers:
            attacker = self.air.doId2do.get(attackerId)

            if not attacker:
                continue

            self.__checkAttacker(attacker, target)

    def __checkAttacker(self, attacker, target):
        # check the current weapon skill and determine if the avatar is still in
        # range that they may still be able to use that weapon in battle...
        skillId = attacker.battleSkillDiary.getCurrentSkill()

        if not skillId:
            return

        ammoSkillId, timestamp, reputation = attacker.battleSkillDiary.getSkill(skillId)

        # now that we have the avatar's current skill, check the range of that specific weapon...
        if not self.targetInRange(attacker, target, skillId, ammoSkillId):
            self.notify.debug('Attacker %d has gone out of range of target %d with skill %d!' % (
                attacker.doId, target.doId, skillId))

            if attacker.doId in self.__removingAttackers:
                return

            # give the attacker a chance to return to battle in order to get their
            # experience and reward values from previous skills used...
            self.__removingAttackers[attacker.doId] = taskMgr.doMethodLater(5.0, self.__removeAttacker, '%s-removing-attacker-%d' % (
                self.__class__.__name__, attacker.doId), extraArgs=[attacker, target], appendTask=True)

    def __removeAttacker(self, attacker, target, task):
        self.removeAttacker(attacker, target)
        del self.__removingAttackers[attacker.doId]
        return task.done

    def rewardAttackers(self, target):
        if target.getHp()[0] > 0:
            return

        for attackerId in self.__targets[target.doId]:
            attacker = self.air.doId2do.get(attackerId)

            if not attacker:
                continue

            self.__rewardAttacker(attacker, target)

    def __rewardAttacker(self, attacker, target):
        inventory = self.air.inventoryManager.getInventory(attacker.doId)

        if not inventory:
            self.notify.debug('Cannot reward avatar %d for killing %d, unknown inventory!' % (
                attacker.doId, target.doId))

            return

        overallReputation = 0
        goldReward = EnemyGlobals.getGoldDrop(target.getAvatarType(), target.getLevel())

        for skillId in attacker.battleSkillDiary.getSkills():
            ammoSkillId, timestamp, reputation = attacker.battleSkillDiary.getSkill(skillId)
            reputationCategoryId = WeaponGlobals.getSkillReputationCategoryId(skillId)

            # update the avatar's skill reputation for each skill it used to kill the target,
            # adding onto the overall reputation rewarded
            overallReputation += reputation
            inventory.setReputation(reputationCategoryId, inventory.getReputation(reputationCategoryId) + reputation)

        # clear the avatar's skill diary since they've been given their
        # reward in full...
        attacker.battleSkillDiary.reset()

        # update the avatar's overall reputation based on all the skills they
        # used to kill the target
        inventory.setOverallRep(inventory.getOverallRep() + overallReputation)
        inventory.setGoldInPocket(inventory.getGoldInPocket() + goldReward)

    def destroy(self):
        if self.__updateTask:
            taskMgr.remove(self.__updateTask)

        self.__updateTask = None
