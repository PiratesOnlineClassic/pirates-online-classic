import unittest
from unittest.mock import Mock

from otp.uberdog.RejectCode import RejectCode
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.DistributedAvatarManagerUD import (
    DistributedAvatarManagerUD,
    makePatternName,
)


ACCOUNT_ID = 1000
AV_ID = 100000001


class FakeDBInterface:
    def __init__(self, objects):
        self.objects = objects
        self.updates = []

    def queryObject(self, dbId, doId, callback):
        dclass, fields = self.objects.get(doId, (None, {}))
        callback(dclass, fields)

    def updateObject(self, dbId, doId, dclass, newFields, oldFields=None, callback=None):
        self.updates.append((doId, newFields, oldFields))


def makeManager(avatarFields=None, avSet=(AV_ID,)):
    accountClass = object()
    pirateClass = object()
    objects = {ACCOUNT_ID: (accountClass, {'ACCOUNT_AV_SET': list(avSet)})}
    if avatarFields is not None:
        objects[AV_ID] = (pirateClass, avatarFields)

    air = Mock()
    air.dbId = 4003
    air.ourChannel = 4321
    air.dclassesByName = {'AccountUD': accountClass, 'DistributedPlayerPirateUD': pirateClass}
    air.dbInterface = FakeDBInterface(objects)
    air.getAccountIdFromSender.return_value = ACCOUNT_ID
    air.getMsgSender.return_value = 777

    mgr = DistributedAvatarManagerUD.__new__(DistributedAvatarManagerUD)
    mgr.air = air
    mgr.doId = 4674
    mgr.account2fsm = {}
    mgr.sendUpdateToAccountId = Mock()
    mgr.sendUpdateToChannel = Mock()
    mgr.killAccount = Mock()
    return mgr


def firstIndex(nameList):
    for index, name in enumerate(nameList):
        if name.strip():
            return index


class AvatarManagerUDTests(unittest.TestCase):
    def test_make_pattern_name(self):
        first = firstIndex(PiratesGlobals.maleNames[1])
        prefix = firstIndex(PiratesGlobals.maleNames[2])
        suffix = firstIndex(PiratesGlobals.maleNames[3])
        name = makePatternName('m', first, prefix, suffix)
        self.assertTrue(name.startswith(PiratesGlobals.maleNames[1][first].strip()))
        self.assertEqual(makePatternName('m', 0, 0, 0), '')
        self.assertEqual(makePatternName('f', 99999, -1, 99999), '')

    def test_pattern_name_updates_open_avatar(self):
        mgr = makeManager({'WishNameState': ('OPEN',), 'WishName': ('',),
                           'setName': ('Pirate',), 'setGender': ('m',)})
        first = firstIndex(PiratesGlobals.maleNames[1])
        mgr.requestPatternName(0, AV_ID, 0, first, 0, 0)

        doId, fields, _ = mgr.air.dbInterface.updates[0]
        self.assertEqual(doId, AV_ID)
        self.assertEqual(fields['setName'], (PiratesGlobals.maleNames[1][first].strip(),))
        mgr.sendUpdateToAccountId.assert_called_with(ACCOUNT_ID, 'patternNameResponse', [True])
        self.assertEqual(mgr.account2fsm, {})

    def test_pattern_name_rejected_when_not_open(self):
        mgr = makeManager({'WishNameState': ('',), 'WishName': ('',),
                           'setName': ('Pirate',), 'setGender': ('m',)})
        mgr.requestPatternName(0, AV_ID, 0, 1, 0, 0)
        self.assertEqual(mgr.air.dbInterface.updates, [])
        mgr.sendUpdateToAccountId.assert_called_with(ACCOUNT_ID, 'patternNameResponse', [False])

    def test_pattern_name_renames_rejected_avatar(self):
        mgr = makeManager({'WishNameState': ('REJECTED',), 'WishName': ('Bad',),
                           'setName': ('Pirate',), 'setGender': ('f',)})
        first = firstIndex(PiratesGlobals.femaleNames[1])
        mgr.requestPatternName(0, AV_ID, 0, first, 0, 0)

        _, fields, _ = mgr.air.dbInterface.updates[0]
        self.assertEqual(fields['setName'], (PiratesGlobals.femaleNames[1][first].strip(),))
        self.assertEqual(fields['WishNameState'], ('',))
        mgr.air.csm.accountDB.removeNameRequest.assert_called_with(AV_ID)
        mgr.sendUpdateToAccountId.assert_called_with(ACCOUNT_ID, 'patternNameResponse', [True])

    def test_foreign_avatar_kills_account(self):
        mgr = makeManager({'WishNameState': ('OPEN',)}, avSet=(1,))
        mgr.requestFinalize(0, AV_ID)
        mgr.killAccount.assert_called_once()
        self.assertEqual(mgr.account2fsm, {})

    def test_finalize_approved_name(self):
        mgr = makeManager({'WishNameState': ('APPROVED',), 'WishName': ('Jack Sparrow',),
                           'setName': ('Pirate',)})
        mgr.air.csm = Mock()
        mgr.requestFinalize(0, AV_ID)
        doId, fields, old = mgr.air.dbInterface.updates[0]
        self.assertEqual(fields['setName'], ('Jack Sparrow',))
        self.assertEqual(fields['WishNameState'], ('',))
        self.assertEqual(old['setName'], ('Pirate',))
        mgr.air.csm.accountDB.removeNameRequest.assert_called_with(AV_ID)

    def test_finalize_rejected_name_reopens(self):
        mgr = makeManager({'WishNameState': ('REJECTED',), 'WishName': ('Bad',),
                           'setName': ('Pirate',)})
        mgr.requestFinalize(0, AV_ID)
        _, fields, _ = mgr.air.dbInterface.updates[0]
        self.assertEqual(fields['WishNameState'], ('OPEN',))
        self.assertEqual(fields['setName'], ('Pirate',))

    def test_share_avatar_rejected(self):
        mgr = makeManager({'WishNameState': ('',)})
        mgr.requestShareAvatar(0, AV_ID, 0, 1)
        mgr.sendUpdateToAccountId.assert_called_with(ACCOUNT_ID, 'rejectShareAvatar', [RejectCode.INVALID_ACCOUNT])

    def test_awardable_avatars_and_gender(self):
        mgr = makeManager({'setName': ('Pirate',), 'setGender': ('f',)})
        mgr.requestAwardableAvatars(ACCOUNT_ID, 5)
        mgr.sendUpdateToChannel.assert_called_with(777, 'recvAwardableAvatars', [5, [AV_ID], ['Pirate']])
        mgr.requestAvatarGender(AV_ID, 6)
        mgr.sendUpdateToChannel.assert_called_with(777, 'recvAvatarGender', [AV_ID, 'f', 6])

    def test_duplicate_operation_kills(self):
        mgr = makeManager({'WishNameState': ('OPEN',)})
        mgr.account2fsm[ACCOUNT_ID] = Mock()
        mgr.requestFinalize(0, AV_ID)
        mgr.killAccount.assert_called_once()


if __name__ == '__main__':
    unittest.main()
