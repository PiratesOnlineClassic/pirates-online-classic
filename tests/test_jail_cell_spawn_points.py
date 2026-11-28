import sys
import types
import unittest
from unittest.mock import patch

# the area builder pulls in the whole level editor, which needs a running
# ShowBase; the spawn point bookkeeping doesn't use it so stub it out...
_builderModule = types.ModuleType('pirates.world.ClientAreaBuilderAI')
_builderModule.ClientAreaBuilderAI = type('ClientAreaBuilderAI', (), {})
with patch.dict(sys.modules, {'pirates.world.ClientAreaBuilderAI': _builderModule}):
    sys.modules.pop('pirates.instance.DistributedInstanceBaseAI', None)
    from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
    sys.modules.pop('pirates.instance.DistributedInstanceBaseAI', None)


class JailCellSpawnPointTests(unittest.TestCase):

    def makeInstance(self):
        instance = DistributedInstanceBaseAI.__new__(DistributedInstanceBaseAI)
        instance.spawnPts = {}
        return instance

    def test_jail_cell_zero_keeps_its_own_spawn_point(self):
        # the jail world data lists it's spawn nodes out of order, with cell 0 fourth...
        instance = self.makeInstance()
        for index in (2, 3, 1, 0, 5, 4):
            instance.addSpawnPt('jail', (index, 0, 0, 0), index)

        self.assertEqual(sorted(instance.spawnPts['jail']), [0, 1, 2, 3, 4, 5])
        for index in range(6):
            self.assertEqual(instance.getSpawnPt('jail', index), (index, 0, 0, 0))

    def test_spawn_points_without_an_index_are_appended(self):
        instance = self.makeInstance()
        instance.addSpawnPt('island', 'a')
        instance.addSpawnPt('island', 'b', -1)
        instance.addSpawnPt('island', 'c')

        self.assertEqual(instance.spawnPts['island'], {0: 'a', 1: 'b', 2: 'c'})

    def test_unknown_index_falls_back_to_a_real_spawn_point(self):
        instance = self.makeInstance()
        instance.addSpawnPt('island', (5, 5, 5, 0), 3)
        self.assertEqual(instance.getSpawnPt('island', 0), (5, 5, 5, 0))
        self.assertEqual(instance.getSpawnPt('island'), (5, 5, 5, 0))
        self.assertEqual(instance.getSpawnPt('missing', 0), (0, 0, 0, 0))


if __name__ == '__main__':
    unittest.main()
