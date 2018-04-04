from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class AvatarAccessoriesManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('AvatarAccessoriesManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)