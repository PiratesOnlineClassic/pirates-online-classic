# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestIndicatorNodeIntDoor
from direct.showbase.PythonUtil import StackTrace, report
from pirates.effects.QuestIndicatorEffect import QuestIndicatorEffect
from pirates.piratesgui.RadarGui import *
from pirates.piratesgui.RadarGui import RADAR_OBJ_TYPE_QUEST
from pirates.quest.QuestIndicatorNode import QuestIndicatorNode


class QuestIndicatorNodeIntDoor(QuestIndicatorNode):
    __module__ = __name__

    def __init__(self, questStep):
        self.pendingStepObj = None
        QuestIndicatorNode.__init__(self, 'IntDoorIndicator', [
         15], questStep)
        self.nearEffect = None
        return

    def delete(self):
        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        QuestIndicatorNode.delete(self)
        self.nearEffect = None
        return

    def placeInWorld(self):

        def stepObjHere(stepObj):
            self.pendingStepObj = None
            self.reparentTo(stepObj)
            self.setPos(0, 0, 0)
            self.setHpr(0, 0, 0)
            return

        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        self.pendingStepObj = base.cr.relatedObjectMgr.requestObjects([self.questStep.getStepDoId()], eachCallback=stepObjHere)
        return

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
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def enterNear(self):
        if self.nearEffect:
            self.nearEffect.reallyCleanUpEffect()
        self.nearEffect = QuestIndicatorEffect.getEffect()
        self.nearEffect.setWantBottomEffect(self.wantBottomEffect)
        self.nearEffect.reparentTo(self)
        self.nearEffect.particleDummy.reparentTo(self)
        self.nearEffect.startLoop(pos=Point3(0, -10, 0))
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
# okay decompiling .\pirates\quest\QuestIndicatorNodeIntDoor.pyc
