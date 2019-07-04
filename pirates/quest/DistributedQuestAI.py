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

        self.ownerId = 0
        self.combineOp = 0

        self.finalizeStateIndex = 0

    def generate(self):
        DistributedObjectAI.generate(self)

        self.accept(self.getChangeEvent(), self.handleQuestChanged)
        self.d_announceNewQuest()

    def handleQuestChanged(self):
        self.d_setTaskStates(self.getTaskStates())

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def getOwnerId(self):
        return self.ownerId

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
        self.sendUpdateToAvatarId(self.ownerId, 'announceNewQuest', [])

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

    def setFinalizeStateIndex(self, finalizeStateIndex):
        self.finalizeStateIndex = finalizeStateIndex

    def getFinalizeStateIndex(self):
        return self.finalizeStateIndex

    def sendFinalizeEvent(self, idx=None):
        try:
            finalizeStateInfo = self.questDNA.getFinalizeInfo()[idx or self.finalizeStateIndex]
        except IndexError:
            return

        finalizeEvent = finalizeStateInfo.get('sendEvent', '')
        if not finalizeEvent:
            return

        messenger.send('%s-%d' % (finalizeEvent, self.doId))

    def d_startFinalizeScene(self, idx, giverId):
        if self.questId not in QuestDB.QuestDict:
            self.notify.warning('Cannot start finalize scene for quest %s, '
                'quest was not found in the QuestDB dictionary!' % self.questId)

            return

        try:
            finalizeInfo = self.questDNA.getFinalizeInfo()[idx]
        except IndexError:
            self.notify.warning('Failed to start finalize scene for avatar: %d, '
                'invalid sceneId: %d!' % (self.ownerId, idx))

            return

        endEvent = finalizeInfo.get('sendEvent', '')
        self.sendUpdateToAvatarId(self.ownerId, 'startFinalizeScene', [idx, giverId, endEvent])

    def doneFinalizeScene(self):
        messenger.send('quest-finalize-%d' % self.doId)

    def d_amFinalized(self):
        Quest.setFinalized(self)
        self.sendUpdateToAvatarId(self.ownerId, 'amFinalized', [])

    def handleEvent(self, holder, questEvent):
        modified = 0
        for (taskState, taskDNA) in zip(self.taskStates, self.questDNA.getTasks()):
            if questEvent.applyTo(taskState, taskDNA):
                taskState.resetModified()
                if holder.getAccess() != 2 and self.questDNA.getVelvetRoped():
                    holder.d_popupProgressBlocker(self.getQuestId())
                else:
                    questEvent.complete(taskState, taskDNA)

            modified += taskState.isModified()

        if modified:
            self.sendTaskStates(self.taskStates)

    def delete(self):
        self.ignore(self.getChangeEvent())

        QuestBase.delete(self)
        DistributedObjectAI.delete(self)
