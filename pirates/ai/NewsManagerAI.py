import datetime
import time

from panda3d.core import ConfigVariableList

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task

from otp.ai.MagicWordGlobal import *

from pirates.ai import HolidayGlobals
from pirates.ai.HolidayDates import HolidayDates
from pirates.piratesbase import PiratesGlobals, TODGlobals

# NewsManager.messages ids
MSG_FULL_MOON_WARNING = 0
MSG_FULL_MOON_FINAL_WARNING = 1
MSG_CURSE_COMING = 2
MSG_CURSE_ACTIVE = 3
MSG_CURSE_END = 7

# the jolly curse cycle starts with the moon waxing to full (five minutes of
# a regular hour long cycle), the final warning is given a minute before...
FULL_MOON_FINAL_WARNING_TIME = 60

JollyCurseMessages = {
    PiratesGlobals.TOD_HALF2FULLMOON: MSG_FULL_MOON_WARNING,
    PiratesGlobals.TOD_FULLMOON: MSG_CURSE_ACTIVE,
    PiratesGlobals.TOD_FULL2HALFMOON: MSG_CURSE_END
}

JollyCurseHolidays = [
    PiratesGlobals.JOLLYROGERCURSE,
    PiratesGlobals.JOLLYCURSEAUTO
]


class NewsManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('NewsManagerAI')
    notify.setInfo(True)

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.wantHolidays = config.GetBool('want-holidays', True)

        self.holidayList = {}

        # holidays stopped while they are scheduled to be running are not
        # restarted by the schedule until their scheduled end time...
        self.suppressedHolidays = {}

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        self.air.timeOfDayMgr.addTimeOfDayStateMethod(PiratesGlobals.TOD_HALF2FULLMOON, 'JollyCurse-Half2FullMoon', self.processTimeChange)
        self.air.timeOfDayMgr.addTimeOfDayStateMethod(PiratesGlobals.TOD_FULLMOON, 'JollyCurse-FullMoon', self.processTimeChange)
        self.air.timeOfDayMgr.addTimeOfDayStateMethod(PiratesGlobals.TOD_FULL2HALFMOON, 'JollyCurse-Full2HalfMoon', self.processTimeChange)

        # Register holiday tasks
        taskMgr.doMethodLater(15, self.__checkHolidays, self.taskName('checkHolidays'))
        taskMgr.doMethodLater(15, self.__runHolidayTimer, self.taskName('holidayTimerTask'))

        # Accept remote networked start and stop of holidays from the UberDOG
        self.air.netMessenger.accept('startHoliday', self, self.startHoliday)
        self.air.netMessenger.accept('stopHoliday', self, self.endHoliday)

        # Load holidays from PRC
        if self.wantHolidays:
            debugHolidays = ConfigVariableList('debug-holiday')
            for holiday in debugHolidays:
                holidaySplit = holiday.split(';')

                holidayId = int(holidaySplit[0])
                endTime = int(holidaySplit[1])

                self.startHoliday(holidayId, endTime)

    def delete(self):
        taskMgr.remove(self.taskName('checkHolidays'))
        taskMgr.remove(self.taskName('holidayTimerTask'))
        taskMgr.remove(self.taskName('fullMoonWarning'))

        DistributedObjectAI.delete(self)

    def isHolidayActive(self, holidayId):
        return holidayId in self.holidayList

    def getScheduledEndTime(self, holidayId, currentTime):
        """
        Returns the end time of the scheduled date the holiday is running in
        at the current time, or None when the holiday is not scheduled to run
        """

        date = HolidayGlobals.getHolidayDates(holidayId)
        if date is None or isinstance(date, dict):
            return None

        for index in range(len(date.startDates)):
            start = date.getStartTime(index)
            end = date.getEndTime(index)
            if currentTime >= start and currentTime <= end:
                return end

        return None

    def __checkHolidays(self, task=None):
        holidays = HolidayGlobals.holidays

        for holidayId in holidays:
            currentTime = time.time()
            end = self.getScheduledEndTime(holidayId, currentTime)

            suppressedEnd = self.suppressedHolidays.get(holidayId)
            if suppressedEnd is not None:
                if end is not None and currentTime <= suppressedEnd:
                    continue

                del self.suppressedHolidays[holidayId]

            if end is not None:
                remaining = end - currentTime
                self.startHoliday(holidayId, remaining)

        return Task.again

    def __runHolidayTimer(self, task=None):
        currentTime = time.time()
        for holidayId, endTime in list(self.holidayList.items()):
            if currentTime >= endTime:
                self.endHoliday(holidayId)

        return Task.again

    def getHolidayEndTime(self, holidayId):
        return self.holidayList.get(holidayId, 0)

    def startHoliday(self, holidayId, duration, quietly=False):
        # the clients look up the holiday's messages as soon as it starts,
        # an unknown holiday would break every client in the district...
        if holidayId not in HolidayGlobals.holidayNames:
            self.notify.warning('Attempted to start unknown holiday %d!' % holidayId)
            return

        if self.isHolidayActive(holidayId):
            return

        if holidayId not in self.holidayList:
            # Holidays are kept by the epoch time they end at, which is also
            # what the client expects in its NewsItem list.
            self.holidayList[holidayId] = int(time.time() + duration)
            self.notify.info('Holiday "%s" (%d) is starting!' % (HolidayGlobals.getHolidayName(holidayId), holidayId))
            self.air.netMessenger.send('uberDOGHolidayStarted', [holidayId, quietly])

            # warn everyone before the time of day switches over to
            # the jolly curse cycle and the moon starts to become full...
            if holidayId in JollyCurseHolidays:
                self.d_displayMessage(MSG_CURSE_COMING)

            messenger.send('HolidayStarted', [holidayId])

        self.suppressedHolidays.pop(holidayId, None)
        self.processHolidayChange()

    def endHoliday(self, holidayId):
        if not self.isHolidayActive(holidayId):
            self.notify.warning('Attempted to stop inactive holiday %d!' % holidayId)
            return

        if holidayId in self.holidayList:
            del self.holidayList[holidayId]
            self.notify.info('Holiday %s is ending!' % holidayId)
            messenger.send('HolidayEnded', [holidayId])

        # don't let the schedule start the holiday right back up again,
        # if it was stopped before it's scheduled end time...
        scheduledEnd = self.getScheduledEndTime(holidayId, time.time())
        if scheduledEnd is not None:
            self.suppressedHolidays[holidayId] = scheduledEnd

        self.processHolidayChange()
        self.air.netMessenger.send('uberDOGHolidayEnded', [holidayId])

    def processHolidayChange(self):
        self.sendHolidayList()
        self.d_holidayNotify()

        # Tell the UberDOG about the change
        if self.air.districtTracker:
            self.air.districtTracker.sendDistrictStatusQuery()

    def sendHolidayList(self):
        # Send updated holiday list
        holidayList = []
        for holiday in self.holidayList:

            endTime = self.holidayList[holiday]
            holidayList.append((holiday, endTime))

        self.sendUpdate('setHolidayIdList', [holidayList])

    def d_displayMessage(self, messageId):
        self.sendUpdate('displayMessage', [messageId])

    def d_holidayNotify(self):
        self.sendUpdate('holidayNotify', [])

    def d_displayMessageToAvatar(self, avatarId, messageId):
        self.sendUpdateToAvatarId(avatarId, 'displayMessage', [messageId])

    def processTimeChange(self, cycleType, todState, stateTime):
        # the moon phases are only part of the jolly curse cycle,
        # which runs while one of Jolly Roger's curse holidays is active...
        taskMgr.remove(self.taskName('fullMoonWarning'))
        if cycleType != TODGlobals.TOD_JOLLYCURSE_CYCLE:
            return

        messageId = JollyCurseMessages.get(todState, None)
        if messageId is None:
            return

        if todState == PiratesGlobals.TOD_HALF2FULLMOON:
            stateDuration = self.air.timeOfDayMgr.cycleDuration * TODGlobals.getStateDuration(cycleType, todState)
            warningDelay = stateDuration - stateTime - FULL_MOON_FINAL_WARNING_TIME
            if warningDelay <= 0:
                self.d_displayMessage(MSG_FULL_MOON_FINAL_WARNING)
                return

            taskMgr.doMethodLater(warningDelay, self.d_displayMessage, self.taskName('fullMoonWarning'),
                extraArgs=[MSG_FULL_MOON_FINAL_WARNING])

        self.d_displayMessage(messageId)

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def stopHoliday(holidayId):
    base.air.newsManager.endHoliday(holidayId)
    return 'Stopped Holiday %d' % holidayId

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int, int])
def startHoliday(holidayId, duration):
    if holidayId not in HolidayGlobals.holidayNames:
        return 'Unknown holiday %d!' % holidayId

    base.air.newsManager.startHoliday(holidayId, duration, True)
    return 'Started Holiday %d' % holidayId

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def displayMessage(messageId):
    base.air.newsManager.d_displayMessage(messageId)
    return 'Sent message: %d' % messageId
