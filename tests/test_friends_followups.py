import unittest

from direct.distributed.PyDatagramIterator import PyDatagramIterator

from otp.distributed.OtpDoGlobals import OTP_DO_ID_AVATAR_FRIENDS_MANAGER, OTP_DO_ID_PLAYER_FRIENDS_MANAGER
from tests.otp.friends.test_friends_managers_ud import FakeAir, FakeDBM, account, getDcFile, puppet
from pirates.friends.PCAvatarFriendsManagerUD import PCAvatarFriendsManagerUD
from pirates.friends.PCPlayerFriendsManagerUD import PCPlayerFriendsManagerUD

JACK, WILL, LIZ = 100000001, 100000002, 100000003


class FriendsTestBase(unittest.TestCase):

    def setUp(self):
        self.air = FakeAir()
        self.air.dclassesByName['DistributedDinghy'] = getDcFile().getClassByName('DistributedDinghy')
        self.air.msgSender = 0
        self.air.getMsgSender = lambda: self.air.msgSender

        self.afm = PCAvatarFriendsManagerUD(self.air)
        self.afm.doId = OTP_DO_ID_AVATAR_FRIENDS_MANAGER
        self.pfm = PCPlayerFriendsManagerUD(self.air)
        self.pfm.doId = OTP_DO_ID_PLAYER_FRIENDS_MANAGER
        self.pfm.dbm = FakeDBM()
        self.air.avatarFriendsManager = self.afm
        self.air.playerFriendsManager = self.pfm

    def online(self, avId, accountId):
        self.afm.comingOnline(avId, accountId)
        self.pfm.comingOnline(avId, accountId)
        self.air.dbInterface.flush()

    def sentTo(self, channel, fieldName):
        return [a for c, f, a in self.air.updates if c == channel and f == fieldName]

    def makePlayerFriends(self, accountId, otherAccountId):
        for first, second in ((accountId, otherAccountId), (otherAccountId, accountId)):
            accountInfo = self.pfm.getAccount(first)
            accountInfo['friends'].append(second)
            self.pfm.storeAccount(first, accountInfo)


class TestFriendsBandIds(FriendsTestBase):

    def test_band_id_sent_to_avatar_and_player_friends(self):
        self.air.addPirate(JACK, 'Jack', 1, friends=[WILL])
        self.air.addPirate(WILL, 'Will', 2, friends=[JACK])
        self.air.addPirate(LIZ, 'Elizabeth', 3)
        self.makePlayerFriends(1, 3)
        for avId, accountId in ((JACK, 1), (WILL, 2), (LIZ, 3)):
            self.online(avId, accountId)

        self.air.updates = []
        self.afm.setBandId(JACK, 300, 7)
        self.assertEqual(self.sentTo(puppet(WILL), 'setBandId'), [[JACK, 300, 7]])
        self.assertEqual(self.sentTo(account(3), 'setBandId'), [[1, 300, 7]])
        self.assertEqual(self.afm.getBandId(JACK), (300, 7))

        # a fresh friend info forgets the crew, so the crew follows every update:
        self.air.updates = []
        self.afm.d_updateAvatarFriend(WILL, JACK)
        self.assertEqual(self.sentTo(puppet(WILL), 'setBandId'), [[JACK, 300, 7]])
        self.pfm.d_updatePlayerFriend(3, 1)
        self.assertEqual(self.sentTo(account(3), 'setBandId'), [[1, 300, 7]])

        self.afm.setBandId(JACK, 0, 0)
        self.assertEqual(self.afm.getBandId(JACK), (0, 0))
        self.assertEqual(self.sentTo(puppet(WILL), 'setBandId')[-1], [JACK, 0, 0])

    def test_band_id_forgotten_offline(self):
        self.air.addPirate(JACK, 'Jack', 1)
        self.online(JACK, 1)
        self.afm.setBandId(JACK, 300, 7)
        self.afm.goingOffline(JACK)
        self.assertEqual(self.afm.getBandId(JACK), (0, 0))

        self.afm.setBandId(JACK, 300, 7)
        self.assertEqual(self.afm.getBandId(JACK), (0, 0))


class TestFriendsLists(FriendsTestBase):

    def test_deleted_friends_are_pruned_on_load(self):
        self.air.addPirate(WILL, 'Will', 2, friends=[JACK])
        self.air.addPirate(JACK, 'Jack', 1, friends=[WILL, 100000009])
        self.online(JACK, 1)
        self.assertEqual(self.afm.getFriendIds(JACK), [WILL])
        # the avatar is active, so the list is updated through the avatar object
        dclass = self.air.dclassesByName['DistributedPlayerPirateUD']
        expected = dclass.aiFormatUpdate('setFriendsList', JACK, JACK, self.air.ourChannel, [[(WILL, 0)]])
        self.assertIn(expected.getMessage(), [datagram.getMessage() for datagram in self.air.datagrams])

    def test_online_friends_are_declared_for_teleports(self):
        self.air.addPirate(JACK, 'Jack', 1, friends=[WILL])
        self.air.addPirate(WILL, 'Will', 2, friends=[JACK])
        self.online(JACK, 1)
        self.assertEqual(self.air.declares, [])

        self.online(WILL, 2)
        self.assertIn((puppet(JACK), True, WILL), self.air.declares)
        self.assertIn((puppet(WILL), True, JACK), self.air.declares)

        self.air.sender = 1 << 32 | JACK
        self.afm.requestRemove(WILL)
        self.assertIn((puppet(JACK), False, WILL), self.air.declares)
        self.assertIn((puppet(WILL), False, JACK), self.air.declares)

    def test_player_friends_are_declared_for_teleports(self):
        self.air.addPirate(JACK, 'Jack', 1)
        self.air.addPirate(WILL, 'Will', 2)
        self.makePlayerFriends(1, 2)
        self.online(JACK, 1)
        self.online(WILL, 2)
        self.assertIn((account(1), True, WILL), self.air.declares)
        self.assertIn((account(2), True, JACK), self.air.declares)

    def test_dinghy_friends_list(self):
        self.air.addPirate(JACK, 'Jack', 1, friends=[WILL])
        self.air.addPirate(WILL, 'Will', 2, friends=[JACK])
        self.air.addPirate(LIZ, 'Elizabeth', 3)
        self.makePlayerFriends(1, 3)
        for avId, accountId in ((JACK, 1), (WILL, 2), (LIZ, 3)):
            self.online(avId, accountId)

        self.air.datagrams = []
        self.air.msgSender = 1234
        self.afm.requestDinghyFriendsList(5555, JACK, 1)
        self.assertEqual(len(self.air.datagrams), 1)

        dgi = PyDatagramIterator(self.air.datagrams[0])
        self.assertEqual(dgi.getUint8(), 1)
        self.assertEqual(dgi.getUint64(), 1234)
        dclass = getDcFile().getClassByName('DistributedDinghy')
        expected = dclass.aiFormatUpdate('responseFriendsList', 5555, 1234, self.air.ourChannel, [JACK, [WILL, LIZ]])
        self.assertEqual(self.air.datagrams[0].getMessage(), expected.getMessage())


class TestAvatarRenames(FriendsTestBase):

    def test_rename_reaches_online_friends(self):
        self.air.addPirate(JACK, 'Jack', 1, friends=[WILL])
        self.air.addPirate(WILL, 'Will', 2, friends=[JACK])
        self.makePlayerFriends(1, 2)
        self.online(JACK, 1)
        self.online(WILL, 2)
        self.afm.goingOffline(JACK)
        self.pfm.goingOffline(JACK)

        self.air.updates = []
        self.afm.avatarNameChanged(JACK, 1, 'Captain Jack')
        self.pfm.avatarNameChanged(JACK, 1, 'Captain Jack')
        self.assertEqual(self.sentTo(puppet(WILL), 'updateAvatarName'), [[JACK, 'Captain Jack']])
        self.assertEqual(self.sentTo(puppet(WILL), 'updateAvatarFriend')[-1][1][0], 'Captain Jack')
        self.assertEqual(self.sentTo(account(2), 'updatePlayerFriend')[-1][1][0], 'Captain Jack')
        self.assertEqual(self.pfm.getAccount(1)['avatarName'], 'Captain Jack')

        # nothing to tell when the name is the same
        self.air.updates = []
        self.afm.avatarNameChanged(JACK, 1, 'Captain Jack')
        self.pfm.avatarNameChanged(JACK, 1, 'Captain Jack')
        self.assertEqual(self.air.updates, [])


if __name__ == '__main__':
    unittest.main()
