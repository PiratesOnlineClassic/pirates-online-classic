# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.CannonSplash
import random

from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.particles import ForceGroup, ParticleEffect, Particles
from .EffectController import EffectController
from pandac.PandaModules import *
from .PooledEffect import PooledEffect


class CannonSplash(PooledEffect, EffectController):
    __module__ = __name__
    cardScale = 64.0
    splashSfx = []
    particleDummy = None
    splashSfxNames = ('wtrsplash_1.mp3', 'wtrsplash_2.mp3', 'wtrsplash_3.mp3', 'wtrsplash_4.mp3',
                      'wtrsplash_5.mp3', 'wtrsplash_6.mp3', 'wtrsplash_7.mp3', 'wtrsplash_8.mp3')

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleSplash')
        if not CannonSplash.particleDummy:
            CannonSplash.particleDummy = render.attachNewNode(ModelNode('CannonSplashParticleDummy'))
            CannonSplash.particleDummy.setDepthWrite(0)
        if not self.splashSfx:
            for filename in self.splashSfxNames:
                self.splashSfx.append(loader.loadSfx('audio/' + filename))

        self.f = ParticleEffect.ParticleEffect()
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        f0 = ForceGroup.ForceGroup('gravity')
        force0 = LinearVectorForce(Vec3(0.0, 0.0, -40.0), 1.0, 1)
        force0.setActive(1)
        f0.addForce(force0)
        self.f.addForceGroup(f0)

    def createTrack(self):
        self.p0.setPoolSize(32)
        self.p0.setLitterSize(5)
        self.p0.setLitterSpread(2)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.setFloorZ(-8.0)
        self.p0.factory.setLifespanBase(3.0)
        self.p0.factory.setLifespanSpread(1.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.9)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(0.2)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.1 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.7 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.1 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.7 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETCUSTOM)
        self.p0.emitter.setAmplitude(2.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 40.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 1.0))
        self.p0.emitter.setRadius(1.0)
        self.p0.emitter.setOuterAngle(90.0)
        self.p0.emitter.setInnerAngle(0.0)
        self.p0.emitter.setOuterMagnitude(20.0)
        self.p0.emitter.setInnerMagnitude(0.0)
        self.p0.emitter.setCubicLerping(0)
        particleSpray = Sequence(Func(self.p0.setBirthRate, 0.05), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Wait(0.3), Func(self.p0.setBirthRate, 100), Wait(4.0))
        sfx = random.choice(self.splashSfx)
        sfx.setVolume(1.0)
        self.track = Sequence(Parallel(Func(base.playSfx, sfx, node=self, cutoff=1500), particleSpray), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)
# okay decompiling .\pirates\effects\CannonSplash.pyc
