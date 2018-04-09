# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.WispSpiral
import random

from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from EffectController import EffectController
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from PooledEffect import PooledEffect


class WispSpiral(PooledEffect, EffectController):
    __module__ = __name__

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.numWisps = 6
        self.wisps = []
        self.setColorScaleOff()
        self.startCol = Vec4(1.0, 1.0, 1.0, 0.2)
        self.fadeTime = 4.0
        self.startScale = Vec3(1.0, 1.0, 0.1)
        self.endScale = Vec3(3.0, 3.0, 4.0)
        self.flashDummy = self.attachNewNode('FlashDummy')
        self.flashDummy.reparentTo(self)
        self.flashDummy.hide()
        self.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingColor, ColorBlendAttrib.OOneMinusIncomingAlpha))
        for i in range(self.numWisps):
            flash = loader.loadModelCopy('models/effects/wisp_cylinder')
            flash.setDepthWrite(0)
            flash.setFogOff()
            flash.setColorScaleOff()
            flash.setLightOff()
            flash.reparentTo(self.flashDummy)
            self.wisps.append(flash)

    def createTrack(self):
        animation = Parallel()
        for i in range(self.numWisps):
            fadeBlast = self.wisps[i].colorScaleInterval(self.fadeTime, Vec4(0.5, 0.5, 0.5, 0), startColorScale=self.startCol, blendType='easeOut')
            offset = random.uniform(0.0, 2.0)
            endScale = Vec3(self.endScale[0] * offset, self.endScale[1] * offset, self.endScale[2] * offset)
            scaleBlast = self.wisps[i].scaleInterval(self.fadeTime, endScale, startScale=self.startScale, blendType='easeOut')
            randVal = random.uniform(0.0, 360.0)
            rotateBlast = self.wisps[i].hprInterval(self.fadeTime, Vec3(450 + randVal, 0, 0), startHpr=Vec3(randVal, 0, 0))
            randtime = random.uniform(0.0, 0.5)
            anim = Sequence(Func(self.wisps[i].hide), Wait(randtime * i), Func(self.wisps[i].show), Parallel(fadeBlast, scaleBlast, rotateBlast), Func(self.wisps[i].hide), Func(self.wisps[i].setScale, 1.0), Func(self.wisps[i].setColorScale, Vec4(1, 1, 1, 1)))
            animation.append(anim)

        self.track = Sequence(Func(self.flashDummy.show), animation, Func(self.flashDummy.hide), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)
# okay decompiling .\pirates\effects\WispSpiral.pyc
