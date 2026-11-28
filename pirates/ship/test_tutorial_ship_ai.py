import ast
import unittest
from pathlib import Path
from types import SimpleNamespace


def _load_tutorial_ship_methods():
    source = Path(__file__).with_name('TutorialShipAI.py').read_text()
    tree = ast.parse(source)
    cls = next(node for node in tree.body
               if isinstance(node, ast.ClassDef) and node.name == 'TutorialShipAI')
    methods = [node for node in cls.body if isinstance(node, ast.FunctionDef)
               and node.name in ('setGameState', 'stopSailing', 'resetSailingToAuthoredPose')]

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


if __name__ == '__main__':
    unittest.main()
