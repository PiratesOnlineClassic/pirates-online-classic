from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.actor import Actor
from pandac.PandaModules import *
from pirates.piratesbase.PiratesGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.shipparts import BowSpritDNA
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.Fire import Fire
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.battle import CannonGlobals
from pirates.battle import WeaponGlobals
from pirates.shipparts import ShipPart
from pirates.ship import ShipGlobals

class BowSprit(NodePath, ShipPart.ShipPart):
    notify = directNotify.newCategory('BowSprit')
    
    def __init__(self):
        ShipPart.ShipPart.__init__(self)
        NodePath.__init__(self, 'bowsprit')
        self.rotateMin = 360
        self.rotateMax = 720
        self.texture = None
    
    def disable(self):
        ShipPart.ShipPart.disable(self)
    
    def delete(self):
        ShipPart.ShipPart.destroy(self)
        del self.dna
        self.clearTargetableCollisions()

    def loadModel(self, dna):
        if config.GetBool('disable-ship-geom', 0):
            return
        
        if self.prop:
            return
        
        self.dna = dna
        filePrefix = self.getPrefix(self.dna.prowType)
        self.geom_High = loader.loadModel('%s_hi' % filePrefix)
        self.geom_Medium = loader.loadModel('%s_hi' % filePrefix)
        self.geom_Low = loader.loadModel('%s_hi' % filePrefix)
        self.controls = []
        self.numBreaks = 1
        self.propCollisions = NodePath(ModelNode('BowSprit-%d' % self.doId))
        self.setTargetBitmask(1)
        self.loaded = True

    def unloadModel(self):
        self.removeNode()

    def findDebris(self):
        self.break1High = self.controls
        self.break2High = [self.geom_High]
        self.break1Med = None
        self.break2Med = None
        self.break1Low = None
        self.break2Low = None

    def getDebrisParent(self):
        return render

    def getPrefix(self, shipClass):
        filePrefix = BowSpritDNA.BowSpritDict.get(shipClass)
        return filePrefix
    
    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker):
        pass

    def death(self):
        pass
    
    def respawn(self):
        if not self.isAlive:
            self.isAlive = 1
    
    def addToShip(self):
        self.propCollisions.reparentTo(self.ship.modelCollisions)
        ShipPart.ShipPart.addToShip(self)

