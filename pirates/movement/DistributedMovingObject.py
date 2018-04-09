# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.movement.DistributedMovingObject
import random

from direct.distributed import DistributedSmoothNode
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from direct.task.Task import Task
from otp.movement import Mover
from pirates.battle import EnemyGlobals
from pirates.demo import DemoGlobals
from pirates.distributed import DistributedTargetableObject
from pirates.piratesbase import PiratesGlobals


class DistributedMovingObject(DistributedSmoothNode.DistributedSmoothNode, DistributedTargetableObject.DistributedTargetableObject):
    
    notify = directNotify.newCategory('DistributedMovingObject')

    def __init__(self, cr):
        DistributedSmoothNode.DistributedSmoothNode.__init__(self, cr)
        DistributedTargetableObject.DistributedTargetableObject.__init__(self, cr)
        self.maxAISpeed = 0
        self.canMove = True
        self.aggroMode = EnemyGlobals.AGGRO_MODE_FORCED
        self.debugName = None
        self.debugNameNP = None
        return

    def requestGameState(self, state):
        pass

    def generate(self):
        DistributedSmoothNode.DistributedSmoothNode.generate(self)
        DistributedTargetableObject.DistributedTargetableObject.generate(self)
        if base.config.GetBool('create-client-coll-spheres', 0) is 1:
            self.setupDebugCollisions()

    def announceGenerate(self):
        DistributedSmoothNode.DistributedSmoothNode.announceGenerate(self)
        DistributedTargetableObject.DistributedTargetableObject.announceGenerate(self)

    def disable(self):
        self.stopSmooth()
        DistributedSmoothNode.DistributedSmoothNode.disable(self)
        DistributedTargetableObject.DistributedTargetableObject.disable(self)
        if base.config.GetBool('create-client-coll-spheres', 0) is 1:
            self.cleanupDebugcollisions()
        base.cr.handleObjDelete(self)

    def delete(self):
        DistributedSmoothNode.DistributedSmoothNode.delete(self)
        DistributedTargetableObject.DistributedTargetableObject.delete(self)

    def setLocation(self, parentId, zoneId, teleport=0):
        DistributedSmoothNode.DistributedSmoothNode.setLocation(self, parentId, zoneId, teleport)

    def wrtReparentTo(self, parent):
        DistributedSmoothNode.DistributedSmoothNode.wrtReparentTo(self, parent)

    def setupDebugCollisions(self):
        pass

    def cleanupDebugcollisions(self):
        pass

    def setMaxSpeed(self, speed):
        self.maxAISpeed = speed

    def getMaxSpeed(self):
        return self.maxAISpeed

    def wantsSmoothing(self):
        return 1

    def setMyPosHpr(self, x, y, z, h, p, r):
        self.setPosHpr(x, y, z, h, p, r)

    def showDebugName(self):
        if __debug__ and base.config.GetBool('move-obj-nametags', 0) is 1:
            if self.debugNameNP:
                self.debugNameNP.removeNode()
            else:
                self.debugName = TextNode('NPCName')
                self.debugName.setAlign(TextNode.ACenter)
                self.debugName.setTextColor(0, 0, 0, 1)
            debugNameText = str(self.getDoId()) + ' (Team:' + str(self.getTeam()) + ')'
            if hasattr(self, 'level'):
                debugNameText += ' (Lvl: ' + str(self.level) + ')'
            self.debugName.setText(debugNameText)
            self.debugNameNP = self.attachNewNode(self.debugName.generate())
            posAndScale = self.getDebugNamePosScale()
            self.debugNameNP.setPos(*posAndScale[0])
            self.debugNameNP.setScale(posAndScale[1])
            self.debugNameNP.setBillboardPointEye(2)
            CullBinManager.getGlobalPtr().addBin('gui-popup', CullBinManager.BTUnsorted, 60)
            self.debugNameNP.setBin('gui-popup', 0)
            self.debugNameNP.setDepthTest(0)

    def getDebugNamePosScale(self):
        return [
         (0, 0, 10), 2.0]

    def setStartState(self, startState):
        self.startState = startState

    def setAggroRadius(self, val):
        self.aggroRadius = val

    def getAggroRadius(self):
        return self.aggroRadius

    def setAggroMode(self, val):
        self.aggroMode = val

    def getAggroMode(self):
        return self.aggroMode
# okay decompiling .\pirates\movement\DistributedMovingObject.pyc
