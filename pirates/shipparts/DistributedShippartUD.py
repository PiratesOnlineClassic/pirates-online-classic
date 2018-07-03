from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal


class DistributedShippartUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShippartUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
