import random

from direct.interval.IntervalGlobal import *
from direct.particles import ForceGroup, ParticleEffect, Particles
from EffectController import EffectController
from pandac.PandaModules import *
from PooledEffect import PooledEffect

class CeilingDebris(PooledEffect, EffectController):
    __module__ = __name__
    cardScale = 128.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleRockShower')
        if not CeilingDebris.particleDummy:
            CeilingDebris.particleDummy = render.attachNewNode(ModelNode('CeilingDebrisParticleDummy'))
            CeilingDebris.particleDummy.setDepthWrite(0)
        self.f = ParticleEffect.ParticleEffect()
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1', 64)
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        f0 = ForceGroup.ForceGroup('Gravity')
        force0 = LinearVectorForce(Vec3(0.0, 0.0, -5.0), 2.0, 1)
        force0.setVectorMasks(1, 1, 1)
        force0.setActive(1)
        f0.addForce(force0)
        self.f.addForceGroup(f0)
        self.p0.setBirthRate(0.02)
        self.p0.setLitterSize(100)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(3.0)
        self.p0.factory.setLifespanSpread(2.5)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.2)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAUSER)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(0.3, 0.2, 0, 1))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.015 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.015 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.01 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.01 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(0.2, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(100.0)

    def createTrack(self):
        self.track = Sequence(Func(self.p0.setBirthRate, 0.02), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self), Wait(0.2), Func(self.p0.setBirthRate, 100), Wait(7.0), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)