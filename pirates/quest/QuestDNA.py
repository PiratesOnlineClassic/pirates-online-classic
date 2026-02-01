from direct.directnotify import DirectNotifyGlobal
from otp.otpbase.OTPUtil import ParamObj, makeTuple
from direct.showbase.PythonUtil import getSetter
from otp.otpbase.OTPUtil import POD
from pirates.piratesbase import PLocalizer
from pirates.quest.QuestLadder import QuestStub
import random

class CombineOps:
    OR = 0
    AND = 1


class QuestDNA(ParamObj):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestDNA')
    OR = CombineOps.OR
    AND = CombineOps.AND
    
    class ParamSet(ParamObj.ParamSet):
        Params = {
            'prereqs': tuple(),
            'tasks': tuple(),
            'combineOp': CombineOps.OR,
            'returnGiverIds': None,
            'chainedQuests': tuple(),
            'questId': None,
            'questInt': -1,
            'title': '',
            'droppable': True,
            'rewards': tuple(),
            'finalizeInfo': tuple(),
            'instanceInfo': tuple(),
            'completeRequiresVisit': True,
            'playStinger': True,
            'displayGoal': True,
            'requiresVoyage': False,
            'progressBlock': False,
            'velvetRoped': True,
            'checkPoint': -1,
            'finalQuest': False,
            'acquireOnce': False,
            'minLevel': 0,
            'minWeapLevel': 0,
            'weapLvlType': None}

    def __init__(self, *args, **kwArgs):
        ParamObj.__init__(self, *args, **kwArgs)
        self.goal = 0
    
    def makeCopy(self):
        copy = QuestDNA(self.getCurrentParams())
        taskDNAs = []
        for taskDNA in self.tasks:
            taskDNAs.append(taskDNA.makeCopy())
        
        copy.setTasks(tuple(taskDNAs))
        return copy

    def setTasks(self, tasks):
        self.tasks = makeTuple(tasks)

    def setRewards(self, rewards):
        self.rewards = makeTuple(rewards)

    def setFinalizeInfo(self, finalizeInfo):
        self.finalizeInfo = makeTuple(finalizeInfo)

    def setInstanceInfo(self, instanceInfo):
        self.instanceInfo = makeTuple(instanceInfo)

    def setChainedQuests(self, chainedQuests):
        self.chainedQuests = makeTuple(chainedQuests)

    def setPrereqs(self, prereqs):
        self.prereqs = makeTuple(prereqs)
        self._giverPreqs = []
        self._avPreqs = []
        self._envPreqs = []
        for preq in self.prereqs:
            if preq.giverMatters():
                self._giverPreqs.append(preq)
            
            if preq.avMatters():
                self._avPreqs.append(preq)
            
            if preq.environMatters():
                self._envPreqs.append(preq)

    def vetGiver(self, giver):
        for preq in self._giverPreqs:
            if not preq.giverCanGive(giver):
                return False
        
        return True

    def vetAv(self, av):
        for preq in self._avPreqs:
            if not preq.avIsReady(av):
                return False
        
        return True

    def vetEnviron(self):
        for preq in self._envPreqs:
            if not preq.environIsValid():
                return False

        return True

    def getInitialTaskStates(self, holder):
        states = []
        for task in self.tasks:
            states.append(task.getInitialTaskState(holder))
        
        return states

    def _getString(self, stringName):
        if self.questId not in PLocalizer.QuestStrings:
            return None
        
        string = PLocalizer.QuestStrings[self.questId].get(stringName)
        if string is None or len(string) == 0:
            return None
        
        return string
    
    def getTitle(self):
        title = self._getString('title')
        if title is not None:
            return title
        
        return self.tasks[0].getTitle()

    def getDialogBefore(self):
        dialog = self._getString('dialogBefore')
        if dialog is not None:
            return dialog
        
        return self.tasks[0].getDialogBefore()
    
    def getDialogDuring(self):
        dialog = self._getString('dialogDuring')
        if dialog is not None:
            return dialog
        
        return self.tasks[0].getDialogDuring()
    
    def getDialogAfter(self):
        dialog = self._getString('dialogAfter')
        if dialog is not None:
            return dialog
        
        return self.tasks[0].getDialogAfter()
    
    def getTaskDNAs(self):
        return self.tasks

    def getDescriptionText(self, taskStates = []):
        taskDNAs = self.getTaskDNAs()
        if len(taskDNAs) == 1:
            taskStr = PLocalizer.QuestDescTaskSingle % {
                'task': taskDNAs[0].getDescriptionText(taskStates[0])}
            str = PLocalizer.QuestStrOneTask % {
                'task': taskStr}
        else:
            headingStr = {
                QuestDNA.OR: PLocalizer.QuestMultiHeadingOr,
                QuestDNA.AND: PLocalizer.QuestMultiHeadingAnd}[self.getCombineOp()]
            tasksStr = ''
            for (taskDNA, taskState) in zip(taskDNAs, taskStates):
                tasksStr += PLocalizer.QuestDescTaskMulti % {
                    'task': taskDNA.getDescriptionText(taskState)}
            
            str = PLocalizer.QuestStrMultiTask % {
                'heading': headingStr,
                'tasks': tasksStr}
        return str

    def getSCSummaryText(self, taskNum):
        taskDNAs = self.getTasks()
        if len(taskDNAs) == 1:
            taskStr = PLocalizer.QuestDescTaskSingleNoPeriod % {
                'task': taskDNAs[0].getSCSummaryText([])}
            str = PLocalizer.QuestStrOneTask % {
                'task': taskStr}
        elif len(taskDNAs) >= taskNum:
            taskStr = PLocalizer.QuestDescTaskSingleNoPeriod % {
                'task': taskDNAs[taskNum].getSCSummaryText([])}
            str = PLocalizer.QuestStrOneTask % {
                'task': taskStr}
        else:
            str = ''
        return str

    def getSCWhereIsText(self, taskNum):
        taskDNAs = self.getTasks()
        if len(taskDNAs) == 1:
            taskStr = PLocalizer.QuestDescTaskSingleNoPeriod % {
                'task': taskDNAs[0].getSCWhereIsText([])}
            str = PLocalizer.QuestStrOneTask % {
                'task': taskStr}
        elif len(taskDNAs) >= taskNum:
            taskStr = PLocalizer.QuestDescTaskSingleNoPeriod % {
                'task': taskDNAs[taskNum].getSCWhereIsText([])}
            str = PLocalizer.QuestStrOneTask % {
                'task': taskStr}
        else:
            str = ''
        return str
    
    def getSCHowToText(self, taskNum):
        taskDNAs = self.getTasks()
        if len(taskDNAs) == 1:
            taskStr = PLocalizer.QuestDescTaskSingleNoPeriod % {
                'task': taskDNAs[0].getSCHowToText([])}
            str = PLocalizer.QuestStrOneTask % {
                'task': taskStr}
        elif len(taskDNAs) >= taskNum:
            taskStr = PLocalizer.QuestDescTaskSingleNoPeriod % {
                'task': taskDNAs[taskNum].getSCHowToText([])}
            str = PLocalizer.QuestStrOneTask % {
                'task': taskStr}
        else:
            str = ''
        return str

    def hasQuest(self, questId):
        return questId == self.getQuestId()

    def initialize(self, parentIsChoice):
        self.setDroppable(False)

    def initializeFortune(self, droppable):
        self.setDroppable(droppable)

    def getGoal(self):
        return self.goal

    def constructDynamicCopy(self, av, parent):
        questInt = self.getQuestInt()
        complete = False
        if questInt in av.getQuestHistory():
            complete = True
        
        rewards = self.getRewards()
        questId = self.getQuestId()
        for task in self.tasks:
            self.goal += task.getGoalNum()
        
        return QuestStub(name = questId, av = av, questInt = questInt, parent = parent, giverId = None, rewards = rewards, complete = complete, goal = self.getGoal())
    
    def getContainer(self, name):
        if self.getQuestId() == name:
            return self
        return None

    def isContainer(self):
        return False

    def compileStats(self, questStatData):
        if self.requiresVoyage:
            questStatData.incrementMisc('voyages')
        
        for task in self.tasks:
            task.compileStats(questStatData)

    def computeRewards(self, initialTaskStates, holder):
        rewards = []
        for (taskDNA, taskState) in zip(self.getTaskDNAs(), initialTaskStates):
            rewards.extend(makeList(taskDNA.computeRewards(taskState, holder)))
        
        return tuple(rewards)

    if __dev__:
        
        def check(self):
            pass

    

