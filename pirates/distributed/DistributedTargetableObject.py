import random
import types

from direct.distributed import DistributedNode
from direct.interval.IntervalGlobal import *
from panda3d.core import *
from pirates.battle import ClientComboDiary, WeaponGlobals
from pirates.effects import CombatEffect
from pirates.effects.AttuneSmoke import AttuneSmoke
from pirates.pirate import AvatarTypes
from pirates.uberdog.UberDogGlobals import InventoryType


class DistributedTargetableObject(DistributedNode.DistributedNode):
    NoPain = base.config.GetBool('no-pain', 0)

    def __init__(self, cr):
        DistributedNode.DistributedNode.__init__(self, cr)
        self.comboDiary = None
        self.isTeamCombo = 0
        self.currentWeapon = None
        self.height = 5
        self.gameFSM = None
        self.voodooSmokeEffect2 = None

    def getHeight(self):
        return self.height

    def generate(self):
        DistributedNode.DistributedNode.generate(self)
        self.ouchAnim = None

    def disable(self):
        DistributedNode.DistributedNode.disable(self)
        if self.ouchAnim:
            self.ouchAnim.pause()
            self.ouchAnim = None
        if self.voodooSmokeEffect2:
            self.voodooSmokeEffect2.stopLoop()
            self.voodooSmokeEffect2 = None

    def delete(self):
        DistributedNode.DistributedNode.delete(self)
        if self.comboDiary:
            self.comboDiary.cleanup()
            self.comboDiary = None
        self.currentWeapon = None

    def initializeBattleCollisions(self):
        pass

    def deleteBattleCollisions(self):
        pass

    def stashBattleCollisions(self):
        pass

    def unstashBattleCollisions(self):
        pass

    def isDistributed(self):
        return 1

    def setTargetZ(self, z):
        self.targetZ = z

    def setViewpoint(self, viewpointIndex=0):
        camera.reparentTo(self)

    def resetComboLevel(self, args=None):
        pass

    def setLocalTarget(self, on):
        pass

    def showHpMeter(self):
        pass

    def hideHpMeter(self, delay=0.0):
        pass

    def playHitSound(self, skillId, ammoSkillId, skillResult):
        if WeaponGlobals.getIsStaffChargeSkill(skillId):
            return
        if WeaponGlobals.getIsStaffAttackSkill(skillId):
            return
        skillInfo = WeaponGlobals.getSkillAnimInfo(skillId)
        if skillInfo:
            soundFx = None
            sfxs = None
            if skillResult == WeaponGlobals.RESULT_HIT:
                getHitSfxFunc = skillInfo[WeaponGlobals.HIT_SFX_INDEX]
                if getHitSfxFunc:
                    sfxs = getHitSfxFunc()
            else:
                getMissSfxFunc = skillInfo[WeaponGlobals.MISS_SFX_INDEX]
                if getMissSfxFunc:
                    sfxs = getMissSfxFunc()
            if sfxs:
                if type(sfxs) == types.DictType:
                    soundFx = sfxs.get(ammoSkillId)
                elif type(sfxs) == types.TupleType:
                    soundFx = random.choice(sfxs)
                else:
                    soundFx = sfxs
            if soundFx:
                base.playSfx(soundFx, node=self, volume=0.7, cutoff=100)

    def setCombo(self, combo, teamCombo, comboDamage, attackerId=0):
        pass

    def addCombo(self, attackerId, skillId, damage=0):
        if self.comboDiary is None:
            self.comboDiary = ClientComboDiary.ClientComboDiary(self)
        self.comboDiary.recordAttack(attackerId, skillId, damage)
        hasCombo = self.comboDiary.hasCombo(attackerId)
        if hasCombo:
            combo, comboDamage, teamCombo = self.comboDiary.getCombo()
            self.setCombo(combo, self.isTeamCombo, comboDamage)

    def cleanupOuchIval(self):
        pass

    def playOuch(self,
                 skillId,
                 ammoSkillId,
                 targetEffects,
                 attacker,
                 pos,
                 multihit=0,
                 targetBonus=0):
        targetHp, targetPower, targetEffect, targetMojo, targetSwiftness = targetEffects
        if attacker:
            self.addCombo(attacker.getDoId(), skillId, -targetHp)
        self.cleanupOuchIval()
        if not targetBonus:
            if ammoSkillId:
                effectId = WeaponGlobals.getHitEffect(ammoSkillId)
            else:
                effectId = WeaponGlobals.getHitEffect(skillId)
        if not targetBonus and not self.NoPain and targetEffects[0] < 0:
            if self.gameFSM.state not in ('Ensnared', 'Knockdown', 'Stunned',
                                          'Rooted', 'NPCInteract',
                                          'ShipBoarding'):
                ouchSfx = None
                if self.currentWeapon:
                    if not self.avatarType.isA(
                            AvatarTypes.Creature
                    ) and effectId == WeaponGlobals.VFX_BLIND:
                        actorIval = self.actorInterval(
                            'sand_in_eyes_holdweapon_noswing',
                            playRate=random.uniform(0.7, 1.5))
                    else:
                        actorIval = self.actorInterval(
                            self.currentWeapon.painAnim,
                            playRate=random.uniform(0.7, 1.5))
                        if WeaponGlobals.getIsStaffAttackSkill(skillId):
                            skillInfo = WeaponGlobals.getSkillAnimInfo(skillId)
                            getOuchSfxFunc = skillInfo[
                                WeaponGlobals.OUCH_SFX_INDEX]
                            if getOuchSfxFunc:
                                ouchSfx = getOuchSfxFunc()
                        else:
                            ouchSfx = self.getSfx('pain')
                else:
                    if not self.avatarType.isA(
                            AvatarTypes.Creature
                    ) and effectId == WeaponGlobals.VFX_BLIND:
                        actorIval = self.actorInterval(
                            'sand_in_eyes', playRate=random.uniform(0.7, 1.5))
                    else:
                        actorIval = self.actorInterval(
                            'boxing_hit_head_right',
                            playRate=random.uniform(0.7, 1.5))
                if ouchSfx:
                    self.ouchAnim = Sequence(
                        Func(base.playSfx, ouchSfx, node=self, cutoff=100),
                        actorIval)
                else:
                    self.ouchAnim = actorIval
                self.ouchAnim.start()
        effect = CombatEffect.CombatEffect(effectId, multihit, attacker)
        effect.reparentTo(self)
        effect.setPos(self, pos[0], pos[1], pos[2])
        if not WeaponGlobals.getIsDollAttackSkill(
                skillId) and not WeaponGlobals.getIsStaffAttackSkill(skillId):
            if attacker and not attacker.isEmpty():
                effect.lookAt(attacker)
            effect.setH(effect, 180)
        effect.play()
        if WeaponGlobals.getIsDollAttackSkill(skillId):
            self.voodooSmokeEffect2 = AttuneSmoke.getEffect()
            if self.voodooSmokeEffect2:
                self.voodooSmokeEffect2.reparentTo(self)
                self.voodooSmokeEffect2.setPos(0, 0, 0.2)
                self.voodooSmokeEffect2.play()

    def showHpString(self, text, pos=0, duration=2.0, scale=0.5):
        pass

    def packMultiHitEffects(self, targetEffects, numHits):
        if numHits <= 1:
            return targetEffects
        divDamage = int(targetEffects[0] / numHits + 1)
        multiHitEffects = []
        multiHitEffects.append(list(targetEffects))
        multiHitEffects[0][0] = divDamage
        for i in range(numHits - 2):
            multiHitEffects.append([divDamage, 0, 0, 0, 0])

        multiHitEffects.append(
            [targetEffects[0] - divDamage * (numHits - 1), 0, 0, 0, 0])
        return multiHitEffects

    def useTargetedSkill(self,
                         skillId,
                         ammoSkillId,
                         skillResult,
                         targetId,
                         areaIdList,
                         attackerEffects,
                         targetEffects,
                         areaIdEffects,
                         timestamp,
                         pos,
                         charge=0,
                         localSignal=0):
        if not self.isLocal() or localSignal:
            multiHits = []
            numHits = WeaponGlobals.getNumHits(skillId)
            hitTiming = WeaponGlobals.getMultiHitAttacks(skillId)
            if hitTiming:
                multiHits += hitTiming
            if ammoSkillId:
                numHits += WeaponGlobals.getNumHits(ammoSkillId) - 1
                hitTiming = WeaponGlobals.getMultiHitAttacks(ammoSkillId)
                if hitTiming:
                    multiHits += hitTiming
            if not targetId and areaIdList:
                self.playSkillMovie(skillId, ammoSkillId, skillResult, charge,
                                    areaIdList[0])
            else:
                self.playSkillMovie(skillId, ammoSkillId, skillResult, charge,
                                    targetId)
            if self.currentTarget and targetId:
                if multiHits and numHits:
                    multiHitEffects = self.packMultiHitEffects(
                        targetEffects, numHits)
                    for i in range(numHits):
                        self.currentTarget.targetedWeaponHit(
                            skillId, ammoSkillId, skillResult,
                            multiHitEffects[i], self, pos, charge, multiHits[i],
                            i)

                else:
                    self.currentTarget.targetedWeaponHit(
                        skillId, ammoSkillId, skillResult, targetEffects, self,
                        pos, charge)
            for targetId, areaEffects in zip(areaIdList, areaIdEffects):
                target = self.cr.doId2do.get(targetId)
                if target:
                    if multiHits and numHits:
                        multiHitEffects = self.packMultiHitEffects(
                            areaEffects, numHits)
                        for i in range(numHits):
                            target.targetedWeaponHit(
                                skillId, ammoSkillId, skillResult,
                                multiHitEffects[i], self, pos, charge,
                                multiHits[i], i)

                    else:
                        target.targetedWeaponHit(skillId, ammoSkillId,
                                                 skillResult, areaEffects, self,
                                                 pos, charge)

            if not self.currentTarget and not areaIdList:
                self.playHitSound(skillId, ammoSkillId,
                                  WeaponGlobals.RESULT_MISS)

    def getProjectileInfo(self, skillId, target):
        throwSpeed = WeaponGlobals.getProjectileSpeed(skillId)
        if not throwSpeed:
            return (None, None, None)
        placeHolder = self.attachNewNode('projectilePlaceHolder')
        if target:
            if not target.isEmpty():
                placeHolder.setPos(render, target.getPos(render))
                placeHolder.setZ(placeHolder, target.getHeight() * 0.666)
        else:
            range = WeaponGlobals.getProjectileDefaultRange(skillId)
            if self == localAvatar:
                placeHolder.setPos(camera, 0, range[0], range[1])
            else:
                placeHolder.setPos(self, 0, range[0], 4.0)
        dist = self.getDistance(placeHolder)
        time = dist / throwSpeed
        impactT = time
        animT = WeaponGlobals.getProjectileAnimT(skillId)
        if animT:
            impactT += animT
        targetPos = placeHolder.getPos(render)
        placeHolder.removeNode()
        return (targetPos, time, impactT)

    def targetedWeaponHit(self,
                          skillId,
                          ammoSkillId,
                          skillResult,
                          targetEffects,
                          attacker,
                          pos,
                          charge=0,
                          delay=None,
                          multihit=0):
        if self == attacker and not (targetEffects[0] or targetEffects[1] or
                                     targetEffects[2] or targetEffects[4]):
            return
        if not delay:
            targetPos, time, impactT = self.getProjectileInfo(skillId, attacker)
            if impactT:
                delay = impactT
            else:
                delay = WeaponGlobals.getAttackReactionDelay(
                    skillId, ammoSkillId)
        if WeaponGlobals.getIsDollAttackSkill(skillId):
            delay += random.uniform(0.0, 0.5)
        if attacker and attacker.isLocal():
            centerEffect = WeaponGlobals.getCenterEffect(skillId, ammoSkillId)
            if centerEffect == 2 or not (
                    self.avatarType.isA(AvatarTypes.Stump) or
                    self.avatarType.isA(AvatarTypes.FlyTrap) or
                    self.avatarType.isA(AvatarTypes.GiantCrab)):
                pos = Vec3(0, 0, self.height * 0.666)
            elif centerEffect == 1:
                newZ = attacker.getZ(self)
                pos = Vec3(0, 0, newZ + attacker.height * 0.666)
            else:
                newPos = self.cr.targetMgr.getAimHitPos(attacker)
                if newPos:
                    pos = Vec3(newPos[0], newPos[1], newPos[2] + 1.5)
        else:
            centerEffect = WeaponGlobals.getCenterEffect(skillId, ammoSkillId)
            if centerEffect >= 1:
                pos = Vec3(0, 0, self.height * 0.666)
        if delay > 0.0:
            taskMgr.doMethodLater(
                delay,
                self.playHitSound,
                self.taskName('playHitSoundTask'),
                extraArgs=[skillId, ammoSkillId, skillResult])
        else:
            self.playHitSound(skillId, ammoSkillId, skillResult)
        if skillResult == WeaponGlobals.RESULT_HIT:
            bonus = 0
            if bonus:
                targetEffects[0] -= bonus
            if delay > 0.0:
                taskMgr.doMethodLater(
                    delay,
                    self.playOuch,
                    self.taskName('playOuchTask'),
                    extraArgs=[
                        skillId, ammoSkillId, targetEffects, attacker, pos,
                        multihit
                    ])
            else:
                self.playOuch(skillId, ammoSkillId, targetEffects, attacker,
                              pos, multihit)
            if bonus:
                taskMgr.doMethodLater(
                    WeaponGlobals.COMBO_DAMAGE_DELAY,
                    self.playOuch,
                    self.taskName('playBonusOuchTask'),
                    extraArgs=[
                        skillId, ammoSkillId, [bonus, 0, 0, 0, 0], attacker,
                        pos, multihit, 1
                    ])
            if skillId in InventoryType.BackstabSkills and charge:
                if attacker and attacker.isLocal():
                    messenger.send(('').join(['trackBackstab-',
                                              str(self.doId)]))
        else:
            if skillResult == WeaponGlobals.RESULT_MISS or skillResult == WeaponGlobals.RESULT_DODGE or skillResult == WeaponGlobals.RESULT_PARRY or skillResult == WeaponGlobals.RESULT_RESIST:
                resultString = WeaponGlobals.getSkillResultName(skillResult)
                delay = WeaponGlobals.getAttackReactionDelay(
                    skillId, ammoSkillId)
                if delay > 0.0:
                    taskMgr.doMethodLater(
                        delay,
                        self.showHpString,
                        self.taskName('showMissTask'),
                        extraArgs=[resultString, pos])
                else:
                    self.showHpString(resultString, pos)
            else:
                if skillResult == WeaponGlobals.RESULT_OUT_OF_RANGE:
                    pass
                else:
                    if skillResult == WeaponGlobals.RESULT_AGAINST_PIRATE_CODE:
                        if attacker and attacker.isLocal():
                            resultString = WeaponGlobals.getSkillResultName(
                                skillResult)
                            self.showHpString(resultString, pos)
                    else:
                        if skillResult == WeaponGlobals.RESULT_NOT_AVAILABLE:
                            self.notify.warning(
                                'WeaponGlobals.RESULT_NOT_AVAILABLE')
                        else:
                            self.notify.error(
                                'unknown skillResult: %d' % skillResult)

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult,
                            targetEffects, pos, normal, codes, attacker):
        self.targetedWeaponHit(skillId, ammoSkillId, skillResult, targetEffects,
                               attacker, pos)

    def takeDamage(self, hpLost, pos, bonus=0):
        shipId = 0
        if base.localAvatar.ship:
            shipId = base.localAvatar.ship.getDoId()
        if self.hp == None or hpLost < 0:
            return
        self.refreshStatusTray()
        if hpLost > 0:
            self.showHpText(-hpLost, pos, bonus)
            self.hpChange(quietly=0)

    def takeMpDamage(self, mpLost, pos, bonus=3):
        if self.mojo == None or mpLost < 0 or self.mojo <= 0:
            return
        if mpLost > 0:
            self.showHpText(-mpLost, pos, bonus)

    def respawn(self):
        pass
