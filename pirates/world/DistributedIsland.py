import imp
import random
import re

from direct.actor import *
from direct.distributed import DistributedCartesianGrid
from direct.gui import DirectGuiGlobals
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import report
from direct.task import Task
from otp.otpbase import OTPGlobals, OTPRender
from pandac.PandaModules import *
from pirates.battle.Teamable import Teamable
from pirates.distributed import DistributedInteractive
from pirates.effects import Grass
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.LanternGlow import LanternGlow
from pirates.effects.VolcanoEffect import VolcanoEffect
from pirates.piratesbase import PiratesGlobals, PLocalizer, TODGlobals
from pirates.piratesgui import PiratesGuiGlobals, RadarGui
from pirates.pvp import PVPGlobals
from pirates.quest.QuestConstants import LocationIds
from pirates.seapatch.Reflection import Reflection
from pirates.seapatch.Water import IslandWaterParameters
from pirates.swamp.Swamp import Swamp
from pirates.world import (ClientArea, DistributedGameArea, WorldGlobals,
                           ZoneLOD)
from otp.nametag.NametagGroup import NametagGroup
from otp.nametag.Nametag import Nametag


class DistributedIsland(DistributedGameArea.DistributedGameArea, DistributedCartesianGrid.DistributedCartesianGrid, ZoneLOD.ZoneLOD, ClientArea.ClientArea, Teamable):
    __module__ = __name__
    MusicNames = {'Port Royal': 'island-port-royal', 'Tortuga': 'island-tortuga', 'Cuba': 'island-cuba', 'Padre Del Fuego': 'island-padre-del-fuego', "Devil's Anvil": 'island-devils-anvil', 'Driftwood Island': 'island-driftwood', 'Kingshead': 'island-kingshead', 'Outcast Isle': 'island-outcast', 'Isla Perdida': 'island-perdida', "Rumrunner's Isle": 'island-rumrunner', 'Isla Tormenta': 'island-tormenta', 'Isla Cangrejos': 'island-cangrejos', 'Cutthroat Isle': 'island-cutthroat'}
    MusicDefault = 'island-general'
    SiegeIcon = None
    notify = directNotify.newCategory('DistributedIsland')

    def __init__(self, cr):
        DistributedGameArea.DistributedGameArea.__init__(self, cr)
        DistributedCartesianGrid.DistributedCartesianGrid.__init__(self, cr)
        ClientArea.ClientArea.__init__(self)
        Teamable.__init__(self)
        self.gridNodes = {}
        self.islandObjectsLoaded = False
        self.animControls = None
        self.sphereRadii = [
         1000, 2000, 3000, 100000]
        self.sphereCenter = [0, 0]
        ZoneLOD.ZoneLOD.__init__(self, self.uniqueName)
        self.parentWorld = None
        self.gridSphere = None
        self.GridLOD = {}
        self.nameText = None
        islandLOD = FadeLODNode('islandLOD')
        islandLOD.addSwitch(10000, 0)
        islandLOD.addSwitch(20000, 10000)
        islandLOD.setFadeTime(0.5)
        lodnp = NodePath(islandLOD)
        lodnp.reparentTo(self.allDetails)
        lodnp.showThrough(OTPRender.ReflectionCameraBitmask)
        self.geomLOD = lodnp
        self.highDetail = lodnp.attachNewNode('highDetail')
        self.lowDetail = lodnp.attachNewNode('lowDetail')
        self.geom = None
        self.playerBarrierNP = None
        self.islandLowLod = None
        self.gold = 0
        self.islandTunnel = []
        self.hasTunnelsOnRadar = False
        self.name = 'Island Name'
        self.nametag = None
        self.nametag3d = None
        self.grass = None
        self.blackSmokeEffect = None
        self.volcanoEffect = None
        self.lavaFlowEffect = None
        self.steamFlowEffect = None
        self.islandMapModelPath = None
        self.mapName = None
        self.objsCached = False
        self.oceanVisEnabled = base.config.GetBool('ocean-visibility', False)
        self.flatShipsOnIsland = base.config.GetBool('flat-ships-on-island', True)
        self.visTable = {}
        self.locationSphereName = ''
        self.SiegeIcons = []
        if not DistributedIsland.SiegeIcon and launcher.getPhaseComplete(3):
            logos = loader.loadModel('models/textureCards/sailLogo')
            if logos:
                DistributedIsland.SiegeIcon = [logos.find('**/logo_french_flag'), logos.find('**/logo_spanish_flag')]
        return

    def announceGenerate(self):
        DistributedGameArea.DistributedGameArea.announceGenerate(self)
        DistributedCartesianGrid.DistributedCartesianGrid.announceGenerate(self)
        gridSphereName = self.uniqueName('GridSphere')
        self.gridSphereEnterEvent = 'enter' + gridSphereName
        self.gridSphereExitEvent = 'exit' + gridSphereName
        self.setLodCollideMask(self.getLodCollideMask() | PiratesGlobals.ShipCollideBitmask)
        self.setZoneRadii(self.sphereRadii, self.sphereCenter)
        self.cr.distributedDistrict.worldCreator.loadObjectsByUid(self, self.uniqueId, dynamic=0)
        self.setupLODs()
        self.parentWorld.islands[self.doId] = self
        self.initializeNametag3d()
        self.setName(self.name)
        self.addActive()
        self.understandable = 1
        self.setPlayerType(NametagGroup.CCNormal)
        self.placeOnMap()

    def disable(self):
        self.removeFromMap()
        self.turnOff()
        ZoneLOD.ZoneLOD.cleanup(self)
        DistributedGameArea.DistributedGameArea.disable(self)
        DistributedCartesianGrid.DistributedCartesianGrid.disable(self)
        self.deleteZoneCollisions()
        self.parentWorld.islands.pop(self.doId, None)
        self.parentWorld = None
        self.removeActive()
        self.deleteNametag3d()
        if self.grass:
            self.grass.destroy()
        if self.blackSmokeEffect:
            self.blackSmokeEffect.destroy()
        if self.volcanoEffect:
            self.stopVolcanoSmokeEffect()
            self.stopVolcanoRestEffects()
            self.volcanoEffect.destroy()
        return

    def delete(self):
        self.clearAnims()
        DistributedGameArea.DistributedGameArea.delete(self)
        DistributedCartesianGrid.DistributedCartesianGrid.delete(self)
        ZoneLOD.ZoneLOD.delete(self)
        ClientArea.ClientArea.delete(self)
        self.unloadIslandShoreWave()
        self.unloadPlayerBarrier()
        for node in list(self.GridLOD.values()):
            node.cleanup()

        del self.GridLOD
        self.removeNode()
        while len(self.SiegeIcons):
            icon = self.SiegeIcons.pop()
            icon.removeNode()
            icon = None

        return

    def turnOff(self, cache=False):
        self.stopCustomEffects()
        if not cache:
            self.setZoneLevelOuter()
        else:
            if self.lastZoneLevel == 0:
                self.removeIslandGridSphere()
                if self.hasTunnelsOnRadar:
                    self.handleTunnelsOnRadar(False)
        DistributedGameArea.DistributedGameArea.turnOff(self)
        DistributedCartesianGrid.DistributedCartesianGrid.turnOff(self)
        ZoneLOD.ZoneLOD.turnOff(self)

    @report(types=['frameCount', 'args'], dConfigParam=['want-connector-report', 'want-death-debug'])
    def turnOn(self, av=None):
        self.startCustomEffects()
        if self.lastZoneLevel == 0:
            if not self.gridSphere:
                self.setupIslandGridSphere()
            if not self.hasTunnelsOnRadar:
                self.handleTunnelsOnRadar(True)
        if base.shipsVisibleFromIsland:
            self.parentWorld.worldGrid.startProcessVisibility(localAvatar)
        if av:
            self.addObjectToGrid(av)
            self.setZoneLevel(0)
            self.loadConnectors()
        DistributedGameArea.DistributedGameArea.turnOn(self)
        DistributedCartesianGrid.DistributedCartesianGrid.turnOn(self, av)
        ZoneLOD.ZoneLOD.turnOn(self)

    def isGridParent(self):
        return 1

    @report(types=['frameCount', 'args'], dConfigParam=['want-connector-report', 'want-death-debug'])
    def addObjectToGrid(self, av):
        DistributedCartesianGrid.DistributedCartesianGrid.addObjectToGrid(self, av)
        if av.isLocal():
            self.updateAvReturnLocation(av)
            self.startProcessVisibility(av)

    def setLocation(self, parentId, zoneId):
        DistributedGameArea.DistributedGameArea.setLocation(self, parentId, zoneId)
        world = self.cr.doId2do.get(parentId)
        if parentId not in (0, self.cr.getGameDoId()):
            pass
        if world:
            self.reparentTo(world)
            self.parentWorld = world

    def setZoneSphereSize(self, rad0, rad1, rad2):
        self.sphereRadii = [
         rad0, rad1, rad2, 100000]

    def getZoneSphereSize(self):
        return self.sphereRadii

    def setZoneSphereCenter(self, x, y):
        self.sphereCenter = [
         x, y]

    def getZoneSphereCenter(self):
        return self.sphereCenter

    def getMusicName(self):
        islandName = self.getName()
        musicName = self.MusicNames.get(islandName, self.MusicDefault)
        return musicName

    @report(types=['frameCount', 'args'], dConfigParam=['want-connector-report', 'want-jail-report', 'want-island-report'])
    def loadZoneLevel(self, level):
        if level == 0:
            self.islandObjectsLoaded = True
            self.retrieveCacheData()
            self.playAnims()
            self.loadConnectors()
            self.listenForLocationSphere()
            self.setupIslandGridSphere()
            base.musicMgr.request(self.getMusicName(), priority=-1, volume=0.6)
            self.hideName()
            base.localAvatar.guiMgr.radarGui.loadMap(self.geom)
            if not self.hasTunnelsOnRadar:
                self.handleTunnelsOnRadar(True)
            self.setIslandWaterParameters(True)
            if base.config.GetBool('island-prepare-scene', 1) and base.win.getGsg():
                render.prepareScene(base.win.getGsg())
            self.initBlockers(self.staticGridRoot)
            self.startCustomEffects()
            self.handleEnterGameArea()
            return
        elif level == 1:
            localAvatar.setInterest(self.doId, PiratesGlobals.IslandShipDeployerZone, ['ShipDeployer'])
            self.startVolcanoRestEffects()
            self.adjustSmokeParentAndPos(self.geom, Vec3(-40.0, 75.0, 600.0))
            self.showName()
            self.setIslandWaterParameters(True)
            if not self.undockable:
                localAvatar.setPort(self.doId)
            return
        elif level == 2:
            self.unloadIslandLowLod()
            self.retrieveIslandTerrain()
            self.setupIslandGeom()
            self.setIslandWaterParameters(True)
            self.addToOceanSeapatch()
            return
        elif level == 3:
            self.allEnabled = False
            self.loadIslandLowLod()
            self.startVolcanoSmokeEffect()
            self.adjustSmokeParentAndPos(self.islandLowLod, Vec3(-40.0, 75.0, 600.0))
            self.showName()
            return
        elif level == 4:
            pass

    @report(types=['frameCount', 'args'], dConfigParam=['want-connector-report', 'want-jail-report', 'want-island-report'])
    def unloadZoneLevel(self, level):
        if level == 0:
            self.islandObjectsLoaded = False
            self.handleExitGameArea()
            self.unloadConnectors()
            self.cleanupIslandData()
            self.stopListenForLocationSphere()
            self.removeIslandGridSphere()
            self.stopCustomEffects()
            base.localAvatar.guiMgr.radarGui.unloadMap()
            if self.hasTunnelsOnRadar:
                self.handleTunnelsOnRadar(False)
            base.musicMgr.requestFadeOut(self.getMusicName())
            return
        else:
            if level == 1:
                localAvatar.clearInterestNamed(None, ['ShipDeployer'])
                self.stopVolcanoRestEffects()
                localAvatar.clearPort(self.doId)
                return
            else:
                if level == 2:
                    self.showName()
                    self.removeFromOceanSeapatch()
                    self.setIslandWaterParameters(False)
                    self.cleanupTerrain()
                    self.loadIslandLowLod()
                    self.startVolcanoSmokeEffect()
                    self.adjustSmokeParentAndPos(self.islandLowLod, Vec3(-40.0, 75.0, 600.0))
                    return
                else:
                    if level == 3:
                        self.stopVolcanoSmokeEffect()
                        self.unloadIslandLowLod()
                        self.hideName()
                        return
                    else:
                        if level == 4:
                            pass
        return

    def handleChildArrive(self, child, zoneId):
        DistributedGameArea.DistributedGameArea.handleChildArrive(self, child, zoneId)
        if child.isLocal():
            self.accept('ship_vis_change', self.shipVisibilityChanged)
            if base.cr.config.GetBool('remove-island-barriers', False):
                self.setupPlayerBarrier()
            if not base.shipsVisibleFromIsland:
                self.parentWorld.worldGrid.stopProcessVisibility()
            else:
                self.parentWorld.worldGrid.startProcessVisibility(localAvatar)
            base.hideShipNametags = True
            messenger.send('hide-ship-nametags')
            if base.shipsVisibleFromIsland == 1:
                base.showShipFlats = True
                messenger.send('far-ships')
            else:
                base.showShipFlats = False
                messenger.send('normal-ships')
            self.setZoneLevel(0)

    def handleChildLeave(self, child, zoneId):
        if child.isLocal():
            self.ignore('ship_vis_change')
            self.unloadPlayerBarrier()
            messenger.send('normal-ships')
            base.showShipFlats = False
            base.hideShipNametags = False
            messenger.send('show-ship-nametags')
        DistributedGameArea.DistributedGameArea.handleChildLeave(self, child, zoneId)

    def handleEnterGameArea(self, collEntry=None):
        if self.uniqueId == LocationIds.KINGSHEAD_ISLAND:
            self.accept(PiratesGlobals.EVENT_SPHERE_SNEAK + PiratesGlobals.SPHERE_ENTER_SUFFIX, self._handleSneakIntoKingshead)
        DistributedGameArea.DistributedGameArea.handleEnterGameArea(self, collEntry)

    def handleExitGameArea(self, collEntry=None):
        if self.uniqueId == LocationIds.KINGSHEAD_ISLAND:
            self.ignore(PiratesGlobals.EVENT_SPHERE_SNEAK + PiratesGlobals.SPHERE_ENTER_SUFFIX)
        DistributedGameArea.DistributedGameArea.handleExitGameArea(self, collEntry)

    def setupIslandGridSphere(self):
        gridSphereRadius = (self.gridSize - self.viewingRadius) * self.cellWidth / 2.0
        self.gridSphere = CollisionSphere(self.zoneCenter[0], self.zoneCenter[1], 0.0, gridSphereRadius)
        self.gridSphere.setTangible(0)
        gridSphereName = self.uniqueName('GridSphere')
        cSphereNode = CollisionNode(gridSphereName)
        cSphereNode.setFromCollideMask(BitMask32.allOff())
        cSphereNode.setIntoCollideMask(OTPGlobals.WallBitmask | PiratesGlobals.GoldBitmask | OTPGlobals.GhostBitmask | PiratesGlobals.ShipCollideBitmask)
        cSphereNode.addSolid(self.gridSphere)
        self.gridSphereNodePath = self.attachNewNode(cSphereNode)
        self.accept(self.gridSphereEnterEvent, self.addIslandToOcean)
        self.accept(self.gridSphereExitEvent, self.removeIslandFromOcean)

    def _handleSneakIntoKingshead(self, msgName, avId):
        if avId == localAvatar.doId:
            if base.cr.isPaid() != OTPGlobals.AccessFull:
                self.deniedEntryToIsland()
            else:
                localAvatar.motionFSM.off()
                self.sendUpdate('requestEntryToIsland')
                if self.uniqueId == LocationIds.KINGSHEAD_ISLAND:
                    localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.EnterKingsheadMessage)

    def deniedEntryToIsland(self):
        if self.uniqueId == LocationIds.KINGSHEAD_ISLAND:
            localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.EnterKingsheadWarning)

    def removeIslandGridSphere(self):
        self.ignore(self.gridSphereEnterEvent)
        self.ignore(self.gridSphereExitEvent)
        self.gridSphereNodePath.removeNode()
        self.gridSphere = None

    @report(types=['frameCount', 'args'], dConfigParam=['want-jail-report', 'want-teleport-report'])
    def setupPlayerBarrier(self):
        if not self.playerBarrierNP:
            playerBarrier = CollisionInvSphere(self.zoneCenter[0], self.zoneCenter[1], 0, self.zoneRadii[0] * 0.95)
            playerBarrier.setTangible(1)
            cName = self.uniqueName('PlayerBarrier')
            cSphereNode = CollisionNode(cName)
            cSphereNode.setIntoCollideMask(OTPGlobals.WallBitmask | OTPGlobals.GhostBitmask)
            cSphereNode.addSolid(playerBarrier)
            self.playerBarrierNP = self.attachNewNode(cSphereNode)
            self.accept('enter' + self.uniqueName('PlayerBarrier'), self.enteredPlayerBarrier)
            self.accept('islandPlayerBarrier', self.setPlayerBarrier)

        self.setPlayerBarrier(1)

    @report(types=['frameCount', 'args'], dConfigParam=['want-jail-report', 'want-teleport-report'])
    def enteredPlayerBarrier(self, *args):
        localAvatar.guiMgr.createWarning(PLocalizer.IslandPlayerBarrierWarning, PiratesGuiGlobals.TextFG6)

    @report(types=['frameCount', 'args'], dConfigParam=['want-jail-report', 'want-teleport-report'])
    def unloadPlayerBarrier(self):
        self.ignore('enter' + self.uniqueName('PlayerBarrier'))
        self.ignore('islandPlayerBarrier')
        if self.playerBarrierNP:
            self.playerBarrierNP.removeNode()
            self.playerBarrierNP = None
        return

    @report(types=['frameCount', 'args'], dConfigParam=['want-jail-report', 'want-teleport-report'])
    def setPlayerBarrier(self, isOn):
        if self.playerBarrierNP:
            if isOn:
                self.playerBarrierNP.unstash()
            else:
                self.playerBarrierNP.stash()

    def addIslandToOcean(self, event):
        if self.parentWorld.worldGrid:
            self.parentWorld.worldGrid.addIslandGrid(self)
        else:
            self.notify.error('worldGrid is none for %s %s' % (self.parentWorld, self))

    def removeIslandFromOcean(self, event):
        if self.parentWorld:
            self.parentWorld.worldGrid.removeIslandGrid(self)

    @report(types=['frameCount', 'args'], dConfigParam=['want-jail-report'])
    def setLinks(self, links):
        DistributedGameArea.DistributedGameArea.setLinks(self, links)
        if self.lastZoneLevel == 0:
            self.loadConnectors()

    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    def loadIslandLowLod(self):
        flatName = self.modelPath.split('_zero')
        if not self.islandLowLod:
            self.islandLowLod = loader.loadModelCopy(flatName[0] + '_low')
        if self.islandLowLod and not self.islandLowLod.isEmpty():
            self.islandLowLod.reparentTo(self)
        if 'madre_del_fuego' in self.modelPath:
            self.setupMadreDelFuegoEffects()

    def unloadIslandLowLod(self):
        if self.islandLowLod:
            self.islandLowLod.removeNode()
        self.islandLowLod = None
        return

    def loadIslandMapModel(self):
        if not self.islandMapModelPath:
            mapModelName = self.modelPath.split('_zero')
            self.islandMapModelPath = mapModelName[0] + '_worldmap'

    @report(types=['frameCount', 'args'], dConfigParam='want-map-report')
    def placeOnMap(self):
        self.loadIslandMapModel()
        if not self.mapName and self.islandMapModelPath:
            mapPage = localAvatar.guiMgr.mapPage
            self.mapName = mapPage.addIsland(self.name, self.uniqueId, self.islandMapModelPath, self.getPos(), self.getH())

    @report(types=['frameCount', 'args'], dConfigParam='want-map-report')
    def removeFromMap(self):
        if self.mapName:
            mapPage = localAvatar.guiMgr.mapPage
            mapPage.removeIsland(self.mapName)
        self.mapName = None
        return

    def loadIslandShoreWave(self, parent):
        if hasattr(self, 'islandShoreWave'):
            self.islandShoreWave.reparentTo(parent)
            return
        lowend = ''
        if base.options.terrain_detail_level == 0:
            lowend = '_lowend'
        islandBaseName = self.modelPath.split('_zero')[0]
        waveModel = loader.loadModelCopy(islandBaseName + lowend + '_wave_none')
        if lowend != '' and not waveModel:
            lowend = ''
            waveModel = loader.loadModelCopy(islandBaseName + lowend + '_wave_none')
        if waveModel:
            self.islandShoreWave = Actor.Actor(waveModel)
            self.islandShoreWave.loadAnims({'idle': islandBaseName + lowend + '_wave_idle'})
            self.islandShoreWave.reparentTo(parent)
            self.islandShoreWave.loop('idle')
            meshes = self.islandShoreWave.findAllMatches('**/mesh_tide1')
            if not meshes.isEmpty():
                mesh = meshes[0]
                joint = self.islandShoreWave.findAllMatches('**/uvj_WakeWhiteTide1')[0]
                mesh.setTexProjector(mesh.findTextureStage('default'), joint, parent)
            meshes = self.islandShoreWave.findAllMatches('**/mesh_tide2')
            if not meshes.isEmpty():
                mesh = meshes[0]
                joint = self.islandShoreWave.findAllMatches('**/uvj_WakeWhiteTide2')[0]
                mesh.setTexProjector(mesh.findTextureStage('default'), joint, parent)
            self.islandShoreWave.setPlayRate(0.8, 'idle')
            OTPRender.renderReflection(False, self.islandShoreWave, 'p_island_shore', None)
            alpha_test_attrib = AlphaTestAttrib.make(RenderAttrib.MAlways, 0)
            self.islandShoreWave.setAttrib(alpha_test_attrib, 100)
            self.islandShoreWave.setTwoSided(1, 100)
            self.islandShoreWave.setDepthWrite(0, 100)
        return

    def unloadIslandShoreWave(self):
        if hasattr(self, 'islandShoreWave'):
            self.islandShoreWave.delete()
            del self.islandShoreWave

    def foo(self):
        collNodes = self.geom.findAllMatches('**/+CollisionNode')
        for collNode in collNodes:
            curMask = collNode.node().getIntoCollideMask()
            if curMask.hasBitsInCommon(OTPGlobals.FloorBitmask):
                self.setupCannonballLandColl(collNode, PiratesGlobals.TargetBitmask | curMask, 0)

    def loadIslandParts(self):
        loaderOptions = LoaderOptions(LoaderOptions.LFSearch)
        islandBaseName = self.modelPath.split('_zero')[0]
        lowend = ''
        if base.options.terrain_detail_level == 0:
            lowend = '_lowend'
        terrainModel = loader.loadModelCopy(islandBaseName + '_terrain', loaderOptions)
        if terrainModel:
            self.geom = terrainModel
        else:
            self.geom = loader.loadModelCopy(islandBaseName)
            return
        collNode = self.geom.find('**/cannoncol*')
        if collNode != collNode.notFound():
            collNode.node().setIntoCollideMask(collNode.node().getIntoCollideMask() | PiratesGlobals.TargetBitmask)
            collNode.setTag('objType', str(PiratesGlobals.COLL_BLOCKER))
        terrainDetailModel = loader.loadModelCopy(islandBaseName + lowend + '_terrain_detail', loaderOptions)
        if lowend != '' and not terrainDetailModel:
            terrainDetailModel = loader.loadModelCopy(islandBaseName + '_terrain_detail', loaderOptions)
        if terrainDetailModel:
            terrainDetailModel.getChild(0).reparentTo(self.geom)
        pierModel = loader.loadModelCopy(islandBaseName + lowend + '_pier', loaderOptions)
        if lowend != '' and not pierModel:
            pierModel = loader.loadModelCopy(islandBaseName + '_pier', loaderOptions)
        if pierModel:
            pierModel.getChild(0).reparentTo(self.geom)
        vegeWallModel = loader.loadModelCopy(islandBaseName + lowend + '_nat_wall', loaderOptions)
        if lowend != '' and not vegeWallModel:
            vegeWallModel = loader.loadModelCopy(islandBaseName + '_nat_wall', loaderOptions)
        if vegeWallModel:
            vegeWallModel.getChild(0).reparentTo(self.geom)
        fortModel = loader.loadModelCopy(islandBaseName + lowend + '_fort', loaderOptions)
        if lowend != '' and not fortModel:
            fortModel = loader.loadModelCopy(islandBaseName + '_fort', loaderOptions)
        if fortModel:
            fortModel.getChild(0).reparentTo(self.geom)
        tunnelModel = loader.loadModelCopy(islandBaseName + lowend + '_tunnel', loaderOptions)
        if lowend != '' and not tunnelModel:
            tunnelModel = loader.loadModelCopy(islandBaseName + '_tunnel', loaderOptions)
        if tunnelModel:
            tunnelModel.getChild(0).reparentTo(self.geom)
        rocksModel = loader.loadModelCopy(islandBaseName + lowend + '_rocks', loaderOptions)
        if lowend != '' and not rocksModel:
            rocksModel = loader.loadModelCopy(islandBaseName + '_rocks', loaderOptions)
        if rocksModel:
            rocksModel.getChild(0).reparentTo(self.geom)
        logsModel = loader.loadModelCopy(islandBaseName + lowend + '_logs', loaderOptions)
        if lowend != '' and not logsModel:
            logsModel = loader.loadModelCopy(islandBaseName + '_logs', loaderOptions)
        if logsModel:
            logsModel.getChild(0).reparentTo(self.geom)

    def addToOceanSeapatch(self):
        if self.parentWorld and self.parentWorld.getWater():
            self.parentWorld.getWater().patch.addFlatWell(self.uniqueName('flatWell'), self, self.zoneCenter[0], self.zoneCenter[1], self.zoneRadii[0], self.zoneRadii[0] + 100)

    def removeFromOceanSeapatch(self):
        if self.parentWorld.getWater():
            if 0 and self.portCollisionSpheres:
                for x, pcs in enumerate(self.portCollisionSpheres):
                    self.parentWorld.getWater().patch.removeFlatWell(self.uniqueName('island-%d' % x))

            else:
                self.parentWorld.getWater().patch.removeFlatWell(self.uniqueName('flatWell'))

    def setupIslandGeom(self):
        self.allDetails.unstash()
        self.loadIslandShoreWave(self.geom)
        if base.config.GetBool('want-grass', 0) and Grass.HasGrass(self.modelPath):
            self.grass = Grass.Grass(self)
            self.grass.reparentTo(self.highDetail)
        if 'madre_del_fuego' in self.modelPath:
            self.setupMadreDelFuegoEffects()
        self.ground = {}
        self.ground[0] = self.geom.find('**/island')
        collNodes = self.geom.findAllMatches('**/+CollisionNode')
        for collNode in collNodes:
            curMask = collNode.node().getIntoCollideMask()
            if curMask.hasBitsInCommon(OTPGlobals.FloorBitmask):
                self.setupCannonballLandColl(collNode, PiratesGlobals.TargetBitmask | curMask, 0)

        shipWall = self.geom.find('**/collision_ship*')
        if not shipWall.isEmpty():
            shipWall.setTag('objType', str(PiratesGlobals.COLL_SHIP))
        self.initializeIslandWaterParameters()

    def loadIslandStuff(self):
        self.largeObjects = self.geom.findAllMatches('**/*bldg*')
        for b in self.largeObjects:
            b.wrtReparentTo(self.largeObjectsHigh)
            wallGeom = b.find('**/wall*_n_window*')
            roofGeom = b.find('**/roof')
            for c in [wallGeom, roofGeom]:
                self.setupCannonballBldgColl(c, PiratesGlobals.TargetBitmask)

        details = [
         self.geom.find('**/barrels'), self.geom.find('**/crates'), self.geom.find('**/canopys'), self.geom.find('**/bushes')]
        for detail in details:
            if not detail.isEmpty():
                detail.wrtReparentTo(self.smallObjectsHigh)
                detail.flattenLight()

        self.smallObjects = details
        del details
        details = [self.geom.find('**/palmtrees'), self.geom.find('**/pier')]
        for detail in details:
            if not detail.isEmpty():
                detail.wrtReparentTo(self.medObjectsHigh)
                detail.flattenLight()

        self.mediumObjects = details

    def setName(self, name):
        self.name = name
        if not self.nametag:
            self.createNametag(self.name)
        else:
            self.nametag.setName(name)
        self.nametag.setDisplayName('        ')
        if self.nameText:
            self.nameText['text'] = name
            siegeTeam = self.getSiegeTeam()
            if siegeTeam and self.SiegeIcon:
                color = VBase4(PVPGlobals.getSiegeColor(siegeTeam))
                color.setW(0.7)
                icon = self.SiegeIcon[siegeTeam - 1].copyTo(NodePath('siegeIcons'))
                icon.reparentTo(self.nameText)
                self.SiegeIcons.append(icon)
                icon.setZ(1.5)
                icon.setScale(0.75)
            else:
                color = Vec4(0.6, 0.6, 1, 0.4)
            self.nameText['fg'] = color

    def setDisplayName(self, str):
        self.nametag.setDisplayName(str)

    def getName(self):
        return self.name

    def getNameVisible(self):
        return self.__nameVisible

    def setNameVisible(self, bool):
        self.__nameVisible = bool
        if bool:
            self.showName()
        if not bool:
            self.hideName()

    def hideName(self):
        self.nametag.getNametag3d().setContents(Nametag.CSpeech | Nametag.CThought)

    def showName(self):
        if self.__nameVisible:
            self.nametag.getNametag3d().setContents(Nametag.CName | Nametag.CSpeech | Nametag.CThought)

    def hideNametag2d(self):
        self.nametag2dContents = 0
        self.nametag.getNametag2d().setContents(self.nametag2dContents & self.nametag2dDist)

    def showNametag2d(self):
        self.nametag2dContents = self.nametag2dNormalContents
        self.nametag2dContents = Nametag.CSpeech
        self.nametag.getNametag2d().setContents(self.nametag2dContents & self.nametag2dDist)

    def hideNametag3d(self):
        self.nametag.getNametag3d().setContents(0)

    def showNametag3d(self):
        if self.__nameVisible:
            self.nametag.getNametag3d().setContents(Nametag.CName | Nametag.CSpeech | Nametag.CThought)
        else:
            self.nametag.getNametag3d().setContents(0)

    def setPickable(self, flag):
        self.nametag.setActive(flag)

    def clickedNametag(self):
        if self.nametag.isActive():
            messenger.send('clickedNametag', [self])

    def initializeNametag3d(self):
        self.deleteNametag3d()
        self.nametag.setFont(PiratesGlobals.getPirateFont())
        nametagNode = self.nametag.getNametag3d()
        self.nametag3d.attachNewNode(nametagNode)
        self.nametag3d.setFogOff()
        self.nametag3d.setLightOff()
        self.nametag3d.setColorScaleOff(100)
        self.nametag3d.setDepthWrite(0)
        self.iconNodePath = self.nametag.getNameIcon()
        if self.iconNodePath.isEmpty():
            self.notify.warning('empty iconNodePath in initializeNametag3d')
            return 0

        if not self.nameText:
            self.nameText = OnscreenText(fg=Vec4(1, 1, 1, 1), bg=Vec4(0, 0, 0, 0), scale=1.1, align=TextNode.ACenter, mayChange=1, font=PiratesGlobals.getPirateBoldOutlineFont())
            self.nameText.setDepthWrite(0)
            self.nameText.reparentTo(self.iconNodePath)
            self.nameText.setColorScaleOff(100)
            self.nameText.setLightOff()
            self.nameText.setFogOff()

    def deleteNametag3d(self):
        children = self.nametag3d.getChildren()
        for i in range(children.getNumPaths()):
            children[i].removeNode()

    def addActive(self):
        if base.wantNametags:
            self.nametag.manage(base.marginManager)
            self.accept(self.nametag.getUniqueId(), self.clickedNametag)

    def removeActive(self):
        if base.wantNametags and self.nametag:
            self.nametag.unmanage(base.marginManager)
            self.ignore(self.nametag.getUniqueId())

    def createNametag(self, name):
        self.__nameVisible = 1
        self.nametag = NametagGroup()
        self.nametag.setAvatar(self)
        self.nametag.setFont(PiratesGlobals.getPirateFont())
        self.nametag2dContents = Nametag.CName
        self.nametag2dDist = Nametag.CName
        self.nametag2dNormalContents = Nametag.CName
        self.nametag3d = self.attachNewNode('nametag3d')
        self.nametag3d.setTag('cam', 'nametag')
        self.nametag.setName(name)
        self.nametag.setWordwrap(PiratesGlobals.NAMETAG_WORDWRAP)
        OTPRender.renderReflection(False, self.nametag3d, 'p_island_nametag', None)
        self.nametag3d.setPos(0, 0, WorldGlobals.getNametagHeight(self.name))
        self.setNametagScale(WorldGlobals.getNametagScale(self.name))
        self.nametag3d.setFogOff()
        self.setPickable(0)
        self.nametag.setColorCode(1)

    def getNametagScale(self):
        return self.nametagScale

    def setNametagScale(self, scale):
        self.nametagScale = scale
        self.nametag3d.setScale(scale)

    def setPlayerType(self, playerType):
        self.playerType = playerType
        self.nametag.setColorCode(self.playerType)

    def startCustomEffects(self, interior=False):
        DistributedGameArea.DistributedGameArea.startCustomEffects(self, interior=False)
        if self.grass:
            self.grass.start()

        if self.blackSmokeEffect:
            self.blackSmokeEffect.reparentTo(self.geom)
            self.blackSmokeEffect.setPos(0, 0, 650)
            self.blackSmokeEffect.startLoop()

        if self.volcanoEffect:
            if self.lastZoneLevel <= 3:
                self.startVolcanoSmokeEffect()

            if self.lastZoneLevel < 2:
                self.startVolcanoRestEffects()

        base.cr.timeOfDayManager.setEnvironment(TODGlobals.ENV_DEFAULT)
        self.resumeSFX()

    def stopCustomEffects(self):
        DistributedGameArea.DistributedGameArea.stopCustomEffects(self)
        if self.grass:
            self.grass.stop()
        if self.blackSmokeEffect:
            self.blackSmokeEffect.stop()
        if self.volcanoEffect:
            self.stopVolcanoSmokeEffect()
            self.stopVolcanoRestEffects()
        self.pauseSFX()

    def startVolcanoRestEffects(self):
        if self.volcanoEffect:
            self.volcanoEffect.enableFogSmoke()
            self.volcanoEffect.start()
        if self.lavaFlowEffect:
            self.startLavaFlow()
        if self.steamFlowEffect:
            self.startSteamFlow()

    def stopVolcanoRestEffects(self):
        if self.volcanoEffect:
            self.volcanoEffect.stop()
            self.volcanoEffect.disableFogSmoke()
            self.volcanoEffect.disableRest()
        if self.lavaFlowEffect:
            self.stopLavaFlow()
        if self.steamFlowEffect:
            self.stopSteamFlow()

    def startVolcanoSmokeEffect(self):
        if self.volcanoEffect:
            self.volcanoEffect.enableSmoke()
            self.volcanoEffect.accelerateSmoke(time=90)

    def stopVolcanoSmokeEffect(self):
        if self.volcanoEffect:
            self.volcanoEffect.disableSmoke()

    def adjustSmokeParentAndPos(self, parent, pos):
        if self.volcanoEffect:
            self.volcanoEffect.reparentTo(parent)
            self.volcanoEffect.setPos(pos)

    def setupMadreDelFuegoEffects(self):
        if not self.volcanoEffect:
            self.volcanoEffect = VolcanoEffect()
        self.lavaFlowEffect = True
        self.steamFlowEffect = True

    def startLavaFlow(self):
        self.stopLavaFlow()
        lavaGeom = self.geom.find('**/lava')
        if not lavaGeom.isEmpty():
            lavaGeom.setLightOff()
            if base.main_rtt:
                lavaGeom.setFogOff()
                lavaGeom.showThrough(OTPRender.GlowCameraBitmask)
            tex = None
            if not lavaGeom.findTextureStage('VertexColor'):
                ts = TextureStage('VertexColor')
                ts.setSort(30)
                tex = lavaGeom.findTexture('*')
                if tex:
                    lavaGeom.setTexture(ts, tex)
            tsSet = lavaGeom.findAllTextureStages()
            tsSet = [ tsSet[x] for x in range(tsSet.getNumTextureStages()) ]
            tsSet.sort(key=lambda x: x.getSort())
            if not tsSet:
                return
            TS = TextureStage
            tsSet[0].setCombineRgb(TS.CMReplace, TS.CSTexture, TS.COSrcColor)
            tsSet[1].setCombineRgb(TS.CMAdd, TS.CSTexture, TS.COSrcColor, TS.CSPrevious, TS.COSrcColor)
            tsSet[2].setCombineRgb(TS.CMInterpolate, TS.CSTexture, TS.COSrcColor, TS.CSPrevious, TS.COSrcColor, TS.CSPrimaryColor, TS.COSrcAlpha)
            lavaSpeed = {0: 0.04, 1: 0.02, 2: 0.01}
            if tex:
                tsSet[3].setCombineRgb(TS.CMModulate, TS.CSPrevious, TS.COSrcColor, TS.CSPrimaryColor, TS.COSrcColor)
                tsSet[3].setCombineAlpha(TS.CMReplace, TS.CSConstant, TS.COSrcAlpha)
                tsSet[3].setColor(Vec4(1))
                lavaSpeed[3] = 0.0

            def flowLava(task):
                dt = globalClock.getDt()
                for key in list(lavaSpeed.keys()):
                    offset = lavaGeom.getTexOffset(tsSet[key])[0]
                    offset -= lavaSpeed[key] * dt
                    offset %= 1.0
                    lavaGeom.setTexOffset(tsSet[key], offset, 0)

                return Task.cont

            taskMgr.add(flowLava, self.uniqueName('flowLava'))
        return

    def stopLavaFlow(self):
        if self.geom and not self.geom.isEmpty():
            lavaGeom = self.geom.find('**/lava_red*')
            if lavaGeom and not lavaGeom.isEmpty():
                lavaGeom.clearLight()
                lavaGeom.clearFog()
        taskMgr.remove(self.uniqueName('flowLava'))

    def startSteamFlow(self):
        steamGeom = self.geom.find('**/steam')
        if not steamGeom.isEmpty():
            steamGeom.setDepthWrite(0)
            steamGeom.setBin('fixed', 20)
            steamGeom.setTwoSided(True)

            def flowSteam(task):
                dt = globalClock.getDt()
                offset = steamGeom.getTexOffset(TextureStage.getDefault())[1]
                offset -= 0.0025
                offset %= 1.0
                steamGeom.setTexOffset(TextureStage.getDefault(), 0, offset)
                return Task.cont

            taskMgr.add(flowSteam, self.uniqueName('flowSteam'))

    def stopSteamFlow(self):
        taskMgr.remove(self.uniqueName('flowSteam'))

    def setIslandWaterParameters(self, use_alpha_map):
        if self.islandWaterParameters:
            if self.parentWorld:
                self.islandWaterParameters.setIslandWaterParameters(self.parentWorld.getWater(), use_alpha_map)

    def setX(self, *args, **kwargs):
        DistributedGameArea.DistributedGameArea.setX(self, *args, **kwargs)
        mapPage = base.localAvatar.guiMgr.mapPage
        mapPage.updateIsland(self.mapName, worldPos=self.getPos())

    def setY(self, *args, **kwargs):
        DistributedGameArea.DistributedGameArea.setY(self, *args, **kwargs)
        mapPage = base.localAvatar.guiMgr.mapPage
        mapPage.updateIsland(self.mapName, worldPos=self.getPos())

    def setH(self, *args, **kwargs):
        DistributedGameArea.DistributedGameArea.setH(self, *args, **kwargs)
        mapPage = base.localAvatar.guiMgr.mapPage
        mapPage.updateIsland(self.mapName, rotation=self.getH())

    def getTeam(self):
        return PiratesGlobals.ISLAND_TEAM

    def updateAvReturnLocation(self, av):
        av.d_requestReturnLocation(self.doId)

    def updateAvIsland(self, av):
        av.d_requestCurrentIsland(self.doId)

    def startFloatables(self):
        world = base.cr.getActiveWorld()
        if world:
            water = world.getWater()
            if water:
                for uid, obj in self.floatables.items():
                    water.addFloatable(uid, obj, mass=5)

    def stopFloatables(self):
        world = base.cr.getActiveWorld()
        if world:
            water = world.getWater()
            if water:
                for uid in self.floatables:
                    water.removeFloatable(uid)

    @report(types=['frameCount', 'args'], dConfigParam='want-connector-report')
    def setOceanVisEnabled(self, enabled):
        self.oceanVisEnabled = enabled
        if self.lastZoneLevel == 0:
            if not self.oceanVisEnabled:
                self.parentWorld.worldGrid.stopProcessVisibility()
            else:
                self.parentWorld.worldGrid.startProcessVisibility(localAvatar)

    def setFlatShips(self, value):
        self.flatShipsOnIsland = value
        if self.lastZoneLevel == 0:
            if self.flatShipsOnIsland:
                messenger.send('far-ships')
                base.showShipFlats = True
            else:
                messenger.send('normal-ships')
                base.showShipFlats = False

    def listenForLocationSphere(self):
        self.locationSphereName = self.cr.activeWorld.uniqueName('locSphere')
        msgName = PiratesGlobals.LOCATION_SPHERE
        self.accept('enter' + self.locationSphereName, self.cr.getActiveWorld().enteredSphere, extraArgs=[[msgName]])
        self.accept('exit' + self.locationSphereName, self.cr.getActiveWorld().exitedSphere, extraArgs=[[msgName]])

    def stopListenForLocationSphere(self):
        if self.locationSphereName:
            self.ignore('enter' + self.locationSphereName)
            self.ignore('exit' + self.locationSphereName)

    def buildCacheData(self):
        coreCache = self.getCoreCache()
        dependencies = self.cr.distributedDistrict.worldCreator.getFilelistByUid(self.uniqueId)
        if self.playerBarrierNP:
            self.playerBarrierNP.detachNode()
        if self.geom:
            self.geom.detachNode()
        gridGeomCache = self.getGridCache()
        largeGeomCache = self.getLargeObjectsCache()
        animCache = self.getAnimCache()
        self.loadZoneObjects(-1)
        avatarParent = localAvatar.getParent()
        localAvatar.detachNode()
        largeObjectsLOD = self.largeObjectsHigh.getParent()
        largeGeomCache.setData(largeObjectsLOD.node(), 0)
        base.bamCache.store(largeGeomCache)
        objectsHighParent = self.largeObjectsHigh.getParent()
        self.largeObjectsHigh.detachNode()
        objectsLowParent = self.largeObjectsLow.getParent()
        self.largeObjectsLow.detachNode()
        gridGeomCache.setData(self.staticGridRoot.node(), 0)
        base.bamCache.store(gridGeomCache)
        animCache.setData(self.animNode.node(), 0)
        base.bamCache.store(animCache)
        allDetailsParent = self.allDetails.getParent()
        self.allDetails.detachNode()
        for sphere in self.zoneSphere:
            sphere.detachNode()

        nametagParent = self.nametag3d.getParent()
        self.nametag3d.detachNode()
        animNodeParent = self.animNode.getParent()
        self.animNode.detachNode()
        staticGridParent = self.staticGridRoot.getParent()
        self.staticGridRoot.detachNode()
        if localAvatar.questStep and localAvatar.questStep.getStepDoId() == self.doId:
            localAvatar.questIndicator.indicatorNode.detachNode()
        shipDeployer = self.find('ShipDeployer')
        if not shipDeployer.isEmpty():
            shipDeployer.detachNode()
        coreCache.setData(self.node(), 0)
        base.bamCache.store(coreCache)
        if not shipDeployer.isEmpty():
            shipDeployer.reparentTo(self)
        if localAvatar.questStep and localAvatar.questStep.getStepDoId() == self.doId:
            localAvatar.questIndicator.indicatorNode.reparentTo(self)
        self.animNode.reparentTo(animNodeParent)
        self.staticGridRoot.reparentTo(staticGridParent)
        self.allDetails.reparentTo(allDetailsParent)
        self.largeObjectsHigh.reparentTo(objectsHighParent)
        self.largeObjectsLow.reparentTo(objectsLowParent)
        self.nametag3d.reparentTo(nametagParent)
        if self.geom:
            self.geom.reparentTo(self)
        for sphere in self.zoneSphere:
            sphere.reparentTo(self)

        localAvatar.reparentTo(avatarParent)
        if self.playerBarrierNP:
            self.playerBarrierNP.reparentTo(self)

    def buildIslandTerrain(self):
        islandGeomCache = self.getIslandCache()
        self.loadIslandParts()
        if self.geom:
            flat = self.geom.find('**/island_flat_lod')
            if not flat.isEmpty():
                flat.removeNode()
            islandGeomCache.setData(self.geom.node(), 0)
            base.bamCache.store(islandGeomCache)
        else:
            self.geom = NodePath('bad island')
            self.notify.warning('Island %s,%s terrain failed to load!' % (self.doId, self.name))

    def retrieveIslandTerrain(self):
        islandGeomCache = self.getIslandCache()
        if not islandGeomCache.hasData() or not base.config.GetBool('want-disk-cache', 0):
            self.buildIslandTerrain()
        else:
            data = islandGeomCache.getData()
            newData = data.copySubgraph()
            self.geom = NodePath(newData)
        self.geom.reparentTo(self)

    @report(types=['frameCount', 'args'], dConfigParam=['want-island-report'])
    def retrieveCacheData(self):
        coreCache = self.getCoreCache()
        if not coreCache.hasData() or not base.config.GetBool('want-disk-cache', 0):
            self.buildCacheData()
        else:
            gridGeomCache = self.getGridCache()
            largeGeomCache = self.getLargeObjectsCache()
            animCache = self.getAnimCache()
            if gridGeomCache.hasData() and largeGeomCache.hasData() and animCache.hasData():
                data = coreCache.getData()
                newData = data.copySubgraph()
                self.collisions.removeNode()
                self.node().stealChildren(newData)
                self.node().copyTags(newData)
                self.collisions = self.find('collisions')
                data = gridGeomCache.getData()
                newData = data.copySubgraph()
                self.staticGridRoot.node().stealChildren(newData)
                self.staticGridRoot.node().copyTags(newData)
                self.staticGridRoot.setClipPlane(base.farCull)
                data = largeGeomCache.getData()
                newData = data.copySubgraph()
                largeObjects = NodePath(newData)
                largeObjects.reparentTo(self.allDetails)
                self.largeObjectsHigh.node().stealChildren(newData.getChild(0))
                self.largeObjectsHigh.node().copyTags(newData)
                self.largeObjectsLow.node().stealChildren(newData.getChild(1))
                self.largeObjectsLow.node().copyTags(newData)
                for np in self.largeObjectsHigh.findAllMatches('**/+LODNode') :
                    np.setClipPlane(base.farCull)

                data = animCache.getData()
                newData = data.copySubgraph()
                self.animNode.node().stealChildren(newData)
                self.animNode.node().copyTags(newData)
            else:
                self.buildCacheData()

    def checkCacheValidity(self):
        if base.launcher.isDownloadComplete():
            coreCache = self.getCoreCache()
            if not coreCache.hasData():
                self.buildCacheData()
                self.buildIslandTerrain()
                self.cleanupIslandData()
                self.cleanupTerrain()

    def cleanupIslandData(self):
        self.clearAnims()
        self.unloadZoneObjects()
        self.staticGridRoot.get_children().detach()
        self.largeObjectsHigh.get_children().detach()
        self.largeObjectsLow.get_children().detach()
        self.animNode.get_children().detach()

    def cleanupTerrain(self):
        self.geom.removeNode()
        self.geom = None
        return

    def getCoreCache(self):
        return base.bamCache.lookup(Filename('/%s_%s_core_%s_%s' % (self.name, self.uniqueId, base.launcher.ServerVersion, base.gridDetail)), '')

    def getGridCache(self):
        return base.bamCache.lookup(Filename('/%s_%s_grid_%s' % (self.name, self.uniqueId, base.gridDetail)), '')

    def getAnimCache(self):
        return base.bamCache.lookup(Filename('/%s_%s_anims_%s' % (self.name, self.uniqueId, base.gridDetail)), '')

    def getLargeObjectsCache(self):
        return base.bamCache.lookup(Filename('/%s_large_%s' % (self.name, base.gridDetail)), '')

    def getIslandCache(self):
        return base.bamCache.lookup(Filename('/%s_%s_island_%s_%s' % (self.name, self.uniqueId, base.launcher.ServerVersion, base.gridDetail)), '')

    def getSiegeTeam(self):
        return base.cr.distributedDistrict.worldCreator.getPvpIslandTeam(self.uniqueId)

    def setUndockable(self, undockable):
        self.undockable = undockable

    def shipVisibilityChanged(self, value):
        if value == 0:
            self.parentWorld.worldGrid.stopProcessVisibility()
        else:
            if value == 1:
                self.parentWorld.worldGrid.startProcessVisibility(localAvatar)
                base.showShipFlats = True
                messenger.send('far-ships')
            else:
                if value == 2:
                    self.parentWorld.worldGrid.startProcessVisibility(localAvatar)
                    base.showShipFlats = False
                    messenger.send('normal-ships')

    def handleTunnelsOnRadar(self, show=True):
        self.hasTunnelsOnRadar = show
        portalNPs = self.findAllMatches('**/portal_exterior*')
        for i in range(0, portalNPs.getNumPaths()):
            pe = portalNPs[i]
            if show:
                localAvatar.guiMgr.radarGui.addRadarObjectAtLoc(pe.getPos(render), objType=RadarGui.RADAR_OBJ_TYPE_EXIT, targetObjId='exit-' + str(i))
            else:
                localAvatar.guiMgr.radarGui.removeRadarObject('exit-' + str(i))

    if __dev__:

        @report(types=['frameCount', 'args'], dConfigParam=['want-connector-report', 'want-jail-report', 'want-island-report'])
        def setZoneLevel(self, *args, **kw):
            ZoneLOD.ZoneLOD.setZoneLevel(self, *args, **kw)

    def getIslandTransform(self):
        return (
         self.getX(), self.getY(), self.getZ(), self.getH())

    def setIslandTransform(self, x, y, z, h):
        self.setXYZH(x, y, z, h)

    def buildGridTable(self):
        nodes = self.staticGridRoot.findAllMatches('Grid*')
        for i in range(nodes.getNumPaths()):
            node = nodes[i]
            gridNum = int(re.search('Grid-([0-9]+)Node', node.getName()).groups()[0])
            self.gridNodes[gridNum] = node
            node.hide()

    def handleAvatarZoneChangeNew(self, av, zoneId):
        if av.isLocal():
            if not self.gridNodes:
                self.buildGridTable()
            zonesNew = None
            zonesOld = None
            if self.visTable:
                zonesNew = self.visTable.get(zoneId)
            if not zonesNew:
                zonesNew = set(self.getConcentricZones(zoneId, 3) + self.getConcentricZones(zoneId, 2) + self.getConcentricZones(zoneId, 1))
            zonesNew.add(zoneId)
            if self.visTable:
                zonesOld = self.visTable.get(av.zoneId)
            if not zonesOld:
                zonesOld = set(self.getConcentricZones(av.zoneId, 3) + self.getConcentricZones(av.zoneId, 2) + self.getConcentricZones(av.zoneId, 1))
            zonesOld.add(av.zoneId)
            for zone in zonesOld:
                gridZone = self.gridNodes.get(zone)
                if gridZone:
                    gridZone.hide()

            for zone in zonesNew:
                gridZone = self.gridNodes.get(zone)
                if gridZone:
                    gridZone.show()
                    gridZone.setColor(0, 1, 0, 1)

        DistributedCartesianGrid.DistributedCartesianGrid.handleAvatarZoneChange(self, av, zoneId)
        return
