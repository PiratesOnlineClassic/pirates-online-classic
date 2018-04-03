# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.FuryTrail
import random

from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.particles import ForceGroup, ParticleEffect, Particles
from EffectController import EffectController
from pandac.PandaModules import *
from PooledEffect import PooledEffect


class FuryTrail(PooledEffect, EffectController):
    __module__ = __name__
    faceCardScale = 64.0
    cardScale = 128.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.g = None
        self.p1 = None
        self.glow = None
        self.wantGlow = 1
        self.wantBlur = 1
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleGlowBlue')
        self.faceCard = model.find('**/effectFury')
        if not FuryTrail.particleDummy:
            FuryTrail.particleDummy = render.attachNewNode(ModelNode('FuryTrailParticleDummy'))
            FuryTrail.particleDummy.setDepthWrite(0)
            FuryTrail.particleDummy.setFogOff()
            FuryTrail.particleDummy.setLightOff()
            FuryTrail.particleDummy.setTwoSided(1)
        self.f = ParticleEffect.ParticleEffect()
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        f0 = ForceGroup.ForceGroup('noise')
        force0 = LinearNoiseForce(1.5, 1)
        force0.setActive(1)
        f0.addForce(force0)
        self.f.addForceGroup(f0)
        self.p0.setPoolSize(128)
        self.p0.setBirthRate(0.1)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(1.2)
        self.p0.factory.setLifespanSpread(0.5)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.2)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setInitialXScale(0.13 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.13 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.05 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.05 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(-2.0)
        self.p0.emitter.setAmplitudeSpread(0.5)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 10.0))
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(1.0)
        return

    def loadFaceBlur(self):
        if not self.g and self.wantBlur:
            self.g = ParticleEffect.ParticleEffect()
            self.g.reparentTo(self)
            self.p1 = Particles.Particles('particles-2')
            self.p1.setFactory('PointParticleFactory')
            self.p1.setRenderer('SpriteParticleRenderer')
            self.p1.setEmitter('SphereVolumeEmitter')
            self.g.addParticles(self.p1)
            self.p1.setPoolSize(128)
            self.p1.setBirthRate(0.01)
            self.p1.setLitterSize(1)
            self.p1.setLitterSpread(0)
            self.p1.setSystemLifespan(0.0)
            self.p1.setLocalVelocityFlag(1)
            self.p1.setSystemGrowsOlderFlag(0)
            self.p1.factory.setLifespanBase(0.5)
            self.p1.factory.setLifespanSpread(0)
            self.p1.factory.setMassBase(1.0)
            self.p1.factory.setMassSpread(0.0)
            self.p1.factory.setTerminalVelocityBase(400.0)
            self.p1.factory.setTerminalVelocitySpread(0.0)
            self.p1.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
            self.p1.renderer.setUserAlpha(1.0)
            self.p1.renderer.setFromNode(self.faceCard)
            self.p1.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
            self.p1.renderer.setXScaleFlag(1)
            self.p1.renderer.setYScaleFlag(1)
            self.p1.renderer.setAnimAngleFlag(0)
            self.p1.renderer.setInitialXScale(0.15 * self.faceCardScale)
            self.p1.renderer.setInitialYScale(0.15 * self.faceCardScale)
            self.p1.renderer.setFinalXScale(0.01 * self.faceCardScale)
            self.p1.renderer.setFinalYScale(0.01 * self.faceCardScale)
            self.p1.renderer.setNonanimatedTheta(0.0)
            self.p1.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
            self.p1.renderer.setAlphaDisable(0)
            self.p1.renderer.getColorInterpolationManager().addConstant(0.0, 1.0, Vec4(0.0, 0.0, 0.0, 1.0), 1)
            self.p1.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
            self.p1.emitter.setAmplitude(0.5)
            self.p1.emitter.setAmplitudeSpread(0.0)
            self.p1.emitter.setOffsetForce(Vec3(0.0, -100.0, 7.0))
            self.p1.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
            self.p1.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
            self.p1.emitter.setRadius(0.2)

    def loadGlow(self):
        if not self.glow and self.wantGlow:
            self.glow = loader.loadModelCopy('models/effects/furyEffect')
            self.glow.setDepthWrite(0)
            self.glow.setFogOff()
            self.glow.setLightOff()
            self.glow.setBin('fixed', 120)
            self.glow.setColorScale(1, 1, 1, 1)
            self.glow.reparentTo(self)
            self.glow.setBillboardPointEye()

    def startGlow(self):
        if self.glow and self.wantGlow:
            self.pulseTrack.loop()

    def stopGlow(self):
        if self.glow and self.wantGlow:
            self.pulseTrack.finish()

    def startBlur(self):
        if self.g and self.wantBlur:
            self.p1.setBirthRate(0.01)
            self.p1.clearToInitial()
            self.g.start(self, self)
            self.g.reparentTo(self)

    def stopBlur(self):
        if self.g:
            self.p1.setBirthRate(100.0)

    def createTrack(self):
        if self.wantGlow:
            self.loadGlow()
            randomness = random.random() / 20
            scaleUp = self.glow.scaleInterval(0.05, 7, startScale=9, blendType='easeInOut')
            scaleDown = self.glow.scaleInterval(0.05, 9, startScale=7, blendType='easeInOut')
            self.pulseTrack = Sequence(scaleUp, scaleDown)
        else:
            if self.glow:
                self.glow.removeNode()
                self.glow = None
        if self.wantBlur:
            self.loadFaceBlur()
        else:
            if self.g:
                self.g.disable()
                self.g.cleanup()
                self.g = None
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.01), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self), Func(self.startBlur), Func(self.startGlow))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 2.0), Func(self.stopBlur), Func(self.stopGlow), Wait(1.5), Func(self.cleanUpEffect))
        self.track = Parallel(self.startEffect, Wait(6.0), self.endEffect)
        return

    def cleanUpEffect(self):
        if self.g:
            self.g.disable()
        self.stopBlur()
        self.stopGlow()
        EffectController.cleanUpEffect(self)
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        if self.g:
            self.g.cleanup()
        if self.glow:
            self.glow.removeNode()
            self.glow = None
        self.g = None
        self.p1 = None
        EffectController.destroy(self)
        PooledEffect.destroy(self)
        return
# okay decompiling .\pirates\effects\FuryTrail.pyc
