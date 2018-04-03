# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.ObjectEffects
from pandac.PandaModules import *

def Defaults(objectNode):
    objectNode.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MNone))
    objectNode.setColorScale(1.0, 1.0, 1.0, 1.0)
    objectNode.setTransparency(0, 1)
    objectNode.setDepthWrite(1)
    objectNode.clearLight()


def Ghost_Effect(objectNode):
    objectNode.setTransparency(1, 1)
    objectNode.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
    objectNode.setColorScale(0.15, 0.3, 0.05, 0.55)
    objectNode.setDepthWrite(0)
    objectNode.setLightOff()


OBJECT_EFFECTS = {'None': Defaults, 'Ghost': Ghost_Effect}
# okay decompiling .\pirates\effects\ObjectEffects.pyc
