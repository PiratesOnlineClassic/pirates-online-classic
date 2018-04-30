# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.ShipItemList
from direct.gui.DirectGui import *
from panda3d.core import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import (InventoryItemList, PiratesGuiGlobals,
                                ShipItemGUI)


class ShipItemList(InventoryItemList.InventoryItemList):
    

    def __init__(self, inventory, height, trade=0, buy=0, sell=0, use=0):
        InventoryItemList.InventoryItemList.__init__(self, inventory, height, trade, buy, sell, use)
        self.initialiseoptions(ShipItemList)

    def loadInventoryPanels(self):
        for item in self.inventory:
            data = [
             item, 1]
            self.addPanel(data, repack=0)

        self.repackPanels()

    def addPanel(self, data, repack=1):
        panel = ShipItemGUI.ShipItemGUI(data, trade=self.trade, buy=self.buy, sell=self.sell, use=self.use)
        panel.reparentTo(self.getCanvas())
        self.panels.append(panel)
        if repack:
            self.repackPanels()

    def repackPanels(self):
        invHeight = len(self.inventory)
        z = 0.01 + PiratesGuiGlobals.ShipItemGuiHeight
        i = 0
        for i in range(len(self.panels)):
            self.panels[i].setPos(0.01, 0, -z * (i + 1))
            self.panels[i].origionalPos = self.panels[i].getPos(render2d)

        self['canvasSize'] = (
         0, PiratesGuiGlobals.ShipItemGuiWidth - 0.09, -z * (i + 1), 0)
# okay decompiling .\pirates\piratesgui\ShipItemList.pyc
