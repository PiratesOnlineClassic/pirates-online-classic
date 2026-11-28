import importlib.util
import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

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


if __name__ == '__main__':
    unittest.main()
