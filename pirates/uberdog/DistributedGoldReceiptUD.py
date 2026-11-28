from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal


class DistributedGoldReceiptUD(DistributedObjectUD):
    """
    UberDOG view of a gold receipt. Receipts live in the database next to the
    inventories; the UberDOG only needs to create them and read them back.
    """

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

    @staticmethod
    def createReceipt(air, goldPaid, expirationDate, callback=None):
        """
        Stores a new receipt in the database and calls back with its doId.
        """

        def handleCreate(doId):
            if not doId:
                DistributedGoldReceiptUD.notify.warning('Failed to create gold receipt!')

            if callback:
                callback(doId)

        air.dbInterface.createObject(
            air.dbId,
            air.dclassesByName['DistributedGoldReceiptUD'],
            fields={'setGoldPaid': (goldPaid,),
                    'setExpirationDate': (expirationDate,)},
            callback=handleCreate)
