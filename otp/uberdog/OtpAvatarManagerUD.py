
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class OtpAvatarManagerUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('OtpAvatarManagerUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)


    # online()

    def online(self, online):
        self.sendUpdate('online', [online])


    # rejectAvatarList(uint32)

    def rejectAvatarList(self, rejectAvatarList):
        self.sendUpdate('rejectAvatarList', [rejectAvatarList])

    # avatarListResponse(blob)

    def avatarListResponse(self, avatarListResponse):
        self.sendUpdate('avatarListResponse', [avatarListResponse])


    # rejectAvatarSlot(uint32, uint32, uint8)

    def rejectAvatarSlot(self, rejectAvatarSlot, todo_uint32_1, todo_uint8_2):
        self.sendUpdate('rejectAvatarSlot', [rejectAvatarSlot, todo_uint32_1, todo_uint8_2])

    # avatarSlotResponse(uint32, uint8)

    def avatarSlotResponse(self, avatarSlotResponse, todo_uint8_1):
        self.sendUpdate('avatarSlotResponse', [avatarSlotResponse, todo_uint8_1])


    # rejectPlayAvatar(uint32, uint32)

    def rejectPlayAvatar(self, rejectPlayAvatar, todo_uint32_1):
        self.sendUpdate('rejectPlayAvatar', [rejectPlayAvatar, todo_uint32_1])

    # playAvatarResponse(uint32, uint32, uint8, uint8)

    def playAvatarResponse(self, playAvatarResponse, todo_uint32_1, todo_uint8_2, todo_uint8_3):
        self.sendUpdate('playAvatarResponse', [playAvatarResponse, todo_uint32_1, todo_uint8_2, todo_uint8_3])

    # rejectCreateAvatar(uint32)

    def rejectCreateAvatar(self, rejectCreateAvatar):
        self.sendUpdate('rejectCreateAvatar', [rejectCreateAvatar])

    # createAvatarResponse(uint32, uint32, uint8, uint8)

    def createAvatarResponse(self, createAvatarResponse, todo_uint32_1, todo_uint8_2, todo_uint8_3):
        self.sendUpdate('createAvatarResponse', [createAvatarResponse, todo_uint32_1, todo_uint8_2, todo_uint8_3])


    # rejectRemoveAvatar(uint32)

    def rejectRemoveAvatar(self, rejectRemoveAvatar):
        self.sendUpdate('rejectRemoveAvatar', [rejectRemoveAvatar])

    # removeAvatarResponse(uint32, uint32)

    def removeAvatarResponse(self, removeAvatarResponse, todo_uint32_1):
        self.sendUpdate('removeAvatarResponse', [removeAvatarResponse, todo_uint32_1])


    # rejectShareAvatar(uint32)

    def rejectShareAvatar(self, rejectShareAvatar):
        self.sendUpdate('rejectShareAvatar', [rejectShareAvatar])

    # shareAvatarResponse(uint32, uint32, uint8)

    def shareAvatarResponse(self, shareAvatarResponse, todo_uint32_1, todo_uint8_2):
        self.sendUpdate('shareAvatarResponse', [shareAvatarResponse, todo_uint32_1, todo_uint8_2])


