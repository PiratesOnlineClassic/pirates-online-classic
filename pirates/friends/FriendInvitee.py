# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.friends.FriendInvitee
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from otp.otpbase import OTPGlobals, OTPLocalizer
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import GuiPanel, PDialog, PiratesGuiGlobals
from pirates.piratesgui.RequestButton import RequestButton


class FriendInviteeButton(RequestButton):
    __module__ = __name__

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(FriendInviteeButton)


class FriendInvitee(GuiPanel.GuiPanel):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendInvitee')

    def __init__(self, avId, avName, isPlayerInvite):
        GuiPanel.GuiPanel.__init__(self, 'Friend Invitation', 0.5, 0.5)
        self.initialiseoptions(FriendInvitee)
        self.setPos(0.15, 0, 0.25)
        self.avId = avId
        self.avName = avName
        self.isPlayerInvite = isPlayerInvite
        if base.cr.avatarFriendsManager.checkIgnored(self.avId):
            self.__handleNo()
            return
        if self.isPlayerInvite:
            text = OTPLocalizer.FriendInviteeInvitation % (self.avName + "'s player")
        else:
            text = OTPLocalizer.FriendInviteeInvitation % self.avName
        self.message = DirectLabel(parent=self, relief=None, text=text, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.25,
                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                      0.35), textMayChange=1)
        self.bOk = FriendInviteeButton(text=OTPLocalizer.FriendInviteeOK, command=self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.1, 0, 0.05)
        self.bNo = FriendInviteeButton(text=OTPLocalizer.FriendInviteeNo, command=self.__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.3, 0, 0.05)
        self.accept('cancelFriendInvitation', self.__handleCancelFromAbove)
        return

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.ignore('cancelFriendInvitation')
        GuiPanel.GuiPanel.destroy(self)

    def __handleOk(self):
        if self.isPlayerInvite:
            base.cr.playerFriendsManager.sendRequestInvite(self.avId)
        else:
            base.cr.avatarFriendsManager.sendRequestInvite(self.avId)
        self.destroy()

    def __handleNo(self):
        if self.isPlayerInvite:
            base.cr.playerFriendsManager.sendRequestDecline(self.avId)
        else:
            base.cr.avatarFriendsManager.sendRequestRemove(self.avId)
        self.destroy()

    def __handleCancelFromAbove(self):
        self.destroy()
# okay decompiling .\pirates\friends\FriendInvitee.pyc
