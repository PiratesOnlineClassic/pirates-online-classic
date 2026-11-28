import ast
import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from panda3d.core import NodePath

from tests import REPO_ROOT


class FakeBattleAvatar(NodePath):

    def __init__(self, name, local=False):
        NodePath.__init__(self, name)
        self.local = local
        self.swapFloorCollideMask = Mock()
        self.refreshActiveQuestStep = Mock()

    def isLocal(self):
        return self.local


def load_handle_child_arrive():
    source = (REPO_ROOT / 'pirates/ship/DistributedShip.py').read_text()
    tree = ast.parse(source)
    cls = next(node for node in tree.body
               if isinstance(node, ast.ClassDef) and node.name == 'DistributedShip')
    method = next(node for node in cls.body
                  if isinstance(node, ast.FunctionDef) and node.name == 'handleChildArrive')
    worldGrid = SimpleNamespace(startProcessVisibility=Mock())
    namespace = {
        'DistributedMovingObject': SimpleNamespace(handleChildArrive=Mock()),
        'DistributedBattleAvatar': SimpleNamespace(DistributedBattleAvatar=FakeBattleAvatar),
        'PiratesGlobals': SimpleNamespace(FloorBitmask=1, ShipFloorBitmask=2),
        'base': SimpleNamespace(cr=SimpleNamespace(activeWorld=SimpleNamespace(worldGrid=worldGrid))),
        'localAvatar': None,
    }
    exec(compile(ast.Module(body=[method], type_ignores=[]), str(__file__), 'exec'), namespace)
    return namespace['handleChildArrive']


class ShipDeckParentingTests(unittest.TestCase):

    def setUp(self):
        self.handleChildArrive = load_handle_child_arrive()
        self.render = NodePath('render')
        ship = self.render.attachNewNode('ship')
        ship.setPos(128.5, 152.1, 0)
        ship.setH(-114)
        self.ship = SimpleNamespace(root=ship.attachNewNode('shipRoot'), boardingInProgress=0)

    def test_crew_generated_on_deck_is_put_on_the_deck(self):
        # Bo Beck is generated straight into the deck zone, the AI's position
        # is relative to the ship so it must not be converted...
        beck = FakeBattleAvatar('Captain Bo Beck')
        beck.setPos(0, -1.2, 9)
        self.handleChildArrive(self.ship, beck, 500)
        self.assertEqual(beck.getParent(), self.ship.root)
        self.assertAlmostEqual(beck.getPos().getY(), -1.2, places=4)
        self.assertAlmostEqual(beck.getPos().getZ(), 9, places=4)

    def test_local_avatar_from_island_grid_keeps_world_position(self):
        # Panda's DistributedNode detaches a child still under the grid cell
        # it is leaving, the local avatar must already be on the deck by then...
        cell = self.render.attachNewNode('cellOrigin-33140')
        avatar = FakeBattleAvatar('localAvatar', local=True)
        avatar.reparentTo(cell)
        avatar.setPos(128.1, 127.4, 3.9)
        worldPos = avatar.getPos(self.render)
        self.handleChildArrive(self.ship, avatar, 500)
        self.assertEqual(avatar.getParent(), self.ship.root)
        self.assertTrue(avatar.getPos(self.render).almostEqual(worldPos, 0.001))
        avatar.refreshActiveQuestStep.assert_called_once_with()

    def test_child_already_on_deck_is_left_alone(self):
        avatar = FakeBattleAvatar('pirate')
        avatar.reparentTo(self.ship.root)
        avatar.setPos(1, 2, 3)
        self.handleChildArrive(self.ship, avatar, 500)
        self.assertEqual(avatar.getParent(), self.ship.root)
        self.assertTrue(avatar.getPos().almostEqual((1, 2, 3), 0.001))


if __name__ == '__main__':
    unittest.main()
