import random
from pirates.piratesbase.PiratesGlobals import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from pirates.piratesbase import PiratesGlobals
from direct.distributed import DistributedObject
from pirates.piratesbase import PLocalizer
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.battle import CannonGlobals
from pirates.battle import WeaponGlobals
from pirates.shipparts import DecorDNA
from pirates.shipparts import Lantern
from pirates.shipparts import ShipDecor
from pirates.shipparts import Window
from pirates.shipparts import DistributedShippart
from pirates.destructibles import DistributedDestructibleObject

class DistributedShipDecor(DistributedShippart.DistributedShippart, DistributedDestructibleObject.DistributedDestructibleObject):
    notify = directNotify.newCategory('DistributedShipDecor')
    
    def __init__(self, cr):
        DistributedShippart.DistributedShippart.__init__(self, cr)
        DistributedDestructibleObject.DistributedDestructibleObject.__init__(self, cr)
        NodePath.__init__(self, 'shipDecor')
    
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
            self.prop.showBrokenState()
    
    def createProp(self):
        decorClass = DecorDNA.getDecorType(self.dna.decorType)
        self.decorClass = decorClass
        decorIndex = DecorDNA.DecorDict[self.dna.decorType][1]
        self.decorIndex = decorIndex
        decor = self.ship.decors[decorIndex].get(self.dna.posIndex, 0)
        if decor:
            if decor[0]:
                self.prop = decor[0]
                self.ship.decors[decorIndex][self.dna.posIndex][1] = self
                return

        if decorClass == 'lantern':
            self.prop = Lantern.Lantern()
        elif decorClass == 'decoration':
            self.prop = ShipDecor.ShipDecor()
        elif decorClass == 'window':
            self.prop = Window.Window()
        
        self.prop.shipId = self.shipId
        self.prop.doId = self.doId
        self.ship.decors[decorIndex][self.dna.posIndex] = [
            self.prop,
            self]

    def disable(self):
        self.notify.debug('Disable ' + str(self.doId))
        DistributedShippart.DistributedShippart.disable(self)
        DistributedDestructibleObject.DistributedDestructibleObject.disable(self)
    
    def delete(self):
        self.notify.debug('Delete ' + str(self.doId))
        if self.ship.decors[self.decorIndex].get(self.dna.posIndex, 0):
            self.ship.decors[self.decorIndex][self.dna.posIndex][0].delete()
            self.ship.decors[self.decorIndex][self.dna.posIndex][1] = None
            del self.ship.decors[self.decorIndex][self.dna.posIndex]
        
        del self.dna
        DistributedShippart.DistributedShippart.delete(self)
        DistributedDestructibleObject.DistributedDestructibleObject.delete(self)

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker):
        self.prop.projectileWeaponHit(skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker)
    
    def playDeath(self):
        if self.prop:
            self.prop.death()
    
    def respawn(self):
        if self.prop:
            self.prop.respawn()

    def setDefaultDNA(self):
        newDNA = DecorDNA.DecorDNA()
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

    def setDecorType(self, val):
        self.dna.setDecorType(val)

    def setPosIndex(self, val):
        self.dna.setPosIndex(val)

    def setColorIndex(self, val):
        self.dna.setColorIndex(val)
    
    def addPropToShip(self):
        decorPlacement = DecorDNA.DecorDict.get(self.dna.decorType)
        if decorPlacement[1] == DecorDNA.WALL:
            locator = self.ship.locators.find('**/wall_decor_' + str(self.dna.posIndex) + ';+s')
        elif decorPlacement[1] == DecorDNA.FLOOR:
            locator = self.ship.locators.find('**/floor_decor_' + str(self.dna.posIndex) + ';+s')
        elif decorPlacement[1] == DecorDNA.WINDOW:
            locator = self.ship.locators.find('**/window_' + str(self.dna.posIndex) + ';+s')
        
        self.prop.propCollisions.reparentTo(self.ship.modelCollisions)
        self.prop.propCollisions.setPos(locator.getPos(self.ship.root))
        self.prop.propCollisions.setHpr(locator.getHpr(self.ship.root))
        self.prop.propCollisions.setScale(locator.getScale(self.ship.root))
        self.prop.propCollisions.flattenStrong()
        self.prop.geom_High.setPos(locator.getPos(self.ship.root))
        self.prop.geom_High.setHpr(locator.getHpr(self.ship.root))
        self.prop.geom_High.setScale(locator.getScale(self.ship.root))
        self.prop.geom_Medium.setPos(locator.getPos(self.ship.root))
        self.prop.geom_Medium.setHpr(locator.getHpr(self.ship.root))
        self.prop.geom_Medium.setScale(locator.getScale(self.ship.root))
        self.prop.addToShip()

