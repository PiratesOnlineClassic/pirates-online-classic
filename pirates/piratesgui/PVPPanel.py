# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.PVPPanel
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.GuiPanel import GuiPanel
from pirates.piratesgui.ListFrame import ListFrame
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PVPRankGui

class PVPPanel(DirectFrame):
    __module__ = __name__

    def __init__(self, name, holder=None):
        w = PiratesGuiGlobals.PVPPanelWidth
        h = PiratesGuiGlobals.PVPPanelHeight
        DirectFrame.__init__(self, relief=None, frameSize=(0.0, w, 0.0, h))
        self.initialiseoptions(PVPPanel)
        self.list = ListFrame(PiratesGuiGlobals.PVPPageWidth, None, name, holder, frameColor=(0,
                                                                                              0,
                                                                                              0,
                                                                                              0))
        self.list.setup()
        self.list.reparentTo(self)
        self.list.setPos(0.005, 0.2, 0.17)
        self.renownDisplay = None
        if base.config.GetBool('want-infamy', 0) and not self.renownDisplay:
            self.renownDisplay = PVPRankGui.PVPRankGui(parent=base.a2dBottomRight, displayType=PVPRankGui.LAND_RENOWN_DISPLAY)
            self.renownDisplay.setPos(0.0, 0.0, 0.0)
        return

    def destroy(self):
        if self.list:
            self.list.destroy()
            self.list = None
        if self.renownDisplay:
            self.renownDisplay.destroy()
            self.renownDisplay = None
        DirectFrame.destroy(self)
        return

    def cleanup(self):
        self.list.cleanup()

    def show(self):
        DirectFrame.show(self)
        if self.renownDisplay:
            self.renownDisplay.show()

    def hide(self):
        DirectFrame.hide(self)
        if self.renownDisplay:
            self.renownDisplay.hide()
# okay decompiling .\pirates\piratesgui\PVPPanel.pyc
