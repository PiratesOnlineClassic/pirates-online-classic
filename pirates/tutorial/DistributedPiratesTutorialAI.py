from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

from pirates.piratesbase import PiratesGlobals
from pirates.tutorial import TutorialGlobals


class DistributedPiratesTutorialAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPiratesTutorialAI')
    notify.setInfo(True)

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'DistributedPiratesTutorialAI')

        self.avatarId = None

    def setAvatarId(self, avatarId):
        self.avatarId = avatarId

    def getAvatar(self):
        if self.avatarId:
            return self.air.doId2do.get(self.avatarId)
        return None

    # --------------------------------------------------
    # Client -> AI messages (airecv clsend)
    # --------------------------------------------------

    def clientEnterAct0Tutorial(self):
        """Client has reached Act0Tutorial and is ready to begin.

        The avatar was already spawned in the jail interior by TutorialFSM,
        so no server-side teleport is needed here.
        """
        avatar = self.getAvatar()
        if not avatar:
            self.notify.warning('clientEnterAct0Tutorial: avatar %s not found' % self.avatarId)
            return

        self.notify.info('Avatar %d entered Act0Tutorial' % self.avatarId)
        self.request('Act0Tutorial')

    def makeAPirateComplete(self):
        """Client finished the Make-A-Pirate customization screen.

        Advance the tutorial flag, create the first quest, and signal the
        client to fade in.
        """
        avatar = self.getAvatar()
        if not avatar:
            self.notify.warning('makeAPirateComplete: avatar %s not found' % self.avatarId)
            return

        self.notify.info('Avatar %d completed Make-A-Pirate' % self.avatarId)

        # Mark customisation complete so later logins skip this step.
        avatar.b_setTutorial(PiratesGlobals.TUT_MADE_PIRATE)

        # Give the first tutorial quest (Jack Sparrow jail-break storyline).
        if not self.air.questMgr.hasQuest(avatar, questId=TutorialGlobals.FIRST_QUEST):
            self.air.questMgr.createQuest(avatar, TutorialGlobals.FIRST_QUEST)

        self.d_makeAPirateCompleteResp()

    def giveInitQuest(self, questType):
        """Client requests an initial quest.

        questType 0 → FIRST_QUEST  (Chapter1.rung1)
        questType 1 → SECOND_QUEST (Chapter1.rung2)
        """
        avatar = self.getAvatar()
        if not avatar:
            return

        questId = TutorialGlobals.FIRST_QUEST if questType == 0 else TutorialGlobals.SECOND_QUEST
        self.notify.info('Avatar %d requesting quest %s (type %d)' % (self.avatarId, questId, questType))

        if not self.air.questMgr.hasQuest(avatar, questId=questId):
            self.air.questMgr.createQuest(avatar, questId)

    def autoVisit(self, npcDoId):
        """Client triggered a proximity-based auto-visit with an NPC or object.

        Used for scripted encounters: Dan gives the quest for Stumpy, the boat
        proximity triggers the boarding sequence, etc.
        """
        avatar = self.getAvatar()
        if not avatar:
            return

        self.notify.info('Avatar %d auto-visiting doId %d' % (self.avatarId, npcDoId))

        npc = self.air.doId2do.get(npcDoId)
        if npc and hasattr(npc, 'getUniqueId'):
            self.air.questMgr.requestInteract(avatar, npc)

    def tutorialSeachestFinished(self):
        """Client finished the sea-chest tutorial segment."""
        avatar = self.getAvatar()
        if not avatar:
            return

        self.notify.info('Avatar %d finished seachest tutorial' % self.avatarId)
        avatar.b_setTutorial(PiratesGlobals.TUT_GOT_SEACHEST)

    def boardedTutorialShip(self):
        """Client boarded Stumpy's boat."""
        avatar = self.getAvatar()
        if not avatar:
            return

        self.notify.info('Avatar %d boarded tutorial ship' % self.avatarId)
        self.request('BoardedShip')

    def startSailingStumpy(self):
        """Client started sailing with Stumpy (cannon practice phase)."""
        avatar = self.getAvatar()
        if not avatar:
            return

        self.notify.info('Avatar %d started sailing with Stumpy' % self.avatarId)
        self.request('Sailing')

    def targetPracticeDone(self):
        """Client finished cannon target practice."""
        avatar = self.getAvatar()
        if not avatar:
            return

        self.notify.info('Avatar %d finished target practice' % self.avatarId)
        self.request('TargetPracticeDone')

    # --------------------------------------------------
    # AI -> Client messages
    # --------------------------------------------------

    def d_makeAPirateCompleteResp(self):
        """Broadcast the fade-in signal after Make-A-Pirate completes."""
        self.sendUpdate('makeAPirateCompleteResp', [])

    def d_inventoryFailed(self):
        """Tell the client inventory creation failed so it can bail out."""
        self.sendUpdate('inventoryFailed', [])

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
