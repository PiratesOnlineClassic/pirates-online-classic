# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.DownloadBlockerPanel
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.showbase.PythonUtil import GoldenRectangle
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PLocalizer

class DownloadBlockerPanel(GuiPanel.GuiPanel):
    __module__ = __name__
    Reasons = Enum('GENERIC,ISLAND,BOAT,TELEPORT,LOOKOUT')
    _Messages = {Reasons.GENERIC: PLocalizer.DownloadBlockerMsgGeneric, Reasons.ISLAND: PLocalizer.DownloadBlockerMsgIsland, Reasons.BOAT: PLocalizer.DownloadBlockerMsgBoat, Reasons.TELEPORT: PLocalizer.DownloadBlockerMsgTeleport, Reasons.LOOKOUT: PLocalizer.DownloadBlockerMsgLookout}

    def __init__(self, reason=None):
        if reason is None:
            reason = DownloadBlockerPanel.Reasons.GENERIC
        height = 0.6
        GuiPanel.GuiPanel.__init__(self, PLocalizer.DownloadBlockerPanelTitle, GoldenRectangle.getLongerEdge(height), height)
        self._reason = reason
        self._message = DirectLabel(parent=self, relief=None, text=DownloadBlockerPanel._Messages[self._reason], text_pos=(0.2,
                                                                                                                           0), text_scale=0.072, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=9, pos=(0.291294,
                                                                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                                                                 0.400258), textMayChange=1)
        taskMgr.doMethodLater(10, self.destroy, 'downloadBlockerTimer', extraArgs=[])
        return

    def destroy(self):
        taskMgr.remove('downloadBlockerTimer')
        GuiPanel.GuiPanel.destroy(self)
# okay decompiling .\pirates\piratesgui\DownloadBlockerPanel.pyc
