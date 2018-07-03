from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class DistributedShipUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
