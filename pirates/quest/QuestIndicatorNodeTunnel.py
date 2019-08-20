from pirates.piratesgui.RadarGui import *
from pirates.quest.QuestIndicatorNode import QuestIndicatorNode
from pirates.piratesgui.RadarGui import RADAR_OBJ_TYPE_QUEST
from direct.showbase.PythonUtil import report, StackTrace

class QuestIndicatorNodeTunnel(QuestIndicatorNode):
    
    def __init__(self, questStep):
        self.pendingStepObj = None
        QuestIndicatorNode.__init__(self, 'TunnelIndicator', [5], questStep)
        self.arrowNode = None

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

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def placeInWorld(self):

        @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
        def stepObjHere(stepObj):
            self.pendingStepObj = None
            
            def performReparent(tunnelObj = stepObj):
                if tunnelObj == stepObj:
                    areaIndex = tunnelObj.getAreaIndexFromDoId(self.questStep.getOriginDoId())
                    if areaIndex != None:
                        (pos, hpr) = tunnelObj.getConnectorNodePosHpr(areaIndex)
                        t = TransformState.makePosHpr(pos, hpr)
                        ti = t.invertCompose(TransformState.makeIdentity())
                        self.reparentTo(tunnelObj)
                        self.setPos(ti.getPos())
                        self.setHpr(ti.getHpr())
                        self.setPos(self, 30, 0, 5)
                        self.arrowNode = tunnelObj.attachNewNode('arrowNode')
                        self.arrowNode.setPos(ti.getPos())

            if not stepObj.isConnectorLoaded():
                self.acceptOnce('tunnelSetLinks', performReparent)
            else:
                performReparent()

        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        
        self.pendingStepObj = base.cr.relatedObjectMgr.requestObjects([
            self.questStep.getStepDoId()], eachCallback = stepObjHere)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def loadZoneLevel(self, level):
        QuestIndicatorNode.loadZoneLevel(self, level)
        if level == 0:
            self.request('At')
        elif level == 1:
            self.request('Far')

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def unloadZoneLevel(self, level):
        QuestIndicatorNode.unloadZoneLevel(self, level)
        if level == 0:
            self.request('Far')
        elif level == 1:
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

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def exitAt(self):
        if hasattr(localAvatar, 'guiMgr') and localAvatar.guiMgr:
            absPos = self.getPos(render)
            localAvatar.guiMgr.radarGui.addRadarObjectAtLoc(absPos, objType = RADAR_OBJ_TYPE_QUEST, targetObjId = self.questStep.getStepDoId())
        
        localAvatar.enableQuestArrow(self)


