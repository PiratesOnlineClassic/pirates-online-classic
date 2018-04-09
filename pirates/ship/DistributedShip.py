# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.ship.DistributedShip
import re, random
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.PythonUtil import Functor, ScratchPad, report, lerp, quickProfile, safeRepr
from direct.controls import ControlManager
from pirates.ship.ShipPilot import ShipPilot
from direct.task import Task
from direct.distributed.ClockDelta import *
from direct.showutil import Rope
from direct.distributed.CachedDOData import CachedDOData
from pirates.movement.DistributedMovingObject import DistributedMovingObject
from pirates.ship.GameFSMShip import GameFSMShip
from pirates.distributed.DistributedCharterableObject import DistributedCharterableObject
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.ShipStatusDisplay import ShipStatusDisplay
from pirates.piratesgui import ShipTargetPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import ShipFrameBoard
from pirates.shipparts import DistributedSteeringWheel
from pirates.shipparts import HullDNA
from pirates.shipparts import SailDNA, Sail
from pirates.demo import DemoGlobals
from pirates.ship import ShipMeter
from pirates.ship import ShipCameraParams
from pirates.world import ZoneLOD
from pirates.battle import WeaponGlobals
from pirates.battle import DistributedShipCannon
from pirates.effects.Wake import Wake
from pirates.effects.WakeMist import WakeMist
from pirates.effects.WindBlurCone import WindBlurCone
from pirates.effects.DarkMaelstrom import DarkMaelstrom
from pirates.effects.Wind import Wind
from pirates.effects.FadingCard import FadingCard
from pirates.effects.ShipFog import ShipFog
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.ShockwaveHit import ShockwaveHit
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.CameraShaker import CameraShaker
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.uberdog import DistributedInventory
from pirates.battle import DistributedBattleAvatar
from pirates.battle import CannonGlobals
from pirates.ship import ShipRocker
from pirates.battle import EnemyGlobals
from pirates.piratesbase import TeamUtils
from pirates.piratesbase import Freebooter
from pirates.pvp import PVPGlobals
from pirates.piratesgui import PVPRankGui
from pirates.battle.Teamable import Teamable
from pirates.world import DistributedOceanGrid
from pirates.effects import TextEffect
from pirates.piratesgui.ShipTargets import ShipTargets, Target
from pirates.effects.WaterSplashes import WaterSplashes
from pirates.effects.WaterWakes import WaterWakes
from pirates.effects.WaterMist import WaterMist
from pirates.effects.ProtectionDome import ProtectionDome
from pirates.effects.ShipPowerRecharge import ShipPowerRecharge
from pirates.effects.ShipDestruction import ShipDestruction
from pirates.band.DistributedBandMember import DistributedBandMember
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPRender
import ShipGlobals, ShipBalance
from direct.fsm.StatePush import FunctionCall, AttrSetter
import random, math
STOP = 0
FWD = 1
BACK = -1
RIGHT = 1
LEFT = -1

def getRamSfx():
    hitSfxs = (
     base.loader.loadSfx('audio/wood_impact_1.mp3'), base.loader.loadSfx('audio/wood_impact_3.mp3'))
    return hitSfxs


class CachedShipData(CachedDOData):
    

    def __init__(self, optimized, broadside, hull, cabin, masts, sails, cannons, wheel, bowsprit, fullsailSfx, rammingSfx, sinkingSfx, lodRoot, highDetail, medDetail, lowDetail, highStatic, medStatic, lowStatic, modelCollisions, sailProjectors, locators):
        self.optimized = optimized
        self.broadside = broadside
        self.hull = hull
        self.cabin = cabin
        self.masts = masts
        self.sails = sails
        self.cannons = cannons
        self.wheel = wheel
        self.bowsprit = bowsprit
        self.fullsailSfx = fullsailSfx
        self.rammingSfx = rammingSfx
        self.sinkingSfx = sinkingSfx
        self.lodRoot = lodRoot
        self.highDetail = highDetail
        self.medDetail = medDetail
        self.lowDetail = lowDetail
        self.highStatic = highStatic
        self.medStatic = medStatic
        self.lowStatic = lowStatic
        self.modelCollisions = modelCollisions
        self.sailProjectors = sailProjectors
        self.locators = locators

    def flush(self):
        if self.broadside:
            for side in self.broadside[0]:
                for cannonPort in side:
                    if cannonPort:
                        cannonPort.delete()

        if self.hull:
            self.hull[0].unloadModel()
            self.hull[0].disable()
            self.hull[0].delete()
        if self.cabin:
            self.cabin[0].unloadModel()
            self.cabin[0].disable()
            self.cabin[0].delete()
        for mast in self.sails.values():
            for sail in mast.values():
                sail[0].delete()

        for mast in self.masts.values():
            mast[0].delete()

        for entry in self.cannons.values():
            cannon = entry[0]
            cannon.delete()

        self.locators.detachNode()


class ActorNodeMgr:
    

    def __init__(self, actorNode):
        self._actorNode = actorNode
        self._attached = False
        self._loadedZoneLevels = set()
        self._wantPhysics = True
        self._processStateChange()

    def destroy(self):
        if self._attached:
            base.avatarPhysicsMgr.removePhysicalNode(self._actorNode)
        self._actorNode = None
        return

    def setWantPhysics(self, flag):
        self._wantPhysics = flag
        self._processStateChange()

    def loadZoneLevel(self, level):
        self._loadedZoneLevels.add(level)
        self._processStateChange()

    def unloadZoneLevel(self, level):
        self._loadedZoneLevels.remove(level)
        self._processStateChange()

    def _processStateChange(self):
        if self._attached:
            if not self._wantPhysics or 1 not in self._loadedZoneLevels:
                base.avatarPhysicsMgr.removePhysicalNode(self._actorNode)
                self._attached = False
        else:
            if self._wantPhysics and 1 in self._loadedZoneLevels:
                base.avatarPhysicsMgr.attachPhysicalNode(self._actorNode)
                self._attached = True


class DistributedShip(DistributedMovingObject, DistributedCharterableObject, ZoneLOD.ZoneLOD, Teamable):
    
    deferrable = True
    notify = directNotify.newCategory('DistributedShip')
    WantWake = config.GetBool('want-wake', 1)
    HpTextGenerator = TextNode('HpTextGenerator')
    HpTextEnabled = 1
    fullsailSfx = None
    rammingSfx = None
    sinkingSfx = None
    ShipBin = 100
    ShipBinPriority = 2000
    BountyIcon = None
    Sp2indices = {ShipGlobals.SamplePoints.FL: (-1, 1), ShipGlobals.SamplePoints.F: (0, 1), ShipGlobals.SamplePoints.FR: (1, 1), ShipGlobals.SamplePoints.L: (-1, 0), ShipGlobals.SamplePoints.C: (0, 0), ShipGlobals.SamplePoints.R: (1, 0), ShipGlobals.SamplePoints.BL: (-1, -1), ShipGlobals.SamplePoints.B: (0, -1), ShipGlobals.SamplePoints.BR: (1, -1)}
    SAIL_READY_DELAY = 1.4

    def __init__(self, cr):
        self.actorNode = ActorNode('ship-physicsActor')
        NodePath.__init__(self, self.actorNode)
        DistributedMovingObject.__init__(self, cr)
        DistributedCharterableObject.__init__(self, cr)
        Teamable.__init__(self)
        self.optimized = False
        self.uniqueId = ''
        self.captainId = 0
        self.propCollisions = self.attachNewNode('propCollisions')
        self.buildComplete = False
        self.buildCompleteFunctions = []
        self.mainPartsBuilt = False
        self.mainBuiltFunctions = []
        self.hpText = None
        self.repairCount = 0
        self.diskRadius = 5.0
        self.proximityRadius = 4.0
        self.nametag = None
        self.nametag3d = None
        self.badge = None
        self.shoutTextEffect = None
        self.takeCoverEffect = None
        self.openFireEffect = None
        self.windConeEffect = None
        self.windTunnelEffect1 = None
        self.windTunnelEffect2 = None
        self.powerRechargeEffect = None
        self.protectionEffect = None
        self.sinkEffectsRoot = None
        self.sinkEffects = []
        self.sphereRadii = PiratesGlobals.ShipZones
        ZoneLOD.ZoneLOD.__init__(self, self.uniqueName)
        self.name = ''
        self.isNpc = 0
        self.isFlagship = 0
        self.beacon = None
        self._boardingTimer = None
        self.ship = None
        self.locators = None
        self.hull = None
        self.cabin = None
        self.ram = None
        self.bowsprit = None
        self.wheel = None
        self.masts = {}
        self.sails = {}
        self.sailProjectors = {}
        self.decors = {1: {}, 2: {}, 3: {}}
        self.sailsDown = 0
        self.dimensionsComputed = False
        self.bow = None
        self.port = None
        self.starboard = None
        self.stern = None
        self.keel = None
        self.peak = None
        self.center = None
        self.hullCenter = None
        self.dimensions = None
        self.hullDimensions = None
        self.cannons = {}
        self.broadside = None
        self.zoneCollNodes = []
        self.zoneSpheres = []
        self.zoneStates = [
         0, 0, 0, 0]
        self.shipClass = 0
        self.modelClass = 0
        self.pvpTeam = 0
        self.Hp = 0
        self.maxSp = 0
        self.Sp = 0
        self.deltaHp = 0
        self.deltaSp = 0
        self.cargo = []
        self.maxCargo = 0
        self.level = 0
        self.crew = []
        self.steeringAvId = 0
        self.inventoryId = 0
        self.isStatusDisplayVisible = 0
        self.isTargetPanelVisible = 0
        self.iconNodePath = None
        self.velocity = 0
        self.zOffset = 0
        self.worldVelocity = Vec3.zero()
        self.currentTurning = 0
        self.autoSailing = 0
        self.sailsReady = 1
        self._rocker = ShipRocker.ShipRocker()
        self.leftDamageLvl = 0
        self.rightDamageLvl = 0
        self.renownDisplay = None
        self.shipStatusDisplay = None
        self.shipTargetPanel = None
        self.sunk = 0
        self.sinkTime = 0
        self.sinkTimestamp = 0
        self.sinkTrack = None
        self.fadeInSpawnIval = None
        self.stats = None
        self.fadeIval = None
        self.listIval = None
        self.fog = None
        self.fogIval = None
        self.rope = None
        self.boardableShipId = None
        self.isInBoardingPosition = 0
        self.landedGrapples = []
        self.landedGrappleNodes = []
        self.pendingLandedGrapples = None
        self.boardingPanel = None
        self.boardingInProgress = 0
        self.collHandler = None
        self.rammingSphereNodePath = None
        self.debugCSphere = None
        self.debugCSphereNodePath = None
        self.unboardTubeNodePath = None
        self.unboardTube = None
        self.interactTube = None
        self.shellSphereNodePath = None
        self.collModels = []
        self.wake = None
        self.fader = None
        self.skillEffects = {}
        self.enableAutoSail = 0
        self.deckName = None
        self.railingName = None
        self.floorCollisions = None
        self.isBoardable = 0
        self.isExitable = 0
        self.lockedSails = 0
        self.pendingClientSteer = None
        self.pendingBeginSteer = None
        self.unboardTest = 0
        self.stormEffect = None
        self.gameFSM = GameFSMShip(self)
        self.pendingDoMovie = None
        self.curAttackAnim = None
        self.textEffects = []
        self.waterlineNode = self.attachNewNode('waterlineZ')
        self.waterlineNode.setH(180)
        self.transNode = self.waterlineNode.attachNewNode('transNode')
        self.root = self.transNode.attachNewNode('shipRoot')
        self.flat = None
        self.lookAtDummy = self.transNode.attachNewNode('lookAtDummy')
        self.clipParent1 = self.root.attachNewNode(ModelNode('clipParent1'))
        self.clipParent2 = self.root.attachNewNode(ModelNode('clipParent2'))
        self.modelGeom = self.clipParent1.attachNewNode(ModelNode('modelGeomRoot'))
        self.modelCollisions = self.root.attachNewNode(ModelNode('modelCol'))
        self.modelCollisions.hide()
        self.interactionCollisions = self.root.attachNewNode(ModelNode('interactCol'))
        self.avCannonNode = self.root.attachNewNode(ModelNode('avCannonNode'))
        self.avCannonRotate = self.avCannonNode.attachNewNode(ModelNode('avCannonRotate'))
        self.avCannonView = self.avCannonRotate.attachNewNode(ModelNode('avCannonView'))
        self.avCannonPivot = self.avCannonRotate.attachNewNode(ModelNode('avCannonPivot'))
        lodNode = LODNode('lodRoot')
        lodNode.addSwitch(200, 0)
        lodNode.addSwitch(1200, 200)
        lodNode.addSwitch(100000, 1200)
        self.lodRoot = NodePath(lodNode)
        self.lodRoot.reparentTo(self.modelGeom)
        self.highDetail = self.lodRoot.attachNewNode(ModelNode('high'))
        self.mediumDetail = self.lodRoot.attachNewNode(ModelNode('medium'))
        self.lowDetail = self.lodRoot.attachNewNode(ModelNode('low'))
        self.highStatic = self.highDetail.attachNewNode(ModelNode('staticGeom'))
        self.mediumStatic = self.mediumDetail.attachNewNode(ModelNode('staticGeom'))
        self.lowStatic = self.lowDetail.attachNewNode(ModelNode('staticGeom'))
        self._instantBoard = 0
        self.controlManager = None
        self._shipCamParams = None
        self.respectDeployBarriers = False
        self.deployBarrierId = 0
        self.clientController = 0
        self.oldRightTarget = None
        self.oldLeftTarget = None
        self.localAvatarBoardingPosHpr = None
        if not self.fullsailSfx:
            self.fullsailSfx = loader.loadSfx('audio/sfx_ship_sails-unfurl.mp3')
        if not self.rammingSfx:
            self.rammingSfx = loader.loadSfx('audio/sfx_ship_ramming.mp3')
        if not self.sinkingSfx:
            self.sinkingSfx = loader.loadSfx('audio/sfx_ship_sinking.mp3')
        self.bandId = (0, 0)
        self.isSplit = False
        self.miniLog = None
        self.kraken = None
        self.textEffects = []
        self.oldZoom = None
        self.baseSpeedMod = 1.0
        self.targets = ShipTargets(self)
        self.target = Target(self)
        self.BountyIcons = []
        if not self.BountyIcon and base.config.GetBool('want-bountyicons', 0):
            gui = loader.loadModel('models/gui/toplevel_gui')
            self.BountyIcon = [gui.find('**/ship_pvp_icon_french'), gui.find('**/ship_pvp_icon_spanish')]
        return

    def getPrefix(self):
        filePrefix = HullDNA.HullDict.get(self.modelClass)
        return filePrefix

    def destroy(self):
        if not self.DistributedObject_deleted:
            from direct.showbase.PythonUtil import StackTrace
            print StackTrace()
            self.notify.error('ship(%s,%d) called destroy() outside of delete()' % (self.name, self.doId))
        self._rocker.destroy()
        del self._rocker
        del self.actorNode
        self.removeNode()
        self.gameFSM.cleanup()
        self.gameFSM = None
        while len(self.BountyIcons):
            icon = self.BountyIcons.pop()
            icon.removeNode()
            icon = None

        return

    def generate(self):
        if self.hasCachedData('DistributedShip'):
            cachedData = self.getCachedData('DistributedShip')
            self.optimized = cachedData.optimized
            self.broadside = cachedData.broadside
            self.hull = cachedData.hull
            self.cabin = cachedData.cabin
            self.masts = cachedData.masts
            self.sails = cachedData.sails
            self.cannons = cachedData.cannons
            self.wheel = cachedData.wheel
            self.bowsprit = cachedData.bowsprit
            self.fullsailSfx = cachedData.fullsailSfx
            self.rammingSfx = cachedData.rammingSfx
            self.sinkingSfx = cachedData.sinkingSfx
            self.lodRoot = cachedData.lodRoot
            self.lodRoot.reparentTo(self.modelGeom)
            self.highDetail = cachedData.highDetail
            self.mediumDetail = cachedData.medDetail
            self.lowDetail = cachedData.lowDetail
            self.highStatic = cachedData.highStatic
            self.mediumStatic = cachedData.medStatic
            self.lowStatic = cachedData.lowStatic
            self.modelCollisions = cachedData.modelCollisions
            self.modelCollisions.reparentTo(self.root)
            self.modelCollisions.hide()
            self.sailProjectors = cachedData.sailProjectors
            self.locators = cachedData.locators
            self.locators.reparentTo(self.root)
            for sailProjector in self.sailProjectors.itervalues():
                sailProjector.reparentTo(self.modelGeom)

            if self.hull:
                self.hull[0].uncache(self)
            if self.cabin:
                self.cabin[0].uncache(self)
            for mast in self.masts.values():
                mast[0].uncache(self)

            for mast in self.sails.values():
                for sail in mast.values():
                    sail[0].uncache(self)

            for entry in self.cannons.values():
                cannon = entry[0]
                cannon.uncache(self)

            if self.wheel:
                self.wheel[0].uncache(self)
            if self.bowsprit:
                self.bowsprit[0].uncache(self)
        self._actorNodeMgr = ActorNodeMgr(self.actorNode)
        DistributedMovingObject.generate(self)
        self.shipSunkEvent = self.uniqueName('shipSunk')

    def announceGenerate(self):
        self.miniLog = None
        self.node().getPhysicsObject().setPosition(self.getPos())
        self.node().getPhysicsObject().setLastPosition(self.getPos())
        self.node().getPhysicsObject().setVelocity(Vec3(0))
        self.mainBuiltEvent = self.uniqueName('ship-main-complete')
        self.fullBuiltEvent = self.uniqueName('ship-full-complete')
        self.acceptOnce(self.mainBuiltEvent, self.setMainPartsBuilt)
        self.acceptOnce(self.fullBuiltEvent, self.setBuildComplete)
        self.accept('far-ships', self.onlyShowFlat)
        self.accept('normal-ships', self.showNormalShip)
        self.accept('hide-ship-nametags', self.hideNametag)
        self.accept('show-ship-nametags', self.showNametag)
        self.accept('armor-change', self.adjustArmorDisplay)
        if self.cr.tutorial:
            self.setupBoardingSphere(bitmask=PiratesGlobals.WallBitmask | PiratesGlobals.SelectBitmask | PiratesGlobals.RadarShipBitmask)
        else:
            self.setupBoardingSphere()
        DistributedMovingObject.announceGenerate(self)
        self.setLodCollideMask(self.getLodCollideMask() | PiratesGlobals.ShipCollideBitmask)
        if not self.zoneSphere:
            self.setZoneRadii(self.sphereRadii)
        self.deckName = self.uniqueName('deck')
        self.railingName = self.uniqueName('railing')
        self.loadInterface()
        self.steeringSphereEvent = self.uniqueName('steeringSphere')
        self.steeringSphereEnterEvent = 'enter' + self.steeringSphereEvent
        self.exitWorldEvent = 'exitWorldBoundsSphere'
        self.createWake()
        self.enableFloors()
        self.showDebugName()
        self.setName(self.name)
        if self.initializeNametag3d():
            self.addActive()
        self.understandable = 1
        self.setPlayerType(NametagGroup.CCNormal)
        self.setFlagDNAString(self.getFlagDNAString())
        self.waterlineNode.setZ(ShipGlobals.WaterlineOffsets[self.modelClass])
        self._rocker.reset()
        self._rocker.setFakeMass(ShipGlobals.TiltFakeMass[self.modelClass])
        showSamplePoints = config.GetBool('show-ship-sample-points', False)
        self._sampleNPs = {}
        self._samplePoints = self.attachNewNode('samplePoints')
        if showSamplePoints:
            axis = loader.loadModel('models/misc/xyzAxis')
        gx, gy = ShipGlobals.SamplePointOffsets[self.modelClass][0]
        for sp in ShipGlobals.SamplePoints:
            np = self._samplePoints.attachNewNode(ShipGlobals.SamplePoints.getString(sp))
            np.setX(gx + ShipGlobals.SamplePointOffsets[self.modelClass][1][sp][0])
            np.setY(gy + ShipGlobals.SamplePointOffsets[self.modelClass][1][sp][1])
            self._sampleNPs[sp] = np
            if showSamplePoints:
                axis.instanceTo(np)

        self._maxSampleDistance = abs(self._sampleNPs[ShipGlobals.SamplePoints.C].getY() - self._sampleNPs[ShipGlobals.SamplePoints.F].getY())
        self.zoneSilhouette = self.cr.addInterest(self.getDoId(), PiratesGlobals.ShipZoneSilhouette, self.uniqueName('silhouette'), event=self.mainBuiltEvent)
        self.registerMainBuiltFunction(self.computeDimensions)
        self.registerMainBuiltFunction(self.loadFlat)
        self.registerBuildCompleteFunction(self.disableOnDeckInteractions)
        if __dev__ and base.config.GetBool('show-aggro-radius', 0):
            size = self.getAggroSphereSize()
            sphere = loader.loadModel('models/effects/explosion_sphere')
            sphere.reparentTo(self)
            sphere.setTransparency(1)
            sphere.setAlphaScale(0.3)
            sphere.setScale(render, size)
        currentState = self.gameFSM.getCurrentOrNextState()
        if currentState == 'Sunk' or currentState == 'Sinking':
            self.transNode.stash()
        else:
            self.transNode.unstash()
        self.disabledCollisionBits = {}
        if self.lastZoneLevel == 4 and self.flat:
            self.flat.unstash()
            self.root.stash()
        if base.showShipFlats:
            self.onlyShowFlat()
        else:
            self.showNormalShip()
        if base.hideShipNametags:
            self.hideNametag()
        else:
            self.showNametag()
        self.gameFSM.createGrappleProximitySphere()
        self.setupKrakenLocators()
        self.speedUpdate = FunctionCall(self.setBaseSpeedMod, ShipBalance.SpeedModifier)
        self.setupSmoothing()
        return

    def getAggroSphereSize(self):
        if base.localAvatar.ship:
            playerLevel = base.localAvatar.ship.getCrewLevel()
            enemyLevel = self.getLevel()
            levelDiff = max(1, abs(playerLevel - enemyLevel) - EnemyGlobals.AGGRO_RADIUS_LEVEL_BUFFER)
            aggroSphereRadius = max(EnemyGlobals.SHIP_SEARCH_RADIUS / max(1.0, levelDiff / EnemyGlobals.AGGRO_RADIUS_FALLOFF_RATE), EnemyGlobals.SHIP_MIN_SEARCH_RADIUS)
            return aggroSphereRadius
        else:
            return 1.0

    def _doSailAlpha(self):
        for d in self.sails.itervalues():
            for sail, distSail in d.itervalues():
                sail.sailGeom.setAlphaScale(0.4)

    def getModelGeomRoot(self):
        return self.modelGeom

    def getModelCollisionRoot(self):
        return self.modelCollisions

    def getInteractCollisionRoot(self):
        return self.interactionCollisions

    def getLocator(self, locatorName):
        return self.locators.find('**/%s;+s' % locatorName)

    def computeDimensions(self):
        debug = 0
        reset = __dev__ and debug
        if self.dimensionsComputed and not reset:
            return
        if reset:
            self.bow.removeNode()
            self.port.removeNode()
            self.starboard.removeNode()
            self.stern.removeNode()
            self.keel.removeNode()
            self.peak.removeNode()
            self.center.removeNode()
            self.hullCenter.removeNode()
        tb = self.root.getTightBounds()
        self.bow = self.transNode.attachNewNode('bowPos')
        self.port = self.transNode.attachNewNode('portPos')
        self.starboard = self.transNode.attachNewNode('starboardPos')
        self.stern = self.transNode.attachNewNode('sternPos')
        self.keel = self.transNode.attachNewNode('keel')
        self.peak = self.transNode.attachNewNode('peak')
        self.center = self.transNode.attachNewNode('center')
        self.hullCenter = self.transNode.attachNewNode('hullCenter')
        self.stern.setPos(Point3(0, tb[1][1], 0))
        self.bow.setPos(Point3(0, tb[0][1], 0))
        self.starboard.setPos(Point3(tb[1][0], 0, 0))
        self.port.setPos(Point3(tb[0][0], 0, 0))
        self.keel.setPos(Point3(0, 0, tb[0][2]))
        self.peak.setPos(Point3(0, 0, tb[1][2]))
        self.center.setPos((tb[0] + tb[1]) / 2.0)
        self.dimensions = tb[1] - tb[0]
        hb = self.hull[0].geom_High.getTightBounds()
        self.hullCenter.setPos((hb[0] + hb[1]) / 2.0)
        self.hullDimensions = hb[1] - hb[0]
        if debug:
            axis = loader.loadModel('models/misc/xyzAxis')
            axis.instanceTo(self.stern)
            axis.instanceTo(self.bow)
            axis.instanceTo(self.starboard)
            axis.instanceTo(self.port)
            axis.instanceTo(self.keel)
            axis.instanceTo(self.peak)
        self.dimensionsComputed = True

    def getFlagDNAString(self):
        if hasattr(self, 'flagDNAString'):
            return self.flagDNAString
        return

    def setFlagDNAString(self, dnaStr):
        if dnaStr:
            self.flagDNAString = dnaStr
            self.notify.debug('got dnaStr: ' + dnaStr)
            self.notify.debug('setting flag on ship')
            if self.hull:
                self.hull[0].setFlagDNAString(dnaStr)
        else:
            self.notify.debug('no flag on avatar')

    def getDimensions(self, other=None):
        return (
         VBase3(self.port.getX(other), self.bow.getY(other), self.keel.getZ(other)),
         VBase3(self.starboard.getX(other), self.stern.getY(other), self.peak.getZ(other)))

    def startDeployEffect(self, startT=0):
        if not self.fog:
            self.fog = ShipFog(parent=self.root, psbskp=(self.port.getX(), self.starboard.getX(), self.bow.getY(), self.stern.getY(), self.keel.getZ(), self.peak.getZ()), bin=self.ShipBin, binPriority=self.ShipBinPriority, camera=base.cam)
        if not self.fogIval:
            duration = 8
            fadeTime = 6
            self.fogIval = Sequence(Wait(5), Parallel(self.fog.getParticleInterval(duration=duration, fadeTime=fadeTime), Sequence(Func(self.setDeployHidden), LerpColorScaleInterval(self, fadeTime, Vec4(1), Vec4(0.001), blendType='easeIn'))), Func(self.clearDeployHidden), Func(messenger.send, 'deployEffectComplete-%d' % self.doId))
        self.fogIval.start(startT)

    def cleanupDeployEffect(self):
        if self.fogIval:
            self.fogIval.finish()
            self.fogIval = None
        if self.fog:
            self.fog.delete()
            self.fog = None
        return

    def disable(self):
        if hasattr(self, 'zoneSilhouette'):
            if self.zoneSilhouette is not None:
                self.cr.removeInterest(self.zoneSilhouette, self.uniqueName('silhouette'))
                self.zoneSilhouette = None
        self.clearLog()
        if self.flat:
            self.flat.removeNode()
            self.flat = None
        self.setZoneLevel(4)
        self.removeWake()
        taskMgr.remove(self.getReadySailsTaskName())
        taskMgr.remove('pvp-infamy-display')
        self.sailsReady = 1
        self.setClientController(0)
        if self.controlManager:
            self.controlManager.delete()
            self.controlManager = None
        if self.hull:
            self.hull[0].cleanupEffects()
        if self.cabin:
            self.cabin[0].cleanupEffects()
        if self.pendingClientSteer:
            self.cr.relatedObjectMgr.abortRequest(self.pendingClientSteer)
            self.pendingClientSteer = None
        if self.pendingBeginSteer:
            self.cr.relatedObjectMgr.abortRequest(self.pendingBeginSteer)
            self.pendingBeginSteer = None
        if self.pendingDoMovie:
            self.cr.relatedObjectMgr.abortRequest(self.pendingDoMovie)
            self.pendingDoMovie = None
        if self.pendingLandedGrapples:
            self.cr.relatedObjectMgr.abortRequest(self.pendingLandedGrapples)
            self.pendingLandedGrapples = None
        if self.isInCrew(localAvatar.doId) and not base.cr.noNewInterests():
            self.localAvatarExitShip()
        if self.stormEffect:
            self.stormEffect.destroy()
            self.stormEffect = None
        if self.windTunnelEffect1:
            self.windTunnelEffect1.finish()
            self.windTunnelEffect1 = None
        if self.windTunnelEffect2:
            self.windTunnelEffect2.finish()
            self.windTunnelEffect2 = None
        if self.windConeEffect:
            self.windConeEffect.stopLoop()
            self.windConeEffect = None
        if self.curAttackAnim != None:
            self.curAttackAnim.pause()
        if self.powerRechargeEffect:
            self.powerRechargeEffect.stopLoop()
            self.powerRechargeEffect = None
        if self.protectionEffect:
            self.protectionEffect.stopLoop()
            self.protectionEffect = None
        if self.takeCoverEffect:
            self.takeCoverEffect.stop()
            self.takeCoverEffect = None
        if self.openFireEffect:
            self.openFireEffect.stop()
            self.openFireEffect = None
        if self.broadside:
            if self.broadside[1]:
                self.broadside[1].setLocalAvatarUsingWeapon(0)
                self.broadside[1].av = None
        self.cleanupRammingCollisions()
        if hasattr(self, 'zoneOnDeck'):
            if self.zoneOnDeck is not None:
                self.cr.removeInterest(self.zoneOnDeck, self.uniqueName('onDeck'))
                self.zoneOnDeck = None
        if hasattr(self, 'zoneDetails'):
            if self.zoneDetails is not None:
                self.cr.removeInterest(self.zoneDetails, self.uniqueName('details'))
                self.zoneDetails = None
        if hasattr(self, 'zoneDistance'):
            if self.zoneDistance is not None:
                self.cr.removeInterest(self.zoneDistance, self.uniqueName('distance'))
                self.zoneDistance = None
        for currTextEffect in self.textEffects:
            if currTextEffect:
                currTextEffect.finish()

        self.textEffects = []
        if self.shoutTextEffect:
            self.shoutTextEffect.finish()
        self.stopAnimateLandedGrappleTask()
        if self.boardingPanel:
            self.boardingPanel.destroy()
            self.boardingPanel = None
        if self.fader:
            self.fader.pause()
        self.cleanupDeployEffect()
        self.removeActive()
        self.removeBoardingSphere()
        parentId, zoneId = self.getLocation()
        self.cleanupFloatTask()
        self.deleteZoneCollisions()
        self.stopShipRocking()
        self.stopAutoSailing()
        if self.sinkTrack:
            self.sinkTrack.finish()
            self.sinkTrack = None
            if self.getSiegeTeam():
                self._undoSinking()
        self.ignoreAll()
        for collModel in self.collModels:
            collModel.removeNode()

        DistributedMovingObject.disable(self)
        self.unloadInterface()
        self.steeringAvId = 0
        self.buildComplete = False
        self.buildCompleteFunctions = []
        self.mainPartsBuilt = False
        self.mainBuiltFunctions = []
        self.kraken = None
        self._actorNodeMgr.destroy()
        self._actorNodeMgr = None
        for currTextEffect in self.textEffects:
            if currTextEffect:
                currTextEffect.finish()

        self.textEffects = []
        self.speedUpdate.destroy()
        return

    def delete(self):
        self.deleteNametag3d()
        if self.iconNodePath:
            self.iconNodePath.removeNode()
            self.iconNodePath = None
        if self.fadeIval is not None:
            self.fadeIval.pause()
            self.fadeIval = None
        if self.lookAtDummy:
            self.lookAtDummy.removeNode()
            self.lookAtDummy = None
        self.wake = None
        self.windConeEffect = None
        self.curAttackAnim = None
        self.fader = None
        if self.hull:
            self.hull[0].cache()
        if self.cabin:
            self.cabin[0].cache()
        for mast in self.sails.values():
            for sail in mast.values():
                sail[0].cache()

        for mast in self.masts.values():
            mast[0].cache()

        for entry in self.cannons.values():
            cannon = entry[0]
            cannon.cache()

        if self.wheel:
            self.wheel[0].cache()
        if self.bowsprit:
            self.bowsprit[0].cache()
        self.setCachedData('DistributedShip', CachedShipData(self.optimized, self.broadside, self.hull, self.cabin, self.masts, self.sails, self.cannons, self.wheel, self.bowsprit, self.fullsailSfx, self.rammingSfx, self.sinkingSfx, self.lodRoot, self.highDetail, self.mediumDetail, self.lowDetail, self.highStatic, self.mediumStatic, self.lowStatic, self.modelCollisions, self.sailProjectors, self.locators))
        self.lodRoot.detachNode()
        self.lodRoot = None
        self.modelCollisions.detachNode()
        self.modelCollisions = None
        self.locators.detachNode()
        self.locators = None
        for sailProjector in self.sailProjectors.itervalues():
            sailProjector.detachNode()

        self.broadside = None
        self.hull = None
        self.cabin = None
        self.masts = {}
        self.sails = {}
        self.cannons = {}
        self.wheel = None
        self.bowsprit = None
        self.root.removeNode()
        self.transNode.removeNode()
        DistributedMovingObject.delete(self)
        ZoneLOD.ZoneLOD.delete(self)
        self.fullsailSfx = None
        self.rammingSfx = None
        self.sinkingSfx = None
        self.targets.destroy()
        self.targets = None
        self.destroy()
        return

    def requestGameState(self, state, *args):
        s = MiniLogSentry(self.miniLog, 'requestGameState', state, *args)
        self.gameFSM.request(state, *args)

    def queryGameState(self):
        return self.gameFSM.getCurrentOrNextState()

    def isSailable(self):
        return self.queryGameState() not in ('Sunk', 'Sinking', 'PutAway', 'Off')

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam=['want-shipboard-report', 'want-shipsink-report'])
    def setGameState(self, stateName, avId, timeStamp):
        if stateName == 'ClientSteering':
            s = MiniLogSentry(self.miniLog, 'setGameState', stateName, avId, timeStamp)
            self.requestGameState(stateName, avId)
        else:
            if stateName == 'AISteering':
                self.requestGameState(stateName, avId)
            else:
                self.requestGameState(stateName)

    def setUniqueId(self, uid):
        if self.uniqueId != '' and uid != self.uniqueId:
            base.cr.uidMgr.removeUid(self.uniqueId)
        self.uniqueId = uid
        base.cr.uidMgr.addUid(self.uniqueId, self.getDoId())

    def getUniqueId(self):
        return self.uniqueId

    def getWorld(self):
        return base.cr.activeWorld

    def getBoardingPosHpr(self):
        return self.localAvatarBoardingPosHpr

    def localAvatarInstantBoard(self):
        self._instantBoard = 1
        self.handleUseKey()

    def setBuildComplete(self):
        self.buildComplete = True
        self.optimizeShip()
        self.performBuildCompleteFunctions()

    def getBuildComplete(self):
        return self.buildComplete

    def registerBuildCompleteFunction(self, func, extraArgs=[], extraKwArgs={}):
        if self.buildComplete:
            func(*extraArgs, **extraKwArgs)
        else:
            self.buildCompleteFunctions.append([func, extraArgs, extraKwArgs])

    def performBuildCompleteFunctions(self):
        for func, args, kwargs in self.buildCompleteFunctions:
            func(*args, **kwargs)

        self.buildCompleteFunctions = []

    def setMainPartsBuilt(self):
        self.mainPartsBuilt = True
        self.performMainBuiltFunctions()

    def getMainPartsBuilt(self):
        return self.mainPartsBuilt

    def registerMainBuiltFunction(self, func, extraArgs=[], extraKwArgs={}):
        if self.mainPartsBuilt:
            func(*extraArgs, **extraKwArgs)
        else:
            self.mainBuiltFunctions.append([func, extraArgs, extraKwArgs])

    def performMainBuiltFunctions(self):
        for func, args, kwargs in self.mainBuiltFunctions:
            func(*args, **kwargs)

        self.mainBuiltFunctions = []

    def optimizeShip(self):
        if not self.hull or self.optimized:
            self.notify.warning('ship not in a state for optimizing (may allready be optimized)')
            return
        self.hull[0].cutState()
        sailStates = {}
        for mast in self.sails.values():
            for entry in mast.values():
                sail = entry[0]
                sailStates[entry[0]] = sail.sailFSM.state
                sail.setAnimState('Off')
                sail.setAnimState('Idle')
                sail.sailActor.fixBounds()
                sail.sailActor.getBounds()
                sail.cutState()

        if self.cabin:
            self.cabin[0].cutState()
        self.modelGeom.flattenStrong()
        self.modelGeom.getBounds()
        self.hull[0].pasteState()
        for entry in self.masts.values():
            mast = entry[0]
            if hasattr(mast.prop, 'postFlatten'):
                mast.prop.postFlatten()
                mast.setupMast()

        for mast in self.sails.values():
            for entry in mast.values():
                sail = entry[0]
                if hasattr(sail.sailActor, 'postFlatten'):
                    sail.sailActor.postFlatten()
                sail.pasteState()
                sail.setAnimState('Off')
                sail.setAnimState(sailStates[entry[0]])

        if self.cabin:
            self.cabin[0].pasteState()
        if self.broadside:
            for side in self.broadside[0]:
                for cannon in side:
                    if cannon:
                        cannon.prop.postFlatten()

        for entry in self.cannons.values():
            if entry[0]:
                entry[0].prop.postFlatten()

        for floor in self.modelCollisions.findAllMatches('**/*floors*') :
            floor.node().setIntoCollideMask(floor.node().getIntoCollideMask() | PiratesGlobals.TargetBitmask)
            floor.setTag('shipId', str(self.doId))

        self.optimized = True

    def setDeploy(self, deployState, timestamp):
        if deployState:

            def shipMainpartsArrived(doList=[]):
                elapsedTime = globalClockDelta.localElapsedTime(timestamp)
                self.startDeployEffect(elapsedTime)

            self.setDeployHidden()
            self.registerMainBuiltFunction(shipMainpartsArrived)
        else:
            self.cleanupDeployEffect()

    def setDeployHidden(self):
        self.setBin('fixed', self.ShipBin, self.ShipBinPriority)
        self.setColorScale(Vec4(1, 1, 1, 0.001))
        self.setTransparency(1)

    def clearDeployHidden(self):
        self.clearBin()
        self.clearColorScale()
        self.clearTransparency()

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-shipboard-report')
    def setMovie(self, mode, avId, fromShipId, instant, timestamp):
        self.notify.debug('setMovie %s, %s, %s, %s, %s' % (mode, avId, fromShipId, instant, timestamp))

        def doMovie(args):
            fromShip = None
            av = None
            if type(args) == list:
                if args[0] == None or args[1] == None:
                    return
                av, fromShip = args
            else:
                if args == None:
                    return
                av = args
            if timestamp is None:
                ts = 0.0
            else:
                ts = globalClockDelta.localElapsedTime(timestamp)
            currentState = av.gameFSM.getCurrentOrNextState()
            if currentState != 'ShipBoarding':
                boardMode = ShipGlobals.SHIP_BOARD_FROM_WALK
                if currentState == 'WaterRoam':
                    boardMode = ShipGlobals.SHIP_BOARD_FROM_SWIM
                av.gameFSM.request('ShipBoarding', [self, fromShip, boardMode, instant, ts])
            return

        if self.pendingDoMovie:
            self.cr.relatedObjectMgr.abortRequest(self.pendingDoMovie)
            self.pendingDoMovie = None
        if fromShipId != 0:
            self.pendingDoMovie = self.cr.relatedObjectMgr.requestObjects([avId, fromShipId], allCallback=doMovie, timeout=60)
        else:
            self.pendingDoMovie = self.cr.relatedObjectMgr.requestObjects([avId], eachCallback=doMovie, timeout=60)
        return

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='want-shipboard-report')
    def localAvatarBoardShip(self):
        if self.hull:
            self.hull[0].unstashPlaneCollisions()
        if base.config.GetBool('want-board-ram-ship', 0):
            self.setMainPartsBuilt()
            self.setBuildComplete()
        self.registerMainBuiltFunction(self.setupControls)
        if self.nametag:
            self.hideName()
        if self.gameFSM:
            self.gameFSM.startCurrentMusic()
        messenger.send('islandPlayerBarrier', [0])
        zoneId = PiratesGlobals.ShipZoneOnDeck
        localAvatar.setP(self.root.getP())
        localAvatar.setR(self.root.getR())
        localAvatar.ship = self
        if self.isFlagship:
            localAvatar.b_setTeleportFlag(PiratesGlobals.TFFlagshipBattle)
        if self.getBaseTeam() == PiratesGlobals.PLAYER_TEAM:
            self.enableOnDeckInteractions()
        self.oldZoom = base.localAvatar.guiMgr.radarGui.zoomFSM.state
        base.localAvatar.guiMgr.radarGui.zoomFSM.request('Zoom3')
        messenger.send(self.uniqueName('localAvBoardedShip'))
        self.setTargetBitmask(1)
        base.ambientMgr.requestFadeIn('ship-creak')

    def setTargetBitmask(self, bool):
        if not self.hull:
            return
        self.hull[0].setTargetBitmask(bool)
        for entry in self.masts.values():
            mast = entry[1]
            if mast:
                mast.prop.setTargetBitmask(bool)
            for index in self.sails.values():
                for entry in index.values():
                    sail = entry[0]
                    if sail:
                        sail.setTargetBitmask(bool)

        if self.cabin:
            self.cabin[0].setTargetBitmask(bool)
        if self.ram:
            self.ram[0].setTargetBitmask(bool)
        if self.bowsprit:
            self.bowsprit[0].setTargetBitmask(bool)
        for decorType in self.decors.values():
            for decor in decorType.values():
                if decor:
                    decor[0].setTargetBitmask(bool)

    @report(types=['frameCount', 'deltaStamp'], dConfigParam=['want-shipboard-report', 'want-shipsink-report'])
    def localAvatarExitShip(self, boardingFlagship=0):
        self.sendUpdate('leave', [self.getDoId()])
        if self.gameFSM:
            self.gameFSM.stopCurrentMusic()
        if self.nametag and not base.cr.tutorial:
            self.showName()
        self.hideStatusDisplay()
        if self.isFlagship:
            localAvatar.b_clearTeleportFlag(PiratesGlobals.TFFlagshipBattle)
        self.stashFloorCollisions()
        if self.hull:
            self.hull[0].stashPlaneCollisions()
        if self.isGenerated() and self.cr.activeWorld and self.cr.activeWorld.getType() == PiratesGlobals.INSTANCE_PVP and self.modelClass >= ShipGlobals.INTERCEPTORL1 and self.modelClass <= ShipGlobals.INTERCEPTORL4:
            mastCollisions = self.findAllMatches('**/*collision_mast*')
            for currColl in mastCollisions :
                currColl.unstash()

        if self.oldZoom:
            newZoom = self.oldZoom
        else:
            newZoom = 'Zoom1'
        base.localAvatar.guiMgr.radarGui.zoomFSM.request(newZoom)
        if self.hull:
            if self.hull[0].prop:
                self.setTargetBitmask(1)
        base.sfxPlayer.setCutoffDistance(120)
        base.ambientMgr.requestFadeOut('ship-creak')
        self.disableOnDeckInteractions()
        if self.controlManager:
            self.controlManager.delete()
            self.controlManager = None
        return

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='want-shipboard-report')
    def boardingInit(self, av, ship):
        self.notify.debug('%s boardingInit' % self.doId)
        if av.isLocal():
            self.unstashFloorCollisions()
            if self.cr and self.cr.activeWorld and self.cr.activeWorld.getWater():
                self.cr.activeWorld.getWater().hideWaterFloor()

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='want-shipboard-report')
    def boardingLeaveShip(self, av):
        self.notify.debug('%s boardingLeaveShip' % self.doId)
        if av.isLocal():
            self.localAvatarExitShip(1)

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='want-shipboard-report')
    def boardingFinish(self, av, pos, showMovie=True):
        if showMovie == False:
            base.transitions.fadeIn(1.0)
        self.notify.debug('%s boardingFinish' % self.doId)
        if av.isLocal():
            av.placeOnShip(self)
            self.boardingInProgress = 0
        if av.rope:
            av.rope.detachNode()
        if av.ropeEndNode:
            av.ropeEndNode.detachNode()
        av.wrtReparentTo(self.root)
        if av.isLocal():
            av.controlManager.currentControls.oneTimeCollide()
        if pos:
            av.setPos(pos)
        if av.isLocal():
            av.b_setGameState('LandRoam')

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='want-shipboard-report')
    def getRope(self, thickness=0.15):
        rope = Rope.Rope()
        rope.ropeNode.setRenderMode(RopeNode.RMTube)
        rope.ropeNode.setNumSlices(10)
        rope.ropeNode.setUvMode(RopeNode.UVDistance)
        rope.ropeNode.setUvDirection(1)
        rope.ropeNode.setUvScale(0.25)
        rope.ropeNode.setThickness(thickness)
        ropePile = loader.loadModel('models/char/rope_high')
        ropeTex = ropePile.findTexture('rope_single_omit')
        ropePile.removeNode()
        rope.setTexture(ropeTex)
        rope.setLightOff()
        rope.setColorScale(0.5, 0.5, 0.5, 1)
        return rope

    def setLandedGrapples(self, landedGrapples):

        def doGrapples(ship, landedGrapples=landedGrapples):
            for grapple in landedGrapples:
                if grapple not in self.landedGrapples:
                    self.createLandedGrapple(grapple[0], grapple[1])

            self.landedGrapples = landedGrapples
            self.startAnimateLandedGrappleTask()

        if len(landedGrapples) == 0:
            self.stopAnimateLandedGrappleTask()
            self.landedGrapples = landedGrapples
        else:
            if self.boardableShipId:
                if self.pendingLandedGrapples:
                    self.cr.relatedObjectMgr.abortRequest(self.pendingLandedGrapples)
                    self.pendingLandedGrapples = None
                self.pendingLandedGrapples = self.cr.relatedObjectMgr.requestObjects([self.boardableShipId], eachCallback=doGrapples, timeout=60)
        return

    def createLandedGrapple(self, shipId, targetId):
        if shipId:
            ship = self.cr.doId2do.get(shipId)
            if ship:
                shipRelX = ship.getX(self)
                grappleStr = '**/grapple_right*'
                anchorOffset = Vec3(0, 0, -1)
                if shipRelX < 0:
                    grappleStr = '**/grapple_left*'
                anchorNode = random.choice(self.locators.findAllMatches(grappleStr) )
                anchorPos = anchorNode.getPos(self.root) + anchorOffset
                targetRelX = self.getX(ship)
                targetStr = '**/grapple_right_'
                if targetRelX < 0:
                    targetStr = '**/grapple_left_'
                if targetId >= 0:
                    targetStr += str(targetId)
                    locator = ship.locators.find(targetStr)
                else:
                    locator = random.choice(ship.locators.findAllMatches(targetStr + '*') )
                rope = self.getRope(thickness=0.5)
                targetPos = locator.getPos(self.root)
                sagNode = self.root.attachNewNode('sagNode')
                sagPos = (targetPos + anchorPos) * 0.5
                sagPos.setZ(targetPos[2] - 2.0)
                sagNode.setPos(sagPos)
                grapple = loader.loadModel('models/ammunition/GrapplingHook')
                grapple.reparentTo(locator)
                hpr = (-270, -350, 80)
                pos = (2, 0, -2.5)
                if targetStr.find('right') > 0:
                    hpr = (90, -40, -180)
                    pos = (1, 0, -1.5)
                grapple.setHpr(*hpr)
                grapple.setPos(*pos)
                grapple.wrtReparentTo(ship.root)
                grapplePos = grapple.getPos(ship.root)
                rope.reparentTo(ship.root)
                rope.setup(3, ((None, grapplePos), (sagNode, Point3(0, 0, 0)), (self.root, anchorPos)))
                self.landedGrappleNodes.append([ship, grapple, anchorNode, sagNode, locator, rope])
                self.accept(ship.getDisableEvent(), self.stopAnimateLandedGrappleTask)
        return

    def removeLandedGrapples(self):
        for ship, grapple, anchorNode, sagNode, locator, rope in self.landedGrappleNodes:
            grapple.removeNode()
            sagNode.removeNode()
            rope.removeNode()
            del grapple
            del ship
            del anchorNode
            del sagNode
            del locator
            del rope

        self.landedGrappleNodes = []
        self.landedGrapples = []

    def startAnimateLandedGrappleTask(self):
        self.sagDist = 0
        taskMgr.add(self.animateLandedGrappleTask, self.uniqueName('animateGrapple'))

    def stopAnimateLandedGrappleTask(self):
        taskMgr.remove(self.uniqueName('animateGrapple'))
        self.removeLandedGrapples()

    def animateLandedGrappleTask(self, task):
        ship = None
        for ship, grapple, anchorNode, sagNode, locator, rope in self.landedGrappleNodes:
            targetPos = locator.getPos(self.root)
            anchorPos = anchorNode.getPos(self.root)
            sagPos = (targetPos + anchorPos) * 0.5
            if ship.queryGameState() != 'GrappleLerping':
                if self.sagDist < 20:
                    self.sagDist += 1
                sagPos.setZ(sagPos[2] - self.sagDist)
            sagNode.setPos(sagPos)

        return Task.cont

    def setSinkTimer(self, duration, timestamp):
        self.sinkTime = duration
        self.sinkTimestamp = timestamp
        dt = globalClockDelta.localElapsedTime(self.sinkTimestamp)
        if self.shipTargetPanel:
            if self.sinkTime > dt >= 0:
                self.shipTargetPanel.setTimer(self.sinkTime - dt)
                self.shipTargetPanel.timer.countdown(self.sinkTime - dt)
            else:
                self.shipTargetPanel.stopTimer()

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='want-shipboard-report')
    def clientSteeringBegin(self, avId):
        self.steeringAvId = avId
        av = self.cr.doId2do.get(self.steeringAvId)
        if not av:
            self.notify.warning('enterClientSteering: avId: %s not found' % self.steeringAvId)

            def reClientSteer(av):
                avId = av.doId
                self.clientSteeringBegin(avId)

            if self.pendingClientSteer:
                self.cr.relatedObjectMgr.abortRequest(self.pendingClientSteer)
                self.pendingClientSteer = None
            self.pendingClientSteer = self.cr.relatedObjectMgr.requestObjects([avId], eachCallback=reClientSteer)
            return
        if av.isLocal() and self.wheel:
            s = MiniLogSentry(self.miniLog, 'clientSteeringBegin', avId)
            self.calcModifiedStats()
            if self.broadside:
                if self.broadside[1]:
                    self.broadside[1].setLocalAvatarUsingWeapon(1)
                    self.broadside[1].av = av
            self.wheel[1].acceptInteraction()
            localAvatar.b_setGameState('ShipPilot', [self])
            self.accept(self.exitWorldEvent, self.handleOutOfRange)
            self.enableShipControls()
            self.setupRammingCollisions()
            collNPs = self.findAllMatches('**/+CollisionNode') 
            self.disabledCollisionBits = {}
            for np in collNPs:
                cMask = np.node().getIntoCollideMask()
                disabledBits = BitMask32()
                if not (cMask & PiratesGlobals.CameraBitmask).isZero():
                    cMask ^= PiratesGlobals.CameraBitmask
                    disabledBits |= PiratesGlobals.CameraBitmask
                if not (cMask & PiratesGlobals.FloorBitmask).isZero():
                    cMask ^= PiratesGlobals.FloorBitmask
                    disabledBits |= PiratesGlobals.FloorBitmask
                if not disabledBits.isZero():
                    np.node().setIntoCollideMask(cMask)
                    self.disabledCollisionBits[np] = disabledBits

            if self.broadside:
                if self.broadside[1]:
                    self.broadside[1].localPirate = 1
            self.checkAbleDropAnchor()
            self.accept('w', self.startAutoSailing)
            self.accept('arrow_up', self.startAutoSailing)
            av.stopSmooth()
        return

    @report(types=['frameCount', 'deltaStamp'], dConfigParam=['want-shipboard-report', 'want-shiksink-report'])
    def clientSteeringEnd(self):
        if not self.steeringAvId:
            return
        av = base.cr.doId2do.get(self.steeringAvId)
        if not av:
            self.notify.warning('avId: %s not found' % self.steeringAvId)
            return
        if av.isLocal():
            self.stopAutoSailing()
            if self.broadside:
                if self.broadside[1]:
                    self.broadside[1].setLocalAvatarUsingWeapon(0)
                    self.broadside[1].av = None
            self.ignore('escape')
            self.ignore(self.stopSteeringEvent)
            self.ignore(self.exitWorldEvent)
            taskMgr.remove(self.getReadySailsTaskName())
            self.sailsReady = 1
            self.cleanupRammingCollisions(stash=True)
            self.disableShipControls()
            localAvatar.cameraFSM.getOrbitCamera().setSubject(None)
            if self.shipStatusDisplay:
                self.shipStatusDisplay.disableAnchorButton()
            if localAvatar.getGameState() == 'ShipPilot':
                localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)
            for np, disabledBits in self.disabledCollisionBits.items():
                cMask = np.node().getIntoCollideMask()
                cMask |= disabledBits
                np.node().setIntoCollideMask(cMask)

            self.disabledCollisionBits = {}
            if self.broadside:
                if self.broadside[1]:
                    self.broadside[1].localPirate = 0
            av.wrtReparentTo(self.root)
            av.startSmooth()
            wheelpost = self.locators.find('**/location_wheel;+s')
            av.setPos(wheelpost.getPos(self.root) - Vec3(0.56, -3.0, 0))
        self.steeringAvId = 0
        self.ignore('arrow_up')
        self.ignore('w')
        return

    def canTakeWheel(self, wheel, av):
        return self.queryGameState() not in ('Pinned', 'Sinking', 'Sunk')

    def enableShipControls(self):
        base.cr.activeWorld.worldGrid.visAvatar = self
        localAvatar.controlManager.stop()
        if not self.controlManager:
            self.setupControls()
        self.controlManager.enable()
        self.controlManager.use('ship', self)
        self.controlManager.currentControls.enableAvatarControls()
        self.controlManager.setTag('avId', str(localAvatar.getDoId()))
        self.controlManager.setTag('shipId', str(self.getDoId()))
        localAvatar.stopListenAutoRun()
        localAvatar.cameraFSM.request('Orbit', self)
        localAvatar.cameraFSM.orbitCamera.pushParams()
        camParams = self.retrieveCamParams()
        if not camParams:
            camParams = ShipCameraParams.ShipModelClass2CameraParams[self.modelClass]
        camParams.applyTo(localAvatar.cameraFSM.orbitCamera)
        localAvatar.cameraFSM.orbitCamera.popToIdealDistance()
        base.localAvatar.guiMgr.combatTray.initCombatTray(InventoryType.SailingRep)
        base.localAvatar.guiMgr.combatTray.skillTray.updateSkillTray(rep=InventoryType.SailingRep, weaponMode=WeaponGlobals.SAILING)

    def disableShipControls(self):
        if localAvatar.cameraFSM.getOrbitCamera().getSubject():
            curParams = localAvatar.cameraFSM.orbitCamera.popParams()
            self.storeCamParams(curParams)
        else:
            self.notify.warning('disableShipControls: no orbitCam subject, cannot preserve ship camera settings')
        controls = self.controlManager.currentControls
        if controls:
            controls.disableAvatarControls()
        self.controlManager.disable()
        localAvatar.controlManager.enable()
        localAvatar.controlManager.use('walk', localAvatar)
        localAvatar.startListenAutoRun()
        base.cr.activeWorld.worldGrid.visAvatar = localAvatar
        base.localAvatar.guiMgr.combatTray.skillTray.hideSkillTray()
        base.localAvatar.guiMgr.combatTray.initCombatTray(localAvatar.currentWeaponId)

    def loadInterface(self):
        self.stopSteeringEvent = self.uniqueName('stopSteering')
        self.stopCannonEvent = self.uniqueName('stopCannon')

    def loadShipStatusDisplay(self):
        if self.shipStatusDisplay or base.cr.tutorial:
            return
        if base.config.GetBool('want-infamy', 0) and not self.renownDisplay:
            self.renownDisplay = PVPRankGui.PVPRankGui(parent=base.a2dBottomRight, displayType=PVPRankGui.SHIP_RENOWN_DISPLAY)
            self.renownDisplay.reparentTo(base.a2dBottomRight, sort=-1)
        self.shipStatusDisplay = ShipStatusDisplay(parent=base.a2dTopLeft, shipId=self.getDoId(), shipName=(self.name, self.getBaseTeam()), shipClass=self.shipClass, shipHp=(self.Hp, self.maxHp), shipSp=(self.Sp, self.maxSp), shipCargo=(self.cargo, self.maxCargo), shipCrew=(self.crew, self.maxCrew), ownShip=base.cr.hasOwnerViewDoId(self.getDoId()))
        self.adjustArmorDisplay()
        self.shipStatusDisplay.hide()
        if self.renownDisplay:
            self.renownDisplay.hide()
        self.refreshStatusTray()

    def loadShipTargetPanel(self):
        if self.shipTargetPanel or base.cr.tutorial:
            return
        self.loadShipStatusDisplay()
        self.shipTargetPanel = ShipTargetPanel.ShipTargetPanel(self)
        self.shipTargetPanel.hide()
        self.adjustArmorDisplay()

    def showStatusDisplay(self):
        self.loadShipStatusDisplay()
        self.isStatusDisplayVisible += 1
        self.__checkStatusDisplayVisible()

    def hideStatusDisplay(self):
        self.isStatusDisplayVisible = max(self.isStatusDisplayVisible - 1, 0)
        self.__checkStatusDisplayVisible()

    def __checkStatusDisplayVisible(self):
        if self.shipStatusDisplay:
            if self.isStatusDisplayVisible > 0:
                self.shipStatusDisplay.show()
                if self.getSiegeTeam() and self.renownDisplay:
                    self.renownDisplay.show()
            else:
                self.shipStatusDisplay.hide()
                if self.renownDisplay:
                    self.renownDisplay.hide()
                self.hideBoardingChoice()

    def showTargets(self):
        if self.targets:
            self.targets.show()

    def hideTargets(self):
        if self.targets:
            self.targets.hide()

    def unloadInterface(self):
        if self.target:
            self.target.destroy()
            self.target = None
        if self.shipTargetPanel:
            self.shipTargetPanel.destroy()
            self.shipTargetPanel = None
        if self.shipStatusDisplay:
            self.shipStatusDisplay.destroy()
            self.shipStatusDisplay = None
            self.ignore(self.uniqueName('ship-inventory-arrived'))
        if self.renownDisplay:
            self.renownDisplay.destroy()
            self.renownDisplay = None
        return

    def spawnInAnim(self, speed=1.0):
        self.root.setTransparency(1)
        self.root.setAlphaScale(0.0)
        if self.fadeIval is not None:
            self.fadeIval.finish()
        self.fadeIval = Sequence(Func(self.root.show), LerpFunctionInterval(self.root.setAlphaScale, fromData=0.0, toData=1.0, duration=speed), Func(self.root.clearTransparency))
        self.fadeIval.start()
        return

    def spawnOutAnim(self, speed=1.0):
        self.root.setTransparency(1)
        self.root.setAlphaScale(1.0)
        if self.fadeIval is not None:
            self.fadeIval.finish()
        self.fadeIval = Sequence(LerpFunctionInterval(self.root.setAlphaScale, fromData=1.0, toData=0.0, duration=speed), Func(self.root.hide), Func(self.root.clearTransparency))
        self.fadeIval.start()
        return

    def listenForFloorEvents(self, on):
        if on:
            self.accept('enterFloor' + self.deckName, self.__handleOnDeck)
            self.accept('exitFloor' + self.deckName, self.__handleOffDeck)
            self.accept('enterFloor' + self.railingName, self.__handleOnRailing)
            self.accept('exitFloor' + self.railingName, self.__handleOffRailing)
        else:
            if self.deckName != None:
                self.ignore('enterFloor' + self.deckName)
                self.ignore('exitFloor' + self.deckName)
            if self.railingName != None:
                self.ignore('enterFloor' + self.railingName)
                self.ignore('exitFloor' + self.railingName)
        return

    def __handleOnDeck(self, entry):
        base.ambientMgr.requestFadeIn('ship-creak')
        eventObject = entry.getIntoNodePath()
        objType = eventObject.getNetTag('objType')
        if not objType:
            return
        objType = int(objType)
        if entry.getIntoNode().getName() == self.deckName:
            floorType = entry.getIntoNodePath().getNetTag('floorType')
            if floorType:
                floorType = int(floorType)

    def __handleOffDeck(self, entry):
        base.ambientMgr.requestFadeOut('ship-creak')
        eventObject = entry.getIntoNodePath()
        objType = eventObject.getNetTag('objType')
        if not objType:
            return
        objType = int(objType)
        if entry.getIntoNode().getName() == self.deckName:
            floorType = entry.getIntoNodePath().getNetTag('floorType')
            if floorType:
                floorType = int(floorType)

    def __handleOnRailing(self, entry):
        base.ambientMgr.requestFadeIn('ship-creak')

    def __handleOffRailing(self, entry):
        base.ambientMgr.requestFadeOut('ship-creak')

    def __handleUnboardShip(self, collEntry):
        base.ambientMgr.requestFadeOut('ship-creak', 1)
        parent = base.localAvatar.getParent()
        if parent and parent.compareTo(self.root) == 0:
            self.localAvatarExitShip()

        parent.compareTo(self.root) == 0

    def enableFloors(self):
        self.listenForFloorEvents(1)

    def ignoreFloors(self):
        self.listenForFloorEvents(0)

    def enableWheelInteraction(self):
        if self.wheel:
            if self.wheel[1]:
                self.wheel[1].setAllowInteract(1)
                self.wheel[1].checkInUse()

    def disableWheelInteraction(self):
        if self.wheel:
            if self.wheel[1]:
                self.wheel[1].setAllowInteract(0, forceOff=True)
                self.wheel[1].refreshState()

    def enableOnDeckInteractions(self):
        self.notify.debug('enableOnDeckInteractions')
        for cannon in self.cannons.values():
            if cannon[1]:
                cannon[1].setAllowInteract(1)
                cannon[1].checkInUse()
                cannon[1].refreshState()

        if self.wheel:
            if self.wheel[1]:
                self.wheel[1].setAllowInteract(1)
                self.wheel[1].checkInUse()
                self.wheel[1].refreshState()

    def disableOnDeckInteractions(self):
        self.notify.debug('disableOnDeckInteractions')
        for cannon in self.cannons.values():
            if cannon[1]:
                cannon[1].setAllowInteract(0, forceOff=True)
                cannon[1].refreshState()

        if self.wheel:
            if self.wheel[1]:
                self.wheel[1].setAllowInteract(0, forceOff=True)
                self.wheel[1].refreshState()

    def stashFloorCollisions(self):
        return
        if self.hull:
            self.hull[0].stashFloorCollisions()
        if self.cabin:
            self.cabin[0].stashFloorCollisions()

    def unstashFloorCollisions(self):
        return
        if self.hull:
            self.hull[0].unstashFloorCollisions()
        if self.cabin:
            self.cabin[0].unstashFloorCollisions()

    def stashDetailCollisions(self):
        if self.hull:
            self.hull[0].stashDetailCollisions()
        if self.cabin:
            self.cabin[0].stashDetailCollisions()

    def unstashDetailCollisions(self):
        if self.hull:
            self.hull[0].unstashDetailCollisions()
        if self.cabin:
            self.cabin[0].unstashDetailCollisions()

    def stopSmoke(self):
        if self.hull:
            if self.hull[0]:
                self.hull[0].stopAllSmoke()
        if self.cabin:
            if self.cabin[0]:
                self.cabin[0].stopAllSmoke()

    def startSmoke(self):
        if self.hull and self.hull[1]:
            for i in range(len(self.hull[1].arrayHp)):
                if self.hull[1].arrayHp[i] <= 0 and self.hull[0]:
                    self.hull[0].startSmoke(i)

    def hideMasts(self):
        for entry in self.masts.values():
            mast = entry[1]
            if mast:
                if mast.prop:
                    mast.prop.hideMast(0)
                if mast.prop.propCollisions:
                    if not mast.prop.propCollisions.isEmpty():
                        mast.prop.propCollisions.hide()

    def showMasts(self):
        for entry in self.masts.values():
            mast = entry[1]
            if mast:
                if mast.prop:
                    for i in range(len(mast.prop.mastsState)):
                        if mast.prop.mastsState[i] == 0:
                            mast.prop.showMast(i)

                if mast.prop.propCollisions:
                    if not mast.prop.propCollisions.isEmpty():
                        mast.prop.propCollisions.show()

    def handleChildArrive(self, child, zoneId):
        DistributedMovingObject.handleChildArrive(self, child, zoneId)
        if isinstance(child, DistributedBattleAvatar.DistributedBattleAvatar):
            child.swapFloorCollideMask(PiratesGlobals.FloorBitmask, PiratesGlobals.ShipFloorBitmask)
            if not (child.isLocal() and self.boardingInProgress):
                child.wrtReparentTo(self.root)
            if child.isLocal():
                child.refreshActiveQuestStep()
                base.cr.activeWorld.worldGrid.startProcessVisibility(localAvatar)

    def handleChildLeave(self, child, zoneId):
        if isinstance(child, DistributedBattleAvatar.DistributedBattleAvatar):
            child.swapFloorCollideMask(PiratesGlobals.ShipFloorBitmask, PiratesGlobals.FloorBitmask)
            if child.isLocal():
                localAvatar.guiMgr.combatTray.skillTray.removePowerRechargeEffect()
                if self.sinkTrack:
                    self.sinkTrack.finish()
                    self.sinkTrack = None
        DistributedMovingObject.handleChildLeave(self, child, zoneId)
        return

    def setupBoardingSphere(self, bitmask=PiratesGlobals.RadarShipBitmask):
        self.removeBoardingSphere()
        tubeName = self.uniqueName('proximityCollision')
        result = self.createShipTube(tubeName, bitmask)
        self.interactTube = result[2]
        self.interactTube.setTag('objType', str(PiratesGlobals.COLL_AV))
        self.interactTube.setTag('avId', str(self.doId))
        sphereScale = ShipGlobals.getBoardingSphereScale(self.modelClass)
        spherePosH = ShipGlobals.getBoardingSpherePosH(self.modelClass)
        self.interactTube.setY(spherePosH[0][1])
        self.proximityCollisionEnterEvent = 'enter' + tubeName

    def forceTutorial(self, collEntry):
        self.sendUpdate('requestBoard', [localAvatar.doId])

    def removeBoardingSphere(self):
        if self.shellSphereNodePath:
            self.shellSphereNodePath.removeNode()
        if self.interactTube:
            self.interactTube.removeNode()

    def createShipTube(self, tubeName, bitmask, tangible=0):
        tubeSize = ShipGlobals.getBoardingSphereScale(self.modelClass)
        unboardTube = CollisionTube(0, -tubeSize, tubeSize * 0.4, 0, tubeSize, tubeSize * 0.4, tubeSize)
        unboardTube.setTangible(tangible)
        cSphereNode = CollisionNode(tubeName)
        cSphereNode.addSolid(unboardTube)
        unboardTubeNodePath = self.interactionCollisions.attachNewNode(cSphereNode)
        cSphereNode.setFromCollideMask(BitMask32.allOff())
        cSphereNode.setIntoCollideMask(bitmask)
        return [
         unboardTube, cSphereNode, unboardTubeNodePath]

    def cleanShipTube(self, tubeName, tube, tubeNodePath):
        if tubeNodePath:
            tubeNodePath.removeNode()
            del tubeNodePath
        if tube:
            del tube
        self.ignore('exit' + tubeName)

    def setupRammingCollisions(self):
        enterCollEvent = self.uniqueName('enterRammingEvent')
        exitCollEvent = self.uniqueName('exitRammingEvent')
        if not self.rammingSphereNodePath:
            x, y, z, s = ShipGlobals.getRammingSphereScale(self.modelClass)
            cSphere = CollisionSphere(x, y, z, s)
            cSphere.setTangible(0)
            rammingEvent = self.uniqueName('ShipRammingEvent')
            cSphereNode = CollisionNode(rammingEvent)
            cSphereNode.setFromCollideMask(PiratesGlobals.ShipCollideBitmask)
            cSphereNode.setIntoCollideMask(BitMask32.allOff())
            cSphereNode.addSolid(cSphere)
            self.rammingSphereNodePath = self.interactionCollisions.attachNewNode(cSphereNode)
            self.rammingSphereNodePath.stash()
            self.collHandler = CollisionHandlerEvent()
            self.collHandler.addInPattern(enterCollEvent)
            self.collHandler.addOutPattern(exitCollEvent)
            base.cTrav.addCollider(self.rammingSphereNodePath, self.collHandler)
        self.accept(enterCollEvent, self.enterShipEvent)
        self.accept(exitCollEvent, self.exitShipEvent)

    def cleanupRammingCollisions(self, stash=False):
        enterCollEvent = self.uniqueName('enterRammingEvent')
        exitCollEvent = self.uniqueName('exitRammingEvent')
        self.ignore(enterCollEvent)
        self.ignore(exitCollEvent)
        if not stash:
            if self.collHandler:
                base.cTrav.removeCollider(self.rammingSphereNodePath)
                self.collHandler = None
            if self.rammingSphereNodePath:
                self.rammingSphereNodePath.removeNode()
                self.rammingSphereNodePath = None
        return

    def isRamming(self):
        for buffKeyId in self.skillEffects.keys():
            buffId = self.skillEffects[buffKeyId][0]
            if WeaponGlobals.C_RAM == buffId:
                return True

        return False

    def enterShipEvent(self, entry):
        eventObject = entry.getIntoNodePath()
        objType = eventObject.getNetTag('objType')
        if not objType:
            return
        objType = int(objType)
        if objType == PiratesGlobals.COLL_SHIP and self.isRamming():
            targetId = int(eventObject.getNetTag('shipId'))
            pos = entry.getSurfacePoint(self)
            self.composeRequestShipRam(targetId, pos)

    def exitShipEvent(self, entry):
        eventObject = entry.getIntoNodePath()
        objType = eventObject.getNetTag('objType')
        if not objType:
            return
        objType = int(objType)
        if objType == PiratesGlobals.COLL_SHIP:
            pass

    def setupAggroCollisions(self):
        self.cAggro = CollisionSphere(0, 0, 0, self.getInstantAggroSphereSize())
        self.cAggro.setTangible(0)
        self.cAggroNode = CollisionNode(self.uniqueName('AggroSphere'))
        self.cAggroNode.setFromCollideMask(BitMask32.allOff())
        self.cAggroNode.setIntoCollideMask(PiratesGlobals.ShipCollideBitmask)
        self.cAggroNode.addSolid(self.cAggro)
        self.cAggroNodePath = self.attachNewNode(self.cAggroNode)
        if base.config.GetBool('show-aggro-radius', 0):
            self.cAggroNodePath.show()
        enterCollEvent = self.uniqueName('enter' + 'AggroSphere')
        self.accept(enterCollEvent, self._handleEnterAggroSphere)

    def cleanupAggroCollisions(self):
        if self.cAggroNodePath:
            base.cTrav.removeCollider(self.cAggroNodePath)
            self.cAggroNodePath.removeNode()
            self.cAggroNodePath = None
        if self.cAggroNode:
            self.cAggroNode = None
        if self.cAggro:
            self.cAggro = None
        return

    def _handleEnterAggroSphere(self, collEntry):
        if localAvatar.getSiegeTeam():
            return
        otherCollNode = collEntry.getFromNodePath()
        myCollNode = collEntry.getIntoNodePath()
        self.sendRequestClientAggro()

    def getInstantAggroSphereSize(self):
        return EnemyGlobals.SHIP_INSTANT_AGGRO_RADIUS

    def sendRequestClientAggro(self):
        self.sendUpdate('requestClientAggro', [])

    def setupFloatTask(self):
        if base.cr.activeWorld:
            self.startShipRocking(startOffset=random.uniform(0, 360))

    def cleanupFloatTask(self, water=None):
        self.stopShipRocking()

    def createWake(self):
        if not (base.cr.activeWorld and base.cr.activeWorld.getWater()):
            self.notify.warning('Ship %s is trying to create a wake without an ocean. (world: %s)' % (self.doId, base.cr.activeWorld))
            return
        if self.WantWake and base.cr.wantSpecialEffects:
            self.removeWake()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                if not hasattr(base.cr.activeWorld.getWater(), 'patch'):
                    self.notify.error("Ship %s is in location %s,%s (%s[%s]).\nThis causes Attribute Error: 'NoneType' object has no attribute 'patch'\n" % (self.doId, self.getLocation()[0], self.getLocation()[1], type(self.getParentObj()), safeRepr(self.getParentObj())))
                self.wake = Wake.getEffect()
                if self.wake:
                    self.wake.attachToShip(self)
                    compassFX = CompassEffect.make(render)
                    self.wake.setEffect(compassFX)
                    self.wake.startAnimate(self)

    def removeWake(self):
        if self.wake:
            self.wake.cleanUpEffect()
            self.wake = None
        return

    def getForwardVelocity(self):
        velocity = 0
        if hasattr(self, 'worldVelocity'):
            rotMat = Mat3.rotateMatNormaxis(self.getH(), Vec3.up())
            fwdVec = rotMat.xform(Vec3.forward())
            velocity = self.worldVelocity.dot(fwdVec)
            velocity += self.smoother.getSmoothForwardVelocity()
        return velocity

    def getRotationalVelocity(self):
        return self.currentTurning + self.smoother.getSmoothRotationalVelocity()

    def loadStats(self):
        if self.stats:
            return
        if not self.shipClass:
            return
        if self.getBaseTeam() == PiratesGlobals.INVALID_TEAM:
            return
        self.stats = ShipGlobals.getHullStats(self.shipClass)
        self.acceleration = self.stats['acceleration']
        self.maxSpeed = self.stats['maxSpeed']
        self.reverseAcceleration = self.stats['reverseAcceleration']
        self.maxReverseSpeed = self.stats['maxReverseSpeed']
        self.turnRate = self.stats['turn']
        self.maxTurn = self.stats['maxTurn']
        self.mass = self.stats['mass']
        self.waterIntakeDrag = self.stats['waterIntakeDrag']
        self.rammingPower = self.stats['rammingPower']
        self.baseAcceleration = self.acceleration
        self.acceleration *= self.baseSpeedMod
        self.baseMaxSpeed = self.maxSpeed
        self.maxSpeed *= self.baseSpeedMod
        self.baseReverseAcceleration = self.reverseAcceleration
        self.reverseAcceleration *= self.baseSpeedMod
        self.baseMaxReverseSpeed = self.maxReverseSpeed
        self.maxReverseSpeed *= self.baseSpeedMod
        self.baseTurnRate = self.turnRate
        self.turnRate *= self.baseSpeedMod
        self.baseMaxTurn = self.maxTurn
        self.maxTurn *= self.baseSpeedMod

    def loadZoneLevel(self, level):
        if level == 0:
            self.zoneOnDeck = self.cr.addInterest(self.getDoId(), PiratesGlobals.ShipZoneOnDeck, self.uniqueName('onDeck'))
        else:
            if level == 1:
                self.zoneDetails = self.cr.addInterest(self.getDoId(), PiratesGlobals.ShipZoneDetails, self.uniqueName('details'))
                self.setupFloatTask()
            else:
                if level == 2:
                    self.createWake()
                    self.zoneDistance = self.cr.addInterest(self.getDoId(), PiratesGlobals.ShipZoneDistance, self.uniqueName('distance'), event=self.fullBuiltEvent)
                    base.localAvatar.shipList.append(self.doId)
                else:
                    if level == 3:
                        if self.flat:
                            self.flat.stash()
                        currentState = self.gameFSM.getCurrentOrNextState()
                        if not currentState == 'Sunk':
                            if not currentState == 'Sinking':
                                self.root.unstash()
                            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                                if self.modelClass == ShipGlobals.SKEL_WARSHIPL3 or self.modelClass == ShipGlobals.SKEL_INTERCEPTORL3:
                                    if not self.stormEffect:
                                        self.stormEffect = self.isEmpty() or DarkMaelstrom(self)
                                        self.stormEffect.setZ(50)
                                        self.stormEffect.loop()
                                        compassFX = CompassEffect.make(render)
                                        self.stormEffect.setEffect(compassFX)
                    else:
                        if level == 4:
                            if self.flat:
                                self.flat.unstash()
                            self.root.stash()
        self._actorNodeMgr.loadZoneLevel(level)
        messenger.send('zoneLevelChange-%s' % self.getDoId(), [level])

    def unloadZoneLevel(self, level):
        if level == 0:
            if not self.zoneOnDeck:
                return
            self.cr.removeInterest(self.zoneOnDeck)
            self.zoneOnDeck = None
        else:
            if level == 1:
                if not self.zoneDetails:
                    return
                self.cr.removeInterest(self.zoneDetails)
                self.zoneDetails = None
                self.cleanupFloatTask()
            else:
                if level == 2:
                    self.removeWake()
                    if not self.zoneDistance:
                        return
                    self.cr.removeInterest(self.zoneDistance)
                    self.zoneDistance = None
                    if self.doId in base.localAvatar.shipList:
                        base.localAvatar.shipList.remove(self.doId)
                else:
                    if level == 3:
                        if self.flat:
                            self.flat.unstash()
                        self.root.stash()
                        if self.stormEffect:
                            self.stormEffect.destroy()
                            self.stormEffect = None
        self._actorNodeMgr.unloadZoneLevel(level)
        messenger.send('zoneLevelChange-%s' % self.getDoId(), [level])
        return

    def handleOutOfRange(self, entry):
        if self.redirectTrack:
            self.redirectTrack.pause()
            self.redirectTrack = None
        oldHpr = self.getHpr()
        self.lookAt(0, 0, 0)
        newHpr = self.getHpr()
        self.redirectTrack = Sequence(LerpHprInterval(self, 5, newHpr, startHpr=oldHpr))
        self.redirectTrack.start()
        return

    def autoAdjustPower(self, delta):
        for cannon in self.cannons.values():
            if not cannon[0].av:
                cannon[0].adjustPower(delta)

    def autoFireCannons(self, side):
        if self.broadside:
            if self.broadside[1]:
                target = self.autoAimBroadside(side)
                self.broadside[1].fireBroadside(side, target)

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker):
        if attacker:
            if isinstance(attacker, DistributedShip):
                attackShip = attacker
            else:
                if attacker.getShip():
                    attackShip = attacker.getShip()
                else:
                    return
            if self.isInCrew(localAvatar.doId):
                localAvatar.addShipTarget(attackShip, 1)
                localAvatar.guiMgr.radarGui.flashRadarObjectTimed(attackShip.doId)
            elif attackShip.isInCrew(localAvatar.doId):
                localAvatar.addShipTarget(self, 2)

    def damage(self, damage, pos, attackerId):
        if attackerId and localAvatar.doId == attackerId and damage != 0:
            self.showHpText(damage, pos=pos)
        offset = Vec3(*pos)
        offset.setZ(0.0)
        distance = offset.length()
        dot = offset.dot(Vec3.right())
        power = abs(damage) / 20.0
        if dot < 0.0:
            power = -power
        self.setRockTarget(power)

    def adjustArmorDisplay(self):
        if self.hull:
            left, rear, right = self.hull[1].getArmorStatus()
        else:
            left = rear = right = 1.0
        if self.shipStatusDisplay:
            self.shipStatusDisplay.setArmorStatus(ShipGlobals.ARMOR_LEFT, left)
            self.shipStatusDisplay.setArmorStatus(ShipGlobals.ARMOR_RIGHT, right)
            self.shipStatusDisplay.setArmorStatus(ShipGlobals.ARMOR_REAR, rear)
        if self.shipTargetPanel:
            self.shipTargetPanel.setArmorStatus(ShipGlobals.ARMOR_LEFT, left)
            self.shipTargetPanel.setArmorStatus(ShipGlobals.ARMOR_RIGHT, right)
            self.shipTargetPanel.setArmorStatus(ShipGlobals.ARMOR_REAR, rear)

    def startShipRocking(self, startOffset=0, wantRocking=1):
        if config.GetBool('use-old-ship-controls', 0):
            self.rockSpeedMult = 0.75
            self.currRockSpeed = self.rockSpeedMult
            self.currentTime = startOffset
            self.prevTime = random.uniform(0.0, 360.0)
            self.oceanRockTime = 0
            self.wantRocking = wantRocking
            taskMgr.add(self.shipRockingTask_old, self.uniqueName('shipRocking'), 24)
        else:
            taskMgr.add(self.shipRockingTask, self.uniqueName('shipRocking'), 24)

    def stopShipRocking(self):
        taskMgr.remove(self.uniqueName('shipRocking'))

    def shipRockingTask(self, task):
        self.transNode.setPosHpr(0, 0, 0, 0, 0, 0)
        frontBackPeriod = 25.55
        leftRightPeriod = 10.13
        upDownPeriod = 15.43
        elapsed = task.time
        fbTheta = elapsed / frontBackPeriod * 2.0 * math.pi
        lrTheta = elapsed / leftRightPeriod * 2.0 * math.pi
        udTheta = elapsed / upDownPeriod * 2.0 * math.pi
        avgWaveHeight = 0.0
        avgLRheight = [0.0, 0.0, 0.0]
        avgFBheight = [0.0, 0.0, 0.0]
        lrAngle = 0.0
        fbAngle = 0.0
        world, water = self.cr.getActiveWorld(), None
        if world:
            water = world.getWater()
        if water:
            for sp, node in self._sampleNPs.items():
                height = water.calcFilteredHeight(minWaveLength=3.0 * self._maxSampleDistance, node=node)
                avgWaveHeight += height
                lrIndex, fbIndex = DistributedShip.Sp2indices[sp]
                avgLRheight[lrIndex] += height
                avgFBheight[fbIndex] += height

            avgWaveHeight /= len(self._sampleNPs)
            fl = self._sampleNPs[ShipGlobals.SamplePoints.FL]
            lrDist = abs(fl.getX())
            fbDist = abs(fl.getY())
            a = (avgLRheight[0] - avgLRheight[-1]) / 3.0
            b = (avgLRheight[1] - avgLRheight[0]) / 3.0
            lrAvg = (a + b) / 2.0
            a = (avgFBheight[0] - avgFBheight[-1]) / 3.0
            b = (avgFBheight[1] - avgFBheight[0]) / 3.0
            fbAvg = (a + b) / 2.0
            lrAngle, fbAngle = self.debugFunc(lrAvg, fbAvg, lrDist, fbDist)
        maxSpd = 40.0
        velVec = self.actorNode.getPhysicsObject().getVelocity()
        speed = velVec.length()
        normSpeed = min(speed / maxSpd, 1.0)
        velVec.normalize()
        rotMat = Mat3.rotateMatNormaxis(self.getH(), Vec3.up())
        fwdVec = rotMat.xform(Vec3.forward())
        rightVec = rotMat.xform(Vec3.right())
        leanValue = -40.0 * clampScalar(velVec.dot(rightVec) * 2.0, -1.0, 1.0) * normSpeed
        tiltMult = lerp(0.9, 0.4, normSpeed)
        if not hasattr(base, 'localAvatar') or base.localAvatar.ship == self and self.steeringAvId != localAvatar.doId:
            tiltMult *= 0.1
        if self.kraken:
            rollAngle = self.kraken.getRollAngle()
            tiltMult *= 1 - self.kraken.getDampenAmount()
        else:
            rollAngle = self._rocker.getRollAngle()
        rollAngle += leanValue
        self.transNode.setP(tiltMult * (fbAngle + math.sin(fbTheta) * 0.5))
        self.transNode.setR(tiltMult * (lrAngle + math.sin(lrTheta) + rollAngle))
        self.transNode.setZ(avgWaveHeight + math.sin(udTheta) * 0.5)
        return Task.cont

    @exceptionLogged()
    def debugFunc(self, lrAvg, fbAvg, lrDist, fbDist):
        return (
         math.atan(lrAvg / lrDist) * 180.0 / math.pi, -math.atan(fbAvg / fbDist) * 180.0 / math.pi)

    def calcSmootherTurn(self):
        self.smoother.getSmoothRotationalVelocity()

    def addRoll(self, roll):
        self._rocker.addRoll(roll)

    def b_setRockTarget(self, power):
        self.setRockTarget(power)
        self.d_setRockTarget(power)

    def d_setRockTarget(self, power):
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.sendUpdate('d_setRockTarget', [power])

    def setRockTarget(self, power, timestamp=None):
        if timestamp == None:
            ts = 0.0
        else:
            ts = globalClockDelta.localElapsedTime(timestamp)
        self.addRoll(power)
        return

    def checkAbleDropAnchor(self):
        if localAvatar.doId == self.steeringAvId:
            if self.shipStatusDisplay:
                if localAvatar.getPort():
                    self.shipStatusDisplay.enableAnchorButton()
                else:
                    self.shipStatusDisplay.disableAnchorButton()

    def requestDropAnchor(self):
        self.sendUpdate('dropAnchor', [localAvatar.getPort()])

    def requestRepairAll(self):
        self.sendUpdate('purchaseRepairAll')

    def setIsFlagship(self, isFlagship):
        if isFlagship != self.isFlagship:
            self.isFlagship = isFlagship

    def canLocalAvatarBoardFlagship(self):
        boardableShip = self.getBoardableShip()
        if boardableShip and self.getIsInBoardingPosition():
            flagshipX = boardableShip.getX(self)
            avX = localAvatar.getX(self)
            if avX * flagshipX > 0:
                return True
        return False

    def setBoardableShipId(self, shipId):
        self.boardableShipId = shipId
        if self.isInCrew(localAvatar.getDoId()):
            self.notify.debug('ship %s is boardable' % shipId)

    def getBoardableShipId(self):
        return self.boardableShipId

    def getBoardableShip(self):
        if self.boardableShipId:
            boardableShip = self.cr.doId2do.get(self.boardableShipId)
            return boardableShip
        return

    def setBoardingSuccess(self, attackShipId, timestamp):
        self.notify.debug('%s setBoardingSuccess %s' % (self.doId, attackShipId))
        if attackShipId != self.boardableShipId:
            self.notify.warning('boardingSuccess: attackShipId != boardableShipId')
            return
        if timestamp is None:
            ts = 0.0
        else:
            ts = globalClockDelta.localElapsedTime(timestamp)
        if self.isInCrew(base.localAvatar.getDoId()):
            originalShip = self.getBoardableShip()
            if originalShip:
                self.swingLocalAvatarToGrappledShip(originalShip.doId)
        return

    def swingLocalAvatarToGrappledShip(self, grappledShipId):
        grappledShip = base.cr.doId2do.get(grappledShipId)
        if grappledShip:
            currentInteractive = base.cr.interactionMgr.getCurrentInteractive()
            if currentInteractive:
                currentInteractive.requestExit()
            if localAvatar.gameFSM.getCurrentOrNextState() == 'Battle':
                localAvatar.b_setGameState('LandRoam')
            grappledShip.boardingInProgress = 1
            grappledShip.sendUpdate('requestBoard', [localAvatar.getDoId()])

    def d_requestBoardFlagship(self, flagshipId):
        self.sendUpdate('requestBoardFlagship', [flagshipId])

    def getRopeAnchorNode(self, av, ropeEndNode):
        nearestDist = 99999999
        ropeAnchorNode = self.hull
        rightHand = av.rightHandNode
        for entry in self.masts.values():
            mast = entry[1]
            if mast:
                boom0 = mast.prop.locators.find('**/joint_anchor_net_0;+s')
                boom1 = mast.prop.locators.find('**/joint_anchor_net_1;+s')
                if not boom0.isEmpty():
                    dist0 = rightHand.getDistance(boom0)
                    if dist0 < nearestDist:
                        ropeAnchorNode = boom0
                        ropeEndNode.setPos(boom0.getPos(self))
                        nearestDist = dist0
                    if not boom1.isEmpty():
                        dist1 = rightHand.getDistance(boom1)
                        if dist1 < nearestDist:
                            ropeAnchorNode = boom1
                            ropeEndNode.setPos(boom1.getPos(self))
                            nearestDist = dist1

        if ropeAnchorNode == self.hull:
            ropeAnchorNode = self.attachNewNode('ropeAnchorNode')
            rhp = rightHand.getPos(self)
            ropeAnchorNode.setPos(rhp[0], rhp[1], rhp[2] + 130)
            ropeEndNode.setPos(rhp[0] - 100, rhp[1], rhp[2] + 130)
        return ropeAnchorNode

    def setBaseTeam(self, team):
        self.setTeam(team)
        self.teamName = ''
        messenger.send('setName-%s' % self.getDoId(), [self.name, self.getBaseTeam()])
        if self.isGenerated():
            self.showDebugName()
        self.loadStats()

    def getBaseTeam(self):
        return self.getTeam()

    def setBadge(self, titleId, rank):
        if titleId < 0 or rank < 0:
            self.badge = None
        else:
            self.badge = (
             titleId, rank)
        self.setName(self.name)
        return

    def setName(self, name):
        self.name = name
        badgeText = ''
        if self.badge and base.config.GetBool('want-titles-page', 0):
            badgeText = ' \x05badge-%s-%s\x05 ' % (self.badge[0], self.badge[1])
        messenger.send('setName-%s' % self.getDoId(), [self.name, self.getBaseTeam()])
        self.checkMakeNametag()
        if self.nametag:
            self.nametag.setName(name + badgeText)
            self.nametag.setDisplayName('        ')
        if self.nametag3d:
            if self.nameText:
                self.nameText['text'] = badgeText + name
            if self.classNameText:
                className = PLocalizer.ShipClassNames.get(self.modelClass)
                if self.getBaseTeam() != PiratesGlobals.PLAYER_TEAM:
                    self.classNameText['text'] = PLocalizer.Lv + str(self.level) + ' ' + className
                else:
                    self.classNameText['text'] = className

    def checkMakeNametag(self):
        if not self.shipClass:
            return
        if not self.name:
            return
        if not self.nametag:
            self.createNametag(self.name)
            return

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
        if not self.nametag:
            return
        self.nametag.getNametag3d().setContents(Nametag.CSpeech | Nametag.CThought)

    def showName(self):
        if not self.nametag:
            return
        if self.__nameVisible:
            self.nametag.getNametag3d().setContents(Nametag.CName | Nametag.CSpeech | Nametag.CThought)

    def hideNametag2d(self):
        if not self.nametag:
            return
        self.nametag2dContents = 0
        self.nametag.getNametag2d().setContents(self.nametag2dContents & self.nametag2dDist)

    def showNametag2d(self):
        if not self.nametag:
            return
        self.nametag2dContents = self.nametag2dNormalContents
        self.nametag2dContents = Nametag.CSpeech
        self.nametag.getNametag2d().setContents(self.nametag2dContents & self.nametag2dDist)

    def hideNametag3d(self):
        if self.nametag:
            self.nametag.getNametag3d().setContents(0)

    def showNametag3d(self):
        if not self.nametag:
            return
        if self.__nameVisible:
            self.nametag.getNametag3d().setContents(Nametag.CName | Nametag.CSpeech | Nametag.CThought)
        else:
            self.nametag.getNametag3d().setContents(0)

    def updatePickable(self):
        if self.isInCrew(base.localAvatar.doId):
            self.setPickable(0)
        else:
            self.setPickable(1)

    def setPickable(self, flag):
        if self.nametag:
            self.nametag.setActive(flag)

    def clickedNametag(self):
        pass

    def initializeNametag3d(self):
        if not self.nametag:
            return 0
        self.deleteNametag3d()
        nametagNode = self.nametag.getNametag3d().upcastToPandaNode()
        self.nametag3d.attachNewNode(nametagNode)
        self.nametag3d.setLightOff()
        self.iconNodePath = self.nametag.getNameIcon()
        if self.iconNodePath.isEmpty():
            self.notify.warning('empty iconNodePath in initializeNametag3d')
            return 0
        if self.nameText:
            self.nameText.reparentTo(self.iconNodePath)
        if self.classNameText:
            self.classNameText.reparentTo(self.iconNodePath)
        if self.isFlagship:
            modelPath = EnemyGlobals.getFlagshipIconModelPath(self.getBaseTeam())
            if modelPath:
                flagshipIcon = loader.loadModel(modelPath)
                flagshipIcon.setPos(0, 0, 2)
                flagshipIcon.setScale(1.5)
                flagshipIcon.reparentTo(self.iconNodePath)
                flagshipIcon.flattenLight()
        return 1

    def deleteNametag3d(self):
        if self.nametag3d:
            children = self.nametag3d.getChildren()
            for i in range(children.getNumPaths()):
                children[i].removeNode()

    def addActive(self):
        if base.wantNametags and self.nametag:
            self.nametag.manage(base.marginManager)
            self.accept(self.nametag.getUniqueId(), self.clickedNametag)

    def removeActive(self):
        if base.wantNametags and self.nametag:
            self.nametag.unmanage(base.marginManager)
            self.ignore(self.nametag.getUniqueId())

    def createNametag(self, name):
        if self.shipClass == ShipGlobals.STUMPY_SHIP:
            return
        self.__nameVisible = 1
        self.nametag = NametagGroup()
        self.nametag.setAvatar(self)
        self.nametag.setFont(PiratesGlobals.getPirateBoldOutlineFont())
        self.nametag2dContents = Nametag.CName
        self.nametag2dDist = Nametag.CName
        self.nametag2dNormalContents = Nametag.CName
        self.nametag3d = self.attachNewNode('nametag3d')
        self.nametag3d.setTag('cam', 'nametag')
        self.nametag3d.setFogOff()
        self.nametag3d.setLightOff()
        self.setNametagScale(12)
        name = PLocalizer.Lv + str(self.level) + ' ' + name
        self.nametag.setName(name)
        self.nametag.setNameWordwrap(PiratesGlobals.NAMETAG_WORDWRAP)
        OTPRender.renderReflection(False, self.nametag3d, 'p_ship_nametag', None)
        posAndScale = self.getDebugNamePosScale()
        self.nametag3d.setPos(0, 0, posAndScale[0][2])
        self.updatePickable()
        if self.pvpTeam:
            color = PVPGlobals.getTeamColor(self.pvpTeam)
        else:
            if self.getSiegeTeam():
                color = PVPGlobals.getSiegeColor(self.getSiegeTeam())
            else:
                color = EnemyGlobals.getShipNametagColor(self.getBaseTeam())
        self.nameText = OnscreenText(fg=color, bg=Vec4(0, 0, 0, 0), scale=0.95, align=TextNode.ACenter, mayChange=1, font=PiratesGlobals.getPirateBoldOutlineFont())
        self.nameText.setTransparency(TransparencyAttrib.MDual, 2)
        self.nameText.setColorScaleOff(100)
        self.nameText.setLightOff()
        self.nameText.setFogOff()
        self.classNameText = OnscreenText(pos=(0, -0.85), fg=Vec4(0.9, 0.9, 0.9, 1), bg=Vec4(0, 0, 0, 0), scale=0.6, align=TextNode.ACenter, mayChange=1, font=PiratesGlobals.getPirateBoldOutlineFont())
        self.classNameText.setTransparency(TransparencyAttrib.MDual, 2)
        self.classNameText.setColorScaleOff(100)
        self.classNameText.setLightOff()
        self.classNameText.setFogOff()
        siegeTeam = self.getSiegeTeam()
        if siegeTeam and base.config.GetBool('want-bountyicons', 0):
            for i in range(0, PVPGlobals.BountyRankLevels):
                icon = self.BountyIcon[siegeTeam - 1].copyTo(NodePath('bountyIcons'))
                icon.reparentTo(self.nameText)
                self.BountyIcons.append(icon)
                icon.setZ(1.3)
                icon.setScale(0.6)
                icon.hide()

        return

    def setGUIBounty(self, bounty):
        if not base.config.GetBool('want-bountyicons', 0):
            return
        bountyRank = 0
        for rank in PVPGlobals.BountyRanks:
            if bounty >= rank:
                bountyRank += 1

        for icon in self.BountyIcons:
            icon.hide()

        for i in range(0, bountyRank):
            icon = self.BountyIcons[i]
            icon.setX(i - (bountyRank - 1) / 2.0)
            icon.show()

    def getNametagScale(self):
        return self.nametagScale

    def setNametagScale(self, scale):
        self.nametagScale = scale
        if self.nametag3d:
            self.nametag3d.setScale(scale)

    def setPlayerType(self, playerType):
        self.playerType = playerType
        if self.nametag:
            self.nametag.setColorCode(self.playerType)

    def getInventory(self):
        return self.cr.doId2do.get(self.inventoryId)

    def setInventoryId(self, inventoryId):
        self.inventoryId = inventoryId

    def getInventoryId(self):
        return self.inventoryId

    def setShipClass(self, val):
        self.shipClass = val
        messenger.send('setShipClass-%s' % self.getDoId(), [self.shipClass])
        self.loadStats()
        self.checkMakeNametag()
        self.modelClass = ShipGlobals.getModelClass(val)
        filePrefix = self.getPrefix()
        if not self.locators:
            self.locators = loader.loadModel(filePrefix + '-locators')
            if self.locators:
                self.locators.reparentTo(self.root)
                self.locators.stash()

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='want-shipboard-report')
    def setCrew(self, crewArray):
        if self.crew != crewArray:
            messenger.send('setShipCrew-%s' % self.getDoId(), [
             crewArray, self.maxCrew])
        self.crew = crewArray
        self.updatePickable()

    def getCrew(self):
        return self.crew

    def setHp(self, Hp):
        self.deltaHp = Hp - self.Hp
        self.Hp = Hp
        messenger.send('setShipHp-%s' % self.getDoId(), [self.Hp, self.maxHp])
        if self.shipTargetPanel:
            self.shipTargetPanel.hpMeter['range'] = self.maxHp
            self.shipTargetPanel.hpMeter['value'] = self.Hp
        if self.Hp <= 0:
            if localAvatar.guiMgr and localAvatar.guiMgr.radarGui:
                localAvatar.guiMgr.radarGui.removeRadarObject(self.doId, force=True)
        else:
            self.transNode.unstash()
        if self.Hp == self.maxHp:
            if self.sinkTrack:
                self.sinkTrack.finish()
                self.sinkTrack = None
            self.root.unstash()
        return

    def getHp(self):
        return self.Hp

    def setMaxHp(self, Hp):
        self.maxHp = Hp

    def getMaxHp(self):
        return self.maxHp

    def setMaxCargo(self, maxCargo):
        if self.maxCargo != maxCargo:
            messenger.send('setShipCargo-%s' % self.getDoId(), [self.cargo, maxCargo])
        self.maxCargo = maxCargo

    def setCargo(self, cargo):
        self.cargo = cargo
        messenger.send('setShipCargo-%s' % self.getDoId(), [self.cargo, self.maxCargo])

    def setMaxCrew(self, val):
        self.maxCrew = val

    def getMaxCrew(self):
        return self.maxCrew

    def setSp(self, sp):
        self.deltaSp = sp - self.Sp
        self.Sp = sp
        messenger.send('setShipSp-%s' % self.getDoId(), [self.Sp, self.maxSp])
        self.calcModifiedStats()
        if self.shipTargetPanel:
            self.shipTargetPanel.speedMeter['range'] = self.maxSp
            self.shipTargetPanel.speedMeter['value'] = self.Sp

    def getSp(self):
        return self.Sp

    def setMaxSp(self, sp):
        self.maxSp = sp
        messenger.send('setShipSp-%s' % self.getDoId(), [self.Sp, self.maxSp])
        self.calcModifiedStats()

    def getMaxSp(self):
        return self.maxSp

    def setIsBoardable(self, val):
        self.isBoardable = val

    def getIsBoardable(self):
        return self.isBoardable

    def getNPCship(self):
        return False

    def setIsExitable(self, val):
        self.isExitable = val

    def getIsExitable(self):
        if base.config.GetBool('interact-check-exempt', 0):
            return True
        return self.isExitable

    def setIsInBoardingPosition(self, val):
        self.isInBoardingPosition = val

    def getIsInBoardingPosition(self):
        return self.isInBoardingPosition

    def notifyReceivedLoot(self, lootList):
        if self.getCrew().count(base.localAvatar.doId):
            base.localAvatar.guiMgr.messageStack.showLoot(lootList)

    def setHullCondition(self, condition):
        overhaulBit = 1 << 7
        self.isInOverhaul = bool(condition & overhaulBit)
        self.hullCondition = condition & ~overhaulBit

    def setBaseSpeedMod(self, mod):
        self.baseSpeedMod = mod
        self.maxSpeed = self.baseMaxSpeed * mod
        self.acceleration = self.baseAcceleration * mod
        self.reverseAcceleration = self.baseReverseAcceleration * mod
        self.maxReverseSpeed = self.baseMaxReverseSpeed * mod
        self.turnRate = self.baseTurnRate * mod
        self.maxTurn = self.baseMaxTurn * mod

    def setLockSails(self, val):
        self.lockedSails = val

    def b_setLocation(self, parentId, zoneId):
        if config.GetBool('watch-ship-parents', 1):
            parent = base.cr.getDo(parentId)
            try:
                if parent and parent.isGridParent() and not isinstance(parent, DistributedOceanGrid.DistributedOceanGrid):
                    raise HierarchyException(0, 'Ship being placed somewhere other than the ocean')
            except AttributeError:
                pass

        DistributedMovingObject.b_setLocation(self, parentId, zoneId)

    def setLocation(self, parentId, zoneId):
        if self.name == 'The Black Pearl':
            print '---------------setLocation %s %s-----------' % (parentId, zoneId)
        if self.parentId == parentId and self.zoneId == zoneId:
            return
        if hasattr(base, 'localAvatar'):
            if localAvatar.getDoId() == self.steeringAvId:
                gridObj = base.cr.doId2do.get(parentId)
                if gridObj:
                    pos = self.getPos(gridObj)
                    zone = gridObj.getZoneFromXYZ(pos)
                    currParentId, currZoneId = self.getLocation()
                    if parentId == currParentId and currZoneId == zoneId:
                        return
            DistributedMovingObject.setLocation(self, parentId, zoneId)

    def wrtReparentTo(self, parent):
        DistributedMovingObject.wrtReparentTo(self, parent)

    def stopSmooth(self):
        if self.smoothStarted:
            taskName = self.taskName('smooth')
            taskMgr.remove(taskName)
            self.smoothStarted = 0

    def getDebugNamePosScale(self):
        if self.modelClass == ShipGlobals.INTERCEPTORL1 or self.modelClass == ShipGlobals.MERCHANTL1 or self.modelClass == ShipGlobals.WARSHIPL1:
            return [(0, 0, 150), 50.0]
        else:
            if self.modelClass == ShipGlobals.INTERCEPTORL2 or self.modelClass == ShipGlobals.MERCHANTL2 or self.modelClass == ShipGlobals.WARSHIPL2 or self.modelClass == ShipGlobals.SKEL_INTERCEPTORL3:
                return [
                 (0, 0, 250), 100.0]
            else:
                if self.modelClass == ShipGlobals.INTERCEPTORL3 or self.modelClass == ShipGlobals.MERCHANTL3 or self.modelClass == ShipGlobals.WARSHIPL3 or self.modelClass == ShipGlobals.BLACK_PEARL or self.modelClass == ShipGlobals.SKEL_WARSHIPL3:
                    return [
                     (0, 0, 350), 125.0]
                else:
                    if self.modelClass == ShipGlobals.INTERCEPTORL4 or self.modelClass == ShipGlobals.MERCHANTL4 or self.modelClass == ShipGlobals.WARSHIPL4:
                        return [(0, 0, 450), 150.0]
                    else:
                        if self.modelClass == ShipGlobals.GOLIATH:
                            return [(0, 0, 450), 2.0]
                        else:
                            return [
                             (0, 0, 50), 2.0]

    def setupDebugCollisions(self):
        return
        if base.config.GetBool('process-movingObj-collisions', 1) is 0:
            return
        self.debugCSphere = CollisionSphere(0.0, 0.0, 0.0, ShipGlobals.AVOID_SPHERE_RADIUS)
        self.debugCSphere.setTangible(0)
        cSphereNode = CollisionNode(self.uniqueName('ShipSphere'))
        cSphereNode.addSolid(self.debugCSphere)
        self.debugCSphereNodePath = self.attachNewNode(cSphereNode)

    def cleanupDebugcollisions(self):
        return
        if base.config.GetBool('process-movingObj-collisions', 1) is 0:
            return
        if self.debugCSphereNodePath:
            self.debugCSphereNodePath.removeNode()
            del self.debugCSphereNodePath
            self.debugCSphereNodePath = None
        if self.debugCSphere:
            del self.debugCSphere
            self.debugCSphere = None
        return

    def getShipInfoId(self):
        return self.shipInfoId

    def setShipInfoId(self, shipInfoId):
        self.shipInfoId = shipInfoId

    def __repr__(self):
        return 'DistributedShip-%s' % self.doId

    def useShipSkill(self, skillId, ammoSkillId, skillResult, targetId, attackerEffects, targetEffects, timestamp, localSignal=0):
        effectId = WeaponGlobals.getSkillEffectFlag(skillId)
        newPriority = WeaponGlobals.getBuffPriority(effectId)
        newCategory = WeaponGlobals.getBuffCategory(effectId)
        if newPriority:
            for buffKeyId in self.skillEffects.keys():
                buffId = self.skillEffects[buffKeyId][0]
                priority = WeaponGlobals.getBuffPriority(buffId)
                category = WeaponGlobals.getBuffCategory(buffId)
                if newPriority < priority and category == newCategory:
                    return

        helmsman = self.cr.doId2do.get(self.steeringAvId)
        if helmsman:
            if helmsman.isNpc:
                return
            if not helmsman.isLocal() or localSignal:
                self.playSkillMovie(skillId, ammoSkillId)
            if helmsman.isLocal():
                if self.broadside:
                    if skillId == InventoryType.SailBroadsideRight:
                        self.autoFireCannons(1)
                    elif skillId == InventoryType.SailBroadsideLeft:
                        self.autoFireCannons(0)

    def playSkillMovie(self, skillId, ammoSkillId):
        skillInfo = WeaponGlobals.getSkillAnimInfo(skillId)
        anim = skillInfo[WeaponGlobals.PLAYABLE_INDEX]
        helmsman = self.cr.doId2do.get(self.steeringAvId)
        if helmsman:
            if helmsman.isNpc:
                return
        self.curAttackAnim = getattr(self.cr.combatAnims, anim)(helmsman, skillId, ammoSkillId)
        self.curAttackAnim.start()

    def getSkills(self, weaponId):
        if self.getInventory() is None:
            self.notify.warning('Inventory not created yet!')
            return {}
        return self.getInventory().getSkills(weaponId)

    def setSkillEffects(self, buffs):
        for entry in buffs:
            buffKeyId = '%s-%s' % (entry[0], entry[3])
            if buffKeyId not in self.skillEffects.keys():
                self.skillEffects[buffKeyId] = (
                 entry[0], entry[1], entry[2], entry[3])
                self.addStatusEffect(entry[0], entry[3])

        killList = []
        for buffKeyId in self.skillEffects.keys():
            foundEntry = 0
            for entry in buffs:
                id = '%s-%s' % (entry[0], entry[3])
                if buffKeyId == id:
                    foundEntry = 1

            if not foundEntry:
                killList.append((buffKeyId, self.skillEffects[buffKeyId][0], self.skillEffects[buffKeyId][3]))

        for buffKeyId, effectId, attackerId in killList:
            del self.skillEffects[buffKeyId]
            self.removeStatusEffect(effectId, attackerId)

        self.refreshStatusTray()

    def getSkillEffects(self):
        buffIds = []
        for buffKeyId in self.skillEffects.keys():
            buffId = self.skillEffects[buffKeyId][0]
            if buffId not in buffIds:
                buffIds.append(buffId)

        return buffIds

    def addStatusEffect(self, effectId, attackerId):
        if not self.mainPartsBuilt:
            self.registerMainBuiltFunction(self.addStatusEffect, extraArgs=[effectId, attackerId])
            return
        if effectId == WeaponGlobals.C_FULLSAIL:
            if self.isLocalCaptain():
                if self.queryGameState() != 'Docked':
                    if self.autoSailing:
                        self.b_animateSails('Billow', 6.0)
                    else:
                        self.startAutoSailing()
            if self.fullsailSfx:
                base.playSfx(self.fullsailSfx, node=self, cutoff=2000)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                if not self.windTunnelEffect1:
                    self.windTunnelEffect1 = Wind.getEffect()
                if self.windTunnelEffect1:
                    self.windTunnelEffect1.reparentTo(self.center)
                    self.windTunnelEffect1.fadeColor = Vec4(0.8, 0.8, 0.8, 0.5)
                    self.windTunnelEffect1.setScale(self.dimensions / 6.0)
                    self.windTunnelEffect1.fadeTime = 2.0
                    self.windTunnelEffect1.setH(180)
                    self.windTunnelEffect1.play()
        else:
            if effectId == WeaponGlobals.C_COMEABOUT:
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                    if not self.windTunnelEffect2:
                        self.windTunnelEffect2 = Wind.getEffect()
                    if self.windTunnelEffect2:
                        self.windTunnelEffect2.reparentTo(self.center)
                        self.windTunnelEffect2.fadeColor = Vec4(0.8, 0.8, 0.8, 0.4)
                        self.windTunnelEffect2.setScale(self.dimensions / 10.0)
                        self.windTunnelEffect2.fadeTime = 2.0
                        self.windTunnelEffect2.setH(0)
                        self.windTunnelEffect2.play()
            else:
                if effectId == WeaponGlobals.C_RAM:
                    if self.isLocalCaptain():
                        if self.queryGameState() != 'Docked':
                            if self.autoSailing:
                                self.b_animateSails('Billow', 8.0)
                            else:
                                self.startAutoSailing()
                    if self.rammingSfx:
                        base.playSfx(self.rammingSfx, node=self, cutoff=2000)
                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                        if not self.windConeEffect:
                            self.windConeEffect = WindBlurCone.getEffect()
                        if self.windConeEffect:
                            self.windConeEffect.reparentTo(self.bow)
                            self.windConeEffect.fadeColor = Vec4(0.8, 0.8, 0.8, 0.5)
                            self.windConeEffect.setScale(self.dimensions / 3.0)
                            self.windConeEffect.setPos(0, self.dimensions[1], self.hullDimensions[2])
                            self.windConeEffect.fadeTime = 2.0
                            self.windConeEffect.setH(180)
                            self.windConeEffect.startLoop()
                    if self.rammingSphereNodePath:
                        self.rammingSphereNodePath.unstash()
                else:
                    if effectId == WeaponGlobals.C_RECHARGE:
                        if self.isInCrew(localAvatar.doId):
                            localAvatar.guiMgr.combatTray.skillTray.addPowerRechargeEffect()
                            if localAvatar.cannon:
                                localAvatar.cannon.updateReloadBar()
                        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                            if not self.powerRechargeEffect:
                                self.powerRechargeEffect = ShipPowerRecharge.getEffect()
                            if self.powerRechargeEffect:
                                self.powerRechargeEffect.reparentTo(self.hullCenter)
                                self.powerRechargeEffect.setEffectColor(Vec4(0.5, 0.5, 1, 1))
                                self.powerRechargeEffect.setScale(self.dimensions / 4.0)
                                self.powerRechargeEffect.startLoop()
                    else:
                        if effectId == WeaponGlobals.C_SPAWN:
                            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                                self.protectionEffect = ProtectionDome.getEffect()
                                if self.protectionEffect:
                                    self.protectionEffect.reparentTo(self.waterlineNode)
                                    self.protectionEffect.setScale(self.dimensions[1] / 15.0)
                                    self.protectionEffect.startLoop()
                        else:
                            if effectId == WeaponGlobals.C_TAKECOVER:
                                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                                    if not self.takeCoverEffect:
                                        self.takeCoverEffect = FadingCard(loader.loadModel('models/textureCards/skillIcons').find('**/sail_take_cover'), color=Vec4(1, 1, 1, 1), fadeTime=0.01, waitTime=2.5, startScale=1.0, endScale=1.0)
                                    if self.takeCoverEffect:
                                        self.takeCoverEffect.reparentTo(self.waterlineNode)
                                        self.takeCoverEffect.setPos(0, 0, self.getDebugNamePosScale()[0][2] + 75)
                                        self.takeCoverEffect.setScale(50)
                                        self.takeCoverEffect.play()
                                        self.playTextEffect(PLocalizer.CrewBuffTakeCoverString)
                            else:
                                if effectId == WeaponGlobals.C_OPENFIRE:
                                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                                        if not self.openFireEffect:
                                            self.openFireEffect = FadingCard(loader.loadModel('models/textureCards/skillIcons').find('**/sail_openfire2'), color=Vec4(1, 1, 1, 1), fadeTime=0.01, waitTime=2.5, startScale=1.0, endScale=1.0)
                                        if self.openFireEffect:
                                            self.openFireEffect.reparentTo(self.waterlineNode)
                                            self.openFireEffect.setPos(0, 0, self.getDebugNamePosScale()[0][2] + 75)
                                            self.openFireEffect.setScale(50)
                                            self.openFireEffect.play()
                                            self.playTextEffect(PLocalizer.CrewBuffOpenFireString)
        self.calcModifiedStats()

    def playTextEffect(self, message):
        if self.shoutTextEffect:
            self.shoutTextEffect.finish()
            self.shoutTextEffect = None
        self.HpTextGenerator.setFont(PiratesGlobals.getPirateOutlineFont())
        duration = 4.0
        self.HpTextGenerator.setText(message)
        self.HpTextGenerator.clearShadow()
        self.HpTextGenerator.setAlign(TextNode.ACenter)
        color = Vec4(1, 1, 0, 1)
        hpTextDummy = self.attachNewNode('hpTextDummy')
        self.HpTextGenerator.setTextColor(color)
        textNode = self.HpTextGenerator.generate()
        hpText = hpTextDummy.attachNewNode(textNode)
        hpText.setScale(1.0)
        hpText.setBillboardPointEye(3.0)
        hpText.setBin('fixed', 100)
        hpText.setDepthWrite(0)
        hpText.setFogOff()
        hpText.setLightOff()
        hpText.setPos(0, 0, 2.0)
        OTPRender.renderReflection(False, hpText, 'p_text_effect', None)
        height = self.getDebugNamePosScale()[0][2]
        hpTextDummy.setPos(self, 0, 0, height - 13)
        hpTextDummy.headsUp(base.camera)
        hpTextDummy.setH(hpTextDummy.getH() + 180)
        tgtColor = Vec4(color[0], color[1], color[2], 0)
        scaleUp = hpTextDummy.scaleInterval(duration * 0.003, 20)
        fadeIn = hpTextDummy.colorScaleInterval(0.0, color, startColorScale=tgtColor)
        noFade = hpTextDummy.colorScaleInterval(0.5, color, startColorScale=color)
        fadeOut = hpTextDummy.colorScaleInterval(2.0, tgtColor, startColorScale=Vec4(color))
        trackParallel = Parallel(scaleUp, Sequence(fadeIn, noFade, fadeOut))
        self.shoutTextEffect = Sequence(trackParallel, Func(self.cleanupTextEffect, hpTextDummy))
        self.shoutTextEffect.start()
        return

    def cleanupTextEffect(self, hpTextDummy):
        if hpTextDummy:
            hpTextDummy.hide()
            hpTextDummy.removeNode()

    def invulnerable(self):
        return self.hasSpawnBuff()

    def hasSpawnBuff(self):
        return WeaponGlobals.C_SPAWN in self.getSkillEffects()

    def removeStatusEffect(self, effectId, attackerId):
        if self.findAllBuffCopyKeys(effectId):
            return
        if effectId == WeaponGlobals.C_RAM:
            if self.windConeEffect:
                self.windConeEffect.stopLoop()
            if self.rammingSphereNodePath:
                self.rammingSphereNodePath.stash()
        else:
            if effectId == WeaponGlobals.C_RECHARGE:
                if self.isInCrew(localAvatar.doId):
                    localAvatar.guiMgr.combatTray.skillTray.removePowerRechargeEffect()
                    if localAvatar.cannon:
                        localAvatar.cannon.updateReloadBar()
                if self.powerRechargeEffect:
                    self.powerRechargeEffect.stopLoop()
            else:
                if effectId == WeaponGlobals.C_SPAWN:
                    if self.protectionEffect:
                        self.protectionEffect.stopLoop()
                else:
                    if effectId == WeaponGlobals.C_TAKECOVER:
                        if self.takeCoverEffect:
                            self.takeCoverEffect.stop()
                    else:
                        if effectId == WeaponGlobals.C_OPENFIRE:
                            if self.openFireEffect:
                                self.openFireEffect.stop()
        slowDown = True
        for buffKeyId in self.skillEffects.keys():
            buffId = self.skillEffects[buffKeyId][0]
            if WeaponGlobals.C_FULLSAIL == buffId or WeaponGlobals.C_RAM == buffId:
                slowDown = False

        if self.isLocalCaptain() and self.autoSailing and slowDown:
            self.b_animateSails('Idle')
        self.calcModifiedStats()

    def findAllBuffCopyKeys(self, effectId):
        buffCopies = []
        for buffKeyId in self.skillEffects.keys():
            if self.skillEffects[buffKeyId][0] == effectId:
                buffCopies.append(buffKeyId)

        return buffCopies

    def startAutoSailing(self):
        if self.enableAutoSail:
            return
        if not self.sailsReady:
            return
        self.enableAutoSail = 1
        self.setIsAutoSailing(1)
        self.accept('arrow_down', self.stopAutoSailing)
        self.accept('s', self.stopAutoSailing)
        self.sailsReady = 0
        taskMgr.remove(self.getReadySailsTaskName())
        taskMgr.doMethodLater(self.SAIL_READY_DELAY, self.__readySails, self.getReadySailsTaskName())

    def stopAutoSailing(self):
        if not self.enableAutoSail:
            return
        if not self.sailsReady:
            return
        for buffId in self.getSkillEffects():
            if WeaponGlobals.C_RAM == buffId:
                return

        self.enableAutoSail = 0
        self.setIsAutoSailing(0)
        self.ignore('arrow_down')
        self.ignore('s')
        self.sailsReady = 0
        taskMgr.remove(self.getReadySailsTaskName())
        taskMgr.doMethodLater(self.SAIL_READY_DELAY, self.__readySails, self.getReadySailsTaskName())

    def toggleAutoSailing(self):
        if self.enableAutoSail:
            self.stopAutoSailing()
        else:
            self.startAutoSailing()

    def setIsAutoSailing(self, value):
        if self.lockedSails:
            return
        self.autoSailing = value
        if value:
            self.rolldownSails()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                localAvatar.enableCloudScudEffect()
        else:
            self.rollupSails()
            localAvatar.disableCloudScudEffect()

    def getIsAutoSailing(self):
        return self.autoSailing

    def refreshStatusTray(self):
        if self.shipStatusDisplay:
            self.shipStatusDisplay.updateStatusEffects(self.skillEffects)

    def calcModifiedStats(self):
        self.stats = None
        self.loadStats()
        passiveSkills = []
        for skillId in range(InventoryType.begin_SkillSailing, InventoryType.end_SkillSailing):
            if WeaponGlobals.getSkillTrack(skillId) == WeaponGlobals.PASSIVE_SKILL_INDEX:
                passiveSkills.append(skillId)

        helmsman = self.cr.doId2do.get(self.steeringAvId)
        if helmsman:
            if not helmsman.isNpc:
                inventory = helmsman.getInventory()
                if inventory:
                    for skillId in passiveSkills:
                        self.addPassiveSkill(skillId, inventory)

        speed = max(1, self.Sp)
        maxSpeed = max(1, self.maxSp)
        speedModifier = speed / maxSpeed * 0.25 + 0.75
        turnModifier = speed / maxSpeed * 0.25 + 0.75
        self.acceleration = self.baseAcceleration * self.baseSpeedMod * speedModifier
        self.maxSpeed = self.baseMaxSpeed * self.baseSpeedMod * speedModifier
        self.reverseAcceleration = self.baseReverseAcceleration * self.baseSpeedMod * speedModifier
        self.maxReverseSpeed = self.baseMaxReverseSpeed * self.baseSpeedMod * speedModifier
        self.turnRate = self.baseTurnRate * self.baseSpeedMod * turnModifier
        self.maxTurn = self.baseMaxTurn * self.baseSpeedMod * turnModifier
        for buffKeyId in self.skillEffects:
            buffId = self.skillEffects[buffKeyId][0]
            if WeaponGlobals.C_RAM == buffId:
                self.acceleration += ShipGlobals.defaultAcceleration * 1.0
                self.maxSpeed += ShipGlobals.defaultMaxSpeed * 1.0
                self.turnRate = 0.0
                self.maxTurn = 0.0
            elif WeaponGlobals.C_COMEABOUT == buffId:
                self.turnRate += ShipGlobals.defaultTurn * 0.35
                self.maxTurn += ShipGlobals.defaultMaxTurn * 0.35
            elif WeaponGlobals.C_FULLSAIL == buffId:
                self.acceleration += ShipGlobals.defaultAcceleration * 0.5
                self.maxSpeed += ShipGlobals.defaultMaxSpeed * 0.5

        return

    def addPassiveSkill(self, skillId, inventory):
        skillLvl = max(0, inventory.getStackQuantity(skillId) - 1)
        effects = WeaponGlobals.getShipEffects(skillId)
        if effects != [0, 0, 0, 0, 0, 0]:
            self.acceleration += self.baseAcceleration * effects[0] * skillLvl
            self.maxSpeed += self.baseMaxSpeed * effects[1] * skillLvl
            self.reverseAcceleration += self.baseReverseAcceleration * effects[2] * skillLvl
            self.maxReverseSpeed += self.baseMaxReverseSpeed * effects[3] * skillLvl
            self.turnRate += self.baseTurnRate * effects[4] * skillLvl
            self.maxTurn += self.baseMaxTurn * effects[5] * skillLvl

    def setLevel(self, level):
        self.level = level

    def getLevel(self):
        return self.level

    def getCrewLevel(self):
        captainWeight = 2
        crewLevel = 0
        for playerId in self.getCrew():
            player = self.cr.doId2do.get(playerId)
            if player:
                playerLevel = player.getLevel()
                if player.doId == self.getCaptainId():
                    playerLevel *= captainWeight
                crewLevel += playerLevel

        crewLevel = int(crewLevel / (len(self.getCrew()) + captainWeight - 1))
        return crewLevel

    def composeRequestShipRam(self, targetId, pos):
        target = self.cr.doId2do.get(targetId)
        if not target:
            return
        if not TeamUtils.damageAllowed(target, self):
            localAvatar.guiMgr.createWarning(PLocalizer.FriendlyFireWarning, PiratesGuiGlobals.TextFG6)
            return
        for buffKeyId in self.skillEffects.keys():
            buffId = self.skillEffects[buffKeyId][0]
            if WeaponGlobals.C_RAM == buffId:
                self.sendRequestShipRam(targetId, pos)
                deleteMe = []
                for buffKeyId in self.skillEffects:
                    buffId = self.skillEffects[buffKeyId][0]
                    attackerId = self.skillEffects[buffKeyId][3]
                    if buffId == WeaponGlobals.C_RAM:
                        deleteMe.append((buffKeyId, buffId, attackerId))

                for buffKeyId, buffId, attackerId in deleteMe:
                    del self.skillEffects[buffKeyId]
                    self.removeStatusEffect(buffId, attackerId)

                self.refreshStatusTray()

        self.addShipTarget(target, 2)
        if self.isInCrew(base.localAvatar.doId):
            cameraShakerEffect = CameraShaker()
            cameraShakerEffect.wrtReparentTo(self)
            cameraShakerEffect.setPos(self, 0, 0, 0)
            cameraShakerEffect.shakeSpeed = 0.08
            cameraShakerEffect.shakePower = 2.0
            cameraShakerEffect.numShakes = 4
            cameraShakerEffect.scalePower = 1
            cameraShakerEffect.play(500.0)

    def sendRequestShipRam(self, targetId, pos):
        timestamp32 = globalClockDelta.getFrameNetworkTime(bits=32)
        self.sendUpdate('requestShipRam', [targetId, [pos[0], pos[1], pos[2]], timestamp32])

    def useShipRam(self, pos):
        power = 1000
        if pos != [0, 0, 0]:
            pos = Vec3(pos[0], pos[1], pos[2])
            pos.setZ(0.0)
            distance = pos.length()
            dot = pos.dot(Vec3.right())
            if dot < 0.0:
                power = -power
        else:
            x, y, z, s = ShipGlobals.getRammingSphereScale(self.modelClass)
            pos = Vec3(x, y, z)
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
            shipSplintersAEffect = ShipSplintersA.getEffect()
            if shipSplintersAEffect:
                shipSplintersAEffect.reparentTo(self)
                shipSplintersAEffect.setPos(self, pos)
                shipSplintersAEffect.play()
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            smokeCloudEffect = SmokeCloud.getEffect()
            if smokeCloudEffect:
                smokeCloudEffect.wrtReparentTo(self)
                smokeCloudEffect.setPos(self, pos)
                smokeCloudEffect.setScale(3.0)
                smokeCloudEffect.spriteScale = 4.0
                smokeCloudEffect.radius = 10.0
                smokeCloudEffect.play()
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
            shockwaveRingEffect = ShockwaveHit.getEffect()
            if shockwaveRingEffect:
                shockwaveRingEffect.wrtReparentTo(self)
                shockwaveRingEffect.setPos(self, pos)
                shockwaveRingEffect.size = 200
                shockwaveRingEffect.play()
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            if self.isInCrew(base.localAvatar.doId):
                cameraShakerEffect = CameraShaker()
                cameraShakerEffect.wrtReparentTo(self)
                cameraShakerEffect.setPos(self, pos)
                cameraShakerEffect.shakeSpeed = 0.08
                cameraShakerEffect.shakePower = 2.0
                cameraShakerEffect.numShakes = 4
                cameraShakerEffect.scalePower = 1
                cameraShakerEffect.play(500.0)
        self.setRockTarget(power)
        soundFx = random.choice(getRamSfx())
        base.playSfx(soundFx, node=self, cutoff=2500)

    def printExpText(self, totalExp, colorSetting, basicPenalty, crewBonus, doubleXPbonus, holidayBonus):
        taskMgr.doMethodLater(0.5, self.showHpText, self.taskName('printExp'), [
         totalExp, colorSetting, 6.0, 1.0, 0, basicPenalty, crewBonus, doubleXPbonus, holidayBonus])

    def showHpText(self, number, bonus=0, duration=2.0, scale=1.0, pos=None, basicPenalty=0, crewBonus=0, doubleXPBonus=0, holidayBonus=0):
        if self.isEmpty():
            return
        distance = camera.getDistance(self)
        scale *= max(1.0, distance / 25.0)
        posAndScale = self.getDebugNamePosScale()
        height = posAndScale[0][2]
        startPos = (0, 0, height / 4)
        destPos = (0, 0, height / 2)
        if pos:
            startPos = pos
            destPos = (pos[0], pos[1], pos[2] + height / 4)
        newEffect = None

        def cleanup():
            if newEffect in self.textEffects:
                self.textEffects.remove(newEffect)

        mods = {}
        if basicPenalty > 0:
            mods[TextEffect.MOD_BASICPENALTY] = basicPenalty
        if crewBonus > 0:
            mods[TextEffect.MOD_CREWBONUS] = crewBonus
        if doubleXPBonus > 0:
            mods[TextEffect.MOD_2XPBONUS] = doubleXPBonus
        if holidayBonus > 0:
            mods[TextEffect.MOD_HOLIDAYBONUS] = holidayBonus
        effect = TextEffect.genTextEffect(self, self.HpTextGenerator, number, bonus, self.isNpc, Functor(self.removeEffect, newEffect), startPos, destPos, scale, modifiers=mods)
        if effect:
            self.textEffects.append(effect)
        return

    def removeEffect(self, effect):
        if effect in self.textEffects:
            self.textEffects.remove(effect)

    def enablePhysics(self):
        pass

    def disablePhysics(self):
        pass

    def setupControls(self):
        if not self.controlManager:
            self.controlManager = ControlManager.ControlManager(enable=False)
            controls = ShipPilot()
            controls.initializeCollisions(base.cTrav, self.transNode, self.bow, self.stern, self.starboard, self.port)
            wallBitMask = PiratesGlobals.ShipCollideBitmask | PiratesGlobals.GoldBitmask
            if self.respectDeployBarriers:
                wallBitMask |= PiratesGlobals.ShipDeployBitmask
            controls.setWallBitMask(wallBitMask)
            controls.setFloorBitMask(BitMask32().allOff())
            self.controlManager.add(controls, 'ship')

    def getReadySailsTaskName(self):
        return 'readySails-%s' % self.doId

    def __readySails(self, args=None):
        self.sailsReady = 1

    def rollupSails(self):
        if not self.sailsDown:
            return
        currentState = self.gameFSM.getCurrentOrNextState()
        if currentState == 'Sunk' or currentState == 'Sinking':
            return
        self.sailsDown = 0
        self.b_animateSails('Rollup')

    def rolldownSails(self):
        if self.sailsDown:
            return
        self.sailsDown = 1
        self.b_animateSails('Rolldown')

    def animateSails(self, anim, rate=1.0):
        for mast in self.sails.values():
            for sail in mast.values():
                if sail[1]:
                    sail[0].setAnimState(anim)

    def b_animateSails(self, anim, rate=1.0):
        for mast in self.sails.values():
            for sail in mast.values():
                if sail[1]:
                    sail[1].b_setAnimState(anim)

    def tiedupSails(self):
        self.animateSails('TiedUp')

    def autoAimBroadside(self, side):
        targetList = {}
        for shipId in base.localAvatar.shipList:
            ship = self.cr.doId2do.get(shipId)
            if ship:
                if shipId != self.doId and ship.getHp() > 0:
                    if TeamUtils.damageAllowed(ship, self):
                        dist = self.checkBroadsideAlignment(ship, side)
                        if dist:
                            targetList[dist] = shipId

        if targetList:
            keys = targetList.keys()
            keys.sort()
            return targetList[keys[0]]
        return 0

    def checkBroadsideAlignment(self, target, side):
        if self.lookAtDummy == None:
            return 0
        if not target:
            return 0
        distToTgt = self.getDistance(target)
        if target.bow and target.stern:
            self.lookAtDummy.lookAt(target.bow)
            targetHeading = self.lookAtDummy.getH(self.transNode)
            if distToTgt < ShipGlobals.BROADSIDE_MAX_AUTOAIM_DIST:
                if targetHeading > 65 and targetHeading < 115 and side == 1:
                    return distToTgt
                elif targetHeading < -65 and targetHeading > -115 and side == 0:
                    return distToTgt
            self.lookAtDummy.lookAt(target.stern)
            targetHeading = self.lookAtDummy.getH(self.transNode)
            if distToTgt < ShipGlobals.BROADSIDE_MAX_AUTOAIM_DIST:
                if targetHeading > 65 and targetHeading < 115 and side == 1:
                    return distToTgt
                elif targetHeading < -65 and targetHeading > -115 and side == 0:
                    return distToTgt
        else:
            self.lookAtDummy.lookAt(target)
            targetHeading = self.lookAtDummy.getH(self.transNode)
            if distToTgt < ShipGlobals.BROADSIDE_MAX_AUTOAIM_DIST:
                if targetHeading > 65 and targetHeading < 115 and side == 1:
                    return distToTgt
                elif targetHeading < -65 and targetHeading > -115 and side == 0:
                    return distToTgt
        return 0

    def setRepairCount(self, val):
        self.repairCount = val

    def getRepairCount(self):
        return self.repairCount

    def setCaptainId(self, val):
        self.captainId = val

    def getCaptainId(self):
        return self.captainId

    def isInCrew(self, avId):
        return avId in self.getCrew()

    def isCaptain(self, avId):
        return avId == self.captainId

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='want-shipboard-report')
    def getRandomBoardingPos(self):
        allBoardingSpots = self.locators.findAllMatches('**/boarding_spot_*;+s') 
        if not allBoardingSpots:
            return
        return random.choice(allBoardingSpots).getPos()

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='want-shipboard-report')
    def getClosestBoardingPos(self):
        allBoardingSpots = self.locators.findAllMatches('**/boarding_spot_*;+s') 
        if not allBoardingSpots:
            return
        closestBoardingSpot = allBoardingSpots[0]
        for locator in allBoardingSpots:
            dist = locator.getDistance(base.localAvatar)
            currentClosestDist = closestBoardingSpot.getDistance(base.localAvatar)
            if dist < currentClosestDist:
                closestBoardingSpot = locator

        return closestBoardingSpot.getPos() + Vec3(1, 0, 0)

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='want-shipboard-report')
    def getClosestBoardingPosH(self):
        allBoardingSpots = self.locators.findAllMatches('**/boarding_spot_*;+s') 
        if not allBoardingSpots:
            return
        closestBoardingSpot = allBoardingSpots[0]
        for locator in allBoardingSpots:
            dist = locator.getDistance(base.localAvatar)
            currentClosestDist = closestBoardingSpot.getDistance(base.localAvatar)
            if dist < currentClosestDist:
                closestBoardingSpot = locator

        return (
         closestBoardingSpot.getPos() + Vec3(1, 0, 0), closestBoardingSpot.getH() + 180)

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam=['want-shipdeploy-report', 'want-shipboard-report'])
    def setRespectDeployBarriers(self, respect, barrierId):
        self.respectDeployBarriers = respect
        if not self.controlManager:
            return
        controls = self.controlManager.get('ship')
        if controls:
            if respect:
                controls.adjustWallBitMask(BitMask32.allOff(), PiratesGlobals.ShipDeployBitmask)
            else:
                controls.adjustWallBitMask(PiratesGlobals.ShipDeployBitmask, BitMask32.allOff())

    def getRespectDeployBarriers(self):
        return self.respectDeployBarriers

    def placeAvatarAtWheel(self, av):
        wheelpost = self.locators.find('**/location_wheel;+s')
        av.setPos(wheelpost.getPos(self.root) - Vec3(0.0, -2.0, 0))
        av.setHpr(180, 0, 0)

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-shipboard-report')
    def setClientController(self, avId):
        if not self.mainPartsBuilt:
            self.registerMainBuiltFunction(self.setClientController, extraArgs=[avId])
            return
        self.clientController = avId
        if avId != 0 and avId == localAvatar.doId:
            self.setupControls()
            shipControls = self.controlManager.get('ship')
            shipControls.setShip(self)
            self.controlManager.setTag('avId', str(avId))
            self.controlManager.setTag('shipId', str(self.getDoId()))
            self.stopSmooth()
            self.startPosHprBroadcast()
        else:
            self.stopPosHprBroadcast()
            if self.controlManager:
                shipControls = self.controlManager.get('ship')
                shipControls.setShip(None)
            self.startSmooth()
        return

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-shipboard-report')
    def sendCrewToIsland(self, islandId, posH):
        island = base.cr.doId2do.get(islandId)
        localAvatar.removeFromShip(self)
        posHpr = posH + (0, 0)
        islandUid = island.getUniqueId()
        base.cr.loadingScreen.showTarget(islandUid)
        base.cr.loadingScreen.showHint(islandUid)
        base.cr.loadingScreen.show()
        base.cr.teleportMgr.localTeleportPos(posHpr, island)

    def getShipInfo(self):
        return [
         self.doId, self.getName(), self.shipClass, [ [dMast.getMastType(), dMast.getPosIndex(), dMast.getSailConfig()] for mast, dMast in self.masts.itervalues() if dMast ]]

    def getLocalShipInfo(self):
        return [
         self.doId, self.getName(), self.shipClass, [ [mast.dna.getMastType(), mast.dna.getPosIndex(), mast.dna.getSailConfig()] for mast, dMast in self.masts.itervalues() ]]

    def showBoardingChoice(self, shipToBoard):
        if not self.boardingPanel:
            shipInfo = shipToBoard.getShipInfo()
            dt = globalClockDelta.localElapsedTime(shipToBoard.sinkTimestamp)
            time = shipToBoard.sinkTime - dt
            self.boardingPanel = ShipFrameBoard.ShipFrameBoard(shipName=shipInfo[1], shipClass=shipInfo[2], mastInfo=shipInfo[3], parent=base.a2dTopCenter, pos=(-0.45, 0, -0.5), time=time, command=self.__handleBoardingChoice)
            self._boardingTimer = taskMgr.doMethodLater(time, self._boardingChoiceTimeout, 'boardingTimer')
        self.boardingPanel.show()

    def _boardingChoiceTimeout(self, task):
        self.removeBoardingChoice()

    def hideBoardingChoice(self):
        if self.boardingPanel:
            self.boardingPanel.hide()

    def removeBoardingChoice(self):
        if self.boardingPanel:
            self.boardingPanel.destroy()
            self.boardingPanel = None
        if self._boardingTimer:
            self._boardingTimer.remove()
            self._boardingTimer = None
        return

    def __handleBoardingChoice(self, wishToBoard):
        self.removeBoardingChoice()
        if wishToBoard:
            self.d_requestBoardFlagship(self.boardableShipId)

    def clearLog(self):
        if hasattr(base, 'shipLogs'):
            if self.doId in base.shipLogs:
                del base.shipLogs[self.doId]

    def loadFlat(self):
        if self.flat:
            return
        self.flat = self.root.attachNewNode('Flat')
        hullPrefix = self.hull[0].getFlatPrefix(self.modelClass)
        hull = loader.loadModel(hullPrefix)
        hull.reparentTo(self.flat)
        modelScale = ShipGlobals.ShipFlatScales.get(self.modelClass, Vec3(1, 1, 1))
        modelPos = ShipGlobals.ShipFlatOffsets.get(self.modelClass, Vec3(0, 0, 0))
        hull.setScale(modelScale)
        hull.setPos(modelPos)
        hull.findAllMatches('**/+GeomNode').wrtReparentTo(self.flat)
        hull.detachNode()
        for mastIndex in self.masts:
            mast = self.masts[mastIndex][0]
            mastPrefix = mast.getFlatPrefix(mast.dna.mastType)
            posIndex = mast.dna.posIndex
            id = ShipGlobals.getMastClassification(mast.dna.mastType)[0]
            if id == ShipGlobals.FOREMAST:
                locator = self.locators.find('**/location_foremast;+s')
            else:
                if id == ShipGlobals.MAINMAST:
                    locator = self.locators.find('**/location_mainmast_%s;+s' % posIndex)
                else:
                    if id == ShipGlobals.AFTMAST:
                        locator = self.locators.find('**/location_aftmast;+s')
            mastGeom = loader.loadModel(mastPrefix)
            mastGeom.reparentTo(locator)
            if self.getBaseTeam() == PiratesGlobals.PLAYER_TEAM:
                sails = mastGeom.findAllMatches('**/*_a')
                sails.addPathsFrom(mastGeom.findAllMatches('**/*_a_*'))
                team = self.getSiegeTeam()
                fileName = None
                if team == 1:
                    fileName = SailDNA.LogoDict.get(210)
                else:
                    if team == 2:
                        fileName = SailDNA.LogoDict.get(211)
                if fileName:
                    ts = TextureStage('logo')
                    ts.setTexcoordName('uvLogo')
                    tex = Sail.Sail.logoCard.find('**/%s' % fileName).findTexture('*')
                    sails.setTexture(ts, tex)
                mastGeom.findAllMatches('**/*_b').detach()
                mastGeom.findAllMatches('**/*_b_*').detach()
                mastGeom.findAllMatches('**/*_c').detach()
                mastGeom.findAllMatches('**/*_c_*').detach()
            else:
                if self.getBaseTeam() == PiratesGlobals.NAVY_TEAM:
                    mastGeom.findAllMatches('**/*_a').detach()
                    mastGeom.findAllMatches('**/*_a_*').detach()
                    mastGeom.findAllMatches('**/*_c').detach()
                    mastGeom.findAllMatches('**/*_c_*').detach()
                else:
                    if self.getBaseTeam() == PiratesGlobals.TRADING_CO_TEAM:
                        mastGeom.findAllMatches('**/*_a').detach()
                        mastGeom.findAllMatches('**/*_a_*').detach()
                        mastGeom.findAllMatches('**/*_b').detach()
                        mastGeom.findAllMatches('**/*_b_*').detach()
            mastHeight = len(mast.mastsState)
            if mastHeight < 2:
                mastGeom.findAllMatches('**/*_1*').detach()
                mastGeom.findAllMatches('**/*_2*').detach()
                mastGeom.findAllMatches('**/*_3*').detach()
            else:
                if mastHeight < 3:
                    mastGeom.findAllMatches('**/*_2*').detach()
                    mastGeom.findAllMatches('**/*_3*').detach()
                else:
                    if mastHeight < 4:
                        mastGeom.findAllMatches('**/*_3*').detach()
            sails = mastGeom.findAllMatches('**/sail*')
            mastGeom.findAllMatches('**/+GeomNode').wrtReparentTo(self.flat)
            mastGeom.detachNode()

        self.flat.flattenStrong()
        if self.lastZoneLevel == 4 or base.showShipFlats:
            self.root.stash()
        else:
            self.root.unstash()
            self.flat.stash()
        return

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-shipboard-report')
    def confirmSameCrewTeleport(self, toFrom, incomingAvId=0):
        if toFrom == 'from':
            return True
        else:
            if not self.isGenerated():
                self.notify.warning('confirmSameCrewTeleport(%s)' % localAvatar.getShipString())
                return False
            if incomingAvId == self.ownerId:
                return True
            if localAvatar.doId == self.ownerId and self.cr.identifyFriend(incomingAvId):
                return True
            handle = self.cr.identifyAvatar(incomingAvId)
            if handle and handle.getBandId() != (0, 0) and handle.getBandId() == self.getBandId():
                return True
            return False

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-shipboard-report')
    def confirmOnShipTeleport(self, toFrom, incomingAvId=0):
        if toFrom == 'from':
            if self.getSiegeTeam() and localAvatar.avId == self.ownerId:
                return False
            else:
                return True
        else:
            return self.hasSpace(incomingAvId)

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-shipboard-report')
    def confirmSiegeCaptainTeleport(self, toFrom, incomingAvId=0):
        if toFrom == 'from':
            return not self.getSiegeTeam() or localAvatar.doId != self.ownerId
        else:
            return True

    def hasSpace(self, avId=0):
        if avId == self.ownerId:
            return True
        if self.isInCrew(avId):
            return True
        if self.isInCrew(self.ownerId):
            return len(self.crew) < self.maxCrew
        return len(self.crew) < self.maxCrew - 1

    def onlyShowFlat(self):
        if self.flat:
            self.root.stash()
            self.flat.unstash()
        self.forceZoneLevel(4)

    def showNormalShip(self):
        self.clearForceZoneLevel()

    def hideNametag(self):
        if self.nametag3d:
            self.nametag3d.stash()

    def showNametag(self):
        if self.nametag3d:
            self.nametag3d.unstash()

    def setBandId(self, bandManagerId, bandId):
        self.bandId = (bandManagerId, bandId)

    def getBandId(self):
        return self.bandId

    def resetMiniLog(self, name=None):
        self.miniLog = name and MiniLog(name)

    def requestShipSkill(self, skillId, ammoSkillId):
        self.sendUpdate('requestSkillEvent', [skillId, ammoSkillId])

    def recordSkillEvent(self, skillId, ammoSkillId):
        if self.isInCrew(localAvatar.doId):
            localAvatar.skillDiary.startRecharging(skillId, ammoSkillId)
            localAvatar.guiMgr.combatTray.skillTray.updateSkillIval(skillId)

    def setupKrakenLocators(self):
        if not hasattr(self, 'krakenLocators') and self.kraken:
            self.findAllMatches('**/kraken-*').detach()
            self.krakenLocators = []
            locatorInfo = ShipGlobals.KrakenLocators.get(self.shipClass)
            for x, (pos, scale, rPos, rScale) in enumerate(locatorInfo):
                pos.setX(pos[0] + 30)
                locator = self.attachNewNode('kraken-%s' % (x,))
                locator.setPosHprScale(pos, VBase3(-90, 0, 0), VBase3(scale))
                locator.wrtReparentTo(self.waterlineNode)
                rangeParent = locator.attachNewNode('rangeParent')
                rangeParent.setPos(rPos)
                rangeParent.setScale(VBase3(rScale, rScale, 1))
                self.krakenLocators.insert(x, locator)
                x += len(locatorInfo)
                pos.setX(-pos[0])
                rPos.setX(-rPos[0])
                locator = self.attachNewNode('kraken-%s' % (x,))
                locator.setPosHprScale(pos, VBase3(90, 0, 0), VBase3(scale))
                locator.wrtReparentTo(self.waterlineNode)
                rangeParent = locator.attachNewNode('rangeParent')
                rangeParent.setPos(rPos)
                rangeParent.setScale(VBase3(rScale, rScale, 1))
                self.krakenLocators.append(locator)

    def getKrakenGrabberLocator(self, locatorId):
        self.setupKrakenLocators()
        return self.krakenLocators[locatorId]

    def getKrakenRangeParent(self, locatorId):
        locator = self.getKrakenGrabberLocator(locatorId)
        return locator.find('rangeParent')

    def setKraken(self, kraken):
        self.kraken = kraken

    def getModelRoot(self):
        return self.root

    def startSinkEffects(self):
        if not self.sinkEffectsRoot:
            self.sinkEffectsRoot = self.attachNewNode('sinkEffectsRoot')
        self.sinkEffectsRoot.setY(self.center.getY())
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
            ripples = WaterWakes.getEffect()
            if ripples:
                scale = self.hullDimensions
                ripples.reparentTo(self.sinkEffectsRoot)
                ripples.setScale(scale[0] / 5, scale[1] / 9, scale[2] / 3)
                ripples.startLoop()
                self.sinkEffects.append(ripples)
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
            mist = WaterMist.getEffect()
            if mist:
                mist.reparentTo(self.sinkEffectsRoot)
                mist.setScale(self.hullDimensions / 50.0)
                mist.setEffectScale(1.0)
                mist.setZ(-5.0)
                mist.startLoop()
                self.sinkEffects.append(mist)
        taskMgr.add(self.updateSinkEffects, self.uniqueName('updateSinkEffects'))

    def endSinkEffects(self):
        taskMgr.remove(self.uniqueName('updateSinkEffects'))
        for effect in self.sinkEffects:
            effect.stopLoop()

        self.sinkEffects = []

    def updateSinkEffects(self, task):
        pos = self.getPos(render)
        if base.cr.activeWorld.getWater():
            waterHeight = base.cr.activeWorld.getWater().calcHeight(pos[0], pos[1], 0, render)
            self.sinkEffectsRoot.setZ(render, waterHeight)
            if not self.kraken:
                self.sinkEffectsRoot.setY(self.sinkEffectsRoot.getY() - 0.15)
            return task.cont
        return task.done

    def startDestroyEffects(self):
        effectScale = self.dimensions[1] / 150
        if self.isInCrew(base.localAvatar.doId):
            cameraShakerEffect = CameraShaker()
            cameraShakerEffect.reparentTo(self)
            cameraShakerEffect.shakeSpeed = 0.04
            cameraShakerEffect.shakePower = 1.5
            cameraShakerEffect.numShakes = 4
            cameraShakerEffect.scalePower = 1.5
            cameraShakerEffect.play(500.0)
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
            shipDust = ShipSplintersA.getEffect()
            if shipDust:
                shipDust.reparentTo(self.hullCenter)
                shipDust.play()
            smokeCloud = SmokeCloud.getEffect()
            if smokeCloud:
                smokeCloud.reparentTo(self.hullCenter)
                smokeCloud.spriteScale = 2.0 * effectScale
                smokeCloud.setScale(2.0 * effectScale)
                smokeCloud.radius = 10.0 * effectScale
                smokeCloud.play()
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
            shipDebris = ShipDestruction.getEffect()
            if shipDebris:
                shipDebris.reparentTo(self.hullCenter)
                shipDebris.setEffectScale(effectScale)
                shipDebris.loadObjects(12)
                shipDebris.play()

    def _animateMiddleMast(self, anims):
        anims = makeList(anims)
        mast = ShipGlobals.getShipBreakMast(self.shipClass)
        if mast >= 0:
            self.masts[mast][0].setBreakAnim(0)
            numSails = len(self.sails[mast])
            for i in range(numSails):
                for anim in anims:
                    self.sails[mast][i][0].setAnimState(anim)

            if self.modelClass < 11:
                for anim in anims:
                    self.sails[3][0][0].setAnimState(anim)

    def breakMiddleMast(self):
        self._animateMiddleMast('Falling')

    def unbreakMiddleMast(self):
        self._animateMiddleMast(('Off', 'Idle'))

    def getSinkCamIval(self):
        camStartPos = Vec3(-4.0 * self.dimensions[0], -1.25 * self.dimensions[1], 40)
        camEndPos = Vec3(-4.0 * self.dimensions[0], self.dimensions[1], self.dimensions[2] / 2.0)
        self.lookAtDummy.setPos(0, 0, self.center.getZ())

        def camLookAtDummy(t):
            camera.lookAt(self.lookAtDummy)

        return Parallel(Func(camera.reparentTo, self.attachNewNode('cameraDummy')), LerpPosInterval(camera, 16.0, camEndPos, startPos=camStartPos, blendType='easeInOut'), LerpPosInterval(self.lookAtDummy, 18.0, Vec3(0, 80, 0)), LerpFunc(camLookAtDummy, 18.0))

    def getKrakenSinkCamIval(self):
        camStartPos = Vec3(-75, 2 * self.dimensions[1], 10)
        camEndPos = Vec3(-4 * self.dimensions[0], 20, 40)
        camEndPos2 = Vec3(-3.5 * self.dimensions[0], 0, 100)
        self.lookAtDummy.setPos(self.dimensions[0] / 3.0, 0, self.dimensions[2] / 2.0)

        def camLookAtDummy(t):
            camera.lookAt(self.lookAtDummy)

        return Parallel(Func(camera.reparentTo, self.attachNewNode('cameraDummy')), Sequence(LerpPosInterval(camera, 12.0, camEndPos, startPos=camStartPos, blendType='easeInOut'), LerpPosInterval(camera, 8.0, camEndPos2, blendType='easeInOut')), LerpPosInterval(self.lookAtDummy, 18.0, Vec3(10, 0, 20)), LerpFunc(camLookAtDummy, 18.0))

    def getSinkShipIval(self):
        return Parallel(LerpPosInterval(self.root, 18.0, Vec3(0, 0, -1.5 * self.dimensions[2])), LerpHprInterval(self.root, 12.0, VBase3(self.root.getH(), self.root.getP() - 75, self.root.getR())))

    def getKrakenSinkShipIval(self):
        self.splitShip()
        gap = self.dimensions[1] / 2.0
        return Parallel(Sequence(LerpPosInterval(self.root, 0.2, Vec3(0, 0, 1.0)), LerpPosInterval(self.root, 5.0, Vec3(0, 0, -0.15 * self.dimensions[2])), LerpPosInterval(self.root, 13.0, Vec3(0, 0, -1 * self.dimensions[2]))), Sequence(LerpPosHprInterval(self.clipParent1, 0.2, Vec3(0, 2, 0), Vec3(0, -3, 0)), LerpPosHprInterval(self.clipParent1, 8.0, Vec3(0, gap / 2.5, 0), Vec3(0, 40, 0)), LerpPosHprInterval(self.clipParent1, 6.0, Vec3(0, gap / 1.5, 0), Vec3(0, 50, 0))), Sequence(LerpPosHprInterval(self.clipParent2, 0.2, Vec3(0, -2, 0), Vec3(0, 3, 0)), LerpPosHprInterval(self.clipParent2, 8.0, Vec3(0, -gap / 2.5, 0), Vec3(0, -40, 0)), LerpPosHprInterval(self.clipParent2, 6.0, Vec3(0, -gap / 1.5, 0), Vec3(0, -50, 0))))

    def sinkingBegin(self):
        messenger.send(self.uniqueName('shipSinking'))
        self.computeDimensions()
        self.disableOnDeckInteractions()
        if self.cabin:
            self.cabin[0].cleanupEffects()
        if self.hull:
            self.hull[0].cleanupEffects()
        if self.nametag3d:
            self.nametag3d.hide()
        self.removeWake()
        soundTrack = Sequence()
        if self.sinkingSfx:
            soundTrack = Sequence(Func(base.playSfx, self.sinkingSfx, node=self, cutoff=1000))
        self.sinkTrack = Sequence()
        sinkParallel = Parallel()
        fadeClasstagOut = self.classNameText.colorScaleInterval(3.0, Vec4(0, 0, 0, 0))
        fadeNametagOut = self.nameText.colorScaleInterval(3.0, Vec4(0, 0, 0, 0))
        sinkParallel.append(fadeClasstagOut)
        sinkParallel.append(fadeNametagOut)
        if self.stormEffect:
            sinkParallel.append(Func(self.stormEffect.fadeOutAndStop))
        if self.isInCrew(localAvatar.doId):
            sinkParallel.append(Func(base.localAvatar.b_setGameState, 'Cutscene', localArgs=[self]))
            if self.kraken:
                sinkParallel.append(self.getKrakenSinkCamIval())
                sinkParallel.append(Sequence(Func(base.musicMgr.requestCurMusicFadeOut), Wait(5.2), Func(base.musicMgr.request, 'kraken-sink-ship', looping=0), Func(base.musicMgr.requestFadeIn, 'kraken-sink-ship', duration=0)))
            else:
                sinkParallel.append(self.getSinkCamIval())
        if self.kraken:
            sinkParallel.append(Sequence(Func(self.kraken.spawnDoomTentacle), Wait(5.2), Func(self.startSinkEffects), Func(self.startDestroyEffects), self.getKrakenSinkShipIval()))
            sinkParallel.append(Sequence(Func(self.kraken.hideSideTentacles, 1), Wait(5.0), Func(self.breakMiddleMast)))
        else:
            sinkParallel.append(Sequence(Func(self.startSinkEffects), soundTrack, self.getSinkShipIval()))
        self.sinkTrack.append(sinkParallel)
        self.sinkTrack.append(Func(self.endSinkEffects))
        if self.isInCrew(localAvatar.doId):
            self.sinkTrack.append(Func(self.cleanupLocalSinking))
        self.sinkTrack.start()
        self.removeTarget()

    def cleanupLocalSinking(self):
        base.transitions.fadeOut()
        base.transitions.letterboxOff()
        base.cr.interactionMgr.unlock()
        base.cr.interactionMgr.start()
        base.musicMgr.requestCurMusicFadeOut()

    def sinkingEnd(self):
        if self.sinkTrack:
            self.sinkTrack.finish()
            self.sinkTrack = None
        self.unloadInterface()
        self.endSinkEffects()
        messenger.send(self.shipSunkEvent)
        return

    def _undoSinking(self):
        self.root.setPosHpr(0, 0, 0, 0, 0, 0)
        self.transNode.setPosHpr(0, 0, 0, 0, 0, 0)
        if self.isSplit:
            self.clipParent1.setPosHpr(0, 0, 0, 0, 0, 0)
            self.clipParent2.setPosHpr(0, 0, 0, 0, 0, 0)
        self.nametag3d.show()
        self.classNameText.setColorScale(Vec4(1, 1, 1, 1))
        self.nameText.setColorScale(Vec4(1, 1, 1, 1))

    def recoverFromSunk(self):
        if self.isStatusDisplayVisible > 0:
            self.loadShipStatusDisplay()
            self.__checkStatusDisplayVisible()
        self.target = Target(self)
        self._undoSinking()
        self.createWake()
        if self.stormEffect:
            self.stormEffect.loop()
        if self.kraken and self.kraken.doomTentacle:
            self.kraken.doomTentacle.detachNode()
            self.kraken.doomTentacle = None
        if self.isInCrew(localAvatar.doId):
            base.localAvatar.b_setGameState('LandRoam')
            base.transitions.fadeIn()
            base.cr.loadingScreen.hide()
        self.enableOnDeckInteractions()
        return

    def splitShip(self):
        if not self.isSplit:
            self.isSplit = True
            self.modelGeom.instanceTo(self.clipParent2)
            planeNode1 = NodePath(PlaneNode('planeNode1', Plane(Vec4(0, 1, 0, 0))))
            planeNode1.reparentTo(self.clipParent1)
            planeNode1.setY(ShipGlobals.getShipSplitOffset(self.shipClass))
            self.clipParent1.setClipPlane(planeNode1)
            planeNode2 = NodePath(PlaneNode('planeNode2', Plane(Vec4(0, -1, 0, 0))))
            planeNode2.reparentTo(self.clipParent2)
            planeNode2.setY(ShipGlobals.getShipSplitOffset(self.shipClass))
            self.clipParent2.setClipPlane(planeNode2)

    def forceExitShip(self):
        self.localAvatarExitShip()

    def printCrazyInfo(self):
        print 'Name:\t\t', self.getName()
        print 'doId:\t\t', self.doId
        print 'location:\t', self.getLocation()
        print 'inv id:\t\t', self.getInventoryId()
        print 'inventory:\t', bool(self.getInventory())
        print 'shard:\t\t', self.cr.activeWorld.getParentObj().name, self.cr.activeWorld.getParentObj().doId

    def addShipTarget(self, ship, priority=0):
        if self.getBuildComplete() and ship.getBuildComplete():
            self.targets.add(ship.getTarget(), priority)

    def removeTarget(self, shipId=0):
        if self.target:
            if not shipId or shipId == self.doId:
                self.target.remove()

    def getTarget(self):
        if not self.target:
            self.target = Target(self)
        return self.target

    def getTargetPanel(self):
        if not self.shipTargetPanel:
            self.loadShipTargetPanel()
        return self.shipTargetPanel

    def getDamageInputModifier(self):
        return 1.0

    def getDamageOutputModifier(self):
        return 1.0

    def isLocalCaptain(self):
        return self.steeringAvId == localAvatar.doId

    def setupSmoothing(self):
        self.activateSmoothing(1, 0)
        self.smoother.setDelay(OTPGlobals.NetworkLatency * 1.5)
        broadcastPeriod = 2.0
        self.smoother.setMaxPositionAge(broadcastPeriod * 1.25 * 10)
        self.smoother.setExpectedBroadcastPeriod(broadcastPeriod)
        self.smoother.setDefaultToStandingStill(False)
        self.setSmoothWrtReparents(True)
        self.startSmooth()

    def setWheelInUse(self, wheelInUse):
        pass

    def storeCamParams(self, shipCamParams):
        self._shipCamParams = shipCamParams

    def retrieveCamParams(self):
        return self._shipCamParams
