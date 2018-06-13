from pirates.movement.DistributedMovingObjectAI import DistributedMovingObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.battle.Teamable import Teamable

class DistributedShipAI(DistributedMovingObjectAI, Teamable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipAI')

    def __init__(self, air):
        DistributedMovingObjectAI.__init__(self, air)
        Teamable.__init__(self)

        self.gameState = ['Off', 0, 0]

    def setGameState(self, stateName, avId, timeStamp):
        self.gamestate = [stateName, avId, timeStamp]

    def d_setGameState(self, stateName, avId, timeStamp):
        self.sendUpdate('setGameState', [stateName, avId, timeStamp])

    def b_setGameState(self, stateName, avId, timeStamp):
        self.setGameState(stateName, avId, timeStamp)
        self.d_setGameState(stateName, avId, timeStamp)

    def getGameState(self):
        return self.gameState
