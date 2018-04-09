# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.friends.PCAvatarFriendsManager
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from otp.friends.AvatarFriendsManager import AvatarFriendsManager
from otp.otpbase import OTPGlobals
from pirates.friends.PCFriendInfo import PCFriendInfo


class PCAvatarFriendsManager(AvatarFriendsManager):
    
    notify = directNotify.newCategory('PCAvatarFriendsManager')

    def __init__(self, cr):
        AvatarFriendsManager.__init__(self, cr)
        self.avatarId2ShipState = {}
        self.avatarId2ShipId = {}
        self.shipId2ShipState = {}

    def updateAvatarFriend(self, id, info):
        pcinfo = PCFriendInfo.makeFromFriendInfo(info)
        AvatarFriendsManager.updateAvatarFriend(self, id, pcinfo)

    def removeAvatarFriend(self, avId):
        AvatarFriendsManager.removeAvatarFriend(self, avId)
        self.avatarId2ShipState.pop(avId, None)
        shipId = self.avatarId2ShipId.get(avId, 0)
        if shipId:
            self.shipId2ShipState.pop(avId, None)
        self.avatarId2ShipId.pop(avId, None)
        return

    def setShipState(self, avatarId, onShip, shipId):
        if not hasattr(base, 'localAvatar'):
            self.notify.warning("setShipState: But I don't have a base.localAvatar!  gameFSM in state: %s" % base.cr.gameFSM.getCurrentState().getName())
            return
        self.avatarId2ShipState[avatarId] = onShip
        self.avatarId2ShipId[avatarId] = shipId
        self.shipId2ShipState[shipId] = onShip
        base.localAvatar.guiMgr.socialPanel.updateAll()

    def getShipId2State(self, shipId):
        return self.shipId2ShipState.get(shipId, 0)

    def getShipState(self, avatarId):
        return self.avatarId2ShipState.get(avatarId, 0)

    def getShipId(self, avatarId):
        return self.avatarId2ShipId.get(avatarId, 0)

    def setBandId(self, avatarId, bandMgrId, bandId):
        info = self.avatarId2Info.get(avatarId)
        if info:
            info.setBandId(bandMgrId, bandId)

    def getBandId(self, avatarId):
        info = self.avatarId2Info.get(avatarId)
        if info:
            return info.getBandId()
# okay decompiling .\pirates\friends\PCAvatarFriendsManager.pyc
