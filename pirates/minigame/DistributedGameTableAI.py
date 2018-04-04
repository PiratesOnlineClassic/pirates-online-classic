
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal

class DistributedGameTableAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGameTableAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.tableType = 0
        self.dealerName = ''
        self.dealerType = 0
        self.aIList = 0


    # setTableType(uint8) required broadcast
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setTableType(self, tableType):
        self.tableType = tableType

    def d_setTableType(self, tableType):
        self.sendUpdate('setTableType', [tableType])

    def b_setTableType(self, tableType):
        self.setTableType(tableType)
        self.d_setTableType(tableType)

    def getTableType(self):
        return self.tableType

    # setDealerName(string) required broadcast
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setDealerName(self, dealerName):
        self.dealerName = dealerName

    def d_setDealerName(self, dealerName):
        self.sendUpdate('setDealerName', [dealerName])

    def b_setDealerName(self, dealerName):
        self.setDealerName(dealerName)
        self.d_setDealerName(dealerName)

    def getDealerName(self):
        return self.dealerName

    # setDealerType(uint8) required broadcast
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setDealerType(self, dealerType):
        self.dealerType = dealerType

    def d_setDealerType(self, dealerType):
        self.sendUpdate('setDealerType', [dealerType])

    def b_setDealerType(self, dealerType):
        self.setDealerType(dealerType)
        self.d_setDealerType(dealerType)

    def getDealerType(self):
        return self.dealerType

    # setAIList(uint8 []) required broadcast
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setAIList(self, aIList):
        self.aIList = aIList

    def d_setAIList(self, aIList):
        self.sendUpdate('setAIList', [aIList])

    def b_setAIList(self, aIList):
        self.setAIList(aIList)
        self.d_setAIList(aIList)

    def getAIList(self):
        return self.aIList

    # receiveAISpeech(int8, string) broadcast

    def receiveAISpeech(self, receiveAISpeech, todo_string_1):
        self.sendUpdate('receiveAISpeech', [receiveAISpeech, todo_string_1])

    # receiveAIThoughts(int8, string)

    def receiveAIThoughts(self, receiveAIThoughts, todo_string_1):
        self.sendUpdate('receiveAIThoughts', [receiveAIThoughts, todo_string_1])

    # requestSeat(uint8, string) airecv clsend

    def requestSeat(self, requestSeat, todo_string_1):
        pass

    # requestExit() airecv clsend

    def requestExit(self, requestExit):
        pass

    # requestSeatResponse(uint8(0-5), uint8)

    def requestSeatResponse(self, requestSeatResponse, todo_uint8_1):
        self.sendUpdate('requestSeatResponse', [requestSeatResponse, todo_uint8_1])

    # setAvatarSeat(uint32 []) broadcast ram

    def setAvatarSeat(self, avatarSeat):
        self.sendUpdate('setAvatarSeat', [avatarSeat])

    # avatarSit(uint32, uint8) broadcast

    def avatarSit(self, avatarSit, todo_uint8_1):
        self.sendUpdate('avatarSit', [avatarSit, todo_uint8_1])

    # avatarStand(uint32, uint8) broadcast

    def avatarStand(self, avatarStand, todo_uint8_1):
        self.sendUpdate('avatarStand', [avatarStand, todo_uint8_1])


