import traceback
import sys

from panda3d.core import *
from direct.distributed.AstronInternalRepository import AstronInternalRepository
from otp.distributed.OtpDoGlobals import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *

class OTPInternalRepository(AstronInternalRepository):

    def __init__(self, baseChannel, serverId=None, dcFileNames = None, dcSuffix='AI', connectMethod=None, threadedNet=None):
        AstronInternalRepository.__init__(self, baseChannel, serverId, dcFileNames, dcSuffix, connectMethod, threadedNet)
        self._netMessageCounter = 0

    def _registerInternalNetMessage(self, message):
        self.netMessenger.register(self._netMessageCounter, message)
        self._netMessageCounter += 1
        
    def _registerNetMessages(self):
        pass # Override me!

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

        senderName =  districtName = self.distributedDistrict.getName() if hasattr(self, 'distributedDistrict') else None
        if not senderName:
            if self.dcSuffix == 'AI':
                senderName = 'AI'
            else:
                senderName = 'UberDOG'
        self.centralLogger.reportException(senderName, trace, False)
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