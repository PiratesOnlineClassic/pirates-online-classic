from otp.chat.ChatInputWhiteList import ChatInputWhiteList
from pirates.chat.PWhiteList import PWhiteList

class PChatInputWhiteList(ChatInputWhiteList):
    

    def __init__(self, parent=None, **kw):
        ChatInputWhiteList.__init__(self, parent, **kw)
        self.initialiseoptions(PChatInputWhiteList)
        self.whiteList = PWhiteList()
