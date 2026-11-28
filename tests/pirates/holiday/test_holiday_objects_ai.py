import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')

if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

from pirates.holiday.DistributedHolidayBonfireAI import DistributedHolidayBonfireAI
from pirates.holiday.DistributedHolidayPigAI import DistributedHolidayPigAI


class AnyDClass(dict):

    def __missing__(self, className):
        return None


class FakeIsland:

    def __init__(self, doId):
        self.doId = doId
        self.b_setFeastFireEnabled = Mock()


def makeAir(*islands):
    air = SimpleNamespace(doId2do={}, dclassesByName=AnyDClass(),
        newsManager=SimpleNamespace(isHolidayActive=lambda holidayId: False))
    for island in islands:
        air.doId2do[island.doId] = island

    return air


def place(obj, air, parentId, doId):
    obj.doId = doId
    obj.parentId = parentId
    obj.zoneId = 500
    obj.cr = air
    obj.sendUpdate = Mock()
    obj.sendUpdateToAvatarId = Mock()


class HolidayObjectTests(unittest.TestCase):

    def setUp(self):
        self.island = FakeIsland(1000)
        self.otherIsland = FakeIsland(2000)
        self.air = makeAir(self.island, self.otherIsland)

        self.bonfire = DistributedHolidayBonfireAI(self.air)
        place(self.bonfire, self.air, self.island.doId, 10)
        self.pig = DistributedHolidayPigAI(self.air)
        place(self.pig, self.air, self.island.doId, 11)
        self.otherPig = DistributedHolidayPigAI(self.air)
        place(self.otherPig, self.air, self.otherIsland.doId, 12)

        for pig in (self.pig, self.otherPig):
            pig.bonfireStartedEvent = DistributedHolidayBonfireAI.getBonfireStartedEvent(pig.parentId)
            pig.accept(pig.bonfireStartedEvent, pig.bonfireStarted)

    def tearDown(self):
        for obj in (self.bonfire, self.pig, self.otherPig):
            obj.ignoreAll()

    def test_bonfire_only_roasts_the_pig_on_its_island(self):
        self.bonfire.b_setFireStarted(True)

        self.assertTrue(self.pig.getPigRoasting())
        self.assertFalse(self.otherPig.getPigRoasting())
        self.island.b_setFeastFireEnabled.assert_called_once_with(True)
        self.otherIsland.b_setFeastFireEnabled.assert_not_called()

    def test_bonfire_is_lit_once(self):
        avatar = SimpleNamespace(doId=42)
        self.assertEqual(self.bonfire.handleHolidayInteract(avatar, 0, False), self.bonfire.ACCEPT)
        self.assertEqual(self.bonfire.handleHolidayInteract(avatar, 0, False), self.bonfire.DENY)
        self.bonfire.lightTrack.finish()
        self.assertTrue(self.bonfire.getFireStarted())
        self.bonfire.sendUpdateToAvatarId.assert_called_once_with(42, 'finishInteraction', [])
        self.assertEqual(self.bonfire.handleHolidayInteract(avatar, 0, False), self.bonfire.DENY)

    def test_holiday_objects_are_shared(self):
        self.assertTrue(DistributedHolidayBonfireAI.MULTIUSE)
        self.assertTrue(DistributedHolidayPigAI.MULTIUSE)


if __name__ == '__main__':
    unittest.main()
