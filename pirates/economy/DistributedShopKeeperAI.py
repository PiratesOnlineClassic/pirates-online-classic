import math
import string

from panda3d.core import ConfigVariableBool, Vec2
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from otp.uberdog.RejectCode import RejectCode
from pirates.distributed import InteractGlobals
from pirates.economy import EconomyGlobals
from pirates.economy.AvatarAccessoriesManagerAI import getClothingGender, getJewelryGender, getWornClothing
from pirates.economy.EconomyGlobals import ItemType, ItemId
from pirates.makeapirate import BarberGlobals, ClothingGlobals, JewelryGlobals, TattooGlobals
from pirates.pirate import AvatarTypes
from pirates.pirate.HumanDNA import availableHairColors
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.ship import ShipGlobals
from pirates.uberdog.UberDogGlobals import InventoryType, InventoryCategory, getNumRespecType

# the barber's saint patrick's day green, see BarberStoreGUI.setPage
SAINT_PATRICKS_HAIR_COLOR = 8


class DistributedShopKeeperAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShopKeeperAI')

    # The client refreshes the balance of a store that is still open on this
    # response, the tailor, jeweler and tattoo parlor stay open after a sale,
    # see DistributedShopKeeper.makeSaleResponse...
    SALE_SUCCESS = 2

    # ...the item store, ship store and musician close as the sale is sent,
    # this response refreshes the skill tray's ammo and the tonic buttons.
    SALE_COMPLETE = 1

    # Ships a Freebooter (unpaid) account may purchase, matching the check
    # in ShipStoreGUI.handleCommitPurchase.
    FREE_SHIP_CLASSES = (ItemId.INTERCEPTOR_L1, ItemId.MERCHANT_L1)

    # The hull condition bit the client reads as "ship is in overhaul",
    # see DistributedShipOV.setHullCondition.
    OVERHAUL_BIT = 1 << 7

    # The longest typed ship name we accept and the characters it may contain,
    # these match the client's name entry (see NamePanelGui).
    MAX_SHIP_NAME_LENGTH = 32
    SHIP_NAME_CHARS = set(string.ascii_letters + " .,'-")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def getShopInventory(self):
        # the shelves the client builds in DistributedShopKeeper.announceGenerate...
        avatarType = getattr(self, 'avatarType', None)
        if avatarType is None:
            return []

        # any shopkeeper offering the ships option opens the ship store with
        # the full ship shelf, see DistributedShopKeeper.startShopping...
        menu = InteractGlobals.getNPCInteractMenu(avatarType)
        options = menu[1] if menu else []
        if InteractGlobals.SHIPS in options:
            return EconomyGlobals.SHIP_SHELF

        # the bartender stocks a shelf but has no store option to open it...
        if InteractGlobals.STORE not in options:
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
        # the same rules the client enforces in StoreGUI.handleBuyItem
        # and ShipStoreGUI.handleCommitPurchase...
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
            if not self.isAvatarPaid(avatar) and itemId not in self.FREE_SHIP_CLASSES:
                self.air.logPotentialHacker(
                    message='Received makeSale buy for a ship a Freebooter can not purchase!',
                    avatarId=avatar.doId,
                    itemId=itemId)

                return RejectCode.TIMEOUT, 0, 0

            shipCount = len(inventory.getShipDoIdList()) + pendingShips
            if shipCount >= inventory.getCategoryLimit(InventoryCategory.SHIPS):
                return RejectCode.OVERFLOW, 0, 0

            return self.SALE_SUCCESS, int(itemCost), 1

        # Freebooters may only buy tonics and ammo, see InventoryItemGui.checkFreebooter...
        if itemCategory not in (ItemType.CONSUMABLE, ItemType.AMMO) and not self.isAvatarPaid(avatar):
            self.air.logPotentialHacker(
                message='Received makeSale buy for an item a Freebooter can not purchase!',
                avatarId=avatar.doId,
                itemId=itemId)

            return RejectCode.TIMEOUT, 0, 0

        # ammo is only sold for a learned skill, see InventoryItemGui.checkSkillReq...
        if itemCategory == ItemType.AMMO:
            from pirates.battle import WeaponGlobals

            skillId = WeaponGlobals.getSkillIdForAmmoSkillId(itemId)
            if skillId and inventory.getStackQuantity(skillId) < 2:
                return RejectCode.TIMEOUT, 0, 0

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
        # the ammo capacity a pouch gave is kept, so pouches are never bought back...
        if itemCost is None or itemQuantity <= 0 or currentStack < pending + itemQuantity or \
                EconomyGlobals.getItemCategory(itemId) in (ItemType.SHIP, ItemType.POUCH):
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

        # the pouch bonus is the ammo's new stack limit, not an amount
        # added onto it, see the starting limits in InventoryInit...
        for ammoId, bonus in zip(ammoList, stackBonus):
            if bonus > inventory.getStackLimit(ammoId):
                inventory.b_setStackLimit(ammoId, bonus)

    def __getShipName(self, names, index):
        # the client sends a (typedName, nameIndices) pair per ship, see NamePanelGui...
        if index >= len(names):
            return ''

        typedName, nameIndices = names[index]
        if nameIndices:
            if len(nameIndices) != 2 or \
                    nameIndices[0] not in PLocalizer.PirateShipPrefix.values() or \
                    nameIndices[1] not in PLocalizer.PirateShipSuffix.values():
                return ''

            return PLocalizer.getShipName(nameIndices).strip()

        typedName = ' '.join(typedName.split())
        if not typedName or len(typedName) > self.MAX_SHIP_NAME_LENGTH:
            return ''

        if not set(typedName).issubset(self.SHIP_NAME_CHARS):
            return ''

        return typedName

    def __createPurchasedShip(self, avatar, shipClass, shipName, price):

        def _shipCreatedCallback(shipId):
            if shipId:
                return

            # the ship could not be created, give the avatar back their gold...
            self.notify.warning('Failed to create purchased ship %d for avatar %d, '
                'refunding %d gold!' % (shipClass, avatar.doId, price))

            inventory = self.air.inventoryManager.getInventory(avatar.doId)
            if not inventory:
                return

            inventory.setGoldInPocket(inventory.getGoldInPocket() + price)
            self.logShopkeepTransaction(
                type='refundShipPurchase',
                shipClass=shipClass,
                price=price,
                purchaser=avatar.doId)

        self.air.shipLoader.createShip(avatar, shipClass, shipName, callback=_shipCreatedCallback)

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

            purchases.append((itemId, quantity, price))
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

        shipIndex = 0
        for itemId, itemQuantity, price in purchases:
            itemCategory = EconomyGlobals.getItemCategory(itemId)
            if itemCategory == ItemType.SHIP:
                # the ship loader creates the ship asynchronously, the gold
                # is refunded should the ship fail to be created...
                self.__createPurchasedShip(avatar, itemId, self.__getShipName(names, shipIndex), price)
                shipIndex += 1
                continue

            inventory.b_setStackQuantity(itemId, (inventory.getStackQuantity(itemId) or 0) + itemQuantity)
            if itemCategory == ItemType.POUCH:
                self.__applyPouchBonus(inventory, itemId)

        # Log transaction for analytics and GM purposes
        self.logShopkeepTransaction(
            type='requestMakeSale',
            buying=[(itemId, itemQuantity) for itemId, itemQuantity, price in purchases],
            selling=sales,
            price=totalCost,
            gain=totalGain,
            purchaser=avatar.doId)

        self.d_makeSaleResponse(avatar.doId, self.SALE_COMPLETE)

    def requestMusic(self, songId):
        avatar, inventory = self.__getAvatarAndInventory('requestMusic')
        if not inventory:
            return

        menu = InteractGlobals.getNPCInteractMenu(getattr(self, 'avatarType', None))
        if not menu or InteractGlobals.MUSICIAN not in menu[1]:
            self.air.logPotentialHacker(
                message='Received requestMusic for a shopkeeper that is not a musician!',
                avatarId=avatar.doId,
                songId=songId)

            self.d_makeSaleResponse(avatar.doId, RejectCode.TIMEOUT)
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
        self.d_makeSaleResponse(avatar.doId, self.SALE_COMPLETE)

    def d_playMusic(self, songId):
        self.sendUpdate('playMusic', [songId])

    # The tailor, jeweler and tattoo parlor. Wardrobes are stored by the
    # AvatarAccessoriesManager, what the avatar is wearing lives in its DNA.

    def __getStoreAvatar(self, handlerName, storeType):
        avatar, inventory = self.__getAvatarAndInventory(handlerName)
        if not inventory:
            return None, None

        menu = None
        if getattr(self, 'avatarType', None) is not None:
            menu = InteractGlobals.getNPCInteractMenu(self.avatarType)

        if not menu or storeType not in menu[1]:
            self.air.logPotentialHacker(
                message='Received %s for a shopkeeper without that store!' % handlerName,
                avatarId=avatar.doId,
                storeType=storeType)

            self.d_makeSaleResponse(avatar.doId, RejectCode.TIMEOUT)
            return None, None

        # Freebooters can look but not touch, see the store GUIs' velvet rope...
        if not self.isAvatarPaid(avatar):
            self.air.logPotentialHacker(
                message='Received %s from a Freebooter!' % handlerName,
                avatarId=avatar.doId)

            self.d_makeSaleResponse(avatar.doId, RejectCode.TIMEOUT)
            return None, None

        return avatar, inventory

    def __rejectAccessories(self, avatarId, message, **kwargs):
        # This may run once the wardrobe has been loaded from the UberDOG, so
        # the sender is not necessarily the avatar anymore...
        self.notify.warning('%s (avatar %d)' % (message, avatarId))
        self.air.writeServerEvent('suspicious', avId=avatarId, message=message, **kwargs)
        self.d_makeSaleResponse(avatarId, RejectCode.TIMEOUT)

    def __getCurrency(self, inventory, currency):
        if currency == InventoryType.GoldInPocket:
            return inventory.getGoldInPocket()

        return inventory.getStackQuantity(currency) or 0

    def __setCurrency(self, inventory, currency, amount):
        amount = max(0, amount)
        if currency == InventoryType.GoldInPocket:
            inventory.setGoldInPocket(amount)
        else:
            inventory.b_setStackQuantity(currency, amount)

    def __handleWardrobeChanged(self, avatarId, success, currency, refund, handlerName):
        # the avatar has already been charged or paid, so give or take it back...
        if success:
            return

        self.notify.warning('Wardrobe change for %s failed for avatar %d, returning %d!' % (
            handlerName, avatarId, refund))

        inventory = self.air.inventoryManager.getInventory(avatarId)
        if inventory:
            self.__setCurrency(inventory, currency, self.__getCurrency(inventory, currency) + refund)

    def isAvatarPaid(self, avatar):
        # everyone is a member during the all access weekend, see NewsManager.startHoliday...
        return avatar.isPaid() or self.air.newsManager.isHolidayActive(PiratesGlobals.ALLACCESSWEEKEND)

    def getCustomizationCost(self, avatar, cost):
        # members pay half at the tailor, jeweler, tattoo parlor and barber during
        # the half off holiday, see NewsManager.divideAllAccessories...
        if avatar.isPaid() and self.air.newsManager.isHolidayActive(PiratesGlobals.HALFOFFCUSTOMIZATION):
            return int(cost / 2)

        return cost

    def __isHolidayItemAvailable(self, holidayId):
        # holiday items are only offered by the stores while their holiday
        # is running, see NewsManager.startHoliday...
        return holidayId is None or self.air.newsManager.isHolidayActive(holidayId)

    # Tailor:

    def __getClothingPrice(self, avatar, uid, colorId):
        # colors cost more the rarer they are, see AccessoriesStoreGUI.setPage...
        cost = self.getCustomizationCost(avatar, ClothingGlobals.UNIQUE_ID[uid][5])
        scaler = ClothingGlobals.colorCostScaler.get(colorId)
        if scaler:
            cost = int(cost * scaler)

        return cost

    def __findClothing(self, clothing, uid, colorId):
        for item in clothing:
            if item[0] == uid and item[1] == colorId:
                return item

        return None

    def __countClothing(self, clothing, clothingType):
        count = 0
        for item in clothing:
            cloth = ClothingGlobals.UNIQUE_ID.get(item[0])
            if cloth and cloth[0] == clothingType:
                count += 1

        return count

    def __isWearingClothing(self, avatar, uid, colorId):
        item = ClothingGlobals.UNIQUE_ID[uid]
        return getWornClothing(avatar, item[0]) == (item[1], item[2], colorId)

    def __canTakeOffClothing(self, avatar, clothingType):
        # pants and a lady's shirt can never be taken off, the tailor hides
        # their take off button...
        if clothingType == ClothingGlobals.PANT:
            return False
        elif clothingType == ClothingGlobals.SHIRT and avatar.getGender() == 'f':
            return False

        return True

    def requestAccessoriesList(self, avId):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.notify.warning('Failed to requestAccessoriesList for non-existant avatar %d!' %
                avatarId)

            return

        self.air.accessoriesManager.getClothing(avatarId,
            lambda clothing: self.d_responseClothingList(avatarId, clothing))

    def d_responseClothingList(self, avatarId, accessories=[]):
        # each entry is a [uid, colorId, original] list, see AccessoriesStoreGUI.setPage...
        self.sendUpdateToAvatarId(avatarId, 'responseClothingList', [avatarId, accessories])

    def requestAccessories(self, purchases, selling):
        avatar, inventory = self.__getStoreAvatar('requestAccessories', InteractGlobals.ACCESSORIES_STORE)
        if not inventory:
            return

        avatarId = avatar.doId
        self.air.accessoriesManager.getClothing(avatarId,
            lambda clothing: self.__handleAccessories(avatarId, purchases, selling, clothing),
            useCache=True)

    def __handleAccessories(self, avatarId, purchases, selling, clothing):
        avatar = self.air.doId2do.get(avatarId)
        inventory = self.air.inventoryManager.getInventory(avatarId)
        if not avatar or not inventory:
            return

        gender = avatar.getGender()
        storeItems = ClothingGlobals.stores.get(self.getShopId(), {})

        # validate the entire transaction before anything is changed, the
        # same rules AccessoriesStoreGUI enforces...
        sold = []
        takeOff = []
        totalGain = 0
        for uid, colorId, clothingType in selling:
            item = ClothingGlobals.UNIQUE_ID.get(uid)
            owned = self.__findClothing(clothing, uid, colorId)
            if not item or item[0] != clothingType or not owned or owned[2] or [uid, colorId] in sold:
                self.__rejectAccessories(avatarId, 'Received requestAccessories sell for clothing the avatar can not sell!',
                    uid=uid, colorId=colorId)

                return

            if self.__isWearingClothing(avatar, uid, colorId):
                if not self.__canTakeOffClothing(avatar, clothingType):
                    self.__rejectAccessories(avatarId, 'Received requestAccessories sell for clothing the avatar must wear!',
                        uid=uid, colorId=colorId)

                    return

                takeOff.append(clothingType)

            sold.append([uid, colorId])

            # clothing is bought back at a quarter of its value...
            totalGain += int(self.__getClothingPrice(avatar, uid, colorId) * 0.25)

        bought = []
        totalCost = 0
        for uid, colorId, clothingType in purchases:
            item = ClothingGlobals.UNIQUE_ID.get(uid)
            if not item or item[0] != clothingType or colorId not in storeItems.get(uid, []) or \
                    getClothingGender(uid) != gender or self.__findClothing(clothing, uid, colorId) or \
                    [uid, colorId] in bought or not self.__isHolidayItemAvailable(item[8]):
                self.__rejectAccessories(avatarId, 'Received requestAccessories buy for clothing this shop does not sell!',
                    uid=uid, colorId=colorId)

                return

            bought.append([uid, colorId])
            totalCost += self.__getClothingPrice(avatar, uid, colorId)

        for clothingType in set([ClothingGlobals.UNIQUE_ID[uid][0] for uid, colorId in bought]):
            remaining = [item for item in clothing if item[:2] not in sold]
            count = self.__countClothing(remaining, clothingType) + self.__countClothing(bought, clothingType)
            if count > PiratesGlobals.WARDROBE_LIMIT_TAILOR:
                self.d_makeSaleResponse(avatarId, RejectCode.OVERFLOW)
                return

        currentGold = inventory.getGoldInPocket()
        if totalCost > currentGold + totalGain:
            self.__rejectAccessories(avatarId, 'Received requestAccessories buy for clothing the avatar can not afford!',
                currentGold=currentGold, totalCost=totalCost)

            return

        inventory.setGoldInPocket(currentGold + totalGain - totalCost)

        # sold clothing is removed first so it does not count against the
        # wardrobe limit of what was bought...
        if sold:
            self.air.accessoriesManager.removeClothing(avatarId, sold, refund=totalGain,
                callback=lambda success: self.__handleWardrobeChanged(avatarId, success,
                    InventoryType.GoldInPocket, -totalGain, 'requestAccessories'))

        if bought:
            self.air.accessoriesManager.addClothing(avatarId, bought, cost=totalCost, location=self.getShopId(),
                callback=lambda success: self.__handleWardrobeChanged(avatarId, success,
                    InventoryType.GoldInPocket, totalCost, 'requestAccessories'))

        if takeOff:
            for clothingType in takeOff:
                avatar.setClothesByType(ClothingGlobals.CLOTHING_STRING[clothingType], 0, 0, 0)

            avatar.d_setClothes()

        # Log transaction for analytics and GM purposes
        self.logShopkeepTransaction(
            type='requestAccessories',
            buying=bought,
            selling=sold,
            price=totalCost,
            gain=totalGain,
            purchaser=avatarId)

        # the store GUI refreshes the avatar's gold, see DistributedShopKeeper.makeSaleResponse...
        self.d_makeSaleResponse(avatarId, self.SALE_SUCCESS)

    def requestAccessoryEquip(self, accessory):
        avatar, inventory = self.__getStoreAvatar('requestAccessoryEquip', InteractGlobals.ACCESSORIES_STORE)
        if not inventory:
            return

        avatarId = avatar.doId
        self.air.accessoriesManager.getClothing(avatarId,
            lambda clothing: self.__handleAccessoryEquip(avatarId, accessory, clothing),
            useCache=True)

    def __handleAccessoryEquip(self, avatarId, accessory, clothing):
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return

        changes = []
        for uid, colorId, clothingType in accessory:
            typeString = ClothingGlobals.CLOTHING_STRING.get(clothingType)
            if typeString is None:
                self.__rejectAccessories(avatarId, 'Received requestAccessoryEquip for an unknown clothing type!',
                    clothingType=clothingType)

                return

            # a uid of 0 takes the clothing off, see AccessoriesStoreGUI.closePanel...
            if not uid:
                if not self.__canTakeOffClothing(avatar, clothingType):
                    self.__rejectAccessories(avatarId, 'Received requestAccessoryEquip to take off clothing the avatar must wear!',
                        clothingType=clothingType)

                    return

                changes.append((typeString, 0, 0, 0))
                continue

            item = ClothingGlobals.UNIQUE_ID.get(uid)
            if not item or item[0] != clothingType or not self.__findClothing(clothing, uid, colorId):
                self.__rejectAccessories(avatarId, 'Received requestAccessoryEquip for clothing the avatar does not own!',
                    uid=uid, colorId=colorId)

                return

            changes.append((typeString, item[1], item[2], colorId))

        if not changes:
            return

        for typeString, modelId, texId, colorId in changes:
            avatar.setClothesByType(typeString, modelId, texId, colorId)

        avatar.d_setClothes()

    # Tattoo parlor:

    # tattoo zone -> the HumanDNA field the zone is stored in.
    TattooZoneFields = {
        TattooGlobals.ZONE1: 'TattooChest',
        TattooGlobals.ZONE2: 'TattooZone2',
        TattooGlobals.ZONE3: 'TattooZone3',
        TattooGlobals.ZONE4: 'TattooZone4'}

    def __getTattooDNA(self, gender, uid):
        # the same values TattooStoreGUI.closePanel gives the avatar's DNA...
        tattoo = TattooGlobals.tattoos.get(uid)
        if tattoo is not None:
            if gender == 'm':
                offsetIndex = 5
            else:
                offsetIndex = 6

            offsetx = tattoo[offsetIndex][0]
            offsety = tattoo[offsetIndex][1]
            scale = tattoo[offsetIndex][2]
            rotate = tattoo[offsetIndex][3]
            tattooId = tattoo[1]
        else:
            offsetx = 0
            offsety = 0
            scale = 1.0
            rotate = 0
            tattooId = 0

        S = Vec2(1 / float(scale), 1 / float(scale))
        Iv = Vec2(offsetx, offsety)
        Vm = Vec2(math.sin(rotate * math.pi / 180.0), math.cos(rotate * math.pi / 180.0))
        Vms = Vec2(Vm[0] * S[0], Vm[1] * S[1])
        Vn = Vec2(Vm[1], -Vm[0])
        Vns = Vec2(Vn[0] * S[0], Vn[1] * S[1])
        F = Vec2(-Vns.dot(Iv) + 0.5, -Vms.dot(Iv) + 0.5)
        return [tattooId, F[0], F[1], S[0], rotate, 0]

    def __isWearingTattoo(self, avatar, uid):
        tattoo = TattooGlobals.tattoos[uid]
        fieldName = self.TattooZoneFields.get(tattoo[0])
        if not fieldName:
            return False

        return getattr(avatar, 'get' + fieldName)()[0] == tattoo[1]

    def __getTattooStore(self, currencyType):
        # the PvP rewards shopkeeper sells the privateer tattoos for infamy,
        # see DistributedShopKeeper.startShopping and TattooStoreGUI.getMoney...
        if currencyType:
            return InteractGlobals.PVP_REWARDS_TATTOO, PiratesGlobals.PRIVATEER_TATTOOS, InventoryType.PVPCurrentInfamy

        return InteractGlobals.TATTOO_STORE, self.getShopId(), InventoryType.GoldInPocket

    def requestTattooList(self, avId):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.notify.warning('Failed to requestTattooList for non-existant avatar %d!' %
                avatarId)

            return

        self.air.accessoriesManager.getTattoos(avatarId,
            lambda tattoos: self.d_responseTattooList(avatarId, tattoos or [-1]))

    def d_responseTattooList(self, avatarId, tattoos=[-1]):
        # the store GUI ignores an empty wardrobe, so an avatar that owns no
        # tattoos is sent [-1] instead...
        self.sendUpdateToAvatarId(avatarId, 'responseTattooList', [avatarId, tattoos])

    def requestTattoo(self, purchases, selling, currencyType=0):
        if currencyType not in (0, 1):
            avatarId = self.air.getAvatarIdFromSender()
            self.air.logPotentialHacker(
                message='Received requestTattoo with an unknown currency!',
                avatarId=avatarId,
                currencyType=currencyType)

            return

        storeType, shopId, currency = self.__getTattooStore(currencyType)
        avatar, inventory = self.__getStoreAvatar('requestTattoo', storeType)
        if not inventory:
            return

        avatarId = avatar.doId
        self.air.accessoriesManager.getTattoos(avatarId,
            lambda tattoos: self.__handleTattoo(avatarId, purchases, selling, shopId, currency, tattoos),
            useCache=True)

    def __handleTattoo(self, avatarId, purchases, selling, shopId, currency, tattoos):
        avatar = self.air.doId2do.get(avatarId)
        inventory = self.air.inventoryManager.getInventory(avatarId)
        if not avatar or not inventory:
            return

        storeItems = TattooGlobals.stores.get(shopId, [])
        sold = []
        takeOff = []
        for uid in selling:
            if uid not in TattooGlobals.tattoos or uid not in tattoos or uid in sold:
                self.__rejectAccessories(avatarId, 'Received requestTattoo sell for a tattoo the avatar does not own!',
                    uid=uid)

                return

            if self.__isWearingTattoo(avatar, uid):
                takeOff.append(TattooGlobals.tattoos[uid][0])

            sold.append(uid)

        bought = []
        for uid in purchases:
            if uid not in TattooGlobals.tattoos or uid not in storeItems or uid in tattoos or uid in bought or \
                    not self.__isHolidayItemAvailable(TattooGlobals.tattoos[uid][7]):
                self.__rejectAccessories(avatarId, 'Received requestTattoo buy for a tattoo this shop does not sell!',
                    uid=uid)

                return

            bought.append(uid)

        remaining = [uid for uid in tattoos if uid not in sold] + bought
        for zone in set([TattooGlobals.tattoos[uid][0] for uid in bought]):
            count = len([uid for uid in remaining if uid in TattooGlobals.tattoos and TattooGlobals.tattoos[uid][0] == zone])
            if count > PiratesGlobals.WARDROBE_LIMIT_TATTOO:
                self.d_makeSaleResponse(avatarId, RejectCode.OVERFLOW)
                return

        # tattoos are bought back at a quarter of their value, see TattooStoreGUI.setPage...
        prices = dict([(uid, self.getCustomizationCost(avatar, TattooGlobals.tattoos[uid][4])) for uid in bought])
        gains = dict([(uid, int(self.getCustomizationCost(avatar, TattooGlobals.tattoos[uid][4]) * 0.25)) for uid in sold])
        totalCost = sum(prices.values())
        totalGain = sum(gains.values())
        currentMoney = self.__getCurrency(inventory, currency)
        if totalCost > currentMoney + totalGain:
            self.__rejectAccessories(avatarId, 'Received requestTattoo buy for tattoos the avatar can not afford!',
                currentMoney=currentMoney, totalCost=totalCost)

            return

        self.__setCurrency(inventory, currency, currentMoney + totalGain - totalCost)

        for uid in sold:
            self.air.accessoriesManager.removeTattoo(avatarId, uid, refund=gains[uid],
                callback=lambda success, uid=uid: self.__handleWardrobeChanged(avatarId, success,
                    currency, -gains[uid], 'requestTattoo'))

        for uid in bought:
            self.air.accessoriesManager.addTattoo(avatarId, uid, cost=prices[uid], location=shopId,
                callback=lambda success, uid=uid: self.__handleWardrobeChanged(avatarId, success,
                    currency, prices[uid], 'requestTattoo'))

        if takeOff:
            empty = self.__getTattooDNA(avatar.getGender(), 0)
            for zone in takeOff:
                getattr(avatar, 'set' + self.TattooZoneFields[zone])(*empty)

            avatar.d_setTattoos()

        # Log transaction for analytics and GM purposes
        self.logShopkeepTransaction(
            type='requestTattoo',
            buying=bought,
            selling=sold,
            currency=currency,
            price=totalCost,
            gain=totalGain,
            purchaser=avatarId)

        self.d_makeSaleResponse(avatarId, self.SALE_SUCCESS)

    def d_makeTattooResponse(self, avatarId, tattoo, zone, success):
        self.sendUpdateToAvatarId(avatarId, 'makeTattooResponse', [tattoo, zone, success])

    def requestTattooEquip(self, tattoos):
        # the privateer tattoo store is run by the PvP rewards shopkeeper...
        storeType = InteractGlobals.TATTOO_STORE
        menu = None
        if getattr(self, 'avatarType', None) is not None:
            menu = InteractGlobals.getNPCInteractMenu(self.avatarType)

        if menu and InteractGlobals.PVP_REWARDS_TATTOO in menu[1]:
            storeType = InteractGlobals.PVP_REWARDS_TATTOO

        avatar, inventory = self.__getStoreAvatar('requestTattooEquip', storeType)
        if not inventory:
            return

        avatarId = avatar.doId
        self.air.accessoriesManager.getTattoos(avatarId,
            lambda owned: self.__handleTattooEquip(avatarId, tattoos, owned),
            useCache=True)

    def __handleTattooEquip(self, avatarId, tattoos, owned):
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return

        gender = avatar.getGender()
        changes = []
        for zone, uid in tattoos:
            fieldName = self.TattooZoneFields.get(zone)
            if not fieldName:
                self.__rejectAccessories(avatarId, 'Received requestTattooEquip for an unknown zone!',
                    zone=zone)

                return

            # a uid of -1 removes the tattoo, see TattooStoreGUI.closePanel...
            if uid != -1:
                tattoo = TattooGlobals.tattoos.get(uid)
                if not tattoo or tattoo[0] != zone or uid not in owned:
                    self.__rejectAccessories(avatarId, 'Received requestTattooEquip for a tattoo the avatar does not own!',
                        uid=uid, zone=zone)

                    return

            changes.append((fieldName, self.__getTattooDNA(gender, uid)))

        if not changes:
            return

        for fieldName, dna in changes:
            getattr(avatar, 'set' + fieldName)(*dna)

        avatar.d_setTattoos()

    # Jeweler:

    # jewelry type -> the HumanDNA field the jewelry is stored in,
    # see JewelryStoreGUI.closePanel.
    JewelryZoneFields = {
        JewelryGlobals.LEAR: 'JewelryZone1',
        JewelryGlobals.REAR: 'JewelryZone2',
        JewelryGlobals.LBROW: 'JewelryZone3',
        JewelryGlobals.RBROW: 'JewelryZone4',
        JewelryGlobals.NOSE: 'JewelryZone5',
        JewelryGlobals.MOUTH: 'JewelryZone6',
        JewelryGlobals.LHAND: 'JewelryZone7',
        JewelryGlobals.RHAND: 'JewelryZone8'}

    def __isWearingJewelry(self, avatar, uid):
        item = JewelryGlobals.jewelry_id[uid]
        fieldName = self.JewelryZoneFields.get(item[1])
        if not fieldName:
            return False

        return list(getattr(avatar, 'get' + fieldName)()) == [item[0], item[4], item[5]]

    def requestJewelryList(self, avId):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.notify.warning('Failed to requestJewelryList for non-existant avatar %d!' %
                avatarId)

            return

        self.air.accessoriesManager.getJewelry(avatarId,
            lambda jewelry: self.d_responseJewelryList(avatarId, jewelry or [-1]))

    def d_responseJewelryList(self, avatarId, items=[-1]):
        # the store GUI ignores an empty wardrobe, so an avatar that owns no
        # jewelry is sent [-1] instead...
        self.sendUpdateToAvatarId(avatarId, 'responseJewelryList', [avatarId, items])

    def requestJewelry(self, purchases, selling):
        avatar, inventory = self.__getStoreAvatar('requestJewelry', InteractGlobals.JEWELRY_STORE)
        if not inventory:
            return

        avatarId = avatar.doId
        self.air.accessoriesManager.getJewelry(avatarId,
            lambda jewelry: self.__handleJewelry(avatarId, purchases, selling, jewelry),
            useCache=True)

    def __handleJewelry(self, avatarId, purchases, selling, jewelry):
        avatar = self.air.doId2do.get(avatarId)
        inventory = self.air.inventoryManager.getInventory(avatarId)
        if not avatar or not inventory:
            return

        gender = avatar.getGender()
        storeItems = JewelryGlobals.stores.get(self.getShopId(), [])
        sold = []
        takeOff = []
        for uid in selling:
            if uid not in JewelryGlobals.jewelry_id or uid not in jewelry or uid in sold:
                self.__rejectAccessories(avatarId, 'Received requestJewelry sell for jewelry the avatar does not own!',
                    uid=uid)

                return

            if self.__isWearingJewelry(avatar, uid):
                takeOff.append(JewelryGlobals.jewelry_id[uid][1])

            sold.append(uid)

        bought = []
        for uid in purchases:
            if uid not in JewelryGlobals.jewelry_id or uid not in storeItems or getJewelryGender(uid) != gender or \
                    uid in jewelry or uid in bought or not self.__isHolidayItemAvailable(JewelryGlobals.jewelry_id[uid][6]):
                self.__rejectAccessories(avatarId, 'Received requestJewelry buy for jewelry this shop does not sell!',
                    uid=uid)

                return

            bought.append(uid)

        remaining = [uid for uid in jewelry if uid not in sold] + bought
        for jewelryType in set([JewelryGlobals.jewelry_id[uid][1] for uid in bought]):
            count = len([uid for uid in remaining if uid in JewelryGlobals.jewelry_id and
                JewelryGlobals.jewelry_id[uid][1] == jewelryType])
            if count > PiratesGlobals.WARDROBE_LIMIT_JEWELER:
                self.d_makeSaleResponse(avatarId, RejectCode.OVERFLOW)
                return

        # jewelry is bought back at a quarter of its value, see JewelryStoreGUI.setPage...
        prices = dict([(uid, self.getCustomizationCost(avatar, JewelryGlobals.jewelry_id[uid][3])) for uid in bought])
        gains = dict([(uid, int(self.getCustomizationCost(avatar, JewelryGlobals.jewelry_id[uid][3]) * 0.25)) for uid in sold])
        totalCost = sum(prices.values())
        totalGain = sum(gains.values())
        currentGold = inventory.getGoldInPocket()
        if totalCost > currentGold + totalGain:
            self.__rejectAccessories(avatarId, 'Received requestJewelry buy for jewelry the avatar can not afford!',
                currentGold=currentGold, totalCost=totalCost)

            return

        inventory.setGoldInPocket(currentGold + totalGain - totalCost)

        for uid in sold:
            self.air.accessoriesManager.removeJewelry(avatarId, uid, refund=gains[uid],
                callback=lambda success, uid=uid: self.__handleWardrobeChanged(avatarId, success,
                    InventoryType.GoldInPocket, -gains[uid], 'requestJewelry'))

        for uid in bought:
            self.air.accessoriesManager.addJewelry(avatarId, uid, cost=prices[uid], location=self.getShopId(),
                callback=lambda success, uid=uid: self.__handleWardrobeChanged(avatarId, success,
                    InventoryType.GoldInPocket, prices[uid], 'requestJewelry'))

        if takeOff:
            for jewelryType in takeOff:
                getattr(avatar, 'set' + self.JewelryZoneFields[jewelryType])(0, 0, 0)

            avatar.d_setJewelry()

        # Log transaction for analytics and GM purposes
        self.logShopkeepTransaction(
            type='requestJewelry',
            buying=bought,
            selling=sold,
            price=totalCost,
            gain=totalGain,
            purchaser=avatarId)

        self.d_makeSaleResponse(avatarId, self.SALE_SUCCESS)

    def requestJewelryEquip(self, jewelry):
        avatar, inventory = self.__getStoreAvatar('requestJewelryEquip', InteractGlobals.JEWELRY_STORE)
        if not inventory:
            return

        avatarId = avatar.doId
        self.air.accessoriesManager.getJewelry(avatarId,
            lambda owned: self.__handleJewelryEquip(avatarId, jewelry, owned),
            useCache=True)

    def __handleJewelryEquip(self, avatarId, jewelry, owned):
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return

        changes = []
        for jewelryType, uid in jewelry:
            fieldName = self.JewelryZoneFields.get(jewelryType)
            if not fieldName:
                self.__rejectAccessories(avatarId, 'Received requestJewelryEquip for an unknown jewelry type!',
                    jewelryType=jewelryType)

                return

            # a uid of -1 removes the jewelry, see JewelryStoreGUI.closePanel...
            if uid == -1:
                changes.append((fieldName, (0, 0, 0)))
                continue

            item = JewelryGlobals.jewelry_id.get(uid)
            if not item or item[1] != jewelryType or uid not in owned:
                self.__rejectAccessories(avatarId, 'Received requestJewelryEquip for jewelry the avatar does not own!',
                    uid=uid, jewelryType=jewelryType)

                return

            changes.append((fieldName, (item[0], item[4], item[5])))

        if not changes:
            return

        for fieldName, dna in changes:
            getattr(avatar, 'set' + fieldName)(*dna)

        avatar.d_setJewelry()

    def requestBarber(self, idx, color):
        avatar, inventory = self.__getStoreAvatar('requestBarber', InteractGlobals.BARBER_STORE)
        if not inventory:
            return

        currentGold = inventory.getGoldInPocket()
        item = BarberGlobals.barber_id.get(idx, None)
        if item is None:
            self.notify.warning('Unknown barber id: %s!' % idx)

            self.d_makeBarberResponse(avatar.doId, idx, color, False)
            return

        # the barber only offers it's store's styles for the avatar's gender,
        # see BarberStoreGUI.setPage...
        if idx not in BarberGlobals.stores.get(self.getShopId(), []) or \
                (idx >= BarberGlobals.FEMALE_HAIR) != (avatar.getGender() == 'f'):
            self.air.logPotentialHacker(
                message='Received requestBarber for a style this barber does not offer!',
                avatarId=avatar.doId,
                idx=idx)

            self.d_makeBarberResponse(avatar.doId, idx, color, False)
            return

        itemId = item[0]
        itemPrice = self.getCustomizationCost(avatar, item[4])
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

        # the green hair color is only offered during saint patrick's day,
        # styles without a color choice keep the avatar's current color,
        # see BarberStoreGUI.setPage...
        colorOffered = color in availableHairColors or color == avatar.getHairColor() or (
            color == SAINT_PATRICKS_HAIR_COLOR and self.__isHolidayItemAvailable(PiratesGlobals.SAINTPATRICKSDAY))
        if not colorOffered or not self.__isHolidayItemAvailable(item[5]):
            self.air.logPotentialHacker(
                message='Received requestBarber for a style or color the barber does not offer!',
                itemId=itemId,
                itemType=itemType,
                color=color)

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

    # a ship that isn't out at sea: never launched this session (Off), or brought back
    # and put away once it's crew left it (PutAway)...
    InPortShipStates = ('Off', 'PutAway')

    def __getOwnedShip(self, avatarId, shipId, handlerName, states=InPortShipStates):
        inventory = self.air.inventoryManager.getInventory(avatarId)
        ship = self.air.doId2do.get(shipId)
        if (not inventory or not ship or
                shipId not in inventory.getShipDoIdList() or
                ship.getGameState()[0] not in states):
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

        # a sunk ship stays sunk until it is repaired, the client offers a
        # repair for any damaged ship (DistributedNPCTownfolk.computeOptions),
        # so a ship waiting at the dock can be repaired too...
        inventory, ship = self.__getOwnedShip(avatarId, shipId, 'repair',
            states=self.InPortShipStates + ('Sunk', 'Docked'))
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

        # restores the ship's hp and sp along with the hp of all of it's parts...
        ship.repairShip()

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

        # reconstruct the ship, this restores it (and all of it's parts)
        # to full health and takes it out of overhaul...
        ship.repairShip()
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

    # Trainer respecs, see DistributedNPCTownfolk.showRespecMenu:

    RespecSkills = {
        InteractGlobals.RESPEC_CUTLASS: (InventoryType.CutlassRep, InventoryType.begin_WeaponSkillCutlass,
            InventoryType.end_WeaponSkillCutlass, InventoryType.UnspentCutlass),
        InteractGlobals.RESPEC_PISTOL: (InventoryType.PistolRep, InventoryType.begin_WeaponSkillPistol,
            InventoryType.end_WeaponSkillPistol, InventoryType.UnspentPistol),
        InteractGlobals.RESPEC_DAGGER: (InventoryType.DaggerRep, InventoryType.begin_WeaponSkillDagger,
            InventoryType.end_WeaponSkillDagger, InventoryType.UnspentDagger),
        InteractGlobals.RESPEC_DOLL: (InventoryType.DollRep, InventoryType.begin_WeaponSkillDoll,
            InventoryType.end_WeaponSkillDoll, InventoryType.UnspentDoll),
        InteractGlobals.RESPEC_GRENADE: (InventoryType.GrenadeRep, InventoryType.begin_WeaponSkillGrenade,
            InventoryType.end_WeaponSkillGrenade, InventoryType.UnspentGrenade),
        InteractGlobals.RESPEC_STAFF: (InventoryType.WandRep, InventoryType.begin_WeaponSkillWand,
            InventoryType.end_WeaponSkillWand, InventoryType.UnspentWand),
        InteractGlobals.RESPEC_SAILING: (InventoryType.SailingRep, InventoryType.begin_SkillSailing,
            InventoryType.end_SkillSailing, InventoryType.UnspentSailing),
        InteractGlobals.RESPEC_CANNON: (InventoryType.CannonRep, InventoryType.begin_WeaponSkillCannon,
            InventoryType.end_WeaponSkillCannon, InventoryType.UnspentCannon)}

    def isRespecOption(self, option):
        return option in self.RespecSkills

    def handleRespec(self, avatar, inventory, option):
        # resets a weapon's skills back to their starting rank and returns the
        # spent points, every respec of a weapon costs more than the last...
        menu = InteractGlobals.getNPCInteractMenu(getattr(self, 'avatarType', None))
        if not menu or InteractGlobals.RESPEC not in menu[1] or option not in self.RespecSkills:
            self.air.logPotentialHacker(
                message='Received a respec for a shopkeeper that is not a trainer!',
                avatarId=avatar.doId,
                option=option)

            return False

        weaponRep, begin, end, unspentId = self.RespecSkills[option]
        numRespecType = getNumRespecType(weaponRep)
        numRespecs = inventory.getStackQuantity(numRespecType)
        cost = EconomyGlobals.getRespecCost(numRespecs)
        currentGold = inventory.getGoldInPocket()
        if cost > currentGold:
            self.air.logPotentialHacker(
                message='Received a respec the avatar can not afford!',
                avatarId=avatar.doId,
                currentGold=currentGold,
                cost=cost)

            return False

        # a skill's stack is it's rank plus one, the starting skills are learned
        # with the weapon, see DistributedNPCTownfolk.isRespecAvailable...
        resets = []
        refund = 0
        for skillId in range(begin, end):
            if skillId in InventoryType.DontResetSkills:
                continue

            resetAmount = 2 if skillId in InventoryType.StartingSkills else 1
            skillAmount = inventory.getStackQuantity(skillId)
            if skillAmount > resetAmount:
                resets.append((skillId, resetAmount))
                refund += skillAmount - resetAmount

        if not resets:
            return False

        inventory.setGoldInPocket(currentGold - cost)
        for skillId, resetAmount in resets:
            inventory.b_setStackQuantity(skillId, resetAmount)

        inventory.b_setStackQuantity(unspentId, inventory.getStackQuantity(unspentId) + refund)
        inventory.b_setStackQuantity(numRespecType, numRespecs + 1)
        avatar.d_spentSkillPoint(weaponRep)

        # Log transaction for analytics and GM purposes
        self.logShopkeepTransaction(
            type='respec',
            weaponRep=weaponRep,
            refund=refund,
            price=cost,
            purchaser=avatar.doId)

        return True

    def d_makeSaleResponse(self, avatarId, results):
        self.sendUpdateToAvatarId(avatarId, 'makeSaleResponse', [results])

    def logShopkeepTransaction(self, **kwargs):
        self.air.writeServerEvent('shopkeep-transaction', **kwargs)
