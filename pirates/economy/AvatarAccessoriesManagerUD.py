import json

import semidbm

from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

from pirates.makeapirate import ClothingGlobals
from pirates.piratesbase import PiratesGlobals


def packClothing(uid, colorId):
    return (uid << 8) | (colorId & 0xFF)


def unpackClothing(value):
    return (value >> 8, value & 0xFF)


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
        for ownedUid, colorId in clothing:
            if self.getClothingType(ownedUid) == itemType:
                count += 1

        return count < self.ClothingLimit

    def getClothingList(self, avatarId):
        wardrobe = self.accessoriesDB.getWardrobe(avatarId)
        return [packClothing(uid, colorId) for uid, colorId in wardrobe['clothing']]

    def addClothing(self, avatarId, items):
        wardrobe = self.accessoriesDB.getWardrobe(avatarId)
        clothing = wardrobe['clothing']
        for uid, colorId in items:
            if [uid, colorId] in clothing:
                continue

            if not self.canAddClothing(clothing, uid):
                return False

            clothing.append([uid, colorId])

        self.accessoriesDB.setWardrobe(avatarId, wardrobe)
        return True

    def removeClothing(self, avatarId, items):
        wardrobe = self.accessoriesDB.getWardrobe(avatarId)
        clothing = wardrobe['clothing']
        for uid, colorId in items:
            if [uid, colorId] not in clothing:
                return False

        for uid, colorId in items:
            clothing.remove([uid, colorId])

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
        success = self.addClothing(avatarId, [(item[0], item[1]) for item in items])
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
        success = self.addClothing(avatarId, [(uid, colorId)])
        if success:
            self.air.writeServerEvent('clothingDropped', avId=avatarId, uid=uid, colorId=colorId)

        self.reply('responseClothingDropFromDB', [context, packClothing(uid, colorId), int(success)])

    def requestPaidToUnpaidRollBackDB(self, context, avatarId, accountId):
        # Accounts never lose access on this server, so nothing is rolled back.
        self.reply('responsePaidToUnpaidRollBack', [context, [], 1])

    def migrateDNAElements(self, context, avatarId, accountId, elements, location):
        # Wardrobes start empty; there is no legacy DNA storage to migrate.
        self.notify.debug('migrateDNAElements for %d ignored' % avatarId)

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
