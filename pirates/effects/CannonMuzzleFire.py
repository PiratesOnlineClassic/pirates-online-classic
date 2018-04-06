# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.CannonMuzzleFire
import random

from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.particles import ForceGroup, ParticleEffect, Particles
from .EffectController import EffectController
from pandac.PandaModules import *
from .PooledEffect import PooledEffect


class CannonMuzzleFire(PooledEffect, EffectController):
    __module__ = __name__

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.splash = Actor.Actor()
        self.splash.loadModel('models/effects/cannonMuzzleFlash-zero')
        animDict = {}
        animDict['splashdown'] = 'models/effects/cannonMuzzleFlash-anim'
        self.splash.loadAnims(animDict)
        self.splash.reparentTo(self)
        self.splash.setTransparency(1)
        self.splash.setDepthWrite(0)
        self.splash.setColorScaleOff()
        self.splash.setLightOff()
        self.splash.setFogOff()

    def createTrack(self, rate=1):
        self.splash.setPlayRate(rate, 'splashdown')
        animDuration = self.splash.getDuration('splashdown') * 0.3
        fadeOut = self.splash.colorInterval(0.6, Vec4(1, 1, 1, 0), startColor=Vec4(1, 1, 1, 1))
        self.track = Sequence(Func(self.splash.setColor, 1, 1, 1, 1), Func(self.splash.play, 'splashdown'), Wait(animDuration), fadeOut, Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        self.detachNode()
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        self.stop()
        self.splash.cleanup()
        del self.splash
        EffectController.destroy(self)
        PooledEffect.destroy(self)
# okay decompiling .\pirates\effects\CannonMuzzleFire.pyc
