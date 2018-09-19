import random

from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals
from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI

class DistributedJailInteriorAI(DistributedGAInteriorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedJailInteriorAI')

    def __init__(self, air):
        DistributedGAInteriorAI.__init__(self, air, True)

        self.__cellDoors = {}

    def handleChildArrive(self, childObj, zoneId):
        if isinstance(childObj, DistributedPlayerPirateAI) and not childObj.isNpc:
            if childObj.getJailCellIndex() < 100:
                childObj.b_setGameState('ThrownInJail')

        DistributedGAInteriorAI.handleChildArrive(self, childObj, zoneId)

    def handleChildLeave(self, childObj, zoneId):
        if isinstance(childObj, DistributedPlayerPirateAI) and not childObj.isNpc:
            if childObj.getJailCellIndex() < 100:
                cellDoor = self.getCellDoor(avatarId=childObj.doId)

                if not cellDoor:
                    self.notify.warning('Cannot reset cell door for avatar %d, no cell door found!' % (
                        avatar.doId))

                    return

                childObj.b_setJailCellIndex(100)
                cellDoor.b_setHealth(cellDoor.getMaxHealth())

        DistributedGAInteriorAI.handleChildLeave(self, childObj, zoneId)

    def hasCellDoor(self, cellDoorId):
        return cellDoorId in self.__cellDoors

    def addCellDoor(self, cellDoor):
        if cellDoor.doId in self.__cellDoors:
            return

        self.__cellDoors[cellDoor.doId] = cellDoor

    def removeCellDoor(self, cellDoor):
        if cellDoor.doId not in self.__cellDoors:
            return

        del self.__cellDoors[cellDoor.doId]

    def getCellDoor(self, cellDoorId=None, avatarId=None):
        if avatarId:
            for cellDoor in self.__cellDoors.values():
                if cellDoor.getAvatarId() == avatarId:
                    cellDoorId = cellDoor.doId
                    break

        if not cellDoorId:
            cellDoorId = random.choice(self.__cellDoors.keys())

        return self.__cellDoors.get(cellDoorId)

    def avatarAlreadyInJail(self):
        pass
