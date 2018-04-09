# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.battle.RangeDetector
from pandac.PandaModules import *
from pirates.battle import WeaponGlobals


class RangeDetector(NodePath):
    

    def __init__(self):
        NodePath.__init__(self, 'rangeDetector')
        self.spheres = []
        for radius in WeaponGlobals.Ranges:
            sphere = CollisionSphere(0, 0, 0, 1.0)
            sphere.setTangible(0)
            sphereNode = CollisionNode('rangeDetector-%s' % radius)
            sphereNode.addSolid(sphere)
            sphereNodePath = self.attachNewNode(sphereNode)
            self.spheres.append(sphereNodePath)
# okay decompiling .\pirates\battle\RangeDetector.pyc
