import random

from panda3d.core import *

from direct.distributed.ClockDelta import *
from direct.showbase import PythonUtil
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.GridParent import GridParent

from pirates.battle import EnemyGlobals
from pirates.pirate.BattleAvatarGameFSMAI import BattleAvatarGameFSMAI
from pirates.movement import MotionFSM
from pirates.battle import WeaponGlobals
from pirates.battle.EnemySkills import EnemySkills
from pirates.pirate import AvatarTypes


def decision(probability):
    """
    Returns True if the result is less than the probability otherwise False
    """

    return (100 * random.random()) < probability


class BattleNPCGameFSMAI(BattleAvatarGameFSMAI):
    notify = directNotify.newCategory('BattleNPCGameFSMAI')

    def __init__(self, air, avatar):
        BattleAvatarGameFSMAI.__init__(self, air, avatar)

        self.attackTarget = None

        self.__movementInterval = None
        self.__pausedTask = None
        self.__updateBattleStateTask = None
        self.__nextAttackTask = None

    def getPatrolRadius(self):
        return float(self.avatar.spawnNode.objectData.get('Patrol Radius', 0.0))

    def getPauseChance(self):
        return float(self.avatar.spawnNode.objectData.get('Pause Chance', 50.0))

    def getPauseDuration(self):
        return float(self.avatar.spawnNode.objectData.get('Pause Duration', 15.0))

    def shouldFollowTarget(self, attackTarget):
        if not attackTarget:
            return False

        distance = self.avatar.getDistance(attackTarget)
        return distance > EnemyGlobals.INSTANT_AGGRO_RADIUS_DEFAULT / 2

    def getPatrolPoint(self, avatar):
        parentObj = avatar.getParentObj()
        if not parentObj:
            return None

        patrolRadius = self.getPatrolRadius()
        if patrolRadius == 0.0:
            return None

        sx, sy, sz = avatar.getSpawnPos()
        x = random.uniform(sx - patrolRadius, sx + patrolRadius)
        y = random.uniform(sy - patrolRadius, sy + patrolRadius)
        return Point3(x, y, sz)

    def getWalkToPointDoneName(self):
        return self.avatar.uniqueName('walkToPoint-done')

    def getWalkToPointPausedName(self):
        return self.avatar.uniqueName('walkToPoint-paused')

    def getWatchTargetName(self):
        return self.avatar.uniqueName('watch-target')

    def getNextAttackName(self):
        return self.avatar.uniqueName('next-attack')

    def getTargetSwitchType(self):
        targetSwitchTypes = [
            TARGET_SWITCH_TYPE_RANDOM,
            TARGET_SWITCH_TYPE_DAMAGE,
            TARGET_SWITCH_TYPE_LOW_LVL,
            TARGET_SWITCH_TYPE_HIGH_LVL]

        return random.choice(targetSwitchTypes)

    def getAttackDelayModdifier(self):
        delayInfo = [
            WeaponGlobals.NO_DELAY,
            WeaponGlobals.SHORT_DELAY,
            WeaponGlobals.MED_DELAY,
            WeaponGlobals.LONG_DELAY]

        return random.choice(delayInfo)

    def getNewAttackTargetDoId(self):
        attackTargets = self.air.battleMgr.getAttackers(self.avatar.doId)
        if not attackTargets:
            return None

        # if we only have a single attack target, don't bother trying to
        # select a target based on a random weighted switch type...
        if len(attackTargets) == 1:
            return attackTargets[0]

        targetSwitchType = self.getTargetSwitchType()
        if targetSwitchType == TARGET_SWITCH_TYPE_RANDOM:
            return random.choice(attackTargets)
        elif targetSwitchType == TARGET_SWITCH_TYPE_DAMAGE:
            weights = {}
            for attackTarget in attackTargets:
                totalDamageDone = 0
                recordedAttacks = list(attackTarget.comboDiary.timers[attacker.doId])
                for recordedAttack in recordedAttacks:
                    totalDamageDone += recordedAttack[2]

                weights[attackTarget] = totalDamageDone

            return max(weights, key=weights.get)
        elif targetSwitchType == TARGET_SWITCH_TYPE_LOW_LVL:
            weights = {}
            for attackTarget in attackTargets:
                weights[attackTarget] = attackTarget.getLevel()

            return min(weights, key=weights.get)
        elif targetSwitchType == TARGET_SWITCH_TYPE_HIGH_LVL:
            weights = {}
            for attackTarget in attackTargets:
                weights[attackTarget] = attackTarget.getLevel()

            return max(weights, key=weights.get)

        return None

    def getNewAttackTarget(self):
        attackTargetDoId = self.getNewAttackTargetDoId()
        if not attackTargetDoId:
            return None

        return self.air.doId2do.get(attackTargetDoId)

    def getDistFromSpawnNode(self):
        spawnNodeNP = NodePath('spawnNode-%d' % self.avatar.doId)
        spawnNodeNP.setPos(*self.avatar.getSpawnPos())
        return self.avatar.getDistance(spawnNodeNP)

    def _drawWeapon(self):
        if not self.avatar.isWeaponDrawn:
            self.avatar.b_setCurrentWeapon(self.avatar.currentWeaponId, 1)

    def _putAwayWeapon(self):
        self.avatar.b_setCurrentWeapon(self.avatar.currentWeaponId, 0)

    def _chooseNextAttack(self, task):
        self.chooseNextAttack()
        return task.done

    def chooseNextAttack(self):
        # choose a random skill to attack the player with
        baseSkills = EnemyGlobals.getBaseSkills(self.avatar.getAvatarType())
        skillList = baseSkills[1]
        skillId = random.choice(skillList)

        areaIdList = self.air.battleMgr.getAttackers(self.avatar.doId)
        timestamp = globalClockDelta.getRealNetworkTime(bits=16)
        self.avatar.useTargetedSkill(self.avatar, self.attackTarget, skillId, 0, areaIdList, timestamp, self.avatar.getPos(), 0)

        # get the total delay on how long it will take the enemy to
        # use this attack, once the enemy has completed it's attack,
        # select another attack until this loop is broken...
        delay = WeaponGlobals.getAttackDelay(skillId)
        duration = WeaponGlobals.getAttackDuration(skillId)
        delay = EnemyGlobals.getAttackDelay(skillId, [delay, duration])
        delay += self.getAttackDelayModdifier()

        self.__nextAttackTask = taskMgr.doMethodLater(delay, self._chooseNextAttack, self.getNextAttackName())

    def findNextWalkToPoint(self):
        if self.state == 'Patrol' or self.state == 'Walk':
            patrolPoint = self.getPatrolPoint(self.avatar)
            if not patrolPoint:
                self.notify.warning('Could not find patrol point for NPC with doId: %d' % self.avatar.doId)

                # since we couldn't find an attack target, we cannot just do nothing;
                # instead let's just set our current state to our starting state.
                self.avatar.b_setGameState(self.avatar.getStartState())
                return

            doPause = decision(self.getPauseChance())
            if doPause:
                pauseDuration = random.uniform(1.0, self.getPauseDuration())
                self.__pausedTask = taskMgr.doMethodLater(pauseDuration, self.walkToPoint, self.getWalkToPointPausedName(),
                    extraArgs=[patrolPoint], appendTask=False)
            else:
                self.walkToPoint(patrolPoint)
        elif self.state == 'AttackChase':
            if not self.attackTarget:
                self.avatar.b_setGameState('BreakCombat')
                return

            spawnNodeDistance = self.getDistFromSpawnNode()
            if spawnNodeDistance > EnemyGlobals.AGGRO_RADIUS_TOLERANCE:
                # we've went too far away from our spawn node, walk us back to our spawn node,
                # then set our default state and wait for a new battle...
                self.avatar.b_setGameState('BreakCombat')
                return

            shouldFollowTarget = self.shouldFollowTarget(self.attackTarget)
            if not shouldFollowTarget:
                # we've arrived at the walk point and the attacker hasn't gone
                # outside our aggro radius, let's begin attacking the avatar...
                self.avatar.b_setGameState('Battle')
                return

            self.walkToPoint(self.attackTarget.getPos(), self.attackTarget.getParent())
        elif self.state == 'BreakCombat':
            self.avatar.b_setGameState(self.avatar.getStartState())

    def walkToPoint(self, walkPoint, parent=None):
        if not parent or parent.isEmpty():
            parent = self.avatar.getParentObj()

        # setup a node applying the walkPoint relative to the parent
        # parameter provided by this function, this allows us to properly
        # face towards the correct location even across the cartesian grid...
        walkPointNode = NodePath('walkPoint-%d' % self.avatar.doId)
        walkPointNode.setPos(parent, walkPoint)

        self.avatar.lookAt(walkPointNode)

        self.acceptOnce(self.getWalkToPointDoneName(), self.findNextWalkToPoint)
        walkSpeed = MotionFSM.WALK_CUTOFF * 2

        self.__movementInterval = self.avatar.posInterval(walkSpeed, walkPoint, other=parent)
        self.__movementInterval.setDoneEvent(self.getWalkToPointDoneName())
        self.__movementInterval.start()

    def enterPatrol(self, *args, **kwargs):
        self.findNextWalkToPoint()

    def exitPatrol(self):
        if self.__movementInterval:
            self.__movementInterval.finish()
            self.__movementInterval = None

        if self.__pausedTask:
            taskMgr.remove(self.__pausedTask)
            self.__pausedTask = None

    def enterWalk(self):
        self.findNextWalkToPoint()

    def exitWalk(self):
        if self.__movementInterval:
            self.__movementInterval.finish()
            self.__movementInterval = None

        if self.__pausedTask:
            taskMgr.remove(self.__pausedTask)
            self.__pausedTask = None

    def __updateBattleState(self, task):
        if not self.attackTarget:
            self.avatar.b_setGameState('BreakCombat')
            return task.done

        # check to see if the target is even on the same cartesian grid...
        if self.attackTarget.parentId != self.avatar.parentId:
            self.avatar.b_setGameState('BreakCombat')
            return task.done

        shouldFollowTarget = self.shouldFollowTarget(self.attackTarget)
        if shouldFollowTarget and self.avatar.getAvatarType() != AvatarTypes.FlyTrap:
            if self.state == 'Battle':
                self.avatar.b_setGameState('AttackChase')
                return task.done

            self.findNextWalkToPoint()

        # check to see if the target goes out of range of us,
        # this is mostly useful for fly traps (which don't move).
        distanceFromTarget = self.avatar.getDistance(self.attackTarget)
        if distanceFromTarget > EnemyGlobals.AGGRO_RADIUS_TOLERANCE:
            # the player has went too far away, walk us back to our spawn node,
            # then set our default state and wait for a new battle...
            self.avatar.b_setGameState('BreakCombat')
            return task.done

        # only rotate our avatar to face the attacker if we are not moving
        if self.state == 'Battle':
            self.avatar.lookAt(self.attackTarget)

        return task.cont

    def enterBattle(self):
        if not self.attackTarget:
            self.attackTarget = self.getNewAttackTarget()
            assert(self.attackTarget is not None)

        # update our anim state
        self.avatar.b_setAnimSet('default')

        # draw our weapon
        self._drawWeapon()

        # start attacking our target
        self.chooseNextAttack()
        self.__updateBattleStateTask = taskMgr.add(self.__updateBattleState, self.getWatchTargetName())

    def exitBattle(self):
        if self.__updateBattleStateTask is not None:
            taskMgr.remove(self.__updateBattleStateTask)
            self.__updateBattleStateTask = None

        if self.__nextAttackTask is not None:
            taskMgr.remove(self.__nextAttackTask)
            self.__nextAttackTask = None

        # update our anim state
        spawnNode = self.avatar.getSpawnNode()
        self.avatar.b_setAnimSet(spawnNode.objectData.get('AnimSet', 'default'))

    def enterAttackChase(self, *args, **kwargs):
        assert(self.attackTarget is not None)

        # begin following our target
        self.findNextWalkToPoint()
        self.__updateBattleStateTask = taskMgr.add(self.__updateBattleState, self.getWatchTargetName())

    def exitAttackChase(self):
        if self.__movementInterval:
            self.__movementInterval.finish()
            self.__movementInterval = None

        if self.__updateBattleStateTask is not None:
            taskMgr.remove(self.__updateBattleStateTask)
            self.__updateBattleStateTask = None

        if self.__nextAttackTask is not None:
            taskMgr.remove(self.__nextAttackTask)
            self.__nextAttackTask = None

    def enterBreakCombat(self):
        self.attackTarget = None

        # put away our weapon
        self._putAwayWeapon()

        # walk us back to our spawn point then set our default state.
        self.walkToPoint(Point3(*self.avatar.getSpawnPos()))

    def exitBreakCombat(self):
        pass

    def enterDeath(self, *args, **kwargs):
        self.air.battleMgr.rewardAttackers(self.avatar)
        self.avatar.spawnNode.processDeath()

    def exitDeath(self):
        pass
