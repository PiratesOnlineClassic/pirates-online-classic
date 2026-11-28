import random

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClockDelta import globalClockDelta

from pirates.pirate.BattleNPCGameFSMAI import BattleNPCGameFSMAI
from pirates.battle import WeaponGlobals


class BossNPCGameFSMAI(BattleNPCGameFSMAI):
    notify = directNotify.newCategory('BossNPCGameFSMAI')

    def _chooseNextAttack(self, task):
        # bosses also get to use their own special skills along
        # with the skills of their non boss avatar type.
        skillId = random.choice(self.avatar.getAttackSkills())

        areaIdList = self.air.targetMgr.getAttackers(self.avatar.doId)
        timestamp = globalClockDelta.getRealNetworkTime(bits=16)
        self.avatar.useTargetedSkill(self.avatar, self.avatar.currentTarget, skillId, 0, areaIdList, timestamp, self.avatar.getPos(), 0)

        delay = WeaponGlobals.getAttackDelay(skillId)
        delay += WeaponGlobals.getAttackDuration(skillId)
        delay += self.getAttackDelayModdifier()

        task.setDelay(delay)
        return task.again
