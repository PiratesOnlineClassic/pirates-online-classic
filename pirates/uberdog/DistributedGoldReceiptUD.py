
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class DistributedGoldReceiptUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGoldReceiptUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)


    # setGoldPaid(uint16) db

    # setExpirationDate(uint32) db


