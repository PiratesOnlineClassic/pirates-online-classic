import importlib.util
import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from pirates.piratesbase import PiratesGlobals


def _load_teleport_module():
    stubs = {
        'pirates.quest.QuestConstants': {'LocationIds': SimpleNamespace(
            KINGSHEAD_ISLAND='kingshead')},
        'pirates.instance.DistributedInstanceBaseAI': {
            'DistributedInstanceBaseAI': type('DistributedInstanceBaseAI', (), {})},
        'pirates.instance.DistributedTeleportZoneAI': {
            'DistributedTeleportZoneAI': type('DistributedTeleportZoneAI', (), {})},
        'pirates.instance.DistributedTeleportHandlerAI': {
            'DistributedTeleportHandlerAI': type('DistributedTeleportHandlerAI', (), {})},
        'pirates.world.DistributedGameAreaAI': {
            'DistributedGameAreaAI': type('DistributedGameAreaAI', (), {})},
    }
    modules = {}
    for name, attributes in stubs.items():
        module = types.ModuleType(name)
        module.__dict__.update(attributes)
        modules[name] = module

    with patch.dict(sys.modules, modules):
        spec = importlib.util.spec_from_file_location(
            '_test_DistributedTeleportMgrAI',
            Path(__file__).with_name('DistributedTeleportMgrAI.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return module


teleport = _load_teleport_module()


class _World(teleport.DistributedInstanceBaseAI):

    def __init__(self, instanceType, fileName):
        self.instanceType = instanceType
        self.fileName = fileName

    def getType(self):
        return self.instanceType

    def getFileName(self):
        return self.fileName


class MainWorldLookupTests(unittest.TestCase):

    def makeManager(self, *worlds):
        manager = teleport.DistributedTeleportMgrAI.__new__(teleport.DistributedTeleportMgrAI)
        manager.air = SimpleNamespace(doId2do={
            index: world for index, world in enumerate(worlds)})
        return manager

    def test_generic_main_world_name_resolves_to_the_districts_main_world(self):
        tutorialWorld = _World(PiratesGlobals.INSTANCE_TUTORIAL, 'RambleshackWorld')
        mainWorld = _World(PiratesGlobals.INSTANCE_MAIN, 'piratesWorld')
        manager = self.makeManager(tutorialWorld, mainWorld)

        self.assertIs(manager.getWorld(PiratesGlobals.INSTANCE_MAIN, 'mainWorld'), mainWorld)
        self.assertIs(manager.getWorld(PiratesGlobals.INSTANCE_MAIN, 'piratesWorld'), mainWorld)

    def test_other_instance_types_still_require_an_exact_name(self):
        tutorialWorld = _World(PiratesGlobals.INSTANCE_TUTORIAL, 'RambleshackWorld')
        manager = self.makeManager(tutorialWorld)

        self.assertIsNone(manager.getWorld(PiratesGlobals.INSTANCE_TUTORIAL, 'mainWorld'))
        self.assertIsNone(manager.getWorld(PiratesGlobals.INSTANCE_MAIN, 'mainWorld'))


class TutorialLoginTeleportTests(unittest.TestCase):

    def test_client_tutorial_teleport_is_handed_to_the_tutorial_manager(self):
        # On login the client asks to teleport into the tutorial; the tutorial
        # manager takes it over. Reporting a failure would make the client fall
        # back on a mainWorld teleport that collides with the tutorial's jail teleport.
        avatar = SimpleNamespace(doId=100000004, getTutorial=lambda: 0)
        manager = teleport.DistributedTeleportMgrAI.__new__(teleport.DistributedTeleportMgrAI)
        manager.avatar2fsm = {}
        tutorialManager = SimpleNamespace(avatar2fsm={}, _requestTutorial=Mock())
        manager.air = SimpleNamespace(
            doId2do={avatar.doId: avatar}, districtId=1,
            getAvatarIdFromSender=lambda: avatar.doId,
            tutorialManager=tutorialManager)
        manager.d_teleportFailed = Mock()

        shipModule = types.ModuleType('pirates.ship.DistributedShipAI')
        shipModule.DistributedShipAI = type('DistributedShipAI', (), {})
        with patch.dict(sys.modules, {'pirates.ship.DistributedShipAI': shipModule}):
            manager.initiateTeleport(PiratesGlobals.INSTANCE_TUTORIAL, 0, 0, '', 0,
                'RambleshackWorld', -1, 0, 0)

        tutorialManager._requestTutorial.assert_called_once_with(avatar)
        manager.d_teleportFailed.assert_not_called()
        self.assertEqual(manager.avatar2fsm, {})


if __name__ == '__main__':
    unittest.main()
