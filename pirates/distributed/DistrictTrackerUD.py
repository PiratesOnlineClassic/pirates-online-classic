from direct.directnotify.DirectNotifyGlobal import directNotify

class DistrictTrackerUD:
    notify = directNotify.newCategory('DistrictTrackerUD')

    def __init__(self, air):
        self.air = air
        self.shards = {}

        self.air.netMessenger.accept('districtStatus', self, self.handleDistrictStatus)
        self.requestStatus()
        
    def handleDistrictStatus(self, channel, status):
        self.notify.debug('Received update for channel %d; %s' % (channel, str(status)))
        self.shards.setdefault(channel, {}).update(status)

    def getShards(self):
        return self.shards

    def requestStatus(self):
        self.air.netMessenger.send('queryDistrictStatus')