# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.login.LoginGSAccount
from . import LoginBase
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.MsgTypes import *
from direct.distributed.PyDatagram import PyDatagram
from pandac.PandaModules import *


class LoginGSAccount(LoginBase.LoginBase):
    __module__ = __name__

    def __init__(self, cr):
        LoginBase.LoginBase.__init__(self, cr)

    def createAccount(self, loginName, password, data):
        self.loginName = loginName
        self.password = password
        self.createFlag = 1
        self.cr.freeTimeExpiresAt = -1
        self.cr.setIsPaid(1)
        return

    def authorize(self, loginName, password):
        self.loginName = loginName
        self.password = password
        self.createFlag = 0
        self.cr.freeTimeExpiresAt = -1
        self.cr.setIsPaid(1)
        return

    def supportsRelogin(self):
        return 1

    def sendLoginMsg(self):
        cr = self.cr
        datagram = PyDatagram()
        datagram.addUint16(CLIENT_LOGIN)
        datagram.addString(self.loginName)
        if cr.connectMethod != cr.CM_HTTP:
            datagram.addUint32(cr.tcpConn.getAddress().getIp())
        else:
            datagram.addUint32(0)
        datagram.addUint16(5150)
        datagram.addString(cr.serverVersion)
        datagram.addUint32(cr.hashVal)
        datagram.addString(self.password)
        datagram.addBool(self.createFlag)
        datagram.addString(cr.validateDownload)
        datagram.addString(cr.wantMagicWords)
        datagram.addUint32(config.GetInt('fake-DISL-PlayerAccountId', 0))
        cr.send(datagram)

    def resendPlayToken(self):
        pass

    def requestPwdReminder(self, email=None, acctName=None):
        return 0

    def getAccountData(self, loginName, password):
        return 'Unsupported'

    def supportsParentPassword(self):
        return 1

    def authenticateParentPassword(self, loginName, password, parentPassword):
        return (
         password == parentPassword, None)

    def supportsAuthenticateDelete(self):
        return 1

    def authenticateDelete(self, loginName, password):
        return (
         password == self.cr.password, None)

    def enableSecretFriends(self, loginName, password, parentPassword, enable=1):
        return (
         password == parentPassword, None)
# okay decompiling .\otp\login\LoginGSAccount.pyc
