import builtins
import importlib
import math
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from panda3d.core import NodePath, Point3, loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')


def _ensureWeaponGlobals():
    # WeaponGlobals needs the game resources (pkl files) which the
    # unit tests may not have, the deployer only needs the buff ids...
    try:
        importlib.import_module('pirates.battle.WeaponGlobals')
    except (IOError, OSError):
        from pirates.battle import WeaponConstants
        module = types.ModuleType('pirates.battle.WeaponGlobals')
        module.__dict__.update({key: value for key, value in vars(WeaponConstants).items()
            if not key.startswith('__')})
        sys.modules['pirates.battle.WeaponGlobals'] = module
        setattr(importlib.import_module('pirates.battle'), 'WeaponGlobals', module)


_ensureWeaponGlobals()

from pirates.battle import WeaponGlobals
from pirates.economy.EconomyGlobals import ItemId
from pirates.economy.DistributedShopKeeperAI import DistributedShopKeeperAI
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PLocalizer
from pirates.uberdog import DistributedShipLoaderAI as loader_ai
from pirates.uberdog import DistributedShipLoaderUD as loader_ud
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.world import DistributedShipDeployerAI as deployer_module
from pirates.world.DistributedShipDeployerAI import DistributedShipDeployerAI, DeployShipFSM, getDeploySpacing


# Port Royal's zone spheres and transform, taken from piratesWorld world data:
PORT_ROYAL_RADII = [4377.6, 5000.0, 7573.95]
PORT_ROYAL_CENTER = [402.2, 358.0]
PORT_ROYAL_TRANSFORM = [-87.0, 12.0, 0.0, -180.0]


class FakeOceanGrid(NodePath):

    def __init__(self):
        NodePath.__init__(self, 'oceanGrid')
        self.doId = 4000


class FakeShip(NodePath):

    def __init__(self, doId, hp=100, parentObj=None):
        NodePath.__init__(self, 'ship-%d' % doId)
        self.doId = doId
        self.hp = hp
        self.parentObj = parentObj
        self.clientController = 0
        self.crew = []
        self.skillEffects = []
        self.inventoryId = 0
        self.shipClass = 1

    def getHp(self):
        return self.hp

    def getShipClass(self):
        return self.shipClass

    def getParentObj(self):
        return self.parentObj

    def getClientController(self):
        return self.clientController

    def getCrew(self):
        return self.crew

    def hasSpawnBuff(self):
        return any(effect[0] == WeaponGlobals.C_SPAWN for effect in self.skillEffects)

    def addSkillEffect(self, effectId, duration, attackerId):
        self.skillEffects.append([effectId, duration, 0, attackerId])

    def removeSkillEffect(self, effectId, attackerId=0):
        self.skillEffects = [effect for effect in self.skillEffects if effect[0] != effectId]


class ShipDeployerTests(unittest.TestCase):

    def setUp(self):
        self.oceanGrid = FakeOceanGrid()
        self.oceanGrid.getZoneFromXYZ = lambda pos: 2000
        self.oceanGrid.addObjectToOceanGrid = Mock()
        self.island = SimpleNamespace(doId=3000,
            getIslandTransform=lambda: PORT_ROYAL_TRANSFORM,
            getParentObj=lambda: SimpleNamespace(oceanGrid=self.oceanGrid))
        self.shipManager = SimpleNamespace(playerShips=[], getPlayerShips=lambda: list(self.shipManager.playerShips),
            getShips=lambda: [], addPlayerShip=Mock())
        self.air = SimpleNamespace(doId2do={3000: self.island}, shipManager=self.shipManager,
            getAvatarIdFromSender=lambda: 10, writeServerEvent=Mock(), sendSetObjectLocation=Mock(),
            dclassesByName={'DistributedShipDeployerAI': None})
        self.deployer = DistributedShipDeployerAI(self.air, self.island)
        self.deployer.parentId = self.island.doId
        minRadius, maxRadius = PORT_ROYAL_RADII[0], PORT_ROYAL_RADII[1]
        self.deployer.setPos(PORT_ROYAL_CENTER[0], PORT_ROYAL_CENTER[1], 0)
        self.deployer.setMinRadius(minRadius)
        self.deployer.setMaxRadius(maxRadius)
        self.deployer.setSpacing(round(getDeploySpacing(minRadius, maxRadius), 2))
        self.deployer.createDeploySpheres()

    def getOceanCenter(self):
        return self.deployer.localToOceanPoint(*PORT_ROYAL_CENTER)

    def test_spheres_fill_the_band_between_the_reef_and_the_barrier(self):
        self.assertEqual(self.deployer.getSpacing(), round(PORT_ROYAL_RADII[1] - PORT_ROYAL_RADII[0], 2))
        self.assertTrue(1 < self.deployer.getNumSpheres() <= deployer_module.MAX_DEPLOY_SPHERES)

        center = self.getOceanCenter()
        for sphereId in range(self.deployer.getNumSpheres()):
            spawnPoint = self.deployer.getOceanSpawnPoint(sphereId)
            distance = (spawnPoint - center).length()
            self.assertGreater(distance - self.deployer.getSphereRadius(), PORT_ROYAL_RADII[0] - 0.1)
            self.assertLess(distance + self.deployer.getSphereRadius(), PORT_ROYAL_RADII[1] + 0.1)
            self.assertEqual(spawnPoint[2], 0)

    def test_sphere_ids_always_fit_in_an_uint8(self):
        spacing = getDeploySpacing(20000, 20050)
        numSpheres = int(2 * math.pi * (20000 + spacing / 2.0) / spacing)
        self.assertLessEqual(numSpheres, deployer_module.MAX_DEPLOY_SPHERES)
        self.assertEqual(getDeploySpacing(1000, 1000), deployer_module.DEFAULT_DEPLOY_SPACING)

    def test_ship_faces_out_to_sea(self):
        center = self.getOceanCenter()
        for sphereId in (0, 5, self.deployer.getNumSpheres() - 1):
            spawnPoint = self.deployer.getOceanSpawnPoint(sphereId)
            heading = math.radians(self.deployer.getOceanSpawnHeading(sphereId))
            forward = Point3(-math.sin(heading), math.cos(heading), 0)
            outward = spawnPoint - center
            outward.normalize()
            self.assertAlmostEqual(forward.dot(outward), 1.0, places=4)

    def test_closest_free_sphere_to_the_dinghy_is_chosen(self):
        dinghyPos = self.deployer.getIslandSpherePos(7)
        self.assertEqual(self.deployer.chooseDeploySphere(self.oceanGrid, preferredPos=dinghyPos), 7)

        # a sphere reported as occupied by a ship's client is skipped...
        self.air.doId2do[50] = FakeShip(50)
        self.deployer.addShipToSphere(7, 50)
        self.assertIn(self.deployer.chooseDeploySphere(self.oceanGrid, preferredPos=dinghyPos), (6, 8))

        # unless that is the ship being deployed:
        self.assertEqual(self.deployer.chooseDeploySphere(self.oceanGrid, preferredPos=dinghyPos,
            excludeShipId=50), 7)

    def test_sphere_with_a_ship_sitting_in_it_is_skipped(self):
        dinghyPos = self.deployer.getIslandSpherePos(3)
        ship = FakeShip(60, parentObj=self.oceanGrid)
        ship.reparentTo(self.oceanGrid)
        ship.setPos(self.oceanGrid, self.deployer.getOceanSpawnPoint(3))
        self.shipManager.playerShips.append(ship)
        self.assertIn(self.deployer.chooseDeploySphere(self.oceanGrid, preferredPos=dinghyPos), (2, 4))

    def makeFSM(self, ship, allowSunk=False, preferredPos=None, paid=True):
        avatar = SimpleNamespace(doId=10, isPaid=lambda: paid)
        inventory = SimpleNamespace(getShipMainpartsDoIdList=lambda: [70])
        shippart = SimpleNamespace(doId=70, b_setLocation=Mock())
        ship.inventoryId = 80
        ship.b_setCaptainId = Mock()
        ship.b_setLocation = Mock()
        ship.sendCurrentPosition = Mock()
        ship.b_setGameState = Mock()
        ship.b_setDeploy = Mock()
        ship.repairShip = Mock()
        self.air.doId2do.update({ship.doId: ship, 70: shippart, 80: inventory})
        callback = Mock()
        self.deployer.deployShip(avatar, ship.doId, callback, preferredPos=preferredPos, allowSunk=allowSunk)
        return callback

    def test_deploy_places_ship_in_sphere_and_protects_it(self):
        ship = FakeShip(90)
        ship.reparentTo(self.oceanGrid)
        callback = self.makeFSM(ship, preferredPos=self.deployer.getIslandSpherePos(4))
        callback.assert_called_once_with(True)

        spawnPoint = self.deployer.getOceanSpawnPoint(4)
        self.assertAlmostEqual((ship.getPos(self.oceanGrid) - spawnPoint).length(), 0, places=1)
        self.assertAlmostEqual(ship.getH(self.oceanGrid) % 360.0,
            self.deployer.getOceanSpawnHeading(4), places=2)
        ship.b_setLocation.assert_called_once_with(self.oceanGrid.doId, 2000)
        ship.b_setDeploy.assert_called_once_with(1)
        self.assertTrue(ship.hasSpawnBuff())
        self.assertEqual(ship.skillEffects[0][1], int(deployer_module.SPAWN_PROTECTION_DURATION))
        self.assertEqual(self.deployer.sphere2shipIds, {4: {90}})
        self.shipManager.addPlayerShip.assert_called_once_with(ship)

    def test_sunk_ship_is_not_deployed(self):
        ship = FakeShip(91, hp=0)
        callback = self.makeFSM(ship)
        callback.assert_called_once_with(False)
        ship.b_setLocation.assert_not_called()
        self.assertFalse(ship.hasSpawnBuff())
        self.assertEqual(self.deployer.avatar2fsm, {})

    def test_freebooter_only_deploys_free_ship_classes(self):
        from pirates.ship import ShipGlobals

        ship = FakeShip(95)
        ship.shipClass = ShipGlobals.WARSHIPL1
        callback = self.makeFSM(ship, paid=False)
        callback.assert_called_once_with(False)
        ship.b_setLocation.assert_not_called()

        ship = FakeShip(96)
        ship.shipClass = ShipGlobals.MERCHANTL1
        callback = self.makeFSM(ship, paid=False)
        callback.assert_called_once_with(True)

    def test_sunk_siege_ship_is_repaired_on_deploy(self):
        ship = FakeShip(92, hp=0)
        callback = self.makeFSM(ship, allowSunk=True)
        callback.assert_called_once_with(True)
        ship.repairShip.assert_called_once_with()

    def test_busy_deployer_reports_failure(self):
        avatar = SimpleNamespace(doId=10)
        self.deployer.avatar2fsm[10] = object()
        callback = Mock()
        self.deployer.deployShip(avatar, 93, callback)
        callback.assert_called_once_with(False)

    def test_leaving_the_barrier_ends_the_protection(self):
        ship = FakeShip(94)
        ship.clientController = 10
        self.air.doId2do[94] = ship
        self.deployer.protectShip(ship)
        self.deployer.addShipToSphere(2, 94)

        self.deployer.shipExitedBarrier(94)
        self.assertFalse(ship.hasSpawnBuff())
        self.assertEqual(self.deployer.sphere2shipIds, {})

    def test_sphere_reports_are_only_accepted_from_the_ship_crew(self):
        ship = FakeShip(95)
        self.air.doId2do[95] = ship
        self.deployer.protectShip(ship)

        self.deployer.shipEnteredSphere(95, 1)
        self.deployer.shipExitedBarrier(95)
        self.assertEqual(self.deployer.sphere2shipIds, {})
        self.assertTrue(ship.hasSpawnBuff())
        self.assertEqual(self.air.writeServerEvent.call_count, 2)

        ship.crew = [10]
        self.deployer.shipEnteredSphere(95, 1)
        self.deployer.shipEnteredSphere(95, 255)
        self.assertEqual(self.deployer.sphere2shipIds, {1: {95}})
        self.deployer.shipExitedSphere(95, 1)
        self.assertEqual(self.deployer.sphere2shipIds, {})


class ShipPurchaseTests(unittest.TestCase):

    def setUp(self):
        self.avatar = SimpleNamespace(doId=1000, isPaid=lambda: True, isDeleted=lambda: False)
        self.gold = 1000
        self.inventory = SimpleNamespace(
            getGoldInPocket=lambda: self.gold,
            setGoldInPocket=self.setGold,
            getShipDoIdList=lambda: [],
            getCategoryLimit=lambda category: 3,
            getStackQuantity=lambda itemId: 1 if itemId == InventoryType.NewShipToken else 0)
        self.air = Mock()
        self.air.getAvatarIdFromSender.return_value = self.avatar.doId
        self.air.doId2do = {self.avatar.doId: self.avatar}
        self.air.inventoryManager.getInventory.side_effect = lambda avId: self.inventory
        self.shop = DistributedShopKeeperAI.__new__(DistributedShopKeeperAI)
        self.shop.air = self.air
        self.shop.avatarType = AvatarTypes.Shipwright
        self.shop.sendUpdateToAvatarId = Mock()

    def setGold(self, gold):
        self.gold = gold

    def test_ship_names_are_passed_to_the_loader(self):
        self.shop.requestMakeSale([[ItemId.INTERCEPTOR_L1, 1], [ItemId.INTERCEPTOR_L1, 1]], [],
            [['', [0, 2]], ['  The  Salty Dog ', []]])

        calls = self.air.shipLoader.createShip.call_args_list
        self.assertEqual(calls[0][0][2], PLocalizer.getShipName([0, 2]).strip())
        self.assertEqual(calls[0][0][2], 'Sea Hunter')
        self.assertEqual(calls[1][0][2], 'The Salty Dog')

    def test_invalid_ship_names_fall_back_to_the_default(self):
        self.shop.requestMakeSale([[ItemId.INTERCEPTOR_L1, 1]], [], [['<b>bad</b>', []]])
        self.assertEqual(self.air.shipLoader.createShip.call_args[0][2], '')

        self.shop.requestMakeSale([[ItemId.INTERCEPTOR_L1, 1]], [], [['', [250, 250]]])
        self.assertEqual(self.air.shipLoader.createShip.call_args[0][2], '')

    def test_failed_ship_creation_is_refunded(self):
        self.shop.logShopkeepTransaction = Mock()
        self.shop.requestMakeSale([[ItemId.INTERCEPTOR_L1, 1]], [], [])
        self.assertEqual(self.gold, 900)

        callback = self.air.shipLoader.createShip.call_args[1]['callback']
        callback(1234)
        self.assertEqual(self.gold, 900)
        callback(0)
        self.assertEqual(self.gold, 1000)


class ShipLoaderQueueTests(unittest.TestCase):

    def makeLoader(self):
        loader = loader_ai.DistributedShipLoaderAI.__new__(loader_ai.DistributedShipLoaderAI)
        loader.avatar2fsm = {}
        loader.avatar2pendingShips = {}
        loader.air = SimpleNamespace(shipLoader=loader)
        loader.sendCreateShip = Mock()
        loader.sendActivateShip = Mock()
        return loader

    def test_purchases_are_queued_behind_running_operations(self):
        loader = self.makeLoader()
        inventory = SimpleNamespace(ships=[])
        inventory.getShipDoIdList = lambda: list(inventory.ships)
        inventory.setShipDoIdList = lambda ships: setattr(inventory, 'ships', ships)
        avatar = SimpleNamespace(doId=42, getInventory=lambda: inventory, isDeleted=lambda: False)
        first, second = Mock(), Mock()

        with patch.object(loader_ai.ActivateShipFSM, 'ignoreAll', create=True), \
                patch.object(loader_ai.CreateShipFSM, 'ignoreAll', create=True):
            loader.activateShip(avatar, 1)
            loader.createShip(avatar, ItemId.INTERCEPTOR_L1, 'Sea Dog', callback=first)
            loader.createShip(avatar, ItemId.INTERCEPTOR_L1, '', callback=second)
            loader.sendCreateShip.assert_not_called()

            loader.activateShipResponse(42, 1, True)
            loader.sendCreateShip.assert_called_once_with(42, ItemId.INTERCEPTOR_L1, 'Sea Dog')

            loader.createShipResponse(42, 500)
            first.assert_called_once_with(500)
            loader.sendActivateShip.assert_called_with(42, 500)

            loader.activateShipResponse(42, 500, True)
            loader.sendCreateShip.assert_called_with(42, ItemId.INTERCEPTOR_L1, '')
            loader.createShipResponse(42, 0)
            second.assert_called_once_with(0)

        self.assertEqual(inventory.ships, [500])
        self.assertEqual(loader.avatar2fsm, {})
        self.assertEqual(loader.avatar2pendingShips, {})

    def test_ud_rejects_create_while_busy(self):
        loader = loader_ud.DistributedShipLoaderUD.__new__(loader_ud.DistributedShipLoaderUD)
        loader.avatar2fsm = {42: object()}
        loader.air = SimpleNamespace(netMessenger=Mock())
        loader.createShip(42, ItemId.INTERCEPTOR_L1, 'Sea Dog')
        loader.air.netMessenger.send.assert_called_once_with('createShipResponse', [42, 0])


if __name__ == '__main__':
    unittest.main()
