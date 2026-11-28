import random

from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject

from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.ship.PlayerShipAI import PlayerShipAI
from pirates.ship.NPCShipAI import NPCShipAI
from pirates.ship.TutorialShipAI import TutorialShipAI
from pirates.ship.GameFSMShipAI import getIslandAvoidSpheres
from pirates.ship import ShipGlobals
from pirates.ship import FlagshipGlobals
from pirates.world import OceanZone
from pirates.world import WorldGlobals
from pirates.leveleditor import WorldDataGlobals
from pirates.piratesbase.PLocalizerEnglish import *


NPCSHIP_POP_UPKEEP_DELAY = config.GetFloat('npcship-pop-upkeep-delay', 10.0)
NPCSHIP_POP_MAX = config.GetInt('npcship-pop-max', 96)
FLAGSHIP_POP_MAX = config.GetInt('flagship-pop-max', 24)
FLAGSHIP_SPAWN_DELAY = config.GetFloat('flagship-spawn-delay', 120.0)


# Regular NPC ship classes (non-flagship)
REGULAR_NPC_SHIPS = [
    # Navy ships
    ShipGlobals.NAVY_FERRET,
    ShipGlobals.NAVY_GREYHOUND,
    ShipGlobals.NAVY_PREDATOR,
    ShipGlobals.NAVY_BULWARK,
    ShipGlobals.NAVY_VANGUARD,
    ShipGlobals.NAVY_MONARCH,
    ShipGlobals.NAVY_PANTHER,
    ShipGlobals.NAVY_CENTURION,
    ShipGlobals.NAVY_DREADNOUGHT,
    # EITC ships
    ShipGlobals.EITC_SEA_VIPER,
    ShipGlobals.EITC_BLOODHOUND,
    ShipGlobals.EITC_CORSAIR,
    ShipGlobals.EITC_IRONWALL,
    ShipGlobals.EITC_OGRE,
    ShipGlobals.EITC_BEHEMOTH,
    ShipGlobals.EITC_MARAUDER,
    ShipGlobals.EITC_WARLORD,
    ShipGlobals.EITC_JUGGERNAUT,
    # Undead ships (regular skeleton ships)
    ShipGlobals.SKEL_PHANTOM,
    ShipGlobals.SKEL_REVENANT,
    ShipGlobals.SKEL_STORM_REAPER,
    ShipGlobals.SKEL_BLACK_HARBINGER,
    ShipGlobals.SKEL_DEATH_OMEN,
    # French Undead ships
    ShipGlobals.SKEL_SHADOW_CROW_FR,
    ShipGlobals.SKEL_HELLHOUND_FR,
    # Spanish Undead ships  
    ShipGlobals.SKEL_SHADOW_CROW_SP,
    ShipGlobals.SKEL_HELLHOUND_SP,
]


class ShipManagerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipManagerAI')
    notify.setInfo(True)

    def __init__(self, air):
        self.air = air
        self.world = None

        self.playerShips = set()
        self.npcShips = set()
        self.flagships = set()  # Track flagships separately

        self.NPCShipUpkeepTask = None
        self.FlagshipUpkeepTask = None

        # the world's ship spawn nodes, and the ship each one has out at sea:
        self.shipSpawnNodes = None
        self.spawnNodeShips = {}
        self.islandAvoidSpheres = None

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

    def hasActiveShip(self, shipId):
        for ship in self.playerShips:
            if ship.doId == shipId:
                return True

        return False

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

    # =========================================================================
    # Spawn Position Helpers
    # =========================================================================

    def _getGridBounds(self):
        """
        Get the valid ocean grid boundaries for spawning ships.
        Ships must spawn within these bounds to have valid zone IDs.
        
        Returns: (minX, maxX, minY, maxY) tuple
        """
        gridSize = WorldGlobals.OCEAN_GRID_SIZE
        cellWidth = WorldGlobals.OCEAN_CELL_SIZE
        halfSize = (gridSize * cellWidth) / 2.0
        
        # Add a safety margin to keep ships well within bounds
        margin = cellWidth * 2  # 2 cells from edge
        
        return (-halfSize + margin, halfSize - margin, 
                -halfSize + margin, halfSize - margin)

    def _isValidSpawnPosition(self, x, y):
        """
        Check if a position is valid for spawning a ship.
        Must be within the Cartesian grid bounds and clear of the islands.
        """
        minX, maxX, minY, maxY = self._getGridBounds()
        return minX <= x <= maxX and minY <= y <= maxY and self._isClearOfIslands(x, y)

    def _isClearOfIslands(self, x, y):
        if self.islandAvoidSpheres is None:
            if not self.world or not hasattr(self.world, 'builder'):
                return True

            self.islandAvoidSpheres = getIslandAvoidSpheres(self.world)

        for centerX, centerY, radius in self.islandAvoidSpheres:
            if (x - centerX) ** 2 + (y - centerY) ** 2 < radius * radius:
                return False

        return True

    def _clampToGridBounds(self, x, y):
        """Clamp coordinates to be within valid grid bounds."""
        minX, maxX, minY, maxY = self._getGridBounds()
        clampedX = max(minX, min(maxX, x))
        clampedY = max(minY, min(maxY, y))
        return clampedX, clampedY

    def _getValidSpawnPosition(self, oceanGrid, world):
        """
        Get a valid spawn position within the Cartesian grid.
        Tries ocean area manager first, then falls back to random grid position.
        
        Returns: (x, y) tuple of valid coordinates
        """
        maxAttempts = 10
        
        for _ in range(maxAttempts):
            try:
                # Try to get position from ocean area manager
                sx, sy = self.air.worldCreator.oceanAreaManager.getRandomOceanPos(
                    world.getUniqueId())
                
                # Validate it's within grid bounds
                if self._isValidSpawnPosition(sx, sy):
                    return sx, sy
                
                # If outside bounds, clamp it
                sx, sy = self._clampToGridBounds(sx, sy)
                if self._isValidSpawnPosition(sx, sy):
                    return sx, sy
                    
            except Exception as e:
                pass
        
        # Fallback: generate random position within grid bounds, out in open water
        minX, maxX, minY, maxY = self._getGridBounds()
        for _ in range(maxAttempts * 10):
            sx = random.uniform(minX, maxX)
            sy = random.uniform(minY, maxY)
            if self._isClearOfIslands(sx, sy):
                break

        return sx, sy

    def _getIslandPatrolPosition(self, island):
        """
        Get a spawn position near an island for patrol ships.
        Ships will spawn in the outer patrol radius of the island.
        
        Args:
            island: DistributedIslandAI to patrol around
            
        Returns: (x, y) tuple or None if invalid
        """
        if not island:
            return None
        
        try:
            # Island world pose is carried by setIslandTransform, not NodePath setX/setY.
            islandTransform = island.getIslandTransform()
            islandX, islandY = islandTransform[0], islandTransform[1]
            islandH = islandTransform[3] if len(islandTransform) > 3 else 0.0

            # Get island sphere radius (use outer sphere for patrol distance)
            sphereRadii = getattr(island, 'sphereRadii', None)
            if sphereRadii and len(sphereRadii) > 2:
                patrolRadius = sphereRadii[2] + 500  # Just outside outer sphere
            else:
                patrolRadius = 3000  # Default patrol distance

            # Random angle around island in island-local space, then rotate by heading.
            import math
            localAngle = random.uniform(0, 2 * math.pi)
            localX = patrolRadius * math.cos(localAngle)
            localY = patrolRadius * math.sin(localAngle)
            headingRad = math.radians(islandH)
            cosH = math.cos(headingRad)
            sinH = math.sin(headingRad)
            sx = islandX + localX * cosH - localY * sinH
            sy = islandY + localX * sinH + localY * cosH

            # Validate and clamp
            if not self._isValidSpawnPosition(sx, sy):
                sx, sy = self._clampToGridBounds(sx, sy)

            return sx, sy

        except Exception:
            return None

    # =========================================================================
    # Ship Spawning
    # =========================================================================

    def _spawnEnemyShip(self, shipClass, isFlagship=False, spawnNearIsland=None, pos=None, patrolRoute=None):
        """
        Spawn an NPC enemy ship.
        
        Args:
            shipClass: The ship class from ShipGlobals
            isFlagship: Whether this ship should be marked as a flagship
            spawnNearIsland: Optional island to spawn near for patrol ships
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
        
        # Mark as flagship if applicable (use setter before generate, not b_)
        if isFlagship or FlagshipGlobals.isFlagship(shipClass):
            ship.setIsFlagship(1)

        oceanGrid = self.world.oceanGrid
        world = oceanGrid.getParentObj()
        
        # Get valid spawn position
        if pos is not None:
            sx, sy = pos[0], pos[1]
        elif spawnNearIsland:
            pos = self._getIslandPatrolPosition(spawnNearIsland)
            if pos:
                sx, sy = pos
            else:
                sx, sy = self._getValidSpawnPosition(oceanGrid, world)
        else:
            sx, sy = self._getValidSpawnPosition(oceanGrid, world)
        
        # Get zone ID and validate
        zoneId = oceanGrid.getZoneFromXYZ((sx, sy, 0))
        
        # Final validation - if zone is invalid, try center of grid
        if zoneId < WorldGlobals.OCEAN_GRID_STARTING_ZONE:
            self.notify.warning('Invalid zone %d for pos (%f, %f), using grid center' % (
                zoneId, sx, sy))
            sx, sy = 0, 0
            zoneId = oceanGrid.getZoneFromXYZ((sx, sy, 0))

        oceanGrid.generateChildWithRequired(ship, zoneId)
        ship.setPos(oceanGrid, sx, sy, 0)
        oceanGrid.addObjectToOceanGrid(ship)

        ship.sendCurrentPosition()
        ship.startPosHprBroadcast()
        if patrolRoute:
            ship.gameFSM.setPatrolRoute(patrolRoute)

        ship.b_setGameState('Patrol', 0)
        
        # Track flagships separately
        if isFlagship or FlagshipGlobals.isFlagship(shipClass):
            self.addFlagship(ship)
        
        return ship

    def spawnTutorialShip(self, oceanGrid, shipClass, level, hp, pos, h, uniqueId=''):
        """
        Spawns a ship for the new pirate tutorial. These are TutorialShips rather than
        NPCShips, they're never part of the ocean's ship population and the AI never
        engages from Idle, so the ship just sits there and takes it...
        """
        shipConfig = ShipGlobals.getShipConfig(shipClass)
        hullConfig = ShipGlobals.getHullConfig(shipClass)
        if shipConfig is None or hullConfig is None:
            self.notify.warning('Failed to get config for tutorial shipClass %s' % shipClass)
            return None

        ship = TutorialShipAI(self.air)
        ship.setUniqueId(uniqueId)
        ship.setBaseTeam(ShipGlobals.getShipTeam(shipClass))
        ship.setLevel(level)
        ship.setShipClass(shipClass)
        ship.setName(ShipClassNames.get(shipClass, ''))
        ship.setNPCship(1)
        ship.setIsBoardable(0)
        ship.setMaxHp(hp)
        ship.setHp(hp)
        ship.setMaxSp(hullConfig['setMaxSp'][0])
        ship.setSp(hullConfig['setSp'][0])
        ship.setHullCondition(1 << 7)

        zoneId = oceanGrid.getZoneFromXYZ(pos)
        oceanGrid.generateChildWithRequired(ship, zoneId)
        ship.setPos(oceanGrid, *pos)
        ship.setHpr(oceanGrid, h, 0, 0)
        oceanGrid.addObjectToOceanGrid(ship)
        ship.sendCurrentPosition()
        ship.startPosHprBroadcast()
        ship.b_setGameState('Idle', 0)
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
            import traceback
            traceback.print_exc()
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

    def getShipSpawnNodes(self):
        """
        The world's ship spawn nodes. Each one names the ship it spawns, and the world's node
        links join it to the ship movement nodes that make up the route the ship patrols,
        the routes are laid out through open water, clear of the islands.
        """
        if self.shipSpawnNodes is not None:
            return self.shipSpawnNodes

        self.shipSpawnNodes = []
        fileName = self.world.getFileName() if self.world else ''
        fileData = self.air.worldCreator.openFile(fileName + '.py') if fileName else None
        if not fileData:
            return self.shipSpawnNodes

        nodes = {}

        def collectNodes(objects):
            for objKey, objData in list(objects.items()):
                if objData.get('Type') in ('Ship Spawn Node', 'Ship Movement Node'):
                    nodes[objKey] = objData

                collectNodes(objData.get('Objects', {}))

        collectNodes(fileData.get('Objects', {}))

        links = {}
        for link in fileData.get(WorldDataGlobals.LINK_TYPE_AI_NODE, []):
            if link[0] in nodes and link[1] in nodes:
                links.setdefault(link[0], []).append(link[1])
                links.setdefault(link[1], []).append(link[0])

        for objKey, objData in list(nodes.items()):
            if objData['Type'] != 'Ship Spawn Node':
                continue

            shipClass = getattr(ShipGlobals, objData.get('Spawnables', ''), None)
            if shipClass is None:
                self.notify.warning('Ship spawn node %s spawns unknown ship %s!' % (
                    objKey, objData.get('Spawnables')))

                continue

            # follow the movement nodes linked on from the spawn node:
            route = [objData['Pos']]
            visited = {objKey}
            nodeKey = objKey
            while True:
                nextKeys = [key for key in links.get(nodeKey, []) if key not in visited and
                    nodes[key]['Type'] == 'Ship Movement Node']
                if not nextKeys:
                    break

                nodeKey = nextKeys[0]
                visited.add(nodeKey)
                route.append(nodes[nodeKey]['Pos'])

            self.shipSpawnNodes.append({
                'uid': objKey,
                'shipClass': shipClass,
                'flagship': objData.get('Flagship', False),
                'route': [(pos[0], pos[1]) for pos in route]})

        return self.shipSpawnNodes

    def _spawnNodeShip(self, spawnNode):
        ship = self._spawnEnemyShip(spawnNode['shipClass'], isFlagship=spawnNode['flagship'],
            pos=spawnNode['route'][0], patrolRoute=spawnNode['route'])
        if ship:
            self.spawnNodeShips[spawnNode['uid']] = ship

        return ship

    def _upkeepFlagshipPop(self, task):
        """Maintain flagship population."""
        task.delayTime = random.random() * 30.0 + FLAGSHIP_SPAWN_DELAY

        # Clean up deleted flagships
        self.flagships = {s for s in self.flagships if not s.isEmpty()}

        # a world with ship spawn nodes keeps a ship out on each node's route:
        spawnNodes = self.getShipSpawnNodes()
        if spawnNodes:
            for spawnNode in spawnNodes:
                ship = self.spawnNodeShips.get(spawnNode['uid'])
                if ship is None or ship.isEmpty() or ship.isDeleted():
                    self._spawnNodeShip(spawnNode)

            return task.again

        # Spawn new flagships if below max
        for _ in range(FLAGSHIP_POP_MAX - len(self.flagships)):
            self._spawnFlagship()

        return task.again

    def startSpawnEnemyShips(self, world):
        self.world = world
        assert(world is not None)

        self.shipSpawnNodes = None
        self.spawnNodeShips = {}
        self.islandAvoidSpheres = None

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
