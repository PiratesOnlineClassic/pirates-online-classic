import DistributedGAConnector
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import report
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.world import ClientArea


class DistributedGATunnel(DistributedGAConnector.DistributedGAConnector, ClientArea.ClientArea):

    notify = directNotify.newCategory('DistributedGATunnel')

    def __init__(self, cr):
        DistributedGAConnector.DistributedGAConnector.__init__(self, cr, 'DistributedGATunnel')
        ClientArea.ClientArea.__init__(self)
        self.loadSphere = [
         None, None]
        self.unloadSphere = None
        self.connectorNodes = ['portal_connector_1', 'portal_connector_2']
        self.ambientNames = [None, None]
        self.avatarZoneContext = None
        self.ownContext = None
        self.floorIndex = -1
        self.lastFloor = -1
        self.lastFloorTime = 0
        self.loadedAreaDoId = 0
        self.floorNames = []
        self.quickLoadActive = False
        return

    def generate(self):
        DistributedGAConnector.DistributedGAConnector.generate(self)
        self.__startProcessVisibility()

    def announceGenerate(self):
        DistributedGAConnector.DistributedGAConnector.announceGenerate(self)
        self.cr.distributedDistrict.worldCreator.loadObjectsByUid(self, self.uniqueId, dynamic=0)
        self.loadZoneObjects(-1)
        if len(self.GridLOD) > 0:
            self.geom.reparentTo(self.GridLOD[self.fakeZoneId].highLodNode)
        else:
            self.notify.debug('no grid created')
        self.setClipPlane(base.farCull)

    def delete(self):
        self.__stopProcessVisibility()
        if self.ownContext:
            self.cr.removeInterest(self.ownContext)
            self.ownContext = None
        for sphere in self.loadSphere:
            if sphere:
                sphere.removeNode()

        del self.loadSphere
        self.fadeoutAllAmbient()
        DistributedGAConnector.DistributedGAConnector.delete(self)
        ClientArea.ClientArea.delete(self)
        return

    def loadModel(self):
        DistributedGAConnector.DistributedGAConnector.loadModel(self)

    def __startProcessVisibility(self):
        if not self.avatarZoneContext and self.isGenerated():
            self.avatarZoneContext = self.cr.addInterest(self.getDoId(), 500, self.uniqueName('visibility'))

    def __stopProcessVisibility(self):
        if self.avatarZoneContext:
            self.cr.removeInterest(self.avatarZoneContext)
            self.avatarZoneContext = None
        return

    def setupCollisions(self):
        if self.floorNames == []:
            self.floorNames = [
             'collision_floor_1', 'collision_floor_2', 'collision_floor_middle']
        floors = []
        for i in range(len(self.floorNames)):
            floorName = self.floorNames[i]
            floor = self.find('**/' + floorName)
            uniqueFloorName = self.uniqueName(floorName)
            floor.setName(uniqueFloorName)
            self.floorNames[i] = uniqueFloorName
            self.accept('enterFloor' + uniqueFloorName, self.__handleOnFloor, extraArgs=[i])

    @report(types=['frameCount', 'printInterests'], dConfigParam='want-connector-report')
    def unloadWorldFinished(self, areaDoId):
        DistributedGAConnector.DistributedGAConnector.unloadWorldFinished(self, areaDoId)
        self.loadArea(self.floorIndex, False)

    def fadeOutAmbient(self, index):
        if self.ambientNames[index]:
            base.ambientMgr.requestFadeOut(self.ambientNames[index], duration=0.01)
        if self.ambientNames[1 - index]:
            base.ambientMgr.requestChangeVolume(self.ambientNames[1 - index], duration=0, finalVolume=0)

    def fadeInAmbient(self, index):
        if self.ambientNames[index]:
            base.ambientMgr.requestChangeVolume(self.ambientNames[index], duration=0.1, finalVolume=PiratesGlobals.DEFAULT_AMBIENT_VOLUME_NEAR)

    @report(types=['frameCount', 'printInterests'], dConfigParam='want-connector-report')
    def __handleOnFloor(self, areaIndex, collEntry):
        if not collEntry or areaIndex in (0, 1) and not localAvatar.testTeleportFlag(PiratesGlobals.TFInTunnel):
            if not self.ownContext:
                parent, zone = self.getLocation()
                self.ownContext = self.cr.addInterest(parent, zone, 'tunnelSelfInterest')

            def enterTunnelFinished():
                if localAvatar.getGameState() in ('EnterTunnel', 'Off', 'Dialog', 'Cutscene',
                                                  'LandRoam'):
                    localAvatar.b_setLocation(self.doId, 500)
                    self.floorIndex = 1 - areaIndex
                    self.unloadLoadedArea()
                    localAvatar.b_setGameState('LandRoam')

            localAvatar.motionFSM.off()
            localAvatar.b_setTeleportFlag(PiratesGlobals.TFInTunnel)
            if collEntry != None:
                area = self.getLoadedArea()
                if not area:
                    self.notify.warning('***JCW*** No loaded area in GATunnel: %s' % self.getUniqueId())
                    self.notify.warning('***JCW*** Areas: %s, %s' % (self.areaUid[0], self.areaUid[1]))
                    self.notify.warning('***JCW*** Ignoring __handleOnFloor(%s) event' % areaIndex)
                    return
                entranceNode = self.areaNode[areaIndex]
                entryLocator = area.find('**/' + entranceNode + '*')
                camera.wrtReparentTo(render)
                localAvatar.lookAt(entryLocator, -50, 0, localAvatar.getZ(entryLocator))
                camera.wrtReparentTo(localAvatar)
                self.acceptOnce('EnterTunnelFinished', enterTunnelFinished)
                localAvatar.b_setGameState('EnterTunnel')
            else:
                base.transitions.fadeOut(0.75, Func(enterTunnelFinished))
        return

    @report(types=['frameCount', 'printInterests'], dConfigParam='want-connector-report')
    def loadAreaFinished(self, area, autoFadeIn=True):

        @report(types=['frameCount', 'printInterests'], dConfigParam='want-connector-report')
        def leaveTunnel():
            areaIndex = self.getAreaIndex(area)
            entranceNode = self.areaNode[areaIndex]
            entryLocator = area.find('**/' + entranceNode + '*')
            localAvatar.reparentTo(entryLocator)
            localAvatar.setPos(0, 0, 0)
            if not autoFadeIn:
                if localAvatar.style.tutorial == PiratesGlobals.TUT_KILLED_1_SKELETON:
                    localAvatar.setX(30)
                    localAvatar.setH(90)
            else:
                localAvatar.setH(-90)
            localAvatar.wrtReparentTo(area)
            if autoFadeIn:

                def leaveTunnelFinished():
                    localAvatar.b_clearTeleportFlag(PiratesGlobals.TFInTunnel)
                    localAvatar.b_setGameState('LandRoam')

                self.acceptOnce('LeaveTunnelFinished', leaveTunnelFinished)
                base.localAvatar.b_setGameState('LeaveTunnel')
            else:
                self.sendUpdate('sendLeaveTunnelDone')
            self.fadeInAmbient(self.floorIndex)

        self.cr.setAllInterestsCompleteCallback(leaveTunnel)
        transform = localAvatar.getTransform(self)
        DistributedGAConnector.DistributedGAConnector.loadAreaFinished(self, area, autoFadeIn)
        self.lastFloorTime = globalClock.getFrameTime()
        self.loadedAreaDoId = area.doId
        self.reparentConnectorToArea(area)
        localAvatar.setTransform(self, transform)
        localAvatar.wrtReparentTo(area)
        area.addObjectToGrid(localAvatar)

    @report(types=['frameCount'], dConfigParam='want-connector-report')
    def handleChildArrive(self, childObj, zoneId):
        DistributedGAConnector.DistributedGAConnector.handleChildArrive(self, childObj, zoneId)
        if childObj.isLocal():
            childObj.wrtReparentTo(self)

    @report(types=['frameCount'], dConfigParam='want-connector-report')
    def handleChildLeave(self, childObj, zoneId):
        DistributedGAConnector.DistributedGAConnector.handleChildLeave(self, childObj, zoneId)
        if childObj.isLocal():
            if self.ownContext:
                self.cr.removeInterest(self.ownContext)
                self.ownContext = None
        return

    def fadeoutAllAmbient(self):
        if self.lastFloor >= 0:
            for ambientName in self.ambientNames:
                if ambientName:
                    base.ambientMgr.requestFadeOut(ambientName)

    def setLinks(self, isExterior, exteriorUid, links):
        DistributedGAConnector.DistributedGAConnector.setLinks(self, isExterior, exteriorUid, links)
        self.calcAmbientNames()

    def calcOneAmbientName(self, area):
        retval = None
        if area:
            parts = area.split('_')
            retval = base.ambientMgr.calcAmbientNameFromStr(parts[-1])
        return retval

    def calcAmbientNames(self):
        for i in xrange(2):
            area = self.areaNode[i]
            ambientName = self.calcOneAmbientName(area)
            self.ambientNames[i] = ambientName

        if not self.ambientNames[0] and not self.ambientNames[1]:
            self.ambientNames[1] = base.ambientMgr.calcAmbientNameFromStr(self.modelPath)
            self.notify.debug('Assuming self.ambientNames[1] = %s' % self.ambientNames[1])

    def quickLoadOtherSide(self):
        self.cr.loadingScreen.show(waitForLocation=True)
        if self.floorIndex != -1:
            self.__handleOnFloor(self.floorIndex, None)
        return

    @report(types=['frameCount'], dConfigParam='want-connector-report')
    def turnOn(self):
        DistributedGAConnector.DistributedGAConnector.turnOn(self)
        self.__startProcessVisibility()

    @report(types=['frameCount'], dConfigParam='want-connector-report')
    def turnOff(self):
        self.__stopProcessVisibility()
        DistributedGAConnector.DistributedGAConnector.turnOff(self)
