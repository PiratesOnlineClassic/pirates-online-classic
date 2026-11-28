import json

import semidbm

from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

from pirates.makeapirate import ClothingGlobals
from pirates.piratesbase import PiratesGlobals


# Set on starting items, the clothing an avatar was made with. The tailor
# shows these as "Starting Item" and will not buy them back.
ORIGINAL_BIT = 1 << 31


def packClothing(uid, colorId, original=0):
    value = (uid << 8) | (colorId & 0xFF)
    if original:
        value |= ORIGINAL_BIT

    return value


def unpackClothing(value):
    return ((value & ~ORIGINAL_BIT) >> 8, value & 0xFF, int(bool(value & ORIGINAL_BIT)))


class AccessoriesDB:
    """
    Simple key value bridge holding every avatar's wardrobe: the clothing,
    jewelry and tattoos it owns but is not necessarily wearing. Worn items
    live in the avatar's DNA.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('AccessoriesDB')

    def __init__(self, filename):
        self.dbm = semidbm.open(filename, 'c')

    def getWardrobe(self, avatarId):
        key = str(avatarId)
        if key not in self.dbm:
            return {'clothing': [], 'jewelry': [], 'tattoos': []}

        data = self.dbm[key]
        if isinstance(data, bytes):
            data = data.decode('utf-8')

        wardrobe = json.loads(data)
        wardrobe.setdefault('clothing', [])

        # Clothing is stored as [uid, colorId, original].
        wardrobe['clothing'] = [list(item[:2]) + [item[2] if len(item) > 2 else 0]
            for item in wardrobe['clothing']]
        wardrobe.setdefault('jewelry', [])
        wardrobe.setdefault('tattoos', [])
        return wardrobe

    def setWardrobe(self, avatarId, wardrobe):
        self.dbm[str(avatarId)] = json.dumps(wardrobe)
        if getattr(self.dbm, 'sync', None):
            self.dbm.sync()

    def close(self):
        self.dbm.close()


class AvatarAccessoriesManagerUD(DistributedObjectGlobalUD):
    """
    The accessories database. The AIs ask for an avatar's wardrobe when it
    visits a tailor, jeweler or tattoo parlor and ask for items to be added
    or removed when they are bought, sold, dropped or awarded. Every response
    goes back to the channel the request came from.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('AvatarAccessoriesManagerUD')

    # Clothing is limited per clothing type, like the tailor GUI enforces.
    # Jewelry and tattoos are limited per zone by the store GUIs, so only a
    # sanity cap is applied to the whole list here.
    ClothingLimit = PiratesGlobals.WARDROBE_LIMIT_TAILOR
    MaxItems = 64

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        self.accessoriesDB = None

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        filename = config.GetString('accessories-bridge-filename', 'astron/databases/accessories-bridge')
        self.accessoriesDB = AccessoriesDB(filename)
        self.notify.info('%s going online' % self.__class__.__name__)

    def delete(self):
        if self.accessoriesDB:
            self.accessoriesDB.close()
            self.accessoriesDB = None

        DistributedObjectGlobalUD.delete(self)

    # Helpers:

    def getClothingType(self, uid):
        item = ClothingGlobals.getItemById(uid)
        if not item:
            return None

        return item[ClothingGlobals.TYPE_INDEX]

    def canAddClothing(self, clothing, uid):
        itemType = self.getClothingType(uid)
        if itemType is None:
            return False

        count = 0
        for owned in clothing:
            if self.getClothingType(owned[0]) == itemType:
                count += 1

        return count < self.ClothingLimit

    def getClothingList(self, avatarId):
        wardrobe = self.accessoriesDB.getWardrobe(avatarId)
        return [packClothing(*item) for item in wardrobe['clothing']]

    def findClothing(self, clothing, uid, colorId):
        for item in clothing:
            if item[0] == uid and item[1] == colorId:
                return item

        return None

    def addClothing(self, avatarId, items):
        wardrobe = self.accessoriesDB.getWardrobe(avatarId)
        clothing = wardrobe['clothing']
        for uid, colorId, original in items:
            if self.findClothing(clothing, uid, colorId):
                continue

            if not self.canAddClothing(clothing, uid):
                return False

            clothing.append([uid, colorId, int(bool(original))])

        self.accessoriesDB.setWardrobe(avatarId, wardrobe)
        return True

    def removeClothing(self, avatarId, items):
        wardrobe = self.accessoriesDB.getWardrobe(avatarId)
        clothing = wardrobe['clothing']
        for uid, colorId in items:
            if not self.findClothing(clothing, uid, colorId):
                return False

        for uid, colorId in items:
            clothing.remove(self.findClothing(clothing, uid, colorId))

        self.accessoriesDB.setWardrobe(avatarId, wardrobe)
        return True

    def addItem(self, avatarId, category, itemId):
        wardrobe = self.accessoriesDB.getWardrobe(avatarId)
        items = wardrobe[category]
        if itemId in items:
            return True

        if len(items) >= self.MaxItems:
            return False

        items.append(itemId)
        self.accessoriesDB.setWardrobe(avatarId, wardrobe)
        return True

    def removeItem(self, avatarId, category, itemId):
        wardrobe = self.accessoriesDB.getWardrobe(avatarId)
        items = wardrobe[category]
        if itemId not in items:
            return False

        items.remove(itemId)
        self.accessoriesDB.setWardrobe(avatarId, wardrobe)
        return True

    def getItemList(self, avatarId, category):
        return list(self.accessoriesDB.getWardrobe(avatarId)[category])

    def reply(self, fieldName, args):
        self.sendUpdateToChannel(self.air.getMsgSender(), fieldName, args)

    # Clothing:

    def requestClothingFromDB(self, context, avatarId, accountId):
        self.reply('responseClothingFromDB', [context, self.getClothingList(avatarId)])

    def requestClothingAddDB(self, context, avatarId, accountId, items, cost, location):
        success = self.addClothing(avatarId, [(item[0], item[1], item[2]) for item in items])
        if success:
            self.air.writeServerEvent('clothingAdded', avId=avatarId, items=items, cost=cost, location=location)

        self.reply('responseClothingAddDB', [context, int(success), avatarId])

    def requestClothingDeleteDB(self, context, avatarId, accountId, items, refund):
        success = self.removeClothing(avatarId, [(item[0], item[1]) for item in items])
        if success:
            self.air.writeServerEvent('clothingRemoved', avId=avatarId, items=items, refund=refund)

        self.reply('responseClothingDeleteDB', [context, int(success), avatarId])

    def requestClothingDropDB(self, context, avatarId, accountId, gender, level):
        uid = ClothingGlobals.getRandomClothingDrop(level, gender)
        colorId = ClothingGlobals.getRandomClothingColor(level)
        success = self.addClothing(avatarId, [(uid, colorId, 0)])
        if success:
            self.air.writeServerEvent('clothingDropped', avId=avatarId, uid=uid, colorId=colorId)

        self.reply('responseClothingDropFromDB', [context, packClothing(uid, colorId), int(success)])

    def requestPaidToUnpaidRollBackDB(self, context, avatarId, accountId):
        # Accounts never lose access on this server, so nothing is rolled back.
        self.reply('responsePaidToUnpaidRollBack', [context, [], 1])

    def migrateDNAElements(self, context, avatarId, accountId, elements, location):
        """
        Sent by the AI the first time an avatar's wardrobe is loaded, with the
        clothing the avatar is wearing. These become its starting items.
        """

        if self.accessoriesDB.getWardrobe(avatarId)['clothing']:
            # Already migrated.
            return

        items = [unpackClothing(value) for value in elements]
        items = [(uid, colorId, 1) for uid, colorId, original in items if self.getClothingType(uid) is not None]
        if items and self.addClothing(avatarId, items):
            self.air.writeServerEvent('clothingMigrated', avId=avatarId, items=items, location=location)

    def sendCurrentDNAtoAccDB(self, avatarId, location):
        self.notify.debug('sendCurrentDNAtoAccDB for %d ignored' % avatarId)

    # Jewelry:

    def requestJewelryListDB(self, context, avatarId, accountId):
        self.reply('responseJewelryList', [context, self.getItemList(avatarId, 'jewelry')])

    def requestJewelryAddDB(self, context, avatarId, accountId, jewelryId, cost, location):
        success = self.addItem(avatarId, 'jewelry', jewelryId)
        self.reply('responseJewelryAddDB', [context, int(success), avatarId, jewelryId])

    def requestJewelryDeleteDB(self, context, avatarId, accountId, jewelryId, refund):
        success = self.removeItem(avatarId, 'jewelry', jewelryId)
        self.reply('responseJewelryDeleteDB', [context, int(success), avatarId, jewelryId])

    # Tattoos:

    def requestTattooListDB(self, context, avatarId, accountId):
        self.reply('responseTattooList', [context, self.getItemList(avatarId, 'tattoos')])

    def requestTattooAddDB(self, context, avatarId, accountId, tattooId, cost, location):
        success = self.addItem(avatarId, 'tattoos', tattooId)
        self.reply('responseTattooAddDB', [context, int(success), avatarId, tattooId])

    def requestTattooDeleteDB(self, context, avatarId, accountId, tattooId, refund):
        success = self.removeItem(avatarId, 'tattoos', tattooId)
        self.reply('responseTattooDelete', [context, int(success), avatarId, tattooId])
