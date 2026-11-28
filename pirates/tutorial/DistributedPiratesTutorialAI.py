from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from direct.showbase.MessengerGlobal import messenger
from direct.task import Task

from pirates.npc.DistributedNPCTownfolkAI import DistributedNPCTownfolkAI
from pirates.piratesbase import PiratesGlobals
from pirates.quest import QuestDB
from pirates.quest.QuestConstants import LocationIds
from pirates.tutorial import TutorialGlobals


class DistributedPiratesTutorialAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPiratesTutorialAI')
    notify.setInfo(True)

    INVENTORY_WAIT_SECONDS = 1.0
    INVENTORY_WAIT_ATTEMPTS = 15

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'DistributedPiratesTutorialAI')

        self.avatarId = None
        self._firstQuestCreatePending = False
        self._firstQuestFinalizeStarted = False
        self._pendingMakeAPirateComplete = False
        self._inventoryWaitAttempts = 0

    def delete(self):
        taskMgr.remove(self.uniqueName('waitForInventory'))
        DistributedObjectAI.delete(self)

    def setAvatarId(self, avatarId):
        self.avatarId = avatarId

    def getAvatar(self):
        if self.avatarId:
            return self.air.doId2do.get(self.avatarId)
        return None

    def _getAvatarFromSender(self, action):
        senderId = self.air.getAvatarIdFromSender()
        if senderId != self.avatarId:
            self.notify.warning(
                'Ignoring %s from avatar %s; tutorial handler belongs to avatar %s' %
                (action, senderId, self.avatarId))
            return None

        avatar = self.getAvatar()
        if not avatar:
            self.notify.warning('%s: avatar %s not found' % (action, self.avatarId))
        return avatar

    def _firstQuestIsComplete(self, avatar):
        questDNA = QuestDB.QuestDict.get(TutorialGlobals.FIRST_QUEST)
        return bool(
            questDNA and questDNA.getQuestInt() in avatar.getQuestHistory())

    def _sendQuestEvent(self, quest, event):
        messenger.send('%s-%d' % (event, quest.doId))

    def _startFirstQuestFinalization(self, avatar, quest, finalizeIndex):
        if self._firstQuestIsComplete(avatar):
            self._pendingMakeAPirateComplete = False
            self.air.questMgr.resumeCompletedTutorialQuest(avatar)
            return

        if self._firstQuestFinalizeStarted or quest.isFinalized():
            return

        self._firstQuestFinalizeStarted = True
        self.air.questMgr.finalizeCutscene(
            avatar, quest, finalizeIndex=finalizeIndex)

        if self._pendingMakeAPirateComplete:
            self._pendingMakeAPirateComplete = False
            self._sendQuestEvent(quest, 'makeAPirateComplete')

    def _ensureFirstQuest(self, avatar):
        if self._firstQuestCreatePending or self._firstQuestFinalizeStarted:
            return

        questMgr = self.air.questMgr
        if self._firstQuestIsComplete(avatar):
            questMgr.resumeCompletedTutorialQuest(avatar)
            return

        self._firstQuestCreatePending = True

        def questIdle():
            if self._firstQuestIsComplete(avatar):
                self._firstQuestCreatePending = False
                self._pendingMakeAPirateComplete = False
                questMgr.resumeCompletedTutorialQuest(avatar)
                return

            quest = questMgr.getQuest(
                avatar, questId=TutorialGlobals.FIRST_QUEST)
            if quest:
                self._firstQuestCreatePending = False
                tutorialState = avatar.getTutorial()
                if tutorialState >= PiratesGlobals.TUT_GOT_SEACHEST:
                    self._pendingMakeAPirateComplete = False
                    return

                finalizeIndex = int(
                    tutorialState >= PiratesGlobals.TUT_MADE_PIRATE)
                if self._pendingMakeAPirateComplete:
                    finalizeIndex = max(finalizeIndex, 1)
                self._startFirstQuestFinalization(avatar, quest, finalizeIndex)
                return

            if avatar.getTutorial() != 0:
                self._firstQuestCreatePending = False
                self._pendingMakeAPirateComplete = False
                self.notify.warning(
                    'Avatar %d has tutorial state %d but no active %s quest; '
                    'not recreating a completed or later quest' %
                    (avatar.doId, avatar.getTutorial(), TutorialGlobals.FIRST_QUEST))
                return

            def questCreated(createdQuest=None):
                self._firstQuestCreatePending = False
                if not createdQuest:
                    self._pendingMakeAPirateComplete = False
                    self.notify.warning(
                        'Failed to create %s for avatar %d' %
                        (TutorialGlobals.FIRST_QUEST, avatar.doId))
                    if not avatar.getInventory():
                        self.d_inventoryFailed()
                    return

                tutorialState = avatar.getTutorial()
                finalizeIndex = int(
                    tutorialState >= PiratesGlobals.TUT_MADE_PIRATE)
                if self._pendingMakeAPirateComplete:
                    finalizeIndex = max(finalizeIndex, 1)
                self._startFirstQuestFinalization(
                    avatar, createdQuest, finalizeIndex)

            questMgr.createQuest(
                avatar, TutorialGlobals.FIRST_QUEST, questCreated)

        questMgr.whenQuestIdle(avatar, questIdle)

    # --------------------------------------------------
    # Client -> AI messages (airecv clsend)
    # --------------------------------------------------

    def clientEnterAct0Tutorial(self):
        """Client has reached Act0Tutorial and is ready to begin.

        The avatar was already spawned in the jail interior by TutorialFSM,
        so no server-side teleport is needed here.
        """
        avatar = self._getAvatarFromSender('clientEnterAct0Tutorial')
        if not avatar:
            return

        self.notify.info('Avatar %d entered Act0Tutorial' % self.avatarId)
        self.request('Act0Tutorial')
        if not avatar.getInventory():
            # The tutorial quests live on the avatar's inventory, wait for it
            # to finish loading before handing out the first quest...
            self._inventoryWaitAttempts = 0
            taskMgr.remove(self.uniqueName('waitForInventory'))
            taskMgr.doMethodLater(self.INVENTORY_WAIT_SECONDS, self.__waitForInventory,
                self.uniqueName('waitForInventory'))
            return

        self._ensureFirstQuest(avatar)

    def __waitForInventory(self, task):
        avatar = self.getAvatar()
        if not avatar:
            return Task.done

        if avatar.getInventory():
            self._ensureFirstQuest(avatar)
            return Task.done

        self._inventoryWaitAttempts += 1
        if self._inventoryWaitAttempts >= self.INVENTORY_WAIT_ATTEMPTS:
            self.notify.warning('Avatar %d has no inventory, cannot start the tutorial!' % avatar.doId)
            self.d_inventoryFailed()
            return Task.done

        return Task.again

    def makeAPirateComplete(self):
        """Client finished the Make-A-Pirate customization screen.

        Continue the first quest's Make-A-Pirate wait event and signal the
        client to fade in. The client tutorial checkpoint update is replicated
        through HumanDNA.setTutorial.
        """
        avatar = self._getAvatarFromSender('makeAPirateComplete')
        if not avatar:
            return

        self.notify.info('Avatar %d completed Make-A-Pirate' % self.avatarId)

        if self._firstQuestIsComplete(avatar):
            self.air.questMgr.resumeCompletedTutorialQuest(avatar)
            self.d_makeAPirateCompleteResp()
            return

        quest = self.air.questMgr.getQuest(
            avatar, questId=TutorialGlobals.FIRST_QUEST)
        if quest:
            if not self._firstQuestFinalizeStarted:
                self._startFirstQuestFinalization(avatar, quest, 1)
            self._sendQuestEvent(quest, 'makeAPirateComplete')
        elif self._firstQuestCreatePending:
            self._pendingMakeAPirateComplete = True

        self.d_makeAPirateCompleteResp()

    def giveInitQuest(self, questType):
        """Accept only the initial rung; later rungs are quest-manager driven."""
        avatar = self._getAvatarFromSender('giveInitQuest')
        if not avatar:
            return

        if questType == 0:
            self._ensureFirstQuest(avatar)
        elif questType == 1:
            self.notify.warning(
                'Ignoring manual request for %s; quest progression is managed by QuestManagerAI' %
                TutorialGlobals.SECOND_QUEST)
        else:
            self.notify.warning(
                'Ignoring invalid initial quest type %s from avatar %d' %
                (questType, self.avatarId))

    def autoVisit(self, npcDoId):
        """Client triggered a proximity-based auto-visit with an NPC or object.

        Tutorial NPC and Stumpy-boat visits are handled by the quest manager.
        """
        avatar = self._getAvatarFromSender('autoVisit')
        if not avatar:
            return

        self.notify.info('Avatar %d auto-visiting doId %d' % (self.avatarId, npcDoId))

        target = self.air.doId2do.get(npcDoId)
        if not target or not hasattr(target, 'getUniqueId'):
            return

        uniqueId = target.getUniqueId()
        isDan = (uniqueId == TutorialGlobals.DAN_UID and
                 isinstance(target, DistributedNPCTownfolkAI))
        isStumpyBoat = uniqueId == TutorialGlobals.STUMPY_BOAT_UID
        if isDan or isStumpyBoat:
            self.air.questMgr.requestInteract(avatar, target)
        else:
            self.notify.warning(
                'Ignoring unsupported tutorial auto-visit target %s (%d)' %
                (uniqueId, npcDoId))

    def tutorialSeachestFinished(self):
        """Compatibility RPC; quest finalization owns the sea-chest checkpoint."""
        avatar = self._getAvatarFromSender('tutorialSeachestFinished')
        if not avatar:
            return

        self.notify.info('Avatar %d finished seachest tutorial' % self.avatarId)

    def boardedTutorialShip(self):
        """Client boarded Stumpy's boat."""
        avatar = self._getAvatarFromSender('boardedTutorialShip')
        if not avatar:
            return

        self.notify.info('Avatar %d boarded tutorial ship' % self.avatarId)
        self.request('BoardedShip')

    def startSailingStumpy(self):
        """Client started sailing with Stumpy (cannon practice phase)."""
        avatar = self._getAvatarFromSender('startSailingStumpy')
        if not avatar:
            return

        tutorialFSM = self.air.tutorialManager.avatar2fsm.get(avatar.doId)
        if not tutorialFSM or tutorialFSM.tutorialHandler is not self:
            self.notify.warning('Ignoring sailing request from inactive tutorial handler')
            return

        from pirates.ship.TutorialShipAI import TutorialShipAI
        from pirates.world import WorldGlobals

        ship = self.air.uidMgr.justGetMeMeObject(TutorialGlobals.STUMPY_BOAT_UID)
        builder = getattr(ship, 'tutorialBuilder', None)
        world = getattr(builder, 'parent', None)
        if (not isinstance(ship, TutorialShipAI)
                or ship.getUniqueId() != TutorialGlobals.STUMPY_BOAT_UID
                or not world
                or world.getFileName() != WorldGlobals.PiratesTutorialSceneFileBase):
            self.notify.warning('Cannot start sailing: tutorial ship is unavailable')
            return

        self.notify.info('Avatar %d started sailing with Stumpy' % self.avatarId)
        if not ship.startSailing():
            self.notify.warning('Failed to start tutorial ship sailing')
            return
        self.request('Sailing')

    def targetPracticeDone(self):
        """Client finished target practice and reached the Jolly Roger stage."""
        avatar = self._getAvatarFromSender('targetPracticeDone')
        if not avatar:
            return

        self.notify.info('Avatar %d finished target practice' % self.avatarId)

        # once the Jolly Roger sinks Stumpy's boat the client initiates a teleport
        # to the main world using it's return location, new pirates wash up in Port Royal...
        if avatar.getReturnLocation() != LocationIds.PORT_ROYAL_ISLAND:
            avatar.b_setReturnLocation(LocationIds.PORT_ROYAL_ISLAND)

        self.air.questMgr.tutorialJROnStage(avatar)
        self.request('TargetPracticeDone')

    # --------------------------------------------------
    # AI -> Client messages
    # --------------------------------------------------

    def d_makeAPirateCompleteResp(self):
        """Send the fade-in signal only to this tutorial handler's owner."""
        if self.avatarId:
            self.sendUpdateToAvatarId(self.avatarId, 'makeAPirateCompleteResp', [])

    def d_inventoryFailed(self):
        """Tell the client inventory creation failed so it can bail out."""
        if self.avatarId:
            self.sendUpdateToAvatarId(self.avatarId, 'inventoryFailed', [])

    # --------------------------------------------------
    # FSM States
    # --------------------------------------------------

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterAct0Tutorial(self):
        """Player is in the jail cell.  The Jack Sparrow cutscene is entirely
        client-driven; the server just needs to be in this state."""
        self.notify.info('Avatar %d: Act0Tutorial started' % (self.avatarId or 0))

    def exitAct0Tutorial(self):
        pass

    def enterBoardedShip(self):
        self.notify.info('Avatar %d: boarded Stumpy\'s ship' % (self.avatarId or 0))

    def exitBoardedShip(self):
        pass

    def enterSailing(self):
        self.notify.info('Avatar %d: sailing with Stumpy' % (self.avatarId or 0))

    def exitSailing(self):
        pass

    def enterTargetPracticeDone(self):
        self.notify.info('Avatar %d: cannon target practice complete' % (self.avatarId or 0))

    def exitTargetPracticeDone(self):
        pass
