from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedDestructibleObjectUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDestructibleObjectUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)