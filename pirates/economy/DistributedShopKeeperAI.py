from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedShopKeeperAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShopKeeperAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        
    def requestMakeSale(self, buying, selling, names):
        pass
        
    def requestMusic(self, songId):
        pass
        
    def requestAccessories(self, purchases, selling):
        pass
        
    def requestAccessoriesList(self, avId):
        pass
        
    def requestAccessoryEquip(self, accessory):
        pass
        
    def requestTattoo(self, purchases, selling, currencyType=0):
        pass
    
    def requestTattooList(self, avId):
        pass
        
    def requestTattooEquip(self, tattoos):
        pass
        
    def requestJewelry(self, purchases, selling):
        pass
        
    def requestJewelryList(self, avId):
        pass
        
    def requestJewelryEquip(self, jewelry):
        pass
        
    def requestBarber(self, idx, color):
        pass
        
    def requestPurchaseRepair(self, shipId):
        pass
        
    def requestPurchaseOverhaul(self, shipId):
        pass
        
    def requestSellShip(self, shipId):
        pass