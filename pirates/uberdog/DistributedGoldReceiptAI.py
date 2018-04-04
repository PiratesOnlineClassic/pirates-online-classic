
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedGoldReceiptAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGoldReceiptAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # setGoldPaid(uint16) db

    # setExpirationDate(uint32) db


