from direct.directnotify import DirectNotifyGlobal
from otp.friends.PlayerFriendsManagerUD import PlayerFriendsManagerUD

class PCPlayerFriendsManagerUD(PlayerFriendsManagerUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PCPlayerFriendsManagerUD')

    def __init__(self, air):
        PlayerFriendsManagerUD.__init__(self, air)

    def d_setShipState(self, accountId, onShip, shipId):
        for friendId in self.getFriendIds(accountId):
            if self.isOnline(friendId):
                self.sendUpdateToAccountId(friendId, 'setShipState', [accountId, onShip, shipId])

    def d_setBandId(self, accountId, bandMgrId, bandId):
        for friendId in self.getFriendIds(accountId):
            if self.isOnline(friendId):
                self.sendUpdateToAccountId(friendId, 'setBandId', [accountId, bandMgrId, bandId])
