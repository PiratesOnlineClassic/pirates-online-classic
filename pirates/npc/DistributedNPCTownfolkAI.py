from direct.distributed.DistributedObjectAI import DistributedObjectAI
from pirates.battle.DistributedBattleNPCAI import DistributedBattleNPCAI
from pirates.economy.DistributedShopKeeperAI import DistributedShopKeeperAI
from direct.directnotify import DirectNotifyGlobal


class DistributedNPCTownfolkAI(DistributedBattleNPCAI, DistributedShopKeeperAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCTownfolkAI')

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