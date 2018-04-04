from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class TutorialShipAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TutorialShipAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)