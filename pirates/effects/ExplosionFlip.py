# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.ExplosionFlip
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class ExplosionFlip(PooledEffect, EffectController):
    __module__ = __name__

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
# okay decompiling .\pirates\effects\ExplosionFlip.pyc
