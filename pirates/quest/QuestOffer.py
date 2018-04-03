# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestOffer
from direct.showbase.PythonUtil import POD, makeTuple
from pirates.quest import QuestReward, QuestDB

class QuestOffer(POD):
    __module__ = __name__
    DataSet = {'questId': None, 'title': '', 'initialTaskStates': tuple(), 'rewardStructs': tuple()}

    @staticmethod
    def create(questId, holder):
        questDNA = QuestDB.QuestDict[questId]
        initialTaskStates = questDNA.getInitialTaskStates(holder)
        rewards = questDNA.getRewards()
        if len(rewards) == 0:
            rewards = questDNA.computeRewards(initialTaskStates, holder)
        return QuestOffer(questId, questId, initialTaskStates, rewards)

    def __init__(self, questId=None, title=None, initialTaskStates=None, rewards=None):
        POD.__init__(self)
        if questId is not None:
            self.setQuestId(questId)
            self.setTitle(title)
            self.setInitialTaskStates(initialTaskStates)
            self.setRewards(rewards)
        return

    def getRewards(self):
        rewards = []
        for rewardStruct in self.getRewardStructs():
            rewards.append(QuestReward.QuestReward.makeFromStruct(rewardStruct))

        return rewards

    def setRewards(self, rewards):
        rewardStructs = []
        for reward in makeTuple(rewards):
            if reward:
                rewardStructs.append(reward.getQuestRewardStruct())

        self.setRewardStructs(rewardStructs)

    def getQuestDNA(self):
        return QuestDB.QuestDict[self.questId]

    def isLadder(self):
        return False
# okay decompiling .\pirates\quest\QuestOffer.pyc
