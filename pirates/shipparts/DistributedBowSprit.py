from direct.showbase.PythonUtil import quickProfile
from pirates.piratesbase.PiratesGlobals import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.ship import ShipGlobals
from pirates.battle import CannonGlobals
from pirates.battle import WeaponGlobals
from pirates.shipparts import BowSpritDNA
from pirates.shipparts import BowSprit
from pirates.shipparts import DistributedShippart
from pirates.destructibles import DistributedDestructibleObject

class DistributedBowSprit(DistributedShippart.DistributedShippart, DistributedDestructibleObject.DistributedDestructibleObject):
    notify = directNotify.newCategory('DistributedBowSprit')
    
    def __init__(self, cr):
        DistributedShippart.DistributedShippart.__init__(self, cr)
        DistributedDestructibleObject.DistributedDestructibleObject.__init__(self, cr)
        NodePath.__init__(self, 'bowsprit')
        self.stats = None
        self.hull = None
    
    def generate(self):
        self.notify.debug('Generate ' + str(self.doId))
        self.setDefaultDNA()
        DistributedShippart.DistributedShippart.generate(self)
        DistributedDestructibleObject.DistributedDestructibleObject.generate(self)
    
    def announceGenerate(self):
        self.notify.debug('Announce Generate ' + str(self.doId))
        DistributedShippart.DistributedShippart.announceGenerate(self)
        DistributedDestructibleObject.DistributedDestructibleObject.announceGenerate(self)
        if self.Hp <= 0:
            self.prop.hideBreakAll()
        else:
            breakThreshold = self.maxHp / self.prop.numBreaks
            for i in range(self.prop.numBreaks):
                if self.Hp < breakThreshold * i:
                    self.prop.hideBreak()
    
    def disable(self):
        self.notify.debug('Disable ' + str(self.doId))
        DistributedShippart.DistributedShippart.disable(self)
        DistributedDestructibleObject.DistributedDestructibleObject.disable(self)
    
    def delete(self):
        self.notify.debug('Delete ' + str(self.doId))
        isRam = self.dna.prowIsRam(self.dna.prowType)
        if isRam:
            if self.ship.ram:
                self.ship.ram[1] = None
            
        elif self.ship.bowsprit:
            self.ship.bowsprit[1] = None
        
        del self.dna
        DistributedShippart.DistributedShippart.delete(self)
        DistributedDestructibleObject.DistributedDestructibleObject.delete(self)
    
    def createProp(self):
        isRam = self.dna.prowIsRam(self.dna.prowType)
        if isRam:
            bowsprit = self.ship.ram
        else:
            bowsprit = self.ship.bowsprit
        if bowsprit:
            if bowsprit[0]:
                self.prop = bowsprit[0]
                if isRam:
                    self.ship.ram[1] = self
                else:
                    self.ship.bowsprit[1] = self
                return

        self.prop = BowSprit.BowSprit()
        self.prop.shipId = self.shipId
        self.prop.isAlive = 1
        if isRam:
            self.ship.ram = [self.prop, self]
            self.prop.hideDebris = 1
        else:
            self.ship.bowsprit = [self.prop, self]

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker):
        self.prop.projectileWeaponHit(skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker)

    def setHp(self, newHp):
        DistributedDestructibleObject.DistributedDestructibleObject.setHp(self, newHp)
        if self.ship:
            if self.dna.prowIsRam(self.dna.prowType):
                messenger.send('setRamHp-%s' % self.ship.doId, self.getHp())
            else:
                messenger.send('setBowspritHp-%s' % self.ship.doId, self.getHp())

    def getHp(self):
        return [self.Hp, self.maxHp]

    def playDeath(self):
        pass

    def respawn(self):
        pass

    def loadStats(self):
        if self.stats:
            return

    def setDefaultDNA(self):
        newDNA = BowSpritDNA.BowSpritDNA()
        self.setDNA(newDNA)

    def setDNA(self, dna):
        if self.dna:
            self.updateDNA(dna)
        else:
            self.dna = dna

    def updateDNA(self, newDNA, fForce=0):
        oldDna = self.dna
        self.dna = newDNA

    def setBaseTeam(self, val):
        self.dna.setBaseTeam(val)

    def setProwType(self, val):
        self.dna.setProwType(val)
        self.loadStats()

    def setPosIndex(self, val):
        self.dna.setPosIndex(val)

    def setColorIndex(self, val):
        self.dna.setColorIndex(val)
    
    def addPropToShip(self):
        if self.dna.prowIsRam(self.dna.prowType):
            locator = self.ship.locators.find('**/location_ram;+s')
        else:
            locator = self.ship.locators.find('**/location_bowsprit;+s')
        self.prop.addToShip()
        lpos = locator.getPos(self.ship.root)
        lhpr = locator.getHpr(self.ship.root)
        lscl = locator.getScale(self.ship.root)
        self.prop.geom_High.setPos(lpos)
        self.prop.geom_Medium.setPos(lpos)
        self.prop.geom_Low.setPos(lpos)
        self.prop.geom_High.setHpr(lhpr)
        self.prop.geom_Medium.setHpr(lhpr)
        self.prop.geom_Low.setHpr(lhpr)
        self.prop.geom_High.setScale(lscl)
        self.prop.geom_Medium.setScale(lscl)
        self.prop.geom_Low.setScale(lscl)
        if self.ship:
            if self.dna.prowIsRam(self.dna.prowType):
                messenger.send('setRamHp-%s' % self.ship.doId, [self.Hp, self.maxHp])
            else:
                messenger.send('setBowspritHp-%s' % self.ship.doId, [self.Hp, self.maxHp])


