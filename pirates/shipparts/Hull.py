import random
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.PythonUtil import report
from pandac.PandaModules import *
from pirates.piratesbase.PiratesGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.ship import ShipGlobals
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.Fire import Fire
from pirates.effects.Flame import Flame
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.WoodShards import WoodShards
from pirates.effects.MuzzleFlash import MuzzleFlash
from pirates.effects.DarkShipFog import DarkShipFog
from pirates.battle import CannonGlobals
from pirates.battle import WeaponGlobals
from pirates.shipparts import HullDNA
from pirates.shipparts import SplattableObject
from pirates.shipparts import ShipPart
from pirates.uberdog.UberDogGlobals import InventoryType

class Hull(SplattableObject.SplattableObject, ShipPart.ShipPart):
    notify = directNotify.newCategory('Hull')
    
    def __init__(self, ship, cr):
        self.cr = cr
        SplattableObject.SplattableObject.__init__(self)
        ShipPart.ShipPart.__init__(self)
        NodePath.__init__(self, 'Hull')
        self.collisions = None
        self.locators = None
        self.floors = None
        self.deck = None
        self.railing = None
        self.details = None
        self.fogEffect = None
        self.ship = ship
        self.breakLevel = {}
        self.breakLevel[0] = 100
        self.listingThreshold = 2
        self.listingIncrement = 5
        self.waterIntakeThreshold = 2
        self.waterIntakeIncrement = 7
        self.leftDamageLvl = 0
        self.rightDamageLvl = 0
        self.propCollisions = NodePath('Collisions-Hull')

    def disable(self):
        SplattableObject.SplattableObject.disable(self)
        ShipPart.ShipPart.disable(self)

    def delete(self):
        SplattableObject.SplattableObject.delete(self)
        ShipPart.ShipPart.destroy(self)
        if self.fogEffect:
            self.fogEffect.destroy()
            self.fogEffect = None
        
        del self.leftDamageLvl
        del self.rightDamageLvl
    
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
        filePrefix = self.getPrefix(self.dna.modelClass)
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
            for i in xrange(numPanels):
                panel = hull.find('**/panel_High_%s' % i)
                self.panelsHigh.append(panel)
            
            self.geom_High.flattenStrong()
            for i in range(len(self.panelsHigh)):
                panel = self.panelsHigh[i]
                panelGeom = panel.getChild(0)
                panelGeom.setName('panel_High_%d' % i)
                panelGeom.reparentTo(self.geom_High)
                panelGeom.node().setPreserved(True)
                panel.detachNode()
                self.panelsHigh[i] = panelGeom
            
        else:
            self.geom_High = NodePath('Hull-model')
        if __dev__ and base.config.GetBool('show-ship-lods', 0):
            s = loader.loadModelCopy('models/effects/explosion_sphere')
            s.reparentTo(self.geom_High)
            s.setColorScale(1, 0, 0, 1)
            s.setScale(30)
            s.setZ(250)

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
        filePrefix = self.getPrefix(self.dna.modelClass)
        (result, data) = ShipGlobals.getShipGeom('%s-geometry_Medium' % filePrefix)
        if result:
            (geom, static) = data
            hull = geom.copyTo(hidden)
            self.geom_Medium = hull
            staticGeom = static.copyTo(hidden)
            self.changeColor(self.geom_Medium)
            self.changeColor(staticGeom)
            staticGeom.findAllMatches('*').reparentTo(self.ship.mediumStatic)
            staticGeom.detachNode()
            numPanels = hull.findAllMatches('**/panel_High_*').getNumPaths()
            for i in xrange(numPanels):
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
            
            self.initDestruction()
            if __dev__ and base.config.GetBool('show-ship-lods', 0):
                s = loader.loadModelCopy('models/effects/explosion_sphere')
                s.reparentTo(self.geom_Medium)
                s.setColorScale(0, 1, 0, 1)
                s.setScale(30)
                s.setZ(250)
            
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

    def requestLow(self):
        return self.geom_Low
    
    def loadLow(self):
        filePrefix = self.getPrefix(self.dna.modelClass)
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
            self.geom_Low.findAllMatches('**/+GeomNode').reparentTo(self.geom_Low)
            self.geom_Low.findAllMatches('**/+ModelNode').detach()
        else:
            self.geom_Low = NodePath('hull_geom')
        if __dev__ and base.config.GetBool('show-ship-lods', 0):
            s = loader.loadModelCopy('models/effects/explosion_sphere')
            s.reparentTo(self.geom_Low)
            s.setColorScale(0, 0, 1, 1)
            s.setScale(30)
            s.setZ(250)

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
    
    def loadCollisions(self):
        if config.GetBool('disable-ship-geom', 0):
            return
        
        filePrefix = self.getPrefix(self.dna.modelClass)
        self.collisions = loader.loadModelCopy(filePrefix + '-collisions')
        if not self.collisions:
            return
        
        self.collisions.reparentTo(self.propCollisions)
        numPanels = self.collisions.findAllMatches('**/collision_panel_*').getNumPaths()
        for i in range(numPanels):
            self.collPanels.append(self.collisions.find('**/collision_panel_' + str(i)))
        
        if self.ship:
            self.setupCollisions(self.ship)
        
        colls = []
        edgeRoot = self.collisions.find('**/collision_inside_edge')
        if edgeRoot != edgeRoot.notFound():
            colls += edgeRoot.getChildrenAsList()
        
        deckRoot = self.collisions.find('**/collision_deck')
        if deckRoot != deckRoot.notFound():
            colls += deckRoot.getChildrenAsList()
        
        for coll in colls:
            coll.stash()
        
        bound = self.collisions.getBounds()
        for coll in colls:
            coll.unstash()
        
        for coll in colls:
            coll.node().setBounds(bound)
    
    def unloadCollisions(self):
        if not self.collisions:
            return
        
        if self.collisions.isEmpty():
            return
        
        self.collisions.removeNode()
        self.collisions = None
        self.collPanels = []
        self.clearTargetableCollisions()
    
    def getPrefix(self, shipClass):
        filePrefix = HullDNA.HullDict.get(shipClass)
        return filePrefix

    def getFlatPrefix(self, shipClass):
        filePrefix = HullDNA.HullFlatDict.get(shipClass)
        return filePrefix
    
    def setupCollisions(self, ship = None):
        if config.GetBool('disable-ship-geom', 0):
            return

        def setCannonballTags(collNode):
            collNode.setTag('objType', str(PiratesGlobals.COLL_SHIPPART))
            collNode.setTag('shipId', str(self.shipId))
            collNode.setTag('propId', str(self.doId))

        self.floors = self.collisions.find('**/collision_floors')
        if not self.floors.isEmpty():
            self.floors.flattenStrong()
            collideMask = self.floors.getCollideMask()
            collideMask ^= PiratesGlobals.FloorBitmask
            collideMask |= PiratesGlobals.ShipFloorBitmask
            self.floors.setCollideMask(collideMask)
        
        self.deck = self.collisions.find('**/collision_deck')
        if not self.deck.isEmpty():
            collideMask = self.floors.getCollideMask()
            collideMask ^= PiratesGlobals.FloorBitmask
            collideMask |= PiratesGlobals.ShipFloorBitmask
            self.deck.setCollideMask(collideMask)
        
        collNodes = self.collisions.findAllMatches('**/collision_floors/*')
        for i in range(collNodes.getNumPaths()):
            if ship:
                collNodes[i].setName(ship.deckName)
            
            setCannonballTags(collNodes[i])
            collNodes[i].setTag('hullCode', str(255))
            collNodes[i].setTag('objType', '9')
            self.addTargetableCollision(collNodes[i])
        
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
        
        shipCollWall = self.collisions.find('**/collision_hull')
        if not shipCollWall.isEmpty():
            shipCollWall.setCollideMask(PiratesGlobals.ShipCollideBitmask)
            shipCollWall.setTag('objType', str(PiratesGlobals.COLL_SHIP))
            if self.ship:
                shipCollWall.setTag('shipId', str(self.ship.doId))

        self.shipInsideWall = self.collisions.find('**/collision_inside_edge')
        for i in range(len(self.collPanels)):
            setCannonballTags(self.collPanels[i])
            self.collPanels[i].setTag('hullCode', str(i + 1))
            self.addTargetableCollision(self.collPanels[i])
        
        if self.dna.shipClass == ShipGlobals.DINGHY:
            self.prop.setBin('background', 195)
            clippingPlane = self.prop.find('**/water_clipping_plane')
            if not clippingPlane.isEmpty():
                clippingPlane.setBin('background', 199)

        if hasattr(base, 'localAvatar') and base.localAvatar:
            if base.localAvatar.ship:
                if base.localAvatar.ship != self.ship:
                    self.stashFloorCollisions()
                
            else:
                self.stashFloorCollisions()
        
        self.setTargetBitmask(1)
        self.stashPlaneCollisions()
    
    def enableInsideWall(self, isOn):
        if not self.shipInsideWall.isEmpty():
            if isOn:
                self.shipInsideWall.unstash()
            else:
                self.shipInsideWall.stash()

    def getInsideWallName(self):
        if self.shipInsideWall:
            return self.shipInsideWall.getName()
        
        return ''
    
    def stashPlaneCollisions(self):
        if not self.deck.isEmpty():
            self.deck.stash()
        
        if not self.shipInsideWall.isEmpty():
            self.shipInsideWall.stash()
    
    def unstashPlaneCollisions(self):
        if not self.deck.isEmpty():
            self.deck.unstash()
        
        if not self.shipInsideWall.isEmpty():
            self.shipInsideWall.unstash()

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
        if self.ship.invulnerable():
            return
        
        if localAvatar.ship == self.ship:
            sfx = random.choice(self.woodBreakSfx)
            base.playSfx(sfx, node = self.ship, cutoff = 3000)
        else:
            sfx = random.choice(self.distantBreakSfx)
            base.playSfx(sfx, node = self.ship, cutoff = 3500)
        (cannonCode, hullCode, sailCode) = codes
        if hullCode != 255:
            index = hullCode - 1
            if index > 0:
                index = (index - 1) % 2 + 1
            
            self.playHoleSplat(pos, normal, index)
            if len(self.panelsMed) > index and len(self.panelsHigh) > index:
                self.copyMultitexLayer(self.panelsMed[index], self.panelsHigh[index])

    def death(self, index = None):
        panelIndex = self.getPanelIndex(index)
        if self.panelsHigh[panelIndex] != None:
            self.notify.debug('SECTION CRIPPLE ' + str(index))
            self.playBreak(panelIndex, index)
            if len(self.panelsMed) > panelIndex and len(self.panelsHigh) > panelIndex:
                self.copyMultitexLayer(self.panelsMed[panelIndex], self.panelsHigh[panelIndex])

    def respawn(self, index):
        self.resetDestruction(index)

    def respawnAll(self):
        for i in range(len(self.panelsHigh)):
            self.respawn(i)

    def getPanelIndex(self, index):
        if index > 0:
            index = index % 2
            if index == 0:
                index = 2
        
        return index
    
    def getClosestBoardingPos(self):
        return self.ship.getClosestBoardingPos()
    
    def startDarkFog(self, offset = None):
        self.fogEffect = DarkShipFog.getEffect()
        if self.fogEffect:
            self.fogEffect.reparentTo(self)
            if offset:
                self.fogEffect.setY(self.fogEffect, offset)
            
            self.fogEffect.setZ(self.fogEffect, 50)
            self.fogEffect.startLoop()

    def stopDarkFog(self):
        if self.fogEffect:
            self.fogEffect.stopLoop()
            self.fogEffect = None

    def addToShip(self):
        self.propCollisions.reparentTo(self.ship.modelCollisions)
        ShipPart.ShipPart.addToShip(self)

