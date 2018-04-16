import random

from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from pandac.PandaModules import *
from PooledEffect import PooledEffect

class ExplosionFlip(PooledEffect, EffectController):
    

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.speed = 20.0
        self.explosionSequence = 0
        self.explosion = loader.loadModelOnce('models/effects/explosion.bam')
        self.explosion.setBillboardPointWorld()
        self.explosion.setDepthWrite(0)
        self.explosion.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        self.explosion.setLightOff()
        self.explosion.setFogOff()
        self.explosion.setColorScaleOff()
        self.explosion.reparentTo(self)
        self.explosion.hide()

    def createTrack(self, rate=1):
        self.track = Sequence(Func(self.explosion.show), Wait(0.3), Func(self.explosion.hide), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)