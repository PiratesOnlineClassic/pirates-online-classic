from direct.directnotify.DirectNotifyGlobal import directNotify

class DistrictTrackerAI:
    notify = directNotify.newCategory('DistrictTrackerAI')

    def __init__(self, air):
        self.air = air
        self.shards = {}

        self.populationTracker = self.air.populationTracker
        self.district = self.air.distributedDistrict
        self.newsManager = self.air.newsManager

        # Handle incoming District status queries so that the 
        # UberDog is able to report them to the internal services
        self.air.netMessenger.accept('queryDistrictStatus', self, self.sendDistrictStatusQuery)

        # Just in case UberDOG was started first. Send our info
        self.sendDistrictStatusQuery()

    def sendDistrictStatusQuery(self):
        # Send district status update containing our information
        status = {
            'shardId': self.populationTracker.getShardId(),
            'districtName': self.district.getName(),
            'population': self.populationTracker.getPopulation(),
            'populationLimits': self.populationTracker.getPopLimits(),
            'holidays': list(self.newsManager.holidayList.keys())
        }

        self.notify.info('Sending District update status to UberDOG')
        self.air.netMessenger.send('districtStatus', [self.air.ourChannel, status])

