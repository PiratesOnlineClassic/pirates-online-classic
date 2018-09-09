from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from direct.fsm.FSM import FSM

from otp.distributed.OtpDoGlobals import *
from otp.ai.MagicWordGlobal import *

from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.npc.DistributedNPCTownfolkAI import DistributedNPCTownfolkAI
from pirates.quest.DistributedQuestAI import DistributedQuestAI
from pirates.quest.QuestTaskState import QuestTaskState
from pirates.quest.QuestRewardStruct import QuestRewardStruct
from pirates.quest import QuestEvent
from pirates.quest import QuestDB
from pirates.quest import QuestLadderDB
from pirates.quest.QuestPath import QuestStep
from pirates.quest.QuestLadderDNA import QuestLadderDNA
from pirates.quest import QuestTaskDNA
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.world.DistributedIslandAI import DistributedIslandAI
from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI
from pirates.world.DistributedBuildingDoorAI import DistributedBuildingDoorAI
from pirates.world.DistributedInteriorDoorAI import DistributedInteriorDoorAI
from pirates.world.DistributedDinghyAI import DistributedDinghyAI
from pirates.uberdog.UberDogGlobals import InventoryCategory


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

        fields = {
            'setQuestId': (questId,),
            'setGiverId': ('',),
            'setCombineOp': (0,),
            'setTaskStates': ([QuestTaskState()],),
            'setRewardStructs': ([],),
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

        # update the player's quest list on their inventory...
        questList.remove(quest.doId)
        inventory.setQuestList(questList)

        # update the player's quest history so that we will not ever give
        # the player the same quest again...
        questHistory = avatar.getQuestHistory()
        questHistory.append(quest.questDNA.getQuestInt())
        avatar.b_setQuestHistory(questHistory)

        # finally, deactivate the old quest.
        self.deactivateQuest(avatar, quest.doId)
        messenger.send(quest.getDroppedEventString())

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

    def completeQuest(self, avatar, quest):
        path = QuestLadderDB.getFamePath(quest.questId)
        if not path:
            path = QuestLadderDB.getFortunePath(quest.questId)

        if not path:
            self.notify.debug('Failed to complete quest %s for avatar %d, '
                'no path found!' % (quest.getQuestId(), avatar.doId))

            return

        for questLadder in path:
            if isinstance(questLadder, QuestLadderDNA):
                containers = questLadder.getContainers()
                if not containers:
                    continue

                currentQuestIndex = None
                for index in xrange(len(containers)):
                    questDNA = containers[index]
                    if questDNA.getQuestId() == quest.getQuestId():
                        currentQuestIndex = index
                        break
            else:
                currentQuestIndex = path.index(questLadder)

            if not currentQuestIndex:
                continue

            # get the next quest in the quest ladder DNA.
            try:
                nextQuestDNA = containers[currentQuestIndex + 1]
            except IndexError:
                return

            def questCreatedCallback():
                avatar.b_setActiveQuest(nextQuestDNA.getQuestId())

            # drop the avatar's previous quest and give them the new quest
            # appropriate to their current quest path...
            self.dropQuest(avatar, quest)
            self.createQuest(avatar, nextQuestDNA.getQuestId(),
                questCreatedCallback)

            break

    def __completeTaskState(self, avatar, questEvent, callback=None):
        activeQuest = self.getQuest(avatar, questId=avatar.getActiveQuest())
        if not activeQuest:
            return

        taskDNAs = activeQuest.questDNA.getTaskDNAs()
        taskStates = activeQuest.getTaskStates()

        taskDNA = None
        taskState = None

        # iterate through all of the task states and check to see if we
        # have successfully completed one...
        for index in xrange(len(taskStates)):
            taskDNA = taskDNAs[index]
            taskState = taskStates[index]

            if questEvent.applyTo(taskState, taskDNA):
                taskDNA.complete(questEvent, taskState)
                break

        if not taskDNA and not taskState:
            return

        # update the active quest's new task states.
        activeQuest.b_setTaskStates(taskStates)

        # check to see if the task state event has been completed.
        if taskState.isComplete():
            if callback is not None:
                callback(taskDNA, taskState)
            else:
                self.completeQuest(avatar, activeQuest)

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

            def finalizeCallback(isDialog=False):
                # TODO: handle quest choices!
                self.completeQuest(avatar, activeQuest)

            taskStates = activeQuest.getTaskStates()
            taskIndex = taskStates.index(taskState)

            try:
                finalizeInfo = activeQuest.questDNA.getFinalizeInfo()[taskIndex]
            except IndexError:
                # looks like this quest has no finalize info, let's just
                # give the avatar their next quest...
                self.completeQuest(avatar, activeQuest)
                return

            finalizeType = finalizeInfo['type']
            if finalizeType == 'cutscene':
                self.acceptOnce('quest-finalize-%d' % activeQuest.doId, finalizeCallback)
                activeQuest.d_startFinalizeScene(taskIndex, npc.doId)
            elif finalizeType == 'dialog':
                self.acceptOnce('dialog-complete-%d' % activeQuest.doId, finalizeCallback, extraArgs=[True])
                npc.d_playDialogMovie(avatar.doId, finalizeInfo['sceneId'])
            else:
                self.notify.warning('Failed to handle interact callback with npc %d for avatar %d '
                    'with unknown finalizeType: %s!' % (npc.doId, avatar.doId, finalizeType))

                return

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

        self.__completeTaskState(avatar, questEvent)

        # update the avatar's gold in pocket
        inventory.setGoldInPocket(inventory.getGoldInPocket() - goldAmount)

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
                return None

            otherParent = otherObject.getParentObj()
            if not otherParent:
                return None

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
        return 'Could not find active quest: %s' % questId

    simbase.air.questMgr.dropQuest(invoker, activeQuest.doId)
    return 'Dropped active quest: %s!' % questId

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def dropAllQuests():
    simbase.air.questMgr.dropQuests(spellbook.getInvoker())
    return 'Dropped all active quests.'
