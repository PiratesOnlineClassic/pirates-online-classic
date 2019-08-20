from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.directnotify import DirectNotifyGlobal

class DistributedDestructibleObjectAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDestructibleObjectAI')

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)