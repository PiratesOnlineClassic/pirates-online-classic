# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.FadingSigil
import random

from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from EffectController import EffectController
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from PooledEffect import PooledEffect


class FadingSigil(PooledEffect, EffectController):
    __module__ = __name__

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.fadeTime = 1.0
        self.waitTime = 1.0
        self.startScale = 6.0
        self.endScale = 7.0
        self.fadeColor = Vec4(1.0, 1.0, 1.0, 1.0)
        self.flashDummy = self.attachNewNode('FlashDummy')
        self.flashDummy.setBillboardPointEye(1.0)
        self.flashDummy.reparentTo(self)
        self.flashDummy.hide()
        self.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.flash = loader.loadModelCopy('models/effects/sigils')
        self.flash.setDepthWrite(0)
        self.flash.setColorScaleOff()
        self.flash.setFogOff()
        self.flash.setLightOff()
        self.flash.setScale(self.startScale)
        self.flash.reparentTo(self.flashDummy)

    def createTrack(self):
        self.flash.setScale(1)
        self.flash.setColorScale(1, 1, 1, 1)
        fadeIn = self.flash.colorScaleInterval(self.fadeTime, self.fadeColor, startColorScale=Vec4(0, 0, 0, 0))
        fadeOut = self.flash.colorScaleInterval(self.fadeTime, Vec4(0, 0, 0, 0), startColorScale=self.fadeColor)
        mover = self.flash.posInterval(self.fadeTime * 2 + self.waitTime, Vec3(0, 0, 1.0))
        scaleBlast = self.flash.scaleInterval(self.fadeTime * 2 + self.waitTime, self.endScale, startScale=self.startScale, blendType='easeOut')
        self.track = Sequence(Func(self.flashDummy.show), Parallel(Sequence(fadeIn, Wait(self.waitTime), fadeOut), scaleBlast, mover), Func(self.flashDummy.hide), Func(self.flash.setScale, 1.0), Func(self.flash.setColorScale, Vec4(1, 1, 1, 1)), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)
# okay decompiling .\pirates\effects\FadingSigil.pyc
