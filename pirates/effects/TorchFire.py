import random

from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.particles import ForceGroup, ParticleEffect, Particles
from pirates.effects.EffectController import EffectController
from panda3d.core import *
from pirates.piratesgui.GameOptions import Options

class TorchFire(EffectController, NodePath):
    
    cardScale = 64.0

    def __init__(self, newParent=None):
        NodePath.__init__(self, 'TorchFire')
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleFlame')
        if not TorchFire.particleDummy:
            TorchFire.particleDummy = render.attachNewNode(ModelNode('TorchFireParticleDummy'))
            TorchFire.particleDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
            TorchFire.particleDummy.setBin('fixed', 120)
            TorchFire.particleDummy.setDepthWrite(0)
            TorchFire.particleDummy.setLightOff()
            TorchFire.particleDummy.setFogOff()
        self.f = ParticleEffect.ParticleEffect()
        self.f.reparentTo(self)
        self.f.setPos(0, 0, 0.75)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        if newParent:
            self.reparentTo(newParent)
        self.p0.setPoolSize(8)
        self.p0.setBirthRate(0.06)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(0.35)
        self.p0.factory.setLifespanSpread(0.02)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.5)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setInitialXScale(0.014 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.002 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.024 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.002 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(0.15)
        self.p0.emitter.setAmplitudeSpread(0.3)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 6.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(0.2)

    def createTrack(self, lod=Options.SpecialEffectsHigh):
        poolsize = 4 + 2 * lod
        lifespan = 0.25 + 0.05 * lod
        self.p0.setPoolSize(poolsize)
        self.p0.factory.setLifespanBase(lifespan)
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.06), Func(self.setPoolSize, int(poolsize)), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(1.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(10.0), self.endEffect)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)

    def destroy(self):
        EffectController.destroy(self)
# okay decompiling .\pirates\effects\TorchFire.pyc
