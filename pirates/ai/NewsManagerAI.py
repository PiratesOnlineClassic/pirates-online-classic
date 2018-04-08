from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from pirates.ai import HolidayGlobals
from pirates.ai.HolidayDates import HolidayDates
from pirates.piratesbase import PiratesGlobals, TODGlobals
import datetime
import time

class NewsManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('NewsManagerAI')
    notify.setInfo(True)

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.wantHolidays = config.GetBool('want-holidays', True)

        self.holidayList = {}

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        self.__checkHolidays()
        self.holidayCheckTask = taskMgr.doMethodLater(15, self.__checkHolidays, 'checkHolidays')
        self.holdayTimerTask = taskMgr.doMethodLater(15, self.__runHolidayTimer, 'holidayTimerTask')

    def delete(self):
        DistributedObjectAI.delete(self) 

        taskMgr.remove(self.holidayCheckTask)
        taskMgr.remove(self.holidayTimerTask)

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

    def startHoliday(self, holidayId, time):

        if self.isHolidayActive(holidayId):
            return
        
        if holidayId not in self.holidayList:
            self.holidayList[holidayId] = time
            self.notify.info('Holiday %s is starting!' % holidayId)

        self.processHolidayChange()

    def endHoliday(self, holidayId):
        
        if not self.isHolidayActive(holidayId):
            return

        if holidayId in self.holidayList:
            del self.holidayList[holidayId]
            self.notify.info('Holiday %s is ending!' % holidayId)

        self.processHolidayChange()

    def processHolidayChange(self):
        self.updateTODCycle()
        self.sendHolidayList()

    def sendHolidayList(self):
        # Send updated holiday list
        holidayList = []
        for holiday in self.holidayList:

            endTime = self.holidayList[holiday]
            holidayList.append((holiday, endTime))

        self.sendUpdate('setHolidayIdList', [holidayList])

    def updateTODCycle(self):
        HolidayTODS = {
            PiratesGlobals.HALLOWEEN: TODGlobals.TOD_HALLOWEEN_CYCLE,
            PiratesGlobals.JOLLYROGERCURSE: TODGlobals.TOD_JOLLYCURSE_CYCLE
        }

        found = None
        for holiday in HolidayTODS:
            if holiday in self.holidayList:
                found = holiday
                break

        # Update TOD Cycle
        tod = self.air.timeOfDayMgr
        if found is not None:
            tod.changeCycleType(HolidayTODS[found])
        else:
            if tod.cycleType != TODGlobals.TOD_REGULAR_CYCLE:
                tod.changeCycleType(TODGlobals.TOD_REGULAR_CYCLE)


    
        
