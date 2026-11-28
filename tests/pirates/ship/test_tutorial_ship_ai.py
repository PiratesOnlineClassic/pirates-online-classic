import ast
import unittest
from types import SimpleNamespace
from tests import REPO_ROOT


def _load_tutorial_ship_methods():
    source = (REPO_ROOT / 'pirates/ship/TutorialShipAI.py').read_text()
    tree = ast.parse(source)
    cls = next(node for node in tree.body
               if isinstance(node, ast.ClassDef) and node.name == 'TutorialShipAI')
    methods = [node for node in cls.body if isinstance(node, ast.FunctionDef)
               and node.name in ('setGameState', 'stopSailing', 'resetSailingToAuthoredPose',
                                 'removeTutorialTarget')]

    class StubDistributedShipAI:

        def setGameState(self, stateName, avId, timeStamp=0):
            self.gameState = [stateName, avId, timeStamp]

        def getGameState(self):
            return self.gameState

    namespace = {'DistributedShipAI': StubDistributedShipAI}
    exec(compile(ast.Module(body=methods, type_ignores=[]), str(__file__), 'exec'), namespace)
    return type('TutorialShipMethods', (StubDistributedShipAI,), {
        node.name: namespace[node.name] for node in methods})


class TutorialShipStateTests(unittest.TestCase):

    def makeShip(self):
        ship = _load_tutorial_ship_methods()()
        ship.tutorialAuthoredState = None
        ship._tutorialSailing = False
        ship.tutorialAuthoredPos = (1, 2, 3)
        ship.tutorialAuthoredHpr = (4, 5, 6)
        ship.tutorialOceanGrid = SimpleNamespace(doId=10, getZoneFromXYZ=lambda pos: 20)
        ship.parentId = 10
        ship.zoneId = 20
        ship.setPos = lambda *args: None
        ship.setHpr = lambda *args: None
        ship.sendCurrentPosition = lambda: None
        ship.b_setLocation = lambda parentId, zoneId: (
            setattr(ship, 'parentId', parentId), setattr(ship, 'zoneId', zoneId))
        ship.b_setGameState = lambda stateName, avId: ship.setGameState(stateName, avId)
        return ship

    def test_reset_restores_authored_state_after_ship_is_put_away(self):
        ship = self.makeShip()
        ship.setGameState('Idle', 0)
        ship.setGameState('PutAway', 0)
        ship.zoneId = 0

        self.assertTrue(ship.resetSailingToAuthoredPose())

        self.assertEqual(ship.tutorialAuthoredState, 'Idle')
        self.assertEqual(ship.gameState[0], 'Idle')
        self.assertEqual((ship.parentId, ship.zoneId), (10, 20))


def _load_tutorial_ship_class():
    import sys
    from unittest.mock import Mock

    from pirates.ship import ShipGlobals
    from pirates.tutorial import TutorialGlobals

    source = (REPO_ROOT / 'pirates/ship/TutorialShipAI.py').read_text()
    tree = ast.parse(source)
    cls = next(node for node in tree.body
               if isinstance(node, ast.ClassDef) and node.name == 'TutorialShipAI')

    class StubDistributedShipAI:

        def __init__(self, air):
            self.air = air
            self.accepted = {}

        def acceptOnce(self, event, method):
            self.accepted[event] = method

        def ignore(self, event):
            self.accepted.pop(event, None)

    namespace = {
        'DistributedShipAI': StubDistributedShipAI,
        'DirectNotifyGlobal': SimpleNamespace(directNotify=SimpleNamespace(
            newCategory=lambda name: SimpleNamespace(warning=Mock(), info=Mock()))),
        'ShipGlobals': ShipGlobals,
        'TutorialGlobals': TutorialGlobals,
    }
    exec(compile(ast.Module(body=[cls], type_ignores=[]), str(__file__), 'exec'), namespace)
    return namespace['TutorialShipAI']


class StubNPCShip:

    def __init__(self, air):
        self.air = air
        self.doId = 77
        self.deleted = False
        self.generated = None
        self.values = {}

    def __getattr__(self, name):
        if name.startswith('set') or name.startswith('b_set'):
            return lambda *args: self.values.__setitem__(name, args)
        raise AttributeError(name)

    def uniqueName(self, name):
        return '%s-%d' % (name, self.doId)

    def sendCurrentPosition(self):
        pass

    def startPosHprBroadcast(self):
        pass

    def isDeleted(self):
        return self.deleted

    def requestDelete(self):
        self.deleted = True


class FakeShipManager:

    def __init__(self):
        self.requests = []

    def spawnTutorialShip(self, oceanGrid, shipClass, level, hp, pos, h, uniqueId=''):
        self.requests.append((oceanGrid, shipClass, level, hp, pos, h, uniqueId))
        return StubNPCShip(None)


class TutorialTargetShipTests(unittest.TestCase):

    def setUp(self):
        shipClass = _load_tutorial_ship_class()
        self.shipManager = FakeShipManager()
        self.ship = shipClass(SimpleNamespace(shipManager=self.shipManager))
        self.grid = SimpleNamespace(name='tutorial ocean grid')
        self.ship.tutorialOceanGrid = self.grid

    def test_undead_ship_is_requested_once_from_the_ship_manager(self):
        from pirates.ship import ShipGlobals
        from pirates.tutorial import TutorialGlobals

        target = self.ship.spawnTutorialTarget()

        self.assertIs(self.ship.spawnTutorialTarget(), target)
        self.assertEqual(self.shipManager.requests, [(
            self.grid, ShipGlobals.SKEL_PHANTOM, 1, self.ship.TargetShipHp,
            self.ship.TargetShipPos, self.ship.TargetShipH, TutorialGlobals.UNDEAD_SHIP_UID)])
        self.assertFalse(self.ship.isTutorialTargetSunk())

    def test_target_practice_ends_when_the_undead_ship_sinks(self):
        target = self.ship.spawnTutorialTarget()
        sinking = self.ship.accepted[target.uniqueName('shipSinking')]

        sinking(StubNPCShip(None))
        self.assertFalse(self.ship.isTutorialTargetSunk())
        sinking(target)
        self.assertTrue(self.ship.isTutorialTargetSunk())

    def test_tutorial_reset_removes_the_undead_ship(self):
        target = self.ship.spawnTutorialTarget()

        self.ship.removeTutorialTarget()

        self.assertTrue(target.deleted)
        self.assertIsNone(self.ship.tutorialTarget)
        self.assertFalse(self.ship.isTutorialTargetSunk())
        self.assertNotIn(target.uniqueName('shipSinking'), self.ship.accepted)
        # the next pirate gets a fresh one...
        self.assertIsNot(self.ship.spawnTutorialTarget(), target)


if __name__ == '__main__':
    unittest.main()
