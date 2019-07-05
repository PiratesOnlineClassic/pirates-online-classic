from pirates.uberdog.DistributedInventoryAI import DistributedInventoryAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType, InventoryCategory
from pirates.reputation import RepChart
from pirates.reputation import ReputationGlobals
from pirates.battle import WeaponGlobals
from pirates.piratesbase import PiratesGlobals

class PirateInventoryAI(DistributedInventoryAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PirateInventoryAI')

    def setReputation(self, repType, quantity):
        avatar = self.air.doId2do.get(self.ownerId)
        if not avatar:
            return

        totalRep = self.getReputation(repType)
        currentLevel, currentReputation = ReputationGlobals.getLevelFromTotalReputation(repType, totalRep)
        newLevel, newReputation = ReputationGlobals.getLevelFromTotalReputation(repType, quantity)

        if newLevel > currentLevel:
            # check to see if the type of reputation we're giving the avatar is
            # their overall reputation/level, then set their level...
            if repType == InventoryType.OverallRep:
                avatar.b_setLevel(newLevel)
                avatar.d_levelUpMsg(repType, avatar.getLevel(), 0)

                # Assign level up quests...
                try:
                    level_up_quests = RepChart.getLevelUpQuest(repType, newLevel)[0]
                    if not self.air.questMgr.hasQuest(level_up_quests):
                        self.air.questMgr.createQuest(avatar, level_up_quests)
                except IndexError:
                    self.notify.debug('Failed to give level up quest for %s(Level: %s); '
                        'They\'re not the proper level!' % (avatar.getName(), newLevel))

                avatar.b_setHp(avatar.getMaxHp())
                avatar.b_setMojo(avatar.getMaxMojo())
            else:
                avatar.d_levelUpMsg(repType, newLevel, 0)

                # Give level up skills
                earnedUnspent, earnedSkill = RepChart.getLevelUpSkills(repType, newLevel)
                for unspent in earnedUnspent:
                    self.b_setStackQuantity(unspent, 1)

                for earnedSkill in earnedSkill:
                    self.b_setStackQuantity(earnedSkill, 1)

                for unspent in RepChart.getLevelUpSkills(repType, 0)[1] + RepChart.getLevelUpSkills(repType, 1)[1]:
                    if not self.getStackQuantity(unspent):
                        self.b_setStackQuantity(unspent, 1)

                # Give weapon level up quests...
                try:
                    weapon_quests = RepChart.getWeaponLevelUpQuest(repType, newLevel, avatar)[0]
                    if not self.air.questMgr.hasQuest(weapon_quests):
                        self.air.questMgr.createQuest(avatar, weapon_quests)
                except IndexError:
                    self.notify.debug('Failed to give weapon level up quest for %s(Level: %s); '
                        'They\'re not the proper level!' % (avatar.getName(), newLevel))

                maxMojo = avatar.getMaxMojo()
                maxMojo += RepChart.getManaGain(repType)

                maxHp = avatar.getMaxHp()
                maxHp += RepChart.getHpGain(repType)

                avatar.b_setMaxHp(maxHp)
                avatar.b_setMaxMojo(maxMojo)

        self.b_setAccumulator(repType, quantity)

    def getReputation(self, repType):
        return self.getAccumulator(repType)

    def setOverallRep(self, quantity):
        self.setReputation(InventoryType.OverallRep, quantity)

    def getOverallRep(self):
        return self.getReputation(InventoryType.OverallRep)

    def setGeneralRep(self, quantity):
        self.setReputation(InventoryType.GeneralRep, quantity)

    def getGeneralRep(self, quantity):
        return self.getReputation(InventoryType.GeneralRep)

    def setGoldInPocket(self, quantity):
        self.b_setStackQuantity(InventoryType.GoldInPocket, min(quantity, 65000))

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

        avatar.giveCardMessage(cardId)
        self.b_setStackQuantity(cardId, amount)

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

        # populate the avatar's ship doId list
        shipDoIdList = self.getShipDoIdList()
        for shipId in shipDoIdList:
            self.air.shipLoader.activateShip(avatar, shipId)

        DistributedInventoryAI.populateInventory(self)
