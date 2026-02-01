from pirates.piratesbase import PLocalizer
from otp.friends.GuildManager import GuildManager

class PCGuildManager(GuildManager):
    
    def sendSCQuest(self, questInt, msgType, taskNum):
        self.notify.debugCall()
        print('GuildManager.sendSCQuest() called')
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


