import string
import sys
import time

from direct.showbase import DirectObject
from otp.otpbase import OTPLocalizer
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from otp.speedchat import SCDecoders
from panda3d.core import *
from otp.chat.ChatGlobals import *
from otp.chat.ChatMessage import ChatMessage
from otp.nametag.NametagConstants import CFSpeech, CFTimeout, CFThought


def isThought(message):
    if len(message) == 0:
        return 0
    elif string.find(message, ThoughtPrefix, 0, len(ThoughtPrefix)) >= 0:
        return 1
    else:
        return 0


def removeThoughtPrefix(message):
    if isThought(message):
        return message[len(ThoughtPrefix):]
    else:
        return message


class ChatAssistant(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('ChatAssistant')
    execChat = base.config.GetBool('exec-chat', 0)

    def __init__(self):
        self.logWhispers = 1
        self.whiteList = None
        self.historyOpen = []

        self.historyReceivedWhisperAvatar = {}
        self.historySentWhisperAvatar = {}
        self.historyReceivedWhisperPlayer = {}
        self.historySentWhisperPlayer = {}
        self.zeroTimeDay = time.time()
        self.zeroTimeGame = globalClock.getRealTime()
        self.useWhiteListFilter = base.config.GetBool(
            'white-list-filter-openchat', 0)
        return

    def clearHistory(self):
        self.historyOpen = []
        self.historyReceivedWhisperAvatar = {}
        self.historySentWhisperAvatar = {}
        self.historyReceivedWhisperPlayer = {}
        self.historySentWhisperPlayer = {}

    def chatTime(self):
        return self.zeroTimeDay + \
            (globalClock.getRealTime() - self.zeroTimeGame)

    def delete(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def getOpenText(self, numLines, startPoint=0):
        return self.historyOpen[startPoint:startPoint + numLines]

    def getSizeOpenText(self):
        return len(self.historyOpen)

    def checkOpenTypedChat(self):
        if base.localAvatar.commonChatFlags & OTPGlobals.CommonChat:
            return True
        return False

    def checkOpenSpeedChat(self):
        return True

    def checkWhisperTypedChatAvatar(self, avatarId):
        remoteAvatar = base.cr.doId2do.get(avatarId)
        if remoteAvatar:
            if remoteAvatar.commonChatFlags & base.localAvatar.commonChatFlags & OTPGlobals.CommonChat:
                return True
        if base.localAvatar.commonChatFlags & OTPGlobals.SuperChat:
            return True
        info = base.cr.playerFriendsManager.findPlayerInfoFromAvId(avatarId)
        if info:
            if info.understandableYesNo:
                return True
        info = base.cr.avatarFriendsManager.getFriendInfo(avatarId)
        if info:
            if info.understandableYesNo:
                return True
        if base.cr.getFriendFlags(avatarId) & OTPGlobals.FriendChat:
            return True
        return False

    def checkWhisperSpeedChatAvatar(self, avatarId):
        return True

    def checkWhisperTypedChatPlayer(self, playerId):
        info = base.cr.playerFriendsManager.getFriendInfo(playerId)
        if info:
            if info.understandableYesNo:
                return True
        return False

    def checkWhisperSpeedChatPlayer(self, playerId):
        if base.cr.playerFriendsManager.isPlayerFriend(playerId):
            return True
        return False

    def receiveGameMessage(self, message):
        error = None
        if not isThought(message):
            self.historyOpen.insert(
                0,
                ChatMessage(self.chatTime(), GAMECHAT, message, None, None,
                            None, 0, 0, 0))
        messenger.send('NewOpenMessage')
        return error

    def receiveSystemMessage(self, message):
        error = None
        if not isThought(message):
            self.historyOpen.insert(
                0,
                ChatMessage(self.chatTime(), SYSTEMCHAT, message, None, None,
                            None, 0, 0, 0))
        messenger.send('NewOpenMessage')
        return error

    def receivePartyMessage(self, message):
        error = None
        if not isThought(message):
            self.historyOpen.insert(
                0,
                ChatMessage(self.chatTime(), PARTYCHAT, message, None, None,
                            None, 0, 0, 0))
        messenger.send('NewOpenMessage')
        return error

    def receiveFriendUpdate(self, friendId, friendName, isOnline):
        if isOnline:
            self.historyOpen.insert(
                0,
                ChatMessage(self.chatTime(), FRIEND_UPDATE,
                            OTPLocalizer.FriendOnline % friendName, None, None,
                            None, 0, 0, 0))
        else:
            self.historyOpen.insert(
                0,
                ChatMessage(self.chatTime(), FRIEND_UPDATE,
                            OTPLocalizer.FriendOffline % friendName, None, None,
                            None, 0, 0, 0))
        messenger.send('NewOpenMessage')
        return

    def receiveCrewUpdate(self, memberId, memberName, isOnline):
        self.receiveGameMessage('OMG')

    def receiveGuildUpdate(self, memberId, memberName, isOnline):
        if base.cr.identifyFriend(memberId) is None:
            if isOnline:
                self.historyOpen.insert(
                    0,
                    ChatMessage(self.chatTime(), GUILD_UPDATE,
                                OTPLocalizer.GuildMemberOnline % memberName,
                                None, None, None, 0, 0, 0))
            else:
                self.historyOpen.insert(
                    0,
                    ChatMessage(self.chatTime(), GUILD_UPDATE,
                                OTPLocalizer.GuildMemberOffline % memberName,
                                None, None, None, 0, 0, 0))
            messenger.send('NewOpenMessage')
        return

    def receiveAvatarOpenTypedChat(self,
                                   message,
                                   chatFlags,
                                   senderId,
                                   name=None):
        if self.useWhiteListFilter:
            message = self.whiteListFilterMessage(message)
        error = None
        if not name and senderId:
            name = self.findName(senderId, 0)
        if not isThought(message):
            self.historyOpen.insert(
                0,
                ChatMessage(self.chatTime(), TYPEDCHAT, message, chatFlags,
                            senderId, name, 0, 0, 0))
        messenger.send('NewOpenMessage')
        return error

    def receiveAvatarOpenWLChat(self, message, chatFlags, senderId, name=None):
        error = None
        if not name and senderId:
            name = self.findName(senderId, 0)
        if not isThought(message):
            self.historyOpen.insert(
                0,
                ChatMessage(self.chatTime(), TYPEDCHAT, message, chatFlags,
                            senderId, name, 0, 0, 0))
        messenger.send('NewOpenMessage')
        return error

    def receiveAvatarOpenSpeedChat(self,
                                   type,
                                   messageIndex,
                                   senderId,
                                   name=None):
        error = None
        if not name and senderId:
            name = self.findName(senderId, 0)
        if senderId == base.localAvatar.doId:
            IAmSender = 1
        else:
            IAmSender = 0
        self.historyOpen.insert(
            0,
            ChatMessage(self.chatTime(), type, messageIndex, None, senderId,
                        name, 0, 0, IAmSender))
        messenger.send('NewOpenMessage')
        return error

    def receiveAvatarWhisperTypedChat(self, message, senderId, name=None):
        if self.useWhiteListFilter:
            return self.receiveAvatarWhisperWLChat(message, senderId, name)
        error = None
        if not name and senderId:
            name = self.findName(senderId, 0)
        if not self.historyReceivedWhisperAvatar.get(senderId):
            self.historyReceivedWhisperAvatar[senderId] = []
        self.historyReceivedWhisperAvatar[senderId].insert(
            0,
            ChatMessage(self.chatTime(), TYPEDCHAT, message, None, senderId,
                        name, 0, 1, 0))
        self.historyOpen.insert(
            0,
            ChatMessage(self.chatTime(), TYPEDCHAT, message, None, senderId,
                        name, 0, 1, 0))
        messenger.send('NewOpenMessage')
        return error

    def receiveAvatarWhisperWLChat(self, message, senderId, name=None):
        error = None
        if not name and senderId:
            name = self.findName(senderId, 0)
        if not self.historyReceivedWhisperAvatar.get(senderId):
            self.historyReceivedWhisperAvatar[senderId] = []
        self.historyReceivedWhisperAvatar[senderId].insert(
            0,
            ChatMessage(self.chatTime(), TYPEDCHAT, message, None, senderId,
                        name, 0, 1, 0))
        self.historyOpen.insert(
            0,
            ChatMessage(self.chatTime(), TYPEDCHAT, message, None, senderId,
                        name, 0, 1, 0))
        messenger.send('NewOpenMessage')
        return error

    def receiveAvatarWhisperSpeedChat(self,
                                      type,
                                      messageIndex,
                                      senderId,
                                      name=None):
        error = None
        if not name and senderId:
            name = self.findName(senderId, 0)
        if not self.historyReceivedWhisperAvatar.get(senderId):
            self.historyReceivedWhisperAvatar[senderId] = []
        self.historyReceivedWhisperAvatar[senderId].insert(
            0,
            ChatMessage(self.chatTime(), type, messageIndex, None, senderId,
                        name, 0, 1, 0))
        self.historyOpen.insert(
            0,
            ChatMessage(self.chatTime(), type, messageIndex, None, senderId,
                        name, 0, 1, 0))
        messenger.send('NewOpenMessage')
        return error

    def receivePlayerOpenTypedChat(self, message, senderId, name=None):
        error = None
        if not name and senderId:
            name = self.findName(senderId, 1)
        if not self.historyOpen.get(senderId):
            self.historyOpen[senderId] = []
        self.historyOpen.insert(
            0,
            ChatMessage(self.chatTime(), TYPEDCHAT, message, None, senderId,
                        name, 1, 0, 0))
        messenger.send('NewOpenMessage')
        return error

    def receivePlayerOpenSpeedChat(self,
                                   type,
                                   messageIndex,
                                   senderId,
                                   name=None):
        error = None
        if not name and senderId:
            name = self.findName(senderId, 1)
        if not self.historyOpen.get(senderId):
            self.historyOpen[senderId] = []
        self.historyOpen.insert(
            0,
            ChatMessage(self.chatTime(), type, messageIndex, None, senderId,
                        name, 1, 0, 0))
        messenger.send('NewOpenMessage')
        return error

    def receivePlayerWhisperTypedChat(self, message, senderId, name=None):
        error = None
        if not name and senderId:
            name = self.findName(senderId, 1)
        if not self.historyReceivedWhisperPlayer.get(senderId):
            self.historyReceivedWhisperPlayer[senderId] = []
        self.historyReceivedWhisperPlayer[senderId].insert(
            0,
            ChatMessage(self.chatTime(), TYPEDCHAT, message, None, senderId,
                        name, 1, 1, 0))
        self.historyOpen.insert(
            0,
            ChatMessage(self.chatTime(), TYPEDCHAT, message, None, senderId,
                        name, 1, 1, 0))
        messenger.send('NewOpenMessage')
        return error

    def receivePlayerWhisperWLChat(self, message, senderId, name=None):
        error = None
        if not name and senderId:
            name = self.findName(senderId, 1)
        if not self.historyReceivedWhisperPlayer.get(senderId):
            self.historyReceivedWhisperPlayer[senderId] = []
        self.historyReceivedWhisperPlayer[senderId].insert(
            0,
            ChatMessage(self.chatTime(), TYPEDCHAT, message, None, senderId,
                        name, 1, 1, 0))
        self.historyOpen.insert(
            0,
            ChatMessage(self.chatTime(), TYPEDCHAT, message, None, senderId,
                        name, 1, 1, 0))
        messenger.send('NewOpenMessage')
        return error

    def receivePlayerWhisperSpeedChat(self,
                                      type,
                                      messageIndex,
                                      senderId,
                                      name=None):
        error = None
        if not name and senderId:
            name = self.findName(senderId, 1)
        if not self.historyReceivedWhisperPlayer.get(senderId):
            self.historyReceivedWhisperPlayer[senderId] = []
        self.historyReceivedWhisperPlayer[senderId].insert(
            0,
            ChatMessage(self.chatTime(), type, messageIndex, None, senderId,
                        name, 1, 1, 0))
        self.historyOpen.insert(
            0,
            ChatMessage(self.chatTime(), type, messageIndex, None, senderId,
                        name, 1, 1, 0))
        messenger.send('NewOpenMessage')
        return error

    def sendAvatarOpenTypedChat(self, message):
        error = None
        if not self.checkOpenTypedChat():
            error = ERROR_NO_OPEN_CHAT
        chatFlags = CFSpeech | CFTimeout
        if base.cr.wantSwitchboardHacks:
            from otp.switchboard import badwordpy
            badwordpy.init('', '')
            message = badwordpy.scrub(message)
        if isThought(message):
            message = removeThoughtPrefix(message)
            chatFlags = CFThought
        if base.cr.wantMagicWords and len(message) > 0 and message[0] == '~':
            messenger.send('magicWord', [message])
            return
        if self.useWhiteListFilter:
            message = self.whiteListFilterMessage(message)
        base.localAvatar.b_setChat(message, chatFlags)
        messenger.send('chatUpdate', [message, chatFlags])
        return error

    def sendAvatarOpenWLChat(self, message):
        error = None
        chatFlags = CFSpeech | CFTimeout
        if isThought(message):
            message = removeThoughtPrefix(message)
            chatFlags = CFThought
        base.localAvatar.b_setWLChat(message, chatFlags)
        messenger.send('chatUpdateWL', [message])
        return error

    def sendAvatarOpenSpeedChat(self, type, messageIndex):
        error = None
        if type == SPEEDCHAT_NORMAL:
            messenger.send(SCChatEvent)
            messenger.send('chatUpdateSC', [messageIndex])
            base.localAvatar.b_setSC(messageIndex)
        elif type == SPEEDCHAT_EMOTE:
            messenger.send('chatUpdateSCEmote', [messageIndex])
            messenger.send(SCEmoteChatEvent)
            base.localAvatar.b_setSCEmote(messageIndex)
        elif type == SPEEDCHAT_CUSTOM:
            messenger.send('chatUpdateSCCustom', [messageIndex])
            messenger.send(SCCustomChatEvent)
            base.localAvatar.b_setSCCustom(messageIndex)
        return error

    def sendAvatarWhisperTypedChat(self, message, receiverId):
        error = None
        if not self.historySentWhisperAvatar.get(receiverId):
            self.historySentWhisperAvatar[receiverId] = []
        handle = base.cr.identifyAvatar(receiverId)
        if handle:
            base.localAvatar.whisperTo(message, receiverId)
            self.historySentWhisperAvatar[receiverId].insert(
                0,
                ChatMessage(self.chatTime(), TYPEDCHAT, message, None,
                            receiverId, self.findName(receiverId), 0, 1, 1))
            if self.logWhispers:
                self.historyOpen.insert(
                    0,
                    ChatMessage(self.chatTime(), TYPEDCHAT, message, None,
                                receiverId, self.findName(receiverId), 0, 1, 1))
                messenger.send('NewOpenMessage')
        else:
            self.historySentWhisperAvatar[receiverId].insert(
                0,
                ChatMessage(self.chatTime(), AVATAR_UNAVAILABLE,
                            OTPLocalizer.WhisperUnavailable, None, receiverId,
                            '', 0, 1, 1))
            if self.logWhispers:
                self.historyOpen.insert(
                    0,
                    ChatMessage(self.chatTime(), AVATAR_UNAVAILABLE,
                                OTPLocalizer.WhisperUnavailable, None,
                                receiverId, '', 0, 1, 1))
                messenger.send('NewOpenMessage')
        return error

    def sendAvatarWhisperWLChat(self, message, receiverId):
        error = None
        if not self.historySentWhisperAvatar.get(receiverId):
            self.historySentWhisperAvatar[receiverId] = []
        base.localAvatar.whisperWLTo(message, receiverId)
        self.historySentWhisperAvatar[receiverId].insert(
            0,
            ChatMessage(self.chatTime(), TYPEDCHAT, message, None, receiverId,
                        self.findName(receiverId), 0, 1, 1))
        if self.logWhispers:
            self.historyOpen.insert(
                0,
                ChatMessage(self.chatTime(), TYPEDCHAT, message, None,
                            receiverId, self.findName(receiverId), 0, 1, 1))
            messenger.send('NewOpenMessage')
        return error

    def sendAvatarWhisperSpeedChat(self, type, messageIndex, receiverId):
        error = None
        if not self.historySentWhisperAvatar.get(receiverId):
            self.historySentWhisperAvatar[receiverId] = []
        if type == SPEEDCHAT_NORMAL:
            base.localAvatar.whisperSCTo(messageIndex, receiverId, 0)
        else:
            if type == SPEEDCHAT_EMOTE:
                base.localAvatar.whisperSCEmoteTo(messageIndex, receiverId, 0)
            elif type == SPEEDCHAT_CUSTOM:
                base.localAvatar.whisperSCCustomTo(messageIndex, receiverId, 0)
            self.historySentWhisperAvatar[receiverId].insert(
                0,
                ChatMessage(self.chatTime(), type, messageIndex, None,
                            receiverId, self.findName(receiverId), 0, 1, 1))
            if self.logWhispers:
                self.historyOpen.insert(
                    0,
                    ChatMessage(self.chatTime(), type, messageIndex, None,
                                receiverId, self.findName(receiverId), 0, 1, 1))
                messenger.send('NewOpenMessage')
        return error

    def sendPlayerOpenTypedChat(self, message):
        error = None
        return error

    def sendPlayerOpenSpeedChat(self, type, messageIndex):
        error = None
        return error

    def sendPlayerWhisperTypedChat(self, message, receiverId):
        error = None
        if not self.historySentWhisperPlayer.get(receiverId):
            self.historySentWhisperPlayer[receiverId] = []
        base.cr.playerFriendsManager.sendWhisper(receiverId, message)
        self.historySentWhisperPlayer[receiverId].insert(
            0,
            ChatMessage(self.chatTime(), TYPEDCHAT, message, None, receiverId,
                        self.findName(receiverId), 1, 1, 1))
        if self.logWhispers:
            self.historyOpen.insert(
                0,
                ChatMessage(self.chatTime(), TYPEDCHAT, message, None,
                            receiverId, self.findName(receiverId, 1), 1, 1, 1))
            messenger.send('NewOpenMessage')
        return error

    def sendPlayerWhisperWLChat(self, message, receiverId):
        error = None
        if not self.historySentWhisperPlayer.get(receiverId):
            self.historySentWhisperPlayer[receiverId] = []
        base.cr.playerFriendsManager.sendWLWhisper(receiverId, message)
        self.historySentWhisperPlayer[receiverId].insert(
            0,
            ChatMessage(self.chatTime(), TYPEDCHAT, message, None, receiverId,
                        self.findName(receiverId), 1, 1, 1))
        if self.logWhispers:
            self.historyOpen.insert(
                0,
                ChatMessage(self.chatTime(), TYPEDCHAT, message, None,
                            receiverId, self.findName(receiverId, 1), 1, 1, 1))
            messenger.send('NewOpenMessage')
        return error

    def sendPlayerWhisperSpeedChat(self, type, messageIndex, receiverId):
        error = None
        if not self.historySentWhisperPlayer.get(receiverId):
            self.historySentWhisperPlayer[receiverId] = []
        if type == SPEEDCHAT_NORMAL:
            base.cr.playerFriendsManager.sendSCWhisper(receiverId, messageIndex)
        else:
            if type == SPEEDCHAT_EMOTE:
                base.cr.playerFriendsManager.sendSCEmoteWhisper(
                    receiverId, messageIndex)
            elif type == SPEEDCHAT_CUSTOM:
                base.cr.playerFriendsManager.sendSCCustomWhisper(
                    receiverId, messageIndex)
            self.historySentWhisperPlayer[receiverId].insert(
                0,
                ChatMessage(self.chatTime(), type, messageIndex, None,
                            receiverId, self.findName(receiverId), 1, 1, 1))
            if self.logWhispers:
                self.historyOpen.insert(
                    0,
                    ChatMessage(self.chatTime(), type,
                                messageIndex, None, receiverId,
                                self.findName(receiverId, 1), 1, 1, 1))
                messenger.send('NewOpenMessage')
        return error

    def findName(self, id, isPlayer=0):
        info = base.cr.getAvatar(id)
        if info:
            return info.getName()
        else:
            return ''

    def whiteListFilterMessage(self, text):
        if not self.useWhiteListFilter:
            return text
        elif not base.whiteList:
            return 'no list'
        words = text.split(' ')
        newwords = []
        for word in words:
            if word == '' or base.whiteList.isWord(word):
                newwords.append(word)
            else:
                newwords.append(base.whiteList.defaultWord)

        newText = ' '.join(newwords)
        return newText

    def executeSlashCommand(self, text):
        pass
