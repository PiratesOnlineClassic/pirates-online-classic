import random
import copy
import math
from direct.showbase.PythonUtil import report, quickProfile
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.distributed import DistributedObject
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase.PiratesGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.ship import ShipGlobals
from pirates.ship import ShipBalance
from pirates.battle import CannonGlobals
from pirates.battle import WeaponGlobals
from pirates.shipparts import HullDNA
from pirates.shipparts import Hull
from pirates.shipparts import DistributedShippart
from pirates.destructibles import DistributedDestructibleArray

class DistributedHull(DistributedShippart.DistributedShippart, DistributedDestructibleArray.DistributedDestructibleArray):
    notify = directNotify.newCategory('DistributedHull')

    def __init__(self, cr):
        DistributedShippart.DistributedShippart.__init__(self, cr)
        DistributedDestructibleArray.DistributedDestructibleArray.__init__(self, cr)
        NodePath.__init__(self, 'DistributedHull')
        self.stats = None
        self.hackHullTransform = {
            0: 0,
            1: 5,
            2: 6,
            3: 3,
            4: 4,
            5: 1,
            6: 2,
            7: 7,
            8: 8}
        self.prop = None
        self.listingThreshold = 2
        self.listingIncrement = 5
        self.waterIntakeThreshold = 2
        self.waterIntakeIncrement = 7
        self.leftDamageLvl = 0
        self.rightDamageLvl = 0
        self.pendingLoadStats = None
        self.pendingStateTest = None

    def generate(self):
        self.notify.debug('Generate ' + str(self.doId))
        if not self.prop:
            self.setDefaultDNA()
        else:
            self.dna = self.prop.dna
        DistributedShippart.DistributedShippart.generate(self)
        DistributedDestructibleArray.DistributedDestructibleArray.generate(self)

    def announceGenerate(self):
        self.notify.debug('AnnounceGenerate ' + str(self.doId))
        DistributedShippart.DistributedShippart.announceGenerate(self)
        DistributedDestructibleArray.DistributedDestructibleArray.announceGenerate(self)

    def createProp(self):
        hull = self.ship.hull
        if hull:
            if hull[0]:
                self.prop = hull[0]
                self.ship.hull[1] = self
                self.stashFloorCollisions()
                return

        self.prop = Hull.Hull(self.ship, base.cr)
        self.prop.shipId = self.shipId
        self.prop.doId = self.doId
        self.ship.hull = [self.prop, self]
        self.stashFloorCollisions()

    def propLoaded(self):
        if self.ship.getHp() <= 0:
            return

        for i in range(len(self.arrayHp)):
            if self.arrayHp[i] <= 0:
                panelIndex = self.prop.getPanelIndex(i)
                self.prop.playBreak(panelIndex, i)

    def disable(self):
        self.notify.debug('Disable ' + str(self.doId))
        DistributedShippart.DistributedShippart.disable(self)
        DistributedDestructibleArray.DistributedDestructibleArray.disable(self)

    def delete(self):
        self.notify.debug('Delete ' + str(self.doId))
        del self.dna
        if self.ship.hull:
            self.ship.hull[1] = None

        del self.leftDamageLvl
        del self.rightDamageLvl
        DistributedShippart.DistributedShippart.delete(self)
        DistributedDestructibleArray.DistributedDestructibleArray.delete(self)

    def getFlagDNAString(self):
        return self.ship.getFlagDNAString()

    def setFlagDNAString(self, dnaStr):
        pass

    def getArmorStatus(self):
        if len(self.arrayHp) % 2 == 1:
            left = 1.0 - (self.arrayHp[1] + self.arrayHp[3] + self.arrayHp[5]) / float(self.maxArrayHp[1] + self.maxArrayHp[3] + self.maxArrayHp[5])
            rear = 1.0 - self.arrayHp[0] / float(self.maxArrayHp[0])
            right = 1.0 - (self.arrayHp[2] + self.arrayHp[4] + self.arrayHp[6]) / float(self.maxArrayHp[2] + self.maxArrayHp[4] + self.maxArrayHp[6])
        else:
            left = 1.0 - (self.arrayHp[1] + self.arrayHp[3] + self.arrayHp[5]) / float(self.maxArrayHp[1] + self.maxArrayHp[3] + self.maxArrayHp[5])
            rear = 1.0 - self.arrayHp[0] / float(self.maxArrayHp[0])
            right = 1.0 - (self.arrayHp[2] + self.arrayHp[4]) / float(self.maxArrayHp[2] + self.maxArrayHp[4])
        return (left, rear, right)

    def setArrayHp(self, hpArray):
        self.rightDamageLvl = 0
        self.leftDamageLvl = 0
        for index in range(len(self.arrayHp)):
            deltaHp = int(hpArray[index] - self.arrayHp[index])
            if deltaHp > 0 and self.arrayHp[index] == 0:
                self.respawn(index)

            self.arrayHp[index] = int(hpArray[index])
            if base.cr.config.GetBool('want-ship-hpdisplay', 0) is 1:
                self.updateHpDisplay(index)

            if deltaHp < 0:
                if self.prop:
                    if self.arrayHp[index] <= 0 and self.arrayHp[index] - deltaHp > 0:
                        self.playDeath(index)

        self.arrayHp = copy.copy(hpArray)
        for index in range(len(self.arrayHp)):
            self.arrayHp[index] = int(self.arrayHp[index])

        if self.ship:
            self.ship.adjustArmorDisplay()

        for index in range(len(self.arrayHp)):
            if index % 2 == 1:
                if self.arrayHp[index] <= 0:
                    self.rightDamageLvl += 1
            elif index % 2 == 0:
                if self.arrayHp[index] <= 0:
                    self.leftDamageLvl += 1

        messenger.send('setHullHp-%s' % self.shipId, self.getArrayHp())
        if self.arrayHp == self.maxArrayHp:
            self.respawnAll()

    def getArrayHp(self):
        return [
            self.arrayHp,
            self.maxArrayHp]

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker):
        if self.ship.invulnerable():
            return

        self.prop.projectileWeaponHit(skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker)

    def playDeath(self, index = None):
        if self.prop:
            self.prop.death(index)

    def respawn(self, index):
        if self.prop:
            self.prop.respawn(index)

    def respawnAll(self):
        if self.prop:
            self.prop.respawnAll()

    def setGeomParentId(self, geomParentId):
        self.geomParentId = geomParentId

    def stashFloorCollisions(self):
        if self.prop:
            self.prop.stashFloorCollisions()

    def unstashFloorCollisions(self):
        if self.prop:
            self.prop.unstashFloorCollisions()

    def startRiggingConstraint(self):
        if base.cr.config.GetBool('want-ship-rigging', 0) is 1:
            taskMgr.add(self.riggingConstraintTask, self.uniqueName('riggingConstraint'))

    def loadStats(self, ship):
        if self.stats:
            return

        if not self.dna.shipClass:
            return

        if self.dna.baseTeam == PiratesGlobals.INVALID_TEAM:
            return

        self.stats = ShipGlobals.getHullStats(self.dna.shipClass)
        if self.stats:
            self.maxArrayHp = copy.copy(self.stats['maxArrayHp'])
            self.arrayHp = copy.copy(self.maxArrayHp)

    def setDefaultDNA(self):
        newDNA = HullDNA.HullDNA()
        self.setDNA(newDNA)

    def setDNA(self, dna):
        if self.dna:
            self.updateDNA(dna)
        else:
            self.dna = dna

    def updateDNA(self, newDNA, fForce = 0):
        oldDna = self.dna
        self.dna = newDNA

    def setShipId(self, shipId):
        DistributedShippart.DistributedShippart.setShipId(self, shipId)
        if self.pendingLoadStats:
            base.cr.relatedObjectMgr.abortRequest(self.pendingLoadStats)

        self.pendingLoadStats = base.cr.relatedObjectMgr.requestObjects([
            self.shipId], eachCallback = self.loadStats)

    def setShipClass(self, val):
        self.dna.setShipClass(val)

    def setBaseTeam(self, val):
        self.dna.setBaseTeam(val)

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

    def setMastConfig1(self, val):
        self.dna.setMastConfig1(val)

    def setMastConfig2(self, val):
        self.dna.setMastConfig2(val)

    def setMastConfig3(self, val):
        self.dna.setMastConfig3(val)

    def setForemastConfig(self, val):
        self.dna.setForemastConfig(val)

    def setAftmastConfig(self, val):
        self.dna.setAftmastConfig(val)

    def setSailConfig1(self, val):
        self.dna.setSailConfig1(val)

    def setSailConfig2(self, val):
        self.dna.setSailConfig2(val)

    def setSailConfig3(self, val):
        self.dna.setSailConfig3(val)

    def setForesailConfig(self, val):
        self.dna.setForesailConfig(val)

    def setAftsailConfig(self, val):
        self.dna.setAftsailConfig(val)

    def setProwType(self, val):
        self.dna.setProwType(val)

    def setRamType(self, val):
        self.dna.setRamType(val)

    def setCabinType(self, val):
        self.dna.setCabinType(val)

    def setCannonConfig(self, val):
        self.dna.setCannonConfig(val)

    def setLeftBroadsideConfig(self, val):
        self.dna.setLeftBroadsideConfig(val)

    def setRightBroadsideConfig(self, val):
        self.dna.setRightBroadsideConfig(val)

    def setWallDecorConfig(self, val):
        self.dna.setWallDecorConfig(val)

    def setFloorDecorConfig(self, val):
        self.dna.setFloorDecorConfig(val)

    def setMaxCargo(self, maxCargo):
        self.maxCargo = maxCargo

    def addPropToShip(self):
        self.prop.addToShip()
