# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.ShipFrame
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesbase import PiratesGlobals
from pirates.ship.ShipMeter import ShipMeter

class ShipFrame(DirectFrame):
    __module__ = __name__
    logos = None

    def __init__(self, parent, **kw):
        optiondefs = (('state', DGG.DISABLED, None), ('frameSize', (0.0, 1, 0.0, 0.5), None), ('relief', DGG.FLAT, None), ('shipId', 0, None), ('shipName', '', None), ('shipClass', 0, None), ('shipPos', Point3(0, 0, 0), None), ('shipHpr', VBase3(-90, 0, 0), None), ('shipScale', VBase3(1), None), ('shipColorScale', VBase4(1), self.setShipColorScale), ('siegeTeam', 0, None), ('mastInfo', [], None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        self.initialiseoptions(ShipFrame)
        self.shipDisplay = None
        self.shipMeter = None
        self.createGui()
        return

    def destroy(self):
        self.shipDisplay = None
        if self.shipMeter:
            self.shipMeter.destroy()
            self.shipMeter = None
        DirectFrame.destroy(self)
        return

    def createGui(self):
        self.shipDisplay = self.attachNewNode('shipDisplay')
        self.shipDisplay.setPos(self['shipPos'])
        self.shipDisplay.setHpr(self['shipHpr'])
        self.shipDisplay.setScale(self['shipScale'])
        self.shipDisplay.setColorScale(self['shipColorScale'])
        self.shipMeter = ShipMeter(self['shipId'], self['shipClass'], self['mastInfo'], siegeTeam=self['siegeTeam'])
        if not ShipFrame.logos:
            ShipFrame.logos = loader.loadModel('models/textureCards/sailLogo')
        if ShipFrame.logos:
            image = None
            if self['siegeTeam'] == 1:
                image = ShipFrame.logos.find('**/logo_french_flag')
            else:
                if self['siegeTeam'] == 2:
                    image = ShipFrame.logos.find('**/logo_spanish_flag')
            if image:
                self.flag = DirectLabel(parent=self, image=image, image_scale=0.08, image_pos=(0.09,
                                                                                               0,
                                                                                               0.09))
        self.shipMeter.reparentTo(self.shipDisplay)
        self.shipMeter.setDepthTest(1)
        self.shipMeter.setDepthWrite(1)
        return

    def setShipColorScale(self):
        if self.shipDisplay:
            self.shipDisplay.setColorScale(self['shipColorScale'])
# okay decompiling .\pirates\piratesgui\ShipFrame.pyc
