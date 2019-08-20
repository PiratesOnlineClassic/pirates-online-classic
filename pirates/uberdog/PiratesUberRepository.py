from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.PyDatagram import *

from otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from otp.distributed.OtpDoGlobals import *

from pirates.distributed.PiratesInternalRepository import PiratesInternalRepository
from pirates.distributed.DistrictTrackerUD import DistrictTrackerUD
from pirates.ai.NewsManagerUD import NewsManagerUD
from pirates.discord.DiscordNotificationsUD import DiscordNotificationsUD
from pirates.web.PiratesRPCServiceUD import PiratesRPCServiceUD
from pirates.web.PiratesHTTPRestUD import PiratesHTTPRestUD
from pirates.web.RPCGlobals import rpcservice, ResponseCodes
from pirates.web.RPCServiceUD import RPCServiceUD

class PiratesUberRepository(PiratesInternalRepository):
    notify = directNotify.newCategory('PiratesUberRepository')
    notify.setInfo(True)

    def __init__(self, baseChannel, serverId):
        PiratesInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='UD')
        self.rpc = None
        self.districtTracker = None
        self.http = None

    def handleConnected(self):
        PiratesInternalRepository.handleConnected(self)

        rootObj = DistributedDirectoryAI(self)
        rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)

        if config.GetBool('want-rpc-server', True):
            self.rpc = PiratesRPCServiceUD(self)
            self.rpc.daemon = True
            self.rpc.start()

        self.createGlobals()
        self.serverSetupFinished()

    def serverSetupFinished(self):
        PiratesInternalRepository.serverSetupFinished(self)
        self.notify.info('UberDOG ready!')

    def createGlobals(self):
        """
        Create "global" objects.
        """

        self.rest = PiratesHTTPRestUD(self)
        self.discordNotifications = DiscordNotificationsUD(self)
        self.districtTracker = DistrictTrackerUD(self)
        self.newsManager = NewsManagerUD(self)

        self.settingsMgr = self.generateGlobalObject(OTP_DO_ID_PIRATES_SETTINGS_MANAGER, 'PiratesSettingsMgr')
        self.centralLogger = self.generateGlobalObject(OTP_DO_ID_CENTRAL_LOGGER, 'CentralLogger')
        self.csm = self.generateGlobalObject(OTP_DO_ID_CLIENT_SERVICES_MANAGER, 'ClientServicesManager')
        self.travelAgent = self.generateGlobalObject(OTP_DO_ID_PIRATES_TRAVEL_AGENT, 'DistributedTravelAgent')
        self.codeRedemption = self.generateGlobalObject(OTP_DO_ID_PIRATES_CODE_REDEMPTION, 'CodeRedemption')
        self.inventoryManager = self.generateGlobalObject(OTP_DO_ID_PIRATES_INVENTORY_MANAGER, 'DistributedInventoryManager')
        self.shipLoader = self.generateGlobalObject(OTP_DO_ID_PIRATES_SHIP_MANAGER, 'DistributedShipLoader')
        self.avatarFriendsManager = self.generateGlobalObject(OTP_DO_ID_AVATAR_FRIENDS_MANAGER, 'PCAvatarFriendsManager')

@rpcservice(serviceName='cluster')
class ClusterService(RPCServiceUD):
    """
    Handles all cluster related handlers for the RPC
    """

    def ping(self, response):
        """
        Summary:
            Responds with the [data] that was sent. This method exists only for
            testing purposes.
        Parameters:
            [any data] = The data to be given back in response.
        Example response: 'pong'
        """

        return self._formatResults(response=response)

    def systemMessage(self, message):
        """
        Summary:
            Broadcasts a [message] to the entire server globally.
        Parameters:
            [str message] = The message to broadcast.
        """

        self.air.systemMessage(message)
        return self._formatResults()

    def systemMessageChannel(self, message, channel):
        """
        Summary:
            Broadcasts a [message] to any client whose Client Agent is
            subscribed to the provided [channel].
        Parameters:
            [int channel] = The channel to direct the message to.
            [str message] = The message to broadcast.
        """

        channel = (channel + 1 << 32) | 2
        self.air.systemMessage(message, channel)
        return self._formatResults()

    def kickChannel(self, channel, reason=1, message=''):
        """
        Summary:
            Kicks any users whose CAs are subscribed to a particular [channel] with a [code].
        Parameters:
            [int channel] = The channel to direct the message to.
            [int code] = An optional code to kick.
            [string reason] = An optional reason.
        """

        try:
            self.air.kickChannel(channel, reason, message)
        except Exception as e:
            return self._formatResults(
                code=ResponseCodes.INTERNAL_ERROR,
                 message='Failed to kick channel, An unexpected error occured',
                 error=repr(e))

        return self._formatResults()