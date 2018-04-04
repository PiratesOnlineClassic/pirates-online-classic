
from pirates.minigame.DistributedDiceGameAI import DistributedDiceGameAI
from direct.directnotify import DirectNotifyGlobal

class DistributedLiarsDiceAI(DistributedDiceGameAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLiarsDiceAI')

    def __init__(self, air):
        DistributedDiceGameAI.__init__(self, air)


    # tableStatus(uint8, uint8) broadcast

    def tableStatus(self, tableStatus, todo_uint8_1):
        self.sendUpdate('tableStatus', [tableStatus, todo_uint8_1])

    # betUpdate(uint8, uint8, uint8) airecv clsend

    def betUpdate(self, betUpdate, todo_uint8_1, todo_uint8_2):
        pass

    # youWin(uint32, string) broadcast

    def youWin(self, youWin, todo_string_1):
        self.sendUpdate('youWin', [youWin, todo_string_1])

    # newRound() broadcast

    def newRound(self, newRound):
        self.sendUpdate('newRound', [newRound])

    # cheatResult(uint8, uint8, uint8) airecv clsend

    def cheatResult(self, cheatResult, todo_uint8_1, todo_uint8_2):
        pass

    # incomingCheat(uint8, uint8, uint8) broadcast

    def incomingCheat(self, incomingCheat, todo_uint8_1, todo_uint8_2):
        self.sendUpdate('incomingCheat', [incomingCheat, todo_uint8_1, todo_uint8_2])

    # catchCheater(uint8) airecv clsend

    def catchCheater(self, catchCheater):
        pass

    # gotCaught(uint8, string) broadcast

    def gotCaught(self, gotCaught, todo_string_1):
        self.sendUpdate('gotCaught', [gotCaught, todo_string_1])

    # callBluff(uint8, uint8, uint8) airecv clsend

    def callBluff(self, callBluff, todo_uint8_1, todo_uint8_2):
        pass

    # displayChallenge(uint8, uint8, uint8, uint8, string) broadcast

    def displayChallenge(self, displayChallenge, todo_uint8_1, todo_uint8_2, todo_uint8_3, todo_string_4):
        self.sendUpdate('displayChallenge', [displayChallenge, todo_uint8_1, todo_uint8_2, todo_uint8_3, todo_string_4])


