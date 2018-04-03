# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.chat.PChatAssistant
import string, sys
from direct.showbase import DirectObject
from otp.otpbase import OTPLocalizer
from pirates.piratesbase import PLocalizer
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from otp.speedchat import SCDecoders
from pandac.PandaModules import *
from otp.chat.ChatGlobals import *
from otp.speedchat import SpeedChatGlobals
from otp.chat.ChatMessage import ChatMessage
from otp.chat.ChatAssistant import ChatAssistant
from pirates.ai import NewsManager
import time

class PChatAssistant(ChatAssistant):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PChatAssistant')

    def __init__(self):
        ChatAssistant.__init__(self)

    def checkCrewTypedChat(self):
        if localAvatar.bandMember:
            return True
        return False

    def checkCrewSpeedChat(self):
        if localAvatar.bandMember:
            return True
        return False

    def checkGuildTypedChat(self):
        if localAvatar.guildId:
            return True
        return False

    def checkGuildSpeedChat(self):
        if localAvatar.guildId:
            return True
        return False

    def checkShipPVPTypedChat(self):
        if not hasattr(localAvatar.ship, 'getSiegeTeam'):
            return False
        if localAvatar.ship.getSiegeTeam():
            return True
        return False

    def checkShipPVPSpeedChat(self):
        if not hasattr(localAvatar.ship, 'getSiegeTeam'):
            return False
        if localAvatar.ship.getSiegeTeam():
            return True
        return False

    def receiveSystemMessage(self, message):
        base.localAvatar.guiMgr.messageStack.addTextMessage(message, seconds=20, priority=0, color=(0.5,
                                                                                                    0,
                                                                                                    0,
                                                                                                    1), icon=('admin',
                                                                                                              ''))
        ChatAssistant.receiveSystemMessage(self, message)

    def receiveGuildMessage(self, message):
        error = None
        if not isThought(message):
            self.historyOpen.insert(0, ChatMessage(self.chatTime(), GUILDCHAT, message, None, None, None, 0, 0, 0))
        messenger.send('NewOpenMessage')
        return error

    def receiveCrewMessage(self, message):
        error = None
        if not isThought(message):
            self.historyOpen.insert(0, ChatMessage(self.chatTime(), CREWCHAT, message, None, None, None, 0, 0, 0))
        messenger.send('NewOpenMessage')
        return error

    def receiveShipPVPMessage(self, message):
        error = None
        if not isThought(message):
            self.historyOpen.insert(0, ChatMessage(self.chatTime(), SHIPPVPCHAT, message, None, None, None, 0, 0, 0))
        messenger.send('NewOpenMessage')
        return error

    def receiveGMOpenTypedChat(self, message, chatFlags, senderId, name=None):
        if self.useWhiteListFilter:
            message = self.whiteListFilterMessage(message)
        error = None
        if not name and senderId:
            name = self.findName(senderId, 0)
        if not isThought(message):
            self.historyOpen.insert(0, ChatMessage(self.chatTime(), GMCHAT, message, chatFlags, senderId, name, 0, 0, 0))
        messenger.send('NewOpenMessage')
        return error

    def sendAvatarGuildTypedChat(self, message):
        error = None
        if self.checkGuildTypedChat():
            base.cr.guildManager.sendChat(message)
        else:
            print 'Guild chat error'
            error = ERROR_NO_GUILD_CHAT
        return error

    def sendAvatarGuildWLChat(self, message):
        error = None
        if self.checkGuildSpeedChat():
            base.cr.guildManager.sendWLChat(message)
        else:
            print 'Guild chat error'
            error = ERROR_NO_GUILD_CHAT
        return error

    def sendAvatarGuildSpeedChat(self, type, msgIndex):
        error = None
        if self.checkGuildSpeedChat():
            base.cr.guildManager.sendSC(msgIndex)
        else:
            print 'Guild chat error'
            error = ERROR_NO_GUILD_CHAT
        return error

    def sendAvatarGuildSCQuestChat(self, msgType, questInt, taskNum):
        error = None
        if self.checkGuildSpeedChat():
            pass
        else:
            print 'Guild chat error'
            error = ERROR_NO_GUILD_CHAT
        return error

    def sendAvatarCrewTypedChat(self, message):
        error = None
        if self.checkCrewTypedChat():
            chatFlags = CFSpeech | CFTimeout
            localAvatar.bandMember.b_setChat(message, chatFlags)
        else:
            print 'Crew chat error'
            error = ERROR_NO_CREW_CHAT
        return error

    def sendAvatarCrewWLChat(self, message):
        error = None
        if self.checkCrewSpeedChat():
            chatFlags = CFSpeech | CFTimeout
            localAvatar.bandMember.b_setWLChat(message, chatFlags)
        else:
            print 'Crew chat error'
            error = ERROR_NO_CREW_CHAT
        return error

    def sendAvatarCrewSpeedChat(self, type, msgIndex):
        error = None
        if self.checkCrewSpeedChat():
            localAvatar.bandMember.b_setSpeedChat(msgIndex)
        else:
            print 'Crew chat error'
            error = ERROR_NO_CREW_CHAT
        return error

    def sendAvatarCrewSCQuestChat(self, msgType, questInt, taskNum):
        error = None
        if self.checkCrewSpeedChat():
            localAvatar.bandMember.b_setSCQuestChat(questInt, msgType, taskNum)
        else:
            print 'Quest Crew chat error'
            error = ERROR_NO_CREW_CHAT
        msgIndex = taskNum
        return error

    def sendAvatarShipPVPCrewTypedChat(self, message):
        error = None
        if self.checkShipPVPTypedChat():
            base.cr.distributedDistrict.siegeManager.sendChat(message)
        else:
            print 'Ship PVP chat error: Crew typed Chat'
            error = ERROR_NO_SHIPPVP_CHAT
        return error

    def sendAvatarShipPVPCrewWLChat(self, message):
        error = None
        if self.checkShipPVPTypedChat():
            base.cr.distributedDistrict.siegeManager.sendWLChat(message)
        else:
            print 'Ship PVP chat error: Crew WL Chat'
            error = ERROR_NO_SHIPPVP_CHAT
        return error

    def sendAvatarShipPVPCrewSpeedChat(self, type, msgIndex):
        error = None
        if self.checkShipPVPSpeedChat():
            base.cr.distributedDistrict.siegeManager.sendSC(msgIndex)
        else:
            print 'Ship PVP chat error: Crew Speed Chat'
            error = ERROR_NO_SHIPPVP_CHAT
        return error

    def sendAvatarShipPVPCrewSCQuestChat(self, msgType, questInt, taskNum):
        error = None
        if self.checkShipPVPSpeedChat():
            pass
        else:
            print 'Ship PVP chat error: SCQuest Chat'
            error = ERROR_NO_SHIPPVP_CHAT
        return error

    def sendAvatarSCQuestChat(self, msgType, questInt, taskNum):
        error = None
        messenger.send(SCQuestEvent)
        messenger.send('chatUpdateSCQuest', [questInt, msgType, taskNum])
        return

    def executeSlashCommand(self, text):
        words = text[1:].split(' ')
        comm = words[0].lower()
        argStr = ('').join(words[1:])
        if comm in ('afk', 'away'):
            localAvatar.toggleAFK()
        else:
            if comm in PLocalizer.EmoteCommands.keys():
                emoteCode = PLocalizer.EmoteCommands[comm]
                messenger.send(SpeedChatGlobals.SCEmoteMsgEvent, [emoteCode])
            else:
                if comm == 'quit':
                    import sys
                    sys.exit(0)
                else:
                    if comm == 'flirt':
                        emoteCode = PLocalizer.EMOTE_VALENTINES
                        messenger.send(SpeedChatGlobals.SCEmoteMsgEvent, [emoteCode])
                    else:
                        if comm in ('lfc', 'lfg', 'lookingforcrew'):
                            localAvatar.toggleLookingForCrewSign()
                        else:
                            if comm in ('code', 'redeemcode'):
                                localAvatar.submitCodeToServer(argStr)
                                base.chatAssistant.receiveGameMessage(PLocalizer.CodeSubmitting % argStr)
                            else:
                                if comm in ('holiday', 'holidays', 'holidaylist', 'event'):
                                    base.cr.newsManager.displayHolidayStatus()
                                else:
                                    if comm in ('x2', 'x2bonus'):
                                        timeRemain = localAvatar.getTempDoubleXPReward()
                                        if timeRemain:
                                            timeRemain = int(timeRemain)
                                            minutes, seconds = divmod(timeRemain, 60)
                                            hours, minutes = divmod(minutes, 60)
                                            base.chatAssistant.receiveGameMessage(PLocalizer.TEMP_DOUBLE_REP_CHAT % (hours, minutes))
                                        else:
                                            base.chatAssistant.receiveGameMessage(PLocalizer.NO_TEMP_DOUBLE_REP)
                                    else:
                                        if comm in 'crewhud':
                                            localAvatar.guiMgr.crewPage.crewHUD.toggleHUD()
                                        else:
                                            if comm == 'time':
                                                messenger.send('requestServerTime')

    def getWhisperReplyId(self):
        for message in self.historyOpen:
            if message.getWhisper():
                return (message.getId(), message.getIsPlayer())

        return (0, 0)
# okay decompiling .\pirates\chat\PChatAssistant.pyc
