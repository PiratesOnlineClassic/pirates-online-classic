from direct.directnotify import DirectNotifyGlobal
from pirates.battle.WeaponBaseBase import WeaponBaseBase

class WeaponBaseAI(WeaponBaseBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('WeaponBaseAI')

    def __init__(self, air):
        self.air = air

    def requestTargetedSkill(self, skillId, ammoSkillId, clientResult, targetId, areaIdList, timestamp, pos, charge):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        target = self.air.doId2do.get(targetId)

        if not target:
            return

        self.sendUpdate('useTargetedSkill', self.air.battleMgr.calculateTargetedSkill(avatar, target, skillId,
            ammoSkillId, clientResult, areaIdList, timestamp, pos, charge))
