import builtins
import unittest

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

from pirates.pirate import AvatarTypes
from pirates.pirate.AvatarType import AvatarType
from pirates.pirate.AvatarTypeSet import AvatarTypeSet


class RandomAvatarTypeTests(unittest.TestCase):
    # level / 3 is a float on Python 3 and can't index the type tuples.

    def test_random_undead_for_every_level(self):
        for level in range(0, 50):
            self.assertIsInstance(AvatarTypes.randomUndead(level), AvatarType)

    def test_random_navy_for_every_level(self):
        for level in range(0, 50):
            self.assertIsInstance(AvatarTypes.randomNavy(level), AvatarType)


class AvatarTypeSetTests(unittest.TestCase):

    def test_sets_compare(self):
        a = AvatarTypeSet(('a', 'a'), AvatarTypes.Cadet, AvatarTypes.Guard)
        b = AvatarTypeSet(('b', 'b'), AvatarTypes.Guard, AvatarTypes.Cadet)
        c = AvatarTypeSet(('c', 'c'), AvatarTypes.Cadet)
        self.assertTrue(a == b)
        self.assertFalse(a != b)
        self.assertTrue(a != c)


if __name__ == '__main__':
    unittest.main()
