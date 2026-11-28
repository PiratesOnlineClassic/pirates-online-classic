import sys
import types
import unittest
from unittest.mock import Mock, patch

import pirates.battle
import pirates.reputation
from otp.uberdog.RejectCode import RejectCode
from pirates.distributed import InteractGlobals
from pirates.economy import EconomyGlobals
from pirates.makeapirate import BarberGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.economy.EconomyGlobals import ItemId
from pirates.economy.DistributedShopKeeperAI import DistributedShopKeeperAI
from pirates.pirate import AvatarTypes
from pirates.uberdog.UberDogGlobals import InventoryType, InventoryCategory


class FakeInventory:
    def __init__(self, gold=1000, stacks=None, limits=None, ships=None, shipLimit=3):
        self.stacks = {InventoryType.GoldInPocket: gold}
        self.stacks.update(stacks or {})
        self.limits = {InventoryType.GoldInPocket: 65000}
        self.limits.update(limits or {})
        self.ships = list(ships or [])
        self.shipLimit = shipLimit
        self.accumulators = {}

    def getGoldInPocket(self):
        return self.stacks[InventoryType.GoldInPocket]

    def setGoldInPocket(self, gold):
        self.stacks[InventoryType.GoldInPocket] = min(gold, 65000)

    def getStackQuantity(self, stackType):
        return self.stacks.get(stackType, 0)

    def b_setStackQuantity(self, stackType, quantity):
        self.stacks[stackType] = quantity

    def getStackLimit(self, stackType):
        return self.limits.get(stackType, 0)

    def b_setStackLimit(self, stackType, limit):
        self.limits[stackType] = limit

    def getAccumulator(self, accumulatorType):
        return self.accumulators.get(accumulatorType, 0)

    def getShipDoIdList(self):
        return self.ships

    def setShipDoIdList(self, ships):
        self.ships = ships

    def getCategoryLimit(self, category):
        assert category == InventoryCategory.SHIPS
        return self.shipLimit


class ShopKeeperAITests(unittest.TestCase):

    def setUp(self):
        self.avatar = types.SimpleNamespace(doId=1000, isPaid=lambda: True,
            b_setHairHair=Mock(), b_setHairBeard=Mock(), b_setHairMustache=Mock(), b_setHairColor=Mock())
        self.inventory = FakeInventory()
        self.air = Mock()
        self.air.getAvatarIdFromSender.return_value = self.avatar.doId
        self.holidays = set()
        self.air.newsManager.isHolidayActive.side_effect = lambda holidayId: holidayId in self.holidays
        self.air.doId2do = {self.avatar.doId: self.avatar}
        self.air.inventoryManager.getInventory.side_effect = lambda avId: self.inventory
        self.shop = DistributedShopKeeperAI.__new__(DistributedShopKeeperAI)
        self.shop.air = self.air
        self.shop.sendUpdateToAvatarId = Mock()
        self.shop.sendUpdate = Mock()

        # WeaponGlobals requires game resources, provide the rep lookups we use
        weaponGlobals = types.ModuleType('pirates.battle.WeaponGlobals')
        weaponGlobals.getRepId = lambda itemId: {
            ItemId.CUTLASS_L2: InventoryType.CutlassRep,
            ItemId.CUTLASS_L3: InventoryType.CutlassRep,
            ItemId.PISTOL_POUCH_L1: InventoryType.PistolRep}.get(itemId, 0)
        weaponGlobals.getSkillIdForAmmoSkillId = lambda itemId: {
            ItemId.VENOMSHOT: InventoryType.PistolVenomShot}.get(itemId)
        repGlobals = types.ModuleType('pirates.reputation.ReputationGlobals')
        repGlobals.getLevelFromTotalReputation = lambda repId, rep: (rep // 100, 0)
        self.modules = patch.dict(sys.modules, {
            'pirates.battle.WeaponGlobals': weaponGlobals,
            'pirates.reputation.ReputationGlobals': repGlobals})
        self.modules.start()
        self.addCleanup(self.modules.stop)
        for package, name, module in ((pirates.battle, 'WeaponGlobals', weaponGlobals),
                                      (pirates.reputation, 'ReputationGlobals', repGlobals)):
            patcher = patch.object(package, name, module, create=True)
            patcher.start()
            self.addCleanup(patcher.stop)

    def lastResponse(self):
        return self.shop.sendUpdateToAvatarId.call_args[0]

    def test_shelves_follow_the_client_shopkeeper_types(self):
        self.shop.avatarType = AvatarTypes.Gypsy
        self.assertIn(ItemId.POTION_1, self.shop.getShopInventory())
        self.assertNotIn(ItemId.CUTLASS_L2, self.shop.getShopInventory())
        self.shop.avatarType = AvatarTypes.Shipwright
        self.assertEqual(self.shop.getShopInventory(), EconomyGlobals.SHIP_SHELF)
        self.shop.avatarType = AvatarTypes.Commoner
        self.assertEqual(self.shop.getShopInventory(), [])

    def test_ammo_bundle_is_priced_and_sized_by_the_economy(self):
        self.shop.avatarType = AvatarTypes.Gunsmith
        self.inventory.limits[ItemId.VENOMSHOT] = 100
        self.inventory.stacks[InventoryType.PistolToken] = 1
        self.inventory.stacks[InventoryType.PistolVenomShot] = 2

        # the client controlled quantity is ignored
        self.shop.requestMakeSale([[ItemId.VENOMSHOT, 9999]], [], [])

        self.assertEqual(self.lastResponse(), (1000, 'makeSaleResponse', [DistributedShopKeeperAI.SALE_COMPLETE]))
        self.assertEqual(self.inventory.getStackQuantity(ItemId.VENOMSHOT), 25)
        self.assertEqual(self.inventory.getGoldInPocket(), 1000 - int(0.15 * 25))

    def test_cart_is_rejected_as_a_whole_when_unaffordable(self):
        self.shop.avatarType = AvatarTypes.Gypsy
        self.inventory.setGoldInPocket(10)
        self.inventory.limits[ItemId.POTION_5] = 3

        self.shop.requestMakeSale([[ItemId.POTION_5, 1]], [], [])

        self.assertEqual(self.lastResponse(), (1000, 'makeSaleResponse', [RejectCode.TIMEOUT]))
        self.assertEqual(self.inventory.getStackQuantity(ItemId.POTION_5), 0)
        self.assertEqual(self.inventory.getGoldInPocket(), 10)

    def test_items_not_on_the_shelf_are_rejected(self):
        self.shop.avatarType = AvatarTypes.Gypsy

        self.shop.requestMakeSale([[ItemId.BLACK_PEARL, 1]], [], [])

        self.assertEqual(self.lastResponse(), (1000, 'makeSaleResponse', [RejectCode.TIMEOUT]))
        self.air.shipLoader.createShip.assert_not_called()

    def test_weapon_requires_training_level_and_is_unique(self):
        self.shop.avatarType = AvatarTypes.Blacksmith
        self.inventory.limits[ItemId.CUTLASS_L2] = 1

        self.shop.requestMakeSale([[ItemId.CUTLASS_L2, 1]], [], [])
        self.assertEqual(self.lastResponse()[2], [RejectCode.TIMEOUT])

        self.inventory.stacks[InventoryType.CutlassToken] = 1
        self.shop.requestMakeSale([[ItemId.CUTLASS_L2, 1]], [], [])
        self.assertEqual(self.lastResponse()[2], [RejectCode.TIMEOUT])

        self.inventory.accumulators[InventoryType.CutlassRep] = 500
        self.shop.requestMakeSale([[ItemId.CUTLASS_L2, 1], [ItemId.CUTLASS_L2, 1]], [], [])
        self.assertEqual(self.lastResponse()[2], [RejectCode.OVERFLOW])

        self.shop.requestMakeSale([[ItemId.CUTLASS_L2, 1]], [], [])
        self.assertEqual(self.lastResponse()[2], [DistributedShopKeeperAI.SALE_COMPLETE])
        self.assertEqual(self.inventory.getStackQuantity(ItemId.CUTLASS_L2), 1)
        self.assertEqual(self.inventory.getGoldInPocket(), 800)

    def test_pouch_raises_ammo_limits(self):
        self.shop.avatarType = AvatarTypes.Gunsmith
        self.inventory.stacks[InventoryType.PistolToken] = 1
        self.inventory.limits[ItemId.PISTOL_POUCH_L1] = 1
        self.inventory.limits[ItemId.VENOMSHOT] = 100
        self.shop.requestMakeSale([[ItemId.PISTOL_POUCH_L1, 1]], [], [])
        self.assertEqual(self.lastResponse()[2], [RejectCode.TIMEOUT])

        self.inventory.accumulators[InventoryType.PistolRep] = 700
        self.shop.requestMakeSale([[ItemId.PISTOL_POUCH_L1, 1]], [], [])

        self.assertEqual(self.lastResponse()[2], [DistributedShopKeeperAI.SALE_COMPLETE])
        self.assertEqual(self.inventory.getStackLimit(ItemId.VENOMSHOT), 125)

    def test_ship_purchase_checks_limit_before_creating(self):
        self.shop.avatarType = AvatarTypes.Shipwright
        self.inventory.stacks[InventoryType.NewShipToken] = 1
        self.inventory.ships = [1, 2, 3]

        self.shop.requestMakeSale([[ItemId.INTERCEPTOR_L1, 1]], [], [])
        self.assertEqual(self.lastResponse()[2], [RejectCode.OVERFLOW])
        self.air.shipLoader.createShip.assert_not_called()

        self.inventory.ships = []
        self.shop.requestMakeSale([[ItemId.INTERCEPTOR_L1, 1]], [], [])
        self.assertEqual(self.lastResponse()[2], [DistributedShopKeeperAI.SALE_COMPLETE])
        self.air.shipLoader.createShip.assert_called_once()
        self.assertEqual(self.air.shipLoader.createShip.call_args[0], (self.avatar, ItemId.INTERCEPTOR_L1, ''))
        self.assertEqual(self.inventory.getGoldInPocket(), 900)
        self.assertNotIn(ItemId.INTERCEPTOR_L1, self.inventory.stacks)

    def test_freebooter_can_only_buy_starter_ships(self):
        self.shop.avatarType = AvatarTypes.Shipwright
        self.avatar.isPaid = lambda: False
        self.inventory.stacks[InventoryType.NewShipToken] = 1

        self.shop.requestMakeSale([[ItemId.WARSHIP_L1, 1]], [], [])

        self.assertEqual(self.lastResponse()[2], [RejectCode.TIMEOUT])
        self.air.shipLoader.createShip.assert_not_called()

    def test_selling_requires_the_item_and_pays_half(self):
        self.shop.avatarType = AvatarTypes.Gypsy
        self.shop.requestMakeSale([], [[ItemId.POTION_4, 1]], [])
        self.assertEqual(self.lastResponse()[2], [RejectCode.TIMEOUT])

        self.inventory.stacks[ItemId.POTION_4] = 2
        self.shop.requestMakeSale([], [[ItemId.POTION_4, 2]], [])
        self.assertEqual(self.lastResponse()[2], [DistributedShopKeeperAI.SALE_COMPLETE])
        self.assertEqual(self.inventory.getStackQuantity(ItemId.POTION_4), 0)
        self.assertEqual(self.inventory.getGoldInPocket(), 1015)

    def test_missing_avatar_does_not_crash(self):
        self.air.doId2do = {}
        self.shop.requestMakeSale([[ItemId.POTION_1, 1]], [], [])
        self.shop.requestBarber(0, 0)
        self.shop.requestMusic(InventoryType.Song_1)
        self.shop.sendUpdateToAvatarId.assert_not_called()

    def openBarber(self, gender='m'):
        self.shop.avatarType = AvatarTypes.Barber
        self.shop.getShopId = lambda: PiratesGlobals.PORT_ROYAL_DEFAULTS
        self.avatar.getGender = lambda: gender
        self.avatar.getHairColor = lambda: 0

    def test_barber_sends_barber_response(self):
        self.openBarber()
        self.shop.requestBarber(1, 3)

        self.avatar.b_setHairHair.assert_called_once_with(1)
        self.avatar.b_setHairColor.assert_called_once_with(3)
        self.assertEqual(self.lastResponse(), (1000, 'makeBarberResponse', [1, 3, True]))
        self.assertEqual(self.inventory.getGoldInPocket(), 800)

    def test_barber_green_hair_only_during_saint_patricks_day(self):
        self.openBarber()
        self.air.newsManager.isHolidayActive.return_value = False
        self.shop.requestBarber(1, 8)
        self.avatar.b_setHairColor.assert_not_called()
        self.assertEqual(self.lastResponse(), (1000, 'makeBarberResponse', [1, 8, False]))
        self.assertEqual(self.inventory.getGoldInPocket(), 1000)

        self.air.newsManager.isHolidayActive.side_effect = lambda holidayId: holidayId == PiratesGlobals.SAINTPATRICKSDAY
        self.shop.requestBarber(1, 8)
        self.avatar.b_setHairColor.assert_called_once_with(8)

        # an avatar may keep the green it already has once the holiday is over...
        self.air.newsManager.isHolidayActive.side_effect = None
        self.avatar.getHairColor = lambda: 8
        self.shop.requestBarber(1, 8)
        self.assertEqual(self.lastResponse(), (1000, 'makeBarberResponse', [1, 8, True]))

        self.shop.requestBarber(1, 9)
        self.assertEqual(self.lastResponse(), (1000, 'makeBarberResponse', [1, 9, False]))

    def test_barber_rejects_unaffordable_style(self):
        self.openBarber()
        self.inventory.setGoldInPocket(0)
        self.shop.requestBarber(1, 3)

        self.avatar.b_setHairHair.assert_not_called()
        self.assertEqual(self.lastResponse(), (1000, 'makeBarberResponse', [1, 3, False]))

    def test_barber_only_offers_its_styles(self):
        self.openBarber(gender='f')

        # a male style, a style of no store and a color the barber does not mix
        for idx, color in ((1, 3), (BarberGlobals.FEMALE_HAIR + 9998, 3), (BarberGlobals.FEMALE_HAIR + 1, 20)):
            self.shop.requestBarber(idx, color)
            self.assertEqual(self.lastResponse(), (1000, 'makeBarberResponse', [idx, color, False]))

        self.avatar.b_setHairHair.assert_not_called()
        self.assertEqual(self.inventory.getGoldInPocket(), 1000)

        # the barber is only open to members...
        self.avatar.isPaid = lambda: False
        self.shop.requestBarber(BarberGlobals.FEMALE_HAIR + 1, 3)
        self.assertEqual(self.lastResponse(), (1000, 'makeSaleResponse', [RejectCode.TIMEOUT]))

        # ...unless it is the all access weekend
        self.holidays.add(PiratesGlobals.ALLACCESSWEEKEND)
        self.shop.requestBarber(BarberGlobals.FEMALE_HAIR + 1, 3)
        self.assertEqual(self.lastResponse()[1:], ('makeBarberResponse', [BarberGlobals.FEMALE_HAIR + 1, 3, True]))

    def test_barber_is_half_off_for_members_during_the_holiday(self):
        self.openBarber()
        self.holidays.add(PiratesGlobals.HALFOFFCUSTOMIZATION)
        self.shop.requestBarber(1, 3)

        self.assertEqual(self.inventory.getGoldInPocket(), 1000 - int(BarberGlobals.barber_id[1][4] / 2))

    def test_music_rejects_unknown_song(self):
        self.shop.avatarType = AvatarTypes.Musician
        self.shop.requestMusic(ItemId.POTION_1)
        self.shop.sendUpdate.assert_not_called()

        self.shop.requestMusic(InventoryType.Song_1)
        self.shop.sendUpdate.assert_called_once_with('playMusic', [InventoryType.Song_1])
        self.assertEqual(self.inventory.getGoldInPocket(), 995)

    def makeShip(self, shipClass=ItemId.WARSHIP_L1, state='Off'):
        ship = Mock()
        ship.getShipClass.return_value = shipClass
        ship.getGameState.return_value = [state]
        ship.getMaxHp.return_value = 1000
        ship.getHp.return_value = 0
        ship.getMaxSp.return_value = 500
        ship.getSp.return_value = 0
        ship.getHullCondition.return_value = 1 << 7 | 3
        self.air.doId2do[5000] = ship
        self.inventory.ships = [5000]
        return ship

    def test_overhaul_charges_ship_percentage_and_restores_ship(self):
        ship = self.makeShip()

        self.shop.requestPurchaseOverhaul(5000)

        self.assertEqual(self.inventory.getGoldInPocket(), 1000 - int(800 * 0.4))
        ship.repairShip.assert_called_once_with()
        ship.b_setHullCondition.assert_called_once_with(3)

    def test_overhaul_rejects_ship_not_in_bottle(self):
        ship = self.makeShip(state='Sailing')

        self.shop.requestPurchaseOverhaul(5000)

        ship.repairShip.assert_not_called()
        self.assertEqual(self.inventory.getGoldInPocket(), 1000)

    def test_sunk_ship_can_be_repaired_but_not_a_sailing_one(self):
        ship = self.makeShip(state='Sailing')
        self.shop.requestPurchaseRepair(5000)
        ship.repairShip.assert_not_called()
        self.assertEqual(self.lastResponse(), (1000, 'makeSaleResponse', [RejectCode.TIMEOUT]))

        ship = self.makeShip(state='Sunk')
        self.shop.requestPurchaseRepair(5000)
        ship.repairShip.assert_called_once_with()
        self.assertEqual(self.lastResponse(), (1000, 'responseShipRepair', [5000]))
        self.assertLess(self.inventory.getGoldInPocket(), 1000)

    def test_sell_ship_pays_half_and_removes_ship(self):
        self.inventory.setShipDoIdList = Mock()
        ship = self.makeShip()

        self.shop.requestSellShip(5000)

        self.inventory.setShipDoIdList.assert_called_once_with([])
        self.assertEqual(self.inventory.getGoldInPocket(), 1400)
        ship.requestDelete.assert_called_once_with()

    def test_bartender_has_no_store(self):
        self.shop.avatarType = AvatarTypes.Bartender
        self.assertEqual(self.shop.getShopInventory(), [])

        self.shop.requestMakeSale([[ItemId.POTION_1, 1]], [], [])
        self.assertEqual(self.lastResponse()[2], [RejectCode.TIMEOUT])

    def test_ammo_requires_its_skill(self):
        self.shop.avatarType = AvatarTypes.Gunsmith
        self.inventory.limits[ItemId.VENOMSHOT] = 100

        self.shop.requestMakeSale([[ItemId.VENOMSHOT, 25]], [], [])
        self.assertEqual(self.lastResponse()[2], [RejectCode.TIMEOUT])
        self.assertEqual(self.inventory.getStackQuantity(ItemId.VENOMSHOT), 0)

        # a skill stack of one is a locked skill...
        self.inventory.stacks[InventoryType.PistolVenomShot] = 1
        self.shop.requestMakeSale([[ItemId.VENOMSHOT, 25]], [], [])
        self.assertEqual(self.lastResponse()[2], [RejectCode.TIMEOUT])

    def test_freebooters_only_buy_tonics_and_ammo(self):
        self.avatar.isPaid = lambda: False
        self.shop.avatarType = AvatarTypes.Blacksmith
        self.inventory.limits[ItemId.CUTLASS_L2] = 1
        self.inventory.stacks[InventoryType.CutlassToken] = 1
        self.inventory.accumulators[InventoryType.CutlassRep] = 500

        self.shop.requestMakeSale([[ItemId.CUTLASS_L2, 1]], [], [])
        self.assertEqual(self.lastResponse()[2], [RejectCode.TIMEOUT])
        self.assertEqual(self.inventory.getStackQuantity(ItemId.CUTLASS_L2), 0)

        self.shop.avatarType = AvatarTypes.MedicineMan
        self.inventory.limits[ItemId.POTION_1] = 5
        self.shop.requestMakeSale([[ItemId.POTION_1, 1]], [], [])
        self.assertEqual(self.lastResponse()[2], [DistributedShopKeeperAI.SALE_COMPLETE])
        self.assertEqual(self.inventory.getStackQuantity(ItemId.POTION_1), 1)

    def test_pouches_can_not_be_sold_back(self):
        self.shop.avatarType = AvatarTypes.Gunsmith
        self.inventory.stacks[ItemId.PISTOL_POUCH_L1] = 1

        self.shop.requestMakeSale([], [[ItemId.PISTOL_POUCH_L1, 1]], [])

        self.assertEqual(self.lastResponse()[2], [RejectCode.TIMEOUT])
        self.assertEqual(self.inventory.getStackQuantity(ItemId.PISTOL_POUCH_L1), 1)
        self.assertEqual(self.inventory.getGoldInPocket(), 1000)

    def test_music_is_only_played_by_musicians(self):
        self.shop.avatarType = AvatarTypes.Gunsmith
        self.shop.requestMusic(InventoryType.Song_1)

        self.shop.sendUpdate.assert_not_called()
        self.assertEqual(self.lastResponse()[2], [RejectCode.TIMEOUT])
        self.assertEqual(self.inventory.getGoldInPocket(), 1000)

        self.shop.avatarType = AvatarTypes.Musician
        self.shop.requestMusic(InventoryType.Song_1)
        self.assertEqual(self.lastResponse()[2], [DistributedShopKeeperAI.SALE_COMPLETE])

    def test_trainer_respec_resets_skills_and_refunds_points(self):
        self.shop.avatarType = AvatarTypes.Trainer
        self.inventory.stacks.update({
            InventoryType.CutlassHack: 4,
            InventoryType.CutlassSlash: 2,
            InventoryType.CutlassCleave: 3,
            InventoryType.UnspentCutlass: 1})

        self.assertTrue(self.shop.isRespecOption(InteractGlobals.RESPEC_CUTLASS))
        self.assertTrue(self.shop.handleRespec(self.avatar, self.inventory, InteractGlobals.RESPEC_CUTLASS))

        # starting skills are reset to their first rank, the rest are locked again
        self.assertEqual(self.inventory.getStackQuantity(InventoryType.CutlassHack), 2)
        self.assertEqual(self.inventory.getStackQuantity(InventoryType.CutlassSlash), 2)
        self.assertEqual(self.inventory.getStackQuantity(InventoryType.CutlassCleave), 1)
        self.assertEqual(self.inventory.getStackQuantity(InventoryType.UnspentCutlass), 1 + 2 + 2)
        self.assertEqual(self.inventory.getStackQuantity(InventoryType.NumRespecCutlass), 1)
        self.assertEqual(self.inventory.getGoldInPocket(), 1000 - EconomyGlobals.getRespecCost(0))

        # nothing left to reset, the avatar is not charged again
        self.assertFalse(self.shop.handleRespec(self.avatar, self.inventory, InteractGlobals.RESPEC_CUTLASS))
        self.assertEqual(self.inventory.getGoldInPocket(), 1000 - EconomyGlobals.getRespecCost(0))

    def test_respec_cost_rises_and_requires_a_trainer(self):
        self.inventory.stacks.update({
            InventoryType.PistolShoot: 5,
            InventoryType.NumRespecPistol: 1})

        self.shop.avatarType = AvatarTypes.Gunsmith
        self.assertFalse(self.shop.handleRespec(self.avatar, self.inventory, InteractGlobals.RESPEC_PISTOL))

        self.shop.avatarType = AvatarTypes.Trainer
        self.assertFalse(self.shop.handleRespec(self.avatar, self.inventory, InteractGlobals.RESPEC_PISTOL))
        self.assertEqual(self.inventory.getStackQuantity(InventoryType.PistolShoot), 5)

        self.inventory.setGoldInPocket(EconomyGlobals.getRespecCost(1))
        self.assertTrue(self.shop.handleRespec(self.avatar, self.inventory, InteractGlobals.RESPEC_PISTOL))
        self.assertEqual(self.inventory.getGoldInPocket(), 0)
        self.assertEqual(self.inventory.getStackQuantity(InventoryType.NumRespecPistol), 2)


if __name__ == '__main__':
    unittest.main()
