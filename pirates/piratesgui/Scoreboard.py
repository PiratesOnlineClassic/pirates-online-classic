# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.Scoreboard
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesgui.ListFrame import ListFrame
from pirates.piratesgui.ScoreboardItemGui import ScoreboardItemGui


class Scoreboard(DirectFrame):
    __module__ = __name__

    def __init__(self, name, width, height, results, titleHeight=1.0):
        DirectFrame.__init__(self, relief=None, state=DGG.NORMAL, frameColor=PiratesGuiGlobals.FrameColor, borderWidth=PiratesGuiGlobals.BorderWidth, pos=(0, 0, -0.03))
        self.initialiseoptions(Scoreboard)
        self.width = width
        self.height = height
        self.titleHeight = titleHeight
        self.results = results
        self.listHeight = self.height
        width = self.width - 0.02
        height = self.height - self.titleHeight - 0.17
        self.list = ListFrame(width - 0.02, 0, name, self, delayedReveal=1)
        self.list.setup()
        self.list.reparentTo(self)
        self.setPos(0.01, 0, 0.01)
        items = self.list.items
        itemHeight = 0.0
        for item in items:
            itemHeight += item.getHeight()

        newZ = height - itemHeight
        self.list.setZ(newZ)
        return

    def destroy(self):
        self.list.destroy()
        DirectFrame.destroy(self)

    def getItemList(self):
        return self.results

    def getItemChangeMsg(self):
        return self.taskName('tmRewardChanged')

    def createNewItem(self, item, parent, itemType=None, columnWidths=[], color=None):
        width = self.width - 0.02
        height = self.listHeight / (len(self.getItemList()) + 1)
        if height > 0.1:
            height = 0.1
        if item.get('Type') == 'Space':
            height = height / 3
        return ScoreboardItemGui(item, width, height, parent)
# okay decompiling .\pirates\piratesgui\Scoreboard.pyc
