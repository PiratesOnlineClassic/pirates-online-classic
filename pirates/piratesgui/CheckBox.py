# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.CheckBox
from direct.gui.DirectCheckBox import DirectCheckBox
from direct.gui.DirectGui import *
from direct.task.Task import Task
from otp.otpbase import OTPGlobals, OTPLocalizer
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals


class CheckBox(DirectCheckBox):
    __module__ = __name__

    def __init__(self, text, command):
        self.charGui = loader.loadModelOnce('models/gui/toplevel_gui')
        uncheckedImage = (self.charGui.find('**/main_gui_checkbox_off'), self.charGui.find('**/main_gui_checkbox_halfcheck'), self.charGui.find('**/main_gui_checkbox_off_over'), self.charGui.find('**/main_gui_checkbox_off_disable'))
        checkedImage = (
         self.charGui.find('**/main_gui_checkbox_on'), self.charGui.find('**/main_gui_checkbox_halfcheck'), self.charGui.find('**/main_gui_checkbox_on_over'), self.charGui.find('**/main_gui_checkbox_on_disable'))
        DirectCheckBox.__init__(self, relief=None, pos=(0, 0, 0), text=text, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.08,
                                                                                                                                                                                                                                              0.025), image=uncheckedImage, image_scale=(0.07,
                                                                                                                                                                                                                                                                                         0.07,
                                                                                                                                                                                                                                                                                         0.07), image_pos=(-0.01, 0.0, 0.035), command=command, uncheckedImage=uncheckedImage, checkedImage=checkedImage)
        self.initialiseoptions(CheckBox)
        self.charGui.removeNode()
        return
# okay decompiling .\pirates\piratesgui\CheckBox.pyc
