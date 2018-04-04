
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBishopsHandTableAI(DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBishopsHandTableAI')

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air)


    # setTableState(uint8, BishopsHandSeat []) broadcast ram

    def setTableState(self, tableState, todo_BishopsHandSeat_1):
        self.sendUpdate('setTableState', [tableState, todo_BishopsHandSeat_1])

    # setPendingStakes(uint32) broadcast ram

    def setPendingStakes(self, pendingStakes):
        self.sendUpdate('setPendingStakes', [pendingStakes])

    # setActiveStakes(uint32) broadcast ram

    def setActiveStakes(self, activeStakes):
        self.sendUpdate('setActiveStakes', [activeStakes])

    # setRunningStakes(uint32) broadcast ram

    def setRunningStakes(self, runningStakes):
        self.sendUpdate('setRunningStakes', [runningStakes])

    # setProgressReport(BishopsHandProgressReport []) broadcast

    def setProgressReport(self, progressReport):
        self.sendUpdate('setProgressReport', [progressReport])

    # setGameTimer(uint16, int32) broadcast ram

    def setGameTimer(self, gameTimer, todo_int32_1):
        self.sendUpdate('setGameTimer', [gameTimer, todo_int32_1])

    # askForClientAction(BishopsHandAction, uint16, int16) broadcast

    def askForClientAction(self, askForClientAction, todo_uint16_1, todo_int16_2):
        self.sendUpdate('askForClientAction', [askForClientAction, todo_uint16_1, todo_int16_2])

    # clientAction(BishopsHandAction) airecv clsend

    def clientAction(self, clientAction):
        pass

    # startRound(uint8 [], uint8, int16)

    def startRound(self, startRound, todo_uint8_1, todo_int16_2):
        self.sendUpdate('startRound', [startRound, todo_uint8_1, todo_int16_2])

    # receiveProgress(uint8, uint8, uint8, int16/100) airecv clsend

    def receiveProgress(self, receiveProgress, todo_uint8_1, todo_uint8_2, todo_int16_100_3):
        pass

    # leftGame()

    def leftGame(self, leftGame):
        self.sendUpdate('leftGame', [leftGame])


