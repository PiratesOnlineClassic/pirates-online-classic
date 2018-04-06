import string
import sys
import time

from direct.directnotify import DirectNotifyGlobal
from direct.showbase import DirectObject
from otp.chat.ChatAssistant import ChatAssistant
from otp.chat.ChatGlobals import *
from otp.chat.ChatMessage import ChatMessage
from otp.otpbase import OTPGlobals, OTPLocalizer
from otp.speedchat import SCDecoders, SpeedChatGlobals
from panda3d.core import *
from pirates.piratesbase import PLocalizer


class PChatAssistant(ChatAssistant):
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
            print('Guild chat error')
            error = ERROR_NO_GUILD_CHAT
        return error

    def sendAvatarGuildWLChat(self, message):
        error = None
        if self.checkGuildSpeedChat():
            base.cr.guildManager.sendWLChat(message)
        else:
            print('Guild chat error')
            error = ERROR_NO_GUILD_CHAT
        return error

    def sendAvatarGuildSpeedChat(self, type, msgIndex):
        error = None
        if self.checkGuildSpeedChat():
            base.cr.guildManager.sendSC(msgIndex)
        else:
            print('Guild chat error')
            error = ERROR_NO_GUILD_CHAT
        return error

    def sendAvatarGuildSCQuestChat(self, msgType, questInt, taskNum):
        error = None
        if self.checkGuildSpeedChat():
            pass
        else:
            print('Guild chat error')
            error = ERROR_NO_GUILD_CHAT
        return error

    def sendAvatarCrewTypedChat(self, message):
        error = None
        if self.checkCrewTypedChat():
            chatFlags = CFSpeech | CFTimeout
            localAvatar.bandMember.b_setChat(message, chatFlags)
        else:
            print('Crew chat error')
            error = ERROR_NO_CREW_CHAT
        return error

    def sendAvatarCrewWLChat(self, message):
        error = None
        if self.checkCrewSpeedChat():
            chatFlags = CFSpeech | CFTimeout
            localAvatar.bandMember.b_setWLChat(message, chatFlags)
        else:
            print('Crew chat error')
            error = ERROR_NO_CREW_CHAT
        return error

    def sendAvatarCrewSpeedChat(self, type, msgIndex):
        error = None
        if self.checkCrewSpeedChat():
            localAvatar.bandMember.b_setSpeedChat(msgIndex)
        else:
            print('Crew chat error')
            error = ERROR_NO_CREW_CHAT
        return error

    def sendAvatarCrewSCQuestChat(self, msgType, questInt, taskNum):
        error = None
        if self.checkCrewSpeedChat():
            localAvatar.bandMember.b_setSCQuestChat(questInt, msgType, taskNum)
        else:
            print('Quest Crew chat error')
            error = ERROR_NO_CREW_CHAT
        msgIndex = taskNum
        return error

    def sendAvatarShipPVPCrewTypedChat(self, message):
        error = None
        if self.checkShipPVPTypedChat():
            base.cr.distributedDistrict.siegeManager.sendChat(message)
        else:
            print('Ship PVP chat error: Crew typed Chat')
            error = ERROR_NO_SHIPPVP_CHAT
        return error

    def sendAvatarShipPVPCrewWLChat(self, message):
        error = None
        if self.checkShipPVPTypedChat():
            base.cr.distributedDistrict.siegeManager.sendWLChat(message)
        else:
            print('Ship PVP chat error: Crew WL Chat')
            error = ERROR_NO_SHIPPVP_CHAT
        return error

    def sendAvatarShipPVPCrewSpeedChat(self, type, msgIndex):
        error = None
        if self.checkShipPVPSpeedChat():
            base.cr.distributedDistrict.siegeManager.sendSC(msgIndex)
        else:
            print('Ship PVP chat error: Crew Speed Chat')
            error = ERROR_NO_SHIPPVP_CHAT
        return error

    def sendAvatarShipPVPCrewSCQuestChat(self, msgType, questInt, taskNum):
        error = None
        if self.checkShipPVPSpeedChat():
            pass
        else:
            print('Ship PVP chat error: SCQuest Chat')
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
        argStr = ' '.join(words[1:])
        valid = True
        if comm in ('afk', 'away'):
            localAvatar.toggleAFK()
        else:
            if comm in list(PLocalizer.EmoteCommands.keys()):
                emoteCode = PLocalizer.EmoteCommands[comm]
                messenger.send(SpeedChatGlobals.SCEmoteMsgEvent, [emoteCode])
            elif comm == 'quit':
                import sys
                sys.exit(0)
            elif comm == 'flirt':
                emoteCode = PLocalizer.EMOTE_VALENTINES
                messenger.send(SpeedChatGlobals.SCEmoteMsgEvent, [emoteCode])
            elif comm in ('lfc', 'lfg', 'lookingforcrew'):
                localAvatar.toggleLookingForCrewSign()
            elif comm in ('code', 'redeemcode'):
                localAvatar.submitCodeToServer(argStr)
                base.chatAssistant.receiveGameMessage(PLocalizer.CodeSubmitting % argStr)
            elif comm in ('holiday', 'holidays', 'holidaylist', 'event'):
                base.cr.newsManager.displayHolidayStatus()
            elif comm in ('x2', 'x2bonus'):
                timeRemain = localAvatar.getTempDoubleXPReward()
                if timeRemain:
                    timeRemain = int(timeRemain)
                    minutes, seconds = divmod(timeRemain, 60)
                    hours, minutes = divmod(minutes, 60)
                    base.chatAssistant.receiveGameMessage(PLocalizer.TEMP_DOUBLE_REP_CHAT % (hours, minutes))
                else:
                    base.chatAssistant.receiveGameMessage(PLocalizer.NO_TEMP_DOUBLE_REP)
            elif comm in 'crewhud':
                localAvatar.guiMgr.crewPage.crewHUD.toggleHUD()
            elif comm == 'time':
                messenger.send('requestServerTime')
            else:
                valid = False
            if valid:
                base.cr.centralLogger.writeClientEvent(('slash command - %s(%s)' % (comm, argStr))[:255])

    def getWhisperReplyId(self):
        for message in self.historyOpen:
            if message.getWhisper():
                return (message.getId(), message.getIsPlayer())

        return (0, 0)