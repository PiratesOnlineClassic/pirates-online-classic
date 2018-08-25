from direct.showbase.PythonUtil import POD, makeTuple
from pirates.quest import QuestDB, QuestReward


class QuestOffer(POD):
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
