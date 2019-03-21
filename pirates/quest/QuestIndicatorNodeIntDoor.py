from pirates.piratesgui.RadarGui import *
from pirates.effects.QuestIndicatorEffect import QuestIndicatorEffect
from pirates.quest.QuestIndicatorNode import QuestIndicatorNode
from pirates.piratesgui.RadarGui import RADAR_OBJ_TYPE_QUEST
from direct.showbase.PythonUtil import report, StackTrace

class QuestIndicatorNodeIntDoor(QuestIndicatorNode):
    
    def __init__(self, questStep):
        self.pendingStepObj = None
        QuestIndicatorNode.__init__(self, 'IntDoorIndicator', [15], questStep)
        self.nearEffect = None
    
    def delete(self):
        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        
        QuestIndicatorNode.delete(self)
        self.nearEffect = None

    def placeInWorld(self):
        
        def stepObjHere(stepObj):
            self.pendingStepObj = None
            self.reparentTo(stepObj)
            self.setPos(0, 0, 0)
            self.setHpr(0, 0, 0)

        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        
        self.pendingStepObj = base.cr.relatedObjectMgr.requestObjects([
            self.questStep.getStepDoId()], eachCallback = stepObjHere)
    
    def loadZoneLevel(self, level):
        QuestIndicatorNode.loadZoneLevel(self, level)
        if level == 0:
            self.request('At')
        
        if level == 1:
            self.request('Near')
    
    def unloadZoneLevel(self, level):
        QuestIndicatorNode.unloadZoneLevel(self, level)
        if level == 0:
            self.request('Near')
        
        if level == 1:
            self.request('Off')

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def enterOff(self):
        QuestIndicatorNode.enterOff(self)
        if self.nearEffect:
            self.nearEffect.reallyCleanUpEffect()
            self.nearEffect = None

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def enterNear(self):
        if self.nearEffect:
            self.nearEffect.reallyCleanUpEffect()
        
        self.nearEffect = QuestIndicatorEffect.getEffect()
        self.nearEffect.setWantBottomEffect(self.wantBottomEffect)
        self.nearEffect.reparentTo(self)
        self.nearEffect.particleDummy.reparentTo(self)
        self.nearEffect.startLoop(pos = Point3(0, -10, 0))
        if self.muted:
            self.hideEffect()

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def exitNear(self):
        if self.nearEffect:
            self.nearEffect.stopLoop()

    def enterAt(self):
        pass

    def exitAt(self):
        pass

    def showEffect(self):
        QuestIndicatorNode.showEffect(self)
        if self.nearEffect:
            self.nearEffect.showEffect()

    def hideEffect(self):
        QuestIndicatorNode.hideEffect(self)
        if self.nearEffect:
            self.nearEffect.hideEffect()
        


