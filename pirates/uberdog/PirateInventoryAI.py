from pirates.uberdog.DistributedInventoryAI import DistributedInventoryAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType, InventoryCategory

class PirateInventoryAI(DistributedInventoryAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PirateInventoryAI')

    def setGeneralRep(self, quantity):
        self.b_setAccumulator(InventoryType.GeneralRep, quantity)

    def getGeneralRep(self):
        return self.getItem(self.getAccumulator, InventoryType.GeneralRep)

    def setGoldInPocket(self, quantity):
        self.b_setStack(InventoryType.GoldInPocket, quantity)

    def getGoldInPocket(self):
        return self.getItem(self.getStack, InventoryType.GoldInPocket)
