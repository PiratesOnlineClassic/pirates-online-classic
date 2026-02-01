import random

from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject

from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.ship.PlayerShipAI import PlayerShipAI
from pirates.ship.NPCShipAI import NPCShipAI
from pirates.ship import ShipGlobals
from pirates.world import OceanZone
from pirates.piratesbase.PLocalizerEnglish import *


NPCSHIP_POP_UPKEEP_DELAY = config.GetFloat('npcship-pop-upkeep-delay', 10.0)
NPCSHIP_POP_MAX = config.GetInt('npcship-pop-max', 128)


class ShipManagerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipManagerAI')

    def __init__(self, air):
        self.air = air
        self.world = None

        self.playerShips = set()
        self.npcShips = set()

        self.NPCShipUpkeepTask = None

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
        return ship in self.npcShips

    def addShip(self, ship):
        assert(ship is not None)
        assert(isinstance(ship, NPCShipAI))
        if ship in self.npcShips:
            return

        self.npcShips.add(ship)

    def removeShip(self, ship):
        assert(ship is not None)
        assert(isinstance(ship, NPCShipAI))
        if ship not in self.npcShips:
            return

        self.npcShips.remove(ship)

    def getShips(self):
        return list(self.npcShips)

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

        oceanGrid = self.world.oceanGrid
        world = oceanGrid.getParentObj()
        sx, sy = self.air.worldCreator.oceanAreaManager.getRandomOceanPos(world.getUniqueId())
        zoneId = oceanGrid.getZoneFromXYZ((sx, sy, 0))

        oceanGrid.generateChildWithRequired(ship, zoneId)
        ship.setPos(oceanGrid, sx, sy, 0)
        oceanGrid.addObjectToOceanGrid(ship)

        ship.sendCurrentPosition()
        ship.startPosHprBroadcast()
        ship.b_setGameState('PathFollow', 0)

    def _upkeepNPCShipPop(self, task):
        task.delayTime = random.random() * 2.0 + NPCSHIP_POP_UPKEEP_DELAY

        # upkeep the NPC ship population:
        activeNPCShips = list(self.npcShips)
        for _ in range(NPCSHIP_POP_MAX - len(activeNPCShips)):
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

        return task.again

    def startSpawnEnemyShips(self, world):
        self.world = world
        assert(world is not None)

        if self.NPCShipUpkeepTask is not None:
            taskMgr.remove(self.NPCShipUpkeepTask)

        # TODO: eventually use unique task names because we will want to setup
        # a ship spawning task for different worlds too, but this is fine for now.
        self.NPCShipUpkeepTask = taskMgr.add(self._upkeepNPCShipPop, 'ShipManagerAI-NPCShipUpkeepPop')
