from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup

class VolcanoSplats(NodePath):
    
    def __init__(self):
        NodePath.__init__(self, 'VolcanoSplats')
        self.renderParent = self.attachNewNode('VolcanoSplats-renderParent')
        self.renderParent.setScale(12)
        self.f = ParticleEffect.ParticleEffect('VolcanoSplats')
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.p0.setPoolSize(100)
        self.p0.setBirthRate(10000)
        self.p0.setLitterSize(5)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(4.0)
        self.p0.factory.setLifespanSpread(0.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(180.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(36.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAUSER)
        self.p0.renderer.setUserAlpha(0.35)
        self.p0.renderer.setTextureFromNode('models/effects/particleMaps', '**/particleVolcanoLava')
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(7.0)
        self.p0.renderer.setFinalXScale(15.0)
        self.p0.renderer.setInitialYScale(7.0)
        self.p0.renderer.setFinalYScale(15.0)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.55, 0.75, Vec4(1.0, 1.0, 1.0, 1.0), Vec4(1.0, 1.0, 1.0, 0.0))
        self.p0.renderer.getColorInterpolationManager().addConstant(0.75, 1.0, Vec4(1.0, 1.0, 1.0, 0.0))
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 50.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(120.0)
        self.f.addParticles(self.p0)
        self.f0 = ForceGroup.ForceGroup('volcano')
        self.force0 = LinearVectorForce(Vec3(0.0, 0.0, -20.0), 2.0, 0)
        self.force0.setVectorMasks(0, 0, 1)
        self.force0.setActive(1)
        self.f0.addForce(self.force0)
        self.force1 = LinearJitterForce(10.0, 0)
        self.force1.setVectorMasks(1, 1, 1)
        self.force1.setActive(1)
        self.f0.addForce(self.force1)
        self.f.addForceGroup(self.f0)
        self.seq = None

    def enable(self):
        self.f.start(self, self.renderParent)

    def disable(self):
        self.f.disable()
        if self.seq:
            self.seq.finish()

    def getRenderParent(self):
        return self.renderParent

    def destroy(self):
        self.disable()
        self.f.cleanup()
        del self.f
        self.renderParent.removeNode()
        del self.renderParent
        del self.seq
        self.removeNode()

    def setParticleScale(self, scale):
        self.p0.renderer.setInitialXScale(7.0 * scale)
        self.p0.renderer.setFinalXScale(15.0 * scale)
        self.p0.renderer.setInitialYScale(7.0 * scale)
        self.p0.renderer.setFinalYScale(15.0 * scale)
        self.p0.emitter.setRadius(120 * scale)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 60.0 * (6 - 1 / scale) / 5))

    def getEruptionSeq(self):
        if not self.seq:
            self.seq = Sequence(Func(self.p0.setBirthRate, 0.2), Func(self.p0.clearToInitial), Wait(3), Func(self.p0.setBirthRate, 10000))
        
        return self.seq

    def isEnabled(self):
        return self.f.isEnabled()


