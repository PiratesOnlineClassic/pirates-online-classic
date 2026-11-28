import builtins
import time
import unittest
from unittest.mock import Mock, patch

from direct.task import Task

from pirates.ai import HolidayGlobals
from pirates.ai.NewsManagerAI import NewsManagerAI
from pirates.holiday.DistributedHolidayObjectAI import DistributedHolidayObjectAI
from pirates.piratesbase import PiratesGlobals


def makeNewsManager():
    newsManager = NewsManagerAI.__new__(NewsManagerAI)
    newsManager.air = Mock()
    newsManager.holidayList = {}
    newsManager.sendUpdate = Mock()
    return newsManager


class NewsManagerAITests(unittest.TestCase):
    def setUp(self):
        self.messenger = Mock()
        self.patcher = patch.object(builtins, 'messenger', self.messenger, create=True)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_holiday_list_uses_end_epoch(self):
        newsManager = makeNewsManager()
        before = int(time.time())
        newsManager.startHoliday(PiratesGlobals.DOUBLEXPHOLIDAY, 3600)
        self.assertTrue(newsManager.isHolidayActive(PiratesGlobals.DOUBLEXPHOLIDAY))

        holidayList = newsManager.sendUpdate.call_args_list[0][0][1][0]
        holidayId, endTime = holidayList[0]
        self.assertEqual(holidayId, PiratesGlobals.DOUBLEXPHOLIDAY)
        self.assertTrue(before + 3600 <= endTime <= int(time.time()) + 3600)
        self.messenger.send.assert_any_call('HolidayStarted', [PiratesGlobals.DOUBLEXPHOLIDAY])

    def test_timer_ends_expired_holidays_and_repeats(self):
        newsManager = makeNewsManager()
        newsManager.startHoliday(PiratesGlobals.DOUBLEXPHOLIDAY, -1)
        newsManager.startHoliday(PiratesGlobals.DOUBLEGOLDHOLIDAY, 3600)
        result = newsManager._NewsManagerAI__runHolidayTimer()
        self.assertEqual(result, Task.again)
        self.assertFalse(newsManager.isHolidayActive(PiratesGlobals.DOUBLEXPHOLIDAY))
        self.assertTrue(newsManager.isHolidayActive(PiratesGlobals.DOUBLEGOLDHOLIDAY))
        self.messenger.send.assert_any_call('HolidayEnded', [PiratesGlobals.DOUBLEXPHOLIDAY])

    def test_jolly_curse_message_zero_is_sent(self):
        newsManager = makeNewsManager()
        newsManager.processTimeChange(0, PiratesGlobals.TOD_HALLOWEEN, 0)
        newsManager.sendUpdate.assert_called_with('displayMessage', [0])


class HolidayObjectAITests(unittest.TestCase):
    def makeObject(self, active):
        obj = DistributedHolidayObjectAI.__new__(DistributedHolidayObjectAI)
        obj.air = Mock()
        obj.air.newsManager.isHolidayActive.return_value = active
        obj.holiday = HolidayGlobals.getHolidayName(PiratesGlobals.FOUNDERSFEAST)
        obj.interactMode = obj.INTERACT_NONE
        obj.activeInteractMode = 'All'
        obj.sendUpdate = Mock()
        obj.holidayStart = Mock()
        obj.holidayEnd = Mock()
        return obj

    def test_start_and_end(self):
        obj = self.makeObject(True)
        obj.serverHolidayStart(PiratesGlobals.FOUNDERSFEAST)
        self.assertEqual(obj.interactMode, obj.INTERACT_ALL)
        obj.sendUpdate.assert_called_with('setInteractMode', [obj.INTERACT_ALL])
        obj.holidayStart.assert_called_once()

        obj.air.newsManager.isHolidayActive.return_value = False
        obj.serverHolidayEnd(PiratesGlobals.FOUNDERSFEAST)
        self.assertEqual(obj.interactMode, obj.INTERACT_NONE)
        obj.holidayEnd.assert_called_once()

    def test_gm_mode_by_name(self):
        obj = self.makeObject(True)
        obj.setActiveInteractMode('GM')
        self.assertEqual(obj.getActiveInteractModeId(), obj.INTERACT_GM)
        obj.setActiveInteractMode('Bogus')
        self.assertEqual(obj.getActiveInteractModeId(), obj.INTERACT_NONE)


if __name__ == '__main__':
    unittest.main()
