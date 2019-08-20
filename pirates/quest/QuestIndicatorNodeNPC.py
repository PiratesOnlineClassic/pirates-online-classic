from pirates.effects.QuestIndicatorEffect import QuestIndicatorEffect
from pirates.quest.QuestIndicatorGridNode import QuestIndicatorGridNode
from direct.showbase.PythonUtil import report

class QuestIndicatorNodeNPC(QuestIndicatorGridNode):
    
    def __init__(self, questStep):
        self.nearEffect = None
        QuestIndicatorGridNode.__init__(self, 'NPCIndicator', [30, 150], questStep)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def delete(self):
        QuestIndicatorGridNode.delete(self)
        self.nearEffect = None

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def enterOff(self):
        if self.nearEffect and not self.nearEffect.isEmpty():
            self.nearEffect.reallyCleanUpEffect()
        
        self.nearEffect = None
        QuestIndicatorGridNode.enterOff(self)
    
    def enterFar(self):
        QuestIndicatorGridNode.enterFar(self)
        self.requestTargetRefresh()
    
    def exitFar(self):
        QuestIndicatorGridNode.exitFar(self)
        self.stopTargetRefresh()

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def enterNear(self):
        QuestIndicatorGridNode.enterNear(self)
        self.startNearEffect()

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def exitNear(self):
        self.stopNearEffect()
        QuestIndicatorGridNode.exitNear(self)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def enterAt(self):
        QuestIndicatorGridNode.enterAt(self)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def exitAt(self):
        QuestIndicatorGridNode.exitAt(self)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def stepObjArrived(self, stepObj):
        QuestIndicatorGridNode.stepObjArrived(self, stepObj)
        if self.getCurrentOrNextState() in ('Near',):
            self.startNearEffect()
    
    def stepObjLeft(self):
        self.stopNearEffect()
        QuestIndicatorGridNode.stepObjLeft(self)
    
    def showEffect(self):
        QuestIndicatorGridNode.showEffect(self)
        if self.nearEffect and not self.nearEffect.isEmpty():
            self.nearEffect.showEffect()

    def hideEffect(self):
        QuestIndicatorGridNode.hideEffect(self)
        if self.nearEffect and not self.nearEffect.isEmpty():
            self.nearEffect.hideEffect()

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def startNearEffect(self):
        if self.nearEffect and not self.nearEffect.isEmpty():
            self.nearEffect.reallyCleanUpEffect()
        
        self.nearEffect = QuestIndicatorEffect.getEffect()
        self.nearEffect.setWantBottomEffect(self.wantBottomEffect)
        self.nearEffect.startLoop()
        if self.stepObj:
            self.nearEffect.particleDummy.reparentTo(self.stepObj)
            self.nearEffect.reparentTo(self.stepObj)
        
        if self.muted:
            self.hideEffect()

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def stopNearEffect(self):
        if self.nearEffect and not self.nearEffect.isEmpty():
            self.nearEffect.stopLoop()


