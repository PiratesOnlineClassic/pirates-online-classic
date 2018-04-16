import copy
import time

from direct.interval.IntervalGlobal import *
from direct.interval.ProjectileInterval import *
from pandac.PandaModules import *
from pirates.battle import Cannon
from pirates.effects.DarkMaelstrom import DarkMaelstrom
from pirates.effects.JRTeleportEffect import JRTeleportEffect
from pirates.effects.SpectralTrail import SpectralTrail
from pirates.effects.Wake import Wake
from pirates.piratesbase import PiratesGlobals
from pirates.ship import ShipGlobals
from pirates.shipparts import (BowSprit, BowSpritDNA, Cabin, CabinDNA,
                               CannonPort, DecorDNA, Hull, HullDNA, Lantern,
                               Mast, MastDNA, Sail, SailDNA, ShipDecor, Wheel,
                               Window)
from pirates.uberdog.UberDogGlobals import InventoryType


class ShipBroadside(NodePath):

    def __init__(self, ship):
        NodePath.__init__(self, 'shipBroadside')
        self.doId = str(time.time())
        self.ship = ship

    def uniqueName(self, name):
        return name + self.doId


class ShipModel(NodePath):
    
    def __init__(self, cr, shipClass, team, wantCollisions=0, fromEditor=False):
        NodePath.__init__(self, 'ShipModel')
        self.doId = 0
        self.cr = cr
        self.baseTeam = team
        self.shipClass = shipClass
        self.modelClass = ShipGlobals.getModelClass(self.shipClass)
        self.wantCollisions = wantCollisions
        self.stormEffect = None
        self.effect = None
        self.fader = None
        self.JRival = None
        self.deckName = 'deck'
        self.railingName = 'railing'
        stats = ShipGlobals.getShipConfigAll(shipClass)
        self.transNode = self.attachNewNode('transNode')
        self.root = self.transNode.attachNewNode('root')
        self.broadside = ShipBroadside(self)
        self.modelGeom = self.root.attachNewNode(ModelNode('modelGeomRoot'))
        self.modelCollisions = self.root.attachNewNode(ModelNode('modelCol'))
        self.interactionCollisions = self.root.attachNewNode(ModelNode('interactCol'))
        self.projScreen = ProjectionScreen('p')
        self.projScreen = self.modelGeom.attachNewNode(ProjectionScreen('one big screen'))
        self.projScreen.node().setTexcoordName('uvHole')
        self.highStatic = self.root.attachNewNode('highStatic')
        self.mediumStatic = NodePath('mediumStatic')
        self.lowStatic = NodePath('lowStatic')
        self.lodRoot = NodePath('lod Node')
        self.lodRoot.reparentTo(self.modelGeom)
        self.highDetail = self.lodRoot.attachNewNode(ModelNode('high'))
        self.mediumDetail = self.lodRoot.attachNewNode(ModelNode('medium'))
        self.lowDetail = self.lodRoot.attachNewNode(ModelNode('low'))
        self.dna = HullDNA.HullDNA()
        self._copyDNAattribs(self.dna, stats)
        hull = Hull.Hull(self, self.cr)
        hull.loadModel(self.dna)
        hull.loadHigh()
        hull.loadMedium()
        hull.loadLow()
        hull.geom_High.reparentTo(self.root)
        hull.geom_Medium.reparentTo(self.root)
        hull.geom_Low.reparentTo(self.root)
        self.hull = [hull, 0]
        self.highStatic.reparentTo(self.root)
        self.mediumStatic.reparentTo(self.root)
        self.lowStatic.reparentTo(self.root)
        filePrefix = HullDNA.HullDict.get(self.modelClass)
        self.locators = loader.loadModelCopy(filePrefix + '-locators')
        if self.locators:
            self.locators.reparentTo(self.root)
            self.locators.stash()
        if self.wantCollisions:
            self.hull[0].loadCollisions()
            self.hull[0].setupCollisions()
            self.hull[0].unstashDetailCollisions()
            self.hull[0].propCollisions.reparentTo(self.hull[0])
        self.hull[0].reparentTo(self)
        self.hull[0].ship = self
        self.cabin = None
        if self.dna.cabinType != 0:
            self.cabin = Cabin.Cabin(self.cr)
            self.cabin.ship = self
            self.cabin.loadModel(self.dna)
            self.cabin.loadHigh()
            self.cabin.loadMedium()
            self.cabin.loadLow()
            if self.wantCollisions:
                self.cabin.loadCollisions()
                self.cabin.setupCollisions()
                self.cabin.unstashDetailCollisions()
                self.cabin.propCollisions.reparentTo(self.hull[0])
            self.cabin.reparentTo(self.root)
            self.cabin.geom_High.reparentTo(self.root)
            self.cabin.geom_Medium.reparentTo(self.root)
            self.cabin.geom_Low.reparentTo(self.root)
            self.cabin.ship = self
        if fromEditor:
            wheelPost = self.locators.find('**/location_wheel;+s')
            if not wheelPost.isEmpty():
                wheel = Wheel.Wheel()
                wheel.ship = self
                wheel.loadModel(self.shipClass)
                if self.shipClass == ShipGlobals.DINGHY:
                    wheel.hide()
                wheel.reparentTo(self.root)
                wheel.geom_High.setPos(wheelPost.getPos(self.root))
                wheel.geom_High.setHpr(wheelPost.getHpr(self.root))
                wheel.geom_High.setScale(wheelPost.getScale(self.root))
                wheel.geom_Medium.setPos(wheelPost.getPos(self.root))
                wheel.geom_Medium.setHpr(wheelPost.getHpr(self.root))
                wheel.geom_Medium.setScale(wheelPost.getScale(self.root))
                wheel.geom_Low.setPos(wheelPost.getPos(self.root))
                wheel.geom_Low.setHpr(wheelPost.getHpr(self.root))
                wheel.geom_Low.setScale(wheelPost.getScale(self.root))
                wheel.addToShip()
        self.cannons = []
        if self.cr is not None or False and fromEditor:
            for i in xrange(len(self.dna.cannonConfig)):
                cannonType = self.dna.cannonConfig[i]
                if cannonType > 0:
                    cannon = Cannon.Cannon(self.cr)
                    cannon.loadModel(self.dna)
                    cannonPost = self.locators.find('**/cannon_' + str(i) + ';+s')
                    cannon.reparentTo(self.root)
                    cannon.setPos(cannonPost.getPos(self.root))
                    cannon.setHpr(cannonPost.getHpr(self.root))
                    cannon.setScale(cannonPost.getScale(self.root))
                    self.cannons.append(cannon)

        self.leftBroadside = []
        self.rightBroadside = []
        if self.cr is not None or fromEditor:
            for i in xrange(len(self.dna.leftBroadsideConfig)):
                cannonType = self.dna.leftBroadsideConfig[i]
                if cannonType > 0:
                    cannonPost = self.locators.find('**/broadside_left_' + str(i) + ';+s')
                    cannon = CannonPort.CannonPort(self.dna.leftBroadsideConfig[i], self.broadside, cannonPost, 0, len(self.leftBroadside))
                    cannon.reparentTo(self.root)
                    cannon.setPos(cannonPost.getPos(self.root))
                    cannon.setHpr(cannonPost.getHpr(self.root))
                    cannon.setScale(cannonPost.getScale(self.root))
                    cannon.geom_High.reparentTo(self.root)
                    cannon.geom_High.setPos(cannonPost.getPos(self.root))
                    cannon.geom_High.setHpr(cannonPost.getHpr(self.root))
                    cannon.geom_High.setScale(cannonPost.getScale(self.root))
                    self.leftBroadside.append(cannon)

            for i in xrange(len(self.dna.rightBroadsideConfig)):
                cannonType = self.dna.rightBroadsideConfig[i]
                if cannonType > 0:
                    cannonPost = self.locators.find('**/broadside_right_' + str(i) + ';+s')
                    cannon = CannonPort.CannonPort(self.dna.rightBroadsideConfig[i], self.broadside, cannonPost, 0, len(self.rightBroadside))
                    cannon.reparentTo(self.root)
                    cannon.setPos(cannonPost.getPos(self.root))
                    cannon.setHpr(cannonPost.getHpr(self.root))
                    cannon.setScale(cannonPost.getScale(self.root))
                    cannon.geom_High.reparentTo(self.root)
                    cannon.geom_High.setPos(cannonPost.getPos(self.root))
                    cannon.geom_High.setHpr(cannonPost.getHpr(self.root))
                    cannon.geom_High.setScale(cannonPost.getScale(self.root))
                    self.rightBroadside.append(cannon)

        self.prow = None
        if self.dna.prowType != 0:
            prowDNA = BowSpritDNA.BowSpritDNA()
            prowDNA.baseTeam = self.baseTeam
            prowDNA.prowType = self.dna.prowType
            self.prow = BowSprit.BowSprit()
            self.prow.loadModel(prowDNA)
            self.prow.loadHigh()
            self.prow.loadMedium()
            self.prow.loadLow()
            if self.wantCollisions:
                self.prow.unstashDetailCollisions()
                self.prow.loadCollisions()
            self.prow.reparentTo(self.root)
            self.prow.ship = self
            locator = self.locators.find('**/location_bowsprit;+s')
            self.prow.setPos(locator.getPos())
            self.prow.setHpr(locator.getHpr())
            self.prow.setScale(locator.getScale())
            if fromEditor:
                self.prow.geom_High.setPos(self.prow.getPos(self.root))
                self.prow.geom_High.setHpr(self.prow.getHpr(self.root))
                self.prow.geom_High.setScale(self.prow.getScale(self.root))
                self.prow.geom_Medium.setPos(self.prow.getPos(self.root))
                self.prow.geom_Medium.setHpr(self.prow.getHpr(self.root))
                self.prow.geom_Medium.setScale(self.prow.getScale(self.root))
                self.prow.geom_Low.setPos(self.prow.getPos(self.root))
                self.prow.geom_Low.setHpr(self.prow.getHpr(self.root))
                self.prow.geom_Low.setScale(self.prow.getScale(self.root))
                self.prow.addToShip()
            if self.wantCollisions and self.prow.propCollisions != NodePath.notFound():
                self.prow.propCollisions.reparentTo(self.root)
                self.prow.propCollisions.setPos(locator.getPos())
                self.prow.propCollisions.setHpr(locator.getHpr())
                self.prow.propCollisions.setScale(locator.getScale())
        self.ram = None
        if self.dna.ramType != 0:
            prowDNA = BowSpritDNA.BowSpritDNA()
            prowDNA.baseTeam = self.baseTeam
            prowDNA.prowType = self.dna.ramType
            self.ram = BowSprit.BowSprit()
            self.ram.loadModel(prowDNA)
            self.ram.loadHigh()
            self.ram.loadMedium()
            self.ram.loadLow()
            if self.wantCollisions:
                self.ram.unstashDetailCollisions()
                self.ram.loadCollisions()
            self.ram.reparentTo(self.root)
            self.ram.ship = self
            locator = self.locators.find('**/location_ram;+s')
            self.ram.setPos(locator.getPos())
            self.ram.setHpr(locator.getHpr())
            self.ram.setScale(locator.getScale())
            if fromEditor:
                self.ram.geom_High.setPos(self.ram.getPos(self.root))
                self.ram.geom_High.setHpr(self.ram.getHpr(self.root))
                self.ram.geom_High.setScale(self.ram.getScale(self.root))
                self.ram.geom_Medium.setPos(self.ram.getPos(self.root))
                self.ram.geom_Medium.setHpr(self.ram.getHpr(self.root))
                self.ram.geom_Medium.setScale(self.ram.getScale(self.root))
                self.ram.geom_Low.setPos(self.ram.getPos(self.root))
                self.ram.geom_Low.setHpr(self.ram.getHpr(self.root))
                self.ram.geom_Low.setScale(self.ram.getScale(self.root))
                self.ram.addToShip()
            if self.wantCollisions:
                self.ram.propCollisions.reparentTo(self.root)
                self.ram.propCollisions.setPos(locator.getPos())
                self.ram.propCollisions.setHpr(locator.getHpr())
                self.ram.propCollisions.setScale(locator.getScale())
        self.masts = {}
        self.sails = {}
        configNames = (('setMastConfig1', 'setSailConfig1'), ('setMastConfig2', 'setSailConfig2'), ('setMastConfig3', 'setSailConfig3'), ('setForemastConfig', 'setForesailConfig'), ('setAftmastConfig', 'setAftsailConfig'))
        for i in xrange(len(configNames)):
            mastConfigName, sailConfigName = configNames[i]
            mastId = getattr(self.dna, 'g' + mastConfigName[1:])()
            if mastId == 0:
                continue
            stats = ShipGlobals.getMastStats(mastId)
            numMasts = len(stats['maxArrayHp'])
            mast = Mast.Mast(self, self.cr)
            mastDNA = MastDNA.MastDNA()
            self._copyMastDNAattribs(mastDNA, mastConfigName, sailConfigName, i)
            mastDNA.textureIndex = self.dna.mastTextureIndex
            mastDNA.sailLogoIndex = self.dna.sailLogoIndex
            mast.ship = self
            mast.loadModel(mastDNA)
            mast.loadHigh()
            mast.loadMedium()
            mast.loadLow()
            mast.addToShip()
            if self.wantCollisions:
                mast.unstashDetailCollisions()
                mast.loadCollisions()
            if mast.dna.mastType >= ShipGlobals.FOREMASTL1 and mast.dna.mastType <= ShipGlobals.FOREMASTL3:
                locator = self.locators.find('**/location_foremast;+s')
            elif mast.dna.mastType >= ShipGlobals.SKEL_FOREMASTL1 and mast.dna.mastType <= ShipGlobals.SKEL_FOREMASTL3:
                locator = self.locators.find('**/location_foremast;+s')
            elif mast.dna.mastType >= ShipGlobals.MAINMASTL1 and mast.dna.mastType <= ShipGlobals.TRIMASTL5:
                locator = self.locators.find('**/location_mainmast_' + str(mast.dna.posIndex) + ';+s')
            elif mast.dna.mastType >= ShipGlobals.SKEL_MAINMASTL1_A and mast.dna.mastType <= ShipGlobals.SKEL_TRIMASTL5:
                locator = self.locators.find('**/location_mainmast_' + str(mast.dna.posIndex) + ';+s')
            elif mast.dna.mastType >= ShipGlobals.AFTMASTL1 and mast.dna.mastType <= ShipGlobals.AFTMASTL3:
                locator = self.locators.find('**/location_aftmast;+s')
            elif mast.dna.mastType >= ShipGlobals.SKEL_AFTMASTL1 and mast.dna.mastType <= ShipGlobals.SKEL_AFTMASTL3:
                locator = self.locators.find('**/location_aftmast;+s')
            self.masts[mast.dna.posIndex] = [
             mast, 0]
            self.sails[mast.dna.posIndex] = {}
            for j in xrange(len(mastDNA.sailConfig)):
                if mastDNA.sailConfig[j] == 0 and fromEditor:
                    continue
                sail = Sail.Sail(self, self.cr)
                sail.mastIndex = mastDNA.mastType
                sailDNA = SailDNA.SailDNA()
                sailDNA.baseTeam = self.dna.baseTeam
                sailDNA.posIndex = j
                sailDNA.textureIndex = mastDNA.sailTextureIndex
                sailDNA.logoIndex = mastDNA.sailLogoIndex
                sailDNA.mastType = mastDNA.mastType
                sailDNA.sailType = mastDNA.sailConfig[j]
                if fromEditor:
                    sailDNA.mastPosIndex = mast.dna.posIndex
                sail.ship = self
                sail.loadModel(sailDNA)
                sail.setProjScreen(self.projScreen)
                sail.addToShip()
                sail.sailActor.reparentTo(mast)
                sail.setScale(locator.getScale())
                self.sails[mast.dna.posIndex][sail.dna.posIndex] = [
                 sail, 0]
                sail.setAnimState('Idle')

        self.decors = []
        for i in range(len(self.dna.wallDecorConfig)):
            self.loadDecor(self.dna.wallDecorConfig[i], i)

        for i in range(len(self.dna.floorDecorConfig)):
            self.loadDecor(self.dna.floorDecorConfig[i], i)

        if self.modelClass == ShipGlobals.SKEL_WARSHIPL3 or self.modelClass == ShipGlobals.SKEL_INTERCEPTORL3:
            if not self.stormEffect:
                self.stormEffect = DarkMaelstrom(self)
                self.stormEffect.setZ(50)
                self.stormEffect.loop()
                compassFX = CompassEffect.make(render)
                self.stormEffect.setEffect(compassFX)
        if fromEditor and base.pe.fRpmMode:
            self.forwardVelocity = 0.0
            self.rotationalVelocity = 0.0
            self.wake = None
            self.createWake()
        self.setLOD('high')
        return

    def createWake(self):
        self.removeWake()
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

    def taskName(self, key):
        return key + str(self.shipClass)

    def getForwardVelocity(self):
        return self.forwardVelocity

    def getRotationalVelocity(self):
        return self.rotationalVelocity

    def setLOD(self, lod):
        lodDic = {'low': 'geom_Low', 'medium': 'geom_Medium', 'high': 'geom_High'}
        self.highDetail.hide()
        self.mediumDetail.hide()
        self.lowDetail.hide()
        self.highStatic.hide()
        self.mediumStatic.hide()
        self.lowStatic.hide()
        exec 'self.' + lod + 'Detail.show()'
        exec 'self.' + lod + 'Static.show()'
        for lodKey in lodDic:
            exec 'self.hull[0].' + lodDic[lodKey] + '.hide()'
            if hasattr(self.cabin, lodDic[lodKey]):
                exec 'self.cabin.' + lodDic[lodKey] + '.hide()'

        exec 'self.hull[0].' + lodDic[lod] + '.show()'
        if hasattr(self.cabin, lodDic[lod]):
            exec 'self.cabin.' + lodDic[lod] + '.show()'

    def fireCannon(self, index, ammo=InventoryType.CannonRoundShot, targetPos=None, targetNode=None, wantCollisions=0, flightTime=None, preciseHit=False, offset=Vec3(0, 0, 0)):
        if targetNode:
            targetPos = targetNode.getPos(render)
        targetPos = targetPos + offset
        if len(self.cannons):
            self.cannons[index].playAttack(InventoryType.CannonShoot, ammo, 'localShipHit', targetPos, wantCollisions, flightTime, preciseHit)

    def fireAllCannons(self, ammo=InventoryType.CannonRoundShot, targetPos=None, targetNode=None, wantCollisions=0):
        for i in xrange(len(self.cannons)):
            self.fireCannon(i, ammo, targetPos, targetNode, wantCollisions)

    def destroy(self):
        if self.stormEffect:
            self.stormEffect.destroy()
            self.stormEffect = None
        if self.effect:
            self.effect.finish()
            self.effect = None
        if self.fader:
            self.fader.pause()
            self.fader = None
        if self.JRival:
            self.JRival.pause()
            self.JRival = None
        if self.ram:
            self.ram.disable()
            self.ram.delete()
            self.ram = None
        if self.prow:
            self.prow.disable()
            self.prow.delete()
            self.prow = None
        for decor in self.decors:
            decor.disable()
            decor.delete()

        self.decors = []
        for mast in self.sails.values():
            for entry in mast.values():
                sail = entry[0]
                sail.disable()
                sail.delete()

        self.sails = {}
        for entry in self.masts.values():
            mast = entry[0]
            mast.disable()
            mast.delete()

        self.masts = {}
        for cannon in self.cannons:
            cannon.disable()
            cannon.delete()

        self.cannons = []
        for cannon in self.leftBroadside:
            cannon.delete()

        self.leftBroadside = []
        for cannon in self.rightBroadside:
            cannon.delete()

        self.rightBroadside = []
        if self.cabin:
            self.cabin.disable()
            self.cabin.delete()
            self.cabin = None
        self.hull[0].disable()
        self.hull[0].delete()
        self.hull = [None, None]
        return

    def hideMasts(self):
        for entry in self.masts.values():
            entry[0].geom_High.stash()
            entry[0].geom_Medium.stash()
            entry[0].geom_Low.stash()

    def showMasts(self):
        for entry in self.masts.values():
            entry[0].geom_High.unstash()
            entry[0].geom_Medium.unstash()
            entry[0].geom_Low.unstash()

    def hideCannons(self):
        for cannon in self.cannons:
            cannon.stash()

    def showCannons(self):
        for cannon in self.cannons:
            cannon.unstash()

    def _copyMastDNAattribs(self, mastDNA, mastType, sailType, posIndex):
        mastDNA.shipClass = self.dna.shipClass
        mastDNA.modelClass = self.dna.modelClass
        mastDNA.baseTeam = self.dna.baseTeam
        mastDNA.sailTextureIndex = self.dna.sailTextureIndex
        mastDNA.posIndex = posIndex
        mastDNA.mastType = getattr(self.dna, 'g' + mastType[1:])()
        mastDNA.sailConfig = getattr(self.dna, 'g' + sailType[1:])()

    def _copyDNAattribs(self, dna, stats):
        dna.shipClass = self.shipClass
        dna.modelClass = self.modelClass
        dna.baseTeam = self.baseTeam
        dna.mastConfig1 = stats['setMastConfig1']
        dna.mastConfig2 = stats['setMastConfig2']
        dna.mastConfig3 = stats['setMastConfig3']
        dna.foremastConfig = stats['setForemastConfig']
        dna.aftmastConfig = stats['setAftmastConfig']
        dna.hullTextureIndex = copy.copy(stats['setHullTextureIndex'])
        dna.stripeTextureIndex = copy.copy(stats['setStripeTextureIndex'])
        dna.patternTextureIndex = copy.copy(stats['setPatternTextureIndex'])
        dna.hullColorIndex = copy.copy(stats['setHullColorIndex'])
        dna.stripeColorIndex = copy.copy(stats['setStripeColorIndex'])
        dna.patternColorIndex = copy.copy(stats['setPatternColorIndex'])
        dna.hullHilightColorIndex = copy.copy(stats['setHullHilightColorIndex'])
        dna.stripeHilightColorIndex = copy.copy(stats['setStripeHilightColorIndex'])
        dna.patternHilightColorIndex = copy.copy(stats['setPatternHilightColorIndex'])
        dna.sailConfig1 = copy.copy(stats['setSailConfig1'])
        dna.sailConfig2 = copy.copy(stats['setSailConfig2'])
        dna.sailConfig3 = copy.copy(stats['setSailConfig3'])
        dna.mastTextureIndex = copy.copy(stats['setMastTextureIndex'])
        dna.sailTextureIndex = copy.copy(stats['setSailTextureIndex'])
        dna.sailLogoIndex = copy.copy(stats['setSailLogoIndex'])
        dna.foresailConfig = copy.copy(stats['setForesailConfig'])
        dna.aftsailConfig = copy.copy(stats['setAftsailConfig'])
        dna.panelArmorConfig = copy.copy(stats['setPanelArmorConfig'])
        dna.cannonConfig = copy.copy(stats['setCannonConfig'])
        dna.leftBroadsideConfig = copy.copy(stats['setLeftBroadsideConfig'])
        dna.rightBroadsideConfig = copy.copy(stats['setRightBroadsideConfig'])
        dna.wallDecorConfig = copy.copy(stats['setWallDecorConfig'])
        dna.floorDecorConfig = copy.copy(stats['setFloorDecorConfig'])
        dna.prowType = stats['setProwType']
        dna.ramType = stats['setRamType']
        dna.cabinType = stats['setCabinType']
        dna.cabinMastConfig = copy.copy(stats['setCabinMastConfig'])
        dna.cabinSailConfig = copy.copy(stats['setCabinSailConfig'])
        dna.cabinCannonConfig = copy.copy(stats['setCabinCannonConfig'])
        dna.cabinWallDecorConfig = copy.copy(stats['setCabinWallDecorConfig'])
        dna.cabinWindowConfig = copy.copy(stats['setCabinWindowConfig'])

    def loadDecor(self, decorType, posIndex):
        if decorType > 0:
            decorClass = DecorDNA.getDecorType(decorType)
            if decorClass == 'lantern':
                prop = Lantern.Lantern()
            elif decorClass == 'decoration':
                prop = ShipDecor.ShipDecor()
            elif decorClass == 'window':
                prop = Window.Window()
            decorDNA = DecorDNA.DecorDNA()
            decorDNA.baseTeam = self.dna.baseTeam
            decorDNA.posIndex = posIndex
            decorDNA.decorType = decorType
            prop.loadModel(decorDNA)
            prop.loadHigh()
            prop.loadMedium()
            prop.loadLow()
            if self.wantCollisions:
                prop.unstashDetailCollisions()
                prop.loadCollisions()
            decorPlacement = DecorDNA.DecorDict.get(decorType)
            if decorPlacement[1] == DecorDNA.WALL:
                locator = self.locators.find('**/wall_decor_' + str(posIndex) + ';+s')
            elif decorPlacement[1] == DecorDNA.FLOOR:
                locator = self.locators.find('**/floor_decor_' + str(posIndex) + ';+s')
            elif decorPlacement[1] == DecorDNA.WINDOW:
                locator = self.locators.find('**/window_' + str(posIndex) + ';+s')
            prop.setPos(locator.getPos(self.root))
            prop.setHpr(locator.getHpr(self.root))
            prop.setScale(locator.getScale(self.root))
            prop.reparentTo(self.root)
            if self.wantCollisions:
                prop.propCollisions.reparentTo(self.hull[0].propCollisions)
                prop.propCollisions.setPos(self.root, locator.getPos(self.root))
                prop.propCollisions.setHpr(self.root, locator.getHpr(self.root))
                prop.propCollisions.setScale(self.root, locator.getScale(self.root))
            self.decors.append(prop)

    def fadeIn(self):
        if self.fader:
            self.fader.finish()
            self.fader = None
        self.setTransparency(1)
        self.hull[0].geom_High.setTextureOff(3)
        self.hull[0].geom_Medium.setTextureOff(3)
        self.hull[0].geom_Low.setTextureOff(3)
        self.cabin.geom_High.setTextureOff(3)
        self.cabin.geom_Medium.setTextureOff(3)
        self.cabin.geom_Low.setTextureOff(3)
        self.fader = Parallel(self.stormEffect.colorScaleInterval(1.0, Vec4(1, 1, 1, 1), startColorScale=Vec4(0, 0, 0, 0)), Func(self.hull[0].geom_High.clearTexture), Func(self.hull[0].geom_Medium.clearTexture), Func(self.hull[0].geom_Low.clearTexture), Func(self.cabin.geom_High.clearTexture), Func(self.cabin.geom_Medium.clearTexture), Func(self.cabin.geom_Low.clearTexture), Sequence(self.colorScaleInterval(1.0, Vec4(0, 0, 0, 1), startColorScale=Vec4(0, 0, 0, 0)), Func(self.showAllPanels), self.colorScaleInterval(1.0, Vec4(1, 1, 1, 1), startColorScale=Vec4(0, 0, 0, 1)), Func(self.clearTransparency)))
        self.fader.start()
        return

    def fadeOut(self):
        if self.fader:
            self.fader.finish()
            self.fader = None
        self.setTransparency(1)
        self.fader = Sequence(Func(self.stormEffect.fadeOutAndStop), self.colorScaleInterval(1.0, Vec4(0, 0, 0, 1), startColorScale=Vec4(1, 1, 1, 1)), Func(self.hull[0].geom_High.setTextureOff, 3), Func(self.hull[0].geom_Medium.setTextureOff, 3), Func(self.hull[0].geom_Low.setTextureOff, 3), Func(self.cabin.geom_High.setTextureOff, 3), Func(self.cabin.geom_Medium.setTextureOff, 3), Func(self.cabin.geom_Low.setTextureOff, 3), self.colorScaleInterval(1.0, Vec4(0, 0, 0, 0), startColorScale=Vec4(0, 0, 0, 1)), Func(self.hideAllPanels), Func(self.clearTransparency))
        self.fader.start()
        return

    def hideAllPanels(self):
        self.hull[0].hideAllPanels()
        self.cabin.hideAllPanels()

    def showAllPanels(self):
        self.hull[0].showAllPanels()
        self.cabin.showAllPanels()

    def playJRteleportFX(self, targetShip):
        if not targetShip:
            return
        targetPos = targetShip.getPos(render)
        targetPos = Vec3(targetPos[0], targetPos[1], targetPos[2] + 30.0)
        startPos = self.hull[0].getPos(render)
        self.effectDummy = render.attachNewNode('effectDummy')
        self.effect = JRTeleportEffect.getEffect()
        if self.effect and self.effectDummy:
            self.effect.reparentTo(self.effectDummy)
            self.effect.duration = 3.0
            self.effect.effectScale = 3.0
            self.effect.radius = 0.5
            self.effect.setPos(0, 0, 0)
        proj_ival = ProjectileInterval(self.effect, endZ=0, startPos=startPos, endPos=targetPos, duration=4.0, gravityMult=1.0)
        self.JRival = Sequence(Func(self.effect.startLoop), proj_ival, Func(self.effect.stopLoop))
        self.JRival.start()

    def stopJRteleportFX(self):
        if self.effect:
            self.effect.finish()
            self.effect = None
        if self.JRival:
            self.JRival.pause()
            self.JRival = None
        return

    def getShipInfo(self):
        return [self.modelClass, [ [mast.dna.getMastType(), mast.dna.getPosIndex(), mast.dna.getSailConfig()] for mast, dMast in self.masts.itervalues() ]]