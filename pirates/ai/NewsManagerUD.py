import datetime

from direct.directnotify import DirectNotifyGlobal


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
        self.discordNotifications.serverHolidayEnd(holidayId)

    def startHoliday(self, holidayId, time, quietly=False):
        self.notify.info('Starting Holiday %s across the network for %s seconds' % (holidayId, time))
        self.air.netMessenger.send('startHoliday', [holidayId, time, quietly])

    def stopHoliday(self, holidayId):
        self.notify.info('Telling all AIs to stop holiday %s!' % holidayId)
        self.air.netMessenger.send('stopHoliday', [holidayId])
