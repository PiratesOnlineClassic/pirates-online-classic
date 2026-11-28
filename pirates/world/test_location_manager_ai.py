import builtins
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

if not hasattr(builtins, 'config'):
    from direct.showbase import DConfig
    builtins.config = DConfig

from pirates.world import WorldGlobals
from pirates.world.DistributedLocationManagerAI import DistributedLocationManagerAI


class OceanGrid:
    pass


class GameArea:
    pass


class Interior(GameArea):
    pass


class Island(GameArea):
    pass


class Ship:
    pass


def stubModule(name, **attributes):
    module = types.ModuleType(name)
    module.__dict__.update(attributes)
    return module


stubs = {
    'pirates.world.DistributedOceanGridAI': stubModule('x', DistributedOceanGridAI=OceanGrid),
    'pirates.world.DistributedGameAreaAI': stubModule('x', DistributedGameAreaAI=GameArea),
    'pirates.world.DistributedGAInteriorAI': stubModule('x', DistributedGAInteriorAI=Interior),
    'pirates.world.DistributedIslandAI': stubModule('x', DistributedIslandAI=Island),
    'pirates.ship.DistributedShipAI': stubModule('x', DistributedShipAI=Ship),
}


class LocationManagerTests(unittest.TestCase):
    def setUp(self):
        self.patch = patch.dict(sys.modules, stubs)
        self.patch.start()
        self.manager = DistributedLocationManagerAI.__new__(DistributedLocationManagerAI)
        self.avatar = SimpleNamespace(doId=100, getParentObj=lambda: Island())
        self.manager.air = SimpleNamespace(doId2do={100: self.avatar}, getAvatarIdFromSender=lambda: 100)
        self.manager.sendUpdateToAvatarId = Mock()

    def tearDown(self):
        self.patch.stop()

    def test_island_categories(self):
        self.assertEqual(self.manager.getLocationCategories(self.avatar),
            [WorldGlobals.GAMEAREA, WorldGlobals.ISLAND])

    def test_request_location_responds(self):
        self.manager.requestLocation(WorldGlobals.ISLAND)
        self.manager.requestLocation(WorldGlobals.OCEAN)
        self.assertEqual(self.manager.sendUpdateToAvatarId.call_args_list[0][0], (100, 'locationResponse', [1]))
        self.assertEqual(self.manager.sendUpdateToAvatarId.call_args_list[1][0], (100, 'locationResponse', [0]))


if __name__ == '__main__':
    unittest.main()
