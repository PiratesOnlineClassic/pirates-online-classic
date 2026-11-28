from panda3d.core import ConfigVariableBool
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from otp.uberdog.RejectCode import RejectCode
from pirates.distributed import InteractGlobals
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import ItemType, ItemId
from pirates.makeapirate import BarberGlobals
from pirates.pirate import AvatarTypes
from pirates.ship import ShipGlobals
from pirates.uberdog.UberDogGlobals import InventoryType, InventoryCategory


class DistributedShopKeeperAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShopKeeperAI')

    # The client treats this response as a completed store transaction,
    # see DistributedShopKeeper.makeSaleResponse.
    SALE_SUCCESS = 2

    # Ships a Freebooter (unpaid) account may purchase, matching the check
    # in ShipStoreGUI.handleCommitPurchase.
    FREE_SHIP_CLASSES = (ItemId.INTERCEPTOR_L1, ItemId.MERCHANT_L1)

    # The hull condition bit the client reads as "ship is in overhaul",
    # see DistributedShipOV.setHullCondition.
    OVERHAUL_BIT = 1 << 7

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def getShopInventory(self):
        # Mirrors the shelves the client builds in DistributedShopKeeper.announceGenerate,
        # so the AI only ever sells what the shopkeeper is displaying.
        avatarType = getattr(self, 'avatarType', None)
        if avatarType is None or not hasattr(avatarType, 'isA'):
            return []

        lowWeaponsOnly = ConfigVariableBool('low-weapons-only', False).getValue()
        if avatarType.isA(AvatarTypes.Cannoneer):
            return EconomyGlobals.CANNON_AMMO_SHELF_L1 + EconomyGlobals.CANNON_AMMO_SHELF_L2 + \
                EconomyGlobals.CANNON_POUCH_SHELF
        elif avatarType.isA(AvatarTypes.Blacksmith):
            shelf = EconomyGlobals.MELEE_SHELF_L1 + EconomyGlobals.MELEE_SHELF_L2
            if not lowWeaponsOnly:
                shelf = shelf + EconomyGlobals.MELEE_SHELF_L3

            return shelf + EconomyGlobals.DAGGER_AMMO_SHELF_L1 + EconomyGlobals.DAGGER_AMMO_SHELF_L2 + \
                EconomyGlobals.DAGGER_POUCH_SHELF
        elif avatarType.isA(AvatarTypes.Bartender):
            return EconomyGlobals.MELEE_SHELF_L1 + EconomyGlobals.MISSILE_SHELF_L1 + EconomyGlobals.BOMB_SHELF_L1
        elif avatarType.isA(AvatarTypes.Gunsmith):
            shelf = EconomyGlobals.MISSILE_SHELF_L1 + EconomyGlobals.MISSILE_SHELF_L2
            if not lowWeaponsOnly:
                shelf = shelf + EconomyGlobals.MISSILE_SHELF_L3

            shelf = shelf + EconomyGlobals.PISTOL_AMMO_SHELF_L1 + EconomyGlobals.PISTOL_AMMO_SHELF_L2 + \
                EconomyGlobals.PISTOL_POUCH_SHELF + EconomyGlobals.BOMB_SHELF_L1 + EconomyGlobals.BOMB_SHELF_L2
            if not lowWeaponsOnly:
                shelf = shelf + EconomyGlobals.BOMB_SHELF_L3

            # the client only displays the repair kit while a siege is running,
            # but the gunsmith is the only shopkeeper who stocks it...
            return shelf + EconomyGlobals.BOMB_AMMO_SHELF_L1 + EconomyGlobals.BOMB_AMMO_SHELF_L2 + \
                EconomyGlobals.GRENADE_POUCH_SHELF + EconomyGlobals.CANNON_AMMO_SHELF_L1 + \
                EconomyGlobals.CANNON_AMMO_SHELF_L2 + EconomyGlobals.CANNON_POUCH_SHELF + \
                EconomyGlobals.SIEGE_SHELF
        elif avatarType.isA(AvatarTypes.Grenadier):
            return EconomyGlobals.BOMB_SHELF_L1 + EconomyGlobals.BOMB_SHELF_L2 + EconomyGlobals.BOMB_SHELF_L3 + \
                EconomyGlobals.BOMB_AMMO_SHELF_L1 + EconomyGlobals.BOMB_AMMO_SHELF_L2 + \
                EconomyGlobals.GRENADE_POUCH_SHELF
        elif avatarType.isA(AvatarTypes.Gypsy):
            shelf = EconomyGlobals.TONIC_SHELF_L1 + EconomyGlobals.TONIC_SHELF_L2
            if lowWeaponsOnly:
                return shelf + EconomyGlobals.MOJO_SHELF_L1 + EconomyGlobals.MOJO_SHELF_L2

            return shelf + EconomyGlobals.MOJO_SHELF_ALL
        elif avatarType.isA(AvatarTypes.Merchant):
            return EconomyGlobals.PISTOL_AMMO_SHELF_L1 + EconomyGlobals.MELEE_SHELF_L1 + \
                EconomyGlobals.MISSILE_SHELF_L1
        elif avatarType.isA(AvatarTypes.MedicineMan):
            return EconomyGlobals.TONIC_SHELF_L1 + EconomyGlobals.TONIC_SHELF_L2

        # any shopkeeper offering the ships option opens the ship store with
        # the full ship shelf, see DistributedShopKeeper.startShopping...
        menu = InteractGlobals.getNPCInteractMenu(avatarType)
        if menu and InteractGlobals.SHIPS in menu[1]:
            return EconomyGlobals.SHIP_SHELF

        return []

    def __getAvatarAndInventory(self, handlerName):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.notify.warning('Failed to process %s for non-existant avatar %d!' % (
                handlerName, avatarId))

            return None, None

        inventory = self.air.inventoryManager.getInventory(avatarId)
        if not inventory:
            self.notify.warning('Failed to process %s for avatar %d, unknown inventory!' % (
                handlerName, avatarId))

            self.d_makeSaleResponse(avatarId, RejectCode.TIMEOUT)
            return avatar, None

        return avatar, inventory

    def __getItemLevel(self, inventory, itemId):
        from pirates.battle import WeaponGlobals
        from pirates.reputation import ReputationGlobals

        repId = WeaponGlobals.getRepId(itemId)
        if not repId:
            return 0

        return ReputationGlobals.getLevelFromTotalReputation(repId, inventory.getAccumulator(repId))[0]

    def __checkPurchase(self, avatar, inventory, itemId, pending, pendingShips):
        """
        Validates a single item of a makeSale buy request and returns a tuple of
        (response, price, quantity). These are the same rules the client enforces
        in StoreGUI.handleBuyItem and ShipStoreGUI.handleCommitPurchase.
        """

        itemCost = EconomyGlobals.getItemCost(itemId)
        if itemCost is None or itemId not in self.getShopInventory():
            self.air.logPotentialHacker(
                message='Received makeSale buy for an item this shop does not sell!',
                avatarId=avatar.doId,
                itemId=itemId)

            return RejectCode.TIMEOUT, 0, 0

        # check to see if the avatar has the training required to purchase
        # this item, e.g. the CutlassToken for a cutlass...
        trainingReq = EconomyGlobals.getItemTrainingReq(itemId)
        if trainingReq and not inventory.getStackQuantity(trainingReq):
            self.notify.debug('Avatar %d cannot buy item %d, missing training %d!' % (
                avatar.doId, itemId, trainingReq))

            return RejectCode.TIMEOUT, 0, 0

        itemCategory = EconomyGlobals.getItemCategory(itemId)
        if itemCategory == ItemType.SHIP:
            if hasattr(avatar, 'isPaid') and not avatar.isPaid() and itemId not in self.FREE_SHIP_CLASSES:
                self.air.logPotentialHacker(
                    message='Received makeSale buy for a ship a Freebooter can not purchase!',
                    avatarId=avatar.doId,
                    itemId=itemId)

                return RejectCode.TIMEOUT, 0, 0

            shipCount = len(inventory.getShipDoIdList()) + pendingShips
            if shipCount >= inventory.getCategoryLimit(InventoryCategory.SHIPS):
                return RejectCode.OVERFLOW, 0, 0

            return self.SALE_SUCCESS, int(itemCost), 1

        minLevel = EconomyGlobals.getItemMinLevel(itemId)
        if minLevel and minLevel > self.__getItemLevel(inventory, itemId):
            self.air.logPotentialHacker(
                message='Received makeSale buy for an item above the avatar\'s level!',
                avatarId=avatar.doId,
                itemId=itemId,
                minLevel=minLevel)

            return RejectCode.TIMEOUT, 0, 0

        # the quantity of a store bundle is defined by the economy,
        # never trust the quantity the client has sent us...
        itemQuantity = EconomyGlobals.getItemQuantity(itemId) or 1
        currentStack = inventory.getStackQuantity(itemId) or 0
        if itemCategory == ItemType.WEAPON and (currentStack or pending):
            return RejectCode.OVERFLOW, 0, 0

        if currentStack + pending >= inventory.getStackLimit(itemId):
            return RejectCode.OVERFLOW, 0, 0

        return self.SALE_SUCCESS, max(int(itemCost * itemQuantity), 1), itemQuantity

    def __checkSale(self, avatar, inventory, itemId, itemQuantity, pending):
        itemCost = EconomyGlobals.getItemCost(itemId)
        currentStack = inventory.getStackQuantity(itemId) or 0
        if itemCost is None or itemQuantity <= 0 or currentStack < pending + itemQuantity or \
                EconomyGlobals.getItemCategory(itemId) == ItemType.SHIP:
            self.air.logPotentialHacker(
                message='Received makeSale sell for an item the avatar does not have!',
                avatarId=avatar.doId,
                itemId=itemId,
                itemQuantity=itemQuantity,
                currentStack=currentStack)

            return RejectCode.TIMEOUT, 0

        # items are sold back to the store at half of their value,
        # see InventoryListItem.loadData...
        return self.SALE_SUCCESS, int(itemCost * itemQuantity / 2)

    def __applyPouchBonus(self, inventory, itemId):
        stackBonus = EconomyGlobals.getInventoryBonus(itemId)
        if not stackBonus:
            return

        pouchType = EconomyGlobals.getItemType(itemId)
        ammoList = EconomyGlobals.getPouchAmmoList(pouchType)
        if (not isinstance(stackBonus, (list, tuple)) or
                not isinstance(ammoList, (list, tuple)) or
                not ammoList or len(ammoList) != len(stackBonus)):
            self.notify.warning('Invalid pouch ammo metadata for item %s' % itemId)
            return

        for ammoId, bonus in zip(ammoList, stackBonus):
            inventory.b_setStackLimit(ammoId, inventory.getStackLimit(ammoId) + bonus)

    def requestMakeSale(self, buying, selling, names):
        avatar, inventory = self.__getAvatarAndInventory('requestMakeSale')
        if not inventory:
            return

        purchases = []
        sales = []
        pending = {}
        pendingShips = 0
        totalCost = 0
        totalGain = 0

        # validate the entire transaction before the inventory is modified,
        # a sale is either applied as a whole or rejected as a whole...
        for itemId, itemQuantity in buying:
            response, price, quantity = self.__checkPurchase(avatar, inventory, itemId,
                pending.get(itemId, 0), pendingShips)

            if response != self.SALE_SUCCESS:
                self.d_makeSaleResponse(avatar.doId, response)
                return

            if EconomyGlobals.getItemCategory(itemId) == ItemType.SHIP:
                pendingShips += 1
            else:
                pending[itemId] = pending.get(itemId, 0) + quantity

            purchases.append((itemId, quantity))
            totalCost += price

        sold = {}
        for itemId, itemQuantity in selling:
            response, price = self.__checkSale(avatar, inventory, itemId, itemQuantity,
                sold.get(itemId, 0))

            if response != self.SALE_SUCCESS:
                self.d_makeSaleResponse(avatar.doId, response)
                return

            sold[itemId] = sold.get(itemId, 0) + itemQuantity
            sales.append((itemId, itemQuantity))
            totalGain += price

        currentGold = inventory.getGoldInPocket()
        if totalCost > currentGold + totalGain:
            self.air.logPotentialHacker(
                message='Received makeSale buy for items the avatar can not afford!',
                avatarId=avatar.doId,
                currentGold=currentGold,
                totalCost=totalCost)

            self.d_makeSaleResponse(avatar.doId, RejectCode.TIMEOUT)
            return

        inventory.setGoldInPocket(currentGold + totalGain - totalCost)

        for itemId, itemQuantity in sales:
            inventory.b_setStackQuantity(itemId, inventory.getStackQuantity(itemId) - itemQuantity)

        for itemId, itemQuantity in purchases:
            itemCategory = EconomyGlobals.getItemCategory(itemId)
            if itemCategory == ItemType.SHIP:
                self.air.shipLoader.createShip(avatar, itemId)
                continue

            inventory.b_setStackQuantity(itemId, (inventory.getStackQuantity(itemId) or 0) + itemQuantity)
            if itemCategory == ItemType.POUCH:
                self.__applyPouchBonus(inventory, itemId)

        # Log transaction for analytics and GM purposes
        self.logShopkeepTransaction(
            type='requestMakeSale',
            buying=purchases,
            selling=sales,
            price=totalCost,
            gain=totalGain,
            purchaser=avatar.doId)

        self.d_makeSaleResponse(avatar.doId, self.SALE_SUCCESS)

    def requestMusic(self, songId):
        avatar, inventory = self.__getAvatarAndInventory('requestMusic')
        if not inventory:
            return

        if songId not in EconomyGlobals.MUSIC_SHELF:
            self.air.logPotentialHacker(
                message='Received requestMusic for an unknown song!',
                avatarId=avatar.doId,
                songId=songId)

            self.d_makeSaleResponse(avatar.doId, RejectCode.TIMEOUT)
            return

        currentGold = inventory.getGoldInPocket()

        # Verify price, see SongListItem
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
            price=itemPrice,
            purchaser=avatar.doId)

        self.d_playMusic(songId)
        self.d_makeSaleResponse(avatar.doId, self.SALE_SUCCESS)

    def d_playMusic(self, songId):
        self.sendUpdate('playMusic', [songId])

    # The tailor, jeweler and tattoo parlor wardrobes are persisted by the
    # AvatarAccessoriesManager. Until it is able to store owned items the
    # shopkeeper reports an empty wardrobe so the store GUIs can load.

    def requestAccessories(self, purchases, selling):
        pass

    def requestAccessoriesList(self, avId):
        pass

    def d_responseClothingList(self, avatarId, accessories=[]):
        self.sendUpdateToAvatarId(avatarId, 'responseClothingList', [avatarId, accessories])

    def requestAccessoryEquip(self, accessory):
        pass

    def requestTattoo(self, purchases, selling, currencyType=0):
        pass

    def d_makeTattooResponse(self, avatarId, tattoo, zone, success):
        self.sendUpdateToAvatarId(avatarId, 'makeTattooResponse', [tattoo, zone, success])

    def requestTattooList(self, avId):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.notify.warning('Failed to requestTattooList for non-existant avatar %d!' %
                avatarId)

            return

        ownedItems = []

        #TODO: pull owned items from the AvatarAccessoriesManager

        if not len(ownedItems):
            ownedItems = [-1]
        self.d_responseTattooList(avatarId, ownedItems)

    def d_responseTattooList(self, avatarId, tattoos=[-1]):
        self.sendUpdateToAvatarId(avatarId, 'responseTattooList', [avatarId, tattoos])

    def requestTattooEquip(self, tattoos):
        pass

    def requestJewelry(self, purchases, selling):
        pass

    def requestJewelryList(self, avId):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.notify.warning('Failed to requestJewelryList for non-existant avatar %d!' %
                avatarId)

            return

        ownedItems = []

        #TODO: pull owned items from the AvatarAccessoriesManager

        if not len(ownedItems):
            ownedItems = [-1]
        self.d_responseJewelryList(avatarId, ownedItems)

    def d_responseJewelryList(self, avatarId, items=[-1]):
        self.sendUpdateToAvatarId(avatarId, 'responseJewelryList', [avatarId, items])

    def requestJewelryEquip(self, jewelry):
        pass

    def requestBarber(self, idx, color):
        avatar, inventory = self.__getAvatarAndInventory('requestBarber')
        if not inventory:
            return

        currentGold = inventory.getGoldInPocket()
        item = BarberGlobals.barber_id.get(idx, None)
        if item is None:
            self.notify.warning('Unknown barber id: %s!' % idx)

            self.d_makeBarberResponse(avatar.doId, idx, color, False)
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

            self.d_makeBarberResponse(avatar.doId, idx, color, False)
            return

        if itemType not in (BarberGlobals.HAIR, BarberGlobals.BEARD, BarberGlobals.MUSTACHE):
            self.notify.warning('Received invalid barber hair type: %s!' % itemType)
            self.d_makeBarberResponse(avatar.doId, idx, color, False)
            return

        inventory.setGoldInPocket(currentGold - itemPrice)

        # Modify the players DNA
        if itemType == BarberGlobals.HAIR:
            avatar.b_setHairHair(itemId)
        elif itemType == BarberGlobals.BEARD:
            avatar.b_setHairBeard(itemId)
        elif itemType == BarberGlobals.MUSTACHE:
            avatar.b_setHairMustache(itemId)

        avatar.b_setHairColor(color)

        # Log transaction for analytics and GM purposes
        self.logShopkeepTransaction(
            type='requestBarber',
            idx=idx,
            color=color,
            price=itemPrice,
            purchaser=avatar.doId)

        # the barber store GUI applies the new style once we respond,
        # see BarberStoreGUI.barberPurchase...
        self.d_makeBarberResponse(avatar.doId, idx, color, True)

    def d_makeBarberResponse(self, avatarId, uid, color, success):
        self.sendUpdateToAvatarId(avatarId, 'makeBarberResponse', [uid, color, success])

    def __getOwnedShip(self, avatarId, shipId, handlerName):
        inventory = self.air.inventoryManager.getInventory(avatarId)
        ship = self.air.doId2do.get(shipId)
        if (not inventory or not ship or
                shipId not in inventory.getShipDoIdList() or
                ship.getGameState()[0] != 'Off'):
            self.notify.warning('Avatar %d requested %s for unavailable ship %d' %
                (avatarId, handlerName, shipId))
            self.d_makeSaleResponse(avatarId, RejectCode.TIMEOUT)
            return None, None

        return inventory, ship

    def requestPurchaseRepair(self, shipId):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.notify.warning('Cannot repair ship %d for missing avatar %d' %
                (shipId, avatarId))
            return

        inventory, ship = self.__getOwnedShip(avatarId, shipId, 'repair')
        if not ship:
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

        # Log transaction for analytics and GM purposes
        self.logShopkeepTransaction(
            type='requestPurchaseRepair',
            shipId=shipId,
            price=cost,
            purchaser=avatarId)

        self.d_responseShipRepair(avatarId, shipId)

    def d_responseShipRepair(self, avatarId, shipId):
        self.sendUpdateToAvatarId(avatarId, 'responseShipRepair', [shipId])

    def requestPurchaseOverhaul(self, shipId):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.notify.warning('Cannot overhaul ship %d for missing avatar %d' %
                (shipId, avatarId))
            return

        inventory, ship = self.__getOwnedShip(avatarId, shipId, 'overhaul')
        if not ship:
            return

        # the client prices an overhaul from the ship class, not the model class,
        # see DistributedShopKeeper.sendRequestOverhaulShip...
        shipPrice = EconomyGlobals.getItemCost(ship.getShipClass())
        if shipPrice is None:
            self.notify.warning('Cannot determine overhaul cost for ship %d' % shipId)
            self.d_makeSaleResponse(avatarId, RejectCode.TIMEOUT)
            return

        cost = int(shipPrice * EconomyGlobals.OVERHAUL_COST_PERCENTAGE)
        currentGold = inventory.getGoldInPocket()
        if currentGold < cost:
            self.air.logPotentialHacker(
                message='Received requestPurchaseOverhaul the avatar can not afford!',
                currentGold=currentGold,
                shipId=shipId,
                cost=cost)

            self.d_makeSaleResponse(avatarId, RejectCode.TIMEOUT)
            return

        inventory.setGoldInPocket(currentGold - cost)

        # reconstruct the ship, this restores it to full health and takes it
        # out of overhaul...
        ship.b_setHp(ship.getMaxHp())
        ship.b_setSp(ship.getMaxSp())
        if hasattr(ship, 'getHullCondition'):
            ship.b_setHullCondition(ship.getHullCondition() & ~self.OVERHAUL_BIT)

        # Log transaction for analytics and GM purposes
        self.logShopkeepTransaction(
            type='requestPurchaseOverhaul',
            shipId=shipId,
            price=cost,
            purchaser=avatarId)

        self.d_responseShipRepair(avatarId, shipId)

    def requestSellShip(self, shipId):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.notify.warning('Cannot sell ship %d for missing avatar %d' %
                (shipId, avatarId))
            return

        inventory, ship = self.__getOwnedShip(avatarId, shipId, 'sale')
        if not ship:
            return

        modelClass = ShipGlobals.getModelClass(ship.getShipClass())
        shipPrice = EconomyGlobals.getItemCost(modelClass)
        if shipPrice is None:
            self.notify.warning('Cannot determine sale value for ship %d' % shipId)
            self.d_makeSaleResponse(avatarId, RejectCode.TIMEOUT)
            return

        shipIds = list(inventory.getShipDoIdList())
        shipIds.remove(shipId)
        inventory.setShipDoIdList(shipIds)

        # any gold over the pocket limit is lost, the client has already
        # warned the avatar about this (PLocalizer.ExcessGoldLost)...
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
