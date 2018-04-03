# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.ship.ShipMeter
import copy

from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from direct.task.Task import Task
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import (GuiButton, GuiTray, PiratesTimer,
                                StatusEffectsPanel)
from pirates.pvp import PVPGlobals
from pirates.ship import ShipGlobals
from pirates.ship.DistributedShipOV import DistributedShipOV
from pirates.shipparts.DistributedHullOV import DistributedHullOV
from pirates.shipparts.DistributedMastOV import DistributedMastOV

HullDict = {ShipGlobals.WARSHIPL1: 'models/shipparts/warshipMeter', ShipGlobals.WARSHIPL2: 'models/shipparts/warshipMeter', ShipGlobals.WARSHIPL3: 'models/shipparts/warshipMeter', ShipGlobals.WARSHIPL4: 'models/shipparts/warshipMeter', ShipGlobals.MERCHANTL1: 'models/shipparts/merchantMeter', ShipGlobals.MERCHANTL2: 'models/shipparts/merchantMeter', ShipGlobals.MERCHANTL3: 'models/shipparts/merchantMeter', ShipGlobals.MERCHANTL4: 'models/shipparts/merchantMeter', ShipGlobals.INTERCEPTORL1: 'models/shipparts/interceptorMeter', ShipGlobals.INTERCEPTORL2: 'models/shipparts/interceptorMeter', ShipGlobals.INTERCEPTORL3: 'models/shipparts/interceptorMeter', ShipGlobals.INTERCEPTORL4: 'models/shipparts/interceptorMeter', ShipGlobals.BLACK_PEARL: 'models/shipparts/merchantMeter', ShipGlobals.GOLIATH: 'models/shipparts/warshipMeter', ShipGlobals.SKEL_WARSHIPL3: 'models/shipparts/warshipMeter', ShipGlobals.SKEL_INTERCEPTORL3: 'models/shipparts/interceptorMeter'}
MastDict = {ShipGlobals.MAINMASTL1: 'models/shipparts/mainmast_square', ShipGlobals.MAINMASTL2: 'models/shipparts/mainmast_square', ShipGlobals.MAINMASTL3: 'models/shipparts/mainmast_square', ShipGlobals.MAINMASTL4: 'models/shipparts/mainmast_square', ShipGlobals.MAINMASTL5: 'models/shipparts/mainmast_square', ShipGlobals.TRIMASTL1: 'models/shipparts/L2mastTri', ShipGlobals.TRIMASTL2: 'models/shipparts/L2mastTri', ShipGlobals.TRIMASTL3: 'models/shipparts/L2mastTri', ShipGlobals.TRIMASTL4: 'models/shipparts/L2mastTri', ShipGlobals.TRIMASTL5: 'models/shipparts/L2mastTri', ShipGlobals.FOREMASTL1: 'models/shipparts/L1foremast', ShipGlobals.FOREMASTL2: 'models/shipparts/L2foremast', ShipGlobals.FOREMASTL3: 'models/shipparts/L2foremast', ShipGlobals.AFTMASTL1: 'models/shipparts/L2aftmast', ShipGlobals.AFTMASTL2: 'models/shipparts/L2aftmast', ShipGlobals.AFTMASTL3: 'models/shipparts/L2aftmast', ShipGlobals.SKEL_MAINMASTL1_A: 'models/shipparts/mainmast_square', ShipGlobals.SKEL_MAINMASTL2_A: 'models/shipparts/mainmast_square', ShipGlobals.SKEL_MAINMASTL3_A: 'models/shipparts/mainmast_square', ShipGlobals.SKEL_MAINMASTL4_A: 'models/shipparts/mainmast_square', ShipGlobals.SKEL_MAINMASTL5_A: 'models/shipparts/mainmast_square', ShipGlobals.SKEL_MAINMASTL1_B: 'models/shipparts/mainmast_square', ShipGlobals.SKEL_MAINMASTL2_B: 'models/shipparts/mainmast_square', ShipGlobals.SKEL_MAINMASTL3_B: 'models/shipparts/mainmast_square', ShipGlobals.SKEL_MAINMASTL4_B: 'models/shipparts/mainmast_square', ShipGlobals.SKEL_MAINMASTL5_B: 'models/shipparts/mainmast_square', ShipGlobals.SKEL_TRIMASTL1: 'models/shipparts/L2mastTri', ShipGlobals.SKEL_TRIMASTL2: 'models/shipparts/L2mastTri', ShipGlobals.SKEL_TRIMASTL3: 'models/shipparts/L2mastTri', ShipGlobals.SKEL_TRIMASTL4: 'models/shipparts/L2mastTri', ShipGlobals.SKEL_TRIMASTL5: 'models/shipparts/L2mastTri', ShipGlobals.SKEL_FOREMASTL1: 'models/shipparts/L1foremast', ShipGlobals.SKEL_FOREMASTL2: 'models/shipparts/L1foremast', ShipGlobals.SKEL_FOREMASTL3: 'models/shipparts/L1foremast', ShipGlobals.SKEL_AFTMASTL1: 'models/shipparts/L2aftmast', ShipGlobals.SKEL_AFTMASTL2: 'models/shipparts/L2aftmast', ShipGlobals.SKEL_AFTMASTL3: 'models/shipparts/L2aftmast'}

class ShipMeter(DirectObject, NodePath):
    __module__ = __name__

    def __init__(self, shipId, shipClass=0, mastInfo=[], siegeTeam=0):
        NodePath.__init__(self, 'ShipMeter')
        self.shipId = shipId
        self.team = 0
        self.siegeTeam = siegeTeam
        self.shipClass = shipClass
        self.modelClass = shipClass
        self.hull = None
        self.panels = []
        self.masts = [None, None, None, None, None]
        self.sails = [None, None, None, None, None]
        self.mastModels = [None, None, None, None, None]
        self.bowsprit = None
        self.ram = None
        self.cabin = None
        self.panelStates = []
        self.mastStates = [
         None, None, None, None, None]
        self.mastTypes = [None, None, None, None, None]
        self.smokeEffects = []
        self.oldHullHp = []
        self.oldMastHp = [[], [], [], [], []]
        self.modelRoot = self.attachNewNode('modelRoot')
        if shipClass and mastInfo:
            self.setShipInfo(shipClass, mastInfo)
            ship = base.cr.doId2do.get(self.shipId)
            if ship:
                if ship.hull and ship.hull[1]:
                    self.setHullHp(*ship.hull[1].getArrayHp())
                if ship.masts:
                    for mast, dMast in ship.masts.itervalues():
                        if dMast:
                            self.setMastHp(*dMast.getArrayHp())

        else:
            if self.shipId:
                hullOVs = base.cr.getOwnerViewDoList(DistributedHullOV)
                hullOVs = [ ov for ov in hullOVs if ov.shipId == self.shipId ]
                for hullOV in hullOVs:
                    self.setHullType(hullOV.shipClass)

                mastOVs = base.cr.getOwnerViewDoList(DistributedMastOV)
                mastOVs = [ ov for ov in mastOVs if ov.shipId == self.shipId ]
                for mastOV in mastOVs:
                    self.setMastType(mastOV.mastType, mastOV.posIndex, mastOV.sailConfig)

        self.accept('setShipClass-%s' % self.shipId, self.setHullType)
        self.accept('setMastType-%s' % self.shipId, self.setMastType)
        self.accept('setHullHp-%s' % self.shipId, self.setHullHp)
        self.accept('setBowspritHp-%s' % self.shipId, self.setBowspritHp)
        self.accept('setCabinHp-%s' % self.shipId, self.setCabinHp)
        self.accept('setMastHp-%s' % self.shipId, self.setMastHp)
        self.accept('setSailHp-%s' % self.shipId, self.setSailHp)
        return

    def destroy(self):
        self.modelRoot = None
        self.ignoreAll()
        self.removeNode()
        return

    def setHullType(self, type):
        if self.panels:
            return
        if not type:
            return
        self.shipClass = type
        self.modelClass = type
        modelType = ShipGlobals.getModelClass(type)
        filePrefix = HullDict.get(modelType)
        self.hull = loader.loadModel(filePrefix)
        self.hull.reparentTo(self.modelRoot)
        allPanels = self.hull.findAllMatches('**/panel_*').asList()
        for i in range(len(allPanels)):
            panel = self.hull.find('**/panel_' + str(i))
            if not panel.isEmpty():
                self.panels.append(panel)
                self.panelStates.append(0)
                self.smokeEffects.append(None)

        self.bowsprit = self.hull.find('**/bowsprit')
        self.ram = self.hull.find('**/ram')
        self.cabin = self.hull.find('**/cabin')
        self.bowsprit.detachNode()
        if self.modelClass == 1:
            self.cabin.detachNode()
        self.placeMasts()
        return

    def setMastType(self, type, index, sailConfig):
        if self.masts[index]:
            return
        if not type:
            return
        filePrefix = MastDict.get(type)
        self.mastModels[index] = loader.loadModel(filePrefix)
        myMasts = []
        myMastStates = []
        mySails = []
        mastSegments = self.mastModels[index].findAllMatches('**/mast_*').asList()
        for i in range(len(mastSegments)):
            mastSegment = self.mastModels[index].find('**/mast_' + str(i))
            if not mastSegment.isEmpty():
                if i >= len(sailConfig):
                    mastSegment.stash()
                    continue
                myMasts.append(mastSegment)
                myMastStates.append(0)
            sail = self.mastModels[index].find('**/sail_' + str(i))
            if not sail.isEmpty():
                sailType = 0
                if i <= len(sailConfig) - 1:
                    sailType = sailConfig[i]
                if sailType and sailType != ShipGlobals.FLAG:
                    mySails.append(sail)
                else:
                    mySails.append(None)
            else:
                mySails.append(None)

        for i in range(len(mySails)):
            if not mySails[i]:
                sail = self.mastModels[index].find('**/sail_' + str(i))
                sail.stash()

        self.masts[index] = myMasts
        self.mastStates[index] = myMastStates
        self.mastTypes[index] = type
        self.sails[index] = mySails
        if self.hull:
            self.placeMasts()
        return

    def placeMasts(self):
        for index in range(len(self.masts)):
            mast = self.masts[index]
            if mast:
                self.mastModels[index].reparentTo(self.modelRoot)
                type = self.mastTypes[index]
                id = ShipGlobals.getMastClassification(type)[0]
                if id == ShipGlobals.FOREMAST:
                    locator = self.hull.find('**/location_foremast;+s')
                else:
                    if id == ShipGlobals.MAINMAST:
                        if self.modelClass == 11 and index == 1:
                            locator = self.hull.find('**/location_mainmast_2;+s')
                        else:
                            locator = self.hull.find('**/location_mainmast_' + str(index) + ';+s')
                    else:
                        if id == ShipGlobals.AFTMAST:
                            locator = self.hull.find('**/location_aftmast;+s')
                self.mastModels[index].setPos(locator.getPos())
                self.mastModels[index].setHpr(locator.getHpr())
                self.mastModels[index].setScale(locator.getScale())

    def setHullHp(self, hpArray, maxHpArray):
        if not self.panels:
            return
        for i in range(len(self.panels)):
            if i <= len(hpArray) - 1:
                hpFraction = float(hpArray[i]) / float(maxHpArray[i])
                damageColor = self.getDamageColor(hpFraction)
                self.panels[i].setColorScale(damageColor)
                if self.oldHullHp:
                    if self.oldHullHp[i] > hpArray[i]:
                        self.playFlash(self.panels[i], damageColor)
                if hpArray[i] <= 0 and self.panelStates[i] == 0:
                    self.panelStates[i] = 1
                elif hpArray[i] > 0 and self.panelStates[i] == 1:
                    self.panelStates[i] = 0
                    if self.smokeEffects[i]:
                        self.smokeEffects[i].endLoop()
            else:
                self.panels[i].stash()

        self.oldHullHp = copy.copy(hpArray)

    def setMastHp(self, index, hpArray, maxHpArray):
        if not self.masts[index]:
            return
        for i in range(len(self.masts[index])):
            if i > len(hpArray) - 1:
                if self.masts[index][i]:
                    self.masts[index][i].stash()

        for i in range(len(hpArray)):
            if i <= len(self.masts[index]) - 1:
                hpFraction = float(hpArray[i]) / float(maxHpArray[i])
                damageColor = self.getDamageColor(hpFraction)
                self.masts[index][i].setColorScale(damageColor)
                if self.oldMastHp[index]:
                    if self.oldMastHp[index][i] > hpArray[i]:
                        self.playFlash(self.masts[index][i], damageColor)
                if hpFraction <= 0:
                    self.mastStates[index][i] = 1
                else:
                    self.mastStates[index][i] = 0

        hasBreak = 0
        for i in range(len(hpArray)):
            if i <= len(self.masts[index]) - 1:
                if self.mastStates[index][i] == 0 and hasBreak == 0:
                    self.masts[index][i].show()
                    if self.sails[index][i]:
                        self.sails[index][i].show()
                else:
                    hasBreak = 1
                    self.masts[index][i].hide()
                    if self.sails[index][i]:
                        self.sails[index][i].hide()
                    self.oldMastHp[index] = copy.copy(hpArray)

    def setSailHp(self, mastIndex, sailIndex, hp, maxHp):
        if self.sails[mastIndex]:
            if len(self.mastStates[mastIndex]) - 1 >= sailIndex:
                hpFraction = float(hp) / float(maxHp)
                damageColor = self.getDamageColor(hpFraction)
                self.sails[mastIndex][sailIndex].setColorScale(damageColor)
                self.playFlash(self.sails[mastIndex][sailIndex], damageColor)
        for i in range(sailIndex):
            if self.mastStates[mastIndex]:
                if len(self.mastStates[mastIndex]) - 1 >= sailIndex:
                    if self.mastStates[mastIndex][i] == 1:
                        self.sails[mastIndex][sailIndex].hide()

    def setBowspritHp(self, hp, maxHp):
        hpFraction = float(hp) / float(maxHp)
        damageColor = self.getDamageColor(hpFraction)
        if self.bowsprit:
            self.bowsprit.setColorScale(damageColor)
            if hpFraction <= 0:
                self.bowsprit.hide()
            else:
                self.bowsprit.show()
                self.playFlash(self.bowsprit, damageColor)

    def setRamHp(self, hp, maxHp):
        hpFraction = float(hp) / float(maxHp)
        damageColor = self.getDamageColor(hpFraction)
        if self.ram:
            self.ram.setColorScale(damageColor)
            if hpFraction <= 0:
                self.ram.hide()
            else:
                self.ram.show()
                self.playFlash(self.ram, damageColor)

    def setCabinHp(self, hp, maxHp):
        hpFraction = float(hp) / float(maxHp)
        damageColor = self.getDamageColor(hpFraction)
        if self.cabin:
            self.cabin.setColorScale(damageColor)
            if hpFraction <= 0:
                self.cabin.hide()
            else:
                self.cabin.show()
                self.playFlash(self.cabin, damageColor)

    def getDamageColor(self, hpFraction):
        if hpFraction >= 0.5:
            return Vec4(1, 1, 1, 1)
        else:
            if hpFraction >= 0.25:
                return Vec4(1, 1, 0, 1)
            else:
                if hpFraction > 0:
                    return Vec4(1, 0, 0.1, 1)
                else:
                    if hpFraction <= 0:
                        return Vec4(0.5, 0, 0, 1)

    def playFlash(self, target, normalColor):
        flash = Sequence(Func(target.setColor, Vec4(1, 1, 0, 1)), Wait(0.1), Func(target.setColor, Vec4(1, 0, 0, 1)), Wait(0.1), Func(target.setColor, Vec4(1, 1, 0, 1)), Wait(0.1), Func(target.setColor, Vec4(1, 0, 0, 1)), Wait(0.1), Func(target.setColor, Vec4(1, 1, 0, 1)), Wait(0.1), Func(target.setColor, Vec4(1, 0, 0, 1)), Wait(0.1), Func(target.setColorOff))
        flash.start()

    def setShipInfo(self, shipClass, mastInfo):
        self.setHullType(shipClass)
        for mast in mastInfo:
            self.setMastType(*mast)

    def getFlat(self):
        self.flattenStrong()
        counter = 1
        whites = NodePath('whites')
        woods = self.attachNewNode(PandaNode('woods'))
        for sailSet in self.sails:
            if sailSet:
                for sail in sailSet:
                    if sail:
                        sail = sail.find('**/+GeomNode')
                        if self.team == 0:
                            sail.setColor(0.7, 0.7, 0.5, 1)
                        else:
                            if self.team == 1:
                                sail.setColor(0.3, 0.3, 0.3, 1)
                            else:
                                if self.team == 2:
                                    if counter % 2:
                                        sail.setColor(0.6, 0, 0, 1)
                                    else:
                                        sail.setColor(0.6, 0.6, 0.6, 1)
                                else:
                                    if self.team == 3:
                                        if counter % 2:
                                            sail.setColor(0, 0, 0, 1)
                                        else:
                                            sail.setColor(0.6, 0.6, 0.6, 1)
                        sail.flattenStrong()
                        sail.reparentTo(whites)
                        counter += 1

        self.findAllMatches('**/+GeomNode').reparentTo(woods)
        whites.reparentTo(self)
        self.findAllMatches('**/+ModelNode').detach()
        woods.setColor(0.2, 0.15, 0, 1)
        self.flattenStrong()
        gn = self.find('**/+GeomNode')
        for i in xrange(gn.node().getNumGeoms()):
            gn.node().setGeomState(i, RenderState.makeEmpty())

        gn.setTwoSided(1)
        gn.flattenStrong()
        return gn

    def setTeam(self, team):
        self.team = team

    def setModelClass(self, mc):
        self.modelClass = mc
# okay decompiling .\pirates\ship\ShipMeter.pyc
