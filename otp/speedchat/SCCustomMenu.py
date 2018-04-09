# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.speedchat.SCCustomMenu
from otp.otpbase.OTPLocalizer import CustomSCStrings
from SCCustomTerminal import SCCustomTerminal
from SCMenu import SCMenu


class SCCustomMenu(SCMenu):
    

    def __init__(self):
        SCMenu.__init__(self)
        self.accept('customMessagesChanged', self.__customMessagesChanged)
        self.__customMessagesChanged()

    def destroy(self):
        SCMenu.destroy(self)

    def __customMessagesChanged(self):
        self.clearMenu()
        try:
            lt = base.localAvatar
        except:
            return
        else:
            for msgIndex in lt.customMessages:
                if CustomSCStrings.has_key(msgIndex):
                    self.append(SCCustomTerminal(msgIndex))
# okay decompiling .\otp\speedchat\SCCustomMenu.pyc
