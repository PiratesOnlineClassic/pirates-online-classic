# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.SoulFlay
import random

from direct.interval.IntervalGlobal import *
from pirates.effects.EffectController import EffectController
from pandac.PandaModules import *
from pirates.effects.PooledEffect import PooledEffect


class SoulFlay(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectModel = loader.loadModelCopy('models/effects/soulflay')
        self.effectModel2 = loader.loadModelCopy('models/effects/soulflay')
        self.effectModel2.reparentTo(self.effectModel)
        self.effectModel.node().setAttrib(
            ColorBlendAttrib.make(ColorBlendAttrib.MAdd,
                                  ColorBlendAttrib.OIncomingAlpha,
                                  ColorBlendAttrib.OOne))
        self.effectModel.reparentTo(self)
        self.effectModel.setDepthWrite(0)
        self.effectModel.setLightOff()
        self.effectModel.setColorScaleOff()
        self.effectModel.setBillboardAxis(0)
        self.effectColor = Vec4(1, 1, 1, 1)
        texture = self.effectModel.findAllTextures()[0]
        texture.setBorderColor(VBase4(0.0, 0.0, 0.0, 0.0))
        texture.setWrapU(Texture.WMBorderColor)
        texture.setWrapV(Texture.WMBorderColor)

    def createTrack(self):
        textureStage = self.effectModel.findAllTextureStages()[0]
        self.effectModel.setTexOffset(textureStage, 0.0, 1.5)
        self.effectModel.setScale(1.0, 1.0, 4.0)
        duration = 1.25
        posIval = LerpPosInterval(
            self.effectModel,
            duration / 2.5,
            Vec3(0.0, 0.0, 2.0),
            startPos=Vec3(0.0, 0.0, 0.0))
        scaleIval = LerpScaleInterval(
            self.effectModel,
            duration,
            Vec3(1.0, 1.0, 4.0),
            startScale=Vec3(1.0, 1.0, 4.0))
        uvScroll = LerpFunctionInterval(
            self.setNewUVs,
            duration,
            toData=-1.25,
            fromData=1.5,
            extraArgs=[self.effectModel, textureStage])
        self.startEffect = Sequence(uvScroll)
        self.endEffect = Sequence(Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(duration), self.endEffect)

    def setNewUVs(self, offset, part, ts):
        part.setTexOffset(ts, 0.0, offset)

    def setEffectColor(self, color):
        diff = Vec4(1, 1, 1, 1) - color
        self.effectColor = Vec4(1, 1, 1, 1) - diff / 4.0 + Vec4(0, 0, 0, 1.0)
        self.effectModel.setColorScale(self.effectColor)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        self.stop()
        if self.track:
            self.track = None
        self.removeNode()
        EffectController.destroy(self)
        PooledEffect.destroy(self)
        return


# okay decompiling .\pirates\effects\SoulFlay.pyc
