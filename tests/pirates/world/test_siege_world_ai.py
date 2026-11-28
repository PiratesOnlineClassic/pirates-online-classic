import builtins
import importlib
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')


def _stubModule(name, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)

    packageName, moduleName = name.rsplit('.', 1)
    sys.modules[name] = module
    setattr(importlib.import_module(packageName), moduleName, module)


def _ensureTestModules():
    # WeaponGlobals and ObjectList need game resources (pkl files, libotp)
    # which are not available to the unit tests.
    try:
        importlib.import_module('pirates.battle.WeaponGlobals')
    except (IOError, OSError):
        _stubModule('pirates.battle.WeaponGlobals', getAttackHullHP=lambda *args: 0,
            getAttackSailHP=lambda *args: 0, HULL_HP_INDEX=0, SAIL_HP_INDEX=1,
            WEAPON_MOVIE_CLEAR=0, WEAPON_MOVIE_START=1, WEAPON_MOVIE_STOP=2,
            **{'__skillInfo': {}})

    try:
        importlib.import_module('pirates.leveleditor.ObjectList')
    except ImportError:
        _stubModule('pirates.leveleditor.ObjectList', AREA_TYPE_ISLAND='Island',
            AREA_TYPE_ISLAND_REGION='Island Game Area')


_ensureTestModules()

from pirates.piratesbase import PiratesGlobals
from pirates.world.DistributedFortAI import DistributedFortAI
from pirates.world.DistributedDinghyAI import DistributedDinghyAI
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.world import IslandAreaBuilderAI as islandBuilderModule
from pirates.town.DistributedTownAI import DistributedTownAI


class DistributedFortAITests(unittest.TestCase):

    def makeFort(self):
        fort = DistributedFortAI.__new__(DistributedFortAI)
        fort.destroyed = False
        fort.cannons = []
        fort.objKey = 'fort'
        fort.hp = 1000
        fort.treasureMapInstance = None
        fort.sendUpdate = Mock()
        fort.b_setHp = Mock(side_effect=lambda hp, quietly: setattr(fort, 'hp', hp))
        return fort

    def test_projectile_damage_uses_hull_damage(self):
        fort = self.makeFort()
        attacker = SimpleNamespace(doId=42)
        battleMgr = Mock()
        battleMgr.getModifiedHullDamage.return_value = -120.0
        fort.air = SimpleNamespace(getAvatarIdFromSender=lambda: 42, doId2do={42: attacker}, battleMgr=battleMgr)

        fort.hitByProjectile(1, 2)

        battleMgr.getModifiedHullDamage.assert_called_once_with(attacker, fort, 1, 2)
        self.assertEqual(fort.hp, 880)

    def test_projectile_damage_falls_back_without_hull_damage(self):
        fort = self.makeFort()
        fort.air = SimpleNamespace(doId2do={})
        self.assertEqual(fort.getProjectileDamage(42, 1, 2), DistributedFortAI.BaseProjectileDamage)

    def test_destroyed_fort_disables_cannons(self):
        fort = self.makeFort()
        cannon = Mock()
        fort.addCannon(cannon)
        fort.addCannon(cannon)
        self.assertEqual(fort.getCannons(), [cannon])

        fort.takeDamage(5000, 42)

        self.assertTrue(fort.isDestroyed())
        cannon.destroyCannon.assert_called_once_with(repair=False)

        # cannons added after the fort fell start out destroyed
        late = Mock()
        fort.addCannon(late)
        late.destroyCannon.assert_called_once_with(repair=False)

        fort.removeCannon(cannon)
        self.assertEqual(fort.getCannons(), [late])

    def test_drawbridge_updates(self):
        fort = self.makeFort()
        fort.d_setDrawbridgesLerpR(1)
        fort.d_hideDrawbridges()
        fort.sendUpdate.assert_any_call('setDrawbridgesLerpR', [1])
        fort.sendUpdate.assert_any_call('hideDrawbridges', [])


class DinghySiegeTeamTests(unittest.TestCase):

    def makeDinghy(self, siegeTeam, denyReason=None):
        avatar = SimpleNamespace(doId=10, getInventory=lambda: SimpleNamespace(getShipDoIdList=lambda: [30]))
        ship = SimpleNamespace(doId=30, getHp=lambda: 100)
        parentObj = DistributedGameAreaAI.__new__(DistributedGameAreaAI)
        parentObj.shipDeployer = Mock()
        parentObj.shipDeployer.deployShip.side_effect = lambda avatar, shipId, callback, **kwargs: callback(True)
        avatar.getParentObj = lambda: parentObj
        siegeManager = Mock()
        siegeManager.getPvpEnabled.return_value = True
        siegeManager.getJoinDenialCode.return_value = denyReason

        dinghy = DistributedDinghyAI.__new__(DistributedDinghyAI)
        dinghy.siegeTeam = siegeTeam
        dinghy.getPos = lambda: (0, 0, 0)
        dinghy.air = SimpleNamespace(
            doId2do={10: avatar, 30: ship},
            getAvatarIdFromSender=lambda: 10,
            siegeManager=siegeManager,
            questMgr=Mock())
        dinghy.sendUpdateToAvatarId = Mock()
        dinghy.sendAvatarToShip = Mock()
        return dinghy, ship, siegeManager

    def test_privateer_dinghy_puts_ship_on_requested_team(self):
        dinghy, ship, siegeManager = self.makeDinghy(1)
        dinghy.selectOwnShip(30, 2)
        siegeManager.getJoinDenialCode.assert_called_once_with(2)
        siegeManager.addShipToTeam.assert_called_once_with(ship, 2)
        dinghy.sendAvatarToShip.assert_called_once()

    def test_privateer_dinghy_denies_full_team(self):
        dinghy, ship, siegeManager = self.makeDinghy(1, PiratesGlobals.PrivateerSingleTeamFull)
        dinghy.selectOwnShip(30, 0)
        dinghy.sendUpdateToAvatarId.assert_called_once_with(10, 'denyAccess',
            [PiratesGlobals.PrivateerSingleTeamFull])
        siegeManager.addShipToTeam.assert_not_called()
        dinghy.sendAvatarToShip.assert_not_called()

    def test_regular_dinghy_has_no_siege_team(self):
        dinghy, ship, siegeManager = self.makeDinghy(0)
        dinghy.selectOwnShip(30, 0)
        siegeManager.getJoinDenialCode.assert_not_called()
        siegeManager.addShipToTeam.assert_not_called()
        dinghy.sendAvatarToShip.assert_called_once()


class IslandCannonBuilderTests(unittest.TestCase):

    def makeBuilder(self, parentType='Island', siegeTeam=1):
        island = SimpleNamespace(doId=20, getSiegeTeam=lambda: siegeTeam,
            getZoneFromXYZ=lambda pos: 600, generateChildWithRequired=Mock())
        builder = islandBuilderModule.IslandAreaBuilderAI.__new__(islandBuilderModule.IslandAreaBuilderAI)
        builder.air = SimpleNamespace(worldCreator=SimpleNamespace(
            getObjectDataByUid=lambda uid: {'Type': parentType}))
        builder.parent = island
        builder.cannonIndex = 0
        builder.parentObjectToCell = Mock()
        builder.addObject = Mock()
        return builder, island

    def test_island_cannon_created_from_world_data(self):
        builder, island = self.makeBuilder()
        cannons = [Mock(), Mock()]
        with patch.object(islandBuilderModule, 'DistributedIslandCannonAI', side_effect=cannons):
            builder.createIslandCannon(None, 'island', 'cannon-a', {'Pos': (1, 2, 3), 'Hpr': (90, 0, 0)})
            builder.createIslandCannon(None, 'island', 'cannon-b', {'Pos': (4, 5, 6)})

        first, second = cannons
        first.setUniqueId.assert_called_once_with('cannon-a')
        first.setIslandId.assert_called_once_with(20)
        first.setIsDestructable.assert_called_once_with(1)
        first.setCannonIndex.assert_called_once_with(0)
        second.setCannonIndex.assert_called_once_with(1)
        island.generateChildWithRequired.assert_any_call(first, 600)
        builder.addObject.assert_any_call(second)

    def test_fort_cannons_are_left_to_the_fort(self):
        builder, island = self.makeBuilder('Simple Fort')
        with patch.object(islandBuilderModule, 'DistributedIslandCannonAI') as cannonClass:
            self.assertIsNone(builder.createIslandCannon(None, 'fort', 'cannon', {}))

        cannonClass.assert_not_called()


class DistributedTownAITests(unittest.TestCase):

    def test_town_is_a_game_area_grid(self):
        air = SimpleNamespace(dclassesByName={'DistributedTownAI': None})
        town = DistributedTownAI(air)
        town.setModelPath('models/town')
        self.assertEqual(town.getModelPath(), 'models/town')
        self.assertEqual(town.getParentingRules()[0], 'Cartesian')
        self.assertEqual(town.getCellWidth(), town.cellWidth)


if __name__ == '__main__':
    unittest.main()
