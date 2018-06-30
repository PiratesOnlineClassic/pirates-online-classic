from pirates.piratesgui import GuiButton
from direct.gui.DirectGui import *
from otp.otpbase import OTPGlobals
from otp.otpgui import OTPDialog
from panda3d.core import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import (BlackPearlCrew, BorderFrame, InventoryPage,
                                PDialog, PiratesGuiGlobals, QuestItemGui,
                                QuestTitleList)
from pirates.quest.QuestDetailGUI import QuestDetailBase
from pirates.uberdog import DistributedInventoryBase
from pirates.uberdog.UberDogGlobals import *

tpMgr = TextPropertiesManager.getGlobalPtr()
questTitle = TextProperties()
questTitle.setSmallCaps(1)
questTitle.setFont(PiratesGlobals.getPirateFont())
questTitle.setTextColor(*PiratesGuiGlobals.TextFG1)
questTitle.setGlyphScale(1.2)
tpMgr.setProperties('questTitle', questTitle)
questPercent = TextProperties()
questPercent.setTextColor(0.8, 0.8, 0, 0.8)
questPercent.setGlyphScale(0.8)
tpMgr.setProperties('questPercent', questPercent)
questNew = TextProperties()
questNew.setTextColor(0.3, 0.7, 0.25, 1)
questNew.setGlyphScale(0.8)
tpMgr.setProperties('questNew', questNew)
questComplete = TextProperties()
questComplete.setTextColor(0.3, 0.7, 0.25, 1)
questComplete.setGlyphScale(0.8)
tpMgr.setProperties('questComplete', questComplete)


class QuestPage(InventoryPage.InventoryPage):
    notify = directNotify.newCategory('QuestPage')

    def __init__(self):
        InventoryPage.InventoryPage.__init__(self)
        self.initialiseoptions(QuestPage)
        self.detailId = None
        self.titleBorder = BorderFrame.BorderFrame(
            parent=self, frameSize=(-0.02, 0.97, -0.02, 0.65))
        self.titleBorder.setPos(0.06, 0, 0.01)
        self.titleList = QuestTitleList.QuestTitleList()
        self.titleList.reparentTo(self.titleBorder)
        self.titleList.setPos(0.005, 0, 0)
        gui = loader.loadModel('models/gui/compass_main')
        self.trackedQuestLabel = DirectLabel(
            parent=base.a2dTopRight,
            relief=None,
            image=gui.find('**/icon_objective_grey'),
            image_color=Vec4(1, 1, 0, 1),
            image_scale=0.14,
            image_pos=(-0.03, 0, 0.012),
            text='',
            text_fg=PiratesGuiGlobals.TextFG2,
            text_scale=PiratesGuiGlobals.TextScaleLarge,
            text_align=TextNode.ALeft,
            text_shadow=PiratesGuiGlobals.TextShadow,
            text_wordwrap=12,
            pos=(-0.9, 0, -0.05))
        self.trackedQuestLabel.hide()
        self.detailFrame = QuestDetailBase(parent=self, pos=(0.54, 0, 1.06))
        self.dropButton = GuiButton.GuiButton(
            parent=self,
            state=DGG.DISABLED,
            text=PLocalizer.DropQuest,
            textMayChange=0,
            text_scale=PiratesGuiGlobals.TextScaleMed,
            text_pos=(0, -0.01),
            pos=(0.91, 0, 0.72),
            command=self.dropQuest,
            helpText=PLocalizer.DropQuestHelp,
            helpDelay=PiratesGuiGlobals.HelpPopupTime,
            helpPos=(-0.335, 0, 0.125))
        objectiveGrey = gui.find('**/icon_objective_grey')
        self.trackButton = GuiButton.GuiButton(
            parent=self,
            state=DGG.DISABLED,
            text=PLocalizer.TrackQuest,
            textMayChange=0,
            text_pos=(0.035, -0.014),
            pos=(0.66, 0, 0.72),
            command=self.trackQuest,
            helpText=PLocalizer.TrackQuestHelp,
            helpDelay=PiratesGuiGlobals.HelpPopupTime,
            helpPos=(-0.08, 0, 0.125),
            geom=objectiveGrey,
            geom_color=Vec4(1, 1, 0, 1),
            geom_scale=0.2,
            geom_pos=(-0.07, 0, -0.002))
        tPos = (0.33, 0, 0.33)
        if base.config.GetBool('want-blackpearl-gui', 0):
            self.blackPearlCrew = BlackPearlCrew.BlackPearlCrew()
            self.blackPearlCrew.hide()
            self.crewButton = GuiButton.GuiButton(
                parent=self,
                text=PLocalizer.BPCrew,
                textMayChange=0,
                text_pos=(0.035, -0.014),
                pos=(0.33, 0, 0.95),
                command=self.showBlackPearlCrew)
            self.crewButton.hide()

        self.accept('questGuiSelect', self.showQuestDetails)
        self.accept('localAvatarQuestComplete', self.updateQuestDetails)
        self.accept('localAvatarQuestUpdate', self.updateQuestDetails)
        self.accept('localAvatarQuestItemUpdate', self.updateQuestDetails)
        self.accept(
            'inventoryAddDoId-%s-%s' % (localAvatar.getInventoryId(),
                                        InventoryCategory.QUESTS),
            self.updateQuestTitlesNewQuest)
        self.accept(
            'inventoryRemoveDoId-%s-%s' % (localAvatar.getInventoryId(),
                                           InventoryCategory.QUESTS),
            self.updateQuestTitles)
        self.accept('localAvatarActiveQuestId', self.updateTrackedQuestLabel)
        self.invRequest = None
        self.tmButtonQuick = None
        self.tmButtonSearch = None
        self.tmReadyDialog = None

    def destroy(self):
        self.trackedQuestLabel.destroy()
        self.titleList.destroy()
        del self.titleList
        if self.tmReadyDialog:
            self.tmReadyDialog.destroy()

        InventoryPage.InventoryPage.destroy(self)
        self.ignoreAll()

    def show(self):
        InventoryPage.InventoryPage.show(self)
        localAvatar.guiMgr.removeNewQuestIndicator()
        if not self.trackedQuestLabel.isHidden():
            self.updateQuestTitles()

    def dropQuest(self):
        self.dropButton['state'] = DGG.DISABLED
        localAvatar.requestDropQuest(self.detailId)

    def trackQuest(self):
        questId = self.detailId
        if questId == localAvatar.activeQuestId:
            localAvatar.b_requestActiveQuest('')
            self.titleList.showTracked('')
            self.trackedQuestLabel.hide()
            localAvatar.guiMgr.mapPage.worldMap.mapBall.removeDart()
        else:
            localAvatar.b_requestActiveQuest(questId)
            self.titleList.showTracked(questId)
            quest = localAvatar.getQuestById(questId)
            if quest is None:
                print 'Tracked quest not found on avatar!\n  Tracked quest: %s\n  Current quests: %s' % (
                    questId,
                    map(lambda q: q.getQuestId(), localAvatar.getQuests()))

                self.trackedQuestLabel.hide()
            else:
                text = quest.getStatusText()
                self.trackedQuestLabel['text'] = text
                self.trackedQuestLabel.show()
                if localAvatar.questStep:
                    mapPage = localAvatar.guiMgr.mapPage
                    doId = base.cr.uidMgr.uid2doId.get(
                        localAvatar.questStep.getIsland())
                    island = base.cr.doId2do.get(doId)
                    if island:
                        pos = island.getPos()
                        if mapPage.worldMap.mapBall.questDartPlaced:
                            localAvatar.guiMgr.mapPage.worldMap.mapBall.updateDart(
                                'questStep', pos)
                        else:
                            localAvatar.guiMgr.mapPage.addQuestDart(
                                'questStep', pos)

    def updateQuestTitlesNewQuest(self, quest):
        self.updateQuestTitles(quest, newQuest=True)

    def updateQuestTitles(self, quest=None, newQuest=False):
        questIds = map(lambda q: q.getQuestId(), localAvatar.getQuests())
        self.titleList.update(questIds, quest, newQuest)
        self.titleList.showTracked(localAvatar.activeQuestId)
        self.updateTrackedQuestLabel(localAvatar.activeQuestId)
        if self.detailId not in questIds:
            if questIds:
                self.showQuestDetails(questIds[0])
            else:
                self.showQuestDetails(None)
                self.dropButton['state'] = DGG.DISABLED
                self.trackButton['state'] = DGG.DISABLED
        else:
            if self.detailId != localAvatar.activeQuestId:
                self.showQuestDetails(localAvatar.activeQuestId)

        localAvatar.l_setActiveQuest(localAvatar.activeQuestId)

    def showQuestDetails(self, questId):
        if base.config.GetBool('want-blackpearl-gui', False):
            if questId == 'Chapter 3':
                self.crewButton.show()
            else:
                self.crewButton.hide()

        self.detailId = questId
        self.updateQuestIdDetails(questId)

    def updateQuestDetails(self, quest, item=None, note=None):
        questId = quest.getQuestId()
        self.updateQuestIdDetails(questId)
        self.updateQuestTitles(quest)
        if questId == localAvatar.activeQuestId:
            self.updateTrackedQuestLabel(questId)

    def updateTrackedQuestLabel(self, questId):
        quest = localAvatar.getQuestById(questId)
        if quest:
            text = quest.getStatusText()
            self.trackedQuestLabel['text'] = text
            self.trackedQuestLabel.show()
        else:
            self.trackedQuestLabel.hide()

    def updateQuestIdDetails(self, questId):
        self.removeTreasureMapButtons()
        if not questId:
            self.detailId = None
            self.detailFrame['text'] = ''
            return

        if self.detailId != questId:
            return

        qs = PLocalizer.QuestStrings.get(questId)
        if qs:
            title = qs.get('title', '')
            desc = qs.get('description', '')
            rew = qs.get('reward', '')
        else:
            title = ''
            desc = ''
            rew = ''

        quest = localAvatar.getQuestById(questId)
        if not quest:
            self.dropButton['state'] = DGG.DISABLED
            self.trackButton['state'] = DGG.DISABLED
            if len(rew) > 1:
                questText = PLocalizer.QuestItemGuiHeadingFormatWithReward % {
                    'title': title,
                    'desc': desc,
                    'reward': rew
                }
            else:
                questText = PLocalizer.QuestItemGuiHeadingFormat % {
                    'title': title,
                    'desc': desc
                }
        else:
            reward = quest.getRewardText()
            returnTo = quest.getReturnText()
            if len(reward) > 1:
                if quest.isComplete():
                    questText = PLocalizer.QuestItemGuiCompleteFormat % {
                        'title': title,
                        'status': quest.getStatusText(),
                        'desc': desc,
                        'reward': reward,
                        'returnTo': returnTo
                    }
                else:
                    questText = PLocalizer.QuestItemGuiIncompleteFormat % {
                        'title': title,
                        'status': quest.getStatusText(),
                        'desc': desc,
                        'reward': reward
                    }
            else:
                if quest.isComplete():
                    questText = PLocalizer.QuestItemGuiCompleteFormatNoReward % {
                        'title': title,
                        'status': quest.getStatusText(),
                        'desc': desc,
                        'returnTo': returnTo
                    }
                else:
                    questText = PLocalizer.QuestItemGuiIncompleteFormatNoReward % {
                        'title': title,
                        'status': quest.getStatusText(),
                        'desc': desc
                    }

            self.checkButtonDisplay(quest)
            self.trackButton['state'] = DGG.NORMAL
            allowDrop = True
            hasParent = True
            container = localAvatar.questStatus.getContainer(quest.questId)
            if container == None:
                hasParent = False
                allowDrop = False

            if hasParent:
                parent = container.getParent()
                if parent:
                    if parent.isChoice():
                        allowDrop = False
                else:
                    hasParent = False
                    allowDrop = False

            if quest.isDroppable() & allowDrop:
                self.dropButton['state'] = DGG.NORMAL
            else:
                self.dropButton['state'] = DGG.DISABLED

        self.detailFrame['text'] = questText

    def checkButtonDisplay(self, quest):
        questDNA = quest.getQuestDNA()
        questTasks = questDNA.getTasks()
        for currQuestTask in questTasks:
            if not hasattr(currQuestTask, 'getTreasureMapId'):
                continue

            tmId = currQuestTask.getTreasureMapId()
            if tmId != None:

                def inventoryReceived(inventory):
                    if inventory:
                        self.invRequest = None
                        tms = inventory.getTreasureMapsList()
                        for currTm in tms:
                            if currTm.mapId == tmId:
                                currTm.sendUpdate('requestIsEnabled')
                                self.addTreasureMapButtons(currTm, 0.715)
                                break

                self.invRequest = DistributedInventoryBase.DistributedInventoryBase.getInventory(
                    localAvatar.getInventoryId(), inventoryReceived)

    def addTreasureMapButtons(self, tm, buttonOffset):
        self.removeTreasureMapButtons()
        helpPos = (-0.26, 0, 0.095)
        self.tmButtonSearch = GuiButton.GuiButton(
            parent=self,
            text=PLocalizer.PlayTMLookout,
            text_align=TextNode.ACenter,
            text_scale=PiratesGuiGlobals.TextScaleLarge,
            text_pos=(0.0, -0.01),
            text_fg=PiratesGuiGlobals.TextFG1,
            text_shadow=PiratesGuiGlobals.TextShadow,
            text_wordwrap=40,
            image_scale=(0.45, 1, 0.25),
            command=self.startTreasureMap,
            extraArgs=[tm, False],
            pos=(0.54, 0, buttonOffset),
            helpText=PLocalizer.PlayTMLookoutHelp,
            helpPos=helpPos)
        if base.cr.teleportMgr.inInstanceType == PiratesGlobals.INSTANCE_TM:
            self.disableTreasureMapButtons()
        else:
            self.enableTreasureMapButtons()

    def removeTreasureMapButtons(self):
        self.trackButton.show()
        self.dropButton.show()
        if self.tmButtonQuick:
            self.tmButtonQuick.removeNode()
            self.tmButtonQuick = None

        if self.tmButtonSearch:
            self.tmButtonSearch.removeNode()
            self.tmButtonSearch = None

    def enableTreasureMapButtons(self):
        if self.tmButtonQuick:
            self.tmButtonQuick['state'] = 'normal'

        if self.tmButtonSearch:
            self.tmButtonSearch['state'] = 'normal'

        self.trackButton.hide()
        self.dropButton.hide()

    def disableTreasureMapButtons(self):
        if self.tmButtonQuick:
            self.tmButtonQuick['state'] = 'disabled'

        if self.tmButtonSearch:
            self.tmButtonSearch['state'] = 'disabled'

        self.trackButton.hide()
        self.dropButton.hide()

    def startTreasureMap(self, tm, quick=True):
        if localAvatar.getAccess() != OTPGlobals.AccessFull:
            self.tmReadyDialog = PDialog.PDialog(
                text=PLocalizer.PlayTMVelvetRope,
                style=OTPDialog.Acknowledge,
                giveMouse=False,
                command=self.notReadyCallback)

            self.tmReadyDialog.show()
            return

        if tm.getIsEnabled() or base.config.GetBool('black-pearl-ready', 0):
            if localAvatar.testTeleportFlag(
                    PiratesGlobals.TFNoTeleport) == False:
                if base.cr.teleportMgr.inInstanceType == PiratesGlobals.INSTANCE_MAIN:
                    tm.requestTreasureMapGo(quick)
                elif base.cr.teleportMgr.inInstanceType == PiratesGlobals.INSTANCE_TM:
                    tm.requestTreasureMapLeave()
        else:
            self.tmReadyDialog = PDialog.PDialog(
                text=PLocalizer.PlayTMBlackPearlNotReady,
                style=OTPDialog.Acknowledge,
                giveMouse=False,
                command=self.notReadyCallback)

            self.tmReadyDialog.show()

    def notReadyCallback(self, args):
        self.tmReadyDialog.hide()

    def showBlackPearlCrew(self):
        self.blackPearlCrew.showCrewStatus()
        self.blackPearlCrew.show()
