# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.CrewMatchInviter
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from otp.otpbase import OTPGlobals
from panda3d.core import *
from pirates.band import BandConstance
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import GuiPanel, PDialog, PiratesGuiGlobals
from pirates.piratesgui.RequestButton import RequestButton


class CrewMatchInviterButton(RequestButton):

    def __init__(self, text, command):
        if text == PLocalizer.CrewMatchAdvancedOptionsButton or text == PLocalizer.CrewMatchSimpleOptionsButton:
            RequestButton.__init__(self, text, command, 2.1)
        else:
            RequestButton.__init__(self, text, command)
        self.initialiseoptions(CrewMatchInviterButton)


class CrewMatchInviter(GuiPanel.GuiPanel):

    notify = DirectNotifyGlobal.directNotify.newCategory('CrewMatchInviter')

    def __init__(self, currentRepLevel, advancedOptions=False):
        if not advancedOptions:
            x = 0.5
            y = 0.55
        else:
            x = 0.5
            y = 0.65
        GuiPanel.GuiPanel.__init__(
            self, PLocalizer.CrewMatchCrewLookout, x, y, showClose=False)
        self.initialiseoptions(CrewMatchInviter)
        self.setPos(0.15, 0, 0.25)
        self.currentRepLevel = currentRepLevel
        self.charGui = loader.loadModelOnce('models/gui/char_gui')
        self.sliderOutputValue = '0'
        self.sliderOutputValueNoto = '0'
        self.sliderOutputValueSail = '0'
        self.sliderOutputValueCannon = '0'
        text = PLocalizer.CrewMatchInviterText
        self.advancedOptions = advancedOptions
        if not advancedOptions:
            self.message = DirectLabel(
                parent=self,
                relief=None,
                text=text,
                text_scale=PiratesGuiGlobals.TextScaleLarge,
                text_align=TextNode.ACenter,
                text_fg=PiratesGuiGlobals.TextFG2,
                text_shadow=PiratesGuiGlobals.TextShadow,
                text_wordwrap=11,
                pos=(0.25, 0, 0.4),
                textMayChange=1)
            self.rangeSlider = DirectSlider(
                parent=self,
                relief=None,
                range=(0, 40),
                value=30,
                pageSize=2,
                scale=(0.19, 0.24, 0.24),
                text=self.sliderOutputValue,
                text_scale=(0.21, 0.18, 0.18),
                text_pos=(0, 0.075),
                text_align=TextNode.ACenter,
                text_fg=PiratesGuiGlobals.TextFG1,
                textMayChange=1,
                frameColor=(0.5, 0.5, 0.5, 0.3),
                image=self.charGui.find('**/chargui_slider_small'),
                thumb_relief=None,
                image_scale=(2.15, 2.15, 1.5),
                thumb_image=(self.charGui.find('**/chargui_slider_node'),
                             self.charGui.find('**/chargui_slider_node_down'),
                             self.charGui.find('**/chargui_slider_node_over')),
                command=self.__showSliderValue)
            self.rangeSlider.reparentTo(self)
            self.rangeSlider.setPos(0.25, 0, 0.24)
            self.bOk = CrewMatchInviterButton(
                text=PLocalizer.CrewInviterOK, command=self.__handleOk)
            self.bOk.reparentTo(self)
            self.bOk.setPos(0.1, 0, 0.1)
            self.bNo = CrewMatchInviterButton(
                text=PLocalizer.CrewMatchCancelButton, command=self.__handleNo)
            self.bNo.reparentTo(self)
            self.bNo.setPos(0.3, 0, 0.1)
            self.bAdvanced = CrewMatchInviterButton(
                text=PLocalizer.CrewMatchAdvancedOptionsButton,
                command=self.__handleAdvanced)
            self.bAdvanced.reparentTo(self)
            self.bAdvanced.setPos(0.2, 0, 0.025)
        else:
            self.dividerLine = DirectButton(
                parent=self,
                relief=None,
                image=self.charGui.find('**/chargui_slider_large_over'),
                scale=0.27,
                image_scale=(1, 1, 0.4))
            self.dividerLine2 = DirectButton(
                parent=self,
                relief=None,
                image=self.charGui.find('**/chargui_slider_large_over'),
                scale=0.27,
                image_scale=(1, 1, 0.4))
            self.dividerLine3 = DirectButton(
                parent=self,
                relief=None,
                image=self.charGui.find('**/chargui_slider_large_over'),
                scale=0.27,
                image_scale=(1, 1, 0.4))
            self.messageNoto = DirectLabel(
                parent=self,
                relief=None,
                text=PLocalizer.CrewMatchAdvancedNotorietyRange,
                text_scale=PiratesGuiGlobals.TextScaleLarge,
                text_align=TextNode.ACenter,
                text_fg=PiratesGuiGlobals.TextFG2,
                text_shadow=PiratesGuiGlobals.TextShadow,
                text_wordwrap=11,
                pos=(0.25, 0, 0.54),
                textMayChange=1)
            self.messageSail = DirectLabel(
                parent=self,
                relief=None,
                text=PLocalizer.CrewMatchAdvancedMinSailSkillLevel,
                text_scale=PiratesGuiGlobals.TextScaleLarge,
                text_align=TextNode.ACenter,
                text_fg=PiratesGuiGlobals.TextFG2,
                text_shadow=PiratesGuiGlobals.TextShadow,
                text_wordwrap=11,
                pos=(0.25, 0, 0.4),
                textMayChange=1)
            self.messageCannon = DirectLabel(
                parent=self,
                relief=None,
                text=PLocalizer.CrewMatchAdvancedMinCannonSkillLevel,
                text_scale=PiratesGuiGlobals.TextScaleLarge,
                text_align=TextNode.ACenter,
                text_fg=PiratesGuiGlobals.TextFG2,
                text_shadow=PiratesGuiGlobals.TextShadow,
                text_wordwrap=11,
                pos=(0.25, 0, 0.27),
                textMayChange=1)
            self.rangeSliderNoto = DirectSlider(
                parent=self,
                relief=None,
                range=(0, 40),
                value=30,
                pageSize=2,
                scale=(0.19, 0.24, 0.24),
                text=self.sliderOutputValue,
                text_scale=(0.21, 0.18, 0.18),
                text_pos=(0, 0.075),
                text_align=TextNode.ACenter,
                text_fg=PiratesGuiGlobals.TextFG1,
                textMayChange=1,
                frameColor=(0.5, 0.5, 0.5, 0.3),
                image=self.charGui.find('**/chargui_slider_small'),
                thumb_relief=None,
                image_scale=(2.15, 2.15, 1.5),
                thumb_image=(self.charGui.find('**/chargui_slider_node'),
                             self.charGui.find('**/chargui_slider_node_down'),
                             self.charGui.find('**/chargui_slider_node_over')),
                command=self.__showSliderValueNoto)
            self.rangeSliderSail = DirectSlider(
                parent=self,
                relief=None,
                range=(1, 24),
                value=1,
                pageSize=2,
                scale=(0.19, 0.24, 0.24),
                text=self.sliderOutputValue,
                text_scale=(0.21, 0.18, 0.18),
                text_pos=(0, 0.075),
                text_align=TextNode.ACenter,
                text_fg=PiratesGuiGlobals.TextFG1,
                textMayChange=1,
                frameColor=(0.5, 0.5, 0.5, 0.3),
                image=self.charGui.find('**/chargui_slider_small'),
                thumb_relief=None,
                image_scale=(2.15, 2.15, 1.5),
                thumb_image=(self.charGui.find('**/chargui_slider_node'),
                             self.charGui.find('**/chargui_slider_node_down'),
                             self.charGui.find('**/chargui_slider_node_over')),
                command=self.__showSliderValueSail)
            self.rangeSliderCannon = DirectSlider(
                parent=self,
                relief=None,
                range=(1, 24),
                value=1,
                pageSize=2,
                scale=(0.19, 0.24, 0.24),
                text=self.sliderOutputValue,
                text_scale=(0.21, 0.18, 0.18),
                text_pos=(0, 0.075),
                text_align=TextNode.ACenter,
                text_fg=PiratesGuiGlobals.TextFG1,
                textMayChange=1,
                frameColor=(0.5, 0.5, 0.5, 0.3),
                image=self.charGui.find('**/chargui_slider_small'),
                thumb_relief=None,
                image_scale=(2.15, 2.15, 1.5),
                thumb_image=(self.charGui.find('**/chargui_slider_node'),
                             self.charGui.find('**/chargui_slider_node_down'),
                             self.charGui.find('**/chargui_slider_node_over')),
                command=self.__showSliderValueCannon)
            self.dividerLine.reparentTo(self)
            self.dividerLine.setPos(0.25, 0, 0.45)
            self.dividerLine['state'] = DGG.DISABLED
            self.dividerLine2.reparentTo(self)
            self.dividerLine2.setPos(0.25, 0, 0.31)
            self.dividerLine2['state'] = DGG.DISABLED
            self.dividerLine3.reparentTo(self)
            self.dividerLine3.setPos(0.25, 0.0, 0.18)
            self.dividerLine3['state'] = DGG.DISABLED
            self.rangeSliderNoto.reparentTo(self)
            self.rangeSliderNoto.setPos(0.25, 0, 0.48)
            self.rangeSliderSail.reparentTo(self)
            self.rangeSliderSail.setPos(0.25, 0, 0.34)
            self.rangeSliderCannon.reparentTo(self)
            self.rangeSliderCannon.setPos(0.25, 0, 0.21)
            self.bOk = CrewMatchInviterButton(
                text=PLocalizer.CrewInviterOK, command=self.__handleOk)
            self.bOk.reparentTo(self)
            self.bOk.setPos(0.1, 0, 0.1)
            self.bNo = CrewMatchInviterButton(
                text=PLocalizer.CrewMatchCancelButton, command=self.__handleNo)
            self.bNo.reparentTo(self)
            self.bNo.setPos(0.3, 0, 0.1)
            self.bAdvanced = CrewMatchInviterButton(
                text=PLocalizer.CrewMatchSimpleOptionsButton,
                command=self.__handleAdvanced)
            self.bAdvanced.reparentTo(self)
            self.bAdvanced.setPos(0.2, 0, 0.025)
        self.accept('clientLogout', self.destroy)
        return

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.ignore('Esc')
        GuiPanel.GuiPanel.destroy(self)

    def __handleOk(self):
        if not self.advancedOptions:
            base.localAvatar.guiMgr.crewPage.b_activateCrewLookout(
                int(self.sliderOutputValue))
        else:
            base.localAvatar.guiMgr.crewPage.b_activateCrewLookout(
                int(self.sliderOutputValueNoto),
                int(self.sliderOutputValueSail),
                int(self.sliderOutputValueCannon))
        self.destroy()

    def __handleNo(self):
        if base.localAvatar.guiMgr.crewPage.startACrewState:
            base.localAvatar.guiMgr.crewPage.toggleStartACrew()
        else:
            if base.localAvatar.guiMgr.crewPage.addCrewLookout:
                base.localAvatar.guiMgr.crewPage.addCrewLookout[
                    'state'] = DGG.NORMAL
        self.destroy()

    def __handleCancelFromAbove(self):
        self.destroy()

    def __showSliderValue(self):
        self.sliderOutputValue = str(int(self.rangeSlider['value']))
        self.rangeSlider['text'] = PLocalizer.CrewMatchRangeIndicator % str(
            int(self.rangeSlider['value']))

    def __showSliderValueNoto(self):
        self.sliderOutputValueNoto = str(int(self.rangeSliderNoto['value']))
        self.rangeSliderNoto['text'] = PLocalizer.CrewMatchRangeIndicator % str(
            int(self.rangeSliderNoto['value']))

    def __showSliderValueSail(self):
        self.sliderOutputValueSail = str(int(self.rangeSliderSail['value']))
        self.rangeSliderSail['text'] = PLocalizer.CrewMatchLevelIndicator % str(
            int(self.rangeSliderSail['value']))

    def __showSliderValueCannon(self):
        self.sliderOutputValueCannon = str(int(self.rangeSliderCannon['value']))
        self.rangeSliderCannon[
            'text'] = PLocalizer.CrewMatchLevelIndicator % str(
                int(self.rangeSliderCannon['value']))

    def __handleAdvanced(self):
        if self.advancedOptions:
            CrewMatchInviter(self.currentRepLevel, False)
        else:
            CrewMatchInviter(self.currentRepLevel, True)
        self.destroy()


# okay decompiling .\pirates\piratesgui\CrewMatchInviter.pyc
