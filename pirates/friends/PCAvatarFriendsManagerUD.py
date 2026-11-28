from direct.directnotify import DirectNotifyGlobal
from otp.friends.AvatarFriendsManagerUD import AvatarFriendsManagerUD

class PCAvatarFriendsManagerUD(AvatarFriendsManagerUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PCAvatarFriendsManagerUD')

    def __init__(self, air):
        AvatarFriendsManagerUD.__init__(self, air)
        self.avatarId2BandId = {}

    def goingOffline(self, avId):
        self.avatarId2BandId.pop(avId, None)
        AvatarFriendsManagerUD.goingOffline(self, avId)

    def getBandId(self, avId):
        return self.avatarId2BandId.get(avId, (0, 0))

    def setBandId(self, avId, bandMgrId, bandId):
        # Sent to us by the district the avatar is on whenever it changes crew.
        if not self.isOnline(avId):
            return

        if bandMgrId and bandId:
            self.avatarId2BandId[avId] = (bandMgrId, bandId)
        else:
            self.avatarId2BandId.pop(avId, None)

        self.d_setBandId(avId, bandMgrId, bandId)
        self.air.playerFriendsManager.avatarBandIdChanged(avId, bandMgrId, bandId)

    def d_updateAvatarFriend(self, avId, friendId):
        AvatarFriendsManagerUD.d_updateAvatarFriend(self, avId, friendId)

        # The client builds a new friend info for every update, which
        # forgets the crew the friend is in:
        bandMgrId, bandId = self.getBandId(friendId)
        if bandId and self.isOnline(avId) and self.isOnline(friendId):
            self.sendUpdateToAvatarId(avId, 'setBandId', [friendId, bandMgrId, bandId])

    def d_setShipState(self, avId, onShip, shipId):
        for friendId in self.getFriendIds(avId):
            if self.isOnline(friendId):
                self.sendUpdateToAvatarId(friendId, 'setShipState', [avId, onShip, shipId])

    def d_setBandId(self, avId, bandMgrId, bandId):
        for friendId in self.getFriendIds(avId):
            if self.isOnline(friendId):
                self.sendUpdateToAvatarId(friendId, 'setBandId', [avId, bandMgrId, bandId])
