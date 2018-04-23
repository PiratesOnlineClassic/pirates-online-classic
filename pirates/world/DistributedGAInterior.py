import random

from direct.distributed import DistributedCartesianGrid, DistributedObject
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import report
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import PiratesGuiGlobals, RadarGui
from pirates.world import (ClientArea, DistributedGameArea, DistributedIsland,
                           WorldGlobals)


class DistributedGAInterior(DistributedGameArea.DistributedGameArea, DistributedCartesianGrid.DistributedCartesianGrid, ClientArea.ClientArea):
    notify = directNotify.newCategory('DistributedGAInterior')

    def __init__(self, cr):
        DistributedGameArea.DistributedGameArea.__init__(self, cr)
        DistributedCartesianGrid.DistributedCartesianGrid.__init__(self, cr)
        ClientArea.ClientArea.__init__(self)
        self.intervals = []
        self.GridLOD = {}
        self.fadeInTrack = None
        self.autoFadeIn = True
        self.musicName = None

    def announceGenerate(self):
        self.notify.debug('AnnounceGenerate')
        DistributedGameArea.DistributedGameArea.announceGenerate(self)
        DistributedCartesianGrid.DistributedCartesianGrid.announceGenerate(self)
        if not base.cr.activeWorld.worldGrid:
            base.cr.activeWorld.setWorldGrid(self)
        self.loadModel()
        self.setupLODs()
        self.enableFloors()
        self.cr.distributedDistrict.worldCreator.loadObjectsByUid(self, self.uniqueId, dynamic=0)
        self.loadZoneObjects(-1)
        self.enableFloors()
        self.loadConnectors()
        self.initBlockers(self.staticGridRoot)
        self.startCustomEffects()
        self.resumeSFX()
        self.closeSfx = base.loader.loadSfx('audio/sfx_door_shanty_slam.mp3')
        if base.options.terrain_detail_level == 0:
            self.handleLowTerrainDetail()

    def disable(self):
        self.stopCustomEffects()
        self.pauseSFX()
        self.unloadConnectors()
        if self.fadeInTrack:
            self.fadeInTrack.pause()
        self.fadeInTrack = None
        self.ignoreAll()
        DistributedGameArea.DistributedGameArea.disable(self)
        DistributedCartesianGrid.DistributedCartesianGrid.disable(self)
        del self.closeSfx

    def delete(self):
        self.notify.debug('delete')
        del self.coll
        self.geom.removeNode()
        for node in self.GridLOD.values():
            node.cleanup()

        del self.GridLOD
        if self.modelPath != 'models/buildings/navy_jail_interior':
            self.stopProcessVisibility()
            self.handleExitGameArea(None)
        self.fadeOutAmbientSound()
        self.disableFloors()
        for anim in self.intervals:
            if anim:
                anim.pause()
                del anim

        self.intervals = []
        DistributedGameArea.DistributedGameArea.delete(self)
        DistributedCartesianGrid.DistributedCartesianGrid.delete(self)
        ClientArea.ClientArea.delete(self)
        return

    def isGridParent(self):
        return 1

    @report(types=['frameCount'], dConfigParam='want-connector-report')
    def addObjectToGrid(self, av):
        DistributedCartesianGrid.DistributedCartesianGrid.addObjectToGrid(self, av)
        if av.isLocal():
            self.updateAvReturnLocation(av)

    @report(types=['frameCount', 'args'], dConfigParam=['want-jail-report', 'want-teleport-report'])
    def setLinks(self, links):
        DistributedGameArea.DistributedGameArea.setLinks(self, links)
        self.loadConnectors()

    @report(types=['frameCount', 'args'], dConfigParam=['want-jail-report', 'want-teleport-report'])
    def setConnectorId(self, connectorId):
        self.notify.debug('setConnectorId %s' % connectorId)
        self.connectorId = connectorId

    def enableFloors(self):
        self.notify.debug('enableFloors')
        floorName = 'floor_interior'
        self.uniqueFloorName = self.uniqueName(floorName)
        collNodes = self.findAllMatches('**/+CollisionNode')
        for collNode in collNodes:
            curMask = collNode.node().getIntoCollideMask()
            if curMask.hasBitsInCommon(PiratesGlobals.FloorBitmask):
                collNode.setName(self.uniqueFloorName)
                self.setupCannonballLandColl(collNode, PiratesGlobals.TargetBitmask | curMask, 0)

        self.accept('enterFloor' + self.uniqueFloorName, self.handleEnterGameArea)
        self.accept('exitFloor' + self.uniqueFloorName, self.handleExitGameArea)

    def disableFloors(self):
        self.notify.debug('disableFloors')
        if self.uniqueFloorName:
            self.ignore('enterFloor' + self.uniqueFloorName)
            self.ignore('exitFloor' + self.uniqueFloorName)

    @report(types=['frameCount'], dConfigParam='want-jail-report')
    def handleEnterGameArea(self, collEntry):
        localAvatar.interior = self
        self.addObjectToGrid(localAvatar)
        localAvatar.guiMgr.radarGui.loadMap(self.geom)
        for x in range(self.locatorNodes.getNumPaths()):
            localAvatar.guiMgr.radarGui.addRadarObjectAtLoc(self.locatorNodes[x].getPos(render), objType=RadarGui.RADAR_OBJ_TYPE_EXIT, targetObjId='exit-' + str(x))

        self.ambientName = base.ambientMgr.calcAmbientNameFromStr(self.modelPath)
        if not (self.ambientName == 'jungle' or self.ambientName == 'cave' or self.ambientName == 'swamp'):
            base.ambientMgr.requestFadeIn(self.ambientName, finalVolume=PiratesGlobals.DEFAULT_AMBIENT_VOLUME)
        if self.musicName:
            base.musicMgr.requestFadeOut(self.musicName)
            self.musicName = None
        if 'tavern' in self.modelPath:
            self.musicName = random.choice(('tavern_a', 'tavern_b', 'tavern_c'))
            base.musicMgr.request(self.musicName)
        DistributedGameArea.DistributedGameArea.handleEnterGameArea(self, collEntry)
        return

    def setLocation(self, parentId, zoneId, teleport=0):
        DistributedObject.DistributedObject.setLocation(self, parentId, zoneId)
        self.reparentTo(render)

    @report(types=['frameCount'], dConfigParam='want-jail-report')
    def handleExitGameArea(self, collEntry):
        self.notify.debug('%s handleExitGameArea' % self.doId)
        if collEntry:
            self.notify.debug('%s handleExitGameArea - doing nothing' % self.doId)
            return
        self.notify.debug('%s handleExitGameArea - doing something' % self.doId)
        self.removeObjectFromGrid(localAvatar)
        localAvatar.interior = None
        localAvatar.guiMgr.radarGui.unloadMap()
        for x in range(self.locatorNodes.getNumPaths()):
            localAvatar.guiMgr.radarGui.removeRadarObject('exit-' + str(x))

        self.fadeOutAmbientSound()
        DistributedGameArea.DistributedGameArea.handleExitGameArea(self, collEntry)

    def fadeOutAmbientSound(self):
        if hasattr(self, 'ambientName') and not (self.ambientName == 'jungle' or self.ambientName == 'cave' or self.ambientName == 'swamp'):
            base.ambientMgr.requestFadeOut(self.ambientName)
        if self.musicName:
            base.musicMgr.requestFadeOut(self.musicName)
            self.musicName = None

    def loadModelParts(self):
        modelBaseName = self.modelPath.split('_zero')[0]
        terrainModel = loader.loadModelCopy(modelBaseName + '_terrain')
        if terrainModel:
            self.geom = terrainModel
        else:
            self.geom = loader.loadModelCopy(self.modelPath)
            return
        terrainDetailModel = loader.loadModelCopy(modelBaseName + '_terrain_detail')
        if terrainDetailModel:
            terrainDetailModel.getChild(0).reparentTo(self.geom)
        pierModel = loader.loadModelCopy(modelBaseName + 'pier')
        if pierModel:
            pierModel.getChild(0).reparentTo(self.geom)
        fortModel = loader.loadModelCopy(modelBaseName + '_fort')
        if fortModel:
            fortModel.getChild(0).reparentTo(self.geom)
        logModel = loader.loadModelCopy(modelBaseName + '_logs')
        if logModel:
            logModel.getChild(0).reparentTo(self.geom)
        vegeWallModel = loader.loadModelCopy(modelBaseName + '_nat_wall')
        if vegeWallModel:
            vegeWallModel.getChild(0).reparentTo(self.geom)
        vegModel = loader.loadModelCopy(modelBaseName + '_veg')
        if vegModel:
            vegModel.getChild(0).reparentTo(self.geom)
        rockModel = loader.loadModelCopy(modelBaseName + '_rocks')
        if rockModel:
            rockModel.getChild(0).reparentTo(self.geom)

    def loadModel(self):
        if 'interior' not in self.modelPath:
            self.loadModelParts()
        else:
            self.geom = loader.loadModel(self.modelPath)
        self.geom.flattenStrong()
        self.geom.reparentTo(self)
        coll = self.geom.findAllMatches('**/+CollisionNode')
        self.coll = coll
        locatorNodes = self.geom.findAllMatches('**/portal_interior_*')
        locatorNodes.wrtReparentTo(self)
        self.locatorNodes = locatorNodes
        self.portalNodes = self.geom.findAllMatches('**/portal_[0-9]')
        self.initBlockers(self.geom)

    def setName(self, name):
        self.name = name

    def getTeam(self):
        return PiratesGlobals.ISLAND_TEAM

    @report(types=['frameCount'], dConfigParam='want-jail-report')
    def updateAvReturnLocation(self, av):
        av.d_requestReturnLocation(self.doId)

    def enterInteriorFromDoor(self, doorIndex):
        doorIndexStr = ''
        if doorIndex > 0:
            doorIndexStr = '_' + str(doorIndex + 1)
        self.doorLeftStr = '**/door_left' + doorIndexStr
        self.doorRightStr = '**/door_right' + doorIndexStr
        self.doorLocatorStr = '**/door_locator' + doorIndexStr
        doorLeft = self.find(self.doorLeftStr)
        doorRight = self.find(self.doorRightStr)
        self.openDoorIval = Parallel()
        self.closeDoorIval = Parallel()
        self.tOpen = 0.5
        if not doorLeft.isEmpty():
            self.openDoorIval.append(LerpHprInterval(doorLeft, self.tOpen, Vec3(-90, 0, 0)))
            self.closeDoorIval.append(LerpHprInterval(doorLeft, self.tOpen, Vec3(0, 0, 0)))
        if not doorRight.isEmpty():
            self.openDoorIval.append(LerpHprInterval(doorRight, self.tOpen, Vec3(90, 0, 0)))
            self.closeDoorIval.append(LerpHprInterval(doorRight, self.tOpen, Vec3(0, 0, 0)))
        doorLocator = self.find(self.doorLocatorStr)
        if doorLocator.isEmpty():
            doorLocator = self.find(self.doorLeftStr)
            if doorLocator.isEmpty():
                doorLocator = self.find(self.doorRightStr)
        localAvatar.reparentTo(doorLocator)
        localAvatar.setPos(0, 10, 0)
        localAvatar.setHpr(0, 0, 0)
        localAvatar.wrtReparentTo(self)
        localAvatar.setP(0)
        localAvatar.setR(0)
        localAvatar.setScale(1)
        self.handleEnterGameArea(None)
        messenger.send('doorToInteriorFadeIn')
        if self.autoFadeIn:
            fadeInFunc = Func(base.transitions.fadeIn, self.tOpen)
            playerStateFunc = Func(localAvatar.gameFSM.request, 'LandRoam')
        else:

            def Nothing():
                pass

            fadeInFunc = Func(Nothing)
            playerStateFunc = Func(Nothing)
        if self.autoFadeIn:
            sf = Sequence(Func(localAvatar.gameFSM.request, 'DoorInteract'), fadeInFunc, self.openDoorIval, self.closeDoorIval, Func(self.closeSfx.play), playerStateFunc)
        else:
            sf = Sequence(Func(localAvatar.gameFSM.request, 'DoorInteract'), fadeInFunc, self.openDoorIval, self.closeDoorIval, playerStateFunc)
        self.fadeInTrack = sf
        self.fadeInTrack.start()

    @report(types=['frameCount'], dConfigParam='want-connector-report')
    def handleChildArrive(self, childObj, zoneId):
        DistributedGameArea.DistributedGameArea.handleChildArrive(self, childObj, zoneId)
        if childObj.isLocal():
            self.updateAvReturnLocation(childObj)

    @report(types=['frameCount', 'args'], dConfigParam=['want-jail-report', 'want-teleport-report'])
    def loadConnectors(self):
        if 'interior' in self.modelPath or 'kingshead_zero' in self.modelPath:
            return
        DistributedGameArea.DistributedGameArea.loadConnectors(self)

    @report(types=['frameCount', 'args'], dConfigParam=['want-jail-report', 'want-teleport-report'])
    def unloadConnectors(self):
        if 'interior' in self.modelPath or 'kingshead_zero' in self.modelPath:
            return
        DistributedGameArea.DistributedGameArea.unloadConnectors(self)

    def setAutoFadeInOnEnter(self, autoFadeIn):
        self.autoFadeIn = autoFadeIn

    def getTeleportDestPosH(self, index=0):
        if 'interior' in self.modelPath or 'kingshead_zero' in self.modelPath:
            pt = self._getDoorSpawnPos(index)
        else:
            pt = self._getTunnelSpawnPos(index)
        return (pt[0], pt[1], pt[2], 0)

    def _getDoorSpawnPos(self, index=0):
        doorIndexStr = ''
        if index > 0:
            index = '_' + str(index + 1)
        doorLocatorStr = '**/door_locator' + doorIndexStr
        doorLocator = self.find(doorLocatorStr)
        if doorLocator.isEmpty():
            doorLocator = self.find(self.doorLeftStr)
            if doorLocator.isEmpty():
                doorLocator = self.find(self.doorRightStr)
        return self.getRelativePoint(doorLocator, Point3(0, 10, 0))

    def turnOn(self, av=None):
        self.unstash()
        DistributedGameArea.DistributedGameArea.turnOn(self, av=None)
        DistributedCartesianGrid.DistributedCartesianGrid.turnOn(self, av=None)
        self.startProcessVisibility(base.localAvatar)

    def turnOff(self):
        DistributedGameArea.DistributedGameArea.turnOn(self)
        DistributedCartesianGrid.DistributedCartesianGrid.turnOn(self)
        self.stash()
        self.stopProcessVisibility()

    def getLevel(self):
        return 1

    def handleLowTerrainDetail(self):
        grids = self.findAllMatches('**/Grid-*')
        for dl in self.dynamicLights:
            if dl.type != 0:
                for gi in range(0, grids.getNumPaths()):
                    geomParent = grids[gi].getChild(0).getChild(0)
                    geomParent.setLightOff(dl.lightNodePath)
                    for ci in range(0, geomParent.getNumChildren()):
                        geoms = geomParent.getChild(ci)
                        geoms.setLightOff(dl.lightNodePath)
