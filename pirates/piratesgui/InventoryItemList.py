from direct.gui.DirectGui import *
from panda3d.core import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryItemGui
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.battle import WeaponGlobals
from pirates.piratesgui.InventoryList import InventoryList

class InventoryItemList(InventoryList):
    
    def __init__(self, inventory, height, trade = 0, buy = 0, sell = 0, use = 0, weapon = 0, listItemClass = InventoryItemGui.InventoryItemGui, listItemWidth = PiratesGuiGlobals.InventoryItemGuiWidth):
        InventoryList.__init__(self, inventory = inventory, height = height, trade = trade, buy = buy, sell = sell, use = use, weapon = weapon, listItemClass = listItemClass, listItemWidth = listItemWidth, listItemHeight = PiratesGuiGlobals.InventoryItemGuiHeight)
        self.initialiseoptions(InventoryItemList)
        self.all_panels = []

    def getPanel(self, data):
        for panel in self.all_panels:
            if panel.data == data:
                return panel

    def filterByItemGroup(self, itemGroup):
        if len(self.all_panels) == 0:
            self.all_panels = self.panels
        
        self.panels = []
        for panel in self.all_panels:
            if getItemGroup(panel.data[0]) == itemGroup:
                self.panels.append(panel)
                panel.show()
            else:
                panel.hide()
        
        self.repackPanels()


