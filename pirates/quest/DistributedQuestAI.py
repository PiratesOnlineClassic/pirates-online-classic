from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from pirates.quest.QuestBase import QuestBase
from pirates.quest.Quest import Quest
from pirates.quest import QuestDB
from pirates.quest.QuestTaskState import QuestTaskState


class DistributedQuestAI(DistributedObjectAI, QuestBase, Quest):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedQuestAI')

    def __init__(self, air, questId='', giverId='', initialTaskStates=[QuestTaskState()], rewards=[]):
        DistributedObjectAI.__init__(self, air)
        Quest.__init__(self, questId, giverId, initialTaskStates, rewards)

        self.combineOp = 0

    def generate(self):
        DistributedObjectAI.generate(self)

        self.d_announceNewQuest()

    def d_setQuestId(self, questId):
        self.sendUpdate('setQuestId', [questId])

    def b_setQuestId(self, questId):
        self.setQuestId(questId)
        self.d_setQuestId(questId)

    def getQuestId(self):
        return self.questId

    def d_setGiverId(self, giverId):
        self.sendUpdate('setGiverId', [giverId])

    def b_setGiverId(self, giverId):
        self.setGiverId(giverId)
        self.d_setGiverId(giverId)

    def getGiverId(self):
        return self.giverId

    def d_announceNewQuest(self):
        self.sendUpdate('announceNewQuest', [])

    def d_setCombineOp(self, combineOp):
        self.sendUpdate('setCombineOp', [combineOp])

    def b_setCombineOp(self, combineOp):
        self.setCombineOp(combineOp)
        self.d_setCombineOp(combineOp)

    def getCombineOp(self):
        return self.combineOp

    def d_setTaskStates(self, taskStates):
        self.sendUpdate('setTaskStates', [taskStates])

    def b_setTaskStates(self, taskStates):
        self.setTaskStates(taskStates)
        self.d_setTaskStates(taskStates)

    def getTaskStates(self):
        return self.taskStates

    def d_setRewardStructs(self, rewardStructs):
        self.sendUpdate('setRewardStructs', [rewardStructs])

    def b_setRewardStructs(self, rewardStructs):
        self.setRewardStructs(rewardStructs)
        self.d_setRewardStructs(rewardStructs)

    def d_startFinalizeScene(self, idx, giverId):
        if self.questId not in QuestDB.QuestDict:
            self.notify.warning('Cannot start finalize scene for quest %s, '
                'quest was not found in the QuestDB dictionary!' % self.questId)

            return

        questDNA = QuestDB.QuestDict[self.questId]
        finalizeInfo = questDNA.getFinalizeInfo()[idx]
        endEvent = finalizeInfo.get('sendEvent', '')

        self.sendUpdate('startFinalizeScene', [idx, giverId, endEvent])

    def doneFinalizeScene(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        messenger.send('quest-finalize-%d' % self.doId)

    def delete(self):
        QuestBase.delete(self)
        DistributedObjectAI.delete(self)
