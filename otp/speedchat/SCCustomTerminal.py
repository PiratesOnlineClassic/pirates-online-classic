# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.speedchat.SCCustomTerminal
from otp.otpbase.OTPLocalizer import CustomSCStrings
from SCTerminal import SCTerminal

SCCustomMsgEvent = 'SCCustomMsg'

def decodeSCCustomMsg(textId):
    return CustomSCStrings.get(textId, None)


class SCCustomTerminal(SCTerminal):
    __module__ = __name__

    def __init__(self, textId):
        SCTerminal.__init__(self)
        self.textId = textId
        self.text = CustomSCStrings[self.textId]

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(SCCustomMsgEvent), [
         self.textId])
# okay decompiling .\otp\speedchat\SCCustomTerminal.pyc
