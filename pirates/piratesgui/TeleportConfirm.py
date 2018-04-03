# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.TeleportConfirm
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

class TeleportConfirmButton(RequestButton):
    __module__ = __name__

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(TeleportConfirmButton)


class TeleportConfirm(GuiPanel.GuiPanel):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('TeleportConfirm')

    def __init__(self, avId, avName):
        GuiPanel.GuiPanel.__init__(self, PLocalizer.TeleportConfirmTitle, 0.5, 0.5)
        self.initialiseoptions(TeleportConfirm)
        self.setPos(0.15, 0, 0.25)
        self.avId = avId
        self.avName = avName
        if base.cr.avatarFriendsManager.checkIgnored(self.avId):
            self.__handleNo()
            return
        text = PLocalizer.TeleportConfirmMessage % self.avName
        self.message = DirectLabel(parent=self, relief=None, text=text, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.25,
                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                      0.35), textMayChange=1)
        self.bOk = TeleportConfirmButton(text=PLocalizer.TeleportConfirmOK, command=self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.1, 0, 0.05)
        self.bNo = TeleportConfirmButton(text=PLocalizer.TeleportConfirmNo, command=self.__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.3, 0, 0.05)
        av = base.cr.getDo(avId)
        if av:
            self.accept(av.getDisableEvent(), self.__handleAvatarLeft)
        return

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.ignore('BandRequestCancel-%s' % (self.avId,))
        self.ignore('Esc')
        GuiPanel.GuiPanel.destroy(self)

    def __handleOk(self):
        base.localAvatar.guiMgr.handleGotoAvatar(self.avId, self.avName)
        self.destroy()

    def __handleNo(self):
        self.destroy()

    def __handleAvatarLeft(self):
        if not base.cr.identifyAvatar(self.avId):
            self.destroy()
# okay decompiling .\pirates\piratesgui\TeleportConfirm.pyc
