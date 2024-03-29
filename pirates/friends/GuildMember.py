from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PDialog
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.RequestButton import RequestButton

class GuildMemberButton(RequestButton):
    
    def __init__(self, text, command):
        RequestButton.__init__(self, text, command, 2.0)
        self.initialiseoptions(GuildMemberButton)


class GuildMember(GuiPanel.GuiPanel):
    notify = DirectNotifyGlobal.directNotify.newCategory('GuildMember')
    
    def __init__(self, avId, avName, guildId, canpromote, candemote, cankick):
        GuiPanel.GuiPanel.__init__(self, OTPLocalizer.GuildMemberTitle, 0.5, 0.5)
        self.initialiseoptions(GuildMember)
        self.setPos(0.15, 0, 0.25)
        self.avId = avId
        self.avName = avName
        self.guildId = guildId
        self.canpromote = canpromote
        self.candemote = candemote
        self.cankick = cankick
        self.message = DirectLabel(parent = self, relief = None, text = avName, text_scale = PiratesGuiGlobals.TextScaleLarge + 0.01, text_align = TextNode.ACenter, text_fg = (0.9, 1, 0.9, 1), text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.25, 0, 0.37), textMayChange = 1)
        if self.canpromote:
            self.bPromote = GuildMemberButton(text = OTPLocalizer.GuildMemberPromote, command = self.__handlePromote)
            self.bPromote.reparentTo(self)
            self.bPromote.setPos(0.2, 0, 0.25)
        
        if self.cankick:
            self.bKick = GuildMemberButton(text = OTPLocalizer.GuildMemberKick, command = self.__handleKick)
            self.bKick.reparentTo(self)
            self.bKick.setPos(0.2, 0, 0.15)
        
        if self.candemote:
            self.bDemote = GuildMemberButton(text = OTPLocalizer.GuildMemberDemote, command = self.__handleDemote)
            self.bDemote.reparentTo(self)
            self.bDemote.setPos(0.2, 0, 0.25)
        
        self.bCancel = GuildMemberButton(text = OTPLocalizer.GuildMemberCancel, command = self.__handleCancel)
        self.bCancel.reparentTo(self)
        self.bCancel.setPos(0.2, 0, 0.05)

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        
        self.destroyed = 1
        GuiPanel.GuiPanel.destroy(self)
    
    def __handlePromote(self):
        base.cr.guildManager.changeRank(self.avId, 2)
        self.destroy()

    def __handleDemote(self):
        base.cr.guildManager.changeRank(self.avId, 1)
        self.destroy()

    def __handleKick(self):
        base.cr.guildManager.removeMember(self.avId)
        messenger.send('kickedFromGuild-%s' % self.avId)
        self.destroy()
    
    def __handleCancel(self):
        self.destroy()


