
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedMatchMakerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMatchMakerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # requestActivity(uint32, uint32, int32, resultPair [], uint32 [], uint32, uint16)

    def requestActivity(self, requestActivity, todo_uint32_1, todo_int32_2, todo_resultPair_3, todo_uint32_4, todo_uint32_5, todo_uint16_6):
        self.sendUpdate('requestActivity', [requestActivity, todo_uint32_1, todo_int32_2, todo_resultPair_3, todo_uint32_4, todo_uint32_5, todo_uint16_6])

    # requestJoin(uint32) airecv clsend

    def requestJoin(self, requestJoin):
        pass

    # skipJoin(uint32, bool) airecv clsend

    def skipJoin(self, skipJoin, todo_bool_1):
        pass

    # cancelRequest(uint32) airecv clsend

    def cancelRequest(self, cancelRequest):
        pass

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


