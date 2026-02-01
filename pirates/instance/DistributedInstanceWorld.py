from pirates.instance.DistributedInstanceBase import DistributedInstanceBase
from panda3d.core import NodePath

class DistributedInstanceWorld(DistributedInstanceBase, NodePath):
    
    def __init__(self, cr):
        DistributedInstanceBase.__init__(self, cr)
        self.jailContext = None

    def delete(self):
        del self.jailContext
        DistributedInstanceBase.delete(self)
    
    def getInstanceNodePath(self):
        return self
    
    def localAvEnterDeath(self, av):
        DistributedInstanceBase.localAvEnterDeath(self, av)
        if av.isLocal():
            self.d_localAvatarDied()

    def localAvExitDeath(self, av):
        DistributedInstanceBase.localAvExitDeath(self, av)

