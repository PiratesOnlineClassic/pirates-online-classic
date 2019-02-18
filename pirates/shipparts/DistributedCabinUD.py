from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal


class DistributedCabinUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCabinUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
