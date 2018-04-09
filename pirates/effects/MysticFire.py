# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.MysticFire
import random

from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.particles import ForceGroup, ParticleEffect, Particles
from EffectController import EffectController
from pandac.PandaModules import *
from PooledEffect import PooledEffect


class MysticFire(PooledEffect, EffectController):
    
    cardScale = 64.0
    burningSfx = None

    def __init__(self, effectParent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if effectParent:
            self.reparentTo(effectParent)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleFire2')
        if not self.burningSfx:
            self.burningSfx = base.loader.loadSfx('audio/sfx_grenade_impact_firebomb_loop.mp3')
        if not MysticFire.particleDummy:
            MysticFire.particleDummy = render.attachNewNode(ModelNode('FireParticleDummy'))
            MysticFire.particleDummy.setDepthWrite(0)
            MysticFire.particleDummy.setFogOff()
            MysticFire.particleDummy.setLightOff()
            MysticFire.particleDummy.setColorScaleOff()
            MysticFire.particleDummy.setBin('fixed', 60)
        self.duration = 10.0
        self.effectScale = 1.0
        self.f = ParticleEffect.ParticleEffect()
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(64)
        self.p0.setBirthRate(0.01)
        self.p0.setLitterSize(3)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.setFloorZ(-1.0)
        self.p0.factory.setLifespanBase(0.75)
        self.p0.factory.setLifespanSpread(0.25)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(360.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(350.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(0.75, 0.85, 0.3, 1.0), Vec4(0.4, 0.85, 0.3, 0.5), 1)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(-1)
        self.p0.emitter.setAmplitudeSpread(0.25)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 15.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))

    def createTrack(self, lod=None):
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setInitialXScale(0.05 * self.cardScale * self.effectScale)
        self.p0.renderer.setInitialYScale(0.05 * self.cardScale * self.effectScale)
        self.p0.renderer.setFinalXScale(0.03 * self.cardScale * self.effectScale)
        self.p0.renderer.setFinalYScale(0.045 * self.cardScale * self.effectScale)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 15.0 * self.effectScale))
        self.p0.emitter.setRadius(6.0 * self.effectScale)
        shrinkSize = LerpFunctionInterval(self.setNewSize, 2.5, toData=0.001, fromData=1.0)
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.01), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self))
        self.endEffect = Sequence(shrinkSize, Func(self.p0.setBirthRate, 100.0), Wait(2.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, SoundInterval(self.burningSfx, loop=1, duration=self.duration), self.endEffect)

    def setNewSize(self, time):
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 15.0 * self.effectScale * time))
        self.p0.renderer.setUserAlpha(1.0 * time)

    def setScale(self, scale=VBase3(1, 1, 1)):
        self.effectScale = scale[0]
        self.p0.renderer.setInitialXScale(0.05 * self.cardScale * self.effectScale)
        self.p0.renderer.setInitialYScale(0.05 * self.cardScale * self.effectScale)
        self.p0.renderer.setFinalXScale(0.03 * self.cardScale * self.effectScale)
        self.p0.renderer.setFinalYScale(0.045 * self.cardScale * self.effectScale)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 15.0 * self.effectScale))
        self.p0.emitter.setRadius(6.0 * self.effectScale)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool and self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)
# okay decompiling .\pirates\effects\MysticFire.pyc
