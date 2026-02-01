import random
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from panda3d.core import *
from pirates.piratesbase.PiratesGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.Fire import Fire
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.MuzzleFlash import MuzzleFlash
from pirates.effects.WoodShards import WoodShards
from pirates.shipparts import CabinDNA
from pirates.shipparts import SplattableObject
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.battle import CannonGlobals
from pirates.battle import WeaponGlobals
from pirates.shipparts import ShipPart
from pirates.ship import ShipGlobals

class Cabin(SplattableObject.SplattableObject, ShipPart.ShipPart):
    notify = directNotify.newCategory('Cabin')
    
    def __init__(self, cr):
        self.cr = cr
        SplattableObject.SplattableObject.__init__(self)
        ShipPart.ShipPart.__init__(self)
        NodePath.__init__(self, 'cabin')
        self.collisions = None
        self.locators = None
        self.floors = None
        self.railing = None
        self.details = None
        self.propCollisions = NodePath('Collisions-Cabin')

    def disable(self):
        SplattableObject.SplattableObject.disable(self)
        ShipPart.ShipPart.disable(self)

    def delete(self):
        SplattableObject.SplattableObject.delete(self)
        ShipPart.ShipPart.destroy(self)
        self.clearTargetableCollisions()

    def loadModel(self, dna):
        self.dna = dna
        SplattableObject.SplattableObject.load(self)
        self.loadCollisions()
        self.loaded = True

    def unloadModel(self):
        SplattableObject.SplattableObject.disable(self)
        if self.propCollisions:
            self.propCollisions.removeNode()
            self.propCollisions = None
        
        self.removeNode()
    
    def loadHigh(self):
        filePrefix = self.getPrefix(self.dna.cabinType)
        (result, data) = ShipGlobals.getShipGeom('%s-geometry_High' % filePrefix)
        if result:
            (geom, static) = data
            hull = geom.copyTo(hidden)
            self.geom_High = hull
            self.tightBounds = hull.getTightBounds()
            staticGeom = static.copyTo(hidden)
            self.changeColor(self.geom_High)
            self.changeColor(staticGeom)
            staticGeom.findAllMatches('*').reparentTo(self.ship.highStatic)
            staticGeom.detachNode()
            numPanels = hull.findAllMatches('**/panel_High_*').getNumPaths()
            for i in range(numPanels):
                panel = hull.find('**/panel_High_%s' % i)
                self.panelsHigh.append(panel)
            
            self.geom_High.flattenStrong()
            for i in range(len(self.panelsHigh)):
                panel = self.panelsHigh[i]
                panelGeom = panel.getChild(0)
                panelGeom.setName('panel_High_%d' % i)
                panelGeom.reparentTo(self.geom_High)
                panelGeom.node().setPreserved(True)
                panelGeom.setTransparency(1)
                panel.detachNode()
                self.panelsHigh[i] = panelGeom
            
        else:
            self.geom_High = NodePath('Cabin-model')

    def unloadHigh(self):
        if not self.geom_High:
            return
        
        if self.geom_High.isEmpty():
            return
        
        if not self.panelsHigh:
            return
        
        self.geom_High.removeNode()
        self.geom_High = None
        self.panelsHigh = []

    def loadMedium(self):
        filePrefix = self.getPrefix(self.dna.cabinType)
        (result, data) = ShipGlobals.getShipGeom('%s-geometry_Medium' % filePrefix)
        if result:
            (geom, static) = data
            hull = geom.copyTo(hidden)
            self.geom_Medium = hull
            staticGeom = static.copyTo(hidden)
            self.changeColor(hull)
            self.changeColor(staticGeom)
            staticGeom.findAllMatches('*').reparentTo(self.ship.mediumStatic)
            staticGeom.detachNode()
            numPanels = hull.findAllMatches('**/panel_High_*').getNumPaths()
            for i in range(numPanels):
                panel = hull.find('**/panel_High_%s' % i)
                self.panelsMed.append(panel)
                self.projScreensNodePaths[i] = panel.getParent()
                self.projScreens[i] = panel.getParent().node()
            
            self.geom_Medium.flattenStrong()
            for i in range(len(self.panelsMed)):
                panel = self.panelsMed[i]
                panelGeom = panel.getChild(0)
                panelGeom.setName('panel_Medium_%d' % i)
                panelGeom.reparentTo(self.projScreensNodePaths[i])
                panelGeom.node().setPreserved(True)
                panel.detachNode()
                self.panelsMed[i] = panelGeom
                panelGeom.setTransparency(1)
            
            self.initDestruction()
        else:
            self.geom_Medium = NodePath('hull-geom')

    def unloadMedium(self):
        if not self.geom_Medium:
            return
        
        if self.geom_Medium.isEmpty():
            return
        
        if not self.panelsMed:
            return
        
        self.geom_Medium.removeNode()
        self.geom_Medium = None
        self.panelsMed = []
        self.flashPanelMed = {}
    
    def loadLow(self):
        filePrefix = self.getPrefix(self.dna.cabinType)
        (result, data) = ShipGlobals.getShipGeom('%s-geometry_Low' % filePrefix)
        if result:
            hull = data[0].copyTo(hidden)
            self.geom_Low = hull
            lodScale = ShipGlobals.getLowLODScale(self.dna.modelClass)
            self.geom_Low.setScale(lodScale)
            lodPosOffset = ShipGlobals.getLowLODPosOffset(self.dna.modelClass)
            self.geom_Low.setPos(self.geom_Low.getPos() + lodPosOffset)
            self.changeColor(self.geom_Low)
            self.geom_Low.flattenStrong()
            self.geom_Low.findAllMatches('**/+GeomNode').reparentTo(self.ship.lowStatic)
        else:
            self.geom_Low = NodePath('hull_geom')

    def unloadLow(self):
        if not self.geom_Low:
            return
        
        if self.geom_Low.isEmpty():
            return
        
        if not self.panelsLow:
            return
        
        self.geom_Low.removeNode()
        self.geom_Low = None
        self.panelsLow = []
        self.flashPanelLow = {}
    
    def loadCollisions(self):
        if config.GetBool('disable-ship-geom', 0):
            return
        
        if self.collisions and self.prop or self.isEmpty():
            return
        
        filePrefix = self.getPrefix(self.dna.cabinType)
        self.collisions = loader.loadModelCopy(filePrefix + '-collisions')
        if not self.collisions:
            return
        
        self.collisions.reparentTo(self.propCollisions)
        numPanels = self.collisions.findAllMatches('**/collision_panel_*').getNumPaths()
        for i in range(numPanels):
            self.collPanels.append(self.collisions.find('**/collision_panel_' + str(i)))
        
        if self.ship:
            self.setupCollisions(self.ship)

    def unloadCollisions(self):
        if not self.collisions:
            return
        
        if self.collisions.isEmpty():
            return
        
        self.collisions.removeNode()
        self.collisions = None
        self.collPanels = []

    def getPrefix(self, shipClass):
        filePrefix = CabinDNA.CabinDict.get(shipClass)
        return filePrefix
    
    def setupCollisions(self, ship = None):
        if config.GetBool('disable-ship-geom', 0):
            return

        def setCannonballTags(collNode):
            collNode.setTag('objType', str(PiratesGlobals.COLL_SHIPPART))
            collNode.setTag('hullCode', str(255))
            collNode.setTag('shipId', str(self.shipId))
            collNode.setTag('propId', str(self.doId))

        self.floors = self.collisions.find('**/collision_floors')
        if not self.floors.isEmpty():
            self.floors.flattenStrong()
            collideMask = self.floors.getCollideMask()
            collideMask ^= PiratesGlobals.FloorBitmask
            collideMask |= PiratesGlobals.ShipFloorBitmask
            self.floors.setCollideMask(collideMask)
        
        collNodes = self.collisions.findAllMatches('**/collision_floors/*')
        for i in range(0, collNodes.getNumPaths()):
            if ship:
                collNodes[i].setName(ship.deckName)
            
            setCannonballTags(collNodes[i])
            collNodes[i].setTag('hullCode', str(255))
            collNodes[i].setTag('objType', '9')
            self.addTargetableCollision(collNodes[i])
        
        self.floors = self.collisions.find('**/collision_floors')
        if not self.floors.isEmpty():
            self.floors.flattenStrong()
        
        self.railing = self.collisions.find('**/collision_railing')
        if not self.railing.isEmpty():
            self.railing.flattenStrong()
            collideMask = self.railing.getCollideMask()
            collideMask ^= PiratesGlobals.FloorBitmask
            collideMask |= PiratesGlobals.ShipFloorBitmask
            self.railing.setCollideMask(collideMask)
            self.railing.setTag('floorType', str(PiratesGlobals.COLL_EXIT))
            if ship:
                self.railing.setName(ship.railingName)
            
            setCannonballTags(self.railing)
            self.railing.setTag('hullCode', str(255))
            self.addTargetableCollision(self.railing)
        
        collNode = self.collisions.find('**/collision_walls')
        if not collNode.isEmpty():
            setCannonballTags(collNode)
            collNode.setTag('hullCode', str(255))
            self.addTargetableCollision(collNode)
        
        collNode = self.collisions.find('**/collision_cannoncoll')
        if not collNode.isEmpty():
            setCannonballTags(collNode)
            collNode.setTag('hullCode', str(255))
            self.addTargetableCollision(collNode)
        
        for i in range(len(self.collPanels)):
            setCannonballTags(self.collPanels[i])
            self.collPanels[i].setTag('hullCode', str(i + 1))
            self.addTargetableCollision(self.collPanels[i])
        
        if base.localAvatar and base.localAvatar.ship:
            if base.localAvatar.ship != self.ship:
                self.stashFloorCollisions()
            
        else:
            self.stashFloorCollisions()
        self.setTargetBitmask(1)
    
    def stashFloorCollisions(self):
        return
        if self.railing:
            if not self.railing.isEmpty():
                self.railing.stash()
        
        if self.floors:
            if not self.floors.isEmpty():
                self.floors.stash()

    def unstashFloorCollisions(self):
        return
        if self.railing:
            if not self.railing.isEmpty():
                self.railing.unstash()

        if self.floors:
            if not self.floors.isEmpty():
                self.floors.unstash()

    def stashDetailCollisions(self):
        if self.details:
            if not self.details.isEmpty():
                self.details.stash()

    def unstashDetailCollisions(self):
        if self.details:
            if not self.details.isEmpty():
                self.details.unstash()

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker):
        if localAvatar.ship == self.ship:
            sfx = random.choice(self.woodBreakSfx)
            base.playSfx(sfx, node = self.ship, cutoff = 2000)
        else:
            sfx = random.choice(self.distantBreakSfx)
            base.playSfx(sfx, node = self.ship, cutoff = 2000)
        (cannonCode, hullCode, sailCode) = codes
        if hullCode != 255:
            index = hullCode - 1
            self.playHoleSplat(pos, normal, index)
    
    def respawn(self):
        self.resetDestruction(0)
        self.resetDestruction(1)

    def addCannon(self, cannon):
        cannonPost = self.find('**/cannon_%s;+s' % cannon.cannonIndex)
        cannon.setPos(cannonPost.getPos())
        cannon.setHpr(cannonPost.getHpr())
        cannon.setScale(cannonPost.getScale())
        cannon.reparentTo(self.prop)
    
    def addToShip(self):
        ShipPart.ShipPart.addToShip(self)
        self.propCollisions.reparentTo(self.ship.modelCollisions)

