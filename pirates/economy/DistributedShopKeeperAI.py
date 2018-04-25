from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.economy import EconomyGlobals

class DistributedShopKeeperAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShopKeeperAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        
    def requestMakeSale(self, buying, selling, names):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            self.notify.warning('Failed to process make sale for non-existant avatar %d!' %
                avatar.doId) 

            self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [RejectCode.TIMEOUT])
            return

        inventory = self.air.inventoryManager.getInventory(avatar.doId)
        if not inventory:
            self.notify.debug('Cannot process sale for avatar %d, unknown inventory!' % 
                avatar.doId)

            self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [RejectCode.TIMEOUT])
            return
        currentGold = inventory.getGoldInPocket()

        # Buy items
        for purchase in buying:
            itemId, itemQuantity = purchase

            # Verify price
            itemPrice = EconomyGlobals.getItemCost(itemId)
            if itemPrice > currentGold:

                self.air.logPotentialHacker(
                    message='Received makeSale buy for an item the avatar can not afford!',
                    currentGold=currentGold,
                    itemId=itemId,
                    itemQuantity=itemQuantity,
                    itemPrice=itemPrice
                )

                self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [RejectCode.TIMEOUT])
                continue

            currentStack = inventory.getStack(itemId)
            if not currentStack:
                currentStack = 0
            else:
                currentStack = currentStack[1]
            
            inventory.b_setStack(itemId, currentStack + itemQuantity)
            inventory.setGoldInPocket(currentGold - itemPrice)

            self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [2])

        # Sell Items
        for sell in selling:
            itemId, itemQuantity = sell
            currentStack = inventory.getStack(itemId)
            if not currentStack:
                currentStack = 0
            else:
                currentStack = currentStack[1]

            if currentStack < itemQuantity:
                self.air.logPotentialHacker(
                    message='Received makeSale sell for an item the avatar does not have!',
                    itemId=itemId,
                    itemQuantity=itemQuantity,
                    currentStack=currentStack
                )       

                self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [RejectCode.TIMEOUT])
                continue

            itemPrice = EconomyGlobals.getItemCost(itemId)
            inventory.b_setStack(itemId, currentStack - itemQuantity)
            inventory.setGoldInPocket(currentGold + itemPrice)                   


    def requestMusic(self, songId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            self.notify.warning('Failed to process make sale for non-existant avatar %d!' %
                avatar.doId) 

            self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [RejectCode.TIMEOUT])
            return

        inventory = self.air.inventoryManager.getInventory(avatar.doId)
        if not inventory:
            self.notify.debug('Cannot process sale for avatar %d, unknown inventory!' % 
                avatar.doId)

            self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [RejectCode.TIMEOUT])
            return

        currentGold = inventory.getGoldInPocket()

        # Verify price
        itemPrice = 5
        if itemPrice > currentGold:

            self.air.logPotentialHacker(
                message='Received requestMusic for a song the avatar can not afford!',
                currentGold=currentGold,
                songId=songId,
                itemPrice=itemPrice
            )

            self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [RejectCode.TIMEOUT])
            return

        inventory.setGoldInPocket(currentGold - itemPrice)
        self.sendUpdate('playMusic', [songId])
        self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [2])
        
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