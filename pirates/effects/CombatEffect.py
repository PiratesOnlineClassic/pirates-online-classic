from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.actor import Actor
from pirates.piratesbase import PiratesGlobals
from pirates.battle import WeaponGlobals
from pirates.effects.CannonExplosion import CannonExplosion
from pirates.effects.CannonSplash import CannonSplash
from pirates.effects.DirtClod import DirtClod
from pirates.effects.DustCloud import DustCloud
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.RockShower import RockShower
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.DustRing import DustRing
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.ShockwaveRing import ShockwaveRing
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.FireTrail import FireTrail
from pirates.effects.GreenBlood import GreenBlood
from pirates.effects.HitFlashA import HitFlashA
from pirates.effects.ShockwaveHit import ShockwaveHit
from pirates.effects.WaspCloud import WaspCloud
from pirates.effects.PoisonHit import PoisonHit
from pirates.effects.FireballHit import FireballHit
from pirates.effects.CurseHit import CurseHit
from pirates.effects.ExplosionCloud import ExplosionCloud
from pirates.effects.FadingSigil import FadingSigil
from pirates.effects.FlashStar import FlashStar
from pirates.effects.VoodooSmoke import VoodooSmoke
from pirates.effects.SpectralSmoke import SpectralSmoke
from pirates.effects.DrainLife import DrainLife
from pirates.effects.Fire import Fire
from pirates.effects.SparkBurst import SparkBurst
from pirates.effects.NovaStar import NovaStar
from pirates.effects.DarkStar import DarkStar
from pirates.effects.HitStar import HitStar
from pirates.effects.VoodooPestilence import VoodooPestilence
from pirates.effects.SoulSpiral import SoulSpiral
from pirates.effects.VoodooExplosion import VoodooExplosion
from pirates.effects.MuzzleFlash import MuzzleFlash
from pirates.effects.DustRingBanish import DustRingBanish
from pirates.effects.WitherStar import WitherStar
from pirates.effects.HellFire import HellFire
from pirates.effects.HealRays import HealRays
from pirates.effects.HealSparks import HealSparks
from pirates.effects.HealSmoke import HealSmoke
import random

class CombatEffect(NodePath):
    notify = DirectNotifyGlobal.directNotify.newCategory('CombatEffect')
    MAX_DURATION = 10.0
    
    def __init__(self, effectId, multihit = 0, attacker = None):
        NodePath.__init__(self, 'CombatEffect')
        self.effectId = effectId
        self.hitNum = multihit
        self.ival = None
        self.attacker = attacker
        self.colorEffect = None
        self.setColorScaleOff()
        self.setTransparency(1)
        self.effects = []
        self.loadEffects()
    
    def loadEffects(self):
        self.effects = []
        if not base.config.GetBool('want-special-effects', 1):
            return None
        
        self.ival = Sequence()
        effectAnims = Parallel()
        if self.attacker and self.attacker.currentWeapon and hasattr(self.attacker.currentWeapon, 'colorAndOffset'):
            self.colorEffect = self.attacker.currentWeapon.getEffectColor(self.attacker.currentWeapon.itemId)
        
        if self.effectId == WeaponGlobals.VFX_HACK:
            effect = HitFlashA.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.useRay = 1
                effect.useSpark = 1
                effect.rayAngle = -45
                effect.splatScale = 10
                effect.rayFlareValue = 2.0
                effect.setColor(1, 1, 1, 1)
                effect.setPos(0, 0, 0.5)
                effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = SparkBurst.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(0, 0, 0.5)
                    effect.particleDummy.reparentTo(self)
                    effectAnims.append(Func(effect.play, 'Yellow'))
                    self.effects.append(effect)
            
        elif self.effectId == WeaponGlobals.VFX_SLASH:
            effect = HitFlashA.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.useRay = 1
                effect.useSpark = 1
                effect.rayAngle = 0
                effect.splatScale = 13
                effect.rayFlareValue = 2.0
                effect.setColor(1, 1, 1, 1)
                effect.setPos(0, 0, 1.0)
                effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = SparkBurst.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(0, 0, 1.0)
                    effect.particleDummy.reparentTo(self)
                    effectAnims.append(Func(effect.play, 'Yellow'))
                    self.effects.append(effect)

        elif self.effectId == WeaponGlobals.VFX_CLEAVE:
            effect = HitFlashA.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.useRay = 1
                effect.useSpark = 1
                effect.rayAngle = 45
                effect.splatScale = 20
                effect.rayFlareValue = 2.5
                effect.setColor(1, 1, 1, 1)
                effect.setPos(0, 0, 1.0)
                effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                shockwaveHitEffect = ShockwaveHit.getEffect()
                if shockwaveHitEffect:
                    shockwaveHitEffect.reparentTo(self)
                    shockwaveHitEffect.size = 10
                    shockwaveHitEffect.speed = 0.2
                    shockwaveHitEffect.loadExplosion(Point3(0, 80, 0), 'Hit')
                    shockwaveHitEffect.setColor(1, 1, 1, 1)
                    shockwaveHitEffect.setPos(0, 0, 0)
                    shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(shockwaveHitEffect.play))
                    self.effects.append(shockwaveHitEffect)
                
                shockwaveHitEffect = ShockwaveHit.getEffect()
                if shockwaveHitEffect:
                    shockwaveHitEffect.reparentTo(self)
                    shockwaveHitEffect.size = 15
                    shockwaveHitEffect.speed = 0.2
                    shockwaveHitEffect.loadExplosion(Point3(-45, -45, 0), 'HitRay')
                    shockwaveHitEffect.setColor(1, 1, 1, 1)
                    shockwaveHitEffect.setPos(0, 0, 0)
                    shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(shockwaveHitEffect.play))
                    self.effects.append(shockwaveHitEffect)
                
                effect = SparkBurst.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(0, 0, 1.0)
                    effect.particleDummy.reparentTo(self)
                    effectAnims.append(Func(effect.play, 'Yellow'))
                    self.effects.append(effect)

        elif self.effectId == WeaponGlobals.VFX_FLOURISH:
            if self.hitNum == 0:
                effect = HitFlashA.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.useRay = 1
                    effect.useSpark = 1
                    effect.rayAngle = 30
                    effect.splatScale = 25
                    effect.rayFlareValue = 2.0
                    effect.setColor(1, 1, 1, 1)
                    effect.setPos(0.5, 0, 0)
                    effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    effect = SparkBurst.getEffect()
                    if effect:
                        effect.reparentTo(self)
                        effect.setPos(0.5, 0, 0)
                        effect.particleDummy.reparentTo(self)
                        effectAnims.append(Func(effect.play, 'Yellow'))
                        self.effects.append(effect)

            elif self.hitNum == 1:
                effect = HitFlashA.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.useRay = 1
                    effect.useSpark = 1
                    effect.rayAngle = 10
                    effect.splatScale = 20
                    effect.rayFlareValue = 2.0
                    effect.setColor(1, 1, 1, 1)
                    effect.setPos(-0.5, 0, 2.0)
                    effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    effect = SparkBurst.getEffect()
                    if effect:
                        effect.reparentTo(self)
                        effect.setPos(-0.5, 0, 2.0)
                        effect.particleDummy.reparentTo(self)
                        effectAnims.append(Func(effect.play, 'Yellow'))
                        self.effects.append(effect)

            elif self.hitNum == 2:
                effect = HitFlashA.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.useRay = 1
                    effect.useSpark = 1
                    effect.rayAngle = -30
                    effect.splatScale = 25
                    effect.rayFlareValue = 3.0
                    effect.setColor(1, 1, 1, 1)
                    effect.setPos(0, 0, -2.0)
                    effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    effect = SparkBurst.getEffect()
                    if effect:
                        effect.reparentTo(self)
                        effect.setPos(0, 0, -2.0)
                        effect.particleDummy.reparentTo(self)
                        effectAnims.append(Func(effect.play, 'Yellow'))
                        self.effects.append(effect)
                    
                    shockwaveHitEffect = ShockwaveHit.getEffect()
                    if shockwaveHitEffect:
                        shockwaveHitEffect.reparentTo(self)
                        shockwaveHitEffect.size = 13
                        shockwaveHitEffect.speed = 0.2
                        shockwaveHitEffect.loadExplosion(Point3(-45, 45, 0), 'Hit')
                        shockwaveHitEffect.setColor(1, 1, 1, 1)
                        shockwaveHitEffect.setPos(0, 0, 0)
                        shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                        effectAnims.append(Func(shockwaveHitEffect.play))
                        self.effects.append(shockwaveHitEffect)
                    
                    shockwaveHitEffect = ShockwaveHit.getEffect()
                    if shockwaveHitEffect:
                        shockwaveHitEffect.reparentTo(self)
                        shockwaveHitEffect.size = 20
                        shockwaveHitEffect.speed = 0.2
                        shockwaveHitEffect.loadExplosion(Point3(-45, -45, 0), 'HitRay')
                        shockwaveHitEffect.setColor(1, 1, 1, 1)
                        shockwaveHitEffect.setPos(0, 0, 0)
                        shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                        effectAnims.append(Func(shockwaveHitEffect.play))
                        self.effects.append(shockwaveHitEffect)

        elif self.effectId == WeaponGlobals.VFX_STAB:
            effect = HitFlashA.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.useRay = 1
                effect.useSpark = 1
                effect.rayAngle = 0
                effect.splatScale = 25
                effect.rayFlareValue = 3.5
                effect.setColor(1, 1, 1, 1)
                effect.setPos(0, 0, 0)
                effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                shockwaveHitEffect = ShockwaveHit.getEffect()
                if shockwaveHitEffect:
                    shockwaveHitEffect.reparentTo(self)
                    shockwaveHitEffect.size = 13
                    shockwaveHitEffect.speed = 0.2
                    shockwaveHitEffect.loadExplosion(Point3(-45, 45, 0), 'Hit')
                    shockwaveHitEffect.setColor(1, 1, 1, 1)
                    shockwaveHitEffect.setPos(0, 0, 0)
                    shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(shockwaveHitEffect.play))
                    self.effects.append(shockwaveHitEffect)
                
                shockwaveHitEffect = ShockwaveHit.getEffect()
                if shockwaveHitEffect:
                    shockwaveHitEffect.reparentTo(self)
                    shockwaveHitEffect.size = 20
                    shockwaveHitEffect.speed = 0.2
                    shockwaveHitEffect.loadExplosion(Point3(-45, -45, 0), 'HitRay')
                    shockwaveHitEffect.setColor(1, 1, 1, 1)
                    shockwaveHitEffect.setPos(0, 0, 0)
                    shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(shockwaveHitEffect.play))
                    self.effects.append(shockwaveHitEffect)
                
                effect = SparkBurst.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(0, 0, 0)
                    effect.particleDummy.reparentTo(self)
                    effectAnims.append(Func(effect.play, 'Yellow'))
                    self.effects.append(effect)

        elif self.effectId == WeaponGlobals.VFX_TAUNT:
            pass
        elif self.effectId == WeaponGlobals.VFX_BRAWL:
            effect = HitFlashA.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.useRay = 0
                effect.useSpark = 1
                effect.splatScale = 15
                effect.rayFlareValue = 0.35
                effect.setColor(1, 1, 1, 1)
                effect.setPos(0, 0, 0)
                effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                shockwaveHitEffect = ShockwaveHit.getEffect()
                if shockwaveHitEffect:
                    shockwaveHitEffect.reparentTo(self)
                    shockwaveHitEffect.size = 13
                    shockwaveHitEffect.speed = 0.2
                    shockwaveHitEffect.loadExplosion(Point3(-45, 45, 0), 'Hit')
                    shockwaveHitEffect.setColor(1, 1, 1, 1)
                    shockwaveHitEffect.setPos(0, 0, 0)
                    shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(shockwaveHitEffect.play))
                    self.effects.append(shockwaveHitEffect)
                
                shockwaveHitEffect = ShockwaveHit.getEffect()
                if shockwaveHitEffect:
                    shockwaveHitEffect.reparentTo(self)
                    shockwaveHitEffect.size = 20
                    shockwaveHitEffect.speed = 0.2
                    shockwaveHitEffect.loadExplosion(Point3(-45, -45, 0), 'HitRay')
                    shockwaveHitEffect.setColor(1, 1, 1, 1)
                    shockwaveHitEffect.setPos(0, 0, 0)
                    shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(shockwaveHitEffect.play))
                    self.effects.append(shockwaveHitEffect)
            
        elif self.effectId == WeaponGlobals.VFX_SWEEP:
            effect = HitFlashA.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.useRay = 1
                effect.useSpark = 1
                effect.rayAngle = 0
                effect.splatScale = 25
                effect.rayFlareValue = 2.5
                effect.setColor(1, 1, 1, 1)
                effect.setPos(0, 0, 0)
                effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                shockwaveHitEffect = ShockwaveHit.getEffect()
                if shockwaveHitEffect:
                    shockwaveHitEffect.reparentTo(self)
                    shockwaveHitEffect.size = 13
                    shockwaveHitEffect.speed = 0.2
                    shockwaveHitEffect.loadExplosion(Point3(-45, 45, 0), 'Hit')
                    shockwaveHitEffect.setColor(1, 1, 1, 1)
                    shockwaveHitEffect.setPos(0, 0, 0)
                    shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(shockwaveHitEffect.play))
                    self.effects.append(shockwaveHitEffect)
                
                shockwaveHitEffect = ShockwaveHit.getEffect()
                if shockwaveHitEffect:
                    shockwaveHitEffect.reparentTo(self)
                    shockwaveHitEffect.size = 20
                    shockwaveHitEffect.speed = 0.2
                    shockwaveHitEffect.loadExplosion(Point3(-45, -45, 0), 'HitRay')
                    shockwaveHitEffect.setColor(1, 1, 1, 1)
                    shockwaveHitEffect.setPos(0, 0, 0)
                    shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(shockwaveHitEffect.play))
                    self.effects.append(shockwaveHitEffect)
                
                effect = SparkBurst.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(0, 0, 0)
                    effect.particleDummy.reparentTo(self)
                    effectAnims.append(Func(effect.play, 'Yellow'))
                    self.effects.append(effect)
            
        elif self.effectId == WeaponGlobals.VFX_BLADESTORM:
            if self.hitNum == 0:
                effect = HitFlashA.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.useRay = 1
                    effect.useSpark = 1
                    effect.rayAngle = 45
                    effect.splatScale = 20
                    effect.rayFlareValue = 2.0
                    effect.setColor(1, 1, 1, 1)
                    effect.setPos(-0.5, 0, 1.5)
                    effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    effect = SparkBurst.getEffect()
                    if effect:
                        effect.reparentTo(self)
                        effect.setPos(0, 0, 0)
                        effect.particleDummy.reparentTo(self)
                        effectAnims.append(Func(effect.play, 'Yellow'))
                        self.effects.append(effect)

            elif self.hitNum == 1:
                effect = HitFlashA.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.useRay = 1
                    effect.useSpark = 1
                    effect.rayAngle = -25
                    effect.splatScale = 18
                    effect.rayFlareValue = 2.5
                    effect.setColor(1, 1, 1, 1)
                    effect.setPos(0.5, 0, 0.5)
                    effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    effect = SparkBurst.getEffect()
                    if effect:
                        effect.reparentTo(self)
                        effect.setPos(0.5, 0, 0.5)
                        effect.particleDummy.reparentTo(self)
                        effectAnims.append(Func(effect.play, 'Yellow'))
                        self.effects.append(effect)

            elif self.hitNum == 2:
                effect = HitFlashA.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.useRay = 1
                    effect.useSpark = 1
                    effect.rayAngle = 10
                    effect.splatScale = 20
                    effect.rayFlareValue = 3.0
                    effect.setColor(1, 1, 1, 1)
                    effect.setPos(0.5, 0, -2.0)
                    effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    effect = SparkBurst.getEffect()
                    if effect:
                        effect.reparentTo(self)
                        effect.setPos(0.5, 0, -2.0)
                        effect.particleDummy.reparentTo(self)
                        effectAnims.append(Func(effect.play, 'Yellow'))
                        self.effects.append(effect)

            elif self.hitNum == 3:
                effect = HitFlashA.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.useRay = 1
                    effect.useSpark = 1
                    effect.rayAngle = 60
                    effect.splatScale = 18
                    effect.rayFlareValue = 3.0
                    effect.setColor(1, 1, 1, 1)
                    effect.setPos(-1.5, 0, -1.0)
                    effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    effect = SparkBurst.getEffect()
                    if effect:
                        effect.reparentTo(self)
                        effect.setPos(-1.5, 0, -1.0)
                        effect.particleDummy.reparentTo(self)
                        effectAnims.append(Func(effect.play, 'Yellow'))
                        self.effects.append(effect)

            elif self.hitNum == 4:
                effect = HitFlashA.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.useRay = 1
                    effect.useSpark = 1
                    effect.rayAngle = 90
                    effect.splatScale = 30
                    effect.rayFlareValue = 4.0
                    effect.setColor(1, 1, 1, 1)
                    effect.setPos(0, 0, 0)
                    effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    effect = SparkBurst.getEffect()
                    if effect:
                        effect.reparentTo(self)
                        effect.setPos(0, 0, 0)
                        effect.particleDummy.reparentTo(self)
                        effectAnims.append(Func(effect.play, 'Yellow'))
                        self.effects.append(effect)
                    
                    shockwaveHitEffect = ShockwaveHit.getEffect()
                    if shockwaveHitEffect:
                        shockwaveHitEffect.reparentTo(self)
                        shockwaveHitEffect.size = 16
                        shockwaveHitEffect.speed = 0.2
                        shockwaveHitEffect.loadExplosion(Point3(-45, 45, 0), 'Hit')
                        shockwaveHitEffect.setColor(1, 1, 1, 1)
                        shockwaveHitEffect.setPos(0, 0, 0)
                        shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                        effectAnims.append(Func(shockwaveHitEffect.play))
                        self.effects.append(shockwaveHitEffect)
                    
                    shockwaveHitEffect = ShockwaveHit.getEffect()
                    if shockwaveHitEffect:
                        shockwaveHitEffect.reparentTo(self)
                        shockwaveHitEffect.size = 22
                        shockwaveHitEffect.speed = 0.2
                        shockwaveHitEffect.loadExplosion(Point3(-45, -45, 0), 'HitRay')
                        shockwaveHitEffect.setColor(1, 1, 1, 1)
                        shockwaveHitEffect.setPos(0, 0, 0)
                        shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                        effectAnims.append(Func(shockwaveHitEffect.play))
                        self.effects.append(shockwaveHitEffect)

        elif self.effectId == WeaponGlobals.VFX_CUT:
            effect = HitFlashA.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.useRay = 1
                effect.useSpark = 1
                effect.rayAngle = -25
                effect.splatScale = 10
                effect.rayFlareValue = 2.0
                effect.setColor(0.2, 0.5, 1, 1)
                effect.setPos(0, 0, 0.8)
                effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = SparkBurst.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(0, 0, 0.8)
                    effect.particleDummy.reparentTo(self)
                    effectAnims.append(Func(effect.play, 'Blue'))
                    self.effects.append(effect)

        elif self.effectId == WeaponGlobals.VFX_MULTIHIT:
            if self.hitNum == 0:
                effect = HitFlashA.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.useRay = 1
                    effect.useSpark = 1
                    effect.rayAngle = 0
                    effect.splatScale = 13
                    effect.rayFlareValue = 2.5
                    effect.setColor(0.2, 0.5, 1, 1)
                    effect.setPos(-0.5, 0, 0.8)
                    effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    effect = SparkBurst.getEffect()
                    if effect:
                        effect.reparentTo(self)
                        effect.setPos(-0.5, 0, 0.8)
                        effect.particleDummy.reparentTo(self)
                        effectAnims.append(Func(effect.play, 'Blue'))
                        self.effects.append(effect)
                
            elif self.hitNum == 1:
                effect = HitFlashA.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.useRay = 1
                    effect.useSpark = 1
                    effect.rayAngle = -25
                    effect.splatScale = 13
                    effect.rayFlareValue = 2.5
                    effect.setColor(0.2, 0.5, 1, 1)
                    effect.setPos(0.5, 0, -0.5)
                    effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    effect = SparkBurst.getEffect()
                    if effect:
                        effect.reparentTo(self)
                        effect.setPos(0.5, 0, -0.5)
                        effect.particleDummy.reparentTo(self)
                        effectAnims.append(Func(effect.play, 'Blue'))
                        self.effects.append(effect)

        elif self.effectId == WeaponGlobals.VFX_SWIPE:
            effect = HitFlashA.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.useRay = 1
                effect.useSpark = 1
                effect.rayAngle = 90
                effect.splatScale = 16
                effect.rayFlareValue = 2.5
                effect.setColor(0.2, 0.5, 1, 1)
                effect.setPos(0, 0, 0)
                effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                shockwaveHitEffect = ShockwaveHit.getEffect()
                if shockwaveHitEffect:
                    shockwaveHitEffect.reparentTo(self)
                    shockwaveHitEffect.size = 8
                    shockwaveHitEffect.speed = 0.2
                    shockwaveHitEffect.loadExplosion(Point3(0, 80, 0), 'Hit')
                    shockwaveHitEffect.setColor(0.3, 0.2, 1, 1)
                    shockwaveHitEffect.setPos(0, 0, 0)
                    shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(shockwaveHitEffect.play))
                    self.effects.append(shockwaveHitEffect)
                
                shockwaveHitEffect = ShockwaveHit.getEffect()
                if shockwaveHitEffect:
                    shockwaveHitEffect.reparentTo(self)
                    shockwaveHitEffect.size = 13
                    shockwaveHitEffect.speed = 0.2
                    shockwaveHitEffect.loadExplosion(Point3(-45, -45, 0), 'HitRay')
                    shockwaveHitEffect.setColor(0.3, 0.2, 1, 1)
                    shockwaveHitEffect.setPos(0, 0, 0)
                    shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(shockwaveHitEffect.play))
                    self.effects.append(shockwaveHitEffect)
                
                effect = SparkBurst.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(0, 0, 0)
                    effect.particleDummy.reparentTo(self)
                    effectAnims.append(Func(effect.play, 'Blue'))
                    self.effects.append(effect)

        elif self.effectId == WeaponGlobals.VFX_IMPALE:
            if self.hitNum == 0:
                effect = HitFlashA.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.useRay = 1
                    effect.useSpark = 1
                    effect.rayAngle = -35
                    effect.splatScale = 20
                    effect.rayFlareValue = 3.0
                    effect.setColor(0.2, 0.5, 1, 1)
                    effect.setPos(0, 0, 0.5)
                    effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    shockwaveHitEffect = ShockwaveHit.getEffect()
                    if shockwaveHitEffect:
                        shockwaveHitEffect.reparentTo(self)
                        shockwaveHitEffect.size = 8
                        shockwaveHitEffect.speed = 0.2
                        shockwaveHitEffect.loadExplosion(Point3(0, 80, 0), 'Hit')
                        shockwaveHitEffect.setColor(0.3, 0.2, 1, 1)
                        shockwaveHitEffect.setPos(0, 0, 0)
                        shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                        effectAnims.append(Func(shockwaveHitEffect.play))
                        self.effects.append(shockwaveHitEffect)
                    
                    shockwaveHitEffect = ShockwaveHit.getEffect()
                    if shockwaveHitEffect:
                        shockwaveHitEffect.reparentTo(self)
                        shockwaveHitEffect.size = 13
                        shockwaveHitEffect.speed = 0.2
                        shockwaveHitEffect.loadExplosion(Point3(-45, -45, 0), 'HitRay')
                        shockwaveHitEffect.setColor(0.3, 0.2, 1, 1)
                        shockwaveHitEffect.setPos(0, 0, 0)
                        shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                        effectAnims.append(Func(shockwaveHitEffect.play))
                        self.effects.append(shockwaveHitEffect)
                    
                    effect = SparkBurst.getEffect()
                    if effect:
                        effect.reparentTo(self)
                        effect.setPos(0, 0, 0)
                        effect.particleDummy.reparentTo(self)
                        effectAnims.append(Func(effect.play, 'Blue'))
                        self.effects.append(effect)

            elif self.hitNum == 1:
                effect = HitFlashA.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.useRay = 1
                    effect.useSpark = 1
                    effect.rayAngle = 35
                    effect.splatScale = 20
                    effect.rayFlareValue = 3.0
                    effect.setColor(0.2, 0.5, 1, 1)
                    effect.setPos(0, 0, 0.5)
                    effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    shockwaveHitEffect = ShockwaveHit.getEffect()
                    if shockwaveHitEffect:
                        shockwaveHitEffect.reparentTo(self)
                        shockwaveHitEffect.size = 8
                        shockwaveHitEffect.speed = 0.2
                        shockwaveHitEffect.loadExplosion(Point3(0, 80, 0), 'Hit')
                        shockwaveHitEffect.setColor(0.3, 0.2, 1, 1)
                        shockwaveHitEffect.setPos(0, 0, 0)
                        shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                        effectAnims.append(Func(shockwaveHitEffect.play))
                        self.effects.append(shockwaveHitEffect)
                    
                    shockwaveHitEffect = ShockwaveHit.getEffect()
                    if shockwaveHitEffect:
                        shockwaveHitEffect.reparentTo(self)
                        shockwaveHitEffect.size = 13
                        shockwaveHitEffect.speed = 0.2
                        shockwaveHitEffect.loadExplosion(Point3(-45, -45, 0), 'HitRay')
                        shockwaveHitEffect.setColor(0.3, 0.2, 1, 1)
                        shockwaveHitEffect.setPos(0, 0, 0)
                        shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                        effectAnims.append(Func(shockwaveHitEffect.play))
                        self.effects.append(shockwaveHitEffect)
                    
                    effect = SparkBurst.getEffect()
                    if effect:
                        effect.reparentTo(self)
                        effect.setPos(0, 0, 0)
                        effect.particleDummy.reparentTo(self)
                        effectAnims.append(Func(effect.play, 'Blue'))
                        self.effects.append(effect)

            elif self.hitNum == 2:
                effect = HitFlashA.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.useRay = 1
                    effect.useSpark = 1
                    effect.rayAngle = -35
                    effect.splatScale = 20
                    effect.rayFlareValue = 3.0
                    effect.setColor(0.2, 0.5, 1, 1)
                    effect.setPos(0, 0, 0.5)
                    effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    shockwaveHitEffect = ShockwaveHit.getEffect()
                    if shockwaveHitEffect:
                        shockwaveHitEffect.reparentTo(self)
                        shockwaveHitEffect.size = 8
                        shockwaveHitEffect.speed = 0.2
                        shockwaveHitEffect.loadExplosion(Point3(0, 80, 0), 'Hit')
                        shockwaveHitEffect.setColor(0.3, 0.2, 1, 1)
                        shockwaveHitEffect.setPos(0, 0, 0)
                        shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                        effectAnims.append(Func(shockwaveHitEffect.play))
                        self.effects.append(shockwaveHitEffect)
                    
                    shockwaveHitEffect = ShockwaveHit.getEffect()
                    if shockwaveHitEffect:
                        shockwaveHitEffect.reparentTo(self)
                        shockwaveHitEffect.size = 13
                        shockwaveHitEffect.speed = 0.2
                        shockwaveHitEffect.loadExplosion(Point3(-45, -45, 0), 'HitRay')
                        shockwaveHitEffect.setColor(0.3, 0.2, 1, 1)
                        shockwaveHitEffect.setPos(0, 0, 0)
                        shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                        effectAnims.append(Func(shockwaveHitEffect.play))
                        self.effects.append(shockwaveHitEffect)
                    
                    effect = SparkBurst.getEffect()
                    if effect:
                        effect.reparentTo(self)
                        effect.setPos(0, 0, 0)
                        effect.particleDummy.reparentTo(self)
                        effectAnims.append(Func(effect.play, 'Blue'))
                        self.effects.append(effect)

        elif self.effectId == WeaponGlobals.VFX_THROWHIT:
            effect = HitFlashA.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.useRay = 1
                effect.useSpark = 1
                effect.rayAngle = 90
                effect.splatScale = 13
                effect.rayFlareValue = 2.5
                effect.setColor(1, 1, 1, 1)
                effect.setPos(0, 0, 0)
                effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                shockwaveHitEffect = ShockwaveHit.getEffect()
                if shockwaveHitEffect:
                    shockwaveHitEffect.reparentTo(self)
                    shockwaveHitEffect.size = 13
                    shockwaveHitEffect.speed = 0.2
                    shockwaveHitEffect.loadExplosion(Point3(-45, -45, 0), 'HitRay')
                    shockwaveHitEffect.setColor(1, 1, 1, 1)
                    shockwaveHitEffect.setPos(0, 0, 0)
                    shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(shockwaveHitEffect.play))
                    self.effects.append(shockwaveHitEffect)
                
                effect = SparkBurst.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(0, 0, 0)
                    effect.particleDummy.reparentTo(self)
                    effectAnims.append(Func(effect.play, 'Yellow'))
                    self.effects.append(effect)

        elif self.effectId == WeaponGlobals.VFX_POISON:
            effect = HitFlashA.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.useRay = 0
                effect.useSpark = 1
                effect.rayAngle = 0
                effect.splatScale = 13
                effect.rayFlareValue = 2.5
                effect.setColor(1, 1, 1, 1)
                effect.setPos(0, 0, 0)
                effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = PoisonHit.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(0, 0, 0)
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)

        elif self.effectId == WeaponGlobals.VFX_BLIND:
            effect = HitFlashA.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.useRay = 0
                effect.useSpark = 1
                effect.splatScale = 10
                effect.rayFlareValue = 2.0
                effect.setColor(1, 1, 1, 1)
                effect.setPos(0, 0, 0)
                effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
        elif self.effectId == WeaponGlobals.VFX_WOUND:
            effect = HitFlashA.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.useRay = 1
                effect.useSpark = 1
                effect.rayAngle = 45
                effect.splatScale = 15
                effect.rayFlareValue = 3.0
                effect.setColor(1, 0.4, 0.4, 1)
                effect.setPos(0, 0, 0)
                effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = HitFlashA.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.useRay = 1
                    effect.useSpark = 1
                    effect.rayAngle = -45
                    effect.splatScale = 20
                    effect.rayFlareValue = 3.0
                    effect.setColor(1, 0.5, 0.5, 1)
                    effect.setPos(0, 0, 0)
                    effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                shockwaveHitEffect = ShockwaveHit.getEffect()
                if shockwaveHitEffect:
                    shockwaveHitEffect.reparentTo(self)
                    shockwaveHitEffect.size = 15
                    shockwaveHitEffect.speed = 0.5
                    shockwaveHitEffect.loadExplosion(Point3(-45, -45, 0), 'HitRay')
                    shockwaveHitEffect.setColor(1.0, 1.0, 1, 1)
                    shockwaveHitEffect.setPos(0, 0, 0)
                    shockwaveHitEffect.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(shockwaveHitEffect.play))
                    self.effects.append(shockwaveHitEffect)

        elif self.effectId == WeaponGlobals.VFX_TRIPLEHIT:
            hitNum = random.randint(0, 2)
            if hitNum == 0:
                effect = HitFlashA.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.useRay = 1
                    effect.useSpark = 1
                    effect.rayAngle = 10
                    effect.splatScale = 15
                    effect.rayFlareValue = 3.5
                    effect.setColor(0.2, 0.5, 1, 1)
                    effect.setPos(-0.5, 0, 0.8)
                    effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    effect = SparkBurst.getEffect()
                    if effect:
                        effect.reparentTo(self)
                        effect.setPos(-0.5, 0, 0.8)
                        effect.particleDummy.reparentTo(self)
                        effectAnims.append(Func(effect.play, 'Blue'))
                        self.effects.append(effect)

            elif hitNum == 1:
                effect = HitFlashA.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.useRay = 1
                    effect.useSpark = 1
                    effect.rayAngle = -25
                    effect.splatScale = 15
                    effect.rayFlareValue = 3.5
                    effect.setColor(0.2, 0.5, 1, 1)
                    effect.setPos(0.5, 0, -0.5)
                    effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    effect = SparkBurst.getEffect()
                    if effect:
                        effect.reparentTo(self)
                        effect.setPos(0.5, 0, -0.5)
                        effect.particleDummy.reparentTo(self)
                        effectAnims.append(Func(effect.play, 'Blue'))
                        self.effects.append(effect)

            elif hitNum == 2:
                effect = HitFlashA.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.useRay = 1
                    effect.useSpark = 1
                    effect.rayAngle = 45
                    effect.splatScale = 15
                    effect.rayFlareValue = 3.5
                    effect.setColor(0.2, 0.5, 1, 1)
                    effect.setPos(-0.5, 0, 0)
                    effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    effect = SparkBurst.getEffect()
                    if effect:
                        effect.reparentTo(self)
                        effect.setPos(-0.5, 0, 0)
                        effect.particleDummy.reparentTo(self)
                        effectAnims.append(Func(effect.play, 'Blue'))
                        self.effects.append(effect)

        elif self.effectId == WeaponGlobals.VFX_WASP:
            if self.hitNum == 0:
                waspEffect = WaspCloud.getEffect()
                if waspEffect:
                    waspEffect.reparentTo(self)
                    waspEffect.setPos(0, 0, 0)
                    waspEffect.particleDummy.reparentTo(self)
                    effectAnims.append(Func(waspEffect.play))
                    self.effects.append(waspEffect)
                
            elif self.hitNum == 1:
                pass
            
        elif self.effectId == WeaponGlobals.VFX_CURSE:
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = CurseHit.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(0, 0, 0)
                    effect.setScale(0.5, 0.5, 1)
                    effect.particleDummy.reparentTo(self)
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)

            effect = FadingSigil.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.setPos(0, 0, 1.0)
                effect.fadeColor = Vec4(0.2, 0.8, 0.2, 1.0)
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
        elif self.effectId == WeaponGlobals.VFX_HEAL:
            effect = HitFlashA.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.useRay = 0
                effect.useSpark = 0
                effect.splatScale = 15
                effect.setColor(0.2, 0.2, 1, 1)
                effect.setPos(0, 0, 0)
                effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = HealSmoke.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(self, 0, 0, -2.0)
                    effect.setEffectColor(Vec4(0.2, 0.2, 1, 1))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)

            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = HealRays.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(self, 0, 0, 0)
                    effect.setScale(0.5, 0.5, 2.5)
                    effect.setEffectColor(Vec4(0.2, 0.2, 1, 1))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
            
        elif self.effectId == WeaponGlobals.VFX_CURE:
            effect = HitFlashA.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.useRay = 0
                effect.useSpark = 1
                effect.splatScale = 15
                effect.setColor(0.2, 0.5, 0.5, 1)
                effect.setPos(0, 0, 0)
                effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = HealSmoke.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(self, 0, 0, -2.0)
                    effect.setEffectColor(Vec4(0, 1, 0, 1))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = HealSparks.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(self, 0, 0, 0)
                    effect.setScale(1, 1, 3)
                    effect.setEffectColor(Vec4(0.2, 0.5, 0.5, 1))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                effect = HealRays.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(self, 0, 0, 0)
                    effect.setScale(0.5, 0.5, 2.5)
                    effect.setEffectColor(Vec4(0.2, 0.5, 0.5, 1))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)

        elif self.effectId == WeaponGlobals.VFX_TONIC:
            effect = HitFlashA.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.useRay = 0
                effect.useSpark = 1
                effect.splatScale = 20
                effect.setColor(0.3, 0.75, 1, 1)
                effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = HealSparks.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setHpr(self, 0, 90, 0)
                    effect.setScale(1, 1, 3)
                    effect.setEffectColor(Vec4(0.3, 1, 1, 0.25))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                effect = HealRays.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setHpr(self, 0, 90, 0)
                    effect.setScale(0.4, 0.4, 2.5)
                    effect.setEffectColor(Vec4(0.3, 1, 1, 1))
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
            
        elif self.effectId == WeaponGlobals.VFX_FIRE:
            effect = FireballHit.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.setPos(0, 0, -2)
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
        elif self.effectId == WeaponGlobals.VFX_ATTUNE:
            effect = HitFlashA.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.useRay = 0
                effect.useSpark = 1
                effect.splatScale = 10
                effect.setColor(0.3, 0.2, 0.75, 1)
                effect.setPos(0, 0, 0)
                effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingColor, ColorBlendAttrib.OOneMinusIncomingAlpha))
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
        elif self.effectId == WeaponGlobals.VFX_POKE:
            effect = FlashStar.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.splatScale = 10
                effect.setColor(0.5, 0.0, 0.5, 1)
                effect.setPos(0, 0, 0)
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
        elif self.effectId == WeaponGlobals.VFX_DRAINLIFE:
            effect = SpectralSmoke.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.setPos(self, 0, 0, 0)
                effect.setScale(1.25, 1.25, 2.5)
                effectAnims.append(Func(effect.play, duration = 1.0))
                self.effects.append(effect)
            
        elif self.effectId == WeaponGlobals.VFX_VOODOO or self.effectId == WeaponGlobals.VFX_SOULFLAY:
            effect = DarkStar.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.setPos(0, 0, 0)
                if self.colorEffect:
                    effect.setEffectColor(self.colorEffect)
                
                effectAnims.append(Func(effect.play, 0.3))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = SparkBurst.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(0, 0, 0)
                    effect.particleDummy.reparentTo(self)
                    if self.colorEffect:
                        effect.setEffectColor(self.colorEffect)
                    
                    effectAnims.append(Func(effect.play, 'Dark'))
                    self.effects.append(effect)
                
                shockwaveHitEffect = ShockwaveHit.getEffect()
                if shockwaveHitEffect:
                    shockwaveHitEffect.reparentTo(self)
                    shockwaveHitEffect.size = 10
                    shockwaveHitEffect.speed = 0.35
                    shockwaveHitEffect.loadExplosion(Point3(0, 0, 0), 'Dark')
                    shockwaveHitEffect.setPos(0, 0, 0)
                    if self.colorEffect:
                        shockwaveHitEffect.setColor(self.colorEffect)
                    
                    effectAnims.append(Func(shockwaveHitEffect.play))
                    self.effects.append(shockwaveHitEffect)

        elif self.effectId == WeaponGlobals.VFX_PESTILENCE:
            effectActor = Actor.Actor('models/effects/mopath_none', {
                'spin': 'models/effects/mopath_spiral'})
            joint = effectActor.find('**/joint1')
            effectActor.setScale(4.0, 3.5, 4.0)
            effectActor.setP(-90)
            effectActor.reparentTo(self)
            effectActor.setPos(self, 0.0, 0.0, 0.0)
            effectActor.setPlayRate(2.5, 'spin')
            effectAnims.append(Func(effectActor.play, 'spin'))
            effect = VoodooPestilence.getEffect()
            if effect:
                effect.particleDummy.reparentTo(self)
                effect.reparentTo(joint)
                effect.effectScale = 4.0
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                shockwaveHitEffect = ShockwaveHit.getEffect()
                if shockwaveHitEffect:
                    shockwaveHitEffect.reparentTo(self)
                    shockwaveHitEffect.size = 13
                    shockwaveHitEffect.speed = 0.3
                    shockwaveHitEffect.loadExplosion(Point3(0, 0, 0), 'Dark')
                    shockwaveHitEffect.setColor(0.25, 0.75, 0.25, 1)
                    shockwaveHitEffect.setPos(0, 0, 0)
                    effectAnims.append(Func(shockwaveHitEffect.play))
                    self.effects.append(shockwaveHitEffect)

        elif self.effectId == WeaponGlobals.VFX_BANISH:
            flashEffect = MuzzleFlash.getEffect()
            if flashEffect:
                flashEffect.reparentTo(self)
                flashEffect.flash.setScale(100)
                flashEffect.startCol = Vec4(0.5, 0.25, 1.0, 1)
                flashEffect.fadeTime = 0.35
                effectAnims.append(Func(flashEffect.play))
                self.effects.append(flashEffect)
            
            shockwaveHitEffect = ShockwaveHit.getEffect()
            if shockwaveHitEffect:
                shockwaveHitEffect.reparentTo(self)
                shockwaveHitEffect.size = 18
                shockwaveHitEffect.speed = 0.5
                shockwaveHitEffect.loadExplosion(Point3(0, 0, 0), 'Dark')
                shockwaveHitEffect.setColor(1, 0, 1, 1)
                shockwaveHitEffect.setPos(0, 0, 0)
                if self.colorEffect:
                    shockwaveHitEffect.setColor(self.colorEffect)
                
                effectAnims.append(Func(shockwaveHitEffect.play))
                self.effects.append(shockwaveHitEffect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                explosionEffect = VoodooExplosion.getEffect()
                if explosionEffect:
                    explosionEffect.reparentTo(self)
                    explosionEffect.setPos(self, 0, 0, -2)
                    if self.colorEffect:
                        explosionEffect.setEffectColor(self.colorEffect)
                    
                    effectAnims.append(Func(explosionEffect.play))
                    self.effects.append(explosionEffect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                dustRing = DustRingBanish.getEffect()
                if dustRing:
                    dustRing.reparentTo(self)
                    dustRing.setPos(self, 0, 0, -2)
                    if self.colorEffect:
                        dustRing.setEffectColor(self.colorEffect)
                    
                    effectAnims.append(Func(dustRing.play))
                    self.effects.append(dustRing)
                
                cameraShakerEffect = CameraShaker()
                cameraShakerEffect.wrtReparentTo(self)
                cameraShakerEffect.shakeSpeed = 0.06
                cameraShakerEffect.shakePower = 4.0
                cameraShakerEffect.numShakes = 2
                cameraShakerEffect.scalePower = 1
                effectAnims.append(Func(cameraShakerEffect.play, 80.0))
            
        elif self.effectId == WeaponGlobals.VFX_WITHER or self.effectId == WeaponGlobals.VFX_DESOLATION:
            effect = WitherStar.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.setPos(0, 0, 0)
                if self.colorEffect:
                    effect.setEffectColor(self.colorEffect)
                
                effectAnims.append(Func(effect.play, 0.2))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = SparkBurst.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.particleDummy.reparentTo(self)
                    if self.colorEffect:
                        effect.setEffectColor(self.colorEffect)
                    
                    effectAnims.append(Func(effect.play, 'Blue'))
                    self.effects.append(effect)
                
                shockwaveHitEffect = ShockwaveHit.getEffect()
                if shockwaveHitEffect:
                    shockwaveHitEffect.reparentTo(self)
                    shockwaveHitEffect.size = 15
                    shockwaveHitEffect.speed = 0.5
                    shockwaveHitEffect.loadExplosion(Point3(0, 0, 0), 'Pulse')
                    shockwaveHitEffect.setColor(1, 1, 1, 1)
                    if self.colorEffect:
                        shockwaveHitEffect.setColor(self.colorEffect)
                    
                    shockwaveHitEffect.setPos(0, 0, 0)
                    effectAnims.append(Func(shockwaveHitEffect.play))
                    self.effects.append(shockwaveHitEffect)

        elif self.effectId == WeaponGlobals.VFX_HELLFIRE:
            if base.options.getSpecialEffectsSetting() == base.options.SpecialEffectsLow:
                effect = FireballHit.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = HellFire.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(self, 0, 0, -2)
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)

        else:
            effect = HitFlashA.getEffect()
            if effect:
                effect.reparentTo(self)
                effect.useRay = 0
                effect.useSpark = 1
                effect.splatScale = 10
                effect.setColor(1, 1, 1, 1)
                effect.setPos(0, 0, 0)
                effect.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                effectAnims.append(Func(effect.play))
                self.effects.append(effect)
            
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = HitStar.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(0, 0, 0)
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)
                
                effect = SparkBurst.getEffect()
                if effect:
                    effect.reparentTo(self)
                    effect.setPos(0, 0, 0)
                    effect.particleDummy.reparentTo(self)
                    effectAnims.append(Func(effect.play))
                    self.effects.append(effect)

        self.ival.append(effectAnims)
        self.ival.append(Wait(self.MAX_DURATION))
        self.ival.append(Func(self.destroy))

    def play(self):
        if self.ival:
            self.ival.start()

    def destroy(self):
        if self.ival:
            self.ival.pause()
            self.ival = None
        
        for effect in self.effects:
            if effect:
                effect.stop()
                effect = None
        
        self.effects = []
        self.removeNode()


