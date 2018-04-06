# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.DarkPortal
import random

from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from pandac.PandaModules import *
from PooledEffect import PooledEffect


class DarkPortal(PooledEffect, EffectController):
    __module__ = __name__

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.speed = 0.75
        self.holdTime = 2.5
        self.size = 40
        self.explosionSequence = 0
        self.explosion = loader.loadModelCopy('models/effects/darkPortal')
        self.explosion.setDepthTest(0)
        self.explosion.setFogOff()
        self.explosion.setLightOff()
        self.explosion.setHpr(0, -90, 0)
        self.explosion.reparentTo(self)
        self.hide()
        self.explosion.setBin('shadow', 0)
        self.explosion.setTransparency(TransparencyAttrib.MAlpha)
        self.explosion.setDepthWrite(0)

    def createTrack(self, rate=1):
        self.explosion.setScale(1)
        self.explosion.setColorScale(1, 1, 1, 0.75)
        scaleUp = self.explosion.scaleInterval(self.speed, self.size, startScale=0.0, blendType='easeIn', other=render)
        scaleDown = self.explosion.scaleInterval(self.speed, 0.0, startScale=self.size, blendType='easeIn', other=render)
        self.track = Sequence(Func(self.show), scaleUp, Wait(self.holdTime), scaleDown, Func(self.hide), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)
# okay decompiling .\pirates\effects\DarkPortal.pyc
