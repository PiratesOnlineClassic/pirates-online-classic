from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PlayerShipAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayerShipAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)