import builtins
import collections
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch

from panda3d.core import loadPrcFileData

loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

from pirates.piratesbase import PiratesGlobals


class FakeBuilder:

    def __init__(self, air, parent):
        self.air = air
        self.parent = parent


def _stubModule(name, **attrs):
    module = types.ModuleType(name)
    for attrName, value in attrs.items():
        setattr(module, attrName, value)

    return module


# the area builders and the level editor object list pull in the entire client
# avatar stack and the game resources, none of which are needed here...
_stubs = {
    'pirates.world.ClientAreaBuilderAI': _stubModule('pirates.world.ClientAreaBuilderAI',
        ClientAreaBuilderAI=FakeBuilder),
    'pirates.world.GameAreaBuilderAI': _stubModule('pirates.world.GameAreaBuilderAI',
        GameAreaBuilderAI=FakeBuilder),
    'pirates.leveleditor.ObjectList': _stubModule('pirates.leveleditor.ObjectList',
        AREA_TYPE_ISLAND_REGION='Island Game Area', LOCATOR_NODE='Locator Node'),
}

for _name in ('pirates.interact.DistributedSearchableContainerAI', 'pirates.world.DistributedDinghyAI',
              'pirates.battle.DistributedIslandCannonAI', 'pirates.treasuremap.DistributedBuriedTreasureAI',
              'pirates.treasuremap.DistributedSurfaceTreasureAI'):
    _stubs[_name] = _stubModule(_name, **{_name.rsplit('.', 1)[1]: MagicMock()})

with patch.dict(sys.modules, _stubs):
    for _name in ('pirates.world.IslandAreaBuilderAI', 'pirates.instance.DistributedInstanceBaseAI'):
        sys.modules.pop(_name, None)

    from pirates.world import IslandAreaBuilderAI as builder_module
    from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI

    # don't leave the modules built against the stubs behind for other tests...
    for _name in ('pirates.world.IslandAreaBuilderAI', 'pirates.instance.DistributedInstanceBaseAI'):
        sys.modules.pop(_name, None)


class FakeWorld:

    def __init__(self, instanceType):
        self.type = instanceType
        self.builder = SimpleNamespace(addObject=Mock())
        self.generateChildWithRequired = Mock()
        self.subInstances = []

    def getType(self):
        return self.type

    def addSubInstance(self, subInstance):
        self.subInstances.append(subInstance)


class IslandGameAreaTests(unittest.TestCase):

    def createGameArea(self, world):
        module = builder_module
        gameArea = MagicMock()
        subInstance = FakeWorld(PiratesGlobals.INSTANCE_GENERIC)
        subInstance.setParentInstance = Mock()
        worldCreator = SimpleNamespace(world=world, createWorldInstance=Mock(return_value=subInstance),
            linkManager=SimpleNamespace(registerLinkData=Mock()),
            locatorManager=SimpleNamespace(addLocator=Mock()),
            loadObjectsFromFile=Mock())

        builder = SimpleNamespace(parent=SimpleNamespace(getParentObj=lambda: world),
            air=SimpleNamespace(worldCreator=worldCreator, allocateZone=Mock(return_value=600)),
            notify=Mock())

        interiorModule = types.ModuleType('pirates.world.DistributedGAInteriorAI')
        interiorModule.DistributedGAInteriorAI = Mock(return_value=gameArea)
        with patch.dict(sys.modules, {'pirates.world.DistributedGAInteriorAI': interiorModule}):
            result = module.IslandAreaBuilderAI.createGameArea(builder,
                {'File': 'pvp_jungle', 'Visual': {'Model': 'jungle'}, 'Objects': {}},
                None, 'island', 'jungle', False)

        return result, gameArea, subInstance, worldCreator

    def test_pvp_game_areas_are_generated_within_the_pvp_instance(self):
        world = FakeWorld(PiratesGlobals.INSTANCE_PVP)
        result, gameArea, subInstance, worldCreator = self.createGameArea(world)
        self.assertIs(result, gameArea)
        worldCreator.createWorldInstance.assert_not_called()
        world.generateChildWithRequired.assert_called_once_with(gameArea, 600)
        world.builder.addObject.assert_called_once_with(gameArea)
        worldCreator.loadObjectsFromFile.assert_called_once_with('pvp_jungle.py', gameArea)

    def test_other_game_areas_get_a_tracked_sub_instance(self):
        world = FakeWorld(PiratesGlobals.INSTANCE_MAIN)
        result, gameArea, subInstance, worldCreator = self.createGameArea(world)
        worldCreator.createWorldInstance.assert_called_once()
        subInstance.generateChildWithRequired.assert_called_once_with(gameArea, 600)
        subInstance.setParentInstance.assert_called_once_with(world)
        self.assertEqual(world.subInstances, [subInstance])
        world.generateChildWithRequired.assert_not_called()


class SubInstanceTests(unittest.TestCase):

    def makeInstance(self, air, doId):
        instance = DistributedInstanceBaseAI(air)
        instance.doId = doId
        air.doId2do[doId] = instance
        return instance

    def test_sub_instances_are_deleted_with_their_parent(self):
        air = SimpleNamespace(doId2do={}, dclassesByName=collections.defaultdict(MagicMock))
        parent = self.makeInstance(air, 100)
        child = self.makeInstance(air, 101)
        child.requestDelete = Mock()
        child.setParentInstance(parent)
        parent.addSubInstance(child)
        self.assertEqual(parent.getSubInstances(), [child])
        self.assertIs(child.getParentInstance(), parent)

        with patch('direct.distributed.DistributedObjectAI.DistributedObjectAI.delete'):
            parent.delete()

        child.requestDelete.assert_called_once_with()
        self.assertEqual(parent.getSubInstances(), [])
        self.assertIsNone(child.getParentInstance())

    def test_deleted_sub_instance_leaves_its_parent(self):
        air = SimpleNamespace(doId2do={}, dclassesByName=collections.defaultdict(MagicMock))
        parent = self.makeInstance(air, 100)
        child = self.makeInstance(air, 101)
        child.setParentInstance(parent)
        parent.addSubInstance(child)

        with patch('direct.distributed.DistributedObjectAI.DistributedObjectAI.delete'):
            child.delete()

        self.assertEqual(parent.getSubInstances(), [])


if __name__ == '__main__':
    unittest.main()
