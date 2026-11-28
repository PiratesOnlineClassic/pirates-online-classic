import ast
import random
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from pirates.world.DistributedCellDoorAI import DistributedCellDoorAI


def _load_jail_interior_methods():
    source = Path(__file__).with_name('DistributedJailInteriorAI.py').read_text()
    tree = ast.parse(source)
    cls = next(node for node in tree.body
               if isinstance(node, ast.ClassDef) and node.name == 'DistributedJailInteriorAI')
    methods = [node for node in cls.body if isinstance(node, ast.FunctionDef)
               and node.name in ('handleChildLeave', 'getCellDoor', 'avatarAlreadyInJail')]

    class StubInterior:
        handleChildLeave = Mock()

    class StubPirate:
        pass

    namespace = {
        'DistributedGAInteriorAI': StubInterior,
        'DistributedPlayerPirateAI': StubPirate,
        'random': random,
    }
    exec(compile(ast.Module(body=methods, type_ignores=[]), str(__file__), 'exec'), namespace)
    interior = type('JailInteriorMethods', (), {
        node.name: namespace[node.name] for node in methods})
    return interior, StubPirate


class _Avatar:

    def __init__(self, doId, cellIndex):
        self.doId = doId
        self.isNpc = False
        self.cellIndex = cellIndex
        self.parentId = 500
        self.parent = None
        self.gameStates = []

    def getJailCellIndex(self):
        return self.cellIndex

    def b_setJailCellIndex(self, cellIndex):
        self.cellIndex = cellIndex

    def getParentObj(self):
        return self.parent

    def b_setGameState(self, gameState):
        self.gameStates.append(gameState)


def _makeCellDoor(cellIndex, avatar, parentId=500):
    door = DistributedCellDoorAI.__new__(DistributedCellDoorAI)
    door.cellIndex = cellIndex
    door.maxHealth = 100
    door.health = 100
    door.avatarId = 0
    door.parentId = parentId
    door.doId = 600 + cellIndex
    door.notify = SimpleNamespace(warning=Mock())
    door.air = SimpleNamespace(doId2do={avatar.doId: avatar},
                               getAvatarIdFromSender=lambda: avatar.doId)
    door.sendUpdate = Mock()
    door.d_rejectInteraction = Mock()
    return door


class CellDoorTests(unittest.TestCase):

    def test_only_the_jailed_avatar_may_kick_its_cell_door(self):
        avatar = _Avatar(1, 2)
        door = _makeCellDoor(3, avatar)

        self.assertEqual(door.handleRequestInteraction(avatar, 0, 0), door.DENY)
        door.doorKicked()
        self.assertEqual(door.getHealth(), 100)

        avatar.cellIndex = 3
        self.assertEqual(door.handleRequestInteraction(avatar, 0, 0), door.ACCEPT)
        door.doorKicked()
        self.assertLessEqual(door.getHealth(), 100)
        door.sendUpdate.assert_called_with('setHealth', [door.getHealth()])


class JailInteriorTests(unittest.TestCase):

    def setUp(self):
        self.interiorClass, self.pirateClass = _load_jail_interior_methods()

    def makeInterior(self, avatar):
        interior = self.interiorClass()
        interior.doId = 500
        interior.notify = SimpleNamespace(warning=Mock())
        interior.air = SimpleNamespace(doId2do={avatar.doId: avatar},
                                       getAvatarIdFromSender=lambda: avatar.doId)
        return interior

    def test_leaving_jail_resets_the_avatars_own_cell_door(self):
        avatar = _Avatar(1, 2)
        avatar.__class__ = type('Pirate', (_Avatar, self.pirateClass), {})
        interior = self.makeInterior(avatar)
        otherDoor = _makeCellDoor(1, avatar)
        ownDoor = _makeCellDoor(2, avatar)
        ownDoor.health = 0
        interior.cellDoors = {otherDoor.doId: otherDoor, ownDoor.doId: ownDoor}

        interior.handleChildLeave(avatar, 0)

        self.assertEqual(avatar.getJailCellIndex(), 100)
        self.assertEqual(ownDoor.getHealth(), 100)
        self.assertEqual(otherDoor.sendUpdate.call_count, 0)
        interior.notify.warning.assert_not_called()

    def test_unknown_avatar_cell_door_is_not_random(self):
        avatar = _Avatar(1, 7)
        interior = self.makeInterior(avatar)
        door = _makeCellDoor(1, avatar)
        interior.cellDoors = {door.doId: door}

        self.assertIsNone(interior.getCellDoor(avatarId=avatar.doId))
        self.assertIs(interior.getCellDoor(), door)

    def test_avatar_already_in_jail_is_thrown_into_its_cell(self):
        avatar = _Avatar(1, 2)
        interior = self.makeInterior(avatar)
        avatar.parent = interior

        interior.avatarAlreadyInJail()
        self.assertEqual(avatar.gameStates, ['ThrownInJail'])

        avatar.gameStates = []
        avatar.parent = None
        interior.avatarAlreadyInJail()
        self.assertEqual(avatar.gameStates, [])


if __name__ == '__main__':
    unittest.main()
