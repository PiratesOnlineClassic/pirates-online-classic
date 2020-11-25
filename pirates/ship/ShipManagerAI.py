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

        self.activeShips = {}

    def hasActiveShip(self, shipId):
        return shipId in self.activeShips

    def addActiveShip(self, ship):
        if ship.doId in self.activeShips:
            return

        assert(ship.getDeploy())
        self.activeShips[ship.doId] = ship

    def removeActiveShip(self, ship):
        if ship.doId not in self.activeShips:
            return

        del self.activeShips[ship.doId]

    def getActiveShip(self, shipId):
        return self.activeShips.get(shipId)

    def getActivePlayerShips(self):
        activePlayerShips = []
        for shipId, ship in list(self.activeShips.items()):
            if not isinstance(ship, PlayerShipAI):
                continue

            activePlayerShips.append(ship)

        return activePlayerShips

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
        ship.b_setGameState('Docked', 0)

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
