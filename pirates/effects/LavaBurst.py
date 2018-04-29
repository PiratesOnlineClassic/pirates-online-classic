# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.LavaBurst
import random

from direct.interval.IntervalGlobal import *
from direct.particles import ForceGroup, ParticleEffect, Particles
from pirates.effects.EffectController import EffectController
from panda3d.core import *
from pirates.effects.PooledEffect import PooledEffect


class LavaBurst(PooledEffect, EffectController):
    
    cardScale = 64.0

    def __init__(self, parent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if parent is not None:
            self.reparentTo(parent)
        self.setDepthWrite(0)
        self.setLightOff()
        self.setFogOff()
        self.f = ParticleEffect.ParticleEffect()
        self.f.reparentTo(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleGlowFire')
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereSurfaceEmitter')
        self.f.addParticles(self.p0)
        return

    def createTrack(self, lod=None):
        self.p0.setPoolSize(16)
        self.p0.setBirthRate(1.0)
        self.p0.setLitterSize(4)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(1.5)
        self.p0.factory.setLifespanSpread(0.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setInitialXScale(0.085 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.001 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.065 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.001 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingColor, ColorBlendAttrib.OOne)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 0.3, Vec4(1.0, 1.0, 1.0, 0.0), Vec4(1.0, 1.0, 1.0, 1.0), 1)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.6, 1.0, Vec4(1.0, 1.0, 1.0, 1.0), Vec4(1.0, 0.25, 0.25, 0.0), 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 3.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(1.0)
        self.effectBirthRate = 4.0 * random.random() + 1.5
        self.loopEffect = Sequence(Wait(self.effectBirthRate), Func(self.randomizeEffect))
        self.startEffect = Sequence(Func(self.p0.setBirthRate, self.effectBirthRate), Func(self.p0.clearToInitial), Func(self.f.start, self, self), Func(self.f.reparentTo, self), Func(self.loopEffect.loop))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 0.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(2.0), self.endEffect)

    def randomizeEffect(self):
        randomX = -10.0 + 20.0 * random.random()
        randomY = -10.0 + 20.0 * random.random()
        randomZ = -2.75 + 1.0 * random.random()
        randomM = random.random()
        self.f.setPos(randomX, randomY, randomZ + randomM)
        self.p0.emitter.setRadius(0.1 + 3.0 * randomM)
        self.p0.factory.setLifespanBase(1.5 + randomM / 2.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 3.0 - 2.5 * randomM))

    def cleanUpEffect(self):
        self.loopEffect.finish()
        EffectController.cleanUpEffect(self)
        if self.pool and self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        self.loopEffect.finish()
        EffectController.destroy(self)
        PooledEffect.destroy(self)
# okay decompiling .\pirates\effects\LavaBurst.pyc
