from direct.gui.DirectGui import *
from panda3d.core import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryPage

class ClothingPage(InventoryPage.InventoryPage):
    
    def __init__(self):
        InventoryPage.InventoryPage.__init__(self)
        self.initialiseoptions(ClothingPage)


