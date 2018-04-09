# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.EnergySpiral
import random

from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from pandac.PandaModules import *
from PooledEffect import PooledEffect


class EnergySpiral(PooledEffect, EffectController):
    __module__ = __name__

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectModel = loader.loadModelCopy('models/effects/energy_spirals')
        self.effectModel2 = loader.loadModelCopy('models/effects/energy_spirals')
        self.effectModel2.reparentTo(self.effectModel)
        self.effectModel.setBillboardAxis(0)
        self.effectModel.setColorScaleOff()
        self.effectModel.reparentTo(self)
        self.effectColor = Vec4(1, 1, 1, 1)
        self.setDepthWrite(0)
        self.setLightOff()
        self.setColorScaleOff()
        self.setTransparency(0, 0)

    def createTrack(self):
        textureStage = self.effectModel.findAllTextureStages()[0]
        self.effectModel.setTexOffset(textureStage, 0.0, 1.0)
        self.effectModel.setScale(0.4, 0.5, 0.5)
        duration = 6.0
        self.setColorScale(1.0, 1.0, 1.0, 0.0)
        fadeIn = LerpColorScaleInterval(self, 1.0, Vec4(1.0, 1.0, 1.0, 1.0), startColorScale=Vec4(0.0, 0.0, 0.0, 0.0))
        fadeOut = LerpColorScaleInterval(self, 1.0, Vec4(0.0, 0.0, 0.0, 0.0), startColorScale=Vec4(1.0, 1.0, 1.0, 1.0))
        scaleIval = LerpScaleInterval(self.effectModel, duration, Vec3(1.0, 1.0, 4.0), startScale=Vec3(1.0, 1.0, 4.0))
        uvScroll = LerpFunctionInterval(self.setNewUVs, duration / 4.0, toData=-1.0, fromData=1.0, extraArgs=[self.effectModel, textureStage])
        self.startEffect = Sequence(Func(uvScroll.loop), fadeIn)
        self.endEffect = Sequence(fadeOut, Func(uvScroll.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(duration), self.endEffect)

    def setEffectColor(self, color):
        self.effectColor = Vec4(1, 1, 1, 1) - (Vec4(1, 1, 1, 1) - color) / 4.0 + Vec4(0.1, 0.1, 0, 1)
        self.effectModel.setColorScale(self.effectColor)

    def setNewUVs(self, offset, part, ts):
        part.setTexOffset(ts, 0.0, offset)

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
# okay decompiling .\pirates\effects\EnergySpiral.pyc
