# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.SocialPage
from direct.gui.DirectGui import *
from panda3d.core import *
from pirates.piratesgui import PiratesGuiGlobals


class SocialPage(DirectFrame):

    def __init__(self, title):
        spacer = 0.1
        DirectFrame.__init__(
            self,
            relief=None,
            state=DGG.NORMAL,
            frameColor=PiratesGuiGlobals.FrameColor,
            borderWidth=PiratesGuiGlobals.BorderWidth,
            frameSize=(0.0, PiratesGuiGlobals.SocialPageWidth, spacer,
                       PiratesGuiGlobals.SocialPageHeight -
                       PiratesGuiGlobals.GridCell),
            pos=(PiratesGuiGlobals.BorderWidth[0], 0,
                 PiratesGuiGlobals.BorderWidth[0] + PiratesGuiGlobals.GridCell),
            sortOrder=5)
        self.initialiseoptions(SocialPage)
        self.title = title
        return

    def show(self):
        DirectFrame.show(self)

    def hide(self):
        DirectFrame.hide(self)


# okay decompiling .\pirates\piratesgui\SocialPage.pyc
