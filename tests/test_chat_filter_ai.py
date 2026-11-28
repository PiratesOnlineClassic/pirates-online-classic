import unittest
from unittest.mock import Mock, call

from otp.chat import ChatFilter
from otp.chat.WhiteList import WhiteList
from otp.avatar.DistributedPlayerAI import DistributedPlayerAI

WhiteListWords = ['ahoy', 'matey', 'where', 'is', 'the', 'treasure']

SenderChannel = (5 << 32) | 1


def makeAvatar(doId=1, senderId=1, parentId=10, zoneId=20):
    av = DistributedPlayerAI.__new__(DistributedPlayerAI)
    av.doId = doId
    av.parentId = parentId
    av.zoneId = zoneId
    av.DISLid = 0
    av.chatFlood = ChatFilter.ChatFlood(limit=3, window=5.0)
    av.air = Mock()
    av.air.ourChannel = 4000
    av.air.getAvatarIdFromSender.return_value = senderId
    av.air.getMsgSender.return_value = (5 << 32) | senderId
    av.dclass = Mock()
    av.sendUpdateToAvatarId = Mock()
    return av


class ChatFilterTests(unittest.TestCase):
    def setUp(self):
        self.whiteList = WhiteList(WhiteListWords)
        ChatFilter.setWhiteList(self.whiteList)

    def tearDown(self):
        ChatFilter.setWhiteList(None)

    def test_clean_message(self):
        self.assertEqual(ChatFilter.cleanMessage('  ahoy  '), 'ahoy')
        self.assertEqual(ChatFilter.cleanMessage('a\x01red\x01b\x02'), 'aredb')
        self.assertIsNone(ChatFilter.cleanMessage('   '))
        self.assertIsNone(ChatFilter.cleanMessage('x' * (ChatFilter.MaxChatLength + 1)))
        self.assertEqual(ChatFilter.cleanMessage('x' * ChatFilter.MaxChatLength), 'x' * ChatFilter.MaxChatLength)

    def test_whitelist_matches_client(self):
        self.assertEqual(ChatFilter.filterWhiteList('Ahoy, matey! where is the rum?'),
                         'Ahoy, matey! where is the arrr')
        self.assertTrue(ChatFilter.isWhiteListed('where is the treasure?'))
        self.assertFalse(ChatFilter.isWhiteListed('give me gold'))

    def test_no_whitelist_passes_through(self):
        ChatFilter.setWhiteList(None)
        self.assertEqual(ChatFilter.filterWhiteList('anything goes'), 'anything goes')

    def test_chat_flags(self):
        self.assertEqual(ChatFilter.cleanChatFlags(0xFF), ChatFilter.CFSpeech | ChatFilter.CFThought | ChatFilter.CFTimeout)

    def test_speedchat_indices(self):
        self.assertTrue(ChatFilter.isValidSpeedChat(100))
        self.assertFalse(ChatFilter.isValidSpeedChat(5))
        self.assertTrue(ChatFilter.isValidSpeedChatCustom(10))
        self.assertFalse(ChatFilter.isValidSpeedChatCustom(65535))
        self.assertTrue(ChatFilter.isValidSpeedChatEmote(0))
        self.assertFalse(ChatFilter.isValidSpeedChatEmote(60000))

    def test_flood(self):
        flood = ChatFilter.ChatFlood(limit=2, window=5.0)
        self.assertFalse(flood.isFlooding(1, now=0))
        self.assertFalse(flood.isFlooding(1, now=1))
        self.assertTrue(flood.isFlooding(1, now=2))
        self.assertFalse(flood.isFlooding(2, now=2))
        self.assertTrue(flood.shouldWarn(1))
        self.assertFalse(flood.shouldWarn(1))
        self.assertFalse(flood.isFlooding(1, now=5.5))
        flood.clear(1)
        self.assertNotIn(1, flood.history)


class PlayerChatTests(unittest.TestCase):
    def setUp(self):
        ChatFilter.setWhiteList(WhiteList(WhiteListWords))

    def tearDown(self):
        ChatFilter.setWhiteList(None)

    def test_open_chat_relayed_to_location_as_sender(self):
        av = makeAvatar()
        av.setChat('  ahoy  ', 0xFF, 1234)
        field = av.dclass.getFieldByName.return_value
        av.dclass.getFieldByName.assert_called_with('setChat')
        field.aiFormatUpdate.assert_called_once_with(
            1, (10 << 32) | 20, SenderChannel, ['ahoy', 11, 0])
        av.air.send.assert_called_once_with(field.aiFormatUpdate.return_value)

    def test_open_chat_from_other_avatar_dropped(self):
        av = makeAvatar(senderId=2)
        av.setChat('ahoy', 1, 0)
        av.air.send.assert_not_called()
        av.air.writeServerEvent.assert_called_once()

    def test_bad_open_chat_dropped(self):
        av = makeAvatar()
        av.setChat('   ', 1, 0)
        av.setChat('x' * 300, 1, 0)
        av.air.send.assert_not_called()

    def test_open_chat_without_location_dropped(self):
        av = makeAvatar(parentId=0, zoneId=0)
        av.setChat('ahoy', 1, 0)
        av.air.send.assert_not_called()

    def test_open_chat_flood(self):
        av = makeAvatar()
        for i in range(5):
            av.setChat('ahoy %d' % i, 1, 0)

        self.assertEqual(av.air.send.call_count, 3)

    def test_whitelist_chat_filtered(self):
        av = makeAvatar()
        av.setWLChat('ahoy you scallywag', 1, 0)
        field = av.dclass.getFieldByName.return_value
        av.dclass.getFieldByName.assert_called_with('setWLChat')
        field.aiFormatUpdate.assert_called_once_with(
            1, (10 << 32) | 20, SenderChannel, ['ahoy arrr arrr', 1, 0])

    def test_speedchat_validation_ejects(self):
        av = makeAvatar()
        av.setSC(100)
        av.setSCCustom(10)
        av.air.kickChannel.assert_not_called()
        av.setSC(5)
        av.air.kickChannel.assert_called_once_with(SenderChannel, ChatFilter.ChatBootCode, unittest.mock.ANY)

    def test_speedchat_relayed_to_location_as_sender(self):
        av = makeAvatar()
        av.setSC(100)
        av.setSCCustom(10)
        names = [c.args[0] for c in av.dclass.getFieldByName.call_args_list]
        field = av.dclass.getFieldByName.return_value
        self.assertEqual(names, ['setSC', 'setSCCustom'])
        self.assertEqual(field.aiFormatUpdate.call_args_list, [
            call(1, (10 << 32) | 20, SenderChannel, [100]),
            call(1, (10 << 32) | 20, SenderChannel, [10])])
        self.assertEqual(av.air.send.call_count, 2)

    def test_invalid_or_spoofed_speedchat_not_relayed(self):
        av = makeAvatar()
        av.setSC(5)
        av.setSCCustom(65535)
        av.air.send.assert_not_called()
        self.assertEqual(av.air.kickChannel.call_count, 2)

        av = makeAvatar(senderId=2)
        av.setSC(100)
        av.air.send.assert_not_called()

    def test_speedchat_flood(self):
        av = makeAvatar()
        for i in range(5):
            av.setSC(100)

        self.assertEqual(av.air.send.call_count, 3)
        av.air.kickChannel.assert_not_called()

    def test_whisper_relayed_to_owner(self):
        av = makeAvatar(doId=2, senderId=1)
        av.chatFlood = ChatFilter.ChatFlood(limit=10, window=5.0)
        av.setWhisperFrom(1, ' psst ', 0)
        av.setWhisperWLFrom(1, 'ahoy landlubber', 0)
        av.setWhisperSCFrom(1, 100)
        av.setWhisperSCCustomFrom(1, 10)
        av.setWhisperSCEmoteFrom(1, 0)
        self.assertEqual(av.sendUpdateToAvatarId.call_args_list, [
            call(2, 'setWhisperFrom', [1, 'psst', 0]),
            call(2, 'setWhisperWLFrom', [1, 'ahoy arrr', 0]),
            call(2, 'setWhisperSCFrom', [1, 100]),
            call(2, 'setWhisperSCCustomFrom', [1, 10]),
            call(2, 'setWhisperSCEmoteFrom', [1, 0])])

    def test_spoofed_and_bad_whispers_dropped(self):
        av = makeAvatar(doId=2, senderId=1)
        av.setWhisperFrom(3, 'i am someone else', 0)
        av.setWhisperSCFrom(1, 5)
        av.setWhisperSCCustomFrom(1, 65535)
        av.setWhisperSCEmoteFrom(1, 60000)
        av.setWhisperFrom(1, 'x' * 300, 0)
        av.sendUpdateToAvatarId.assert_not_called()

    def test_whisper_flood_shared_per_sender(self):
        first = makeAvatar(doId=2, senderId=1)
        second = makeAvatar(doId=3, senderId=1)
        second.chatFlood = first.chatFlood
        first.setWhisperFrom(1, 'one', 0)
        second.setWhisperFrom(1, 'two', 0)
        first.setWhisperFrom(1, 'three', 0)
        second.setWhisperFrom(1, 'four', 0)
        self.assertEqual(first.sendUpdateToAvatarId.call_count + second.sendUpdateToAvatarId.call_count, 3)


if __name__ == '__main__':
    unittest.main()
