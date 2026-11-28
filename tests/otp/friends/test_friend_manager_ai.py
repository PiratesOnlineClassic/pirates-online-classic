import unittest
from unittest.mock import patch

from otp.avatar.DistributedPlayerAI import DistributedPlayerAI
from otp.friends import FriendManagerAI as FriendManagerAIModule
from otp.friends.FriendManagerAI import FriendManagerAI


def puppet(avId):
    return avId + (1001 << 32)


class FakePlayer:
    # DistributedPlayerAI is a NodePath; borrow just the friends list logic.
    getFriendsList = DistributedPlayerAI.getFriendsList
    extendFriendsList = DistributedPlayerAI.extendFriendsList

    def __init__(self, avId, name):
        self.doId = avId
        self.name = name
        self.friendsList = []
        self.sentFriendsLists = []

    def getName(self):
        return self.name

    def d_setFriendsList(self, friendsList):
        self.sentFriendsLists.append(list(friendsList))


class FakeAir:

    def __init__(self):
        self.doId2do = {}
        self.updates = []
        self.events = []
        self.sender = 0

    def getAvatarIdFromSender(self):
        return self.sender & 0xFFFFFFFF

    def sendUpdateToChannel(self, do, channelId, fieldName, args):
        self.updates.append((channelId, fieldName, args))

    def writeServerEvent(self, *args, **kwargs):
        self.events.append((args, kwargs))


class FriendManagerAITests(unittest.TestCase):

    def setUp(self):
        patcher = patch.object(FriendManagerAIModule, 'DistributedPlayerAI', FakePlayer)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.air = FakeAir()
        self.mgr = object.__new__(FriendManagerAI)
        self.mgr.air = self.air
        self.mgr.doId = 4600
        self.mgr.nextContext = 0
        self.mgr.requests = {}
        self.mgr.secrets = {}
        self.jack = FakePlayer(100000001, 'Jack')
        self.will = FakePlayer(100000002, 'Will')
        self.air.doId2do = {self.jack.doId: self.jack, self.will.doId: self.will}

    def sentTo(self, avId):
        return [(f, a) for c, f, a in self.air.updates if c == puppet(avId)]

    def request(self, av, fieldName, *args):
        self.air.sender = av.doId
        getattr(self.mgr, fieldName)(*args)

    def test_query_accept(self):
        self.request(self.jack, 'friendQuery', self.will.doId)
        query = self.sentTo(self.will.doId)
        self.assertEqual(query[0][0], 'inviteeFriendQuery')
        context = query[0][1][3]

        self.request(self.will, 'inviteeFriendConsidering', 1, context)
        self.assertEqual(self.sentTo(self.jack.doId), [('friendConsidering', [1, context])])

        self.request(self.will, 'inviteeFriendResponse', 1, context)
        self.assertEqual(self.sentTo(self.jack.doId)[-1], ('friendResponse', [1, context]))
        self.assertEqual(self.jack.friendsList, [(self.will.doId, 0)])
        self.assertEqual(self.will.friendsList, [(self.jack.doId, 0)])
        self.assertFalse(self.mgr.requests)

    def test_query_unavailable_and_cancel(self):
        self.request(self.jack, 'friendQuery', 100000099)
        self.assertEqual(self.sentTo(self.jack.doId), [('friendConsidering', [0, 0])])

        self.request(self.jack, 'friendQuery', self.will.doId)
        context = self.sentTo(self.will.doId)[0][1][3]
        self.request(self.jack, 'cancelFriendQuery', context)
        self.assertEqual(self.sentTo(self.will.doId)[-1], ('inviteeCancelFriendQuery', [context]))
        self.request(self.will, 'inviteeAcknowledgeCancel', context)
        self.assertFalse(self.mgr.requests)

    def test_wrong_avatar_cannot_answer(self):
        self.request(self.jack, 'friendQuery', self.will.doId)
        context = self.sentTo(self.will.doId)[0][1][3]
        self.request(self.jack, 'inviteeFriendConsidering', 1, context)
        self.request(self.jack, 'inviteeFriendResponse', 1, context)
        self.assertEqual(self.jack.friendsList, [])

    def test_secrets(self):
        self.request(self.jack, 'requestSecret')
        result, secret = self.sentTo(self.jack.doId)[0][1]
        self.assertEqual(result, 1)

        self.request(self.jack, 'submitSecret', secret)
        self.assertEqual(self.sentTo(self.jack.doId)[-1], ('submitSecretResponse', [3, 0]))

        self.request(self.will, 'submitSecret', secret)
        self.assertEqual(self.sentTo(self.will.doId)[-1], ('submitSecretResponse', [1, self.jack.doId]))
        self.assertEqual(self.will.friendsList, [(self.jack.doId, 0)])

        self.request(self.will, 'submitSecret', secret)
        self.assertEqual(self.sentTo(self.will.doId)[-1], ('submitSecretResponse', [0, 0]))


if __name__ == '__main__':
    unittest.main()
