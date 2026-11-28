import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from pirates.world.DistributedCellDoorAI import DistributedCellDoorAI


class DistributedCellDoorAITests(unittest.TestCase):
    def setUp(self):
        self.avatar = SimpleNamespace(doId=42, parentId=7, getJailCellIndex=lambda: 0)
        self.door = DistributedCellDoorAI.__new__(DistributedCellDoorAI)
        self.door.air = SimpleNamespace(
            getAvatarIdFromSender=lambda: 42, doId2do={42: self.avatar})
        self.door.health = 100
        self.door.maxHealth = 100
        self.door.avatarId = 0
        self.door.cellIndex = 0
        self.door.parentId = 7
        self.door.sendUpdate = Mock()
        self.door.sendUpdateToAvatarId = Mock()

    def test_wire_zero_opens_door_on_server_too(self):
        with patch('pirates.world.DistributedCellDoorAI.random.random', return_value=0.997):
            self.door.doorKicked()

        self.assertEqual(self.door.health, 0)
        self.assertEqual(self.door.avatarId, 42)
        self.door.sendUpdate.assert_called_once_with('setHealth', [0])
        self.door.sendUpdateToAvatarId.assert_called_once_with(42, 'rejectInteraction', [])

    def test_nonfinal_kick_preserves_integer_health(self):
        with patch('pirates.world.DistributedCellDoorAI.random.random', return_value=0.245):
            self.door.doorKicked()

        self.assertEqual(self.door.health, 76)
        self.assertEqual(self.door.avatarId, 0)
        self.door.sendUpdate.assert_called_once_with('setHealth', [76])
        self.door.sendUpdateToAvatarId.assert_not_called()


if __name__ == '__main__':
    unittest.main()
