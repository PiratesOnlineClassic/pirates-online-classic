import traceback
import sys

from panda3d.core import *

from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.AstronInternalRepository import AstronInternalRepository

from otp.distributed.OtpDoGlobals import *


class OTPInternalRepository(AstronInternalRepository):
    notify = directNotify.newCategory('OTPInternalRepository')

    def __init__(self, baseChannel, serverId=None, dcFileNames = None, dcSuffix='AI',
        connectMethod=None, threadedNet=None):

        self.notify.setInfo(True)
        AstronInternalRepository.__init__(self, baseChannel, serverId, dcFileNames,
            dcSuffix, connectMethod, threadedNet)

        self._netMessageCounter = 0

    def _registerInternalNetMessage(self, message):
        self.notify.debug('Registering netMessage (%s) (%d)' % (message, self._netMessageCounter))
        self.netMessenger.register(self._netMessageCounter, message)
        self._netMessageCounter += 1

    def _registerNetMessages(self):
        self.notify.info('Registering NetMessages')

        self._registerInternalNetMessage('UberDOGSettingsRequest')

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

    def clientAddInterest(self, clientChannel, interestId, parentId, zoneId, sendInterestDone=True):
        dg = PyDatagram()
        dg.addServerHeader(clientChannel, self.ourChannel, CLIENTAGENT_ADD_INTEREST)
        dg.addUint16(interestId)
        dg.addUint32(parentId)
        dg.addUint32(zoneId)
        dg.addBool(sendInterestDone)
        self.send(dg)

    def clientAddInterestMultiple(self, clientChannel, interestId, parentId, zoneList, sendInterestDone=True):
        dg = PyDatagram()
        dg.addServerHeader(clientChannel, self.ourChannel, CLIENTAGENT_ADD_INTEREST_MULTIPLE)
        dg.addUint16(interestId)
        dg.addUint32(parentId)
        dg.addUint16(len(zoneList))
        for zoneId in zoneList:
            dg.addUint32(zoneId)

        dg.addBool(sendInterestDone)
        self.send(dg)

    def clientRemoveInterest(self, clientChannel, interestId, sendInterestDone=True):
        dg = PyDatagram()
        dg.addServerHeader(clientChannel, self.ourChannel, CLIENTAGENT_REMOVE_INTEREST)
        dg.addUint16(interestId)
        dg.addBool(sendInterestDone)
        self.send(dg)

    def sendSetObjectLocation(self, doId, parentId, zoneId):
        dg = PyDatagram()
        dg.addServerHeader(doId, self.ourChannel, STATESERVER_OBJECT_SET_LOCATION)
        dg.addUint32(parentId)
        dg.addUint32(zoneId)
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

    #def logException(self, e):
    #    pass

    #def readerPollOnce(self):
    #    try:
    #        return AstronInternalRepository.readerPollOnce(self)
    #    except SystemExit, KeyboardInterrupt:
    #        raise
    #    except Exception as e:
    #
    #        if config.GetBool('boot-on-error', True):
    #            avatar = self.doId2do.get(self.getAvatarIdFromSender(), None)
    #
    #            if avatar:
    #                self.kickChannel(self.getMsgSender(), reason=153)
    #
    #        self.logException(e)
    #
    #    return 1
