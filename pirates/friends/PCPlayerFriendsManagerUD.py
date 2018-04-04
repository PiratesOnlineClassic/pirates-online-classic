
from otp.friends.PlayerFriendsManagerUD import PlayerFriendsManagerUD
from direct.directnotify import DirectNotifyGlobal

class PCPlayerFriendsManagerUD(PlayerFriendsManagerUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PCPlayerFriendsManagerUD')

    def __init__(self, air):
        PlayerFriendsManagerUD.__init__(self, air)


    # setShipState(uint32, uint8, uint32)

    def setShipState(self, shipState, todo_uint8_1, todo_uint32_2):
        self.sendUpdate('setShipState', [shipState, todo_uint8_1, todo_uint32_2])

    # setBandId(uint32, uint32, uint32)

    def setBandId(self, bandId, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('setBandId', [bandId, todo_uint32_1, todo_uint32_2])


