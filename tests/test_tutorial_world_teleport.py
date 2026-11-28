import ast
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from pirates.instance.DistributedTeleportHandlerAI import DistributedTeleportHandlerAI
from pirates.leveleditor.worldData.Rambleshack import objectStruct as island_data
from pirates.leveleditor.worldData.RambleshackJailInt import objectStruct as jail_data
from pirates.piratesbase import PiratesGlobals
from pirates.tutorial import TutorialGlobals
from pirates.world.WorldCreatorBase import WorldCreatorBase
from pirates.world import WorldGlobals
from otp.distributed.OtpDoGlobals import OTP_ZONE_ID_MANAGEMENT


class World:
    def __init__(self, do_id, file_name):
        self.doId = do_id
        self.file_name = file_name
        self.spawn_updates = []

    def getFileName(self):
        return self.file_name

    def d_setSpawnInfo(self, *args):
        self.spawn_updates.append(args)


class Area:
    def __init__(self, parent):
        self.doId = 30
        self.parentId = parent.doId
        self.zoneId = 450
        self.parent = parent

    def getParentObj(self):
        return self.parent

    def getZoneFromXYZ(self, pos):
        return 800

    def isValidZone(self, zone):
        return zone == 800


class TutorialWorldTeleportTests(unittest.TestCase):
    def setUp(self):
        self.world = World(10, 'RambleshackWorld')
        self.world.oceanGrid = SimpleNamespace(doId=11, zoneId=PiratesGlobals.IslandAvailableZoneStart)
        self.interior_world = World(20, 'Rambleshack')
        self.area = Area(self.interior_world)
        self.fsm = SimpleNamespace(
            world=self.world, gameArea=self.area, spawnPt=(25.955, 19.1, -1.5, -175),
            cleanup=Mock())
        self.handler = DistributedTeleportHandlerAI.__new__(DistributedTeleportHandlerAI)
        self.handler.teleportFsm = self.fsm
        self.handler.avatar = SimpleNamespace(doId=100)
        self.updates = []
        self.handler.sendUpdateToAvatarId = lambda *args: self.updates.append(args)

    def test_jail_teleport_supplies_both_worlds_and_world_interest_zone(self):
        self.handler.teleportToInstanceReady(0)
        _, name, fields = self.updates[0]
        self.assertEqual(name, 'continueTeleportToInstance')
        self.assertEqual(fields, [
            10, PiratesGlobals.IslandAvailableZoneStart, 10, 'RambleshackWorld',
            20, 450, 20, 'Rambleshack', 11])

        creator = WorldCreatorBase.__new__(WorldCreatorBase)
        creator.fileDicts = {'Rambleshack.py': island_data}
        exterior = creator.getObjectDataByUid(TutorialGlobals.JAIL_INTERIOR)
        self.assertEqual(exterior['File'], 'RambleshackJailInt')
        self.assertIn(TutorialGlobals.JAIL_INTERIOR, jail_data['ObjectIds'])

    def test_spawn_info_goes_to_destination_instance_with_correct_parent_order(self):
        self.handler.readyToFinishTeleport(self.interior_world.doId)
        self.assertEqual(self.world.spawn_updates, [])
        self.assertEqual(self.interior_world.spawn_updates, [
            (100, 25.955, 19.1, -1.5, -175, 0, [30, 450, 20])])
        self.assertEqual(self.updates, [(100, 'teleportToInstanceCleanup', [])])

    def test_island_teleport_keeps_world_as_destination_instance(self):
        self.area.parent = self.world
        self.area.parentId = self.world.doId
        self.area.zoneId = PiratesGlobals.IslandAvailableZoneStart
        self.handler.teleportToInstanceReady(0)
        self.assertEqual(self.updates[0][2], [
            10, PiratesGlobals.IslandAvailableZoneStart, 10, 'RambleshackWorld',
            10, PiratesGlobals.IslandAvailableZoneStart, 10, 'RambleshackWorld', 11])
        self.handler.readyToFinishTeleport(self.world.doId)
        self.assertEqual(self.world.spawn_updates[0][-1], [30, 110, 10])

    def test_missing_destination_instance_aborts(self):
        self.area.parent = None
        self.handler.teleportToInstanceReady(0)
        self.assertEqual(self.updates, [(100, 'abortTeleport', [])])
        self.fsm.cleanup.assert_called_once()

    def test_tutorial_world_type_is_included_in_distributed_generation(self):
        world = Mock(doId=10)
        world.getType.return_value = PiratesGlobals.INSTANCE_TUTORIAL
        world.getUniqueId.return_value = 'region-uid'
        creator = SimpleNamespace(
            air=SimpleNamespace(uidMgr=SimpleNamespace(addUid=Mock())),
            notify=Mock(),
            getObjectFilenameByUid=lambda uid: 'RambleshackWorld',
            oceanAreaManager=SimpleNamespace(
                registerOceanAreaData=Mock(), hasOceanArea=lambda uid: False))
        source = (Path(__file__).parent / 'pirates/world/WorldCreatorAI.py').read_text()
        cls = next(node for node in ast.parse(source).body
                   if isinstance(node, ast.ClassDef) and node.name == 'WorldCreatorAI')
        method = next(node for node in cls.body
                      if isinstance(node, ast.FunctionDef) and node.name == 'createWorldInstance')
        namespace = {
            'DistributedPiratesTutorialWorldAI': Mock(return_value=world),
            'WorldGlobals': WorldGlobals,
            'OTP_ZONE_ID_MANAGEMENT': OTP_ZONE_ID_MANAGEMENT,
        }
        exec(compile(ast.Module(body=[method], type_ignores=[]), '<world-creator>', 'exec'), namespace)
        namespace['createWorldInstance'](creator, {}, None, None, 'region-uid', False)
        world.generateWithRequired.assert_called_once_with(
            OTP_ZONE_ID_MANAGEMENT, ['setType'])

    def test_jail_exit_interest_points_to_the_islands_world(self):
        source = (Path(__file__).parent / 'pirates/world/InteriorAreaBuilderAI.py').read_text()
        cls = next(node for node in ast.parse(source).body
                   if isinstance(node, ast.ClassDef) and node.name == 'InteriorAreaBuilderAI')
        method = next(node for node in cls.body
                      if isinstance(node, ast.FunctionDef) and node.name == 'createDoorLocatorNode')
        namespace = {}
        exec(compile(ast.Module(body=[method], type_ignores=[]), '<interior-builder>', 'exec'), namespace)

        region = SimpleNamespace(doId=10, parentId=100, zoneId=2)
        island = SimpleNamespace(doId=30, zoneId=110, getParentObj=lambda: region)
        exterior_door = Mock()
        exterior_door.getParentObj.return_value = island
        exterior_door.getBuildingUid.return_value = TutorialGlobals.JAIL_BUILDING_EXTERIOR
        jail_instance = SimpleNamespace(doId=20, parentId=100, zoneId=2)
        interior = Mock(doId=40, parentId=20, zoneId=450)
        interior.getParentObj.return_value = jail_instance
        interior.getInteriorFrontDoor.return_value = None
        interior.getExteriorFrontDoor.return_value = exterior_door
        interior.getZoneFromXYZ.return_value = 800
        interior.getLinks.return_value = []
        door = Mock(doId=50)
        builder = SimpleNamespace(parent=interior, air=object(), addObject=Mock(), notify=Mock())
        door_module = SimpleNamespace(DistributedInteriorDoorAI=Mock(return_value=door))
        with patch.dict(sys.modules, {'pirates.world.DistributedInteriorDoorAI': door_module}):
            namespace['createDoorLocatorNode'](builder, interior, 'jail',
                                               TutorialGlobals.JAIL_INTERIOR_DOOR, {})
        door.setExteriorId.assert_called_once_with(30, 10, 110)


if __name__ == '__main__':
    unittest.main()
