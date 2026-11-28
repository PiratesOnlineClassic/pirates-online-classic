import importlib.util
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch
from tests import REPO_ROOT

def stub_module(name, **attributes):
    module = types.ModuleType(name)
    for attribute, value in attributes.items():
        setattr(module, attribute, value)
    sys.modules[name] = module


stubbed_modules = (
    'pirates.instance.DistributedInstanceBaseAI',
    'pirates.instance.DistributedTeleportZoneAI',
    'pirates.instance.DistributedTeleportHandlerAI',
    'pirates.world.DistributedGameAreaAI')
missing = object()
original_modules = {name: sys.modules.get(name, missing) for name in stubbed_modules}
stub_module(stubbed_modules[0], DistributedInstanceBaseAI=type('DistributedInstanceBaseAI', (), {}))
stub_module(stubbed_modules[1], DistributedTeleportZoneAI=type('DistributedTeleportZoneAI', (), {}))
stub_module(stubbed_modules[2], DistributedTeleportHandlerAI=type('DistributedTeleportHandlerAI', (), {}))
stub_module(stubbed_modules[3], DistributedGameAreaAI=type('DistributedGameAreaAI', (), {}))

spec = importlib.util.spec_from_file_location(
    '_test_DistributedTeleportMgrAI',
    REPO_ROOT / 'pirates/instance/DistributedTeleportMgrAI.py')
teleport = importlib.util.module_from_spec(spec)
spec.loader.exec_module(teleport)
for name, original in original_modules.items():
    if original is missing:
        del sys.modules[name]
    else:
        sys.modules[name] = original

from pirates.piratesbase import PiratesGlobals


class Avatar:
    doId = 100

    def __init__(self, tutorial_state):
        self.tutorial_state = tutorial_state

    def getReturnLocation(self):
        return 'saved-location'

    def getCurrentIsland(self):
        return ''

    def getTutorial(self):
        return self.tutorial_state

    def getParentObj(self):
        return None


class Area:
    def __init__(self, world, uid):
        self.world = world
        self.uid = uid
        self.parentId = 200
        self.zoneId = 300

    def getUniqueId(self):
        return self.uid

    def getParentObj(self):
        return self.world

    def getUndockable(self):
        return False


class World(teleport.DistributedInstanceBaseAI):
    def __init__(self, uid, instance_type):
        self.uid = uid
        self.instance_type = instance_type
        self.area = Area(self, uid)
        self.builder = SimpleNamespace(
            getObject=self.getObject,
            getIslands=lambda: [self.area])

    def getObject(self, uniqueId):
        self.requestedUid = uniqueId
        return self.area if uniqueId == self.uid else None

    def getType(self):
        return self.instance_type

    def getFileName(self):
        return 'RambleshackWorld'

    def getSpawnPt(self, uniqueId):
        return (0, 0, 0, 0)


class TeleportManagerLocationTests(unittest.TestCase):
    def make_manager(self, world):
        manager = teleport.DistributedTeleportMgrAI.__new__(
            teleport.DistributedTeleportMgrAI)
        manager.air = SimpleNamespace(
            uidMgr=SimpleNamespace(getDoId=lambda uid: 0),
            tutorialManager=SimpleNamespace(avatar2fsm={}, _requestTutorial=Mock()))
        manager.avatar2fsm = {}
        manager.getWorld = lambda requested_type, name: world
        return manager

    def run_teleport(self, instance_type, tutorial_state):
        world = World('jail-interior', instance_type)
        manager = self.make_manager(world)
        avatar = Avatar(tutorial_state)
        tutorial_fsm = object()
        manager.air.tutorialManager.avatar2fsm[avatar.doId] = tutorial_fsm

        with patch.object(teleport, 'TeleportFSM') as teleport_fsm:
            manager.d_initiateTeleport(
                avatar,
                instanceType=instance_type,
                instanceName='RambleshackWorld',
                locationUid='jail-interior',
                spawnPt=(1, 2, 3, 4),
                tutorialFsm=tutorial_fsm)
        manager.air.tutorialManager._requestTutorial.assert_not_called()
        teleport_fsm.assert_called_once_with(
            manager.air, avatar, world, world.area, (1, 2, 3, 4))
        teleport_fsm.return_value.request.assert_called_once_with('Teleporting')

        return world.requestedUid

    def test_tutorial_spawn_uses_explicit_jail_location(self):
        requested_uid = self.run_teleport(
            PiratesGlobals.INSTANCE_TUTORIAL, PiratesGlobals.TUT_STARTED)
        self.assertEqual(requested_uid, 'jail-interior')

    def test_completed_avatar_main_login_keeps_saved_return_location(self):
        requested_uid = self.run_teleport(
            PiratesGlobals.INSTANCE_MAIN, PiratesGlobals.TUT_MET_JOLLY_ROGER)
        self.assertEqual(requested_uid, 'saved-location')

    def test_external_tutorial_entries_reach_manager_even_with_world_or_active_fsm(self):
        avatar = Avatar(PiratesGlobals.TUT_STARTED)
        for world in (None, World('jail-interior', PiratesGlobals.INSTANCE_TUTORIAL)):
            for active in (False, True):
                with self.subTest(world=bool(world), active=active):
                    manager = self.make_manager(world)
                    if active:
                        manager.air.tutorialManager.avatar2fsm[avatar.doId] = object()
                        manager.avatar2fsm[avatar.doId] = object()
                    with patch.object(teleport, 'TeleportFSM') as teleport_fsm:
                        manager.d_initiateTeleport(
                            avatar, PiratesGlobals.INSTANCE_TUTORIAL,
                            'RambleshackWorld', 'jail-interior')
                    manager.air.tutorialManager._requestTutorial.assert_called_once_with(avatar)
                    teleport_fsm.assert_not_called()

    def test_unrelated_fsm_cannot_bypass_tutorial_manager(self):
        avatar = Avatar(PiratesGlobals.TUT_STARTED)
        manager = self.make_manager(World('jail-interior', PiratesGlobals.INSTANCE_TUTORIAL))
        manager.air.tutorialManager.avatar2fsm[avatar.doId] = object()
        with patch.object(teleport, 'TeleportFSM') as teleport_fsm:
            manager.d_initiateTeleport(
                avatar, PiratesGlobals.INSTANCE_TUTORIAL, 'RambleshackWorld',
                'jail-interior', (1, 2, 3, 4), tutorialFsm=object())
        manager.air.tutorialManager._requestTutorial.assert_called_once_with(avatar)
        teleport_fsm.assert_not_called()


if __name__ == '__main__':
    unittest.main()
