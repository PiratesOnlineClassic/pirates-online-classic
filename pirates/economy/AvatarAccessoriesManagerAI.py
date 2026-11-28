from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal

from otp.distributed.OtpDoGlobals import OTP_DO_ID_PIRATES_AWARD_MAKER
from pirates.economy import AwardGlobals
from pirates.uberdog.UberDogGlobals import InventoryType


def unpackClothing(value):
    return (value >> 8, value & 0xFF)


class AvatarAccessoriesManagerAI(DistributedObjectGlobalAI):
    """
    AI side of the accessories database. Shops use it to read and change an
    avatar's wardrobe on the UberDOG; every request carries a context so the
    response can be handed back to the callback that asked for it.

    It also hands out awards from the AwardMaker to avatars on this district.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('AvatarAccessoriesManagerAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)
        self.context = 0
        self.callbacks = {}

    def delete(self):
        self.callbacks = {}
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

    # Clothing:

    def getClothing(self, avatarId, callback):
        """
        Calls back with a list of [uid, colorId] pairs owned by the avatar.
        """

        def handleClothing(clothing):
            callback([list(unpackClothing(value)) for value in clothing])

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
            if callback:
                callback(bool(success))

        elements = [[uid, colorId, 0] for uid, colorId in items]
        context = self.getNextContext(handleAdded)
        self.sendUpdate('requestClothingAddDB', [context, avatarId, self.getAccountId(avatarId), elements, cost, location])

    def responseClothingAddDB(self, context, success, avatarId):
        self.handleResponse(context, success, avatarId)

    def removeClothing(self, avatarId, items, refund=0, callback=None):
        def handleRemoved(success, avatarId):
            if callback:
                callback(bool(success))

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
            if callback:
                callback(unpackClothing(value) if success else None)

        context = self.getNextContext(handleDrop)
        self.sendUpdate('requestClothingDropDB', [context, avatarId, self.getAccountId(avatarId), gender, level])

    def responseClothingDropFromDB(self, context, value, success):
        self.handleResponse(context, value, success)

    def responsePaidToUnpaidRollBack(self, context, clothing, success):
        self.handleResponse(context, clothing, success)

    # Jewelry:

    def getJewelry(self, avatarId, callback):
        context = self.getNextContext(callback)
        self.sendUpdate('requestJewelryListDB', [context, avatarId, self.getAccountId(avatarId)])

    def responseJewelryList(self, context, jewelry):
        self.handleResponse(context, jewelry)

    def addJewelry(self, avatarId, jewelryId, cost=0, location=0, callback=None):
        def handleAdded(success, avatarId, jewelryId):
            if callback:
                callback(bool(success))

        context = self.getNextContext(handleAdded)
        self.sendUpdate('requestJewelryAddDB', [context, avatarId, self.getAccountId(avatarId), jewelryId, cost, location])

    def responseJewelryAddDB(self, context, success, avatarId, jewelryId):
        self.handleResponse(context, success, avatarId, jewelryId)

    def removeJewelry(self, avatarId, jewelryId, refund=0, callback=None):
        def handleRemoved(success, avatarId, jewelryId):
            if callback:
                callback(bool(success))

        context = self.getNextContext(handleRemoved)
        self.sendUpdate('requestJewelryDeleteDB', [context, avatarId, self.getAccountId(avatarId), jewelryId, refund])

    def responseJewelryDeleteDB(self, context, success, avatarId, jewelryId):
        self.handleResponse(context, success, avatarId, jewelryId)

    # Tattoos:

    def getTattoos(self, avatarId, callback):
        context = self.getNextContext(callback)
        self.sendUpdate('requestTattooListDB', [context, avatarId, self.getAccountId(avatarId)])

    def responseTattooList(self, context, tattoos):
        self.handleResponse(context, tattoos)

    def addTattoo(self, avatarId, tattooId, cost=0, location=0, callback=None):
        def handleAdded(success, avatarId, tattooId):
            if callback:
                callback(bool(success))

        context = self.getNextContext(handleAdded)
        self.sendUpdate('requestTattooAddDB', [context, avatarId, self.getAccountId(avatarId), tattooId, cost, location])

    def responseTattooAddDB(self, context, success, avatarId, tattooId):
        self.handleResponse(context, success, avatarId, tattooId)

    def removeTattoo(self, avatarId, tattooId, refund=0, callback=None):
        def handleRemoved(success, avatarId, tattooId):
            if callback:
                callback(bool(success))

        context = self.getNextContext(handleRemoved)
        self.sendUpdate('requestTattooDeleteDB', [context, avatarId, self.getAccountId(avatarId), tattooId, refund])

    def responseTattooDelete(self, context, success, avatarId, tattooId):
        self.handleResponse(context, success, avatarId, tattooId)

    # Awards:

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
            self.addClothing(avatarId, [(itemId, quantity)], callback=respond)

        elif awardType == AwardGlobals.JEWELRY:
            self.addJewelry(avatarId, itemId, callback=respond)

        elif awardType == AwardGlobals.TATTOO:
            self.addTattoo(avatarId, itemId, callback=respond)

        else:
            self.notify.warning('Unsupported award type %d for avatar %d!' % (awardType, avatarId))
            respond(False)

    def d_awardResult(self, channel, context, success):
        fieldName = 'awardSuccess' if success else 'awardFailure'
        dclass = self.air.dclassesByName['AwardMaker']
        datagram = dclass.aiFormatUpdate(fieldName, OTP_DO_ID_PIRATES_AWARD_MAKER,
            channel, self.air.ourChannel, [context])
        self.air.send(datagram)
