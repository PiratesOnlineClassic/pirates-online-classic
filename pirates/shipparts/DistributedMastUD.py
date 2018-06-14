from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal


class DistributedMastUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMastUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
