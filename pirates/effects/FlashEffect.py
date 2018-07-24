from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from EffectController import EffectController
from pandac.PandaModules import *
from PooledEffect import PooledEffect


class FlashEffect(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.fadeTime = 0.15
        self.effectColor = Vec4(1, 1, 1, 1)
        model = loader.loadModelCopy('models/effects/particleCards')
        self.effectModel = model.find('**/particleWhiteGlow')
        self.effectModel.setBillboardAxis(0)
        self.effectModel.reparentTo(self)
        self.effectModel.setColorScale(0, 0, 0, 0)
        self.effectModel.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.setDepthWrite(0)
        self.setFogOff()

    def createTrack(self):
        fadeBlast = self.effectModel.colorScaleInterval(self.fadeTime, Vec4(0, 0, 0, 0), startColorScale=Vec4(self.effectColor), blendType='easeOut')
        scaleBlast = self.effectModel.scaleInterval(self.fadeTime, 10, startScale=1.0, blendType='easeIn')
        self.track = Sequence(Parallel(fadeBlast, scaleBlast), Func(self.cleanUpEffect))

    def setEffectColor(self, color):
        self.effectColor = color

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)
