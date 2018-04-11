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
            self.notify.debug('Cannot calculate targeted skill for unknown avartar!')
            return

        if not target:
            self.notify.debug('Cannot calculate targeted skill for avatar %d, unknown target!' % (
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
            target.b_setHp(target.getHp()[0] + targetEffects[0], True)
            target.b_setPower(target.getPower() + targetEffects[1])
            target.b_setLuck(target.getLuck() + targetEffects[2])
            target.b_setMojo(target.getMojo() + targetEffects[3])
            target.b_setSwiftness(target.getSwiftness() + targetEffects[4])
        elif skillResult == WeaponGlobals.RESULT_MISS:
            pass
        elif skillResult == WeaponGlobals.RESULT_DODGE:
            pass
        elif skillResult == WeaponGlobals.RESULT_PARRY:
            pass
        elif skillResult == WeaponGlobals.RESULT_RESIST:
            pass

        return [skillId, ammoSkillId, skillResult, target.doId, areaIdList, attackerEffects, targetEffects,
            areaIdEffects, timestamp, pos, charge]
