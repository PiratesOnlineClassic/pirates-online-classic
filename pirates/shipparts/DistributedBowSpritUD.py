from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal


class DistributedBowSpritUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBowSpritUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
