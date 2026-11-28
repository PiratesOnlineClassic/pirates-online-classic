import unittest
from unittest.mock import Mock

from pirates.distributed.PiratesDistrictAI import PiratesDistrictAI


class PiratesDistrictTests(unittest.TestCase):
    def makeDistrict(self):
        district = PiratesDistrictAI.__new__(PiratesDistrictAI)
        district.avatarCount = 0
        district.newAvatarCount = 0
        district.populationLimits = [0, 0]
        district.sendUpdate = Mock()
        return district

    def test_set_stats_broadcasts_molecular_field(self):
        district = self.makeDistrict()
        district.b_setStats(12, 3)
        self.assertEqual((district.getAvatarCount(), district.getNewAvatarCount()), (12, 3))
        district.sendUpdate.assert_called_once_with('setStats', [12, 3])

    def test_full_uses_high_population_limit(self):
        district = self.makeDistrict()
        district.avatarCount = 300
        self.assertFalse(district.isFull())
        district.setPopulationLimits(100, 300)
        self.assertEqual(district.getPopulationLimits(), [100, 300])
        self.assertTrue(district.isFull())


if __name__ == '__main__':
    unittest.main()
