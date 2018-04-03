# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.login.LeaveToPayDialog
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLauncherGlobals
from otp.otpbase import OTPLocalizer
from direct.gui.DirectGui import *
from pandac.PandaModules import *
import os

class LeaveToPayDialog:
    __module__ = __name__

    def __init__(self, paidUser, destructorHook=None, doneFunc=None):
        self.destructorHook = destructorHook
        self.dialog = None
        self.okHandler = self.__handleLeaveToPayOK
        self.cancelHandler = self.__handleLeaveToPayCancel
        self.paidUser = paidUser
        self.doneFunc = doneFunc
        return

    def setOK(self, handler):
        self.okHandler = handler

    def setCancel(self, handler):
        self.cancelHandler = handler

    def show(self):
        if self.paidUser:
            if base.cr.productName in ['DisneyOnline-AP', 'DisneyOnline-UK', 'ES', 'JP', 'T-Online', 'Wanadoo']:
                directFrameText = OTPLocalizer.LeaveToEnableChatUK
                directButtonYesText = OTPLocalizer.LeaveToEnableChatUKYes
                directButtonNoText = OTPLocalizer.LeaveToEnableChatUKNo
            else:
                directFrameText = OTPLocalizer.LeaveToSetParentPassword
                directButtonYesText = OTPLocalizer.LeaveToSetParentPasswordYes
                directButtonNoText = OTPLocalizer.LeaveToSetParentPasswordNo
        else:
            directFrameText = OTPLocalizer.LeaveToPay
            directButtonYesText = OTPLocalizer.LeaveToPayYes
            directButtonNoText = OTPLocalizer.LeaveToPayNo
        if self.dialog == None:
            buttons = loader.loadModelOnce('phase_3/models/gui/dialog_box_buttons_gui')
            okButtonImage = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            cancelButtonImage = (
             buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr'))
            self.dialog = DirectFrame(parent=aspect2dp, pos=(0.0, 0.0, 0.0), relief=None, image=DGG.getDefaultDialogGeom(), image_color=OTPGlobals.GlobalDialogColor, image_scale=(0.9,
                                                                                                                                                                                   1.0,
                                                                                                                                                                                   0.5), text=directFrameText, text_align=TextNode.ALeft, text_wordwrap=14, text_scale=0.06, text_pos=(-0.4, 0.15), textMayChange=0)
            DirectButton(self.dialog, image=okButtonImage, relief=None, text=directButtonYesText, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(-0.23, 0.0, -0.1), command=self.okHandler)
            DirectButton(self.dialog, image=cancelButtonImage, relief=None, text=directButtonNoText, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(0.23, 0.0, -0.1), command=self.cancelHandler)
            buttons.removeNode()
        self.dialog.show()
        return

    def hide(self):
        self.dialog.hide()

    def destroy(self):
        if self.destructorHook:
            self.destructorHook()
        if self.dialog:
            self.dialog.hide()
            self.dialog.destroy()
        self.destructorHook
        self.dialog = None
        self.okHandler = None
        self.cancelHandler = None
        return

    def removed(self):
        if hasattr(self, 'dialog') and self.dialog:
            return self.dialog.removed()
        else:
            return 1

    def __handleLeaveToPayOK(self):
        self.destroy()
        errorCode = None
        if self.paidUser:
            if base.cr.productName in ['DisneyOnline-AP', 'DisneyOnline-UK', 'ES', 'JP', 'T-Online', 'Wanadoo']:
                errorCode = OTPLauncherGlobals.ExitEnableChat
            else:
                errorCode = OTPLauncherGlobals.ExitSetParentPassword
        else:
            errorCode = OTPLauncherGlobals.ExitPurchase
        base.setExitErrorCode(errorCode)
        base.cr.loginFSM.request('shutdown', [errorCode])
        return

    def __handleLeaveToPayCancel(self):
        if self.doneFunc:
            self.doneFunc()
        self.destroy()
# okay decompiling .\otp\login\LeaveToPayDialog.pyc
