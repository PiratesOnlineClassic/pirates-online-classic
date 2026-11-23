import unittest
from unittest.mock import Mock

from pirates.interact.DistributedInteractivePropAI import DistributedInteractivePropAI


class DistributedInteractivePropAITests(unittest.TestCase):
    def test_parent_object_field_is_independent_of_distributed_location(self):
        prop = DistributedInteractivePropAI.__new__(DistributedInteractivePropAI)
        prop.parentId = 100
        prop.sendUpdate = Mock()

        prop.b_setParentObjId(200)

        self.assertEqual(prop.parentId, 100)
        self.assertEqual(prop.getParentObjId(), 200)
        prop.sendUpdate.assert_called_once_with('setParentObjId', [200])


if __name__ == '__main__':
    unittest.main()
