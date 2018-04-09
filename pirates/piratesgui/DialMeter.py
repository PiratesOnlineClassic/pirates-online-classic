# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.DialMeter
from direct.gui.DirectGui import *
from pandac.PandaModules import *


class DialMeter(DirectFrame):
    __module__ = __name__
    MeterFull = None
    MeterHalf = None

    def __init__(self, parent, **kw):
        optiondefs = (
         (
          'state', DGG.DISABLED, None), ('relief', None, None), ('meterColor', VBase4(0, 0, 0, 1), None), ('baseColor', VBase4(1, 1, 1, 1), None), ('wantCover', True, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        self.initialiseoptions(DialMeter)
        if self.MeterFull == None:
            card = loader.loadModelCopy('models/textureCards/dialmeter')
            self.MeterFull = card.find('**/dialmeter_full')
            self.MeterHalf = card.find('**/dialmeter_half')
        self.meterFace = self.MeterFull.copyTo(self)
        self.meterFace.setTransparency(1)
        self.meterFace.setScale(1.15)
        self.meterFace.flattenStrong()
        self.meterFace.setColor(self['baseColor'])
        self.meterFaceHalf1 = self.MeterHalf.copyTo(self)
        self.meterFaceHalf1.setTransparency(1)
        self.meterFaceHalf1.setScale(1.07)
        self.meterFaceHalf1.flattenStrong()
        self.meterFaceHalf1.setColor(self['meterColor'])
        self.meterFaceHalf2 = self.MeterHalf.copyTo(self)
        self.meterFaceHalf2.setTransparency(1)
        self.meterFaceHalf2.setScale(1.07)
        self.meterFaceHalf2.flattenStrong()
        self.meterFaceHalf2.setColor(self['baseColor'])
        if self['wantCover']:
            cover = self.MeterFull.copyTo(self)
            cover.setColor(self['baseColor'])
            cover.setTransparency(1)
            cover.setScale(0.87)
            cover.flattenStrong()
        return

    def update(self, val, max):
        progress = 0
        if max > 0:
            progress = float(val) / max
        if progress <= 0.25:
            meterColor = Vec4(0.8, 0.0, 0.0, 1.0)
        else:
            meterColor = self['meterColor']
        self.meterFaceHalf1.clearColorScale()
        self.meterFaceHalf2.clearColorScale()
        if progress == 0:
            self.meterFaceHalf1.hide()
            self.meterFaceHalf2.hide()
            self.meterFace.setColor(self['baseColor'])
        else:
            if progress == 1:
                self.meterFaceHalf1.hide()
                self.meterFaceHalf2.hide()
                self.meterFace.setColor(meterColor)
            else:
                self.meterFaceHalf1.show()
                self.meterFaceHalf2.show()
                self.meterFace.setColor(self['baseColor'])
                if progress < 0.5:
                    self.meterFaceHalf1.setColor(meterColor)
                    self.meterFaceHalf2.setColor(self['baseColor'])
                else:
                    self.meterFaceHalf1.setColor(meterColor)
                    self.meterFaceHalf2.setColor(meterColor)
                    progress = progress - 0.5
                self.meterFaceHalf2.setR(-180 * (progress / 0.5))
# okay decompiling .\pirates\piratesgui\DialMeter.pyc
