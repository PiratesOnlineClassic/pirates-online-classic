from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from otp.uberdog.RejectCode import RejectCode
from pirates.economy import EconomyGlobals

class DistributedShopKeeperAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShopKeeperAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def __purchaseItem(self, avatar, inventory, itemId):
        
        # Verify price
        currentGold = inventory.getGoldInPocket()
        itemPrice = EconomyGlobals.getItemCost(itemId)
        if itemPrice > currentGold:

            self.air.logPotentialHacker(
                message='Received makeSale buy for an item the avatar can not afford!',
                currentGold=currentGold,
                itemId=itemId,
                itemQuantity=itemQuantity,
                itemPrice=itemPrice
            )

            return RejectCode.TIMEOUT

        currentStack = inventory.getStack(itemId)
        if not currentStack:
            currentStack = 0
        else:
            currentStack = currentStack[1]

        if not inventory.hasStackSpace(itemId, amount=itemQuantity):
            return RejectCode.OVERFLOW
            
        inventory.b_setStack(itemId, currentStack + itemQuantity)
        inventory.setGoldInPocket(currentGold - itemPrice) 

        # Process stack limit changes
        stackBonus = EconomyGlobals.getInventoryBonus(itemId)
        if stackBonus:
            pass #TODO: write me!

        return 2   

    def __sellItem(self, avatar, inventory, item):
        itemId, itemQuantity = item
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

            return RejectCode.TIMEOUT

        itemPrice = EconomyGlobals.getItemCost(itemId)
        inventory.b_setStack(itemId, currentStack - itemQuantity)
        inventory.setGoldInPocket(currentGold + itemPrice)   

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

        response = 2

        # Buy items
        for purchase in buying:
            
            # Verify this is still a valid transaction
            if response != 2:
                break

            response = self.__purchaseItem(avatar, inventory, purchase)

        # Sell Items
        for sell in selling:

            # Verify this is still a valid transaction
            if response != 2:
                break

            response = self.__sellItem(avatar, inventory, sell)

        # Create logging dictionaries
        log_buying = {}
        for itemId in buying:
            log_buying[buying] = EconomyGlobals.getItemCost(itemId)

        log_selling = {}
        for itemId in buying:
            log_selling[buying] = EconomyGlobals.getItemCost(itemId)      

        # Log transaction for analytics and GM purposes
        self.air.writeServerEvent('shopkeep-transaction', 
            type='requestMakeSale',
            buying=log_buying,
            selling=log_selling,
            purchaser=avatar.doId)

        self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [response])                 

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

        # Log transaction for analytics and GM purposes
        self.air.writeServerEvent('shopkeep-transaction', 
            type='requestMusic',
            songId=songId,
            price=5,
            purchaser=avatar.doId)

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