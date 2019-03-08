from direct.showbase.ShowBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.avatar import Avatar
from otp.otpbase import OTPGlobals
from pirates.friends import PirateFriendSecret
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PirateButtonChain
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import Freebooter

class IdentityPanel(GuiPanel.GuiPanel):
    
    def __init__(self, Id, Name, width, height, **kw):
        self.width = width
        GuiPanel.GuiPanel.__init__(self, Name, self.width, height, False, 1, **kw)
        self.initialiseoptions(IdentityPanel)
        self.Name = Name
        self.Id = Id
        self.avDisableName = 'disable-%s' % self.Id
        self.chain = PirateButtonChain.PirateButtonChain(width, self)
        self.load()
        self.determineButtonState()
    
    def load(self):
        pass

    def destroy(self):
        self.ignoreAll()
        if hasattr(self, 'destroyed'):
            return
        
        self.destroyed = 1
        self.chain.destroy()
        GuiPanel.GuiPanel.destroy(self)
    
    def determineButtonState(self):
        pass


