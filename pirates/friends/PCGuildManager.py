# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.friends.PCGuildManager
from otp.friends.GuildManager import GuildManager
from pirates.piratesbase import PLocalizer


class PCGuildManager(GuildManager):
    

    def sendSCQuest(self, questInt, msgType, taskNum):
        self.notify.debugCall()
        print 'GuildManager.sendSCQuest() called'
        self.sendUpdate('sendSCQuest', [questInt, msgType, taskNum])

    def recvSCQuest(self, senderId, questInt, msgType, taskNum):
        self.notify.debugCall()
        senderName = self.id2Name.get(senderId, None)
        message = decodeSCQuestMsgInt(questInt, msgType, taskNum)
        if senderName:
            displayMess = '%s %s %s' % (senderName, OTPLocalizer.GuildPrefix, message)
            base.chatAssistant.receiveGuildMessage(displayMess)
        else:
            self.pendingMsgs.append([senderId, message])
            self.memberList()
        return
# okay decompiling .\pirates\friends\PCGuildManager.pyc
