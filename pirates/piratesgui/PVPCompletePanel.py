# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.PVPCompletePanel
from direct.gui.DirectGui import *
from panda3d.core import *
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui.ListFrame import ListFrame
from pirates.piratesgui.SheetFrame import SheetFrame
from pirates.piratesgui.StatRowGui import StatRowGui
from pirates.piratesgui.StatRowHeadingGui import StatRowHeadingGui
from pirates.treasuremap.RewardItemGui import RewardItemGui


class PVPCompletePanel(BorderFrame):

    SUMMARY_PAGE = 1
    DETAILS_PAGE = 2

    def __init__(self, name, pvp):
        self.width = PiratesGuiGlobals.PVPCompletePanelWidth
        self.height = PiratesGuiGlobals.PVPCompletePanelHeight
        BorderFrame.__init__(self, frameSize=(0, self.width, 0, self.height))
        self.initialiseoptions(PVPCompletePanel)
        self.endButton = GuiButton(
            parent=self,
            text=PLocalizer.PVPExit,
            command=pvp.requestPVPLeave,
            pos=(1.25, 0, 0.1))
        self.name = name
        self.title = DirectLabel(
            parent=self,
            relief=None,
            text=name,
            text_align=TextNode.ALeft,
            text_scale=0.09,
            text_fg=PiratesGuiGlobals.TextFG1,
            text_shadow=PiratesGuiGlobals.TextShadow,
            textMayChange=1,
            pos=(0.2, 0, 1.55))
        self.outcome = DirectLabel(
            parent=self,
            relief=None,
            text='',
            text_align=TextNode.ARight,
            text_scale=0.09,
            text_fg=PiratesGuiGlobals.TextFG1,
            text_shadow=PiratesGuiGlobals.TextShadow,
            textMayChange=1,
            pos=(2.2, 0, 1.55))
        self.game = pvp
        return

    def setOutcome(self, outcome):
        self.outcome['text'] = outcome


# okay decompiling .\pirates\piratesgui\PVPCompletePanel.pyc
