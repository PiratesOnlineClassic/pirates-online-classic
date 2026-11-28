import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')

if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

with patch.object(builtins.loader, 'loadFont', Mock()):
    from pirates.world.DistributedIslandAI import DistributedIslandAI
    from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI
    from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI

from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from pirates.movement.DistributedMovingObjectAI import DistributedMovingObjectAI
from pirates.piratesbase import PiratesGlobals
from pirates.quest.QuestConstants import LocationIds
from pirates.world import WorldGlobals
from pirates.world.WorldGridManagerAI import GridInterestContextAllocator, WorldGridManagerAI


class AnyDClass(dict):

    def __missing__(self, className):
        return None


class FakeAir:

    def __init__(self):
        self.doId2do = {}
        self.dclassesByName = AnyDClass()
        self.clientAddInterest = Mock()
        self.clientRemoveInterest = Mock()
        self.worldGridManager = WorldGridManagerAI(self)
        self.newsManager = SimpleNamespace(holidayList=[])

    def getAvatarIdFromSender(self):
        return 100


class FakeGrid(DistributedCartesianGridAI):

    def __init__(self, air, doId, startingZone=500, gridSize=20, gridRadius=2, cellWidth=75):
        DistributedCartesianGridAI.__init__(self, air, startingZone, gridSize, gridRadius, cellWidth)
        self.doId = doId
        air.doId2do[doId] = self


class FakeWorld:

    def __init__(self, doId, instanceType=PiratesGlobals.INSTANCE_MAIN):
        self.doId = doId
        self.instanceType = instanceType

    def getType(self):
        return self.instanceType


def makeAvatar(air, doId=100):
    avatar = SimpleNamespace(doId=doId)
    avatar.GetPuppetConnectionChannel = lambda doId: (1 << 32) | doId
    air.doId2do[doId] = avatar
    return avatar


def addedContexts(air, parentId=None):
    return [call[0][1] for call in air.clientAddInterest.call_args_list
            if parentId is None or call[0][2] == parentId]


class WorldGridManagerTests(unittest.TestCase):

    def setUp(self):
        self.air = FakeAir()
        self.manager = self.air.worldGridManager
        self.avatar = makeAvatar(self.air)

    def test_contexts_do_not_collide_with_client_or_other_grids(self):
        island = FakeGrid(self.air, 1000)
        oceanGrid = FakeGrid(self.air, 2000, gridSize=60, gridRadius=3, cellWidth=2000)

        # both grids share zone 610, each interest must still get it's own context
        self.manager.handleLocationChanged(island, self.avatar, 610)
        self.manager.handleLocationChanged(oceanGrid, self.avatar, 610)

        islandContexts = addedContexts(self.air, island.doId)
        oceanContexts = addedContexts(self.air, oceanGrid.doId)
        self.assertTrue(islandContexts and oceanContexts)
        self.assertFalse(set(islandContexts) & set(oceanContexts))
        for context in islandContexts + oceanContexts:
            self.assertGreaterEqual(context, GridInterestContextAllocator.MinContext)
            self.assertLessEqual(context, GridInterestContextAllocator.MaxContext)

        # clearing the island only removes the island's own contexts
        self.manager.clearAvatarInterest(island, self.avatar)
        removed = [call[0][1] for call in self.air.clientRemoveInterest.call_args_list]
        self.assertEqual(sorted(removed), sorted(islandContexts))
        self.assertTrue(self.manager.hasInterestHandleByZoneId(oceanGrid, self.avatar, 610))

    def test_moving_cells_only_changes_the_difference(self):
        island = FakeGrid(self.air, 1000)
        self.manager.handleLocationChanged(island, self.avatar, 610)
        added = len(self.air.clientAddInterest.call_args_list)
        self.manager.handleLocationChanged(island, self.avatar, 611)

        # one column of cells is added and one is removed
        self.assertEqual(len(self.air.clientAddInterest.call_args_list) - added, 5)
        self.assertEqual(len(self.air.clientRemoveInterest.call_args_list), 5)

    def test_callback_is_called_without_new_zones(self):
        island = FakeGrid(self.air, 1000)
        self.manager.handleLocationChanged(island, self.avatar, 610)

        callback = Mock()
        self.manager.handleLocationChanged(island, self.avatar, 610, callback)
        taskMgr.step()
        taskMgr.step()
        callback.assert_called_once_with()

    def test_area_interest_waits_for_the_client_agent(self):
        world = FakeWorld(3000)
        world.doId = 3000
        callback = Mock()
        self.manager.handleAreaInterest(world, self.avatar, 720, callback)

        # the client agent has not sent the area to the client yet...
        contexts = addedContexts(self.air, world.doId)
        self.assertEqual(len(contexts), 1)
        self.assertEqual(self.air.clientAddInterest.call_args[0][3], 720)
        taskMgr.step()
        taskMgr.step()
        callback.assert_not_called()

        self.manager.handleInterestContextDone(self.avatar.doId, contexts[0])
        callback.assert_called_once_with()

    def test_area_interest_already_open_calls_back_right_away(self):
        world = FakeWorld(3000)
        self.manager.handleAreaInterest(world, self.avatar, 720, Mock())
        callback = Mock()
        self.manager.handleAreaInterest(world, self.avatar, 720, callback)
        callback.assert_called_once_with()
        self.assertEqual(len(addedContexts(self.air, world.doId)), 1)

    def test_area_interest_cleared(self):
        world = FakeWorld(3000)
        self.manager.handleAreaInterest(world, self.avatar, 720, Mock())
        self.manager.clearAreaInterest(world, self.avatar, 720)
        self.assertFalse(self.manager.hasInterestHandleByZoneId(world, self.avatar, 720))
        self.air.clientRemoveInterest.assert_called_once()

        # clearing an area we never opened is harmless...
        self.manager.clearAreaInterest(world, self.avatar, 721)
        self.air.clientRemoveInterest.assert_called_once()

    def test_explicit_add_interest_handle(self):
        island = FakeGrid(self.air, 1000)
        self.manager.handleLocationChanged(island, self.avatar, 610)
        self.manager.addInterestHandle(island, self.avatar, 900)
        self.assertTrue(self.manager.hasInterestHandleByZoneId(island, self.avatar, 900))

    def test_clear_avatar_interests_with_a_deleted_parent(self):
        island = FakeGrid(self.air, 1000)
        self.manager.handleLocationChanged(island, self.avatar, 610)
        del self.air.doId2do[island.doId]

        self.manager.clearAvatarInterests(self.avatar)
        self.assertNotIn(self.avatar.doId, self.manager.gridInterestHandlers)
        self.assertEqual(len(self.air.clientRemoveInterest.call_args_list),
            len(self.air.clientAddInterest.call_args_list))


def makeIsland(air, doId=1000, uniqueId=LocationIds.PORT_ROYAL_ISLAND, world=None):
    island = DistributedIslandAI(air)
    island.doId = doId
    island.setUniqueId(uniqueId)
    if world is not None:
        air.doId2do[world.doId] = world
        island.parentId = world.doId
        island.zoneId = PiratesGlobals.IslandAvailableZoneStart

    air.doId2do[doId] = island
    return island


def makePlayer(air, doId=100):
    player = DistributedPlayerPirateAI.__new__(DistributedPlayerPirateAI)
    player.air = air
    player.cr = air
    player.doId = doId
    player.parentId = 0
    player.zoneId = 0
    player.currentIsland = ''
    player.returnLocation = ''
    player.GetPuppetConnectionChannel = lambda doId: (1 << 32) | doId
    player.sendUpdate = Mock()
    player.sendUpdateToAvatarId = Mock()
    air.doId2do[doId] = player
    return player


class IslandGridTests(unittest.TestCase):

    def setUp(self):
        self.air = FakeAir()
        self.island = makeIsland(self.air)

    def tearDown(self):
        self.island.stopUpdateGridTask()

    def test_player_arrival_opens_grid_interest_without_ai_zone_tracking(self):
        player = makePlayer(self.air)
        self.island.handleChildArrive(player, 610)

        self.assertTrue(self.air.worldGridManager.hasInterestHandleByZoneId(self.island, player, 610))
        self.assertNotIn(player.doId, self.island.gridObjects)

        self.island.handleChildArriveZone(player, 611)
        self.assertTrue(self.air.worldGridManager.hasInterestHandleByZoneId(self.island, player, 613))

    def test_player_leaving_clears_grid_interest(self):
        player = makePlayer(self.air)
        self.island.handleChildArrive(player, 610)
        self.island.handleChildLeave(player, 610)

        self.assertFalse(self.air.worldGridManager.hasInterestHandleByZoneId(self.island, player, 610))
        self.assertEqual(len(self.air.clientRemoveInterest.call_args_list),
            len(self.air.clientAddInterest.call_args_list))

    def test_leaving_an_area_closes_the_interest_in_it(self):
        world = FakeWorld(3000)
        island = makeIsland(self.air, doId=1001, world=world)
        player = makePlayer(self.air, doId=101)
        self.air.worldGridManager.handleAreaInterest(world, player, island.zoneId, Mock())
        island.handleChildArrive(player, 610)
        island.handleChildLeave(player, 610)

        self.assertFalse(self.air.worldGridManager.hasInterestHandleByZoneId(world, player, island.zoneId))
        island.stopUpdateGridTask()

    def test_ai_moving_objects_are_kept_on_the_grid(self):
        npc = DistributedMovingObjectAI.__new__(DistributedMovingObjectAI)
        npc.doId = 200
        with patch.object(self.island, 'handleAvatarZoneChange') as handleAvatarZoneChange:
            self.island.handleChildArrive(npc, 610)

        handleAvatarZoneChange.assert_called_once_with(npc, -1)
        self.assertIn(npc.doId, self.island.gridObjects)
        self.island.handleChildLeave(npc, 610)
        self.assertNotIn(npc.doId, self.island.gridObjects)


class ReturnLocationTests(unittest.TestCase):

    def setUp(self):
        self.air = FakeAir()
        self.world = FakeWorld(5000)

    def placePlayer(self, player, area):
        player.parentId = area.doId
        player.zoneId = 610

    def test_return_location_is_the_island_requested(self):
        island = makeIsland(self.air, uniqueId=LocationIds.TORTUGA_ISLAND, world=self.world)
        player = makePlayer(self.air)
        player.returnLocation = LocationIds.PORT_ROYAL_ISLAND
        self.placePlayer(player, island)

        player.requestReturnLocation(island.doId)
        self.assertEqual(player.getReturnLocation(), LocationIds.TORTUGA_ISLAND)
        player.sendUpdate.assert_called_once_with('setReturnLocation', [LocationIds.TORTUGA_ISLAND])

    def test_del_fuego_is_a_return_location(self):
        island = makeIsland(self.air, uniqueId=LocationIds.DEL_FUEGO_ISLAND, world=self.world)
        player = makePlayer(self.air)
        self.placePlayer(player, island)

        player.requestReturnLocation(island.doId)
        self.assertEqual(player.getReturnLocation(), LocationIds.DEL_FUEGO_ISLAND)

    def test_islands_without_a_jail_are_not_return_locations(self):
        island = makeIsland(self.air, uniqueId=LocationIds.KINGSHEAD_ISLAND, world=self.world)
        player = makePlayer(self.air)
        player.returnLocation = LocationIds.PORT_ROYAL_ISLAND
        self.placePlayer(player, island)

        player.requestReturnLocation(island.doId)
        self.assertEqual(player.getReturnLocation(), LocationIds.PORT_ROYAL_ISLAND)

    def test_islands_outside_the_main_world_are_not_return_locations(self):
        island = makeIsland(self.air, uniqueId=LocationIds.TORTUGA_ISLAND,
            world=FakeWorld(5001, PiratesGlobals.INSTANCE_PVP))
        player = makePlayer(self.air)
        self.placePlayer(player, island)

        player.requestReturnLocation(island.doId)
        self.assertEqual(player.getReturnLocation(), '')

    def test_request_for_an_area_we_are_not_in_is_ignored(self):
        island = makeIsland(self.air, uniqueId=LocationIds.TORTUGA_ISLAND, world=self.world)
        player = makePlayer(self.air)

        player.requestReturnLocation(island.doId)
        self.assertEqual(player.getReturnLocation(), '')

    def test_building_interior_returns_to_its_island(self):
        island = makeIsland(self.air, uniqueId=LocationIds.CUBA_ISLAND, world=self.world)
        interior = DistributedGAInteriorAI(self.air, True)
        interior.doId = 3000
        self.air.doId2do[interior.doId] = interior
        door = SimpleNamespace(getParentObj=lambda: island)
        interior.setExteriorFrontDoor(door)

        player = makePlayer(self.air)
        self.placePlayer(player, interior)
        player.requestReturnLocation(interior.doId)
        self.assertEqual(player.getReturnLocation(), LocationIds.CUBA_ISLAND)

    def test_current_island_cleared_on_a_crew_ship(self):
        player = makePlayer(self.air)
        player.currentIsland = LocationIds.TORTUGA_ISLAND
        player.parentId = 7000

        player.requestCurrentIsland(0)
        self.assertEqual(player.getCurrentIsland(), '')
        player.sendUpdateToAvatarId.assert_called_once_with(player.doId, 'setCurrentIsland', [''])

    def test_current_island_kept_while_ashore(self):
        island = makeIsland(self.air, uniqueId=LocationIds.TORTUGA_ISLAND, world=self.world)
        player = makePlayer(self.air)
        player.currentIsland = LocationIds.TORTUGA_ISLAND
        self.placePlayer(player, island)

        player.requestCurrentIsland(0)
        self.assertEqual(player.getCurrentIsland(), LocationIds.TORTUGA_ISLAND)

        otherIsland = makeIsland(self.air, doId=1001, uniqueId=LocationIds.CUBA_ISLAND, world=self.world)
        player.requestCurrentIsland(otherIsland.doId)
        self.assertEqual(player.getCurrentIsland(), LocationIds.TORTUGA_ISLAND)


if __name__ == '__main__':
    unittest.main()
