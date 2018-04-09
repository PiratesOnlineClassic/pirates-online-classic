# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.login.LoginWebPlayTokenAccount
import LoginTTAccount
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *


class LoginWebPlayTokenAccount(LoginTTAccount.LoginTTAccount):
    
    notify = DirectNotifyGlobal.directNotify.newCategory('LoginWebPlayTokenAccount')

    def supportsRelogin(self):
        return 0

    def createAccount(self, loginName, password, data):
        pass

    def authorize(self, loginName, password):
        self.playToken = password
        self.playTokenIsEncrypted = 1
        self.freeTimeExpires = -1
        self.cr.freeTimeExpiresAt = self.freeTimeExpires

    def createBilling(self, loginName, password, data):
        pass

    def setParentPassword(self, loginName, password, parentPassword):
        pass

    def supportsParentPassword(self):
        return 1

    def changePassword(self, loginName, password, newPassword):
        pass

    def requestPwdReminder(self, email=None, acctName=None):
        pass

    def cancelAccount(self, loginName, password):
        pass

    def getAccountData(self, loginName, password):
        pass

    def getErrorCode(self):
        if not self.has_key('response'):
            return 0
        return self.response.getInt('errorCode', 0)

    def needToSetParentPassword(self):
        return 0
# okay decompiling .\otp\login\LoginWebPlayTokenAccount.pyc
