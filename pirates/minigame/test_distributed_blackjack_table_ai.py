import unittest
from unittest.mock import patch

from pirates.minigame import DistributedBlackjackTableAI as blackjack_ai_module
from pirates.minigame import PlayingCardGlobals
from pirates.minigame.minigame_test_util import FakeTaskMgr, FakeInventory, makeTable, sentFields, sentToAvatar
from pirates.uberdog.UberDogGlobals import InventoryType

# card values: rank = card % 13, 0 is a two and 12 is an ace
TWO, FIVE, SIX, NINE, TEN, KING, ACE = 0, 3, 4, 7, 8, 11, 12


class BlackjackTests(unittest.TestCase):
    def setUp(self):
        self.fakeTaskMgr = FakeTaskMgr()
        self.patcher = patch.object(blackjack_ai_module, 'taskMgr', self.fakeTaskMgr)
        self.patcher.start()
        self.sender = [101]
        self.inventories = {101: FakeInventory(100)}
        self.table, self.avatars = makeTable(blackjack_ai_module.DistributedBlackjackTableAI,
                                             self.inventories, self.sender, aiSeats=(3,))

    def tearDown(self):
        self.patcher.stop()

    def gold(self):
        return self.inventories[101].getGoldInPocket()

    def startRound(self, deck=None):
        table = self.table
        table.avatarSit(self.avatars[101], 0)
        self.fakeTaskMgr.runTask(table.uniqueName('bj-start'))
        if deck is not None:
            # cards are popped off the end of the deck
            table._buildDeck = lambda: setattr(table, '_deck', list(reversed(deck)))
            table._deck = list(reversed(deck))

    def bid(self, amount):
        self.table.clientAction([PlayingCardGlobals.Bid, amount])

    def runUntilPlayerTurn(self):
        table = self.table
        for i in range(50):
            if table._actionQueue and table._actionQueue[0] == 0 and \
                    self.fakeTaskMgr.hasTask(table.uniqueName('bj-action')) and \
                    self.fakeTaskMgr.tasks[table.uniqueName('bj-action')][0] == table._playerActionTimeoutTask:
                return True
            if not table._roundActive:
                return False
            if not self.fakeTaskMgr.run(limit=1):
                return False
        return False

    def finishRound(self):
        for i in range(50):
            if not self.table._roundActive:
                return
            name = sorted(self.fakeTaskMgr.tasks)[0]
            if name == self.table.uniqueName('bj-start'):
                return
            self.fakeTaskMgr.runTask(name)

    def test_asks_for_bid_and_takes_gold(self):
        self.startRound()
        self.assertIn([0, [PlayingCardGlobals.AskForBid, 0]], sentFields(self.table, 'setEvent'))
        self.bid(10)
        self.assertEqual(self.gold(), 90)
        self.assertEqual(self.table._bids[0], [10])

    def test_bid_clamped_to_table_limits(self):
        self.startRound()
        self.bid(5000)
        self.assertEqual(self.table._bids[0], [self.table._getMaxBidAmount()])

    def test_dealer_hole_card_hidden(self):
        self.startRound()
        self.bid(10)
        self.fakeTaskMgr.runTask(self.table.uniqueName('bj-deal'))
        hands, chips = self.table.getTableState()
        self.assertEqual(hands[7][0][1], PlayingCardGlobals.Unknown)
        self.assertIsNotNone(self.table._dealerHoleCard)

    def test_player_wins_by_standing_on_twenty(self):
        # deal order: player, ai, dealer, player, ai, dealer hole, then dealer draws
        self.startRound(deck=[KING, NINE, TEN, KING, NINE, SIX, NINE])
        self.bid(10)
        self.assertTrue(self.runUntilPlayerTurn())
        self.table.clientAction([PlayingCardGlobals.Stay, 0])
        self.finishRound()
        # dealer 16 draws a nine and busts
        self.assertEqual(self.gold(), 110)
        results = sentFields(self.table, 'setHandResults')[-1][0]
        self.assertEqual(results[0], 10)
        self.table.air.questMgr.blackjackHandWon.assert_called_with(self.avatars[101], 10)
        self.assertEqual(self.inventories[101].getStackQuantity(InventoryType.BlackjackGame), 10)

    def test_blackjack_pays_three_to_two(self):
        self.startRound(deck=[ACE, NINE, TEN, KING, NINE, NINE])
        self.bid(10)
        self.finishRound()
        self.assertEqual(self.gold(), 115)

    def test_bust_loses_bid(self):
        self.startRound(deck=[KING, NINE, TEN, SIX, NINE, NINE, KING])
        self.bid(10)
        self.assertTrue(self.runUntilPlayerTurn())
        self.table.clientAction([PlayingCardGlobals.Hit, 0])
        self.finishRound()
        self.assertEqual(self.gold(), 90)

    def test_double_down(self):
        self.startRound(deck=[FIVE, NINE, TEN, SIX, NINE, NINE, KING])
        self.bid(10)
        self.assertTrue(self.runUntilPlayerTurn())
        self.table.clientAction([PlayingCardGlobals.DoubleDown, 10])
        self.assertEqual(self.table._bids[0], [20])
        self.finishRound()
        # 21 against the dealer's 19
        self.assertEqual(self.gold(), 120)

    def test_split_plays_both_hands(self):
        self.startRound(deck=[NINE + 13, NINE, TEN, NINE + 26, NINE, SIX, KING, ACE, KING, KING])
        self.bid(10)
        self.assertTrue(self.runUntilPlayerTurn())
        self.table.clientAction([PlayingCardGlobals.Split, 10])
        self.assertEqual(len(self.table._allHands[0]), 2)
        self.assertEqual(self.gold(), 80)
        # first hand 9 + K = 19
        self.assertTrue(self.runUntilPlayerTurn())
        self.table.clientAction([PlayingCardGlobals.Stay, 0])
        # second hand 9 + A = 20
        self.assertTrue(self.runUntilPlayerTurn())
        self.assertEqual(len(self.table._allHands[0][1]), 2)
        self.table.clientAction([PlayingCardGlobals.Stay, 0])
        self.finishRound()
        # dealer has 16, draws K and busts; both hands win
        self.assertEqual(self.gold(), 120)

    def test_events_never_send_autostay(self):
        self.startRound(deck=[KING, NINE, TEN, KING, NINE, SIX, NINE])
        self.bid(10)
        self.assertTrue(self.runUntilPlayerTurn())
        self.table.clientAction([PlayingCardGlobals.AutoStay, 0])
        self.finishRound()
        for seatIndex, action in sentFields(self.table, 'setEvent'):
            # the client's BlackjackActionNames has no entry for these
            self.assertNotIn(action[0], (PlayingCardGlobals.AutoStay, PlayingCardGlobals.CardSwap))

    def test_no_bid_sits_out(self):
        self.startRound()
        self.fakeTaskMgr.runTask(self.table.uniqueName('bj-bid'))
        self.assertNotIn(0, self.table._bids)
        self.assertEqual(self.gold(), 100)

    def test_card_swap(self):
        self.startRound(deck=[KING, NINE, TEN, FIVE, NINE, SIX, NINE])
        self.inventories[101].b_setStackQuantity(InventoryType.begin_Cards + ACE + 39, 1)
        self.bid(10)
        self.assertTrue(self.runUntilPlayerTurn())
        self.table.requestCheat(PlayingCardGlobals.ReplaceHoleCardTwoCheat, ACE + 39)
        self.assertEqual(self.table._allHands[0][0], [KING, ACE + 39])
        response = sentToAvatar(self.table, 'cheatResponse')[-1]
        self.assertEqual(response[1][2], 1)

    def test_card_swap_with_duplicate_is_caught(self):
        self.startRound(deck=[KING, NINE, TEN, FIVE, NINE, SIX, NINE])
        self.inventories[101].b_setStackQuantity(InventoryType.begin_Cards + TEN, 1)
        self.bid(10)
        self.assertTrue(self.runUntilPlayerTurn())
        # the dealer's ten is showing on the table
        self.table.requestCheat(PlayingCardGlobals.ReplaceHoleCardTwoCheat, TEN)
        response = sentToAvatar(self.table, 'cheatResponse')[-1]
        self.assertEqual(response[1][0], PlayingCardGlobals.CaughtCheating)
        # the fine takes whatever gold is left, up to the full fine
        self.assertEqual(self.gold(), 0)

    def test_player_leaving_forfeits_and_round_aborts(self):
        self.startRound()
        self.bid(10)
        self.table.handleRequestExit(self.avatars[101])
        self.assertFalse(self.table._roundActive)
        self.assertEqual(self.gold(), 90)


if __name__ == '__main__':
    unittest.main()
