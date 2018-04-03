# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.speedchat.SCEmoteMenu
from SCMenu import SCMenu
from SCEmoteTerminal import SCEmoteTerminal

class SCEmoteMenu(SCMenu):
    __module__ = __name__

    def __init__(self):
        SCMenu.__init__(self)
        self.accept('emotesChanged', self.__emoteAccessChanged)
        self.__emoteAccessChanged()

    def destroy(self):
        SCMenu.destroy(self)

    def __emoteAccessChanged(self):
        self.clearMenu()
        try:
            lt = base.localAvatar
        except:
            return
        else:
            for i in range(len(lt.emoteAccess)):
                if lt.emoteAccess[i]:
                    self.append(SCEmoteTerminal(i))
# okay decompiling .\otp\speedchat\SCEmoteMenu.pyc
