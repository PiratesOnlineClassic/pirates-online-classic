# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.UsesEffectNode
from pandac.PandaModules import *


class UsesEffectNode(NodePath):
    

    def __init__(self, offset=3.0):
        self.billboardNode = self.attachNewNode('billboardNode')
        self.billboardNode.node().setEffect(BillboardEffect.make(Vec3(0, 0, 1), 0, 1, offset, NodePath(), Point3(0, 0, 0)))
        self.effectNode = self.billboardNode.attachNewNode('effectNode')

    def getEffectParent(self):
        return self.effectNode

    def resetEffectParent(self):
        self.billboardNode.reparentTo(self)

    def delete(self):
        self.effectNode.removeNode()
        self.billboardNode.removeNode()
        del self.effectNode
        del self.billboardNode
# okay decompiling .\pirates\effects\UsesEffectNode.pyc
