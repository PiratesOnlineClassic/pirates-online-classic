from pandac.PandaModules import *
from pirates.world.ZoneLOD import ZoneLOD
from direct.fsm.FSM import FSM
from direct.interval.IntervalGlobal import Parallel
from pirates.effects.QuestIndicatorEffect import QuestIndicatorEffect
from pirates.piratesgui.RadarGui import RADAR_OBJ_TYPE_QUEST
from direct.showbase.PythonUtil import report
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import RadarGui

class QuestIndicatorNode(NodePath, FSM, ZoneLOD):
    
    def __init__(self, name, zoneRadii, questStep):
        zoneRadii += [
            1000000]
        NodePath.__init__(self, name)
        FSM.__init__(self, '%sFSM' % name)
        ZoneLOD.__init__(self, self._QuestIndicatorNode__uniqueName, zoneRadii)
        self.questStep = questStep
        self.pendingOriginObj = None
        self.farEffect = None
        self.muted = False
        self.wantBottomEffect = True
        self.setBillboardAxis()
        
        def originObjHere(originObj):
            self.pendingOriginObj = None
            self.placeInWorld()
            self.setZoneRadii(zoneRadii)

        if self.questStep.getOriginDoId():
            self.pendingOriginObj = base.cr.relatedObjectMgr.requestObjects([
                self.questStep.getOriginDoId()], eachCallback = originObjHere)
        else:
            originObjHere(None)
        self._selfRefreshTask = None
        self._refreshTargetZone = None

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def delete(self):
        self.stopTargetRefresh()
        if self.pendingOriginObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingOriginObj)
            self.pendingOriginObj = None
        
        self.__cleanup()
        ZoneLOD.delete(self)
        self.remove()
        self.questStep = None
        self.farEffect = None
    
    def cleanup(self):
        pass

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def __cleanup(self):
        ZoneLOD.cleanup(self)
        FSM.cleanup(self)
    
    def __uniqueName(self, idString):
        return '%s-QuestNodeIndicator-%s' % (idString, id(self.questStep))

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def placeInWorld(self):
        pass
    
    def loadZoneLevel(self, level):
        pass

    def unloadZoneLevel(self, level, cacheObs = False):
        pass

    def defaultFilter(self, request, args):
        if request != self.state:
            return FSM.defaultFilter(self, request, args)
        return None

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def exitOff(self):
        if hasattr(localAvatar, 'guiMgr') and localAvatar.guiMgr:
            absPos = self.getPos(render)
            localAvatar.guiMgr.radarGui.addRadarObjectAtLoc(absPos, objType = RADAR_OBJ_TYPE_QUEST, targetObjId = self.questStep.getStepDoId(), enableUnconvert = True)
        
        localAvatar.enableQuestArrow(self)

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def enterOff(self):
        localAvatar.disableQuestArrow()
        if self.farEffect:
            self.farEffect.reallyCleanUpEffect()
            self.farEffect = None
        
        if hasattr(localAvatar, 'guiMgr') and localAvatar.guiMgr:
            localAvatar.guiMgr.radarGui.restoreRadarObject(self.questStep.getStepDoId())

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def enterFar(self):
        self.startFarEffect()

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def exitFar(self):
        self.stopFarEffect()
    
    def enterNear(self):
        pass

    def exitNear(self):
        pass

    def enterAt(self):
        pass

    def exitAt(self):
        pass

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def startFarEffect(self):
        if self.farEffect:
            self.farEffect.reallyCleanUpEffect()
        
        self.farEffect = QuestIndicatorEffect.getEffect()
        self.farEffect.setWantBottomEffect(self.wantBottomEffect)
        self.farEffect.reparentTo(self)
        self.farEffect.particleDummy.reparentTo(self)
        self.farEffect.startLoop()
        if self.muted:
            self.hideEffect()

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def stopFarEffect(self):
        if self.farEffect:
            self.farEffect.stopLoop()
    
    def showEffect(self):
        self.muted = False
        if self.farEffect:
            self.farEffect.showEffect()

    def hideEffect(self):
        self.muted = True
        if self.farEffect:
            self.farEffect.hideEffect()
    
    def requestTargetRefresh(self):
        self.stopTargetRefresh()
        
        def tryRefresh(task):
            if localAvatar.ship:
                avLoc = localAvatar.ship.getLocation()
            else:
                avLoc = localAvatar.getLocation()
            if self._refreshTargetZone != avLoc:
                localAvatar.refreshActiveQuestStep(False, True)
                self._refreshTargetZone = avLoc
            
            return task.again

        self._selfRefreshTask = taskMgr.doMethodLater(10, tryRefresh, 'indicatorNodeRefresh-%s' % localAvatar.doId)
    
    def stopTargetRefresh(self):
        if self._selfRefreshTask:
            taskMgr.remove(self._selfRefreshTask)
            self._selfRefreshTask = None
            self._refreshTargetZone = None
        


