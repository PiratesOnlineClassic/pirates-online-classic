from pirates.piratesbase.PiratesGlobals import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from pirates.piratesbase import PiratesGlobals
from direct.distributed import DistributedObject
from pirates.piratesbase import PLocalizer
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.ship import ShipGlobals
from pirates.battle import CannonGlobals
from pirates.battle import WeaponGlobals
from direct.showbase.PythonUtil import quickProfile
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.Fire import Fire
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.MuzzleFlash import MuzzleFlash
from pirates.effects.WoodShards import WoodShards
from pirates.shipparts import CabinDNA
from pirates.shipparts import Cabin
from pirates.shipparts import DistributedShippart
from pirates.destructibles import DistributedDestructibleObject
import random

class DistributedCabin(DistributedShippart.DistributedShippart, DistributedDestructibleObject.DistributedDestructibleObject):
    notify = directNotify.newCategory('DistributedCabin')
    woodBreakSfx = None

    def __init__(self, cr):
        DistributedShippart.DistributedShippart.__init__(self, cr)
        DistributedDestructibleObject.DistributedDestructibleObject.__init__(self, cr)
        NodePath.__init__(self, 'DistributedCabin')
        self.shipId = 0
        self.doId = 0
        self.hull = None
        self.decors = []
        self.pendingSetupCollisions = None

    def generate(self):
        self.notify.debug('Generate ' + str(self.doId))
        self.setDefaultDNA()
        DistributedShippart.DistributedShippart.generate(self)
        DistributedDestructibleObject.DistributedDestructibleObject.generate(self)

    def announceGenerate(self):
        self.notify.debug('Announce Generate ' + str(self.doId))
        DistributedShippart.DistributedShippart.announceGenerate(self)
        DistributedDestructibleObject.DistributedDestructibleObject.announceGenerate(self)

    def createProp(self):
        cabin = self.ship.cabin
        if cabin:
            if cabin[0]:
                self.prop = cabin[0]
                self.ship.cabin[1] = self
                return

        self.prop = Cabin.Cabin(base.cr)
        self.prop.shipId = self.shipId
        self.prop.doId = self.doId
        self.ship.cabin = [self.prop, self]

    def propLoaded(self):
        pass

    def disable(self):
        self.notify.debug('Disable ' + str(self.doId))
        if self.pendingSetupCollisions:
            base.cr.relatedObjectMgr.abortRequest(self.pendingSetupCollisions)
            self.pendingSetupCollisions = None

        DistributedShippart.DistributedShippart.disable(self)
        DistributedDestructibleObject.DistributedDestructibleObject.disable(self)

    def delete(self):
        self.notify.debug('Delete ' + str(self.doId))
        if self.ship.cabin:
            self.ship.cabin[1] = None

        del self.dna
        DistributedShippart.DistributedShippart.delete(self)
        DistributedDestructibleObject.DistributedDestructibleObject.delete(self)

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker):
        self.prop.projectileWeaponHit(skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker)

    def setHp(self, newHp):
        DistributedDestructibleObject.DistributedDestructibleObject.setHp(self, newHp)
        if self.ship:
            messenger.send('setCabinHp-%s' % self.doId, self.getHp())

    def getHp(self):
        return [self.Hp, self.maxHp]

    def playDeath(self):
        pass

    def respawn(self):
        if self.prop:
            self.prop.respawn()

    def stashFloorCollisions(self):
        if self.prop:
            self.prop.stashFloorCollisions()

    def unstashFloorCollisions(self):
        if self.prop:
            self.prop.unstashFloorCollisions()

    def attachCannon(self, cannon):
        self.prop.addCannon(cannon)
        myParent = base.cr.doId2do.get(self.shipId)
        myParent.cannons.append(cannon)

    def setDefaultDNA(self):
        newDNA = CabinDNA.CabinDNA()
        self.setDNA(newDNA)

    def setDNA(self, dna):
        if self.dna:
            self.updateDNA(dna)
        else:
            self.dna = dna

    def updateDNA(self, newDNA, fForce = 0):
        oldDna = self.dna
        self.dna = newDNA

    def setShipClass(self, val):
        self.dna.setShipClass(val)

    def setBaseTeam(self, val):
        self.dna.setBaseTeam(val)

    def setCabinType(self, val):
        self.dna.setCabinType(val)

    def setHullTextureIndex(self, val):
        self.dna.setHullTextureIndex(val)

    def setStripeTextureIndex(self, val):
        self.dna.setStripeTextureIndex(val)

    def setPatternTextureIndex(self, val):
        self.dna.setPatternTextureIndex(val)

    def setHullColorIndex(self, val):
        self.dna.setHullColorIndex(val)

    def setStripeColorIndex(self, val):
        self.dna.setStripeColorIndex(val)

    def setPatternColorIndex(self, val):
        self.dna.setPatternColorIndex(val)

    def setHullHilightColorIndex(self, val):
        self.dna.setHullHilightColorIndex(val)

    def setStripeHilightColorIndex(self, val):
        self.dna.setStripeHilightColorIndex(val)

    def setPatternHilightColorIndex(self, val):
        self.dna.setPatternHilightColorIndex(val)

    def setMastConfig(self, val):
        self.dna.setMastConfig(val)

    def setCannonConfig(self, val):
        self.dna.setCannonConfig(val)

    def setWallDecorConfig(self, val):
        self.dna.setWallDecorConfig(val)

    def setFloorDecorConfig(self, val):
        self.dna.setFloorDecorConfig(val)

    def setWindowConfig(self, val):
        self.dna.setWindowConfig(val)

    def setMaxCargo(self, maxCargo):
        self.maxCargo = maxCargo
