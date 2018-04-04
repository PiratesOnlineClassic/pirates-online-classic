
from pirates.battle.DistributedBattleNPCAI import DistributedBattleNPCAI
from pirates.economy.DistributedShopKeeperAI import DistributedShopKeeperAI
from direct.directnotify import DirectNotifyGlobal

class DistributedNPCTownfolkAI(DistributedBattleNPCAI, DistributedShopKeeperAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCTownfolkAI')

    def __init__(self, air):
        DistributedBattleNPCAI.__init__(self, air)
        DistributedShopKeeperAI.__init__(self, air)
        self.dNAId = ''
        self.shopId = 0
        self.helpId = 0


    # setDNAId(string) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setDNAId(self, dNAId):
        self.dNAId = dNAId

    def d_setDNAId(self, dNAId):
        self.sendUpdate('setDNAId', [dNAId])

    def b_setDNAId(self, dNAId):
        self.setDNAId(dNAId)
        self.d_setDNAId(dNAId)

    def getDNAId(self):
        return self.dNAId

    # setMovie(string, uint32) broadcast ram

    def setMovie(self, movie, todo_uint32_1):
        self.sendUpdate('setMovie', [movie, todo_uint32_1])

    # triggerInteractShow(uint32)

    def triggerInteractShow(self, triggerInteractShow):
        self.sendUpdate('triggerInteractShow', [triggerInteractShow])

    # setPageNumber(int16, int8, int16) broadcast ram clsend

    def setPageNumber(self, pageNumber, todo_int8_1, todo_int16_2):
        self.sendUpdate('setPageNumber', [pageNumber, todo_int8_1, todo_int16_2])

    # offerOptions(int8)

    def offerOptions(self, offerOptions):
        self.sendUpdate('offerOptions', [offerOptions])

    # startTutorial(uint8)

    def startTutorial(self, startTutorial):
        self.sendUpdate('startTutorial', [startTutorial])

    # swordTutorialPt1(uint32) airecv clsend

    def swordTutorialPt1(self, swordTutorialPt1):
        pass

    # pistolTutorialPt1(uint32) airecv clsend

    def pistolTutorialPt1(self, pistolTutorialPt1):
        pass

    # shipTutorialPt1(uint32, ItemNameHolder) airecv clsend

    def shipTutorialPt1(self, shipTutorialPt1, todo_ItemNameHolder_1):
        pass

    # setShopId(uint16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setShopId(self, shopId):
        self.shopId = shopId

    def d_setShopId(self, shopId):
        self.sendUpdate('setShopId', [shopId])

    def b_setShopId(self, shopId):
        self.setShopId(shopId)
        self.d_setShopId(shopId)

    def getShopId(self):
        return self.shopId

    # setHelpId(uint16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setHelpId(self, helpId):
        self.helpId = helpId

    def d_setHelpId(self, helpId):
        self.sendUpdate('setHelpId', [helpId])

    def b_setHelpId(self, helpId):
        self.setHelpId(helpId)
        self.d_setHelpId(helpId)

    def getHelpId(self):
        return self.helpId

    # requestMusic(uint32) airecv clsend

    def requestMusic(self, requestMusic):
        pass

    # playMusic(uint32) broadcast

    def playMusic(self, playMusic):
        self.sendUpdate('playMusic', [playMusic])

    # levelUpCutlass(uint32) airecv clsend

    def levelUpCutlass(self, levelUpCutlass):
        pass


