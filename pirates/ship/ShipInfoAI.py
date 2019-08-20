from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class ShipInfoAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipInfoAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
