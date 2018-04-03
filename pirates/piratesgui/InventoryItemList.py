# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.InventoryItemList
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryItemGui
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.battle import WeaponGlobals
from pirates.piratesgui.InventoryList import InventoryList

class InventoryItemList(InventoryList):
    __module__ = __name__

    def __init__(self, inventory, height, trade=0, buy=0, sell=0, use=0, weapon=0, listItemClass=InventoryItemGui.InventoryItemGui, listItemWidth=PiratesGuiGlobals.InventoryItemGuiWidth):
        InventoryList.__init__(self, inventory=inventory, height=height, trade=trade, buy=buy, sell=sell, use=use, weapon=weapon, listItemClass=listItemClass, listItemWidth=listItemWidth, listItemHeight=PiratesGuiGlobals.InventoryItemGuiHeight)
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
# okay decompiling .\pirates\piratesgui\InventoryItemList.pyc
