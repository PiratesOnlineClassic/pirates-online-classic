# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.ScoreFrame
from pirates.piratesgui.SheetFrame import SheetFrame


class ScoreFrame(SheetFrame):
    

    def __init__(self, w, h, holder, team, **kw):
        self.team = team
        title = holder.getTeamName(self.team)
        SheetFrame.__init__(self, w, h, title, holder, **kw)
        self.initialiseoptions(ScoreFrame)
        self.scoreChanged = False

    def getItemList(self):
        return self.holder.getItemList(self.team)

    def _handleItemChange(self):
        self.scoreChanged = True

    def show(self):
        if self.scoreChanged:
            self.scoreChanged = False
            self.redraw()
        SheetFrame.show(self)
# okay decompiling .\pirates\piratesgui\ScoreFrame.pyc
