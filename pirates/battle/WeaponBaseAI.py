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
            self.__useSpecialTargetedSkill(avatar, target, skillId, ammoSkillId, clientResult,
                areaIdList, timestamp, pos, charge)
        else:
            self.__useTargetedSkill(avatar, target, skillId, ammoSkillId, clientResult,
                areaIdList, timestamp, pos, charge)

        for targetId in areaIdList:

            if targetId == avatar.doId:
                continue

            target = self.air.doId2do.get(targetId)

            if not target:
                self.notify.debug('Cannot request targeted skill, unknown areaId target; avatarId=%d!' % (
                    avatar.doId))

                continue

            self.__useTargetedSkill(avatar, target, skillId, ammoSkillId, clientResult,
                areaIdList, timestamp, pos, charge)

    def __useTargetedSkill(self, avatar, target, skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge):
        targetResult = self.air.battleMgr.getTargetedSkillResult(avatar, target, skillId, ammoSkillId,
            clientResult, areaIdList, timestamp, pos, charge)

        if not targetResult:
            self.notify.debug('Cannot get targeted skill, no valid result was given; avatarId=%d, targetId=%d, skillId=%d!' % (
                avatar.doId, target.doId, skillId))

            return

        self.d_useTargetedSkill(*targetResult)

    def __useSpecialTargetedSkill(self, avatar, target, skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge):
        specialResult = self.air.battleMgr.getSpecialTargetedSkillResult(avatar, target, skillId, ammoSkillId,
            clientResult, areaIdList, timestamp, pos, charge)

        if not specialResult:
            self.notify.debug('Cannot get special targeted skill, no valid result was given; avatarId=%d, skillId=%d!' % (
                avatar.doId, skillId))

            return

        self.d_useTargetedSkill(*specialResult)

    def d_useTargetedSkill(self, skillId, ammoSkillId, skillResult, targetDoId, areaIdList, attackerEffects, targetEffects, areaIdEffects, timestamp, pos, charge):
        self.sendUpdate('useTargetedSkill', [skillId, ammoSkillId, skillResult, targetDoId, areaIdList, attackerEffects,
            targetEffects, areaIdEffects, timestamp, pos, charge])
