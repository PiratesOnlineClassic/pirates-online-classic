# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.friends.PCFriendInfo
from otp.friends.FriendInfo import FriendInfo
from pirates.pirate.PAvatarHandle import PAvatarHandle


class PCFriendInfo(FriendInfo, PAvatarHandle):

    @classmethod
    def makeFromFriendInfo(cls, info):
        out = cls()
        out.avatarName = info.avatarName
        out.playerName = info.playerName
        out.onlineYesNo = info.onlineYesNo
        out.openChatEnabledYesNo = info.openChatEnabledYesNo
        out.openChatFriendshipYesNo = info.openChatFriendshipYesNo
        out.understandableYesNo = info.understandableYesNo
        out.location = info.location
        out.sublocation = info.sublocation
        out.timestamp = info.timestamp
        out.avatarId = info.avatarId
        out.friendPrivs = info.friendPrivs
        out.tokenPrivs = info.tokenPrivs
        return out

    def __init__(self, *args, **kw):
        FriendInfo.__init__(self, *args, **kw)
        self.bandId = (0, 0)

    def setBandId(self, bandMgrId, bandId):
        self.bandId = (bandMgrId, bandId)

    def getBandId(self):
        return self.bandId

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def sendTeleportQuery(self, sendToId, localShardId):
        localAvatar.sendTeleportQuery(sendToId, localShardId)

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def sendTeleportResponse(self,
                             available,
                             shardId,
                             instanceDoId,
                             areaDoId,
                             sendToId=None):
        localAvatar.sendTeleportResponse(available, shardId, instanceDoId,
                                         areaDoId, sendToId)


# okay decompiling .\pirates\friends\PCFriendInfo.pyc
