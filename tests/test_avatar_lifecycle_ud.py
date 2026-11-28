import builtins
import importlib
import importlib.util
import os
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from panda3d.core import ConfigVariableBool, ConfigVariableInt
from panda3d.core import ConfigVariableString, Filename
from panda3d.direct import DCFile

from pirates.piratesbase import PiratesGlobals


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class _Config:

    def GetString(self, name, default=''):
        return ConfigVariableString(name, default).getValue()

    def GetInt(self, name, default=0):
        return ConfigVariableInt(name, default).getValue()

    def GetBool(self, name, default=False):
        return ConfigVariableBool(name, default).getValue()


def _load_csm_module():
    stubbedBase = not hasattr(builtins, 'base')
    if stubbedBase:
        builtins.base = SimpleNamespace(config=_Config())
    constants = types.ModuleType('pirates.quest.QuestConstants')
    constants.LocationIds = SimpleNamespace(PORT_ROYAL_ISLAND='1150922126.8dzlu')
    stubs = {'pirates.quest.QuestConstants': constants}
    if importlib.util.find_spec('semidbm') is None:
        stubs['semidbm'] = types.ModuleType('semidbm')
    with patch.dict(sys.modules, stubs):
        sys.modules.pop('pirates.uberdog.ClientServicesManagerUD', None)
        module = importlib.import_module('pirates.uberdog.ClientServicesManagerUD')
    sys.modules.pop('pirates.uberdog.ClientServicesManagerUD', None)
    if stubbedBase:
        del builtins.base
    return module


csm = _load_csm_module()

_dcFile = None


def getDClasses():
    global _dcFile
    if _dcFile is None:
        _dcFile = DCFile()
        for name in ('otp.dc', 'pirates.dc'):
            path = os.path.join(ROOT, 'astron', 'dclass', name)
            assert _dcFile.read(Filename.fromOsSpecific(path)), path

    dclasses = {}
    for i in range(_dcFile.getNumClasses()):
        dclass = _dcFile.getClass(i)
        dclasses[dclass.getName()] = dclass

    dclasses['DistributedPlayerPirateUD'] = dclasses['DistributedPlayerPirate']
    dclasses['AccountUD'] = dclasses['Account']
    return dclasses


ACCOUNT_ID = 1000001
AV_UNFINISHED = 100000001
AV_FINISHED = 100000002


def unfinishedPirate(accountId=ACCOUNT_ID, **extra):
    fields = {
        'setName': ('dbp',),
        'WishNameState': ('OPEN',),
        'WishName': ('',),
        'setTutorial': (PiratesGlobals.TUT_STARTED,),
        'setDISLid': (accountId,),
        'setFriendsList': ([],),
    }
    fields.update(extra)
    return fields


def finishedPirate(accountId=ACCOUNT_ID, **extra):
    fields = unfinishedPirate(accountId, **extra)
    fields.update({'setName': ('Will Swiftbeard',), 'WishNameState': ('',),
                   'setTutorial': (PiratesGlobals.TUT_MADE_PIRATE,)})
    fields.update(extra)
    return fields


class FakeDatabase:
    """
    Answers queries asynchronously (on flush), just like the real database.
    """

    def __init__(self, dclasses):
        self.dclasses = dclasses
        self.objects = {}
        self.pending = []
        self.deleted = []

    def add(self, doId, className, fields):
        self.objects[doId] = (className, dict(fields))

    def queryObject(self, dbId, doId, callback, dclass=None, fieldNames=()):
        def answer():
            if doId not in self.objects:
                callback(None, None)
                return

            className, fields = self.objects[doId]
            callback(self.dclasses[className], dict(fields))

        self.pending.append(answer)

    def updateObject(self, dbId, doId, dclass, newFields, oldFields=None, callback=None):
        className, fields = self.objects[doId]
        if oldFields is None:
            fields.update(newFields)
            if callback:
                callback(None)
            return

        def answer():
            current = dict((key, fields.get(key)) for key in oldFields)
            if any(list(current[key] or []) != list(oldFields[key]) for key in oldFields):
                callback(current)
                return

            fields.update(newFields)
            callback(None)

        self.pending.append(answer)

    def deleteObject(self, dbId, doId):
        self.deleted.append(doId)
        self.objects.pop(doId, None)

    def flush(self):
        while self.pending:
            self.pending.pop(0)()


class FakeNetMessenger:

    def __init__(self):
        self.accepted = {}

    def accept(self, message, obj, method):
        self.accepted[message] = method

    def prepare(self, message, sentArgs=[]):
        return SimpleNamespace(getMessage=lambda: b'', message=message, args=sentArgs)


def makeManager():
    dclasses = getDClasses()
    air = SimpleNamespace(
        dclassesByName=dclasses,
        dbId=4003,
        ourChannel=4665,
        dbInterface=FakeDatabase(dclasses),
        netMessenger=FakeNetMessenger(),
        avatarFriendsManager=Mock(),
        playerFriendsManager=Mock(),
        guildManager=Mock(),
        send=Mock(),
        writeServerEvent=Mock(),
        getAccountIdFromSender=Mock(return_value=ACCOUNT_ID),
        getAvatarIdFromSender=Mock(return_value=0),
        getMsgSender=Mock(return_value=ACCOUNT_ID << 32))

    mgr = csm.ClientServicesManagerUD.__new__(csm.ClientServicesManagerUD)
    mgr.air = air
    mgr.connection2fsm = {}
    mgr.account2fsm = {}
    mgr.activeAvatars = {}
    mgr.avatar2removeFsm = {}
    mgr.accountDB = Mock()
    mgr.sendUpdateToAccountId = Mock()
    mgr.killAccount = Mock()
    mgr.GetAccountConnectionChannel = lambda accountId: accountId + (1003 << 32)
    mgr.GetPuppetConnectionChannel = lambda avId: avId + (1001 << 32)
    return mgr


def addAccount(mgr, avSet):
    mgr.air.dbInterface.add(ACCOUNT_ID, 'Account', {
        'ACCOUNT_AV_SET': list(avSet),
        'ACCOUNT_AV_SET_DEL': [],
        'ACCESS_LEVEL': 100,
    })


def accountAvatars(mgr):
    return mgr.air.dbInterface.objects[ACCOUNT_ID][1]['ACCOUNT_AV_SET']


class UnfinishedCriteriaTests(unittest.TestCase):

    def test_placeholder_tutorial_pirate_is_unfinished(self):
        self.assertTrue(csm.isAvatarUnfinished(unfinishedPirate()))
        self.assertTrue(csm.isAvatarUnfinished(unfinishedPirate(setTutorial=(PiratesGlobals.TUT_MADE_PIRATE,))))

    def test_named_or_progressed_pirates_are_finished(self):
        self.assertFalse(csm.isAvatarUnfinished(finishedPirate()))
        # Picked a name pattern in Make-A-Pirate:
        self.assertFalse(csm.isAvatarUnfinished(unfinishedPirate(setName=('Will Swiftbeard',))))
        # Typed a name that is waiting for approval:
        self.assertFalse(csm.isAvatarUnfinished(unfinishedPirate(WishNameState=('PENDING',), WishName=('Jack',))))
        # Further along in the tutorial than Make-A-Pirate, whatever the name:
        self.assertFalse(csm.isAvatarUnfinished(unfinishedPirate(setTutorial=(PiratesGlobals.TUT_GOT_SEACHEST,))))


class RemoveUnfinishedAvatarTests(unittest.TestCase):

    def setUp(self):
        self.mgr = makeManager()
        self.db = self.mgr.air.dbInterface

    def test_unfinished_avatar_is_removed_from_account_and_database(self):
        addAccount(self.mgr, [AV_FINISHED, AV_UNFINISHED, 0, 0])
        self.db.add(AV_UNFINISHED, 'DistributedPlayerPirate', unfinishedPirate(setInventoryId=(300,)))
        self.db.add(300, 'PirateInventory', {'setDoIds': ([(1004, 400)],)})
        self.db.add(400, 'DistributedQuest', {})
        callback = Mock()

        self.mgr.removeUnfinishedAvatar(ACCOUNT_ID, AV_UNFINISHED, callback)
        self.db.flush()

        callback.assert_called_once_with(True)
        self.assertEqual(accountAvatars(self.mgr), [AV_FINISHED, 0, 0, 0])
        self.assertEqual(sorted(self.db.deleted), [300, 400, AV_UNFINISHED])
        self.mgr.air.guildManager.avatarDeleted.assert_called_once_with(AV_UNFINISHED)
        self.mgr.air.avatarFriendsManager.avatarDeleted.assert_called_once_with(AV_UNFINISHED, [])
        self.assertEqual(self.mgr.avatar2removeFsm, {})

    def test_finished_active_or_foreign_avatars_are_never_removed(self):
        addAccount(self.mgr, [AV_FINISHED, AV_UNFINISHED, 0, 0])
        self.db.add(AV_FINISHED, 'DistributedPlayerPirate', finishedPirate())
        self.db.add(AV_UNFINISHED, 'DistributedPlayerPirate', unfinishedPirate(accountId=ACCOUNT_ID + 1))
        callback = Mock()

        self.mgr.removeUnfinishedAvatar(ACCOUNT_ID, AV_FINISHED, callback)
        self.mgr.removeUnfinishedAvatar(ACCOUNT_ID, AV_UNFINISHED, callback)
        self.db.flush()
        self.assertEqual([c[0][0] for c in callback.call_args_list], [False, False])

        self.db.add(AV_UNFINISHED, 'DistributedPlayerPirate', unfinishedPirate())
        self.mgr.activeAvatars[AV_UNFINISHED] = ACCOUNT_ID
        self.mgr.removeUnfinishedAvatar(ACCOUNT_ID, AV_UNFINISHED, callback)
        self.db.flush()

        self.assertEqual(callback.call_args_list[-1][0][0], False)
        self.assertEqual(accountAvatars(self.mgr), [AV_FINISHED, AV_UNFINISHED, 0, 0])
        self.assertEqual(self.db.deleted, [])

    def test_account_changes_in_the_meantime_are_retried(self):
        addAccount(self.mgr, [AV_UNFINISHED, 0, 0, 0])
        self.db.add(AV_UNFINISHED, 'DistributedPlayerPirate', unfinishedPirate())

        self.mgr.removeUnfinishedAvatar(ACCOUNT_ID, AV_UNFINISHED)
        # Answer the avatar and account queries, then sneak in a new pirate:
        self.db.pending.pop(0)()
        self.db.pending.pop(0)()
        self.db.objects[ACCOUNT_ID][1]['ACCOUNT_AV_SET'] = [AV_UNFINISHED, AV_FINISHED, 0, 0]
        self.db.flush()

        self.assertEqual(accountAvatars(self.mgr), [0, AV_FINISHED, 0, 0])
        self.assertIn(AV_UNFINISHED, self.db.deleted)

    def test_disconnect_removes_unfinished_avatar(self):
        addAccount(self.mgr, [AV_UNFINISHED, 0, 0, 0])
        self.db.add(AV_UNFINISHED, 'DistributedPlayerPirate', unfinishedPirate())
        self.mgr.activeAvatars[AV_UNFINISHED] = ACCOUNT_ID

        self.mgr.avatarDisconnected(ACCOUNT_ID, AV_UNFINISHED)
        self.db.flush()

        self.assertFalse(self.mgr.isAvatarActive(AV_UNFINISHED))
        self.assertEqual(accountAvatars(self.mgr), [0, 0, 0, 0])
        self.assertIn(AV_UNFINISHED, self.db.deleted)

    def test_logout_unloads_and_removes_unfinished_avatar(self):
        addAccount(self.mgr, [AV_UNFINISHED, 0, 0, 0])
        self.db.add(AV_UNFINISHED, 'DistributedPlayerPirate', unfinishedPirate())
        self.mgr.activeAvatars[AV_UNFINISHED] = ACCOUNT_ID

        self.mgr.runAccountFSM(csm.UnloadAvatarFSM, AV_UNFINISHED)
        self.assertEqual(self.mgr.account2fsm, {})
        self.assertFalse(self.mgr.isAvatarActive(AV_UNFINISHED))
        self.mgr.air.avatarFriendsManager.goingOffline.assert_called_once_with(AV_UNFINISHED)

        # The client asks for its avatars straight after logging out:
        self.mgr.requestAvatars()
        self.db.flush()

        self.assertEqual(accountAvatars(self.mgr), [0, 0, 0, 0])
        self.mgr.sendUpdateToAccountId.assert_called_once_with(ACCOUNT_ID, 'setAvatars', [[]])
        self.assertEqual(self.mgr.account2fsm, {})


class AvatarListTests(unittest.TestCase):

    def setUp(self):
        self.mgr = makeManager()
        self.db = self.mgr.air.dbInterface

    def test_orphaned_unfinished_avatar_is_removed_before_listing(self):
        addAccount(self.mgr, [AV_FINISHED, AV_UNFINISHED, 0, 0])
        self.db.add(AV_FINISHED, 'DistributedPlayerPirate', finishedPirate())
        self.db.add(AV_UNFINISHED, 'DistributedPlayerPirate', unfinishedPirate())

        self.mgr.requestAvatars()
        self.db.flush()

        avatars = self.mgr.sendUpdateToAccountId.call_args[0][2][0]
        self.assertEqual([av[0] for av in avatars], [AV_FINISHED])
        self.assertEqual(avatars[0][1], 'Will Swiftbeard')
        self.assertEqual(accountAvatars(self.mgr), [AV_FINISHED, 0, 0, 0])
        self.assertEqual(self.mgr.account2fsm, {})

    def test_active_unfinished_avatar_is_listed(self):
        addAccount(self.mgr, [AV_UNFINISHED, 0, 0, 0])
        self.db.add(AV_UNFINISHED, 'DistributedPlayerPirate', unfinishedPirate())
        self.mgr.activeAvatars[AV_UNFINISHED] = ACCOUNT_ID

        self.mgr.requestAvatars()
        self.db.flush()

        avatars = self.mgr.sendUpdateToAccountId.call_args[0][2][0]
        self.assertEqual([av[0] for av in avatars], [AV_UNFINISHED])
        self.assertEqual(self.db.deleted, [])


class DeleteAvatarTests(unittest.TestCase):

    def setUp(self):
        self.mgr = makeManager()
        self.db = self.mgr.air.dbInterface

    def test_delete_acknowledges_and_cleans_up(self):
        addAccount(self.mgr, [AV_FINISHED, 0, 0, 0])
        self.db.add(AV_FINISHED, 'DistributedPlayerPirate', finishedPirate(
            setInventoryId=(300,), setFriendsList=([(100000005, 0)],)))
        self.db.add(300, 'PirateInventory', {'setDoIds': ([(1001, 500), (1001, 600)],)})
        self.db.add(500, 'PlayerShip', {'setInventoryId': (501,)})
        self.db.add(501, 'DistributedInventory', {'setDoIds': ([(1, 502)],)})
        self.db.add(502, 'DistributedHull', {})
        self.db.add(600, 'DistributedPlayerPirate', finishedPirate())

        self.mgr.deleteAvatar(AV_FINISHED)
        self.db.flush()

        # The client asks for the new avatar list itself, so the operation must
        # be over by the time it does:
        self.mgr.sendUpdateToAccountId.assert_called_once_with(
            ACCOUNT_ID, 'acknowledgeDeleteAvatarResp', [AV_FINISHED, True])
        self.assertEqual(self.mgr.account2fsm, {})
        self.assertEqual(accountAvatars(self.mgr), [0, 0, 0, 0])
        self.assertEqual(self.db.objects[ACCOUNT_ID][1]['ACCOUNT_AV_SET_DEL'][0][0], AV_FINISHED)

        self.assertEqual(sorted(self.db.deleted), [300, 500, 501, 502, AV_FINISHED])
        self.assertIn(600, self.db.objects)
        self.mgr.air.avatarFriendsManager.avatarDeleted.assert_called_once_with(AV_FINISHED, [(100000005, 0)])
        self.mgr.air.playerFriendsManager.avatarDeleted.assert_called_once_with(AV_FINISHED, ACCOUNT_ID)
        self.mgr.air.guildManager.avatarDeleted.assert_called_once_with(AV_FINISHED)
        self.mgr.accountDB.removeNameRequest.assert_called_once_with(AV_FINISHED)

    def test_cannot_delete_the_avatar_being_played(self):
        addAccount(self.mgr, [AV_FINISHED, 0, 0, 0])
        self.db.add(AV_FINISHED, 'DistributedPlayerPirate', finishedPirate())
        self.mgr.activeAvatars[AV_FINISHED] = ACCOUNT_ID

        self.mgr.deleteAvatar(AV_FINISHED)
        self.db.flush()

        self.mgr.killAccount.assert_called_once()
        self.assertEqual(accountAvatars(self.mgr), [AV_FINISHED, 0, 0, 0])
        self.assertEqual(self.db.deleted, [])


class FriendsAvatarDeletedTests(unittest.TestCase):

    def test_avatar_friends_forget_deleted_avatar(self):
        from otp.friends.AvatarFriendsManagerUD import AvatarFriendsManagerUD

        mgr = AvatarFriendsManagerUD.__new__(AvatarFriendsManagerUD)
        mgr.onlineAvatars = {100000005: 5}
        mgr.avatarId2Name = {AV_FINISHED: 'Will'}
        mgr.avatarId2Friends = {100000005: [(AV_FINISHED, 0), (100000006, 0)]}
        mgr.invitations = set()
        mgr.operations = set()
        mgr.avatarId2OnlineFsm = {}
        mgr.d_setFriendsList = Mock()
        mgr.d_removeAvatarFriend = Mock()
        mgr.runOperation = Mock()

        mgr.avatarDeleted(AV_FINISHED, [(100000005, 0), (100000007, 0)])

        self.assertEqual(mgr.avatarId2Friends[100000005], [(100000006, 0)])
        mgr.d_removeAvatarFriend.assert_called_once_with(100000005, AV_FINISHED)
        # Offline friends are fixed up through the database:
        self.assertEqual(mgr.runOperation.call_args[0][1:], (100000007, AV_FINISHED))
        self.assertNotIn(AV_FINISHED, mgr.avatarId2Name)


class TravelAgentShardTests(unittest.TestCase):

    def makeAgent(self, shards):
        from pirates.instance.DistributedTravelAgentUD import DistributedTravelAgentUD

        air = SimpleNamespace(dclassesByName={'DistributedTravelAgentUD': getDClasses()['DistributedTravelAgent']},
            netMessenger=FakeNetMessenger(), getAvatarIdFromSender=Mock(return_value=AV_FINISHED),
            districtTracker=SimpleNamespace(getShards=lambda: shards))
        agent = DistributedTravelAgentUD(air)
        agent.sendUpdateToChannel = Mock()
        return agent

    def test_unknown_or_gone_shard_falls_back_to_a_running_one(self):
        agent = self.makeAgent({})
        agent.addShard(401000000, 200000000)
        agent.addShard(402000000, 200000001)
        agent.removeShard(402000000, 200000001)

        agent.requestInitLocUD('unused', 200000001)

        agent.sendUpdateToChannel.assert_called_once_with(401000000, 'requestInitLocUDtoAI', [AV_FINISHED])

    def test_full_shards_are_avoided(self):
        shards = {401000000: {'population': 300, 'populationLimits': [100, 300]},
                  402000000: {'population': 10, 'populationLimits': [100, 300]}}
        agent = self.makeAgent(shards)
        agent.handleDistrictStatus(401000000, {'shardId': 200000000})
        agent.handleDistrictStatus(402000000, {'shardId': 200000001})

        for i in range(10):
            self.assertEqual(agent.getRandomShard(), 200000001)


if __name__ == '__main__':
    unittest.main()
