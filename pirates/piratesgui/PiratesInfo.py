# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.PiratesInfo
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from otp.otpbase import OTPGlobals
from panda3d.core import *
from pirates.band import BandConstance
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import GuiPanel, PDialog, PiratesGuiGlobals
from pirates.piratesgui.RequestButton import RequestButton


class PiratesInfoButton(RequestButton):

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(PiratesInfoButton)


class PiratesInfo(GuiPanel.GuiPanel):

    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesInfo')

    def __init__(self, title, messageList):
        GuiPanel.GuiPanel.__init__(self, title, 0.8, 0.8)
        self.initialiseoptions(PiratesInfo)
        self.messageList = messageList
        self.currentMessage = 0
        text = ' '
        base.me = self
        self.message = DirectLabel(
            parent=self,
            relief=None,
            text=self.messageList[self.currentMessage],
            text_scale=PiratesGuiGlobals.TextScaleLarge,
            text_align=TextNode.ALeft,
            text_fg=PiratesGuiGlobals.TextFG2,
            text_shadow=PiratesGuiGlobals.TextShadow,
            text_wordwrap=17,
            pos=(0.0667, 0, 0.6),
            textMayChange=1)
        self.bOk = PiratesInfoButton(
            text=PLocalizer.GenericConfirmOK, command=self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.35, 0, 0.05)
        self.nextMessage()
        self.accept('clientLogout', self.destroy)
        return

    def nextMessage(self):
        self.message['text'] = self.messageList[self.currentMessage]
        self.currentMessage += 1
        if self.currentMessage == len(self.messageList):
            self.bOk['text'] = PLocalizer.GenericConfirmDone
        else:
            self.bOk['text'] = PLocalizer.GenericConfirmNext

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.ignore('Esc')
        GuiPanel.GuiPanel.destroy(self)

    def __handleOk(self):
        if self.currentMessage == len(self.messageList):
            self.destroy()
        else:
            self.nextMessage()

    def __handleCancelFromAbove(self):
        self.destroy()


# okay decompiling .\pirates\piratesgui\PiratesInfo.pyc
