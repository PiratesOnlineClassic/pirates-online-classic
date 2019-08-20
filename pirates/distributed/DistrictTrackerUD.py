from direct.directnotify.DirectNotifyGlobal import directNotify

from pirates.web.RPCGlobals import rpcservice, ResponseCodes
from pirates.web.RPCServiceUD import RPCServiceUD


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

@rpcservice(serviceName='districtTracker')
class DistrictTrackerService(RPCServiceUD):
    """
    Handles all district tracker related handlers for the RPC
    """

    def getShards(self):
        """
        Summary:
            Retrieves the last reported status of all the districts in the server cluster
        Returns:
            districts: List containing all districts
        """

        districts = self.air.districtTracker.getShards()
        return self._formatResults(districts=districts)

    def requestStatus(self):
        """
        Summary:
            Requests the latest district status from the cluster on the UD
        Return:
            None
        """

        self.air.districtTracker.requestStatus()
        return self._formatResults()
