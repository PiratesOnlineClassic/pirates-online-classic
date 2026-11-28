import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from otp.otpbase import OTPGlobals
from pirates.pirate.HumanDNA import HumanDNA

from tests.test_avatar_lifecycle_ud import ACCOUNT_ID, _Config, addAccount, csm, makeManager

FULL = OTPGlobals.AccessFull
VELVET = OTPGlobals.AccessVelvetRope


def membership(enabled=True):
    return patch.object(csm.MembershipGlobals, 'wantMembership', return_value=enabled)


class FakeConfig(_Config):

    def __init__(self, **values):
        self.values = values

    def GetString(self, name, default=''):
        return self.values.get(name, default)


def withConfig(**values):
    return patch.object(builtins, 'base', SimpleNamespace(config=FakeConfig(**values)), create=True)


class AccountAccessTests(unittest.TestCase):

    def test_everybody_is_paid_without_membership(self):
        with membership(False), withConfig(**{'default-account-access': 'VELVET'}):
            self.assertEqual(csm.getAccountAccess(VELVET, VELVET), FULL)
            self.assertEqual(csm.getAccountAccess(), FULL)

    def test_override_then_account_then_default(self):
        with membership(), withConfig():
            self.assertEqual(csm.getAccountAccess(FULL, VELVET), VELVET)
            self.assertEqual(csm.getAccountAccess(VELVET), VELVET)
            self.assertEqual(csm.getAccountAccess(), FULL)

        with membership(), withConfig(**{'default-account-access': 'basic'}):
            self.assertEqual(csm.getAccountAccess(), VELVET)
            self.assertEqual(csm.getAccountAccess(FULL), FULL)

    def test_access_names(self):
        self.assertEqual(csm.parseAccess('FULL'), FULL)
        self.assertEqual(csm.parseAccess('velvet'), VELVET)
        self.assertEqual(csm.parseAccess('1'), VELVET)
        self.assertEqual(csm.parseAccess(2), FULL)
        self.assertEqual(csm.parseAccess(7), OTPGlobals.AccessUnknown)
        self.assertEqual(csm.parseAccess('gold'), OTPGlobals.AccessUnknown)

    def test_freebooter_accounts_override_developer_logins(self):
        callback = Mock()
        db = csm.DeveloperAccountDB.__new__(csm.DeveloperAccountDB)
        db.dbm = {}
        with withConfig(**{'freebooter-accounts': 'alice bob'}):
            db.lookup('alice', callback)
            db.lookup('carol', callback)

        self.assertEqual(callback.call_args_list[0][0][0]['access'], VELVET)
        self.assertNotIn('access', callback.call_args_list[1][0][0])


class LoginTests(unittest.TestCase):

    def setUp(self):
        self.mgr = makeManager()
        self.mgr.sendUpdateToChannel = Mock()
        self.target = 5000

    def login(self, result):
        self.mgr.accountDB.lookup = lambda token, callback: callback(dict(result, success=True))
        fsm = csm.LoginAccountFSM(self.mgr, self.target)
        self.mgr.connection2fsm[self.target] = fsm
        fsm.request('Start', 'token')
        self.mgr.air.dbInterface.flush()
        return self.mgr.sendUpdateToChannel.call_args

    def test_paid_login(self):
        addAccount(self.mgr, [0, 0, 0, 0])
        with withConfig():
            args = self.login({'userId': 'dev', 'accountId': ACCOUNT_ID})

        self.assertEqual(args[0], (self.target, 'acceptLogin', [FULL, 4, 4]))
        self.assertEqual(self.mgr.getAccountAccess(ACCOUNT_ID, {}), FULL)

    def test_freebooter_login(self):
        addAccount(self.mgr, [0, 0, 0, 0])
        with membership(), withConfig():
            args = self.login({'userId': 'dev', 'accountId': ACCOUNT_ID, 'access': VELVET})

        self.assertEqual(args[0], (self.target, 'acceptLogin', [VELVET, 2, 4]))
        # a developer override is not stored on the account:
        self.assertNotIn('PAID_LEVEL', self.mgr.air.dbInterface.objects[ACCOUNT_ID][1])

    def test_account_server_access_is_stored(self):
        addAccount(self.mgr, [0, 0, 0, 0])
        with membership(), withConfig():
            args = self.login({'userId': 'dev', 'accountId': ACCOUNT_ID, 'paidLevel': VELVET})

        self.assertEqual(args[0][2][0], VELVET)
        self.assertEqual(self.mgr.air.dbInterface.objects[ACCOUNT_ID][1]['PAID_LEVEL'], VELVET)

    def test_stored_access_is_used(self):
        addAccount(self.mgr, [0, 0, 0, 0])
        self.mgr.air.dbInterface.objects[ACCOUNT_ID][1]['PAID_LEVEL'] = VELVET
        with membership(), withConfig():
            args = self.login({'userId': 'dev', 'accountId': ACCOUNT_ID})

        self.assertEqual(args[0][2][0], VELVET)

        # ...but not while want-membership is off:
        with membership(False), withConfig():
            args = self.login({'userId': 'dev', 'accountId': ACCOUNT_ID})

        self.assertEqual(args[0][2][0], FULL)


class CreateAvatarSlotTests(unittest.TestCase):

    def setUp(self):
        self.mgr = makeManager()

    def create(self, index):
        self.mgr.runAccountFSM(csm.CreateAvatarFSM, HumanDNA('m').makeNetString(), index, 'dbp')
        self.mgr.air.dbInterface.flush()

    def test_freebooter_cannot_fill_unlimited_access_slots(self):
        addAccount(self.mgr, [100000001, 100000002, 0, 0])
        self.mgr.setAccountAccess(ACCOUNT_ID, VELVET)
        with membership(), withConfig():
            self.create(2)

        self.mgr.killAccount.assert_called_once()
        self.assertIn('Unlimited Access', self.mgr.killAccount.call_args[0][1])

    def test_freebooter_may_fill_free_slots(self):
        addAccount(self.mgr, [100000001, 0, 0, 0])
        self.mgr.setAccountAccess(ACCOUNT_ID, VELVET)
        self.mgr.air.dbInterface.createObject = Mock()
        with membership(), withConfig():
            self.create(1)

        self.mgr.killAccount.assert_not_called()
        self.mgr.air.dbInterface.createObject.assert_called_once()

    def test_members_fill_every_slot(self):
        addAccount(self.mgr, [100000001, 100000002, 100000003, 0])
        self.mgr.setAccountAccess(ACCOUNT_ID, FULL)
        self.mgr.air.dbInterface.createObject = Mock()
        with membership(), withConfig():
            self.create(3)

        self.mgr.killAccount.assert_not_called()
        self.mgr.air.dbInterface.createObject.assert_called_once()


if __name__ == '__main__':
    unittest.main()
