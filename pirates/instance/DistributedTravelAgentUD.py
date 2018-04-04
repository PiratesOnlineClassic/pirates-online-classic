
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class DistributedTravelAgentUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTravelAgentUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)


    # registerAsManager(uint32, uint32, uint32, uint8, uint32, uint8)

    def registerAsManager(self, registerAsManager, todo_uint32_1, todo_uint32_2, todo_uint8_3, todo_uint32_4, todo_uint8_5):
        self.sendUpdate('registerAsManager', [registerAsManager, todo_uint32_1, todo_uint32_2, todo_uint8_3, todo_uint32_4, todo_uint8_5])

    # managerOffline(uint32, uint32, uint32)

    def managerOffline(self, managerOffline, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('managerOffline', [managerOffline, todo_uint32_1, todo_uint32_2])

    # requestPopLimits(uint32)

    def requestPopLimits(self, requestPopLimits):
        self.sendUpdate('requestPopLimits', [requestPopLimits])

    # initiateTeleportUD(string, uint8, uint8, uint32, string, uint32, uint32 [], uint32, uint32, int32, shipList [], uint32, uint32)

    def initiateTeleportUD(self, initiateTeleportUD, todo_uint8_1, todo_uint8_2, todo_uint32_3, todo_string_4, todo_uint32_5, todo_uint32_6, todo_uint32_7, todo_uint32_8, todo_int32_9, todo_shipList_10, todo_uint32_11, todo_uint32_12):
        self.sendUpdate('initiateTeleportUD', [initiateTeleportUD, todo_uint8_1, todo_uint8_2, todo_uint32_3, todo_string_4, todo_uint32_5, todo_uint32_6, todo_uint32_7, todo_uint32_8, todo_int32_9, todo_shipList_10, todo_uint32_11, todo_uint32_12])

    # requestInitLocUD(string, uint32) clsend

    # setFullShardTeleportAllowed(uint8)

    def setFullShardTeleportAllowed(self, fullShardTeleportAllowed):
        self.sendUpdate('setFullShardTeleportAllowed', [fullShardTeleportAllowed])

    # requestInstanceUpdates()

    def requestInstanceUpdates(self, requestInstanceUpdates):
        self.sendUpdate('requestInstanceUpdates', [requestInstanceUpdates])

    # requestShipDeployUD(uint32, uint32, string, uint32)

    def requestShipDeployUD(self, requestShipDeployUD, todo_uint32_1, todo_string_2, todo_uint32_3):
        self.sendUpdate('requestShipDeployUD', [requestShipDeployUD, todo_uint32_1, todo_string_2, todo_uint32_3])


