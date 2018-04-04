
from otp.friends.AvatarFriendsManagerUD import AvatarFriendsManagerUD
from direct.directnotify import DirectNotifyGlobal

class PCAvatarFriendsManagerUD(AvatarFriendsManagerUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PCAvatarFriendsManagerUD')

    def __init__(self, air):
        AvatarFriendsManagerUD.__init__(self, air)


    # setShipState(uint32, uint8, uint32)

    def setShipState(self, shipState, todo_uint8_1, todo_uint32_2):
        self.sendUpdate('setShipState', [shipState, todo_uint8_1, todo_uint32_2])

    # setBandId(uint32, uint32, uint32)

    def setBandId(self, bandId, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('setBandId', [bandId, todo_uint32_1, todo_uint32_2])

    # requestDinghyFriendsList(uint32, uint32, uint32)

    def requestDinghyFriendsList(self, requestDinghyFriendsList, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('requestDinghyFriendsList', [requestDinghyFriendsList, todo_uint32_1, todo_uint32_2])


