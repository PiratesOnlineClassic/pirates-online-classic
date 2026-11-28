import builtins
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from pirates.piratesbase import PiratesGlobals


class InstanceBase:
    def __init__(self, doId, instanceType=PiratesGlobals.INSTANCE_MAIN, fileName='piratesWorld'):
        self.doId = doId
        self.type = instanceType
        self.fileName = fileName
        self.oceanGrid = SimpleNamespace(doId=doId + 1, zoneId=PiratesGlobals.IslandAvailableZoneStart)
        self.areas = {}
        self.builder = SimpleNamespace(
            getObject=lambda uniqueId=None: self.areas.get(uniqueId),
            getIslands=lambda: list(self.areas.values()))

    def getType(self):
        return self.type

    def getFileName(self):
        return self.fileName

    def getParentObj(self):
        return None

    def getSpawnPt(self, uid, index=None):
        return (1, 2, 3, 4)


class TeleportZone(InstanceBase):
    pass


class GameArea:
    def __init__(self, doId, uid, parent):
        self.doId = doId
        self.uid = uid
        self.parent = parent
        self.parentId = parent.doId
        self.zoneId = 500
        parent.areas[uid] = self

    def getUniqueId(self):
        return self.uid

    def getParentObj(self):
        return self.parent

    def getUndockable(self):
        return False


class Island(GameArea):
    pass


class Ship:
    def __init__(self, doId, oceanGrid, world):
        self.doId = doId
        self.parentId = oceanGrid.doId
        self.zoneId = 1234
        self.world = world

    def getParentObj(self):
        return SimpleNamespace(doId=self.parentId, getParentObj=lambda: self.world)


def stubModule(name, **attributes):
    module = types.ModuleType(name)
    module.__dict__.update(attributes)
    return module


# Load the module under test without pulling in the game resource files.
stubs = {
    'pirates.quest.QuestConstants': stubModule('pirates.quest.QuestConstants',
        LocationIds=SimpleNamespace(KINGSHEAD_ISLAND='kingshead')),
    'pirates.instance.DistributedInstanceBaseAI': stubModule('pirates.instance.DistributedInstanceBaseAI',
        DistributedInstanceBaseAI=InstanceBase),
    'pirates.instance.DistributedTeleportZoneAI': stubModule('pirates.instance.DistributedTeleportZoneAI',
        DistributedTeleportZoneAI=TeleportZone),
    'pirates.instance.DistributedTeleportHandlerAI': stubModule('pirates.instance.DistributedTeleportHandlerAI',
        DistributedTeleportHandlerAI=object),
    'pirates.world.DistributedGameAreaAI': stubModule('pirates.world.DistributedGameAreaAI',
        DistributedGameAreaAI=GameArea),
}
lazyStubs = {
    'pirates.world.DistributedIslandAI': stubModule('pirates.world.DistributedIslandAI',
        DistributedIslandAI=Island),
    'pirates.ship.DistributedShipAI': stubModule('pirates.ship.DistributedShipAI',
        DistributedShipAI=Ship),
}

with patch.dict(sys.modules, stubs):
    spec = importlib.util.spec_from_file_location('_test_DistributedTeleportMgrAI',
        Path(__file__).parent / 'DistributedTeleportMgrAI.py')
    teleport = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(teleport)


class Avatar:
    def __init__(self, doId=100, parent=None):
        self.doId = doId
        self.parent = parent
        self.returnLocation = ''
        self.currentIsland = 'current'
        self.inventory = SimpleNamespace(getStackQuantity=lambda token: 0)

    def getReturnLocation(self):
        return self.returnLocation

    def getCurrentIsland(self):
        return self.currentIsland

    def getTutorial(self):
        return PiratesGlobals.TUT_FINISHED if hasattr(PiratesGlobals, 'TUT_FINISHED') else 99

    def getParentObj(self):
        return self.parent

    def getInventory(self):
        return self.inventory

    def isPaid(self):
        return True


class TeleportMgrTests(unittest.TestCase):
    def setUp(self):
        self.lazyPatch = patch.dict(sys.modules, lazyStubs)
        self.lazyPatch.start()
        self.configPatch = None
        if not hasattr(builtins, 'config'):
            self.configPatch = patch.object(builtins, 'config',
                SimpleNamespace(GetBool=lambda name, default: default), create=True)
            self.configPatch.start()

        self.world = InstanceBase(10)
        self.otherIsland = Island(31, 'other-island', self.world)
        self.island = Island(30, 'island', self.world)
        self.uids = {'island': self.island, 'other-island': self.otherIsland}
        self.manager = teleport.DistributedTeleportMgrAI.__new__(teleport.DistributedTeleportMgrAI)
        self.manager.avatar2fsm = {}
        self.manager.air = SimpleNamespace(
            districtId=5000,
            doId2do={10: self.world, 30: self.island, 31: self.otherIsland},
            uidMgr=SimpleNamespace(
                getDoId=lambda uid: getattr(self.uids.get(uid), 'doId', None),
                justGetMeMeObject=lambda uid: self.uids.get(uid)),
            travelAgent=Mock(),
            getObject=Mock(),
            getAvatarIdFromSender=lambda: 100)
        self.avatar = Avatar(parent=self.island)
        self.manager.air.doId2do[100] = self.avatar
        self.manager.sendUpdateToAvatarId = Mock()

    def tearDown(self):
        self.lazyPatch.stop()
        if self.configPatch:
            self.configPatch.stop()

    def test_get_world_resolves_generic_client_names(self):
        self.assertIs(self.manager.getWorld(PiratesGlobals.INSTANCE_MAIN, 'mainWorld'), self.world)
        self.assertIs(self.manager.getWorld(PiratesGlobals.INSTANCE_MAIN, ''), self.world)
        self.assertIs(self.manager.getWorld(PiratesGlobals.INSTANCE_WELCOME, 'Welcome World'), self.world)
        self.assertIsNone(self.manager.getWorld(PiratesGlobals.INSTANCE_TM, 'mainWorld'))

    def test_get_world_ignores_teleport_zones(self):
        self.manager.air.doId2do = {1: TeleportZone(1, PiratesGlobals.INSTANCE_MAIN)}
        self.assertIsNone(self.manager.getWorld(PiratesGlobals.INSTANCE_MAIN, 'piratesWorld'))

    def test_instance_from_object_walks_parents(self):
        ship = Ship(40, self.world.oceanGrid, self.world)
        self.assertIs(self.manager.getInstanceFromObject(ship), self.world)
        self.assertIsNone(self.manager.getInstanceFromObject(None))

    def test_island_request_without_token_is_denied(self):
        self.manager.requestTeleportToIsland('other-island')
        self.manager.sendUpdateToAvatarId.assert_called_once_with(100, 'teleportToIslandResponse', [0, 0])

    def test_island_request_with_token_responds_with_world_and_island(self):
        self.avatar.inventory = SimpleNamespace(getStackQuantity=lambda token: 1)
        with patch.object(teleport.InventoryType, 'getIslandTeleportToken', return_value=13500):
            self.manager.requestTeleportToIsland('other-island')
        self.manager.sendUpdateToAvatarId.assert_called_once_with(100, 'teleportToIslandResponse', [10, 31])

    def test_initiate_to_main_world_by_generic_name(self):
        self.avatar.parent = None
        with patch.object(teleport, 'TeleportFSM') as fsm:
            self.manager.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 0, 0, 'island', 0, 'mainWorld', -1, 0, 0)
        fsm.assert_called_once_with(self.manager.air, self.avatar, self.world, self.island, (1, 2, 3, 4))

    def test_initiate_to_friend_on_same_island_is_not_blocked(self):
        friend = Avatar(200, parent=self.island)
        self.manager.air.doId2do[200] = friend
        with patch.object(teleport, 'TeleportFSM') as fsm:
            self.manager.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 0, 5000, '', 10, '', -1, 200, 30)
        fsm.assert_called_once_with(self.manager.air, self.avatar, self.world, self.island, (1, 2, 3, 4))

    def test_initiate_to_missing_friend_fails_the_client(self):
        self.manager.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 0, 0, '', 10, '', -1, 999, 0)
        self.manager.sendUpdateToAvatarId.assert_called_once_with(100, '_localTeleportToIdResponse', [0, 0])

    def test_initiate_to_ship_uses_ship_fsm(self):
        ship = Ship(40, self.world.oceanGrid, self.world)
        self.manager.air.doId2do[40] = ship
        with patch.object(teleport, 'TeleportShipFSM') as fsm:
            self.manager.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 0, 0, '', 10, '', -1, 0, 40)
        fsm.assert_called_once_with(self.manager.air, self.avatar, self.world, ship)
        fsm.return_value.request.assert_called_once_with('Teleporting')

    def test_direct_island_area_requires_token(self):
        with patch.object(teleport, 'TeleportFSM') as fsm:
            self.manager.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 0, 0, '', 10, '', -1, 0, 31)
        fsm.assert_not_called()
        self.manager.sendUpdateToAvatarId.assert_called_once_with(100, '_localTeleportToIdResponse', [0, 0])

    def test_cross_shard_area_is_resolved_to_uid(self):
        self.manager.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 0, 6000, '', 77, '', -1, 300, 88)
        self.manager.air.getObject.assert_called_once()
        doId, callback = self.manager.air.getObject.call_args[0]
        self.assertEqual(doId, 88)
        callback(88, 77, 500, None, {'setUniqueId': ['remote-island']})
        self.manager.air.travelAgent.d_requestTeleportToShardAItoUD.assert_called_once_with(
            100, 6000, PiratesGlobals.INSTANCE_MAIN, '', 'remote-island')

    def test_cross_shard_without_area_forwards_directly(self):
        self.manager.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 0, 6000, 'island', 0, 'mainWorld', -1, 0, 0)
        self.manager.air.travelAgent.d_requestTeleportToShardAItoUD.assert_called_once_with(
            100, 6000, PiratesGlobals.INSTANCE_MAIN, 'mainWorld', 'island')

    def test_return_location_only_overrides_when_requested(self):
        self.avatar.parent = None
        self.avatar.currentIsland = ''
        self.avatar.returnLocation = 'other-island'
        with patch.object(teleport, 'TeleportFSM') as fsm:
            self.manager.d_initiateTeleport(self.avatar, PiratesGlobals.INSTANCE_MAIN, '', 'island',
                useReturnLocation=False)
        self.assertIs(fsm.call_args[0][3], self.island)

    def test_avatar_teleport_location(self):
        self.assertEqual(self.manager.getAvatarTeleportLocation(self.avatar), (5000, 10, 30))
        self.assertIsNone(self.manager.getAvatarTeleportLocation(Avatar(1, parent=None)))


class TeleportHandlerShipTests(unittest.TestCase):
    def test_ship_spawn_uses_world_destination_and_ship_parents(self):
        with patch.dict(sys.modules, {}):
            spec = importlib.util.spec_from_file_location('_test_DistributedTeleportHandlerAI',
                Path(__file__).parent / 'DistributedTeleportHandlerAI.py')
            handlerModule = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(handlerModule)

        world = InstanceBase(10)
        world.d_setSpawnInfo = Mock()
        ship = Ship(40, world.oceanGrid, world)
        handler = handlerModule.DistributedTeleportHandlerAI.__new__(handlerModule.DistributedTeleportHandlerAI)
        handler.avatar = SimpleNamespace(doId=100)
        handler.teleportFsm = SimpleNamespace(world=world, gameArea=ship, ship=ship,
            spawnPt=(0, 0, 0, 0), cleanup=Mock())
        handler.sendUpdateToAvatarId = Mock()

        handler.teleportToInstanceReady(0)
        handler.sendUpdateToAvatarId.assert_called_with(100, 'continueTeleportToInstance', [
            10, world.oceanGrid.zoneId, 10, 'piratesWorld', world.oceanGrid.doId, 1234,
            10, 'piratesWorld', world.oceanGrid.doId])

        handler.readyToFinishTeleport(10)
        world.d_setSpawnInfo.assert_called_once_with(100, 0, 0, 0, 0, 0, [40, 1234, world.oceanGrid.doId])
        handler.sendUpdateToAvatarId.assert_called_with(100, 'teleportToInstanceCleanup', [])
        handler.teleportFsm.cleanup.assert_not_called()


if __name__ == '__main__':
    unittest.main()
