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

OBJECT_EFFECTS = {
    'None': Defaults,
    'Ghost': Ghost_Effect}
