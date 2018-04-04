
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class TimeManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TimeManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # requestServerTime(uint8) airecv clsend

    def requestServerTime(self, requestServerTime):
        pass

    # serverTime(uint8, int32, uint32)

    def serverTime(self, serverTime, todo_int32_1, todo_uint32_2):
        self.sendUpdate('serverTime', [serverTime, todo_int32_1, todo_uint32_2])

    # setDisconnectReason(uint8) airecv clsend

    def setDisconnectReason(self, disconnectReason):
        pass

    # setExceptionInfo(string) airecv clsend

    def setExceptionInfo(self, exceptionInfo):
        pass

    # setSignature(string, char [16], char [16]) airecv clsend

    def setSignature(self, signature, todo_char [16_1, todo_char [16_2):
        pass

    # setFrameRate(uint16/10, uint16/1000, uint16, string, uint32/10, uint32/10, string, uint16, uint16, uint16/10, uint16/10, uint16/10, uint32, OSInfo, CPUSpeed) airecv clsend

    def setFrameRate(self, frameRate, todo_uint16_1000_1, todo_uint16_2, todo_string_3, todo_uint32_10_4, todo_uint32_10_5, todo_string_6, todo_uint16_7, todo_uint16_8, todo_uint16_10_9, todo_uint16_10_10, todo_uint16_10_11, todo_uint32_12, todo_OSInfo_13, todo_CPUSpeed_14):
        pass


