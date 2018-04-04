
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class MagicWordManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('MagicWordManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # setMagicWord(string, uint32, uint32, string) airecv clsend

    def setMagicWord(self, magicWord, todo_uint32_1, todo_uint32_2, todo_string_3):
        pass

    # setMagicWordResponse(string) airecv

    def setMagicWordResponse(self, magicWordResponse):
        pass

    # setWho(uint32array) airecv clsend

    def setWho(self, who):
        pass


