import builtins
import unittest
from unittest.mock import Mock, call

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

from otp.chat import ChatFilter
from otp.chat.WhiteList import WhiteList
from pirates.band.DistributedBandMemberAI import DistributedBandMemberAI
from pirates.quest import QuestDB

AV_ID = 100000001
ACCOUNT_ID = 5
SENDER = (ACCOUNT_ID << 32) | AV_ID
MANAGER_ID = 4000
BAND_ZONE = 7
LOCATION = (MANAGER_ID << 32) | BAND_ZONE


def makeMember(senderAvId=AV_ID):
    member = DistributedBandMemberAI.__new__(DistributedBandMemberAI)
    member.air = Mock()
    member.doId = 300
    member.parentId = MANAGER_ID
    member.zoneId = BAND_ZONE
    member.avatarId = AV_ID
    member.bandId = BAND_ZONE
    member.chatFlood = ChatFilter.ChatFlood(limit=3, window=5.0)
    member.air.ourChannel = 1234
    member.air.getAvatarIdFromSender.return_value = senderAvId
    member.air.getMsgSender.return_value = (ACCOUNT_ID << 32) | senderAvId
    member.dclass = Mock()
    return member


def relayed(member):
    """Returns (fieldName, args) for every update relayed to the band zone."""

    updates = []
    names = [c.args[0] for c in member.dclass.getFieldByName.call_args_list]
    formatted = member.dclass.getFieldByName.return_value.aiFormatUpdate.call_args_list
    for name, c in zip(names, formatted):
        doId, channel, sender, args = c.args
        assert (doId, channel, sender) == (300, LOCATION, SENDER), c
        updates.append((name, args))

    return updates


def anyQuest():
    for questInt, questId in QuestDB.questIntDict.items():
        questDNA = QuestDB.QuestDict.get(questId)
        if questDNA is not None and len(questDNA.getTasks()) > 1:
            return questInt, len(questDNA.getTasks())


class CrewChatTests(unittest.TestCase):
    def setUp(self):
        ChatFilter.setWhiteList(WhiteList(['ahoy', 'matey']))

    def tearDown(self):
        ChatFilter.setWhiteList(None)

    def test_typed_chat_relayed_to_band_zone_as_sender(self):
        member = makeMember()
        member.setChat(' ahoy\x01 ', 0xFF, 99)
        member.setWLChat('ahoy landlubber', 1, 99)
        self.assertEqual(relayed(member), [
            ('setChat', ['ahoy', ChatFilter.AllowedChatFlags, 0]),
            ('setWLChat', ['ahoy arrr', 1, 0])])
        self.assertEqual(member.air.send.call_count, 2)

    def test_chat_on_someone_elses_member_dropped(self):
        member = makeMember(senderAvId=AV_ID + 1)
        member.setChat('ahoy', 1, 0)
        member.setSpeedChat(AV_ID + 1, 100)
        member.air.send.assert_not_called()

    def test_bad_typed_chat_dropped(self):
        member = makeMember()
        member.setChat('   ', 1, 0)
        member.setWLChat('x' * 300, 1, 0)
        member.air.send.assert_not_called()

    def test_flood(self):
        member = makeMember()
        for i in range(5):
            member.setChat('ahoy %d' % i, 1, 0)

        self.assertEqual(member.air.send.call_count, 3)

    def test_speedchat(self):
        member = makeMember()
        member.setSpeedChat(AV_ID, 100)
        self.assertEqual(relayed(member), [('setSpeedChat', [AV_ID, 100])])

    def test_speedchat_spoofed_or_unknown_dropped(self):
        member = makeMember()
        member.setSpeedChat(AV_ID + 1, 100)
        # the client's crew menu sends custom phrases on this field too, so
        # an index the crew can't decode is dropped without booting anyone.
        member.setSpeedChat(AV_ID, 5)
        member.air.send.assert_not_called()
        member.air.kickChannel.assert_not_called()

    def test_quest_speedchat(self):
        questInt, numTasks = anyQuest()
        member = makeMember()
        member.setSCQuestChat(AV_ID, questInt, 2, numTasks - 1)
        self.assertEqual(relayed(member), [('setSCQuestChat', [AV_ID, questInt, 2, numTasks - 1])])

    def test_invalid_quest_speedchat_ejects(self):
        questInt, numTasks = anyQuest()
        member = makeMember()
        member.setSCQuestChat(AV_ID, questInt, 3, 0)
        member.setSCQuestChat(AV_ID, questInt, 0, numTasks)
        member.air.send.assert_not_called()
        self.assertEqual(member.air.kickChannel.call_args_list, [
            call(SENDER, ChatFilter.ChatBootCode, unittest.mock.ANY)] * 2)

    def test_not_relayed_without_location(self):
        member = makeMember()
        member.parentId = member.zoneId = 0
        member.setChat('ahoy', 1, 0)
        member.air.send.assert_not_called()


if __name__ == '__main__':
    unittest.main()
