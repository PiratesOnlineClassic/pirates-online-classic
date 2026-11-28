from direct.directnotify import DirectNotifyGlobal
from direct.task.TaskManagerGlobal import *
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.quest import QuestEvent
from pirates.quest import QuestTaskDNA
from pirates.quest.QuestConstants import PropIds, getPropList


class DistributedSearchableContainerAI(DistributedInteractiveAI):
    """
    A barrel, crate or other container pirates can rummage through for
    quest items (RecoverContainerItem tasks).  The search takes searchTime
    seconds, after which the avatar's quests decide whether the item was found.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSearchableContainerAI')

    # The client sets up its interaction as non-exclusive, several pirates
    # may search the same container at once.
    MULTIUSE = True

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)

        self.color = [1.0, 1.0, 1.0, 1.0]
        self.scale = [1, 1, 1]
        self.searchTime = 0.0
        self.type = 'Crate'
        self.sphereScale = 1.0
        self.searchers = {}

    def delete(self):
        for avatarId in list(self.searchers.keys()):
            self.__stopSearch(avatarId)

        DistributedInteractiveAI.delete(self)

    def handleRequestInteraction(self, avatar, interactType, instant):
        if avatar.doId in self.searchers:
            return self.DENY

        if not self.hasSearchableTask(avatar):
            # nothing in here the avatar is looking for
            return self.DENY

        return self.ACCEPT

    def handlePostRequestInteraction(self, avatar):
        self.d_startSearching(avatar.doId)
        self.searchers[avatar.doId] = avatar
        self.acceptOnce(avatar.getDeleteEvent(), self.__stopSearch, extraArgs=[avatar.doId])
        taskMgr.doMethodLater(self.searchTime, self.__finishSearch,
            self.uniqueName('avatarSearchTask-%d' % avatar.doId),
            extraArgs=[avatar.doId], appendTask=True)

    def handleRequestExit(self, avatar):
        # the avatar gave up searching before the search time was up
        self.__stopSearch(avatar.doId)
        return self.ACCEPT

    def __stopSearch(self, avatarId):
        avatar = self.searchers.pop(avatarId, None)
        if avatar:
            self.ignore(avatar.getDeleteEvent())

        taskMgr.remove(self.uniqueName('avatarSearchTask-%d' % avatarId))

    def __finishSearch(self, avatarId, task=None):
        avatar = self.searchers.get(avatarId)
        self.__stopSearch(avatarId)
        if not avatar:
            return task.done if task else None

        questProgress = self.searchContainer(avatar)
        self.d_stopSearching(avatarId, questProgress)
        self.sendUpdateToAvatarId(avatarId, 'setUserId', [0])
        return task.done if task else None

    def getQuestEvent(self, avatar):
        parentObj = avatar.getParentObj()
        if not parentObj:
            return None

        questEvent = QuestEvent.ContainerSearched()
        questEvent.setLocation(parentObj.getUniqueId())
        questEvent.setContainerId(self.getUniqueId())
        questEvent.setContainerType(self.getType())
        return questEvent

    def _containerMatches(self, taskDNA):
        containerId = taskDNA.getContainerId()
        if containerId == PropIds.ANY_PROP:
            return True

        propList = getPropList(containerId)
        if propList:
            return self.getUniqueId() in propList

        return containerId == self.getUniqueId()

    def _getSearchableTasks(self, avatar, questEvent):
        """
        Returns a list of (quest, taskState) for every container task the
        avatar is working on that this container could hold the item for.
        """

        searchable = []
        quests = self.air.questMgr.getQuestsFromTaskDNAType(avatar, QuestTaskDNA.RecoverContainerItemTaskDNA)
        for quest in quests:
            questDNA = quest.getQuestDNA()
            if not questDNA:
                continue

            for taskDNA, taskState in zip(questDNA.getTasks(), quest.getTaskStates()):
                if not isinstance(taskDNA, QuestTaskDNA.RecoverContainerItemTaskDNA):
                    continue

                if taskState.isComplete() or taskState.hasSearchedContainer(self.getUniqueId()):
                    continue

                if not taskDNA.locationMatches(questEvent) or not self._containerMatches(taskDNA):
                    continue

                searchable.append((quest, taskState))

        return searchable

    def hasSearchableTask(self, avatar):
        questEvent = self.getQuestEvent(avatar)
        if not questEvent:
            return False

        return len(self._getSearchableTasks(avatar, questEvent)) > 0

    def searchContainer(self, avatar):
        """
        Applies the search to the avatar's quests, returns 1 if the avatar
        found a quest item in this container.
        """

        questEvent = self.getQuestEvent(avatar)
        if not questEvent:
            return 0

        madeProgress = False
        searched = []
        for quest, taskState in self._getSearchableTasks(avatar, questEvent):
            if quest not in searched:
                searched.append(quest)

        for quest in searched:
            previousProgress = [state.getProgress() for state in quest.getTaskStates()]
            quest.handleEvent(avatar, questEvent)
            if any(state.getProgress() > previous
                   for state, previous in zip(quest.getTaskStates(), previousProgress)):
                madeProgress = True

            if quest.isComplete() and not quest.completeRequiresVisit():
                if quest.getQuestDNA().getFinalizeInfo():
                    self.air.questMgr.finalizeCutscene(avatar, quest)
                else:
                    self.air.questMgr.completeQuest(avatar, quest)

        return int(madeProgress)

    def d_startSearching(self, avatarId):
        self.sendUpdateToAvatarId(avatarId, 'startSearching', [])

    def d_stopSearching(self, avatarId, questProgress):
        self.sendUpdateToAvatarId(avatarId, 'stopSearching', [questProgress])

    def setSearchTime(self, searchTime):
        self.searchTime = searchTime

    def d_setSearchTime(self, searchTime):
        self.sendUpdate('setSearchTime', [searchTime])

    def b_setSearchTime(self, searchTime):
        self.setSearchTime(searchTime)
        self.d_setSearchTime(searchTime)

    def getSearchTime(self):
        return self.searchTime

    def setType(self, searchType):
        self.type = searchType

    def d_setType(self, searchType):
        self.sendUpdate('setType', [searchType])

    def b_setType(self, searchType):
        self.setType(searchType)
        self.d_setType(searchType)

    def getType(self):
        return self.type

    def setScale(self, scale):
        self.scale = scale

    def d_setScale(self, scale):
        self.sendUpdate('setScale', [scale])

    def b_setScale(self, scale):
        self.setScale(scale)
        self.d_setScale(scale)

    def getScale(self):
        return self.scale

    def setContainerColor(self, color):
        self.color = color

    def d_setContainerColor(self, color):
        self.sendUpdate('setContainerColor', color)

    def b_setContainerColor(self, color):
        self.setContainerColor(color)
        self.d_setContainerColor(color)

    def getContainerColor(self):
        return self.color

    def setSphereScale(self, sphereScale):
        self.sphereScale = sphereScale

    def d_setSphereScale(self, sphereScale):
        self.sendUpdate('setSphereScale', [sphereScale])

    def b_setSphereScale(self, sphereScale):
        self.setSphereScale(sphereScale)
        self.d_setSphereScale(sphereScale)

    def getSphereScale(self):
        return self.sphereScale
