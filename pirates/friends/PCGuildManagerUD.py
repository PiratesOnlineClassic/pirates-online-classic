
from otp.friends.GuildManagerUD import GuildManagerUD
from direct.directnotify import DirectNotifyGlobal

class PCGuildManagerUD(GuildManagerUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PCGuildManagerUD')

    def __init__(self, air):
        GuildManagerUD.__init__(self, air)



    # recvSCQuest(uint32, uint16, uint8, uint16)

    def recvSCQuest(self, recvSCQuest, todo_uint16_1, todo_uint8_2, todo_uint16_3):
        self.sendUpdate('recvSCQuest', [recvSCQuest, todo_uint16_1, todo_uint8_2, todo_uint16_3])


