from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from pirates.battle.DistributedBattleNPCAI import DistributedBattleNPCAI
from pirates.economy.DistributedShopKeeperAI import DistributedShopKeeperAI
from pirates.piratesbase import PiratesGlobals
from pirates.distributed import InteractGlobals
from pirates.economy import EconomyGlobals

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
