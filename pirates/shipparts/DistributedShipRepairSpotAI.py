from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task


class DistributedShipRepairSpotAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipRepairSpotAI')

    RepairPeriod = 1.0

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)

        self.shipId = 0
        self.index = 0
        self.repairTask = None

    def delete(self):
        self.stopRepairing()
        DistributedInteractiveAI.delete(self)

    def setShipId(self, shipId):
        self.shipId = shipId

    def d_setShipId(self, shipId):
        self.sendUpdate('setShipId', [shipId])

    def b_setShipId(self, shipId):
        self.setShipId(shipId)
        self.d_setShipId(shipId)

    def getShipId(self):
        return self.shipId

    def getShip(self):
        return self.air.doId2do.get(self.shipId)

    def setIndex(self, index):
        self.index = index

    def d_setIndex(self, index):
        self.sendUpdate('setIndex', [index])

    def b_setIndex(self, index):
        self.setIndex(index)
        self.d_setIndex(index)

    def getIndex(self):
        return self.index

    def canRepairShip(self, ship):
        if not ship or not ship.isSailable():
            return False

        if ship.getHp() >= ship.getMaxHp() and ship.getSp() >= ship.getMaxSp():
            return False

        # the client will not allow repairs while the wheel is occupied:
        if ship.steeringWheel and ship.steeringWheel.userId:
            return False

        return True

    def handleRequestInteraction(self, avatar, interactType, instant):
        if self.userId and self.userId != avatar.doId:
            return self.DENY

        ship = self.getShip()
        if not ship or not ship.hasCrewMember(avatar.doId):
            return self.DENY

        if not self.canRepairShip(ship):
            return self.DENY

        return self.ACCEPT

    def handlePostRequestInteraction(self, avatar):
        self.acceptOnce(avatar.getDeleteEvent(), self.stopRepairing)
        self.startRepairing()

    def handleRequestExit(self, avatar):
        return self.ACCEPT

    def handlePostRequestExit(self, avatar):
        self.ignore(avatar.getDeleteEvent())
        self.stopRepairing()

    def startRepairing(self):
        self.stopRepairing()
        self.repairTask = taskMgr.doMethodLater(self.RepairPeriod, self.__repairShip,
            self.uniqueName('repairShip'))

    def stopRepairing(self, *args):
        if self.repairTask:
            taskMgr.remove(self.repairTask)
            self.repairTask = None

    def getNumRepairers(self, ship):
        repairSpots = getattr(ship, 'repairSpots', [])
        return max(1, len([spot for spot in repairSpots if spot.userId]))

    def getRepairAmount(self, ship):
        from pirates.pvp import PVPGlobals

        numRepairers = self.getNumRepairers(ship)
        multipliers = PVPGlobals.RepairRateMultipliers.getValue()
        multiplier = multipliers[min(numRepairers, len(multipliers)) - 1]

        # the repair rate is shared between everyone repairing the ship:
        return PVPGlobals.RepairRate.getValue() * multiplier * self.RepairPeriod / numRepairers

    def __repairShip(self, task):
        ship = self.getShip()
        if not self.userId or not ship or not ship.isSailable():
            self.repairTask = None
            if self.userId:
                self.b_setUserId(0)

            return Task.done

        if not self.canRepairShip(ship):
            # nothing to repair right now, wait until the user leaves the spot...
            return Task.again

        amount = self.getRepairAmount(ship)
        ship.b_setHp(min(ship.getMaxHp(), ship.getHp() + amount))
        ship.b_setSp(min(ship.getMaxSp(), ship.getSp() + amount))
        return Task.again
