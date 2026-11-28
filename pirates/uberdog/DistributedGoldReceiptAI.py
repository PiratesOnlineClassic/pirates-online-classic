import time

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class DistributedGoldReceiptAI(DistributedObjectAI):
    """
    A database backed record of gold an avatar has paid for something that
    expires. The receipt keeps how much was paid and when the purchase runs out.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGoldReceiptAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.goldPaid = 0
        self.expirationDate = 0

    def setGoldPaid(self, goldPaid):
        self.goldPaid = goldPaid

    def d_setGoldPaid(self, goldPaid):
        self.sendUpdate('setGoldPaid', [goldPaid])

    def b_setGoldPaid(self, goldPaid):
        self.setGoldPaid(goldPaid)
        self.d_setGoldPaid(goldPaid)

    def getGoldPaid(self):
        return self.goldPaid

    def setExpirationDate(self, expirationDate):
        self.expirationDate = expirationDate

    def d_setExpirationDate(self, expirationDate):
        self.sendUpdate('setExpirationDate', [expirationDate])

    def b_setExpirationDate(self, expirationDate):
        self.setExpirationDate(expirationDate)
        self.d_setExpirationDate(expirationDate)

    def getExpirationDate(self):
        return self.expirationDate

    def isExpired(self, now=None):
        if not self.expirationDate:
            return False

        if now is None:
            now = int(time.time())

        return now >= self.expirationDate

    def getTimeRemaining(self, now=None):
        if not self.expirationDate:
            return 0

        if now is None:
            now = int(time.time())

        return max(0, self.expirationDate - now)
