# Embedded file name: pirates.effects.QuestIndicatorEffect
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from PooledEffect import PooledEffect
from EffectController import EffectController
import os

class QuestIndicatorEffect(PooledEffect, EffectController):
    cardScale = 16.0
    cardScale2 = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/skyBeam')
        self.card = model.find('**/*')
        self.wantBottomEffect = 1
        self.particleDummy = render.attachNewNode(ModelNode('QuestIndicatorParticleDummy'))
        self.particleDummy.setDepthWrite(0)
        self.particleDummy.setLightOff()
        self.particleDummy.setFogOff()
        self.particleDummy.setColorScaleOff()
        self.f = ParticleEffect.ParticleEffect('QuestIndicatorEffect')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('BoxEmitter')
        self.f.addParticles(self.p0)
        self.f2 = ParticleEffect.ParticleEffect('QuestIndicatorEffect2')
        self.f2.reparentTo(self)
        self.p1 = Particles.Particles('particles-2')
        self.p1.setFactory('ZSpinParticleFactory')
        self.p1.setRenderer('SpriteParticleRenderer')
        self.p1.setEmitter('DiscEmitter')
        self.f2.addParticles(self.p1)
        self.p0.setPoolSize(24)
        self.p0.setBirthRate(0.1)
        self.p0.setLitterSize(2)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(1.0)
        self.p0.factory.setLifespanSpread(0.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(0.5)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setInitialXScale(0.2 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.03 * self.cardScale)
        self.p0.renderer.setInitialYScale(7.0 * self.cardScale)
        self.p0.renderer.setFinalYScale(3.0 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(15.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(0.5)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setMinBound(Point3(-2.5, -5.0, 0.0))
        self.p0.emitter.setMaxBound(Point3(2.5, 5.0, 0.0))
        self.f2.setPos(Vec3(0, 0, -5))
        self.p1.setPoolSize(128)
        self.p1.setBirthRate(0.03)
        self.p1.setLitterSize(8)
        self.p1.setLitterSpread(0)
        self.p1.setSystemLifespan(0.0)
        self.p1.setLocalVelocityFlag(1)
        self.p1.setSystemGrowsOlderFlag(0)
        self.p1.factory.setLifespanBase(1.0)
        self.p1.factory.setLifespanSpread(0.5)
        self.p1.factory.setMassBase(1.0)
        self.p1.factory.setMassSpread(0.0)
        self.p1.factory.setTerminalVelocityBase(400.0)
        self.p1.factory.setTerminalVelocitySpread(0.0)
        self.p1.factory.setInitialAngle(0.0)
        self.p1.factory.setInitialAngleSpread(25.0)
        self.p1.factory.enableAngularVelocity(1)
        self.p1.factory.setAngularVelocity(0.0)
        self.p1.factory.setAngularVelocitySpread(0.0)
        self.p1.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p1.renderer.setUserAlpha(0.5)
        self.p1.renderer.setFromNode(self.card)
        self.p1.renderer.setColor(Vec4(1, 1, 1, 1))
        self.p1.renderer.setXScaleFlag(1)
        self.p1.renderer.setYScaleFlag(1)
        self.p1.renderer.setAnimAngleFlag(1)
        self.p1.renderer.setInitialXScale(0.012 * self.cardScale2)
        self.p1.renderer.setFinalXScale(0.015 * self.cardScale2)
        self.p1.renderer.setInitialYScale(0.075 * self.cardScale2)
        self.p1.renderer.setFinalYScale(0.025 * self.cardScale2)
        self.p1.renderer.setNonanimatedTheta(0.0)
        self.p1.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p1.renderer.setAlphaDisable(0)
        self.p1.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p1.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p1.emitter.setAmplitude(0.0)
        self.p1.emitter.setAmplitudeSpread(0.0)
        self.p1.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p1.emitter.setExplicitLaunchVector(Vec3(0.0, 0.0, 0.0))
        self.p1.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p1.emitter.setRadius(8.0)
        self.adjustIval = None
        self.effectScale = 1
        return

    def createTrack(self):
        if self.wantBottomEffect:
            self.p1.setLitterSize(8)
        else:
            self.p1.setLitterSize(0)
        self.startEffect = Sequence(Func(self.p0.clearToInitial), Func(self.p0.softStart), Func(self.f.start, self, self.particleDummy), Func(self.p1.clearToInitial), Func(self.p1.softStart), Func(self.f2.start, self, self.particleDummy), Func(self.startAdjustTask), Func(self.particleDummy.hide), Func(self.hide), Wait(0.01), Func(self.particleDummy.show), Func(self.show))
        self.endEffect = Sequence(Func(self.p0.softStop), Func(self.p1.softStop), Wait(2.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(2.5), self.endEffect)

    def startLoop(self, pos=Point3(0), pdPos=Point3()):
        EffectController.startLoop(self)
        self.particleDummy.hide()
        self.hide()
        self.setPos(pos)
        self.particleDummy.setPos(pdPos)

    def startAdjustTask(self):
        self.stopAdjustTask()
        task = taskMgr.doMethodLater(1, self.adjustTask, 'questIndicatorEffect-adjust')
        self.adjustTask(task, force=True)

    def adjustTask(self, task, force=False):
        if base.localAvatar and not base.localAvatar.isEmpty():
            distance = self.getDistance(localAvatar)
            newFEScale = Vec3(0.25 * (1 + distance / 50)) * self.effectScale
            newPDScale = Vec3(0.75 * (1 + distance / 50)) * self.effectScale
            if self.adjustIval:
                self.adjustIval.pause()
                self.adjustIval = None
            if not force:
                self.adjustIval = Parallel(self.scaleInterval(1, newFEScale), self.particleDummy.scaleInterval(1, newPDScale))
                self.adjustIval.start()
            else:
                self.p0.clearToInitial()
                self.setScale(newFEScale)
                self.particleDummy.setScale(newPDScale)
        return task.again

    def stopAdjustTask(self):
        taskMgr.remove('questIndicatorEffect-adjust')
        if self.adjustIval:
            self.adjustIval.pause()
            self.adjustIval = None
        return

    def setEffectScale(self, scale):
        self.effectScale = scale

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.stopAdjustTask()
        if self.pool and self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        self.stopAdjustTask()
        EffectController.destroy(self)
        PooledEffect.destroy(self)
        self.adjustIval = None
        return

    def showEffect(self):
        self.particleDummy.unstash()

    def hideEffect(self):
        self.particleDummy.stash()

    def setWantBottomEffect(self, want):
        self.wantBottomEffect = want