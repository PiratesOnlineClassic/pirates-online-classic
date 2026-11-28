import random
import unittest
from unittest.mock import patch

from pirates.minigame import DistributedDiceGameAI as dice_ai_module
from pirates.minigame import DistributedLiarsDiceAI as liars_ai_module
from pirates.minigame import DiceGlobals
from pirates.minigame.minigame_test_util import FakeTaskMgr, FakeInventory, makeTable, sentFields


class LiarsDiceTests(unittest.TestCase):
    def setUp(self):
        self.fakeTaskMgr = FakeTaskMgr()
        self.patchers = [patch.object(dice_ai_module, 'taskMgr', self.fakeTaskMgr),
                         patch.object(liars_ai_module, 'taskMgr', self.fakeTaskMgr)]
        for patcher in self.patchers:
            patcher.start()

        self.sender = [101]
        self.inventories = {101: FakeInventory(100), 102: FakeInventory(100)}
        self.table, self.avatars = makeTable(liars_ai_module.DistributedLiarsDiceAI,
                                             self.inventories, self.sender, aiSeats=(3,))
        self.table.avatarSit(self.avatars[101], 0)
        self.table.avatarSit(self.avatars[102], 5)

    def tearDown(self):
        for patcher in self.patchers:
            patcher.stop()

    def act(self, avId, method, *args):
        self.sender[0] = avId
        getattr(self.table, method)(*args)

    def readyUp(self):
        self.act(101, 'playerIsReady')
        self.act(102, 'playerIsReady')

    def rollFor(self, seatIndex, avId, dice):
        self.assertEqual(self.table._activeSeat, seatIndex)
        self.act(avId, 'playerHasRolled', seatIndex, dice)

    def test_ante_and_start_when_all_ready(self):
        self.act(101, 'playerIsReady')
        self.assertFalse(self.table._roundActive)
        self.assertEqual(self.inventories[101].getGoldInPocket(), 90)
        self.act(102, 'playerIsReady')
        self.assertTrue(self.table._roundActive)
        self.assertIn([DiceGlobals.DSTATE_DOROLL, 0, 'Pirate 101'], sentFields(self.table, 'currentTurn'))
        self.assertIn([0], sentFields(self.table, 'yourTurn'))

    def test_invalid_roll_rejected(self):
        self.readyUp()
        self.act(101, 'playerHasRolled', 0, [7, 1, 1, 1, 1])
        self.assertNotIn(0, self.table._rolledDice)
        self.act(101, 'playerHasRolled', 0, [1, 1, 1])
        self.assertNotIn(0, self.table._rolledDice)

    def playToBetting(self):
        self.readyUp()
        self.rollFor(0, 101, [2, 2, 2, 5, 6])
        self.fakeTaskMgr.runTask(self.table.uniqueName('dice-roll'))  # ai seat 3
        self.rollFor(5, 102, [2, 3, 4, 5, 6])
        self.assertTrue(self.table._bettingActive)
        self.assertEqual(self.table._activeSeat, 0)

    def test_betting_turn_sends_your_turn(self):
        self.playToBetting()
        self.assertEqual(sentFields(self.table, 'currentTurn')[-1][0], DiceGlobals.DSTATE_PLAY)
        self.assertEqual(sentFields(self.table, 'yourTurn')[-1], [0])

    def test_claim_must_exceed_previous(self):
        self.playToBetting()
        self.act(101, 'betUpdate', 0, 1, 1)
        self.assertEqual(self.table._activeSeat, 0)
        self.act(101, 'betUpdate', 0, 3, 2)
        self.assertEqual(self.table._lastBetSeat, 0)
        self.assertEqual(self.table._activeSeat, 3)
        self.assertEqual(sentFields(self.table, 'tableStatus')[-1], [3, 2])

    def test_called_bluff_eliminates_claimer(self):
        self.playToBetting()
        self.table._eliminatedSeats.add(3)  # leave just the two pirates
        self.act(101, 'betUpdate', 0, 9, 6)
        self.assertEqual(self.table._activeSeat, 5)
        self.act(102, 'callBluff', 5, 9, 6)
        self.assertEqual(sentFields(self.table, 'displayChallenge')[-1], [9, 6, 0, 5, 'Pirate 101'])
        # pirate 102 is the last one standing and takes both antes
        self.assertEqual(self.inventories[102].getGoldInPocket(), 110)
        self.assertEqual(sentFields(self.table, 'youWin')[-1], [102, 'Pirate 102'])

    def test_true_claim_eliminates_challenger(self):
        self.playToBetting()
        self.table._eliminatedSeats.add(3)
        # there are four 2s between the two pirates
        self.act(101, 'betUpdate', 0, 4, 2)
        self.act(102, 'callBluff', 5, 4, 2)
        self.assertEqual(sentFields(self.table, 'displayChallenge')[-1], [4, 2, 0, 5, 'Pirate 102'])
        self.assertEqual(self.inventories[101].getGoldInPocket(), 110)

    def test_rough_cheat_can_be_caught(self):
        self.playToBetting()
        self.act(101, 'cheatResult', 0, 2, liars_ai_module.DistributedLiarsDiceAI.CheatRough)
        self.assertIn([5, self.table.CatchWindow, 2], sentFields(self.table, 'incomingCheat'))
        self.act(102, 'catchCheater', 5)
        self.assertIn([0, 'Pirate 101'], sentFields(self.table, 'gotCaught'))
        self.assertIn(0, self.table._eliminatedSeats)
        self.assertEqual(self.table._activeSeat, 3)

    def test_change_dice_only_one_die(self):
        self.playToBetting()
        self.act(101, 'changeDice', 0, [2, 2, 2, 2, 6])
        self.assertEqual(self.table._rolledDice[0], [2, 2, 2, 2, 6])
        self.act(101, 'changeDice', 0, [6, 6, 6, 6, 6])
        self.assertEqual(self.table._rolledDice[0], [2, 2, 2, 2, 6])

    def test_full_game_with_ai_finishes(self):
        random.seed(4)
        self.table._shouldAIChallenge = lambda seatIndex: True
        self.readyUp()
        for i in range(500):
            if not self.table._roundActive:
                break
            seat = self.table._activeSeat
            if seat in (0, 5) and not self.table._bettingActive and seat not in self.table._rolledDice:
                avId = 101 if seat == 0 else 102
                self.act(avId, 'playerHasRolled', seat, [random.randint(1, 6) for _ in range(5)])
                continue
            if seat in (0, 5) and self.table._bettingActive:
                avId = 101 if seat == 0 else 102
                if self.table._lastBetSeat >= 0:
                    self.act(avId, 'callBluff', seat, 0, 0)
                else:
                    self.act(avId, 'betUpdate', seat, *self.table._getMinimumClaim())
                continue
            if not self.fakeTaskMgr.run(limit=1):
                break

        self.assertFalse(self.table._roundActive)
        self.assertTrue(sentFields(self.table, 'youWin'))

    def test_leaving_mid_game_eliminates(self):
        self.playToBetting()
        self.table._eliminatedSeats.add(3)
        self.table.handleRequestExit(self.avatars[101])
        self.assertEqual(self.inventories[102].getGoldInPocket(), 110)


if __name__ == '__main__':
    unittest.main()
