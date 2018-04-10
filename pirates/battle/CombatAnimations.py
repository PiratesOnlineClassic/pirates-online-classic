# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.battle.CombatAnimations
import random

import WeaponGlobals
from direct.actor import Actor
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.interval.IntervalGlobal import *
from GrenadeProjectile import GrenadeProjectile
from pandac.PandaModules import *
from pirates.effects.AttuneSmoke import AttuneSmoke
from pirates.effects.BeamEffect import BeamEffect
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.DaggerProjectile import DaggerProjectile
from pirates.effects.DarkPortal import DarkPortal
from pirates.effects.DarkStar import DarkStar
from pirates.effects.DesolationChargeSmoke import DesolationChargeSmoke
from pirates.effects.DesolationSmoke import DesolationSmoke
from pirates.effects.DomeExplosion import DomeExplosion
from pirates.effects.DustRing import DustRing
from pirates.effects.EnergySpiral import EnergySpiral
from pirates.effects.EvilRingEffect import EvilRingEffect
from pirates.effects.FadingCard import FadingCard
from pirates.effects.FlamingSkull import FlamingSkull
from pirates.effects.HealSparks import HealSparks
from pirates.effects.HomingMissile import HomingMissile
from pirates.effects.JollySoulDrain import JollySoulDrain
from pirates.effects.MusketFlame import MusketFlame
from pirates.effects.MusketSmoke import MusketSmoke
from pirates.effects.MuzzleFlash import MuzzleFlash
from pirates.effects.NovaStar import NovaStar
from pirates.effects.Pestilence import Pestilence
from pirates.effects.PistolFlame import PistolFlame
from pirates.effects.PistolSmoke import PistolSmoke
from pirates.effects.ShockwaveRing import ShockwaveRing
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.SoulFlay import SoulFlay
from pirates.effects.SoulHarvest import SoulHarvest
from pirates.effects.SoulHarvest2 import SoulHarvest2
from pirates.effects.SoulSpiral import SoulSpiral
from pirates.effects.SpectralSmoke import SpectralSmoke
from pirates.effects.SpectralTrail import SpectralTrail
from pirates.effects.ThrowDirt import ThrowDirt
from pirates.effects.UnholyFlare import UnholyFlare
from pirates.effects.VenomSpitProjectile import VenomSpitProjectile
from pirates.effects.VoodooAura import VoodooAura
from pirates.effects.VoodooFire import VoodooFire
from pirates.effects.VoodooGlow import VoodooGlow
from pirates.effects.VoodooPestilence import VoodooPestilence
from pirates.effects.VoodooPower import VoodooPower
from pirates.effects.VoodooProjectile import VoodooProjectile
from pirates.effects.VoodooSouls import VoodooSouls
from pirates.effects.VoodooStaffFire import VoodooStaffFire
from pirates.effects.WindBlurCone import WindBlurCone
from pirates.effects.WindCharge import WindCharge
from pirates.effects.WindWave import WindWave
from pirates.effects.WispSpiral import WispSpiral
from pirates.effects.WitherCharge import WitherCharge
from pirates.piratesbase import PLocalizer
from pirates.uberdog.UberDogGlobals import InventoryType
from otp.nametag.NametagConstants import *


class CombatAnimations:
    __module__ = __name__
    notify = directNotify.newCategory('CombatAnimations')
    BASE_GRENADE_POWER = 0.8

    def getHack(self, av, skillId, ammoSkillId, charge, target):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('cutlass_combo', playRate=1.0, startFrame=4, endFrame=30, blendInT=0.2, blendOutT=0.3), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(0.625), Func(self.unlockInput, av)))
        return ival

    def getSlash(self, av, skillId, ammoSkillId, charge, target):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.3), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('cutlass_combo', playRate=1.0, startFrame=31, endFrame=62, blendInT=0.5, blendOutT=0.3), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(0.75), Func(self.unlockInput, av)))
        return ival

    def getCleave(self, av, skillId, ammoSkillId, charge, target):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('cutlass_combo', playRate=1.0, startFrame=63, endFrame=101, blendInT=0.5, blendOutT=0.3), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(1.125), Func(self.unlockInput, av)))
        return ival

    def getFlourish(self, av, skillId, ammoSkillId, charge, target):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('cutlass_combo', playRate=1.0, startFrame=102, endFrame=150, blendInT=0.5, blendOutT=0.3), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(1.58), Func(self.unlockInput, av)))
        return ival

    def getThrust(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = WindBlurCone.getEffect()
                if effect and not av.currentWeapon.isEmpty():
                    if av.currentWeapon.itemId == InventoryType.CutlassWeaponL6:
                        effect.setBlendModeOff()
                    else:
                        effect.setBlendModeOn()
                    effect.fadeColor = av.currentWeapon.getBlurColor()
                    effect.reparentTo(av.currentWeapon)
                    effect.fadeTime = 0.4
                    effect.setPos(0, 0, 0)
                    effect.setScale(1)
                    effect.setH(0)
                    effect.play()

        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.5), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('cutlass_combo', playRate=1.0, startFrame=151, endFrame=164, blendInT=0.5, blendOutT=0), Func(av.currentWeapon.showSpinBlur), av.actorInterval('cutlass_combo', playRate=1.0, startFrame=165, endFrame=170, blendInT=0, blendOutT=0), Func(startVFX), av.actorInterval('cutlass_combo', playRate=1.0, startFrame=171, endFrame=175, blendInT=0, blendOutT=0), Func(av.currentWeapon.hideSpinBlur), av.actorInterval('cutlass_combo', playRate=1.0, startFrame=176, endFrame=210, blendInT=0, blendOutT=0.5), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(1.3), Func(self.unlockInput, av)))
        return ival

    def getSweep(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                shockwaveRingEffect = ShockwaveRing.getEffect()
                if shockwaveRingEffect:
                    shockwaveRingEffect.reparentTo(av)
                    shockwaveRingEffect.size = 40
                    shockwaveRingEffect.setPos(0, 0, 0)
                    shockwaveRingEffect.play()

        def startVFX2():
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                shockwaveRingEffect = ShockwaveRing.getEffect()
                if shockwaveRingEffect:
                    shockwaveRingEffect.reparentTo(av)
                    shockwaveRingEffect.size = 40
                    shockwaveRingEffect.setPos(0, 0, 3)
                    shockwaveRingEffect.play()
                dustRingEffect = DustRing.getEffect()
                if dustRingEffect:
                    dustRingEffect.reparentTo(av)
                    dustRingEffect.setPos(0, 0, 0)
                    dustRingEffect.play()

        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.7), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=1, endFrame=10, blendOutT=0), Func(startVFX), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=11, endFrame=15, blendInT=0, blendOutT=0), Func(startVFX2), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=16, endFrame=35, blendInT=0), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getBladestorm(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.55), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('cutlass_bladestorm', playRate=1.0, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getBrawl(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.3), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av))
        ival.append(av.actorInterval('cutlass_headbutt', playRate=1.0, blendInT=0.5, blendOutT=0.5))
        ival.append(Func(av.currentWeapon.endAttack, av))
        ival.append(Func(av.motionFSM.on))
        ival.append(Func(self.unlockInput, av))
        return ival

    def getTaunt(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.setChatAbsolute, PLocalizer.getTauntPhrase(), CFSpeech | CFTimeout), Func(av.currentWeapon.setTrailLength, 0.15), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('cutlass_taunt', playRate=1.0, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getCut(self, av, skillId, ammoSkillId, charge, target):
        ival = Parallel(Func(av.currentWeapon.playSkillSfx, skillId, av), Sequence(Func(self.lockInput, av), Func(av.currentWeapon.endAttack, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dagger_combo', playRate=1.0, startFrame=1, endFrame=28, blendInT=0.2, blendOutT=0.5)), Sequence(Wait(0.75), Func(self.unlockInput, av)))
        return ival

    def getSwipe(self, av, skillId, ammoSkillId, charge, target):
        ival = Parallel(Func(av.currentWeapon.playSkillSfx, skillId, av), Sequence(Func(self.lockInput, av), Func(av.currentWeapon.endAttack, av), Func(av.currentWeapon.setTrailLength, 0.3), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dagger_combo', playRate=1.0, startFrame=29, endFrame=53, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.hideSpinBlur)), Sequence(Wait(0.583), Func(self.unlockInput, av)), Sequence(Wait(0.1), Func(av.currentWeapon.showSpinBlur)))
        return ival

    def getGouge(self, av, skillId, ammoSkillId, charge, target):
        ival = Parallel(Func(av.currentWeapon.playSkillSfx, skillId, av), Sequence(Func(self.lockInput, av), Func(av.currentWeapon.endAttack, av), Func(av.currentWeapon.setTrailLength, 0.5), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dagger_combo', playRate=1.0, startFrame=54, endFrame=87, blendInT=0.5, blendOutT=0.5)), Sequence(Wait(0.958), Func(self.unlockInput, av)))
        return ival

    def getEviscerate(self, av, skillId, ammoSkillId, charge, target):
        ival = Parallel(Func(av.currentWeapon.playSkillSfx, skillId, av), Sequence(Func(self.lockInput, av), Func(av.currentWeapon.endAttack, av), Func(av.currentWeapon.setTrailLength, 0.6), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dagger_combo', playRate=1.0, startFrame=88, endFrame=142, blendInT=0.5, blendOutT=0.5)), Sequence(Wait(1.5), Func(self.unlockInput, av)))
        return ival

    def throwDagger(self, av, time, targetPos, motion_color=None, startOffset=Vec3(0, 0, 0), roll=0):
        if av:
            roll += random.uniform(-15.0, 15.0)
            effect = DaggerProjectile.getEffect()
            if effect:
                effect.reparentTo(render)
                effect.setPos(av.rightHandNode, startOffset)
                effect.setHpr(av.getH(render) + roll, 90 + roll, roll)
                effect.play(time, targetPos, motion_color)

    def getDaggerThrowDirtInterval(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            effect = ThrowDirt.getEffect()
            if effect:
                effect.reparentTo(render)
                effect.setPos(av.getPos(render))
                effect.setHpr(av.getHpr(render))
                effect.particleDummy.setPos(av.getPos(render))
                effect.particleDummy.setHpr(av.getHpr(render))
                effect.play()

        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(base.disableMouse), Func(av.currentWeapon.endAttack, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.hideWeapon), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dagger_throw_sand', playRate=1.0, startFrame=1, endFrame=10, blendInT=0.2, blendOutT=0), Func(av.currentWeapon.playSkillSfx, skillId, av), Func(startVFX), av.actorInterval('dagger_throw_sand', playRate=1.0, startFrame=11, endFrame=38, blendInT=0, blendOutT=0.3), Func(av.currentWeapon.showWeapon), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getDaggerAspInterval(self, av, skillId, ammoSkillId, charge, target):
        targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
        track = Sequence(Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('knife_throw', endFrame=17, blendInT=0.2, blendOutT=0), Parallel(av.actorInterval('knife_throw', startFrame=18, blendInT=0, blendOutT=0.4), Func(self.throwDagger, av, speed, targetPos), Func(av.currentWeapon.hideWeapon)), Func(av.currentWeapon.showWeapon), Func(self.unlockInput, av))
        return track

    def getDaggerAdderInterval(self, av, skillId, ammoSkillId, charge, target):
        motion_color = [
         Vec4(0.1, 1.0, 0.4, 1.0), Vec4(0.5, 1.0, 0.4, 1.0)]
        targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
        track = Sequence(Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('knife_throw', endFrame=17, blendInT=0.2, blendOutT=0), Parallel(av.actorInterval('knife_throw', startFrame=18, blendInT=0, blendOutT=0.4), Func(self.throwDagger, av, speed, targetPos, motion_color), Func(av.currentWeapon.hideWeapon)), Func(av.currentWeapon.showWeapon), Func(self.unlockInput, av))
        return track

    def getDaggerSidewinderInterval(self, av, skillId, ammoSkillId, charge, target):
        motion_color = [
         Vec4(1.0, 0.0, 0.0, 1.0), Vec4(1.0, 0.2, 0.0, 1.0)]
        targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
        track = Sequence(Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('dagger_asp', endFrame=7, blendInT=0.1, blendOutT=0), Parallel(av.actorInterval('dagger_asp', startFrame=8, blendInT=0, blendOutT=0.4), Func(self.throwDagger, av, speed, targetPos, motion_color, roll=90), Func(av.currentWeapon.hideWeapon)), Func(av.currentWeapon.showWeapon), Func(self.unlockInput, av))
        return track

    def getDaggerViperNestInterval(self, av, skillId, ammoSkillId, charge, target):
        numDaggers = 12.0
        time = 0.7
        placeHolder = av.attachNewNode('daggerPlaceHolder')
        daggerTossIval = Parallel(Sequence(Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.25), av.actorInterval('dagger_vipers_nest', startFrame=21, endFrame=35, blendInT=0, blendOutT=0.4), Func(av.currentWeapon.showWeapon), Func(av.motionFSM.on), Func(self.unlockInput, av)))
        for i in range(numDaggers):
            if av.isLocal():
                placeHolder.setPos(camera, random.uniform(-12, 12), random.uniform(100, 120), random.uniform(8, 18))
            else:
                placeHolder.setPos(av, random.uniform(-12, 12), random.uniform(100, 120), random.uniform(2, 12))
            targetPos = placeHolder.getPos(render)
            daggerTossIval.append(Func(self.throwDagger, av, time + random.uniform(-0.5, 1.0), targetPos, startOffset=Vec3(-3, 0, 0), roll=90))

        placeHolder.removeNode()
        track = Sequence(Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.hideWeapon), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('dagger_vipers_nest', endFrame=20, blendOutT=0), daggerTossIval)
        return track

    def getPistolChargingAnim(self, av, skillId, ammoSkillId, charge, target):
        track = Sequence(Func(base.cr.targetMgr.setWantAimAssist, 1), Func(av.setAimMod, -0.5), av.actorInterval('gun_aim_idle', loop=1, duration=9999, blendInT=0.3, blendOutT=0.3))
        return track

    def getPistolReloadAnim(self, av, skillId, ammoSkillId, charge, target):

        def finishReload():
            if av.isLocal():
                messenger.send('reloadFinished')

        if av.currentWeapon is not None and av.currentWeapon.getName() == 'pistol':
            sfx = av.currentWeapon.reloadSfx
        else:
            sfx = None
        track = Sequence(Func(self.lockInput, av), Func(av.setAimMod, 0), Func(base.playSfx, sfx, node=av), av.actorInterval('gun_reload', blendInT=0, blendOutT=0), Func(finishReload), Func(self.unlockInput, av))
        del finishReload
        return track

    def getPistolFireAnim(self, av, skillId, ammoSkillId, charge, target):
        if av.currentWeapon == None:
            return

        def startVFX():
            if base.cr.wantSpecialEffects and base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                pistolSmokeEffect = PistolSmoke.getEffect()
                if pistolSmokeEffect:
                    pistolSmokeEffect.reparentTo(av)
                    pistolSmokeEffect.setPos(av, 1.2, 2.5, 5)
                    pistolSmokeEffect.play()
                pistolFlameEffect = PistolFlame.getEffect()
                if pistolFlameEffect:
                    pistolFlameEffect.reparentTo(av)
                    pistolFlameEffect.particleDummy.reparentTo(av)
                    pistolFlameEffect.flash.setScale(30)
                    pistolFlameEffect.setPos(av, 1.2, 2.5, 5)
                    pistolFlameEffect.play()

        ival = Sequence(Func(base.cr.targetMgr.setWantAimAssist, 0), Func(self.lockInput, av), Func(av.setAimMod, 0), Func(startVFX), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('gun_fire', endFrame=12, blendInT=0.1, blendOutT=0), Func(self.unlockInput, av), av.actorInterval('gun_fire', startFrame=13, blendInT=0, blendOutT=0.3))
        del startVFX
        return ival

    def getPistolTakeAimAnim(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            if base.cr.wantSpecialEffects and base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                pistolSmokeEffect = PistolSmoke.getEffect()
                if pistolSmokeEffect:
                    pistolSmokeEffect.reparentTo(av)
                    pistolSmokeEffect.setPos(av, 1.2, 2.5, 5)
                    pistolSmokeEffect.play()
                pistolFlameEffect = PistolFlame.getEffect()
                if pistolFlameEffect:
                    pistolFlameEffect.reparentTo(av)
                    pistolFlameEffect.particleDummy.reparentTo(av)
                    pistolFlameEffect.flash.setScale(30)
                    pistolFlameEffect.setPos(av, 1.2, 2.5, 5)
                    pistolFlameEffect.play()

        ival = Parallel(Sequence(Func(base.cr.targetMgr.setWantAimAssist, 0), Func(av.setAimMod, 0), Func(self.lockInput, av), Func(startVFX), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('gun_fire', playRate=1, blendInT=0, blendOutT=0.3), Func(self.unlockInput, av)))
        del startVFX
        return ival

    def getGrenadeReloadAnim(self, av, skillId, ammoSkillId, charge, target):

        def finishReload():
            if av.isLocal():
                messenger.send('reloadFinished')

        if av.currentWeapon.ammoSkillId == InventoryType.GrenadeSiege:
            track = Sequence(Func(self.lockInput, av), Func(av.currentWeapon.detachFrom, av), av.actorInterval('bigbomb_draw', endFrame=11, blendInT=0, blendOutT=0), Func(av.currentWeapon.attachTo, av), av.actorInterval('bigbomb_draw', startFrame=12, blendInT=0, blendOutT=0.3), Func(finishReload), Func(self.unlockInput, av))
        else:
            track = Sequence(Func(self.lockInput, av), Func(av.currentWeapon.detachFrom, av), av.actorInterval('bomb_draw', endFrame=4, blendInT=0, blendOutT=0), Func(av.currentWeapon.attachTo, av), av.actorInterval('bomb_draw', startFrame=5, blendInT=0, blendOutT=0.3), Func(finishReload), Func(self.unlockInput, av))
        del finishReload
        return track

    def getGrenadeChargingAnim(self, av, skillId, ammoSkillId, charge, target):
        if av.currentWeapon.ammoSkillId == InventoryType.GrenadeSiege:
            track = Parallel(Sequence(Func(av.motionFSM.moveLock), Func(av.currentWeapon.hideMouse, av), av.actorInterval('bigbomb_charge', blendInT=0.3, blendOutT=0), av.actorInterval('bigbomb_charge_loop', loop=1, duration=9999, blendInT=0, blendOutT=0.3)), SoundInterval(av.currentWeapon.chargingSfx, loop=1, node=av))
        else:
            track = Parallel(Sequence(Func(av.setAimMod, -0.5), Func(av.currentWeapon.hideMouse, av), av.actorInterval('bomb_charge', blendInT=0.3, blendOutT=0), av.actorInterval('bomb_charge_loop', loop=1, duration=9999, blendInT=0, blendOutT=0.3)), SoundInterval(av.currentWeapon.chargingSfx, loop=1, node=av))
        return track

    def getGrenadeThrow(self, av, skillId, ammoSkillId, charge, target):
        if ammoSkillId == InventoryType.GrenadeSiege:
            attachTime = av.getFrameTime('bigbomb_throw', 40)
            track = Parallel(Func(self.lockInput, av), Func(av.setAimMod, 0), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.playSkillSfx, av.currentWeapon.ammoSkillId, av), Sequence(av.actorInterval('bigbomb_throw', blendInT=0.3, blendOutT=0.3), Func(av.motionFSM.on), Func(self.unlockInput, av)), Sequence(Wait(attachTime), Func(av.currentWeapon.detachFrom, av), Func(self.spawnGrenade, av, skillId, ammoSkillId, charge, target)))
        else:
            attachTime = av.getFrameTime('bomb_throw', 15)
            track = Parallel(Func(self.lockInput, av), Func(av.setAimMod, 0), Func(av.currentWeapon.playSkillSfx, skillId, av), Sequence(av.actorInterval('bomb_throw', blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av)), Sequence(Wait(attachTime), Func(av.currentWeapon.detachFrom, av), Func(self.spawnGrenade, av, skillId, ammoSkillId, charge, target)))
        return track

    def getGrenadeLongVolley(self, av, skillId, ammoSkillId, charge, target):
        if ammoSkillId == InventoryType.GrenadeSiege:
            attachTime = av.getFrameTime('bigbomb_charge_throw', 9)
            track = Parallel(Func(self.lockInput, av), Func(av.setAimMod, 0), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.playSkillSfx, av.currentWeapon.ammoSkillId, av), Sequence(av.actorInterval('bigbomb_charge_throw', blendInT=0.3, blendOutT=0.3), Func(av.motionFSM.on), Func(self.unlockInput, av)), Sequence(Wait(attachTime), Func(av.currentWeapon.detachFrom, av), Func(self.spawnGrenade, av, skillId, ammoSkillId, charge, target)))
        else:
            attachTime = av.getFrameTime('bomb_charge_throw', 11)
            track = Parallel(Func(self.lockInput, av), Func(av.setAimMod, 0), Func(av.currentWeapon.playSkillSfx, skillId, av, startTime=2.0), Sequence(av.actorInterval('bomb_charge_throw', blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av)), Sequence(Wait(attachTime), Func(av.currentWeapon.detachFrom, av), Func(self.spawnGrenade, av, skillId, ammoSkillId, charge, target)))
        return track

    def spawnGrenade(self, av, skillId, ammoSkillId, charge, target):
        grenade = GrenadeProjectile(av.cr, ammoSkillId, av.projectileHitEvent)
        grenade.detachNode()
        grenade.setBillboardPointEye()
        grenadeModelCol = grenade.find('**/collide')
        if grenadeModelCol and not grenadeModelCol.isEmpty():
            grenadeModelCol.removeNode()
        if av.isLocal():
            collNode = grenade.getCollNode()
            collNode.reparentTo(render)
        else:
            collNode = None
        av.ammoSequence = av.ammoSequence + 1 & 255
        grenade.setTag('ammoSequence', str(av.ammoSequence))
        grenade.setTag('skillId', str(int(skillId)))
        grenade.setTag('ammoSkillId', str(int(ammoSkillId)))
        grenade.setTag('attackerId', str(av.getDoId()))
        self.putGrenadeInHand(av, grenade)
        self.addCollider(av, grenade, collNode)
        self.throwGrenade(av, skillId, ammoSkillId, grenade, collNode, charge, target)
        return

    def addCollider(self, av, grenade, collNode):
        if av.isLocal():
            base.cTrav.addCollider(collNode, grenade.collHandler)

    def removeCollider(self, av, collNode):
        if av.isLocal():
            base.cTrav.removeCollider(collNode)

    def throwGrenade(self, av, skillId, ammoSkillId, grenade, collNode, powerMod=0, target=None):
        if not av:
            return
        startPos = av.rightHandNode.getPos(render)
        endPos = None
        duration = None
        wayPoint = None
        timeToWayPoint = None
        if target == None:
            power = WeaponGlobals.getAttackProjectilePower(skillId, ammoSkillId)
            power *= powerMod + self.BASE_GRENADE_POWER
            if av.isLocal():
                pitch = camera.getP(render)
            else:
                pitch = 0.0
            m = av.getMat(render)
            startVel = m.xformVec(Vec3(0, power, 30 + pitch))
            if av.isLocal():
                forwardVel = av.controlManager.currentControls.getSpeeds()[0]
                sideVel = av.controlManager.currentControls.getSpeeds()[2]
                avVel = m.xformVec(Vec3(sideVel / 3.0, forwardVel, 0))
                startVel += avVel
            endPlaneZ = -5
        else:
            startVel = None
            endPos = target.getPos(render)
            wayPoint = endPos
            endPos = None
            tgtDist = av.getDistance(target)
            duration = WeaponGlobals.getAIProjectileAirTime(tgtDist)
            timeToWayPoint = duration
            duration = None
            endPlaneZ = wayPoint.getZ() - 100
        ival = Sequence(ProjectileInterval(grenade, startPos=startPos, endPos=endPos, duration=duration, startVel=startVel, endZ=endPlaneZ, collNode=collNode, wayPoint=wayPoint, timeToWayPoint=timeToWayPoint), Func(self.removeCollider, av, collNode), Func(grenade.destroy), name='Grenade-%s-%s' % (av.doId, grenade.get_key()))
        grenade.setIval(ival, start=True)
        return

    def putGrenadeInHand(self, av, grenade):
        grenade.reparentTo(render)
        grenade.setPos(render, av.rightHandNode.getPos(render))

    def playCastingAnim(self, av):
        if av.attuneEffect:
            av.attuneEffect.castEffect.start()
            effect = FadingCard(av.currentWeapon.effectCard, av.currentWeapon.effectColor)
            effect.reparentTo(av.currentWeapon)
            effect.play()

    def getPoke(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(self.playCastingAnim, av), av.actorInterval('voodoo_doll_poke', endFrame=50, playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getAttune(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), av.actorInterval('voodoo_tune', playRate=2.0, endFrame=35, blendInT=0.2, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getUnattune(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.currentWeapon.playUnattuneSfx, av.currentWeapon), av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getHeal(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(self.playCastingAnim, av), av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getShackles(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(self.playCastingAnim, av), av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getSwarm(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(self.playCastingAnim, av), av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getBurn(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(self.playCastingAnim, av), av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getCure(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(self.playCastingAnim, av), av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getCurse(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(self.playCastingAnim, av), av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getLifeDrain(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            effect = SpectralSmoke.getEffect()
            if effect:
                effect.reparentTo(av)
                effect.setPos(av, 0, 0, av.getHeight() / 2.0)
                effect.setScale(1, 1, av.getHeight() / 2.0)
                effect.play(duration=2.0, delay=1.5)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = HealSparks.getEffect()
                if effect:
                    effect.reparentTo(av)
                    effect.setPos(av, 0, 0, av.getHeight() / 1.5)
                    effect.setScale(1, 1, av.getHeight() / 2.0)
                    effect.setEffectColor(Vec4(0.2, 0.2, 1.0, 1))
                    effect.play(delay=1.5)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = HomingMissile.getEffect()
                if effect and target:
                    effect.reparentTo(render)
                    effect.setPos(target, 0, 0, target.getHeight() - 1.5)
                    effect.target = av
                    effect.initialVelocity = Vec3(0, 0, 1.5)
                    effect.targetOffset = Vec3(0, 0, 3.0)
                    effect.duration = 1.75
                    effect.wantTrail = 0
                    effect.particleEffect = SpectralTrail.getEffect()
                    effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = HomingMissile.getEffect()
                if effect and target:
                    effect.reparentTo(render)
                    effect.setPos(target, 0, 0, target.getHeight() - 1.5)
                    effect.target = av
                    randomness = random.random() * 1.25
                    effect.initialVelocity = Vec3(-1.0 - randomness, 0, 1.5)
                    effect.targetOffset = Vec3(0, 0, 3.0)
                    effect.duration = 1.5 + randomness
                    effect.wantTrail = 0
                    effect.particleEffect = SpectralTrail.getEffect()
                    effect.play()
                effect = HomingMissile.getEffect()
                if effect and target:
                    effect.reparentTo(render)
                    effect.setPos(target, 0, 0, target.getHeight() - 1.5)
                    effect.target = av
                    randomness = random.random() * 1.25
                    effect.initialVelocity = Vec3(1.0 + randomness, 0, 1.5)
                    effect.targetOffset = Vec3(0, 0, 3.0)
                    effect.duration = 1.5 + randomness
                    effect.wantTrail = 0
                    effect.particleEffect = SpectralTrail.getEffect()
                    effect.play()

        ival = Sequence(Func(self.lockInput, av), Func(self.playCastingAnim, av), Parallel(av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Sequence(Wait(0.5), Func(startVFX))), Func(self.unlockInput, av))
        del startVFX
        return ival

    def startChargeSound(self, av, skillId):
        skillInfo = WeaponGlobals.getSkillAnimInfo(skillId)
        getChargeSfxFunc = skillInfo[WeaponGlobals.HIT_SFX_INDEX]
        getChargeLoopSfxFunc = skillInfo[WeaponGlobals.MISS_SFX_INDEX]
        av.currentWeapon.chargeSound = getChargeSfxFunc()
        av.currentWeapon.chargeLoopSound = getChargeLoopSfxFunc()
        av.currentWeapon.chargeSoundSequence = Sequence(SoundInterval(av.currentWeapon.chargeSound, loop=0, node=av.currentWeapon), SoundInterval(av.currentWeapon.chargeLoopSound, loop=1, duration=1000, node=av.currentWeapon))
        av.currentWeapon.chargeSoundSequence.start()
        if hasattr(av.currentWeapon, 'startChargeEffect'):
            av.currentWeapon.startChargeEffect()

    def stopChargeSound(self, av):
        if av.currentWeapon.chargeSoundSequence:
            av.currentWeapon.chargeSoundSequence.finish()
            av.currentWeapon.chargeSoundSequence = None
        if av.currentWeapon.chargeSound:
            av.currentWeapon.chargeSound.stop()
            av.currentWeapon.chargeSound = None
        if av.currentWeapon.chargeLoopSound:
            av.currentWeapon.chargeLoopSound.stop()
            av.currentWeapon.chargeLoopSound = None
        if hasattr(av.currentWeapon, 'stopChargeEffect'):
            av.currentWeapon.stopChargeEffect()
        return

    def playCastSound(self, av, skillId):
        skillInfo = WeaponGlobals.getSkillAnimInfo(skillId)
        getCastSfxFunc = skillInfo[WeaponGlobals.HIT_SFX_INDEX]
        soundFX = getCastSfxFunc()
        if soundFX:
            base.playSfx(soundFX, node=av)

    def getChargeWitherAnim(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                av.currentWeapon.effect = WitherCharge.getEffect()
                if av.currentWeapon.effect and not av.currentWeapon.isEmpty():
                    av.currentWeapon.effect.reparentTo(av.currentWeapon)
                    av.currentWeapon.effect.setPos(av.currentWeapon, -0.1, 1.5, 0)
                    av.currentWeapon.effect.setPos(av.currentWeapon, av.currentWeapon.getOffset(av.currentWeapon.itemId))
                    av.currentWeapon.effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    av.currentWeapon.effect.startLoop()

        seq = Sequence(Func(av.motionFSM.moveLock), Func(av.currentWeapon.hideMouse, av), Func(base.cr.targetMgr.setWantAimAssist, 1), Func(self.startChargeSound, av, skillId), Func(startVFX), av.actorInterval('wand_cast_start', blendOutT=0), Func(av.loop, 'wand_cast_idle', blendT=0))
        del startVFX
        return seq

    def getCastWitherAnim(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            if av.currentWeapon.effect:
                av.currentWeapon.effect.stopLoop()
                av.currentWeapon.effect = None
            effect = SoulHarvest.getEffect()
            if effect:
                effect.reparentTo(av.getParent())
                effect.setPos(av, 0, 5, 0)
                effect.radius = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId)
                effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = DomeExplosion.getEffect()
                if effect:
                    effect.reparentTo(av.getParent())
                    effect.setPos(av, 0, 5, 0)
                    effect.size = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId) * 2.0
                    effect.play()
                effect = DarkPortal.getEffect()
                if effect:
                    effect.reparentTo(av.getParent())
                    effect.setPos(av, 0, 5, 0)
                    effect.size = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId) * 4.0
                    effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = EvilRingEffect.getEffect()
                if effect:
                    effect.reparentTo(av.getParent())
                    effect.setPos(av, 0, 5, 0)
                    effect.effectScale = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId)
                    effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    effect.duration = 2.5
                    effect.play()
            return

        seq = Sequence(Func(av.motionFSM.on), Func(self.lockInput, av), Func(self.stopChargeSound, av), Func(self.playCastSound, av, skillId), Func(startVFX), av.actorInterval('wand_cast_fire'), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getChargeSoulflayAnim(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                av.currentWeapon.effect = SoulSpiral.getEffect()
                if av.currentWeapon.effect and not av.currentWeapon.isEmpty():
                    av.currentWeapon.effect.reparentTo(av.currentWeapon)
                    av.currentWeapon.effect.setPos(av.currentWeapon, -0.1, 1.5, 0)
                    av.currentWeapon.effect.setHpr(av.currentWeapon, 0.0, -90.0, 0.0)
                    av.currentWeapon.effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    av.currentWeapon.effect.setScale(0.9, 0.9, 0.9)
                    av.currentWeapon.effect.startLoop()

        seq = Sequence(Func(av.motionFSM.moveLock), Func(av.currentWeapon.hideMouse, av), Func(base.cr.targetMgr.setWantAimAssist, 1), Func(self.startChargeSound, av, skillId), Func(startVFX), av.actorInterval('wand_cast_start', blendOutT=0), Func(av.loop, 'wand_cast_idle', blendT=0))
        del startVFX
        return seq

    def getCastSoulFlayAnim(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            if av.currentWeapon.effect:
                av.currentWeapon.effect.stopLoop()
                av.currentWeapon.effect = None
            effect = SoulFlay.getEffect()
            if effect:
                effect.reparentTo(av.getParent())
                effect.setPos(av, 0.0, 4.0, 3.0)
                effect.setHpr(av, 0.0, -90.0, 0.0)
                effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                dummy = NodePath('effect')
                dummy.reparentTo(av.getParent())
                dummy.setPos(av, 0.0, 4.0, 4.0)
                dummy.setHpr(av, 0.0, 0.0, 0.0)
                effect = VoodooSouls.getEffect()
                if effect:
                    effect.reparentTo(dummy)
                    effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    effect.play()
                    posIval = LerpPosInterval(effect, 1.0, Vec3(0.0, 50.0, 0.0), startPos=Vec3(0.0, 0.0, 0.0))
                    posIval.start()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = VoodooGlow.getEffect()
                if effect and not av.currentWeapon.isEmpty():
                    effect.reparentTo(av.currentWeapon)
                    effect.setPos(av.currentWeapon, av.currentWeapon.getOffset(av.currentWeapon.itemId))
                    effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    effect.play()
            return

        seq = Sequence(Func(av.motionFSM.on), Func(self.lockInput, av), Func(startVFX), Func(self.stopChargeSound, av), Func(self.playCastSound, av, skillId), av.actorInterval('wand_cast_fire'), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getChargePestilenceAnim(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                av.currentWeapon.effectActor = Actor.Actor('models/effects/mopath_none', {'spin': 'models/effects/mopath_spiral'})
                joint = av.currentWeapon.effectActor.find('**/joint1')
                av.currentWeapon.effectActor.setScale(1.0, 0.75, 1.0)
                av.currentWeapon.effectActor.setHpr(av.currentWeapon.getHpr())
                av.currentWeapon.effectActor.reparentTo(av.currentWeapon)
                av.currentWeapon.effectActor.setPos(av.currentWeapon, 0.0, 1.8, 0.0)
                av.currentWeapon.effectActor.setPlayRate(1.2, 'spin')
                av.currentWeapon.effectActor.loop('spin')
                av.currentWeapon.effect = VoodooPestilence.getEffect()
                if av.currentWeapon.effect and not av.currentWeapon.isEmpty():
                    av.currentWeapon.effect.particleDummy.reparentTo(av.currentWeapon)
                    av.currentWeapon.effect.reparentTo(joint)
                    av.currentWeapon.effect.effectScale = 1.0
                    av.currentWeapon.effect.startLoop()

        seq = Sequence(Func(av.motionFSM.moveLock), Func(av.currentWeapon.hideMouse, av), Func(base.cr.targetMgr.setWantAimAssist, 1), Func(self.startChargeSound, av, skillId), Func(startVFX), av.actorInterval('wand_cast_start', blendOutT=0), Func(av.loop, 'wand_cast_idle', blendT=0))
        del startVFX
        return seq

    def getCastPestilenceAnim(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            if av.currentWeapon.effect:
                av.currentWeapon.effect.stopLoop()
                av.currentWeapon.effect = None
            effect = Pestilence.getEffect()
            if effect:
                effect.reparentTo(av.getParent())
                effect.setPos(av, 0, 4.0, 3.0)
                effect.setHpr(av, 0, -90, 0)
                effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                if not av.currentWeapon.effectActor:
                    av.currentWeapon.effectActor = Actor.Actor('models/effects/mopath_none', {'spin': 'models/effects/mopath_spiral'})
                joint = av.currentWeapon.effectActor.find('**/joint1')
                av.currentWeapon.effectActor.reparentTo(av.getParent())
                av.currentWeapon.effectActor.setPos(av, 0.0, 13.0, 4.0)
                av.currentWeapon.effectActor.setHpr(av.getHpr())
                av.currentWeapon.effectActor.setPlayRate(1.8, 'spin')
                av.currentWeapon.effectActor.play('spin')
                scaleIval = LerpScaleInterval(av.currentWeapon.effectActor, 0.25, Vec3(10.0, 25.0, 10.0), startScale=Vec3(2.0, 15.0, 2.0))
                scaleIval.start()
                effect = VoodooPestilence.getEffect()
                if effect:
                    effect.particleDummy.reparentTo(av.getParent())
                    effect.reparentTo(joint)
                    effect.effectScale = 4.0
                    effect.play()
            return

        seq = Sequence(Func(av.motionFSM.on), Func(self.lockInput, av), Func(startVFX), Func(self.stopChargeSound, av), Func(self.playCastSound, av, skillId), av.actorInterval('wand_cast_fire'), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getChargeHellfireAnim(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            offset = av.currentWeapon.getOffset(av.currentWeapon.itemId) + Vec3(0, 0.2, 0)
            av.currentWeapon.effect = FlamingSkull.getEffect()
            if av.currentWeapon.effect and not av.currentWeapon.isEmpty():
                av.currentWeapon.effect.reparentTo(av.currentWeapon)
                av.currentWeapon.effect.setPos(av.currentWeapon, offset + Vec3(0.2, 1, 0.3))
                av.currentWeapon.effect.setHpr(av.currentWeapon, 0, -90, 40)
                av.currentWeapon.effect.startLoop()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                av.currentWeapon.effect2 = VoodooStaffFire.getEffect()
                if av.currentWeapon.effect2 and not av.currentWeapon.isEmpty():
                    av.currentWeapon.effect2.reparentTo(av.currentWeapon)
                    av.currentWeapon.effect2.setPos(av.currentWeapon, offset)
                    av.currentWeapon.effect2.setHpr(av.currentWeapon, 0, -90, 0)
                    av.currentWeapon.effect2.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    av.currentWeapon.effect2.startLoop()

        seq = Sequence(Func(av.motionFSM.moveLock), Func(av.currentWeapon.hideMouse, av), Func(base.cr.targetMgr.setWantAimAssist, 1), Func(self.startChargeSound, av, skillId), Func(startVFX), av.actorInterval('wand_cast_start', blendOutT=0), Func(av.loop, 'wand_cast_idle', blendT=0))
        del startVFX
        return seq

    def getCastHellfireAnim(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            if isinstance(av.currentWeapon.effect, FlamingSkull):
                av.currentWeapon.effect.wrtReparentTo(render)
                targetPos, speed, impactT = av.getProjectileInfo(skillId, None)
                av.currentWeapon.effect.playLaunch(speed, targetPos)
                av.currentWeapon.effect = None
            if av.currentWeapon.effect2:
                av.currentWeapon.effect2.stopLoop()
                av.currentWeapon.effect2 = None
            return

        seq = Sequence(Func(av.motionFSM.on), Func(self.lockInput, av), Func(startVFX), Func(self.stopChargeSound, av), Func(self.playCastSound, av, skillId), av.actorInterval('wand_cast_fire'), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getChargeBanishAnim(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            offset = av.currentWeapon.getOffset(av.currentWeapon.itemId)
            av.currentWeapon.effect = VoodooPower.getEffect()
            if av.currentWeapon.effect and not av.currentWeapon.isEmpty():
                av.currentWeapon.effect.reparentTo(av.currentWeapon)
                av.currentWeapon.effect.setPos(av.currentWeapon, offset + Vec3(0, 1.45, -0.1))
                av.currentWeapon.effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                av.currentWeapon.effect.startLoop()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                av.currentWeapon.effect2 = EnergySpiral.getEffect()
                if av.currentWeapon.effect2 and not av.currentWeapon.isEmpty():
                    av.currentWeapon.effect2.reparentTo(av.currentWeapon)
                    av.currentWeapon.effect2.setPos(av.currentWeapon, offset + Vec3(0, 0, -0.1))
                    av.currentWeapon.effect2.setHpr(av.currentWeapon, 0.0, -90.0, 0.0)
                    av.currentWeapon.effect2.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    av.currentWeapon.effect2.startLoop()

        seq = Sequence(Func(av.motionFSM.moveLock), Func(av.currentWeapon.hideMouse, av), Func(base.cr.targetMgr.setWantAimAssist, 1), Func(self.startChargeSound, av, skillId), Func(startVFX), av.actorInterval('wand_cast_start', blendOutT=0), Func(av.loop, 'wand_cast_idle', blendT=0))
        del startVFX
        return seq

    def getCastBanishAnim(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            if av.currentWeapon.effect:
                av.currentWeapon.effect.stopLoop()
                av.currentWeapon.effect = None
            if av.currentWeapon.effect2:
                av.currentWeapon.effect2.stopLoop()
                av.currentWeapon.effect2 = None
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = VoodooGlow.getEffect()
                if effect and not av.currentWeapon.isEmpty():
                    effect.reparentTo(av.currentWeapon)
                    effect.setPos(av.currentWeapon, av.currentWeapon.getOffset(av.currentWeapon.itemId))
                    effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    effect.play()
            return

        seq = Sequence(Func(av.motionFSM.on), Func(self.lockInput, av), Func(startVFX), Func(self.stopChargeSound, av), Func(self.playCastSound, av, skillId), av.actorInterval('wand_cast_fire'), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getChargeDesolationAnim(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                av.currentWeapon.effectActor = Actor.Actor('models/effects/mopath_none', {'spin': 'models/effects/mopath_spiral'})
                joint = av.currentWeapon.effectActor.find('**/joint1')
                av.currentWeapon.effectActor.setScale(1.0, 0.75, 1.0)
                av.currentWeapon.effectActor.setP(0.0)
                av.currentWeapon.effectActor.reparentTo(av.currentWeapon)
                av.currentWeapon.effectActor.setPos(av.currentWeapon, 0.0, 1.7, 0.0)
                av.currentWeapon.effectActor.setPlayRate(1.5, 'spin')
                av.currentWeapon.effectActor.loop('spin')
                av.currentWeapon.effect = DesolationChargeSmoke.getEffect()
                if av.currentWeapon.effect and not av.currentWeapon.isEmpty():
                    av.currentWeapon.effect.particleDummy.reparentTo(av.currentWeapon)
                    av.currentWeapon.effect.reparentTo(joint)
                    av.currentWeapon.effect.effectScale = 1.0
                    av.currentWeapon.effect.startLoop()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                av.currentWeapon.effect2 = WindCharge.getEffect()
                if av.currentWeapon.effect2 and not av.currentWeapon.isEmpty():
                    av.currentWeapon.effect2.reparentTo(av.currentWeapon)
                    av.currentWeapon.effect2.setPos(av.currentWeapon, 0.0, 1.25, 0.0)
                    av.currentWeapon.effect2.setHpr(0, -90, 0)
                    av.currentWeapon.effect2.startLoop()

        seq = Sequence(Func(av.motionFSM.moveLock), Func(av.currentWeapon.hideMouse, av), Func(base.cr.targetMgr.setWantAimAssist, 1), Func(self.startChargeSound, av, skillId), Func(startVFX), av.actorInterval('wand_cast_start', blendOutT=0), Func(av.loop, 'wand_cast_idle', blendT=0))
        del startVFX
        return seq

    def getCastDesolationAnim(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            if av.currentWeapon.effect:
                av.currentWeapon.effect.stopLoop()
                av.currentWeapon.effect = None
            if av.currentWeapon.effect2:
                av.currentWeapon.effect2.stopLoop()
                av.currentWeapon.effect2 = None
            effect = WindWave.getEffect()
            if effect:
                effect.reparentTo(av.getParent())
                effect.setPos(av, 0.0, 0.0, 0.0)
                effect.setScale(1.0, 1.0, 1.0)
                effect.setHpr(0.0, 0.0, 0.0)
                effect.play()
            effect = SoulHarvest2.getEffect()
            if effect:
                effect.reparentTo(av.getParent())
                effect.setPos(av, 0, 0, 2)
                effect.radius = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId)
                effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = DesolationSmoke.getEffect()
                if effect:
                    effect.reparentTo(av.getParent())
                    effect.setPos(av, 0.0, 0.0, 0.0)
                    effect.play()
                effect = DomeExplosion.getEffect()
                if effect:
                    effect.reparentTo(av.getParent())
                    effect.setPos(av, 0, 0, 0)
                    effect.size = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId)
                    effect.play()
                effect = DarkPortal.getEffect()
                if effect:
                    effect.reparentTo(av.getParent())
                    effect.setPos(av, 0, 0, 0)
                    effect.size = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId) * 3.0
                    effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                cameraShakerEffect = CameraShaker()
                cameraShakerEffect.wrtReparentTo(av.getParent())
                cameraShakerEffect.setPos(av, 0.0, 0.0, 0.0)
                cameraShakerEffect.shakeSpeed = 0.075
                cameraShakerEffect.shakePower = 1.0
                cameraShakerEffect.numShakes = 30
                cameraShakerEffect.scalePower = 1
                cameraShakerEffect.play(100.0)
            return

        seq = Sequence(Func(av.motionFSM.on), Func(self.lockInput, av), Func(startVFX), Func(self.stopChargeSound, av), Func(self.playCastSound, av, skillId), av.actorInterval('wand_cast_fire'), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getFizzleAnim(self, av, skillId, ammoSkillId, charge, target):
        if av.currentWeapon.effect:
            av.currentWeapon.effect.stopLoop()
            av.currentWeapon.effect = None
        if av.currentWeapon.effect2:
            av.currentWeapon.effect2.stopLoop()
            av.currentWeapon.effect2 = None
        return Sequence(Func(av.motionFSM.on), Func(base.cr.targetMgr.setWantAimAssist, 0), Func(self.lockInput, av), Func(self.stopChargeSound, av), av.actorInterval('wand_cast_fire'), Func(self.unlockInput, av))

    def getCastFireAnim(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            motion_color = [
             Vec4(1.0, 1.0, 1.0, 1.0), Vec4(0.5, 0.2, 1.0, 1.0)]
            targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
            effect = VoodooProjectile.getEffect()
            if effect:
                effect.reparentTo(render)
                effect.setPos(av, 0, 2, 2)
                effect.setH(av.getH(render))
                effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                effect.play(targetPos, speed, target)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = VoodooGlow.getEffect()
                if effect and not av.currentWeapon.isEmpty():
                    effect.reparentTo(av.currentWeapon)
                    effect.setPos(av.currentWeapon, 0.0, 2.0, 0.0)
                    effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    effect.play()

        seq = Sequence(Func(base.cr.targetMgr.setWantAimAssist, 0), Func(self.lockInput, av), Func(startVFX), Func(self.playCastSound, av, skillId), av.actorInterval('wand_cast_fire'), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getDrink(self, av, skillId, ammoSkillId, charge, target):
        if not av.consumable:
            return

        def hideCurrentWeapon():
            if av.currentWeapon:
                if not av.currentWeapon.isEmpty():
                    av.currentWeapon.hide()

        def showCurrentWeapon():
            if av.currentWeapon:
                if not av.currentWeapon.isEmpty():
                    av.currentWeapon.show()

        return Sequence(Func(self.lockInput, av), Func(hideCurrentWeapon), Func(av.consumable.attachTo, av), av.actorInterval('drink_potion', playRate=1.5, startFrame=8, endFrame=45, blendInT=0.2, blendOutT=0.2), Func(showCurrentWeapon), Func(av.consumable.detachFrom, av), Func(self.unlockInput, av))

    def getChop(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('sword_cleave', playRate=1.0, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getDoubleSlash(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('sword_slash', playRate=1.5, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getLunge(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('sword_lunge', playRate=1.5, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getStab(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('sword_thrust', playRate=1.0, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getRollThrust(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('sword_roll_thrust', playRate=1.5, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getComboA(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('sword_comboA', playRate=1.5, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getWildSlash(self, av, skillId, ammoSkillId, charge, target):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.currentWeapon.endAttack, av), Func(av.currentWeapon.setTrailLength, 0.5), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dagger_combo', playRate=1.0, startFrame=54, endFrame=87, blendInT=0.5, blendOutT=0.5)), Sequence(Wait(0.958), Func(self.unlockInput, av)))
        return ival

    def getFlurry(self, av, skillId, ammoSkillId, charge, target):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.currentWeapon.endAttack, av), Func(av.currentWeapon.setTrailLength, 0.6), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dagger_combo', playRate=1.0, startFrame=88, endFrame=142, blendInT=0.5, blendOutT=0.5)), Sequence(Wait(1.5), Func(self.unlockInput, av)))
        return ival

    def getRiposte(self, av, skillId, ammoSkillId, charge, target):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.currentWeapon.endAttack, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dagger_combo', playRate=1.0, startFrame=1, endFrame=28, blendInT=0.2, blendOutT=0.5)), Sequence(Wait(0.75), Func(self.unlockInput, av)))
        return ival

    def getDualCutlassCombination(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dualcutlass_comboB', playRate=1.2, startFrame=0, endFrame=75, blendInT=0.5, blendOutT=0.25), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getDualCutlassSpin(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dualcutlass_comboB', playRate=1, startFrame=70, endFrame=101, blendInT=0.25, blendOutT=0.25), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getDualCutlassBarrage(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.22), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dualcutlass_comboB', playRate=0.575, startFrame=101, endFrame=131, blendInT=0.25, blendOutT=0.25), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getDualCutlassXSlash(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dualcutlass_comboA', playRate=1, startFrame=50, endFrame=100, blendInT=0.25, blendOutT=0.25), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getDualCutlassGore(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dualcutlass_comboA', playRate=1, startFrame=100, endFrame=120, blendInT=0.25, blendOutT=0.25), av.actorInterval('dualcutlass_comboB', playRate=1, startFrame=140, endFrame=200, blendInT=0.25, blendOutT=0.25), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getFoilFleche(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('foil_thrust', playRate=1, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getFoilReprise(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('foil_hack', playRate=1, startFrame=45, endFrame=89, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getFoilSwipe(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('foil_coup', playRate=1, startFrame=75, endFrame=97, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getFoilImpale(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('foil_thrust', playRate=1, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getFoilRemise(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('foil_slash', playRate=1, startFrame=10, endFrame=82, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getFoilBalestraKick(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('foil_kick', playRate=1, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getFoilCadence(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('foil_coup', playRate=1, startFrame=75, endFrame=172, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getKrazyPunch(self, av, skillId, ammoSkillId, charge, target):
        return Sequence(Func(self.lockInput, av), av.actorInterval('boxing_kick', playRate=2), av.actorInterval('boxing_punch', playRate=2), av.actorInterval('boxing_kick', playRate=2), Func(self.unlockInput, av))

    def getBoxingPunch(self, av, skillId, ammoSkillId, charge, target):
        return Sequence(Func(self.lockInput, av), av.actorInterval('boxing_punch', playRate=1.0, blendInT=0.1, blendOutT=0.2), Func(self.unlockInput, av))

    def getKick(self, av, skillId, ammoSkillId, charge, target):
        return Sequence(Func(self.lockInput, av), av.actorInterval('boxing_kick', playRate=1.0), Func(self.unlockInput, av))

    def getBayonetFireAnim(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            if base.cr.wantSpecialEffects:
                pistolSmokeEffect = PistolSmoke.getEffect()
                if pistolSmokeEffect:
                    pistolSmokeEffect.reparentTo(av)
                    pistolSmokeEffect.setPos(av, 1.2, 2.5, 5)
                    pistolSmokeEffect.play()
                pistolFlameEffect = PistolFlame.getEffect()
                if pistolFlameEffect:
                    pistolFlameEffect.reparentTo(av)
                    pistolFlameEffect.particleDummy.reparentTo(av)
                    pistolFlameEffect.flash.setScale(30)
                    pistolFlameEffect.setPos(av, 1.2, 2.5, 5)
                    pistolFlameEffect.play()

        ival = Sequence(Func(base.cr.targetMgr.setWantAimAssist, 0), Func(self.lockInput, av), Func(startVFX), av.actorInterval('gun_fire', endFrame=12, blendInT=0.1, blendOutT=0), Func(self.unlockInput, av), av.actorInterval('gun_fire', startFrame=13, blendInT=0, blendOutT=0.3))
        return ival

    def getBayonetReloadAnim(self, av, skillId, ammoSkillId, charge, target):
        reloadSfx = av.currentWeapon.reloadSfxs
        reloadFx = random.choice(reloadSfx)
        gunCockSfx = av.currentWeapon.gunCockSfxs
        gunCockFx = random.choice(gunCockSfx)
        track = Sequence(Func(self.lockInput, av), av.actorInterval('gun_reload', endFrame=6, blendInT=0, blendOutT=0), Func(base.playSfx, gunCockFx, node=av), av.actorInterval('gun_reload', startFrame=7, endFrame=18, blendInT=0, blendOutT=0), Func(base.playSfx, reloadFx, node=av), av.actorInterval('gun_reload', startFrame=19, blendInT=0, blendOutT=0.3), Func(self.unlockInput, av))
        return track

    def getBayonetStab(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.beginAttack, av), av.actorInterval('bayonet_attackA', playRate=1.0, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(self.unlockInput, av))
        return ival

    def getBayonetBash(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.beginAttack, av), av.actorInterval('bayonet_attackB', playRate=1.0, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(self.unlockInput, av))
        return ival

    def getBayonetRush(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.beginAttack, av), av.actorInterval('bayonet_attackC', playRate=1.0, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(self.unlockInput, av))
        return ival

    def getCrabAttackLeft(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_left', playRate=1.0)

    def getCrabAttackRight(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_right', playRate=1.0)

    def getCrabAttackBoth(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_both', playRate=1.0)

    def getStumpKick(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(av.currentWeapon.setTrailLength, 0.0), av.actorInterval('kick', playRate=1.0))
        return ival

    def getStumpKickRight(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(av.currentWeapon.setTrailLength, 0.0), av.actorInterval('kick_right', playRate=1.0))
        return ival

    def getStumpSlapLeft(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(av.currentWeapon.setTrailLength, 0.5), av.actorInterval('slap_left', playRate=1.0))
        return ival

    def getStumpSlapRight(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(av.currentWeapon.setTrailLength, 0.5), av.actorInterval('slap_right', playRate=1.0))
        return ival

    def getStumpSwatLeft(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(av.currentWeapon.setTrailLength, 0.5), av.actorInterval('swat_left', playRate=1.0))
        return ival

    def getStumpSwatRight(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(Func(av.currentWeapon.setTrailLength, 0.5), av.actorInterval('swat_right', playRate=1.0))
        return ival

    def getStumpStomp(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            shockwaveRingEffect = ShockwaveRing.getEffect()
            if shockwaveRingEffect:
                shockwaveRingEffect.reparentTo(av)
                shockwaveRingEffect.size = 40
                shockwaveRingEffect.setPos(0, 0, 3)
                shockwaveRingEffect.play()
            shockwaveRingEffect = ShockwaveRing.getEffect()
            if shockwaveRingEffect:
                shockwaveRingEffect.reparentTo(av)
                shockwaveRingEffect.size = 80
                shockwaveRingEffect.setPos(0, 0, 3)
                shockwaveRingEffect.play()
            shockwaveRingEffect = ShockwaveRing.getEffect()
            if shockwaveRingEffect:
                shockwaveRingEffect.reparentTo(av)
                shockwaveRingEffect.size = 120
                shockwaveRingEffect.setPos(0, 0, 3)
                shockwaveRingEffect.play()
            dustRingEffect = DustRing.getEffect()
            if dustRingEffect:
                dustRingEffect.reparentTo(av)
                dustRingEffect.setPos(0, 0, 0)
                dustRingEffect.play()
            cameraShakerEffect = CameraShaker()
            cameraShakerEffect.reparentTo(av)
            cameraShakerEffect.setPos(0, 0, 0)
            cameraShakerEffect.shakeSpeed = 0.06
            cameraShakerEffect.shakePower = 4.0
            cameraShakerEffect.numShakes = 2
            cameraShakerEffect.scalePower = 1
            cameraShakerEffect.play(50.0)

        ival = Parallel(Sequence(Wait(1.33), Func(startVFX)), Sequence(Func(av.currentWeapon.beginAttack, av), av.actorInterval('jump_attack', playRate=1.0), Func(av.currentWeapon.endAttack, av)))
        return ival

    def getFlyTrapAttackA(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_a', playRate=1.0)

    def getFlyTrapAttackJab(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_jab', playRate=1.0)

    def getFlyTrapLeftFake(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_left_fake', playRate=1.0)

    def getFlyTrapRightFake(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_right_fake', playRate=1.0)

    def getFlyTrapSpit(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            motion_color = [
             Vec4(1.0, 0.0, 0.5, 1.0), Vec4(1.0, 0.0, 0.0, 1.0)]
            targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
            effect = VenomSpitProjectile.getEffect()
            if effect:
                effect.reparentTo(render)
                effect.setPos(av, 0, 0, av.height * 0.7)
                effect.setH(av.getH(render))
                effect.play(targetPos, speed, target)

        ival = Sequence(av.actorInterval('shoot', endFrame=23), Func(startVFX), av.actorInterval('shoot', startFrame=24))
        return ival

    def getTentacleSlap(self, av, skillId, ammoSkillId, charge, target):
        anim = Parallel(Func(av.alignWithVictim, 0.4), Sequence(ActorInterval(av, 'pound_deck', playRate=2.0), Func(av.loop, 'idle', playRate=random.uniform(1.0, 1.2))), Sequence(Wait(0.6), Func(self.playShockwave, av)))
        return anim

    def getTentaclePound(self, av, skillId, ammoSkillId, charge, target):
        anim = Parallel(Func(av.alignWithVictim, 0.4), Sequence(ActorInterval(av, 'pound_deck', playRate=2.0), Func(av.loop, 'idle', blendT=0, playRate=random.uniform(1.0, 1.2))))
        return anim

    def getTentacleEnsnare(self, av, skillId, ammoSkillId, charge, target):
        anim = Sequence(Parallel(ActorInterval(av, 'grab', playRate=1.0), Func(av.alignWithVictim, 0.66), Sequence(Wait(0.66), Func(av.setupEnsnare), Wait(1.29), Func(av.pickupTarget))), Func(av.loop, 'grab_idle', playRate=random.uniform(1.0, 1.2)))
        return anim

    def getTentaclePiledriver(self, av, skillId, ammoSkillId, charge, target):
        anim = Sequence(Parallel(ActorInterval(av, 'grab_slam', playRate=1.0), Sequence(Wait(2.93), Func(av.piledriveTarget))), Func(av.loop, 'idle', playRate=random.uniform(1.0, 1.2)))
        return anim

    def getTentacleRelease(self, av, skillId, ammoSkillId, charge, target):
        anim = Sequence(Parallel(ActorInterval(av, 'grab_slam', playRate=1.0), Sequence(Wait(2.93), Func(av.piledriveTarget))), Func(av.loop, 'idle', playRate=random.uniform(1.0, 1.2)))
        return anim

    def getTentacleConstrict(self, av, skillId, ammoSkillId, charge, target):
        anim = Sequence(ActorInterval(av, 'grab_constrict', playRate=1.0), Func(av.loop, 'grab_idle', playRate=random.uniform(1.0, 1.2)))
        return anim

    def getKrakenVomit(self, av, skillId, ammoSkillId, charge, target):
        anim = Sequence(ActorInterval(av, 'shoot', playRate=1.0), Func(av.loop, 'idle', playRate=random.uniform(1.0, 1.2)))
        return anim

    def getScorpionAttackLeft(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_left', playRate=1.0)

    def getScorpionAttackRight(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_right', playRate=1.0)

    def getScorpionAttackBoth(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_both', playRate=1.0)

    def getScorpionAttackTailSting(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_tail_sting', playRate=1.0)

    def getScorpionPickUpHuman(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('pick_up_human', playRate=1.0)

    def getScorpionRearUp(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('rear_up', playRate=1.0)

    def getAlligatorAttackLeft(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_left', playRate=1.0)

    def getAlligatorAttackRight(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_right', playRate=1.0)

    def getAlligatorAttackStraight(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_straight', playRate=1.0)

    def getAlligatorAttackTailLeft(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_tail_left', playRate=1.0)

    def getAlligatorAttackTailRight(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_tail_right', playRate=1.0)

    def getBatAttackLeft(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_forward', playRate=1.0)

    def getBatAttackRight(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('attack_right', playRate=1.0)

    def getBatShriek(self, av, skillId, ammoSkillId, charge, target):

        def playFX():
            shockwaveRingEffect = ShockwaveRing.getEffect()
            if shockwaveRingEffect:
                shockwaveRingEffect.reparentTo(av)
                shockwaveRingEffect.size = 40
                shockwaveRingEffect.setPos(0, 0, 0)
                shockwaveRingEffect.play()

        ival = Sequence(Func(playFX), av.actorInterval('attack_forward', playRate=2.0))
        return ival

    def getBatFlurry(self, av, skillId, ammoSkillId, charge, target):
        ival = Sequence(av.actorInterval('attack_right', playRate=2.0), av.actorInterval('attack_forward', playRate=2.0), av.actorInterval('attack_right', playRate=2.0), av.actorInterval('attack_forward', playRate=2.0))
        return ival

    def getWaspAttack(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('sting', playRate=1.0)

    def getWaspAttackLeap(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('leap_sting', playRate=1.0)

    def getWaspAttackSting(self, av, skillId, ammoSkillId, charge, target):
        return av.actorInterval('sting', playRate=1.0)

    def playShockwave(self, av):
        pos = av.getPos(render)
        smokeCloudEffect = SmokeCloud.getEffect()
        if smokeCloudEffect:
            smokeCloudEffect.reparentTo(render)
            smokeCloudEffect.setPos(pos)
            smokeCloudEffect.setScale(1.0)
            smokeCloudEffect.spriteScale = 1.0
            smokeCloudEffect.radius = 7.0
            smokeCloudEffect.play()
        shockwaveRingEffect = ShockwaveRing.getEffect()
        if shockwaveRingEffect:
            shockwaveRingEffect.reparentTo(render)
            shockwaveRingEffect.size = 40
            shockwaveRingEffect.setPos(pos)
            shockwaveRingEffect.play()
        cameraShakerEffect = CameraShaker()
        cameraShakerEffect.reparentTo(render)
        cameraShakerEffect.setPos(pos)
        cameraShakerEffect.shakeSpeed = 0.04
        cameraShakerEffect.shakePower = 6.0
        cameraShakerEffect.numShakes = 2
        cameraShakerEffect.scalePower = 1
        cameraShakerEffect.play(80.0)

    def getBroadsideLeft(self, av, skillId, ammoSkillId, charge=0, target=None):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getLeftBroadsidePhrase(), CFSpeech | CFTimeout)), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getBroadsideRight(self, av, skillId, ammoSkillId, charge=0, target=None):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getRightBroadsidePhrase(), CFSpeech | CFTimeout)), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getFullSail(self, av, skillId, ammoSkillId, charge=0):

        def playSfx():
            if not av.ship:
                return
            sfx = av.ship.fullsailSfx
            base.playSfx(sfx, node=av.ship, cutoff=1500)

        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getFullSailPhrase(), CFSpeech | CFTimeout)), Func(playSfx), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        del playSfx
        return ival

    def getComeAbout(self, av, skillId, ammoSkillId, charge=0):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getComeAboutPhrase(), CFSpeech | CFTimeout)), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getRammingSpeed(self, av, skillId, ammoSkillId, charge=0):

        def playSfx():
            if not av.ship:
                return
            sfx = av.ship.fullsailSfx
            base.playSfx(sfx, node=av.ship, cutoff=1500)

        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.RammingSpeed, CFSpeech | CFTimeout)), Func(playSfx), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        del playSfx
        return ival

    def getOpenFire(self, av, skillId, ammoSkillId, charge, target):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getOpenFirePhrase(), CFSpeech | CFTimeout)), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getTakeCover(self, av, skillId, ammoSkillId, charge, target):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getTakeCoverPhrase(), CFSpeech | CFTimeout)), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getPowerRecharge(self, av, skillId, ammoSkillId, charge=0):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getPowerRechargePhrase(), CFSpeech | CFTimeout)), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getShipRepair(self, av, skillId, ammoSkillId, charge=0):
        return self.getComeAbout(av, skillId, ammoSkillId, charge)

    def lockInput(self, av):
        if av.isLocal():
            messenger.send('skillStarted')

    def unlockInput(self, av):
        if av.isLocal():
            messenger.send('skillFinished')
# okay decompiling .\pirates\battle\CombatAnimations.pyc
