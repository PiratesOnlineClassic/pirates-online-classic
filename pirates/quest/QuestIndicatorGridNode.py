# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestIndicatorGridNode
from direct.showbase.PythonUtil import report
from pirates.piratesgui.RadarGui import RADAR_OBJ_TYPE_QUEST
from pirates.quest.QuestIndicatorNode import QuestIndicatorNode


class QuestIndicatorGridNode(QuestIndicatorNode):
    __module__ = __name__

    def __init__(self, name, zoneRadii, questStep):
        self.pendingStepObj = None
        self.stepObj = None
        QuestIndicatorNode.__init__(self, name, zoneRadii, questStep)
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def delete(self):
        self.ignoreAll()
        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        QuestIndicatorNode.delete(self)
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def placeInWorld(self):
        if self.stepObj:
            self.reparentTo(self.stepObj)
            self.setPos(0, 0, 0)
            self.setHpr(0, 0, 0)
            localAvatar.enableQuestArrow(self)
        else:
            if self.pendingStepObj:
                base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
                self.pendingStepObj = None
            questStepDoId = self.questStep.getStepDoId()
            self.pendingStepObj = base.cr.relatedObjectMgr.requestObjects([questStepDoId], eachCallback=self.stepObjArrived)
            if self.stepObj:
                return
            originObj = base.cr.doId2do.get(self.questStep.getOriginDoId())
            if originObj:
                posH = self.questStep.getPosH()
                pos, h = posH[:3], posH[3]
                self.reparentTo(originObj)
                self.setPos(*pos)
                self.setHpr(h, 0, 0)
                localAvatar.enableQuestArrow(self)
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def loadZoneLevel(self, level):
        QuestIndicatorNode.loadZoneLevel(self, level)
        if level == 0:
            self.request('At')
        if level == 1:
            self.request('Near')
        if level == 2:
            self.request('Far')

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def unloadZoneLevel(self, level):
        QuestIndicatorNode.unloadZoneLevel(self, level)
        if level == 0:
            self.request('Near')
        if level == 1:
            self.request('Far')
        if level == 2:
            self.request('Off')

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def enterFar(self):
        QuestIndicatorNode.enterFar(self)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def exitFar(self):
        QuestIndicatorNode.exitFar(self)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def enterNear(self):
        QuestIndicatorNode.enterNear(self)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def exitNear(self):
        QuestIndicatorNode.exitNear(self)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def enterAt(self):
        QuestIndicatorNode.enterAt(self)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def exitAt(self):
        QuestIndicatorNode.exitAt(self)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def _reparentFarEffectToSelf(self):
        if self.farEffect:
            self.farEffect.wrtReparentTo(self)
            self.farEffect.particleDummy.wrtReparentTo(self)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def _reparentFarEffectToOriginObj(self, stepObj):
        if self.farEffect:
            self.farEffect.wrtReparentTo(stepObj.getParent())
            self.farEffect.particleDummy.wrtReparentTo(stepObj.getParent())

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def stepObjArrived(self, stepObj):
        self.pendingStepObj = None
        self.stepObj = stepObj
        self.accept(stepObj.getDisableEvent(), self.stepObjLeft)
        self.placeInWorld()
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def stepObjLeft(self):
        self.stepObj = None
        self.placeInWorld()
        return
# okay decompiling .\pirates\quest\QuestIndicatorGridNode.pyc
