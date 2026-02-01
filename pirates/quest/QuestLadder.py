from direct.directnotify import DirectNotifyGlobal
from direct.showbase import DirectObject
from pirates.quest.QuestTaskDNA import RandomizedDefeatTaskDNA
from pirates.quest.QuestTaskDNA import RandomizedDefeatShipTaskDNA

class QuestContainer(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestContainer')

    def __init__(self, name, title, av, questInt, parent = None, giverId = None, rewards = (), firstQuestId = None, description = ''):
        self.name = name
        self.questInt = questInt
        if giverId:
            self.giverId = giverId
        else:
            self.giverId = ''
        if title == '':
            self.title = name
        else:
            self.title = title
        self.rewards = rewards
        self.description = description
        self.av = av
        self.parent = parent
        if not parent:
            pass

        self.firstQuestId = firstQuestId
        self.containers = []
        self.completedQuests = []
        self.goal = 0
        self.complete = False
        self.viewedInGUI = True

    def destroy(self):
        self.ignoreAll()
        self.completedQuests = []
        for container in self.containers:
            container.destroy()

        self.parent = None
        self.av = None

    def getName(self):
        return self.name

    def getQuestId(self):
        return self.getName()

    def getQuestInt(self):
        return self.questInt

    def getParent(self):
        return self.parent

    def getRewards(self):
        return self.rewards

    def getTitle(self):
        return self.title

    def getDescription(self):
        return self.description

    def getGiverId(self):
        return self.giverId

    def getRewards(self):
        return self.rewards

    def getContainers(self):
        return self.containers

    def getValidContainers(self):
        return self.containers

    def getGoal(self):
        return self.goal

    def setGoal(self, goal):
        self.goal = goal

    def getComplete(self):
        return self.complete

    def isChoice(self):
        return False

    def addContainer(self, container):
        self.containers.append(container)

    def hasQuest(self, questId):
        for container in self.containers:
            if container.hasQuest(questId):
                return True

        return False

    def linkQuest(self, quest):
        for container in self.containers:
            if container.linkQuest(quest):
                return True

        return False

    def unlinkQuest(self, questId):
        if not self.hasQuest(questId):
            self.notify.warning("tried to unlink quest: %s I don't have" % questId)
            return False

        for container in self.containers:
            if container.unlinkQuest(questId):
                return True

        return False

    def isComplete(self, showComplete = False):
        for container in self.getContainers():
            if not container.isComplete(showComplete):
                return False

        return True

    def percentComplete(self, history):
        if self.complete:
            return (self.goal, self.goal)
        elif self.getQuestInt() in history:
            self.complete = True
            return (self.goal, self.goal)

        goal = self.goal
        containers = self.getContainers()
        if containers and isinstance(containers[0], QuestStub):
            quest = containers[0].quest
            if quest and hasattr(quest, 'tasks') and quest.tasks:
                taskDNA = quest.tasks[0]
                if isinstance(taskDNA, RandomizedDefeatTaskDNA) or isinstance(taskDNA, RandomizedDefeatShipTaskDNA):
                    goal = self.getContainers()[0].quest.taskStates[0].getGoal()

        totCompCont = 0
        for container in self.getContainers():
            (compCont, cont) = container.percentComplete(history)
            totCompCont += compCont

        return (totCompCont, goal)

    def getNextContainer(self, currentQuestId):
        for container in self.containers:
            if container.hasQuest(currentQuestId):
                nextContainerIndex = self.containers.index(container) + 1
                if nextContainerIndex >= len(self.containers):
                    return

                return self.containers[nextContainerIndex]
        return None

    def assignFirstQuest(self, completedQuests):
        self.containers[0].assignFirstQuest(completedQuests)

    def updateCompletedQuests(self, completedQuest, prevCompletedQuests = []):
        self.notify.debug('QContainer.updateCompletedQuests.SELF.QUEST_INT: %s' % self.questInt)
        self.notify.debug('QContainer.updateCompletedQuests.COMPLETED_QUEST: %s' % completedQuest)
        self.notify.debug('QContainer.updateCompletedQuests.COMPLETED_QUESTS: %s' % self.completedQuests)
        self.notify.debug('QContainer.updateCompletedQuests.PREV_COMPLETED_QUESTS: %s' % prevCompletedQuests)
        if len(self.completedQuests) == 0:
            if len(prevCompletedQuests) > 0:
                self.notify.warning('QContainer SELF( %s ).COMPLETED_QUESTS is SET to: %s' % (self.questInt, prevCompletedQuests))
                self.completedQuests = prevCompletedQuests

        if completedQuest in self.completedQuests:
            self.notify.warning('Quest: %s already in completedQuests!' % completedQuest.getQuestId())
        else:
            self.notify.warning('QContainer SELF( %s ).COMPLETED_QUESTS is APPENDED with: %s' % (self.questInt, completedQuest))
            self.completedQuests.append(completedQuest)

    def handleQuestComplete(self, completedQuest, completedContainer, prevCompletedQuests = []):
        self.notify.debug('QC.handleQuestComplete.SELF.QUEST_INT: %s' % self.questInt)
        self.notify.debug('QC.handleQuestComplete.COMPLETED_QUEST: %s' % completedQuest)
        self.notify.debug('QC.handleQuestComplete.COMPLETED_CONTAINER: %s' % completedContainer.questInt)
        self.notify.debug('QC.handleQuestComplete.COMPLETED_CONTAINER.COMPLETED_QUESTS: %s' % completedContainer.completedQuests)
        self.notify.debug('QC.handleQuestComplete.PREV_COMPLETED_QUESTS: %s' % prevCompletedQuests)
        self.notify.debug('QC.handleQuestComplete.IS_COMPLETE: %s' % self.isComplete())
        self.notify.debug('QC.handleQuestComplete.SELF.COMPLETED_QUESTS: %s' % self.completedQuests)
        if self.isComplete():
            if self.parent:
                self.updateCompletedQuests(completedQuest, prevCompletedQuests)
                self.parent.handleQuestComplete(completedQuest, self, self.completedQuests)
            else:
                self.av.questStatus.updateHistory(self)
                self.updateCompletedQuests(completedQuest)
                quests = completedContainer.completedQuests
                self.av._swapQuest(oldQuests = quests, giverId = None, questIds = None, rewards = None)
                self.av.questStatus.handleLadderComplete(self)
        else:
            self.av.questStatus.updateHistory(completedContainer)
            self.updateCompletedQuests(completedQuest)
            self.advance(completedContainer)

    def handleQuestDropped(self, droppedQuest):
        if self.parent:
            self.parent.handleQuestDropped(droppedQuest)
        else:
            self.av._dropQuest(droppedQuest)
            self.av.questStatus.handleQuestDropped(droppedQuest, self)

    def advance(self, completedContainer):
        self.notify.debug('QC.advance() called. QUEST_INT: %s' % self.questInt)
        self.notify.debug('QC.advance().completedContainer: %s' % completedContainer.name)
        self.notify.debug('QC.advance().completedContainer.completedQuests: %s' % completedContainer.completedQuests)
        nextIndex = self.containers.index(completedContainer) + 1
        nextContainer = self.containers[nextIndex]
        nextContainer.assignFirstQuest(completedContainer.completedQuests)
        for questId in completedContainer.completedQuests:
            if self.completedQuests.count(questId):
                self.completedQuests.remove(questId)

        completedContainer.completedQuests = []

    def assignQuest(self, quests, giverId, nextQuestIds, rewards = [], callback = None):
        for quest in quests:
            if hasattr(quest, 'questDNA'):
                questDNA = quest.getQuestDNA()
                if questDNA and questDNA.getProgressBlock():
                    if questDNA.getFinalQuest() or self.av.getAccess() != 2:
                        nextQuestId = nextQuestIds[0]
                        self.av.d_popupProgressBlocker(nextQuestId)

                else:
                    break
            else:
                self.notify.warning('%s has no questDNA!' % quest.getQuestId())

        nextQuestId = nextQuestIds[0]
        if len(quests):
            self.av._swapQuest(quests, giverId, nextQuestIds, rewards)
        else:
            if len(nextQuestIds) > 1:
                self.notify.warning('attempted to assign multiple quests: %s' % nextQuestIds)
            self.av._acceptQuest(nextQuestId, giverId, rewards)

        def handleQuestsAvailable(callback, av, quests):
            goalDisplayed = False
            for quest in quests:
                av.questStatus.assignQuest(quest)
                if not goalDisplayed:
                    if quest.getQuestDNA().getDisplayGoal() == True:
                        av.requestActiveQuest(quest.getQuestId())
                        goalDisplayed = True

            if callback:
                callback(av.getDoId())

        self.acceptOnce('quest-available-%s-%d' % (nextQuestId, self.av.getDoId()), handleQuestsAvailable, extraArgs = [callback])

    def updateHistory(self, completedContainer):
        self.av.questStatus.updateHistory(completedContainer)

    def getDownstreamContainers(self, downstreamContainers):
        for container in self.containers:
            downstreamContainers.append(container)
            container.getDownstreamContainers(downstreamContainers)

    def getChoiceContainers(self, choiceContainers):
        for container in self.getContainers():
            container.getChoiceContainers(choiceContainers)

        if self.isChoice():
            choiceContainers.append(self)

    def getPathToRoot(self, rootPath):
        container = self
        while container != None:
            parent = container.getParent()
            if parent:
                rootPath.append(parent)

            container = parent
        rootPath.reverse()

    def getQuestPath(self, questId, cpath):
        if self.name == questId:
            self.getPathToRoot(cpath)
            return True

        for container in self.containers:
            if container.getQuestPath(questId, cpath):
                return True

        return False

    def getQuestStub(self, questId):
        if self.name == questId:
            return self

        for container in self.containers:
            qs = container.getQuestStub(questId)
            if qs:
                return qs
        return None

    def getFirstQuestId(self):
        if self.firstQuestId:
            return self.firstQuestId

        return self.containers[0].getFirstQuestId()

    def getNextQuestId(self, currQuestId):
        questStub = self.getQuestStub(currQuestId)
        if questStub:
            parent = questStub.getParent()
            nextContainer = parent.getNextContainer(currQuestId)
            if nextContainer:
                return nextContainer.getFirstQuestId()
            container = parent
            while container != None:
                parent = container.getParent()
                if parent:
                    nextContainer = parent.getNextContainer(currQuestId)
                    if nextContainer:
                        return nextContainer.getFirstQuestId()
                container = parent

    def getSiblingQuestIds(self, questId):
        siblings = []
        questStub = self.getQuestStub(questId)
        if questStub:
            parent = questStub.getParent()
            for container in parent.getContainers():
                firstQuestId = container.getFirstQuestId()
                if firstQuestId and firstQuestId != questId:
                    siblings.append(firstQuestId)

        return siblings

    def getContainer(self, name):
        if self.name == name:
            return self
        else:
            for container in self.containers:
                ctr = container.getContainer(name)
                if ctr:
                    return ctr
        return None

    def getContainerInt(self, containerInt):
        if self.questInt == containerInt:
            return self
        else:
            for container in self.containers:
                ctr = container.getContainerInt(containerInt)
                if ctr:
                    return ctr
        return None

    def completeChildContainers(self):
        for container in self.getContainers():
            container.completeChildContainers()

        self.av.questStatus.updateHistory(self)

    def completePreviousContainers(self, container = None):
        if self.parent:
            self.parent.completePreviousContainers(self)

        if not self.isChoice() and container:
            if self.containers.count(container):
                index = self.containers.index(container)
                for idx in range(0, index):
                    self.containers[idx].completeChildContainers()

            else:
                self.notify.warning("%s not in parent's container list!" % container.getName())

    def printLine(self, indent, text):
        for i in range(0, indent):
            text = ' ' + text

        print(text)

    def printAll(self, indent = 0):
        self.printLine(indent, 'Name: %s Title: %s' % (self.name, self.title))
        self.printLine(indent, 'Giver: %s FirstQuestId: %s' % (self.giverId, self.firstQuestId))
        self.printLine(indent, 'Description: %s' % self.description)
        self.printLine(indent, '--------------------------------------------')
        for container in self.containers:
            container.printAll(indent + 1)


class QuestStub(QuestContainer):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestStub')

    def __init__(self, name, av, questInt, parent, giverId, rewards, complete = False, description = '', goal = 1):
        title = name
        QuestContainer.__init__(self, name, title, av, questInt, parent, giverId, rewards, firstQuestId = name, description = description)
        self.quest = None
        self.goal = goal
        self.complete = complete
        self.processed = False

    def destroy(self):
        self.quest = None
        QuestContainer.destroy(self)

    def linkQuest(self, quest):
        if quest.getQuestId() == self.name:
            self.quest = quest
            if quest.isDroppable():
                self.acceptOnce(quest.getDroppedEventString(), self.handleQuestDropped)

            self.complete = False
            return True
        else:
            return False

    def unlinkQuest(self, questId):
        if questId == self.name:
            if self.quest == None:
                self.notify.warning('Unlinking empty quest stub: %s' % self.name)

            self.ignore(self.quest.getDroppedEventString())
            self.quest = None
            return True
        else:
            return False

    def hasQuest(self, questId):
        return self.name == questId

    def assignFirstQuest(self, completedQuests):
        if not self.name:
            self.notify.warning('QuestStub no quest to assignFirstQuest!')
            return

        self.assignQuest(completedQuests, self.giverId, [self.name], [self.rewards])

    def handleQuestComplete(self, quest, prevCompletedQuests = []):
        self.notify.debug('QStub.handleQuestComplete.SELF.QUEST_INT: %s' % self.questInt)
        self.notify.debug('QS.handleQuestComplete.quest: %s' % quest)
        self.notify.debug('QS.handleQuestComplete.PREV_COMPLETED_QUESTS: %s' % prevCompletedQuests)
        self.notify.debug('QS.handleQuestComplete.SELF.COMPLETED_QUESTS: %s' % self.completedQuests)
        self.notify.debug('QS.handleQuestComplete.IS_COMPLETE: %s' % self.isComplete())
        self.notify.debug('QS.handleQuestComplete.SELF.av.queststatus.NPC_Interact_Mode: %s' % self.av.questStatus.getNPCInteractMode())
        if self.complete:
            return False

        if self.av.questStatus.getNPCInteractMode() == False:
            self.complete = True
            if len(self.completedQuests) > 0:
                self.notify.warning('self.completedQuests is not empty after getNPCInteractMode is reset False (interaction with npc is done)')

            self.completedQuests = [
                quest]
            self.processed = True
            self.parent.handleQuestComplete(quest, self, self.completedQuests)

        return True

    def handleQuestDropped(self, quest):
        self.complete = False
        self.parent.handleQuestDropped(quest)

    def percentComplete(self, history):
        if self.complete:
            return (self.goal, self.goal)
        elif self.getQuestInt() in history:
            self.complete = True
            return (self.goal, self.goal)

        totProg = 0
        totGoal = 0
        if self.quest:
            for prog in self.quest.getTaskProgress():
                (progress, goal) = prog
                totProg += progress
                totGoal += goal

        return (totProg, totGoal)

    def isComplete(self, showComplete = False):
        if showComplete:
            if self.quest:
                return self.quest.isComplete()
            else:
                return self.getComplete()

        if self.quest:
            if self.processed:
                return self.quest.isComplete()
            else:
                return False

        return self.getComplete()

    def getFirstQuestId(self):
        return self.name

    def getTaskProgress(self):
        if self.quest:
            return self.quest.getTaskProgress()

        return []


class QuestChoice(QuestContainer):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestChoice')
    CompleteAll = -1

    def __init__(self, name, title, av, questInt, parent, giverId, rewards, description = '', completeCount = -1):
        firstQuestId = None
        QuestContainer.__init__(self, name, title, av, questInt, parent, giverId, rewards, firstQuestId, description)
        self.revisitQuestId = '%s-revisit' % self.name
        self.completeCount = completeCount
        self.completeCountVerified = False

    def isChoice(self):
        return True

    def __verifyCompleteCount(self):
        if not self.completeCountVerified:
            if self.completeCount == self.CompleteAll:
                self.completeCount = len(self.getContainers())

            self.completeCountVerified = True

    def getProgress(self, showComplete = False):
        self.__verifyCompleteCount()
        compCont = 0
        history = []
        if self.av:
            history = self.av.getQuestLadderHistory()

        for container in self.getContainers():
            if container.isComplete(showComplete) or container.getQuestInt() in history:
                compCont += 1

        return (compCont, self.completeCount, len(self.getContainers()))

    def getValidContainers(self):
        quests = self.av.questStatus.getCurrentQuests()
        containers = self.getContainers()
        validContainers = []
        for container in containers:
            valid = True
            for quest in quests:
                if container.hasQuest(quest.getQuestId()):
                    valid = False
                    break

            if valid:
                validContainers.append(container)

        return validContainers

    def isComplete(self, showComplete = False):
        self.__verifyCompleteCount()
        compCont = 0
        for container in self.getContainers():
            if container.isComplete(showComplete):
                compCont += 1

        return compCont == self.completeCount

    def chooseQuest(self, nextQuestId, giverId, rewards, callback = None):
        if len(self.completedQuests):
            pass

        container = self.getContainer(nextQuestId)
        if container:
            nextQuestId = container.getFirstQuestId()

        self.assignQuest(self.completedQuests, self.giverId, nextQuestId, rewards = rewards, callback = callback)
        self.completedQuests = []

    def assignFirstQuest(self, completedQuests):
        nextQuestIds = []
        rewards = []
        for container in self.getContainers():
            nextQuestIds.append(container.getQuestId())
            rewards.append(container.getRewards())

        self.assignQuest(completedQuests, self.giverId, nextQuestIds, rewards)

    def updateCompletedQuests(self, completedQuest, prevCompletedQuests = []):
        self.notify.debug('QChoice.updateCompletedQuests.SELF.QUEST_INT: %s' % self.questInt)
        self.notify.debug('QChoice.updateCompletedQuests.completedQuest: %s' % completedQuest)
        if completedQuest in self.completedQuests:
            self.notify.warning('Quest: %s already in completedQuests!' % completedQuest.getQuestId())
        else:
            self.completedQuests.append(completedQuest)

    def advance(self, completedContainer):
        pass

    def handleQuestDropped(self, droppedQuest):
        quests = self.av.questStatus.getCurrentQuests()
        found = 0
        if quests:
            droppedQuestId = droppedQuest.getQuestId()
            for quest in quests:
                if quest.getQuestId() != droppedQuestId and self.hasQuest(quest.getQuestId()):
                    found = 1
                    break

        if not found:
            if self.revisitQuestId:
                self.assignQuest([
                    droppedQuest], self.giverId, self.revisitQuestId, self.rewards)
            else:
                self.notify.warning('RevisitQuestId not defined for: %s' % self.getName())
                self.av._dropQuest(droppedQuest)
        else:
            self.av._dropQuest(droppedQuest)


class QuestLadder(QuestContainer):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestLadder')

    def isComplete(self, showComplete = False):
        return self.containers[-1].isComplete(showComplete)

    def percentCompleteR(self, history):
        if self.getQuestInt() in history:
            return (self.goal, self.goal)

        totCompCont = 0
        totCont = 0
        containers = self.getContainers()
        length = len(containers)
        for index in range(length - 1, -1, -1):
            (compCont, cont) = containers[index].percentComplete()
            totCompCont += compCont
            totCont += cont
            if compCont > 0:
                for tindex in range(0, index):
                    (compCont, cont) = containers[tindex].percentComplete()
                    totCompCont += cont
                    totCont += cont

                break

        return (totCompCont, totCont)


class QuestChoiceSingle(QuestLadder):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestChoiceSingle')
