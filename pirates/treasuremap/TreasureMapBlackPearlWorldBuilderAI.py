"""
TreasureMapBlackPearlWorldBuilderAI - World Builder Helper for the Black Pearl Treasure Map Instance

This is a helper class (NOT a replacement builder) that creates Black Pearl-specific
objects on an existing DistributedIslandAI. It works alongside the normal world loading
process and is called by TreasureMapBlackPearlAI after the island is created.

Objects created:
- Forts (Simple Fort structures with cannons)
- Fort cannons
- Cutscene origin nodes data
- Pier data
"""

from direct.showbase.DirectObject import DirectObject
from direct.directnotify.DirectNotifyGlobal import directNotify

from pirates.world.DistributedFortAI import DistributedFortAI
from pirates.battle.DistributedFortCannonAI import DistributedFortCannonAI
from pirates.treasuremap import TreasureMapBlackPearlGlobals


class TreasureMapBlackPearlWorldBuilderAI(DirectObject):
    """
    Helper class for creating Black Pearl-specific objects on an island.
    
    This is NOT a replacement for IslandAreaBuilderAI - it's a helper that
    creates additional objects (forts, cannons) that are specific to the
    Black Pearl treasure map instance.
    
    Usage:
        builder = TreasureMapBlackPearlWorldBuilderAI(air, island, instance)
        builder.buildFromWorldData(islandData)
    """
    notify = directNotify.newCategory('TreasureMapBlackPearlWorldBuilderAI')

    def __init__(self, air, island, treasureMapInstance=None):
        DirectObject.__init__(self)
        
        self.air = air
        self.island = island  # The DistributedIslandAI to build on
        self.treasureMapInstance = treasureMapInstance

        # Configuration flags for what to build
        self.wantForts = config.GetBool('want-blackpearl-forts', True)
        self.wantFortCannons = config.GetBool('want-blackpearl-cannons', True)

        # Track created objects
        self.forts = {}  # uid -> DistributedFortAI
        self.fortCannons = {}  # uid -> list of DistributedFortCannonAI
        self.cutsceneNodes = {}  # uid -> node data
        self.piers = {}  # uid -> pier data

    def setTreasureMapInstance(self, instance):
        """Set the treasure map instance this builder is working for"""
        self.treasureMapInstance = instance

    def buildFromWorldData(self, objectData=None):
        """
        Build all Black Pearl-specific objects from world data.
        
        If objectData is not provided, it will be loaded from the world files.
        """
        if objectData is None:
            objectData = self._loadIslandWorldData()
        
        if not objectData:
            self.notify.warning('No object data available for Black Pearl island')
            return
        
        # Process all objects in the island data
        objects = objectData.get('Objects', {})
        self._processObjects(objects, self.island, objectData.get('Type', ''))
        
        self.notify.info('Built %d forts with %d total cannons' % (
            len(self.forts), sum(len(c) for c in self.fortCannons.values())))

    def _loadIslandWorldData(self):
        """Load the island world data from the world creator"""
        islandUid = TreasureMapBlackPearlGlobals.BLACKPEARL_ISLAND_UID
        
        # Try to get the data from the world creator's file cache
        islandData = self.air.worldCreator.getObjectDataByUid(islandUid)
        if islandData:
            return islandData
        
        # Fall back to loading the file directly
        try:
            from pirates.leveleditor.worldData import BlackpearlIsland
            return BlackpearlIsland.objectStruct.get('Objects', {}).get(islandUid, {})
        except ImportError:
            self.notify.warning('Could not import BlackpearlIsland world data')
            return None

    def _processObjects(self, objects, parent, parentType):
        """Recursively process objects from world data"""
        for objKey, objData in objects.items():
            objType = objData.get('Type', '')
            
            if objType == 'Simple Fort' and self.wantForts:
                self._createSimpleFort(objKey, objData)
            elif objType == 'Cutscene Origin Node':
                self._registerCutsceneNode(objKey, objData)
            elif objType == 'Pier':
                self._registerPier(objKey, objData)
            
            # Recursively process child objects (but NOT cannon children of forts,
            # those are handled in _createSimpleFort)
            childObjects = objData.get('Objects', {})
            if childObjects and objType != 'Simple Fort':
                self._processObjects(childObjects, parent, objType)

    # =========================================================================
    # Fort Creation
    # =========================================================================

    def _createSimpleFort(self, objKey, objectData):
        """
        Create a Simple Fort (used as drawbridge/barricade in Black Pearl quest).
        """
        if not objectData.get('CreateObject', False):
            self.notify.debug('Skipping fort %s - CreateObject is False' % objKey)
            return None

        if not self.island:
            self.notify.warning('Cannot create fort %s - no island set' % objKey)
            return None

        fort = DistributedFortAI(self.air)
        fort.setObjKey(objKey)

        # Get position and rotation from object data
        pos = objectData.get('Pos', (0, 0, 0))
        hpr = objectData.get('Hpr', (0, 0, 0))

        # Determine fort level based on model
        visual = objectData.get('Visual', {})
        model = visual.get('Model', '')
        if 'fort_medium' in model:
            fort.setFortLevel(2)
            fort.setMaxHp(TreasureMapBlackPearlGlobals.FORT_HP_BY_LEVEL.get(2, 7500))
            fort.setHp(fort.getMaxHp())
        elif 'fort_large' in model:
            fort.setFortLevel(3)
            fort.setMaxHp(TreasureMapBlackPearlGlobals.FORT_HP_BY_LEVEL.get(3, 10000))
            fort.setHp(fort.getMaxHp())
        else:
            fort.setFortLevel(1)
            fort.setMaxHp(TreasureMapBlackPearlGlobals.FORT_HP_BY_LEVEL.get(1, 5000))
            fort.setHp(fort.getMaxHp())

        # Set reference to the treasure map instance
        if self.treasureMapInstance:
            fort.setTreasureMapInstance(self.treasureMapInstance)

        # Generate the fort as a child of the island
        zoneId = self.island.getZoneFromXYZ(pos)
        self.island.generateChildWithRequired(fort, zoneId)
        fort.setPos(self.island, pos[0], pos[1], pos[2])
        fort.setHpr(hpr[0], hpr[1], hpr[2])

        # Set island ID for the fort
        fort.b_setIslandId(self.island.doId)

        # Store the fort reference
        self.forts[objKey] = fort
        
        # Register with UID manager
        self.air.uidMgr.addUid(objKey, fort.doId)

        hp, maxHp = fort.getHp()
        self.notify.info('Created fort %s at %s with HP %d/%d' % (objKey, pos, hp, maxHp))

        # Now process the fort's child objects (cannons)
        if self.wantFortCannons:
            fortObjects = objectData.get('Objects', {})
            if fortObjects:
                self.fortCannons[objKey] = []
                for cannonKey, cannonData in fortObjects.items():
                    if cannonData.get('Type') == 'Cannon':
                        cannon = self._createFortCannon(cannonKey, cannonData, fort)
                        if cannon:
                            self.fortCannons[objKey].append(cannon)

        return fort

    def _createFortCannon(self, objKey, objectData, parentFort):
        """
        Create a cannon that belongs to a fort.
        """
        if not self.island:
            self.notify.warning('Cannot create cannon %s - no island set' % objKey)
            return None

        cannon = DistributedFortCannonAI(self.air)
        cannon.setUniqueId(objKey)

        # Get position - prefer GridPos (absolute) over Pos (relative)
        pos = objectData.get('Pos', (0, 0, 0))
        gridPos = objectData.get('GridPos', None)
        hpr = objectData.get('Hpr', (0, 0, 0))

        actualPos = gridPos if gridPos else pos

        # Set the island ID and fort ID
        cannon.setIslandId(self.island.doId)
        cannon.setFortId(parentFort.doId)

        # Generate the cannon as child of the island
        zoneId = self.island.getZoneFromXYZ(actualPos)
        self.island.generateChildWithRequired(cannon, zoneId)
        cannon.setPos(self.island, actualPos[0], actualPos[1], actualPos[2])
        cannon.setHpr(hpr[0], hpr[1], hpr[2])

        # Register with UID manager
        self.air.uidMgr.addUid(objKey, cannon.doId)

        self.notify.debug('Created cannon %s at %s for fort %s' % (
            objKey, actualPos, parentFort.getObjKey()))

        return cannon

    # =========================================================================
    # Data Registration (non-distributed objects)
    # =========================================================================

    def _registerCutsceneNode(self, objKey, objectData):
        """Register a cutscene origin node (client-side only, no distributed object)"""
        self.cutsceneNodes[objKey] = {
            'cutsceneId': objectData.get('CutsceneId', ''),
            'pos': objectData.get('Pos', (0, 0, 0)),
            'hpr': objectData.get('Hpr', (0, 0, 0))
        }
        self.notify.debug('Registered cutscene node %s' % objKey)

    def _registerPier(self, objKey, objectData):
        """Register pier data (client-side only, no distributed object)"""
        self.piers[objKey] = {
            'pos': objectData.get('Pos', (0, 0, 0)),
            'hpr': objectData.get('Hpr', (0, 0, 0)),
            'model': objectData.get('Visual', {}).get('Model', '')
        }
        self.notify.debug('Registered pier %s' % objKey)

    # =========================================================================
    # Accessor Methods
    # =========================================================================

    def getForts(self):
        """Get all forts created by this builder"""
        return self.forts

    def getFort(self, uid):
        """Get a specific fort by UID"""
        return self.forts.get(uid)

    def getFortCannons(self, fortUid=None):
        """Get cannons for a specific fort or all cannons"""
        if fortUid:
            return self.fortCannons.get(fortUid, [])
        
        allCannons = []
        for cannons in self.fortCannons.values():
            allCannons.extend(cannons)
        return allCannons

    def getCutsceneNodes(self):
        """Get all cutscene origin nodes"""
        return self.cutsceneNodes

    def getPiers(self):
        """Get all pier data"""
        return self.piers

    def getBarricadeForts(self):
        """
        Get the forts that form barricades/drawbridges.
        Returns a dict mapping barricade ID to tuple of fort objects.
        """
        barricades = {}
        for barricadeId, (fortUid1, fortUid2) in TreasureMapBlackPearlGlobals.FortPairsDict.items():
            fort1 = self.forts.get(fortUid1)
            fort2 = self.forts.get(fortUid2)
            if fort1 or fort2:
                barricades[barricadeId] = (fort1, fort2)
        return barricades

    # =========================================================================
    # Cleanup
    # =========================================================================

    def cleanup(self):
        """Clean up all objects created by this builder"""
        # Clean up cannons first (they're children of the island, not forts)
        for cannons in self.fortCannons.values():
            for cannon in cannons:
                if cannon and cannon.doId in self.air.doId2do:
                    self.air.uidMgr.removeUid(cannon.getUniqueId())
                    cannon.requestDelete()
        self.fortCannons.clear()

        # Clean up forts
        for uid, fort in self.forts.items():
            if fort and fort.doId in self.air.doId2do:
                self.air.uidMgr.removeUid(uid)
                fort.requestDelete()
        self.forts.clear()

        # Clear data caches
        self.cutsceneNodes.clear()
        self.piers.clear()

        self.notify.info('TreasureMapBlackPearlWorldBuilderAI cleanup complete')
