# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.InventoryPage
from direct.gui.DirectGui import *
from panda3d.core import *
from pirates.piratesgui import PiratesGuiGlobals


class InventoryPage(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(
            self,
            relief=None,
            state=DGG.DISABLED,
            frameColor=PiratesGuiGlobals.FrameColor,
            borderWidth=PiratesGuiGlobals.BorderWidth,
            frameSize=(0.0, PiratesGuiGlobals.InventoryPageWidth, 0.0,
                       PiratesGuiGlobals.InventoryPageHeight),
            pos=(-0.54, 0, -0.72))
        self.initialiseoptions(InventoryPage)
        return

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


# okay decompiling .\pirates\piratesgui\InventoryPage.pyc
