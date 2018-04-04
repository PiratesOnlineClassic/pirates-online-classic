from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class BlackPearlShipAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('BlackPearlShipAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)