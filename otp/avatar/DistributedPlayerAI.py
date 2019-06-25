from direct.showbase import GarbageReport
from otp.avatar import DistributedAvatarAI
from otp.avatar import PlayerBase
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import CLIENTAGENT_EJECT
from otp.distributed import OtpDoGlobals
from otp.ai.MagicWordGlobal import *


class DistributedPlayerAI(DistributedAvatarAI.DistributedAvatarAI, PlayerBase.PlayerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerAI')

    def __init__(self, air):
        DistributedAvatarAI.DistributedAvatarAI.__init__(self, air)
        self.friendsList = []
        self.DISLname = ''
        self.DISLid = 0
        self.adminAccess = 0

    def announceGenerate(self):
        DistributedAvatarAI.DistributedAvatarAI.announceGenerate(self)
        self._doPlayerEnter()

    def _announceArrival(self):
        self.sendUpdate('arrivedOnDistrict', [self.air.districtId])

    def _announceExit(self):
        self.sendUpdate('arrivedOnDistrict', [0])

    def _sendExitServerEvent(self):
        self.air.writeServerEvent('avatarExit', self.doId, '')

    def delete(self):
        self._doPlayerExit()
        if __dev__:
            GarbageReport.checkForGarbageLeaks()

        DistributedAvatarAI.DistributedAvatarAI.delete(self)

    def isPlayerControlled(self):
        return True

    def setLocation(self, parentId, zoneId):
        DistributedAvatarAI.DistributedAvatarAI.setLocation(self, parentId, zoneId)

        if self.isPlayerControlled():
            if not self.air._isValidPlayerLocation(parentId, zoneId):
                self.notify.info('booting player %s for doing setLocation to (%s, %s)' % (
                    self.doId, parentId, zoneId))

                self.air.writeServerEvent('suspicious', avId=self.doId, issue='invalid setLocation: (%s, %s)' % (
                    parentId, zoneId))

                self.requestDelete()

    def _doPlayerEnter(self):
        self.incrementPopulation()
        self._announceArrival()

    def _doPlayerExit(self):
        self._announceExit()
        self.decrementPopulation()

    def incrementPopulation(self):
        self.air.incrementPopulation()

    def decrementPopulation(self):
        self.air.decrementPopulation()

    def b_setChat(self, chatString, chatFlags):
        self.setChat(chatString, chatFlags)
        self.d_setChat(chatString, chatFlags)

    def d_setChat(self, chatString, chatFlags):
        self.sendUpdate('setChat', [chatString, chatFlags])

    def setChat(self, chatString, chatFlags):
        pass

    def d_setSystemMessage(self, aboutId, chatString):
        self.sendUpdate('setSystemMessage', [aboutId, chatString])

    def d_setCommonChatFlags(self, flags):
        self.sendUpdate('setCommonChatFlags', [flags])

    def setCommonChatFlags(self, flags):
        pass

    def d_friendsNotify(self, avId, status):
        self.sendUpdate('friendsNotify', [avId, status])

    def friendsNotify(self, avId, status):
        pass

    def setAccountName(self, accountName):
        self.accountName = accountName

    def getAccountName(self):
        return self.accountName

    def setDISLid(self, id):
        self.DISLid = id

    def getDISLid(self):
        return self.DISLid

    def d_setFriendsList(self, friendsList):
        self.sendUpdate('setFriendsList', [friendsList])

    def setFriendsList(self, friendsList):
        self.friendsList = friendsList
        self.notify.debug('setting friends list to %s' % self.friendsList)

    def getFriendsList(self):
        return self.friendsList

    def setAdminAccess(self, access):
        self.adminAccess = access

    def d_setAdminAccess(self, access):
        self.sendUpdate('setAdminAccess', [access])

    def b_setAdminAccess(self, access):
        self.setAdminAccess(access)
        self.d_setAdminAccess(access)

    def getAdminAccess(self):
        return self.adminAccess

    def extendFriendsList(self, friendId, friendCode):
        for i in range(len(self.friendsList)):
            friendPair = self.friendsList[i]
            if friendPair[0] == friendId:
                self.friendsList[i] = (friendId, friendCode)
                return

        self.friendsList.append((friendId, friendCode))


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def system(message):
    """
    Send a system message to the whole district
    """

    simbase.air.systemMessage(message)


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def sysadmin(message):
    """
    Send a system message to the whole district, prefixed with 'ADMIN:'.
    """

    text = 'ADMIN: ' + message
    simbase.air.systemMessage(text)
    return "Sent system message '%s' to all players in the district." % text


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def update(minutes):
    """
    Initiate the maintenance message sequence. It will last for the specified
    amount of <minutes>.
    """

    def disconnect(task):
        dg = PyDatagram()
        dg.addServerHeader(10, simbase.air.ourChannel, CLIENTAGENT_EJECT)
        dg.addUint16(154)
        dg.addString('Pirates Online Classic is now closed for maintenance.')
        simbase.air.send(dg)
        return task.done

    def countdown(minutes):
        if minutes > 0:
            system(OTPLocalizer.CRMaintenanceCountdownMessage % minutes)
        else:
            system(OTPLocalizer.CRMaintenanceMessage)
            taskMgr.doMethodLater(10, disconnect, 'maintenance-disconnection')
        if minutes <= 5:
            next = 60
            minutes -= 1
        elif minutes % 5:
            next = 60 * (minutes % 5)
            minutes -= minutes % 5
        else:
            next = 300
            minutes -= 5
        if minutes >= 0:
            taskMgr.doMethodLater(next, countdown, 'maintenance-task',
                                  extraArgs=[minutes])

    countdown(minutes)
