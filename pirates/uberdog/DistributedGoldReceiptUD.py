from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal


class DistributedGoldReceiptUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGoldReceiptUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
        self.goldPaid = 0
        self.expirationDate = 0

    def setGoldPaid(self, goldPaid):
        self.goldPaid = goldPaid

    def getGoldPaid(self):
        return self.goldPaid

    def setExpirationDate(self, expirationDate):
        self.expirationDate = expirationDate

    def getExpirationDate(self):
        return self.expirationDate

