from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedDestructibleObjectAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDestructibleObjectAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)