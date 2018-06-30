from direct.directnotify import DirectNotifyGlobal
from pirates.quest.QuestAvatarBase import QuestAvatarBase
from pirates.quest.QuestHolder import QuestHolder


class DistributedQuestAvatarAI(QuestAvatarBase, QuestHolder):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedQuestAvatarAI')

    def __init__(self, air):
        self.air = air
        self.activeQuest = ''
        self.questHistory = []
        self.questLadderHistory = []
        self.currentQuestChoiceContainers = []

    def setActiveQuest(self, activeQuest):
        self.activeQuest = activeQuest

    def d_setActiveQuest(self, activeQuest):
        self.sendUpdate('setActiveQuest', [activeQuest])

    def b_setActiveQuest(self, activeQuest):
        self.setActiveQuest(activeQuest)
        self.d_setActiveQuest(activeQuest)

    def getActiveQuest(self):
        return self.activeQuest

    def setQuestHistory(self, questHistory):
        self.questHistory = questHistory

    def d_setQuestHistory(self, questHistory):
        self.sendUpdate('setQuestHistory', [questHistory])

    def b_setQuestHistory(self, questHistory):
        self.setQuestHistory(questHistory)
        self.d_setQuestHistory(questHistory)

    def getQuestHistory(self):
        return self.questHistory

    def setQuestLadderHistory(self, questLadderHistory):
        self.questLadderHistory = questLadderHistory

    def d_setQuestLadderHistory(self, questLadderHistory):
        self.sendUpdate('setQuestLadderHistory', [questLadderHistory])

    def b_setQuestLadderHistory(self, questLadderHistory):
        self.setQuestLadderHistory(questLadderHistory)
        self.d_setQuestLadderHistory(questLadderHistory)

    def getQuestLadderHistory(self):
        return self.questLadderHistory

    def setCurrentQuestChoiceContainers(self, currentQuestChoiceContainers):
        self.currentQuestChoiceContainers = currentQuestChoiceContainers

    def d_setCurrentQuestChoiceContainers(self, currentQuestChoiceContainers):
        self.sendUpdate('setCurrentQuestChoiceContainers',
                        [currentQuestChoiceContainers])

    def b_setCurrentQuestChoiceContainers(self, currentQuestChoiceContainers):
        self.setCurrentQuestChoiceContainers(currentQuestChoiceContainers)
        self.d_setCurrentQuestChoiceContainers(currentQuestChoiceContainers)

    def getCurrentQuestChoiceContainers(self):
        return self.currentQuestChoiceContainers
