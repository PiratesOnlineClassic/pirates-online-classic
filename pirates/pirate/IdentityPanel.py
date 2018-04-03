# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pirate.IdentityPanel
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
    __module__ = __name__

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
# okay decompiling .\pirates\pirate\IdentityPanel.pyc
