from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PDialog
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.band import BandConstance
from pirates.piratesgui.RequestButton import RequestButton

class PiratesConfirmButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(PiratesConfirmButton)



class PiratesConfirm(GuiPanel.GuiPanel):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesConfirm')
    
    def __init__(self, title, message, command, avId = None, tattoo = None, barber = None):
        GuiPanel.GuiPanel.__init__(self, title, 0.5, 0.5)
        self.initialiseoptions(PiratesConfirm)
        self.command = command
        self.avId = avId
        self.tattoo = tattoo
        self.barber = barber
        if base.cr.avatarFriendsManager.checkIgnored(self.avId):
            self.__handleNo()
            return None
        
        text = message
        self.message = DirectLabel(parent = self, relief = None, text = message, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.25, 0, 0.35), textMayChange = 1)
        self.bOk = PiratesConfirmButton(text = PLocalizer.GenericConfirmOK, command = self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.1, 0, 0.05)
        self.bNo = PiratesConfirmButton(text = PLocalizer.GenericConfirmNo, command = self.__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.3, 0, 0.05)
        self.accept('clientLogout', self.destroy)

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignore('BandRequestCancel-%s' % (self.avId,))
        self.ignore('Esc')
        GuiPanel.GuiPanel.destroy(self)

    def __handleOk(self):
        if self.avId:
            self.command(self.avId)
        elif self.tattoo:
            self.command(self.tattoo[0], self.tattoo[1], self.tattoo[2])
        elif self.barber:
            self.command(self.barber[0], self.barber[1], self.barber[2])
        else:
            self.command()
        self.destroy()

    def __handleNo(self):
        self.destroy()
    
    def __handleCancelFromAbove(self):
        self.destroy()


