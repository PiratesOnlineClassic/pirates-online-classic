from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from pirates.battle.DistributedBattleNPCAI import DistributedBattleNPCAI
from pirates.economy.DistributedShopKeeperAI import DistributedShopKeeperAI
from pirates.piratesbase import PiratesGlobals
from pirates.distributed import InteractGlobals
from pirates.economy import EconomyGlobals
from pirates.reputation import ReputationGlobals
from pirates.ship import ShipGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

NPC_TOWNFOLK_MOVIE_START = 'start'
NPC_TOWNFOLK_MOVIE_STOP = 'stop'
NPC_TOWNFOLK_MOVIE_CLEAR = 'clear'

# the dialog flag sent with offerOptions picks what the npc says as the menu opens,
# the client falls back to the brushoff itself when it has nothing to offer...
NPC_DIALOG_GREETING = 0
NPC_DIALOG_ENCOURAGE = 1
NPC_DIALOG_BRUSHOFF = 2


class DistributedNPCTownfolkAI(DistributedBattleNPCAI, DistributedShopKeeperAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCTownfolkAI')

    # every avatar talks to the npc on it's own, one avatar talking to the npc
    # must not stop another from interacting with or leaving it...
    MULTIUSE = True

    def __init__(self, air):
        DistributedBattleNPCAI.__init__(self, air)
        DistributedShopKeeperAI.__init__(self, air)
        self.dnaId = ''
        self.shopId = 0
        self.helpId = 0
        self.tutorialShipAvIds = set()

    def setDNAId(self, dnaId):
        self.dnaId = dnaId

    def d_setDNAId(self, dnaId):
        self.sendUpdate('setDNAId', [dnaId])

    def b_setDNAId(self, dnaId):
        self.setDNAId(dnaId)
        self.d_setDNAId(dnaId)

    def getDNAId(self):
        return self.dnaId

    def d_setMovie(self, avatarId, mode):
        self.sendUpdateToAvatarId(avatarId, 'setMovie', [mode, avatarId])

    def setShopId(self, shopId):
        self.shopId = shopId

    def d_setShopId(self, shopId):
        self.sendUpdate('setShopId', [shopId])

    def b_setShopId(self, shopId):
        self.setShopId(shopId)
        self.d_setShopId(shopId)

    def getShopId(self):
        return self.shopId

    def setHelpId(self, helpId):
        self.helpId = helpId

    def d_setHelpId(self, helpId):
        self.sendUpdate('setHelpId', [helpId])

    def b_setHelpId(self, helpId):
        self.setHelpId(helpId)
        self.d_setHelpId(helpId)

    def getHelpId(self):
        return self.helpId

    def d_triggerInteractShow(self, avatarId, interactObj):
        self.sendUpdateToAvatarId(avatarId, 'triggerInteractShow', [interactObj])

    def d_offerOptions(self, avatarId, options):
        self.sendUpdateToAvatarId(avatarId, 'offerOptions', options)

    def getDialogFlag(self, avatar):
        # an avatar still working on a quest this npc gave them is encouraged,
        # anyone else is greeted...
        for quest in list(self.air.questMgr.quests.get(avatar.doId, {}).values()):
            if quest.getGiverId() == self.getUniqueId() and not quest.isComplete():
                return NPC_DIALOG_ENCOURAGE

        return NPC_DIALOG_GREETING

    def handleRequestInteraction(self, avatar, interactType, instant):
        # the townsfolk will never serve the Undead,
        # see DistributedNPCTownfolk.requestInteraction...
        if getattr(avatar, 'zombie', 0):
            return self.DENY

        if interactType != PiratesGlobals.INTERACT_TYPE_FRIENDLY:
            return self.DENY

        self.air.questMgr.requestInteract(avatar, self)
        self.d_triggerInteractShow(avatar.doId, 0)
        self.d_offerOptions(avatar.doId, [self.getDialogFlag(avatar)])
        return self.ACCEPT

    def selectOption(self, option):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        inventory = self.air.inventoryManager.getInventory(avatar.doId)
        if not inventory:
            return

        if option == InteractGlobals.HEAL_HP:
            # a groggy avatar is only healed up to it's adjusted max hp,
            # just like the client's heal confirmation...
            hp = avatar.hp
            maxHp = avatar.getAdjMaxHp()
            if hp >= maxHp:
                return

            cost = EconomyGlobals.getAvatarHealHpCost(maxHp - hp)
            if cost > inventory.getGoldInPocket():
                return

            inventory.setGoldInPocket(inventory.getGoldInPocket() - cost)
            avatar.b_setHp(maxHp)
        elif option == InteractGlobals.HEAL_MOJO:
            mojo = avatar.getMojo()
            maxMojo = avatar.getMaxMojo()
            if mojo >= maxMojo:
                return

            cost = EconomyGlobals.getAvatarHealMojoCost(maxMojo - mojo)
            if cost > inventory.getGoldInPocket():
                return

            inventory.setGoldInPocket(inventory.getGoldInPocket() - cost)
            avatar.b_setMojo(maxMojo)
        elif option == InteractGlobals.BRIBE:
            self.air.questMgr.attemptBribeNPC(avatar, self)
        elif option == InteractGlobals.QUEST:
            self.offerQuests(avatar)
        elif option == InteractGlobals.BACK:
            pass
        elif self.isRespecOption(option):
            self.handleRespec(avatar, inventory, option)

    def offerQuests(self, avatar):
        # check to see if the avatar is in the middle of a quest choice
        # given by this npc, if so let them choose from the remaining quests...
        finalOffers, container, numAssignedIncomplete = avatar.questStatus.getQuestOffersFromGiver(self.getUniqueId())
        if finalOffers:
            offers = self.air.questMgr.getQuestLadderOffers(avatar, finalOffers)
            self.d_setQuestLadderOffer(avatar.doId, offers, int(numAssignedIncomplete > 0))
            return

        offers = self.air.questMgr.getQuestOffers(avatar, self.getUniqueId())
        self.d_setQuestOffer(avatar.doId, offers)

    def handleOfferResponse(self, avatar, offer, ladder):
        self.air.questMgr.acceptQuestOffer(avatar, self, offer, offer.isLadder())

    def handleRequestExit(self, avatar):
        return self.ACCEPT

    def __getTutorialAvatar(self, fieldName, avId):
        """
        The quest movies (QuestScripts) call FUNCTION npc "..." on the
        client, which sends the avatar's own doId along with the request...
        """

        senderId = self.air.getAvatarIdFromSender()
        if avId != senderId:
            self.air.logPotentialHacker(
                message='Received %s for another avatar!' % fieldName,
                targetAvId=avId)

            return None

        return self.air.doId2do.get(avId)

    def levelUpCutlass(self, avId):
        # Will Turner's sword lesson ends (or is skipped) by leveling the
        # avatar's cutlass up, which earns the skill point for Sweep...
        avatar = self.__getTutorialAvatar('levelUpCutlass', avId)
        if not avatar or avatar.getTutorial() > PiratesGlobals.TUT_GOT_CUTLASS:
            return

        inventory = avatar.getInventory()
        if not inventory:
            return

        reputation = inventory.getReputation(InventoryType.CutlassRep)
        level, _ = ReputationGlobals.getLevelFromTotalReputation(InventoryType.CutlassRep, reputation)
        if level >= 2:
            return

        trade = self.air.tradeMgr.createTrade(avatar.doId)
        if not trade:
            return

        trade.giveReputation(InventoryType.CutlassRep,
            ReputationGlobals.getTotalReputation(InventoryType.CutlassRep, 2) - reputation)

    def shipTutorialPt1(self, avId, nameHolder):
        # Darby Drydock builds the avatar's first ship with the name they picked,
        # the quest's ShipReward then hands the constructed ship over...
        avatar = self.__getTutorialAvatar('shipTutorialPt1', avId)
        if not avatar or avatar.getTutorial() >= PiratesGlobals.TUT_GOT_SHIP:
            return

        inventory = avatar.getInventory()
        if not inventory or inventory.getShipDoIdList() or avatar.getConstructedShipDoId():
            return

        if avId in self.tutorialShipAvIds:
            return

        typedName, nameIndices = nameHolder
        shipName = self._DistributedShopKeeperAI__getShipName([(typedName, nameIndices)], 0)

        def _shipCreatedCallback(shipId):
            self.tutorialShipAvIds.discard(avId)
            if shipId:
                avatar.setConstructedShipDoId(shipId)

        self.tutorialShipAvIds.add(avId)
        self.air.shipLoader.createShip(avatar, ShipGlobals.INTERCEPTORL1, shipName, callback=_shipCreatedCallback)
