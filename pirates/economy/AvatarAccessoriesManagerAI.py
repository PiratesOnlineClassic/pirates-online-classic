from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal

from otp.distributed.OtpDoGlobals import OTP_DO_ID_PIRATES_AWARD_MAKER
from pirates.economy import AwardGlobals
from pirates.makeapirate import ClothingGlobals, JewelryGlobals, TattooGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

# Set on starting items, see AvatarAccessoriesManagerUD.
ORIGINAL_BIT = 1 << 31


def packClothing(uid, colorId, original=0):
    value = (uid << 8) | (colorId & 0xFF)
    if original:
        value |= ORIGINAL_BIT

    return value


def unpackClothing(value):
    return ((value & ~ORIGINAL_BIT) >> 8, value & 0xFF, int(bool(value & ORIGINAL_BIT)))


def getClothingGender(uid):
    if uid >= ClothingGlobals.HAT_START_RANGE_FEMALE:
        return 'f'

    return 'm'


def getJewelryGender(uid):
    if uid >= JewelryGlobals.FEMALE_RBROW:
        return 'f'

    return 'm'


# (gender, clothing type, model, texture) -> clothing uid, used to find the
# clothing an avatar was made with.
_clothingByDNA = {}


def getClothingUidFromDNA(gender, clothingType, modelId, texId):
    if not _clothingByDNA:
        for uid, item in ClothingGlobals.UNIQUE_ID.items():
            _clothingByDNA[(getClothingGender(uid), item[0], item[1], item[2])] = uid

    return _clothingByDNA.get((gender, clothingType, modelId, texId))


def getWornClothing(avatar, clothingType):
    """
    Returns the (modelId, texId, colorId) the avatar is wearing of a type.
    """

    clothes = avatar.clothes
    if clothingType == ClothingGlobals.HAT:
        return (clothes.hat, clothes.hatTexture, clothes.hatColor)
    elif clothingType == ClothingGlobals.SHIRT:
        return (clothes.shirt, clothes.shirtTexture, clothes.shirtColor)
    elif clothingType == ClothingGlobals.VEST:
        return (clothes.vest, clothes.vestTexture, clothes.vestColor)
    elif clothingType == ClothingGlobals.COAT:
        return (clothes.coat, clothes.coatTexture, clothes.coatColor)
    elif clothingType == ClothingGlobals.PANT:
        return (clothes.pant, clothes.pantTexture, clothes.pantColor)
    elif clothingType == ClothingGlobals.BELT:
        return (clothes.belt, clothes.beltTexture, clothes.sashColor)
    elif clothingType == ClothingGlobals.SHOE:
        return (clothes.shoe, clothes.shoeTexture, clothes.shoeColor)

    return None


class AvatarAccessoriesManagerAI(DistributedObjectGlobalAI):
    """
    AI side of the accessories database. Shops use it to read and change an
    avatar's wardrobe on the UberDOG; every request carries a context so the
    response can be handed back to the callback that asked for it.

    The wardrobes of avatars on this district are cached so the shops can
    validate a transaction as soon as it arrives. Changes are applied to the
    cache straight away, and the UberDOG applies them in the order they were
    sent, so a wardrobe list requested right after a purchase includes it.

    It also hands out awards from the AwardMaker to avatars on this district.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('AvatarAccessoriesManagerAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)
        self.context = 0
        self.callbacks = {}
        self.clothing = {}
        self.jewelry = {}
        self.tattoos = {}

    def delete(self):
        self.ignoreAll()
        self.callbacks = {}
        self.clothing = {}
        self.jewelry = {}
        self.tattoos = {}
        DistributedObjectGlobalAI.delete(self)

    def getNextContext(self, callback):
        self.context = (self.context + 1) & 0xFFFFFFFF
        self.callbacks[self.context] = callback
        return self.context

    def handleResponse(self, context, *args):
        callback = self.callbacks.pop(context, None)
        if callback is None:
            # Response meant for another district, or a request that was
            # already answered.
            return

        callback(*args)

    def getAccountId(self, avatarId):
        avatar = self.air.doId2do.get(avatarId)
        if avatar and hasattr(avatar, 'getDISLid'):
            return avatar.getDISLid() or 0

        return 0

    def cacheWardrobe(self, cache, avatarId, items):
        if avatarId not in self.clothing and avatarId not in self.jewelry and avatarId not in self.tattoos:
            self.acceptOnce(self.air.getAvatarExitEvent(avatarId), self.__handleAvatarExit, extraArgs=[avatarId])

        cache[avatarId] = items

    def __handleAvatarExit(self, avatarId):
        self.clothing.pop(avatarId, None)
        self.jewelry.pop(avatarId, None)
        self.tattoos.pop(avatarId, None)

    # Clothing:

    def getDNAClothing(self, avatar):
        """
        Returns the [uid, colorId, original] items the avatar is wearing.
        """

        gender = avatar.getGender()
        items = []
        for clothingType in sorted(ClothingGlobals.CLOTHING_STRING):
            modelId, texId, colorId = getWornClothing(avatar, clothingType)
            uid = getClothingUidFromDNA(gender, clothingType, modelId, texId)
            if uid is not None:
                items.append([uid, colorId, 1])

        return items

    def getClothing(self, avatarId, callback, useCache=False):
        """
        Calls back with a list of [uid, colorId, original] items owned by the
        avatar. An avatar whose wardrobe has never been loaded starts out with
        the clothing it is wearing as its starting items.
        """

        if useCache and avatarId in self.clothing:
            callback([list(item) for item in self.clothing[avatarId]])
            return

        def handleClothing(clothing):
            clothing = [list(unpackClothing(value)) for value in clothing]
            avatar = self.air.doId2do.get(avatarId)
            if not clothing and avatar and hasattr(avatar, 'clothes'):
                clothing = self.getDNAClothing(avatar)
                if clothing:
                    self.sendUpdate('migrateDNAElements', [0, avatarId, self.getAccountId(avatarId),
                        [packClothing(*item) for item in clothing], 0])

            self.cacheWardrobe(self.clothing, avatarId, clothing)
            callback([list(item) for item in clothing])

        context = self.getNextContext(handleClothing)
        self.sendUpdate('requestClothingFromDB', [context, avatarId, self.getAccountId(avatarId)])

    def responseClothingFromDB(self, context, clothing):
        self.handleResponse(context, clothing)

    def addClothing(self, avatarId, items, cost=0, location=0, callback=None):
        """
        Adds (uid, colorId) pairs to the avatar's wardrobe and calls back with
        whether they were all added.
        """

        def handleAdded(success, avatarId):
            if not success:
                # Our cache is out of date, load it again next time.
                self.clothing.pop(avatarId, None)

            if callback:
                callback(bool(success))

        clothing = self.clothing.get(avatarId)
        if clothing is not None:
            for uid, colorId in items:
                if [uid, colorId] not in [item[:2] for item in clothing]:
                    clothing.append([uid, colorId, 0])

        elements = [[uid, colorId, 0] for uid, colorId in items]
        context = self.getNextContext(handleAdded)
        self.sendUpdate('requestClothingAddDB', [context, avatarId, self.getAccountId(avatarId), elements, cost, location])

    def responseClothingAddDB(self, context, success, avatarId):
        self.handleResponse(context, success, avatarId)

    def removeClothing(self, avatarId, items, refund=0, callback=None):
        def handleRemoved(success, avatarId):
            if not success:
                self.clothing.pop(avatarId, None)

            if callback:
                callback(bool(success))

        clothing = self.clothing.get(avatarId)
        if clothing is not None:
            removed = [[uid, colorId] for uid, colorId in items]
            self.clothing[avatarId] = [item for item in clothing if item[:2] not in removed]

        elements = [[uid, colorId, 0] for uid, colorId in items]
        context = self.getNextContext(handleRemoved)
        self.sendUpdate('requestClothingDeleteDB', [context, avatarId, self.getAccountId(avatarId), elements, refund])

    def responseClothingDeleteDB(self, context, success, avatarId):
        self.handleResponse(context, success, avatarId)

    def dropClothing(self, avatarId, gender, level, callback=None):
        """
        Gives the avatar a random clothing loot drop, calling back with the
        (uid, colorId) given or None if the wardrobe had no room.
        """

        def handleDrop(value, success):
            uid, colorId, original = unpackClothing(value)
            clothing = self.clothing.get(avatarId)
            if success and clothing is not None and [uid, colorId] not in [item[:2] for item in clothing]:
                clothing.append([uid, colorId, 0])

            if callback:
                callback((uid, colorId) if success else None)

        context = self.getNextContext(handleDrop)
        self.sendUpdate('requestClothingDropDB', [context, avatarId, self.getAccountId(avatarId), gender, level])

    def responseClothingDropFromDB(self, context, value, success):
        self.handleResponse(context, value, success)

    def responsePaidToUnpaidRollBack(self, context, clothing, success):
        self.handleResponse(context, clothing, success)

    # Jewelry:

    def getJewelry(self, avatarId, callback, useCache=False):
        """
        Calls back with the list of jewelry uids owned by the avatar.
        """

        if useCache and avatarId in self.jewelry:
            callback(list(self.jewelry[avatarId]))
            return

        def handleJewelry(jewelry):
            self.cacheWardrobe(self.jewelry, avatarId, list(jewelry))
            callback(list(jewelry))

        context = self.getNextContext(handleJewelry)
        self.sendUpdate('requestJewelryListDB', [context, avatarId, self.getAccountId(avatarId)])

    def responseJewelryList(self, context, jewelry):
        self.handleResponse(context, jewelry)

    def addJewelry(self, avatarId, jewelryId, cost=0, location=0, callback=None):
        def handleAdded(success, avatarId, jewelryId):
            if not success:
                self.jewelry.pop(avatarId, None)

            if callback:
                callback(bool(success))

        jewelry = self.jewelry.get(avatarId)
        if jewelry is not None and jewelryId not in jewelry:
            jewelry.append(jewelryId)

        context = self.getNextContext(handleAdded)
        self.sendUpdate('requestJewelryAddDB', [context, avatarId, self.getAccountId(avatarId), jewelryId, cost, location])

    def responseJewelryAddDB(self, context, success, avatarId, jewelryId):
        self.handleResponse(context, success, avatarId, jewelryId)

    def removeJewelry(self, avatarId, jewelryId, refund=0, callback=None):
        def handleRemoved(success, avatarId, jewelryId):
            if not success:
                self.jewelry.pop(avatarId, None)

            if callback:
                callback(bool(success))

        jewelry = self.jewelry.get(avatarId)
        if jewelry is not None and jewelryId in jewelry:
            jewelry.remove(jewelryId)

        context = self.getNextContext(handleRemoved)
        self.sendUpdate('requestJewelryDeleteDB', [context, avatarId, self.getAccountId(avatarId), jewelryId, refund])

    def responseJewelryDeleteDB(self, context, success, avatarId, jewelryId):
        self.handleResponse(context, success, avatarId, jewelryId)

    # Tattoos:

    def getTattoos(self, avatarId, callback, useCache=False):
        """
        Calls back with the list of tattoo uids owned by the avatar.
        """

        if useCache and avatarId in self.tattoos:
            callback(list(self.tattoos[avatarId]))
            return

        def handleTattoos(tattoos):
            self.cacheWardrobe(self.tattoos, avatarId, list(tattoos))
            callback(list(tattoos))

        context = self.getNextContext(handleTattoos)
        self.sendUpdate('requestTattooListDB', [context, avatarId, self.getAccountId(avatarId)])

    def responseTattooList(self, context, tattoos):
        self.handleResponse(context, tattoos)

    def addTattoo(self, avatarId, tattooId, cost=0, location=0, callback=None):
        def handleAdded(success, avatarId, tattooId):
            if not success:
                self.tattoos.pop(avatarId, None)

            if callback:
                callback(bool(success))

        tattoos = self.tattoos.get(avatarId)
        if tattoos is not None and tattooId not in tattoos:
            tattoos.append(tattooId)

        context = self.getNextContext(handleAdded)
        self.sendUpdate('requestTattooAddDB', [context, avatarId, self.getAccountId(avatarId), tattooId, cost, location])

    def responseTattooAddDB(self, context, success, avatarId, tattooId):
        self.handleResponse(context, success, avatarId, tattooId)

    def removeTattoo(self, avatarId, tattooId, refund=0, callback=None):
        def handleRemoved(success, avatarId, tattooId):
            if not success:
                self.tattoos.pop(avatarId, None)

            if callback:
                callback(bool(success))

        tattoos = self.tattoos.get(avatarId)
        if tattoos is not None and tattooId in tattoos:
            tattoos.remove(tattooId)

        context = self.getNextContext(handleRemoved)
        self.sendUpdate('requestTattooDeleteDB', [context, avatarId, self.getAccountId(avatarId), tattooId, refund])

    def responseTattooDelete(self, context, success, avatarId, tattooId):
        self.handleResponse(context, success, avatarId, tattooId)

    # Awards:

    def getAvatarGender(self, avatar):
        if hasattr(avatar, 'getGender'):
            return avatar.getGender()

        return None

    def requestAward(self, context, awardType, avatarId, itemId, quantity):
        """
        Sent by the AwardMaker to every district. Only the district the avatar
        is on hands the award out and answers.
        """

        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return

        replyTo = self.air.getMsgSender()

        def respond(success):
            self.d_awardResult(replyTo, context, success)
            self.air.writeServerEvent('award', avId=avatarId, awardType=awardType,
                itemId=itemId, quantity=quantity, success=success)

        if awardType in (AwardGlobals.GOLD, AwardGlobals.STACK):
            inventory = avatar.getInventory()
            if not inventory:
                respond(False)
                return

            if awardType == AwardGlobals.GOLD:
                itemId = InventoryType.GoldInPocket

            current = inventory.getStackQuantity(itemId)
            limit = inventory.getStackLimit(itemId)
            if limit and current >= limit:
                respond(False)
                return

            inventory.b_setStackQuantity(itemId, current + quantity)
            respond(True)

        elif awardType == AwardGlobals.CLOTHING:
            # The quantity of a clothing award is the color it comes in.
            if not ClothingGlobals.getItemById(itemId) or quantity not in ClothingGlobals.colorCostScaler or \
                    getClothingGender(itemId) != self.getAvatarGender(avatar):
                self.notify.warning('Invalid clothing award %d (color %d) for avatar %d!' % (itemId, quantity, avatarId))
                respond(False)
                return

            def clothingAdded(success):
                if success and hasattr(avatar, 'giveClothingMessage'):
                    avatar.giveClothingMessage(itemId, quantity)

                respond(success)

            self.addClothing(avatarId, [(itemId, quantity)], callback=clothingAdded)

        elif awardType == AwardGlobals.JEWELRY:
            if itemId not in JewelryGlobals.jewelry_id or getJewelryGender(itemId) != self.getAvatarGender(avatar):
                self.notify.warning('Invalid jewelry award %d for avatar %d!' % (itemId, avatarId))
                respond(False)
                return

            def jewelryAdded(success):
                if success and hasattr(avatar, 'giveJewelryMessage'):
                    avatar.giveJewelryMessage(itemId)

                respond(success)

            self.addJewelry(avatarId, itemId, callback=jewelryAdded)

        elif awardType == AwardGlobals.TATTOO:
            if itemId not in TattooGlobals.tattoos:
                self.notify.warning('Invalid tattoo award %d for avatar %d!' % (itemId, avatarId))
                respond(False)
                return

            def tattooAdded(success):
                if success and hasattr(avatar, 'giveTattooMessage'):
                    avatar.giveTattooMessage(itemId)

                respond(success)

            self.addTattoo(avatarId, itemId, callback=tattooAdded)

        else:
            self.notify.warning('Unsupported award type %d for avatar %d!' % (awardType, avatarId))
            respond(False)

    def d_awardResult(self, channel, context, success):
        fieldName = 'awardSuccess' if success else 'awardFailure'
        dclass = self.air.dclassesByName['AwardMaker']
        datagram = dclass.aiFormatUpdate(fieldName, OTP_DO_ID_PIRATES_AWARD_MAKER,
            channel, self.air.ourChannel, [context])
        self.air.send(datagram)
