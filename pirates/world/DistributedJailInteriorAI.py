import random

from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI
from direct.directnotify import DirectNotifyGlobal
from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI

class DistributedJailInteriorAI(DistributedGAInteriorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedJailInteriorAI')

    def __init__(self, air):
        DistributedGAInteriorAI.__init__(self, air)

        self.__cellDoors = {}

    def handleChildArrive(self, childObj, zoneId):
        if isinstance(childObj, DistributedPlayerPirateAI):
            if childObj.getJailCellIndex() < 100:
                childObj.b_setGameState('ThrownInJail')

        DistributedGAInteriorAI.handleChildArrive(self, childObj, zoneId)

    def hasCellDoor(self, cellDoorDoId):
        return cellDoorDoId in self.__cellDoors

    def addCellDoor(self, cellDoor):
        if cellDoor.doId in self.__cellDoors:
            return

        self.__cellDoors[cellDoor.doId] = cellDoor

    def removeCellDoor(self, cellDoor):
        if cellDoor.doId not in self.__cellDoors:
            return

        del self.__cellDoors[cellDoor.doId]

    def getCellDoor(self, cellDoorDoId=None):
        if not cellDoorDoId:
            cellDoorDoId = random.choice(self.__cellDoors.keys())

        return self.__cellDoors.get(cellDoorDoId)

    def avatarAlreadyInJail(self):
        pass
