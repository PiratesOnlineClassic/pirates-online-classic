from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals

class InventoryPage(DirectFrame):
    
    def __init__(self):
        DirectFrame.__init__(self, relief = None, state = DGG.DISABLED, frameColor = PiratesGuiGlobals.FrameColor, borderWidth = PiratesGuiGlobals.BorderWidth, frameSize = (0.0, PiratesGuiGlobals.InventoryPageWidth, 0.0, PiratesGuiGlobals.InventoryPageHeight), pos = (-0.54000000000000004, 0, -0.71999999999999997))
        self.initialiseoptions(InventoryPage)
    
    def show(self):
        DirectFrame.show(self)

    def hide(self):
        DirectFrame.hide(self)
    
    def slideOpenCallback(self):
        pass

    def slideCloseCallback(self):
        pass
    
    def slideOpenPrecall(self):
        pass


