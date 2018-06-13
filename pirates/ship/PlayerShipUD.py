from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class PlayerShipUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayerShipUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
