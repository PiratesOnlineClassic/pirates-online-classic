
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class DistributedFlagShopUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFlagShopUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)



