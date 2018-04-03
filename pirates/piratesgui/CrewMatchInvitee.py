# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.CrewMatchInvitee
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

class CrewMatchInviteeButton(RequestButton):
    __module__ = __name__

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(CrewMatchInviteeButton)


class CrewMatchInvitee(GuiPanel.GuiPanel):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('CrewMatchInvitee')

    def __init__(self, avId, avName, location, initialRequest=False, crewType=1):
        GuiPanel.GuiPanel.__init__(self, PLocalizer.CrewMatchCrewLookout, 0.5, 0.5, showClose=False)
        self.initialiseoptions(CrewMatchInvitee)
        self.setPos(0.15, 0, 0.25)
        self.avId = avId
        self.avName = avName
        self.initialRequest = initialRequest
        self.location = location
        self.crewType = crewType
        if location != '':
            text = PLocalizer.CrewMatchInviteeInvitation % (self.avName, self.location)
        else:
            text = PLocalizer.CrewMatchInviteeInvitationNoLocation % self.avName
        self.message = DirectLabel(parent=self, relief=None, text=text, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.25,
                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                      0.35), textMayChange=1)
        self.bOk = CrewMatchInviteeButton(text=PLocalizer.CrewInviteeOK, command=self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.1, 0, 0.05)
        self.bNo = CrewMatchInviteeButton(text=PLocalizer.CrewInviteeNo, command=self.__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.3, 0, 0.05)
        self.accept('clientLogout', self.destroy)
        self.accept('destroyCrewMatchInvite', self.destroy)
        return

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.ignore('Esc')
        GuiPanel.GuiPanel.destroy(self)

    def __handleOk(self):
        if self.initialRequest:
            base.cr.pirateCrewMatch.acceptInitialInviteGUI()
        else:
            base.cr.pirateCrewMatch.acceptInvite()
            base.cr.pirateCrewMatch.offerCurrentlyOnScreen = False
        self.destroy()

    def __handleNo(self):
        if self.initialRequest:
            base.cr.pirateCrewMatch.putAvatarOnLookoutList(self.crewType)
        else:
            base.cr.pirateCrewMatch.offerCurrentlyOnScreen = False
            base.cr.pirateCrewMatch.checkOfferCache()
        self.destroy()

    def __handleCancelFromAbove(self):
        self.destroy()
# okay decompiling .\pirates\piratesgui\CrewMatchInvitee.pyc
