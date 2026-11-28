import importlib.util
import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


class GameArea:
    def __init__(self, parent):
        self.doId = 30
        self.parentId = parent.doId
        self.zoneId = 500
        self.parent = parent

    def getUniqueId(self):
        return 'area'

    def getParentObj(self):
        return self.parent


def stubModule(name, **attributes):
    module = types.ModuleType(name)
    module.__dict__.update(attributes)
    return module


class WorldNodeAI:
    def __init__(self, air):
        pass


stubs = {
    'pirates.world.WorldNodeAI': stubModule('pirates.world.WorldNodeAI', WorldNodeAI=WorldNodeAI),
    'pirates.world.ClientAreaBuilderAI': stubModule('pirates.world.ClientAreaBuilderAI',
        ClientAreaBuilderAI=lambda air, parent: None),
    'pirates.world.DistributedGameAreaAI': stubModule('pirates.world.DistributedGameAreaAI',
        DistributedGameAreaAI=GameArea),
}

with patch.dict(sys.modules, stubs):
    spec = importlib.util.spec_from_file_location('_test_DistributedInstanceBaseAI',
        Path(__file__).parent / 'DistributedInstanceBaseAI.py')
    instanceModule = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(instanceModule)


class InstanceBaseTests(unittest.TestCase):
    def setUp(self):
        self.patch = patch.dict(sys.modules, stubs)
        self.patch.start()
        self.instance = instanceModule.DistributedInstanceBaseAI.__new__(instanceModule.DistributedInstanceBaseAI)
        self.instance.doId = 10
        self.instance.spawnPts = {'area': {0: (1, 2, 3, 4)}}
        self.area = GameArea(self.instance)
        self.avatar = SimpleNamespace(doId=100, getParentObj=lambda: self.area,
            gameFSM=SimpleNamespace(getCurrentOrNextState=lambda: 'Death'),
            getJailCellIndex=lambda: 100, getMaxHp=lambda: 50,
            b_setHp=Mock(), b_setGameState=Mock())
        self.instance.air = SimpleNamespace(doId2do={100: self.avatar},
            getAvatarIdFromSender=lambda: 100)
        self.instance.sendUpdateToAvatarId = Mock()

    def tearDown(self):
        self.patch.stop()

    def test_request_spawn_loc_sends_spawn_info(self):
        self.instance.requestSpawnLoc()
        self.instance.sendUpdateToAvatarId.assert_called_once_with(100, 'setSpawnInfo',
            [1, 2, 3, 4, 0, [30, 500, 10]])

    def test_request_spawn_loc_ignores_avatars_elsewhere(self):
        self.area.parent = SimpleNamespace(doId=99)
        self.instance.requestSpawnLoc()
        self.instance.sendUpdateToAvatarId.assert_not_called()

    def test_avatar_died_without_jail_cell_is_released(self):
        self.instance.avatarDied()
        self.avatar.b_setHp.assert_called_once_with(50)
        self.avatar.b_setGameState.assert_called_once_with('LandRoam')
        self.instance.sendUpdateToAvatarId.assert_called_once_with(100, 'sendLocalAvatarToJail', [0, 0, 0])

    def test_avatar_died_with_jail_cell_is_left_alone(self):
        self.avatar.getJailCellIndex = lambda: 2
        self.instance.avatarDied()
        self.instance.sendUpdateToAvatarId.assert_not_called()


if __name__ == '__main__':
    unittest.main()
