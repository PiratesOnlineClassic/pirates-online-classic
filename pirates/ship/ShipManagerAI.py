import random

from direct.directnotify import DirectNotifyGlobal

from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.ship.PlayerShipAI import PlayerShipAI
from pirates.ship.NPCShipAI import NPCShipAI
from pirates.ship import ShipGlobals
from pirates.world import OceanZone
from pirates.piratesbase.PLocalizerEnglish import *


class ShipManagerAI(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipManagerAI')

    def __init__(self, air):
        self.air = air

        self.playerShips = set()
        self.ships = set()

    def hasPlayerShip(self, ship):
        assert(ship is not None)
        return ship in self.playerShips

    def addPlayerShip(self, ship):
        assert(ship is not None)
        assert(isinstance(ship, PlayerShipAI))
        if ship in self.playerShips:
            return

        self.playerShips.add(ship)

    def removePlayerShip(self, ship):
        assert(ship is not None)
        assert(isinstance(ship, PlayerShipAI))
        if ship not in self.playerShips:
            return

        self.playerShips.remove(ship)

    def getPlayerShips(self):
        return list(self.playerShips)

    def hasShip(self, ship):
        assert(ship is not None)
        return ship in self.ships

    def addShip(self, ship):
        assert(ship is not None)
        assert(not isinstance(ship, PlayerShipAI))
        if ship in self.ships:
            return

        self.ships.add(ship)

    def removeShip(self, ship):
        assert(ship is not None)
        assert(not isinstance(ship, PlayerShipAI))
        if ship not in self.ships:
            return

        self.ships.remove(ship)

    def getShips(self):
        return list(self.ships)

    def _spawnEnemyShip(self, shipClass):
        modelClass = ShipGlobals.getModelClass(shipClass)
        shipConfig = ShipGlobals.getShipConfig(modelClass)
        hullConfig = ShipGlobals.getHullConfig(modelClass)

        ship = NPCShipAI(self.air)
        ship.setBaseTeam(ShipGlobals.getShipTeam(shipClass))
        ship.setLevel(1)
        ship.setShipClass(shipConfig['setShipClass'][0])
        ship.setName(ShipClassNames[shipClass])
        ship.setNPCship(1)
        ship.setIsBoardable(1)

        ship.setMaxHp(shipConfig['setMaxHp'][0])
        ship.setHp(shipConfig['setHp'][0])
        ship.setMaxSp(hullConfig['setMaxSp'][0])
        ship.setSp(hullConfig['setSp'][0])
        ship.setHullCondition(1 << 7)

        oceanGrid = self.air.worldCreator.world.oceanGrid
        world = oceanGrid.getParentObj()
        sx, sy = self.air.worldCreator.oceanAreaManager.getRandomOceanPos(world.getUniqueId())
        zoneId = oceanGrid.getZoneFromXYZ((sx, sy, 0))

        oceanGrid.generateChildWithRequired(ship, zoneId)
        ship.setPos(oceanGrid, sx, sy, 0)
        oceanGrid.addObjectToOceanGrid(ship)

        ship.sendCurrentPosition()
        ship.startPosHprBroadcast()
        ship.b_setGameState('PathFollow', 0)

    def startSpawnEnemyShips(self):
        for x in xrange(64):
            self._spawnEnemyShip(random.choice([ShipGlobals.NAVY_FERRET,
                                                ShipGlobals.NAVY_GREYHOUND,
                                                ShipGlobals.NAVY_KINGFISHER,
                                                ShipGlobals.NAVY_PREDATOR,
                                                ShipGlobals.NAVY_BULWARK,
                                                ShipGlobals.NAVY_VANGUARD,
                                                ShipGlobals.NAVY_MONARCH,
                                                ShipGlobals.NAVY_COLOSSUS,
                                                ShipGlobals.NAVY_PANTHER,
                                                ShipGlobals.NAVY_CENTURION,
                                                ShipGlobals.NAVY_MAN_O_WAR,
                                                ShipGlobals.NAVY_DREADNOUGHT,
                                                ShipGlobals.EITC_SEA_VIPER,
                                                ShipGlobals.EITC_BLOODHOUND,
                                                ShipGlobals.EITC_BARRACUDA,
                                                ShipGlobals.EITC_CORSAIR,
                                                ShipGlobals.EITC_SENTINEL,
                                                ShipGlobals.EITC_IRONWALL,
                                                ShipGlobals.EITC_OGRE,
                                                ShipGlobals.EITC_BEHEMOTH,
                                                ShipGlobals.EITC_CORVETTE,
                                                ShipGlobals.EITC_MARAUDER,
                                                ShipGlobals.EITC_WARLORD,
                                                ShipGlobals.EITC_JUGGERNAUT]))
