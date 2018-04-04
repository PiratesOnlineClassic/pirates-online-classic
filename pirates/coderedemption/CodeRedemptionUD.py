
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class CodeRedemptionUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('CodeRedemptionUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)


    # online()

    def online(self, online):
        self.sendUpdate('online', [online])

    # recvAvatarGender(uint32, string, uint32)

    def recvAvatarGender(self, recvAvatarGender, todo_string_1, todo_uint32_2):
        self.sendUpdate('recvAvatarGender', [recvAvatarGender, todo_string_1, todo_uint32_2])


    # notifyClientCodeRedeemStatus(uint8)

    def notifyClientCodeRedeemStatus(self, notifyClientCodeRedeemStatus):
        self.sendUpdate('notifyClientCodeRedeemStatus', [notifyClientCodeRedeemStatus])


