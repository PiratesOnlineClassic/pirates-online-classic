import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from pirates.minigame import DistributedPokerTableAI as poker_ai_module
from pirates.minigame import DistributedHoldemTableAI as holdem_ai_module
from pirates.minigame import Distributed7StudTableAI as stud_ai_module
from pirates.minigame import PlayingCardGlobals
from tests.pirates.minigame.minigame_test_util import FakeTaskMgr, FakeInventory, makeTable, sentFields
from pirates.uberdog.UberDogGlobals import InventoryType


class PokerTurnValidationTests(unittest.TestCase):
    def make_table(self):
        table = poker_ai_module.DistributedPokerTableAI.__new__(
            poker_ai_module.DistributedPokerTableAI)
        avatar = SimpleNamespace(doId=101)
        table.air = SimpleNamespace(
            doId2do={101: avatar},
            getAvatarIdFromSender=lambda: 101)
        table.seats = [avatar, SimpleNamespace(doId=102)] + [None] * 5
        table._round = 3
        table._bettingOrder = [1, 0]
        table._playerActions = [[PlayingCardGlobals.NoAction, 0] for _ in range(7)]
        table._activeBettors = [0, 1]
        table.uniqueName = lambda name: name
        return table

    def test_out_of_turn_action_does_not_consume_current_turn(self):
        table = self.make_table()
        table._broadcastPlayerActions = Mock()
        table._broadcastTableState = Mock()
        table._nextBettingAction = Mock()

        table._applyAction(0, PlayingCardGlobals.Check, 0)

        self.assertEqual(table._bettingOrder, [1, 0])
        self.assertEqual(table._playerActions[0],
                         [PlayingCardGlobals.NoAction, 0])
        table._nextBettingAction.assert_not_called()

    def test_stale_round_action_does_not_cancel_current_timeout(self):
        table = self.make_table()
        table._bettingOrder = [0, 1]
        table._applyAction = Mock()

        with patch.object(poker_ai_module.taskMgr, 'remove') as remove_task:
            table.clientAction(2, [PlayingCardGlobals.Check, 0])

        table._applyAction.assert_not_called()
        remove_task.assert_not_called()


class HandEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.table = poker_ai_module.DistributedPokerTableAI.__new__(
            poker_ai_module.DistributedPokerTableAI)

    def card(self, rank, suit=0):
        return suit * 13 + rank

    def test_ace_low_straight_sorted_five_high(self):
        cards = [self.card(12, 0), self.card(0, 1), self.card(1, 2), self.card(2, 3), self.card(3, 0)]
        handId, sortedCards = self.table._bestHandFrom(cards)
        self.assertEqual(handId, PlayingCardGlobals.Straight)
        self.assertEqual(sortedCards[0] % 13, 3)
        self.assertEqual(sortedCards[-1] % 13, 12)

    def test_four_suited_cards_are_not_a_flush(self):
        cards = [self.card(1), self.card(5), self.card(8), self.card(10)]
        handId, sortedCards = self.table._bestHandFrom(cards)
        self.assertEqual(handId, PlayingCardGlobals.NoPair)

    def test_full_house_sorted_trips_first(self):
        cards = [self.card(4, 0), self.card(9, 0), self.card(4, 1), self.card(9, 1), self.card(9, 2),
                 self.card(0, 3), self.card(2, 3)]
        handId, sortedCards = self.table._bestHandFrom(cards)
        self.assertEqual(handId, PlayingCardGlobals.FlHouse)
        self.assertEqual([c % 13 for c in sortedCards], [9, 9, 9, 4, 4])

    def test_side_pot_split(self):
        table = self.table
        table._availableSeats = 7
        table._buttonSeat = 0
        table._caughtCheating = set()
        table._contributions = {0: 10, 1: 50, 2: 50}
        # seat 0 has the best hand but was only all-in for 10
        scores = {0: [9], 1: [5], 2: [3]}
        winnings = table._distributePot(scores)
        self.assertEqual(winnings, {0: 30, 1: 80})


class PokerHandFlowTests(unittest.TestCase):
    def setUp(self):
        self.fakeTaskMgr = FakeTaskMgr()
        self.patcher = patch.object(poker_ai_module, 'taskMgr', self.fakeTaskMgr)
        self.patcher.start()
        self.sender = [101]
        self.inventories = {101: FakeInventory(200)}

    def tearDown(self):
        self.patcher.stop()

    def playHand(self, table, action):
        for i in range(300):
            if not table._handActive and table._round == table.NumRounds:
                return
            if table._bettingOrder and table._bettingOrder[0] == 0 and \
                    self.fakeTaskMgr.hasTask(table.uniqueName('poker-timeout')):
                table.clientAction(table._round, action(table))
                continue
            if not self.fakeTaskMgr.run(limit=1):
                return

    def test_player_cannot_sit_without_minimum_gold(self):
        self.inventories[101].setGoldInPocket(5)
        table, avatars = makeTable(holdem_ai_module.DistributedHoldemTableAI,
                                   self.inventories, self.sender, aiSeats=(1, 2))
        result = table.handleRequestInteraction(avatars[101], 0, False)
        self.assertEqual(result, table.DENY)
        table.sendUpdateToAvatarId.assert_called_with(101, 'requestSeatResponse', [4, 0])

    def test_full_holdem_hand_with_player_folding(self):
        table, avatars = makeTable(holdem_ai_module.DistributedHoldemTableAI,
                                   self.inventories, self.sender, aiSeats=(1, 2))
        table.avatarSit(avatars[101], 0)
        self.fakeTaskMgr.run(limit=3)  # start hand, post blinds, deal
        self.assertTrue(table._handActive)
        self.assertEqual(table._round, 1)
        self.assertEqual(len(table._playerHands[0]), 2)

        # the player's private hand is sent, the public view is hidden
        privateHands = [c[0][2][0] for c in table.sendUpdateToAvatarId.call_args_list
                        if c[0][1] == 'setLocalAvatarHand']
        self.assertEqual(privateHands[-1], table._playerHands[0])
        self.assertEqual(table.getPublicPlayerHands()[0], [PlayingCardGlobals.Unknown] * 2)

        self.playHand(table, lambda t: [PlayingCardGlobals.Fold, 0])

        # no Ante actions are ever sent, the client can't display them
        for maxBet, actions, chips in sentFields(table, 'setPlayerActions'):
            for action, amount in actions:
                self.assertNotEqual(action, PlayingCardGlobals.Ante)

        self.assertFalse(table._handActive)
        self.assertEqual(table.potSize, 0)
        self.assertNotEqual(table._totalWinnings[0], PlayingCardGlobals.PlayerInactive)
        # total gold in the game is conserved
        total = self.inventories[101].getGoldInPocket() + table._chipsCount[1] + table._chipsCount[2]
        self.assertEqual(total, 200 + 2 * table.AIStartingChips)

    def test_player_calls_down_to_showdown(self):
        table, avatars = makeTable(holdem_ai_module.DistributedHoldemTableAI,
                                   self.inventories, self.sender, aiSeats=(3,))
        table._aiDecide = lambda seatIndex: table._applyAction(
            seatIndex, PlayingCardGlobals.CheckCall, 0)
        table.avatarSit(avatars[101], 0)
        self.playHand(table, lambda t: [PlayingCardGlobals.CheckCall, t._maxBet])

        self.assertEqual(table._round, table.NumRounds)
        self.assertEqual(len(table._communityCards), 5)
        self.assertTrue(sentFields(table, 'setAllHandValues'))
        # at the showdown every hand is revealed
        self.assertNotIn(PlayingCardGlobals.Unknown, table.getPublicPlayerHands()[0])
        total = self.inventories[101].getGoldInPocket() + table._chipsCount[3]
        self.assertEqual(total, 200 + table.AIStartingChips)
        # each betting round moves the pot by the blinds
        self.assertEqual(table._contributions[0], table._contributions[3])

    def test_player_all_in_deals_out_board(self):
        self.inventories[101].setGoldInPocket(30)
        table, avatars = makeTable(holdem_ai_module.DistributedHoldemTableAI,
                                   self.inventories, self.sender, aiSeats=(3,))
        table._aiDecide = lambda seatIndex: table._applyAction(
            seatIndex, PlayingCardGlobals.CheckCall, 0)
        table.avatarSit(avatars[101], 0)
        self.playHand(table, lambda t: [PlayingCardGlobals.AllIn, 0])

        self.assertEqual(table._round, table.NumRounds)
        self.assertEqual(len(table._communityCards), 5)
        self.assertEqual(table._contributions[0], 30)
        total = self.inventories[101].getGoldInPocket() + table._chipsCount[3]
        self.assertEqual(total, 30 + table.AIStartingChips)

    def test_player_leaving_mid_hand_folds(self):
        table, avatars = makeTable(holdem_ai_module.DistributedHoldemTableAI,
                                   self.inventories, self.sender, aiSeats=(1, 2))
        table.avatarSit(avatars[101], 0)
        self.fakeTaskMgr.run(limit=3)
        table.handleRequestExit(avatars[101])
        self.assertIsNone(table.seats[0])
        self.assertNotIn(0, table._activeBettors)
        # with no pirates left the hand is abandoned
        self.assertFalse(table._handActive)

    def test_card_swap_cheat_uses_inventory_card(self):
        table, avatars = makeTable(holdem_ai_module.DistributedHoldemTableAI,
                                   self.inventories, self.sender, aiSeats=(1,))
        table.avatarSit(avatars[101], 0)
        self.fakeTaskMgr.run(limit=3)
        self.inventories[101].b_setStackQuantity(InventoryType.begin_Cards + 51, 1)
        table._playerHands[0] = [0, 1]

        table.requestCheat(PlayingCardGlobals.ReplaceHoleCardOneCheat, 51)

        self.assertEqual(table._playerHands[0], [51, 1])
        self.assertEqual(self.inventories[101].getStackQuantity(InventoryType.begin_Cards + 51), 0)
        table.sendUpdateToAvatarId.assert_any_call(101, 'cheatResponse',
            [PlayingCardGlobals.ReplaceHoleCardOneCheat, 51, 1, [51, 1]])

        # a second swap in the same hand is refused
        self.inventories[101].b_setStackQuantity(InventoryType.begin_Cards + 50, 1)
        table.requestCheat(PlayingCardGlobals.ReplaceHoleCardTwoCheat, 50)
        self.assertEqual(table._playerHands[0], [51, 1])

    def test_card_swap_without_card_is_refused(self):
        table, avatars = makeTable(holdem_ai_module.DistributedHoldemTableAI,
                                   self.inventories, self.sender, aiSeats=(1,))
        table.avatarSit(avatars[101], 0)
        self.fakeTaskMgr.run(limit=3)
        hand = list(table._playerHands[0])
        table.requestCheat(PlayingCardGlobals.ReplaceHoleCardOneCheat, 40)
        self.assertEqual(table._playerHands[0], hand)

    def test_duplicate_card_at_showdown_catches_cheater(self):
        table, avatars = makeTable(holdem_ai_module.DistributedHoldemTableAI,
                                   self.inventories, self.sender, aiSeats=(1,))
        table._activeBettors = [0, 1]
        table._playerHands[0] = [51, 1]
        table._playerHands[1] = [51, 2]
        table._communityCards = []
        table._cheaters = {0: 51}
        table._caughtCheating = set()
        table._checkForCheaters()
        self.assertEqual(table._caughtCheating, {0})


class SevenStudTests(unittest.TestCase):
    def test_up_cards_are_public(self):
        table, avatars = makeTable(stud_ai_module.Distributed7StudTableAI,
                                   {101: FakeInventory(200)}, [101], aiSeats=(1,))
        table._activeBettors = [1]
        table._playerHands[1] = [0, 1, 2, 3, 4, 5, 6]
        self.assertEqual(table.getPublicPlayerHands()[1],
                         [255, 255, 2, 3, 4, 5, 255])

    def test_seven_cards_dealt_over_the_hand(self):
        table = stud_ai_module.Distributed7StudTableAI.__new__(stud_ai_module.Distributed7StudTableAI)
        total = sum(table.getRoundDeal(r)[0] for r in range(1, table.NumRounds))
        self.assertEqual(total, 7)

    def test_full_stud_hand(self):
        fakeTaskMgr = FakeTaskMgr()
        inventories = {101: FakeInventory(200)}
        with patch.object(poker_ai_module, 'taskMgr', fakeTaskMgr):
            table, avatars = makeTable(stud_ai_module.Distributed7StudTableAI,
                                       inventories, [101], aiSeats=(4,))
            table._aiDecide = lambda seatIndex: table._applyAction(
                seatIndex, PlayingCardGlobals.CheckCall, 0)
            table.avatarSit(avatars[101], 0)
            for i in range(300):
                if not table._handActive and table._round == table.NumRounds:
                    break
                if table._bettingOrder and table._bettingOrder[0] == 0 and \
                        fakeTaskMgr.hasTask(table.uniqueName('poker-timeout')):
                    table.clientAction(table._round, [PlayingCardGlobals.CheckCall, table._maxBet])
                    continue
                fakeTaskMgr.run(limit=1)

        self.assertEqual(table._round, 6)
        self.assertEqual(len(table._playerHands[0]), 7)
        self.assertEqual(table._communityCards, [])


if __name__ == '__main__':
    unittest.main()
