import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from pirates.minigame import DistributedPokerTableAI as poker_ai_module
from pirates.minigame import PlayingCardGlobals


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


if __name__ == '__main__':
    unittest.main()
