import datetime

from direct.directnotify import DirectNotifyGlobal

from pirates.ai import HolidayGlobals
from pirates.web.RPCGlobals import rpcservice, ResponseCodes
from pirates.web.RPCServiceUD import RPCServiceUD


class NewsManagerUD:
    """
    Simple UD class to communicate globally with all AI newsManagers through the
    NetMessenger interface
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('NewsManagerUD')
    notify.setInfo(True)

    def __init__(self, air):
        self.air = air
        self.air.netMessenger.accept('uberDOGHolidayStarted', self, self.handleHolidayStarted)
        self.air.netMessenger.accept('uberDOGHolidayEnded', self, self.handleHolidayEnded)
        self.notify.info('%s is online' % self.__class__.__name__)

    def handleHolidayStarted(self, holidayId, quietly):
        self.notify.info('Holiday (%s) started' % holidayId)
        self.air.discordNotifications.serverHolidayStart(holidayId, quietly)

    def handleHolidayEnded(self, holidayId):
        self.notify.info('Holiday (%s) ended' % holidayId)
        self.air.discordNotifications.serverHolidayEnd(holidayId)

    def startHoliday(self, holidayId, time, quietly=False):
        self.notify.info('Starting Holiday %s across the network for %s seconds' % (holidayId, time))
        self.air.netMessenger.send('startHoliday', [holidayId, time, quietly])

    def stopHoliday(self, holidayId):
        self.notify.info('Telling all AIs to stop holiday %s!' % holidayId)
        self.air.netMessenger.send('stopHoliday', [holidayId])

@rpcservice(serviceName='newsManager')
class NewsService(RPCServiceUD):
    """
    Handles all news related handlers for the RPC
    """

    def getHolidayDates(self):
        """
        Summary:
            Returns the start and end date of all holidays in the source
        Returns:
            dates: List of all holiday start and end dates
        """

        holidays = {}
        for holidayId in HolidayGlobals.holidays:
            date = HolidayGlobals.getHolidayDates(holidayId)
            scheduledDates = {}
            if isinstance(date, dict):
                continue

            for index in range(len(date.startDates)):
                start = date.getStartTime(index)
                end = date.getEndTime(index)
                scheduledDates[index] = [start, end]

            holidays[holidayId] = scheduledDates

        results = self._formatResults(
            dates=holidays)

        return results

    def getHolidays(self):
        """
        Summary:
            Retrieves a list of all holidays happening on the cluster
        Returns:
            holidays: List containing all unique holidays
        """

        districts = self.air.districtTracker.getShards()
        clusterHolidays = []
        for districtId in districts:
            district = districts[districtId]
            holidays = district.get('holidays', [])
            for holiday in holidays:
                if holiday not in clusterHolidays:
                    clusterHolidays.append(holiday)

        results = self._formatResults(
            holidays=clusterHolidays)

        return results

    def startHoliday(self, holidayId, time, announce=False):
        """
        Summary:
            Tells all NewsManagers in the cluster to start a specific holiday id for a
            set amount of time.
        Parameters:
            [int holidayId] = The holiday id to start
            [int time] = The time in seconds for the holiday to run
            [bool announce] = Broadcasts to Discord that the holiday started
        """

        self.air.newsManager.startHoliday(int(holidayId), int(time), quietly=not announce)

        results = self._formatResults(
            code=ResponseCodes.SUCCESS,
            message='Holiday Started',
            holidayId=holidayId,
            time=time,
            announce=announce)

        return results

    def stopHoliday(self, holidayId):
        """
        Summary:
            Tells all NewsManagers in the cluster to stop a specific holiday id.
        Parameters:
            [int holidayId] = The holiday id to stop
        """

        self.air.newsManager.stopHoliday(int(holidayId))

        results = self._formatResults(
            code=ResponseCodes.SUCCESS,
            message='Holiday Stopped',
            holidayId=holidayId)

        return results
