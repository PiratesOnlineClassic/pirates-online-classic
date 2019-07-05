from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.distributed.PiratesInternalRepository import PiratesInternalRepository
from pirates.distributed.DistrictTrackerUD import DistrictTrackerUD
from direct.distributed.PyDatagram import *
from otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from otp.distributed.OtpDoGlobals import *
from pirates.uberdog.PiratesRPCServerUD import PiratesRPCServerUD
from pirates.ai.NewsManagerUD import NewsManagerUD
from pirates.web.PiratesHTTPRestUD import PiratesHTTPRestUD
from pirates.discord.DiscordNotificationsUD import DiscordNotificationsUD

class PiratesUberRepository(PiratesInternalRepository):
    notify = directNotify.newCategory('PiratesUberRepository')
    notify.setInfo(True)

    def __init__(self, baseChannel, serverId):
        PiratesInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='UD')
        self.rpc = None
        self.districtTracker = None
        self.http = None

    def handleConnected(self):
        rootObj = DistributedDirectoryAI(self)
        rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)

        if config.GetBool('want-rpc-server', True):
            self.rpc = PiratesRPCServerUD(self)
            self.rpc.daemon = True
            self.rpc.start()

        self.createGlobals()
        self.notify.info('UberDOG ready!')

    def createGlobals(self):
        """
        Create "global" objects.
        """

        self.rest = PiratesHTTPRestUD(self)
        self.discordNotifications = DiscordNotificationsUD(self)
        self.districtTracker = DistrictTrackerUD(self)
        self.newsManager = NewsManagerUD(self)

        self.centralLogger = self.generateGlobalObject(OTP_DO_ID_CENTRAL_LOGGER, 'CentralLogger')
        self.csm = self.generateGlobalObject(OTP_DO_ID_CLIENT_SERVICES_MANAGER, 'ClientServicesManager')
        self.travelAgent = self.generateGlobalObject(OTP_DO_ID_PIRATES_TRAVEL_AGENT, 'DistributedTravelAgent')
        self.codeRedemption = self.generateGlobalObject(OTP_DO_ID_PIRATES_CODE_REDEMPTION, 'CodeRedemption')
        self.inventoryManager = self.generateGlobalObject(OTP_DO_ID_PIRATES_INVENTORY_MANAGER, 'DistributedInventoryManager')
        self.shipLoader = self.generateGlobalObject(OTP_DO_ID_PIRATES_SHIP_MANAGER, 'DistributedShipLoader')
        self.avatarFriendsManager = self.generateGlobalObject(OTP_DO_ID_AVATAR_FRIENDS_MANAGER, 'PCAvatarFriendsManager')
