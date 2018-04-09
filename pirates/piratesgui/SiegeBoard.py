# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.SiegeBoard
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.ScoreFrame import ScoreFrame


class SiegeBoard:
    __module__ = __name__

    def __init__(self, holder):
        self.one = ScoreFrame(PiratesGuiGlobals.ScorePanelWidth, PiratesGuiGlobals.ScorePanelHeight, holder, 1, sortOrder=2)
        self.one.setPos(-1.25, 0, -0.6)
        self.one.hide()
        self.two = ScoreFrame(PiratesGuiGlobals.ScorePanelWidth, PiratesGuiGlobals.ScorePanelHeight, holder, 2, sortOrder=2)
        self.two.setPos(-1.25 + PiratesGuiGlobals.ScorePanelWidth + 0.01, 0, -0.6)
        self.two.hide()

    def hide(self):
        self.one.hide()
        self.two.hide()

    def show(self):
        self.one.show()
        self.two.show()

    def destroy(self):
        self.one.hide()
        self.two.hide()
        self.one.destroy()
        self.two.destroy()
# okay decompiling .\pirates\piratesgui\SiegeBoard.pyc
