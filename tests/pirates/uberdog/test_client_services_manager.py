import ast
import builtins
import importlib
import os
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from otp.otpbase.OTPUtil import Enum

from otp.otpbase import OTPGlobals
from pirates.pirate.HumanDNA import HumanDNA


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def _loadClientServicesManager():
    # The client CSM imports requests for a disabled address lookup:
    stubs = {}
    if 'requests' not in sys.modules:
        requests = types.ModuleType('requests')
        requests.get = Mock()
        stubs['requests'] = requests

    with patch.dict(sys.modules, stubs):
        return importlib.import_module('pirates.uberdog.ClientServicesManager')


def _loadWishNameRepository():
    # OTPClientRepository needs a running ShowBase to be imported, compile only
    # its wish name methods:
    path = os.path.join(ROOT, 'otp', 'distributed', 'OTPClientRepository.py')
    tree = ast.parse(open(path).read())
    crClass = [node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'OTPClientRepository'][0]
    wanted = ('WishNameResult', 'sendWishName', 'sendWishNameAnonymous', 'getWishNameResultMsg', 'gotWishnameResult')
    body = []
    for node in crClass.body:
        if isinstance(node, ast.FunctionDef) and node.name in wanted:
            body.append(node)
        elif isinstance(node, ast.Assign) and node.targets[0].id in wanted:
            body.append(node)

    crClass.body = body
    crClass.bases = []
    module = ast.Module(body=[crClass], type_ignores=[])
    namespace = {'Enum': Enum}
    exec(compile(module, path, 'exec'), namespace)
    return namespace['OTPClientRepository']


csmModule = _loadClientServicesManager()
ClientServicesManager = csmModule.ClientServicesManager
OTPClientRepository = _loadWishNameRepository()


def makeCSM():
    mgr = ClientServicesManager.__new__(ClientServicesManager)
    mgr.cr = Mock()
    mgr.sendUpdate = Mock()
    return mgr


def potentialPirate(avId, name, slot, nameState=0, wishName='', defaultShard=0, lastLogout=0):
    return [avId, name, HumanDNA('m').makeNetString(), slot, nameState, wishName, defaultShard, lastLogout]


class SetAvatarsTests(unittest.TestCase):

    def test_pirates_are_shown_in_their_own_slots(self):
        mgr = makeCSM()
        mgr.setAvatars([
            potentialPirate(100000003, 'Ben Badbane', 3, defaultShard=401000000, lastLogout=29000000),
            potentialPirate(100000001, 'Bess', 1)])

        avList = mgr.cr.handleAvatarsList.call_args[0][0]
        slots = avList[1]
        self.assertEqual(len(slots), 4)
        self.assertEqual(slots[0], OTPGlobals.AvatarSlotAvailable)
        self.assertEqual(slots[2], OTPGlobals.AvatarSlotAvailable)
        self.assertEqual((slots[1].id, slots[1].position, slots[1].name), (100000001, 1, 'Bess'))
        self.assertEqual((slots[3].id, slots[3].position), (100000003, 3))
        self.assertEqual((slots[3].defaultShard, slots[3].lastLogout), (401000000, 29000000))
        # The chooser shows the pirate's name from its DNA:
        self.assertEqual(slots[3].dna.getDNAName(), 'Ben Badbane')

    def test_name_states_map_to_the_choosers_wish_states(self):
        mgr = makeCSM()
        mgr.setAvatars([
            potentialPirate(1, 'Temp One', 0, ClientServicesManager.NameStateClosed),
            potentialPirate(2, 'Temp Two', 1, ClientServicesManager.NameStateOpen),
            potentialPirate(3, 'Temp Three', 2, ClientServicesManager.NameStatePending),
            potentialPirate(4, 'Temp Four', 3, ClientServicesManager.NameStateApproved, 'Typedname')])
        slots = mgr.cr.handleAvatarsList.call_args[0][0][1]
        self.assertEqual([av.wishState for av in slots], ['CLOSED', 'OPEN', 'PENDING', 'APPROVED'])
        self.assertEqual(slots[3].wishName, 'Typedname')
        self.assertEqual(slots[3].name, 'Temp Four')
        self.assertEqual(slots[1].allowedName, 1)

        mgr.setAvatars([potentialPirate(5, 'Temp Five', 0, ClientServicesManager.NameStateRejected)])
        slots = mgr.cr.handleAvatarsList.call_args[0][0][1]
        self.assertEqual(slots[0].wishState, 'DENIED')


class WishNameTests(unittest.TestCase):

    def setUp(self):
        self.cr = OTPClientRepository.__new__(OTPClientRepository)
        self.cr.csm = makeCSM()
        self.results = []
        patcher = patch.object(builtins, 'messenger', SimpleNamespace(
            send=lambda event, args=[]: self.results.append((event, args))), create=True)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_typed_names_are_sent_to_the_csm(self):
        self.cr.sendWishName(100000001, 'Typedname')
        self.cr.csm.sendUpdate.assert_called_once_with('setNameTyped', [100000001, 'Typedname'])

        self.cr.csm.setNameTypedResp(100000001, 1)
        WNR = OTPClientRepository.WishNameResult
        self.assertEqual(self.results, [(self.cr.getWishNameResultMsg(), [WNR.PendingApproval, 100000001, 'Typedname'])])

    def test_anonymous_name_check(self):
        self.cr.sendWishNameAnonymous('Badname')
        self.cr.csm.sendUpdate.assert_called_once_with('setNameTyped', [0, 'Badname'])

        self.cr.csm.setNameTypedResp(0, 0)
        WNR = OTPClientRepository.WishNameResult
        self.assertEqual(self.results, [(self.cr.getWishNameResultMsg(), [WNR.Failure, 0, 'Badname'])])

        # A stray response is ignored:
        self.cr.csm.setNameTypedResp(0, 1)
        self.assertEqual(len(self.results), 1)


if __name__ == '__main__':
    unittest.main()
