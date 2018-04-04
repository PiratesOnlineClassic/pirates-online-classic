
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class TradeManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TradeManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # requestCreateTrade(uint32) airecv clsend

    def requestCreateTrade(self, requestCreateTrade):
        pass

    # rejectCreateTrade(uint32, uint32)

    def rejectCreateTrade(self, rejectCreateTrade, todo_uint32_1):
        self.sendUpdate('rejectCreateTrade', [rejectCreateTrade, todo_uint32_1])

    # createTradeResponse(uint32, uint32)

    def createTradeResponse(self, createTradeResponse, todo_uint32_1):
        self.sendUpdate('createTradeResponse', [createTradeResponse, todo_uint32_1])


