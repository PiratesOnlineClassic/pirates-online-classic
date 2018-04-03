# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.DistributedQuestGiver
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import getShortestRotation
from direct.showbase.ShowBaseGlobal import *
from otp.avatar import Avatar
from otp.otpgui import OTPDialog
from pandac.PandaModules import *
from pirates.distributed import InteractGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import BlackPearlCrew, PDialog, RewardPanel
from pirates.quest import (QuestConstants, QuestDB, QuestLadderDB,
                           QuestMenuGUI, QuestParser, QuestTaskDNA)
from pirates.quest.QuestDetailGUI import QuestDetailGUI
from pirates.reputation.ReputationGlobals import getLevelFromTotalReputation


class DistributedQuestGiver(Avatar.Avatar):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedQuestGiver')
    NoOffer = 0
    LadderOffer = 1
    QuestOffer = 2
    InteractOffer = 3
    QuestIconWorkTexture = None
    QuestIconStoryTexture = None
    QuestIconProgressTexture = None
    QuestIconCompleteTexture = None
    QuestIconDontCare = 1
    QuestIconStory = 2
    QuestIconWork = 3
    QuestIconNew = 1
    QuestIconProgress = 2
    QuestIconComplete = 3

    def __init__(self):
        self.playingQuestString = False
        self.dialogOpen = False
        self.newOffer = False
        self.offers = None
        self.offerType = self.NoOffer
        self.dialogFlag = 0
        self.firstDialog = True
        self.newDialog = False
        self.npcMoviePlayer = None
        self.quitButton = 0
        self.nametagIcon = None
        self.nametagIconGlow = None
        self.containerId = None
        self.rewardPanel = None
        return

    def generate(self):
        DistributedQuestGiver.notify.debug('generate(%s)' % self.doId)
        self.questMenuGUI = None
        self.questDetailGUI = None
        self.questDetailCamera = None
        return

    def announceGenerate(self):
        DistributedQuestGiver.notify.debug('announceGenerate(%s)' % self.doId)

    def disable(self):
        DistributedQuestGiver.notify.debug('disable(%s)' % self.doId)
        if self.npcMoviePlayer:
            self.npcMoviePlayer.cleanup()
            self.npcMoviePlayer = None
        self.cleanUpQuestMenu()
        self.cleanUpQuestDetails()
        self.questMenuGUI = None
        self.questDetailGUI = None
        if self.rewardPanel:
            self.rewardPanel.cleanup()
            self.rewardPanel = None
        self.ignore('lastSubtitlePage')
        return

    def cleanUpQuestMenu(self):
        if self.questMenuGUI:
            self.questMenuGUI.destroy()
            self.questMenuGUI = None
        return

    def cleanUpQuestDetails(self, hide=False):
        if self.questDetailGUI:
            if hide:
                self.questDetailGUI.hidePanelAndDestroy()
            else:
                self.questDetailGUI.destroy()
            self.questDetailGUI = None
        if not hide and self.questDetailCamera:
            self.questDetailCamera.finish()
            self.questDetailCamera = None
        return

    def delete(self):
        DistributedQuestGiver.notify.debug('delete(%s)' % self.doId)

    def offerOptions(self):
        self.notify.warning('offerOptions() needs override!')

    def cancelInteraction(self, av):
        self.notify.warning('cancelInteraction() needs override!')

    def hasOpenGUI(self):
        self.notify.warning('hasOpenGUI() needs override!')
        return False

    def hasQuestOffers(self):
        AvailableQuests = []
        inventory = localAvatar.getInventory()
        for questId, questDNA in QuestDB.QuestDict.items():
            prereqExcludes = base.config.GetString('exclude-prereq-quests', '')
            if len(prereqExcludes):
                if questId in prereqExcludes:
                    continue
            prereqs = questDNA.getPrereqs()
            boolWeapLvlCheck = (questDNA.weapLvlType != None) & (questDNA.minWeapLevel > 0)
            for prereq in prereqs:
                if prereq.giverMatters():
                    if prereq.giverCanGive(self.getUniqueId()):
                        if questDNA.minLevel > localAvatar.level:
                            pass
                        elif not base.cr.questDependency.checkDependency(questId, localAvatar.getQuestLadderHistory(), 1):
                            pass
                        elif boolWeapLvlCheck & (questDNA.minWeapLevel > getLevelFromTotalReputation(questDNA.weapLvlType, inventory.getReputation(questDNA.weapLvlType))[0]):
                            pass
                        elif questDNA.getAcquireOnce():
                            history = localAvatar.getQuestLadderHistory()
                            questLadderId = base.cr.questDynMap.findQuestLadderInt(questId)
                            containsLadderId = history.count(questLadderId)
                            if containsLadderId:
                                pass
                            else:
                                AvailableQuests.append(questDNA)
                        else:
                            AvailableQuests.append(questDNA)

        if len(AvailableQuests):
            inventory = localAvatar.getInventory()
            if inventory:
                toRemove = []
                questList = inventory.getQuestList()
                for questDNA in AvailableQuests:
                    found = False
                    for quest in questList:
                        questId = questDNA.getQuestId()
                        if questId == quest.getQuestId() or localAvatar.questStatus.hasLadderQuestId(questId):
                            found = True

                    if found:
                        toRemove.append(questDNA)

                for questDNA in toRemove:
                    AvailableQuests.remove(questDNA)

        return len(AvailableQuests) > 0

    def receiveOffer(self, offerType):
        self.newOffer = True
        self.offerType = offerType

    def clearOffer(self):
        self.newOffer = False
        self.offerType = self.NoOffer

    def presentOffer(self):
        if self.newOffer == False:
            if len(localAvatar.currentStoryQuests):
                storyQuest = localAvatar.currentStoryQuests[0]
                self.presentQuestGiven(storyQuest)
                localAvatar.currentStoryQuests.remove(storyQuest)
            return
        if self.offerType == self.QuestOffer:
            self.presentQuestOffer(self.offers)
        else:
            if self.offerType == self.LadderOffer:
                self.presentQuestOffer(self.offers, ladder=True)
            else:
                if self.offerType == self.InteractOffer:
                    self.offerOptions(self.dialogFlag)
                else:
                    if self.offerType == self.NoOffer:
                        self.notify.warning('offerType == No Offer')
        self.clearOffer()

    def setQuestOffer(self, offers):
        self.receiveOffer(self.QuestOffer)
        self.offers = offers
        if not self.playingQuestString:
            self.presentQuestOffer(self.offers)

    def setQuestLadderOffer(self, offers, quitButton):
        self.receiveOffer(self.LadderOffer)
        self.offers = offers
        self.quitButton = quitButton
        if not self.playingQuestString:
            self.presentQuestOffer(self.offers, ladder=True)

    def presentQuestOffer(self, offers, ladder=False):
        if self.questMenuGUI:
            DistributedQuestGiver.notify.warning('setQuestOffer: old questMenu GUI still around')
            self.cleanUpQuestMenu()
        self.cleanUpQuestDetails()

        def handleSelection(offer, self=self, offers=offers):
            self.cleanUpQuestMenu()
            if offer == QuestConstants.CANCEL_QUEST:
                index = QuestConstants.CANCEL_QUEST
            else:
                index = offers.index(offer)
            self.sendOfferResponse(index, ladder)

        def handleOption(option, offer):
            self.adjustNPCCamera('back')
            self.cleanUpQuestDetails(hide=True)
            self.ignore('lastSubtitlePage')
            if self.questMenuGUI:
                self.questMenuGUI.show()
            if option == PLocalizer.Accept:
                handleSelection(offer)

        def displayQuestDetails(offer):
            self.questDetailGUI = QuestDetailGUI(offer, None)
            base.questdet = self.questDetailGUI
            return

        def describeQuest(offer):
            self.adjustNPCCamera('forward')
            questDNA = offer.getQuestDNA()
            if questDNA:
                questStr = questDNA.getDialogBefore()
                self.acceptOnce('lastSubtitlePage', displayQuestDetails, [offer])
                localAvatar.guiMgr.subtitler.setPageChat(questStr, options=[PLocalizer.Decline, PLocalizer.Accept], callback=handleOption, extraArgs=[offer])

        def questFull(arg):
            self.cleanUpQuestMenu()
            self.sendOfferResponse(QuestConstants.CANCEL_QUEST, ladder)

        inv = base.localAvatar.getInventory()
        numWorkQuests = 0
        if inv:
            questList = inv.getQuestList()
            for questId in questList:
                if not QuestLadderDB.getFamePath(questId):
                    numWorkQuests += 1

        if numWorkQuests > QuestConstants.MAXIMUM_MERC_WORK:
            self.questMenuGUI = PDialog.PDialog(text=PLocalizer.QuestFull, style=OTPDialog.Acknowledge, command=questFull)
        else:
            self.questMenuGUI = QuestMenuGUI.QuestMenuGUI(offers, handleSelection, describeQuest)
        self.clearOffer()

    def presentQuestGiven(self, quest):

        def handleOption(option):
            if len(localAvatar.currentStoryQuests):
                self.cleanUpQuestDetails(hide=True)
                storyQuest = localAvatar.currentStoryQuests[0]
                self.presentQuestGiven(storyQuest)
                localAvatar.currentStoryQuests.remove(storyQuest)
            else:
                self.__handleDoneChatPage(0)

        self.questDetailGUI = QuestDetailGUI(None, None, quest)
        localAvatar.guiMgr.subtitler.setPageChat('', options=[PLocalizer.Accept], callback=handleOption)
        base.questdet = self.questDetailGUI
        self.ignore('doneChatPage')
        return

    def adjustNPCCamera(self, direction):
        dummy = NodePath('dummy')
        dummy.reparentTo(camera)
        if direction == 'forward':
            dummy.setH(dummy, -15)
            dummy.setY(dummy, 0.75)
            duration = 0.7
        else:
            dummy.setY(dummy, -0.75)
            dummy.setH(dummy, 15)
            duration = 0.5
        dummy.wrtReparentTo(camera.getParent())
        camH, dummyH = getShortestRotation(camera.getH(), dummy.getH())
        self.questDetailCamera = Parallel(LerpFunc(camera.setH, duration=duration, fromData=camH, toData=dummyH, blendType='easeInOut'), LerpFunc(camera.setY, duration=duration, fromData=camera.getY(), toData=dummy.getY(), blendType='easeInOut'))
        dummy.removeNode()
        self.questDetailCamera.start()

    def getOfferedQuests(self):
        return list(self.offers)

    def sendOfferResponse(self, index, ladder=False):
        if index == QuestConstants.CANCEL_QUEST:
            self.dialogOpen = False
        self.sendUpdate('setOfferResponse', [index, ladder])
        self.offers = None
        self.clearOffer()
        return

    def b_setPageNumber(self, paragraph, pageNumber):
        self.setPageNumber(paragraph, pageNumber)
        self.d_setPageNumber(paragraph, pageNumber)

    def d_setPageNumber(self, paragraph, pageNumber):
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.sendUpdate('setPageNumber', [paragraph, pageNumber, timestamp])

    def playQuestString(self, questStr, timeout=False, quitButton=1, useChatBubble=False, confirm=False):
        self.notify.debug('playQuestString %s, %s, %s, %s' % (timeout, quitButton, useChatBubble, confirm))
        if questStr.find('quest_') == 0:
            nmp = QuestParser.NPCMoviePlayer(questStr, localAvatar, self)
            nmp.play()
            self.npcMoviePlayer = nmp
        else:
            self.firstDialog = False
            if questStr:
                if timeout:
                    if useChatBubble:
                        self.setPageChat(localAvatar.doId, 0, questStr, 0, extraChatFlags=CFSpeech | CFTimeout, pageButton=False)
                    else:
                        base.localAvatar.guiMgr.subtitler.setPageChat(questStr, timeout=timeout)
                    return
                else:
                    self.playingQuestString = True
                    if self.newOffer == False:
                        questStr += '\x07'
                    base.localAvatar.guiMgr.subtitler.setPageChat(questStr, confirm=confirm)
                    self.dialogOpen = True
                if quitButton == 1 or confirm:
                    self.accept('doneChatPage', self.__handleDoneChatPage)
                if base.localAvatar.guiMgr.subtitler.getNumChatPages() == 1:
                    self.__handleNextChatPage(0, 0)
                else:
                    self.accept('nextChatPage', self.__handleNextChatPage)

    def __handleNextChatPage(self, pageNumber, elapsed):
        self.notify.debug('handleNextChatPage pageNumber = %s, elapsed = %s' % (pageNumber, elapsed))
        if pageNumber == base.localAvatar.guiMgr.subtitler.getNumChatPages() - 1:
            self.ignore('nextChatPage')
            self.playingQuestString = False
            if base.config.GetBool('want-blackpearl-gui', 0):
                self.showBlackPearlCrew()
            self.presentOffer()

    def __handleDoneChatPage(self, elapsed):
        self.ignore('nextChatPage')
        self.ignore('doneChatPage')
        self.playingQuestString = False
        self.dialogOpen = False
        if self.newDialog:
            self.playDialog()
        if not self.hasOpenGUI():
            self.interactMode = 1
            self.cancelInteraction(base.localAvatar)
        if self.containerId and self.containerId == 'MainStory':

            def cleanupReward():
                if self.rewardPanel:
                    self.rewardPanel.cleanup()
                    self.rewardPanel = None
                return

            self.rewardPanel = RewardPanel.RewardPanel(aspect2d, doneCallback=cleanupReward)

    def playDialog(self):
        self.notify.warning('playDialog() needs override!')

    def setQuestsCompleted(self, menuFlag, completedContainerIds, completedChainedQuestIds, completedQuestIds, completedQuestDoIds):
        questStr = ''
        if len(completedContainerIds):
            if len(completedContainerIds) > 1:
                self.notify.warning('Multiple simultaneous completed quest containers for the same NPC: %s!' % completedContainerIds)
            containerId = completedContainerIds[0]
            self.containerId = containerId
            container = QuestLadderDB.getContainer(containerId)
            if container:
                questStr = container.getDialogAfter()
                localAvatar.b_setGameState('NPCInteract', localArgs=[self, False])
                self.playQuestString(questStr, quitButton=menuFlag, confirm=True)
                return
            else:
                self.notify.warning('%s not in QuestLadderDB!' % containerId)
        if len(completedChainedQuestIds):
            pass
        if len(completedQuestIds):
            if len(completedContainerIds) == 0:
                questId = completedQuestIds[0]
                quest = QuestDB.QuestDict.get(questId)
                if quest:
                    questStr = quest.getDialogAfter()
                    self.notify.debug('%s dialogAfter: %s' % (questId, questStr))
                    self.playQuestString(questStr, quitButton=menuFlag, confirm=True)
                else:
                    self.notify.warning('%s not in QuestDB!' % questId)
            localAvatar.b_setGameState('NPCInteract', localArgs=[self, True])
        if len(completedQuestIds) == 0 and len(completedChainedQuestIds) == 0 and len(completedContainerIds) == 0:
            if not self.hasOpenGUI():
                self.cancelInteraction(base.localAvatar)

    def playDialogMovie(self, dialogId, doneCallback=None, oldLocalAvState=None):
        movieChoice = InteractGlobals.getNPCTutorial(dialogId)
        if movieChoice == None:
            movieChoice = dialogId
        globalClock.tick()
        self.currentDialogMovie = QuestParser.NPCMoviePlayer(movieChoice, localAvatar, self)
        self.currentDialogMovie.overrideOldAvState(oldLocalAvState)
        self.currentDialogMovie.play()
        self.acceptOnce('dialogFinish', self.stopDialogMovie, extraArgs=[doneCallback])
        return

    def stopDialogMovie(self, doneCallback):
        if hasattr(self, 'currentDialogMovie'):
            self.currentDialogMovie.npc.showName()
            self.currentDialogMovie.npc.nametag3d.setZ(0)
            self.currentDialogMovie.finishUpAll()
            del self.currentDialogMovie
            self.sendUpdate('dialogMovieComplete')
            if doneCallback:
                doneCallback()

    def swapCurrentDialogMovie(self, newDialogMovie):
        if hasattr(self, 'currentDialogMovie'):
            if newDialogMovie:
                oldAvState = self.currentDialogMovie.overrideOldAvState(None)
                newDialogMovie.overrideOldAvState(oldAvState)
            self.currentDialogMovie.finishUpAll()
        self.currentDialogMovie = newDialogMovie
        return

    def getQuestGiverId(self):
        return self.getUniqueId()

    def hasQuestOffersForLocalAvatar(self):
        av = localAvatar
        inventory = av.getInventory()
        selfId = self.getQuestGiverId()
        if inventory:
            numInProgress = 0
            for quest in inventory.getQuestList():
                questType = self.QuestIconDontCare
                if quest.tasks is None:
                    self.notify.warning('quest %s: does not contain a dna; potential for crash.' % quest.getQuestId())
                    return False
                for task, taskState in zip(quest.tasks, quest.taskStates):
                    if isinstance(task, QuestTaskDNA.VisitTaskDNA):
                        if task.npcId == selfId:
                            questStatus = self.QuestIconComplete
                            return (
                             questType, questStatus)

                if quest.canBeReturnedTo(selfId):
                    if quest.isComplete():
                        questStatus = self.QuestIconComplete
                        return (
                         questType, questStatus)
                    else:
                        numInProgress += 1

        else:
            self.notify.warning('avatar does not have inventory yet')
            return False
        offerDict = {}
        fromQuests = []
        for questId, questDNA in QuestDB.QuestDict.items():
            prereqExcludes = base.config.GetString('exclude-prereq-quests', '')
            if len(prereqExcludes):
                if questId in prereqExcludes:
                    continue
            boolWeapLvlCheck = (questDNA.weapLvlType != None) & (questDNA.minWeapLevel > 0)
            for prereq in questDNA.prereqs:
                if prereq.giverMatters():
                    if prereq.giverCanGive(selfId):
                        if questDNA.minLevel > localAvatar.level:
                            pass
                        elif not base.cr.questDependency.checkDependency(questId, localAvatar.getQuestLadderHistory(), 1):
                            pass
                        elif boolWeapLvlCheck & (questDNA.minWeapLevel > getLevelFromTotalReputation(questDNA.weapLvlType, inventory.getReputation(questDNA.weapLvlType))[0]):
                            pass
                        elif questDNA.getAcquireOnce():
                            history = localAvatar.getQuestLadderHistory()
                            questLadderId = base.cr.questDynMap.findQuestLadderInt(questId)
                            containsLadderId = history.count(questLadderId)
                            if containsLadderId:
                                pass
                            else:
                                fromQuests.append(questDNA)
                        else:
                            fromQuests.append(questDNA)

        if len(fromQuests):
            inventory = av.getInventory()
            if inventory:
                toRemove = []
                questList = inventory.getQuestList()
                for questDNA in fromQuests:
                    found = False
                    for quest in questList:
                        questId = questDNA.questId
                        if questId == quest.questId or av.questStatus.hasLadderQuestId(questId):
                            found = True

                    if found:
                        toRemove.append(questDNA)

                for questDNA in toRemove:
                    fromQuests.remove(questDNA)

        if fromQuests:
            questType = self.QuestIconWork
            for quest in fromQuests:
                if QuestLadderDB.getFamePath(quest.questId):
                    questType = self.QuestIconStory
                    break

            questStatus = self.QuestIconNew
            return (
             questType, questStatus)
        if numInProgress:
            questStatus = self.QuestIconProgress
            return (
             questType, questStatus)
        return False

    def loadQuestIcons(self):
        if not DistributedQuestGiver.QuestIconWorkTexture:
            DistributedQuestGiver.QuestIconWorkTexture = loader.loadModel('models/gui/new_work_quest_icon')
            DistributedQuestGiver.QuestIconStoryTexture = loader.loadModel('models/gui/new_story_quest_icon')
            discardNP = DistributedQuestGiver.QuestIconStoryTexture.find('**/pPlane2')
            if not discardNP.isEmpty():
                discardNP.removeNode()
            gui = loader.loadModel('models/gui/toplevel_gui')
            DistributedQuestGiver.QuestIconProgressTexture = gui.find('**/quest_pending_icon')
            DistributedQuestGiver.QuestIconCompleteTexture = gui.find('**/reward_waiting_icon')

    def updateNametagQuestIcon(self, questId=None, item=None, note=None):
        offers = self.hasQuestOffersForLocalAvatar()
        if offers:
            if self.nametagIcon:
                self.nametagIcon.removeNode()
            if self.nametagIconGlow:
                self.nametagIconGlow.removeNode()
            self.loadQuestIcons()
            type, status = offers
            if status == DistributedQuestGiver.QuestIconNew:
                if type == DistributedQuestGiver.QuestIconStory:
                    self.nametagIcon = DistributedQuestGiver.QuestIconStoryTexture.copyTo(self.nametag3d)
                else:
                    self.nametagIcon = DistributedQuestGiver.QuestIconStoryTexture.copyTo(self.nametag3d)
                self.nametagIcon.setScale(3.5)
            else:
                if status == DistributedQuestGiver.QuestIconComplete:
                    self.nametagIcon = DistributedQuestGiver.QuestIconCompleteTexture.copyTo(self.nametag3d)
                    self.nametagIcon.setScale(12)
                else:
                    if status == DistributedQuestGiver.QuestIconProgress:
                        self.nametagIcon = DistributedQuestGiver.QuestIconProgressTexture.copyTo(self.nametag3d)
                        self.nametagIcon.setScale(12)
                    else:
                        self.notify.error('invalid quest status: %s or type: %s' % (status, type))
            self.nametagIcon.setPos(0, 0, 3.5)
            self.nametagIcon.reparentTo(self.getNameText())
            self.nametagIcon.setDepthWrite(0)
            if status == DistributedQuestGiver.QuestIconComplete or status == DistributedQuestGiver.QuestIconNew:
                self.nametagIconGlow = loader.loadModel('models/effects/lanternGlow')
                self.nametagIconGlow.reparentTo(self.nametag.getNameIcon())
                self.nametagIconGlow.setScale(20.0)
                self.nametagIconGlow.setColorScaleOff()
                self.nametagIconGlow.setFogOff()
                self.nametagIconGlow.setLightOff()
                self.nametagIconGlow.setPos(0, -0.05, 3.0)
                self.nametagIconGlow.setDepthWrite(0)
                self.nametagIconGlow.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                self.nametagIconGlow.setColor(0.85, 0.85, 0.85, 0.85)
        else:
            if self.nametagIcon:
                self.nametagIcon.detachNode()
            if self.nametagIconGlow:
                self.nametagIconGlow.detachNode()
        self.loadShopCoin()

    def forceDoneChatPage(self):
        self.__handleDoneChatPage(0)

    def showBlackPearlCrew(self):
        self.blackPearlCrew = BlackPearlCrew.BlackPearlCrew()
        currQuestList = localAvatar.getInventory().getQuestList()
        currQuest = localAvatar.getInventory().getQuestList()[0].getQuestId()
        for item in currQuestList:
            if item.getQuestId()[0] == 'c' and item.getQuestId()[1] == '3':
                currQuest = item.getQuestId()

        if currQuest == 'c3r2r1.15visitJoshamee':
            self.blackPearlCrew.show()
            self.blackPearlCrew.showCarver()
        if currQuest == 'c3r2r2.11visitJoshamee':
            self.blackPearlCrew.show()
            self.blackPearlCrew.showGordon()
        if currQuest == 'c3r2r3.14visitJoshamee':
            self.blackPearlCrew.show()
            self.blackPearlCrew.showHendry()
        if currQuest == 'c3r2r4.12visitJoshamee':
            self.blackPearlCrew.show()
            self.blackPearlCrew.showNill()
        if currQuest == 'c3r2r5.11visitJoshamee':
            self.blackPearlCrew.show()
            self.blackPearlCrew.showLeCerdo()
        if currQuest == 'c3r3r1.53visitJoshamee':
            self.blackPearlCrew.show()
            self.blackPearlCrew.showGunner()
        if currQuest == 'c3r3r2.21visitJoshamee':
            self.blackPearlCrew.show()
            self.blackPearlCrew.showScaryMary()
        if currQuest == 'c3r3r3.14visitJoshamee':
            self.blackPearlCrew.show()
            self.blackPearlCrew.showGiladoga()
        if currQuest == 'c3r3r4.13visitJoshamee':
            self.blackPearlCrew.show()
            self.blackPearlCrew.showJohn()
# okay decompiling .\pirates\quest\DistributedQuestGiver.pyc
