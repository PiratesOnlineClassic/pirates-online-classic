# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestLadderDynMap
from direct.directnotify import DirectNotifyGlobal
from pirates.quest import QuestDB, QuestLadder, QuestLadderDB


class QuestLadderDynMap:

    def __init__(self):
        self.QuestIDLadderDynMap = {}
        for ladderId, ladderDNA in QuestLadderDB.FortuneQuestLadderDict.items():
            ladderInt = ladderDNA.questInt
            for container in ladderDNA.getContainers():
                if container.isContainer():
                    self.getMappingFromContainer(container, ladderId, ladderInt)
                else:
                    self.addMapping(container.questId, ladderId, ladderInt)

        for ladderId, ladderDNA in QuestLadderDB.FameQuestLadderDict.items():
            ladderInt = ladderDNA.questInt
            for container in ladderDNA.getContainers():
                if container.isContainer():
                    self.getMappingFromContainer(container, ladderId, ladderInt)
                else:
                    self.addMapping(container.questId, ladderId, ladderInt)

    def getMappingFromContainer(self, container, ladderId, ladderInt):
        for containerChild in container.getContainers():
            if containerChild.isContainer():
                self.getMappingFromContainer(containerChild, ladderId,
                                             ladderInt)
            else:
                self.addMapping(containerChild.questId, ladderId, ladderInt)

    def addMapping(self, questId, ladderId, ladderInt):
        ladder = (ladderId, ladderInt)
        self.QuestIDLadderDynMap[questId] = ladder

    def findQuestLadderId(self, questId):
        if questId == 'test.1visit':
            return 'Error'
        if questId == 'test.3visit':
            return 'Error'
        ladder = self.QuestIDLadderDynMap[questId]
        return ladder[0]

    def findQuestLadderInt(self, questId):
        if questId == 'test.1visit':
            return 8888
        if questId == 'test.3visit':
            return 8888
        ladder = self.QuestIDLadderDynMap[questId]
        return ladder[1]

    def getCompleteMapping(self):
        return self.QuestIDLadderDynMap


# okay decompiling .\pirates\quest\QuestLadderDynMap.pyc
