from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal


class DistributedHullUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHullUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
