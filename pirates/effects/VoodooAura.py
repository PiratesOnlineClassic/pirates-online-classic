# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.VoodooAura
import random

from direct.interval.IntervalGlobal import *
from direct.particles import ForceGroup, ParticleEffect, Particles
from .EffectController import EffectController
from otp.otpbase import OTPRender
from pandac.PandaModules import *
from .PooledEffect import PooledEffect


class VoodooAura(PooledEffect, EffectController):
    __module__ = __name__
    cardScale = 128.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/battleEffects')
        self.card = model.find('**/effectVoodooShockwave')
        if not self.particleDummy:
            self.particleDummy = self.attachNewNode(ModelNode('VoodooAuraParticleDummy'))
            self.particleDummy.setDepthWrite(0)
            self.particleDummy.hide(OTPRender.ShadowCameraBitmask)
        self.effectColor = Vec4(1, 1, 1, 1)
        self.f = ParticleEffect.ParticleEffect()
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(64)
        self.p0.setBirthRate(0.02)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(0)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(1.0)
        self.p0.factory.setLifespanSpread(0.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(0.5)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setInitialXScale(0.005 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.012 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.005 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.012 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(0.0, 0.0, 0.0, 0.5), self.effectColor, 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(0.2)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(0.15)

    def createTrack(self, rate=1):
        self.castEffect = Sequence(Func(self.p0.emitter.setRadius, 0.75), Func(self.p0.renderer.setFinalXScale, 0.02 * self.cardScale), Func(self.p0.renderer.setFinalYScale, 0.02 * self.cardScale), Wait(2.0), Func(self.p0.emitter.setRadius, 0.15), Func(self.p0.renderer.setFinalXScale, 0.012 * self.cardScale), Func(self.p0.renderer.setFinalYScale, 0.012 * self.cardScale))
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.03), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100), Wait(7.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(1.0), self.endEffect)

    def pulseUp(self):
        self.p0.renderer.setInitialXScale(0.01 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.024 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.008 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.017 * self.cardScale)

    def pulseDown(self):
        self.p0.renderer.setInitialXScale(0.005 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.012 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.005 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.012 * self.cardScale)

    def setEffectColor(self, color):
        self.effectColor = color
        self.p0.renderer.getColorInterpolationManager().clearToInitial()
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(0.0, 0.0, 0.0, 0.5), self.effectColor, 1)

    def cleanUpEffect(self):
        self.f.disable()
        self.detachNode()
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)
# okay decompiling .\pirates\effects\VoodooAura.pyc
