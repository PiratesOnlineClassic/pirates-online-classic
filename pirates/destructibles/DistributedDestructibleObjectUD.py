from direct.distributed.DistributedNodeUD import DistributedNodeUD
from direct.directnotify import DirectNotifyGlobal

class DistributedDestructibleObjectUD(DistributedNodeUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDestructibleObjectUD')

    def __init__(self, air):
        DistributedNodeUD.__init__(self, air)