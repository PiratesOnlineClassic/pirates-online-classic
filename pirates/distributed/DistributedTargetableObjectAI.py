from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from pirates.battle.ComboDiaryAI import ComboDiaryAI
from pirates.piratesbase import PiratesGlobals


class DistributedTargetableObjectAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTargetableObjectAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def generate(self):
        DistributedObjectAI.generate(self)

        self.comboDiary = ComboDiaryAI(self.air, self)

    def getDamagable(self):
        return True

    def setCombo(self, combo, teamCombo, comboDamage, attackerId=0):
        # only battle avatars broadcast their combo (see DistributedBattleAvatarAI),
        # any other targetable object just keeps it, like the client's...
        self.combo = combo
        self.teamCombo = teamCombo
        self.comboDamage = comboDamage
        self.attackerId = attackerId

    def b_setCombo(self, combo, teamCombo, comboDamage, attackerId=0):
        self.setCombo(combo, teamCombo, comboDamage, attackerId)

    def resetComboLevel(self, args=None):
        pass

    def requestTarget(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        # only objects that are registered with the target manager
        # can be targeted by an attacker...
        if not self.air.targetMgr.hasTarget(self.doId):
            self.notify.debug('Avatar %d requested target on non-targetable object %d!' % (
                avatar.doId, self.doId))

            return

        self.air.targetMgr.addAttacker(avatar, self)

    def removeTarget(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if not self.air.targetMgr.hasAttacker(avatar.doId, self.doId):
            return

        self.air.targetMgr.removeAttacker(avatar, self)
