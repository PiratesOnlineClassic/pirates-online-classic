import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from pirates.interact.DistributedNPCToyAI import DistributedNPCToyAI
from pirates.destructibles.DistributedDestructibleObjectAI import DistributedDestructibleObjectAI


class DistributedNPCToyAITests(unittest.TestCase):
    def makeToy(self):
        toy = DistributedNPCToyAI.__new__(DistributedNPCToyAI)
        toy.modelPath = ''
        toy.parentObjId = 0
        toy.movie = 0
        toy.uniqueId = ''
        toy.sendUpdate = Mock()
        toy.sendUpdateToAvatarId = Mock()
        return toy

    def test_required_fields_have_getters(self):
        toy = self.makeToy()
        toy.setUniqueId('toy-1')
        toy.setModelPath('models/props/barrel')
        toy.setParentObjId(100)
        self.assertEqual(toy.getUniqueId(), 'toy-1')
        self.assertEqual(toy.getModelPath(), 'models/props/barrel')
        self.assertEqual(toy.getParentObjId(), 100)
        self.assertEqual(toy.getMovie(), 0)

    def test_interaction_plays_movie_without_storing_it(self):
        toy = self.makeToy()
        avatar = SimpleNamespace(doId=42)
        self.assertEqual(toy.handleRequestInteraction(avatar, 0, False), toy.ACCEPT)
        toy.handlePostRequestInteraction(avatar)
        toy.sendUpdate.assert_called_once_with('setMovie', [42])
        self.assertEqual(toy.getMovie(), 0)
        self.assertEqual(toy.handleRequestExit(avatar), toy.ACCEPT)


class DistributedDestructibleObjectAITests(unittest.TestCase):
    def test_dc_object_type(self):
        obj = DistributedDestructibleObjectAI.__new__(DistributedDestructibleObjectAI)
        obj.setDcObjectType('Barrel')
        self.assertEqual(obj.getDcObjectType(), 'Barrel')


if __name__ == '__main__':
    unittest.main()
