from direct.directnotify import DirectNotifyGlobal
from pirates.quest import QuestConstants, QuestAvatarBase, QuestHolder
from pirates.quest.QuestStepIndicator import QuestStepIndicator
from pirates.quest.QuestPath import QuestStep
from direct.showbase.PythonUtil import report
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PDialog
from otp.otpgui import OTPDialog

class DistributedQuestAvatar(QuestAvatarBase.QuestAvatarBase, QuestHolder.QuestHolder):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedQuestAvatar')
    
    def __init__(self):
        self.lastQuestStepRequest = None
        self.questStep = None
        self.oldQuestStep = None
        self.questIndicator = QuestStepIndicator()
        self.activeQuestId = ''
        self.popupDialog = None
    
    def delete(self):
        self.activeQuestId = ''
        self.questIndicator.delete()
        self.questStep = None
        self.oldQuestStep = None
        self.lastQuestStepRequest = None
    
    def setQuestHistory(self, history):
        self.questHistory = history

    def getQuestHistory(self):
        return self.questHistory

    def setQuestLadderHistory(self, history):
        self.questLadderHistory = history

    def getQuestLadderHistory(self):
        return self.questLadderHistory

    def setCurrentQuestChoiceContainers(self, containers):
        self.currentQuestChoiceContainers = containers

    def getCurrentQuestChoiceContainers(self):
        return self.currentQuestChoiceContainers
    
    def requestDropQuest(self, questId):
        DistributedQuestAvatar.notify.debug('requestDropQuest: %s (%s)' % (questId, self.doId))
        self.sendUpdate('requestDropQuest', [questId])
    
    def requestShareQuest(self, questId):
        DistributedQuestAvatar.notify.debug('requestShareQuest: %s (%s)' % (questId, self.doId))
        self.sendUpdate('requestShareQuest', [questId])

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def refreshActiveQuestStep(self, forceClear = False, forceRefresh = False):
        if self.activeQuestId:
            if forceRefresh or forceClear:
                self.lastQuestStepRequest = None
                self.oldQuestStep = None
                self.questStep = None
            
            if not forceClear:
                self.b_requestQuestStep(self.activeQuestId)
            else:
                self.b_requestQuestStep('')

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def b_requestQuestStep(self, questId):
        if questId:
            stepRequest = (self.getLocation()[0], questId)
            if stepRequest[0]:
                if self.lastQuestStepRequest == stepRequest:
                    if self.questStep:
                        self.l_setQuestStep(self.questStep)
                    elif self.oldQuestStep:
                        self.l_setQuestStep(self.oldQuestStep)
                    else:
                        self.d_requestQuestStep(stepRequest)
                        self.l_requestQuestStep(stepRequest)
                else:
                    self.d_requestQuestStep(stepRequest)
                    self.l_requestQuestStep(stepRequest)
            
        else:
            self.l_requestQuestStep(None)
            self.l_setQuestStep(None)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def d_requestQuestStep(self, stepRequest):
        self.sendUpdate('requestQuestStep', [stepRequest[1]])

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def l_requestQuestStep(self, stepRequest):
        if stepRequest:
            self.lastQuestStepRequest = stepRequest
            self.oldQuestStep = None

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def setQuestStep(self, questStepArgs):
        questStep = QuestStep(*questStepArgs)
        self.l_setQuestStep(questStep)
        if questStep == QuestStep.getNullStep():
            localAvatar.guiMgr.mapPage.worldMap.mapBall.removeDart()
            return
        
        mapPage = localAvatar.guiMgr.mapPage
        doId = base.cr.uidMgr.uid2doId.get(questStep.getIsland())
        island = base.cr.doId2do.get(doId)
        if island:
            pos = island.getPos()
            if mapPage.worldMap.mapBall.questDartPlaced:
                localAvatar.guiMgr.mapPage.worldMap.mapBall.updateDart('questStep', pos)
            else:
                localAvatar.guiMgr.mapPage.addQuestDart('questStep', pos)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def l_setQuestStep(self, questStep):
        if questStep == QuestStep.getNullStep():
            self.oldQuestStep = None
            questStep = None
        elif not questStep and self.questStep:
            self.oldQuestStep = self.questStep
        
        self.questStep = questStep
        self.questIndicator.showQuestStep(self.questStep)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def b_requestActiveQuest(self, questId):
        if not questId == self.activeQuestId:
            self.d_requestActiveQuest(questId)
        
        self.l_requestActiveQuest(questId)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def d_requestActiveQuest(self, questId):
        self.sendUpdate('requestActiveQuest', [questId])

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def l_requestActiveQuest(self, questId):
        self.b_requestQuestStep(questId)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def setActiveQuest(self, questId):
        self.l_setActiveQuest(questId)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def l_setActiveQuest(self, questId):
        if questId != self.activeQuestId:
            self.activeQuestId = questId
            messenger.send('localAvatarActiveQuestId', sentArgs = [self.activeQuestId])
            self.b_requestQuestStep(questId)
            if self.guiMgr and self.guiMgr.mapPage:
                questDartName = localAvatar.guiMgr.mapPage.worldMap.mapBall.questDartName
                if questDartName:
                    localAvatar.guiMgr.mapPage.worldMap.mapBall.updateDartText(questDartName, questId)
    
    def popupProgressBlocker(self, questId):
        if questId == 'c3visitJoshamee':
            localAvatar.guiMgr.showNonPayer(quest = questId, focus = 9)
            return
        elif questId == 'c4.1visitValentina':
            localAvatar.guiMgr.showStayTuned(quest = questId, focus = 0)
            return
        
        popupDialogText = PLocalizer.ProgressBlockPopupDialog.get(questId)
        if popupDialogText:
            self.popupDialog = PDialog.PDialog(text = popupDialogText, style = OTPDialog.Acknowledge, command = self.__cleanupDialog)
        else:
            localAvatar.guiMgr.showNonPayer(quest = questId, focus = 9)
            self.notify.warning('%s: No progressBlock dialog found!' % questId)
    
    def __cleanupDialog(self, value = None):
        if self.popupDialog:
            self.popupDialog.destroy()
            del self.popupDialog
            self.popupDialog = None
        


