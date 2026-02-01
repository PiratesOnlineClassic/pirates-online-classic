from direct.gui.DirectGui import *
from panda3d.core import *
from pirates.piratesgui import PiratesGuiGlobals

class SocialPage(DirectFrame):
    
    def __init__(self, title):
        spacer = 0.1
        DirectFrame.__init__(self, relief = None, state = DGG.NORMAL, frameColor = PiratesGuiGlobals.FrameColor, borderWidth = PiratesGuiGlobals.BorderWidth, frameSize = (0.0, PiratesGuiGlobals.SocialPageWidth, spacer, PiratesGuiGlobals.SocialPageHeight - PiratesGuiGlobals.GridCell), pos = (PiratesGuiGlobals.BorderWidth[0], 0, PiratesGuiGlobals.BorderWidth[0] + PiratesGuiGlobals.GridCell), sortOrder = 5)
        self.initialiseoptions(SocialPage)
        self.title = title
    
    def show(self):
        DirectFrame.show(self)

    def hide(self):
        DirectFrame.hide(self)


