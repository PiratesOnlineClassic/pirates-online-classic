from panda3d.core import *
from direct.showbase import Pool
from direct.showbase.DirectObject import DirectObject

class PooledEffect(DirectObject, NodePath):
    pool = None
    poolLimit = 124

    @classmethod
    def getEffect(self):
        if self.pool is None:
            self.pool = Pool.Pool()
        
        if self.pool.hasFree():
            return self.pool.checkout()
        else:
            (free, used) = self.pool.getNumItems()
            if free + used < self.poolLimit:
                self.pool.add(self())
                return self.pool.checkout()
            else:
                return None

    @classmethod
    def cleanup(self):
        if self.pool:
            self.pool.cleanup(self.destroy)
            self.pool = None
    
    def __init__(self):
        NodePath.__init__(self, self.__class__.__name__)
        self.accept('clientLogout', self.__class__.cleanup)
    
    def destroy(self, item = None):
        if item:
            self.pool.remove(item)
        
        self.ignore('clientLogout')
        self.removeNode()


