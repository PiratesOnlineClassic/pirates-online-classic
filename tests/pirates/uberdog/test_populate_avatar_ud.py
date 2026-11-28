import builtins
import importlib
import importlib.util
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from panda3d.core import ConfigVariableBool, ConfigVariableInt
from panda3d.core import ConfigVariableString, Filename
from panda3d.direct import DCFile

from pirates.piratesbase import PiratesGlobals


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


_dcFile = DCFile()


def _loadDClasses():
    dcFile = _dcFile
    if dcFile.getNumClasses():
        dcFile.clear()
    dcFile.read(Filename('astron/dclass/otp.dc'))
    dcFile.read(Filename('astron/dclass/pirates.dc'))
    dclasses = {dcFile.getClass(i).getName(): dcFile.getClass(i)
                for i in range(dcFile.getNumClasses())}
    dclasses['DistributedPlayerPirateUD'] = dclasses['DistributedPlayerPirate']
    return dclasses


class PopulateAvatarTests(unittest.TestCase):

    def makeFSM(self):
        fsm = csm.PopulateAvatarFSM.__new__(csm.PopulateAvatarFSM)
        fsm.avId = 100000001
        fsm.csm = SimpleNamespace(air=SimpleNamespace(
            dclassesByName=_loadDClasses(), ourChannel=4665, send=Mock()))
        fsm.demand = Mock()
        return fsm

    def test_populate_is_refused_once_the_pirate_has_been_made(self):
        fsm = self.makeFSM()
        dclass = fsm.csm.air.dclassesByName['DistributedPlayerPirateUD']

        fsm._PopulateAvatarFSM__handleAvatar(
            dclass, {'setTutorial': (PiratesGlobals.TUT_MADE_PIRATE,)})
        fsm.demand.assert_called_once_with(
            'Kill', 'Tried to populate an avatar that has already been made!')

        fsm.demand.reset_mock()
        fsm._PopulateAvatarFSM__handleAvatar(
            dclass, {'setTutorial': (PiratesGlobals.TUT_STARTED,)})
        fsm.demand.assert_called_once_with('UpdateAvatar')

    def test_live_avatar_receives_the_populated_fields(self):
        fsm = self.makeFSM()

        fsm.sendLiveAvatarFields({'setName': ('Will Swiftbeard',), 'setGender': ('f',)})

        self.assertEqual(fsm.csm.air.send.call_count, 1)


if __name__ == '__main__':
    unittest.main()
