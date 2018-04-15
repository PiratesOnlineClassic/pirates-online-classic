import random

from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from EffectController import EffectController
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals

class CandleFlame(EffectController, NodePath):
    __module__ = __name__

    def __init__(self, newParent=render, billboardOffset=1.0):
        NodePath.__init__(self, 'CandleFlame')
        EffectController.__init__(self)
        self.newParent = newParent
        self.setColorScaleOff()
        self.setBillboardPointEye(billboardOffset)
        self.haloTrack = None
        self.glow = loader.loadModelCopy('models/effects/candleFlame')
        self.glow.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.glow.setDepthWrite(0)
        self.glow.setFogOff()
        self.glow.setLightOff()
        self.glow.setBin('fixed', 120)
        self.glow.setColorScale(1.0, 1.0, 1.0, 1)
        self.glow.setPos(0, 0, 0.15)
        self.glow.reparentTo(self)
        self.glowHalo = loader.loadModelCopy('models/effects/candleHalo')
        self.glowHalo.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.glowHalo.setDepthWrite(0)
        self.glowHalo.setFogOff()
        self.glowHalo.setLightOff()
        self.glowHalo.setBin('fixed', 120)
        self.glowHalo.setColorScale(1.0, 1.0, 1.0, 1)
        self.glowHalo.setPos(0, 0, 0.15)
        self.glowHalo.reparentTo(self)

    def createTrack(self):
        baseScale = Vec3(1.1, 1.1, 1.1)
        endScale = Vec3(1.0, 1.0, 1.4)
        randomness1 = random.random() / 10
        randomness2 = random.random() / 10
        randomness3 = random.random() / 10
        scaleUp1 = self.glow.scaleInterval(0.1 + randomness1, endScale, startScale=baseScale, blendType='easeInOut')
        scaleDown1 = self.glow.scaleInterval(0.1 + randomness1, baseScale, startScale=endScale, blendType='easeInOut')
        scaleUp2 = self.glow.scaleInterval(0.1 + randomness2, endScale, startScale=baseScale, blendType='easeInOut')
        scaleDown2 = self.glow.scaleInterval(0.1 + randomness2, baseScale, startScale=endScale, blendType='easeInOut')
        scaleUp3 = self.glow.scaleInterval(0.1 + randomness3, endScale, startScale=baseScale, blendType='easeInOut')
        scaleDown3 = self.glow.scaleInterval(0.1 + randomness3, baseScale, startScale=endScale, blendType='easeInOut')
        self.track = Sequence(scaleUp1, scaleDown1, scaleUp2, scaleDown2, scaleUp3, scaleDown3)
        randomness = random.random() / 20
        scaleUpHalo = self.glowHalo.scaleInterval(0.1 + randomness, 2.0, startScale=2.2, blendType='easeInOut')
        scaleDownHalo = self.glowHalo.scaleInterval(0.1 + randomness, 2.2, startScale=2.0, blendType='easeInOut')
        self.haloTrack = Sequence(scaleUpHalo, scaleDownHalo)
        self.reparentTo(self.newParent)

    def play(self, rate=1):
        EffectController.play(self)
        self.haloTrack.start()

    def startLoop(self, rate=1):
        self.createTrack()
        self.track.loop()
        self.haloTrack.loop()

    def stopLoop(self, rate=1):
        self.track.finish()
        self.haloTrack.finish()

    def stop(self):
        EffectController.stop(self)
        if self.haloTrack:
            self.haloTrack.finish()

    def destroy(self):
        EffectController.destroy(self)
        if self.haloTrack:
            self.haloTrack.finish()
            self.haloTrack = None