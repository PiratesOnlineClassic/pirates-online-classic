from direct.showbase import GarbageReport
from otp.avatar import DistributedAvatarAI
from otp.avatar import PlayerBase
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from otp.chat import ChatFilter
from otp.chat.ChatRelayAI import ChatRelayAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.PyDatagram import PyDatagram
from otp.distributed.MsgTypes import CLIENTAGENT_EJECT
from otp.distributed import OtpDoGlobals
from otp.ai.MagicWordGlobal import *


class DistributedPlayerAI(DistributedAvatarAI.DistributedAvatarAI, PlayerBase.PlayerBase, ChatRelayAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerAI')

    # Shared by every avatar on the district, since a whisper is handled by
    # the AI of the avatar receiving it rather than the one sending it.
    chatFlood = ChatFilter.ChatFlood()

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
        self.chatFlood.clear(self.doId)
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

    # Chat:
    #
    # Typed chat and whispers are not broadcast by the State Server; the
    # client sends them to us and we relay them once they've been checked,
    # which is what the original game server did when it scrubbed chat.

    def _getChatSender(self, fieldName):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId != self.doId:
            self.chatViolation('%s sent on avatar %d' % (fieldName, self.doId))
            return 0

        return avatarId

    def d_setChat(self, chatString, chatFlags, senderChannel=None):
        self.sendUpdateToLocation('setChat', [chatString, chatFlags, self.DISLid], senderChannel)

    def setChat(self, chatString, chatFlags, DISLid):
        avatarId = self._getChatSender('setChat')
        if not avatarId:
            return

        message = self._cleanTypedChat(avatarId, 'setChat', chatString)
        if message is None:
            return

        self.air.writeServerEvent('chat-said', avId=avatarId, chatFlags=chatFlags, message=message)
        self.d_setChat(message, ChatFilter.cleanChatFlags(chatFlags), self.air.getMsgSender())

    def d_setWLChat(self, chatString, chatFlags, senderChannel=None):
        self.sendUpdateToLocation('setWLChat', [chatString, chatFlags, self.DISLid], senderChannel)

    def setWLChat(self, chatString, chatFlags, DISLid):
        avatarId = self._getChatSender('setWLChat')
        if not avatarId:
            return

        message = self._cleanTypedChat(avatarId, 'setWLChat', chatString)
        if message is None:
            return

        # The client only sends whitelisted words, and the avatars receiving
        # whitelist chat display it without filtering it again.
        message = ChatFilter.filterWhiteList(message)
        self.air.writeServerEvent('chat-said-wl', avId=avatarId, chatFlags=chatFlags, message=message)
        self.d_setWLChat(message, ChatFilter.cleanChatFlags(chatFlags), self.air.getMsgSender())

    # SpeedChat comes to us too rather than being broadcast, so that a phrase
    # the menu doesn't have never reaches the other clients (they look the
    # phrase up when they log it).

    def _getSpeedChatSender(self, fieldName, isValid, description):
        avatarId = self._getChatSender(fieldName)
        if not avatarId:
            return 0

        if not isValid:
            self.chatViolation('invalid %s' % description, eject=True)
            return 0

        if self._isFlooding(avatarId):
            return 0

        return avatarId

    def d_setSC(self, msgIndex, senderChannel=None):
        self.sendUpdateToLocation('setSC', [msgIndex], senderChannel)

    def setSC(self, msgIndex):
        if self._getSpeedChatSender('setSC', ChatFilter.isValidSpeedChat(msgIndex),
                                    'SpeedChat index %d' % msgIndex):
            self.d_setSC(msgIndex, self.air.getMsgSender())

    def d_setSCCustom(self, msgIndex, senderChannel=None):
        self.sendUpdateToLocation('setSCCustom', [msgIndex], senderChannel)

    def setSCCustom(self, msgIndex):
        if self._getSpeedChatSender('setSCCustom', ChatFilter.isValidSpeedChatCustom(msgIndex),
                                    'SpeedChat custom index %d' % msgIndex):
            self.d_setSCCustom(msgIndex, self.air.getMsgSender())

    # Whispers come to the AI of the avatar being whispered, from whoever
    # sent them, so all we know about the sender is their channel.

    def _getWhisperSender(self, fieldName, fromId):
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId:
            return 0

        if fromId != avatarId:
            self.chatViolation('%s to %d claiming to be from %d' % (fieldName, self.doId, fromId))
            return 0

        if avatarId == self.doId or self._isFlooding(avatarId):
            return 0

        return avatarId

    def setWhisperFrom(self, fromId, chatString, senderDISLid):
        avatarId = self._getWhisperSender('setWhisperFrom', fromId)
        if not avatarId:
            return

        message = ChatFilter.cleanMessage(chatString)
        if message is None:
            return

        self.air.writeServerEvent('whisper-said', avId=avatarId, toId=self.doId, message=message)
        self.sendUpdateToAvatarId(self.doId, 'setWhisperFrom', [avatarId, message, senderDISLid])

    def setWhisperWLFrom(self, fromId, chatString, senderDISLid):
        avatarId = self._getWhisperSender('setWhisperWLFrom', fromId)
        if not avatarId:
            return

        message = ChatFilter.cleanMessage(chatString)
        if message is None:
            return

        message = ChatFilter.filterWhiteList(message)
        self.air.writeServerEvent('whisper-said-wl', avId=avatarId, toId=self.doId, message=message)
        self.sendUpdateToAvatarId(self.doId, 'setWhisperWLFrom', [avatarId, message, senderDISLid])

    def setWhisperSCFrom(self, fromId, msgIndex):
        avatarId = self._getWhisperSender('setWhisperSCFrom', fromId)
        if avatarId and ChatFilter.isValidSpeedChat(msgIndex):
            self.sendUpdateToAvatarId(self.doId, 'setWhisperSCFrom', [avatarId, msgIndex])

    def setWhisperSCCustomFrom(self, fromId, msgIndex):
        avatarId = self._getWhisperSender('setWhisperSCCustomFrom', fromId)
        if avatarId and ChatFilter.isValidSpeedChatCustom(msgIndex):
            self.sendUpdateToAvatarId(self.doId, 'setWhisperSCCustomFrom', [avatarId, msgIndex])

    def setWhisperSCEmoteFrom(self, fromId, emoteId):
        avatarId = self._getWhisperSender('setWhisperSCEmoteFrom', fromId)
        if avatarId and ChatFilter.isValidSpeedChatEmote(emoteId):
            self.sendUpdateToAvatarId(self.doId, 'setWhisperSCEmoteFrom', [avatarId, emoteId])

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

    base.air.systemMessage(message)


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def sysadmin(message):
    """
    Send a system message to the whole district, prefixed with 'ADMIN:'.
    """

    text = 'ADMIN: ' + message
    base.air.systemMessage(text)
    return "Sent system message '%s' to all players in the district." % text


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def update(minutes):
    """
    Initiate the maintenance message sequence. It will last for the specified
    amount of <minutes>.
    """

    def disconnect(task):
        dg = PyDatagram()
        dg.addServerHeader(OtpDoGlobals.OTP_CHANNEL_ALL_CLIENTS, base.air.ourChannel, CLIENTAGENT_EJECT)
        dg.addUint16(154)
        dg.addString('Pirates Online Classic is now closed for maintenance.')
        base.air.send(dg)
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
