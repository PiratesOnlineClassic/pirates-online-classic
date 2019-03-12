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

class CrewInviteeButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(CrewInviteeButton)



class CrewInvitee(GuiPanel.GuiPanel):
    notify = DirectNotifyGlobal.directNotify.newCategory('CrewInvitee')
    
    def __init__(self, avId, avName):
        GuiPanel.GuiPanel.__init__(self, 'Crew Invitation', 0.5, 0.5, showClose = False)
        self.initialiseoptions(CrewInvitee)
        self.setPos(0.15, 0, 0.25)
        self.avId = avId
        self.avName = avName
        if base.cr.avatarFriendsManager.checkIgnored(self.avId):
            self.__handleNo()
            return None
        
        text = PLocalizer.CrewInviteeInvitation % self.avName
        self.message = DirectLabel(parent = self, relief = None, text = text, text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.25, 0, 0.35), textMayChange = 1)
        self.bOk = CrewInviteeButton(text = PLocalizer.CrewInviteeOK, command = self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.1, 0, 0.05)
        self.bNo = CrewInviteeButton(text = PLocalizer.CrewInviteeNo, command = self.__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.3, 0, 0.05)
        self.accept('BandRequestCancel-%s' % (self.avId,), self.__handleCancelFromAbove)
    
    def destroy(self):
        if hasattr(self, 'destroyed'):
            return None
        
        self.destroyed = 1
        self.ignore('BandRequestCancel-%s' % (self.avId,))
        self.ignore('Esc')
        GuiPanel.GuiPanel.destroy(self)
    
    def __handleOk(self):
        base.cr.PirateBandManager.d_invitationResponce(self.avId, BandConstance.outcome_ok)
        self.destroy()

    def __handleNo(self):
        base.cr.PirateBandManager.d_invitationResponce(self.avId, BandConstance.outcome_declined)
        self.destroy()
    
    def __handleCancelFromAbove(self):
        self.destroy()


