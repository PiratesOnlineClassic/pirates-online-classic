# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pirate.IdentityPanel
from direct.gui.DirectGui import *
from direct.showbase.ShowBaseGlobal import *
from otp.avatar import Avatar
from otp.otpbase import OTPGlobals
from panda3d.core import *
from pirates.friends import PirateFriendSecret
from pirates.piratesbase import Freebooter, PiratesGlobals, PLocalizer
from pirates.piratesgui import GuiPanel, PirateButtonChain, PiratesGuiGlobals


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
# okay decompiling .\pirates\pirate\IdentityPanel.pyc
