
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class PlayerFriendsManagerUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayerFriendsManagerUD')

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



    # secretResponse(string)

    def secretResponse(self, secretResponse):
        self.sendUpdate('secretResponse', [secretResponse])

    # rejectSecret(string)

    def rejectSecret(self, rejectSecret):
        self.sendUpdate('rejectSecret', [rejectSecret])



    # rejectUseSecret(string)

    def rejectUseSecret(self, rejectUseSecret):
        self.sendUpdate('rejectUseSecret', [rejectUseSecret])






    # whisperFrom(uint32, string)

    def whisperFrom(self, whisperFrom, todo_string_1):
        self.sendUpdate('whisperFrom', [whisperFrom, todo_string_1])

    # whisperWLFrom(uint32, string)

    def whisperWLFrom(self, whisperWLFrom, todo_string_1):
        self.sendUpdate('whisperWLFrom', [whisperWLFrom, todo_string_1])

    # whisperSCFrom(uint32, string)

    def whisperSCFrom(self, whisperSCFrom, todo_string_1):
        self.sendUpdate('whisperSCFrom', [whisperSCFrom, todo_string_1])

    # updatePlayerFriend(uint32, FriendInfo)

    def updatePlayerFriend(self, updatePlayerFriend, todo_FriendInfo_1):
        self.sendUpdate('updatePlayerFriend', [updatePlayerFriend, todo_FriendInfo_1])

    # removePlayerFriend(uint32)

    def removePlayerFriend(self, removePlayerFriend):
        self.sendUpdate('removePlayerFriend', [removePlayerFriend])

    # avatarOffline(uint32)

    def avatarOffline(self, avatarOffline):
        self.sendUpdate('avatarOffline', [avatarOffline])


