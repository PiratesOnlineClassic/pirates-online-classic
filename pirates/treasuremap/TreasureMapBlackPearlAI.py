from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
from direct.task import Task

from pirates.treasuremap.DistributedTreasureMapInstanceAI import DistributedTreasureMapInstanceAI
from pirates.treasuremap import TreasureMapBlackPearlGlobals
from pirates.treasuremap.TreasureMapBlackPearlWorldBuilderAI import TreasureMapBlackPearlWorldBuilderAI
from pirates.ship import ShipGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.pirate import AvatarTypes
from pirates.battle import EnemyGlobals


class TreasureMapBlackPearlAI(DistributedTreasureMapInstanceAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TreasureMapBlackPearlAI')
    notify.setInfo(True)

    # Ship spawn positions
    BLACK_PEARL_SPAWN_POS = (-350, -3800, 0)
    BLACK_PEARL_SPAWN_HPR = (180, 0, 0)
    GOLIATH_SPAWN_POS = (1200, -5500, 0)
    GOLIATH_SPAWN_HPR = (200, 0, 0)

    # Attack ship spawn positions
    ATTACK_SHIP_POSITIONS = [
        ((-1400, -6100, 0), (45, 0, 0)),
        ((-600, -6500, 0), (30, 0, 0)),
        ((600, -6200, 0), (315, 0, 0)),
        ((1400, -5800, 0), (290, 0, 0)),
    ]

    # Navy guard positions on the Black Pearl deck (relative to ship)
    # These are positioned around the main deck for combat encounters
    NAVY_GUARD_POSITIONS = [
        # Main deck - front
        ((-15, 30, 8), (180, 0, 0)),
        ((15, 30, 8), (180, 0, 0)),
        # Main deck - middle
        ((-20, 0, 8), (90, 0, 0)),
        ((20, 0, 8), (270, 0, 0)),
        ((0, 5, 8), (0, 0, 0)),
        # Main deck - rear
        ((-15, -25, 8), (0, 0, 0)),
        ((15, -25, 8), (0, 0, 0)),
        # Near steering wheel
        ((0, -40, 12), (180, 0, 0)),
        ((-8, -35, 12), (135, 0, 0)),
        ((8, -35, 12), (225, 0, 0)),
    ]

    # Number of guards to spawn
    NUM_NAVY_GUARDS = 10

    # Navy guard avatar types to use (mix of soldiers and marksmen)
    NAVY_GUARD_TYPES = [
        AvatarTypes.Veteran,       # Level 30+ marksman
        AvatarTypes.Officer,       # Level 40+ marksman
        AvatarTypes.RoyalGuard,    # Level 30+ soldier
        AvatarTypes.MasterSwordsman,  # Level 40+ soldier
    ]

    # Stage timing constants
    CUTSCENE_WAIT_TIME = 60.0  # Max time to wait for cutscene sync
    STAGE_TWO_DELAY = 5.0  # Delay before moving to stage two

    def __init__(self, air):
        DistributedTreasureMapInstanceAI.__init__(self, air)

        self.fileName = 'BlackpearlWorld'
        self.type = PiratesGlobals.INSTANCE_TM

        # Ship references
        self.blackPearlId = 0
        self.blackPearl = None
        self.goliathId = 0
        self.goliath = None
        self.attackShipIds = []
        self.attackShips = []

        # Navy guard references
        self.navyGuards = []
        self.navyGuardsKilled = 0

        # Fort references
        self.forts = {}
        self.barricadeStates = {}  # barricadeId -> destroyed
        
        # World builder helper (created after island loads)
        self.worldBuilder = None

        # Quest state
        self.cutsceneEndedCount = 0
        self.shipCaptured = False
        self.npcsKilled = False
        self.attackShipsSunk = 0
        self.barricadesDestroyed = []

        # Barrier sync for multi-player
        self.barrierCallbacks = {}

        # Ready state for teleporting
        self.isReady = False
        self.pendingTeleportCallbacks = []

        # Interest tracking for Black Pearl visibility
        # Maps avatarId -> interestId for cleanup
        self.blackPearlInterests = {}
        self.nextInterestId = 5000  # Start with a high number to avoid conflicts

    def announceGenerate(self):
        DistributedTreasureMapInstanceAI.announceGenerate(self)
        self.notify.info('TreasureMapBlackPearlAI generated with doId %d' % self.doId)

        # Schedule ship and world setup after instance is fully loaded
        taskMgr.doMethodLater(2.0, self._setupInstance, self.uniqueName('setupInstance'))

    def _setupInstance(self, task):
        """Set up the Black Pearl instance after world loading"""
        self.notify.info('Setting up Black Pearl instance...')

        # Get the Black Pearl island
        island = self._getBlackPearlIsland()
        if island:
            # Create the world builder helper to build forts and cannons
            self.worldBuilder = TreasureMapBlackPearlWorldBuilderAI(self.air, island, self)
            self.worldBuilder.buildFromWorldData()
            
            # Register forts from the builder
            self._registerForts()
        else:
            self.notify.warning('Could not find Black Pearl island - skipping fort creation')

        # Create the Black Pearl ship
        self._createBlackPearl()

        # Add Black Pearl interest for any participants who joined before ship was created
        #self._addBlackPearlInterestForAllParticipants()

        # Spawn Navy guards on the Black Pearl
        self._spawnNavyGuards()

        # Create the Goliath ship (enemy flagship)
        self._createGoliath()

        # Create attack ships
        self._createAttackShips()

        # Initialize barricade states
        for barricadeId in range(5):
            self.barricadeStates[barricadeId] = False

        # Move to initial state
        self.b_setState('WaitClientsReady')

        # Mark instance as ready and process pending teleport callbacks
        self.isReady = True
        self.notify.info('Black Pearl instance is now ready')
        for callback in self.pendingTeleportCallbacks:
            callback()
        self.pendingTeleportCallbacks = []

        return Task.done

    def delete(self):
        """Clean up the instance"""
        taskMgr.remove(self.uniqueName('setupInstance'))
        taskMgr.remove(self.uniqueName('cutsceneTimeout'))
        taskMgr.remove(self.uniqueName('stageTwoDelay'))
        taskMgr.remove(self.uniqueName('stageFourCutscene'))
        taskMgr.remove(self.uniqueName('checkVictory'))

        # Clean up Navy guards
        for guard in self.navyGuards:
            if guard:
                guard.requestDelete()
        self.navyGuards = []

        # Clean up world builder (forts and cannons)
        if self.worldBuilder:
            self.worldBuilder.cleanup()
            self.worldBuilder = None

        # Clean up ships
        if self.blackPearl:
            self.blackPearl.requestDelete()
            self.blackPearl = None

        if self.goliath:
            self.goliath.requestDelete()
            self.goliath = None

        for ship in self.attackShips:
            if ship:
                ship.requestDelete()
        self.attackShips = []

        DistributedTreasureMapInstanceAI.delete(self)

    # =========================================================================
    # Interest Management - Ensure clients see the Black Pearl
    # =========================================================================

    def addParticipant(self, avatarId):
        """Override to add Black Pearl interest when avatar joins"""
        DistributedTreasureMapInstanceAI.addParticipant(self, avatarId)

        # Add interest to the Black Pearl ship zone for this avatar
        #if self.blackPearl and self.oceanGrid:
        #    self._addBlackPearlInterest(avatarId)

    def removeParticipant(self, avatarId):
        """Override to remove Black Pearl interest when avatar leaves"""
        # Remove interest first
        #self._removeBlackPearlInterest(avatarId)

        DistributedTreasureMapInstanceAI.removeParticipant(self, avatarId)

    def _addBlackPearlInterest(self, avatarId):
        """Add interest to the Black Pearl zone for an avatar so they always see the ship"""
        if not self.blackPearl or not self.oceanGrid:
            self.notify.warning('Cannot add Black Pearl interest: ship or oceanGrid not available')
            return

        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.notify.warning('Cannot add Black Pearl interest: avatar %d not found' % avatarId)
            return

        # Get the zone where the Black Pearl is located
        shipZoneId = self.blackPearl.zoneId

        # Generate a unique interest ID for this avatar
        interestId = self.nextInterestId
        self.nextInterestId += 1

        # Get the client channel for this avatar
        clientChannel = avatar.GetPuppetConnectionChannel(avatarId)

        # Add interest to the ocean grid's zone where the Black Pearl is
        self.air.clientAddInterest(clientChannel, interestId, self.oceanGrid.doId, shipZoneId)

        # Store the interest ID for cleanup
        self.blackPearlInterests[avatarId] = interestId

        self.notify.info('Added Black Pearl interest (id=%d, zone=%d) for avatar %d' % (
            interestId, shipZoneId, avatarId))

    def _removeBlackPearlInterest(self, avatarId):
        """Remove Black Pearl interest for an avatar"""
        interestId = self.blackPearlInterests.pop(avatarId, None)
        if interestId is None:
            return

        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return

        clientChannel = avatar.GetPuppetConnectionChannel(avatarId)
        self.air.clientRemoveInterest(clientChannel, interestId)

        self.notify.info('Removed Black Pearl interest (id=%d) for avatar %d' % (interestId, avatarId))

    def _addBlackPearlInterestForAllParticipants(self):
        """Add Black Pearl interest for all current participants"""
        for avatarId in self.participants:
            if avatarId not in self.blackPearlInterests:
                self._addBlackPearlInterest(avatarId)

    # =========================================================================
    # Ship Creation
    # =========================================================================

    def _createBlackPearl(self):
        """Create the Black Pearl ship"""
        from pirates.ship.NPCShipAI import NPCShipAI

        self.notify.info('Creating Black Pearl ship...')
        self.notify.info('self.air = %s' % self.air)
        self.notify.info('self.oceanGrid = %s' % self.oceanGrid)

        try:
            # Use NPCShipAI for now since BlackPearlShipAI may have issues
            self.blackPearl = NPCShipAI(self.air)
        except Exception as e:
            self.notify.error('Failed to create Black Pearl ship: %s' % e)
            return

        self.notify.info('Black Pearl ship created, setting properties...')
        self.blackPearl.setBaseTeam(ShipGlobals.PLAYER_TEAM)
        self.blackPearl.setLevel(50)
        self.blackPearl.setShipClass(ShipGlobals.BLACK_PEARL)
        self.blackPearl.setName('Black Pearl')
        self.blackPearl.setNPCship(1)
        self.blackPearl.setIsBoardable(1)
        self.blackPearl.setIsFlagship(1)

        # Ship HP/SP from config
        shipConfig = ShipGlobals.getShipConfig(ShipGlobals.BLACK_PEARL)
        hullConfig = ShipGlobals.getHullConfig(ShipGlobals.BLACK_PEARL)

        if shipConfig is None or hullConfig is None:
            self.notify.error('Failed to get ship config for BLACK_PEARL')
            return

        maxHp = shipConfig.get('setMaxHp', [10000])[0]
        self.blackPearl.setMaxHp(maxHp)
        self.blackPearl.setHp(maxHp)
        self.blackPearl.setMaxSp(hullConfig.get('setMaxSp', [5000])[0])
        self.blackPearl.setSp(hullConfig.get('setSp', [5000])[0])
        self.blackPearl.setHullCondition(1 << 7)

        # Position the ship
        x, y, z = self.BLACK_PEARL_SPAWN_POS
        h, p, r = self.BLACK_PEARL_SPAWN_HPR

        # Generate in the ocean grid using generateChildWithRequired (like ShipManagerAI does)
        if self.oceanGrid:
            zoneId = self.oceanGrid.getZoneFromXYZ((x, y, 0))
            self.notify.info('Generating Black Pearl in zone %d with parent %d' % (zoneId, self.oceanGrid.doId))
            self.oceanGrid.generateChildWithRequired(self.blackPearl, zoneId)
            self.blackPearl.setPos(self.oceanGrid, x, y, z)
            self.blackPearl.setHpr(h, p, r)
            self.oceanGrid.addObjectToOceanGrid(self.blackPearl)
            self.blackPearl.sendCurrentPosition()

            # Set game state to Adrift so players can board it
            # (default is 'Off' which prevents teleporting to the ship)
            self.blackPearl.b_setGameState('Adrift', 0)
        else:
            self.notify.error('No oceanGrid available to generate Black Pearl')
            return

        self.blackPearlId = self.blackPearl.doId
        self.notify.info('Black Pearl created with doId %d' % self.blackPearlId)

    def _createGoliath(self):
        """Create the Goliath enemy ship"""
        from pirates.ship.NPCShipAI import NPCShipAI

        self.notify.info('Creating Goliath ship...')

        self.goliath = NPCShipAI(self.air)
        self.goliath.setBaseTeam(ShipGlobals.UNDEAD_TEAM)
        self.goliath.setLevel(50)
        self.goliath.setShipClass(ShipGlobals.GOLIATH)
        self.goliath.setName('Goliath')
        self.goliath.setNPCship(1)
        self.goliath.setIsBoardable(0)
        self.goliath.setIsFlagship(1)

        # Ship HP/SP from config
        shipConfig = ShipGlobals.getShipConfig(ShipGlobals.GOLIATH)
        hullConfig = ShipGlobals.getHullConfig(ShipGlobals.GOLIATH)

        if shipConfig is None or hullConfig is None:
            self.notify.error('Failed to get ship config for GOLIATH')
            return

        maxHp = shipConfig.get('setMaxHp', [15000])[0]
        self.goliath.setMaxHp(maxHp)
        self.goliath.setHp(maxHp)
        self.goliath.setMaxSp(hullConfig.get('setMaxSp', [7500])[0])
        self.goliath.setSp(hullConfig.get('setSp', [7500])[0])
        self.goliath.setHullCondition(1 << 7)

        # Position the ship
        x, y, z = self.GOLIATH_SPAWN_POS
        h, p, r = self.GOLIATH_SPAWN_HPR

        # Generate in the ocean grid using generateChildWithRequired
        if self.oceanGrid:
            zoneId = self.oceanGrid.getZoneFromXYZ((x, y, 0))
            self.notify.info('Generating Goliath in zone %d' % zoneId)
            self.oceanGrid.generateChildWithRequired(self.goliath, zoneId)
            self.goliath.setPos(self.oceanGrid, x, y, z)
            self.goliath.setHpr(h, p, r)
            self.oceanGrid.addObjectToOceanGrid(self.goliath)
            self.goliath.sendCurrentPosition()

            # Set game state to AISteering for enemy ship
            self.goliath.b_setGameState('AISteering', 0)
        else:
            self.notify.error('No oceanGrid available to generate Goliath')
            return

        self.goliathId = self.goliath.doId
        self.notify.info('Goliath created with doId %d' % self.goliathId)

    def _createAttackShips(self):
        """Create the Navy attack ships"""
        from pirates.ship.NPCShipAI import NPCShipAI

        self.notify.info('Creating attack ships...')

        attackShipClasses = [
            ShipGlobals.NPC_WARSHIPL1,
            ShipGlobals.NPC_WARSHIPL2,
            ShipGlobals.NPC_WARSHIPL2,
            ShipGlobals.NPC_WARSHIPL3,
        ]

        for i, (pos, hpr) in enumerate(self.ATTACK_SHIP_POSITIONS):
            shipClass = attackShipClasses[i] if i < len(attackShipClasses) else ShipGlobals.WARSHIP_L2

            ship = NPCShipAI(self.air)
            ship.setBaseTeam(ShipGlobals.NAVY_TEAM)
            ship.setLevel(30 + i * 5)
            ship.setShipClass(shipClass)
            ship.setName('HMS Interceptor %d' % (i + 1))
            ship.setNPCship(1)
            ship.setIsBoardable(0)

            # Ship HP/SP from config
            shipConfig = ShipGlobals.getShipConfig(shipClass)
            hullConfig = ShipGlobals.getHullConfig(shipClass)

            if shipConfig is None or hullConfig is None:
                self.notify.warning('Failed to get ship config for shipClass %d' % shipClass)
                continue

            maxHp = shipConfig.get('setMaxHp', [5000])[0]
            ship.setMaxHp(maxHp)
            ship.setHp(maxHp)
            ship.setMaxSp(hullConfig.get('setMaxSp', [2500])[0])
            ship.setSp(hullConfig.get('setSp', [2500])[0])
            ship.setHullCondition(1 << 7)

            x, y, z = pos
            h, p, r = hpr

            if self.oceanGrid:
                zoneId = self.oceanGrid.getZoneFromXYZ((x, y, 0))
                self.oceanGrid.generateChildWithRequired(ship, zoneId)
                ship.setPos(self.oceanGrid, x, y, z)
                ship.setHpr(h, p, r)
                self.oceanGrid.addObjectToOceanGrid(ship)
                ship.sendCurrentPosition()

                # Set game state to AISteering for enemy ship
                ship.b_setGameState('AISteering', 0)

            self.attackShips.append(ship)
            self.attackShipIds.append(ship.doId)

        self.notify.info('Created %d attack ships' % len(self.attackShips))

    def _spawnNavyGuards(self):
        """Spawn Navy guards on the Black Pearl deck"""
        from pirates.npc.DistributedNPCNavySailorAI import DistributedNPCNavySailorAI
        import random

        if not self.blackPearl:
            self.notify.warning('Cannot spawn Navy guards: Black Pearl not created')
            return

        self.notify.info('Spawning Navy guards on the Black Pearl...')

        for i in range(min(self.NUM_NAVY_GUARDS, len(self.NAVY_GUARD_POSITIONS))):
            pos, hpr = self.NAVY_GUARD_POSITIONS[i]

            # Create the Navy guard NPC
            guard = DistributedNPCNavySailorAI(self.air)

            # Pick a random avatar type from our guard types
            avatarType = random.choice(self.NAVY_GUARD_TYPES)
            guard.setAvatarType(avatarType)

            # Set level based on avatar type (soldiers/marksmen levels)
            level = 30 + (i % 4) * 5  # Levels 30, 35, 40, 45
            guard.setLevel(level)

            # Get HP/MP from EnemyGlobals based on avatar type and level
            npcHp, npcMp = EnemyGlobals.getEnemyStats(avatarType, level)
            guard.setMaxHp(npcHp)
            guard.setHp(npcHp)
            guard.setMaxMojo(npcMp)
            guard.setMojo(npcMp)

            # Set name based on avatar type
            guard.setName(avatarType.getName())

            # Set spawn position
            sx, sy, sz = pos
            guard.setSpawnPos((sx, sy, sz))

            # Set animation and combat state
            guard.setAnimSet('default')
            guard.setStartState('Idle')

            # Set up a dummy spawn node reference to prevent crashes in gameFSM
            # The gameFSM's enterDeath calls spawnNode.processDeath()
            guard.setSpawnNode(self)

            # Generate the guard as a child of the Black Pearl ship
            # This makes the guard move with the ship
            zoneId = self.blackPearl.zoneId
            self.blackPearl.generateChildWithRequired(guard, zoneId)

            # Position relative to the ship
            guard.setPos(self.blackPearl, sx, sy, sz)
            h, p, r = hpr
            guard.setHpr(self.blackPearl, h, p, r)

            # Initialize guard state
            guard.d_setInitZ(sz)
            guard.d_setSpawnIn()
            guard.b_setGameState('Idle')

            # Store reference to this instance for death callback
            guard._blackPearlInstance = self

            self.navyGuards.append(guard)
            self.notify.debug('Spawned Navy guard %d (%s) at %s' % (i, avatarType.getName(), pos))

        self.notify.info('Spawned %d Navy guards on the Black Pearl' % len(self.navyGuards))

    def processDeath(self):
        """
        Called when a Navy guard's gameFSM enters Death state.
        This method is called because we set guard.setSpawnNode(self).
        """
        # We need to track which guard died - check all guards for HP <= 0
        for guard in list(self.navyGuards):
            hp = guard.getHp()
            # getHp returns [hp, quietly] tuple
            if isinstance(hp, list):
                hp = hp[0]
            if hp <= 0:
                self._onNavyGuardKilled(guard)
                break

    def _onNavyGuardKilled(self, guard):
        """Handle a Navy guard being killed"""
        self.navyGuardsKilled += 1
        self.notify.info('Navy guard killed: %d/%d' % (self.navyGuardsKilled, len(self.navyGuards)))

        # Remove the dead guard from our list
        if guard in self.navyGuards:
            self.navyGuards.remove(guard)

        # Check if all guards are killed
        if self.navyGuardsKilled >= self.NUM_NAVY_GUARDS:
            self.notify.info('All Navy guards killed! Ship captured!')
            self.npcsKilled = True
            self.d_handleNPCsKilled()

    def _getBlackPearlIsland(self):
        """Get the Black Pearl island (standard DistributedIslandAI)"""
        # Search by UID for the Black Pearl island
        islandUid = TreasureMapBlackPearlGlobals.BLACKPEARL_ISLAND_UID
        islandDoId = self.air.uidMgr.getDoId(islandUid)
        if islandDoId:
            return self.air.doId2do.get(islandDoId)
        
        return None

    def _registerForts(self):
        """Register forts from the world builder"""
        # Get forts from our world builder helper
        if self.worldBuilder:
            builderForts = self.worldBuilder.getForts()
            for fortUid, fort in builderForts.items():
                self.forts[fortUid] = fort
                self.notify.debug('Registered fort from builder: %s (doId=%d)' % (fortUid, fort.doId))
        else:
            # Fallback to the old method - find forts by UID
            self.notify.info('Using fallback fort registration method')
            for fortPairId, (fortUid1, fortUid2) in TreasureMapBlackPearlGlobals.FortPairsDict.items():
                fortDoId1 = self.air.uidMgr.getDoId(fortUid1)
                fortDoId2 = self.air.uidMgr.getDoId(fortUid2)

                if fortDoId1:
                    fort1 = self.air.doId2do.get(fortDoId1)
                    if fort1:
                        self.forts[fortUid1] = fort1

                if fortDoId2:
                    fort2 = self.air.doId2do.get(fortDoId2)
                    if fort2:
                        self.forts[fortUid2] = fort2

        fortIds = [fort.doId for fort in self.forts.values()]
        self.b_setFortIds(fortIds)
        self.notify.info('Registered %d forts' % len(self.forts))

    # =========================================================================
    # Network Updates
    # =========================================================================

    def setBlackPearlId(self, doId):
        self.blackPearlId = doId

    def d_setBlackPearlId(self, doId):
        self.sendUpdate('setBlackPearlId', [doId])

    def b_setBlackPearlId(self, doId):
        self.setBlackPearlId(doId)
        self.d_setBlackPearlId(doId)

    def getBlackPearlId(self):
        return self.blackPearlId

    def setGoliathId(self, doId):
        self.goliathId = doId

    def d_setGoliathId(self, doId):
        self.sendUpdate('setGoliathId', [doId])

    def b_setGoliathId(self, doId):
        self.setGoliathId(doId)
        self.d_setGoliathId(doId)

    def getGoliathId(self):
        return self.goliathId

    def setAttackShipIds(self, shipIds):
        self.attackShipIds = shipIds

    def d_setAttackShipIds(self, shipIds):
        self.sendUpdate('setAttackShipIds', [shipIds])

    def b_setAttackShipIds(self, shipIds):
        self.setAttackShipIds(shipIds)
        self.d_setAttackShipIds(shipIds)

    def getAttackShipIds(self):
        return self.attackShipIds

    def d_setAllPlayersReady(self, ready):
        self.sendUpdate('setAllPlayersReady', [ready])

    def d_endCutscene(self):
        self.sendUpdate('endCutscene', [])

    def d_displayCutsceneMessage(self, doId, messageNum):
        self.sendUpdate('displayCutsceneMessage', [doId, messageNum])

    def d_fireShipCannonsAtTarget(self, shipId, targetId):
        self.sendUpdate('fireShipCannonsAtTarget', [shipId, targetId])

    def d_destroyBarricade(self, barricadeId):
        self.sendUpdate('destroyBarricade', [barricadeId])

    def d_barricadeWarning(self, barricadeId):
        self.sendUpdate('barricadeWarning', [barricadeId])

    def d_disableBarricadeCollisions(self, barricadeId):
        self.sendUpdate('disableBarricadeCollisions', [barricadeId])

    def d_enableBarricadeCollisions(self, barricadeId):
        self.sendUpdate('enableBarricadeCollisions', [barricadeId])

    def d_startStageFourCutscene(self):
        self.sendUpdate('startStageFourCutscene', [])

    def d_stopStageFourCutscene(self):
        self.sendUpdate('stopStageFourCutscene', [])

    def d_handleAttackShipSunk(self):
        self.sendUpdate('handleAttackShipSunk', [])

    def d_handleNPCsKilled(self):
        self.sendUpdate('handleNPCsKilled', [])

    # =========================================================================
    # Client Requests
    # =========================================================================

    def requestShipCapture(self):
        """Client requests ship capture (entered capture zone)"""
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId:
            return

        self.notify.info('Avatar %d triggered ship capture' % avatarId)

        if not self.shipCaptured:
            self.shipCaptured = True
            # Move to stage two after the NPCs are killed
            self._checkStageOneComplete()

    def requestShipAmbush(self):
        """Client requests ship ambush event"""
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId:
            return

        self.notify.info('Avatar %d triggered ship ambush' % avatarId)

    def requestEndCutscene(self):
        """Client requests to end the cutscene (cutscene finished or skipped)"""
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId:
            return

        self.notify.info('Avatar %d finished cutscene' % avatarId)
        self.cutsceneEndedCount += 1

        # Check if all participants have finished
        if self.cutsceneEndedCount >= len(self.participants) or self.cutsceneEndedCount >= 1:
            # All ready, end the cutscene for everyone
            taskMgr.remove(self.uniqueName('cutsceneTimeout'))
            self.d_endCutscene()

    def handleNPCsKilledOnPearl(self):
        """Called when all NPCs on the Black Pearl are killed"""
        if not self.npcsKilled:
            self.npcsKilled = True
            self.d_handleNPCsKilled()
            self._checkStageOneComplete()

    def _checkStageOneComplete(self):
        """Check if stage one is complete"""
        if self.shipCaptured and self.npcsKilled and self.state == 'StageOne':
            # Delay before moving to stage two
            taskMgr.doMethodLater(self.STAGE_TWO_DELAY, self._moveToStageTwo,
                self.uniqueName('stageTwoDelay'))

    def _moveToStageTwo(self, task):
        self.b_setState('StageTwo')
        return Task.done

    def handleAttackShipDestroyed(self, shipDoId):
        """Called when an attack ship is destroyed"""
        self.attackShipsSunk += 1
        self.d_handleAttackShipSunk()
        self.notify.info('Attack ship %d destroyed (%d/%d)' % (
            shipDoId, self.attackShipsSunk, len(self.attackShipIds)))

        # Check if all attack ships are destroyed
        if self.attackShipsSunk >= len(self.attackShipIds):
            self._allAttackShipsDestroyed()

    def _allAttackShipsDestroyed(self):
        """All attack ships have been destroyed"""
        self.notify.info('All attack ships destroyed!')
        if self.state == 'StageTwo':
            self.b_setState('StageThree')

    def handleBarricadeDestroyed(self, barricadeId):
        """Called when a barricade is destroyed"""
        if barricadeId not in self.barricadesDestroyed:
            self.barricadesDestroyed.append(barricadeId)
            self.barricadeStates[barricadeId] = True
            self.d_destroyBarricade(barricadeId)
            self.notify.info('Barricade %d destroyed' % barricadeId)

            # Check if enough barricades are destroyed to proceed
            self._checkBarricadeProgress()

    def _checkBarricadeProgress(self):
        """Check if enough barricades are destroyed to proceed to stage four"""
        # Need barricades 0 or 1 destroyed, and 2 or 3 or 4 destroyed
        pathOneOpen = 0 in self.barricadesDestroyed or 1 in self.barricadesDestroyed
        pathTwoOpen = (2 in self.barricadesDestroyed or
                       3 in self.barricadesDestroyed or
                       4 in self.barricadesDestroyed)

        if pathOneOpen and pathTwoOpen and self.state == 'StageThree':
            self._moveToStageFour()

    def _moveToStageFour(self):
        """Move to stage four - final battle"""
        self.notify.info('Moving to Stage Four - Final Battle!')
        self.d_startStageFourCutscene()
        taskMgr.doMethodLater(20.0, self._startStageFour, self.uniqueName('stageFourCutscene'))

    def _startStageFour(self, task):
        self.d_stopStageFourCutscene()
        self.b_setState('StageFour')
        return Task.done

    def handleGoliathDestroyed(self):
        """Called when the Goliath is destroyed - Victory!"""
        self.notify.info('Goliath destroyed! Victory!')
        if self.state == 'StageFour':
            self.b_setState('Reward')

    def handleBlackPearlDestroyed(self):
        """Called when the Black Pearl is destroyed - Defeat!"""
        self.notify.info('Black Pearl destroyed! Defeat!')
        self.b_setState('NotCompleted')

    # =========================================================================
    # State Enter/Exit
    # =========================================================================

    def enterWaitClientsReady(self):
        DistributedTreasureMapInstanceAI.enterWaitClientsReady(self)

        # Send ship IDs to clients
        self.d_setBlackPearlId(self.blackPearlId)
        self.d_setGoliathId(self.goliathId)
        self.d_setAttackShipIds(self.attackShipIds)

        # Start a timeout to move to stage one even if not all players ready
        taskMgr.doMethodLater(10.0, self._waitClientsReadyTimeout,
            self.uniqueName('waitClientsTimeout'))

    def _waitClientsReadyTimeout(self, task):
        """Timeout waiting for clients, move to stage one anyway"""
        if self.state == 'WaitClientsReady':
            self.notify.info('Wait clients ready timeout, moving to StageOne')
            self.b_setState('StageOne')
        return Task.done

    def exitWaitClientsReady(self):
        taskMgr.remove(self.uniqueName('waitClientsTimeout'))

    def enterStageOne(self):
        """Stage One: Cutscene and board the Black Pearl"""
        DistributedTreasureMapInstanceAI.enterStageOne(self)
        self.notify.info('Entering Stage One - Board the Black Pearl')

        # Start cutscene timeout
        taskMgr.doMethodLater(self.CUTSCENE_WAIT_TIME, self._cutsceneTimeout,
            self.uniqueName('cutsceneTimeout'))

    def _cutsceneTimeout(self, task):
        """Cutscene timeout - force end cutscene for stragglers"""
        self.notify.info('Cutscene timeout, forcing end')
        self.d_endCutscene()
        return Task.done

    def exitStageOne(self):
        taskMgr.remove(self.uniqueName('cutsceneTimeout'))

    def enterStageTwo(self):
        """Stage Two: Fight attack ships"""
        DistributedTreasureMapInstanceAI.enterStageTwo(self)
        self.notify.info('Entering Stage Two - Defeat the attack ships')

    def exitStageTwo(self):
        pass

    def enterStageThree(self):
        """Stage Three: Destroy the barricades/drawbridges"""
        DistributedTreasureMapInstanceAI.enterStageThree(self)
        self.notify.info('Entering Stage Three - Destroy the barricades')

        # Enable barricade collisions
        for barricadeId in [0, 1, 4]:
            self.d_enableBarricadeCollisions(barricadeId)

    def exitStageThree(self):
        pass

    def enterStageFour(self):
        """Stage Four: Final battle with Goliath"""
        DistributedTreasureMapInstanceAI.enterStageFour(self)
        self.notify.info('Entering Stage Four - Destroy the Goliath!')

        # Start checking for victory/defeat
        taskMgr.doMethodLater(5.0, self._checkVictoryCondition,
            self.uniqueName('checkVictory'))

    def _checkVictoryCondition(self, task):
        """Periodically check victory/defeat conditions"""
        # Check if Goliath is destroyed
        if self.goliath and self.goliath.getHp() <= 0:
            self.handleGoliathDestroyed()
            return Task.done

        # Check if Black Pearl is destroyed
        if self.blackPearl and self.blackPearl.getHp() <= 0:
            self.handleBlackPearlDestroyed()
            return Task.done

        return Task.again

    def exitStageFour(self):
        taskMgr.remove(self.uniqueName('checkVictory'))

    def enterReward(self):
        """Victory! Give rewards"""
        DistributedTreasureMapInstanceAI.enterReward(self)
        self.notify.info('Entering Reward state - Victory!')

        # Calculate and distribute rewards
        instanceResults = []
        playerResults = []

        for avatarId in self.participants:
            avatar = self.air.doId2do.get(avatarId)
            if avatar:
                # Award gold, reputation, loot
                playerResults.append([avatarId, 1])  # 1 = success

        self.d_setTMComplete(instanceResults, playerResults)

        # Schedule move to completed
        taskMgr.doMethodLater(30.0, self._moveToCompleted, self.uniqueName('moveToCompleted'))

    def _moveToCompleted(self, task):
        self.b_setState('Completed')
        return Task.done

    def exitReward(self):
        pass

    def enterNotCompleted(self):
        """Defeat - instance failed"""
        DistributedTreasureMapInstanceAI.enterNotCompleted(self)
        self.notify.info('Instance not completed - Defeat!')

        # Schedule move to completed
        taskMgr.doMethodLater(15.0, self._moveToCompleted, self.uniqueName('moveToCompleted'))

    def exitNotCompleted(self):
        pass

    def enterCompleted(self):
        """Instance is completely done"""
        DistributedTreasureMapInstanceAI.enterCompleted(self)
        self.notify.info('Instance completed, cleaning up...')

    def exitCompleted(self):
        pass
