# Embedded file name: pirates.effects.FireworkEffect
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
import random
from pirates.effects.FireworkGlobals import *
from pirates.effects.Glow import Glow
from pirates.effects.GlowTrail import GlowTrail
from pirates.effects.SparksTrail import SparksTrail
from pirates.effects.SparksTrailLong import SparksTrailLong
from pirates.effects.FlashEffect import FlashEffect
from pirates.effects.BlastEffect import BlastEffect
from pirates.effects.Sparkles import Sparkles
from pirates.effects.SimpleSparkles import SimpleSparkles
from pirates.effects.NoiseSparkles import NoiseSparkles
from pirates.effects.RayBurst import RayBurst
from pirates.effects.StarBurst import StarBurst
from pirates.effects.CircleBurst import CircleBurst
from pirates.effects.ShellBurst import ShellBurst
from pirates.effects.SkullBurst import SkullBurst
from pirates.effects.SkullFlash import SkullFlash
from pirates.effects.TrailExplosion import TrailExplosion
trailSfxNames = [
 'firework_whistle_01.mp3', 'firework_whistle_02.mp3']
burstSfxNames = [
 'firework_explosion_01.mp3', 'firework_explosion_02.mp3', 'firework_explosion_03.mp3', 'firework_distance_01.mp3', 'firework_distance_02.mp3', 'firework_distance_03.mp3']

class FireworkEffect(NodePath):

    def __init__(self, burstEffectId, trailEffectId=FireworkTrailType.Default, velocity=Vec3(0, 0, 400), scale=1.0, primaryColor=Vec4(1, 1, 1, 1), secondaryColor=None, burstDelay=1.5):
        NodePath.__init__(self, 'FireworkEffect')
        self.burstTypeId = burstEffectId
        self.trailTypeId = trailEffectId
        self.velocity = velocity
        self.scale = scale
        self.primaryColor = primaryColor
        self.secondaryColor = secondaryColor
        if not self.secondaryColor:
            self.secondaryColor = self.primaryColor
        self.burstDelay = burstDelay
        self.gravityMult = 3.0
        self.fireworkMainIval = None
        self.trailEffectsIval = None
        self.burstEffectsIval = None
        self.effectsNode = self.attachNewNode('fireworkEffectsNode')
        self.trailEffects = []
        self.burstEffects = []
        self.trailSfx = []
        for filename in trailSfxNames:
            self.trailSfx.append(base.loadSfx('audio/' + filename))

        self.burstSfx = []
        for filename in burstSfxNames:
            self.burstSfx.append(base.loadSfx('audio/' + filename))

        return

    def play(self):
        self.getFireworkMainIval().start()

    def getFireworkMainIval(self):
        self.effectsNode.setPos(0, 0, 0)
        if not self.fireworkMainIval:
            self.fireworkMainIval = Parallel()
            self.fireworkMainIval.append(self.getTrailEffectsIval())
            self.fireworkMainIval.append(Sequence(Wait(self.burstDelay - 0.1), Func(self.cleanupTrailEffects), self.getBurstEffectsIval(), Func(self.cleanupBurstEffects), Func(self.cleanupEffect)))
        return self.fireworkMainIval

    def getTrailEffectsIval(self):
        if not self.trailEffectsIval:
            self.trailEffectsIval = Parallel()
            self.trailEffectsIval.append(ProjectileInterval(self.effectsNode, startVel=self.velocity, duration=self.burstDelay, gravityMult=self.gravityMult))
            if self.trailTypeId is None:
                return self.trailEffectsIval
            self.trailEffectsIval.append(SoundInterval(random.choice(self.trailSfx), node=self.effectsNode, cutOff=3000))
            if base.options.getSpecialEffectsSetting() == base.options.SpecialEffectsLow:
                if self.trailTypeId != FireworkTrailType.LongGlowSparkle:
                    self.trailTypeId = FireworkTrailType.Default
            if self.trailTypeId == FireworkTrailType.Default:
                glowEffect = Glow.getEffect()
                if glowEffect:
                    glowEffect.reparentTo(self.effectsNode)
                    glowEffect.setColorScale(Vec4(1, 1, 1, 1))
                    glowEffect.setScale(30.0)
                    self.trailEffects.append(glowEffect)
                    self.trailEffectsIval.append(Func(glowEffect.startLoop))
            elif self.trailTypeId == FireworkTrailType.Glow:
                trailEffect = GlowTrail.getEffect()
                if trailEffect:
                    trailEffect.reparentTo(self.effectsNode)
                    trailEffect.setEffectScale(self.scale * 0.75)
                    trailEffect.setEffectColor(Vec4(1, 1, 1, 1))
                    trailEffect.setLifespan(0.25)
                    self.trailEffects.append(trailEffect)
                    self.trailEffectsIval.append(Func(trailEffect.startLoop))
            elif self.trailTypeId == FireworkTrailType.Sparkle:
                trailEffect = SparksTrail.getEffect()
                if trailEffect:
                    trailEffect.reparentTo(self.effectsNode)
                    trailEffect.setEffectScale(self.scale)
                    trailEffect.setEffectColor(Vec4(1, 1, 1, 1))
                    self.trailEffects.append(trailEffect)
                    self.trailEffectsIval.append(Func(trailEffect.startLoop))
            elif self.trailTypeId == FireworkTrailType.GlowSparkle:
                glowEffect = Glow.getEffect()
                if glowEffect:
                    glowEffect.reparentTo(self.effectsNode)
                    glowEffect.setColorScale(Vec4(1, 1, 1, 1))
                    glowEffect.setScale(50.0)
                    self.trailEffects.append(glowEffect)
                    self.trailEffectsIval.append(Func(glowEffect.startLoop))
                trailEffect = SparksTrail.getEffect()
                if trailEffect:
                    trailEffect.reparentTo(self.effectsNode)
                    trailEffect.setEffectScale(self.scale)
                    trailEffect.setEffectColor(Vec4(1, 1, 1, 1))
                    self.trailEffects.append(trailEffect)
                    self.trailEffectsIval.append(Func(trailEffect.startLoop))
            elif self.trailTypeId == FireworkTrailType.LongSparkle:
                trailEffect = SparksTrailLong.getEffect()
                if trailEffect:
                    trailEffect.reparentTo(self.effectsNode)
                    trailEffect.setEffectScale(self.scale)
                    trailEffect.setEffectColor(Vec4(1, 1, 1, 1))
                    trailEffect.setLifespan(4.0)
                    self.trailEffects.append(trailEffect)
                    self.trailEffectsIval.append(Func(trailEffect.startLoop))
            elif self.trailTypeId == FireworkTrailType.LongGlowSparkle:
                trailEffect = SparksTrailLong.getEffect()
                if trailEffect:
                    trailEffect.reparentTo(self.effectsNode)
                    trailEffect.setEffectScale(self.scale)
                    trailEffect.setEffectColor(self.secondaryColor)
                    trailEffect.setLifespan(3.5)
                    self.trailEffects.append(trailEffect)
                    self.trailEffectsIval.append(Func(trailEffect.startLoop))
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                    trailEffect = GlowTrail.getEffect()
                    if trailEffect:
                        trailEffect.reparentTo(self.effectsNode)
                        trailEffect.setEffectScale(self.scale)
                        trailEffect.setEffectColor(self.primaryColor)
                        trailEffect.setLifespan(1.0)
                        self.trailEffects.append(trailEffect)
                        self.trailEffectsIval.append(Func(trailEffect.startLoop))
        return self.trailEffectsIval

    def getBurstEffectsIval(self):
        if not self.burstEffectsIval:
            self.burstEffectsIval = Parallel()
            if self.burstTypeId is None:
                return self.burstEffectsIval
            self.burstEffectsIval.append(SoundInterval(random.choice(self.burstSfx), node=self.effectsNode, cutOff=8000))
            flash = FlashEffect.getEffect()
            if flash:
                flash.reparentTo(self.effectsNode)
                flash.setEffectColor(self.primaryColor)
                flash.setScale(1200 * self.scale)
                flash.fadeTime = 0.5
                self.burstEffectsIval.append(Sequence(Wait(0.1), flash.getTrack()))
                self.burstEffects.append(flash)
            primaryBlast = BlastEffect.getEffect()
            if primaryBlast:
                primaryBlast.reparentTo(self.effectsNode)
                primaryBlast.setScale(100 * self.scale)
                primaryBlast.setEffectColor(Vec4(1, 1, 1, 1))
                primaryBlast.fadeTime = 0.75
                self.burstEffectsIval.append(Sequence(Wait(0.1), primaryBlast.getTrack()))
                self.burstEffects.append(primaryBlast)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                secondaryBlast = BlastEffect.getEffect()
                if secondaryBlast:
                    secondaryBlast.reparentTo(self.effectsNode)
                    secondaryBlast.setScale(250 * self.scale)
                    secondaryBlast.setEffectColor(self.primaryColor)
                    secondaryBlast.fadeTime = 0.3
                    self.burstEffectsIval.append(Sequence(Wait(0.1), secondaryBlast.getTrack()))
                    self.burstEffects.append(secondaryBlast)
            if self.burstTypeId == FireworkBurstType.Sparkles:
                sparkles = Sparkles.getEffect()
                if sparkles:
                    sparkles.reparentTo(self.effectsNode)
                    sparkles.setEffectScale(self.scale)
                    sparkles.setRadius(100 * self.scale)
                    sparkles.setEffectColor(self.primaryColor)
                    self.burstEffectsIval.append(Sequence(Wait(0.1), sparkles.getTrack()))
                    self.burstEffects.append(sparkles)
            if self.burstTypeId == FireworkBurstType.BasicShell:
                explosion = ShellBurst.getEffect()
                if explosion:
                    explosion.reparentTo(self.effectsNode)
                    explosion.setEffectScale(self.scale)
                    explosion.setEffectColor(self.primaryColor)
                    self.burstEffectsIval.append(Sequence(Wait(0.1), explosion.getTrack()))
                    self.burstEffects.append(explosion)
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                    rays = RayBurst.getEffect()
                    if rays:
                        rays.reparentTo(self.effectsNode)
                        rays.setEffectScale(self.scale)
                        rays.setEffectColor(self.primaryColor)
                        self.burstEffectsIval.append(rays.getTrack())
                        self.burstEffects.append(rays)
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    sparkles = Sparkles.getEffect()
                    if sparkles:
                        sparkles.reparentTo(self.effectsNode)
                        sparkles.setEffectScale(self.scale * 1.25)
                        sparkles.setEffectColor(self.secondaryColor)
                        self.burstEffectsIval.append(Sequence(Wait(0.1), sparkles.getTrack()))
                        self.burstEffects.append(sparkles)
            elif self.burstTypeId == FireworkBurstType.LongShell:
                explosion = StarBurst.getEffect()
                if explosion:
                    explosion.reparentTo(self.effectsNode)
                    explosion.setEffectScale(self.scale)
                    explosion.setEffectColor(self.primaryColor)
                    self.burstEffectsIval.append(Sequence(Wait(0.1), explosion.getTrack()))
                    self.burstEffects.append(explosion)
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                    rays = RayBurst.getEffect()
                    if rays:
                        rays.reparentTo(self.effectsNode)
                        rays.setEffectScale(self.scale)
                        rays.setEffectColor(self.primaryColor)
                        self.burstEffectsIval.append(rays.getTrack())
                        self.burstEffects.append(rays)
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    sparkles = SimpleSparkles.getEffect()
                    if sparkles:
                        sparkles.reparentTo(self.effectsNode)
                        sparkles.setEffectScale(self.scale)
                        sparkles.setRadius(100 * self.scale)
                        sparkles.setEffectColor(self.secondaryColor)
                        self.burstEffectsIval.append(Sequence(Wait(0.1), sparkles.getTrack()))
                        self.burstEffects.append(sparkles)
            elif self.burstTypeId == FireworkBurstType.SkullBlast:
                explosion = SkullBurst.getEffect()
                if explosion:
                    explosion.reparentTo(self.effectsNode)
                    explosion.setEffectScale(self.scale)
                    explosion.setEffectColor(self.primaryColor)
                    self.burstEffectsIval.append(Sequence(Wait(0.12), explosion.getTrack()))
                    self.burstEffects.append(explosion)
                skullFlash = SkullFlash.getEffect()
                if skullFlash:
                    skullFlash.reparentTo(self.effectsNode)
                    skullFlash.setScale(650 * self.scale)
                    skullFlash.fadeTime = 1.3
                    self.burstEffectsIval.append(Sequence(Wait(0.12), skullFlash.getTrack()))
                    self.burstEffects.append(skullFlash)
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                    rays = RayBurst.getEffect()
                    if rays:
                        rays.reparentTo(self.effectsNode)
                        rays.setEffectScale(self.scale * 1.3)
                        rays.setEffectColor(self.primaryColor)
                        self.burstEffectsIval.append(rays.getTrack())
                        self.burstEffects.append(rays)
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    sparkles = Sparkles.getEffect()
                    if sparkles:
                        sparkles.reparentTo(self.effectsNode)
                        sparkles.setEffectScale(self.scale / 1.2)
                        sparkles.setRadius(400 * self.scale)
                        sparkles.setEffectColor(self.secondaryColor)
                        self.burstEffectsIval.append(Sequence(Wait(0.12), sparkles.getTrack()))
                        self.burstEffects.append(sparkles)
            elif self.burstTypeId == FireworkBurstType.TrailExplosion:
                explosion = TrailExplosion.getEffect()
                if explosion:
                    explosion.reparentTo(self.effectsNode)
                    explosion.setEffectScale(self.scale)
                    explosion.setEffectColor(self.primaryColor)
                    explosion.numTrails = 3 + base.options.getSpecialEffectsSetting()
                    self.burstEffectsIval.append(Sequence(Wait(0.1), explosion.getTrack()))
                    self.burstEffects.append(explosion)
            elif self.burstTypeId == FireworkBurstType.RingBlast:
                explosion = CircleBurst.getEffect()
                if explosion:
                    explosion.reparentTo(self.effectsNode)
                    explosion.setEffectScale(self.scale)
                    explosion.setEffectColor(self.primaryColor)
                    self.burstEffectsIval.append(Sequence(Wait(0.1), explosion.getTrack()))
                    self.burstEffects.append(explosion)
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    sparkles = SimpleSparkles.getEffect()
                    if sparkles:
                        sparkles.reparentTo(self.effectsNode)
                        sparkles.setEffectScale(self.scale / 1.25)
                        sparkles.setRadius(50 * self.scale)
                        sparkles.setEffectColor(self.secondaryColor)
                        self.burstEffectsIval.append(Sequence(Wait(0.12), sparkles.getTrack()))
                        self.burstEffects.append(sparkles)
            elif self.burstTypeId == FireworkBurstType.NoiseBall:
                explosion = NoiseSparkles.getEffect()
                if explosion:
                    explosion.reparentTo(self.effectsNode)
                    explosion.setEffectScale(self.scale)
                    explosion.setEffectColor(self.primaryColor)
                    self.burstEffectsIval.append(Sequence(Wait(0.1), explosion.getTrack()))
                    self.burstEffects.append(explosion)
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                    rays = RayBurst.getEffect()
                    if rays:
                        rays.reparentTo(self.effectsNode)
                        rays.setEffectScale(self.scale)
                        rays.setEffectColor(self.primaryColor)
                        self.burstEffectsIval.append(rays.getTrack())
                        self.burstEffects.append(rays)
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    sparkles = SimpleSparkles.getEffect()
                    if sparkles:
                        sparkles.reparentTo(self.effectsNode)
                        sparkles.setEffectScale(self.scale * 1.3)
                        sparkles.setRadius(200 * self.scale)
                        sparkles.setEffectColor(self.secondaryColor)
                        self.burstEffectsIval.append(Sequence(Wait(0.1), sparkles.getTrack()))
                        self.burstEffects.append(sparkles)
        return self.burstEffectsIval

    def cleanupTrailEffects(self):
        if self.trailEffectsIval:
            self.trailEffectsIval.pause()
            self.trailEffectsIval = None
        for effect in self.trailEffects:
            effect.stopLoop()
            effect = None

        self.trailEffects = []
        return

    def cleanupBurstEffects(self):
        if self.burstEffectsIval:
            self.burstEffectsIval.pause()
            self.burstEffectsIval = None
        for effect in self.burstEffects:
            effect.stop()
            effect = None

        self.burstEffects = []
        return

    def cleanupEffect(self):
        if self.fireworkMainIval:
            self.fireworkMainIval.pause()
            self.fireworkMainIval = None
        self.cleanupTrailEffects()
        self.cleanupBurstEffects()
        return