from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from direct.fsm.FSM import FSM

from otp.distributed.OtpDoGlobals import *
from otp.ai.MagicWordGlobal import *

from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.cutscene import CutsceneData
from pirates.npc.DistributedNPCTownfolkAI import DistributedNPCTownfolkAI
from pirates.quest.DistributedQuestAI import DistributedQuestAI
from pirates.quest.QuestTaskState import QuestTaskState
from pirates.quest.QuestReward import *
from pirates.quest.QuestRewardStruct import QuestRewardStruct
from pirates.quest import QuestEvent
from pirates.quest import QuestDB
from pirates.quest import QuestLadderDB
from pirates.quest.QuestPath import QuestStep
from pirates.quest.QuestLadderDNA import QuestLadderDNA, QuestContainerDNA
from pirates.quest import QuestTaskDNA
from pirates.piratesbase import PiratesGlobals
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.world.DistributedIslandAI import DistributedIslandAI
from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI
from pirates.world.DistributedBuildingDoorAI import DistributedBuildingDoorAI
from pirates.world.DistributedInteriorDoorAI import DistributedInteriorDoorAI
from pirates.world.DistributedDinghyAI import DistributedDinghyAI
from pirates.uberdog.UberDogGlobals import InventoryCategory
from pirates.tutorial import TutorialGlobals


class QuestOperationFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestOperationFSM')

    def __init__(self, air, avatar, callback=None):
        FSM.__init__(self, self.__class__.__name__)

        self.air = air
        self.avatar = avatar
        self.callback = callback

    def enterOff(self):
        pass

    def exitOff(Self):
        pass

    def cleanup(self, *args, **kwargs):
        del self.air.questMgr.avatar2fsm[self.avatar.doId]
        self.ignoreAll()
        self.demand('Off')

        if self.callback:
            self.callback(*args, **kwargs)

class CreateQuestFSM(QuestOperationFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('CreateQuestFSM')

    def enterStart(self, questId):
        self.inventory = self.avatar.getInventory()
        if not self.inventory:
            self.notify.warning('Failed to create quest %s for avatar %d, '
                'no inventory found!' % (questId, self.avatar.doId))

            self.cleanup()
            return

        questDNA = QuestDB.QuestDict.get(questId)
        if not questDNA:
            self.notify.warning('Failed to create quest %s for avatar %d, '
                'quest is invalid!' % (questId, self.avatar.doId))

            self.cleanup()
            return

        fields = {
            'setQuestId': (questId,),
            'setGiverId': ('',),
            'setCombineOp': (questDNA.getCombineOp(),),
            'setTaskStates': (questDNA.getInitialTaskStates(self.avatar),),
            'setRewardStructs': ([reward.getQuestRewardStruct() for reward in questDNA.getRewards()],),
        }

        def questCreatedCallback(questDoId):
            if not questDoId:
                self.notify.warning('Failed to create quest %s for avatar %d!' % (
                    questId, self.avatar.doId))

                self.cleanup()
                return

            def questActivatedCallback(quest):
                if not quest:
                    self.notify.warning('Failed to activate quest %d for avatar %d, '
                        'quest failed to generate!' % (questDoId, self.avatar.doId))

                    self.cleanup()
                    return

                # update the avatar's quest list so the quest will be stored in
                # the database so we can retrieve and activate it later...
                questList = self.inventory.getDoIdListCategory(InventoryCategory.QUESTS)
                questList.append(questDoId)
                self.inventory.setQuestList(questList)

                # update the avatar's active quest...
                self.avatar.b_setActiveQuest(quest.getQuestId())

                # we're done.
                self.cleanup()

            self.air.questMgr.activateQuest(self.avatar, questDoId,
                questActivatedCallback)

        self.air.dbInterface.createObject(self.air.dbId,
            self.air.dclassesByName['DistributedQuestAI'],
            fields,
            questCreatedCallback)

    def exitStart(self):
        pass

class ActivateQuestsFSM(QuestOperationFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('ActivateQuestsFSM')

    def enterStart(self):
        self.inventory = self.avatar.getInventory()
        if not self.inventory:
            self.notify.warning('Failed to activate quests for avatar %d, '
                'no inventory found!' % (questId, self.avatar.doId))

            self.cleanup()
            return

        self.questList = self.inventory.getDoIdListCategory(InventoryCategory.QUESTS)
        if not self.questList:
            self.cleanup()
            return

        for questDoId in self.questList:
            # check to see if the quest object has already been generated,
            # we do not want to regenerate the object over again...
            if questDoId in self.air.doId2do:
                continue

            def queryQuestCallback(dclass, fields, questDoId=questDoId):
                if not dclass and not fields:
                    self.notify.warning('Failed to query quest %d, quest not found!' % (
                        questDoId))

                    self.cleanup()
                    return

                def questActivatedCallback(quest):
                    if not quest:
                        self.notify.warning('Failed to activate quest %d for avatar %d, '
                            'quest failed to generate!' % (questDoId, self.avatar.doId))

                        self.cleanup()
                        return

                    self.questList.remove(questDoId)
                    if not self.questList:
                        self.cleanup()

                self.air.questMgr.activateQuest(self.avatar, questDoId,
                    questActivatedCallback)

            self.air.dbInterface.queryObject(self.air.dbId,
                questDoId,
                queryQuestCallback,
                self.air.dclassesByName['DistributedQuestAI'])

    def exitStart(self):
        pass

class QuestManagerAI(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestManagerAI')

    def __init__(self, air):
        self.air = air
        self.avatar2fsm = {}
        self.quests = {}

    def runQuestFSM(self, fsmtype, avatar, *args, **kwargs):
        if avatar.doId in self.avatar2fsm:
            self.notify.debug('Failed to run quest FSM for avatar %d, '
                'an FSM already running!' % avatar.doId)

            return

        callback = kwargs.pop('callback', None)

        self.avatar2fsm[avatar.doId] = fsmtype(self.air, avatar, callback)
        self.avatar2fsm[avatar.doId].request('Start', *args, **kwargs)

    def hasQuest(self, avatar, questDoId=None, questId=None):
        return self.getQuest(avatar, questDoId, questId) is not None

    def createQuest(self, avatar, questId, callback=None):
        self.runQuestFSM(CreateQuestFSM, avatar, questId, callback=callback)

    def activateQuest(self, avatar, questDoId, callback):
        activeQuests = self.quests.setdefault(avatar.doId, {})
        if questDoId in activeQuests:
            self.notify.warning('Cannot add a new quest %d for avatar %d, '
                'quest already added!' % (questDoId, avatar.doId))

            return

        def questArrivedCallback(quest):
            if not quest:
                self.notify.warning('Failed to activate quest %d for avatar %d!' % (
                    questDoId, avatar.doId))

                # call the callback and let them know the quest failed
                # to activate on the dbss...
                callback(None)
                return

            # TODO FIXME!
            # set the owner of the quest object, this will then send an
            # OwnerView object generate to the client...
            #channel = avatar.getDISLid() << 32 | avatar.doId
            #self.air.setOwner(quest.doId, channel)

            # store the new quest object to the dictionary of quest objects
            # so we can keep track of it for later use...
            self.quests[avatar.doId][quest.doId] = quest
            quest.setOwnerId(avatar.doId)
            avatar.questStatus.assignQuest(quest)

            # finally, call the callback specified and let them know,
            # the quest has been activated...
            callback(quest)

        self.acceptOnce('generate-%d' % questDoId, questArrivedCallback)
        self.air.sendActivate(questDoId, self.air.districtId, OTP_ZONE_ID_MANAGEMENT,
            self.air.dclassesByName['DistributedQuestAI'])

    def activateQuests(self, avatar, callback=None):
        self.runQuestFSM(ActivateQuestsFSM, avatar, callback=callback)

    def deactivateQuest(self, avatar, questDoId):
        if not self.hasQuest(avatar, questDoId):
            self.notify.warning('Cannot drop deactivate %d for avatar %d, '
                'quest never added!' % (questDoId, avatar.doId))

            return

        quest = self.quests[avatar.doId].pop(questDoId)
        quest.requestDelete()
        del quest

    def deactivateQuests(self, avatar):
        if avatar.doId not in self.quests:
            return

        for questDoId in list(self.quests[avatar.doId]):
            self.deactivateQuest(avatar, questDoId)

    def dropQuest(self, avatar, quest):
        if not self.hasQuest(avatar, quest.doId):
            self.notify.warning('Cannot drop quest %d for avatar %d, '
                'quest never added!' % (quest.doId, avatar.doId))

            return

        inventory = avatar.getInventory()
        if not inventory:
            self.notify.debug('Failed to drop quest %d for avatar %d, '
                'no inventory found!' % (quest.doId, avatar.doId))

            return

        questList = inventory.getDoIdListCategory(InventoryCategory.QUESTS)
        if quest.doId not in questList:
            self.notify.warning('Cannot drop quest %d for avatar %d, '
                'quest not found!' % (quest.doId, avatar.doId))

            return

        questStub = avatar.questStatus.getQuestStub(quest.getQuestId())
        avatar.questStatus.handleQuestDropped(quest, questStub)

        # update the player's quest list on their inventory...
        questList.remove(quest.doId)
        inventory.setQuestList(questList)

        # update the player's quest history so that we will not ever give
        # the player the same quest again...
        questHistory = avatar.getQuestHistory()
        questHistory.append(quest.questDNA.getQuestInt())
        avatar.b_setQuestHistory(questHistory)

        # check to see if this quest is the avatar's active quest,
        # if so then let's clear their active quest...
        if quest.getQuestId() == avatar.getActiveQuest():
            avatar.b_setActiveQuest('')

        # finally, deactivate the old quest.
        messenger.send(quest.getDroppedEventString())
        self.deactivateQuest(avatar, quest.doId)

    def dropQuests(self, avatar):
        if avatar.doId not in self.quests:
            return

        for quest in list(self.quests[avatar.doId].values()):
            self.dropQuest(avatar, quest)

    def getQuest(self, avatar, questDoId=None, questId=None):
        if not questDoId and not questId:
            return None

        if avatar.doId not in self.quests:
            return None

        questList = self.quests[avatar.doId]
        if questId is not None:
            for quest in list(questList.values()):
                if quest.questId == questId:
                    return quest

        return questList.get(questDoId)

    def getQuestPath(self, questId):
        return QuestLadderDB.getFamePath(questId) or QuestLadderDB.getFortunePath(questId)

    def getActiveTask(self, quest):
        activeTask = None
        for task, taskState in zip(quest.getTasks(), quest.getTaskStates()):
            if taskState.isComplete():
                continue

            activeTask = task
            break

        return activeTask

    def __giveRewards(self, avatar, rewards=[]):
        if not rewards:
            self.notify.debug('Failed to give rewards for avatar %d, '
                'no rewards specified!' % avatar.doId)

            return

        trade = self.air.tradeMgr.createTrade(avatar.doId)
        for reward in rewards:
            reward.applyTo(trade, avatar)

    def completeQuest(self, avatar, quest):
        # update the quest task states...
        quest.b_setTaskStates(quest.getTaskStates())

        # give the avatar their quest reward(s)...
        self.__giveRewards(avatar, quest.getRewards())

        questStub = avatar.questStatus.getQuestStub(quest.getQuestId())
        questStub.handleQuestComplete(quest, questStub.getContainer(quest.getQuestId()))

    def __completeTaskState(self, avatar, questEvent, callback=None):
        activeQuest = self.getQuest(avatar, questId=avatar.getActiveQuest())
        if not activeQuest:
            self.notify.debug('Failed to complete task state for avatar %d, '
                'avatar has no active quest!' % avatar.doId)

            return

        tasks = activeQuest.getTasks()
        taskStates = activeQuest.getTaskStates()

        currentTask = None
        currentTaskState = None

        for task, taskState in zip(tasks, taskStates):
            # check to see if the quest event applys to this task state.
            if questEvent.applyTo(taskState, task):
                # check to see if this task state is complete.
                if taskState.isComplete():
                    continue

                task.complete(questEvent, taskState)

                currentTask = task
                currentTaskState = taskState
                break

        if not currentTask and not currentTaskState:
            return

        # check to see if the task state event has been completed.
        if activeQuest.isComplete():
            if callback is not None:
                callback(currentTask, currentTaskState)
            else:
                self.completeQuest(avatar, activeQuest)
        else:
            activeQuest.b_setTaskStates(taskStates)

    def enemyDefeated(self, avatar, enemy):
        parentObj = avatar.getParentObj()
        if not parentObj:
            return

        questEvent = QuestEvent.EnemyDefeated()
        questEvent.setLocation(parentObj.getUniqueId())
        questEvent.setEnemyType(enemy.getAvatarType())
        questEvent.setLevel(enemy.getLevel())
        questEvent.setWeaponType(enemy.getCurrentWeapon()[0])

        self.__completeTaskState(avatar, questEvent)

    def finalizeCutscene(self, avatar, quest, finalizeIndex=0, npc=None):
        taskStates = quest.getTaskStates()
        finalizeInfo = quest.questDNA.getFinalizeInfo()

        def finalize(finalizeIndex):
            quest.setFinalizeStateIndex(finalizeIndex)

            try:
                finalizeStateInfo = finalizeInfo[finalizeIndex]
            except IndexError:
                # looks like this quest has no finalize info, let's just
                # give the avatar their next quest...
                self.completeQuest(avatar, quest)
                return

            def finalizeCompleteCallback():
                quest.d_amFinalized()
                self.completeQuest(avatar, quest)

            def finalizeCallback(isDialog=False):
                if finalizeIndex >= len(finalizeInfo):
                    if not isDialog:
                        questEvent = QuestEvent.CutsceneWatched()
                        questEvent.setNpcId(npc.getUniqueId())
                        self.__completeTaskState(avatar, questEvent, callback=finalizeCompleteCallback)
                    else:
                        finalizeCompleteCallback()
                else:
                    # attempt to handle any explicit cutscene rewards that are not given
                    # specifically by the quest as a reward...
                    if not isDialog:
                        rewards = []
                        sceneId = finalizeStateInfo.get('sceneId', '')
                        if sceneId == CutsceneData.Cutscene2_1:
                            rewards.append(CutlassReward())
                        elif sceneId == CutsceneData.Cutscene2_4:
                            rewards.append(PistolReward())

                        # give the avatar their quest reward(s)...
                        self.__giveRewards(avatar, rewards)

                    finalize(finalizeIndex + 1)

            finalizeType = finalizeStateInfo['type']
            if finalizeType == 'cutscene':
                if npc is not None:
                    giverId = npc.doId
                else:
                    giverId = 0

                sendEvent = finalizeStateInfo.get('sendEvent', '')
                if not sendEvent:
                    self.acceptOnce('quest-finalize-%d' % quest.doId, finalizeCallback)
                else:
                    self.acceptOnce('%s-%d' % (sendEvent, quest.doId), finalizeCallback)

                quest.d_startFinalizeScene(finalizeIndex, giverId)
            elif finalizeType == 'dialog':
                if npc is None:
                    self.notify.warning('Failed to handle interact callback with unknown npc for avatar %d '
                        'with unknown finalizeType: %s!' % (avatar.doId, finalizeType))

                    return

                self.acceptOnce('dialog-complete-%d' % npc.doId, finalizeCallback, extraArgs=[True])
                npc.d_playDialogMovie(avatar.doId, finalizeStateInfo['sceneId'])
            else:
                self.notify.warning('Failed to handle interact callback with npc %d for avatar %d '
                    'with unknown finalizeType: %s!' % (npc.doId, avatar.doId, finalizeType))

                return

        finalize(finalizeIndex)

    def requestInteract(self, avatar, npc):
        activeQuest = self.getQuest(avatar, questId=avatar.getActiveQuest())
        if not activeQuest:
            return

        if isinstance(npc, DistributedNPCTownfolkAI):
            questEvent = QuestEvent.NPCVisited()
            questEvent.setNpcId(npc.getUniqueId())
            questEvent.setAvId(avatar.doId)
        else:
            self.notify.warning('Avatar %d failed to request interact for npc %d, '
                'invalid npc type!' % (avatar.doId, npc.doId))

            return

        def interactCallback(taskDNA, taskState):
            self.finalizeCutscene(avatar, activeQuest, npc=npc)

        self.__completeTaskState(avatar, questEvent, callback=interactCallback)

    def attemptBribeNPC(self, avatar, npc):
        activeQuest = self.getQuest(avatar, questId=avatar.getActiveQuest())
        if not activeQuest:
            return

        inventory = avatar.getInventory()
        if not inventory:
            self.notify.debug('Failed to get quest bribe amount for avatar %d, '
                'avatar has no inventory!' % avatar.doId)

            return

        # figure out how much gold this will cost the player
        # in order to successfully bribe the npc...
        goldAmount = None
        for task in activeQuest.questDNA.getTasks():
            if isinstance(task, QuestTaskDNA.BribeNPCTaskDNA) and task.getNpcId() == npc.getUniqueId():
                goldAmount = task.getGold()
                break

        if not goldAmount:
            self.notify.debug('Failed to get quest bribe amount for avatar %d, '
                'task was not found!' % avatar.doId)

            return

        # check to see if the avatar even has enough gold in their
        # pocket to bribe the npc...
        if inventory.getGoldInPocket() < goldAmount:
            self.notify.debug('Failed to get quest bribe amount for avatar %d, '
                'avatar does not have enough gold %d!' % (avatar.doId, goldAmount))

            return

        questEvent = QuestEvent.NPCBribed()
        questEvent.setNpcId(npc.getDNAId())
        questEvent.setGold(goldAmount)

        def bribeCallback(taskDNA, taskState):
            inventory.setGoldInPocket(inventory.getGoldInPocket() - goldAmount)
            self.completeQuest(avatar, activeQuest)

        self.__completeTaskState(avatar, questEvent, callback=bribeCallback)

    def getQuestStepType(self, goalObject):
        if isinstance(goalObject, DistributedNPCTownfolkAI):
            stepType = QuestStep.STNPC
        elif isinstance(goalObject, DistributedBattleAvatarAI):
            stepType = QuestStep.STNPCEnemy
        elif isinstance(goalObject, DistributedGAInteriorAI):
            stepType = QuestStep.STInteriorDoor
        elif isinstance(goalObject, DistributedBuildingDoorAI):
            stepType = QuestStep.STExteriorDoor
        elif isinstance(goalObject, DistributedDinghyAI):
            stepType = QuestStep.STDinghy
        elif isinstance(goalObject, DistributedGameAreaAI):
            stepType = QuestStep.STArea
        elif isinstance(goalObject, DistributedShipAI):
            stepType = QuestStep.STShip
        else:
            stepType = QuestStep.NullStep

        return stepType

    def getQuestStepObject(self, avatar, goalObject):
        if not goalObject:
            return None

        def findObject(goalObject, otherObject):
            goalParent = goalObject.getParentObj()
            if not goalParent:
                return None, None

            otherParent = otherObject.getParentObj()
            if not otherParent:
                return None, None

            if goalParent.doId != otherParent.doId:
                return findObject(goalParent, otherParent)

            return goalObject, otherObject

        # recurse through the scenegraph and find the target goal object...
        goalObject, otherObject = findObject(goalObject, avatar)

        # interiors are parented under the world instance object,
        # the avatar is parented under the island...
        if isinstance(goalObject, DistributedGAInteriorAI) and isinstance(otherObject, DistributedIslandAI):
            doorLocatorNode = goalObject.getExteriorFrontDoor()
            if not doorLocatorNode:
                doorLocatorNode = goalObject.getExteriorBackDoor()

            if not doorLocatorNode:
                return None

            # check to see if the door locator node's parent object is the
            # same parent object as the avatar's, if so return the door locator node
            # otherwise this means the avatar is located on a different island...
            doorLocatorNodeParent = doorLocatorNode.getParentObj()
            if doorLocatorNodeParent.doId != otherObject.doId:
                return doorLocatorNodeParent
            else:
                return doorLocatorNode

        return goalObject

    def getQuestStep(self, avatar, goalUid):
        goalObject = self.getQuestStepObject(avatar,
            self.air.uidMgr.justGetMeMeObject(goalUid))

        if not goalObject:
            return None, None

        return self.getQuestStepType(goalObject), goalObject

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def giveQuest(questId):
    invoker = spellbook.getInvoker()
    if simbase.air.questMgr.hasQuest(invoker, questId=questId):
        return 'Avatar already has active quest: %s!' % questId

    simbase.air.questMgr.createQuest(invoker, questId)
    return 'Given new active quest: %s.' % questId

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def dropQuest(questId):
    invoker = spellbook.getInvoker()
    activeQuest = simbase.air.questMgr.getQuest(invoker, questId=questId)
    if not activeQuest:
        return 'Could not find active quest: %s!' % questId

    simbase.air.questMgr.dropQuest(invoker, activeQuest.doId)
    return 'Dropped active quest: %s!' % questId

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def dropAllQuests():
    simbase.air.questMgr.dropQuests(spellbook.getInvoker())
    return 'Dropped all active quests.'

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def skipQuest(questId=''):
    invoker = spellbook.getInvoker()
    if not questId:
        questId = invoker.getActiveQuest()

    if not questId:
        return 'You did not provide a valid questId!'

    quest = simbase.air.questMgr.getQuest(invoker, questId=questId)
    for taskState in quest.getTaskStates():
        taskState.forceComplete()

    simbase.air.questMgr.completeQuest(invoker, quest)
    return 'Forced quest: %s completion status.' % questId
