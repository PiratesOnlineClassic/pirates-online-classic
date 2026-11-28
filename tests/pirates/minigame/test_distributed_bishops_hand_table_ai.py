import unittest
from unittest.mock import patch

from pirates.minigame import DistributedBishopsHandTableAI as bishops_ai_module
from pirates.minigame import BishopsHandGlobals
from tests.pirates.minigame.minigame_test_util import FakeTaskMgr, FakeInventory, makeTable, sentFields, sentToAvatar

ACTIONS = BishopsHandGlobals.PLAYER_ACTIONS
GAME_ACTIONS = BishopsHandGlobals.GAME_ACTIONS
CONTINUE = BishopsHandGlobals.CONTINUE_OPTIONS


class BishopsHandTests(unittest.TestCase):
    def setUp(self):
        self.fakeTaskMgr = FakeTaskMgr()
        self.patcher = patch.object(bishops_ai_module, 'taskMgr', self.fakeTaskMgr)
        self.patcher.start()
        self.sender = [101]
        self.inventories = {101: FakeInventory(10), 102: FakeInventory(10)}
        self.table, self.avatars = makeTable(bishops_ai_module.DistributedBishopsHandTableAI,
                                             self.inventories, self.sender)
        self.table.avatarSit(self.avatars[101], 1)
        self.table.avatarSit(self.avatars[102], 4)

    def tearDown(self):
        self.patcher.stop()

    def act(self, avId, *action):
        self.sender[0] = avId
        self.table.clientAction(list(action))

    def progress(self, avId, step, misses=0, elapsed=10.0):
        self.sender[0] = avId
        self.table.receiveProgress(step, misses, step, elapsed)

    def startGame(self):
        self.act(101, ACTIONS.JoinGame, 0)
        self.act(102, ACTIONS.JoinGame, 0)
        self.fakeTaskMgr.runTask(self.table.uniqueName('bh-start'))

    def test_table_state_covers_every_seat(self):
        tableState, seatStatus = self.table.getTableState()
        self.assertEqual(len(seatStatus), 7)
        self.assertEqual(seatStatus[1], [101, 0])
        self.assertEqual(seatStatus[0], [0, -1])

    def test_join_takes_fee_and_unjoin_returns_it(self):
        self.act(101, ACTIONS.JoinGame, 0)
        self.assertEqual(self.inventories[101].getGoldInPocket(), 8)
        self.assertEqual(self.table.getPendingStakes(), 2)
        self.act(101, ACTIONS.UnjoinGame, 0)
        self.assertEqual(self.inventories[101].getGoldInPocket(), 10)
        self.assertEqual(self.table.getPendingStakes(), 0)

    def test_round_starts_for_joined_players(self):
        self.startGame()
        self.assertEqual(self.table.getRunningStakes(), 4)
        starts = sentToAvatar(self.table, 'startRound')
        self.assertEqual(sorted(avId for avId, args in starts), [101, 102])
        self.assertEqual(len(starts[0][1][0]), self.table.SequenceLength)
        self.assertEqual(self.table.getTableState()[1][1], [101, 2])

    def test_slowest_finisher_is_out_and_winner_leaves_with_stakes(self):
        self.startGame()
        self.progress(101, 10)
        self.assertEqual(sentFields(self.table, 'setProgressReport')[-1][0], [[1, 33], [4, 0]])
        self.progress(101, 30, elapsed=12.0)
        self.progress(102, 30, elapsed=20.0)

        asks = [(avId, args[0], args[1]) for avId, args in sentToAvatar(self.table, 'askForClientAction')]
        self.assertIn((102, [GAME_ACTIONS.AskForContinue, CONTINUE.Rejoin],
                       BishopsHandGlobals.RoundContinueWait), asks)
        self.assertIn((101, [GAME_ACTIONS.AskForContinue, CONTINUE.Leave],
                       BishopsHandGlobals.RoundContinueWait), asks)
        self.assertEqual(self.table._winnerSeat, 1)

        self.act(101, ACTIONS.Leave, 0)
        self.assertEqual(self.inventories[101].getGoldInPocket(), 12)
        self.assertEqual(self.table.getRunningStakes(), 0)

    def test_nobody_finishing_loses_stakes(self):
        self.startGame()
        self.fakeTaskMgr.runTask(self.table.uniqueName('bh-round'))
        self.assertEqual(self.table.getRunningStakes(), 0)
        self.assertIsNone(self.table._winnerSeat)
        self.assertEqual(self.table.getTableState()[1][4], [102, 0])

    def test_resign_and_win_by_default(self):
        self.startGame()
        self.act(102, ACTIONS.Resign, 0)
        self.progress(101, 30)
        self.assertEqual(self.table._winnerSeat, 1)
        self.fakeTaskMgr.runTask(self.table.uniqueName('bh-continue'))
        self.assertEqual(self.inventories[101].getGoldInPocket(), 12)

    def test_progress_from_non_player_ignored(self):
        self.act(101, ACTIONS.JoinGame, 0)
        self.fakeTaskMgr.runTask(self.table.uniqueName('bh-start'))
        self.progress(102, 30)
        self.assertNotIn(4, self.table._finished)


if __name__ == '__main__':
    unittest.main()
