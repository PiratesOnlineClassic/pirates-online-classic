from direct.gui.DirectGui import *
from panda3d.core import *
from pirates.piratesgui import InventoryPage, PiratesGuiGlobals


class ClothingPage(InventoryPage.InventoryPage):
    

    def __init__(self):
        InventoryPage.InventoryPage.__init__(self)
        self.initialiseoptions(ClothingPage)
