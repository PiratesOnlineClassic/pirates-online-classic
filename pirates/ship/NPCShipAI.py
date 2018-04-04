from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class NPCShipAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('NPCShipAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)