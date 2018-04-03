# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.TeleportBlockerPanel
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.showbase.PythonUtil import GoldenRectangle
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PLocalizer, PiratesGlobals

class TeleportBlockerPanel(GuiPanel.GuiPanel):
    __module__ = __name__
    _Messages = {PiratesGlobals.TFInBattle.getWord(): PLocalizer.TeleportBlockerMsgBattle, PiratesGlobals.TFOnShip.getWord(): PLocalizer.TeleportBlockerMsgOnShip, PiratesGlobals.TFInPVP.getWord(): PLocalizer.TeleportBlockerMsgInPVP}

    def __init__(self):
        message = TeleportBlockerPanel._Messages.get(localAvatar.getMaxTeleportFlag().getWord(), "You can't teleport from here")
        height = 0.6
        GuiPanel.GuiPanel.__init__(self, PLocalizer.TeleportBlockerPanelTitle, GoldenRectangle.getLongerEdge(height), height)
        self._message = DirectLabel(parent=self, relief=None, text=message, text_pos=(0.2,
                                                                                      0), text_scale=0.072, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=9, pos=(0.291294,
                                                                                                                                                                                                                                            0,
                                                                                                                                                                                                                                            0.400258), textMayChange=1)
        taskMgr.doMethodLater(10, self.destroy, 'teleportBlockerTimer', extraArgs=[])
        return

    def destroy(self):
        taskMgr.remove('teleportBlockerTimer')
        GuiPanel.GuiPanel.destroy(self)
# okay decompiling .\pirates\piratesgui\TeleportBlockerPanel.pyc
