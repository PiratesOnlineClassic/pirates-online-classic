from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTravelAgentAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTravelAgentAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
