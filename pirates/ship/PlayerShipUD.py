from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class PlayerShipUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayerShipUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)