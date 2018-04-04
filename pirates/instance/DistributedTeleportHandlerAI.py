
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTeleportHandlerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTeleportHandlerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # startTeleportProcess(uint32, uint32, uint32) airecv clsend

    def startTeleportProcess(self, startTeleportProcess, todo_uint32_1, todo_uint32_2):
        pass

    # continueTeleportToTZ() airecv clsend

    def continueTeleportToTZ(self, continueTeleportToTZ):
        pass

    # waitInTZ(uint32 [], uint32) broadcast ram

    def waitInTZ(self, waitInTZ, todo_uint32_1):
        self.sendUpdate('waitInTZ', [waitInTZ, todo_uint32_1])

    # teleportToInstanceReady(uint32) airecv clsend

    def teleportToInstanceReady(self, teleportToInstanceReady):
        pass

    # continueTeleportToInstance(uint32, uint32, uint32, string, uint32, uint32, uint32, string, uint32) broadcast ram

    def continueTeleportToInstance(self, continueTeleportToInstance, todo_uint32_1, todo_uint32_2, todo_string_3, todo_uint32_4, todo_uint32_5, todo_uint32_6, todo_string_7, todo_uint32_8):
        self.sendUpdate('continueTeleportToInstance', [continueTeleportToInstance, todo_uint32_1, todo_uint32_2, todo_string_3, todo_uint32_4, todo_uint32_5, todo_uint32_6, todo_string_7, todo_uint32_8])

    # readyToFinishTeleport(uint32) airecv clsend

    def readyToFinishTeleport(self, readyToFinishTeleport):
        pass

    # teleportToInstanceCleanup() broadcast ram

    def teleportToInstanceCleanup(self, teleportToInstanceCleanup):
        self.sendUpdate('teleportToInstanceCleanup', [teleportToInstanceCleanup])

    # teleportToInstanceFinal(uint32) airecv clsend

    def teleportToInstanceFinal(self, teleportToInstanceFinal):
        pass

    # abortTeleport() broadcast ram

    def abortTeleport(self, abortTeleport):
        self.sendUpdate('abortTeleport', [abortTeleport])

    # avatarLeft() airecv clsend

    def avatarLeft(self, avatarLeft):
        pass


