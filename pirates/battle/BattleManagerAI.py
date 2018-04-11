from pirates.battle.BattleManagerBase import BattleManagerBase
from direct.directnotify import DirectNotifyGlobal
from pirates.battle import WeaponGlobals
from direct.distributed.ClockDelta import globalClockDelta

class BattleManagerAI(BattleManagerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleManagerAI')

    def __init__(self, air):
        self.air = air

    def calculateTargetedSkill(self, avatar, target, skillId, ammoSkillId, clientResult, areaIdList, timestamp, pos, charge):
        if not avatar:
            self.notify.warning('Cannot calculate targeted skill for unknown avatar!')
            return

        if not target:
            self.notify.warning('Cannot calculate targeted skill for avatar %d, unknown target!' % (
                avatar.doId))

            return

        skillResult = self.willWeaponHit(avatar, target, skillId,
            ammoSkillId, charge)

        timestamp = globalClockDelta.getRealNetworkTime(bits=32)
        distance = avatar.getDistance(target)

        attackerEffects, targetEffects = self.getModifiedSkillEffects(avatar, target,
            skillId, ammoSkillId, charge, distance)

        areaIdEffects = [
            attackerEffects,
            targetEffects
        ]

        if skillResult == WeaponGlobals.RESULT_HIT:
            self.__applyTargetEffects(target, targetEffects)
        elif skillResult == WeaponGlobals.RESULT_MISS:
            pass
        elif skillResult == WeaponGlobals.RESULT_DODGE:
            pass
        elif skillResult == WeaponGlobals.RESULT_PARRY:
            pass
        elif skillResult == WeaponGlobals.RESULT_RESIST:
            pass
        else:
            self.notify.warning('Cannot calculate targeted skill, unknown weapon skill result was found, %d!' % (
                skillResult))

        return [skillId, ammoSkillId, skillResult, target.doId, areaIdList, attackerEffects, targetEffects,
            areaIdEffects, timestamp, pos, charge]

    def __applyTargetEffects(self, target, targetEffects):
        if not target:
            self.notify.warning('Cannot apply target effects for unknown target!')
            return

        target.b_setHp(target.getHp()[0] + targetEffects[0])
        target.b_setPower(target.getPower() + targetEffects[1])
        target.b_setLuck(target.getLuck() + targetEffects[2])
        target.b_setMojo(target.getMojo() + targetEffects[3])
        target.b_setSwiftness(target.getSwiftness() + targetEffects[4])

    def __applyAttackerEffects(self, avatar, attackerEffects):
        if not target:
            self.notify.warning('Cannot apply attacker effects for unknown avatar!')
            return

        avatar.b_setHp(avatar.getHp()[0] + targetEffects[0])
        avatar.b_setPower(avatar.getPower() + targetEffects[1])
        avatar.b_setLuck(avatar.getLuck() + targetEffects[2])
        avatar.b_setMojo(avatar.getMojo() + targetEffects[3])
        avatar.b_setSwiftness(avatar.getSwiftness() + targetEffects[4])
