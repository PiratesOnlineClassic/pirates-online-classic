import random

from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject

from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.ship.PlayerShipAI import PlayerShipAI
from pirates.ship.NPCShipAI import NPCShipAI
from pirates.ship import ShipGlobals
from pirates.ship import FlagshipGlobals
from pirates.world import OceanZone
from pirates.piratesbase.PLocalizerEnglish import *


NPCSHIP_POP_UPKEEP_DELAY = config.GetFloat('npcship-pop-upkeep-delay', 10.0)
NPCSHIP_POP_MAX = config.GetInt('npcship-pop-max', 128)
FLAGSHIP_POP_MAX = config.GetInt('flagship-pop-max', 6)
FLAGSHIP_SPAWN_DELAY = config.GetFloat('flagship-spawn-delay', 120.0)


# Regular NPC ship classes (non-flagship)
REGULAR_NPC_SHIPS = [
    ShipGlobals.NAVY_FERRET,
    ShipGlobals.NAVY_GREYHOUND,
    ShipGlobals.NAVY_PREDATOR,
    ShipGlobals.NAVY_BULWARK,
    ShipGlobals.NAVY_VANGUARD,
    ShipGlobals.NAVY_MONARCH,
    ShipGlobals.NAVY_PANTHER,
    ShipGlobals.NAVY_CENTURION,
    ShipGlobals.NAVY_DREADNOUGHT,
    ShipGlobals.EITC_SEA_VIPER,
    ShipGlobals.EITC_BLOODHOUND,
    ShipGlobals.EITC_CORSAIR,
    ShipGlobals.EITC_IRONWALL,
    ShipGlobals.EITC_OGRE,
    ShipGlobals.EITC_BEHEMOTH,
    ShipGlobals.EITC_MARAUDER,
    ShipGlobals.EITC_WARLORD,
    ShipGlobals.EITC_JUGGERNAUT,
]


class ShipManagerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipManagerAI')

    def __init__(self, air):
        self.air = air
        self.world = None

        self.playerShips = set()
        self.npcShips = set()
        self.flagships = set()  # Track flagships separately

        self.NPCShipUpkeepTask = None
        self.FlagshipUpkeepTask = None

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

    def getFlagships(self):
        """Get all active flagships."""
        return list(self.flagships)

    def addFlagship(self, ship):
        """Add a flagship to tracking."""
        self.flagships.add(ship)
        self.npcShips.add(ship)

    def removeFlagship(self, ship):
        """Remove a flagship from tracking."""
        self.flagships.discard(ship)
        self.npcShips.discard(ship)

    def _spawnEnemyShip(self, shipClass, isFlagship=False):
        """
        Spawn an NPC enemy ship.
        
        Args:
            shipClass: The ship class from ShipGlobals
            isFlagship: Whether this ship should be marked as a flagship
        """
        # Get ship configuration - use shipClass for all lookups
        shipConfig = ShipGlobals.getShipConfig(shipClass)
        hullConfig = ShipGlobals.getHullConfig(shipClass)
        
        # Validate that we got valid configs
        if shipConfig is None or hullConfig is None:
            self.notify.warning('Failed to get config for shipClass %s' % shipClass)
            return None

        ship = NPCShipAI(self.air)
        ship.setBaseTeam(ShipGlobals.getShipTeam(shipClass))
        ship.setLevel(1)
        ship.setShipClass(shipConfig['setShipClass'][0])
        ship.setName(ShipClassNames.get(shipClass, 'Unknown Ship'))
        ship.setNPCship(1)
        ship.setIsBoardable(1)

        ship.setMaxHp(shipConfig['setMaxHp'][0])
        ship.setHp(shipConfig['setHp'][0])
        ship.setMaxSp(hullConfig['setMaxSp'][0])
        ship.setSp(hullConfig['setSp'][0])
        ship.setHullCondition(1 << 7)
        
        # Mark as flagship if applicable
        if isFlagship or FlagshipGlobals.isFlagship(shipClass):
            ship.b_setIsFlagship(1)

        oceanGrid = self.world.oceanGrid
        world = oceanGrid.getParentObj()
        sx, sy = self.air.worldCreator.oceanAreaManager.getRandomOceanPos(world.getUniqueId())
        zoneId = oceanGrid.getZoneFromXYZ((sx, sy, 0))

        oceanGrid.generateChildWithRequired(ship, zoneId)
        ship.setPos(oceanGrid, sx, sy, 0)
        oceanGrid.addObjectToOceanGrid(ship)

        ship.sendCurrentPosition()
        ship.startPosHprBroadcast()
        ship.b_setGameState('Patrol', 0)
        
        # Track flagships separately
        if isFlagship or FlagshipGlobals.isFlagship(shipClass):
            self.addFlagship(ship)
        
        return ship

    def _spawnFlagship(self, shipClass=None):
        """
        Spawn a flagship. If shipClass is None, picks a random flagship type.
        Returns the spawned ship or None if spawn failed.
        """
        if not FlagshipGlobals.ALL_FLAGSHIPS:
            self.notify.warning('No flagship classes defined in FlagshipGlobals')
            return None
        
        if shipClass is None:
            shipClass = random.choice(FlagshipGlobals.ALL_FLAGSHIPS)
        
        try:
            ship = self._spawnEnemyShip(shipClass, isFlagship=True)
            
            if ship:
                self.notify.info('Spawned flagship: %s (doId=%d)' % (
                    ShipClassNames.get(shipClass, 'Unknown'), ship.doId))
            else:
                self.notify.warning('Failed to spawn flagship: %s' % 
                    ShipClassNames.get(shipClass, 'Unknown'))
            
            return ship
        except Exception as e:
            self.notify.warning('Exception spawning flagship %s: %s' % (shipClass, e))
            return None

    def _upkeepNPCShipPop(self, task):
        task.delayTime = random.random() * 2.0 + NPCSHIP_POP_UPKEEP_DELAY

        # Clean up deleted ships from tracking
        self.npcShips = {s for s in self.npcShips if not s.isEmpty()}
        self.flagships = {s for s in self.flagships if not s.isEmpty()}

        # upkeep the NPC ship population (excluding flagships):
        regularShipCount = len(self.npcShips) - len(self.flagships)
        for _ in range(NPCSHIP_POP_MAX - regularShipCount):
            self._spawnEnemyShip(random.choice(REGULAR_NPC_SHIPS))

        return task.again

    def _upkeepFlagshipPop(self, task):
        """Maintain flagship population."""
        task.delayTime = random.random() * 30.0 + FLAGSHIP_SPAWN_DELAY

        # Clean up deleted flagships
        self.flagships = {s for s in self.flagships if not s.isEmpty()}

        # Spawn new flagships if below max
        for _ in range(FLAGSHIP_POP_MAX - len(self.flagships)):
            self._spawnFlagship()

        return task.again

    def startSpawnEnemyShips(self, world):
        self.world = world
        assert(world is not None)

        if self.NPCShipUpkeepTask is not None:
            taskMgr.remove(self.NPCShipUpkeepTask)

        if self.FlagshipUpkeepTask is not None:
            taskMgr.remove(self.FlagshipUpkeepTask)

        # Start regular NPC ship spawning
        self.NPCShipUpkeepTask = taskMgr.add(self._upkeepNPCShipPop, 'ShipManagerAI-NPCShipUpkeepPop')
        
        # Start flagship spawning (delayed start to give world time to load)
        self.FlagshipUpkeepTask = taskMgr.doMethodLater(
            30.0,  # Wait 30 seconds before spawning flagships
            self._upkeepFlagshipPop, 
            'ShipManagerAI-FlagshipUpkeepPop')
