import random

from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import POD
from pirates.piratesbase import PLocalizer
from pirates.quest import QuestDB
from pirates.quest.QuestDNA import QuestDNA
from pirates.quest.QuestLadder import (QuestChoice, QuestChoiceSingle,
                                       QuestLadder)
from pirates.quest.QuestTaskDNA import VisitTaskDNA


class QuestContainerDNA(POD):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestContainerDNA')
    Counter = 1102
    DataSet = {
        'name': None,
        'questInt': -1,
        'title': '',
        'description': '',
        'giverId': None,
        'firstQuestId': None,
        'containers': None,
        'rewards': tuple(),
        'completeCount': QuestChoice.CompleteAll,
        'dialogBefore': '',
        'dialogDuring': '',
        'dialogAfter': '',
        'dialogBrushoff': '',
        'droppable': False
    }

    def hasQuest(self, questId):
        for container in self.getContainers():
            if container.hasQuest(questId):
                return True

        return False

    def isContainer(self):
        return True

    def getQuestId(self):
        return self.name

    def getObject(self, id):
        if self.getQuestId() == id:
            return self
        for container in self.getContainers():
            container.getObject(id)

        return

    def getContainer(self, name):
        if self.name == name:
            return self
        for container in self.getContainers():
            ctr = container.getContainer(name)
            if ctr:
                return ctr

        return

    def oldinitialize(self, parentIsChoice=False):
        giverId = self.getGiverId()
        if giverId:
            parentIsChoice = True
            id = '%s-revisit' % self.getName()
            questDNA = QuestDB.QuestDict.get(id)
            if questDNA:
                title = PLocalizer.ReturnVisitQuestTitle % PLocalizer.NPCNames[giverId]
                desc = PLocalizer.ReturnVisitQuestDesc % PLocalizer.NPCNames[giverId]
                dialog = PLocalizer.ReturnVisitQuestDialog
                PLocalizer.QuestStrings[id] = {
                    'title': title,
                    'description': desc,
                    'dialogAfter': dialog
                }
                self.containers = (questDNA,) + self.containers
            else:
                self.notify.warning('%s not found in QuestDB!' % id)
        for container in self.getContainers():
            container.initialize(parentIsChoice)

    def initialize(self, parentIsChoice=False):
        for container in self.getContainers():
            container.initialize(parentIsChoice)

    def initializeFortune(self, droppable):
        for container in self.getContainers():
            container.initializeFortune(droppable)

    def constructDynamicCopy(self, av, parent=None):
        dynCopy = self._makeDynamicCopy(self.getName(), self.getTitle(), av,
                                        self.getQuestInt(), parent,
                                        self.getGiverId(), self.getRewards(),
                                        self.getFirstQuestId(),
                                        self.getDescription(),
                                        self.getCompleteCount())
        goal = 0
        for container in self.getContainers():
            dynObj = container.constructDynamicCopy(av, parent=dynCopy)
            goal += dynObj.getGoal()
            dynCopy.addContainer(dynObj)

        dynCopy.setGoal(goal)
        return dynCopy

    def _getString(self, stringName):
        if self.name not in PLocalizer.QuestStrings:
            return
        string = PLocalizer.QuestStrings[self.name].get(stringName)
        if string is None or len(string) == 0:
            return
        return string

    def getDialogBefore(self):
        dialog = self._getString('dialogBefore')
        if dialog is not None:
            return dialog
        return random.choice(PLocalizer.QuestDefaultDialogBefore)

    def getDialogDuring(self):
        dialog = self._getString('dialogDuring')
        if dialog is not None:
            return dialog
        return random.choice(PLocalizer.QuestDefaultDialogDuring)

    def getDialogAfter(self):
        dialog = self._getString('dialogAfter')
        if dialog is not None:
            return dialog
        return random.choice(PLocalizer.QuestDefaultDialogAfter)

    def getDialogBrushoff(self):
        dialog = self._getString('dialogBrushoff')
        if dialog is not None:
            return dialog
        return random.choice(PLocalizer.QuestDefaultDialogBrushoff)

    def getDescriptionText(self):
        dialog = self._getString('description')
        if dialog is not None:
            return dialog
        return 'Unknown'

    def compileStats(self, questStatData):
        if self.completeCount == QuestChoice.CompleteAll:
            containers = self.containers
        else:
            containers = self.containers[:self.completeCount]
        for container in containers:
            container.compileStats(questStatData)


class QuestChoiceDNA(QuestContainerDNA):

    def _makeDynamicCopy(self, name, title, av, questInt, parent, giverId,
                         rewards, firstQuestId, description, completeCount):
        return QuestChoice(name, title, av, questInt, parent, giverId, rewards,
                           description, completeCount)


class QuestChoiceSingleDNA(QuestContainerDNA):

    def _makeDynamicCopy(self, name, title, av, questInt, parent, giverId,
                         rewards, firstQuestId, description, completeCount):
        return QuestChoiceSingle(name, title, av, questInt, parent, giverId,
                                 rewards, firstQuestId, description)


class QuestLadderDNA(QuestContainerDNA):

    def _makeDynamicCopy(self, name, title, av, questInt, parent, giverId,
                         rewards, firstQuestId, description, completeCount):
        return QuestLadder(name, title, av, questInt, parent, giverId, rewards,
                           firstQuestId, description)
