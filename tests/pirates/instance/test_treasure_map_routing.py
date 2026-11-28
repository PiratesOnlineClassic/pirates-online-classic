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

from pirates.instance import DistributedTeleportMgrAI as teleport_module
from pirates.treasuremap.DistributedTreasureMapAI import DistributedTreasureMapAI
from pirates.world.ClientAreaBuilderAI import ClientAreaBuilderAI


class TreasureMapRoutingTests(unittest.TestCase):
    def test_create_captures_new_world_id_before_another_creation(self):
        treasure_map = DistributedTreasureMapAI.__new__(DistributedTreasureMapAI)
        treasure_map.air = SimpleNamespace(
            worldCreator=SimpleNamespace(loadObjectsFromFile=Mock()),
            uidMgr=SimpleNamespace(getDoId=Mock(side_effect=[100, 200])),
            doId2do={200: object()})
        treasure_map._onInstanceCreated = Mock()
        avatar = SimpleNamespace(doId=42)
        treasure_map._createTreasureMapInstance(avatar, 'BlackpearlWorld')
        treasure_map._onInstanceCreated.assert_called_once_with(200, avatar)

    def test_explicit_world_selects_its_island_and_ignores_login_return_location(self):
        island = SimpleNamespace(getUniqueId=lambda: 'black-pearl-island')
        world = SimpleNamespace(doId=200, builder=SimpleNamespace(
            getObject=Mock(return_value=island)))
        avatar = SimpleNamespace(
            doId=42, getReturnLocation=lambda: 'previous-island',
            getCurrentIsland=lambda: 0, getParentObj=lambda: None)
        manager = teleport_module.DistributedTeleportMgrAI.__new__(
            teleport_module.DistributedTeleportMgrAI)
        manager.air = SimpleNamespace(doId2do={200: world})
        manager.avatar2fsm = {}
        manager.getWorld = Mock()
        operation = Mock()
        with patch.object(teleport_module, 'DistributedInstanceBaseAI', SimpleNamespace), \
                patch.object(teleport_module, 'TeleportFSM', return_value=operation):
            manager.d_initiateTeleport(
                avatar, instanceType=4, instanceName='BlackpearlWorld',
                locationUid='black-pearl-island', spawnPt=(1, 2, 3, 4),
                targetWorld=world)
        world.builder.getObject.assert_called_once_with(uniqueId='black-pearl-island')
        manager.getWorld.assert_not_called()
        self.assertIs(manager.avatar2fsm[42], operation)
        operation.request.assert_called_once_with('Teleporting')

    def test_deleted_target_world_cannot_be_used(self):
        world = SimpleNamespace(doId=200, builder=SimpleNamespace(getObject=Mock()))
        avatar = SimpleNamespace(
            doId=42, getReturnLocation=lambda: '', getCurrentIsland=lambda: 0,
            getParentObj=lambda: None)
        manager = teleport_module.DistributedTeleportMgrAI.__new__(
            teleport_module.DistributedTeleportMgrAI)
        manager.air = SimpleNamespace(doId2do={})
        manager.avatar2fsm = {}
        manager.d_initiateTeleport(avatar, targetWorld=world)
        self.assertEqual(manager.avatar2fsm, {})
        world.builder.getObject.assert_not_called()

    def test_same_uid_in_other_world_does_not_block_teleport(self):
        source = SimpleNamespace(getUniqueId=lambda: 'island')
        destination = SimpleNamespace(getUniqueId=lambda: 'island')
        world = SimpleNamespace(doId=200, builder=SimpleNamespace(
            getObject=Mock(return_value=destination)))
        avatar = SimpleNamespace(
            doId=42, getReturnLocation=lambda: '', getCurrentIsland=lambda: 1,
            getParentObj=lambda: source)
        manager = teleport_module.DistributedTeleportMgrAI.__new__(
            teleport_module.DistributedTeleportMgrAI)
        manager.air = SimpleNamespace(doId2do={200: world})
        manager.avatar2fsm = {}
        operation = Mock()
        with patch.object(teleport_module, 'DistributedGameAreaAI', SimpleNamespace), \
                patch.object(teleport_module, 'DistributedInstanceBaseAI', SimpleNamespace), \
                patch.object(teleport_module, 'TeleportFSM', return_value=operation):
            manager.d_initiateTeleport(
                avatar, locationUid='island', spawnPt=(1, 2, 3, 4), targetWorld=world)
        operation.request.assert_called_once_with('Teleporting')

    def test_missing_location_does_not_fall_back_to_another_world(self):
        world = SimpleNamespace(doId=200, builder=SimpleNamespace(
            getObject=Mock(return_value=None), getIslands=Mock()))
        avatar = SimpleNamespace(
            doId=42, getReturnLocation=lambda: '', getCurrentIsland=lambda: 0,
            getParentObj=lambda: None)
        manager = teleport_module.DistributedTeleportMgrAI.__new__(
            teleport_module.DistributedTeleportMgrAI)
        manager.air = SimpleNamespace(doId2do={200: world})
        manager.avatar2fsm = {}
        with patch.object(teleport_module, 'DistributedInstanceBaseAI', SimpleNamespace):
            manager.d_initiateTeleport(avatar, locationUid='missing', targetWorld=world)
        world.builder.getIslands.assert_not_called()
        self.assertEqual(manager.avatar2fsm, {})

    def test_failed_creation_does_not_use_old_world(self):
        treasure_map = DistributedTreasureMapAI.__new__(DistributedTreasureMapAI)
        treasure_map.air = SimpleNamespace(
            worldCreator=SimpleNamespace(loadObjectsFromFile=Mock()),
            uidMgr=SimpleNamespace(getDoId=Mock(return_value=100)),
            doId2do={100: object()})
        treasure_map._onInstanceCreated = Mock()
        treasure_map._createTreasureMapInstance(SimpleNamespace(doId=42), 'BlackpearlWorld')
        treasure_map._onInstanceCreated.assert_not_called()

    def test_removing_old_area_preserves_new_instance_uid(self):
        uidMgr = SimpleNamespace(getDoId=Mock(return_value=200), removeUid=Mock())
        builder = ClientAreaBuilderAI(SimpleNamespace(uidMgr=uidMgr), None)
        island = SimpleNamespace(doId=100, getUniqueId=lambda: 'island')
        builder.objectList[100] = island
        builder.removeObject(island)
        uidMgr.removeUid.assert_not_called()
        self.assertEqual(builder.objectList, {})


if __name__ == '__main__':
    unittest.main()
