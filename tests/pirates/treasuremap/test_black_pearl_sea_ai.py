import builtins
import math
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from panda3d.core import NodePath, Point3, loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

from pirates.battle.DistributedIslandCannonAI import DistributedIslandCannonAI
from pirates.ship.GameFSMShipAI import GameFSMShipAI
from pirates.treasuremap import TreasureMapBlackPearlGlobals as Globals
from pirates.treasuremap.TreasureMapBlackPearlAI import TreasureMapBlackPearlAI
from pirates.world.DistributedFortAI import DistributedFortAI


class ShipNode(NodePath):
    def getParentObj(self):
        return None


def makeLaneFSM(lane, pos=(0, 0, 0)):
    ship = ShipNode('ship')
    ship.setPos(*pos)
    fsm = GameFSMShipAI.__new__(GameFSMShipAI)
    fsm.ship = ship
    fsm.oceanGrid = None
    fsm.world = None
    fsm.seaLane = None
    fsm.setSeaLane(lane)
    fsm._broadsideTarget = None
    fsm._islandSpheres = []
    return fsm, ship


class SeaLaneTests(unittest.TestCase):
    LANE = [(0, 0, 100), (0, 1000, 100), (1000, 1000, 50)]

    def test_lane_points_are_inside_and_land_is_outside(self):
        fsm, _ = makeLaneFSM(self.LANE)
        self.assertTrue(fsm._isInLane(50, 500))
        self.assertFalse(fsm._isInLane(300, 500))
        self.assertTrue(fsm._isInLane(500, 1030))
        self.assertFalse(fsm._isInLane(500, 1080))

    def test_ship_follows_the_lane_around_the_bend(self):
        fsm, _ = makeLaneFSM(self.LANE, pos=(0, 100, 0))
        waypoint = fsm._getLaneWaypoint(Point3(1000, 1000, 0))
        # the destination is round the corner, the ship sails up the lane first:
        self.assertAlmostEqual(waypoint[0], 0, delta=1)
        self.assertGreater(waypoint[1], 100)

    def test_destination_off_the_lane_is_pulled_into_it(self):
        fsm, _ = makeLaneFSM([(0, 0, 500)])
        point = fsm._clampToLane(2000, 0)
        self.assertLess(point.length(), 500)

    def test_lanes_follow_the_channel_through_the_water(self):
        # the channel's lane runs from the Pearl's mooring to the open sea:
        lane = Globals.CHANNEL_SEA_LANE
        self.assertAlmostEqual(lane[0][0], Globals.BLACK_PEARL_SPAWN_POS[0], delta=1)
        self.assertAlmostEqual(lane[0][1], Globals.BLACK_PEARL_SPAWN_POS[1], delta=1)
        fsm, _ = makeLaneFSM(lane)
        for pos, hpr in Globals.ATTACK_SHIP_SPAWNS:
            self.assertTrue(fsm._isInLane(pos[0], pos[1]), pos)

        self.assertTrue(fsm._isInLane(*Globals.STAGE_FOUR_TRIGGER_POS[:2]))
        sea, _ = makeLaneFSM(Globals.OPEN_SEA_LANE)
        self.assertTrue(sea._isInLane(*Globals.STAGE_FOUR_PEARL_POS[:2]))
        self.assertTrue(sea._isInLane(*Globals.STAGE_FOUR_GOLIATH_POS[:2]))

    def test_hunted_target_is_kept(self):
        fsm = GameFSMShipAI.__new__(GameFSMShipAI)
        target = Mock()
        fsm._isValidTarget = lambda t: t is target
        fsm.engageTarget = Mock(return_value=True)
        fsm.huntTarget = None
        self.assertTrue(fsm.hunt(target))
        self.assertIs(fsm._getHuntTarget(), target)
        fsm._isValidTarget = lambda t: False
        self.assertIsNone(fsm._getHuntTarget())


class FortCannonTests(unittest.TestCase):
    def makeCannon(self, cannonPos, targetPos):
        grid = NodePath('grid')
        cannon = DistributedIslandCannonAI.__new__(DistributedIslandCannonAI)
        NodePath.__init__(cannon, 'cannon')
        cannon.reparentTo(grid)
        cannon.setPos(*cannonPos)
        target = NodePath('target')
        target.reparentTo(grid)
        target.setPos(*targetPos)
        targetObj = SimpleNamespace(getParentObj=lambda: grid, getPos=target.getPos,
                                    isEmpty=lambda: False, isDeleted=lambda: False, takeDamage=Mock())
        return cannon, targetObj

    def test_aim_lands_the_shot_on_the_target(self):
        cannon, target = self.makeCannon((0, 0, 150), (0, 1200, 20))
        heading, pitch, flightTime = cannon.getAim(target)
        self.assertAlmostEqual(heading, 0, places=3)

        # follow the shot the way the client's ProjectileInterval does:
        speed = cannon.getProjectileSpeed()
        horizontal = speed * math.cos(math.radians(pitch)) * flightTime
        height = 150 + speed * math.sin(math.radians(pitch)) * flightTime - \
            0.5 * cannon.AIProjectileGravity * flightTime ** 2
        self.assertAlmostEqual(horizontal, 1200, delta=1)
        self.assertAlmostEqual(height, 20, delta=1)

    def test_out_of_range_target_is_not_fired_at(self):
        cannon, target = self.makeCannon((0, 0, 0), (0, 100000, 0))
        self.assertIsNone(cannon.getAim(target))

    def test_shot_is_shown_and_lands_on_target(self):
        cannon, target = self.makeCannon((0, 0, 150), (800, 0, 20))
        cannon.doId = 5
        cannon.userId = 0
        cannon.destructState = 0
        cannon.uniqueName = lambda name: name
        cannon.sendUpdate = Mock()
        taskMgr = Mock()
        with patch.object(builtins, 'taskMgr', taskMgr, create=True), patch('random.random', return_value=0.0):
            self.assertTrue(cannon.fireAtTarget(target, 0.5, 77))

        self.assertEqual(cannon.sendUpdate.call_args[0][0], 'useProjectileSkill')
        delay, callback, name = taskMgr.doMethodLater.call_args[0]
        callback(*taskMgr.doMethodLater.call_args[1]['extraArgs'])
        target.takeDamage.assert_called_once_with(cannon.getAIShotDamage(), 77, applyModifiers=False)

    def test_manned_cannon_holds_fire(self):
        cannon, target = self.makeCannon((0, 0, 150), (800, 0, 20))
        cannon.userId = 42
        cannon.destructState = 0
        self.assertFalse(cannon.fireAtTarget(target, 1.0))


class FortGunnerTests(unittest.TestCase):
    def test_destroyed_fort_stops_firing(self):
        fort = DistributedFortAI.__new__(DistributedFortAI)
        fort.doId = 9
        fort.destroyed = False
        fort.cannons = []
        fort.attackTarget = None
        fort.cannonReloadTimes = {}
        fort.treasureMapInstance = None
        fort.objKey = 'fort'
        taskMgr = Mock(hasTaskNamed=lambda name: False)
        with patch.object(builtins, 'taskMgr', taskMgr, create=True):
            fort.startAttacking('pearl')
            self.assertEqual(fort.getAttackTarget(), 'pearl')
            fort._handleDestroyed(1)

        self.assertIsNone(fort.getAttackTarget())
        fort.startAttacking('pearl')
        self.assertIsNone(fort.getAttackTarget())


class StageThreeTests(unittest.TestCase):
    def makeInstance(self, pearlPos):
        instance = TreasureMapBlackPearlAI.__new__(TreasureMapBlackPearlAI)
        instance.state = 'StageThree'
        instance.stageFourStarted = False
        instance.barricadesDestroyed = []
        instance.barricadesWarned = set()
        instance.oceanGrid = NodePath('grid')
        pearl = NodePath('pearl')
        pearl.reparentTo(instance.oceanGrid)
        pearl.setPos(*pearlPos)
        instance.blackPearl = pearl
        instance.d_barricadeWarning = Mock()
        instance._moveToStageFour = Mock()
        return instance

    def test_either_entrance_drawbridge_opens_the_channel(self):
        instance = self.makeInstance((0, 0, 0))
        self.assertFalse(instance.isChannelOpen())
        instance.barricadesDestroyed = [1]
        self.assertTrue(instance.isBarricadePassable(0))
        self.assertTrue(instance.isBarricadePassable(2))
        self.assertFalse(instance.isChannelOpen())
        instance.barricadesDestroyed = [1, 4]
        self.assertTrue(instance.isChannelOpen())

    def test_pearl_is_warned_once_about_a_closed_drawbridge(self):
        x, y = Globals.BarricadePositions[4]
        instance = self.makeInstance((x, y + 100, 0))
        instance.barricadesDestroyed = [0]
        instance._checkStageThree()
        instance._checkStageThree()
        instance.d_barricadeWarning.assert_called_once_with(4)
        instance._moveToStageFour.assert_not_called()

    def test_pearl_sailing_past_the_last_drawbridge_starts_stage_four(self):
        instance = self.makeInstance(Globals.STAGE_FOUR_TRIGGER_POS)
        instance._checkStageThree()
        instance._moveToStageFour.assert_not_called()
        instance.barricadesDestroyed = [0, 4]
        instance._checkStageThree()
        instance._moveToStageFour.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
