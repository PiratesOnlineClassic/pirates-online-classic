from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedDestructibleArrayUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDestructibleArrayUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)