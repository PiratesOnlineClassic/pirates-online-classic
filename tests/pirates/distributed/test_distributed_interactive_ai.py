import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI


class DistributedInteractiveAITests(unittest.TestCase):
    def setUp(self):
        self.sender = 42
        self.avatar = SimpleNamespace(
            doId=self.sender, uniqueName=lambda event: '%s-%s' % (event, self.sender))
        self.air = SimpleNamespace(
            doId2do={self.sender: self.avatar},
            getAvatarIdFromSender=lambda: self.sender,
            logPotentialHacker=Mock())
        self.obj = DistributedInteractiveAI.__new__(DistributedInteractiveAI)
        self.obj.air = self.air
        self.obj.doId = 100
        self.obj.userId = 0
        self.obj.sendUpdate = Mock()
        self.obj.sendUpdateToAvatarId = Mock()
        self.obj.handleRequestInteraction = Mock(return_value=self.obj.ACCEPT)
        self.obj.handleRequestExit = Mock(return_value=self.obj.ACCEPT)
        self.obj.handlePostRequestInteraction = Mock()
        self.obj.handlePostRequestExit = Mock()

    def test_missing_sender_is_logged_for_interaction_and_exit(self):
        self.air.doId2do.clear()
        self.obj.requestInteraction(42, 0, False)
        self.obj.requestExit()

        self.assertEqual(self.air.logPotentialHacker.call_count, 2)
        self.assertEqual(self.air.logPotentialHacker.call_args_list[0].kwargs['targetAvId'], 42)
        self.assertEqual(self.air.logPotentialHacker.call_args_list[1].kwargs['targetAvId'], 42)
        self.obj.handleRequestInteraction.assert_not_called()
        self.obj.handleRequestExit.assert_not_called()

    def test_valid_interaction_and_exit_preserve_user_state(self):
        with patch('pirates.distributed.DistributedInteractiveAI.messenger',
                   create=True) as messenger:
            self.obj.requestInteraction(42, 0, False)
            self.assertEqual(self.obj.userId, 42)
            self.obj.requestExit()

        self.assertEqual(self.obj.userId, 0)
        self.obj.handleRequestInteraction.assert_called_once_with(self.avatar, 0, False)
        self.obj.handleRequestExit.assert_called_once_with(self.avatar)
        self.assertEqual(messenger.send.call_count, 2)

    def test_another_avatar_cannot_clear_the_user(self):
        self.obj.userId = 7
        with patch('pirates.distributed.DistributedInteractiveAI.messenger',
                   create=True) as messenger:
            self.obj.requestExit()
            self.obj.demandExit()

        self.assertEqual(self.obj.userId, 7)
        self.obj.sendUpdateToAvatarId.assert_called_once_with(42, 'rejectExit', [])
        self.obj.handlePostRequestExit.assert_not_called()
        messenger.send.assert_not_called()

    def test_user_can_demand_exit(self):
        self.obj.userId = 42
        with patch('pirates.distributed.DistributedInteractiveAI.messenger',
                   create=True) as messenger:
            self.obj.demandExit()

        self.assertEqual(self.obj.userId, 0)
        self.obj.handlePostRequestExit.assert_called_once_with(self.avatar)
        messenger.send.assert_called_once_with('interact-canceled-42')

    def test_multiuse_exit_is_never_refused_for_another_user(self):
        self.obj.MULTIUSE = True
        self.obj.userId = 7
        with patch('pirates.distributed.DistributedInteractiveAI.messenger',
                   create=True) as messenger:
            self.obj.requestExit()

        self.obj.sendUpdateToAvatarId.assert_called_once_with(42, 'setUserId', [0])
        messenger.send.assert_called_once_with('interact-canceled-42')


if __name__ == '__main__':
    unittest.main()
