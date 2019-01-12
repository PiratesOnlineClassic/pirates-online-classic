from pirates.effects.QuestIndicatorEffect import QuestIndicatorEffect
from pirates.quest.QuestIndicatorGridNode import QuestIndicatorGridNode

class QuestIndicatorNodeShip(QuestIndicatorGridNode):
    
    def __init__(self, questStep):
        self.nearEffect = None
        QuestIndicatorGridNode.__init__(self, 'ShipIndicator', [
            300,
            1500], questStep)
        self._selfRefreshTask = None
        self._refreshTargetZone = None

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def delete(self):
        QuestIndicatorGridNode.delete(self)
        self.nearEffect = None
        self.stopTargetRefresh()

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def enterOff(self):
        if self.nearEffect:
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
        if self.nearEffect:
            self.nearEffect.showEffect()

    def hideEffect(self):
        QuestIndicatorGridNode.hideEffect(self)
        if self.nearEffect:
            self.nearEffect.hideEffect()

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def startNearEffect(self):
        if self.nearEffect:
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
        if self.nearEffect:
            self.nearEffect.stopLoop()

