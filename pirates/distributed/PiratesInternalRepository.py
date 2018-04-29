import traceback
import sys

from panda3d.core import *
from direct.distributed.AstronInternalRepository import AstronInternalRepository
from otp.distributed.OtpDoGlobals import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from pirates.uberdog.WebhooksUD import PiratesWebhookManager

class PiratesInternalRepository(AstronInternalRepository):
    GameGlobalsId = OTP_DO_ID_PIRATES
    dbId = 4003

    def __init__(self, baseChannel, serverId=None, dcFileNames = None, dcSuffix='AI', connectMethod=None, threadedNet=None):
        AstronInternalRepository.__init__(self, baseChannel, serverId, dcFileNames, dcSuffix, connectMethod, threadedNet)
        self.webhookManager = PiratesWebhookManager(self)

        self._netMessageCounter = 0
        self.__registerNetMessages()


    def __registerInternalNetMessage(self, message):
        self.netMessenger.register(self._netMessageCounter, message)
        self._netMessageCounter += 1

    def __registerNetMessages(self):
        # District Status
        self.__registerInternalNetMessage('districtStatus')
        self.__registerInternalNetMessage('queryDistrictStatus')

        # Holiday Management
        self.__registerInternalNetMessage('startHoliday')
        self.__registerInternalNetMessage('stopHoliday')
        self.__registerInternalNetMessage('uberDOGHolidayStarted')

        # Remote Inventory Manager Control
        #AI
        self.__registerInternalNetMessage('hasInventory')
        self.__registerInternalNetMessage('addInventory')
        self.__registerInternalNetMessage('removeInventory')
        self.__registerInternalNetMessage('getInventory')

        #UD
        self.__registerInternalNetMessage('hasInventoryResponse')
        self.__registerInternalNetMessage('getInventoryResponse')

        # Remote Inventory Control
        #AI
        self.__registerInternalNetMessage('b_setAccumulators')
        self.__registerInternalNetMessage('b_setAccumulator')
        self.__registerInternalNetMessage('b_setStackLimits')
        self.__registerInternalNetMessage('b_setStacks')
        self.__registerInternalNetMessage('b_setStack')
        self.__registerInternalNetMessage('b_setOwnerId')
        self.__registerInternalNetMessage('getAccumulators')
        self.__registerInternalNetMessage('getAccumulator')
        self.__registerInternalNetMessage('getStackLimit')
        self.__registerInternalNetMessage('getStack')
        self.__registerInternalNetMessage('getOwnerId')

        #UD
        self.__registerInternalNetMessage('getOwnerIdResponse')
        self.__registerInternalNetMessage('getAccumulatorsResponse')
        self.__registerInternalNetMessage('getAccumulatorResponse')
        self.__registerInternalNetMessage('getStackLimitResponse')
        self.__registerInternalNetMessage('getStackResponse')

    def getAvatarIdFromSender(self):
        return self.getMsgSender() & 0xFFFFFFFF

    def getAccountIdFromSender(self):
        return (self.getMsgSender() >> 32) & 0xFFFFFFFF

    def isDevServer(self):
        return 'dev' in config.GetString('server-version', '') or __dev__

    def setAllowClientSend(self, avId, distObj, fieldNameList=[]):
        dg = PyDatagram()
        dg.addServerHeader(distObj.GetPuppetConnectionChannel(avId), self.ourChannel, CLIENTAGENT_SET_FIELDS_SENDABLE)
        fieldIds = []
        for fieldName in fieldNameList:
            field = distObj.dclass.getFieldByName(fieldName)
            if field:
                fieldIds.append(field.getNumber())

        dg.addUint32(distObj.getDoId())
        dg.addUint16(len(fieldIds))
        for fieldId in fieldIds:
            dg.addUint16(fieldId)

        self.send(dg)

    def _isValidPlayerLocation(self, parentId, zoneId):
        return True

    def systemMessage(self, message, channel=10):
        msgDg = PyDatagram()
        msgDg.addUint16(10)
        msgDg.addString(message)

        self.writeServerEvent('system-message',
            sourceChannel=self.ourChannel,
            message=message,
            targetChannel=channel)

        dg = PyDatagram()
        dg.addServerHeader(channel, self.ourChannel, CLIENTAGENT_SEND_DATAGRAM)
        dg.addString(msgDg.getMessage())
        self.send(dg)

    def kickChannel(self, channel, reason=1, message='An unexpected problem has occured.'):
        dg = PyDatagram()
        dg.addServerHeader(channel, self.ourChannel, CLIENTAGENT_EJECT)
        dg.addUint16(reason)
        dg.addString(message)
        self.send(dg)

    def logPotentialHacker(self, message, kickChannel=False, **kwargs):
        self.notify.warning(message)

        avatarId = self.getAvatarIdFromSender() or 0
        accountId = self.getAccountIdFromSender() or 0

        # Log to event logger
        self.writeServerEvent('suspicious-event',
            message=message,
            avatarId=avatarId,
            accountId=accountId,
            **kwargs)

        # Log message to Discord
        self.webhookManager.logPotentialHacker(avatarId, accountId, message, **kwargs)

        if kickChannel:
            self.kickChannel(kickChannel)

    def logException(self, e):
        trace = traceback.format_exc()

        avatarId = self.getAvatarIdFromSender() or 0
        accountId = self.getAccountIdFromSender() or 0

        self.writeServerEvent('internal-exception',
            serverSuffix=self.dcSuffix,
            avId=avatarId,
            accountId=accountId,
            exception=trace)

        self.notify.warning('internal-exception: %s (%s)' % (repr(e), self.getAvatarIdFromSender()))
        print(trace)

        self.webhookManager.logServerException(e, avatarId, accountId)

        # Python 2 Vs 3 compatibility
        if not sys.version_info >= (3, 0):
            sys.exc_clear()

    def readerPollOnce(self):
        try:
            return AstronInternalRepository.readerPollOnce(self)
        except SystemExit, KeyboardInterrupt:
            raise
        except Exception as e:

            if config.GetBool('boot-on-error', True):
                avatar = self.doId2do.get(self.getAvatarIdFromSender(), None)

                if avatar:
                    self.kickChannel(self.getMsgSender(), reason=153)

            self.logException(e)

        return 1
