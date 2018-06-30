from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class DistributedGAConnectorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedGAConnectorAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
