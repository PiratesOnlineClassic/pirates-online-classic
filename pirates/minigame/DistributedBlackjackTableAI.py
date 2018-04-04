
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBlackjackTableAI(DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBlackjackTableAI')

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air)
        self.betMultiplier = 0
        self.tableState = [[], 0]


    # setBetMultiplier(uint32) required broadcast
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setBetMultiplier(self, betMultiplier):
        self.betMultiplier = betMultiplier

    def d_setBetMultiplier(self, betMultiplier):
        self.sendUpdate('setBetMultiplier', [betMultiplier])

    def b_setBetMultiplier(self, betMultiplier):
        self.setBetMultiplier(betMultiplier)
        self.d_setBetMultiplier(betMultiplier)

    def getBetMultiplier(self):
        return self.betMultiplier

    # setTableState(CardHandArray [], int32 []) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setTableState(self, tableState, todo_int32_1):
        self.tableState = tableState

    def d_setTableState(self, tableState, todo_int32_1):
        self.sendUpdate('setTableState', [tableState, todo_int32_1])

    def b_setTableState(self, tableState, todo_int32_1):
        self.setTableState(tableState, todo_int32_1)
        self.d_setTableState(tableState, todo_int32_1)

    def getTableState(self):
        return self.tableState

    # setEvent(uint8, BlackjackAction) broadcast

    def setEvent(self, event, todo_BlackjackAction_1):
        self.sendUpdate('setEvent', [event, todo_BlackjackAction_1])

    # requestClientAction(uint8) airecv clsend

    def requestClientAction(self, requestClientAction):
        pass

    # clientAction(BlackjackAction) airecv clsend

    def clientAction(self, clientAction):
        pass

    # requestCheat(uint8, uint8) airecv clsend

    def requestCheat(self, requestCheat, todo_uint8_1):
        pass

    # cheatResponse(uint8, uint8, uint8, CardHand)

    def cheatResponse(self, cheatResponse, todo_uint8_1, todo_uint8_2, todo_CardHand_3):
        self.sendUpdate('cheatResponse', [cheatResponse, todo_uint8_1, todo_uint8_2, todo_CardHand_3])

    # setHandResults(int16 []) broadcast

    def setHandResults(self, handResults):
        self.sendUpdate('setHandResults', [handResults])


