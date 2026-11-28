import types
import unittest
from unittest.mock import Mock

from otp.uberdog.RejectCode import RejectCode
from pirates.economy.EconomyGlobals import ItemId
from pirates.trades.TradeAI import LocalTrade, TradeAI
from pirates.trades.TradeManagerAI import TradeManagerAI
from pirates.uberdog.UberDogGlobals import InventoryType


class FakeInventory:
    def __init__(self, stacks, limits=None):
        self.stacks = dict(stacks)
        self.limits = {InventoryType.GoldInPocket: 65000, ItemId.POTION_1: 3}
        self.limits.update(limits or {})
        self.reputation = {}

    def getStackQuantity(self, stackType):
        return self.stacks.get(stackType, 0)

    def b_setStackQuantity(self, stackType, quantity):
        self.stacks[stackType] = quantity

    def getStackLimit(self, stackType):
        return self.limits.get(stackType, 0)

    def getReputation(self, repType):
        return self.reputation.get(repType, 0)

    def setReputation(self, repType, quantity):
        self.reputation[repType] = quantity

    def getOverallRep(self):
        return self.getReputation(InventoryType.OverallRep)

    def setOverallRep(self, quantity):
        self.setReputation(InventoryType.OverallRep, quantity)


def makeAvatar(doId, inventory):
    return types.SimpleNamespace(doId=doId, getInventory=lambda: inventory)


class TradeAITests(unittest.TestCase):

    def setUp(self):
        self.firstInventory = FakeInventory({InventoryType.GoldInPocket: 100})
        self.secondInventory = FakeInventory({InventoryType.GoldInPocket: 10, ItemId.POTION_1: 2})
        self.air = Mock()
        self.air.doId2do = {
            1: makeAvatar(1, self.firstInventory),
            2: makeAvatar(2, self.secondInventory)}
        self.trade = TradeAI.__new__(TradeAI)
        self.trade.air = self.air
        self.trade.doId = 500
        self.trade.firstAvatarId = 1
        self.trade.secondAvatarId = 2
        self.trade.firstAvatarStatus = 0
        self.trade.secondAvatarStatus = 0
        self.trade.firstAvatarGiving = []
        self.trade.secondAvatarGiving = []
        self.trade.finished = False
        self.trade.sendUpdate = Mock()
        self.trade.sendUpdateToAvatarId = Mock()

    def sendAs(self, avatarId, method, *args):
        self.air.getAvatarIdFromSender.return_value = avatarId
        getattr(self.trade, method)(*args)

    def test_giving_is_collapsed_and_resets_ready_status(self):
        self.trade.secondAvatarStatus = 1
        self.sendAs(1, 'requestChangeGiving', [[InventoryType.GoldInPocket, 1], [InventoryType.GoldInPocket, 1]])

        self.assertEqual(self.trade.firstAvatarGiving, [[InventoryType.GoldInPocket, 2]])
        self.assertEqual(self.trade.secondAvatarStatus, 0)
        self.trade.sendUpdate.assert_any_call('setFirstAvatarGiving', [[[InventoryType.GoldInPocket, 2]]])

    def test_giving_more_than_owned_or_untradable_is_rejected(self):
        self.sendAs(1, 'requestChangeGiving', [[InventoryType.GoldInPocket, 101]])
        self.trade.sendUpdateToAvatarId.assert_called_with(1, 'rejectChangeGiving', [RejectCode.HAS_NONE_OF_THAT_TYPE])

        self.sendAs(1, 'requestChangeGiving', [[InventoryType.CutlassRep, 1]])
        self.trade.sendUpdateToAvatarId.assert_called_with(1, 'rejectChangeGiving', [RejectCode.CONTENT_TYPE_NOT_ALLOWED])
        self.assertEqual(self.trade.firstAvatarGiving, [])

    def test_pouches_can_not_be_traded(self):
        self.assertFalse(self.trade.isTradableType(InventoryType.PistolPouchL1))
        self.assertTrue(self.trade.isTradableType(InventoryType.Potion1))

    def test_outsiders_cannot_change_the_trade(self):
        self.sendAs(3, 'requestChangeGiving', [[InventoryType.GoldInPocket, 1]])
        self.sendAs(3, 'requestChangeStatus', 1)

        self.assertEqual(self.trade.firstAvatarGiving, [])
        self.trade.sendUpdate.assert_not_called()

    def test_both_ready_swaps_the_offers(self):
        self.sendAs(1, 'requestChangeGiving', [[InventoryType.GoldInPocket, 40]])
        self.sendAs(2, 'requestChangeGiving', [[ItemId.POTION_1, 2]])
        self.sendAs(1, 'requestChangeStatus', 1)
        self.air.tradeMgr.removeTrade.assert_not_called()
        self.sendAs(2, 'requestChangeStatus', 1)

        self.assertEqual(self.firstInventory.stacks, {InventoryType.GoldInPocket: 60, ItemId.POTION_1: 2})
        self.assertEqual(self.secondInventory.stacks, {InventoryType.GoldInPocket: 50, ItemId.POTION_1: 0})
        self.trade.sendUpdateToAvatarId.assert_any_call(1, 'tradeCompleted', [])
        self.trade.sendUpdateToAvatarId.assert_any_call(2, 'tradeCompleted', [])
        self.air.tradeMgr.removeTrade.assert_called_once_with(500)

    def test_trade_fails_if_receiver_cannot_hold_items(self):
        self.firstInventory.stacks[ItemId.POTION_1] = 3
        self.sendAs(2, 'requestChangeGiving', [[ItemId.POTION_1, 1]])
        self.sendAs(1, 'requestChangeStatus', 1)
        self.sendAs(2, 'requestChangeStatus', 1)

        self.assertEqual(self.secondInventory.stacks[ItemId.POTION_1], 2)
        self.trade.sendUpdateToAvatarId.assert_any_call(1, 'tradeFailed', [])
        self.air.tradeMgr.removeTrade.assert_called_once_with(500)

    def test_remove_trade_cancels(self):
        self.sendAs(2, 'requestRemoveTrade')
        self.trade.sendUpdateToAvatarId.assert_any_call(1, 'tradeCanceled', [])
        self.air.tradeMgr.removeTrade.assert_called_once_with(500)

        # a second request is ignored once the trade is finished
        self.sendAs(1, 'requestRemoveTrade')
        self.air.tradeMgr.removeTrade.assert_called_once_with(500)


class TradeManagerAITests(unittest.TestCase):

    def setUp(self):
        self.air = Mock()
        self.air.doId2do = {
            1: makeAvatar(1, FakeInventory({})),
            2: makeAvatar(2, FakeInventory({}))}
        self.air.allocateZone.return_value = 9000
        self.air.dclassesByName = {'TradeAI': Mock()}
        self.manager = TradeManagerAI.__new__(TradeManagerAI)
        self.manager.air = self.air
        self.manager.doId = 77
        self.manager._TradeManagerAI__trades = {}
        self.manager._TradeManagerAI__tradeZones = {}
        self.manager.sendUpdateToAvatarId = Mock()

    def test_local_trades_are_not_tracked(self):
        trade = self.manager.createTrade(1)
        self.assertIsInstance(trade, LocalTrade)
        self.assertEqual(self.manager.getTradeFromAvatar(1), None)

    def test_request_create_trade_generates_under_manager(self):
        generated = []

        def generate(self, doId, parentId, zoneId):
            self.doId = doId
            generated.append((parentId, zoneId))

        self.air.allocateChannel.return_value = 600
        original = TradeAI.generateWithRequiredAndId
        TradeAI.generateWithRequiredAndId = generate
        try:
            self.air.getAvatarIdFromSender.return_value = 1
            self.manager.requestCreateTrade(2)
        finally:
            TradeAI.generateWithRequiredAndId = original

        self.assertEqual(generated, [(77, 9000)])
        self.manager.sendUpdateToAvatarId.assert_any_call(1, 'createTradeResponse', [2, 9000])
        self.manager.sendUpdateToAvatarId.assert_any_call(2, 'createTradeResponse', [1, 9000])
        self.assertTrue(self.manager.getTradeFromAvatar(2))

        # neither avatar may start another trade while this one is active
        self.air.getAvatarIdFromSender.return_value = 2
        self.manager.requestCreateTrade(1)
        self.manager.sendUpdateToAvatarId.assert_called_with(2, 'rejectCreateTrade', [1, RejectCode.MAY_NOT_TRADE])

        trade = self.manager.getTrade(600)
        trade.requestDelete = Mock()
        self.manager.removeTrade(600)
        self.air.deallocateZone.assert_called_once_with(9000)

    def test_request_create_trade_rejects_self_and_missing(self):
        self.air.getAvatarIdFromSender.return_value = 1
        self.manager.requestCreateTrade(1)
        self.manager.sendUpdateToAvatarId.assert_called_with(1, 'rejectCreateTrade', [1, RejectCode.NO_SELF_TRADE])
        self.manager.requestCreateTrade(3)
        self.manager.sendUpdateToAvatarId.assert_called_with(1, 'rejectCreateTrade', [3, RejectCode.OTHER_AVATAR_NOT_HERE])


class LocalTradeTests(unittest.TestCase):

    def test_reputation_counts_towards_notoriety(self):
        inventory = FakeInventory({})
        air = types.SimpleNamespace(doId2do={1: makeAvatar(1, inventory)})
        trade = LocalTrade(air)
        trade.setAvatarId(1)

        trade.giveReputation(InventoryType.GeneralRep, 50)

        self.assertEqual(inventory.reputation, {InventoryType.GeneralRep: 50, InventoryType.OverallRep: 50})

    def test_quest_gold_cards_and_ships_are_given(self):
        inventory = FakeInventory({InventoryType.GoldInPocket: 10})
        inventory.getGoldInPocket = lambda: inventory.getStackQuantity(InventoryType.GoldInPocket)
        inventory.setGoldInPocket = lambda quantity: inventory.b_setStackQuantity(
            InventoryType.GoldInPocket, quantity)
        inventory.ships = [5]
        inventory.getShipDoIdList = lambda: list(inventory.ships)
        inventory.setShipDoIdList = lambda ships: setattr(inventory, 'ships', ships)
        air = types.SimpleNamespace(doId2do={1: makeAvatar(1, inventory)})
        trade = LocalTrade(air)
        trade.setAvatarId(1)

        trade.giveGoldInPocket(25)
        trade.givePlayingCard(3)
        trade.giveShip(6)
        trade.giveShip(6)
        trade.giveNewShipToken()

        self.assertEqual(inventory.getGoldInPocket(), 35)
        self.assertEqual(inventory.getStackQuantity(InventoryType.begin_Cards + 3), 1)
        self.assertEqual(inventory.ships, [5, 6])
        self.assertEqual(inventory.getStackQuantity(InventoryType.NewShipToken), 1)


if __name__ == '__main__':
    unittest.main()
