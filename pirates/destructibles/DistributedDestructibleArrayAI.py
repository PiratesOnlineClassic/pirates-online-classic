from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedDestructibleArrayAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDestructibleArrayAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)