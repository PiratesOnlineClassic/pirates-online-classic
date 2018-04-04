from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedSeaSerpentAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSeaSerpentAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)