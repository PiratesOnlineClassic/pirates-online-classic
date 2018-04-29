from direct.interval.IntervalGlobal import *
from pirates.effects.EffectController import EffectController
from panda3d.core import *
from pirates.effects.PooledEffect import PooledEffect

class Glow(PooledEffect, EffectController):
    

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModelCopy('models/effects/particleCards')
        self.spark = model.find('**/particleSparkle')
        self.glow = model.find('**/particleWhiteGlow')
        self.effectModel = self.attachNewNode('effectModelNode')
        self.spark.reparentTo(self.effectModel)
        self.glow.reparentTo(self.effectModel)
        self.effectColor = Vec4(1, 1, 1, 1)
        self.effectModel.hide()
        self.effectModel.setDepthWrite(0)
        self.effectModel.setBillboardPointWorld()
        self.effectModel.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))

    def createTrack(self):
        self.effectModel.hide()
        self.glow.setScale(1.0)
        self.spark.setScale(1.0)
        self.setColorScale(1, 1, 1, 1)
        self.effectModel.setColorScale(self.effectColor)
        flash = LerpScaleInterval(self.glow, 0.15, 1.0, startScale=50.0)
        fadeOut = LerpColorScaleInterval(self, 0.25, Vec4(0, 0, 0, 0), startColorScale=Vec4(1, 1, 1, 1))
        scaleUp = self.spark.scaleInterval(0.3, 1.2, startScale=1.0, blendType='easeOut')
        scaleDown = self.spark.scaleInterval(0.4, 1.0, startScale=1.2, blendType='easeInOut')
        colorUp = self.glow.colorScaleInterval(0.3, Vec4(1, 1, 1, 1), startColorScale=Vec4(1, 1, 1, 0.75), blendType='easeOut')
        colorDown = self.glow.colorScaleInterval(0.4, Vec4(1, 1, 1, 0.75), startColorScale=Vec4(1, 1, 1, 1), blendType='easeInOut')
        pulseIval = Sequence(Parallel(scaleUp, colorUp), Parallel(scaleDown, colorDown))
        self.startEffect = Sequence(Func(self.effectModel.show), Func(self.glow.setColorScale, Vec4(1, 1, 1, 0.15)), flash, Func(pulseIval.loop))
        self.endEffect = Sequence(fadeOut, Func(pulseIval.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(1.0), self.endEffect)

    def cleanUpEffect(self):
        self.effectModel.hide()
        EffectController.cleanUpEffect(self)
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)