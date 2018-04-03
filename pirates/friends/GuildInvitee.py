# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.friends.GuildInvitee
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from otp.otpbase import OTPLocalizer
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesgui.RequestButton import RequestButton


class GuildInviteeButton(RequestButton):
    __module__ = __name__

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(GuildInviteeButton)


class GuildInvitee(GuiPanel.GuiPanel):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('GuildInvitee')

    def __init__(self, avId, avName, guildId, guildName):
        GuiPanel.GuiPanel.__init__(self, 'Guild Invitation', 0.5, 0.5)
        self.initialiseoptions(GuildInvitee)
        self.setPos(0.15, 0, 0.25)
        self.avId = avId
        self.avName = avName
        self.guildId = guildId
        if base.cr.avatarFriendsManager.checkIgnored(self.avId):
            self.__handleNo()
            return
        if guildName == 0 or guildName == '' or guildName == '0':
            self.guildName = PLocalizer.GuildDefaultName % self.guildId
        else:
            self.guildName = guildName
        text = OTPLocalizer.GuildInviteeInvitation % (self.avName, self.guildName)
        self.message = DirectLabel(parent=self, relief=None, text=text, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.25,
                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                      0.35), textMayChange=1)
        self.bOk = GuildInviteeButton(text=OTPLocalizer.GuildInviteeOK, command=self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.1, 0, 0.05)
        self.bNo = GuildInviteeButton(text=OTPLocalizer.GuildInviteeNo, command=self.__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.3, 0, 0.05)
        self.accept('cancelGuildInvitation', self.__handleCancelFromAbove)
        return

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.ignore('cancelGuildInvitation')
        GuiPanel.GuiPanel.destroy(self)

    def __handleOk(self):
        base.cr.guildManager.sendAcceptInvite()
        self.destroy()

    def __handleNo(self):
        base.cr.guildManager.sendDeclineInvite()
        self.destroy()

    def __handleCancelFromAbove(self):
        self.destroy()
# okay decompiling .\pirates\friends\GuildInvitee.pyc
