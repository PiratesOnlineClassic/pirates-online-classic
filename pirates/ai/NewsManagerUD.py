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

    def startHoliday(self, holidayId, time):
        self.notify.info('Starting Holiday %s accross the network for %s seconds' % (holidayId, time))
        self.air.netMessenger.send('startHoliday', [holidayId, time])

    def stopHoliday(self, holidayId):
        self.notify.info('Telling all AIs to stop holiday %s!' % holidayId)
        self.air.netMessenger.send('stopHoliday', [holidayId])