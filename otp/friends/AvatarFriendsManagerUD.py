
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class AvatarFriendsManagerUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('AvatarFriendsManagerUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)


    # online()

    def online(self, online):
        self.sendUpdate('online', [online])



    # invitationFrom(uint32, string)

    def invitationFrom(self, invitationFrom, todo_string_1):
        self.sendUpdate('invitationFrom', [invitationFrom, todo_string_1])

    # retractInvite(uint32)

    def retractInvite(self, retractInvite):
        self.sendUpdate('retractInvite', [retractInvite])

    # rejectInvite(uint32, uint32)

    def rejectInvite(self, rejectInvite, todo_uint32_1):
        self.sendUpdate('rejectInvite', [rejectInvite, todo_uint32_1])


    # rejectRemove(uint32, uint32)

    def rejectRemove(self, rejectRemove, todo_uint32_1):
        self.sendUpdate('rejectRemove', [rejectRemove, todo_uint32_1])

    # updateAvatarFriend(uint32, FriendInfo)

    def updateAvatarFriend(self, updateAvatarFriend, todo_FriendInfo_1):
        self.sendUpdate('updateAvatarFriend', [updateAvatarFriend, todo_FriendInfo_1])

    # removeAvatarFriend(uint32)

    def removeAvatarFriend(self, removeAvatarFriend):
        self.sendUpdate('removeAvatarFriend', [removeAvatarFriend])

    # updateAvatarName(uint32, string)

    def updateAvatarName(self, updateAvatarName, todo_string_1):
        self.sendUpdate('updateAvatarName', [updateAvatarName, todo_string_1])

    # avatarOffline(uint32)

    def avatarOffline(self, avatarOffline):
        self.sendUpdate('avatarOffline', [avatarOffline])


