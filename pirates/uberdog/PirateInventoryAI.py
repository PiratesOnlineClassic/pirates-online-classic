from pirates.uberdog.DistributedInventoryAI import DistributedInventoryAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType, InventoryCategory
from pirates.reputation import RepChart
from pirates.reputation import ReputationGlobals
from pirates.battle import WeaponGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.TreasureMapInventoryAI import TreasureMapInventoryAI
from pirates.uberdog import InventoryInit
from pirates.economy import EconomyGlobals
from pirates.piratesbase import FreebooterAI

class PirateInventoryAI(DistributedInventoryAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PirateInventoryAI')

    def __init__(self, air):
        DistributedInventoryAI.__init__(self, air)
        self.treasureMaps = TreasureMapInventoryAI(self)

    def delete(self):
        self.treasureMaps.close()
        DistributedInventoryAI.delete(self)

    def giveTreasureMap(self, mapId, callback):
        self.treasureMaps.give(mapId, callback)

    def setReputation(self, repType, quantity):
        avatar = self.air.doId2do.get(self.ownerId)
        if not avatar:
            return

        limit = InventoryInit.AccumulatorLimits.get(repType)
        if limit:
            quantity = min(quantity, limit)

        # a Freebooter stops earning reputation at the level caps...
        totalRep = self.getReputation(repType)
        quantity = FreebooterAI.capReputation(avatar, repType, totalRep, quantity)
        if quantity == totalRep:
            return

        currentLevel, currentReputation = ReputationGlobals.getLevelFromTotalReputation(repType, totalRep)
        newLevel, newReputation = ReputationGlobals.getLevelFromTotalReputation(repType, quantity)

        # update the accumulator before announcing any level ups, the client
        # reads the new reputation when showing the level up text...
        self.b_setAccumulator(repType, quantity)

        # a single reward may be large enough to earn several levels at once,
        # each level is rewarded individually...
        for level in range(currentLevel + 1, newLevel + 1):
            self.handleLevelUp(avatar, repType, level)

    def handleLevelUp(self, avatar, repType, level):
        # check to see if the type of reputation we're giving the avatar is
        # their overall reputation/level, then set their level...
        if repType == InventoryType.OverallRep:
            avatar.b_setLevel(level)

            # Assign level up quests...
            for questId in RepChart.getLevelUpQuest(repType, level):
                if not self.air.questMgr.hasQuest(avatar, questId=questId):
                    self.air.questMgr.createQuest(avatar, questId)
        else:
            # Give level up skills, the first list holds the skill points
            # earned and the second the skills unlocked at this level...
            skills = RepChart.getLevelUpSkills(repType, level)
            for unspent in skills[0]:
                self.b_setStackQuantity(unspent, self.getStackQuantity(unspent) + 1)

            for earnedSkill in skills[1]:
                if InventoryType.begin_Unspent <= earnedSkill < InventoryType.end_Unspent:
                    continue

                if not self.getStackQuantity(earnedSkill):
                    self.b_setStackQuantity(earnedSkill, 1)

            for skillId in RepChart.getLevelUpSkills(repType, 0)[1] + RepChart.getLevelUpSkills(repType, 1)[1]:
                if not self.getStackQuantity(skillId):
                    self.b_setStackQuantity(skillId, 1)

            # Give weapon level up quests, these check the inventory
            # for the prerequisite weapon...
            for questId in RepChart.getWeaponLevelUpQuest(repType, level, self):
                if not self.air.questMgr.hasQuest(avatar, questId=questId):
                    self.air.questMgr.createQuest(avatar, questId)

        # every reputation category raises the avatar's max hp and mojo,
        # see GuiManager.showLevelUpText...
        maxHp = avatar.getMaxHp() + RepChart.getHpGain(repType)
        maxMojo = avatar.getMaxMojo() + RepChart.getManaGain(repType)
        avatar.b_setMaxHp(maxHp)
        avatar.b_setMaxMojo(maxMojo)

        # the client derives the local avatar's max hp and mojo from these
        # stack limits, see DistributedInventory.stackLimit...
        self.b_setStackLimit(InventoryType.Hp, maxHp)
        self.b_setStackLimit(InventoryType.Mojo, maxMojo)

        if repType == InventoryType.OverallRep:
            avatar.b_setHp(maxHp)
            avatar.b_setMojo(maxMojo)

        avatar.d_levelUpMsg(repType, level, 0)

    def getReputation(self, repType):
        return self.getAccumulator(repType)

    def updateStackLimits(self):
        # inventories are only given the stack limits known when they were
        # created, give older inventories any limits added since. The client
        # will not let the avatar train a skill that has no stack limit...
        stackLimits = dict(self.stackLimits)
        for stackType, limit in list(InventoryInit.StackLimits.items()):
            stackLimits.setdefault(stackType, limit)

        # the ammo pouches owned raise the limits of the ammo they carry...
        for pouchId in InventoryInit.AmmoPouches:
            if not self.getStackQuantity(pouchId):
                continue

            ammoList = EconomyGlobals.getPouchAmmoList(EconomyGlobals.getItemType(pouchId)) or []
            for ammoId, limit in zip(ammoList, EconomyGlobals.getInventoryBonus(pouchId) or []):
                stackLimits[ammoId] = max(stackLimits.get(ammoId, 0), limit)

        if stackLimits == self.stackLimits:
            return

        self.b_setStackLimits(list(stackLimits.items()))

    def updateSkillUnlocks(self):
        # make sure every skill unlocked by the avatar's weapon levels has
        # been given, the client only shows unlocked skills on the skill page...
        for repType in ReputationGlobals.getReputationCategories():
            level, _ = ReputationGlobals.getLevelFromTotalReputation(repType, self.getReputation(repType))
            for unlockLevel in range(level + 1):
                for skillId in RepChart.getLevelUpSkills(repType, unlockLevel)[1]:
                    if InventoryType.begin_Unspent <= skillId < InventoryType.end_Unspent:
                        continue

                    if not self.getStackQuantity(skillId):
                        self.b_setStackQuantity(skillId, 1)

    def setOverallRep(self, quantity):
        self.setReputation(InventoryType.OverallRep, quantity)

    def getOverallRep(self):
        return self.getReputation(InventoryType.OverallRep)

    def setGeneralRep(self, quantity):
        self.setReputation(InventoryType.GeneralRep, quantity)

    def getGeneralRep(self):
        return self.getReputation(InventoryType.GeneralRep)

    def setGoldInPocket(self, quantity):
        # the gold carried is capped by it's stack limit, see InventoryInit...
        self.b_setStackQuantity(InventoryType.GoldInPocket, max(0, quantity))

    def addGoldInPocket(self, quantity):
        newsManager = self.air.newsManager
        if newsManager.isHolidayActive(PiratesGlobals.DOUBLEGOLDHOLIDAY):
            quantity *= 2
        
        avatar = self.air.doId2do.get(self.ownerId)
        if avatar:
            if newsManager.isHolidayActive(PiratesGlobals.DOUBLEGOLDHOLIDAYPAID) and avatar.isPaid():
                quantity *= 2

        quantity += self.getGoldInPocket() 
        self.setGoldInPocket(quantity)

    def setVitaeLevel(self, quantity):
        self.b_setStackQuantity(InventoryType.Vitae_Level, quantity)

    def getVitaeLevel(self):
        return self.getStackQuantity(InventoryType.Vitae_Level)

    def setVitaeLeft(self, quantity):
        self.b_setStackQuantity(InventoryType.Vitae_Left, quantity)

    def getVitaeLeft(self):
        return self.getStackQuantity(InventoryType.Vitae_Left)

    def giveCards(self, cardId, amount):
        avatar = self.air.doId2do.get(self.ownerId)
        if not avatar:
            return

        # cardId is the card's InventoryType, which is also what the
        # client expects to receive in it's card loot message...
        avatar.giveCardMessage(cardId)
        self.b_setStackQuantity(cardId, self.getStackQuantity(cardId) + amount)

    def giveCollectionItem(self, itemId, amount=1):
        avatar = self.air.doId2do.get(self.ownerId)
        if not avatar:
            return

        # itemId is the collection item's InventoryType, the client looks
        # up the item's rarity and value from it, see LootPopupPanel.showLoot...
        self.b_setStackQuantity(itemId, self.getStackQuantity(itemId) + amount)
        avatar.d_sendLootMessage(itemId)

    def setShipDoIdList(self, shipList):
        return self.b_setDoIdListCategory(InventoryCategory.SHIPS, shipList)

    def setQuestList(self, questList):
        self.b_setDoIdListCategory(InventoryCategory.QUESTS, questList)

    def populateInventory(self):
        avatar = self.air.doId2do.get(self.ownerId)
        if not avatar:
            self.notify.warning('Failed to populate inventory %d, '
                'for non-existant AI owner object: %d' % (self.doId, self.ownerId))

            return

        # populate the avatar's quest list
        self.air.questMgr.activateQuests(avatar)
        self.treasureMaps.activateAll()

        # populate the avatar's ship doId list
        shipDoIdList = self.getShipDoIdList()
        for shipId in shipDoIdList:
            self.air.shipLoader.activateShip(avatar, shipId)

        DistributedInventoryAI.populateInventory(self)
