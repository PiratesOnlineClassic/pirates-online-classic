from direct.directnotify import DirectNotifyGlobal
from otp.friends.AvatarFriendsManagerUD import AvatarFriendsManagerUD

class PCAvatarFriendsManagerUD(AvatarFriendsManagerUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PCAvatarFriendsManagerUD')

    def __init__(self, air):
        AvatarFriendsManagerUD.__init__(self, air)

    def d_setShipState(self, avId, onShip, shipId):
        for friendId in self.getFriendIds(avId):
            if self.isOnline(friendId):
                self.sendUpdateToAvatarId(friendId, 'setShipState', [avId, onShip, shipId])

    def d_setBandId(self, avId, bandMgrId, bandId):
        for friendId in self.getFriendIds(avId):
            if self.isOnline(friendId):
                self.sendUpdateToAvatarId(friendId, 'setBandId', [avId, bandMgrId, bandId])
