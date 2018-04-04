
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedInstanceBaseAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInstanceBaseAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # setType(uint8) broadcast ram

    def setType(self, type):
        self.sendUpdate('setType', [type])

    # setSpawnInfo(int32/10, int32/10, int32/10, int16, uint32, uint32 [])

    def setSpawnInfo(self, spawnInfo, todo_int32_10_1, todo_int32_10_2, todo_int16_3, todo_uint32_4, todo_uint32_5):
        self.sendUpdate('setSpawnInfo', [spawnInfo, todo_int32_10_1, todo_int32_10_2, todo_int16_3, todo_uint32_4, todo_uint32_5])

    # requestSpawnLoc() airecv clsend

    def requestSpawnLoc(self, requestSpawnLoc):
        pass

    # avatarDied() airecv clsend

    def avatarDied(self, avatarDied):
        pass

    # sendLocalAvatarToJail(uint32, uint32, uint32) broadcast

    def sendLocalAvatarToJail(self, sendLocalAvatarToJail, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('sendLocalAvatarToJail', [sendLocalAvatarToJail, todo_uint32_1, todo_uint32_2])


