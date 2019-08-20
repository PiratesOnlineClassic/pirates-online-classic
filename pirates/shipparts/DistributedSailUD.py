from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal


class DistributedSailUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSailUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
