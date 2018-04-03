# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.WakeMist
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class WakeMist(PooledEffect, EffectController):
    __module__ = __name__
    cardScale = 64.0
    splashSfxNames = ('wtrsplash_1.mp3', 'wtrsplash_2.mp3', 'wtrsplash_3.mp3', 'wtrsplash_4.mp3')
    splashSfx = []

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleSplash')
        if not self.splashSfx:
            for filename in self.splashSfxNames:
                self.splashSfx.append(base.loadSfx('audio/' + filename))

        if not WakeMist.particleDummy:
            WakeMist.particleDummy = render.attachNewNode(ModelNode('WakeMistParticleDummy'))
            WakeMist.particleDummy.setDepthWrite(0)
        self.f = ParticleEffect.ParticleEffect()
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('LineEmitter')
        self.f.addParticles(self.p0)
        f0 = ForceGroup.ForceGroup('gravity')
        force0 = LinearVectorForce(Vec3(0.0, 0.0, -20.0), 1.0, 1)
        force0.setActive(1)
        f0.addForce(force0)
        self.f.addForceGroup(f0)

    def createTrack(self):
        self.p0.setPoolSize(16)
        self.p0.setBirthRate(0.15)
        self.p0.setLitterSize(6)
        self.p0.setLitterSpread(3)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.setFloorZ(-5.0)
        self.p0.factory.setLifespanBase(3.0)
        self.p0.factory.setLifespanSpread(1.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.95)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(180.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.06 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.22 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.06 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.22 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETCUSTOM)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 6.0, 20.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 1.0))
        self.p0.emitter.setEndpoint1(Point3(-10.0, 0.0, 0.0))
        self.p0.emitter.setEndpoint2(Point3(10.0, 0.0, 0.0))

    def createTrack(self, rate=1):
        sfx = random.choice(self.splashSfx)
        particleSpray = Sequence(Func(self.p0.setBirthRate, 0.15), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self), Wait(0.3), Func(self.p0.setBirthRate, 8), Wait(4.0), Func(self.cleanUpEffect))
        self.track = Parallel(particleSpray, Func(base.playSfx, sfx, node=self))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)
# okay decompiling .\pirates\effects\WakeMist.pyc
