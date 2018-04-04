
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class DistributedMatchMakerUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMatchMakerUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)


    # requestActivity(uint32, uint32, int32, resultPair [], uint32 [], uint32, uint16)

    def requestActivity(self, requestActivity, todo_uint32_1, todo_int32_2, todo_resultPair_3, todo_uint32_4, todo_uint32_5, todo_uint16_6):
        self.sendUpdate('requestActivity', [requestActivity, todo_uint32_1, todo_int32_2, todo_resultPair_3, todo_uint32_4, todo_uint32_5, todo_uint16_6])




    # instanceCreated(uint32, uint32, uint32)

    def instanceCreated(self, instanceCreated, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('instanceCreated', [instanceCreated, todo_uint32_1, todo_uint32_2])

    # instanceRemoved(uint32, uint32, uint32)

    def instanceRemoved(self, instanceRemoved, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('instanceRemoved', [instanceRemoved, todo_uint32_1, todo_uint32_2])

    # printStatus(uint32)

    def printStatus(self, printStatus):
        self.sendUpdate('printStatus', [printStatus])

    # newDistrictOnline(uint32)

    def newDistrictOnline(self, newDistrictOnline):
        self.sendUpdate('newDistrictOnline', [newDistrictOnline])

    # initiateTeleportResp(uint32, uint32)

    def initiateTeleportResp(self, initiateTeleportResp, todo_uint32_1):
        self.sendUpdate('initiateTeleportResp', [initiateTeleportResp, todo_uint32_1])

    # avatarOffline(uint32)

    def avatarOffline(self, avatarOffline):
        self.sendUpdate('avatarOffline', [avatarOffline])


