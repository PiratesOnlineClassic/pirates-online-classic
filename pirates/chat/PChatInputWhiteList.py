# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.chat.PChatInputWhiteList
from otp.chat.ChatInputWhiteList import ChatInputWhiteList
from pirates.chat.PWhiteList import PWhiteList


class PChatInputWhiteList(ChatInputWhiteList):
    __module__ = __name__

    def __init__(self, parent=None, **kw):
        ChatInputWhiteList.__init__(self, parent, **kw)
        self.initialiseoptions(PChatInputWhiteList)
        self.whiteList = PWhiteList()
# okay decompiling .\pirates\chat\PChatInputWhiteList.pyc
