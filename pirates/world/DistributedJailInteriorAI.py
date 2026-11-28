import random

from direct.directnotify import DirectNotifyGlobal

from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI
from pirates.piratesbase import PiratesGlobals
from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI


class DistributedJailInteriorAI(DistributedGAInteriorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedJailInteriorAI')

    def __init__(self, air):
        DistributedGAInteriorAI.__init__(self, air, True)

        self.cellDoors = {}

    def handleChildLeave(self, childObj, zoneId):
        if isinstance(childObj, DistributedPlayerPirateAI) and not childObj.isNpc:
            if childObj.getJailCellIndex() < 100:
                cellDoor = self.getCellDoor(avatarId=childObj.doId)
                childObj.b_setJailCellIndex(100)
                if cellDoor is None:
                    self.notify.warning('Cannot reset cell door for avatar %d, no cell door found!' % childObj.doId)
                else:
                    cellDoor.setAvatarId(0)
                    cellDoor.b_setHealth(cellDoor.getMaxHealth())

        DistributedGAInteriorAI.handleChildLeave(self, childObj, zoneId)

    def hasCellDoor(self, cellDoorId):
        return cellDoorId in self.cellDoors

    def addCellDoor(self, cellDoor):
        if cellDoor.doId in self.cellDoors:
            return

        self.cellDoors[cellDoor.doId] = cellDoor

    def removeCellDoor(self, cellDoor):
        if cellDoor.doId not in self.cellDoors:
            return

        del self.cellDoors[cellDoor.doId]

    def getCellDoor(self, cellDoorId=None, avatarId=None):
        if cellDoorId is not None:
            return self.cellDoors.get(cellDoorId)

        if avatarId is not None:
            for cellDoor in list(self.cellDoors.values()):
                if cellDoor.getAvatarId() == avatarId:
                    return cellDoor

            avatar = self.air.doId2do.get(avatarId)
            if avatar:
                for cellDoor in list(self.cellDoors.values()):
                    if cellDoor.getCellIndex() == avatar.getJailCellIndex():
                        return cellDoor

            return None

        if len(self.cellDoors) == 0:
            return None

        return random.choice(list(self.cellDoors.values()))

    def avatarAlreadyInJail(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if avatar.getParentObj() is not self:
            self.notify.warning('Avatar %d claims to already be in jail %d, '
                'but is not in this interior!' % (avatar.doId, self.doId))

            return

        if avatar.getJailCellIndex() >= 100:
            return

        # the avatar died inside of this jail so the client never sees itself
        # arrive here, finish throwing the avatar into it's cell instead...
        avatar.b_setGameState('ThrownInJail')
