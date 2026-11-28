import collections

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
from pirates.quest.QuestPath import QuestStep, QuestGoal
from pirates.quest.QuestLadderDNA import QuestLadderDNA, QuestContainerDNA
from pirates.quest.QuestLadder import QuestStub
from pirates.quest.QuestLadderDynMap import QuestLadderDynMap
from pirates.quest.QuestLadderDependency import QuestLadderDependency
from pirates.quest.QuestOffer import QuestOffer
from pirates.quest.QuestLadderOffer import QuestLadderOffer
from pirates.quest import QuestTaskDNA
from pirates.quest.QuestConstants import PropIds, QuestItems, getPropList, getShipList, getTreasureList, getLocationList
from pirates.piratesbase import CollectionMap
from pirates.pirate import AvatarTypes
from pirates.reputation.ReputationGlobals import getLevelFromTotalReputation
from pirates.piratesbase import PiratesGlobals
from pirates.ship import ShipGlobals
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.world.DistributedIslandAI import DistributedIslandAI
from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI
from pirates.world.DistributedBuildingDoorAI import DistributedBuildingDoorAI
from pirates.world.DistributedInteriorDoorAI import DistributedInteriorDoorAI
from pirates.world.DistributedDinghyAI import DistributedDinghyAI
from pirates.world.DistributedGATunnelAI import DistributedGATunnelAI
from pirates.interact.DistributedSearchableContainerAI import DistributedSearchableContainerAI
from pirates.treasuremap.DistributedBuriedTreasureAI import DistributedBuriedTreasureAI
from pirates.uberdog.UberDogGlobals import InventoryCategory, InventoryType
from pirates.uberdog import InventoryInit
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

    def exitOff(self):
        pass

    def cleanup(self, *args, **kwargs):
        del self.air.questMgr.avatar2fsm[self.avatar.doId]
        self.ignoreAll()
        self.demand('Off')

        try:
            if self.callback:
                self.callback(*args, **kwargs)
        finally:
            self.air.questMgr.runDeferredQuestCompletions(self.avatar)


class CreateQuestsFSM(QuestOperationFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('CreateQuestsFSM')

    def createQuestEntry(self, questId, callback=None):
        questDNA = QuestDB.QuestDict.get(questId)
        if not questDNA:
            self.notify.warning('Failed to create quest %s for avatar %d, '
                'quest is invalid!' % (questId, self.avatar.doId))

            return False

        # the quest giver is the npc the avatar was talking to when the
        # quest was handed to them, this is who the quest is returned to...
        giverId = self.air.questMgr.getQuestGiverId(self.avatar)

        # quests accepted from an offer keep the tasks and rewards the avatar
        # was shown, randomized quests would otherwise roll new ones...
        offer = self.air.questMgr.popQuestOffer(self.avatar, questId)
        if offer:
            taskStates = list(offer.getInitialTaskStates())
            rewardStructs = list(offer.getRewardStructs())
        else:
            taskStates = questDNA.getInitialTaskStates(self.avatar)
            rewards = questDNA.getRewards()
            if not rewards:
                rewards = questDNA.computeRewards(taskStates, self.avatar)

            rewardStructs = [reward.getQuestRewardStruct() for reward in rewards]

        fields = {
            'setQuestId': (questId,),
            'setGiverId': (giverId,),
            'setCombineOp': (questDNA.getCombineOp(),),
            'setTaskStates': (taskStates,),
            'setRewardStructs': (rewardStructs,),
        }

        self.air.dbInterface.createObject(self.air.dbId,
            self.air.dclassesByName['DistributedQuestAI'],
            fields,
            callback)

        return True

    def activateQuestEntry(self, questDoId, callback=None):
        if not questDoId:
            self.notify.warning('Failed to create a quest for avatar %d, '
                'quest was never created!' % self.avatar.doId)

            return False

        self.air.questMgr.activateQuest(self.avatar, questDoId, callback)
        return True

    def enterStart(self, questIds):
        if not questIds:
            self.notify.warning('Failed to create quests for avatar %d, '
                'no quest ids provided!' % self.avatar.doId)

            self.cleanup()
            return

        self.inventory = self.avatar.getInventory()
        if not self.inventory:
            self.notify.warning('Failed to create quests for avatar %d, '
                'no inventory found!' % self.avatar.doId)

            self.cleanup()
            return

        # Work from a copy so mutations don't affect the caller's list
        self.pendingQuestIds = list(questIds)

        def _questActivatedCallback(quest):
            if not quest:
                self.notify.warning('Failed to activate a quest for avatar %d, '
                    'quest failed to generate!' % self.avatar.doId)

                self.cleanup()
                return

            # update the avatar's quest list
            questList = self.inventory.getDoIdListCategory(InventoryCategory.QUESTS)
            questList.append(quest.doId)
            self.inventory.setQuestList(questList)

            # check to see if we're done
            self.pendingQuestIds.remove(quest.getQuestId())
            if not self.pendingQuestIds:
                self.cleanup()
            else:
                _createNextQuest()

        def _questCreatedCallback(questDoId):
            if not self.activateQuestEntry(questDoId, _questActivatedCallback):
                self.cleanup()

        def _createNextQuest():
            if not self.createQuestEntry(self.pendingQuestIds[0], callback=_questCreatedCallback):
                self.cleanup()

        _createNextQuest()


class CreateQuestFSM(CreateQuestsFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('CreateQuestFSM')

    def enterStart(self, questId):
        self.inventory = self.avatar.getInventory()
        if not self.inventory:
            self.notify.warning('Failed to create quest %s for avatar %d, '
                'no inventory found!' % (questId, self.avatar.doId))

            self.cleanup(None)
            return

        def _questActivatedCallback(quest):
            if not quest:
                self.notify.warning('Failed to activate quest for avatar %d, '
                    'quest failed to generate!' % self.avatar.doId)

                self.cleanup(None)
                return

            # update the avatar's quest list
            questList = self.inventory.getDoIdListCategory(InventoryCategory.QUESTS)
            questList.append(quest.doId)
            self.inventory.setQuestList(questList)

            # update the avatar's active quest
            self.avatar.b_setActiveQuest(quest.getQuestId())

            # we're done - pass the quest to the callback
            self.cleanup(quest)

        def _questCreatedCallback(questDoId):
            if not self.activateQuestEntry(questDoId, _questActivatedCallback):
                self.cleanup(None)

        if not self.createQuestEntry(questId, _questCreatedCallback):
            self.cleanup(None)

    def exitStart(self):
        pass


class ActivateQuestsFSM(QuestOperationFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('ActivateQuestsFSM')

    def enterStart(self):
        self.inventory = self.avatar.getInventory()
        if not self.inventory:
            self.notify.warning('Failed to activate quests for avatar %d, '
                'no inventory found!' % self.avatar.doId)

            self.cleanup()
            return

        questDoIds = self.inventory.getDoIdListCategory(InventoryCategory.QUESTS)
        if not questDoIds:
            self.cleanup()
            return

        # Count how many quests actually need to be queried from the database.
        # Quests already in doId2do are already live and don't need re-activation.
        self._pendingQuests = sum(
            1 for doId in questDoIds if doId not in self.air.doId2do)

        if not self._pendingQuests:
            self.cleanup()
            return

        for questDoId in questDoIds:
            if questDoId in self.air.doId2do:
                continue

            def _queryQuestCallback(dclass, fields, questDoId=questDoId):
                if not dclass and not fields:
                    self.notify.warning('Failed to query quest %d, quest not found!' % questDoId)
                    self._pendingQuests -= 1
                    if not self._pendingQuests:
                        self.cleanup()
                    return

                def _questActivatedCallback(quest):
                    if not quest:
                        self.notify.warning('Failed to activate quest %d for avatar %d, '
                            'quest failed to generate!' % (questDoId, self.avatar.doId))
                        self._pendingQuests -= 1
                        if not self._pendingQuests:
                            self.cleanup()
                        return

                    self._pendingQuests -= 1
                    if not self._pendingQuests:
                        self.cleanup()

                self.air.questMgr.activateQuest(self.avatar, questDoId, _questActivatedCallback)

            self.air.dbInterface.queryObject(self.air.dbId,
                questDoId,
                _queryQuestCallback,
                self.air.dclassesByName['DistributedQuestAI'])

    def exitStart(self):
        pass


class QuestManagerAI(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestManagerAI')

    def __init__(self, air):
        self.air = air
        self.avatar2fsm = {}
        self.quests = {}
        self.deferredQuestCompletions = {}
        self.questIdleCallbacks = {}
        self.finalizingQuests = set()
        self.completingQuests = set()
        self.tutorialJollyReady = set()
        self.tutorialJollyWaiters = {}
        self.tutorialShipWaits = {}
        self.avatar2questGiver = {}
        self.avatar2questOffer = {}
        self.questDynMap = QuestLadderDynMap()
        self.questDependency = QuestLadderDependency()

        questInts = collections.Counter(questDNA.getQuestInt() for questDNA in QuestDB.QuestDict.values())
        self.sharedQuestInts = set(questInt for questInt, count in questInts.items() if count > 1)

    def hasCompletedQuest(self, avatar, questDNA):
        # a few quests share their quest int with another quest of the same
        # ladder, the quest history can not tell these quests apart...
        questInt = questDNA.getQuestInt()
        if questInt in self.sharedQuestInts:
            return False

        return questInt in avatar.getQuestHistory()

    def setQuestOffer(self, avatar, offer):
        self.avatar2questOffer[avatar.doId] = offer

    def popQuestOffer(self, avatar, questId):
        offer = self.avatar2questOffer.get(avatar.doId)
        if not offer or offer.getQuestId() != questId:
            return None

        del self.avatar2questOffer[avatar.doId]
        return offer

    def setQuestGiverId(self, avatar, giverId):
        self.avatar2questGiver[avatar.doId] = giverId or ''

    def getQuestGiverId(self, avatar):
        return self.avatar2questGiver.get(avatar.doId, '')

    def tutorialJROnStage(self, avatar):
        quest = self.getQuest(avatar, questId='Chapter1.rung3')
        if (not quest or quest.doId in self.tutorialJollyReady or
                quest.getQuestDNA().getQuestInt() in avatar.getQuestHistory()):
            return

        self.tutorialJollyReady.add(quest.doId)
        callback = self.tutorialJollyWaiters.pop(quest.doId, None)
        if callback:
            callback()

    def whenQuestIdle(self, avatar, callback):
        if avatar.doId not in self.avatar2fsm:
            callback()
            return
        callbacks = self.questIdleCallbacks.setdefault(avatar.doId, [])
        if callback not in callbacks:
            callbacks.append(callback)

    def runDeferredQuestCompletions(self, avatar):
        while avatar.doId not in self.avatar2fsm:
            pending = self.deferredQuestCompletions.get(avatar.doId)
            if pending:
                quest = pending.pop(0)
                if self.getQuest(avatar, questDoId=quest.doId) is quest:
                    self.completeQuest(avatar, quest)
                continue
            self.deferredQuestCompletions.pop(avatar.doId, None)
            callbacks = self.questIdleCallbacks.get(avatar.doId)
            if callbacks:
                callbacks.pop(0)()
                continue
            self.questIdleCallbacks.pop(avatar.doId, None)
            return

    def runQuestFSM(self, fsmtype, avatar, *args, **kwargs):
        if avatar.doId in self.avatar2fsm:
            self.notify.warning('Failed to run quest FSM for avatar %d, '
                'an FSM already running!' % avatar.doId)

            return

        callback = kwargs.pop('callback', None)

        self.avatar2fsm[avatar.doId] = fsmtype(self.air, avatar, callback)
        self.avatar2fsm[avatar.doId].request('Start', *args, **kwargs)

    def hasQuest(self, avatar, questDoId=None, questId=None):
        return self.getQuest(avatar, questDoId, questId) is not None

    def createQuest(self, avatar, questId, callback=None):
        self.runQuestFSM(CreateQuestFSM, avatar, questId, callback=callback)

    def createQuests(self, avatar, questIds, callback=None):
        self.runQuestFSM(CreateQuestsFSM, avatar, questIds, callback=callback)

    def activateQuest(self, avatar, questDoId, callback):
        inventory = avatar.getInventory()
        if not inventory:
            self.notify.debug('Failed to activate quest %d for avatar %d, '
                'no inventory found!' % (questDoId, avatar.doId))

            callback(None)
            return

        activeQuests = self.quests.setdefault(avatar.doId, {})
        if questDoId in activeQuests:
            self.notify.warning('Cannot add a new quest %d for avatar %d, '
                'quest already added!' % (questDoId, avatar.doId))

            callback(None)
            return

        def _questArrivedCallback(quest):
            if not quest:
                self.notify.warning('Failed to activate quest %d for avatar %d!' % (questDoId, avatar.doId))
                callback(None)
                return

            channel = avatar.getDISLid() << 32 | avatar.doId
            #self.air.setOwner(quest.doId, channel)

            # store the new quest object to the dictionary of quest objects
            # so we can keep track of it for later use...
            self.quests[avatar.doId][quest.doId] = quest
            quest.setOwnerId(avatar.doId)
            avatar.questStatus.assignQuest(quest, True)

            # finally, call the callback specified and let them know,
            # the quest has been activated...
            callback(quest)

        self.acceptOnce('generate-%d' % questDoId, _questArrivedCallback)
        self.air.sendActivate(questDoId, inventory.doId, OTP_ZONE_ID_MANAGEMENT,
            self.air.dclassesByName['DistributedQuestAI'])

    def activateQuests(self, avatar, callback=None):
        def activated():
            self.restoreQuestChoiceContainers(avatar)
            self.resumeCompletedTutorialQuest(avatar)
            if callback:
                callback()

        self.runQuestFSM(ActivateQuestsFSM, avatar, callback=activated)

    def restoreQuestChoiceContainers(self, avatar):
        # the avatar's quest ladders are only built once their quests have
        # been activated, so the choice containers the avatar was offered
        # before they logged out must be restored afterwards...
        questStatus = avatar.questStatus
        if not questStatus:
            return

        choiceInts = avatar.getCurrentQuestChoiceContainers()
        choiceContainers = []
        for ladder in list(questStatus.ladders.values()):
            ladder.getChoiceContainers(choiceContainers)

        for container in choiceContainers:
            if container.getQuestInt() in choiceInts:
                questStatus.choiceContainers[container.getName()] = container

    def registerQuestChoiceContainer(self, avatar, questId):
        questStub = avatar.questStatus.getQuestStub(questId)
        if not questStub:
            return

        container = questStub.getParent()
        if not container or not container.isChoice():
            return

        if container.getQuestInt() in avatar.getQuestLadderHistory():
            return

        if container.getQuestInt() in avatar.getCurrentQuestChoiceContainers():
            avatar.questStatus.choiceContainers[container.getName()] = container
        else:
            avatar.questStatus.addCurrentQuestChoiceContainer(container)

    def resumeCompletedTutorialQuest(self, avatar):
        for quest in list(self.quests.get(avatar.doId, {}).values()):
            if (quest.getQuestId() in ('Chapter1.rung1', 'Chapter1.rung2',
                                       'Chapter1.rung3', 'c2_visit_will_turner') and
                    quest.getQuestDNA().getQuestInt() in avatar.getQuestHistory()):
                if avatar.doId in self.avatar2fsm:
                    pending = self.deferredQuestCompletions.setdefault(avatar.doId, [])
                    if quest not in pending:
                        pending.append(quest)
                    return
                nextQuestId = avatar.questStatus.getNextQuestId(quest.getQuestId())
                while nextQuestId:
                    nextDNA = QuestDB.QuestDict.get(nextQuestId)
                    if not nextDNA or nextDNA.getQuestInt() not in avatar.getQuestHistory():
                        break
                    nextQuestId = avatar.questStatus.getNextQuestId(nextQuestId)
                if nextQuestId:
                    avatar._swapQuest([quest], questIds=[nextQuestId])
                return

    def deactivateQuest(self, avatar, questDoId):
        if not self.hasQuest(avatar, questDoId):
            self.notify.warning('Cannot drop deactivate %d for avatar %d, '
                'quest never added!' % (questDoId, avatar.doId))

            return

        quest = self.quests[avatar.doId].pop(questDoId)
        self.finalizingQuests.discard(questDoId)
        self.tutorialJollyReady.discard(questDoId)
        self.tutorialJollyWaiters.pop(questDoId, None)
        self.ignore('quest-finalize-%d' % questDoId)
        self.ignore('makeAPirateComplete-%d' % questDoId)
        shipEvent = self.tutorialShipWaits.pop(questDoId, None)
        if shipEvent:
            self.ignore(shipEvent)
        quest.requestDelete()
        del quest

    def deactivateQuests(self, avatar):
        self.deferredQuestCompletions.pop(avatar.doId, None)
        self.questIdleCallbacks.pop(avatar.doId, None)
        self.avatar2questGiver.pop(avatar.doId, None)
        self.avatar2questOffer.pop(avatar.doId, None)
        if avatar.doId not in self.quests:
            return

        for questDoId in list(self.quests[avatar.doId]):
            self.deactivateQuest(avatar, questDoId)

    def dropQuest(self, avatar, quest, completed=False):
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

        if not completed:
            # let the quest's ladder know the quest is being dropped while the
            # quest is still in the avatar's quest list, the ladder may decide
            # to hand the avatar a revisit quest in it's place...
            messenger.send(quest.getDroppedEventString(), [quest])
            if not self.hasQuest(avatar, quest.doId):
                return

        # a dropped quest does not count towards the avatar's quest history,
        # so the quest may be offered to the avatar again...
        questStub = avatar.questStatus.getQuestStub(quest.getQuestId())
        if questStub and questStub.quest is quest:
            questStub.unlinkQuest(quest.getQuestId())

        # update the player's quest list on their inventory...
        questList = inventory.getDoIdListCategory(InventoryCategory.QUESTS)
        if quest.doId in questList:
            questList.remove(quest.doId)
            inventory.setQuestList(questList)

        # check to see if this quest is the avatar's active quest,
        # if so then let's clear their active quest...
        if quest.getQuestId() == avatar.getActiveQuest():
            avatar.b_setActiveQuest('')

        # finally, deactivate the old quest.
        self.deactivateQuest(avatar, quest.doId)

    def dropQuests(self, avatar):
        questList = self.quests.get(avatar.doId)
        if not questList:
            return

        for quest in list(questList.values()):
            self.dropQuest(avatar, quest)

    def getQuest(self, avatar, questDoId=None, questId=None):
        if questDoId is None and questId is None:
            return None

        questList = self.quests.get(avatar.doId)
        if not questList:
            return None

        if questId is not None:
            for quest in list(questList.values()):
                if quest.questId == questId:
                    return quest

        return questList.get(questDoId)

    def getActiveTask(self, quest):
        activeTask = None
        for task, taskState in zip(quest.getTasks(), quest.getTaskStates()):
            if taskState.isComplete():
                continue

            activeTask = task
            break

        return activeTask

    def getQuestsFromTaskDNAType(self, avatar, taskDNAClass):
        """
        Returns a list of active quests the avatar currently has in which it's task DNA
        corresponds to the task dna class type specified
        """

        assert(taskDNAClass is not None)
        questList = self.quests.get(avatar.doId)
        if not questList:
            return []

        quests = []
        for quest in list(questList.values()):
            assert(quest is not None)
            questDNA = quest.getQuestDNA()
            assert(questDNA is not None)

            for taskDNA in questDNA.getTaskDNAs():
                assert(taskDNA is not None)
                if isinstance(taskDNA, taskDNAClass):
                    quests.append(quest)
                    break

        return quests

    def getTaskBribeAmountFromNPC(self, avatar, npcId):
        """
        Returns the amount of gold a task requires for a certain NPC bribe event
        """

        quests = self.getQuestsFromTaskDNAType(avatar, QuestTaskDNA.BribeNPCTaskDNA)
        for quest in quests:
            assert(quest is not None)
            if quest.isComplete():
                continue

            questDNA = quest.getQuestDNA()
            assert(questDNA is not None)

            for taskDNA in questDNA.getTaskDNAs():
                assert(taskDNA is not None)
                if isinstance(taskDNA, QuestTaskDNA.BribeNPCTaskDNA) and taskDNA.getNpcId() == npcId:
                    return taskDNA.getGold()

        return -1

    def _giveRewards(self, avatar, rewards=[]):
        if not rewards:
            return True

        inventory = avatar.getInventory()
        if not inventory:
            self.notify.warning('Cannot give quest rewards to avatar %d: no inventory!' % avatar.doId)
            return False
        trade = self.air.tradeMgr.createTrade(avatar.doId)
        if not trade:
            self.notify.warning('Cannot give quest rewards to avatar %d: no trade available!' % avatar.doId)
            return False
        for reward in rewards:
            if isinstance(reward, CutlassReward):
                if not inventory.getStackQuantity(InventoryType.CutlassToken):
                    trade.giveCutlassTraining()
                if not inventory.getStackQuantity(InventoryType.CutlassWeaponL1):
                    trade.giveStack(InventoryType.CutlassWeaponL1, 1)
            elif isinstance(reward, (LuckReward, SwiftnessReward)):
                # these attributes were never implemented by the game,
                # there is nothing to give the avatar...
                self.notify.warning('Cannot give unsupported quest reward %s to avatar %d!' % (
                    reward.__class__.__name__, avatar.doId))
            else:
                reward.applyTo(trade, avatar)
        return True

    def completeQuest(self, avatar, quest):
        assert(avatar is not None)
        assert(quest is not None)

        if not quest.isComplete():
            self.notify.warning('Failed to handle complete quest for avatar %d, '
                'quest %s was never completed!' % (avatar.doId, quest.getQuestId()))

            return

        if avatar.doId in self.avatar2fsm:
            pending = self.deferredQuestCompletions.setdefault(avatar.doId, [])
            if quest not in pending:
                pending.append(quest)
            return

        self.finalizingQuests.discard(quest.doId)
        questDNA = quest.getQuestDNA()
        assert(questDNA is not None)

        # check to see if we've already completed this quest
        questHistory = avatar.getQuestHistory()
        if self.hasCompletedQuest(avatar, questDNA):
            self.resumeCompletedTutorialQuest(avatar)
            return

        questStub = avatar.questStatus.getQuestStub(quest.getQuestId())
        if not questStub:
            if QuestLadderDB.getFamePath(quest.getQuestId()) or QuestLadderDB.getFortunePath(quest.getQuestId()):
                self.notify.warning('Failed to handle complete quest for avatar %d, '
                    'quest %s does not have a questStub!' % (avatar.doId, quest.getQuestId()))

                return

            # this quest does not belong to a quest ladder (level up, revisit quests),
            # there is no ladder to advance so simply reward the avatar for it...
            self.completeSingleQuest(avatar, quest)
            return

        if (questStub.complete or avatar.questStatus.getNPCInteractMode() or
                quest.doId in self.completingQuests):
            return

        self.completingQuests.add(quest.doId)
        rewards = quest.getRewards()
        mapRewards = [reward for reward in rewards if isinstance(reward, TreasureMapReward)]
        otherRewards = ([reward for reward in rewards if not isinstance(reward, TreasureMapReward)]
                        if mapRewards else rewards)

        def finish(success):
            try:
                if not success:
                    return
                if mapRewards and (self.air.doId2do.get(avatar.doId) is not avatar or
                                   self.getQuest(avatar, questDoId=quest.doId) is not quest):
                    return
                if not self._giveRewards(avatar, otherRewards):
                    return
                questInt = questDNA.getQuestInt()
                questHistory = avatar.getQuestHistory()
                if self.hasCompletedQuest(avatar, questDNA):
                    return
                if questInt not in questHistory:
                    avatar.b_setQuestHistory(questHistory + [questInt])
                checkpoint = questDNA.getCheckPoint()
                if checkpoint != -1 and avatar.getTutorial() < checkpoint:
                    avatar.b_setTutorial(checkpoint)
                questStub.handleQuestComplete(quest, questHistory)
                self.handleChoiceQuestComplete(avatar, quest, questStub)
                self.handleLaddersComplete(avatar)
            finally:
                self.completingQuests.discard(quest.doId)

        if not mapRewards:
            finish(True)
            return
        if len(mapRewards) != 1:
            self.notify.warning('Cannot award multiple treasure maps for quest %s' % quest.getQuestId())
            finish(False)
            return
        trade = self.air.tradeMgr.createTrade(avatar.doId)
        if not trade:
            finish(False)
            return
        try:
            mapRewards[0].applyTo(trade, avatar, finish)
        except Exception:
            self.completingQuests.discard(quest.doId)
            raise

    def completeSingleQuest(self, avatar, quest):
        if quest.doId in self.completingQuests:
            return

        questDNA = quest.getQuestDNA()
        rewards = [reward for reward in quest.getRewards() if not isinstance(reward, TreasureMapReward)]
        self.completingQuests.add(quest.doId)
        try:
            if not self._giveRewards(avatar, rewards):
                return

            questHistory = avatar.getQuestHistory()
            if questDNA.getQuestInt() not in questHistory:
                avatar.b_setQuestHistory(questHistory + [questDNA.getQuestInt()])

            messenger.send(quest.getCompleteEventString())
            self.dropQuest(avatar, quest, completed=True)
        finally:
            self.completingQuests.discard(quest.doId)

    def handleChoiceQuestComplete(self, avatar, quest, questStub):
        # quests handed out by a quest choice are completed one at a time,
        # the choice only advances the ladder once all of it's quests have
        # been completed, so remove the finished quest from the avatar now...
        container = getattr(questStub, 'parent', None)
        if not container or not container.isChoice() or container.isComplete():
            return

        def removeQuest():
            if self.getQuest(avatar, questDoId=quest.doId) is quest:
                messenger.send(quest.getCompleteEventString())
                self.dropQuest(avatar, quest, completed=True)

        self.whenQuestIdle(avatar, removeQuest)

    def getCompletedContainerIds(self, avatar, quest):
        """
        Returns the name of the outermost quest container (quest ladder, chapter or
        quest choice) that will be completed once the quest has been handed in, the
        npc plays the container's dialog instead of the quest's and the whole main
        story ladder also shows the main story reward panel (see
        DistributedQuestGiver.setQuestsCompleted)
        """

        questStatus = getattr(avatar, 'questStatus', None)
        questStub = questStatus.getQuestStub(quest.getQuestId()) if questStatus else None
        if (not isinstance(questStub, QuestStub) or questStub.quest is not quest or
                questStub.complete):
            return []

        # the stub is only treated as complete by it's containers once
        # the quest has been processed, pretend it has been...
        processed = questStub.processed
        questStub.processed = True
        try:
            completedContainer = None
            container = questStub.getParent()
            while container is not None and container.isComplete():
                completedContainer = container
                container = container.getParent()
        finally:
            questStub.processed = processed

        if completedContainer is None or not QuestLadderDB.getContainer(completedContainer.getName()):
            return []

        return [completedContainer.getName()]

    def handleLaddersComplete(self, avatar):
        # quest ladders the avatar has completed are no longer needed, a
        # repeatable quest ladder is rebuilt when it is offered again...
        ladderDeleteList = getattr(avatar.questStatus, 'ladderDeleteList', None)
        if not ladderDeleteList:
            return

        for ladderName in list(ladderDeleteList):
            ladderDeleteList.remove(ladderName)
            self.removeLadderChoiceContainers(avatar, ladderName)
            avatar.questStatus.deleteLadder(ladderName)

    def removeLadderChoiceContainers(self, avatar, ladderName):
        # a ladder that ends with a quest choice only adds itself to the ladder
        # history once completed, not it's final choice. the choice must not stay
        # behind in the avatar's current choices once the ladder is gone...
        ladder = avatar.questStatus.ladders.get(ladderName)
        if not ladder:
            return

        choiceContainers = []
        ladder.getChoiceContainers(choiceContainers)
        for container in choiceContainers:
            if (container.getQuestInt() in avatar.getCurrentQuestChoiceContainers() or
                    avatar.questStatus.choiceContainers.get(container.getName()) is container):
                avatar.questStatus.removeCurrentQuestChoiceContainer(container)

    def completeTaskState(self, avatar, questEvent, callback=None):
        questObjects = list(self.quests.get(avatar.doId, {}).values())
        if not questObjects:
            return False

        completed = False
        for quest in questObjects:
            if quest.getQuestDNA() is None:
                continue

            if quest.isComplete():
                if (callback is None and not quest.getQuestDNA().getFinalizeInfo() and
                        not quest.completeRequiresVisit() and
                        quest.getQuestDNA().getQuestInt() not in avatar.getQuestHistory()):
                    self.completeQuest(avatar, quest)
                    continue
                if (callback is not None and
                        isinstance(questEvent, QuestEvent.NPCVisited) and
                        quest.doId not in self.finalizingQuests and
                        quest.getQuestDNA().getQuestInt() not in avatar.getQuestHistory() and
                        any(isinstance(task, QuestTaskDNA.VisitTaskDNA) and
                            task.locationMatches(questEvent) and
                            task.getNpcId() == questEvent.getNpcId()
                            for task in quest.getQuestDNA().getTasks())):
                    callback(quest)
                    return True
                continue

            # treasure collections are delivered by handing over the collection pieces...
            collectionTasks = self.getCollectionDeliverTasks(avatar, quest, questEvent)
            if collectionTasks is None:
                continue

            isActiveQuest = quest.getQuestId() == avatar.getActiveQuest()
            if isActiveQuest:
                previousGoal = self.getQuestStepGoalKey(avatar, quest)

            quest.handleEvent(avatar, questEvent)
            for taskState, collectionId in collectionTasks:
                if taskState.isComplete():
                    self.takeCollection(avatar, collectionId)

            # the client only asks for a new quest step when it changes areas, let it
            # know when the active quest's goal has moved on to another task or npc...
            if isActiveQuest and self.getQuestStepGoalKey(avatar, quest) != previousGoal:
                self.updateQuestStep(avatar, quest)

            # check to see if the quest event has been completed,
            # if so then handle the callback we set...
            if quest.isComplete():
                if callback is not None:
                    callback(quest)
                    return True

                # quests completed out in the world are handed in to the npc
                # that gave the quest, unless the quest says otherwise...
                if not quest.completeRequiresVisit():
                    self.setQuestGiverId(avatar, '')
                    finalizeInfo = quest.getQuestDNA().getFinalizeInfo()
                    if finalizeInfo and all(info.get('type') == 'cutscene' for info in finalizeInfo):
                        self.finalizeCutscene(avatar, quest)
                    else:
                        self.completeQuest(avatar, quest)

                completed = True

        return completed

    # the treasure collection quests ask the avatar to deliver a whole treasure
    # collection, the collection is unlocked by the previous quest of the ladder
    # (see the CollectReward of tr.3visitElizabeth, tt.2recoverTooth, tm.1visitWill,
    # trr.1visitBarbossa, tc.2poker and tf.1visitTia). the number of items the task
    # asks for is the number of pieces the collection needs (CollectionMap.Collection_Needed)...
    DeliverCollections = {
        QuestItems.Painting: InventoryType.Collection_Set3,
        QuestItems.Tooth: InventoryType.Collection_Set5,
        QuestItems.Medal: InventoryType.Collection_Set4,
        QuestItems.Ring: InventoryType.Collection_Set6,
        QuestItems.ChessPiece: InventoryType.Collection_Set7,
        QuestItems.Figurine: InventoryType.Collection_Set8,
    }

    def getCollectionPieces(self, collectionId):
        return [(collectionId + 1 + i, CollectionMap.Collection_Needed.get(collectionId + 1 + i, 1))
                for i in range(CollectionMap.Collection_Set_Sizes.get(collectionId, 0))]

    def hasCollection(self, avatar, collectionId):
        inventory = avatar.getInventory()
        if not inventory:
            return False

        return all(inventory.getStackQuantity(pieceId) >= needed
                   for pieceId, needed in self.getCollectionPieces(collectionId))

    def takeCollection(self, avatar, collectionId):
        inventory = avatar.getInventory()
        if not inventory:
            return

        for pieceId, needed in self.getCollectionPieces(collectionId):
            quantity = inventory.getStackQuantity(pieceId)
            inventory.b_setStackQuantity(pieceId, max(0, quantity - needed))

    def getCollectionDeliverTasks(self, avatar, quest, questEvent):
        """
        Returns the (taskState, collectionId) pairs of the quest's incomplete collection
        deliver tasks the npc visit applies to, or None when the avatar has not yet
        found every piece of a collection the npc is waiting for
        """

        if not isinstance(questEvent, QuestEvent.NPCVisited):
            return []

        collectionTasks = []
        for taskDNA, taskState in zip(quest.getQuestDNA().getTasks(), quest.getTaskStates()):
            if type(taskDNA) is not QuestTaskDNA.DeliverItemTaskDNA or taskState.isComplete():
                continue

            # only the tasks asking for the whole collection, a single medal
            # handed to Will Turner is not the medal collection...
            collectionId = self.DeliverCollections.get(taskDNA.getItem())
            if collectionId is None or taskDNA.getNpcId() != questEvent.getNpcId():
                continue

            if taskDNA.getNum() != sum(needed for pieceId, needed in self.getCollectionPieces(collectionId)):
                continue

            if not DistributedQuestAI.taskLocationMatches(taskDNA, questEvent):
                continue

            if not self.hasCollection(avatar, collectionId):
                return None

            collectionTasks.append((taskState, collectionId))

        return collectionTasks

    def treasureChestOpened(self, avatar, treasureChest, callback=None):
        parentObj = avatar.getParentObj()
        if not parentObj:
            return

        questEvent = QuestEvent.TreasureChestOpened()
        questEvent.setLocation(parentObj.getUniqueId())
        questEvent.setTreasureId(treasureChest.getUniqueId())
        questEvent.setTreasureType(0) #Unused value

        return self.completeTaskState(avatar, questEvent, callback=callback)

    def finishBuriedTreasure(self, avatar, treasureChest):
        parentObj = avatar.getParentObj()
        if not parentObj:
            return 0

        questEvent = QuestEvent.TreasureChestOpened()
        questEvent.setLocation(parentObj.getUniqueId())
        questEvent.setTreasureId(treasureChest.getUniqueId())
        questEvent.setTreasureType(0)
        madeProgress = False

        for quest in list(self.quests.get(avatar.doId, {}).values()):
            dna = quest.getQuestDNA()
            if dna is None:
                continue
            treasureStates = [
                state for task, state in zip(dna.getTasks(), quest.getTaskStates())
                if isinstance(task, QuestTaskDNA.RecoverTreasureItemTaskDNA)]
            if not treasureStates:
                continue

            if quest.isComplete():
                if (not dna.getFinalizeInfo() and not quest.completeRequiresVisit() and
                        dna.getQuestInt() not in avatar.getQuestHistory()):
                    self.completeQuest(avatar, quest)
                continue

            previousProgress = [state.getProgress() for state in treasureStates]
            quest.handleEvent(avatar, questEvent)
            if any(state.getProgress() > previous
                   for state, previous in zip(treasureStates, previousProgress)):
                madeProgress = True

            if quest.isComplete() and not quest.completeRequiresVisit():
                if dna.getFinalizeInfo():
                    self.finalizeCutscene(avatar, quest)
                else:
                    self.completeQuest(avatar, quest)

        return int(madeProgress)

    def getContainerSearchTasks(self, avatar, questEvent):
        """
        Returns a list of (quest, taskState) pairs of the avatar's incomplete
        container search tasks that the searched container applies to
        """

        searchTasks = []
        for quest in list(self.quests.get(avatar.doId, {}).values()):
            questDNA = quest.getQuestDNA()
            if questDNA is None or quest.isComplete():
                continue

            for taskDNA, taskState in zip(questDNA.getTasks(), quest.getTaskStates()):
                if not isinstance(taskDNA, QuestTaskDNA.RecoverContainerItemTaskDNA):
                    continue

                if taskState.isComplete() or not taskDNA.locationMatches(questEvent):
                    continue

                if taskState.hasSearchedContainer(questEvent.getContainerId()):
                    continue

                containerId = taskDNA.getContainerId()
                if containerId != PropIds.ANY_PROP:
                    propList = getPropList(containerId)
                    if propList:
                        if questEvent.getContainerId() not in propList:
                            continue
                    elif containerId != questEvent.getContainerId():
                        continue

                searchTasks.append((quest, taskState))

        return searchTasks

    def makeContainerSearchedEvent(self, avatar, container):
        parentObj = avatar.getParentObj()
        if not parentObj:
            return None

        questEvent = QuestEvent.ContainerSearched()
        questEvent.setLocation(parentObj.getUniqueId())
        questEvent.setContainerId(container.getUniqueId())
        questEvent.setContainerType(container.getType())
        return questEvent

    def canSearchContainer(self, avatar, container):
        questEvent = self.makeContainerSearchedEvent(avatar, container)
        if not questEvent:
            return False

        return len(self.getContainerSearchTasks(avatar, questEvent)) > 0

    def containerSearched(self, avatar, container):
        questEvent = self.makeContainerSearchedEvent(avatar, container)
        if not questEvent:
            return False

        searchTasks = self.getContainerSearchTasks(avatar, questEvent)
        if not searchTasks:
            return False

        previousProgress = [taskState.getProgress() for quest, taskState in searchTasks]
        self.completeTaskState(avatar, questEvent)

        return any(taskState.getProgress() > progress
                   for (quest, taskState), progress in zip(searchTasks, previousProgress))

    def deployedShip(self, avatar):
        parentObj = avatar.getParentObj()
        if not parentObj:
            return

        questEvent = QuestEvent.DeployedShip()
        questEvent.setLocation(parentObj.getUniqueId())

        return self.completeTaskState(avatar, questEvent)

    def enemyDefeated(self, avatar, enemy):
        parentObj = avatar.getParentObj()
        if not parentObj:
            return

        questEvent = QuestEvent.EnemyDefeated()
        questEvent.setLocation(parentObj.getUniqueId())
        questEvent.setEnemyType(enemy.getAvatarType())
        questEvent.setLevel(enemy.getLevel())
        questEvent.setWeaponType(enemy.getCurrentWeapon()[0])

        madeProgress = self.completeTaskState(avatar, questEvent)

        # named enemies are also tracked by their unique id, these
        # are used by the defeat npc tasks...
        npcId = enemy.getUniqueId() if hasattr(enemy, 'getUniqueId') else ''
        if npcId:
            questEvent = QuestEvent.NPCDefeated()
            questEvent.setLocation(parentObj.getUniqueId())
            questEvent.setNpcId(npcId)
            madeProgress = self.completeTaskState(avatar, questEvent) or madeProgress

        return madeProgress

    def getShipFaction(self, ship):
        team = ship.getBaseTeam()
        if team in (PiratesGlobals.INVALID_TEAM, PiratesGlobals.PLAYER_TEAM):
            team = ShipGlobals.getShipTeam(ship.getShipClass())

        return {
            PiratesGlobals.UNDEAD_TEAM: AvatarTypes.Undead,
            PiratesGlobals.NAVY_TEAM: AvatarTypes.Navy,
            PiratesGlobals.TRADING_CO_TEAM: AvatarTypes.TradingCo,
            PiratesGlobals.FRENCH_UNDEAD_TEAM: AvatarTypes.French,
            PiratesGlobals.SPANISH_UNDEAD_TEAM: AvatarTypes.Spanish,
        }.get(team, AvatarTypes.Pirate)

    def shipDefeated(self, avatar, ship):
        # the ship's location is where the battle took place, the
        # avatar itself is most likely parented to their own ship...
        parentObj = ship.getParentObj() or avatar.getParentObj()

        # ships at sea are parented to the ocean grid which has no uid of it's
        # own, the battle took place in the world the ocean belongs to...
        while parentObj and not hasattr(parentObj, 'getUniqueId'):
            parentObj = parentObj.getParentObj()

        if not parentObj:
            return

        questEvent = QuestEvent.ShipDefeated()
        questEvent.setLocation(parentObj.getUniqueId())
        questEvent.setFaction(self.getShipFaction(ship))
        questEvent.setHull(ship.getShipClass())
        questEvent.setIsFlagship(bool(ship.getIsFlagship()))
        questEvent.setLevel(ship.getLevel())

        return self.completeTaskState(avatar, questEvent)

    def getAttackerAvatars(self, attackerIds):
        # attackers are either ships, in which case their whole crew takes
        # part in the attack, or the avatars themselves...
        avatars = []
        for attackerId in attackerIds:
            attacker = self.air.doId2do.get(attackerId)
            if isinstance(attacker, DistributedShipAI):
                avatarIds = attacker.getCrew()
            else:
                avatarIds = [attackerId]

            for avatarId in avatarIds:
                avatar = self.air.doId2do.get(avatarId)
                if avatar and avatar not in avatars and avatar.doId in self.quests:
                    avatars.append(avatar)

        return avatars

    def getShipAttackerIds(self, ship):
        # the ship that landed the final blow, followed by every
        # other ship that has damaged the ship...
        attackerIds = []
        lastAttackerId = getattr(ship, 'lastAttackerShipId', 0)
        if lastAttackerId:
            attackerIds.append(lastAttackerId)

        for attackerId in list(getattr(ship, 'attackerDamage', {}).keys()):
            if attackerId and attackerId not in attackerIds:
                attackerIds.append(attackerId)

        return attackerIds

    def shipSunk(self, ship, attackerIds):
        # every member of the crews that took part in sinking the ship
        # receives credit for it, just like every avatar that attacked a
        # defeated enemy does (see BattleManagerAI.rewardAttackers)...
        for avatar in self.getAttackerAvatars(attackerIds):
            self.shipDefeated(avatar, ship)

    def shipSinking(self, ship):
        """
        Called by the ship once it's hp have been depleted and it begins sinking
        """

        if ship.getSiegeTeam():
            self.shipPVPSunk(ship)

        if ship.getNPCship():
            self.shipSunk(ship, self.getShipAttackerIds(ship))

    # =========================================================================
    # Ship PVP (privateering)
    # =========================================================================

    SiegeTeam2ShipPVPClass = {
        1: PiratesGlobals.ShipPVPFrench,
        2: PiratesGlobals.ShipPVPSpanish,
    }

    def getShipPVPClass(self, teamId):
        return self.SiegeTeam2ShipPVPClass.get(teamId)

    def getShipPVPWeapon(self, skillId):
        # cannon skills are the deck cannons manned by the avatar, everything
        # else (broadsides and rams) is done using the ship itself...
        if InventoryType.begin_WeaponSkillCannon <= skillId < InventoryType.end_ExtendedWeaponSkillCannon:
            return PiratesGlobals.ShipPVPKillCannon

        return PiratesGlobals.ShipPVPKillShip

    def getShipPVPEnemyAvatars(self, attackers, enemyTeam):
        # only avatars on the opposing siege team receive credit...
        avatars = []
        for attacker in attackers:
            if attacker is None:
                continue

            if isinstance(attacker, DistributedShipAI):
                if not attacker.getSiegeTeam() or attacker.getSiegeTeam() == enemyTeam:
                    continue

            for avatar in self.getAttackerAvatars([attacker.doId]):
                if avatar not in avatars and avatar.getSiegeTeam() and avatar.getSiegeTeam() != enemyTeam:
                    avatars.append(avatar)

        return avatars

    def handleShipPVPEvent(self, avatar, questEvent):
        parentObj = avatar.getParentObj()
        if parentObj and hasattr(parentObj, 'getUniqueId'):
            questEvent.setLocation(parentObj.getUniqueId())

        # sieges (privateering) are the only ship pvp game in this version...
        if hasattr(questEvent, 'setGameType'):
            questEvent.setGameType(PiratesGlobals.ShipPVPSiege)

        return self.completeTaskState(avatar, questEvent)

    def shipPVPSunk(self, ship):
        """
        A privateer ship has been sunk. The crew that landed the final blow is credited with
        the weapon they used, every other enemy crew that damaged the ship is credited as well
        (for tasks that do not require a specific weapon). The crew of the sunk ship loses the
        progress of any tasks that have to be completed without sinking.
        """

        enemyTeam = ship.getSiegeTeam()
        enemyClass = self.getShipPVPClass(enemyTeam)
        for avatar in self.getAttackerAvatars([ship.doId]):
            self.handleShipPVPEvent(avatar, QuestEvent.ShipPVPSink())

        if enemyClass is None:
            return

        credited = []
        lastAttackerId = getattr(ship, 'lastAttackerShipId', 0)
        for attackerId in self.getShipAttackerIds(ship):
            attacker = self.air.doId2do.get(attackerId)
            killWeapon = None
            if attackerId == lastAttackerId:
                killWeapon = self.getShipPVPWeapon(getattr(ship, 'lastAttackSkillId', 0))

            for avatar in self.getShipPVPEnemyAvatars([attacker], enemyTeam):
                if avatar in credited:
                    continue

                credited.append(avatar)
                questEvent = QuestEvent.ShipPVPEnemyDefeated()
                questEvent.setEnemyClass(enemyClass)
                questEvent.setNum(1)
                questEvent.setKillType(PiratesGlobals.ShipPVPShip)
                questEvent.setKillWeapon(killWeapon)
                self.handleShipPVPEvent(avatar, questEvent)

    def shipPVPSpawned(self, ship):
        # a privateer ship has (re)joined the battle...
        for avatar in self.getAttackerAvatars([ship.doId]):
            self.handleShipPVPEvent(avatar, QuestEvent.ShipPVPSpawn())

    def shipPVPShipDamaged(self, ship, attacker, damage, skillId=0):
        """
        A privateer ship took damage from an attacker, either an avatar (cannons and
        broadsides) or a ship (rams).
        """

        enemyClass = self.getShipPVPClass(ship.getSiegeTeam())
        if enemyClass is None or damage <= 0:
            return

        if isinstance(attacker, DistributedShipAI):
            weapon = PiratesGlobals.ShipPVPKillShip
        else:
            weapon = self.getShipPVPWeapon(skillId)

        for avatar in self.getShipPVPEnemyAvatars([attacker], ship.getSiegeTeam()):
            questEvent = QuestEvent.ShipPVPShipDamage()
            questEvent.setEnemyClass(enemyClass)
            questEvent.setDamage(int(damage))
            questEvent.setDamageWeapon(weapon)
            self.handleShipPVPEvent(avatar, questEvent)

    def shipPVPPlayerDamaged(self, target, attacker, damage, skillId=0):
        enemyClass = self.getShipPVPClass(target.getSiegeTeam())
        if enemyClass is None or damage <= 0:
            return

        for avatar in self.getShipPVPEnemyAvatars([attacker], target.getSiegeTeam()):
            questEvent = QuestEvent.ShipPVPPlayerDamage()
            questEvent.setEnemyClass(enemyClass)
            questEvent.setDamage(int(damage))
            questEvent.setDamageWeapon(self.getShipPVPWeapon(skillId))
            self.handleShipPVPEvent(avatar, questEvent)

    def shipPVPPirateDefeated(self, target, attackers):
        """
        A privateer has been defeated, every enemy privateer that attacked them is
        credited, using the weapon of the last skill they have used.
        """

        enemyClass = self.getShipPVPClass(target.getSiegeTeam())
        if enemyClass is None:
            return

        for avatar in self.getShipPVPEnemyAvatars(attackers, target.getSiegeTeam()):
            killWeapon = None
            diary = getattr(avatar, 'battleSkillDiary', None)
            if diary and diary.getCurrentSkill():
                killWeapon = self.getShipPVPWeapon(diary.getCurrentSkill())

            questEvent = QuestEvent.ShipPVPEnemyDefeated()
            questEvent.setEnemyClass(enemyClass)
            questEvent.setNum(1)
            questEvent.setKillType(PiratesGlobals.ShipPVPPirate)
            questEvent.setKillWeapon(killWeapon)
            self.handleShipPVPEvent(avatar, questEvent)

    def dockedAtPort(self, avatar, island):
        questEvent = QuestEvent.DockedAtPort()
        questEvent.setLocation(island.getUniqueId())

        return self.completeTaskState(avatar, questEvent)

    def objectVisited(self, avatar, obj):
        parentObj = avatar.getParentObj()
        if not parentObj:
            return

        questEvent = QuestEvent.ObjectVisited()
        questEvent.setLocation(parentObj.getUniqueId())
        questEvent.setObjectId(obj.getUniqueId())
        questEvent.setAvId(avatar.doId)

        return self.completeTaskState(avatar, questEvent)

    def pokerHandWon(self, avatar, gold):
        parentObj = avatar.getParentObj()
        if not parentObj:
            return

        questEvent = QuestEvent.PokerHandWon()
        questEvent.setLocation(parentObj.getUniqueId())
        questEvent.setGold(gold)

        return self.completeTaskState(avatar, questEvent)

    def blackjackHandWon(self, avatar, gold):
        parentObj = avatar.getParentObj()
        if not parentObj:
            return

        questEvent = QuestEvent.BlackjackHandWon()
        questEvent.setLocation(parentObj.getUniqueId())
        questEvent.setGold(gold)

        return self.completeTaskState(avatar, questEvent)

    def finalizeCutscene(self, avatar, quest, finalizeIndex=0, npc=None):
        if quest.getQuestDNA().getQuestInt() in avatar.getQuestHistory():
            self.resumeCompletedTutorialQuest(avatar)
            return
        if quest.doId in self.finalizingQuests:
            return
        self.finalizingQuests.add(quest.doId)
        finalizeInfo = quest.questDNA.getFinalizeInfo()

        def finalizeInteract():
            self.completeQuest(avatar, quest)

        def finalize(finalizeIndex, waitSatisfied=False):
            if finalizeIndex >= len(finalizeInfo):
                if finalizeInfo:
                    checkpoint = quest.questDNA.getCheckPoint()
                    if checkpoint == -1 or avatar.getTutorial() <= checkpoint:
                        quest.d_amFinalized()
                    else:
                        quest.setFinalized()
                # if an npc is present send the quest completed information
                if not npc or not quest.completeRequiresVisit():
                    # didn't have an NPC, just go ahead and complete the quest anyways...
                    self.completeQuest(avatar, quest)
                else:
                    self.acceptOnce(avatar.uniqueName('interact-canceled'), finalizeInteract)
                    npc.d_setQuestsCompleted(avatar.doId,
                        completedContainerIds=self.getCompletedContainerIds(avatar, quest),
                        completedQuestIds=[quest.getQuestId()], completedQuestDoIds=[quest.doId])

                return
            else:
                finalizeStateInfo = finalizeInfo[finalizeIndex]
                quest.setFinalizeStateIndex(finalizeIndex)

            if (quest.getQuestId() == TutorialGlobals.FIRST_QUEST and
                    finalizeStateInfo.get('waitEvent') == 'makeAPirateComplete' and
                    not waitSatisfied and
                    avatar.getTutorial() < PiratesGlobals.TUT_MADE_PIRATE):
                self.acceptOnce('makeAPirateComplete-%d' % quest.doId,
                                finalize, extraArgs=[finalizeIndex, True])
                return

            # Darby Drydock's closing dialog waits for the ship the avatar just
            # named to be built, the quest's ShipReward hands that ship over...
            if (finalizeStateInfo.get('waitEvent') == 'tutorialShipConstructed' and
                    not waitSatisfied and not avatar.getConstructedShipDoId()):
                def shipConstructed():
                    self.tutorialShipWaits.pop(quest.doId, None)
                    finalize(finalizeIndex, True)

                shipEvent = avatar.uniqueName('tutorialShipConstructed')
                self.tutorialShipWaits[quest.doId] = shipEvent
                self.acceptOnce(shipEvent, shipConstructed)
                return

            if (quest.getQuestId() == 'Chapter1.rung3' and
                    finalizeStateInfo.get('waitEvent') == 'tutorialJROnStage' and
                    quest.doId not in self.tutorialJollyReady):
                self.tutorialJollyWaiters[quest.doId] = lambda: finalize(finalizeIndex)
                return

            def finalizeCompleteCallback():
                finalize(len(finalizeInfo))

            def finalizeCallback(isDialog=False):
                if finalizeIndex >= len(finalizeInfo):
                    if not isDialog:
                        questEvent = QuestEvent.CutsceneWatched()
                        questEvent.setNpcId(npc.getUniqueId())
                        self.completeTaskState(avatar, questEvent, callback=finalizeCompleteCallback)
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
                        if not self._giveRewards(avatar, rewards):
                            self.finalizingQuests.discard(quest.doId)
                            return

                    finalize(finalizeIndex + 1)

            finalizeType = finalizeStateInfo['type']
            if finalizeType == 'cutscene':
                if npc is not None:
                    giverId = npc.doId
                else:
                    giverId = 0

                self.acceptOnce('quest-finalize-%d' % quest.doId, finalizeCallback)
                quest.d_startFinalizeScene(finalizeIndex, giverId)
            elif finalizeType == 'dialog':
                if npc is None:
                    self.finalizingQuests.discard(quest.doId)
                    self.notify.warning('Failed to handle interact callback with unknown npc for avatar %d '
                        'with unknown finalizeType: %s!' % (avatar.doId, finalizeType))

                    return

                self.acceptOnce('quest-finalize-%d' % quest.doId, finalizeCallback, extraArgs=[True])
                quest.d_startFinalizeScene(finalizeIndex, npc.doId)
            else:
                self.finalizingQuests.discard(quest.doId)
                self.notify.warning('Failed to handle interact callback with npc %d for avatar %d '
                    'with unknown finalizeType: %s!' % (npc.doId if npc else 0, avatar.doId, finalizeType))

                return

        finalize(finalizeIndex)

    def requestInteract(self, avatar, npc):
        parentObj = avatar.getParentObj()
        if not parentObj:
            return

        if (isinstance(npc, DistributedNPCTownfolkAI) or
                isinstance(npc, DistributedShipAI) and
                npc.getUniqueId() == TutorialGlobals.STUMPY_BOAT_UID):
            questEvent = QuestEvent.NPCVisited()
            questEvent.setLocation(parentObj.getUniqueId())
            questEvent.setNpcId(npc.getUniqueId())
            questEvent.setAvId(avatar.doId)
        else:
            self.notify.warning('Avatar %d failed to request interact for npc %d, '
                'invalid npc type!' % (avatar.doId, npc.doId))

            return

        # any quest handed to the avatar during this interaction
        # will be returned to this npc...
        self.setQuestGiverId(avatar, npc.getUniqueId())

        def interactCallback(quest):
            self.finalizeCutscene(avatar, quest, npc=npc)

        if self.completeTaskState(avatar, questEvent, callback=interactCallback):
            return True

        # finally, check to see if the avatar has any completed
        # quests that are to be handed in to this npc...
        for quest in list(self.quests.get(avatar.doId, {}).values()):
            dna = quest.getQuestDNA()
            if (dna is None or not quest.isComplete() or not quest.completeRequiresVisit() or
                    quest.doId in self.finalizingQuests or
                    dna.getQuestInt() in avatar.getQuestHistory()):
                continue
            if quest.canBeReturnedTo(npc.getUniqueId()):
                self.finalizeCutscene(avatar, quest, npc=npc)
                return True
        return False

    def attemptBribeNPC(self, avatar, npc):
        parentObj = avatar.getParentObj()
        if not parentObj:
            return

        inventory = avatar.getInventory()
        if not inventory:
            self.notify.warning('Failed to get quest bribe amount for avatar %d, '
                'avatar has no inventory!' % avatar.doId)

            return

        bribeAmount = self.getTaskBribeAmountFromNPC(avatar, npc.getUniqueId())
        if bribeAmount < 0:
            self.notify.warning('Failed to get quest bribe amount for avatar %d, '
                'task was not found!' % avatar.doId)

            return

        if bribeAmount > inventory.getGoldInPocket():
            self.notify.debug('Avatar %d cannot afford to bribe npc %s for %d gold!' % (
                avatar.doId, npc.getUniqueId(), bribeAmount))

            return

        questEvent = QuestEvent.NPCBribed()
        questEvent.setLocation(parentObj.getUniqueId())
        questEvent.setNpcId(npc.getUniqueId())
        questEvent.setGold(bribeAmount)

        def _bribeCallback(quest):
            inventory.setGoldInPocket(inventory.getGoldInPocket() - bribeAmount)
            self.finalizeCutscene(avatar, quest, npc=npc)

        return self.completeTaskState(avatar, questEvent, callback=_bribeCallback)

    def canOfferQuest(self, avatar, questId, questDNA, giverId):
        """
        Returns True if the quest giver is able to offer the quest to the avatar,
        these checks mirror DistributedQuestGiver.hasQuestOffers on the client
        """

        if not any(prereq.giverMatters() and prereq.giverCanGive(giverId)
                   for prereq in questDNA.getPrereqs()):
            return False

        if not questDNA.vetAv(avatar):
            return False

        if questDNA.getMinLevel() > avatar.getLevel():
            return False

        ladderHistory = avatar.getQuestLadderHistory()
        if not self.questDependency.checkDependency(questId, ladderHistory, 1):
            return False

        inventory = avatar.getInventory()
        if questDNA.getWeapLvlType() is not None and questDNA.getMinWeapLevel() > 0:
            weaponLevel = getLevelFromTotalReputation(questDNA.getWeapLvlType(),
                inventory.getReputation(questDNA.getWeapLvlType()))[0]

            if questDNA.getMinWeapLevel() > weaponLevel:
                return False

        if questDNA.getAcquireOnce():
            try:
                questLadderInt = self.questDynMap.findQuestLadderInt(questId)
            except KeyError:
                questLadderInt = questDNA.getQuestInt()

            if questLadderInt in ladderHistory:
                return False

        # the avatar's inventory only holds so many quests...
        questLimit = InventoryInit.CategoryLimits[InventoryCategory.QUESTS]
        if inventory and len(inventory.getDoIdListCategory(InventoryCategory.QUESTS)) >= questLimit:
            return False

        # the avatar must not already be working on this quest,
        # or any other quest from the same quest ladder...
        if self.hasQuest(avatar, questId=questId):
            return False

        if avatar.questStatus.hasLadderQuestId(questId):
            return False

        return True

    def getQuestOffers(self, avatar, giverId):
        inventory = avatar.getInventory()
        if not inventory:
            return []

        offers = []
        for questId, questDNA in list(QuestDB.QuestDict.items()):
            if self.canOfferQuest(avatar, questId, questDNA, giverId):
                offers.append(QuestOffer.create(questId, avatar))

        return offers

    def getQuestLadderOffers(self, avatar, containers):
        offers = []
        for container in containers:
            offers.append(QuestLadderOffer(container.getName(), container.getTitle(),
                container.getRewards()))

        return offers

    def acceptQuestOffer(self, avatar, giver, offer, ladder):
        giverId = giver.getUniqueId()
        questId = offer.getQuestId()
        if ladder:
            # the avatar chose a container from one of their quest choices,
            # give them the first quest of the chosen container...
            container = avatar.questStatus.getContainer(questId)
            if not container:
                self.notify.warning('Avatar %d accepted unknown quest container %s from %s!' % (
                    avatar.doId, questId, giverId))

                return

            choice = container.getParent()
            if choice and choice.getGiverId():
                giverId = choice.getGiverId()

            questId = container.getFirstQuestId()
        else:
            questDNA = QuestDB.QuestDict.get(questId)
            if not questDNA or not self.canOfferQuest(avatar, questId, questDNA, giverId):
                self.air.logPotentialHacker(message='Avatar accepted a quest that cannot be offered to them!',
                    questId=questId, giverId=giverId)

                return

            self.resetRepeatableQuestLadder(avatar, questId)
            self.setQuestOffer(avatar, offer)

        if self.hasQuest(avatar, questId=questId):
            self.notify.debug('Avatar %d already has offered quest %s!' % (avatar.doId, questId))
            return

        self.setQuestGiverId(avatar, giverId)
        self.createQuest(avatar, questId)

    def resetRepeatableQuestLadder(self, avatar, questId):
        # quest ladders that can be acquired more than once must have their
        # quests removed from the avatar's history, otherwise the ladder would
        # believe it's quests were already completed when it's taken again...
        path = QuestLadderDB.getFortunePath(questId)
        if not path:
            return

        ladderDNA = path[0]
        if ladderDNA.getName() in avatar.questStatus.ladders:
            return

        questInts = []
        self.__getQuestInts(ladderDNA, questInts)

        questHistory = avatar.getQuestHistory()
        newQuestHistory = [questInt for questInt in questHistory if questInt not in questInts]
        if newQuestHistory != questHistory:
            avatar.b_setQuestHistory(newQuestHistory)

        ladderHistory = avatar.getQuestLadderHistory()
        newLadderHistory = [questInt for questInt in ladderHistory
                            if questInt not in questInts or questInt == ladderDNA.getQuestInt()]
        if newLadderHistory != ladderHistory:
            avatar.b_setQuestLadderHistory(newLadderHistory)

    def __getQuestInts(self, container, questInts):
        for child in container.getContainers():
            questInts.append(child.getQuestInt())
            if child.isContainer():
                self.__getQuestInts(child, questInts)

    def getQuestStepType(self, stepObject):
        if isinstance(stepObject, DistributedBuildingDoorAI):
            stepType = QuestStep.STExteriorDoor
        elif isinstance(stepObject, DistributedInteriorDoorAI):
            stepType = QuestStep.STInteriorDoor
        elif isinstance(stepObject, DistributedGATunnelAI):
            stepType = QuestStep.STTunnel
        elif isinstance(stepObject, DistributedDinghyAI):
            stepType = QuestStep.STQuestNode
        elif isinstance(stepObject, DistributedGameAreaAI):
            stepType = QuestStep.STArea
        elif isinstance(stepObject, DistributedShipAI):
            stepType = QuestStep.STShip
        elif isinstance(stepObject, (DistributedNPCTownfolkAI, DistributedBattleAvatarAI,
                                     DistributedSearchableContainerAI, DistributedBuriedTreasureAI)):
            # townfolk, enemies, containers and buried treasure all use the npc indicator,
            # the client places the beam on the object once it has been generated...
            stepType = QuestStep.STNPC
        else:
            stepType = QuestStep.NullStep

        return stepType

    def getQuestStepGoalUid(self, avatar, quest):
        """
        Returns the goal the avatar's quest step points to, either the goal of the
        quest's active task, or the npc the quest is to be returned to once complete
        """

        questDNA = quest.getQuestDNA()
        if questDNA is None:
            return None

        if not quest.isComplete():
            activeTask = self.getActiveTask(quest)
            return activeTask.getGoalUid() if activeTask else None

        if not quest.completeRequiresVisit():
            return None

        # the same order as Quest.canBeReturnedTo...
        returnGiverIds = questDNA.getReturnGiverIds()
        if returnGiverIds:
            return returnGiverIds[0]

        for task, taskState in zip(quest.getTasks(), quest.getTaskStates()):
            returnGiverIds = task.getReturnGiverIds()
            if taskState.isComplete() and returnGiverIds:
                return returnGiverIds[0]

        return quest.getGiverId() or None

    def getQuestStepGoalKey(self, avatar, quest):
        goal = self.getQuestStepGoalUid(avatar, quest)
        goalKey = goal._asString() if isinstance(goal, QuestGoal) else goal

        # the step of an enemy, container or treasure goal points at the closest one,
        # which is another one once the avatar has made progress on the task...
        activeTask = self.getActiveTask(quest) if not quest.isComplete() else None
        closestGoal = isinstance(goal, QuestGoal) or isinstance(activeTask, (
            QuestTaskDNA.RecoverContainerItemTaskDNA, QuestTaskDNA.RecoverTreasureItemTaskDNA))
        if not closestGoal and isinstance(goal, str):
            closestGoal = isinstance(self.air.uidMgr.justGetMeMeObject(goal), DistributedGameAreaAI)

        if closestGoal:
            return goalKey, tuple(taskState.getProgress() for taskState in quest.getTaskStates())

        return goalKey

    def updateQuestStep(self, avatar, quest):
        if hasattr(avatar, 'requestQuestStep'):
            avatar.requestQuestStep(quest.getQuestId())

    def questGoalMatches(self, avatar, goal, obj):
        goalData = goal._QuestGoal__goalData
        level = goalData[0] if goalData else 0
        if level > 0 and hasattr(obj, 'getLevel') and level > obj.getLevel():
            return False

        if goal.getTargetType() == 'ship':
            if not isinstance(obj, DistributedShipAI) or not obj.getNPCship() or not obj.isSailable():
                return False

            if len(goalData) > 2 and goalData[2] is not None:
                if not self.getShipFaction(obj).isA(goalData[2]):
                    return False

            if len(goalData) > 3 and goalData[3] is not None:
                shipClassList = getShipList(goalData[3])
                if shipClassList and obj.getShipClass() not in shipClassList:
                    return False

            if len(goalData) > 4 and goalData[4] is not None:
                if bool(goalData[4]) != bool(obj.getIsFlagship()):
                    return False

            return True

        if isinstance(obj, DistributedShipAI) or not isinstance(obj, DistributedBattleAvatarAI):
            return False

        if obj is avatar or obj.doId in self.quests or not hasattr(obj, 'getAvatarType'):
            return False

        hp = obj.getHp() if hasattr(obj, 'getHp') else 1
        if isinstance(hp, (list, tuple)):
            hp = hp[0]

        if hp <= 0:
            return False

        avatarType = obj.getAvatarType()
        return avatarType is not None and avatarType.isA(goalData[1])

    def findQuestGoalObject(self, avatar, goal, area=None):
        """
        Finds the closest object that matches the custom quest goal (an enemy type or a
        type of ship) in the area the avatar is currently in
        """

        if area is None:
            area = self.getQuestStepArea(avatar)
            if goal.getTargetType() == 'ship' and isinstance(area, DistributedShipAI):
                area = area.getParentObj()

        if area is None:
            return None

        # an avatar sailing it's ship is as far away as it's ship...
        avatarObj = avatar
        if avatar.parentId != area.doId and isinstance(avatar.getParentObj(), DistributedShipAI):
            avatarObj = avatar.getParentObj()

        avatarPos = self.getQuestStepPos(avatarObj, area)
        closest, closestDistance = None, None
        for obj in list(self.air.doId2do.values()):
            if getattr(obj, 'parentId', None) != area.doId:
                continue

            try:
                if not self.questGoalMatches(avatar, goal, obj):
                    continue
            except Exception:
                continue

            distance = self.getQuestStepDistance(avatarPos, self.getQuestStepPos(obj, area))
            if closestDistance is None or distance < closestDistance:
                closest, closestDistance = obj, distance

        return closest

    def getQuestStepArea(self, obj):
        """
        Returns the game area (an island, interior or cave) or the
        ship the object is in, this is where the object's quest step starts from
        """

        while obj is not None:
            if isinstance(obj, (DistributedGameAreaAI, DistributedShipAI)):
                return obj

            obj = obj.getParentObj()

        return None

    def getQuestStepPos(self, obj, area):
        """
        Returns the position of the object relative to the area, the client places
        the quest indicator relative to the area until the step's object arrives
        """

        # objects in the zones of a grid (islands and the ocean) are parented
        # to the origin of their grid cell, as they are on the client...
        if not obj.isEmpty() and not area.isEmpty() and area.isAncestorOf(obj):
            return obj.getPos(area)

        return obj.getPos()

    def getQuestStepDistance(self, pos, otherPos):
        return (pos[0] - otherPos[0]) ** 2 + (pos[1] - otherPos[1]) ** 2

    def getQuestStepLinks(self, area, connectors):
        """
        Returns a list of (connector, area) pairs of the doors and tunnels
        leading out of the area, and the area each of them leads to
        """

        links = []
        for connector in connectors.get(area.doId, []):
            if isinstance(connector, DistributedBuildingDoorAI):
                otherAreas = [self.air.doId2do.get(connector.interiorDoId)]
            elif isinstance(connector, DistributedInteriorDoorAI):
                otherDoor = connector.otherDoor
                otherAreas = [otherDoor.getParentObj() if otherDoor else None]
            else:
                otherAreas = [self.air.doId2do.get(link[1]) for link in connector.getLinks()[2]]

            for otherArea in otherAreas:
                if otherArea is None or otherArea is area:
                    continue

                if (connector, otherArea) not in links:
                    links.append((connector, otherArea))

        return links

    def getQuestStepConnectors(self):
        # the doors and tunnels of every game area, by the doId of the area they are in...
        connectors = collections.defaultdict(list)
        for obj in list(self.air.doId2do.values()):
            if isinstance(obj, (DistributedBuildingDoorAI, DistributedInteriorDoorAI, DistributedGATunnelAI)):
                connectors[obj.parentId].append(obj)

        return connectors

    def getQuestStepPath(self, area, isGoal, connectors):
        """
        Returns the connectors the avatar has to go through to get from the
        area to the first area that isGoal accepts, the same breadth first search
        the client's QuestPath does through each area's exit links
        """

        paths = {area.doId: []}
        needToVisit = [area]
        while needToVisit:
            nextArea = needToVisit.pop(0)
            if isGoal(nextArea):
                return nextArea, paths[nextArea.doId]

            for connector, otherArea in self.getQuestStepLinks(nextArea, connectors):
                if otherArea.doId in paths:
                    continue

                paths[otherArea.doId] = paths[nextArea.doId] + [connector]
                needToVisit.append(otherArea)

        return None, None

    def getQuestStepIsland(self, area, connectors):
        # the island the area is on, interiors and caves lead out onto their island...
        if isinstance(area, DistributedIslandAI):
            return area

        island, path = self.getQuestStepPath(area, lambda other: isinstance(other, DistributedIslandAI), connectors)
        return island

    def getQuestStepTargetNode(self, uid):
        """
        Returns the game area and the position of a quest node (or a dinghy) defined
        in the world data, quest nodes are only markers and have no object of their own
        """

        worldCreator = getattr(self.air, 'worldCreator', None)
        if not worldCreator:
            return None

        for fileName, fileData in list(worldCreator.fileDicts.items()):
            objectPath = fileData.get('ObjectIds', {}).get(uid)
            if not objectPath:
                continue

            objectInfo = worldCreator.getObjectDataFromFileByUid(uid, fileName)
            if not objectInfo or objectInfo.get('Type') not in ('Quest Node', 'Dinghy'):
                continue

            # the node is placed relative to the game area it is defined in...
            parentUids = [part.strip('"\'') for part in objectPath.replace('][', '|').strip('[]').split('|')]
            parentUids = [parentUid for parentUid in parentUids[:-1] if parentUid != 'Objects']
            area = self.air.uidMgr.justGetMeMeObject(parentUids[-1]) if parentUids else None
            if isinstance(area, DistributedGameAreaAI):
                pos, hpr = objectInfo['Pos'], objectInfo.get('Hpr', (0, 0, 0))
                return area, [pos[0], pos[1], pos[2], hpr[0]]

        return None

    def getQuestStepTargets(self, avatar, quest, goalUid):
        """
        Returns the objects (or quest nodes) the avatar's quest step may lead to,
        a target is a (area, object, posH) tuple where the object may be None
        """

        def objectTarget(obj):
            if isinstance(obj, DistributedGameAreaAI):
                area = obj
            elif isinstance(obj, DistributedShipAI):
                # ships sail the ocean grid...
                area = obj.getParentObj()
            else:
                area = self.getQuestStepArea(obj.getParentObj())

            if area is None:
                return None

            pos = self.getQuestStepPos(obj, area) if area is not obj else (0, 0, 0)
            h = obj.getH() if area is not obj else 0
            return area, obj, [pos[0], pos[1], pos[2], h]

        def uidTargets(uids):
            targets = []
            for uid in uids:
                obj = self.air.uidMgr.justGetMeMeObject(uid)
                if obj is not None:
                    target = objectTarget(obj)
                else:
                    node = self.getQuestStepTargetNode(uid)
                    target = (node[0], None, node[1]) if node else None

                if target:
                    targets.append(target)

            return targets

        if goalUid is None:
            # containers and treasure are searched for by their uid, or the name
            # of a group of them, the step leads to one that is yet to be searched...
            activeTask = self.getActiveTask(quest) if not quest.isComplete() else None
            if isinstance(activeTask, QuestTaskDNA.RecoverContainerItemTaskDNA):
                taskState = quest.getTaskStates()[quest.getTasks().index(activeTask)]
                containerId = activeTask.getContainerId()
                if containerId == PropIds.ANY_PROP:
                    return []

                containerIds = getPropList(containerId) or [containerId]
                return uidTargets([uid for uid in containerIds if not taskState.hasSearchedContainer(uid)])

            return []

        if isinstance(goalUid, QuestGoal):
            if goalUid.getType() != QuestGoal.Type_Custom:
                return []

            # custom goals lead to the closest matching enemy (or ship) around the avatar...
            goalObject = self.findQuestGoalObject(avatar, goalUid)
            if goalObject is None:
                return []

            target = objectTarget(goalObject)
            return [target] if target else []

        treasureIds = getTreasureList(goalUid)
        if treasureIds:
            return uidTargets(treasureIds)

        # a task's location may be any of a list of areas (an island and it's caves),
        # the step leads to the closest of them...
        activeTask = self.getActiveTask(quest) if not quest.isComplete() else None
        if activeTask is not None and not activeTask.getGoalLocation():
            locationIds = getLocationList(activeTask.getLocation())
            if locationIds and goalUid in locationIds:
                return uidTargets(locationIds)

        return uidTargets([goalUid])

    def getQuestStepTaskGoal(self, quest):
        # the custom goal (the type of enemy) of the active task, ignoring it's
        # location, used once the avatar has arrived at the task's location...
        activeTask = self.getActiveTask(quest) if not quest.isComplete() else None
        if activeTask is None:
            return None

        task = activeTask.makeCopy()
        task.setLocation(QuestTaskDNA.LocationIds.ANY_LOCATION)
        task.setGoalLocation(None)
        try:
            goal = task.getGoalUid()
        except Exception:
            return None

        if isinstance(goal, QuestGoal) and goal.getType() == QuestGoal.Type_Custom:
            return goal

        return None

    def getQuestStep(self, avatar, quest):
        """
        Returns the quest step of the avatar's active quest as the list of QuestStep
        fields the client expects, the step leads from the area the avatar is in
        (originDoId) to the next object (stepDoId) on the way to the quest's goal
        """

        nullStep = [0, 0, 0, [0, 0, 0, 0], '']
        if quest is None:
            return nullStep

        area = self.getQuestStepArea(avatar)
        if area is None:
            return nullStep

        goalUid = self.getQuestStepGoalUid(avatar, quest)
        targets = self.getQuestStepTargets(avatar, quest, goalUid)
        if not targets:
            return nullStep

        # ships are pointed at across the ocean grid they sail,
        # the client's ship indicator is placed relative to the grid...
        if isinstance(targets[0][1], DistributedShipAI):
            oceanGrid, ship, posH = targets[0]
            return [oceanGrid.doId, ship.doId, QuestStep.STShip, posH, '']

        connectors = self.getQuestStepConnectors()
        avatarPos = self.getQuestStepPos(avatar, area)
        targetAreaIds = set(target[0].doId for target in targets)

        # the avatar has arrived at the area the goal is in...
        if area.doId in targetAreaIds:
            areaTargets = [target for target in targets if target[0].doId == area.doId]
            if all(target[1] is area for target in areaTargets):
                # the goal is the area itself (the location of a defeat or recover task),
                # lead the avatar to the closest enemy that counts towards the task...
                taskGoal = self.getQuestStepTaskGoal(quest)
                goalObject = self.findQuestGoalObject(avatar, taskGoal, area) if taskGoal else None
                if goalObject is None:
                    return nullStep

                pos = self.getQuestStepPos(goalObject, area)
                areaTargets = [(area, goalObject, [pos[0], pos[1], pos[2], goalObject.getH()])]

            areaTargets.sort(key=lambda target: self.getQuestStepDistance(avatarPos, target[2]))
            targetArea, stepObject, posH = areaTargets[0]
            if stepObject is None:
                # a quest node, the indicator is placed at the node's position...
                stepType, stepDoId = QuestStep.STQuestNode, 0
            else:
                stepType, stepDoId = self.getQuestStepType(stepObject), stepObject.doId
                if not stepType:
                    return nullStep

            return [area.doId, stepDoId, stepType, posH, self.getQuestStepIslandUid(targetArea, connectors)]

        # find the shortest way through the doors and tunnels to the goal...
        targetArea, path = None, None
        if not isinstance(area, DistributedShipAI):
            targetArea, path = self.getQuestStepPath(area, lambda other: other.doId in targetAreaIds, connectors)

        if targetArea is None:
            # the goal is on another island, an island is pointed at from the island or
            # ship the avatar is on, from anywhere else the avatar has to go out first...
            targetIslands = []
            for target in targets:
                island = self.getQuestStepIsland(target[0], connectors)
                if island is not None and island not in targetIslands:
                    targetIslands.append(island)

            if not targetIslands:
                return nullStep

            if isinstance(area, (DistributedIslandAI, DistributedShipAI)):
                island = targetIslands[0]
                return [area.doId, island.doId, QuestStep.STArea, [0, 0, 0, 0], island.getUniqueId()]

            targetArea, path = self.getQuestStepPath(area, lambda other: isinstance(other, DistributedIslandAI), connectors)
            if targetArea is None:
                return nullStep

            islandUid = targetIslands[0].getUniqueId()
        else:
            islandUid = self.getQuestStepIslandUid(targetArea, connectors)

        if not path:
            return nullStep

        # of the doors leading the same way, lead the avatar to the closest one...
        stepObject = path[0]
        nextArea = None
        for connector, otherArea in self.getQuestStepLinks(area, connectors):
            if connector is stepObject:
                nextArea = otherArea
                break

        sameWay = [connector for connector, otherArea in self.getQuestStepLinks(area, connectors)
                   if otherArea is nextArea and type(connector) is type(stepObject)]
        sameWay.sort(key=lambda connector: self.getQuestStepDistance(avatarPos, self.getQuestStepPos(connector, area)))
        if sameWay:
            stepObject = sameWay[0]

        stepType = self.getQuestStepType(stepObject)
        pos = self.getQuestStepPos(stepObject, area)
        return [area.doId, stepObject.doId, stepType, [pos[0], pos[1], pos[2], stepObject.getH()], islandUid]

    def getQuestStepIslandUid(self, area, connectors=None):
        # the island the goal is located on, the client places the quest
        # dart on it's world map at this island...
        if connectors is None:
            connectors = self.getQuestStepConnectors()

        island = self.getQuestStepIsland(area, connectors) if area is not None else None
        return island.getUniqueId() if island is not None else ''


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def giveQuest(questId):
    invoker = spellbook.getInvoker()
    if base.air.questMgr.hasQuest(invoker, questId=questId):
        return 'Avatar already has active quest: %s!' % questId

    base.air.questMgr.createQuest(invoker, questId)
    return 'Given new active quest: %s.' % questId


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def dropQuest(questId):
    invoker = spellbook.getInvoker()
    activeQuest = base.air.questMgr.getQuest(invoker, questId=questId)
    if not activeQuest:
        return 'Could not find active quest: %s!' % questId

    base.air.questMgr.dropQuest(invoker, activeQuest)
    return 'Dropped active quest: %s!' % questId


@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def dropAllQuests():
    base.air.questMgr.dropQuests(spellbook.getInvoker())
    return 'Dropped all active quests.'


@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def skipQuest(questId=''):
    invoker = spellbook.getInvoker()
    if not questId:
        questId = invoker.getActiveQuest()

    if not questId:
        return 'You did not provide a valid questId!'

    quest = base.air.questMgr.getQuest(invoker, questId=questId)
    if not quest:
        return 'Could not find active quest: %s!' % questId

    for taskState in quest.getTaskStates():
        taskState.forceComplete()

    base.air.questMgr.completeQuest(invoker, quest)
    return 'Forced quest: %s completion status.' % questId
