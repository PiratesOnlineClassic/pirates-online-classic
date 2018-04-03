# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.VolcanoSmoke
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup

class VolcanoSmoke(NodePath):
    __module__ = __name__

    def __init__(self):
        NodePath.__init__(self, 'VolcanoSmoke')
        self.renderParent = self.attachNewNode('VolcanoSmoke-renderParent')
        self.renderParent.setScale(80)
        self.f = ParticleEffect.ParticleEffect()
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.p0.setPoolSize(100)
        self.p0.setBirthRate(2)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(90.0)
        self.p0.factory.setLifespanSpread(10.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(180.0)
        self.p0.factory.setFinalAngle(0.0)
        self.p0.factory.setFinalAngleSpread(720.0)
        self.p0.factory.enableAngularVelocity(0)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAUSER)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setTextureFromNode('models/effects/particleMaps', '**/particleVolcanoSmoke')
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(1.5)
        self.p0.renderer.setFinalXScale(8.0)
        self.p0.renderer.setInitialYScale(1.5)
        self.p0.renderer.setFinalYScale(8.0)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 0.35, Vec4(1, 0.5, 0.25, 1), Vec4(0.0, 0.0, 0.0, 1.0))
        self.p0.renderer.getColorInterpolationManager().addConstant(0.35, 1.0, Vec4(0.0, 0.0, 0.0, 1.0))
        self.p0.renderer.getColorInterpolationManager().addLinear(0.5, 0.85, Vec4(1.0, 1.0, 1.0, 1.0), Vec4(1.0, 1.0, 1.0, 0.0))
        self.p0.renderer.getColorInterpolationManager().addConstant(0.85, 1.0, Vec4(1.0, 1.0, 1.0, 0.0))
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETEXPLICIT)
        self.p0.emitter.setAmplitude(0.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(0.0, 0.0, 2.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(1.0)
        self.f.addParticles(self.p0)
        self.f0 = ForceGroup.ForceGroup('volcano')
        self.force0 = LinearJitterForce(0.075, 0)
        self.force0.setVectorMasks(1, 1, 0)
        self.force0.setActive(1)
        self.f0.addForce(self.force0)
        self.force1 = LinearSourceForce(Point3(0.0, 0.0, 0.0), LinearDistanceForce.FTONEOVERRSQUARED, 1.125, 1.0, 0)
        self.force1.setVectorMasks(1, 1, 0)
        self.force1.setAmplitude(0.005)
        self.force1.setActive(0)
        self.f0.addForce(self.force1)
        self.force2 = LinearVectorForce(Vec3(0.0, -0.75, 3.0), 1.0, 0)
        self.force2.setVectorMasks(1, 1, 1)
        self.force2.setAmplitude(0.0042)
        self.force2.setActive(1)
        self.f0.addForce(self.force2)
        self.f.addForceGroup(self.f0)

    def enable(self):
        self.f.start(self, self.renderParent)

    def disable(self):
        self.f.disable()

    def getRenderParent(self):
        return self.renderParent

    def accelerate(self, time):
        self.p0.accelerate(time, 1, 0.05 * self.p0.getBirthRate())

    def destroy(self):
        self.disable()
        self.f.cleanup()
        del self.f
        self.renderParent.removeNode()
        del self.renderParent
        self.removeNode()

    def isEnabled(self):
        return self.f.isEnabled()
# okay decompiling .\pirates\effects\VolcanoSmoke.pyc
