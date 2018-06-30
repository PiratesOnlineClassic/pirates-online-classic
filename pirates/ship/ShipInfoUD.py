from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal


class ShipInfoUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipInfoUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
