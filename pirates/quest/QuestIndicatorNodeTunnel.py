# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestIndicatorNodeTunnel
from direct.showbase.PythonUtil import StackTrace, report
from pirates.piratesgui.RadarGui import *
from pirates.piratesgui.RadarGui import RADAR_OBJ_TYPE_QUEST
from pirates.quest.QuestIndicatorNode import QuestIndicatorNode


class QuestIndicatorNodeTunnel(QuestIndicatorNode):
    

    def __init__(self, questStep):
        self.pendingStepObj = None
        QuestIndicatorNode.__init__(self, 'TunnelIndicator', [
         5], questStep)
        self.arrowNode = None
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def delete(self):
        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        if self.arrowNode:
            self.arrowNode.removeNode()
            self.arrowNode = None
        self.ignore('tunnelSetLinks')
        QuestIndicatorNode.delete(self)
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def placeInWorld(self):

        @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
        def stepObjHere(stepObj):
            self.pendingStepObj = None

            def performReparent(tunnelObj=stepObj):
                if tunnelObj == stepObj:
                    areaIndex = tunnelObj.getAreaIndexFromDoId(self.questStep.getOriginDoId())
                    if areaIndex != None:
                        pos, hpr = tunnelObj.getConnectorNodePosHpr(areaIndex)
                        t = TransformState.makePosHpr(pos, hpr)
                        ti = t.invertCompose(TransformState.makeIdentity())
                        self.reparentTo(tunnelObj)
                        self.setPos(ti.getPos())
                        self.setHpr(ti.getHpr())
                        self.setPos(self, 30, 0, 5)
                        self.arrowNode = tunnelObj.attachNewNode('arrowNode')
                        self.arrowNode.setPos(ti.getPos())
                return

            if not stepObj.isConnectorLoaded():
                self.acceptOnce('tunnelSetLinks', performReparent)
            else:
                performReparent()
            return

        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        self.pendingStepObj = base.cr.relatedObjectMgr.requestObjects([self.questStep.getStepDoId()], eachCallback=stepObjHere)
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def loadZoneLevel(self, level):
        QuestIndicatorNode.loadZoneLevel(self, level)
        if level == 0:
            self.request('At')
        else:
            if level == 1:
                self.request('Far')

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def unloadZoneLevel(self, level):
        QuestIndicatorNode.unloadZoneLevel(self, level)
        if level == 0:
            self.request('Far')
        else:
            if level == 1:
                self.request('Off')

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def enterFar(self):
        QuestIndicatorNode.enterFar(self)
        self.farEffect.setEffectScale(1.5)
        localAvatar.enableQuestArrow(self.arrowNode)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def exitFar(self):
        self.farEffect.setEffectScale(1)
        QuestIndicatorNode.exitFar(self)
        localAvatar.enableQuestArrow(self)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def enterAt(self):
        self.pendingStepObj = None
        localAvatar.enableQuestArrow(self.arrowNode)
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def exitAt(self):
        if hasattr(localAvatar, 'guiMgr') and localAvatar.guiMgr:
            absPos = self.getPos(render)
            localAvatar.guiMgr.radarGui.addRadarObjectAtLoc(absPos, objType=RADAR_OBJ_TYPE_QUEST, targetObjId=self.questStep.getStepDoId())
        localAvatar.enableQuestArrow(self)
# okay decompiling .\pirates\quest\QuestIndicatorNodeTunnel.pyc
