from pirates.uberdog.DistributedInventoryAI import DistributedInventoryAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType, InventoryCategory
from pirates.reputation import ReputationGlobals
from pirates.battle import WeaponGlobals

class PirateInventoryAI(DistributedInventoryAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PirateInventoryAI')

    def setReputation(self, repType, quantity):
        avatar = self.air.doId2do.get(self.ownerId)

        if not avatar:
            return

        oldLevel, oldReputation = ReputationGlobals.getLevelFromTotalReputation(
            repType, self.getReputation(repType))

        newLevel, newReputation = ReputationGlobals.getLevelFromTotalReputation(
            repType, quantity)

        # check to see if the type of reputation we're giving the avatar is
        # their overall reputation/level, then set their level...
        if repType == InventoryType.OverallRep and newLevel > avatar.getLevel():
            avatar.b_setLevel(newLevel)
            avatar.d_levelUpMsg(repType, avatar.getLevel(), 0)
        else:
            # only play the level up message for the avatar if their new reputation
            # is greater than their previous reputation...
            if newLevel > oldLevel:
                avatar.d_levelUpMsg(repType, newLevel, 0)

        self.b_setAccumulator(repType, quantity)

    def getReputation(self, repType):
        return self.getAccumulator(repType)

    def setOverallRep(self, quantity):
        self.setReputation(InventoryType.OverallRep, quantity)

        # since the client still makes use of the general reputation type,
        # let's just set the value as well...
        self.b_setAccumulator(InventoryType.GeneralRep, quantity)

    def getOverallRep(self):
        return self.getReputation(InventoryType.OverallRep)

    def setGoldInPocket(self, quantity):
        self.b_setStackQuantity(InventoryType.GoldInPocket, min(quantity, 65000))

    def setVitaeLevel(self, quantity):
        self.b_setStackQuantity(InventoryType.Vitae_Level, quantity)

    def getVitaeLevel(self):
        return self.getStackQuantity(InventoryType.Vitae_Level)

    def setVitaeLeft(self, quantity):
        self.b_setStackQuantity(InventoryType.Vitae_Left, quantity)

    def getVitaeLeft(self):
        return self.getStackQuantity(InventoryType.Vitae_Left)

    def setShipList(self, shipList):
        return self.b_setDoIdListCategory(InventoryCategory.SHIPS, shipList)

    def setQuestList(self, questList):
        self.b_setDoIdListCategory(InventoryCategory.QUESTS, questList)
