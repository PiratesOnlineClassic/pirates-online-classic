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


class BattleNPCGameFSMAI(BattleAvatarGameFSMAI):
    notify = directNotify.newCategory('BattleNPCGameFSMAI')

    # how fast npcs walk between the movement nodes of their patrol route
    WAYPOINT_WALK_SPEED = 8.0

    # how long a stunned enemy waits before trying to attack again
    StunnedAttackDelay = 0.5

    def __init__(self, air, avatar):
        BattleAvatarGameFSMAI.__init__(self, air, avatar)

        self.__movementInterval = None
        self.__pausedTask = None
        self.__updateBattleStateTask = None
        self.__nextAttackTask = None
        self.__chaseTargetTask = None
        self.__attackChaseTask = None
        self.__returnToSpawnTask = None
        self.__mojoRegenTask = None

        # the targets our voodoo weapon has attuned to
        self.attunedTargetIds = []

        # the movement node we are currently at on our patrol route,
        # None when we are at our spawn node...
        self.__waypointUid = None
        self.__waypointData = None
        self.__lastWaypointUid = None
        self.__walkingRoute = False

        # where we left our patrol route to fight, when we were walking one
        self.__routeOrigin = None

        # update our game state as we change it
        self.setBroadcastStateChanges(True)
        self.accept(self.getStateChangeEvent(), self.__updateGameState)

    def __updateGameState(self):
        self.avatar.d_setGameState(self.getCurrentOrNextState())

    def getPatrolRadius(self):
        return float(self.avatar.spawnNode.objectData.get('Patrol Radius', 1.0))

    def getPatrolNodeData(self):
        # the pause properties come from the node we're currently standing at,
        # which is either our spawn node or a movement node on our patrol route...
        if self.__waypointData is not None:
            return self.__waypointData

        return self.avatar.spawnNode.objectData

    def getPauseChance(self):
        return float(self.getPatrolNodeData().get('Pause Chance', 100.0))

    def getPauseDuration(self):
        # movement nodes use the level editor's default pause duration
        defaultDuration = 30.0 if self.__waypointData is not None else 15.0
        return float(self.getPatrolNodeData().get('Pause Duration', defaultDuration))

    def getNextPauseDuration(self):
        if random.random() * 100.0 >= self.getPauseChance():
            return 0

        return random.uniform(1.0, max(self.getPauseDuration(), 1.0))

    def resetWaypoint(self):
        self.__waypointUid = None
        self.__waypointData = None
        self.__lastWaypointUid = None

    def getNextWaypoint(self):
        spawnNode = self.avatar.getSpawnNode()
        if not spawnNode or not hasattr(spawnNode, 'getLinkedWaypoints'):
            return None

        linkedWaypoints = spawnNode.getLinkedWaypoints(self.__waypointUid)
        if not linkedWaypoints:
            return None

        # don't turn back the way we came unless we've reached a dead end
        choices = [waypoint for waypoint in linkedWaypoints if waypoint[0] != self.__lastWaypointUid]
        waypointUid, waypointData = random.choice(choices or linkedWaypoints)

        previousWaypointUid = self.__waypointUid or spawnNode.objKey
        if waypointUid == spawnNode.objKey:
            self.__waypointUid = None
            self.__waypointData = None
        else:
            self.__waypointUid = waypointUid
            self.__waypointData = waypointData

        self.__lastWaypointUid = previousWaypointUid
        return spawnNode.getWaypointPos(waypointUid, waypointData)

    def shouldFollowTarget(self, attackTarget):
        if not attackTarget:
            return False

        distance = self.avatar.getDistance(attackTarget)
        return distance > EnemyGlobals.INSTANT_AGGRO_RADIUS_DEFAULT / 2

    def getPointInRadius(self, cx, cy, cz, radius):
        x = random.uniform(cx - radius, cx + radius)
        y = random.uniform(cy - radius, cy + radius)
        return Point3(x, y, cz)

    def getPatrolPoint(self):
        parentObj = self.avatar.getParentObj()
        if not parentObj:
            return None

        # npcs with a patrol route walk along the movement nodes linked
        # to their spawn node, rather than around their spawn node...
        waypointPos = self.getNextWaypoint()
        self.__walkingRoute = waypointPos is not None
        if self.__walkingRoute:
            return Point3(*waypointPos)

        patrolRadius = self.getPatrolRadius()
        if patrolRadius == 0.0:
            return None

        sx, sy, sz = self.avatar.getSpawnPos()
        return self.getPointInRadius(sx, sy, sz, patrolRadius)

    def getWalkToPointDoneName(self):
        return self.avatar.uniqueName('walkToPoint-done')

    def getWalkToPointPausedName(self):
        return self.avatar.uniqueName('walkToPoint-paused')

    def getWalkToPointChaseName(self):
        return self.avatar.uniqueName('walkToPoint-attack-chase')

    def getUpdateBattleStateTaskName(self):
        return self.avatar.taskName('update-battle-state')

    def getNextAttackTaskName(self):
        return self.avatar.taskName('next-attack')

    def getChaseTargetTaskName(self):
        return self.avatar.taskName('chase-target')

    def getReturnToSpawnTaskName(self):
        return self.avatar.taskName('return-to-spawn')

    def getMojoRegenTaskName(self):
        return self.avatar.taskName('mojo-regen')

    def getAttackDelayModdifier(self):
        delayInfo = [
            WeaponGlobals.NO_DELAY,
            WeaponGlobals.SHORT_DELAY,
            WeaponGlobals.MED_DELAY,
            WeaponGlobals.LONG_DELAY]

        return random.choice(delayInfo)

    def getNewAttackTarget(self):
        attackTargetDoId = self.air.targetMgr.findTargetableObject(self.avatar.doId)
        if not attackTargetDoId:
            return None

        return self.air.doId2do.get(attackTargetDoId)

    def findNewAttackTarget(self):
        # remove any attackers that are no longer valid (dead or logged out)
        # then attempt to switch over to one of our remaining attackers...
        for attackerDoId in list(self.air.targetMgr.getAttackers(self.avatar.doId)):
            attacker = self.air.doId2do.get(attackerDoId)
            if attacker and not self.avatar.isTargetValid(attacker):
                self.air.targetMgr.removeAttacker(attacker, self.avatar)

        attackTarget = self.getNewAttackTarget()
        if not attackTarget or not self.avatar.isTargetValid(attackTarget):
            self.avatar.b_setCurrentTarget(0)
            return None

        self.avatar.b_setCurrentTarget(attackTarget.doId)
        return attackTarget

    def getPatrolOrigin(self):
        if self.__routeOrigin is not None:
            return self.__routeOrigin

        return Point3(*self.avatar.getSpawnPos())

    def rememberPatrolOrigin(self):
        # npcs walking a patrol route may be far away from their spawn node when
        # they get into a fight, they fight around and return to where they left
        # their route instead of their spawn node...
        if self.__routeOrigin is not None or not self.__walkingRoute:
            return

        parentObj = self.avatar.getParentObj()
        if parentObj:
            self.__routeOrigin = self.avatar.getPos(parentObj)

    def getDistFromSpawnNode(self):
        spawnNodeNP = NodePath('spawnNode-%d' % self.avatar.doId)
        spawnNodeNP.setPos(*self.getPatrolOrigin())
        return self.avatar.getDistance(spawnNodeNP)

    def _drawWeapon(self):
        if not self.avatar.isWeaponDrawn:
            self.avatar.b_setCurrentWeapon(self.avatar.currentWeaponId, 1)

    def _putAwayWeapon(self):
        self.avatar.b_setCurrentWeapon(self.avatar.currentWeaponId, 0)

    def __mojoRegen(self, task):
        currentMojo = self.avatar.getMojo()
        maxMojo = self.avatar.getMaxMojo()
        if currentMojo >= maxMojo:
            return task.again

        mojoRegen = 2 #TODO: constant?
        self.avatar.b_setMojo(min(currentMojo + mojoRegen, maxMojo))
        return task.again

    def getAttackSkills(self):
        return EnemyGlobals.getBaseSkills(self.avatar.avatarType)[EnemyGlobals.SKILL_INDEX]

    def getUsableSkills(self):
        # some enemies know the skills of more than one weapon, but they only ever
        # hold one of them. the skills of the other weapons would never land...
        skillList = self.getAttackSkills()
        weaponId = self.avatar.currentWeaponId
        repId = WeaponGlobals.getRepId(weaponId)
        usableSkills = [skillId for skillId in skillList if WeaponGlobals.isValidSkill(skillId, weaponId, repId)]
        return usableSkills or skillList

    def _chooseNextAttack(self, task):
        # our target may have died or left the district since our last
        # attack, find someone else to fight or give up the battle...
        if not self.avatar.isTargetValid(self.avatar.currentTarget):
            if not self.findNewAttackTarget():
                self.demand('BreakCombat')
                return task.done

        # stunned enemies cannot attack until the stun wears off...
        if WeaponGlobals.C_STUN in self.avatar.getSkillEffectIds():
            task.setDelay(self.StunnedAttackDelay)
            return task.again

        # choose a random skill to attack the player with, some enemies
        # (townsfolk, the mossman...) do not have any skills at all...
        skillList = self.getUsableSkills()
        if not skillList:
            task.setDelay(WeaponGlobals.SHORT_DELAY)
            return task.again

        skillId = random.choice(skillList)

        # wait until our target is within range of the skill, mobile enemies
        # will be chasing their target meanwhile...
        if not self.air.battleMgr.getTargetInRange(self.avatar, self.avatar.currentTarget, skillId, 0):
            task.setDelay(WeaponGlobals.SHORT_DELAY)
            return task.again

        # enemy skills only hit our current target, we must not send our list
        # of attackers here otherwise every client will play hit effects on them
        areaIdList = []
        timestamp = globalClockDelta.getRealNetworkTime(bits=16)
        self.avatar.useTargetedSkill(self.avatar, self.avatar.currentTarget, skillId, 0, areaIdList, timestamp, self.avatar.getPos(), 0)

        # get the total delay on how long it will take the enemy to
        # use this attack, once the enemy has completed it's attack,
        # select another attack until this loop is broken...
        delay = WeaponGlobals.getAttackDelay(skillId)
        delay += WeaponGlobals.getAttackDuration(skillId)
        delay += self.getAttackDelayModdifier()

        # update our task delay
        task.setDelay(delay)
        return task.again

    def beginAttackingTarget(self):
        self.__nextAttackTask = taskMgr.doMethodLater(WeaponGlobals.SHORT_DELAY, self._chooseNextAttack, self.getNextAttackTaskName())

    def stopAttackingTarget(self):
        if self.__nextAttackTask:
            taskMgr.remove(self.__nextAttackTask)
            self.__nextAttackTask = None

    def _chaseTarget(self, task):
        self.findNextWalkToPoint()
        return task.done

    def beginChasingTarget(self):
        # we setup a task for this because we do not want to block
        # the state call with an infinite recursive loop...
        self.__chaseTargetTask = taskMgr.add(self._chaseTarget, self.getChaseTargetTaskName())

    def _returnToSpawn(self, task):
        self.walkToPoint(self.getPatrolOrigin())
        return task.done

    def doReturnToSpawn(self):
        # we setup a task for this because we do not want to block
        # the state call with an infinite recursive loop...
        self.__returnToSpawnTask = taskMgr.add(self._returnToSpawn, self.getReturnToSpawnTaskName())

    def findNextWalkToPoint(self):
        state = self.getCurrentOrNextState()
        if state == 'Patrol' or state == 'Walk':
            patrolPoint = self.getPatrolPoint()
            if not patrolPoint:
                self.notify.warning('Could not find patrol point for NPC with doId: %d' % self.avatar.doId)

                # since we couldn't find an attack target, we cannot just do nothing;
                # instead let's just set our current state to our starting state.
                self.demand(self.avatar.getStartState())
                return

            # we may pause at our current node before walking on to the next one
            pauseDuration = self.getNextPauseDuration()

            walkSpeed = self.WAYPOINT_WALK_SPEED if self.__walkingRoute else None
            self.__pausedTask = taskMgr.doMethodLater(pauseDuration, self.walkToPoint, self.getWalkToPointPausedName(),
                extraArgs=[patrolPoint, None, walkSpeed], appendTask=False)
        elif state == 'AttackChase':
            currentTarget = self.avatar.currentTarget
            if not self.avatar.isTargetValid(currentTarget):
                self.demand('BreakCombat')
                return

            spawnNodeDistance = self.getDistFromSpawnNode()
            if spawnNodeDistance > EnemyGlobals.AGGRO_RADIUS_TOLERANCE:
                # we've went too far away from our spawn node, walk us back to our spawn node,
                # then set our default state and wait for a new battle...
                self.request('BreakCombat')
                return

            shouldFollowTarget = self.shouldFollowTarget(currentTarget)
            if not shouldFollowTarget:
                # we've arrived at the walk point and the attacker hasn't gone
                # outside our aggro radius, let's begin attacking the avatar...
                self.request('Battle')
                return

            self.__attackChaseTask = taskMgr.doMethodLater(0.1, self._walkToPoint,
                                                                self.getWalkToPointChaseName(),
                                                                extraArgs=[currentTarget],
                                                                appendTask=False)

        elif state == 'BreakCombat':
            self.request(self.avatar.getStartState())

    # how much longer a slowed enemy takes to walk anywhere
    SlowedWalkModifier = 2.0

    def isMovementHeld(self):
        # stunned and shackled enemies are rooted in place until the effect wears off...
        skillEffectIds = self.avatar.getSkillEffectIds()
        return WeaponGlobals.C_STUN in skillEffectIds or WeaponGlobals.C_HOLD in skillEffectIds

    def _walkToPoint(self, currentTarget):
        if self.isMovementHeld():
            self.__attackChaseTask = taskMgr.doMethodLater(self.StunnedAttackDelay, self._walkToPoint,
                self.getWalkToPointChaseName(), extraArgs=[currentTarget], appendTask=False)

            return

        self.walkToPoint(currentTarget.getPos(), currentTarget.getParent())

    def walkToPoint(self, walkPoint, parent=None, walkSpeed=None):
        if not parent or parent.isEmpty():
            parent = self.avatar.getParentObj()

        # setup a node applying the walkPoint relative to the parent
        # parameter provided by this function, this allows us to properly
        # face towards the correct location even across the cartesian grid...
        walkPointNode = NodePath('walkPoint-%d' % self.avatar.doId)
        walkPointNode.setPos(parent, walkPoint)

        self.avatar.lookAt(walkPointNode)

        self.acceptOnce(self.getWalkToPointDoneName(), self.findNextWalkToPoint)

        # walks along a patrol route take as long as the distance requires,
        # otherwise we're only walking a short distance around our spawn node...
        walkDuration = MotionFSM.WALK_CUTOFF * 2
        if walkSpeed:
            walkDuration = max(self.avatar.getDistance(walkPointNode) / walkSpeed, walkDuration)

        if WeaponGlobals.C_SLOW in self.avatar.getSkillEffectIds():
            walkDuration *= self.SlowedWalkModifier

        self.__movementInterval = self.avatar.posInterval(walkDuration, walkPoint, other=parent)
        self.__movementInterval.setDoneEvent(self.getWalkToPointDoneName())
        self.__movementInterval.start()

        # broadcast the walk until we come to rest again:
        self.avatar.kickPosHprBroadcast()

    def _stopMovement(self):
        # stop walking where we currently are; we do not finish the interval
        # since that would warp us to the end point and send the done event
        # while we are in the middle of a state transition...
        self.ignore(self.getWalkToPointDoneName())
        if self.__movementInterval:
            self.__movementInterval.pause()
            self.__movementInterval = None

        if self.__pausedTask:
            taskMgr.remove(self.__pausedTask)
            self.__pausedTask = None

        if self.__attackChaseTask:
            taskMgr.remove(self.__attackChaseTask)
            self.__attackChaseTask = None

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterIdle(self):
        pass

    def filterIdle(self, request, args=[]):
        # the monkey cannot attack anyone, as it does not have a weapon or skills;
        # with this in mind we can argue the monkey will never leave Idle state.
        if self.avatar.avatarType == AvatarTypes.Monkey:
            return None

        return self.defaultFilter(request, args)

    def exitIdle(self):
        pass

    def enterPatrol(self, *args, **kwargs):
        self.findNextWalkToPoint()

    def exitPatrol(self):
        self._stopMovement()

    def enterWalk(self):
        self.findNextWalkToPoint()

    def exitWalk(self):
        self._stopMovement()

    def __updateBattleState(self, task):
        currentTarget = self.avatar.currentTarget
        if not self.avatar.isTargetValid(currentTarget):
            currentTarget = self.findNewAttackTarget()

        if not currentTarget:
            self.demand('BreakCombat')
            return task.done

        shouldFollowTarget = self.shouldFollowTarget(currentTarget)
        if shouldFollowTarget and (self.avatar.avatarType not in [AvatarTypes.FlyTrap, AvatarTypes.Monkey]):
            state = self.getCurrentOrNextState()
            if state == 'Battle':
                self.request('AttackChase')
                return task.done

            self.findNextWalkToPoint()

        # check to see if the target goes out of range of us,
        # this is mostly useful for fly traps (which don't move).
        distanceFromTarget = self.avatar.getDistance(currentTarget)
        if distanceFromTarget > EnemyGlobals.AGGRO_RADIUS_TOLERANCE:
            # the player has went too far away, walk us back to our spawn node,
            # then set our default state and wait for a new battle...
            self.request('BreakCombat')
            return task.done

        return task.cont

    def enterAmbush(self):
        pass

    def exitAmbush(self):
        pass

    def enterBattle(self):
        self.rememberPatrolOrigin()
        if not self.avatar.isTargetValid(self.avatar.currentTarget):
            if not self.findNewAttackTarget():
                # there is nobody left for us to fight...
                self.demand('BreakCombat')
                return

        self.avatar.startLookAt()

        # update our anim state
        self.avatar.b_setAnimSet('default')

        # draw our weapon
        self._drawWeapon()

        # attune if we have a voodoo weapon and start our regen task
        if WeaponGlobals.isVoodooWeapon(self.avatar.currentWeaponId):
            self.attuneTarget(self.avatar.currentTarget)
            self.__mojoRegenTask = taskMgr.doMethodLater(2, self.__mojoRegen, self.getMojoRegenTaskName())

        # start attacking our target
        self.beginAttackingTarget()
        self.__updateBattleStateTask = taskMgr.add(self.__updateBattleState, self.getUpdateBattleStateTaskName())

    def exitBattle(self):
        if self.__updateBattleStateTask:
            taskMgr.remove(self.__updateBattleStateTask)
            self.__updateBattleStateTask = None

        self.stopAttackingTarget()

        if self.__mojoRegenTask:
            taskMgr.remove(self.__mojoRegenTask)
            self.__mojoRegenTask = None

        # remove the attunes of our voodoo weapon, our current target may
        # no longer be the target we have attuned...
        self.unattuneTargets()

        self.avatar.stopLookAt()

    def attuneTarget(self, target):
        target.addSkillEffect(WeaponGlobals.C_ATTUNE, 0, self.avatar.doId)
        if target.doId not in self.attunedTargetIds:
            self.attunedTargetIds.append(target.doId)

    def unattuneTargets(self):
        for targetDoId in self.attunedTargetIds:
            target = self.air.doId2do.get(targetDoId)
            if target and hasattr(target, 'removeSkillEffect'):
                target.removeSkillEffect(WeaponGlobals.C_ATTUNE, self.avatar.doId)

        self.attunedTargetIds = []

    def enterAttackChase(self, *args, **kwargs):
        self.rememberPatrolOrigin()
        assert(self.avatar.currentTarget is not None)
        self.avatar.startLookAt()
        self.avatar.d_setChat(self.avatar.getTauntPhrase())

        # start attacking our target
        self.beginAttackingTarget()

        # start our regen task if we have a voodoo weapon
        if WeaponGlobals.isVoodooWeapon(self.avatar.currentWeaponId):
            self.__mojoRegenTask = taskMgr.doMethodLater(2, self.__mojoRegen, self.getMojoRegenTaskName())

        # begin following our target
        self.beginChasingTarget()
        self.__updateBattleStateTask = taskMgr.add(self.__updateBattleState, self.getUpdateBattleStateTaskName())

    def exitAttackChase(self):
        if self.__chaseTargetTask:
            taskMgr.remove(self.__chaseTargetTask)
            self.__chaseTargetTask = None

        self._stopMovement()

        if self.__updateBattleStateTask:
            taskMgr.remove(self.__updateBattleStateTask)
            self.__updateBattleStateTask = None

        if self.__nextAttackTask:
            taskMgr.remove(self.__nextAttackTask)
            self.__nextAttackTask = None

        if self.__mojoRegenTask:
            taskMgr.remove(self.__mojoRegenTask)
            self.__mojoRegenTask = None

        self.stopAttackingTarget()
        self.avatar.stopLookAt()

    def enterBreakCombat(self):
        self.avatar.b_setCurrentTarget(0)
        self.avatar.d_setChat(self.avatar.getBreakCombatPhrase())

        # put away our weapon
        self._putAwayWeapon()

        # clear our attackers from the target mgr
        self.air.targetMgr.clearTarget(self.avatar)

        # walk us back to our spawn point then set our default state,
        # or back to our patrol route if we left it to fight...
        if self.__routeOrigin is None:
            self.resetWaypoint()

        self.doReturnToSpawn()

    def filterBreakCombat(self, request, args=[]):
        if request == 'advance':
            return 'LandRoam'

        if request == 'Battle':
            return None

        return self.defaultFilter(request, args)

    def exitBreakCombat(self):
        self.__routeOrigin = None

        if self.__returnToSpawnTask:
            taskMgr.remove(self.__returnToSpawnTask)
            self.__returnToSpawnTask = None

        self._stopMovement()

        # update our anim state
        spawnNode = self.avatar.getSpawnNode()
        if spawnNode:
            self.avatar.b_setAnimSet(spawnNode.objectData.get('AnimSet', 'default'))

            # set the rotation of the avatar to be that of it's initial spawn constants
            if hasattr(spawnNode, 'getSpawnHpr'):
                self.avatar.setHpr(spawnNode.getSpawnHpr())
            else:
                self.avatar.setHpr(spawnNode.objectData.get('Hpr', (0, 0, 0)))

            self.avatar.kickPosHprBroadcast()

        # reset the avatar's mojo and health
        self.avatar.b_setHp(self.avatar.getMaxHp())
        self.avatar.b_setMojo(self.avatar.getMaxMojo())

    def enterDeath(self, *args, **kwargs):
        self.air.battleMgr.rewardAttackers(self.avatar)

        # now that our attackers have been rewarded, clear them from the
        # target mgr so that their skill diaries cannot be rewarded twice
        self.air.targetMgr.clearTarget(self.avatar)
        self.avatar.b_setCurrentTarget(0)

        spawnNode = self.avatar.getSpawnNode()
        if spawnNode:
            spawnNode.processDeath()

    def exitDeath(self):
        pass
