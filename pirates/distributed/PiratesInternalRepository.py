from panda3d.core import *
from otp.distributed.OtpDoGlobals import *
from otp.distributed.OTPInternalRepository import OTPInternalRepository
from pirates.uberdog.WebhooksUD import PiratesWebhookManager

class PiratesInternalRepository(OTPInternalRepository):
    GameGlobalsId = OTP_DO_ID_PIRATES
    dbId = 4003

    def __init__(self, baseChannel, serverId=None, dcFileNames = None, dcSuffix='AI', connectMethod=None, threadedNet=None):
        OTPInternalRepository.__init__(self, baseChannel, serverId, dcFileNames, dcSuffix, connectMethod, threadedNet)
        self.webhookManager = PiratesWebhookManager(self)
        self._registerNetMessages()

    def _registerNetMessages(self):
        # District Status
        self._registerInternalNetMessage('districtStatus')
        self._registerInternalNetMessage('queryDistrictStatus')

        # Holiday Management
        self._registerInternalNetMessage('startHoliday')
        self._registerInternalNetMessage('stopHoliday')
        self._registerInternalNetMessage('uberDOGHolidayStarted')

        # Remote Inventory Manager Control
        #AI
        self._registerInternalNetMessage('hasInventory')
        self._registerInternalNetMessage('addInventory')
        self._registerInternalNetMessage('removeInventory')
        self._registerInternalNetMessage('getInventory')

        #UD
        self._registerInternalNetMessage('hasInventoryResponse')
        self._registerInternalNetMessage('getInventoryResponse')

        # Remote Inventory Control
        #AI
        self._registerInternalNetMessage('b_setAccumulators')
        self._registerInternalNetMessage('b_setAccumulator')
        self._registerInternalNetMessage('b_setStackLimits')
        self._registerInternalNetMessage('b_setStacks')
        self._registerInternalNetMessage('b_setStack')
        self._registerInternalNetMessage('b_setOwnerId')
        self._registerInternalNetMessage('getAccumulators')
        self._registerInternalNetMessage('getAccumulator')
        self._registerInternalNetMessage('getStackLimit')
        self._registerInternalNetMessage('getStack')
        self._registerInternalNetMessage('getOwnerId')

        #UD
        self._registerInternalNetMessage('getOwnerIdResponse')
        self._registerInternalNetMessage('getAccumulatorsResponse')
        self._registerInternalNetMessage('getAccumulatorResponse')
        self._registerInternalNetMessage('getStackLimitResponse')
        self._registerInternalNetMessage('getStackResponse')

