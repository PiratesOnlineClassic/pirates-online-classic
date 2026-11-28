import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from pirates.piratesbase import PiratesGlobals
from pirates.treasuremap.DistributedTreasureMapAI import DistributedTreasureMapAI
from pirates.uberdog.DistributedInventoryAI import DistributedInventoryAI


class TreasureMapLifecycleTests(unittest.TestCase):
    def test_map_is_inventory_but_not_registered_as_pirate_inventory(self):
        self.assertTrue(issubclass(DistributedTreasureMapAI, DistributedInventoryAI))
        self.assertFalse(DistributedTreasureMapAI.registerWithInventoryManager)

    def test_start_rejects_nonowner_and_duplicate_requests(self):
        avatar = SimpleNamespace(doId=42)
        sender = [43]
        treasure_map = DistributedTreasureMapAI.__new__(DistributedTreasureMapAI)
        treasure_map.ownerId = 42
        treasure_map.air = SimpleNamespace(getAvatarIdFromSender=lambda: sender[0],
                                          doId2do={42: avatar, 43: object()})
        treasure_map.isEnabled = 1
        treasure_map.mapId = PiratesGlobals.GAME_STYLE_TM_BLACK_PEARL
        treasure_map.startPending = False
        treasure_map.activeInstance = None
        treasure_map._createTreasureMapInstance = Mock(return_value=True)
        treasure_map.requestStart(5)
        treasure_map._createTreasureMapInstance.assert_not_called()
        sender[0] = 42
        treasure_map.requestStart(5)
        treasure_map.requestStart(5)
        treasure_map._createTreasureMapInstance.assert_called_once_with(avatar, 'BlackpearlWorld')

        instance = SimpleNamespace(doId=100, participants=[42])
        treasure_map.air.doId2do[100] = instance
        treasure_map.startPending = False
        treasure_map.activeInstance = instance
        treasure_map.requestStart(5)
        treasure_map._createTreasureMapInstance.assert_called_once()
        instance.participants.remove(42)
        treasure_map.requestStart(5)
        self.assertEqual(treasure_map._createTreasureMapInstance.call_count, 2)


if __name__ == '__main__':
    unittest.main()
