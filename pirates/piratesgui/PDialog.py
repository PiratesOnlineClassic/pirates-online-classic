# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.PDialog
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from otp.otpgui import OTPDialog
from pandac.PandaModules import TextNode
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import BorderFrame, PiratesGuiGlobals


class PDialog(DirectDialog):
    
    loadedAssets = False
    checkButton = None
    cancelButton = None

    def __init__(self, parent=None, style=OTPDialog.NoButtons, giveMouse=True, **kw):
        self.style = style
        if not self.loadedAssets:
            buttons = loader.loadModel('models/gui/lookout_gui')
            self.checkButton = (buttons.find('**/lookout_submit'), buttons.find('**/lookout_submit_down'), buttons.find('**/lookout_submit_over'))
            self.cancelButton = (
             buttons.find('**/lookout_close_window'), buttons.find('**/lookout_close_window_down'), buttons.find('**/lookout_close_window_over'))
            for button in self.checkButton:
                button.setScale(0.2)
                button.flattenStrong()

            for button in self.cancelButton:
                button.setScale(0.2)
                button.flattenStrong()

            self.loadedAssets = True
            buttons.removeNode()
        if self.style == OTPDialog.TwoChoiceCustom:
            buttonImage = [
             self.checkButton, self.cancelButton]
            buttonValue = [DGG.DIALOG_OK, DGG.DIALOG_CANCEL]
            if 'buttonText' in kw:
                buttonText = kw['buttonText']
                del kw['buttonText']
            else:
                buttonText = [
                 PLocalizer.DialogOK, PLocalizer.DialogCancel]
        else:
            if self.style == OTPDialog.TwoChoice:
                buttonImage = [
                 self.checkButton, self.cancelButton]
                buttonText = [PLocalizer.DialogOK, PLocalizer.DialogCancel]
                buttonValue = [
                 DGG.DIALOG_OK, DGG.DIALOG_CANCEL]
            else:
                if self.style == OTPDialog.YesNo:
                    buttonImage = [
                     self.checkButton, self.cancelButton]
                    buttonText = [PLocalizer.DialogYes, PLocalizer.DialogNo]
                    buttonValue = [
                     DGG.DIALOG_OK, DGG.DIALOG_CANCEL]
                else:
                    if self.style == OTPDialog.Acknowledge:
                        buttonImage = [
                         self.checkButton]
                        buttonText = [PLocalizer.DialogOK]
                        buttonValue = [DGG.DIALOG_OK]
                    else:
                        if self.style == OTPDialog.CancelOnly:
                            buttonImage = [
                             self.cancelButton]
                            buttonText = [PLocalizer.DialogCancel]
                            buttonValue = [DGG.DIALOG_CANCEL]
                        else:
                            if self.style == OTPDialog.NoButtons:
                                buttonImage = []
                                buttonText = []
                                buttonValue = []
                            else:
                                self.notify.error('No such style as: ' + str(self.style))
        self.borderFrame = BorderFrame.BorderFrame(borderScale=0.5)
        optiondefs = (
         (
          'image', self.borderFrame, None), ('buttonImageList', buttonImage, DGG.INITOPT), ('buttonTextList', buttonText, DGG.INITOPT), ('buttonValueList', buttonValue, DGG.INITOPT), ('buttonPadSF', 2.2, DGG.INITOPT), ('title_text', '', None), ('title_text_font', DGG.getDefaultFont(), None), ('title_text_wordwrap', 12, None), ('title_text_scale', PiratesGuiGlobals.TextScaleTitleSmall, None), ('title_text_fg', PiratesGuiGlobals.TextFG1, None), ('title_text_shadow', PiratesGuiGlobals.TextShadow, None), ('title_text_align', TextNode.ACenter, None), ('text_font', DGG.getDefaultFont(), None), ('text_wordwrap', 12, None), ('text_scale', PiratesGuiGlobals.TextScaleLarge, None), ('text_fg', PiratesGuiGlobals.TextFG1, None), ('text_shadow', PiratesGuiGlobals.TextShadow, None), ('text_align', TextNode.ALeft, None), ('button_pad', (0, 0), None), ('button_relief', None, None), ('button_text_pos', (0, -0.08), None), ('button_text_fg', PiratesGuiGlobals.TextFG1, None), ('button_text_shadow', PiratesGuiGlobals.TextShadow, None), ('button_text_scale', PiratesGuiGlobals.TextScaleLarge, None), ('fadeScreen', 0.5, None), ('image_color', (1, 1, 1, 1), None), ('destroyedCallback', None, None))
        self.defineoptions(kw, optiondefs)
        DirectDialog.__init__(self, parent)

        def cleanupBorderFrame():
            self.borderFrame.destroy()

        self.postInitialiseFuncList.append(cleanupBorderFrame)
        self.createcomponent('title', (), None, DirectLabel, (self,), relief=None, text_pos=(0, 0.16))
        self.initialiseoptions(PDialog)
        self.accept('clientLogout', self.destroy)
        self.accept('shardSwitchComplete', self.destroy)
        return

    def destroy(self):
        if self['destroyedCallback']:
            self['destroyedCallback']()
        DirectDialog.destroy(self)


class PGlobalDialog(PDialog):
    
    notify = DirectNotifyGlobal.directNotify.newCategory('PGlobalDialog')

    def __init__(self, message='', doneEvent=None, style=OTPDialog.NoButtons, okButtonText=PLocalizer.DialogOK, cancelButtonText=PLocalizer.DialogCancel, **kw):
        if doneEvent == None and style != OTPDialog.NoButtons:
            self.notify.error('Boxes with buttons must specify a doneEvent.')
        self.__doneEvent = doneEvent
        if style == OTPDialog.NoButtons:
            buttonText = []
        else:
            if style == OTPDialog.Acknowledge:
                buttonText = [
                 okButtonText]
            else:
                if style == OTPDialog.CancelOnly:
                    buttonText = [
                     cancelButtonText]
                else:
                    buttonText = [
                     okButtonText, cancelButtonText]
        optiondefs = (
         (
          'dialogName', 'globalDialog', DGG.INITOPT), ('buttonTextList', buttonText, DGG.INITOPT), ('text', message, None), ('command', self.handleButton, None))
        self.defineoptions(kw, optiondefs)
        PDialog.__init__(self, style=style)
        self.initialiseoptions(PGlobalDialog)
        return

    def handleButton(self, value):
        if value == DGG.DIALOG_OK:
            self.doneStatus = 'ok'
            messenger.send(self.__doneEvent)
        else:
            if value == DGG.DIALOG_CANCEL:
                self.doneStatus = 'cancel'
                messenger.send(self.__doneEvent)
# okay decompiling .\pirates\piratesgui\PDialog.pyc
