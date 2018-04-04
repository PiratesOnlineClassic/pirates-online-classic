# NO BASE CLASSES WERE FOUND! 
 #THIS CLASS LIKELY HAD NO DEFINITION IN THE DCLASS FILES WHEN stub_generator.py WAS RUN!

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedShopKeeperAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShopKeeperAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # requestMakeSale(TradeSlot [], TradeSlot [], ItemNameHolder []) airecv clsend

    def requestMakeSale(self, requestMakeSale, todo_TradeSlot_1, todo_ItemNameHolder_2):
        pass

    # requestPurchaseRepair(uint32) airecv clsend

    def requestPurchaseRepair(self, requestPurchaseRepair):
        pass

    # requestPurchaseOverhaul(uint32) airecv clsend

    def requestPurchaseOverhaul(self, requestPurchaseOverhaul):
        pass

    # requestSellShip(uint32) airecv clsend

    def requestSellShip(self, requestSellShip):
        pass

    # requestAccessoriesList(uint32) airecv clsend

    def requestAccessoriesList(self, requestAccessoriesList):
        pass

    # requestJewelryList(uint32) airecv clsend

    def requestJewelryList(self, requestJewelryList):
        pass

    # requestTattooList(uint32) airecv clsend

    def requestTattooList(self, requestTattooList):
        pass

    # requestAccessories(Accessory [], Accessory []) airecv clsend

    def requestAccessories(self, requestAccessories, todo_Accessory_1):
        pass

    # requestJewelry(int32 [], int32 []) airecv clsend

    def requestJewelry(self, requestJewelry, todo_int32_1):
        pass

    # requestAccessoryEquip(Accessory []) airecv clsend

    def requestAccessoryEquip(self, requestAccessoryEquip):
        pass

    # requestJewelryEquip(Jewelry []) airecv clsend

    def requestJewelryEquip(self, requestJewelryEquip):
        pass

    # requestTattooEquip(Tattoo []) airecv clsend

    def requestTattooEquip(self, requestTattooEquip):
        pass

    # requestTattoo(int32 [], int32 [], int8) airecv clsend

    def requestTattoo(self, requestTattoo, todo_int32_1, todo_int8_2):
        pass

    # requestBarber(uint32, uint8) airecv clsend

    def requestBarber(self, requestBarber, todo_uint8_1):
        pass

    # makeSaleResponse(uint32) ownrecv

    # responseShipRepair(uint32) ownrecv

    # makeTattooResponse(uint16, uint16, bool) ownrecv

    # makeBarberResponse(uint32, uint8, bool) ownrecv

    # responseClothingList(uint32, uint32array []) ownrecv

    # responseTattooList(uint32, int32 []) ownrecv

    # responseJewelryList(uint32, jewelryIdList) ownrecv


