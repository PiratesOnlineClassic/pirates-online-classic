
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class AvatarAccessoriesManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('AvatarAccessoriesManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # migrateDNAElements(uint32, uint32, uint32, uint32array [], uint8)

    def migrateDNAElements(self, migrateDNAElements, todo_uint32_1, todo_uint32_2, todo_uint32array_3, todo_uint8_4):
        self.sendUpdate('migrateDNAElements', [migrateDNAElements, todo_uint32_1, todo_uint32_2, todo_uint32array_3, todo_uint8_4])

    # requestClothingFromDB(uint32, uint32, uint32)

    def requestClothingFromDB(self, requestClothingFromDB, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('requestClothingFromDB', [requestClothingFromDB, todo_uint32_1, todo_uint32_2])

    # responseClothingFromDB(uint32, uint32array [])

    def responseClothingFromDB(self, responseClothingFromDB, todo_uint32array_1):
        self.sendUpdate('responseClothingFromDB', [responseClothingFromDB, todo_uint32array_1])

    # requestClothingAddDB(uint32, uint32, uint32, ClothingDNAElement [], uint32, uint8)

    def requestClothingAddDB(self, requestClothingAddDB, todo_uint32_1, todo_uint32_2, todo_ClothingDNAElement_3, todo_uint32_4, todo_uint8_5):
        self.sendUpdate('requestClothingAddDB', [requestClothingAddDB, todo_uint32_1, todo_uint32_2, todo_ClothingDNAElement_3, todo_uint32_4, todo_uint8_5])

    # responseClothingAddDB(uint32, uint8, uint32)

    def responseClothingAddDB(self, responseClothingAddDB, todo_uint8_1, todo_uint32_2):
        self.sendUpdate('responseClothingAddDB', [responseClothingAddDB, todo_uint8_1, todo_uint32_2])

    # sendCurrentDNAtoAccDB(uint32, uint8)

    def sendCurrentDNAtoAccDB(self, sendCurrentDNAtoAccDB, todo_uint8_1):
        self.sendUpdate('sendCurrentDNAtoAccDB', [sendCurrentDNAtoAccDB, todo_uint8_1])

    # requestClothingDeleteDB(uint32, uint32, uint32, ClothingDNAElement [], uint32)

    def requestClothingDeleteDB(self, requestClothingDeleteDB, todo_uint32_1, todo_uint32_2, todo_ClothingDNAElement_3, todo_uint32_4):
        self.sendUpdate('requestClothingDeleteDB', [requestClothingDeleteDB, todo_uint32_1, todo_uint32_2, todo_ClothingDNAElement_3, todo_uint32_4])

    # responseClothingDeleteDB(uint32, uint8, uint32)

    def responseClothingDeleteDB(self, responseClothingDeleteDB, todo_uint8_1, todo_uint32_2):
        self.sendUpdate('responseClothingDeleteDB', [responseClothingDeleteDB, todo_uint8_1, todo_uint32_2])

    # requestJewelryListDB(uint32, uint32, uint32)

    def requestJewelryListDB(self, requestJewelryListDB, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('requestJewelryListDB', [requestJewelryListDB, todo_uint32_1, todo_uint32_2])

    # responseJewelryList(uint32, jewelryIdList)

    def responseJewelryList(self, responseJewelryList, todo_jewelryIdList_1):
        self.sendUpdate('responseJewelryList', [responseJewelryList, todo_jewelryIdList_1])

    # requestJewelryAddDB(uint32, uint32, uint32, uint32, uint32, uint8)

    def requestJewelryAddDB(self, requestJewelryAddDB, todo_uint32_1, todo_uint32_2, todo_uint32_3, todo_uint32_4, todo_uint8_5):
        self.sendUpdate('requestJewelryAddDB', [requestJewelryAddDB, todo_uint32_1, todo_uint32_2, todo_uint32_3, todo_uint32_4, todo_uint8_5])

    # responseJewelryAddDB(uint32, uint8, uint32, uint32)

    def responseJewelryAddDB(self, responseJewelryAddDB, todo_uint8_1, todo_uint32_2, todo_uint32_3):
        self.sendUpdate('responseJewelryAddDB', [responseJewelryAddDB, todo_uint8_1, todo_uint32_2, todo_uint32_3])

    # requestJewelryDeleteDB(uint32, uint32, uint32, uint32, uint32)

    def requestJewelryDeleteDB(self, requestJewelryDeleteDB, todo_uint32_1, todo_uint32_2, todo_uint32_3, todo_uint32_4):
        self.sendUpdate('requestJewelryDeleteDB', [requestJewelryDeleteDB, todo_uint32_1, todo_uint32_2, todo_uint32_3, todo_uint32_4])

    # responseJewelryDeleteDB(uint32, uint8, uint32, uint32)

    def responseJewelryDeleteDB(self, responseJewelryDeleteDB, todo_uint8_1, todo_uint32_2, todo_uint32_3):
        self.sendUpdate('responseJewelryDeleteDB', [responseJewelryDeleteDB, todo_uint8_1, todo_uint32_2, todo_uint32_3])

    # requestPaidToUnpaidRollBackDB(uint32, uint32, uint32)

    def requestPaidToUnpaidRollBackDB(self, requestPaidToUnpaidRollBackDB, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('requestPaidToUnpaidRollBackDB', [requestPaidToUnpaidRollBackDB, todo_uint32_1, todo_uint32_2])

    # responsePaidToUnpaidRollBack(uint32, uint32array [], uint8)

    def responsePaidToUnpaidRollBack(self, responsePaidToUnpaidRollBack, todo_uint32array_1, todo_uint8_2):
        self.sendUpdate('responsePaidToUnpaidRollBack', [responsePaidToUnpaidRollBack, todo_uint32array_1, todo_uint8_2])

    # requestClothingDropDB(uint32, uint32, uint32, char, uint8)

    def requestClothingDropDB(self, requestClothingDropDB, todo_uint32_1, todo_uint32_2, todo_char_3, todo_uint8_4):
        self.sendUpdate('requestClothingDropDB', [requestClothingDropDB, todo_uint32_1, todo_uint32_2, todo_char_3, todo_uint8_4])

    # responseClothingDropFromDB(uint32, uint32, uint8)

    def responseClothingDropFromDB(self, responseClothingDropFromDB, todo_uint32_1, todo_uint8_2):
        self.sendUpdate('responseClothingDropFromDB', [responseClothingDropFromDB, todo_uint32_1, todo_uint8_2])

    # requestTattooListDB(uint32, uint32, uint32)

    def requestTattooListDB(self, requestTattooListDB, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('requestTattooListDB', [requestTattooListDB, todo_uint32_1, todo_uint32_2])

    # responseTattooList(uint32, tattooIdList)

    def responseTattooList(self, responseTattooList, todo_tattooIdList_1):
        self.sendUpdate('responseTattooList', [responseTattooList, todo_tattooIdList_1])

    # requestTattooAddDB(uint32, uint32, uint32, uint32, uint32, uint8)

    def requestTattooAddDB(self, requestTattooAddDB, todo_uint32_1, todo_uint32_2, todo_uint32_3, todo_uint32_4, todo_uint8_5):
        self.sendUpdate('requestTattooAddDB', [requestTattooAddDB, todo_uint32_1, todo_uint32_2, todo_uint32_3, todo_uint32_4, todo_uint8_5])

    # responseTattooAddDB(uint32, uint8, uint32, uint32)

    def responseTattooAddDB(self, responseTattooAddDB, todo_uint8_1, todo_uint32_2, todo_uint32_3):
        self.sendUpdate('responseTattooAddDB', [responseTattooAddDB, todo_uint8_1, todo_uint32_2, todo_uint32_3])

    # requestTattooDeleteDB(uint32, uint32, uint32, uint32, uint32)

    def requestTattooDeleteDB(self, requestTattooDeleteDB, todo_uint32_1, todo_uint32_2, todo_uint32_3, todo_uint32_4):
        self.sendUpdate('requestTattooDeleteDB', [requestTattooDeleteDB, todo_uint32_1, todo_uint32_2, todo_uint32_3, todo_uint32_4])

    # responseTattooDelete(uint32, uint8, uint32, uint32)

    def responseTattooDelete(self, responseTattooDelete, todo_uint8_1, todo_uint32_2, todo_uint32_3):
        self.sendUpdate('responseTattooDelete', [responseTattooDelete, todo_uint8_1, todo_uint32_2, todo_uint32_3])

    # requestAward(uint32, uint8, uint32, uint32, uint32)

    def requestAward(self, requestAward, todo_uint8_1, todo_uint32_2, todo_uint32_3, todo_uint32_4):
        self.sendUpdate('requestAward', [requestAward, todo_uint8_1, todo_uint32_2, todo_uint32_3, todo_uint32_4])

    # requestTattoosInDNA(uint32)

    def requestTattoosInDNA(self, requestTattoosInDNA):
        self.sendUpdate('requestTattoosInDNA', [requestTattoosInDNA])

    # responseTattoosInDNA(uint32, uint32, uint32, uint32array)

    def responseTattoosInDNA(self, responseTattoosInDNA, todo_uint32_1, todo_uint32_2, todo_uint32array_3):
        self.sendUpdate('responseTattoosInDNA', [responseTattoosInDNA, todo_uint32_1, todo_uint32_2, todo_uint32array_3])


