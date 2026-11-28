import builtins
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch

from panda3d.core import Filename, NodePath, Point3, VirtualFileSystem, loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')


def _stubWeaponGlobals():
    # WeaponGlobals reads WeaponGlobals.pkl from the game resources at import
    # time; when the resources are unavailable fall back to a stub module.
    searchPath = '../resources/phase_2/etc'
    if VirtualFileSystem.getGlobalPtr().exists(Filename(searchPath + '/WeaponGlobals.pkl')):
        return

    module = types.ModuleType('pirates.battle.WeaponGlobals')

    def __getattr__(name):
        if name.startswith('__'):
            raise AttributeError(name)

        value = MagicMock(name='WeaponGlobals.%s' % name)
        setattr(module, name, value)
        return value

    module.__getattr__ = __getattr__
    sys.modules['pirates.battle.WeaponGlobals'] = module
    import pirates.battle
    pirates.battle.WeaponGlobals = module


_stubWeaponGlobals()

if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

with patch.object(builtins.loader, 'loadFont', Mock()):
    from pirates.battle import BattleManagerAI

from pirates.battle import DistributedEnemySpawnerAI as spawner_module
from pirates.battle.DistributedEnemySpawnerAI import (DistributedEnemySpawnerAI, EnemySpawnNode,
    SpawnNodeBase, TownfolkSpawnNode)
from pirates.pirate import AvatarTypes
from pirates.pirate.BattleNPCGameFSMAI import BattleNPCGameFSMAI
from pirates.piratesbase import PiratesGlobals
from pirates.world.WorldCreatorAI import WorldCreatorAI
from pirates.world.InteriorAreaBuilderAI import InteriorAreaBuilderAI


ISLAND_UID = 'island'
FORT_UID = 'fort'
SPAWN_UID = 'spawn'
NODE_A_UID = 'nodeA'
NODE_B_UID = 'nodeB'


def makeFileData():
    spawnData = {'Type': 'Spawn Node', 'Pos': Point3(10, 0, 0), 'Hpr': Point3(0, 0, 0),
        'GridPos': Point3(-999, -999, -999), 'Spawnables': 'Crab', 'Pause Chance': '0'}
    nodeAData = {'Type': 'Movement Node', 'Pos': Point3(0, 10, 0), 'Hpr': Point3(0, 0, 0),
        'Pause Chance': '100', 'Pause Duration': '5'}
    nodeBData = {'Type': 'Movement Node', 'Pos': Point3(50, 50, 0), 'Hpr': Point3(0, 0, 0)}
    fortData = {'Type': 'Simple Fort', 'Pos': Point3(100, 200, 30), 'Hpr': Point3(90, 0, 0),
        'Scale': Point3(1, 1, 1), 'Objects': {SPAWN_UID: spawnData, NODE_A_UID: nodeAData}}
    islandData = {'Type': 'Island', 'Pos': Point3(0, 0, 0), 'Hpr': Point3(0, 0, 0),
        'Objects': {FORT_UID: fortData, NODE_B_UID: nodeBData}}
    return {
        'Objects': {ISLAND_UID: islandData},
        'ObjectIds': {
            ISLAND_UID: '["Objects"]["island"]',
            FORT_UID: '["Objects"]["island"]["Objects"]["fort"]',
            SPAWN_UID: '["Objects"]["island"]["Objects"]["fort"]["Objects"]["spawn"]',
            NODE_A_UID: '["Objects"]["island"]["Objects"]["fort"]["Objects"]["nodeA"]',
            NODE_B_UID: '["Objects"]["island"]["Objects"]["nodeB"]',
        },
        'Node Links': [
            [SPAWN_UID, NODE_A_UID, 'Bi-directional'],
            [NODE_A_UID, NODE_B_UID, 'Direction 1'],
        ],
    }


def makeWorldCreator():
    worldCreator = WorldCreatorAI.__new__(WorldCreatorAI)
    worldCreator.fileDicts = {'testIsland.py': makeFileData()}
    return worldCreator


def objectData(uid):
    fileData = makeFileData()
    return eval('fileData' + fileData['ObjectIds'][uid])


class WorldCreatorTransformTests(unittest.TestCase):
    def test_area_objects_use_their_pos_not_the_stale_grid_pos(self):
        worldCreator = makeWorldCreator()
        pos, hpr = worldCreator.getObjectAreaPosHpr(NODE_B_UID, objectData(NODE_B_UID), ISLAND_UID)
        self.assertAlmostEqual((pos - Point3(50, 50, 0)).length(), 0, places=3)

    def test_objects_placed_on_a_prop_are_relative_to_it(self):
        worldCreator = makeWorldCreator()
        pos, hpr = worldCreator.getObjectAreaPosHpr(SPAWN_UID, objectData(SPAWN_UID), ISLAND_UID)

        # the fort is rotated 90 degrees, so it's local x axis is the island's y axis
        self.assertAlmostEqual((pos - Point3(100, 210, 30)).length(), 0, places=3)
        self.assertAlmostEqual(hpr[0], 90, places=3)

    def test_linked_movement_nodes_respect_link_directions(self):
        worldCreator = makeWorldCreator()
        self.assertEqual([uid for uid, data in worldCreator.getLinkedMovementNodes(SPAWN_UID)], [NODE_A_UID])
        self.assertEqual(sorted(uid for uid, data in worldCreator.getLinkedMovementNodes(NODE_A_UID)),
            [NODE_B_UID, SPAWN_UID])

        # 'Direction 1' links may only be walked from the first node to the second
        self.assertEqual(worldCreator.getLinkedMovementNodes(NODE_B_UID), [])


class SpawnNodePropertyTests(unittest.TestCase):
    def makeNode(self, cls=SpawnNodeBase, objectData=None, objType='Spawn Node', populationIndex=0):
        air = SimpleNamespace(worldCreator=makeWorldCreator(), enemySpawner=Mock())
        return cls(air, objType, objectData if objectData is not None else {}, None, SPAWN_UID,
            ISLAND_UID, populationIndex)

    def test_spawn_delay_defaults_to_the_editor_default(self):
        self.assertEqual(self.makeNode().getSpawnDelay(), spawner_module.SPAWN_DELAY_DEFAULT)
        self.assertEqual(self.makeNode(objectData={'SpawnDelay': '45'}).getSpawnDelay(), 45)

    def test_level_property_fixes_the_enemy_level(self):
        node = self.makeNode(objectData={'Level': '18'})
        self.assertEqual(node.getSpawnLevel(AvatarTypes.Veteran), 18)

        with patch.object(spawner_module.EnemyGlobals, 'getRandomEnemyLevel', return_value=7):
            self.assertEqual(self.makeNode(objectData={'Level': ''}).getSpawnLevel(AvatarTypes.Veteran), 7)
            self.assertEqual(self.makeNode().getSpawnLevel(AvatarTypes.Veteran), 7)

    def test_spawn_position_is_relative_to_the_area(self):
        node = self.makeNode(objectData=objectData(SPAWN_UID))
        pos, hpr = node.getSpawnPosHpr()
        self.assertAlmostEqual((pos - Point3(100, 210, 30)).length(), 0, places=3)

    def test_additional_population_spawns_around_the_node(self):
        node = self.makeNode(objectData=objectData(SPAWN_UID), populationIndex=2)
        pos, hpr = node.getSpawnPosHpr()
        distance = (pos - Point3(100, 210, 30)).length()
        self.assertGreaterEqual(distance, spawner_module.POPULATION_SPREAD_RADIUS[0] - 0.001)
        self.assertLessEqual(distance, spawner_module.POPULATION_SPREAD_RADIUS[1] + 0.001)

        # each slot of the population respawns on it's own
        self.assertNotEqual(node.getSpawnTaskName(), self.makeNode().getSpawnTaskName())

    def test_enemy_team_override(self):
        self.assertEqual(self.makeNode(EnemySpawnNode, {'Team': '2'}).getNPCTeam(AvatarTypes.Clod),
            PiratesGlobals.NAVY_TEAM)
        self.assertEqual(self.makeNode(EnemySpawnNode, {'Team': 'default'}).getNPCTeam(AvatarTypes.Clod),
            PiratesGlobals.UNDEAD_TEAM)

        # enemies are never placed on the player's team
        self.assertEqual(self.makeNode(EnemySpawnNode, {'Team': '0'}).getNPCTeam(AvatarTypes.Clod),
            PiratesGlobals.UNDEAD_TEAM)

    def test_townsfolk_team(self):
        self.assertEqual(self.makeNode(TownfolkSpawnNode, {'Team': 'Player'}).getNPCTeam(AvatarTypes.Commoner),
            PiratesGlobals.PLAYER_TEAM)
        self.assertEqual(self.makeNode(TownfolkSpawnNode, {}).getNPCTeam(AvatarTypes.Commoner),
            PiratesGlobals.VILLAGER_TEAM)

    def test_waypoints_are_linked_movement_nodes(self):
        node = self.makeNode(objectData=objectData(SPAWN_UID))
        self.assertTrue(node.hasWaypoints())
        waypointUid, waypointData = node.getLinkedWaypoints()[0]
        self.assertEqual(waypointUid, NODE_A_UID)

        # (0, 10, 0) on the fort rotated by 90 degrees
        pos = node.getWaypointPos(waypointUid, waypointData)
        self.assertAlmostEqual((pos - Point3(90, 200, 30)).length(), 0, places=3)


class SpawnerPopulationTests(unittest.TestCase):
    def test_min_population_creates_a_spawn_node_per_npc(self):
        spawner = DistributedEnemySpawnerAI.__new__(DistributedEnemySpawnerAI)
        spawner.air = SimpleNamespace()
        spawner.spawnNodes = {}

        with patch.object(EnemySpawnNode, 'setup') as setup, \
                patch.object(EnemySpawnNode, '__init__', return_value=None) as init:
            spawner.createObject('Spawn Node', {'Min Population': '3'}, None, ISLAND_UID, SPAWN_UID, False)
            self.assertEqual(len(spawner.getSpawnNodesFromType('Spawn Node')), 3)
            self.assertEqual([call.args[-1] for call in init.call_args_list], [0, 1, 2])
            self.assertEqual(setup.call_count, 3)

            spawner.createObject('Spawn Node', {'Min Population': 'bad'}, None, ISLAND_UID, 'other', False)
            self.assertEqual(len(spawner.getSpawnNodesFromType('Spawn Node')), 4)


class PatrolRouteTests(unittest.TestCase):
    def makeFSM(self):
        node = SpawnNodeBase(SimpleNamespace(worldCreator=makeWorldCreator()), 'Spawn Node',
            objectData(SPAWN_UID), None, SPAWN_UID, ISLAND_UID)

        fsm = BattleNPCGameFSMAI.__new__(BattleNPCGameFSMAI)
        fsm.avatar = SimpleNamespace(spawnNode=node, getSpawnNode=lambda: node,
            getParentObj=lambda: NodePath('area'))
        fsm._BattleNPCGameFSMAI__routeOrigin = None
        fsm.resetWaypoint()
        return fsm, node

    def test_patrol_walks_along_the_linked_movement_nodes(self):
        fsm, node = self.makeFSM()

        # our spawn node never pauses
        self.assertEqual(fsm.getPauseChance(), 0)
        self.assertEqual(fsm.getNextPauseDuration(), 0)

        point = fsm.getPatrolPoint()
        self.assertAlmostEqual((point - Point3(90, 200, 30)).length(), 0, places=3)

        # the movement node we arrived at always pauses for up to 5 seconds
        self.assertEqual(fsm.getPauseChance(), 100)
        self.assertTrue(1.0 <= fsm.getNextPauseDuration() <= 5.0)

        # we don't walk back the way we came unless we have to
        point = fsm.getPatrolPoint()
        self.assertAlmostEqual((point - Point3(50, 50, 0)).length(), 0, places=3)

        # node B is a dead end, as it's link only goes one way...
        self.assertIsNone(fsm.getNextWaypoint())

    def test_fights_on_a_patrol_route_are_leashed_to_where_we_left_it(self):
        fsm, node = self.makeFSM()
        fsm.avatar.getSpawnPos = lambda: (1, 2, 3)
        fsm.avatar.getPos = lambda other: Point3(70, 80, 0)
        self.assertEqual(fsm.getPatrolOrigin(), Point3(1, 2, 3))

        fsm.getPatrolPoint()
        fsm.rememberPatrolOrigin()
        self.assertEqual(fsm.getPatrolOrigin(), Point3(70, 80, 0))

    def test_patrol_without_route_uses_patrol_radius(self):
        node = SpawnNodeBase(SimpleNamespace(), 'Spawn Node', {'Patrol Radius': '3'}, None, SPAWN_UID)
        fsm = BattleNPCGameFSMAI.__new__(BattleNPCGameFSMAI)
        fsm.avatar = SimpleNamespace(spawnNode=node, getSpawnNode=lambda: node,
            getParentObj=lambda: NodePath('area'), getSpawnPos=lambda: (0, 0, 0))
        fsm.resetWaypoint()

        point = fsm.getPatrolPoint()
        self.assertTrue(abs(point[0]) <= 3 and abs(point[1]) <= 3)

        # without a pause chance we always pause, as we always have
        self.assertEqual(fsm.getPauseChance(), 100)


class InteriorDoorTests(unittest.TestCase):
    def test_interior_with_both_doors_ignores_the_exterior_door_locators(self):
        builder = InteriorAreaBuilderAI.__new__(InteriorAreaBuilderAI)
        builder.air = SimpleNamespace()
        builder.parent = SimpleNamespace(getInteriorFrontDoor=lambda: object(),
            getInteriorBackDoor=lambda: object())

        with patch('pirates.world.DistributedInteriorDoorAI.DistributedInteriorDoorAI') as doorCls:
            self.assertIsNone(builder.createDoorLocatorNode(None, 'exterior', 'door', {}))
            doorCls.assert_not_called()


class BuildingExteriorLoadTests(unittest.TestCase):
    def test_only_door_locators_are_loaded_into_the_interior(self):
        worldCreator = WorldCreatorAI.__new__(WorldCreatorAI)
        worldCreator.world = None
        worldCreator.parentWorlds = []
        interior = SimpleNamespace()
        worldCreator.createObject = Mock(return_value=(interior, None))
        worldCreator.loadObjectDict = Mock()

        exterior = {'Type': 'Building Exterior', 'File': 'interior', 'Objects': {
            'door': {'Type': 'Door Locator Node'},
            'npc': {'Type': 'Townsperson'}}}

        self.assertIs(worldCreator.loadObject(exterior, None, 'area', 'exterior', False), interior)
        objDict = worldCreator.loadObjectDict.call_args[0][0]
        self.assertEqual(list(objDict.keys()), ['door'])


if __name__ == '__main__':
    unittest.main()
