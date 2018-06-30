from otp.avatar.AvatarHandle import AvatarHandle


class FriendInfo(AvatarHandle):

    def __init__(self,
                 avatarName='',
                 playerName='',
                 onlineYesNo=0,
                 openChatEnabledYesNo=0,
                 openChatFriendshipYesNo=0,
                 understandableYesNo=0,
                 location='',
                 sublocation='',
                 timestamp=0,
                 avatarId=0,
                 friendPrivs=0,
                 tokenPrivs=0):
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
        elif self.playerName:
            return self.playerName
        else:
            return ''

    def isUnderstandable(self):
        return self.understandableYesNo

    def isOnline(self):
        return self.onlineYesNo
