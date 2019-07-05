import datetime

from direct.directnotify import DirectNotifyGlobal

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
        self.pastBroadcastCacheDelay = config.GetInt('news-manager-past-broadcast-cache', 5)
        
        self.__broadcastedHolidays = {}
        self.__lastBroadcast = None

    def handleHolidayStarted(self, holidayId, quietly):
        if not quietly:
            # Clear old broadcast checks
            now = datetime.datetime.now()
            for broadcast in self.__broadcastedHolidays:
                expireTime = self.__broadcastedHolidays[broadcast]
                if expireTime <= now:
                    self.__broadcastedHolidays.pop(broadcast)
                    continue

            # Verify we should broadcast
            if holidayId in self.__broadcastedHolidays or self.__lastBroadcast == holidayId:
                return

            success = self.air.webhookManager.logHolidayMessage(holidayId)
            if success:
                self.notify.info('Broadcasted holiday message to Discord')
                expireTime = datetime.datetime.now() + datetime.timedelta(minutes=self.pastBroadcastCacheDelay)
                self.__broadcastedHolidays[holidayId] = expireTime
                self.__lastBroadcast = holidayId

    def startHoliday(self, holidayId, time, quietly=False):
        self.notify.info('Starting Holiday %s across the network for %s seconds' % (holidayId, time))
        self.air.netMessenger.send('startHoliday', [holidayId, time, quietly])

    def stopHoliday(self, holidayId):
        self.notify.info('Telling all AIs to stop holiday %s!' % holidayId)
        self.air.netMessenger.send('stopHoliday', [holidayId])

@rpcservice()
class HolidayService(RPCServiceUD):
    """
    Handles all holiday related handlers for the RPC
    """

    def getHolidays(self):
        """
        Summary:
            Retrieves a list of all holidays happening on the cluster
        Returns:
            holidays: List containing all unique holidays
        """

        districts = self.air.districtTracker.getShards()
        holidays = []
        for district in districts:
            holidays += district['holidays']

        results = self._formatResults(
            holidays=holidays)

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