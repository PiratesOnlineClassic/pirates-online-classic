from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedBowSpritUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBowSpritUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)