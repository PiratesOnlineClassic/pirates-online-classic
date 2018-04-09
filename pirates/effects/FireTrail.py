# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.FireTrail
import random

from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.particles import ForceGroup, ParticleEffect, Particles
from EffectController import EffectController
from pandac.PandaModules import *
from PooledEffect import PooledEffect


class FireTrail(PooledEffect, EffectController):
    
    cardScale = 128.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.wantGlow = 1
        self.glow = None
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleVolcanoLava')
        if not FireTrail.particleDummy:
            FireTrail.particleDummy = render.attachNewNode(ModelNode('FireTrailParticleDummy'))
            FireTrail.particleDummy.setDepthWrite(0)
            FireTrail.particleDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
            FireTrail.particleDummy.setFogOff()
            FireTrail.particleDummy.setLightOff()
            FireTrail.particleDummy.setColorScaleOff()
            FireTrail.particleDummy.setBin('fixed', 60)
            FireTrail.particleDummy.setTwoSided(1)
        self.f = ParticleEffect.ParticleEffect()
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('PointEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(48)
        self.p0.setBirthRate(0.1)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(0.3)
        self.p0.factory.setLifespanSpread(0.05)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(180.0)
        self.p0.factory.enableAngularVelocity(0)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(0.7)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.04 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.04 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.005 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.005 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OOneMinusFbufferAlpha, ColorBlendAttrib.OOneMinusIncomingAlpha)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(1.0, 1.0, 1.0, 1.0), Vec4(0, 0, 0, 0.0), 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(-2.0)
        self.p0.emitter.setAmplitudeSpread(0.5)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 1.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        return

    def loadGlow(self):
        if not self.glow and self.wantGlow:
            self.glow = loader.loadModelCopy('models/effects/flareGlow')
            self.glow.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
            self.glow.setDepthWrite(0)
            self.glow.setFogOff()
            self.glow.setLightOff()
            self.glow.setBin('fixed', 120)
            self.glow.setColorScale(0.125, 0.125, 0.125, 0.125)
            self.glow.reparentTo(self)
            self.glow.setBillboardPointEye()
            self.glow.setR(25)

    def startPulseTrack(self):
        if self.glow and self.wantGlow:
            self.pulseTrack.loop()

    def stopPulseTrack(self):
        if self.glow and self.wantGlow:
            self.pulseTrack.finish()

    def createTrack(self):
        if self.wantGlow:
            self.loadGlow()
            randomness = random.random() / 20
            scaleUp = self.glow.scaleInterval(0.05, 15, startScale=17, blendType='easeInOut')
            scaleDown = self.glow.scaleInterval(0.05, 17, startScale=15, blendType='easeInOut')
            self.pulseTrack = Sequence(scaleUp, scaleDown)
        else:
            if self.glow:
                self.glow.removeNode()
                self.glow = None
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.01), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self), Func(self.startPulseTrack))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 2.0), Wait(1.5), Func(self.stopPulseTrack), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(6.0), self.endEffect)
        return

    def cleanUpEffect(self):
        self.stopPulseTrack()
        EffectController.cleanUpEffect(self)
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        if self.glow:
            self.glow.removeNode()
            self.glow = None
        EffectController.destroy(self)
        PooledEffect.destroy(self)
        return
# okay decompiling .\pirates\effects\FireTrail.pyc
