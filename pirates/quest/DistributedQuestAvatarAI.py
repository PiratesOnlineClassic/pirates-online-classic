from direct.directnotify import DirectNotifyGlobal

from pirates.quest.QuestAvatarBase import QuestAvatarBase
from pirates.quest import QuestTaskDNA
from pirates.quest.QuestHolder import QuestHolder
from pirates.uberdog.UberDogGlobals import InventoryCategory
from pirates.piratesbase import Freebooter


class DistributedQuestAvatarAI(QuestAvatarBase, QuestHolder):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedQuestAvatarAI')

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
        self.sendUpdate('setCurrentQuestChoiceContainers', [currentQuestChoiceContainers])

    def b_setCurrentQuestChoiceContainers(self, currentQuestChoiceContainers):
        self.setCurrentQuestChoiceContainers(currentQuestChoiceContainers)
        self.d_setCurrentQuestChoiceContainers(currentQuestChoiceContainers)

    def getCurrentQuestChoiceContainers(self):
        return self.currentQuestChoiceContainers

    def requestActiveQuest(self, activeQuest):
        inventory = self.getInventory()
        if not inventory:
            self.notify.warning('Failed to set active quest for avatar %d, '
                'no inventory found!' % self.doId)

            return

        if not self.air.questMgr.hasQuest(self, questId=activeQuest):
            self.notify.debug('Failed to set active quest %s for avatar %d, '
                'quest not found in the avatar\'s questList!' % (activeQuest, self.doId))

            return

        self.b_setActiveQuest(activeQuest)

    def requestDropQuest(self, questId):
        inventory = self.getInventory()
        if not inventory:
            self.notify.warning('Failed to drop quest for avatar %d, '
                'no inventory found!' % self.doId)

            return

        activeQuest = self.air.questMgr.getQuest(self, questId=questId)
        if not activeQuest:
            self.notify.debug('Failed to drop active quest %s for avatar %d, '
                'quest not found in the avatar\'s questList!' % (activeQuest, self.doId))

            return

        if not activeQuest.isDroppable():
            self.notify.debug('Failed to drop active quest %s for avatar %d, '
                'quest is not droppable!' % (activeQuest, self.doId))

            return

        self.air.questMgr.dropQuest(self, activeQuest)

    def requestQuestStep(self, questId):
        inventory = self.getInventory()
        if not inventory:
            self.notify.warning('Failed to get quest step for avatar %d, '
                'no inventory found!' % self.doId)

            return

        activeQuest = self.air.questMgr.getQuest(self, questId=questId)
        if not activeQuest:
            self.notify.debug('Failed to get step for quest %s for avatar %d, '
                'quest not found in the avatar\'s questList!' % (activeQuest, self.doId))

            return

        if self.activeQuest != questId:
            return

        activeTask = self.air.questMgr.getActiveTask(activeQuest)
        if not activeTask:
            return

        # attempt to get the quest step object in which,
        # the ray of light will hover over...
        goalUid = activeTask.getGoalUid()
        stepType, goalObject = self.air.questMgr.getQuestStep(self, goalUid)
        if not stepType or not goalObject:
            self.sendUpdate('setQuestStep', [[self.doId, 0, 0, [0, 0, 0, 0], '']])
            return

        (x, y, z), (h, p, r) = goalObject.getPos(), goalObject.getHpr()
        self.sendUpdate('setQuestStep', [[self.doId, goalObject.doId, stepType, [x, y, z, h], goalUid]])

    def _swapQuest(self, oldQuests=[], giverId=None, questIds=None, rewards=None):
        inventory = self.getInventory()
        if not inventory:
            self.notify.debug('Failed to swap quests for avatar %d, '
                'no inventory found!' % self.doId)

            return

        if getattr(self, '_questSwapPending', False):
            return
        self._questSwapPending = True
        oldQuests = list(oldQuests)
        questIds = list(questIds or [])

        def _questsCreatedCallback():
            self._questSwapPending = False
            if any(not self.air.questMgr.hasQuest(self, questId=questId)
                   for questId in questIds):
                return

            for quest in oldQuests:
                if self.air.questMgr.hasQuest(self, questDoId=quest.doId):
                    messenger.send(quest.getCompleteEventString())
                    self.air.questMgr.dropQuest(self, quest, completed=True)

            if questIds and questIds[0] in (
                    'Chapter1.rung1', 'Chapter1.rung2', 'Chapter1.rung3',
                    'c2_visit_will_turner'):
                self.b_setActiveQuest(questIds[0])
                messenger.send('quest-available-%s-%d' % (questIds[0], self.doId),
                               [self, inventory.getQuestList()])

        def _startCreation():
            missing = [questId for questId in questIds
                       if not self.air.questMgr.hasQuest(self, questId=questId)]
            if missing:
                self.air.questMgr.createQuests(self, missing, _questsCreatedCallback)
            else:
                _questsCreatedCallback()

        self.air.questMgr.whenQuestIdle(self, _startCreation)

    def _acceptQuest(self, nextQuestId, giverId, rewards):
        inventory = self.getInventory()
        if not inventory:
            self.notify.debug('Failed to accept quest %d for avatar %d, '
                'no inventory found!' % (nextQuestId, self.doId))

            return

        def questCreatedCallback(quest):
            if quest:
                messenger.send('quest-available-%s-%d' % (nextQuestId, self.doId), [self, inventory.getQuestList()])

        self.air.questMgr.createQuest(self, nextQuestId, questCreatedCallback)

    def d_popupProgressBlocker(self, questId):
        self.sendUpdateToAvatarId(self.doId, 'popupProgressBlocker', [questId])
