from direct.showbase.PythonUtil import report
from pirates.effects.QuestIndicatorEffect import QuestIndicatorEffect
from pirates.piratesgui.RadarGui import *
from pirates.quest.QuestIndicatorGridNode import QuestIndicatorGridNode


class QuestIndicatorNodeExtDoor(QuestIndicatorGridNode):
    

    def __init__(self, questStep):
        self.nearEffect = None
        QuestIndicatorGridNode.__init__(self, 'ExtDoorIndicator', [
         10, 150], questStep)
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def delete(self):
        QuestIndicatorGridNode.delete(self)
        self.nearEffect = None
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def enterOff(self):
        if self.nearEffect:
            self.nearEffect.reallyCleanUpEffect()
            self.nearEffect = None
        QuestIndicatorGridNode.enterOff(self)
        return

    def enterNear(self):
        QuestIndicatorGridNode.enterNear(self)
        if self.stepObj:
            self.startNearEffect()

    def exitNear(self):
        self.stopNearEffect()
        QuestIndicatorGridNode.exitNear(self)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def stepObjArrived(self, stepObj):
        QuestIndicatorGridNode.stepObjArrived(self, stepObj)
        localAvatar.enableQuestArrow(stepObj)
        if self.getCurrentOrNextState() in ('Near', ):
            self.startNearEffect()

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def stepObjLeft(self):
        QuestIndicatorGridNode.stepObjLeft(self)
        self.stopNearEffect()

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
        self.nearEffect.startLoop(pos=Point3(0, 5, 0))
        if self.stepObj:
            self.nearEffect.reparentTo(self.stepObj)
            self.nearEffect.particleDummy.reparentTo(self.stepObj)
        if self.muted:
            self.hideEffect()

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def stopNearEffect(self):
        if self.nearEffect:
            self.nearEffect.stopLoop()
