# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestIndicatorNodeNPC
from direct.showbase.PythonUtil import report
from pirates.effects.QuestIndicatorEffect import QuestIndicatorEffect
from pirates.quest.QuestIndicatorGridNode import QuestIndicatorGridNode


class QuestIndicatorNodeNPC(QuestIndicatorGridNode):
    __module__ = __name__

    def __init__(self, questStep):
        self.nearEffect = None
        QuestIndicatorGridNode.__init__(self, 'NPCIndicator', [
         30, 150], questStep)
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def delete(self):
        QuestIndicatorGridNode.delete(self)
        self.nearEffect = None
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def enterOff(self):
        if self.nearEffect and not self.nearEffect.isEmpty():
            self.nearEffect.reallyCleanUpEffect()
        self.nearEffect = None
        QuestIndicatorGridNode.enterOff(self)
        return

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
        if self.getCurrentOrNextState() in ('Near', ):
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
# okay decompiling .\pirates\quest\QuestIndicatorNodeNPC.pyc
