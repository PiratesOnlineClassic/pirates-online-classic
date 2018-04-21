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

        # this will handle the attackers targeted skill request, however we will not check if the target
        # specified in this update is valid. Because, if their is no target then the client is
        # just requesting targeted skill for no target...
        self.__useTargetedSkill(avatar, target, skillId, ammoSkillId, clientResult,
            areaIdList, timestamp, pos, charge)

        # this will handle the targeted skill for any targets in the range of the attacker,
        # for example if an attacker uses a skill that effects enemies around it...
        for targetId in areaIdList:

            # ignore the avatar if it is in the area list,
            # no reason to handle it here...
            if targetId == avatar.doId:
                continue

            target = self.air.doId2do.get(targetId)

            if not target:
                self.notify.debug('Cannot request targeted skill, unknown areaId target; avatarId=%d skillId=%d!' % (
                    avatar.doId, skillId))

                continue

            self.__useTargetedSkill(avatar, target, skillId, ammoSkillId, clientResult,
                areaIdList, timestamp, pos, charge)

    def __useTargetedSkill(self, avatar, target, skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge):
        targetResult = self.air.battleMgr.getTargetedSkillResult(avatar, target, skillId, ammoSkillId,
            clientResult, areaIdList, timestamp, pos, charge)

        if not targetResult:
            self.notify.debug('Cannot get targeted skill, no valid result was given; avatarId=%d, skillId=%d!' % (
                avatar.doId, skillId))

            return

        self.d_useTargetedSkill(*targetResult)

    def d_useTargetedSkill(self, skillId, ammoSkillId, skillResult, targetDoId, areaIdList, attackerEffects, targetEffects, areaIdEffects, timestamp, pos, charge):
        self.sendUpdate('useTargetedSkill', [skillId, ammoSkillId, skillResult, targetDoId, areaIdList, attackerEffects,
            targetEffects, areaIdEffects, timestamp, pos, charge])
