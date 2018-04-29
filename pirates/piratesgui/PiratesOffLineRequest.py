# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.PiratesOffLineRequest
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectCheckBox import DirectCheckBox
from direct.gui.DirectGui import *
from otp.otpbase import OTPGlobals
from panda3d.core import *
from pirates.band import BandConstance
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import GuiPanel, PDialog, PiratesGuiGlobals
from pirates.piratesgui.CheckBox import CheckBox
from pirates.piratesgui.RequestButton import RequestButton

LAST_BUTTON_SELECTION = 1

class PiratesOffLineConfirmButton(RequestButton):
    

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(PiratesOffLineConfirmButton)


class PiratesOffLineEMailButton(RequestButton):
    

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(PiratesOffLineEMailButton)


class PiratesOffLineCheckBox(CheckBox):
    

    def __init__(self, text, command):
        CheckBox.__init__(self, text, command)
        self.initialiseoptions(PiratesOffLineCheckBox)


class PiratesOffLineRequest(GuiPanel.GuiPanel):
    
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesOffLineInvite')

    def __init__(self, title, message, tokenString=None, preExistPerm=0):
        global LAST_BUTTON_SELECTION
        if tokenString:
            GuiPanel.GuiPanel.__init__(self, title, 0.66, 0.79, 0, '', pos=(0.65, 0, -0.83))
        else:
            GuiPanel.GuiPanel.__init__(self, title, 0.5, 0.5)
        self.initialiseoptions(PiratesOffLineRequest)
        self.sliderOutputValue = '0'
        self.charGui = loader.loadModelOnce('models/gui/char_gui')
        self.tokenString = tokenString
        self.preExistPerm = preExistPerm
        self.currentCodeOption = 1
        text = message
        self.main = None
        if not tokenString:
            self.message = DirectLabel(parent=self, relief=None, text=message, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.25,
                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                             0.35), textMayChange=1)
        else:
            self.message = DirectLabel(parent=self, relief=None, text=message, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=16, pos=(0.33,
                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                             0.68), textMayChange=1)
        if tokenString != None:
            self.tokenMessage = DirectLabel(parent=self, relief=None, text=tokenString, text_scale=PiratesGuiGlobals.TextScaleTitleMed, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.33,
                                                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                                                         0.55), textMayChange=1)
        self.bOk = PiratesOffLineConfirmButton(text=PLocalizer.GenericConfirmOK, command=self.__handleOk)
        self.bOk.reparentTo(self)
        if not tokenString:
            self.bOk.setPos(0.2, 0, 0.05)
        else:
            self.bOk.setPos(0.3, 0, 0.05)
        if tokenString:
            self.cBox1 = self.makeCheckbox((0.215, 0, 0.46), PLocalizer.GuildInviteSingleButton, self.__handleSet, 1, [1])
            self.cBox1.reparentTo(self)
            self.cBox2 = self.makeCheckbox((0.215, 0, 0.365), PLocalizer.GuildInviteLimitedButton, self.__handleSet, 0, [2])
            self.cBox2.reparentTo(self)
            self.cBox3 = self.makeCheckbox((0.215, 0, 0.175), PLocalizer.GuildInviteUnlimitedButton, self.__handleSet, 0, [3])
            self.cBox3.reparentTo(self)
            if self.preExistPerm:
                self.cBox3['state'] = DGG.DISABLED
            if self.preExistPerm and LAST_BUTTON_SELECTION == 3:
                pass
            else:
                if LAST_BUTTON_SELECTION == 2:
                    self.cBox1['indicatorValue'] = 0
                    self.cBox2['indicatorValue'] = 1
                    self.currentCodeOption = 2
            self.rotateSlider = DirectSlider(parent=self, relief=None, range=(1, 100), value=10, pageSize=2, scale=0.25, text=self.sliderOutputValue, text_scale=0.18, text_pos=(0,
                                                                                                                                                                                 0.075), text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG1, textMayChange=1, frameColor=(0.5,
                                                                                                                                                                                                                                                                                      0.5,
                                                                                                                                                                                                                                                                                      0.5,
                                                                                                                                                                                                                                                                                      0.3), image=self.charGui.find('**/chargui_slider_small'), thumb_relief=None, image_scale=(2.15,
                                                                                                                                                                                                                                                                                                                                                                                2.15,
                                                                                                                                                                                                                                                                                                                                                                                1.5), thumb_image=(self.charGui.find('**/chargui_slider_node'), self.charGui.find('**/chargui_slider_node_down'), self.charGui.find('**/chargui_slider_node_over')), command=self.__showSliderValue)
            self.rotateSlider.reparentTo(self)
            self.rotateSlider.setPos(0.33, 0, 0.27)
        self.accept('clientLogout', self.destroy)
        return

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.ignore('Esc')
        GuiPanel.GuiPanel.destroy(self)

    def __handleOk(self):
        global LAST_BUTTON_SELECTION
        LAST_BUTTON_SELECTION = self.currentCodeOption
        if self.currentCodeOption == 1:
            npTokenCount = base.localAvatar.guiMgr.guildPage.getNonPermTokenCount()
            npTokenCount += 1
            base.localAvatar.guiMgr.guildPage.receiveNonPermTokenCount(npTokenCount)
            self.destroy()
            return
        else:
            if self.currentCodeOption == 2:
                base.cr.guildManager.updateTokenRValue(self.tokenString, self.sliderOutputValue)
                npTokenCount = base.localAvatar.guiMgr.guildPage.getNonPermTokenCount()
                npTokenCount += 1
                base.localAvatar.guiMgr.guildPage.receiveNonPermTokenCount(npTokenCount)
            else:
                base.cr.guildManager.updateTokenRValue(self.tokenString, -1)
            self.destroy()
            return

    def __handleNo(self):
        self.destroy()

    def __handleCancelFromAbove(self):
        self.destroy()

    def __handleEMail(self):
        self.destroy()

    def __handleSet(self, status, extraArgs):
        if status == 1:
            if extraArgs == 1:
                self.cBox2['indicatorValue'] = 0
                self.cBox3['indicatorValue'] = 0
                self.currentCodeOption = 1
            if extraArgs == 2:
                self.cBox1['indicatorValue'] = 0
                self.cBox3['indicatorValue'] = 0
                self.currentCodeOption = 2
            if extraArgs == 3:
                self.cBox1['indicatorValue'] = 0
                self.cBox2['indicatorValue'] = 0
                self.currentCodeOption = 3
        if status == 0:
            if extraArgs == 1:
                self.cBox1['indicatorValue'] = 1
                self.cBox2['indicatorValue'] = 0
                self.cBox3['indicatorValue'] = 0
                self.currentCodeOption = 1
            if extraArgs == 2:
                self.cBox1['indicatorValue'] = 0
                self.cBox2['indicatorValue'] = 1
                self.cBox3['indicatorValue'] = 0
                self.currentCodeOption = 2
            if extraArgs == 3:
                self.cBox1['indicatorValue'] = 0
                self.cBox2['indicatorValue'] = 0
                self.cBox3['indicatorValue'] = 1
                self.currentCodeOption = 3

    def makeCheckbox(self, pos, text, command, initialState, extraArgs):
        charGui = loader.loadModelOnce('models/gui/toplevel_gui')
        buttonImage = (charGui.find('**/generic_button'), charGui.find('**/generic_button_down'), charGui.find('**/generic_button_over'), charGui.find('**/generic_button_disabled'))
        geomCheck = [
         charGui.find('**/generic_check'), charGui.find('**/generic_check'), charGui.find('**/generic_check'), None]
        c = DirectCheckButton(parent=self, relief=None, scale=0.064, boxBorder=0.08, boxRelief=None, boxImage=geomCheck, boxImageScale=6.0, boxImageColor=VBase4(0, 1, 0, 1), pos=pos, text=text, text_fg=(1,
                                                                                                                                                                                                           1,
                                                                                                                                                                                                           1,
                                                                                                                                                                                                           1), text_scale=0.6, text_pos=(-0.5,
                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                         -2.8), indicator_pos=(-1,
                                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                                               0.15), command=command, text_align=TextNode.ALeft, indicatorValue=initialState, extraArgs=extraArgs, text0_fg=PiratesGuiGlobals.TextFG2, text1_fg=PiratesGuiGlobals.TextFG3, text2_fg=PiratesGuiGlobals.TextFG1, text3_fg=PiratesGuiGlobals.TextFG9, text_shadow=PiratesGuiGlobals.TextShadow, image=buttonImage, image_pos=(1.8,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            0.15), image_scale=(7.5,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                3.5))
        c.setIndicatorValue()
        return c

    def __showSliderValue(self):
        self.sliderOutputValue = str(int(self.rotateSlider['value']))
        self.rotateSlider['text'] = str(int(self.rotateSlider['value']))
# okay decompiling .\pirates\piratesgui\PiratesOffLineRequest.pyc
