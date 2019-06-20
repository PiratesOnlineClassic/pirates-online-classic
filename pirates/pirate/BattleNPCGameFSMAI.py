import random

from panda3d.core import *

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.GridParent import GridParent

from pirates.battle import EnemyGlobals
from pirates.pirate.BattleAvatarGameFSMAI import BattleAvatarGameFSMAI
from pirates.movement import MotionFSM


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
        self.__watchTargetTask = None

    def getPatrolRadius(self):
        return float(self.avatar.spawnNode.objectData.get('Patrol Radius', 0.0))

    def getPauseChance(self):
        return float(self.avatar.spawnNode.objectData.get('Pause Chance', 50.0))

    def getPauseDuration(self):
        return float(self.avatar.spawnNode.objectData.get('Pause Duration', 15.0))

    def getMinFollowDist(self, attackTarget):
        aggroRadius = attackTarget.getAggroRadius()
        if aggroRadius <= EnemyGlobals.AGGRO_RADIUS_FALLOFF_RATE * 2:
            return EnemyGlobals.AGGRO_RADIUS_FALLOFF_RATE

        return aggroRadius / EnemyGlobals.AGGRO_RADIUS_FALLOFF_RATE

    def shouldFollowTarget(self, attackTarget):
        if attackTarget is None:
            return False

        distance = self.avatar.getDistance(attackTarget)
        minFollowDistance = self.getMinFollowDist(attackTarget)
        return distance <= EnemyGlobals.AGGRO_RADIUS_TOLERANCE and distance >= minFollowDistance

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

    def findNextWalkToPoint(self):
        if self.state == 'Patrol':
            patrolPoint = self.getPatrolPoint(self.avatar)
            if patrolPoint is None:
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
                return

            distance = self.avatar.getDistance(self.attackTarget)
            if distance > EnemyGlobals.AGGRO_RADIUS_TOLERANCE:
                # the player has went too far away, walk us back to our spawn node...
                self.attackTarget = None
                return

            shouldFollowTarget = self.shouldFollowTarget(self.attackTarget)
            if not shouldFollowTarget:
                return

            self.walkToPoint(self.attackTarget.getPos())

    def walkToPoint(self, walkPoint):
        parent = self.avatar.getParentObj()
        self.avatar.lookAt(walkPoint)

        self.acceptOnce(self.getWalkToPointDoneName(), self.findNextWalkToPoint)
        walkSpeed = MotionFSM.WALK_CUTOFF * 2

        self.__movementInterval = self.avatar.posInterval(walkSpeed, walkPoint, other=parent, blendType='easeInOut')
        self.__movementInterval.setDoneEvent(self.getWalkToPointDoneName())
        self.__movementInterval.start()

    def enterPatrol(self, *args, **kwargs):
        patrolPoint = self.getPatrolPoint(self.avatar)
        if not patrolPoint:
            self.notify.warning('Could not find patrol point for NPC with doId: %d!' % self.avatar.doId)
            return

        self.walkToPoint(patrolPoint)

    def exitPatrol(self):
        if self.__movementInterval:
            self.__movementInterval.finish()
            self.__movementInterval = None

        if self.__pausedTask:
            taskMgr.remove(self.__pausedTask)
            self.__pausedTask = None

    def __watchTarget(self, task):
        if not self.attackTarget:
            return task.done

        shouldFollowTarget = self.shouldFollowTarget(self.attackTarget)
        if self.state == 'AttackChase' and shouldFollowTarget:
            self.walkToPoint(self.attackTarget.getPos())

        return task.cont

    def enterAttackChase(self, attackTarget, *args, **kwargs):
        self.attackTarget = attackTarget

        self.__watchTargetTask = taskMgr.add(self.__watchTarget, self.getWatchTargetName())

        self.walkToPoint(self.attackTarget.getPos())

    def exitAttackChase(self):
        if self.__movementInterval:
            self.__movementInterval.finish()
            self.__movementInterval = None

        if self.__watchTargetTask is not None:
            taskMgr.remove(self.__watchTargetTask)
            self.__watchTargetTask = None

        self.attackTarget = None

    def enterDeath(self, *args, **kwargs):
        self.air.battleMgr.rewardAttackers(self.avatar)
        self.avatar.spawnNode.processDeath()

    def exitDeath(self):
        pass
