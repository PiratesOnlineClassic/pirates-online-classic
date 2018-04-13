from pirates.uberdog.DistributedInventoryAI import DistributedInventoryAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType, InventoryCategory
from pirates.reputation import ReputationGlobals

class PirateInventoryAI(DistributedInventoryAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PirateInventoryAI')

    def setGeneralRep(self, quantity):
        avatar = self.air.doId2do.get(self.ownerId)

        if not avatar:
            self.notify.debug('Failed to set general rep for avatar %d, not found!' % (
                avatar.doId))

            return

        newLevel, newReputation = ReputationGlobals.getLevelFromTotalReputation(
            InventoryType.OverallRep, quantity)

        if newLevel > avatar.getLevel():
            avatar.d_levelUpMsg(InventoryType.OverallRep, avatar.getLevel(), 0)

        avatar.b_setLevel(newLevel)
        self.b_setAccumulator(InventoryType.GeneralRep, quantity)

    def getGeneralRep(self):
        return self.getItem(self.getAccumulator, InventoryType.GeneralRep)

    def setGoldInPocket(self, quantity):
        self.b_setStack(InventoryType.GoldInPocket, quantity)

    def getGoldInPocket(self):
        return self.getItem(self.getStack, InventoryType.GoldInPocket)
