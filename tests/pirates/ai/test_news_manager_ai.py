import builtins
import time
import unittest
from unittest.mock import Mock, patch

from direct.task import Task

from pirates.ai import HolidayGlobals
from pirates.ai.NewsManagerAI import NewsManagerAI
from pirates.holiday.DistributedHolidayObjectAI import DistributedHolidayObjectAI
from pirates.piratesbase import PiratesGlobals, TODGlobals


def makeNewsManager():
    newsManager = NewsManagerAI.__new__(NewsManagerAI)
    newsManager.air = Mock()
    newsManager.air.timeOfDayMgr.cycleDuration = PiratesGlobals.TOD_CYCLE_DURATION
    newsManager.doId = 1
    newsManager.holidayList = {}
    newsManager.suppressedHolidays = {}
    newsManager.sendUpdate = Mock()
    return newsManager


class NewsManagerAITests(unittest.TestCase):
    def setUp(self):
        self.messenger = Mock()
        self.patcher = patch.object(builtins, 'messenger', self.messenger, create=True)
        self.patcher.start()
        self.taskMgr = Mock()
        self.taskPatcher = patch.object(builtins, 'taskMgr', self.taskMgr, create=True)
        self.taskPatcher.start()

    def tearDown(self):
        self.taskPatcher.stop()
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

    def test_full_moon_warnings_follow_the_jolly_curse_cycle(self):
        newsManager = makeNewsManager()
        cycle = TODGlobals.TOD_JOLLYCURSE_CYCLE
        newsManager.processTimeChange(cycle, PiratesGlobals.TOD_HALF2FULLMOON, 0)
        newsManager.sendUpdate.assert_called_with('displayMessage', [0])

        # the final warning is given a minute before the moon becomes full...
        delay, method, name = self.taskMgr.doMethodLater.call_args[0]
        stateDuration = PiratesGlobals.TOD_CYCLE_DURATION * TODGlobals.getStateDuration(
            cycle, PiratesGlobals.TOD_HALF2FULLMOON)
        self.assertEqual(delay, stateDuration - 60)
        method(*self.taskMgr.doMethodLater.call_args[1]['extraArgs'])
        newsManager.sendUpdate.assert_called_with('displayMessage', [1])

        newsManager.processTimeChange(cycle, PiratesGlobals.TOD_FULLMOON, 0)
        newsManager.sendUpdate.assert_called_with('displayMessage', [3])
        newsManager.processTimeChange(cycle, PiratesGlobals.TOD_FULL2HALFMOON, 0)
        newsManager.sendUpdate.assert_called_with('displayMessage', [7])

    def test_late_full_moon_warning_and_other_cycles(self):
        newsManager = makeNewsManager()
        cycle = TODGlobals.TOD_JOLLYCURSE_CYCLE
        stateDuration = PiratesGlobals.TOD_CYCLE_DURATION * TODGlobals.getStateDuration(
            cycle, PiratesGlobals.TOD_HALF2FULLMOON)
        newsManager.processTimeChange(cycle, PiratesGlobals.TOD_HALF2FULLMOON, stateDuration - 30)
        newsManager.sendUpdate.assert_called_once_with('displayMessage', [1])
        self.taskMgr.doMethodLater.assert_not_called()

        newsManager.sendUpdate.reset_mock()
        newsManager.processTimeChange(cycle, PiratesGlobals.TOD_HALLOWEEN, 0)
        newsManager.processTimeChange(TODGlobals.TOD_HALLOWEEN_CYCLE, PiratesGlobals.TOD_HALLOWEEN, 0)
        newsManager.sendUpdate.assert_not_called()

    def test_jolly_curse_holiday_warns_before_the_cycle_changes(self):
        newsManager = makeNewsManager()
        sent = []
        newsManager.sendUpdate.side_effect = lambda field, args: sent.append((field, args))
        self.messenger.send.side_effect = lambda event, args: sent.append((event, args))
        newsManager.startHoliday(PiratesGlobals.JOLLYROGERCURSE, 1800)
        self.assertLess(sent.index(('displayMessage', [2])),
                        sent.index(('HolidayStarted', [PiratesGlobals.JOLLYROGERCURSE])))

    def test_unknown_holiday_is_never_started(self):
        newsManager = makeNewsManager()
        newsManager.startHoliday(8, 3600)
        self.assertFalse(newsManager.isHolidayActive(8))
        newsManager.sendUpdate.assert_not_called()
        self.messenger.send.assert_not_called()

    def test_stopped_scheduled_holiday_waits_for_its_next_date(self):
        newsManager = makeNewsManager()
        now = time.time()
        dates = Mock(startDates=[0], getStartTime=lambda index: now - 60,
                     getEndTime=lambda index: now + 3600)
        with patch.object(HolidayGlobals, 'holidays', {PiratesGlobals.HALLOWEEN: dates}):
            newsManager._NewsManagerAI__checkHolidays()
            self.assertTrue(newsManager.isHolidayActive(PiratesGlobals.HALLOWEEN))

            newsManager.endHoliday(PiratesGlobals.HALLOWEEN)
            newsManager._NewsManagerAI__checkHolidays()
            self.assertFalse(newsManager.isHolidayActive(PiratesGlobals.HALLOWEEN))

            # a holiday started by hand is no longer suppressed...
            newsManager.startHoliday(PiratesGlobals.HALLOWEEN, 60)
            self.assertNotIn(PiratesGlobals.HALLOWEEN, newsManager.suppressedHolidays)

        # once the scheduled date is over the suppression is cleared...
        newsManager.endHoliday(PiratesGlobals.HALLOWEEN)
        with patch.object(HolidayGlobals, 'holidays', {PiratesGlobals.HALLOWEEN: dates}), \
                patch.object(time, 'time', return_value=now + 7200):
            newsManager._NewsManagerAI__checkHolidays()

        self.assertNotIn(PiratesGlobals.HALLOWEEN, newsManager.suppressedHolidays)


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
