import dbm.dumb
import math
import os
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock

try:
    import semidbm
except ImportError:
    # semidbm is only needed by the live UberDOG; dbm.dumb has the same API.
    sys.modules['semidbm'] = types.SimpleNamespace(open=dbm.dumb.open)

from otp.uberdog.RejectCode import RejectCode
from pirates.distributed import InteractGlobals
from pirates.economy.AvatarAccessoriesManagerAI import AvatarAccessoriesManagerAI
from pirates.economy.AvatarAccessoriesManagerUD import AccessoriesDB, AvatarAccessoriesManagerUD
from pirates.economy.DistributedShopKeeperAI import DistributedShopKeeperAI
from pirates.makeapirate import ClothingGlobals, JewelryGlobals, TattooGlobals
from pirates.pirate import AvatarTypes
from pirates.pirate.HumanDNAAI import HumanDNAAI
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

SHOP_ID = PiratesGlobals.PORT_ROYAL_DEFAULTS


def storeClothing(clothingType, gender='m', count=1):
    """
    Returns (uid, colorId) pairs the Port Royal tailor sells.
    """

    female = gender == 'f'
    items = []
    for uid, colors in sorted(ClothingGlobals.stores[SHOP_ID].items()):
        item = ClothingGlobals.UNIQUE_ID.get(uid)
        if item and item[0] == clothingType and (uid >= ClothingGlobals.HAT_START_RANGE_FEMALE) == female:
            items.append((uid, colors[0]))

    return items[:count]


def clothingPrice(uid, colorId):
    return int(ClothingGlobals.UNIQUE_ID[uid][5] * ClothingGlobals.colorCostScaler[colorId])


def storeJewelry(jewelryType, gender='m', count=1):
    female = gender == 'f'
    uids = [uid for uid in JewelryGlobals.stores[SHOP_ID] if uid in JewelryGlobals.jewelry_id and
        JewelryGlobals.jewelry_id[uid][1] == jewelryType and (uid >= JewelryGlobals.FEMALE_RBROW) == female]
    return uids[:count]


def storeTattoos(shopId, zone, count=1):
    uids = [uid for uid in TattooGlobals.stores[shopId] if TattooGlobals.tattoos[uid][0] == zone]
    return uids[:count]


class FakeInventory:
    def __init__(self, gold=10000):
        self.stacks = {InventoryType.GoldInPocket: gold}

    def getGoldInPocket(self):
        return self.stacks[InventoryType.GoldInPocket]

    def setGoldInPocket(self, gold):
        self.stacks[InventoryType.GoldInPocket] = min(gold, 65000)

    def getStackQuantity(self, stackType):
        return self.stacks.get(stackType, 0)

    def b_setStackQuantity(self, stackType, quantity):
        self.stacks[stackType] = quantity


class FakePirate(HumanDNAAI):
    def __init__(self, doId, gender):
        HumanDNAAI.__init__(self, gender)
        self.doId = doId
        self.paid = True
        self.sendUpdate = Mock()

    def isPaid(self):
        return self.paid

    def getUpdate(self, fieldName):
        for call in reversed(self.sendUpdate.call_args_list):
            if call[0][0] == fieldName:
                return call[0][1]

        return None


class AccessoriesShopTests(unittest.TestCase):
    """
    Runs the shopkeeper against a real AI and UD accessories manager, wired
    to each other without a message director.
    """

    gender = 'm'

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

        self.avatar = FakePirate(1000, self.gender)
        self.inventory = FakeInventory()
        self.air = Mock()
        self.air.getAvatarIdFromSender.return_value = self.avatar.doId
        self.air.doId2do = {self.avatar.doId: self.avatar}
        self.air.inventoryManager.getInventory.side_effect = lambda avId: self.inventory

        self.ud = AvatarAccessoriesManagerUD.__new__(AvatarAccessoriesManagerUD)
        self.ud.air = Mock()
        self.ud.accessoriesDB = AccessoriesDB(os.path.join(self.tmp.name, 'accessories'))
        self.addCleanup(self.ud.accessoriesDB.close)

        self.manager = AvatarAccessoriesManagerAI.__new__(AvatarAccessoriesManagerAI)
        self.manager.air = self.air
        self.manager.context = 0
        self.manager.callbacks = {}
        self.manager.clothing = {}
        self.manager.jewelry = {}
        self.manager.tattoos = {}
        self.manager.acceptOnce = Mock()
        self.manager.sendUpdate = lambda fieldName, args: getattr(self.ud, fieldName)(*args)
        self.ud.sendUpdateToChannel = lambda channel, fieldName, args: getattr(self.manager, fieldName)(*args)
        self.air.accessoriesManager = self.manager

        self.shop = DistributedShopKeeperAI.__new__(DistributedShopKeeperAI)
        self.shop.air = self.air
        self.shop.avatarType = AvatarTypes.Tailor
        self.shop.getShopId = lambda: SHOP_ID
        self.shop.sendUpdateToAvatarId = Mock()

    def responses(self, fieldName):
        return [call[0][2] for call in self.shop.sendUpdateToAvatarId.call_args_list if call[0][1] == fieldName]

    def lastSaleResponse(self):
        return self.responses('makeSaleResponse')[-1][0]

    def gold(self):
        return self.inventory.getGoldInPocket()


class TailorTests(AccessoriesShopTests):

    def openTailor(self):
        self.shop.requestAccessoriesList(self.avatar.doId)
        return self.responses('responseClothingList')[-1][1]

    def test_wardrobe_starts_with_the_clothing_the_avatar_wears(self):
        wardrobe = self.openTailor()
        self.assertTrue(wardrobe)
        for uid, colorId, original in wardrobe:
            self.assertEqual(original, 1)
            self.assertTrue(self.shop._DistributedShopKeeperAI__isWearingClothing(self.avatar, uid, colorId))

    def test_buy_and_equip_clothing(self):
        self.openTailor()
        (uid, colorId), = storeClothing(ClothingGlobals.HAT)
        self.shop.requestAccessories([[uid, colorId, ClothingGlobals.HAT]], [])

        self.assertEqual(self.lastSaleResponse(), DistributedShopKeeperAI.SALE_SUCCESS)
        self.assertEqual(self.gold(), 10000 - clothingPrice(uid, colorId))
        self.assertIn([uid, colorId, 0], self.openTailor())

        self.shop.requestAccessoryEquip([[uid, colorId, ClothingGlobals.HAT]])
        item = ClothingGlobals.UNIQUE_ID[uid]
        self.assertEqual((self.avatar.getHatIdx(), self.avatar.getHatTexture(), self.avatar.getHatColor()),
            (item[1], item[2], colorId))

        # every client rebuilds the avatar from the molecular field...
        clothes = self.avatar.getUpdate('setClothes')
        self.assertEqual(clothes[:3], [item[1], item[2], colorId])
        self.assertEqual(self.avatar.getUpdate('setHatIdx'), [item[1]])

    def test_take_off(self):
        self.openTailor()
        (uid, colorId), = storeClothing(ClothingGlobals.HAT)
        self.shop.requestAccessories([[uid, colorId, ClothingGlobals.HAT]], [])
        self.shop.requestAccessoryEquip([[uid, colorId, ClothingGlobals.HAT]])
        self.shop.requestAccessoryEquip([[0, 0, ClothingGlobals.HAT]])
        self.assertEqual(self.avatar.getHatIdx(), 0)

        # pants can never be taken off...
        pant = self.avatar.getClothesPant()
        self.shop.requestAccessoryEquip([[0, 0, ClothingGlobals.PANT]])
        self.assertEqual(self.lastSaleResponse(), RejectCode.TIMEOUT)
        self.assertEqual(self.avatar.getClothesPant(), pant)

    def test_cannot_equip_clothing_not_owned(self):
        self.openTailor()
        (uid, colorId), = storeClothing(ClothingGlobals.HAT)
        hat = self.avatar.getHatIdx()
        self.shop.requestAccessoryEquip([[uid, colorId, ClothingGlobals.HAT]])
        self.assertEqual(self.avatar.getHatIdx(), hat)
        self.assertIsNone(self.avatar.getUpdate('setClothes'))

    def test_sell_back_for_a_quarter(self):
        self.openTailor()
        (uid, colorId), = storeClothing(ClothingGlobals.VEST)
        self.shop.requestAccessories([[uid, colorId, ClothingGlobals.VEST]], [])
        self.shop.requestAccessoryEquip([[uid, colorId, ClothingGlobals.VEST]])
        gold = self.gold()

        self.shop.requestAccessories([], [[uid, colorId, ClothingGlobals.VEST]])
        self.assertEqual(self.lastSaleResponse(), DistributedShopKeeperAI.SALE_SUCCESS)
        self.assertEqual(self.gold(), gold + int(clothingPrice(uid, colorId) * 0.25))
        self.assertNotIn(uid, [item[0] for item in self.openTailor()])

        # it was being worn, so it comes off too...
        self.assertEqual(self.avatar.getClothesVest(), [0, 0])

    def test_starting_items_are_not_bought_back(self):
        uid, colorId, original = self.openTailor()[0]
        gold = self.gold()
        self.shop.requestAccessories([], [[uid, colorId, ClothingGlobals.UNIQUE_ID[uid][0]]])
        self.assertEqual(self.lastSaleResponse(), RejectCode.TIMEOUT)
        self.assertEqual(self.gold(), gold)

    def test_invalid_purchases_are_rejected(self):
        self.openTailor()
        (uid, colorId), = storeClothing(ClothingGlobals.HAT)
        (femaleUid, femaleColorId), = storeClothing(ClothingGlobals.HAT, gender='f')
        for purchase in ([uid, colorId, ClothingGlobals.SHIRT],
                         [uid, 99, ClothingGlobals.HAT],
                         [femaleUid, femaleColorId, ClothingGlobals.HAT],
                         [0xFFFFFF, 0, ClothingGlobals.HAT]):
            self.shop.requestAccessories([purchase], [])
            self.assertEqual(self.lastSaleResponse(), RejectCode.TIMEOUT)

        self.inventory.setGoldInPocket(0)
        self.shop.requestAccessories([[uid, colorId, ClothingGlobals.HAT]], [])
        self.assertEqual(self.lastSaleResponse(), RejectCode.TIMEOUT)
        self.assertEqual(self.gold(), 0)
        self.assertNotIn(uid, [item[0] for item in self.openTailor()])

    def test_wardrobe_limit(self):
        self.openTailor()
        hats = storeClothing(ClothingGlobals.HAT, count=PiratesGlobals.WARDROBE_LIMIT_TAILOR + 1)
        self.assertEqual(len(hats), PiratesGlobals.WARDROBE_LIMIT_TAILOR + 1)
        purchases = [[uid, colorId, ClothingGlobals.HAT] for uid, colorId in hats]
        self.shop.requestAccessories(purchases, [])
        self.assertEqual(self.lastSaleResponse(), RejectCode.OVERFLOW)
        self.assertEqual(self.gold(), 10000)

        # selling one makes room...
        self.shop.requestAccessories(purchases[:-1], [])
        self.assertEqual(self.lastSaleResponse(), DistributedShopKeeperAI.SALE_SUCCESS)
        self.shop.requestAccessories(purchases[-1:], purchases[:1])
        self.assertEqual(self.lastSaleResponse(), DistributedShopKeeperAI.SALE_SUCCESS)
        owned = [item[0] for item in self.openTailor()]
        self.assertIn(hats[-1][0], owned)
        self.assertNotIn(hats[0][0], owned)

    def test_freebooters_and_other_shopkeepers_are_rejected(self):
        (uid, colorId), = storeClothing(ClothingGlobals.HAT)
        self.avatar.paid = False
        self.shop.requestAccessories([[uid, colorId, ClothingGlobals.HAT]], [])
        self.assertEqual(self.lastSaleResponse(), RejectCode.TIMEOUT)

        self.avatar.paid = True
        self.shop.avatarType = AvatarTypes.Blacksmith
        self.shop.requestAccessories([[uid, colorId, ClothingGlobals.HAT]], [])
        self.assertEqual(self.lastSaleResponse(), RejectCode.TIMEOUT)
        self.assertEqual(self.gold(), 10000)

    def test_failed_wardrobe_change_is_refunded(self):
        self.openTailor()
        (uid, colorId), = storeClothing(ClothingGlobals.HAT)
        self.ud.addClothing = lambda avatarId, items: False
        self.shop.requestAccessories([[uid, colorId, ClothingGlobals.HAT]], [])
        self.assertEqual(self.gold(), 10000)
        self.assertNotIn(self.avatar.doId, self.manager.clothing)


class FemaleTailorTests(AccessoriesShopTests):
    gender = 'f'

    def test_shirt_can_not_be_taken_off(self):
        self.shop.requestAccessoriesList(self.avatar.doId)
        shirt = self.avatar.getClothesShirt()
        self.shop.requestAccessoryEquip([[0, 0, ClothingGlobals.SHIRT]])
        self.assertEqual(self.lastSaleResponse(), RejectCode.TIMEOUT)
        self.assertEqual(self.avatar.getClothesShirt(), shirt)


class JewelerTests(AccessoriesShopTests):

    def setUp(self):
        AccessoriesShopTests.setUp(self)
        self.shop.avatarType = AvatarTypes.Jeweler

    def openJeweler(self):
        self.shop.requestJewelryList(self.avatar.doId)
        return self.responses('responseJewelryList')[-1][1]

    def test_empty_wardrobe_still_opens_the_store(self):
        self.assertEqual(self.openJeweler(), [-1])

    def test_buy_equip_and_sell(self):
        self.openJeweler()
        uid, = storeJewelry(JewelryGlobals.LEAR)
        item = JewelryGlobals.jewelry_id[uid]
        self.shop.requestJewelry([uid], [])
        self.assertEqual(self.lastSaleResponse(), DistributedShopKeeperAI.SALE_SUCCESS)
        self.assertEqual(self.gold(), 10000 - item[3])
        self.assertEqual(self.openJeweler(), [uid])

        self.shop.requestJewelryEquip([[JewelryGlobals.LEAR, uid]])
        self.assertEqual(self.avatar.getJewelryZone1(), [item[0], item[4], item[5]])
        self.assertEqual(self.avatar.getUpdate('setJewelry')[:3], [item[0], item[4], item[5]])

        gold = self.gold()
        self.shop.requestJewelry([], [uid])
        self.assertEqual(self.gold(), gold + int(item[3] * 0.25))
        self.assertEqual(self.openJeweler(), [-1])
        self.assertEqual(self.avatar.getJewelryZone1(), [0, 0, 0])

    def test_take_off(self):
        self.openJeweler()
        uid, = storeJewelry(JewelryGlobals.NOSE)
        self.shop.requestJewelry([uid], [])
        self.shop.requestJewelryEquip([[JewelryGlobals.NOSE, uid]])
        self.shop.requestJewelryEquip([[JewelryGlobals.NOSE, -1]])
        self.assertEqual(self.avatar.getJewelryZone5(), [0, 0, 0])

    def test_invalid_requests_are_rejected(self):
        self.openJeweler()
        uid, = storeJewelry(JewelryGlobals.LEAR)
        femaleUid, = storeJewelry(JewelryGlobals.LEAR, gender='f')

        self.shop.requestJewelryEquip([[JewelryGlobals.LEAR, uid]])
        self.assertEqual(self.avatar.getJewelryZone1(), [0, 0, 0])

        self.shop.requestJewelry([femaleUid], [])
        self.assertEqual(self.lastSaleResponse(), RejectCode.TIMEOUT)

        self.shop.requestJewelry([], [uid])
        self.assertEqual(self.lastSaleResponse(), RejectCode.TIMEOUT)

        self.shop.requestJewelry([uid], [])
        self.shop.requestJewelryEquip([[JewelryGlobals.REAR, uid]])
        self.assertEqual(self.avatar.getJewelryZone2(), [0, 0, 0])
        self.assertEqual(self.gold(), 10000 - JewelryGlobals.jewelry_id[uid][3])

    def test_wardrobe_limit(self):
        uids = storeJewelry(JewelryGlobals.LEAR, count=PiratesGlobals.WARDROBE_LIMIT_JEWELER + 1)
        self.assertEqual(len(uids), PiratesGlobals.WARDROBE_LIMIT_JEWELER + 1)
        self.openJeweler()
        self.shop.requestJewelry(uids, [])
        self.assertEqual(self.lastSaleResponse(), RejectCode.OVERFLOW)
        self.assertEqual(self.openJeweler(), [-1])


class TattooTests(AccessoriesShopTests):

    def setUp(self):
        AccessoriesShopTests.setUp(self)
        self.shop.avatarType = AvatarTypes.Tattoo

    def openParlor(self):
        self.shop.requestTattooList(self.avatar.doId)
        return self.responses('responseTattooList')[-1][1]

    def expectedDNA(self, uid):
        # the same math as TattooStoreGUI.closePanel...
        tattoo = TattooGlobals.tattoos[uid]
        offsetx, offsety, scale, rotate = tattoo[5]
        S = 1 / float(scale)
        Vm = (math.sin(rotate * math.pi / 180.0), math.cos(rotate * math.pi / 180.0))
        Vn = (Vm[1], -Vm[0])
        F = (-(Vn[0] * S * offsetx + Vn[1] * S * offsety) + 0.5, -(Vm[0] * S * offsetx + Vm[1] * S * offsety) + 0.5)
        return [tattoo[1], F[0], F[1], S, rotate, 0]

    def test_buy_equip_and_sell(self):
        self.assertEqual(self.openParlor(), [-1])
        uid, = storeTattoos(SHOP_ID, TattooGlobals.ZONE2)
        price = TattooGlobals.tattoos[uid][4]
        self.shop.requestTattoo([uid], [], 0)
        self.assertEqual(self.lastSaleResponse(), DistributedShopKeeperAI.SALE_SUCCESS)
        self.assertEqual(self.gold(), 10000 - price)
        self.assertEqual(self.openParlor(), [uid])

        self.shop.requestTattooEquip([[TattooGlobals.ZONE2, uid]])
        for value, expected in zip(self.avatar.getTattooZone2(), self.expectedDNA(uid)):
            self.assertAlmostEqual(value, expected, places=4)

        self.assertEqual(len(self.avatar.getUpdate('setTattoos')), 48)

        gold = self.gold()
        self.shop.requestTattoo([], [uid], 0)
        self.assertEqual(self.gold(), gold + int(price * 0.25))
        self.assertEqual(self.avatar.getTattooZone2()[0], 0)
        self.assertEqual(self.openParlor(), [-1])

    def test_privateer_tattoos_cost_infamy(self):
        uid, = storeTattoos(PiratesGlobals.PRIVATEER_TATTOOS, TattooGlobals.ZONE3)
        price = TattooGlobals.tattoos[uid][4]
        self.openParlor()

        # only the PvP rewards shopkeeper sells them...
        self.shop.requestTattoo([uid], [], 1)
        self.assertEqual(self.lastSaleResponse(), RejectCode.TIMEOUT)

        self.shop.avatarType = AvatarTypes.PvPRewards
        self.inventory.stacks[InventoryType.PVPCurrentInfamy] = price
        self.shop.requestTattoo([uid], [], 1)
        self.assertEqual(self.lastSaleResponse(), DistributedShopKeeperAI.SALE_SUCCESS)
        self.assertEqual(self.inventory.getStackQuantity(InventoryType.PVPCurrentInfamy), 0)
        self.assertEqual(self.gold(), 10000)

        self.shop.requestTattooEquip([[TattooGlobals.ZONE3, uid]])
        self.assertEqual(self.avatar.getTattooZone3()[0], TattooGlobals.tattoos[uid][1])

    def test_invalid_requests_are_rejected(self):
        self.openParlor()
        uid, = storeTattoos(SHOP_ID, TattooGlobals.ZONE1)
        self.shop.requestTattooEquip([[TattooGlobals.ZONE1, uid]])
        self.assertEqual(self.avatar.getTattooChest()[0], 0)

        self.shop.requestTattoo([uid], [], 7)
        self.air.logPotentialHacker.assert_called()

        self.shop.requestTattoo([uid], [], 0)
        self.shop.requestTattooEquip([[TattooGlobals.ZONE2, uid]])
        self.assertEqual(self.avatar.getTattooZone2()[0], 0)

        self.inventory.setGoldInPocket(0)
        other, = storeTattoos(SHOP_ID, TattooGlobals.ZONE4)
        self.shop.requestTattoo([other], [], 0)
        self.assertEqual(self.lastSaleResponse(), RejectCode.TIMEOUT)
        self.assertEqual(self.openParlor(), [uid])


class DCTests(AccessoriesShopTests):
    """
    The fields we send pack with the dc file the client uses.
    """

    def setUp(self):
        AccessoriesShopTests.setUp(self)
        from panda3d.direct import DCFile
        self.dcFile = DCFile()
        root = os.path.join(os.path.dirname(__file__), '..', '..', 'astron', 'dclass')
        self.assertTrue(self.dcFile.read(os.path.join(root, 'otp.dc')))
        self.assertTrue(self.dcFile.read(os.path.join(root, 'pirates.dc')))

    def pack(self, className, fieldName, args):
        from panda3d.direct import DCPacker
        field = self.dcFile.getClassByName(className).getFieldByName(fieldName)
        packer = DCPacker()
        packer.beginPack(field)
        field.packArgs(packer, args)
        self.assertTrue(packer.endPack(), fieldName)

        unpacker = DCPacker()
        unpacker.setUnpackData(packer.getBytes())
        unpacker.beginUnpack(field)
        args = field.unpackArgs(unpacker)
        self.assertTrue(unpacker.endUnpack(), fieldName)
        return args

    def test_clothing_list_unpacks_as_the_tailor_reads_it(self):
        self.shop.requestAccessoriesList(self.avatar.doId)
        args = self.responses('responseClothingList')[-1]
        avatarId, wardrobe = self.pack('DistributedShopKeeper', 'responseClothingList', args)
        self.assertEqual(wardrobe, args[1])

        # AccessoriesStoreGUI.setPage compares [uid, colorId] == item[:2],
        # which only holds for lists...
        for item in wardrobe:
            self.assertIsInstance(item, list)
            self.assertEqual(len(item), 3)

    def test_dna_updates_pack(self):
        self.avatar.d_setClothes()
        self.avatar.d_setJewelry()
        self.avatar.d_setTattoos()
        for call in self.avatar.sendUpdate.call_args_list:
            fieldName, args = call[0]
            self.pack('DistributedPlayerPirate', fieldName, args)


if __name__ == '__main__':
    unittest.main()
