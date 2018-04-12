from direct.directnotify import DirectNotifyGlobal
from pirates.battle.WeaponBaseBase import WeaponBaseBase

class WeaponBaseAI(WeaponBaseBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('WeaponBaseAI')

    def __init__(self, air):
        self.air = air

    def requestTargetedSkill(self, skillId, ammoSkillId, clientResult, targetId, areaIdList, timestamp, pos, charge):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            self.notify.warning('Cannot request targeted skill, unknown avatar!')
            return

        target = self.air.doId2do.get(targetId)

        if not target:
            self.notify.debug('Cannot request targeted skill for avatar %d, unknown specified target!' % (
                avatar.doId))
        else:
            self.__useTargetedSkill(avatar, target, skillId, ammoSkillId, clientResult,
                areaIdList, timestamp, pos, charge)

        for targetId in areaIdList:

            if targetId is avatar.doId:
                continue

            target = self.air.doId2do.get(targetId)

            if not target:
                self.notify.debug('Cannot request targeted skill for avatar %d, unknown areaId target!' % (
                    avatar.doId))

                continue

            self.__useTargetedSkill(avatar, target, skillId, ammoSkillId, clientResult,
                areaIdList, timestamp, pos, charge)

    def __useTargetedSkill(self, avatar, target, skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge):
        targetResult = self.air.battleMgr.useTargetedSkill(avatar, target, skillId, ammoSkillId,
            clientResult, areaIdList, timestamp, pos, charge)

        if not targetResult:
            self.notify.debug('Cannot handle targeted skill for avatar %d, no valid result was given!' % (
                avatar.doId))

            return

        self.sendUpdate('useTargetedSkill', targetResult)
