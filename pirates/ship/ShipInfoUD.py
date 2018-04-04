from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class ShipInfoUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipInfoUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)