# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.speedchat.PSpeedChatQuestTerminal
from otp.speedchat.SCTerminal import *
from pirates.quest import QuestDB
PSpeedChatQuestMsgEvent = 'PSCQuestMsg'

def decodeSCQuestMsg(questId, msgType, taskNum):
    questdb = QuestDB.QuestDict[questId]
    if questdb is None:
        return
    if msgType == 0:
        return questdb.getSCSummaryText(taskNum)
    else:
        if msgType == 1:
            return questdb.getSCWhereIsText(taskNum)
        else:
            if msgType == 2:
                return questdb.getSCHowToText(taskNum)
            else:
                return
    return


def decodeSCQuestMsgInt(questInt, msgType, taskNum):
    qId = QuestDB.getQuestIdFromQuestInt(questInt)
    questDna = QuestDB.QuestDict[qId]
    if questDna is None:
        return
    if msgType == 0:
        return questDna.getSCSummaryText(taskNum)
    else:
        if msgType == 1:
            return questDna.getSCWhereIsText(taskNum)
        else:
            if msgType == 2:
                return questDna.getSCHowToText(taskNum)
            else:
                return
    return


class PSpeedChatQuestTerminal(SCTerminal):
    __module__ = __name__

    def __init__(self, msg, questInt, toNpcId, msgType, taskNum):
        SCTerminal.__init__(self)
        self.msg = msg
        self.questInt = questInt
        self.toNpcId = toNpcId
        self.msgType = msgType
        self.taskNum = taskNum

    def getDisplayText(self):
        return self.msg

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(PSpeedChatQuestMsgEvent), [
         self.questInt, self.toNpcId, self.msgType, self.taskNum])
# okay decompiling .\pirates\speedchat\PSpeedChatQuestTerminal.pyc
