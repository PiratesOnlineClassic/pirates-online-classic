import string
import time

from direct.showbase import PythonUtil
from direct.task import Task
from otp.avatar import Avatar, DistributedAvatar, PlayerBase
from otp.chat import ChatAssistant, ChatGarbler
from otp.margins.WhisperPopup import WhisperPopup
from otp.otpbase import OTPLocalizer
from otp.nametag.NametagConstants import CFQuicktalker, CFPageButton, CFQuitButton, CFSpeech, CFThought, CFTimeout
from otp.speedchat import SCDecoders
from panda3d.core import *


class DistributedPlayer(DistributedAvatar.DistributedAvatar, PlayerBase.PlayerBase):
    __module__ = __name__
    TeleportFailureTimeout = 60.0
    chatGarbler = ChatGarbler.ChatGarbler()

    def __init__(self, cr):
        try:
            self.DistributedPlayer_initialized
        except:
            self.DistributedPlayer_initialized = 1
            DistributedAvatar.DistributedAvatar.__init__(self, cr)
            self.__teleportAvailable = 0
            self.inventory = None
            self.experience = None
            self.friendsList = []
            self.oldFriendsList = None
            self.timeFriendsListChanged = None
            self.ignoreList = []
            self.lastFailedTeleportMessage = {}
            self._districtWeAreGeneratedOn = None
            self.DISLname = ''
            self.DISLid = 0
            self.autoRun = 0
            self.whiteListEnabled = base.config.GetBool('whitelist-chat-enabled', 1)

        return

    def disable(self):
        DistributedAvatar.DistributedAvatar.disable(self)

    def delete(self):
        try:
            self.DistributedPlayer_deleted
        except:
            self.DistributedPlayer_deleted = 1
            del self.experience
            if self.inventory:
                self.inventory.unload()
            del self.inventory
            DistributedAvatar.DistributedAvatar.delete(self)

    def generate(self):
        DistributedAvatar.DistributedAvatar.generate(self)

    def isGeneratedOnDistrict(self, districtId=None):
        if districtId is None:
            return self._districtWeAreGeneratedOn is not None
        else:
            return self._districtWeAreGeneratedOn == districtId
        return

    def getArrivedOnDistrictEvent(self, districtId=None):
        if districtId is None:
            return 'arrivedOnDistrict'
        else:
            return 'arrivedOnDistrict-%s' % districtId
        return

    def arrivedOnDistrict(self, districtId):
        self._districtWeAreGeneratedOn = districtId
        messenger.send(self.getArrivedOnDistrictEvent(districtId))
        messenger.send(self.getArrivedOnDistrictEvent())

    def setLeftDistrict(self):
        self._districtWeAreGeneratedOn = None
        return

    def hasParentingRules(self):
        if self is localAvatar:
            return True

    def setAccountName(self, accountName):
        self.accountName = accountName

    def whisperTo(self, chatString, sendToId):
        messenger.send('wakeup')
        self.sendUpdate('setWhisperFrom', [self.doId, chatString, 0], sendToId)

    def setWhisperFrom(self, fromId, chatString, senderDISLid):
        if fromId == 0:
            return
        if fromId == self.doId:
            return
        handle = base.cr.identifyAvatar(fromId)
        if handle == None:
            return
        if base.cr.avatarFriendsManager.checkIgnored(fromId):
            self.d_setWhisperIgnored(fromId)
            return
        if fromId in self.ignoreList:
            self.d_setWhisperIgnored(fromId)
            return
        chatString = base.chatAssistant.whiteListFilterMessage(chatString)
        if base.localAvatar.garbleChat and not handle.isUnderstandable():
            chatString = self.chatGarbler.garble(self, chatString)
        self.displayWhisper(fromId, chatString, WhisperPopup.WTNormal)
        base.chatAssistant.receiveAvatarWhisperTypedChat(chatString, fromId)
        return

    def whisperWLTo(self, chatString, sendToId):
        messenger.send('wakeup')
        self.sendUpdate('setWhisperWLFrom', [self.doId, chatString, 0], sendToId)

    def setWhisperWLFrom(self, fromId, chatString, senderDISLid):
        if fromId == 0:
            return
        if fromId == self.doId:
            return
        if not self.whiteListEnabled:
            return
        handle = base.cr.identifyAvatar(fromId)
        if handle == None:
            return
        if base.cr.avatarFriendsManager.checkIgnored(fromId):
            self.d_setWhisperIgnored(fromId)
            return
        if fromId in self.ignoreList:
            self.d_setWhisperIgnored(fromId)
            return
        self.displayWhisper(fromId, chatString, WhisperPopup.WTNormal)
        base.chatAssistant.receiveAvatarWhisperWLChat(chatString, fromId)
        return

    def setSystemMessage(self, aboutId, chatString, whisperType=WhisperPopup.WTSystem):
        self.displayWhisper(aboutId, chatString, whisperType)

    def displayWhisper(self, fromId, chatString, whisperType):
        print 'Whisper type %s from %s: %s' % (whisperType, fromId, chatString)

    def displayWhisperPlayer(self, playerId, chatString, whisperType):
        print 'Whisper type %s from %s: %s' % (whisperType, playerId, chatString)

    def whisperSCTo(self, msgIndex, sendToId, toPlayer):
        if toPlayer:
            base.cr.playerFriendsManager.sendSCWhisper(sendToId, msgIndex)
        else:
            messenger.send('wakeup')
            self.sendUpdate('setWhisperSCFrom', [self.doId, msgIndex], sendToId)

    def setWhisperSCFrom(self, fromId, msgIndex):
        handle = base.cr.identifyAvatar(fromId)
        if handle == None:
            return
        if base.cr.avatarFriendsManager.checkIgnored(fromId):
            self.d_setWhisperIgnored(fromId)
            return
        if fromId in self.ignoreList:
            self.d_setWhisperIgnored(fromId)
            return
        chatString = SCDecoders.decodeSCStaticTextMsg(msgIndex)
        if chatString:
            self.displayWhisper(fromId, chatString, WhisperPopup.WTQuickTalker)
            base.chatAssistant.receiveAvatarWhisperSpeedChat(ChatAssistant.SPEEDCHAT_NORMAL, msgIndex, fromId)
        return

    def whisperSCCustomTo(self, msgIndex, sendToId, toPlayer):
        if toPlayer:
            base.cr.playerFriendsManager.sendSCCustomWhisper(sendToId, msgIndex)
            return
        messenger.send('wakeup')
        self.sendUpdate('setWhisperSCCustomFrom', [self.doId, msgIndex], sendToId)

    def setWhisperSCCustomFrom(self, fromId, msgIndex):
        handle = base.cr.identifyAvatar(fromId)
        if handle == None:
            return
        if base.cr.avatarFriendsManager.checkIgnored(fromId):
            self.d_setWhisperIgnored(fromId)
            return
        if fromId in self.ignoreList:
            self.d_setWhisperIgnored(fromId)
            return
        chatString = SCDecoders.decodeSCCustomMsg(msgIndex)
        if chatString:
            self.displayWhisper(fromId, chatString, WhisperPopup.WTQuickTalker)
            base.chatAssistant.receiveAvatarWhisperSpeedChat(ChatAssistant.SPEEDCHAT_CUSTOM, msgIndex, fromId)
        return

    def whisperSCEmoteTo(self, emoteId, sendToId, toPlayer):
        print 'whisperSCEmoteTo %s %s %s' % (emoteId, sendToId, toPlayer)
        if toPlayer:
            base.cr.playerFriendsManager.sendSCEmoteWhisper(sendToId, emoteId)
            return
        messenger.send('wakeup')
        self.sendUpdate('setWhisperSCEmoteFrom', [self.doId, emoteId], sendToId)

    def setWhisperSCEmoteFrom(self, fromId, emoteId):
        handle = base.cr.identifyAvatar(fromId)
        if handle == None:
            return
        if base.cr.avatarFriendsManager.checkIgnored(fromId):
            self.d_setWhisperIgnored(fromId)
            return
        chatString = SCDecoders.decodeSCEmoteWhisperMsg(emoteId, handle.getName())
        if chatString:
            self.displayWhisper(fromId, chatString, WhisperPopup.WTEmote)
            base.chatAssistant.receiveAvatarWhisperSpeedChat(ChatAssistant.SPEEDCHAT_EMOTE, emoteId, fromId)
        return

    def d_setWhisperIgnored(self, sendToId):
        pass

    def setChatAbsolute(self, chatString, chatFlags, dialogue=None, interrupt=1, quiet=0):
        DistributedAvatar.DistributedAvatar.setChatAbsolute(self, chatString, chatFlags, dialogue, interrupt)
        if not quiet:
            base.chatAssistant.receiveAvatarOpenTypedChat(chatString, chatFlags, self.doId)

    def b_setChat(self, chatString, chatFlags):
        if self.cr.wantMagicWords and len(chatString) > 0 and chatString[0] == '~':
            messenger.send('magicWord', [chatString])
        else:
            if base.config.GetBool('want-chatfilter-hacks', 0):
                if base.config.GetBool('want-chatfilter-drop-offending', 0):
                    if badwordpy.test(chatString):
                        return
                else:
                    chatString = badwordpy.scrub(chatString)
            messenger.send('wakeup')
            self.setChatAbsolute(chatString, chatFlags)
            self.d_setChat(chatString, chatFlags)

    def b_setWLChat(self, chatString, chatFlags):
        messenger.send('wakeup')
        self.setChatAbsolute(chatString, chatFlags)
        self.d_setWLChat(chatString, chatFlags)

    def d_setChat(self, chatString, chatFlags):
        self.sendUpdate('setChat', [chatString, chatFlags, 0])

    def d_setWLChat(self, chatString, chatFlags):
        self.sendUpdate('setWLChat', [chatString, chatFlags, 0])

    def setChat(self, chatString, chatFlags, DISLid):
        chatString = base.chatAssistant.whiteListFilterMessage(chatString)
        if base.cr.avatarFriendsManager.checkIgnored(self.doId):
            return
        if base.localAvatar.garbleChat and not self.isUnderstandable():
            chatString = self.chatGarbler.garble(self, chatString)
        chatFlags &= ~(CFQuicktalker | CFPageButton | CFQuitButton)
        if chatFlags & CFThought:
            chatFlags &= ~(CFSpeech | CFTimeout)
        else:
            chatFlags |= CFSpeech | CFTimeout
        self.setChatAbsolute(chatString, chatFlags)

    def setWLChat(self, chatString, chatFlags, DISLid):
        if base.cr.avatarFriendsManager.checkIgnored(self.doId):
            return
        if self.doId in base.localAvatar.ignoreList:
            return
        if not self.whiteListEnabled:
            return
        chatFlags &= ~(CFQuicktalker | CFPageButton | CFQuitButton)
        if chatFlags & CFThought:
            chatFlags &= ~(CFSpeech | CFTimeout)
        else:
            chatFlags |= CFSpeech | CFTimeout
        self.setChatAbsolute(chatString, chatFlags)

    def b_setSC(self, msgIndex):
        self.setSC(msgIndex)
        self.d_setSC(msgIndex)

    def d_setSC(self, msgIndex):
        messenger.send('wakeup')
        self.sendUpdate('setSC', [msgIndex])

    def setSC(self, msgIndex):
        if base.cr.avatarFriendsManager.checkIgnored(self.doId):
            return
        if self.doId in base.localAvatar.ignoreList:
            return
        chatString = SCDecoders.decodeSCStaticTextMsg(msgIndex)
        if chatString:
            self.setChatAbsolute(chatString, CFSpeech | CFQuicktalker | CFTimeout, quiet=1)
        base.chatAssistant.receiveAvatarOpenSpeedChat(ChatAssistant.SPEEDCHAT_NORMAL, msgIndex, self.doId)

    def b_setSCCustom(self, msgIndex):
        self.setSCCustom(msgIndex)
        self.d_setSCCustom(msgIndex)

    def d_setSCCustom(self, msgIndex):
        messenger.send('wakeup')
        self.sendUpdate('setSCCustom', [msgIndex])

    def setSCCustom(self, msgIndex):
        if base.cr.avatarFriendsManager.checkIgnored(self.doId):
            return
        if self.doId in base.localAvatar.ignoreList:
            return
        chatString = SCDecoders.decodeSCCustomMsg(msgIndex)
        if chatString:
            self.setChatAbsolute(chatString, CFSpeech | CFQuicktalker | CFTimeout)
        base.chatAssistant.receiveAvatarOpenSpeedChat(ChatAssistant.SPEEDCHAT_CUSTOM, msgIndex, self.doId)

    def b_setSCEmote(self, emoteId):
        self.b_setEmoteState(emoteId, animMultiplier=self.animMultiplier)

    def d_friendsNotify(self, avId, status):
        self.sendUpdate('friendsNotify', [avId, status])

    def friendsNotify(self, avId, status):
        avatar = base.cr.identifyFriend(avId)
        if avatar != None:
            if status == 1:
                self.setSystemMessage(avId, OTPLocalizer.WhisperNoLongerFriend % avatar.getName())
            elif status == 2:
                self.setSystemMessage(avId, OTPLocalizer.WhisperNowSpecialFriend % avatar.getName())
        return

    def d_teleportQuery(self, requesterId, sendToId=None):
        self.sendUpdate('teleportQuery', [requesterId], sendToId)

    def teleportQuery(self, requesterId):
        avatar = base.cr.playerFriendsManager.identifyFriend(requesterId)
        if avatar != None:
            if base.cr.avatarFriendsManager.checkIgnored(requesterId):
                self.d_teleportResponse(self.doId, 2, 0, 0, 0, sendToId=requesterId)
                return
            if requesterId in self.ignoreList:
                self.d_teleportResponse(self.doId, 2, 0, 0, 0, sendToId=requesterId)
                return
            if self.__teleportAvailable and not self.ghostMode:
                self.setSystemMessage(requesterId, OTPLocalizer.WhisperComingToVisit % avatar.getName())
                messenger.send('teleportQuery', [avatar, self])
                return
            if self.failedTeleportMessageOk(requesterId):
                self.setSystemMessage(requesterId, OTPLocalizer.WhisperFailedVisit % avatar.getName())
        self.d_teleportResponse(self.doId, 0, 0, 0, 0, sendToId=requesterId)
        return

    def failedTeleportMessageOk(self, fromId):
        now = globalClock.getFrameTime()
        lastTime = self.lastFailedTeleportMessage.get(fromId, None)
        if lastTime != None:
            elapsed = now - lastTime
            if elapsed < self.TeleportFailureTimeout:
                return 0
        self.lastFailedTeleportMessage[fromId] = now
        return 1

    def d_teleportResponse(self, avId, available, shardId, hoodId, zoneId, sendToId=None):
        self.sendUpdate('teleportResponse', [avId, available, shardId, hoodId, zoneId], sendToId)

    def teleportResponse(self, avId, available, shardId, hoodId, zoneId):
        messenger.send('teleportResponse', [avId, available, shardId, hoodId, zoneId])

    def d_teleportGiveup(self, requesterId, sendToId=None):
        self.sendUpdate('teleportGiveup', [requesterId], sendToId)

    def teleportGiveup(self, requesterId):
        avatar = base.cr.identifyAvatar(requesterId)
        if avatar != None:
            self.setSystemMessage(requesterId, OTPLocalizer.WhisperGiveupVisit % avatar.getName())
        return

    def b_teleportGreeting(self, avId):
        self.d_teleportGreeting(avId)
        self.teleportGreeting(avId)

    def d_teleportGreeting(self, avId):
        self.sendUpdate('teleportGreeting', [avId])

    def teleportGreeting(self, avId):
        avatar = base.cr.getDo(avId)
        if avatar is not None:
            self.setChatAbsolute(OTPLocalizer.TeleportGreeting % avatar.getName(), CFSpeech | CFTimeout)
        return

    def setTeleportAvailable(self, available):
        self.__teleportAvailable = available

    def getTeleportAvailable(self):
        return self.__teleportAvailable

    def getFriendsList(self):
        return self.friendsList

    def setFriendsList(self, friendsList):
        self.oldFriendsList = self.friendsList
        self.friendsList = friendsList
        self.timeFriendsListChanged = globalClock.getFrameTime()
        messenger.send('friendsListChanged')
        Avatar.reconsiderAllUnderstandable()

    def setDISLname(self, name):
        self.DISLname = name

    def setDISLid(self, id):
        self.DISLid = id

    def setAutoRun(self, value):
        self.autoRun = value

    def getAutoRun(self):
        return self.autoRun
# okay decompiling .\otp\avatar\DistributedPlayer.pyc
