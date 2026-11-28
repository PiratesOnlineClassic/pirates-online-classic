import random

from direct.directnotify import DirectNotifyGlobal
from direct.task import Task

from pirates.kraken import KrakenAI
from pirates.ship.GameFSMShipAI import getIslandAvoidSpheres


class KrakenSummonerAI:
    """
    Every so often the kraken rises from the deep beneath a player ship sailing in
    open water, far from any island. A ship it has attacked is left alone for a while.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('KrakenSummonerAI')

    CheckPeriod = config.GetFloat('kraken-summon-period', 60.0)
    SummonChance = config.GetFloat('kraken-summon-chance', 0.05)
    ShipCooldown = config.GetFloat('kraken-ship-cooldown', 1800.0)

    # how far from the nearest island's avoid sphere a ship must be
    OpenWaterDistance = 4000.0

    # the kraken only goes after ships that are under sail
    SailingStates = ('Adrift', 'ClientSteering', 'AISteering')

    def __init__(self, air, shipManager):
        self.air = air
        self.shipManager = shipManager
        self.lastAttacked = {}
        self.islandSpheres = None
        self.task = None

    def start(self):
        self.stop()
        self.task = taskMgr.doMethodLater(self.CheckPeriod, self.__check, 'KrakenSummonerAI-check')

    def stop(self):
        if self.task:
            taskMgr.remove(self.task)
            self.task = None

    def getIslandSpheres(self):
        if self.islandSpheres is None:
            world = self.shipManager.world
            if not world or not hasattr(world, 'builder'):
                return []

            self.islandSpheres = getIslandAvoidSpheres(world)

        return self.islandSpheres

    def isInOpenWater(self, ship):
        oceanGrid = ship.getParentObj()
        pos = ship.getPos(oceanGrid) if oceanGrid is not None else ship.getPos()
        for x, y, radius in self.getIslandSpheres():
            distance = radius + self.OpenWaterDistance
            if (pos[0] - x) ** 2 + (pos[1] - y) ** 2 < distance * distance:
                return False

        return True

    def canAttack(self, ship, now):
        if not ship.getCrew() or ship.isEmpty():
            return False

        if ship.getCurrentGameState() not in self.SailingStates or ship.hasSpawnBuff():
            return False

        if now - self.lastAttacked.get(ship.doId, -self.ShipCooldown) < self.ShipCooldown:
            return False

        if KrakenAI.getKrakenForShip(self.air, ship.doId):
            return False

        return self.isInOpenWater(ship)

    def __check(self, task):
        now = globalClock.getFrameTime()
        for ship in self.shipManager.getPlayerShips():
            if not self.canAttack(ship, now) or random.random() >= self.SummonChance:
                continue

            if KrakenAI.spawnKraken(self.air, ship):
                self.lastAttacked[ship.doId] = now
                self.notify.info('The kraken rises beneath ship %d!' % ship.doId)

        return Task.again
