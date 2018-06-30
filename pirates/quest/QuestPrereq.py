# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestPrereq
from direct.showbase.PythonUtil import POD, makeTuple


class QuestPrereq(POD):

    def giverMatters(self):
        return hasattr(self, 'giverCanGive')

    def avMatters(self):
        return hasattr(self, 'avIsReady')

    def environMatters(self):
        return hasattr(self, 'environIsValid')


class HpAtLeast(QuestPrereq):

    DataSet = {'minHp': None}

    def __init__(self, minHp):
        QuestPrereq.__init__(self, minHp=minHp)

    def avIsReady(self, av):
        return av.getMaxHp() >= self.minHp


class SwiftnessAtLeast(QuestPrereq):

    DataSet = {'minSwiftness': None}

    def __init__(self, minSwiftness):
        QuestPrereq.__init__(self, minSwiftness=minSwiftness)

    def avIsReady(self, av):
        return av.getMaxSwiftness() >= self.minSwiftness


class LuckAtLeast(QuestPrereq):

    DataSet = {'minLuck': None}

    def __init__(self, minLuck):
        QuestPrereq.__init__(self, minLuck=minLuck)

    def avIsReady(self, av):
        return av.getMaxLuck() >= self.minLuck


class MojoAtLeast(QuestPrereq):

    DataSet = {'minMojo': None}

    def __init__(self, minMojo):
        QuestPrereq.__init__(self, minMojo=minMojo)

    def avIsReady(self, av):
        return av.getMaxMojo() >= self.minMojo


class DidQuest(QuestPrereq):

    DataSet = {'questIds': None}

    def __init__(self, questIds):
        QuestPrereq.__init__(self, questIds=questIds)

    def setQuestIds(self, questIds):
        self.questIds = makeTuple(questIds)

    def avIsReady(self, av):
        for questId in self.questIds:
            if not av.hasDoneQuest(questId):
                return False

        return True


class GetFrom(QuestPrereq):

    DataSet = {'questGivers': None}

    def __init__(self, questGivers):
        QuestPrereq.__init__(self, questGivers=questGivers)

    def setQuestGivers(self, questGivers):
        self.questGivers = makeTuple(questGivers)

    def giverCanGive(self, giver):
        return giver in self.questGivers


# okay decompiling .\pirates\quest\QuestPrereq.pyc
