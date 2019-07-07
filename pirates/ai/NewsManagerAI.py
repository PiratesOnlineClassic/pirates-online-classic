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

JollyCurseMessages = {
    PiratesGlobals.TOD_HALLOWEEN: 0,
    PiratesGlobals.TOD_HALF2FULLMOON: 1,
    PiratesGlobals.TOD_FULLMOON: 3,
    PiratesGlobals.TOD_FULL2HALFMOON: 7
}


class NewsManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('NewsManagerAI')
    notify.setInfo(True)

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.wantHolidays = config.GetBool('want-holidays', True)

        self.holidayList = {}

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

                self.startHoliday(holidayId, time=endTime)

    def delete(self):
        taskMgr.remove(self.taskName('checkHolidays'))
        taskMgr.remove(self.taskName('holidayTimerTask'))

        DistributedObjectAI.delete(self)

    def isHolidayActive(self, holidayId):
        return holidayId in self.holidayList

    def __checkHolidays(self, task=None):
        holidays = HolidayGlobals.holidays

        for holidayId in holidays:
            date = HolidayGlobals.getHolidayDates(holidayId)
            currentTime = time.time()

            if date is None:
                continue

            if isinstance(date, dict):
                continue

            for index in range(len(date.startDates)):
                start = date.getStartTime(index)
                end = date.getEndTime(index)
                if currentTime >= start and currentTime <= end:
                    remaining = end - currentTime
                    self.startHoliday(holidayId, time=remaining)

        return Task.again

    def __runHolidayTimer(self, task=None):
        if len(self.holidayList) > 0:
            for holiday in self.holidayList:
                time = self.holidayList[holiday]
                time -= 15

                self.holidayList[holiday] = time
                if time <= 0:
                    self.endHoliday(holiday)

    def startHoliday(self, holidayId, time, quietly=False):
        if self.isHolidayActive(holidayId):
            return

        if holidayId not in self.holidayList:
            self.holidayList[holidayId] = time
            self.notify.info('Holiday "%s" (%d) is starting!' % (HolidayGlobals.getHolidayName(holidayId), holidayId))
            self.air.netMessenger.send('uberDOGHolidayStarted', [holidayId, quietly])
            messenger.send('HolidayStarted', [holidayId])

        self.processHolidayChange()

    def endHoliday(self, holidayId):
        if not self.isHolidayActive(holidayId):
            self.notify.warning('Attempted to stop inactive holiday %d!' % holidayId)
            return

        if holidayId in self.holidayList:
            del self.holidayList[holidayId]
            self.notify.info('Holiday %s is ending!' % holidayId)
            messenger.send('HolidayEnded', [holidayId])

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
        self.sendUpdateToAvatar(avatarId, 'displayMessage', [messageId])

    def processTimeChange(self, cycleType, todState, stateTime):
        # Check if Jolly Rogers's curse is active
        #curseActive = self.isHolidayActive(PiratesGlobals.CURSEDNIGHT)
        #if curseActive and cycleType == PiratesGlobals.TOD_JOLLYCURSE_CYCLE:
        messageId = JollyCurseMessages.get(todState, None)
        if messageId:
            self.d_displayMessage(messageId)

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def stopHoliday(holidayId):
    simbase.air.newsManager.endHoliday(holidayId)
    return 'Stopped Holiday %d' % holidayId

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int, int])
def startHoliday(holidayId, time):
    simbase.air.newsManager.startHoliday(holidayId, time, True)
    return 'Started Holiday %d' % holidayId

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int, int])
def displayMessage(messageId):
    simbase.air.newsManager.d_displayMessage(messageId)
    return 'Sent message: %d' % messageId
