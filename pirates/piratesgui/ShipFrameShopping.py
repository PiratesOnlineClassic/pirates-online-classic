# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.ShipFrameShopping
from direct.gui.DirectGui import *
from panda3d.core import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.ShipFrameSelect import ShipFrameSelect
from pirates.piratesgui.ShipSnapshot import ShipSnapshot


class ShipFrameShopping(ShipFrameSelect):
    

    def __init__(self, parent, **kw):
        optiondefs = (('mode', 'repair', None), )
        self.defineoptions(kw, optiondefs)
        ShipFrameSelect.__init__(self, parent, **kw)
        self.initialiseoptions(ShipFrameShopping)
        return

    def enableStatsOV(self, shipOV):
        self.snapShot = ShipSnapshot(self, shipOV, pos=self['snapShotPos'])
        typeStr = PLocalizer.YourShip
        if shipOV.state not in 'Off':
            self.button['state'] = DGG.DISABLED
        else:
            self.button['state'] = DGG.NORMAL
        if shipOV.Hp <= 0:
            self['shipColorScale'] = VBase4(1, 0.4, 0.4, 1)
        if self['mode'] == 'repair':
            self.button['text'] = PLocalizer.InteractRepair
            if shipOV.Hp == shipOV.maxHp:
                self.button['state'] = DGG.DISABLED
        else:
            if self['mode'] == 'sell':
                self.button['text'] = PLocalizer.InteractSellShips
            else:
                if self['mode'] == 'overhaul':
                    self.button['text'] = PLocalizer.InteractOverhaul
# okay decompiling .\pirates\piratesgui\ShipFrameShopping.pyc
