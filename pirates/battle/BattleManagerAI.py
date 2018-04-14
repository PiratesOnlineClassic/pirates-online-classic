import random
import math

from panda3d.core import *
from pirates.battle.BattleManagerBase import BattleManagerBase
from direct.directnotify import DirectNotifyGlobal
from pirates.battle import WeaponGlobals
from direct.distributed.ClockDelta import globalClockDelta
from pirates.uberdog import UberDogGlobals
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType, InventoryCategory
from pirates.battle import EnemyGlobals

class BattleAttackerSkillData(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleAttackerSkillData')

    def __init__(self, battleManager):
        self._battleManager = battleManager

        self._attacker = None

        self._skillId = 0
        self._ammoSkillId = 0

        self._reputation = 0

    @property
    def attacker(self):
        return self._attacker

    @attacker.setter
    def attacker(self, attacker):
        self._attacker = attacker

    @property
    def skillId(self):
        return self._skillId

    @skillId.setter
    def skillId(self, skillId):
        self._skillId = skillId

    @property
    def ammoSkillId(self):
        return self._ammoSkillId

    @ammoSkillId.setter
    def ammoSkillId(self, ammoSkillId):
        self._ammoSkillId = ammoSkillId

    @property
    def reputation(self):
        return self._reputation

    @reputation.setter
    def reputation(self, reputation):
        self._reputation = reputation

    def destroy(self):
        self._attacker = None

        self._skillId = 0
        self._ammoSkillId = 0

        self._reputation = 0

class BattleAttackerData(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleAttackerData')

    def __init__(self, battleManager):
        self._battleManager = battleManager

        self._avatar = None
        self._target = None

        self._skillData = {}

        self._currentSkillId = 0
        self._reputation = 0

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        self._target = target

    @property
    def avatar(self):
        return self._avatar

    @avatar.setter
    def avatar(self, avatar):
        self._avatar = avatar

    @property
    def skillData(self):
        return self._skillData

    @property
    def currentSkillId(self):
        return self._currentSkillId

    @currentSkillId.setter
    def currentSkillId(self, currentSkillId):
        self._currentSkillId = currentSkillId

    @property
    def reputation(self):
        return self._reputation

    @reputation.setter
    def reputation(self, reputation):
        self._reputation = reputation

    def hasSkillData(self, skillId):
        if not skillId:
            return False

        return skillId in self._skillData

    def getSkillData(self, skillId):
        if not self.hasSkillData(skillId):
            return None

        return self._skillData[skillId]

    def getSkillDefaultData(self, skillId, ammoSkillId):
        if not self.hasSkillData(skillId):
            self.addSkillData(skillId, ammoSkillId)

        return self.getSkillData(skillId)

    def addSkillData(self, skillId, ammoSkillId):
        if not skillId:
            return

        if self.hasSkillData(skillId):
            return

        skillData = BattleAttackerSkillData(self._battleManager)
        skillData.avatar = self
        skillData.skillId = skillId
        skillData.ammoSkillId = ammoSkillId

        self._skillData[skillId] = skillData

        # if the target is using a doll skill, add the target to the
        # avatar's sticky targets...
        target = self._target.avatar

        if self._battleManager.getSkillInRange(skillId, InventoryType.begin_WeaponSkillDoll, \
            InventoryType.end_WeaponSkillDoll):

            self._avatar.addStickyTarget(self._target.avatar.doId)

    def removeSkillData(self, skillData):
        if not isinstance(skillData, BattleAttackerSkillData):
            return

        if not self.hasSkillData(skillData):
            return

        # if the target is using a doll skill, remove the sticky target from
        # the avatar's sticky targets...
        target = self._target.avatar

        if self._battleManager.getSkillInRange(skillId, InventoryType.begin_WeaponSkillDoll, \
            InventoryType.end_WeaponSkillDoll):

            self._avatar.removeStickyTarget(target.doId)
            target.removeSkillEffect(self._skillId)

        del self._skillData[skillData.skillId]
        skillData.destroy()

    def destroy(self):
        self._avatar = None
        self._target = None

        self._skillData = {}

        self._currentSkillId = 0
        self._reputation = 0

class BattleTargetData(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleTargetData')

    def __init__(self, battleManager):
        self._battleManager = battleManager

        self._avatar = None

        self._attackerData = {}

    @property
    def avatar(self):
        return self._avatar

    @avatar.setter
    def avatar(self, avatar):
        self._avatar = avatar

    @property
    def attackerData(self):
        return self._attackerData

    def hasAttackerData(self, attackerDoId):
        if not attackerDoId:
            return False

        return attackerDoId in self._attackerData

    def getAttackerData(self, attackerDoId):
        if not self.hasAttackerData(attackerDoId):
            return None

        return self._attackerData[attackerDoId]

    def getAttackerDefaultData(self, avatar):
        if not self.hasAttackerData(avatar.doId):
            self.addAttackerData(avatar)

        return self.getAttackerData(avatar.doId)

    def addAttackerData(self, avatar):
        if self.hasAttackerData(avatar.doId):
            return

        attacker = BattleAttackerData(self._battleManager)
        attacker.avatar = avatar
        attacker.target = self

        self._attackerData[avatar.doId] = attacker

    def removeAttackerData(self, attackerData):
        if not isinstance(attackerData, BattleAttackerData):
            return

        avatar = attackerData.avatar

        if not self.hasAttackerData(avatar.doId):
            return

        del self._attackerData[avatar.doId]
        attackerData.destroy()

    def destroy(self):
        self._target = None

        self._attackerData = {}

class BattleManagerData(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleManagerData')

    def __init__(self):
        self.__targetData = {}

    def hasTargetData(self, targetDoId):
        if not targetDoId:
            return False

        return targetDoId in self.__targetData

    def getTargetData(self, targetDoId):
        if not self.hasTargetData(targetDoId):
            return None

        return self.__targetData[targetDoId]

    def getTargetDefaultData(self, target, avatar):
        if not self.hasTargetData(target.doId):
            self.addTargetData(target, avatar)

        return self.getTargetData(target.doId)

    def addTargetData(self, target, avatar):
        if self.hasTargetData(target.doId):
            return

        targetData = BattleTargetData(self)
        targetData.avatar = target
        targetData.addAttackerData(avatar)

        self.__targetData[target.doId] = targetData

    def removeTargetData(self, targetData):
        target = targetData.avatar
        if not self.hasTargetData(target.doId):
            return

        targetData.destroy()
        del self.__targetData[target.doId]

class BattleManagerAI(BattleManagerBase, BattleManagerData):
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleManagerAI')

    def __init__(self, air):
        BattleManagerData.__init__(self)

        self.air = air
        self.enemySpawner = self.air.enemySpawner

        self.__updateTask = None

    def startup(self):
        self.__updateTask = taskMgr.add(self.__update, '%s-update-task-%s' % (
            self.__class__.__name__, id(self)))

    def __update(self, task):
        for spawnNodes in self.enemySpawner.spawnNodes.values():
            for spawnNode in spawnNodes:
                self.__checkEnemySpawnNode(spawnNode)

        return task.cont

    def getTrueDistance(self, avatar, target):
        targetParent = target.getParentObj()

        if not targetParent:
            return 0

        targetNP = NodePath('psuedo-target-%d' % target.doId)
        targetNP.setPosHpr(targetParent, target.getPos(), target.getHpr())

        avatarNP = NodePath('psuedo-avatar-%d' % avatar.doId)
        avatarNP.setPosHpr(targetParent, avatar.getPos(), avatar.getHpr())

        return avatarNP.getDistance(targetNP)

    def getSkillInRange(self, skillId, start, end):
        return skillId >= start and skillId <= end

    def getWeaponReputationType(self, skillId):
        if self.getSkillInRange(skillId, InventoryType.begin_WeaponSkillCutlass, InventoryType.end_WeaponSkillCutlass):
            return InventoryType.CutlassRep
        elif self.getSkillInRange(skillId, InventoryType.begin_WeaponSkillPistol, InventoryType.end_WeaponSkillPistol):
            return InventoryType.PistolRep
        elif self.getSkillInRange(skillId, InventoryType.begin_WeaponSkillMusket, InventoryType.end_WeaponSkillMusket):
            return InventoryType.MusketRep
        elif self.getSkillInRange(skillId, InventoryType.begin_WeaponSkillDagger, InventoryType.end_WeaponSkillDagger):
            return InventoryType.DaggerRep
        elif self.getSkillInRange(skillId, InventoryType.begin_WeaponSkillGrenade, InventoryType.end_WeaponSkillGrenade):
            return InventoryType.GrenadeRep
        elif self.getSkillInRange(skillId, InventoryType.begin_WeaponSkillDoll, InventoryType.end_WeaponSkillDoll):
            return InventoryType.DollRep
        elif self.getSkillInRange(skillId, InventoryType.begin_WeaponSkillWand, InventoryType.end_WeaponSkillWand):
            return InventoryType.WandRep

        return None

    def getTargetInRange(self, attacker, target, skillId, ammoSkillId):
        if not skillId:
            return False

        attackRange = self.getModifiedAttackRange(attacker, skillId, ammoSkillId)
        distance = self.getTrueDistance(attacker, target)

        # TODO FIXME: calculate the range distance in a better way!
        if self.getWeaponReputationType(skillId) == InventoryType.CutlassRep:
            attackRange *= 4

        return attackRange == WeaponGlobals.INF_RANGE or distance <= attackRange

    def getTargetedSkillResult(self, avatar, target, skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge):
        print ("getTargetedSkillResult", avatar, target, skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge)
        if not avatar:
            self.notify.warning('Cannot calculate targeted skill for unknown avatar; skillId=%d!' % (
                skillId))

            return None

        if not target:
            self.notify.warning('Cannot calculate targeted skill, unknown target; avatarId=%d, skillId=%d!' % (
                avatar.doId, skillId))

            return None

        obeysPirateCode = self.obeysPirateCode(avatar, target)

        if not obeysPirateCode:
            self.notify.debug('Cannot calculate targeted skill, avatar does not obey pirate code; avatarId=%d, targetId=%d, skillId=%d' % (
                avatar.doId, target.doId, skillId))

            return None

        skillResult = self.willWeaponHit(avatar, target, skillId, ammoSkillId, charge)
        timestamp = globalClockDelta.getRealNetworkTime(bits=32)
        distance = self.getTrueDistance(avatar, target)

        # TODO FIXME: Find a better way to determine the weapon type...
        if self.getWeaponReputationType(skillId) == InventoryType.CutlassRep:
            attackerEffects, targetEffects = self.getModifiedSkillEffectsSword(avatar, target, skillId,
                ammoSkillId, charge, distance)
        else:
            attackerEffects, targetEffects = self.getModifiedSkillEffects(avatar, target,
                skillId, ammoSkillId, charge, distance)

        areaIdEffects = [
            attackerEffects,
            targetEffects
        ]

        targetSkillId = targetEffects[2]
        if targetSkillId:
            duration = 10 #TODO FIXME: Calculate Properly!
            target.addSkillEffect(targetSkillId, duration, avatar.doId)

        attackerSkillEffect = attackerEffects[2]
        if attackerSkillEffect:
            duration = 10 #TODO FIXME: Calculate Properly!
            target.addSkillEffect(attackerSkillId, duration, avatar.doId)

        targetData = self.getTargetDefaultData(target, avatar)

        if not targetData:
            self.notify.warning('Cannot calculate targeted skill, no target data for target; avatarId=%d, targetId=%d, skillId=%d!' % (
                avatar.doId, target.doId, skillId))

            return None

        attackerData = targetData.getAttackerDefaultData(avatar)
        attackerData.currentSkillId = skillId

        if not attackerData:
            self.notify.warning('Cannot calculate targeted skill, no data for avatar; avatarId=%d, targetId=%d, skillId=%d!' % (
                avatar.doId, target.doId, skillId))

            return None

        skillData = attackerData.getSkillDefaultData(skillId, ammoSkillId)

        if not skillData:
            self.notify.warning('Cannot calculate targeted skill for, no data for skill; avatarId=%d, targetId=%d, skillId=%d!' % (
                avatar.doId, target.doId, skillId))

            return None

        if skillResult == WeaponGlobals.RESULT_HIT:
            self.__targetedSkillHit(avatar, target, targetData, attackerData, areaIdEffects, skillData,
                skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge)
        elif skillResult == WeaponGlobals.RESULT_MISS:
            self.__targetedSkillMiss(avatar, target, targetData, attackerData, areaIdEffects, skillData,
                skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge)
        elif skillResult == WeaponGlobals.RESULT_DODGE:
            self.__targetedSkillDodge(avatar, target, targetData, attackerData, areaIdEffects, skillData,
                skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge)
        elif skillResult == WeaponGlobals.RESULT_PARRY:
            self.__targetedSkillParry(avatar, target, targetData, attackerData, areaIdEffects, skillData,
                skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge)
        elif skillResult == WeaponGlobals.RESULT_RESIST:
            self.__targetedSkillResist(avatar, target, targetData, attackerData, areaIdEffects, skillData,
                skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge)
        else:
            self.notify.warning('Cannot calculate targeted skill, unknown weapon skill result was found; avatarId=%d, targetId=%d, skillId=%d, skillResult=%d!' % (
                avatar.doId, target.doId, skillId, skillResult))

            return None

        return [skillId, ammoSkillId, skillResult, target.doId, areaIdList, attackerEffects, targetEffects,
            areaIdEffects, timestamp, pos, charge]

    def __targetedSkillHit(self, avatar, target, targetData, attackerData, areaIdEffects, skillData, skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge):
        reputation = self.getModifiedAttackReputation(avatar, target, skillId, ammoSkillId)
        skillData.reputation += reputation
        attackerData.reputation += reputation
        self.__applyTargetEffects(target, areaIdEffects[1])

    def __targetedSkillMiss(self, avatar, target, targetData, attackerData, areaIdEffects, skillData, skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge):
        pass

    def __targetedSkillDodge(self, avatar, target, targetData, attackerData, areaIdEffects, skillData, skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge):
        pass

    def __targetedSkillParry(self, avatar, target, targetData, attackerData, areaIdEffects, skillData, skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge):
        pass

    def __targetedSkillResist(self, avatar, target, targetData, attackerData, areaIdEffects, skillData, skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge):
        pass

    def __applyTargetEffects(self, target, targetEffects):
        target.b_setHp(target.getHp()[0] + targetEffects[0])
        target.b_setPower(target.getPower() + targetEffects[1])
        target.b_setLuck(target.getLuck() + targetEffects[2])
        target.b_setMojo(target.getMojo() + targetEffects[3])
        target.b_setSwiftness(target.getSwiftness() + targetEffects[4])

    def __checkEnemySpawnNode(self, spawnNode):
        if not spawnNode:
            return

        target = spawnNode.npc

        if not target:
            return

        targetData = self.getTargetData(target.doId)

        if not targetData:
            return

        for attackerData in targetData.attackerData.values():
            avatar = attackerData.avatar

            # ensure the avatar still exists...
            if not avatar:
                targetData.removeAttackerData(attackerData)
                continue

            skillData = attackerData.getSkillData(attackerData.currentSkillId)
            targetInRange = self.getTargetInRange(avatar, spawnNode.npc, skillData.skillId,
                skillData.ammoSkillId)

            # check to see if the avatar is still in range of target it was attacking
            # if they are not, remove them from the target data; assuming they've moved on...
            if not targetInRange:
                self.notify.debug('Found an avatar that is no longer in range of target; avatarId=%d, targetId=%d!' % (
                    avatar.doId, target.doId))

                targetData.removeAttackerData(attackerData)
                continue

        # check to see if the npc has just died.
        if target.getHp()[0] <= 0:
            self.__enemySpawnNodeDied(spawnNode)
            return

        # check to see if the target has any current attackers,
        # if not then let's just remove the targets data...
        if not targetData.attackerData:
            self.removeTargetData(targetData)

    def __enemySpawnNodeDied(self, spawnNode):
        target = spawnNode.npc

        if not target:
            return

        targetData = self.getTargetData(target.doId)

        if not targetData:
            return

        # give the avatar it's reward for killing the target...
        for attackerData in targetData.attackerData.values():
            self.__giveAttackerReward(attackerData, targetData)

        self.removeTargetData(targetData)
        spawnNode.processDeath()

    def __giveAttackerReward(self, attackerData, targetData):
        avatar = attackerData.avatar
        target = targetData.avatar

        inventory = self.air.inventoryManager.getInventory(avatar.doId)

        if not inventory:
            self.notify.warning('Cannot calculate targeted skill reward, unknown inventory; avatarId=%d!' %(
                avatar.doId))

            return

        # calculate the total reputation for the avatar by adding up each bit of reputation
        # that was given out to the weapons the avatar used to kill the target...
        goldReward = EnemyGlobals.getGoldDrop(target.getAvatarType(),
            target.getLevel())

        # update the avatar's inventory details.
        inventory.setGeneralRep(inventory.getGeneralRep() + attackerData.reputation)
        inventory.setGoldInPocket(inventory.getGoldInPocket() + goldReward)

        # give the avatar an reward for each weapon it used to kill the target...
        for skillData in attackerData.skillData.values():
            self.__giveSkillReward(inventory, attackerData, skillData)

        # remove the attackers data
        targetData.removeAttackerData(attackerData)

    def __giveSkillReward(self, inventory, attackerData, skillData):
        avatar = attackerData.avatar
        target = attackerData.target.avatar

        reputationType = self.getWeaponReputationType(skillData.skillId)

        if not reputationType:
            self.notify.warning('Cannot give skill reward for unknown reputation type; avatarId=%d, targetId=%d, skillId=%d' % (
                avatar.doId, target.doId, skillData.skillId))

            attackerData.removeSkillData(skillData)
            return

        inventory.setReputation(reputationType, inventory.getReputation(reputationType) + \
            skillData.reputation)

        # remove the skills data
        attackerData.removeSkillData(skillData)

    def destroy(self):
        if self.__updateTask:
            taskMgr.remove(self.__updateTask)

        self.__updateTask = None
