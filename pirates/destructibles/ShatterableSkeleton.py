# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.destructibles.ShatterableSkeleton
from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from pirates.effects.ProjectileArc import ProjectileArc
from pirates.destructibles import ShatterableObject
import random

class ShatterableSkeleton(ShatterableObject.ShatterableObject, NodePath):
    __module__ = __name__

    def __init__(self):
        ShatterableObject.ShatterableObject.__init__(self)
        NodePath.__init__(self, 'shatterableSkeletonRenderParent')
        self.prop = loader.loadModelCopy('models/char/ghost_pirate_destruct')
        self.prop.reparentTo(self)
        self.initializeDebris(wantHidden=0, wantColl=0, bounce=0)

    def delete(self):
        ShatterableObject.ShatterableObject.delete(self)
        self.prop.removeNode()
        del self.prop
        self.removeNode()

    def breakMe(self, debrisNode):
        projDummy = ProjectileArc(self.wantRotate, self.wantColl)
        projDummy.reparentTo(self.prop)
        projDummy.startVel = Vec3(random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(20, 40))
        projDummy.gravityMult = 2.0
        projDummy.rotateMin = 90
        projDummy.rotateMax = 200
        if self.wantHidden:
            debrisNode.unstash()
        projDummy.transNode.setPos(render, debrisNode.getPos(render))
        projDummy.transNode.setHpr(render, debrisNode.getHpr(render))
        projDummy.transNode.setScale(render, debrisNode.getScale(render))
        projDummy.startPos = projDummy.transNode.getPos(render)
        debrisNode.reparentTo(projDummy.rotateNode)
        debrisNode.setPos(0, 0, 0)
        debrisNode.setHpr(0, 0, 0)
        debrisNode.setScale(1)
        projDummy.startPos = projDummy.transNode.getPos(render)
        debrisParent = self.getDebrisParent()
        projDummy.wrtReparentTo(render)
        shatterSeq = Sequence(Func(projDummy.play))
        self.intervals.append(shatterSeq)
        shatterSeq.start()
# okay decompiling .\pirates\destructibles\ShatterableSkeleton.pyc
