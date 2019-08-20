from pandac.PandaModules import *
from direct.distributed.MsgTypes import *
from direct.directnotify import DirectNotifyGlobal
import LoginBase
import TTAccount
from direct.distributed.PyDatagram import PyDatagram

class LoginTTAccount(LoginBase.LoginBase, TTAccount.TTAccount):
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


