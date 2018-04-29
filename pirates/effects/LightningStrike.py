# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.LightningStrike
import random

from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from pirates.effects.EffectController import EffectController
from panda3d.core import *
from pirates.piratesbase import PiratesGlobals
from pirates.effects.PooledEffect import PooledEffect


class LightningStrike(PooledEffect, EffectController):
    
    soundFx = []
    soundFxNames = ('thunderclap.mp3', 'thunder-start.mp3')

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if not self.soundFx:
            for filename in self.soundFxNames:
                self.soundFx.append(loader.loadSfx('audio/' + filename))

        self.fadeTime = 0.14
        self.waitTime = 0.2
        self.startScale = 1.0
        self.endScale = 1.01
        self.fadeColor = Vec4(1.0, 1.0, 1.0, 1.0)
        self.flashDummy = self.attachNewNode('FlashDummy')
        self.flashDummy.setBillboardPointEye()
        self.flashDummy.setDepthWrite(0)
        self.flashDummy.setColorScaleOff()
        self.flashDummy.setFogOff()
        self.flashDummy.setLightOff()
        self.flashDummy.reparentTo(self)
        self.flashDummy.setScale(self.startScale)
        self.flashDummy.hide()
        self.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.flasha = loader.loadModelCopy('models/effects/lightning_strike')
        self.flasha.reparentTo(self.flashDummy)
        self.flashb = loader.loadModelCopy('models/effects/lightning_strike')
        self.flashb.reparentTo(self.flasha)

    def createTrack(self):
        self.flashDummy.setScale(self.startScale)
        self.flashDummy.setColorScale(1, 1, 1, 1)
        if random.choice((1, 10)) > 5:
            self.flasha.setH(random.uniform(-60.0, 60.0))
        else:
            self.flasha.setH(random.uniform(120.0, 240.0))
        fadeOut = self.flashDummy.colorScaleInterval(self.fadeTime, Vec4(0, 0, 0, 0), startColorScale=self.fadeColor)
        scaleBlast = self.flashDummy.scaleInterval(self.fadeTime * 2 + self.waitTime, self.endScale, startScale=self.startScale, blendType='easeOut')
        sfx = random.choice(self.soundFx)
        sfx.setVolume(1.0)
        self.track = Sequence(Func(self.flashDummy.show), Parallel(SoundInterval(sfx), Sequence(Wait(self.waitTime), fadeOut), scaleBlast), Func(self.flashDummy.hide), Func(self.flashDummy.setScale, 1.0), Func(self.flashDummy.setColorScale, Vec4(1, 1, 1, 1)), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)
# okay decompiling .\pirates\effects\LightningStrike.pyc
