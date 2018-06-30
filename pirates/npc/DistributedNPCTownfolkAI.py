from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.battle.DistributedBattleNPCAI import DistributedBattleNPCAI
from pirates.economy.DistributedShopKeeperAI import DistributedShopKeeperAI
from pirates.piratesbase import PiratesGlobals
from pirates.distributed import InteractGlobals
from pirates.economy import EconomyGlobals


class DistributedNPCTownfolkAI(DistributedBattleNPCAI, DistributedShopKeeperAI):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedNPCTownfolkAI')

    def __init__(self, air):
        DistributedBattleNPCAI.__init__(self, air)
        DistributedShopKeeperAI.__init__(self, air)
        self.dnaId = ''
        self.shopId = 0
        self.helpId = 0

    def handleRequestInteraction(self, avatar, interactType, instant):
        if interactType == PiratesGlobals.INTERACT_TYPE_FRIENDLY:

            self.sendUpdateToAvatarId(avatar.doId, 'triggerInteractShow', [0])
            self.sendUpdateToAvatarId(avatar.doId, 'offerOptions', [2])

            return self.ACCEPT

        return self.DENY

    def handleRequestExit(self, avatar):
        return self.ACCEPT

    def selectOption(self, option):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        inventory = self.air.inventoryManager.getInventory(avatar.doId)
        if not inventory:
            return

        if option == InteractGlobals.HEAL_HP:
            hp = avatar.hp
            maxHp = avatar.getMaxHp()

            if hp == maxHp:
                return

            cost = EconomyGlobals.getAvatarHealHpCost(maxHp)

            if cost > inventory.getGoldInPocket():
                return

            inventory.setGoldInPocket(inventory.getGoldInPocket() - cost)
            avatar.b_setHp(maxHp)
        elif option == InteractGlobals.HEAL_MOJO:
            mojo = avatar.getMojo()
            maxMojo = avatar.getMaxMojo()

            if mojo == maxMojo:
                return

            cost = EconomyGlobals.getAvatarHealMojoCost(maxMojo - mojo)

            if cost > inventory.getGoldInPocket():
                return

            inventory.setGoldInPocket(inventory.getGoldInPocket() - cost)
            avatar.b_setMojo(maxMojo)

    def setDNAId(self, dnaId):
        self.dnaId = dnaId

    def d_setDNAId(self, dnaId):
        self.sendUpdate('setDNAId', [dnaId])

    def b_setDNAId(self, dnaId):
        self.setDNAId(dnaId)
        self.d_setDNAId(dnaId)

    def getDNAId(self):
        return self.dnaId

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
