# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.shipparts.ShipPart
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals

class ShipPart:
    __module__ = __name__
    woodBreakSfx = None
    distantBreakSfx = None

    def __init__(self):
        self.__targetableCollisions = []
        self.dna = None
        self.geomParent = None
        self.ship = None
        self.prop = None
        self.propCollisions = None
        self.collisions = None
        self.shipId = 0
        self.doId = 0
        self.highDetail = None
        self.medDetail = None
        self.lowDetail = None
        self.geom_High = None
        self.geom_Medium = None
        self.geom_Low = None
        self.zoneLevel = 99
        self.loaded = False
        if not self.woodBreakSfx:
            ShipPart.woodBreakSfx = (
             loader.loadSfx('audio/wood_impact_1.mp3'), loader.loadSfx('audio/wood_impact_2.mp3'), loader.loadSfx('audio/wood_impact_3.mp3'), loader.loadSfx('audio/wood_impact_4.mp3'))
        if not self.distantBreakSfx:
            ShipPart.distantBreakSfx = (
             loader.loadSfx('audio/dist_cannon_01.mp3'), loader.loadSfx('audio/dist_cannon_02.mp3'), loader.loadSfx('audio/dist_cannon_03.mp3'), loader.loadSfx('audio/dist_cannon_04.mp3'), loader.loadSfx('audio/dist_cannon_05.mp3'), loader.loadSfx('audio/dist_cannon_06.mp3'), loader.loadSfx('audio/dist_cannon_07.mp3'), loader.loadSfx('audio/dist_cannon_08.mp3'), loader.loadSfx('audio/dist_cannon_09.mp3'), loader.loadSfx('audio/dist_cannon_10.mp3'))
        return

    def disable(self):
        pass

    def destroy(self):
        pass

    def addTargetableCollision(self, coll):
        self.__targetableCollisions.append(coll)

    def getTargetableCollisions(self):
        return self.__targetableCollisions

    def clearTargetableCollisions(self):
        self.__targetableCollisions = []

    def setTargetBitmask(self, on):
        if on:
            for coll in self.__targetableCollisions:
                curMask = coll.getCollideMask()
                newMask = curMask | PiratesGlobals.TargetBitmask
                coll.setCollideMask(newMask)

        for coll in self.__targetableCollisions:
            curMask = coll.getCollideMask()
            newMask = curMask ^ PiratesGlobals.TargetBitmask
            coll.setCollideMask(newMask)

    def unload(self):
        self.unloadHigh()
        self.unloadMedium()
        self.unloadLow()
        self.unloadCollisions()

    def setZoneLevel(self, level):
        if level > self.zoneLevel:
            for i in range(level):
                self.unloadZoneLevel(i)

        else:
            if level < self.zoneLevel:
                for i in range(len(PiratesGlobals.ShipZones) - level):
                    self.loadZoneLevel(i)

        self.zoneLevel = level

    def loadZoneLevel(self, level):
        if level == 0:
            self.loadHigh()
            self.unstashDetailCollisions()
        else:
            if level == 1:
                self.loadMedium()
            else:
                if level == 2:
                    self.loadCollisions()
                else:
                    if level == 3:
                        self.loadLow()

    def unloadZoneLevel(self, level):
        if level == 0:
            pass
        else:
            if level == 1:
                self.unloadHigh()
                self.stashDetailCollisions()
            else:
                if level == 2:
                    self.unloadMedium()
                else:
                    if level == 3:
                        self.unloadLow()
                        self.unloadCollisions()

    def loadHigh(self):
        pass

    def unloadHigh(self):
        pass

    def loadMedium(self):
        pass

    def unloadMedium(self):
        pass

    def loadLow(self):
        pass

    def unloadLow(self):
        pass

    def loadCollisions(self):
        pass

    def unloadCollisions(self):
        pass

    def stashDetailCollisions(self):
        pass

    def unstashDetailCollisions(self):
        pass

    def addToShip(self):
        if self.geom_Low:
            self.geom_Low.reparentTo(self.ship.lowDetail)
        if self.geom_Medium:
            self.geom_Medium.reparentTo(self.ship.mediumDetail)
        if self.geom_High:
            self.geom_High.reparentTo(self.ship.highDetail)

    def cache(self):
        self.ship = None
        self.shipId = 0
        return

    def uncache(self, ship):
        self.ship = ship
        self.shipId = ship.doId
# okay decompiling .\pirates\shipparts\ShipPart.pyc
