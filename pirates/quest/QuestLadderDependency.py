# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestLadderDependency
from direct.directnotify import DirectNotifyGlobal
from pirates.quest import QuestDB, QuestLadder, QuestLadderDB


class QuestLadderDependency:
    __module__ = __name__

    def __init__(self):
        self.idDependencyMap = {}
        self.intDependencyMap = {}
        self.populateMap()

    def populateMap(self):
        self.idDependencyMap['test'] = 99999
        self.intDependencyMap[99999] = 99999

    def findIdDependency(self, questId):
        if questId in self.idDependencyMap:
            return self.idDependencyMap[questId]
        return 0

    def findIntDependency(self, questInt):
        if questId in self.idDependencyMap:
            return self.intDependencyMap[questId]
        return 0

    def checkDependency(self, quest, ladder, isId):
        dependency = 0
        if isId:
            dependency = self.findIdDependency(quest)
        else:
            dependency = self.findIntDependency(quest)
        if dependency == 0:
            return True
        if ladder.count(dependency):
            return True
        else:
            return False
# okay decompiling .\pirates\quest\QuestLadderDependency.pyc
