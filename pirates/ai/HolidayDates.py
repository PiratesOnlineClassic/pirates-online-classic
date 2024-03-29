import time
from datetime import datetime
class HolidayDates:
    TYPE_CUSTOM = 0
    TYPE_YEARLY = 1
    TYPE_MONTHLY = 2
    TYPE_WEEKLY = 3
    TYPE_DAILY = 4
    
    def __init__(self, holidayType, dateList):
        self.holidayType = holidayType
        self.numDates = len(dateList) / 2
        self.startDates = []
        self.endDates = []
        for i in range(0, len(dateList), 2):
            self.startDates.append(dateList[i])
            self.endDates.append(dateList[i + 1])
    
    def getStartTime(self, index):
        dateTuple = self.startDates[index]
        return self.getTime(dateTuple)
    
    def getAdjustedStartTime(self, index):
        dateTuple = self.startDates[index]
        return self.getAdjustedTime(dateTuple)
    
    def getEndTime(self, index):
        dateTuple = self.endDates[index]
        return self.getTime(dateTuple)
    
    def getAdjustedEndTime(self, index):
        dateTuple = self.endDates[index]
        return self.getAdjustedTime(dateTuple)
    
    def getCurrentDate(self):
        localtime = time.localtime()
        date = (localtime[0], localtime[1], localtime[2], localtime[6])
        return date

    def getTime(self, t):
        date = self.getCurrentDate()
        if self.holidayType == HolidayDates.TYPE_CUSTOM:
            return time.mktime((t[0], t[1], t[2], t[3], t[4], t[5], 0, 0, -1))
        
        if self.holidayType == HolidayDates.TYPE_YEARLY:
            return time.mktime((date[0], t[0], t[1], t[2], t[3], t[4], 0, 0, -1))
        
        if self.holidayType == HolidayDates.TYPE_MONTHLY:
            return time.mktime((date[0], date[1], t[0], t[1], t[2], t[3], 0, 0, -1))
        
        if self.holidayType == HolidayDates.TYPE_WEEKLY:
            cWDay = date[3]
            sWDay = t[0]
            dayOffset = sWDay - cWDay
            day = date[2] + dayOffset
            return time.mktime((date[0], date[1], day, t[1], t[2], t[3], 0, 0, -1))
        
        if self.holidayType == HolidayDates.TYPE_DAILY:
            return time.mktime((date[0], date[1], date[2], t[0], t[1], t[2], 0, 0, -1))

    def getAdjustedTime(self, t):
        date = self.getCurrentDate()
        if self.holidayType == HolidayDates.TYPE_CUSTOM:
            return time.mktime((t[0], t[1], t[2], t[3], t[4], t[5], 0, 0, -1))
        
        if self.holidayType == HolidayDates.TYPE_YEARLY:
            return time.mktime((date[0] + 1, t[0], t[1], t[2], t[3], t[4], 0, 0, -1))
        
        if self.holidayType == HolidayDates.TYPE_MONTHLY:
            return time.mktime((date[0], date[1] + 1, t[0], t[1], t[2], t[3], 0, 0, -1))
        
        if self.holidayType == HolidayDates.TYPE_WEEKLY:
            cWDay = date[3]
            sWDay = t[0]
            dayOffset = sWDay - cWDay
            day = date[2] + dayOffset
            return time.mktime((date[0], date[1], day + 7, t[1], t[2], t[3], 0, 0, -1))
        
        if self.holidayType == HolidayDates.TYPE_DAILY:
            return time.mktime((date[0], date[1], date[2] + 1, t[0], t[1], t[2], 0, 0, -1))
        
    def getReadableStartDate(self, index):
        timestamp = self.getStartTime(index)
        return datetime.utcfromtimestamp(timestamp).strftime('%m/%d/%Y')

    def getReadableEndDate(self, index):
        timestamp = self.getEndTime(index)
        return datetime.utcfromtimestamp(timestamp).strftime('%m/%d/%Y')
