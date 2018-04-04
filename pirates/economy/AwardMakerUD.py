
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class AwardMakerUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('AwardMakerUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)


    # recvAwardableAvatars(uint32, uint32 [], string [])

    def recvAwardableAvatars(self, recvAwardableAvatars, todo_uint32_1, todo_string_2):
        self.sendUpdate('recvAwardableAvatars', [recvAwardableAvatars, todo_uint32_1, todo_string_2])

    # awardSuccess(uint32)

    def awardSuccess(self, awardSuccess):
        self.sendUpdate('awardSuccess', [awardSuccess])

    # awardFailure(uint32)

    def awardFailure(self, awardFailure):
        self.sendUpdate('awardFailure', [awardFailure])


