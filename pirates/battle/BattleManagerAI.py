import random

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

    def hasSkillData(self, skillId):
        if not skillId:
            return False

        return skillId in self._skillData

    def getSkillData(self, skillId):
        if not self.hasSkillData(skillId):
            return None

        return self._skillData[skillId]

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

        if skillData.skillId == WeaponGlobals.C_ATTUNE:
            self._avatar.addStickyTarget(self._target.doId)

    def removeSkillData(self, skillData):
        if not skillData:
            return

        if not isinstance(skillData, BattleAttackerSkillData):
            return

        if not self.hasSkillData(skillData):
            return

        if skillData.skillId == WeaponGlobals.C_ATTUNE:

            # This function already exists for the client. Might as well repurpose it
            self._avatar.reqeuestRemoveStickyTargets([self._target.doId])

        del self._skillData[skillData.skillId]
        skillData.destroy()

    def destroy(self):
        self._avatar = None
        self._target = None

        self._skillData = {}
        self._currentSkillId = 0

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

    def addAttackerData(self, attackerDoId):
        if not attackerDoId:
            return

        avatar = self._battleManager.air.doId2do.get(attackerDoId)

        if not avatar:
            return

        if self.hasAttackerData(attackerDoId):
            return

        attacker = BattleAttackerData(self._battleManager)
        attacker.avatar = avatar
        attacker.target = self

        self._attackerData[attacker.avatar.doId] = attacker

    def removeAttackerData(self, attackerData):
        if not attackerData:
            return

        if not isinstance(attackerData, BattleAttackerData):
            return

        avatar = attackerData.avatar

        if not avatar:
            return

        if not self.hasAttackerData(avatar.doId):
            return

        del self._attackerData[avatar.doId]
        attackerData.destroy()

    def destroy(self):
        self._target = None
        self._attackerData = {}

class BattleManagerAI(BattleManagerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleManagerAI')

    def __init__(self, air):
        self.air = air
        self.enemySpawner = self.air.enemySpawner

        self.__updateTask = None
        self.__targetData = {}

    def startup(self):
        self.__updateTask = taskMgr.add(self.__update, '%s-update-task-%s' % (
            self.__class__.__name__, id(self)))

    def __update(self, task):
        for spawnType, spawnNodes in self.enemySpawner.spawnNodes.items():
            for spawnNode in spawnNodes:
                self.__checkEnemySpawnNode(spawnNode)

        return task.cont

    def hasTargetData(self, targetDoId):
        if not targetDoId:
            return False

        return targetDoId in self.__targetData

    def getTargetData(self, targetDoId):
        if not self.hasTargetData(targetDoId):
            return None

        return self.__targetData[targetDoId]

    def addTargetData(self, target, avatar):
        if not target:
            return

        if not avatar:
            return

        if self.hasTargetData(target.doId):
            return

        targetData = BattleTargetData(self)
        targetData.target = target
        targetData.addAttackerData(avatar.doId)

        self.__targetData[targetData.target.doId] = targetData

    def removeTargetData(self, targetData):
        if not targetData:
            return

        if not self.hasTargetData(targetData.target.doId):
            return

        targetData.destroy()
        del self.__targetData[targetData.target.doId]

    def getTrueDistance(self, avatar, target):
        targetParent = target.getParentObj()

        if not targetParent:
            return 0

        targetNP = NodePath('psuedo-target-%d' % target.doId)
        targetNP.setPosHpr(targetParent, target.getPos(), target.getHpr())

        avatarNP = NodePath('psuedo-target-%d' % avatar.doId)
        avatarNP.setPosHpr(targetParent, avatar.getPos(), avatar.getHpr())

        return avatarNP.getDistance(targetNP)

    def targetInRange(self, attacker, target, skillId, ammoSkillId):
        if not skillId:
            return False

        tolerance = simbase.config.GetFloat('target-range-tolerance', 10.0)
        attackRange = self.getModifiedAttackRange(attacker, skillId, ammoSkillId)
        distance = self.getTrueDistance(attacker, target)

        if attackRange == WeaponGlobals.INF_RANGE:
            return True

        if distance <= attackRange * tolerance:
            return True

        return False

    def useTargetedSkill(self, avatar, target, skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge):
        if not avatar:
            self.notify.debug('Cannot calculate targeted skill for unknown avatar!')
            return None

        if not target:
            self.notify.debug('Cannot calculate targeted skill for avatar %d, unknown target!' % (
                avatar.doId))

            return None

        if not self.hasTargetData(target.doId):
            self.addTargetData(target, avatar)

        skillResult = self.willWeaponHit(avatar, target, skillId,
            ammoSkillId, charge)

        timestamp = globalClockDelta.getRealNetworkTime(bits=32)
        distance = self.getTrueDistance(avatar, target)

        if self.skillInRange(skillId, InventoryType.begin_WeaponSkillCutlass, InventoryType.end_WeaponSkillCutlass) or self.skillInRange(skillId,
            InventoryType.begin_WeaponSkillDagger, InventoryType.end_WeaponSkillDagger):

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
            duration = 10 #TODO: Calculate Proper
            target.addSkillEffect(targetSkillId, duration, timestamp, avatar.doId)

        attackerSkillEffect = attackerEffects[2]
        if attackerSkillEffect:
            duration = 10 #TODO: Calculate Proper
            target.addSkillEffect(attackerSkillId, duration, timestamp, avatar.doId)  

        targetData = self.getTargetData(target.doId)

        if not targetData:
            self.notify.warning('Cannot calculate targeted skill for avatar %d, no target data for target %d!' % (
                avatar.doId, target.doId))

            return None

        if not targetData.hasAttackerData(avatar.doId):
            targetData.addAttackerData(avatar.doId)

        attackerData = targetData.getAttackerData(avatar.doId)
        attackerData.currentSkillId = skillId

        if not attackerData:
            self.notify.warning('Cannot calculate targeted skill for avatar %d, no data for avatar!' % (
                avatar.doId))

            return None

        if not attackerData.hasSkillData(skillId):
            attackerData.addSkillData(skillId, ammoSkillId)

        skillData = attackerData.getSkillData(skillId)

        if not skillData:
            self.notify.warning('Cannot calculate targeted skill for avatar %d, no data for skill!' % (
                avatar.doId))

            return None

        if skillResult == WeaponGlobals.RESULT_HIT:
            reputation = self.getModifiedAttackReputation(avatar, target,
                skillId, ammoSkillId)

            skillData.reputation += reputation
            self.__applyTargetEffects(target, targetEffects)
        elif skillResult == WeaponGlobals.RESULT_MISS:
            pass
        elif skillResult == WeaponGlobals.RESULT_DODGE:
            pass
        elif skillResult == WeaponGlobals.RESULT_PARRY:
            pass
        elif skillResult == WeaponGlobals.RESULT_RESIST:
            pass
        else:
            self.notify.debug('Cannot calculate targeted skill, unknown weapon skill result was found, %d!' % (
                skillResult))

            return None

        return [skillId, ammoSkillId, skillResult, target.doId, areaIdList, attackerEffects, targetEffects,
            areaIdEffects, timestamp, pos, charge]

    def __applyTargetEffects(self, target, targetEffects):
        if not target:
            self.notify.debug('Cannot apply target effects for unknown target!')
            return

        target.b_setHp(target.getHp()[0] + targetEffects[0])
        target.b_setPower(target.getPower() + targetEffects[1])
        target.b_setLuck(target.getLuck() + targetEffects[2])
        target.b_setMojo(target.getMojo() + targetEffects[3])
        target.b_setSwiftness(target.getSwiftness() + targetEffects[4])

    def __applyAttackerEffects(self, avatar, attackerEffects):
        if not target:
            self.notify.debug('Cannot apply attacker effects for unknown avatar!')
            return

        avatar.b_setHp(avatar.getHp()[0] + targetEffects[0])
        avatar.b_setPower(avatar.getPower() + targetEffects[1])
        avatar.b_setLuck(avatar.getLuck() + targetEffects[2])
        avatar.b_setMojo(avatar.getMojo() + targetEffects[3])
        avatar.b_setSwiftness(avatar.getSwiftness() + targetEffects[4])

    def __checkEnemySpawnNode(self, spawnNode):
        if not spawnNode:
            return

        if not spawnNode.npc:
            return

        targetData = self.getTargetData(spawnNode.npc.doId)

        if not targetData:
            return

        for attackerData in list(targetData.attackerData.values()):
            avatar = attackerData.avatar

            if not avatar:
                targetData.removeAttackerData(attackerData)
                continue

            skillData = attackerData.getSkillData(attackerData.currentSkillId)

            if not self.targetInRange(avatar, spawnNode.npc, skillData.skillId, skillData.ammoSkillId):
                targetData.removeAttackerData(attackerData)
                continue

        if spawnNode.npc.getHp()[0] <= 0:
            self.__enemyDied(spawnNode, spawnNode.npc)
            return

        if not targetData.attackerData:
            self.removeTargetData(targetData)

    def __enemyDied(self, spawnNode, target):
        target = self.air.doId2do.get(target.doId)

        if not target:
            return

        if target.getIsKilled():
            return

        targetData = self.getTargetData(target.doId)

        if not targetData:
            return

        for attackerData in list(targetData.attackerData.values()):

            if not attackerData.avatar:
                targetData.removeAttackerData(attackerData)
                continue

            self.__giveAttackerReward(attackerData, targetData)
            targetData.removeAttackerData(attackerData)

        self.removeTargetData(targetData)
        spawnNode.processDeath()

    def skillInRange(self, skillId, start, end):
        return skillId >= start and skillId <= end

    def __giveAttackerReward(self, attackerData, targetData):
        avatar = attackerData.avatar
        target = targetData.target

        inventory = self.air.inventoryManager.getInventory(avatar.doId)

        if not inventory:
            self.notify.debug('Cannot calculate targeted skill reward, unknown inventory for avatar %d!' %(
                avatar.doId))

            return

        totalReputation = 0
        goldReward = EnemyGlobals.getGoldDrop(target.getAvatarType(),
            target.getLevel())

        for skillData in list(attackerData.skillData.values()):
            self.__giveSkillReward(inventory, skillData)
            totalReputation += skillData.reputation
            attackerData.removeSkillData(skillData)

        inventory.setGeneralRep(inventory.getGeneralRep() + totalReputation)
        inventory.setGoldInPocket(inventory.getGoldInPocket() + goldReward)

    def __giveSkillReward(self, inventory, skillData):
        skillId = skillData.skillId

        if self.skillInRange(skillId, InventoryType.begin_WeaponSkillCutlass, InventoryType.end_WeaponSkillCutlass):
            reputationType = InventoryType.CutlassRep
        elif self.skillInRange(skillId, InventoryType.begin_WeaponSkillPistol, InventoryType.end_WeaponSkillPistol):
            reputationType = InventoryType.PistolRep
        elif self.skillInRange(skillId, InventoryType.begin_WeaponSkillMusket, InventoryType.end_WeaponSkillMusket):
            reputationType = InventoryType.MusketRep
        elif self.skillInRange(skillId, InventoryType.begin_WeaponSkillDagger, InventoryType.end_WeaponSkillDagger):
            reputationType = InventoryType.DaggerRep
        elif self.skillInRange(skillId, InventoryType.begin_WeaponSkillGrenade, InventoryType.end_WeaponSkillGrenade):
            reputationType = InventoryType.GrenadeRep
        elif self.skillInRange(skillId, InventoryType.begin_WeaponSkillDoll, InventoryType.end_WeaponSkillDoll):
            reputationType = InventoryType.DollRep
        elif self.skillInRange(skillId, InventoryType.begin_WeaponSkillWand, InventoryType.end_WeaponSkillWand):
            reputationType = InventoryType.WandRep

        inventory.setReputation(reputationType, inventory.getReputation(reputationType) + \
            skillData.reputation)
