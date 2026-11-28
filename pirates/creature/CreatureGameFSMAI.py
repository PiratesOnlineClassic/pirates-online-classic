import random

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClockDelta import globalClockDelta

from pirates.pirate.BattleNPCGameFSMAI import BattleNPCGameFSMAI
from pirates.battle import WeaponGlobals


class CreatureGameFSMAI(BattleNPCGameFSMAI):
    notify = directNotify.newCategory('CreatureGameFSMAI')

    def defaultFilter(self, request, args):
        # stationary creatures (such as the fly trap) are rooted to the ground,
        # instead of walking around they will just idle at their spawn point...
        if self.avatar.isStationary() and request in ['Patrol', 'Walk']:
            return ('Idle',) + tuple(args)

        return BattleNPCGameFSMAI.defaultFilter(self, request, args)

    def filterOff(self, request, args):
        # the creature's first state comes from the Off state, make sure that
        # request is filtered by our creature rules as well...
        return self.defaultFilter(request, args)

    def shouldFollowTarget(self, attackTarget):
        # stationary creatures never chase their attack target,
        # they will only attack the target when it is in range...
        if self.avatar.isStationary():
            return False

        return BattleNPCGameFSMAI.shouldFollowTarget(self, attackTarget)

    def getSkillsInRange(self, attackTarget, skillList):
        skillsInRange = []
        for skillId in skillList:
            if self.air.battleMgr.getTargetInRange(self.avatar, attackTarget, skillId, 0):
                skillsInRange.append(skillId)

        return skillsInRange

    def _chooseNextAttack(self, task):
        if not self.avatar.isStationary():
            return BattleNPCGameFSMAI._chooseNextAttack(self, task)

        currentTarget = self.avatar.currentTarget
        if not currentTarget:
            task.setDelay(WeaponGlobals.SHORT_DELAY)
            return task.again

        # stunned creatures cannot attack until the stun wears off...
        if WeaponGlobals.C_STUN in self.avatar.getSkillEffectIds():
            task.setDelay(self.StunnedAttackDelay)
            return task.again

        # since we cannot move closer to our target, we can only use the skills
        # that will actually reach it; if none do then just wait for the
        # target to move back into our range...
        skillList = self.getSkillsInRange(currentTarget, self.getUsableSkills())
        if not skillList:
            task.setDelay(WeaponGlobals.SHORT_DELAY)
            return task.again

        skillId = random.choice(skillList)

        # enemy skills only hit our current target, see BattleNPCGameFSMAI._chooseNextAttack
        areaIdList = []
        timestamp = globalClockDelta.getRealNetworkTime(bits=16)
        self.avatar.useTargetedSkill(self.avatar, currentTarget, skillId, 0, areaIdList, timestamp, self.avatar.getPos(), 0)

        delay = WeaponGlobals.getAttackDelay(skillId)
        delay += WeaponGlobals.getAttackDuration(skillId)
        delay += self.getAttackDelayModdifier()

        task.setDelay(delay)
        return task.again
