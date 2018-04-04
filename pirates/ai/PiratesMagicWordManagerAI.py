
from otp.ai.MagicWordManagerAI import MagicWordManagerAI
from direct.directnotify import DirectNotifyGlobal

class PiratesMagicWordManagerAI(MagicWordManagerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesMagicWordManagerAI')

    def __init__(self, air):
        MagicWordManagerAI.__init__(self, air)


    # cameraReparent(uint32, uint32, uint32)

    def cameraReparent(self, cameraReparent, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('cameraReparent', [cameraReparent, todo_uint32_1, todo_uint32_2])

    # shipCreated(uint32)

    def shipCreated(self, shipCreated):
        self.sendUpdate('shipCreated', [shipCreated])

    # requestServerTime() clsend airecv

    def requestServerTime(self, requestServerTime):
        pass

    # recvServerTime(uint32)

    def recvServerTime(self, recvServerTime):
        self.sendUpdate('recvServerTime', [recvServerTime])


