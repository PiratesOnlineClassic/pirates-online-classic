
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from direct.directnotify import DirectNotifyGlobal

class DistributedDiceGameAI(DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDiceGameAI')

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air)


    # playerIsReady() airecv clsend

    def playerIsReady(self, playerIsReady):
        pass

    # yourTurn(uint8) broadcast

    def yourTurn(self, yourTurn):
        self.sendUpdate('yourTurn', [yourTurn])

    # changeDice(uint8, uint8 []) airecv clsend

    def changeDice(self, changeDice, todo_uint8_1):
        pass

    # playerHasRolled(uint8, uint8 []) airecv clsend

    def playerHasRolled(self, playerHasRolled, todo_uint8_1):
        pass

    # rollResults(uint8, uint8 []) broadcast

    def rollResults(self, rollResults, todo_uint8_1):
        self.sendUpdate('rollResults', [rollResults, todo_uint8_1])

    # currentTurn(uint8, uint8, string) broadcast

    def currentTurn(self, currentTurn, todo_uint8_1, todo_string_2):
        self.sendUpdate('currentTurn', [currentTurn, todo_uint8_1, todo_string_2])

    # sendChat(uint8, uint32) airecv clsend

    def sendChat(self, sendChat, todo_uint32_1):
        pass


