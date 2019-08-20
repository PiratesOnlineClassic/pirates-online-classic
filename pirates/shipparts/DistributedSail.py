import random
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.distributed import DistributedObject
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.actor import Actor
from direct.fsm import FSM
from direct.fsm import State
from direct.showbase.PythonUtil import quickProfile
from pirates.piratesbase.PiratesGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.ship import ShipGlobals
from pirates.battle import CannonGlobals
from pirates.battle import WeaponGlobals
from pirates.shipparts import MastDNA
from pirates.shipparts import SailDNA
from pirates.shipparts import Sail
from pirates.shipparts import DistributedShippart
from pirates.destructibles import DistributedDestructibleObject

class DistributedSail(DistributedShippart.DistributedShippart, DistributedDestructibleObject.DistributedDestructibleObject):
    notify = directNotify.newCategory('DistributedSail')
    
    def __init__(self, cr):
        self.cr = cr
        DistributedShippart.DistributedShippart.__init__(self, cr)
        DistributedDestructibleObject.DistributedDestructibleObject.__init__(self, cr)
        NodePath.__init__(self, 'DistributedSail')
        self.stats = None
        self.animState = None
        self.pendingMeterHookup = None

    def generate(self):
        self.notify.debug('Generate ' + str(self.doId))
        self.setDefaultDNA()
        DistributedShippart.DistributedShippart.generate(self)
        DistributedDestructibleObject.DistributedDestructibleObject.generate(self)
    
    def announceGenerate(self):
        self.notify.debug('Announce Generate ' + str(self.doId))
        DistributedShippart.DistributedShippart.announceGenerate(self)
        DistributedDestructibleObject.DistributedDestructibleObject.announceGenerate(self)
        self.checkMastParentAlive()
        self.updateSiegeTeam()
    
    def createProp(self):
        mast = self.ship.sails.get(self.dna.mastPosIndex, 0)
        if mast:
            sail = mast.get(self.dna.posIndex, 0)
            if sail:
                if sail[0]:
                    self.notify.debug('SHIP-%d:Reattaching Sail-%d' % (self.ship.doId, self.doId))
                    self.prop = sail[0]
                    self.ship.sails[self.dna.mastPosIndex][self.dna.posIndex][1] = self
                    return
        
        self.notify.debug('SHIP-%d:Creating New Sail-%d' % (self.ship.doId, self.doId))
        self.prop = Sail.Sail(self.ship, self.cr)
        self.prop.shipId = self.shipId
        self.prop.doId = self.doId
        if self.animState:
            self.prop.setAnimState(self.animState)
        
        if not self.ship.sails.get(self.dna.mastPosIndex, 0):
            self.ship.sails[self.dna.mastPosIndex] = {}
            projScreen = self.ship.modelGeom.attachNewNode(ProjectionScreen('sail-set-%d' % self.dna.mastPosIndex))
            projScreen.node().setTexcoordName('uvHole')
            self.ship.sailProjectors[self.dna.mastPosIndex] = projScreen
            self.prop.setProjScreen(projScreen)
        else:
            self.prop.setProjScreen(self.ship.sailProjectors[self.dna.mastPosIndex])
        self.ship.sails[self.dna.mastPosIndex][self.dna.posIndex] = [
            self.prop,
            self]

    def disable(self):
        self.notify.debug('Disable ' + str(self.doId))
        if self.pendingMeterHookup:
            base.cr.relatedObjectMgr.abortRequest(self.pendingMeterHookup)
            self.pendingMeterHookup = None
        
        DistributedShippart.DistributedShippart.disable(self)
        DistributedDestructibleObject.DistributedDestructibleObject.disable(self)

    def delete(self):
        self.notify.debug('Delete ' + str(self.doId))
        mast = self.ship.sails.get(self.dna.mastPosIndex)
        if mast:
            sail = mast.get(self.dna.posIndex, 0)
            if sail:
                sail[1] = None

        del self.dna
        DistributedShippart.DistributedShippart.delete(self)
        DistributedDestructibleObject.DistributedDestructibleObject.delete(self)

    def getFlagDNAString(self):
        return self.ship.mast[self.prop.mastIndex].getFlagDNAString()

    def setFlagDNAString(self, dnaStr):
        pass

    def loadModel(self):
        self.prop.loadModel(self.dna)
        self.prop.loadCollisions()
        self.setAnimState(self.animState)
    
    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker):
        self.prop.projectileWeaponHit(skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker)
        self.setAnimState('Hit')

    def setHp(self, newHp):
        if self.Hp == newHp:
            return
        
        DistributedDestructibleObject.DistributedDestructibleObject.setHp(self, newHp)
        if self.ship:
            messenger.send('setSailHp-%s' % self.ship.doId, self.getHp())
        
        if self.Hp >= self.maxHp:
            self.respawn()
    
    def getHp(self):
        return [
            self.dna.mastPosIndex,
            self.dna.posIndex,
            self.Hp,
            self.maxHp]

    def playDeath(self):
        if self.prop:
            self.prop.playBreak()
    
    def respawn(self):
        if self.prop:
            self.prop.respawn()

    def l_setAnimState(self, animState):
        if self.prop:
            self.prop.setAnimState(animState)
        
        self.animState = animState
        self.sendRequestSetAnimState(animState)

    def setAnimState(self, animState):
        if self.prop:
            self.prop.setAnimState(animState)
        
        self.animState = animState

    def b_setAnimState(self, animState):
        self.setAnimState(animState)
        self.sendUpdate('setAnimState', [animState])

    def getAnimState(self):
        return self.animState

    def sendRequestSetAnimState(self, animState):
        self.sendUpdate('requestSetAnimState', [animState])

    def loadStats(self):
        if self.stats:
            return
        
        if not self.dna.sailType:
            return
        
        self.stats = ShipGlobals.getSailStats(self.dna.sailType)
        self.maxHp = self.stats['maxHp']
        self.Hp = self.maxHp
        self.maxArrayHp = self.stats['maxArrayHp']
        self.arrayHp = self.maxArrayHp
        id = ShipGlobals.getMastClassification(self.dna.mastType)[0]
        if id == ShipGlobals.MAINMAST:
            self.acceleration = self.stats['acceleration']
            self.maxSpeed = self.stats['maxSpeed']
            self.reverseAcceleration = self.stats['reverseAcceleration']
            self.maxReverseSpeed = self.stats['maxReverseSpeed']
            self.mass = self.stats['mass']
        elif id == ShipGlobals.FOREMAST:
            self.acceleration = self.stats['acceleration']
            self.maxSpeed = self.stats['maxSpeed']
            self.reverseAcceleration = self.stats['reverseAcceleration']
            self.maxReverseSpeed = self.stats['maxReverseSpeed']
            self.mass = self.stats['mass']
        elif id == ShipGlobals.AFTMAST:
            self.turnRate = self.stats['turn']
            self.maxTurn = self.stats['maxTurn']
            self.mass = self.stats['mass']
    
    def addStats(self):
        ship = base.cr.doId2do.get(self.shipId)
        if self.dna.sailType >= ShipGlobals.MAINSAILL1 and self.dna.sailType <= ShipGlobals.MAINSAILL3:
            ship.acceleration += self.acceleration
            ship.maxSpeed += self.maxSpeed
            ship.reverseAcceleration += self.reverseAcceleration
            ship.maxReverseSpeed += self.maxReverseSpeed
            ship.mass += self.mass
        elif self.dna.sailType >= ShipGlobals.FORESAILL1 and self.dna.sailType <= ShipGlobals.FORESAILL3:
            ship.acceleration += self.acceleration
            ship.maxSpeed += self.maxSpeed
            ship.reverseAcceleration += self.reverseAcceleration
            ship.maxReverseSpeed += self.maxReverseSpeed
            ship.mass += self.mass
        elif self.dna.sailType >= ShipGlobals.AFTSAILL1 and self.dna.sailType <= ShipGlobals.AFTSAILL3:
            ship.turnRate += self.turnRate
            ship.maxTurn += self.maxTurn
            ship.mass += self.mass

    def removeStats(self):
        ship = base.cr.doId2do.get(self.shipId)
        ship.anchorDrag -= self.anchorDrag
        ship.hullDrag -= self.hullDrag
        self.mass -= self.mass
    
    def setDefaultDNA(self):
        newDNA = SailDNA.SailDNA()
        self.setDNA(newDNA)

    def setDNA(self, dna):
        if self.dna:
            self.updateDNA(dna)
        else:
            self.dna = dna
    
    def updateDNA(self, newDNA, fForce = 0):
        oldDna = self.dna
        self.dna = newDNA

    def setBaseTeam(self, val):
        self.dna.setBaseTeam(val)

    def setMastType(self, val):
        self.dna.setMastType(val)
    
    def setMastPosIndex(self, val):
        self.dna.setMastPosIndex(val)

    def setSailType(self, val):
        self.dna.setSailType(val)

    def setPosIndex(self, val):
        self.dna.setPosIndex(val)
    
    def setTextureIndex(self, val):
        self.dna.setTextureIndex(val)

    def setColorIndex(self, val):
        self.dna.setColorIndex(val)

    def setLogoIndex(self, val):
        self.dna.setLogoIndex(val)
    
    def addPropToShip(self):
        self.prop.addToShip()
        self.checkMastParentAlive()
    
    def checkMastParentAlive(self):
        if self.ship:
            if self.ship.masts:
                mast = self.ship.masts.get(self.dna.mastPosIndex)
                if mast and mast[1]:
                    hpArray = mast[1].arrayHp
                    index = min(self.dna.posIndex, len(hpArray))
                    for i in range(index + 1):
                        if len(hpArray) > i:
                            if hpArray[i] <= 0:
                                self.prop.death()
                                return

    def updateSiegeTeam(self):
        team = self.ship.getSiegeTeam()
        if team == 0:
            self.prop.setLogo(None)
        elif team == 1:
            self.prop.setLogo(210)
        elif team == 2:
            self.prop.setLogo(211)

