from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from otp.uberdog.RejectCode import RejectCode
from pirates.economy import EconomyGlobals
from pirates.makeapirate import BarberGlobals
from pirates.ship import ShipGlobals
from pirates.uberdog.UberDogGlobals import InventoryType, InventoryCategory

class DistributedShopKeeperAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShopKeeperAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def __purchaseItem(self, avatar, inventory, item):
        itemId, itemQuantity = item

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

        # TODO FIXME: properly check to see what inventory type this
        # item they are trying to buy fits under...
        currentStack = inventory.getStackQuantity(itemId)
        stackLimit = inventory.getStackLimit(itemId) if not itemId in EconomyGlobals.SHIP_SHELF else inventory.getCategoryLimit(InventoryCategory.SHIPS)
        if not currentStack:
            currentStack = 0

        if itemId in EconomyGlobals.SHIP_SHELF:
            currentStack = len(inventory.getShipDoIdList())

            self.air.shipLoader.createShip(avatar, itemId)

        if currentStack >= stackLimit:
            return RejectCode.OVERFLOW

        inventory.b_setStackQuantity(itemId, currentStack + itemQuantity)
        inventory.setGoldInPocket(currentGold - itemPrice)

        # Process stack limit changes
        stackBonus = EconomyGlobals.getInventoryBonus(itemId)
        if stackBonus:
            pouchType = EconomyGlobals.getItemType(itemId)
            ammoList = EconomyGlobals.getPouchAmmoList(pouchType)
            if (not isinstance(stackBonus, (list, tuple)) or
                    not isinstance(ammoList, (list, tuple)) or
                    not ammoList or len(ammoList) != len(stackBonus)):
                self.notify.warning('Invalid pouch ammo metadata for item %s' % itemId)
            else:
                for ammoId, bonus in zip(ammoList, stackBonus):
                    inventory.b_setStackLimit(ammoId, inventory.getStackLimit(ammoId) + bonus)

        return 2

    def __sellItem(self, avatar, inventory, item):
        itemId, itemQuantity = item
        currentStack = inventory.getStackQuantity(itemId)
        if not currentStack:
            currentStack = 0

        if currentStack < itemQuantity:
            self.air.logPotentialHacker(
                message='Received makeSale sell for an item the avatar does not have!',
                itemId=itemId,
                itemQuantity=itemQuantity,
                currentStack=currentStack
            )

            return RejectCode.TIMEOUT

        itemPrice = EconomyGlobals.getItemCost(itemId)
        currentGold = inventory.getGoldInPocket()
        inventory.b_setStackQuantity(itemId, currentStack - itemQuantity)
        inventory.setGoldInPocket(currentGold + itemPrice)

    def requestMakeSale(self, buying, selling, names):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            self.notify.warning('Failed to process make sale for non-existant avatar %d!' %
                avatar.doId)

            self.d_makeSaleResponse(avatar.doId, RejectCode.TIMEOUT)
            return

        inventory = self.air.inventoryManager.getInventory(avatar.doId)
        if not inventory:
            self.notify.debug('Cannot process sale for avatar %d, unknown inventory!' %
                avatar.doId)

            self.d_makeSaleResponse(avatar.doId, RejectCode.TIMEOUT)
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

        self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [response])

    def requestMusic(self, songId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            self.notify.warning('Failed to process make sale for non-existant avatar %d!' %
                avatar.doId)

            self.d_makeSaleResponse(avatar.doId, RejectCode.TIMEOUT)
            return

        inventory = self.air.inventoryManager.getInventory(avatar.doId)
        if not inventory:
            self.notify.debug('Cannot process sale for avatar %d, unknown inventory!' %
                avatar.doId)

            self.d_makeSaleResponse(avatar.doId, RejectCode.TIMEOUT)
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

            self.d_makeSaleResponse(avatar.doId, RejectCode.TIMEOUT)
            return

        inventory.setGoldInPocket(currentGold - itemPrice)

        # Log transaction for analytics and GM purposes
        self.logShopkeepTransaction(
            type='requestMusic',
            songId=songId,
            price=5,
            purchaser=avatar.doId)

        self.d_playMusic(songId)
        self.d_makeSaleResponse(avatar.doId, 2)

    def d_playMusic(self, songId):
        self.sendUpdate('playMusic', [songId])

    def requestAccessories(self, purchases, selling):
        pass

    def requestAccessoriesList(self, avId):
        pass

    def d_responseClothingList(self, avatarId, accessories=[-1]):
        self.sendUpdateToAvatarId(avatarId, 'responseClothingList', [avatarId, accessories])

    def requestAccessoryEquip(self, accessory):
        pass

    def requestTattoo(self, purchases, selling, currencyType=0):
        pass

    def requestTattooList(self, avId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            self.notify.warning('Failed to requestTattooList for non-existant avatar %d!' %
                avatar.doId)

            return

        ownedItems = []

        #TODO: pull owned items

        if not len(ownedItems):
            ownedItems = [-1]
        self.d_responseTattooList(avId, ownedItems)

    def d_responseTattooList(self, avatarId, tattoos=[-1]):
        self.sendUpdateToAvatarId(avatarId, 'responseTattooList', [avatarId, tattoos])

    def requestTattooEquip(self, tattoos):
        pass

    def requestJewelry(self, purchases, selling):
        pass

    def requestJewelryList(self, avId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            self.notify.warning('Failed to requestJewelryList for non-existant avatar %d!' %
                avatar.doId)

            return

        ownedItems = []

        #TODO: pull owned items

        if not len(ownedItems):
            ownedItems = [-1]
        self.d_responseJewelryList(avId, ownedItems)

    def d_responseJewelryList(self, avatarId, items=[-1]):
        self.sendUpdateToAvatarId(avatarId, 'responseJewelryList', [avatarId, items])

    def requestJewelryEquip(self, jewelry):
        pass

    def requestBarber(self, idx, color):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            self.notify.warning('Failed to process make sale for non-existant avatar %d!' %
                avatar.doId)

            self.d_makeSaleResponse(avatar.doId, RejectCode.TIMEOUT)
            return

        inventory = self.air.inventoryManager.getInventory(avatar.doId)
        if not inventory:
            self.notify.debug('Cannot process sale for avatar %d, unknown inventory!' %
                avatar.doId)

            self.d_makeSaleResponse(avatar.doId, RejectCode.TIMEOUT)
            return

        currentGold = inventory.getGoldInPocket()
        item = BarberGlobals.barber_id.get(idx, None)
        if item is None:
            self.notify.warning('Unknown barber id: %s!' % idx)

            self.d_makeSaleResponse(avatar.doId, RejectCode.TIMEOUT)
            return

        itemId = item[0]
        itemPrice = item[4]
        itemType = item[1]
        if itemPrice > currentGold:
            self.air.logPotentialHacker(
                message='Received requestBarber for a style the avatar can not afford!',
                currentGold=currentGold,
                itemId=itemId,
                itemType=itemType,
                itemPrice=itemPrice)

            self.d_makeSaleResponse(avatar.doId, RejectCode.TIMEOUT)
            return

        inventory.setGoldInPocket(currentGold - itemPrice)

        # Modify the players DNA
        if itemType == BarberGlobals.HAIR:
            avatar.b_setHairHair(itemId)
        elif itemType == BarberGlobals.BEARD:
            avatar.b_setHairBeard(itemId)
        elif itemType == BarberGlobals.MUSTACHE:
            avatar.b_setHairMustache(itemId)
        else:
            self.notify.warning('Received invalid barber hair type: %s!' % itemType)
            self.d_makeSaleResponse(avatar.doId, RejectCode.TIMEOUT)
            return

        avatar.b_setHairColor(color)

        # Log transaction for analytics and GM purposes
        self.logShopkeepTransaction(
            type='requestBarber',
            idx=idx,
            color=color,
            price=itemPrice,
            purchaser=avatar.doId)

        self.d_makeSaleResponse(avatar.doId, 2)

    def requestPurchaseRepair(self, shipId):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.notify.warning('Cannot repair ship %d for missing avatar %d' %
                (shipId, avatarId))
            return

        inventory = self.air.inventoryManager.getInventory(avatarId)
        ship = self.air.doId2do.get(shipId)
        if (not inventory or not ship or
                shipId not in inventory.getShipDoIdList() or
                ship.getGameState()[0] != 'Off'):
            self.notify.warning('Avatar %d requested repair for unavailable ship %d' %
                (avatarId, shipId))
            self.d_makeSaleResponse(avatarId, RejectCode.TIMEOUT)
            return

        modelClass = ShipGlobals.getModelClass(ship.getShipClass())
        cost = ShipGlobals.calcRepairCost(
            ship.getMaxHp(), ship.getHp(), ship.getMaxSp(), ship.getSp(),
            modelClass)
        currentGold = inventory.getGoldInPocket()
        if currentGold < cost:
            self.d_makeSaleResponse(avatarId, RejectCode.TIMEOUT)
            return

        inventory.setGoldInPocket(currentGold - cost)
        ship.b_setHp(ship.getMaxHp())
        ship.b_setSp(ship.getMaxSp())
        self.sendUpdateToAvatarId(avatarId, 'responseShipRepair', [shipId])

    def requestPurchaseOverhaul(self, shipId):
        pass

    def requestSellShip(self, shipId):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.notify.warning('Cannot sell ship %d for missing avatar %d' %
                (shipId, avatarId))
            return

        inventory = self.air.inventoryManager.getInventory(avatarId)
        ship = self.air.doId2do.get(shipId)
        if (not inventory or not ship or
                shipId not in inventory.getShipDoIdList() or
                ship.getGameState()[0] != 'Off'):
            self.notify.warning('Avatar %d requested sale of unavailable ship %d' %
                (avatarId, shipId))
            self.d_makeSaleResponse(avatarId, RejectCode.TIMEOUT)
            return

        modelClass = ShipGlobals.getModelClass(ship.getShipClass())
        shipPrice = EconomyGlobals.getItemCost(modelClass)
        if shipPrice is None:
            self.notify.warning('Cannot determine sale value for ship %d' % shipId)
            self.d_makeSaleResponse(avatarId, RejectCode.TIMEOUT)
            return

        shipIds = inventory.getShipDoIdList()
        shipIds.remove(shipId)
        inventory.setShipDoIdList(shipIds)
        inventory.setGoldInPocket(
            inventory.getGoldInPocket() + int(shipPrice / 2))
        self.logShopkeepTransaction(
            type='requestSellShip',
            shipId=shipId,
            price=int(shipPrice / 2),
            purchaser=avatarId)
        ship.requestDelete()

    def d_makeSaleResponse(self, avatarId, results):
        self.sendUpdateToAvatarId(avatarId, 'makeSaleResponse', [results])

    def logShopkeepTransaction(self, **kwargs):
        self.air.writeServerEvent('shopkeep-transaction', **kwargs)