import random

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from pirates.battle import EnemyGlobals
from pirates.battle import WeaponGlobals
from pirates.distributed.TargetManagerBase import TargetManagerBase


class TargetManagerAI(DistributedObjectAI, TargetManagerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('TargetManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        TargetManagerBase.__init__(self)

        self.projectiles = {}

        self.__updateTargetsTask = None

    def __updateTargets(self, task):
        for targetId, attackers in list(self.objectDict.items()):
            self.air.battleMgr.updateTarget(targetId, attackers)

        return task.cont

    def startup(self):
        self.__updateTargetsTask = taskMgr.add(self.__updateTargets, self.uniqueName('update-targets-task'))

    def hasTarget(self, targetId):
        return targetId in self.objectDict

    def addTarget(self, target):
        assert(target is not None)
        if target.doId in self.objectDict:
            return

        self.objectDict[target.doId] = []

    def removeTarget(self, target):
        assert(target is not None)
        if target.doId not in self.objectDict:
            return

        # clear all of our previously targeted attackers
        attackerDoIds = self.objectDict[target.doId]
        for attackerDoId in attackerDoIds:
            attacker = self.air.doId2do.get(attackerDoId)
            assert(attacker is not None)
            self.removeAttacker(attacker, target)

        del self.objectDict[target.doId]

    def clearTarget(self, target):
        assert(target is not None)
        if target.doId not in self.objectDict:
            return

        attackerDoIds = self.objectDict[target.doId]
        for attackerDoId in list(attackerDoIds):
            attacker = self.air.doId2do.get(attackerDoId)
            assert(attacker is not None)
            self.removeAttacker(attacker, target)

    def hasAttacker(self, attackerId, targetId):
        if targetId not in self.objectDict:
            return False

        return attackerId in self.objectDict[targetId]

    def addAttacker(self, attacker, target):
        assert(attacker is not None)
        assert(target is not None)

        if target.doId not in self.objectDict:
            return

        attackers = self.objectDict[target.doId]
        if attacker.doId in attackers:
            return

        attackers.append(attacker.doId)
        if len(attackers) == 1 and not target.currentTarget and target.gameFSM.state != 'Battle':
            target.b_setGameState('Battle')

        attacker.b_setCurrentTarget(target.doId)

    def removeAttacker(self, attacker, target):
        assert(attacker is not None)
        assert(target is not None)

        if target.doId not in self.objectDict:
            return

        attackers = self.objectDict[target.doId]
        if attacker.doId not in attackers:
            return

        attackers.remove(attacker.doId)
        self.air.battleMgr.clearAttacker(target, attacker)
        attacker.b_setCurrentTarget(0)

    def clearAttacker(self, attacker):
        assert(attacker is not None)

        # removes attacker from all targets and clears the attacker
        # entirely from the target manager
        for targetDoId, attackerDoIds in list(self.objectDict.items()):
            target = self.air.doId2do.get(targetDoId)
            assert(target is not None)
            if attacker.doId in attackerDoIds:
                attackerDoIds.remove(attacker.doId)
                self.air.battleMgr.clearAttacker(target, attacker)

        attacker.b_setCurrentTarget(0)

    def getAttackers(self, targetDoId):
        return self.objectDict.get(targetDoId)

    def getTargetSwitchType(self):
        targetSwitchTypes = [
            EnemyGlobals.TARGET_SWITCH_TYPE_RANDOM,
            EnemyGlobals.TARGET_SWITCH_TYPE_DAMAGE,
            EnemyGlobals.TARGET_SWITCH_TYPE_LOW_LVL,
            EnemyGlobals.TARGET_SWITCH_TYPE_HIGH_LVL]

        return random.choice(targetSwitchTypes)

    def findTargetableObject(self, targetDoId):
        if targetDoId not in self.objectDict:
            return None

        attackers = self.objectDict.get(targetDoId)
        if not attackers:
            return None

        # if there is a single attacker attacking us, don't bother trying
        # to select an attacker target from switch type...
        if len(attackers) == 1:
            return attackers[0]

        targetSwitchType = self.getTargetSwitchType()
        if targetSwitchType == EnemyGlobals.TARGET_SWITCH_TYPE_RANDOM:
            return random.choice(attackers)
        elif targetSwitchType == EnemyGlobals.TARGET_SWITCH_TYPE_DAMAGE:
            weights = {}
            for attackTargetDoId in list(attackers):
                attacker = self.air.doId2do.get(attackTargetDoId)
                if not attacker:
                    continue

                totalDamageDone = 0
                recordedAttacks = attacker.comboDiary.getCombos(attacker.doId)
                for recordedAttack in list(recordedAttacks):
                    totalDamageDone += recordedAttack[2]

                weights[attackTargetDoId] = totalDamageDone

            return max(weights, key=weights.get)
        elif targetSwitchType == EnemyGlobals.TARGET_SWITCH_TYPE_LOW_LVL:
            weights = {}
            for attackTargetDoId in list(attackers):
                attacker = self.air.doId2do.get(attackTargetDoId)
                if not attacker:
                    continue

                weights[attackTargetDoId] = attacker.getLevel()

            return min(weights, key=weights.get)
        elif targetSwitchType == EnemyGlobals.TARGET_SWITCH_TYPE_HIGH_LVL:
            weights = {}
            for attackTargetDoId in list(attackers):
                attacker = self.air.doId2do.get(attackTargetDoId)
                if not attacker:
                    continue

                weights[attackTargetDoId] = attacker.getLevel()

            return max(weights, key=weights.get)

        return None

    def getAttackers(self, targetId):
        return self.objectDict.get(targetId, [])

    def hasProjectile(self, avatarId, skillId, ammoSkillId):
        #assert(WeaponGlobals.isProjectileSkill(skillId, ammoSkillId))
        projectiles = self.projectiles.get(avatarId)
        if not projectiles:
            return False

        for projectile in projectiles:
            if projectile[0] != skillId or projectile[1] != ammoSkillId:
                continue

            return True

        return False

    def addProjectile(self, avatarId, skillId, ammoSkillId, timestamp):
        #assert(WeaponGlobals.isProjectileSkill(skillId, ammoSkillId))
        if self.hasProjectile(avatarId, skillId, ammoSkillId):
            return

        projectiles = self.projectiles.setdefault(avatarId, [])
        projectiles.append([skillId, ammoSkillId, timestamp])

    def removeProjectile(self, avatarId, skillId, ammoSkillId):
        #assert(WeaponGlobals.isProjectileSkill(skillId, ammoSkillId))
        if not self.hasProjectile(avatarId, skillId, ammoSkillId):
            return

        projectiles = self.projectiles.get(avatarId)
        for index in range(len(projectiles)):
            projectile = projectiles[index]

            if projectile[0] != skillId or projectile[1] != ammoSkillId:
                continue

            del projectiles[index]
            break

    def getProjectile(self, avatarId, skillId, ammoSkillId):
        #assert(WeaponGlobals.isProjectileSkill(skillId, ammoSkillId))
        projectiles = self.projectiles.get(avatarId)
        if not projectiles:
            return None

        for projectile in projectiles:
            if projectile[0] != skillId or projectile[1] != ammoSkillId:
                continue

            return projectile

        return None

    def delete(self):
        if self.__updateTargetsTask:
            taskMgr.remove(self.__updateTargetsTask)
            self.__updateTargetsTask = None

        DistributedObjectAI.delete(self)
        TargetManagerBase.delete(self)
