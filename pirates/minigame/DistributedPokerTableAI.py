
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPokerTableAI(DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPokerTableAI')

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air)
        self.anteList = 0
        self.tableState = [0, 0, [], [], 0, 0]
        self.potSize = 0


    # setAnteList(uint32 []) required broadcast
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setAnteList(self, anteList):
        self.anteList = anteList

    def d_setAnteList(self, anteList):
        self.sendUpdate('setAnteList', [anteList])

    def b_setAnteList(self, anteList):
        self.setAnteList(anteList)
        self.d_setAnteList(anteList)

    def getAnteList(self):
        return self.anteList

    # sendTell(uint32)

    def sendTell(self, sendTell):
        self.sendUpdate('sendTell', [sendTell])

    # requestCheat(uint8, uint8) airecv clsend

    def requestCheat(self, requestCheat, todo_uint8_1):
        pass

    # cheatResponse(uint8, uint8, uint8, CardHand)

    def cheatResponse(self, cheatResponse, todo_uint8_1, todo_uint8_2, todo_CardHand_3):
        self.sendUpdate('cheatResponse', [cheatResponse, todo_uint8_1, todo_uint8_2, todo_CardHand_3])

    # requestAIPlayerTurn(uint8) broadcast

    def requestAIPlayerTurn(self, requestAIPlayerTurn):
        self.sendUpdate('requestAIPlayerTurn', [requestAIPlayerTurn])

    # askForClientAction(uint8) broadcast

    def askForClientAction(self, askForClientAction):
        self.sendUpdate('askForClientAction', [askForClientAction])

    # clientAction(int8, PokerAction) airecv clsend

    def clientAction(self, clientAction, todo_PokerAction_1):
        pass

    # setTableState(int8, uint8, CardHand, CardHand [], int32 [], int32 []) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setTableState(self, tableState, todo_uint8_1, todo_CardHand_2, todo_CardHand_3, todo_int32_4, todo_int32_5):
        self.tableState = tableState

    def d_setTableState(self, tableState, todo_uint8_1, todo_CardHand_2, todo_CardHand_3, todo_int32_4, todo_int32_5):
        self.sendUpdate('setTableState', [tableState, todo_uint8_1, todo_CardHand_2, todo_CardHand_3, todo_int32_4, todo_int32_5])

    def b_setTableState(self, tableState, todo_uint8_1, todo_CardHand_2, todo_CardHand_3, todo_int32_4, todo_int32_5):
        self.setTableState(tableState, todo_uint8_1, todo_CardHand_2, todo_CardHand_3, todo_int32_4, todo_int32_5)
        self.d_setTableState(tableState, todo_uint8_1, todo_CardHand_2, todo_CardHand_3, todo_int32_4, todo_int32_5)

    def getTableState(self):
        return self.tableState

    # setPotSize(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setPotSize(self, potSize):
        self.potSize = potSize

    def d_setPotSize(self, potSize):
        self.sendUpdate('setPotSize', [potSize])

    def b_setPotSize(self, potSize):
        self.setPotSize(potSize)
        self.d_setPotSize(potSize)

    def getPotSize(self):
        return self.potSize

    # setPlayerActions(uint16, PokerActionList, int32 []) broadcast ram

    def setPlayerActions(self, playerActions, todo_PokerActionList_1, todo_int32_2):
        self.sendUpdate('setPlayerActions', [playerActions, todo_PokerActionList_1, todo_int32_2])

    # setLocalAvatarHand(CardHand)

    def setLocalAvatarHand(self, localAvatarHand):
        self.sendUpdate('setLocalAvatarHand', [localAvatarHand])

    # setLocalAvatarHandValue(uint8, CardHand)

    def setLocalAvatarHandValue(self, localAvatarHandValue, todo_CardHand_1):
        self.sendUpdate('setLocalAvatarHandValue', [localAvatarHandValue, todo_CardHand_1])

    # setAllHandValues(uint8 [], CardHand []) broadcast

    def setAllHandValues(self, allHandValues, todo_CardHand_1):
        self.sendUpdate('setAllHandValues', [allHandValues, todo_CardHand_1])


