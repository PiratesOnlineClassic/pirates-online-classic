# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.ship.DistributedFormation
from direct.distributed import DistributedSmoothNode
from direct.fsm import FSM
from direct.showbase.ShowBaseGlobal import *
from pandac.PandaModules import NodePath


class DistributedFormation(DistributedSmoothNode.DistributedSmoothNode, FSM.FSM):
    __module__ = __name__

    def __init__(self, cr):
        DistributedSmoothNode.DistributedSmoothNode.__init__(self, cr)
        FSM.FSM.__init__(self, 'DistributedFormation')
        node = render.attachNewNode('formationNode')
        NodePath.__init__(self, node)
        self.cSphere = None
        self.cSphereNode = None
        return

    def generate(self):
        DistributedSmoothNode.DistributedSmoothNode.generate(self)
        self.setupCollisions()

    def disable(self):
        DistributedSmoothNode.DistributedSmoothNode.disable(self)
        self.cleanupCollisions()
        self.stopSmooth()

    def setState(self, stateName, timeStamp):
        print('DistributedFormation.setState %s' % stateName)
        self.request(stateName)

    def enterAIPatrol(self):
        self.startSmooth()

    def exitAIPatrol(self):
        self.stopSmooth()

    def enterAIPathFollow(self):
        self.startSmooth()

    def exitAIPathFollow(self):
        self.stopSmooth()

    def setupCollisions(self):
        if base.config.GetBool('process-movingObj-collisions', 1) is 0:
            self.notify.debug('skipping setting up collision sphere for formation')
            return
        self.notify.debug('setting up collision sphere for formation')
        self.cSphere = CollisionSphere(0.0, 0.0, 0.0, ShipGlobals.FORMATION_AVOID_SPHERE_RADIUS)
        self.cSphere.setTangible(0)
        cSphereNode = CollisionNode(self.uniqueName('FormationSphere'))
        cSphereNode.addSolid(self.cSphere)
        self.cSphereNodePath = self.attachNewNode(cSphereNode)

    def cleanupCollisions(self):
        self.notify.debug('cleaning up collisions')
        if self.cSphereNodePath:
            self.cSphereNodePath.removeNode()
            del self.cSphereNodePath
            self.cSphereNodePath = None
        if self.cSphere:
            del self.cSphere
            self.cSphere = None
        taskMgr.remove('formationMove-%s' % self.doId)
        return

    def setRadius(self, radius):
        if self.cSphere:
            self.cSphere.setRadius(radius)
# okay decompiling .\pirates\ship\DistributedFormation.pyc
