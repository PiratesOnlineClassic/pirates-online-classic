import os
import sys
import types
import unittest

from panda3d.core import Filename
from panda3d.direct import DCFile

# semidbm is only installed on real servers; give the import something to find.
if 'semidbm' not in sys.modules:
    try:
        import semidbm
    except ImportError:
        sys.modules['semidbm'] = types.ModuleType('semidbm')

from otp.distributed.OtpDoGlobals import OTP_DO_ID_AVATAR_FRIENDS_MANAGER, OTP_DO_ID_PLAYER_FRIENDS_MANAGER
from otp.otpbase import OTPGlobals
from otp.uberdog.RejectCode import RejectCode
from pirates.friends.PCAvatarFriendsManagerUD import PCAvatarFriendsManagerUD
from pirates.friends.PCPlayerFriendsManagerUD import PCPlayerFriendsManagerUD


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_dcFile = None


def getDcFile():
    global _dcFile
    if _dcFile is None:
        _dcFile = DCFile()
        for name in ('otp.dc', 'pirates.dc'):
            path = os.path.join(ROOT, 'astron', 'dclass', name)
            assert _dcFile.read(Filename.fromOsSpecific(path)), path

    return _dcFile


def puppet(avId):
    return avId + (1001 << 32)


def account(accountId):
    return accountId + (1003 << 32)


class FakeDatabase:

    def __init__(self, air):
        self.air = air
        self.objects = {}
        self.queries = []
        self.updates = []

    def queryObject(self, dbId, doId, callback, dclass=None, fieldNames=()):
        self.queries.append((doId, callback))

    def updateObject(self, dbId, doId, dclass, newFields, oldFields=None, callback=None):
        self.updates.append((doId, newFields))
        self.objects.setdefault(doId, {}).update(newFields)

    def flush(self):
        # Answer every outstanding query, including ones made while answering.
        while self.queries:
            doId, callback = self.queries.pop(0)
            if doId in self.objects:
                callback(self.air.dclassesByName['DistributedPlayerPirateUD'], self.objects[doId])
            else:
                callback(None, None)


class FakeDBM(dict):

    def sync(self):
        pass

    def close(self):
        pass


class FakeAir:

    def __init__(self):
        dcFile = getDcFile()
        self.dclassesByName = {
            'PCAvatarFriendsManagerUD': dcFile.getClassByName('PCAvatarFriendsManager'),
            'PCPlayerFriendsManagerUD': dcFile.getClassByName('PCPlayerFriendsManager'),
            'DistributedPlayerPirateUD': dcFile.getClassByName('DistributedPlayerPirate'),
        }
        self.ourChannel = 4000
        self.dbId = 4003
        self.dbInterface = FakeDatabase(self)
        self.updates = []
        self.datagrams = []
        self.events = []
        self.sender = 0

    def getAvatarIdFromSender(self):
        return self.sender & 0xFFFFFFFF

    def getAccountIdFromSender(self):
        return (self.sender >> 32) & 0xFFFFFFFF

    def sendUpdateToChannel(self, do, channelId, fieldName, args):
        # Pack it for real so struct/argument mistakes show up here.
        field = do.dclass.getFieldByName(fieldName)
        assert field is not None, fieldName
        field.aiFormatUpdate(do.doId, channelId, self.ourChannel, args)
        self.updates.append((channelId, fieldName, args))

    def send(self, datagram):
        self.datagrams.append(datagram)

    def writeServerEvent(self, *args, **kwargs):
        self.events.append((args, kwargs))

    def addPirate(self, avId, name, accountId, friends=()):
        self.dbInterface.objects[avId] = {
            'setName': (name,),
            'setDISLid': (accountId,),
            'setAccountName': ('',),
            'setFriendsList': ([(friendId, 0) for friendId in friends],),
        }


class AvatarFriendsManagerUDTests(unittest.TestCase):

    def setUp(self):
        self.air = FakeAir()
        self.mgr = PCAvatarFriendsManagerUD(self.air)
        self.mgr.doId = OTP_DO_ID_AVATAR_FRIENDS_MANAGER

    def online(self, avId, accountId):
        self.mgr.comingOnline(avId, accountId)
        self.air.dbInterface.flush()

    def sentTo(self, channel, fieldName=None):
        return [(f, a) for c, f, a in self.air.updates
                if c == channel and (fieldName is None or f == fieldName)]

    def request(self, avId, accountId, fieldName, *args):
        self.air.sender = accountId << 32 | avId
        getattr(self.mgr, fieldName)(*args)

    def test_online_sends_friend_list_and_notifies_online_friends(self):
        self.air.addPirate(100000001, 'Jack', 1, friends=[100000002, 100000003])
        self.air.addPirate(100000002, 'Will', 2, friends=[100000001])
        self.air.addPirate(100000003, 'Elizabeth', 3, friends=[100000001])
        self.online(100000002, 2)
        self.air.updates = []

        self.online(100000001, 1)

        updates = self.sentTo(puppet(100000001), 'updateAvatarFriend')
        self.assertEqual(sorted(u[1][0] for u in updates), [100000002, 100000003])
        info = dict((u[1][0], u[1][1]) for u in updates)
        self.assertEqual(info[100000002][0], 'Will')
        self.assertEqual(info[100000002][3], 1)
        self.assertEqual(info[100000003][0], 'Elizabeth')
        self.assertEqual(info[100000003][3], 0)

        # Will hears that Jack is online:
        willUpdates = self.sentTo(puppet(100000002), 'updateAvatarFriend')
        self.assertEqual(len(willUpdates), 1)
        self.assertEqual(willUpdates[0][1][0], 100000001)
        self.assertEqual(willUpdates[0][1][1][3], 1)

        # An offline post remove was registered for Jack's connection:
        self.assertEqual(len(self.air.datagrams), 2)

    def test_offline_notifies_friends(self):
        self.air.addPirate(100000001, 'Jack', 1, friends=[100000002])
        self.air.addPirate(100000002, 'Will', 2, friends=[100000001])
        self.online(100000001, 1)
        self.online(100000002, 2)
        self.air.updates = []

        self.mgr.avatarOffline(100000001)

        updates = self.sentTo(puppet(100000002), 'updateAvatarFriend')
        self.assertEqual(len(updates), 1)
        self.assertEqual(updates[0][1][0], 100000001)
        self.assertEqual(updates[0][1][1][3], 0)
        self.assertFalse(self.mgr.isOnline(100000001))

    def test_offline_during_load_never_comes_online(self):
        self.air.addPirate(100000001, 'Jack', 1)
        self.mgr.comingOnline(100000001, 1)
        self.mgr.goingOffline(100000001)
        self.air.dbInterface.flush()
        self.assertFalse(self.mgr.isOnline(100000001))

    def test_invite_accept_flow(self):
        self.air.addPirate(100000001, 'Jack', 1)
        self.air.addPirate(100000002, 'Will', 2)
        self.online(100000001, 1)
        self.online(100000002, 2)
        self.air.updates = []

        self.request(100000001, 1, 'requestInvite', 100000002)
        self.assertEqual(self.sentTo(puppet(100000002)), [('invitationFrom', [100000001, 'Jack'])])
        self.assertEqual(self.sentTo(puppet(100000001)), [('friendConsidering', [100000002])])

        self.air.updates = []
        self.request(100000002, 2, 'requestInvite', 100000001)

        jackUpdates = self.sentTo(puppet(100000001), 'updateAvatarFriend')
        willUpdates = self.sentTo(puppet(100000002), 'updateAvatarFriend')
        self.assertEqual(jackUpdates[0][1][0], 100000002)
        self.assertEqual(willUpdates[0][1][0], 100000001)
        self.assertTrue(self.mgr.isFriend(100000001, 100000002))
        self.assertTrue(self.mgr.isFriend(100000002, 100000001))
        self.assertFalse(self.mgr.invitations)

        # Both lists went to the DBSS through the avatar objects:
        self.assertEqual(len(self.air.datagrams), 4)

    def test_invite_decline(self):
        self.air.addPirate(100000001, 'Jack', 1)
        self.air.addPirate(100000002, 'Will', 2)
        self.online(100000001, 1)
        self.online(100000002, 2)
        self.request(100000001, 1, 'requestInvite', 100000002)
        self.air.updates = []

        self.request(100000002, 2, 'requestRemove', 100000001)

        self.assertEqual(self.sentTo(puppet(100000001)),
                         [('rejectInvite', [100000002, RejectCode.INVITATION_DECLINED])])
        self.assertFalse(self.mgr.isFriend(100000001, 100000002))

    def test_invite_rejections(self):
        self.air.addPirate(100000001, 'Jack', 1, friends=[100000002])
        self.air.addPirate(100000002, 'Will', 2, friends=[100000001])
        self.air.addPirate(100000003, 'Elizabeth', 3)
        self.online(100000001, 1)
        self.online(100000002, 2)
        self.online(100000003, 3)
        self.air.updates = []

        self.request(100000001, 1, 'requestInvite', 100000002)
        self.request(100000001, 1, 'requestInvite', 100000009)
        self.request(100000001, 1, 'requestInvite', 100000003)
        self.request(100000001, 1, 'requestInvite', 100000003)
        rejects = [a[1][1] for a in self.sentTo(puppet(100000001), 'rejectInvite')]
        self.assertEqual(rejects, [RejectCode.ALREADY_YOUR_FRIEND,
                                   RejectCode.INVITEE_NOT_ONLINE,
                                   RejectCode.ALREADY_INVITED])

    def test_invite_list_full(self):
        friends = list(range(200000000, 200000000 + OTPGlobals.MaxFriends))
        self.air.addPirate(100000001, 'Jack', 1, friends=friends)
        self.air.addPirate(100000002, 'Will', 2)
        self.online(100000001, 1)
        self.online(100000002, 2)
        self.air.updates = []

        self.request(100000002, 2, 'requestInvite', 100000001)
        self.assertEqual(self.sentTo(puppet(100000002), 'rejectInvite'),
                         [('rejectInvite', [100000001, RejectCode.OTHER_FRIENDS_LIST_FULL])])

    def test_inviter_going_offline_retracts(self):
        self.air.addPirate(100000001, 'Jack', 1)
        self.air.addPirate(100000002, 'Will', 2)
        self.online(100000001, 1)
        self.online(100000002, 2)
        self.request(100000001, 1, 'requestInvite', 100000002)
        self.air.updates = []

        self.mgr.goingOffline(100000001)
        self.assertEqual(self.sentTo(puppet(100000002)), [('retractInvite', [100000001])])
        self.assertFalse(self.mgr.invitations)

    def test_remove_online_friend(self):
        self.air.addPirate(100000001, 'Jack', 1, friends=[100000002])
        self.air.addPirate(100000002, 'Will', 2, friends=[100000001])
        self.online(100000001, 1)
        self.online(100000002, 2)
        self.air.updates = []

        self.request(100000001, 1, 'requestRemove', 100000002)
        self.assertEqual(self.sentTo(puppet(100000001)), [('removeAvatarFriend', [100000002])])
        self.assertEqual(self.sentTo(puppet(100000002)), [('removeAvatarFriend', [100000001])])
        self.assertFalse(self.mgr.isFriend(100000001, 100000002))
        self.assertFalse(self.mgr.isFriend(100000002, 100000001))

    def test_remove_offline_friend_updates_database(self):
        self.air.addPirate(100000001, 'Jack', 1, friends=[100000002])
        self.air.addPirate(100000002, 'Will', 2, friends=[100000001, 100000005])
        self.online(100000001, 1)
        self.air.updates = []

        self.request(100000001, 1, 'requestRemove', 100000002)
        self.air.dbInterface.flush()

        self.assertEqual(self.sentTo(puppet(100000001)), [('removeAvatarFriend', [100000002])])
        self.assertEqual(self.sentTo(puppet(100000002)), [])
        self.assertIn((100000002, {'setFriendsList': ([(100000005, 0)],)}), self.air.dbInterface.updates)

    def test_remove_non_friend(self):
        self.air.addPirate(100000001, 'Jack', 1)
        self.online(100000001, 1)
        self.air.updates = []

        self.request(100000001, 1, 'requestRemove', 100000002)
        self.assertEqual(self.sentTo(puppet(100000001)),
                         [('rejectRemove', [100000002, RejectCode.ALREADY_NOT_YOUR_FRIEND])])

    def test_offline_post_remove_is_avatar_offline_field(self):
        self.air.addPirate(100000001, 'Jack', 1)
        self.online(100000001, 1)
        self.assertEqual(len(self.air.datagrams), 1)
        field = self.mgr.dclass.getFieldByName('avatarOffline')
        expected = field.aiFormatUpdate(self.mgr.doId, self.mgr.doId, self.air.ourChannel, [100000001])
        self.assertIn(expected.getMessage(), self.air.datagrams[0].getMessage())


class PlayerFriendsManagerUDTests(unittest.TestCase):

    def setUp(self):
        self.air = FakeAir()
        self.mgr = PCPlayerFriendsManagerUD(self.air)
        self.mgr.doId = OTP_DO_ID_PLAYER_FRIENDS_MANAGER
        self.mgr.dbm = FakeDBM()

    def online(self, avId, accountId):
        self.mgr.comingOnline(avId, accountId)
        self.air.dbInterface.flush()

    def sentTo(self, accountId, fieldName=None):
        return [(f, a) for c, f, a in self.air.updates
                if c == account(accountId) and (fieldName is None or f == fieldName)]

    def request(self, avId, accountId, fieldName, *args):
        self.air.sender = accountId << 32 | avId
        getattr(self.mgr, fieldName)(*args)

    def befriend(self):
        self.air.addPirate(100000001, 'Jack', 1)
        self.air.addPirate(100000002, 'Will', 2)
        self.online(100000001, 1)
        self.online(100000002, 2)
        self.request(100000001, 1, 'requestInvite', 0, 100000002, 1)
        self.request(100000002, 2, 'requestInvite', 0, 100000001, 1)

    def test_invite_accept_flow(self):
        self.air.addPirate(100000001, 'Jack', 1)
        self.air.addPirate(100000002, 'Will', 2)
        self.online(100000001, 1)
        self.online(100000002, 2)
        self.air.updates = []

        self.request(100000001, 1, 'requestInvite', 0, 100000002, 1)
        self.assertEqual(self.sentTo(2), [('invitationFrom', [100000001, 'Jack'])])

        self.air.updates = []
        self.request(100000002, 2, 'requestInvite', 0, 100000001, 1)

        jack = self.sentTo(1, 'updatePlayerFriend')
        will = self.sentTo(2, 'updatePlayerFriend')
        self.assertEqual(jack[0][1][0], 2)
        # The inviter's client matches on the invitee's avatar id:
        self.assertEqual(jack[0][1][1][1], 100000002)
        self.assertEqual(jack[0][1][1][7], 'Pirates')
        self.assertEqual(will[0][1][0], 1)
        self.assertEqual(self.mgr.getFriendIds(1), [2])
        self.assertEqual(self.mgr.getFriendIds(2), [1])

    def test_decline(self):
        self.air.addPirate(100000001, 'Jack', 1)
        self.air.addPirate(100000002, 'Will', 2)
        self.online(100000001, 1)
        self.online(100000002, 2)
        self.request(100000001, 1, 'requestInvite', 0, 100000002, 1)
        self.air.updates = []

        self.request(100000002, 2, 'requestDecline', 0, 100000001)
        self.assertEqual(self.sentTo(1), [('rejectInvite', [100000002, RejectCode.INVITATION_DECLINED])])
        self.assertEqual(self.mgr.getFriendIds(1), [])

    def test_friends_persist_and_reload(self):
        self.befriend()
        self.mgr.avatarOffline(100000002)
        offline = self.sentTo(1, 'updatePlayerFriend')[-1]
        self.assertEqual(offline[1][0], 2)
        self.assertEqual(offline[1][1][3], 0)
        self.assertEqual(offline[1][1][0], 'Will')

        self.air.updates = []
        self.online(100000002, 2)
        will = self.sentTo(2, 'updatePlayerFriend')
        self.assertEqual(will[0][1][0], 1)
        self.assertEqual(will[0][1][1][3], 1)
        jack = self.sentTo(1, 'updatePlayerFriend')
        self.assertEqual(jack[0][1][1][3], 1)

    def test_remove(self):
        self.befriend()
        self.air.updates = []
        self.request(100000001, 1, 'requestRemove', 0, 2)
        self.assertEqual(self.sentTo(1), [('removePlayerFriend', [2])])
        self.assertEqual(self.sentTo(2), [('removePlayerFriend', [1])])
        self.assertEqual(self.mgr.getFriendIds(1), [])

        self.air.updates = []
        self.request(100000001, 1, 'requestRemove', 0, 2)
        self.assertEqual(self.sentTo(1), [('rejectRemove', [2, RejectCode.ALREADY_NOT_YOUR_FRIEND])])

    def test_secret_round_trip(self):
        self.air.addPirate(100000001, 'Jack', 1)
        self.air.addPirate(100000002, 'Will', 2)
        self.online(100000001, 1)
        self.online(100000002, 2)
        self.air.updates = []

        self.request(100000001, 1, 'requestUnlimitedSecret', 0)
        secret = self.sentTo(1, 'secretResponse')[0][1][0]
        self.assertEqual(len(secret), 7)

        self.request(100000001, 1, 'requestUseUnlimitedSecret', 0, secret)
        self.assertEqual(self.sentTo(1, 'rejectUseSecret'), [('rejectUseSecret', ['own secret'])])

        self.request(100000002, 2, 'requestUseUnlimitedSecret', 0, ' %s ' % secret.upper())
        self.assertEqual(self.mgr.getFriendIds(2), [1])
        self.assertEqual(self.sentTo(2, 'updatePlayerFriend')[0][1][0], 1)

        # One use only:
        self.mgr.breakFriends(1, 2)
        self.request(100000002, 2, 'requestUseUnlimitedSecret', 0, secret)
        self.assertEqual(self.sentTo(2, 'rejectUseSecret'), [('rejectUseSecret', ['unknown secret'])])

    def test_secret_expires_and_limit(self):
        self.air.addPirate(100000001, 'Jack', 1)
        self.online(100000001, 1)
        self.mgr.MaxSecrets = 2
        self.request(100000001, 1, 'requestLimitedSecret', 0, 'parent', 'password')
        self.request(100000001, 1, 'requestUnlimitedSecret', 0)
        self.request(100000001, 1, 'requestUnlimitedSecret', 0)
        self.assertEqual(len(self.sentTo(1, 'secretResponse')), 2)
        self.assertEqual(len(self.sentTo(1, 'rejectSecret')), 1)

        self.mgr.SecretLifetime = -1
        for secret in self.mgr.getAccount(1)['secrets']:
            self.mgr._PlayerFriendsManagerUD__store('secret-%s' % secret, {'accountId': 1, 'expires': 0})

        self.request(100000001, 1, 'requestUnlimitedSecret', 0)
        self.assertEqual(len(self.sentTo(1, 'secretResponse')), 3)

    def test_parent_password_check_is_silent(self):
        self.air.addPirate(100000001, 'Jack', 1)
        self.online(100000001, 1)
        self.air.updates = []
        self.request(100000001, 1, 'requestUseLimitedSecret', 0, '', 'parent', 'password')
        self.assertEqual(self.air.updates, [])

    def test_whispers_only_between_friends(self):
        self.air.addPirate(100000003, 'Elizabeth', 3)
        self.befriend()
        self.online(100000003, 3)
        self.air.updates = []

        self.request(100000001, 1, 'whisperTo', 0, 2, 'ahoy')
        self.request(100000001, 1, 'whisperWLTo', 0, 2, 'ahoy')
        self.request(100000001, 1, 'whisperTo', 0, 3, 'ahoy')
        self.assertEqual(self.sentTo(2), [('whisperFrom', [1, 'ahoy']), ('whisperWLFrom', [1, 'ahoy'])])
        self.assertEqual(self.sentTo(3), [])

        datagrams = len(self.air.datagrams)
        self.request(100000001, 1, 'whisperSCTo', 0, 2, 100)
        self.assertEqual(len(self.air.datagrams), datagrams + 1)

    def test_invitee_offline_rejects_inviter(self):
        self.air.addPirate(100000001, 'Jack', 1)
        self.air.addPirate(100000002, 'Will', 2)
        self.online(100000001, 1)
        self.online(100000002, 2)
        self.request(100000001, 1, 'requestInvite', 0, 100000002, 1)
        self.air.updates = []

        self.mgr.goingOffline(100000002)
        self.assertEqual(self.sentTo(1, 'rejectInvite'),
                         [('rejectInvite', [100000002, RejectCode.INVITEE_NOT_ONLINE])])

    def test_switching_avatars(self):
        self.befriend()
        self.air.addPirate(100000004, 'Jack Two', 1)
        self.mgr.goingOffline(100000001)
        self.air.updates = []
        self.online(100000004, 1)

        will = self.sentTo(2, 'updatePlayerFriend')
        self.assertEqual(will[-1][1][1][1], 100000004)
        self.assertEqual(will[-1][1][1][0], 'Jack Two')


if __name__ == '__main__':
    unittest.main()
