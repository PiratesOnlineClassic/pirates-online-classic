import sys
import traceback
import sys

from panda3d.core import *
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.distributed.OtpDoGlobals import *
from otp.distributed.OTPInternalRepository import OTPInternalRepository
from pirates.distributed import PiratesMsgTypes

class PiratesInternalRepository(OTPInternalRepository):
    GameGlobalsId = OTP_DO_ID_PIRATES
    dbId = 4003

    def __init__(self, baseChannel, serverId=None, dcFileNames = None, dcSuffix='AI',
        connectMethod=None, threadedNet=None):

        OTPInternalRepository.__init__(self, baseChannel, serverId, dcFileNames,
            dcSuffix, connectMethod, threadedNet)

        self._registerNetMessages()

    def handleDatagram(self, di):
        msgType = self.getMsgType()
        if msgType == CLIENTAGENT_DONE_INTEREST_RESP:
            channel = di.getUint64()
            context = di.getUint16()

            avatarId = channel & 0xffffffff
            self.worldGridManager.handleInterestContextDone(avatarId, context)
        else:
            OTPInternalRepository.handleDatagram(self, di)

    def handleConnected(self):
        OTPInternalRepository.handleConnected(self)

    def serverSetupFinished(self):
        messenger.send('server-ready')

    def _registerNetMessages(self):
        OTPInternalRepository._registerNetMessages(self)
        for netMessage in PiratesMsgTypes.netMessages:
            self._registerInternalNetMessage(netMessage)

        # DistributedShipLoader
        self._registerInternalNetMessage('createShip')
        self._registerInternalNetMessage('createShipResponse')

        self._registerInternalNetMessage('activateShip')
        self._registerInternalNetMessage('activateShipResponse')

    def logPotentialHacker(self, message, kickChannel=False, **kwargs):
        self.notify.warning(message)

        accountId = self.getAccountIdFromSender()
        if not accountId:
            return

        avatarId = self.getAvatarIdFromSender()
        if not avatarId:
            return

        # Log to event logger
        self.writeServerEvent('suspicious-event',
            message=message,
            avatarId=avatarId,
            accountId=accountId,
            **kwargs)

        # Log message to Discord for GameMasters
        self.discordNotifications.reportServerHacker(
            message=message,
            avatarId=avatarId,
            accountId=accountId)

        if kickChannel:
            self.kickChannel(kickChannel)

    def getDistrictName(self):
        if hasattr(self, 'distributedDistrict'):
            return self.distributedDistrict.getName()
        return None

    def getServerName(self):
        serverName = self.getDistrictName()
        if not serverName:
            if self.dcSuffix == 'AI':
                serverName = 'AI'
            else:
                serverName = 'UberDOG'

        return serverName

    def logException(self, e):
        trace = traceback.format_exc()

        accountId = self.getAccountIdFromSender()
        if not accountId:
            return

        avatarId = self.getAvatarIdFromSender()
        if not avatarId:
            return

        senderName = self.getServerName()
        self.centralLogger.reportException(senderName, trace, False)
        self.discordNotifications.reportServerException(e, avatarId, accountId)
        self.notify.warning('internal-exception: %s (%s)' % (repr(e), self.getAvatarIdFromSender()))
        print(trace)

        # Python 2 Vs 3 compatibility
        if not sys.version_info >= (3, 0):
            sys.exc_clear()
