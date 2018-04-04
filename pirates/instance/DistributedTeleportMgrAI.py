
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTeleportMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTeleportMgrAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # initiateTeleport(uint8, uint8, uint32, string, uint32, string, int32, uint32, uint32) airecv clsend

    def initiateTeleport(self, initiateTeleport, todo_uint8_1, todo_uint32_2, todo_string_3, todo_uint32_4, todo_string_5, todo_int32_6, todo_uint32_7, todo_uint32_8):
        pass

    # initiateTeleportAI(uint8, string)

    def initiateTeleportAI(self, initiateTeleportAI, todo_string_1):
        self.sendUpdate('initiateTeleportAI', [initiateTeleportAI, todo_string_1])

    # teleportHasBegun(uint8, uint8, string, int32)

    def teleportHasBegun(self, teleportHasBegun, todo_uint8_1, todo_string_2, todo_int32_3):
        self.sendUpdate('teleportHasBegun', [teleportHasBegun, todo_uint8_1, todo_string_2, todo_int32_3])

    # beginTeleportPull(uint32 [], string, uint8, string, uint32, uint8, uint32, uint32, int32, resultPair [], shipList [], uint32, uint32)

    def beginTeleportPull(self, beginTeleportPull, todo_string_1, todo_uint8_2, todo_string_3, todo_uint32_4, todo_uint8_5, todo_uint32_6, todo_uint32_7, todo_int32_8, todo_resultPair_9, todo_shipList_10, todo_uint32_11, todo_uint32_12):
        self.sendUpdate('beginTeleportPull', [beginTeleportPull, todo_string_1, todo_uint8_2, todo_string_3, todo_uint32_4, todo_uint8_5, todo_uint32_6, todo_uint32_7, todo_int32_8, todo_resultPair_9, todo_shipList_10, todo_uint32_11, todo_uint32_12])

    # beginDeployThenTeleportPull(uint32, string, uint32)

    def beginDeployThenTeleportPull(self, beginDeployThenTeleportPull, todo_string_1, todo_uint32_2):
        self.sendUpdate('beginDeployThenTeleportPull', [beginDeployThenTeleportPull, todo_string_1, todo_uint32_2])

    # requestTargetsLocation(uint32) airecv clsend

    def requestTargetsLocation(self, requestTargetsLocation):
        pass

    # _localTeleportToIdResponse(uint32, uint32)

    def _localTeleportToIdResponse(self, _localTeleportToIdResponse, todo_uint32_1):
        self.sendUpdate('_localTeleportToIdResponse', [_localTeleportToIdResponse, todo_uint32_1])

    # requestTeleportToIsland(string) airecv clsend

    def requestTeleportToIsland(self, requestTeleportToIsland):
        pass

    # teleportToIslandResponse(uint32, uint32)

    def teleportToIslandResponse(self, teleportToIslandResponse, todo_uint32_1):
        self.sendUpdate('teleportToIslandResponse', [teleportToIslandResponse, todo_uint32_1])

    # requestCrossShardDeploy(uint32, string, uint32) clsend airecv

    def requestCrossShardDeploy(self, requestCrossShardDeploy, todo_string_1, todo_uint32_2):
        pass

    # setWelcomeShardMin(uint16)

    def setWelcomeShardMin(self, welcomeShardMin):
        self.sendUpdate('setWelcomeShardMin', [welcomeShardMin])


