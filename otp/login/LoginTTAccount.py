# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.login.LoginTTAccount
import LoginBase
import TTAccount
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.MsgTypes import *
from direct.distributed.PyDatagram import PyDatagram
from pandac.PandaModules import *


class LoginTTAccount(LoginBase.LoginBase, TTAccount.TTAccount):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('LoginTTAcct')

    def __init__(self, cr):
        LoginBase.LoginBase.__init__(self, cr)
        TTAccount.TTAccount.__init__(self, cr)

    def supportsRelogin(self):
        return 1

    def sendLoginMsg(self):
        cr = self.cr
        datagram = PyDatagram()
        datagram.addUint16(CLIENT_LOGIN_2)
        self.__addPlayToken(datagram)
        datagram.addString(cr.serverVersion)
        datagram.addUint32(cr.hashVal)
        self.__addTokenType(datagram)
        datagram.addString(cr.validateDownload)
        datagram.addString(cr.wantMagicWords)
        cr.send(datagram)

    def resendPlayToken(self):
        cr = self.cr
        datagram = PyDatagram()
        datagram.addUint16(CLIENT_SET_SECURITY)
        self.__addPlayToken(datagram)
        self.__addTokenType(datagram)
        cr.send(datagram)

    def __addPlayToken(self, datagram):
        self.playToken = self.playToken.strip()
        datagram.addString(self.playToken)

    def __addTokenType(self, datagram):
        if self.playTokenIsEncrypted:
            datagram.addInt32(CLIENT_LOGIN_2_PLAY_TOKEN)
        else:
            datagram.addInt32(CLIENT_LOGIN_2_PLAY_TOKEN)

    def getErrorCode(self):
        return self.response.getInt('errorCode', 0)

    def needToSetParentPassword(self):
        return self.response.getBool('secretsPasswordNotSet', 0)
# okay decompiling .\otp\login\LoginTTAccount.pyc
