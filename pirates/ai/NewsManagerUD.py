from direct.directnotify import DirectNotifyGlobal
import datetime

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
