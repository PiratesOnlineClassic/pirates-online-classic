# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.SkeletonGlow
import random

from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from pirates.effects.EffectController import EffectController
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.effects.PooledEffect import PooledEffect


class SkeletonGlow(PooledEffect, EffectController):

    def __init__(self, newParent=render, billboardOffset=0.0):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.newParent = newParent
        self.setColorScaleOff()
        self.setBillboardPointEye(billboardOffset)
        self.glowColor = Vec4(0.8, 0.8, 0.8, 1)
        self.pulseRate = 1.0
        self.glow = loader.loadModelCopy('models/effects/skeletonHeart')
        self.glow.setFogOff()
        self.glow.setLightOff()
        self.glow.setBin('fixed', 120)
        self.glow.setColorScaleOff()
        self.glow.reparentTo(self)
        self.glow.setScale(1.0)

    def createTracks(self):
        randomness = random.random() / 20
        pulseUp = self.glow.scaleInterval(0.03 + randomness, 2, startScale=1.3)
        pulseDown = self.glow.scaleInterval(
            0.03 + randomness, 1.3, startScale=2)
        fadeIn = self.glow.colorInterval(
            0.03 + randomness, Vec4(1, 1, 1, 1), startColor=self.glowColor)
        fadeOut = self.glow.colorInterval(
            0.03 + randomness, self.glowColor, startColor=Vec4(1, 1, 1, 1))
        self.track = Sequence(
            Wait(self.pulseRate), Parallel(fadeIn, pulseUp),
            Parallel(fadeOut, pulseDown))

    def adjustHeartColor(self, hpPercent):
        if hpPercent >= 1.0:
            self.glow.find('**/+SwitchNode').node().setVisibleChild(0)
            self.pulseRate = 1.0
        else:
            if hpPercent < 0.5:
                self.glow.find('**/+SwitchNode').node().setVisibleChild(1)
                self.pulseRate = 0.5
            else:
                if hpPercent < 0.25:
                    self.glow.find('**/+SwitchNode').node().setVisibleChild(2)
                    self.pulseRate = 0.1
        self.stop()
        self.createTracks()
        self.loop()

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)


# okay decompiling .\pirates\effects\SkeletonGlow.pyc
