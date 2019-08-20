import copy
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.distributed import DistributedObject
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.actor import Actor
from direct.showbase.PythonUtil import quickProfile
from pirates.piratesbase.PiratesGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.ship import ShipGlobals
from pirates.battle import CannonGlobals
from pirates.battle import WeaponGlobals
from pirates.shipparts import MastDNA
from pirates.shipparts import Mast
from pirates.shipparts import DistributedShippart
from pirates.destructibles import DistributedDestructibleArray

class DistributedMast(DistributedShippart.DistributedShippart, DistributedDestructibleArray.DistributedDestructibleArray, DirectObject.DirectObject):
    notify = directNotify.newCategory('DistributedMast')
    
    def __init__(self, cr):
        self.cr = cr
        DistributedShippart.DistributedShippart.__init__(self, cr)
        DistributedDestructibleArray.DistributedDestructibleArray.__init__(self, cr)
        NodePath.__init__(self, 'DistributedMast')
        self.stats = None

    def generate(self):
        self.notify.debug('Generate ' + str(self.doId))
        self.setDefaultDNA()
        DistributedShippart.DistributedShippart.generate(self)
        DistributedDestructibleArray.DistributedDestructibleArray.generate(self)

    def announceGenerate(self):
        self.notify.debug('Announce Generate ' + str(self.doId))
        DistributedShippart.DistributedShippart.announceGenerate(self)
        DistributedDestructibleArray.DistributedDestructibleArray.announceGenerate(self)
        breakPoint = -1
        for i in range(len(self.arrayHp)):
            if self.arrayHp[i] <= 0:
                for j in range(i, len(self.arrayHp)):
                    self.prop.mastsState[j] = 1
                break
            else:
                self.prop.mastsState[i] = 0

        self.prop.setupMast()
        self.setFlagDNAString(self.ship.getFlagDNAString())

    def createProp(self):
        mast = self.ship.masts.get(self.dna.posIndex, 0)
        if mast:
            if mast[0]:
                self.prop = mast[0]
                self.ship.masts[self.dna.posIndex][1] = self
                return
        
        self.prop = Mast.Mast(self.ship, self.cr)
        self.prop.shipId = self.shipId
        self.prop.doId = self.doId
        self.ship.masts[self.dna.posIndex] = [
            self.prop,
            self]

    def disable(self):
        self.notify.debug('Disable ' + str(self.doId))
        DistributedShippart.DistributedShippart.disable(self)
        DistributedDestructibleArray.DistributedDestructibleArray.disable(self)

    def delete(self):
        self.notify.debug('Delete ' + str(self.doId))
        if self.ship.masts.get(self.dna.posIndex, 0):
            self.ship.masts[self.dna.posIndex][1] = None
        
        del self.dna
        if base.cr.config.GetBool('want-ship-hpdisplay', 0) is 1:
            self.destroyHpDisplay()
        
        DistributedShippart.DistributedShippart.delete(self)
        DistributedDestructibleArray.DistributedDestructibleArray.delete(self)

    def getFlagDNAString(self):
        return self.ship.hull[1].getFlagDNAString()

    def setFlagDNAString(self, dnaStr):
        pass

    def loadModel(self):
        self.prop.loadModel(self.dna)
        self.prop.loadHigh()
        self.prop.loadMedium()
        self.prop.loadLow()
    
    def setArrayHp(self, hpArray):
        DistributedDestructibleArray.DistributedDestructibleArray.setArrayHp(self, hpArray)
        messenger.send('setMastHp-%s' % self.shipId, self.getArrayHp())

    def getArrayHp(self):
        return [
            self.dna.posIndex,
            self.arrayHp,
            self.maxArrayHp]

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker):
        self.prop.projectileWeaponHit(skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker)
    
    def playDeath(self, index = None):
        if self.prop.mastsState[index] == 0 and self.isGenerated():
            if index != None and self.prop:
                self.prop.death(index)

    def respawn(self, index):
        if self.prop:
            for i in range(index, len(self.arrayHp)):
                if self.arrayHp[i] > 0:
                    self.prop.respawn(i)
    
    def setBreakAnim(self, index, animMultiplier = 1.0):
        if self.prop.mastsState[index] == 0:
            self.prop.setBreakAnim(index, animMultiplier)
    
    def loadStats(self):
        if self.stats:
            return
        
        if not self.dna.mastType:
            return
        
        self.stats = ShipGlobals.getMastStats(self.dna.mastType)
        self.maxArrayHp = copy.copy(self.stats['maxArrayHp'])
        self.arrayHp = copy.copy(self.maxArrayHp)
        self.anchorDrag = self.stats['anchorDrag']
        self.hullDrag = self.stats['hullDrag']
        self.mass = self.stats['mass']
        self.addStats()
    
    def addStats(self):
        ship = base.cr.doId2do.get(self.shipId)
        ship.anchorDrag += self.anchorDrag
        ship.hullDrag += self.hullDrag
        self.mass += self.mass

    def removeStats(self):
        ship = base.cr.doId2do.get(self.shipId)
        ship.anchorDrag -= self.anchorDrag
        ship.hullDrag -= self.hullDrag
        self.mass -= self.mass
    
    def setDefaultDNA(self):
        newDNA = MastDNA.MastDNA()
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

    def setMastType(self, val):
        self.dna.setMastType(val)
        stats = ShipGlobals.getMastClassification(val)
        if stats:
            self.level = stats[2]
        else:
            self.level = 0
    
    def getMastType(self):
        return self.dna.getMastType()
    
    def setPosIndex(self, val):
        self.dna.setPosIndex(val)
    
    def getPosIndex(self):
        return self.dna.getPosIndex()
    
    def setTextureIndex(self, val):
        self.dna.setTextureIndex(val)
    
    def setColorIndex(self, val):
        self.dna.setColorIndex(val)
    
    def setSailConfig(self, val):
        self.dna.setSailConfig(val)
        messenger.send('setMastType-%s' % self.shipId, [
            self.dna.mastType,
            self.dna.posIndex,
            self.dna.sailConfig])
        messenger.send('setMastHp-%s' % self.shipId, [
            self.dna.posIndex,
            self.arrayHp,
            self.maxArrayHp])

    def getSailConfig(self):
        return self.dna.getSailConfig()

    def addPropToShip(self):
        self.prop.loadCollisions()
        self.prop.addToShip()

