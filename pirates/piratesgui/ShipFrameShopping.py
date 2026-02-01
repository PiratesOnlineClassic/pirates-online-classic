from direct.gui.DirectGui import *
from panda3d.core import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.ShipFrameSelect import ShipFrameSelect
from pirates.piratesgui.ShipSnapshot import ShipSnapshot

class ShipFrameShopping(ShipFrameSelect):
    
    def __init__(self, parent, **kw):
        optiondefs = (('mode', 'repair', None),)
        self.defineoptions(kw, optiondefs)
        ShipFrameSelect.__init__(self, parent, **kw)
        self.initialiseoptions(ShipFrameShopping)

    def enableStatsOV(self, shipOV):
        self.snapShot = ShipSnapshot(self, shipOV, pos = self['snapShotPos'])
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
            
        elif self['mode'] == 'sell':
            self.button['text'] = PLocalizer.InteractSellShips
        elif self['mode'] == 'overhaul':
            self.button['text'] = PLocalizer.InteractOverhaul
        


