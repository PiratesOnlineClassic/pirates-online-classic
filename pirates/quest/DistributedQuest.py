from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from panda3d.core import *
from pirates.cutscene import Cutscene, CutsceneActor, CutsceneData
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import NewTutorialPanel, PiratesGuiGlobals, RadarGui
from pirates.quest import (Quest, QuestBase, QuestConstants, QuestDB, QuestTaskDNA)

QuestPopupDict = {
    'c2_visit_will_turner': ['showBlacksmith', 'closeShowBlacksmith'], 'c2.2defeatSkeletons': ['showSkeleton', 'closeShowSkeleton'],
    'c2_visit_tia_dalma': ['showJungleTia', 'closeShowJungleTia'], 'c2.4recoverOrders': ['showNavy', 'closeShowNavy'],
    'c2.5deliverOrders': ['showGovMansion', 'closeShowGovMansion'], 'c2.9visitDarby': ['showDarby', 'closeShowDarby'],
    'c2.10visitDockworker': ['showDinghy', 'closeShowDinghy'], 'c2.11visitBarbossa': ['showBarbossa', 'closeShowbarbossa'],
    'c3visitJack': ['showTortugaJack', 'closeShowTortugaJack']}

QUEST_TYPE_AVATAR = 0
QUEST_TYPE_TM = 1

class DistributedQuest(DistributedObject.DistributedObject, QuestBase.QuestBase, Quest.Quest):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedQuest')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        Quest.Quest.__init__(self)
        self.type = QUEST_TYPE_AVATAR
        self.sceneObj = None
        self.targetObjIds = []
        self.setAsActive = False
        self.endEvent = ''
        self.popupDialog = None
        self.preloadedCutscenes = []
        self.prevLocalAvState = None
        self.viewedInGUI = True

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.setActive()
        if self.playStinger():
            messenger.send('localAvatarQuestAdded', [self])
        popupDialogText = QuestPopupDict.get(self.getQuestId())
        if popupDialogText:
            if base.localAvatar.showQuest:
                base.localAvatar.resetQuestShow()
                self.popupDialog = NewTutorialPanel.NewTutorialPanel(popupDialogText)
                self.popupDialog.activate()

                def closeTutorialWindow():
                    messenger.send(self.popupDialog.closeMessage)

                self.popupDialog.setYesCommand(closeTutorialWindow)

    def delete(self):
        messenger.send('localAvatarQuestDeleted', [self])
        DistributedObject.DistributedObject.delete(self)
        Quest.Quest.destroy(self)
        self.setInactive()
        self.__cleanupDialog()
        for currPreload in self.preloadedCutscenes:
            base.cr.cleanupPreloadedCutscene(currPreload)

        self.preloadedCutscenes = []

    def __cleanupDialog(self, value=None):
        if self.popupDialog:
            self.popupDialog.destroy()
            del self.popupDialog
            self.popupDialog = None

    def setTaskStates(self, taskStates):
        oldTaskStates = getattr(self, 'taskStates', None)
        lookingForItems = {}
        if self.isGenerated():
            for task, taskState in zip(self.questDNA.tasks, oldTaskStates):
                if task.__class__ in QuestTaskDNA.RecoverItemClasses:
                    lookingForItems[task.item] = (
                     taskState.getAttempts(), taskState.getProgress(), taskState.getGoal())

        Quest.Quest.setTaskStates(self, taskStates)
        if self.isGenerated():
            for task, taskState in zip(self.questDNA.tasks, self.taskStates):
                if task.__class__ in QuestTaskDNA.RecoverItemClasses:
                    oldAttempts, oldProgress, oldGoal = lookingForItems[task.item]
                    newProgress = taskState.getProgress()
                    newAttempts = taskState.getAttempts()
                    newGoal = taskState.getGoal()
                    if oldProgress >= oldGoal:
                        note = QuestConstants.QuestItemNotification.AlreadyFound
                    elif newProgress > oldProgress:
                        if newProgress >= newGoal:
                            note = QuestConstants.QuestItemNotification.ProgressMadeGoalMet
                        else:
                            note = QuestConstants.QuestItemNotification.ProgressMadeGoalUnmet
                    elif newAttempts > oldAttempts:
                        note = QuestConstants.QuestItemNotification.ValidAttempt
                    else:
                        note = QuestConstants.QuestItemNotification.InvalidAttempt
                    messenger.send('localAvatarQuestItemUpdate', [self, task.item, note])

        if self.isGenerated():
            if self.isComplete():
                messenger.send('localAvatarQuestComplete', [self])
                self.__cleanupDialog()
            else:
                messenger.send('localAvatarQuestUpdate', [self])

    def announceNewQuest(self):
        base.localAvatar.guiMgr.showQuestAddedText(self)

    def getProgressMsg(self):
        if self.taskStates:
            questTaskDNA = self.questDNA.getTaskDNAs()[0]
            taskState = self.taskStates[0]
            return questTaskDNA.getProgressMessage(taskState)
        return (None, None)

    def getCompleteText(self):
        if self.type == QUEST_TYPE_AVATAR:
            return 'QUEST COMPLETE!'
        return 'OBJECTIVE COMPLETE!'

    def startFinalizeScene(self, idx, giverId, endEvent=None):
        sceneInfo = self.questDNA.getFinalizeInfo()
        sceneToPlay = sceneInfo[idx]
        self.endEvent = endEvent
        if sceneToPlay.get('type') == 'dialog':
            npc = base.cr.doId2do.get(giverId)
            dialogId = sceneToPlay.get('sceneId')
            npc.playDialogMovie(dialogId, self.doneFinalizeScene, self.prevLocalAvState)
            if self.prevLocalAvState == None:
                self.prevLocalAvState = npc.currentDialogMovie.oldGameState
        else:
            if sceneToPlay.get('type') == 'cutscene':
                name = sceneToPlay.get('sceneId')
                preloadInfo = sceneToPlay.get('preloadInfo', [])
                for currPreload in preloadInfo:
                    base.cr.preloadCutscene(currPreload)
                    self.preloadedCutscenes.append(currPreload)

                plCutscene = base.cr.getPreloadedCutsceneInfo(name)
                if plCutscene == None:
                    self.sceneObj = Cutscene.Cutscene(self.cr, name, self.doneFinalizeScene, giverId)
                    self.sceneObj.play()
                else:
                    self.sceneObj = plCutscene
                    plCutscene.initialize(self.doneFinalizeScene, giverId, True)
                    plCutscene.play()
                if self.prevLocalAvState == None:

                    def cutsceneStarted():
                        localCutActor = self.sceneObj.getActor(CutsceneActor.CutLocalPirate.getActorKey())
                        self.prevLocalAvState = localCutActor.oldParams.gameState

                    self.sceneObj.setStartCallback(cutsceneStarted)
                else:
                    self.sceneObj.overrideOldAvState(self.prevLocalAvState)

    def doneFinalizeScene(self):
        if self.sceneObj:
            self.sceneObj.destroy()
            self.sceneObj = None
        self.sendUpdate('doneFinalizeScene')
        if self.endEvent != '':
            messenger.send(self.endEvent)

    def setActive(self):
        self.sendUpdate('setActive')
        self.setAsActive = True

    def setInactive(self):
        if self.setAsActive == True:
            if not hasattr(base, 'localAvatar'):
                self.notify.warning('Uh oh, tried to delete active questdoId %s when localAvatar was not present' % self.doId)
                return
            for currObj in self.targetObjIds:
                localAvatar.guiMgr.radarGui.convertRadarObject(RadarGui.RADAR_OBJ_TYPE_DEFAULT, currObj)

            self.targetObjIds = []
            self.setAsActive = False

    def updateTargetLoc(self, pos, worldZone, targetObjId):
        gridPos = base.cr.activeWorld.worldGrid.getZoneCellOrigin(worldZone)
        worldPos = Point3(*pos) + Point3(*gridPos)
        objType = RadarGui.RADAR_OBJ_TYPE_QUEST
        self.targetObjIds.append(targetObjId)

    def amFinalized(self):
        messenger.send('localAvatarQuestFinalized', [self.doId])
        Quest.Quest.setFinalized(self)
        checkPoint = self.questDNA.getCheckPoint()
        if checkPoint != -1:
            base.localAvatar.b_setTutorial(checkPoint)
        base.localAvatar.resetStoryQuest()
