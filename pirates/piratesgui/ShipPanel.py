# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.ShipPanel
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import PiratesGuiGlobals, PiratesTimer
from pirates.piratesgui.ShipFrameBottle import ShipFrameBottle
from pirates.shipparts.DistributedHullOV import DistributedHullOV


class ShipPanel(DirectFrame):
    __module__ = __name__
    Width = PiratesGuiGlobals.ShipPanelWidth
    Height = PiratesGuiGlobals.ShipPanelHeight

    def __init__(self, shipPage, shipId, **kwargs):
        self.shipPage = shipPage
        self.setShipId(shipId)
        self.timer = None
        self.crewDots = []
        self.lBroadsideLimit = 0
        self.rBroadsideLimit = 0
        kwargs.setdefault('relief', None)
        kwargs.setdefault('frameSize', (0, self.Width, 0, self.Height))
        DirectFrame.__init__(self, **kwargs)
        self.initialiseoptions(ShipPanel)
        gui = loader.loadModel('models/gui/toplevel_gui')
        chestIcon = gui.findAllMatches('**/topgui_icon_ship_chest01').asList()
        cannonIcon = gui.find('**/topgui_icon_ship_cannon_single')
        broadsideIcon = gui.find('**/topgui_icon_ship_cannon_multiple')
        self.bottleFrame = ShipFrameBottle(parent=self, shipId=shipId, relief=None, state=DGG.DISABLED, pos=(0.075,
                                                                                                             0,
                                                                                                             0.75), scale=0.835)
        ornament = loader.loadModelOnce('models/gui/gui_ship_window')
        ornament.reparentTo(self)
        ornament.setScale(0.3)
        ornament.setPos(0.54, 0, 0.73)
        ornament.flattenStrong()
        self.nameLabel = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=PLocalizer.makeHeadingString(PLocalizer.EmptyBottle, 2), text_fg=PiratesGuiGlobals.TextFG1, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ACenter, text_shadow=(0,
                                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                                1), text_wordwrap=30, textMayChange=1, text_font=PiratesGlobals.getPirateFont(), pos=(0.55,
                                                                                                                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                                                                                                                      1.22))
        self.classLabel = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=PLocalizer.makeHeadingString(PLocalizer.EmptyBottleDesc, 1), text_scale=PiratesGuiGlobals.TextScaleMed, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=(0,
                                                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                                                              1), text_wordwrap=30, textMayChange=1, text_font=PiratesGlobals.getInterfaceFont(), pos=(0.55,
                                                                                                                                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                                                                                                                                       1.18))
        self.timer = PiratesTimer.PiratesTimer(showMinutes=True, mode=None, titleText='', titleFg='', infoText='', cancelText='', cancelCallback=None)
        self.timer.setFontColor(PiratesGuiGlobals.TextFG2)
        self.timer.reparentTo(self)
        self.timer.setPos(0.45, 0, 0.94)
        self.timer.setScale(0.6)
        self.timer.stash()
        self.hpMeter = DirectWaitBar(parent=self, relief=DGG.RAISED, state=DGG.DISABLED, range=1, value=0, frameColor=(0.0,
                                                                                                                       0.0,
                                                                                                                       0.0,
                                                                                                                       0.0), barColor=(0.1,
                                                                                                                                       0.7,
                                                                                                                                       0.1,
                                                                                                                                       1), frameSize=(0,
                                                                                                                                                      0.31,
                                                                                                                                                      0,
                                                                                                                                                      0.0186), text='', text_align=TextNode.ARight, text_scale=0.03, text_fg=(1,
                                                                                                                                                                                                                              1,
                                                                                                                                                                                                                              1,
                                                                                                                                                                                                                              1), text_shadow=(0,
                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                               1), text_pos=(0.3,
                                                                                                                                                                                                                                                             0.03), pos=(0.361,
                                                                                                                                                                                                                                                                         0.0,
                                                                                                                                                                                                                                                                         0.621), scale=1.2)
        hpLabel = DirectLabel(parent=self.hpMeter, relief=None, state=DGG.DISABLED, text=PLocalizer.HP, text_scale=0.03, text_align=TextNode.ALeft, text_pos=(0.015,
                                                                                                                                                              0.03), text_fg=(1,
                                                                                                                                                                              1,
                                                                                                                                                                              1,
                                                                                                                                                                              1), text_shadow=(0,
                                                                                                                                                                                               0,
                                                                                                                                                                                               0,
                                                                                                                                                                                               1))
        self.speedMeter = DirectWaitBar(parent=self, relief=DGG.RAISED, state=DGG.DISABLED, range=1, value=0, frameColor=(0.0,
                                                                                                                          0.0,
                                                                                                                          0.0,
                                                                                                                          0.0), barColor=(0.7,
                                                                                                                                          0.7,
                                                                                                                                          0.1,
                                                                                                                                          1), frameSize=(0,
                                                                                                                                                         0.31,
                                                                                                                                                         0,
                                                                                                                                                         0.0186), text='', text_align=TextNode.ARight, text_scale=0.03, text_fg=(1,
                                                                                                                                                                                                                                 1,
                                                                                                                                                                                                                                 1,
                                                                                                                                                                                                                                 1), text_shadow=(0,
                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                  1), text_pos=(0.3,
                                                                                                                                                                                                                                                                0.03), pos=(0.361,
                                                                                                                                                                                                                                                                            0.0,
                                                                                                                                                                                                                                                                            0.55), scale=1.2)
        speedLabel = DirectLabel(parent=self.speedMeter, relief=None, state=DGG.DISABLED, text=PLocalizer.Speed, text_scale=0.03, text_align=TextNode.ALeft, text_pos=(0.015,
                                                                                                                                                                       0.03), text_fg=(1,
                                                                                                                                                                                       1,
                                                                                                                                                                                       1,
                                                                                                                                                                                       1), text_shadow=(0,
                                                                                                                                                                                                        0,
                                                                                                                                                                                                        0,
                                                                                                                                                                                                        1))
        textPos = (
         0.0, -0.16)
        self.plunderLimit = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, geom=chestIcon, geom_scale=0.5, text='', text_scale=0.045, text_align=TextNode.ACenter, text_pos=textPos, text_fg=(1,
                                                                                                                                                                                                         1,
                                                                                                                                                                                                         1,
                                                                                                                                                                                                         1), text_shadow=(0,
                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                          1), textMayChange=1, text_font=PiratesGlobals.getInterfaceOutlineFont(), pos=(0.2,
                                                                                                                                                                                                                                                                                                        0,
                                                                                                                                                                                                                                                                                                        0.31))
        plunderLabel = DirectLabel(parent=self.plunderLimit, relief=None, state=DGG.DISABLED, text=PLocalizer.Cargo, text_scale=0.036, text_align=TextNode.ACenter, text_pos=(0,
                                                                                                                                                                              0.15), text_fg=(1,
                                                                                                                                                                                              1,
                                                                                                                                                                                              1,
                                                                                                                                                                                              1), text_shadow=(0,
                                                                                                                                                                                                               0,
                                                                                                                                                                                                               0,
                                                                                                                                                                                                               1))
        self.cannonLimit = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, geom=cannonIcon, geom_scale=0.45, text='', text_scale=0.045, text_align=TextNode.ACenter, text_pos=textPos, text_fg=(1,
                                                                                                                                                                                                          1,
                                                                                                                                                                                                          1,
                                                                                                                                                                                                          1), text_shadow=(0,
                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                           1), textMayChange=1, text_font=PiratesGlobals.getInterfaceOutlineFont(), pos=(0.37,
                                                                                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                                                                                         0.31))
        cannonLabel = DirectLabel(parent=self.cannonLimit, relief=None, state=DGG.DISABLED, text=PLocalizer.Cannon, text_scale=0.036, text_align=TextNode.ACenter, text_pos=(0,
                                                                                                                                                                             0.15), text_fg=(1,
                                                                                                                                                                                             1,
                                                                                                                                                                                             1,
                                                                                                                                                                                             1), text_shadow=(0,
                                                                                                                                                                                                              0,
                                                                                                                                                                                                              0,
                                                                                                                                                                                                              1))
        self.broadsideLeftLimit = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, geom=broadsideIcon, geom_scale=(-0.45, 0.45, 0.45), text='', text_scale=0.045, text_align=TextNode.ACenter, text_pos=textPos, text_fg=(1,
                                                                                                                                                                                                                                   1,
                                                                                                                                                                                                                                   1,
                                                                                                                                                                                                                                   1), text_shadow=(0,
                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                    1), textMayChange=1, text_font=PiratesGlobals.getInterfaceOutlineFont(), pos=(0.74,
                                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                                  0.31))
        self.broadsideRightLimit = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, geom=broadsideIcon, geom_scale=0.45, text='', text_scale=0.045, text_align=TextNode.ACenter, text_pos=textPos, text_fg=(1,
                                                                                                                                                                                                                     1,
                                                                                                                                                                                                                     1,
                                                                                                                                                                                                                     1), text_shadow=(0,
                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                      1), textMayChange=1, text_font=PiratesGlobals.getInterfaceOutlineFont(), pos=(0.885,
                                                                                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                                                                                    0.31))
        broadsideLabel = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=PLocalizer.Broadsides, text_scale=0.036, text_align=TextNode.ACenter, text_fg=(1,
                                                                                                                                                                       1,
                                                                                                                                                                       1,
                                                                                                                                                                       1), text_shadow=(0,
                                                                                                                                                                                        0,
                                                                                                                                                                                        0,
                                                                                                                                                                                        1), pos=(0.81,
                                                                                                                                                                                                 0,
                                                                                                                                                                                                 0.46))
        crewLabel = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=PLocalizer.Crew, text_scale=0.036, text_align=TextNode.ALeft, text_pos=(0.475,
                                                                                                                                                           0.46), text_fg=(1,
                                                                                                                                                                           1,
                                                                                                                                                                           1,
                                                                                                                                                                           1), text_shadow=(0,
                                                                                                                                                                                            0,
                                                                                                                                                                                            0,
                                                                                                                                                                                            1))
        self.crewLimit = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text='', text_scale=0.045, text_align=TextNode.ACenter, text_pos=(0.56,
                                                                                                                                                     0.15), text_fg=(1,
                                                                                                                                                                     1,
                                                                                                                                                                     1,
                                                                                                                                                                     1), text_shadow=(0,
                                                                                                                                                                                      0,
                                                                                                                                                                                      0,
                                                                                                                                                                                      1), textMayChange=1, text_font=PiratesGlobals.getInterfaceOutlineFont())
        shipOV = base.cr.getOwnerView(self.shipId)
        if shipOV:
            self.setShipName(shipOV.name)
            self.setShipClass(shipOV.shipClass)
            self.setShipHp(shipOV.Hp, shipOV.maxHp)
            self.setShipSp(shipOV.Sp, shipOV.maxSp)
            self.setShipCrew(shipOV.crew, shipOV.maxCrew)
            self.setShipCargo([], shipOV.maxCargo)
        hullOVs = base.cr.getOwnerViewDoList(DistributedHullOV)
        hullOVs = [ ov for ov in hullOVs if ov.shipId == self.shipId ]
        for hullOV in hullOVs:
            self.setShipMaxCannons(hullOV.cannonConfig)
            self.setShipMaxLeftBroadside(hullOV.lBroadsideConfig)
            self.setShipMaxRightBroadside(hullOV.rBroadsideConfig)

        self.accept('setName-%s' % self.shipId, self.setShipName)
        self.accept('setShipClass-%s' % self.shipId, self.setShipClass)
        self.accept('setShipHp-%s' % self.shipId, self.setShipHp)
        self.accept('setShipSp-%s' % self.shipId, self.setShipSp)
        self.accept('setShipCargo-%s' % self.shipId, self.setShipCargo)
        self.accept('setShipCrew-%s' % self.shipId, self.setShipCrew)
        self.accept('setShipTimer-%s' % self.shipId, self.setShipTimer)
        self.accept('setHullCannonConfig-%s' % self.shipId, self.setShipMaxCannons)
        self.accept('setHullLeftBroadsideConfig-%s' % self.shipId, self.setShipMaxLeftBroadside)
        self.accept('setHullRightBroadsideConfig-%s' % self.shipId, self.setShipMaxRightBroadside)
        if base.config.GetBool('want-deploy-button', 0):
            pass
        return

    def destroy(self):
        self.ignoreAll()
        self.crewDots = []
        self.hullCards = []
        DirectFrame.destroy(self)

    def setShipId(self, shipId):
        self.shipId = shipId

    def getShipId(self):
        return self.shipId

    def setShipName(self, name, team=None):
        self.nameLabel['text'] = PLocalizer.makeHeadingString(name, 2)

    def setShipClass(self, shipClass):
        self.classLabel['text'] = PLocalizer.makeHeadingString(PLocalizer.ShipClassNames.get(shipClass), 1)

    def setShipHp(self, hp, maxHp):
        self.hpMeter['text'] = '%d/%d' % (hp, maxHp)
        self.hpMeter['range'] = maxHp
        self.hpMeter['value'] = hp

    def setShipSp(self, sp, maxSp):
        self.speedMeter['text'] = '%d/%d' % (sp, maxSp)
        self.speedMeter['range'] = maxSp
        self.speedMeter['value'] = sp

    def setShipPlunderLimit(self, current, limit):
        self.plunderLimit['text'] = str(limit)

    def setShipCrew(self, crewArray, maxCrewCount):
        if len(self.crewDots) != maxCrewCount:
            for dot in self.crewDots:
                dot.destroy()

            self.crewDots = []
        if not self.crewDots:
            gui = loader.loadModel('models/gui/toplevel_gui')
            crewDotGeom = [gui.find('**/topgui_icon_ship_crewdot_off'), gui.find('**/topgui_icon_ship_crewdot_on')]
            columns = 2
            for x in range(maxCrewCount):
                crewDot = DirectButton(parent=self, relief=None, geom=(crewDotGeom[1], crewDotGeom[1], crewDotGeom[1], crewDotGeom[0]), pos=(0.54 + 0.04 * (x % columns), 0, 0.418 - 0.04 * (x / columns)), scale=0.5)
                self.crewDots.append(crewDot)

        crewCount = len(crewArray)
        for x in range(maxCrewCount):
            if crewCount > x:
                self.crewDots[x]['state'] = DGG.NORMAL
            else:
                self.crewDots[x]['state'] = DGG.DISABLED

        self.crewLimit['text'] = '%d/%d' % (crewCount, maxCrewCount)
        return

    def setShipCargo(self, cargo, maxCargo):
        self.plunderLimit['text'] = str(maxCargo)

    def setShipTimer(self, timeLeft):
        if timeLeft:
            self.timer.unstash()
            self.timer.countdown(timeLeft)
        else:
            self.timer.timerExpired()
            self.timer.stop()
            self.timer.stash()

    def setShipMaxCannons(self, cannonConfig):
        self.cannonLimit['text'] = str(len(cannonConfig) - cannonConfig.count(0))

    def setShipMaxLeftBroadside(self, broadsideConfig):
        self.lBroadsideLimit = len(broadsideConfig)
        self.broadsideLeftLimit['text'] = '%d' % (self.lBroadsideLimit - broadsideConfig.count(0))

    def setShipMaxRightBroadside(self, broadsideConfig):
        self.rBroadsideLimit = len(broadsideConfig)
        self.broadsideRightLimit['text'] = '%d' % (self.rBroadsideLimit - broadsideConfig.count(0))
# okay decompiling .\pirates\piratesgui\ShipPanel.pyc
