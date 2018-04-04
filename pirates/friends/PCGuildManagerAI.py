
from otp.friends.GuildManagerAI import GuildManagerAI
from direct.directnotify import DirectNotifyGlobal

class PCGuildManagerAI(GuildManagerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PCGuildManagerAI')

    def __init__(self, air):
        GuildManagerAI.__init__(self, air)


    # sendSCQuest(uint16, uint8, uint16) clsend airecv

    def sendSCQuest(self, sendSCQuest, todo_uint8_1, todo_uint16_2):
        pass

    # recvSCQuest(uint32, uint16, uint8, uint16)

    def recvSCQuest(self, recvSCQuest, todo_uint16_1, todo_uint8_2, todo_uint16_3):
        self.sendUpdate('recvSCQuest', [recvSCQuest, todo_uint16_1, todo_uint8_2, todo_uint16_3])


