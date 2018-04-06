# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.DomeExplosion
import random

from direct.interval.IntervalGlobal import *
from .EffectController import EffectController
from pandac.PandaModules import *
from .PooledEffect import PooledEffect


class DomeExplosion(PooledEffect, EffectController):
    __module__ = __name__

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.speed = 0.75
        self.size = 40
        self.explosionSequence = 0
        self.explosion = loader.loadModelCopy('models/effects/explosion_sphere')
        self.explosion.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingColor, ColorBlendAttrib.OOneMinusIncomingAlpha))
        self.explosion.setFogOff()
        self.explosion.setLightOff()
        self.explosion.reparentTo(self)
        self.explosion.setDepthWrite(0)
        self.hide()

    def createTrack(self, rate=1):
        self.explosion.setScale(1)
        self.explosion.setColorScale(0, 0, 0, 0.65)
        fadeBlast = self.explosion.colorScaleInterval(self.speed * 0.5, Vec4(0, 0, 0, 0))
        waitFade = Sequence(Wait(self.speed * 0.5), fadeBlast)
        scaleUp = self.explosion.scaleInterval(self.speed, self.size, startScale=0.0, blendType='easeIn', other=render)
        self.track = Sequence(Func(self.show), Parallel(scaleUp, waitFade), Func(self.hide), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)
# okay decompiling .\pirates\effects\DomeExplosion.pyc
