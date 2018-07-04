from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedCrewMatchAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCrewMatchAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
