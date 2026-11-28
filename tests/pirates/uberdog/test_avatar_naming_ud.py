import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from panda3d.direct import DCPacker

from pirates.pirate.HumanDNA import HumanDNA
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.DistributedAvatarManagerUD import makePatternName

from tests.test_avatar_lifecycle_ud import ACCOUNT_ID, AV_FINISHED, AV_UNFINISHED
from tests.test_avatar_lifecycle_ud import FakeDatabase, accountAvatars, addAccount
from tests.test_avatar_lifecycle_ud import csm, finishedPirate, makeManager, unfinishedPirate


PATTERN_NAME = makePatternName('m', 5, 2, 3)


class CreatingDatabase(FakeDatabase):

    def __init__(self, dclasses):
        FakeDatabase.__init__(self, dclasses)
        self.nextDoId = 100000010

    def createObject(self, dbId, dclass, fields, callback):
        doId = self.nextDoId
        self.nextDoId += 1
        self.add(doId, dclass.getName(), fields)
        callback(doId)


def makeNamingManager():
    mgr = makeManager()
    mgr.air.dbInterface = CreatingDatabase(mgr.air.dclassesByName)
    mgr.air.avatarNameChanged = Mock()
    mgr.accountDB.addNameRequest.return_value = 'Success'
    mgr.accountDB.getNameStatus.return_value = 'PENDING'
    return mgr


def avatarFields(mgr, avId):
    return mgr.air.dbInterface.objects[avId][1]


def sentAvatars(mgr):
    for call in reversed(mgr.sendUpdateToAccountId.call_args_list):
        if call[0][1] == 'setAvatars':
            return call[0][2][0]


class NameHelperTests(unittest.TestCase):

    def test_pattern_names_are_recognized(self):
        self.assertEqual(PATTERN_NAME, 'Ben Badbane')
        self.assertTrue(csm.isNamePattern(PATTERN_NAME, 'm'))
        self.assertTrue(csm.isNamePattern('Ben', 'm'))
        self.assertFalse(csm.isNamePattern('Captain Typedname', 'm'))
        self.assertFalse(csm.isNamePattern('', 'm'))

    def test_temporary_names_are_pattern_names(self):
        for gender in ('m', 'f'):
            name = csm.makeTemporaryName(gender)
            self.assertTrue(name)
            self.assertNotEqual(name, csm.DefaultAvatarName)
            self.assertTrue(csm.isNamePattern(name, gender), name)


class CreateAvatarNameTests(unittest.TestCase):

    def setUp(self):
        self.mgr = makeNamingManager()
        self.db = self.mgr.air.dbInterface
        addAccount(self.mgr, [AV_FINISHED, 0, 0, 0])
        config = SimpleNamespace(GetBool=lambda name, default=False: default)
        patcher = patch.object(csm, 'base', SimpleNamespace(config=config), create=True)
        patcher.start()
        self.addCleanup(patcher.stop)

    def create(self, name, gender='m'):
        dna = HumanDNA(gender)
        self.mgr.createAvatar(dna.makeNetString(), 1, name)
        self.db.flush()
        avId = accountAvatars(self.mgr)[1]
        self.assertTrue(avId)
        self.mgr.sendUpdateToAccountId.assert_called_with(ACCOUNT_ID, 'createAvatarResp', [avId])
        self.assertEqual(self.mgr.account2fsm, {})
        return avatarFields(self.mgr, avId)

    def test_tutorial_placeholder_pirate_stays_open(self):
        fields = self.create(csm.DefaultAvatarName)
        self.assertEqual(fields['setName'], (csm.DefaultAvatarName,))
        self.assertEqual(fields['WishNameState'], ('OPEN',))
        self.assertTrue(csm.isAvatarUnfinished(fields))
        self.mgr.accountDB.addNameRequest.assert_not_called()

    def test_pattern_name_is_final(self):
        fields = self.create(PATTERN_NAME)
        self.assertEqual(fields['setName'], (PATTERN_NAME,))
        self.assertEqual(fields['WishNameState'], ('',))
        self.mgr.accountDB.addNameRequest.assert_not_called()

    def test_typed_name_waits_for_approval_under_a_temporary_name(self):
        fields = self.create('Captain Typedname')
        self.assertNotEqual(fields['setName'][0], 'Captain Typedname')
        self.assertTrue(csm.isNamePattern(fields['setName'][0], 'm'))
        self.assertEqual(fields['WishNameState'], ('PENDING',))
        self.assertEqual(fields['WishName'], ('Captain Typedname',))
        avId = accountAvatars(self.mgr)[1]
        self.mgr.accountDB.addNameRequest.assert_called_once_with(avId, 'Captain Typedname')
        self.assertFalse(csm.isAvatarUnfinished(fields))

    def test_typed_name_refused_by_the_account_server_is_left_open(self):
        self.mgr.accountDB.addNameRequest.return_value = None
        fields = self.create('Captain Typedname', gender='f')
        self.assertEqual(fields['WishNameState'], ('OPEN',))
        self.assertEqual(fields['WishName'], ('',))
        self.assertTrue(csm.isNamePattern(fields['setName'][0], 'f'))
        self.assertFalse(csm.isAvatarUnfinished(fields))


class AvatarListTests(unittest.TestCase):

    def setUp(self):
        self.mgr = makeNamingManager()
        self.db = self.mgr.air.dbInterface

    def listAvatars(self):
        self.mgr.requestAvatars()
        self.db.flush()
        self.assertEqual(self.mgr.account2fsm, {})
        return dict((av[0], av) for av in sentAvatars(self.mgr))

    def test_list_fields_pack_into_the_dclass(self):
        addAccount(self.mgr, [0, 0, AV_FINISHED, 0])
        self.db.add(AV_FINISHED, 'DistributedPlayerPirate', finishedPirate(
            setDefaultShard=(401000000,), setLastLogout=(29000000,)))

        avatars = self.listAvatars()
        avId, name, dna, slot, nameState, wishName, defaultShard, lastLogout = avatars[AV_FINISHED]
        self.assertEqual((name, slot, nameState, wishName), ('Will Swiftbeard', 2, csm.NameStateClosed, ''))
        self.assertEqual((defaultShard, lastLogout), (401000000, 29000000))
        self.assertTrue(HumanDNA().isValidNetString(dna))

        dclass = self.mgr.air.dclassesByName['ClientServicesManager']
        field = dclass.getFieldByName('setAvatars')
        packer = DCPacker()
        packer.beginPack(field)
        field.packArgs(packer, [list(avatars.values())])
        self.assertTrue(packer.endPack())

    def test_wish_name_states(self):
        pirates = {
            100000020: finishedPirate(WishNameState=('OPEN',)),
            100000021: finishedPirate(WishNameState=('APPROVED',), WishName=('Typedname',)),
            100000022: finishedPirate(WishNameState=('REJECTED',), WishName=('Rudename',)),
            100000023: finishedPirate(WishNameState=('LOCKED',)),
        }
        addAccount(self.mgr, list(pirates))
        for avId, fields in pirates.items():
            self.db.add(avId, 'DistributedPlayerPirate', fields)

        avatars = self.listAvatars()
        self.assertEqual(avatars[100000020][4:6], [csm.NameStateOpen, ''])
        self.assertEqual(avatars[100000021][4:6], [csm.NameStateApproved, 'Typedname'])
        self.assertEqual(avatars[100000021][1], 'Will Swiftbeard')
        self.assertEqual(avatars[100000022][4:6], [csm.NameStateRejected, ''])
        self.assertEqual(avatars[100000023][4:6], [csm.NameStateClosed, ''])
        self.mgr.accountDB.getNameStatus.assert_not_called()

    def test_pending_name_is_refreshed_from_the_account_server(self):
        addAccount(self.mgr, [AV_FINISHED, 0, 0, 0])
        self.db.add(AV_FINISHED, 'DistributedPlayerPirate', finishedPirate(
            WishNameState=('PENDING',), WishName=('Typedname',)))

        avatars = self.listAvatars()
        self.assertEqual(avatars[AV_FINISHED][4], csm.NameStatePending)

        self.mgr.accountDB.getNameStatus.return_value = 'APPROVED'
        avatars = self.listAvatars()
        self.assertEqual(avatars[AV_FINISHED][4:6], [csm.NameStateApproved, 'Typedname'])
        self.assertEqual(avatarFields(self.mgr, AV_FINISHED)['WishNameState'], ('APPROVED',))

    def test_bad_account_server_answer_leaves_the_name_pending(self):
        addAccount(self.mgr, [AV_FINISHED, 0, 0, 0])
        self.db.add(AV_FINISHED, 'DistributedPlayerPirate', finishedPirate(
            WishNameState=('PENDING',), WishName=('Typedname',)))
        self.mgr.accountDB.getNameStatus.return_value = None

        avatars = self.listAvatars()
        self.assertEqual(avatars[AV_FINISHED][4], csm.NameStatePending)
        self.assertEqual(avatarFields(self.mgr, AV_FINISHED)['WishNameState'], ('PENDING',))


class SetNameTypedTests(unittest.TestCase):

    def setUp(self):
        self.mgr = makeNamingManager()
        self.db = self.mgr.air.dbInterface

    def test_anonymous_check_only_judges_the_name(self):
        self.mgr.setNameTyped(0, 'Typedname')
        self.mgr.sendUpdateToAccountId.assert_called_once_with(ACCOUNT_ID, 'setNameTypedResp', [0, True])
        self.mgr.setNameTyped(0, '')
        self.mgr.sendUpdateToAccountId.assert_called_with(ACCOUNT_ID, 'setNameTypedResp', [0, False])
        self.mgr.accountDB.addNameRequest.assert_not_called()
        self.assertEqual(self.mgr.account2fsm, {})

    def test_tutorial_pirate_typed_name_becomes_pending(self):
        addAccount(self.mgr, [AV_UNFINISHED, 0, 0, 0])
        self.db.add(AV_UNFINISHED, 'DistributedPlayerPirate', unfinishedPirate())

        self.mgr.setNameTyped(AV_UNFINISHED, 'Typedname')
        self.db.flush()

        self.mgr.sendUpdateToAccountId.assert_called_once_with(
            ACCOUNT_ID, 'setNameTypedResp', [AV_UNFINISHED, True])
        fields = avatarFields(self.mgr, AV_UNFINISHED)
        self.assertEqual((fields['WishNameState'], fields['WishName']), (('PENDING',), ('Typedname',)))
        self.assertFalse(csm.isAvatarUnfinished(fields))
        self.assertEqual(self.mgr.account2fsm, {})

    def test_rejected_pirate_can_be_renamed(self):
        addAccount(self.mgr, [AV_FINISHED, 0, 0, 0])
        self.db.add(AV_FINISHED, 'DistributedPlayerPirate', finishedPirate(
            WishNameState=('REJECTED',), WishName=('Rudename',)))

        self.mgr.setNameTyped(AV_FINISHED, 'Nicename')
        self.db.flush()

        self.mgr.accountDB.removeNameRequest.assert_called_once_with(AV_FINISHED)
        self.mgr.accountDB.addNameRequest.assert_called_once_with(AV_FINISHED, 'Nicename')
        fields = avatarFields(self.mgr, AV_FINISHED)
        self.assertEqual((fields['WishNameState'], fields['WishName']), (('PENDING',), ('Nicename',)))

    def test_named_pirate_cannot_be_renamed(self):
        addAccount(self.mgr, [AV_FINISHED, 0, 0, 0])
        self.db.add(AV_FINISHED, 'DistributedPlayerPirate', finishedPirate())

        self.mgr.setNameTyped(AV_FINISHED, 'Nicename')
        self.db.flush()

        self.mgr.killAccount.assert_called_once()
        self.mgr.accountDB.addNameRequest.assert_not_called()


class SetNamePatternTests(unittest.TestCase):

    def test_pattern_is_rendered_for_the_pirates_gender(self):
        mgr = makeNamingManager()
        addAccount(mgr, [AV_FINISHED, 0, 0, 0])
        mgr.air.dbInterface.add(AV_FINISHED, 'DistributedPlayerPirate', finishedPirate(
            WishNameState=('REJECTED',), WishName=('Rudename',), setGender=('f',)))

        mgr.setNamePattern(AV_FINISHED, 0, 0, 5, 1, 2, 1, 3, 0)
        mgr.air.dbInterface.flush()

        mgr.sendUpdateToAccountId.assert_called_once_with(ACCOUNT_ID, 'setNamePatternResp', [AV_FINISHED, 1])
        fields = avatarFields(mgr, AV_FINISHED)
        self.assertEqual(fields['setName'], (makePatternName('f', 5, 2, 3),))
        self.assertEqual(fields['WishNameState'], ('',))
        mgr.accountDB.removeNameRequest.assert_called_once_with(AV_FINISHED)
        mgr.air.avatarNameChanged.assert_called_once_with(AV_FINISHED, ACCOUNT_ID, fields['setName'][0])


class PopulateAvatarNameTests(unittest.TestCase):

    def populate(self, usePattern, *pattern):
        mgr = makeNamingManager()
        addAccount(mgr, [AV_UNFINISHED, 0, 0, 0])
        mgr.air.dbInterface.add(AV_UNFINISHED, 'DistributedPlayerPirate', unfinishedPirate(
            WishNameState=('PENDING',), WishName=('Typedname',)))

        mgr.populateAvatar(AV_UNFINISHED, HumanDNA('m').makeNetString(), usePattern, *pattern)
        mgr.air.dbInterface.flush()

        mgr.sendUpdateToAccountId.assert_called_once_with(ACCOUNT_ID, 'populateAvatarResp', [True])
        return avatarFields(mgr, AV_UNFINISHED)

    def test_typed_name_pirate_gets_a_temporary_name(self):
        fields = self.populate(False, 0, 0, 0, 0)
        self.assertNotEqual(fields['setName'][0], csm.DefaultAvatarName)
        self.assertTrue(csm.isNamePattern(fields['setName'][0], 'm'))
        self.assertEqual((fields['WishNameState'], fields['WishName']), (('PENDING',), ('Typedname',)))

    def test_pattern_name(self):
        fields = self.populate(True, 0, 5, 2, 3)
        self.assertEqual(fields['setName'], (PATTERN_NAME,))
        self.assertEqual(fields['WishNameState'], ('',))


class LastLogoutTests(unittest.TestCase):

    def test_leaving_records_the_logout_minute(self):
        mgr = makeNamingManager()
        addAccount(mgr, [AV_FINISHED, 0, 0, 0])
        mgr.air.dbInterface.add(AV_FINISHED, 'DistributedPlayerPirate', finishedPirate())

        with patch.object(csm.time, 'time', return_value=60 * 29000000 + 30):
            mgr.activeAvatars[AV_FINISHED] = ACCOUNT_ID
            mgr.runAccountFSM(csm.UnloadAvatarFSM, AV_FINISHED)
        self.assertEqual(avatarFields(mgr, AV_FINISHED)['setLastLogout'], (29000000,))

        with patch.object(csm.time, 'time', return_value=60 * 29000100):
            mgr.activeAvatars[AV_FINISHED] = ACCOUNT_ID
            mgr.avatarDisconnected(ACCOUNT_ID, AV_FINISHED)
        mgr.air.dbInterface.flush()
        self.assertEqual(avatarFields(mgr, AV_FINISHED)['setLastLogout'], (29000100,))
        self.assertIn(AV_FINISHED, mgr.air.dbInterface.objects)


if __name__ == '__main__':
    unittest.main()
