from direct.distributed import DistributedSmoothNode
from direct.fsm import FSM
from panda3d.core import NodePath
from direct.showbase.ShowBaseGlobal import *

class DistributedFormation(DistributedSmoothNode.DistributedSmoothNode, FSM.FSM):
    
    def __init__(self, cr):
        DistributedSmoothNode.DistributedSmoothNode.__init__(self, cr)
        FSM.FSM.__init__(self, 'DistributedFormation')
        node = render.attachNewNode('formationNode')
        NodePath.__init__(self, node)
        self.cSphere = None
        self.cSphereNode = None
    
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

    def setRadius(self, radius):
        if self.cSphere:
            self.cSphere.setRadius(radius)
        


