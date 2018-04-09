# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.friends.FriendInfo
from otp.avatar.AvatarHandle import AvatarHandle


class FriendInfo(AvatarHandle):
    

    def __init__(self, avatarName='', playerName='', onlineYesNo=0, openChatEnabledYesNo=0, openChatFriendshipYesNo=0, understandableYesNo=0, location='', sublocation='', timestamp=0, avatarId=0, friendPrivs=0, tokenPrivs=0):
        self.avatarName = avatarName
        self.playerName = playerName
        self.onlineYesNo = onlineYesNo
        self.openChatEnabledYesNo = openChatEnabledYesNo
        self.openChatFriendshipYesNo = openChatFriendshipYesNo
        self.understandableYesNo = understandableYesNo
        self.location = location
        self.sublocation = sublocation
        self.timestamp = timestamp
        self.avatarId = avatarId
        self.friendPrivs = friendPrivs
        self.tokenPrivs = tokenPrivs

    def getName(self):
        if self.avatarName:
            return self.avatarName
        else:
            if self.playerName:
                return self.playerName
            else:
                return ''

    def isUnderstandable(self):
        return self.understandableYesNo

    def isOnline(self):
        return self.onlineYesNo
# okay decompiling .\otp\friends\FriendInfo.pyc
