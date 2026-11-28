import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from tests.pirates.ship.test_ship_ai import makeAir, makeShip

from pirates.battle import LootGlobals
from pirates.economy.EconomyGlobals import ItemId
from pirates.pirate import AvatarTypes
from pirates.piratesbase import CollectionMap
from pirates.quest import QuestReward
from pirates.ship.NPCShipAI import NPCShipAI
from pirates.trades.TradeAI import LocalTrade
from pirates.uberdog.PirateInventoryAI import PirateInventoryAI
from pirates.uberdog.UberDogGlobals import InventoryType


class FakeInventory:

    def __init__(self, stacks=None, limits=None):
        self.stacks = dict(stacks or {})
        self.limits = dict(limits or {})

    def getStackQuantity(self, stackType):
        return self.stacks.get(stackType, 0)

    def getStackLimit(self, stackType):
        return self.limits.get(stackType, 0)

    def b_setStackQuantity(self, stackType, quantity):
        self.stacks[stackType] = quantity


class CollectionDropTests(unittest.TestCase):

    def test_only_started_collections_drop(self):
        inventory = FakeInventory()
        self.assertIsNone(LootGlobals.getCollectionDrop(AvatarTypes.Navy, inventory))

        inventory.stacks[InventoryType.Collection_Set3] = 1
        itemId = LootGlobals.getCollectionDrop(AvatarTypes.Navy, inventory)
        self.assertIn(itemId, LootGlobals.getCollectionSetParts(InventoryType.Collection_Set3))

    def test_collections_drop_from_their_enemy_type(self):
        inventory = FakeInventory({InventoryType.Collection_Set5: 1,
                                   InventoryType.Collection_Set6: 1})

        # water undead carry both the teeth and the fingers, other undead only the teeth...
        self.assertEqual(LootGlobals.getCollectionSetsFound(AvatarTypes.Drip),
                         [InventoryType.Collection_Set5, InventoryType.Collection_Set6])
        self.assertEqual(LootGlobals.getCollectionSetsFound(AvatarTypes.Clod),
                         [InventoryType.Collection_Set5])
        self.assertEqual(LootGlobals.getCollectionSetsFound(AvatarTypes.Crab),
                         [InventoryType.Collection_Set8])
        self.assertIsNone(LootGlobals.getCollectionDrop(AvatarTypes.Crab, inventory))

        for _ in range(20):
            self.assertIn(LootGlobals.getCollectionDrop(AvatarTypes.Clod, inventory),
                          LootGlobals.getCollectionSetParts(InventoryType.Collection_Set5))

    def test_full_stacks_are_skipped(self):
        parts = LootGlobals.getCollectionSetParts(InventoryType.Collection_Set3)
        self.assertEqual(len(parts), CollectionMap.Collection_Set_Sizes[InventoryType.Collection_Set3])
        inventory = FakeInventory({InventoryType.Collection_Set3: 1},
                                  dict((partId, 99) for partId in parts))
        inventory.stacks.update(dict((partId, 99) for partId in parts[1:]))
        self.assertEqual(LootGlobals.getCollectionDrop(AvatarTypes.Navy, inventory), parts[0])

        inventory.stacks[parts[0]] = 99
        self.assertIsNone(LootGlobals.getCollectionDrop(AvatarTypes.Navy, inventory))

    def test_rare_items_are_found_less_often(self):
        common = InventoryType.Collection_Set1_Part3
        rare = InventoryType.Collection_Set1_Part6
        self.assertEqual(CollectionMap.Collection_Rarity.get(rare), 2)
        self.assertGreater(LootGlobals.getCollectionPartWeight(common),
                           LootGlobals.getCollectionPartWeight(rare))

    def test_inventory_gives_collection_item_with_loot_message(self):
        inventory = PirateInventoryAI.__new__(PirateInventoryAI)
        avatar = Mock()
        inventory.ownerId = 42
        inventory.air = SimpleNamespace(doId2do={42: avatar})
        inventory.getStackQuantity = Mock(return_value=1)
        inventory.b_setStackQuantity = Mock()

        inventory.giveCollectionItem(InventoryType.Collection_Set3_Part2)
        inventory.b_setStackQuantity.assert_called_once_with(InventoryType.Collection_Set3_Part2, 2)
        avatar.d_sendLootMessage.assert_called_once_with(InventoryType.Collection_Set3_Part2)


class ShipLootTests(unittest.TestCase):

    def test_ship_loot_amount(self):
        for _ in range(20):
            loot = LootGlobals.getShipLoot()
            self.assertTrue(1 <= len(loot) <= 3)
            for itemId in loot:
                self.assertIn(itemId, (ItemId.CARGO_CRATE, ItemId.CARGO_CHEST, ItemId.CARGO_SKCHEST))

            self.assertTrue(3 <= len(LootGlobals.getShipLoot(isFlagship=True)) <= 5)

    def test_treasure_sense_improves_cargo_quality(self):
        base = dict(LootGlobals.getCargoContainerWeights(0))
        sensed = dict(LootGlobals.getCargoContainerWeights(4))
        self.assertEqual(base, LootGlobals.CARGO_CONTAINER_WEIGHTS)
        self.assertEqual(sensed[ItemId.CARGO_CRATE], base[ItemId.CARGO_CRATE])
        self.assertAlmostEqual(sensed[ItemId.CARGO_CHEST], base[ItemId.CARGO_CHEST] * 1.2)
        self.assertAlmostEqual(sensed[ItemId.CARGO_SKCHEST], base[ItemId.CARGO_SKCHEST] * 1.2)

    def makeShips(self, maxCargo=5, cargo=None, treasureSense=0):
        air = makeAir()
        captain = SimpleNamespace(getInventory=lambda: FakeInventory(
            {InventoryType.SailTreasureSense: treasureSense}))
        air.doId2do[42] = captain
        npcShip = makeShip(cls=NPCShipAI, air=air, npcShip=1)
        playerShip = makeShip(doId=2000, air=air, maxCargo=maxCargo, cargo=list(cargo or []),
                              ownerId=42)
        return npcShip, playerShip

    def test_sunk_ship_is_plundered_into_attacker_hold(self):
        npcShip, playerShip = self.makeShips(cargo=[ItemId.CARGO_CHEST])
        loot = [ItemId.CARGO_CRATE, ItemId.CARGO_SKCHEST]
        with patch.object(LootGlobals, 'getShipLoot', return_value=loot) as getShipLoot:
            self.assertEqual(npcShip.plunderShip(playerShip), loot)

        getShipLoot.assert_called_once_with(False, 0)
        self.assertEqual(playerShip.getCargo(), [ItemId.CARGO_CHEST] + loot)
        playerShip.sendUpdate.assert_any_call('setCargo', [[ItemId.CARGO_CHEST] + loot])
        playerShip.sendUpdate.assert_any_call('notifyReceivedLoot', [loot])

    def test_plunder_is_limited_by_cargo_space(self):
        npcShip, playerShip = self.makeShips(maxCargo=2, cargo=[ItemId.CARGO_CRATE], treasureSense=3)
        loot = [ItemId.CARGO_CHEST, ItemId.CARGO_CHEST]
        with patch.object(LootGlobals, 'getShipLoot', return_value=loot) as getShipLoot:
            self.assertEqual(npcShip.plunderShip(playerShip), [ItemId.CARGO_CHEST])

        # the captain's skill rank is one less than the skill's stack...
        getShipLoot.assert_called_once_with(False, 2)
        self.assertEqual(playerShip.getCargo(), [ItemId.CARGO_CRATE, ItemId.CARGO_CHEST])

        playerShip.sendUpdate.reset_mock()
        self.assertEqual(npcShip.plunderShip(playerShip), [])
        playerShip.sendUpdate.assert_not_called()

    def test_npc_ships_do_not_plunder(self):
        npcShip, playerShip = self.makeShips()
        playerShip.npcShip = 1
        self.assertEqual(npcShip.plunderShip(playerShip), [])
        self.assertEqual(npcShip.plunderShip(None), [])

    def test_sinking_ship_plunders_once(self):
        npcShip, playerShip = self.makeShips()
        npcShip.air.questMgr = Mock()
        npcShip.hp = 10
        npcShip.cannonAttackerIds = set()
        npcShip.getDamageInputModifier = lambda: 1.0
        npcShip.getArmorModifier = lambda: 0.0
        npcShip.plunderShip = Mock()
        npcShip.rewardCrew = Mock()
        npcShip.handleShipSinking = Mock(wraps=npcShip.handleShipSinking)
        npcShip.gameFSM.request.side_effect = lambda state: npcShip.gameFSM.getCurrentOrNextState.configure_mock(
            return_value=state)

        npcShip.takeDamage(50, playerShip.doId)
        npcShip.takeDamage(50, playerShip.doId)
        npcShip.handleShipSinking.assert_called_once_with()
        npcShip.plunderShip.assert_called_once_with(playerShip)
        npcShip.rewardCrew.assert_called_once_with(playerShip)
        npcShip.air.questMgr.shipSunk.assert_called_once_with(npcShip, [playerShip.doId])


class PlayingCardRewardTests(unittest.TestCase):

    def test_tier_rewards_give_the_dropped_card(self):
        inventory = FakeInventory()
        avatar = Mock(doId=1)
        avatar.getInventory.return_value = inventory
        trade = LocalTrade(SimpleNamespace(doId2do={1: avatar}))
        trade.setAvatarId(1)

        for rewardClass in (QuestReward.PlayingCardTier0Reward, QuestReward.PlayingCardTier1Reward,
                            QuestReward.PlayingCardTier2Reward, QuestReward.PlayingCardTier3Reward):
            avatar.giveCardMessage.reset_mock()
            inventory.stacks.clear()
            rewardClass().applyTo(trade, avatar)
            cardId = avatar.giveCardMessage.call_args.args[0]
            self.assertTrue(InventoryType.begin_Cards <= cardId < InventoryType.end_Cards)
            self.assertEqual(inventory.stacks, {cardId: 1})


if __name__ == '__main__':
    unittest.main()
