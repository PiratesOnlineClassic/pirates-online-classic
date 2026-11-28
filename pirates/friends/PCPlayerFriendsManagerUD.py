from direct.directnotify import DirectNotifyGlobal
from otp.friends.PlayerFriendsManagerUD import PlayerFriendsManagerUD

class PCPlayerFriendsManagerUD(PlayerFriendsManagerUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PCPlayerFriendsManagerUD')

    def __init__(self, air):
        PlayerFriendsManagerUD.__init__(self, air)

    def avatarBandIdChanged(self, avId, bandMgrId, bandId):
        # The avatar friends manager tells us whenever an avatar changes crew.
        accountId = self.avatar2account.get(avId)
        if accountId is None:
            return

        self.d_setBandId(accountId, bandMgrId, bandId)

    def d_updatePlayerFriend(self, accountId, friendId):
        PlayerFriendsManagerUD.d_updatePlayerFriend(self, accountId, friendId)

        # The client builds a new friend info for every update, which
        # forgets the crew the friend is in:
        friendAvId = self.account2avatar.get(friendId)
        if not friendAvId or not self.isOnline(accountId):
            return

        bandMgrId, bandId = self.air.avatarFriendsManager.getBandId(friendAvId)
        if bandId:
            self.sendUpdateToAccountId(accountId, 'setBandId', [friendId, bandMgrId, bandId])

    def d_setShipState(self, accountId, onShip, shipId):
        for friendId in self.getFriendIds(accountId):
            if self.isOnline(friendId):
                self.sendUpdateToAccountId(friendId, 'setShipState', [accountId, onShip, shipId])

    def d_setBandId(self, accountId, bandMgrId, bandId):
        for friendId in self.getFriendIds(accountId):
            if self.isOnline(friendId):
                self.sendUpdateToAccountId(friendId, 'setBandId', [accountId, bandMgrId, bandId])
