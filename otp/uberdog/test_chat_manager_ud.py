import unittest
from unittest.mock import Mock, call

from otp.uberdog.DistributedChatManagerUD import DistributedChatManagerUD


def makeManager(senderId):
    mgr = DistributedChatManagerUD.__new__(DistributedChatManagerUD)
    mgr.air = Mock()
    mgr.air.getAvatarIdFromSender.return_value = senderId
    mgr.avatarLocations = {}
    mgr.avatarCrews = {}
    mgr.avatarGuilds = {}
    mgr.sendUpdateToAvatarId = Mock()
    return mgr


class ChatManagerUDTests(unittest.TestCase):
    def test_open_chat_goes_to_same_location(self):
        mgr = makeManager(1)
        mgr.setAvatarLocation(1, 10, 20)
        mgr.setAvatarLocation(2, 10, 20)
        mgr.setAvatarLocation(3, 10, 21)
        mgr.chatTo('  ahoy  ', 0)
        self.assertEqual(sorted(mgr.sendUpdateToAvatarId.call_args_list), sorted([
            call(1, 'chatFrom', [1, 'ahoy', 0]),
            call(2, 'chatFrom', [1, 'ahoy', 0])]))

    def test_unknown_sender_and_bad_messages_dropped(self):
        mgr = makeManager(1)
        mgr.chatTo('hello', 0)
        mgr.setAvatarLocation(1, 10, 20)
        mgr.chatTo('   ', 0)
        mgr.chatTo('x' * 300, 0)
        mgr.sendUpdateToAvatarId.assert_not_called()

    def test_whisper_needs_online_target(self):
        mgr = makeManager(1)
        mgr.setAvatarLocation(1, 10, 20)
        mgr.whisperTo(2, 'hi')
        mgr.sendUpdateToAvatarId.assert_not_called()
        mgr.setAvatarLocation(2, 50, 60)
        mgr.whisperTo(2, 'hi')
        mgr.whisperSCTo(2, 7)
        mgr.sendUpdateToAvatarId.assert_has_calls([
            call(2, 'whisperFrom', [1, 'hi']),
            call(2, 'whisperSCFrom', [1, 7])])

    def test_crew_and_guild_chat(self):
        mgr = makeManager(1)
        for avId in (1, 2, 3):
            mgr.setAvatarLocation(avId, avId, avId)
        mgr.setAvatarCrew(1, 9)
        mgr.setAvatarCrew(2, 9)
        mgr.setAvatarGuild(1, 4)
        mgr.setAvatarGuild(3, 4)
        mgr.crewChatTo('crew')
        mgr.guildChatTo('guild')
        calls = mgr.sendUpdateToAvatarId.call_args_list
        self.assertIn(call(2, 'crewChatFrom', [1, 'crew']), calls)
        self.assertIn(call(3, 'guildChatFrom', [1, 'guild']), calls)
        self.assertNotIn(call(3, 'crewChatFrom', [1, 'crew']), calls)

    def test_offline_clears_avatar(self):
        mgr = makeManager(1)
        mgr.setAvatarLocation(1, 10, 20)
        mgr.setAvatarCrew(1, 9)
        mgr.setAvatarLocation(1, 0, 0)
        self.assertFalse(mgr.isAvatarOnline(1))
        self.assertEqual(mgr.avatarCrews, {})


if __name__ == '__main__':
    unittest.main()
