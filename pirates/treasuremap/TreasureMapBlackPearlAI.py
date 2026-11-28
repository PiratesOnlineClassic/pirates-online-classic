from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
from direct.task import Task
from panda3d.core import Vec3

from otp.ai import AIInterestHandles
from pirates.treasuremap.DistributedTreasureMapInstanceAI import DistributedTreasureMapInstanceAI
from pirates.treasuremap import TreasureMapBlackPearlGlobals
from pirates.treasuremap.TreasureMapBlackPearlWorldBuilderAI import TreasureMapBlackPearlWorldBuilderAI
from pirates.quest import QuestEvent
from pirates.ship import ShipGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.pirate import AvatarTypes
from pirates.battle import EnemyGlobals


class NavyGuardPost:
    """
    The spot on the Black Pearl's deck a Navy guard stands guard at, the guard's
    spawn node as far as it's gameFSM is concerned (see BattleNPCGameFSMAI)...
    """

    # a guard steps no further than this from it's post to fight the crew, far enough
    # to reach anyone it aggros on the deck without chasing them off of it...
    GuardRadius = 25.0

    def __init__(self, instance, index, pos, hpr):
        self.instance = instance
        self.objKey = 'navyGuardPost-%d' % index
        self.objectData = {
            'Pos': pos,
            'Hpr': hpr,
            'AnimSet': 'default',
            'Start State': 'Idle',
            'Patrol Radius': 1.0,
            'Guard Radius': self.GuardRadius,
        }

    def getSpawnHpr(self):
        return self.objectData['Hpr']

    def processDeath(self):
        self.instance.processDeath()


class TreasureMapBlackPearlAI(DistributedTreasureMapInstanceAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TreasureMapBlackPearlAI')
    notify.setInfo(True)

    # Ship spawn positions
    BLACK_PEARL_SPAWN_POS = TreasureMapBlackPearlGlobals.BLACK_PEARL_SPAWN_POS
    BLACK_PEARL_SPAWN_HPR = TreasureMapBlackPearlGlobals.BLACK_PEARL_SPAWN_HPR
    GOLIATH_SPAWN_POS = TreasureMapBlackPearlGlobals.GOLIATH_WAIT_POS
    GOLIATH_SPAWN_HPR = TreasureMapBlackPearlGlobals.GOLIATH_WAIT_HPR

    # Attack ship spawn positions
    ATTACK_SHIP_POSITIONS = TreasureMapBlackPearlGlobals.ATTACK_SHIP_SPAWNS

    # the attack ships come for the Pearl once the stage two camera move has shown them:
    ATTACK_SHIP_HUNT_DELAY = 6.0
    SEA_CHECK_PERIOD = 1.0

    # Navy guard positions on the Black Pearl deck (relative to ship), the heights are
    # the Pearl's main deck under each guard, it rises toward the bow and stern...
    NAVY_GUARD_POSITIONS = [
        # Main deck - front
        ((-15, 30, 42.3), (180, 0, 0)),
        ((15, 30, 42.3), (180, 0, 0)),
        # Main deck - middle
        ((-20, 0, 42.1), (90, 0, 0)),
        ((20, 0, 42.1), (270, 0, 0)),
        ((0, 5, 43.1), (0, 0, 0)),
        # Main deck - rear
        ((-15, -25, 43.0), (0, 0, 0)),
        ((15, -25, 43.0), (0, 0, 0)),
        # Near the main mast
        ((0, -40, 44.6), (180, 0, 0)),
        ((-8, -35, 44.3), (135, 0, 0)),
        ((8, -35, 44.3), (225, 0, 0)),
    ]

    # Number of guards to spawn
    NUM_NAVY_GUARDS = 10

    # Navy guard avatar types to use, only the common navy (the marksmen) have
    # enemy stats, the client cannot generate the soldier tracks...
    NAVY_GUARD_TYPES = [
        AvatarTypes.Veteran,
        AvatarTypes.Officer,
    ]

    # Stage timing constants
    CUTSCENE_WAIT_TIME = 60.0  # Max time to wait for the clients to load
    CUTSCENE_TIMEOUT = 120.0  # Max time to wait for the crew to watch cutscene 3.1
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
        self.deadNavyGuards = []
        self.navyGuardsKilled = 0

        # Fort references
        self.forts = {}
        self.barricadeStates = {}  # barricadeId -> destroyed
        
        # World builder helper (created after island loads)
        self.worldBuilder = None

        # Quest state
        self.cutsceneEndedAvatars = set()
        self.cutsceneFinished = False
        self.shipCaptured = False
        self.npcsKilled = False
        self.attackShipsSunk = 0
        self.sunkAttackShipIds = set()
        self.barricadesDestroyed = []
        self.barricadesWarned = set()
        self.stageFourStarted = False

        # Barrier sync for multi-player
        self.barrierCallbacks = {}
        self.readyBarrier = None
        self.arrivedParticipants = set()

        # Ready state for teleporting
        self.isReady = False
        self.pendingTeleportCallbacks = []

        # Interest tracking for Black Pearl visibility
        # Maps avatarId -> interestId for cleanup
        self.blackPearlInterests = {}

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
            self.notify.error('Could not find Black Pearl island for instance %d' % self.doId)

        # Create the Black Pearl ship
        self._createBlackPearl()

        # Spawn Navy guards on the Black Pearl
        self._spawnNavyGuards()

        # Create the Goliath ship (enemy flagship)
        self._createGoliath()

        # Create attack ships
        self._createAttackShips()
        taskMgr.doMethodLater(1.0, self._refreshBlackPearlInterests,
            self.uniqueName('refreshBlackPearlInterests'))

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
        taskMgr.remove(self.uniqueName('checkAttackShips'))
        taskMgr.remove(self.uniqueName('checkNavyGuards'))
        taskMgr.remove(self.uniqueName('waitClientsTimeout'))
        taskMgr.remove(self.uniqueName('moveToCompleted'))
        taskMgr.remove(self.uniqueName('refreshBlackPearlInterests'))
        taskMgr.remove(self.uniqueName('huntBlackPearl'))
        taskMgr.remove(self.uniqueName('checkStageThree'))
        taskMgr.remove(self.uniqueName('moveShipsOutToSea'))
        self._stopFortsAttacking()
        if self.readyBarrier is not None:
            self.ignoreBarrier(self.readyBarrier)
            self.readyBarrier = None
        for avatarId in self.participants:
            self.ignore('teleportDone-%d' % avatarId)
        self.arrivedParticipants.clear()
        for avatarId in list(self.blackPearlInterests):
            self._removeBlackPearlInterest(avatarId)
        self.pendingTeleportCallbacks = []

        # Clean up Navy guards
        for guard in self.navyGuards + self.deadNavyGuards:
            if guard:
                guard.requestDelete()
        self.navyGuards = []
        self.deadNavyGuards = []

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
        if avatarId not in self.participants:
            self.acceptOnce('teleportDone-%d' % avatarId, self._participantArrived,
                extraArgs=[avatarId])
        DistributedTreasureMapInstanceAI.addParticipant(self, avatarId)

        # Add interest to the Black Pearl ship zone for this avatar
        if self.isReady and avatarId in self.readyAvatars:
            self._addBlackPearlInterest(avatarId)

    def removeParticipant(self, avatarId):
        """Override to remove Black Pearl interest when avatar leaves"""
        self.ignore('teleportDone-%d' % avatarId)
        self.arrivedParticipants.discard(avatarId)
        # Remove interest first
        self._removeBlackPearlInterest(avatarId)
        self.cutsceneEndedAvatars.discard(avatarId)

        DistributedTreasureMapInstanceAI.removeParticipant(self, avatarId)
        self._finishCutsceneIfReady()
        if self.state == 'WaitClientsReady':
            self._waitClientsReadyTimeout(None)

    def _participantArrived(self, avatarId):
        if avatarId not in self.participants:
            return
        self.arrivedParticipants.add(avatarId)
        if self.state == 'WaitClientsReady':
            self._waitClientsReadyTimeout(None)

    def _addBlackPearlInterest(self, avatarId):
        """Keep the encounter ships and forts visible to a participant."""
        if not self.blackPearl or not self.oceanGrid:
            self.notify.warning('Cannot add Black Pearl interest: ship or oceanGrid not available')
            return

        # the client hides the pearl it knows of while cutscene 3.1 plays (see
        # TreasureMapBlackPearl.enterStageOne) and only shows it again in stage two,
        # the crew boards the pearl by teleporting to it once the cutscene ends,
        # which brings the pearl in, so the ships are kept out until then...
        if not self.cutsceneFinished and self.state in ('Off', 'WaitClientsReady', 'StageOne'):
            return

        island = self._getBlackPearlIsland()
        if not island:
            self.notify.warning('Cannot add Black Pearl interest: island not available')
            return
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.notify.warning('Cannot add Black Pearl interest: avatar %d not found' % avatarId)
            return

        clientChannel = avatar.GetPuppetConnectionChannel(avatarId)
        ships = [self.blackPearl, self.goliath] + self.attackShips
        shipZones = tuple(sorted({ship.zoneId for ship in ships if ship and ship.zoneId}))
        fortZones = tuple(sorted({fort.zoneId for fort in self.forts.values() if fort.zoneId}))
        previous = self.blackPearlInterests.get(avatarId)
        if not previous or previous[0] != shipZones:
            self.air.clientAddInterestMultiple(clientChannel,
                AIInterestHandles.PIRATES_TREASUREMAP, self.oceanGrid.doId, shipZones, False)
        if fortZones and (not previous or previous[1] != fortZones):
            self.air.clientAddInterestMultiple(clientChannel,
                AIInterestHandles.PIRATES_TREASUREMAP_FORTS, island.doId, fortZones, False)
        elif not fortZones and previous and previous[1]:
            self.air.clientRemoveInterest(clientChannel,
                AIInterestHandles.PIRATES_TREASUREMAP_FORTS, False)
        self.blackPearlInterests[avatarId] = (shipZones, fortZones)

    def _removeBlackPearlInterest(self, avatarId):
        """Remove Black Pearl interest for an avatar"""
        interests = self.blackPearlInterests.pop(avatarId, None)
        if interests is None:
            return

        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return

        clientChannel = avatar.GetPuppetConnectionChannel(avatarId)
        self.air.clientRemoveInterest(clientChannel, AIInterestHandles.PIRATES_TREASUREMAP, False)
        if interests[1]:
            self.air.clientRemoveInterest(clientChannel, AIInterestHandles.PIRATES_TREASUREMAP_FORTS, False)

    def _addBlackPearlInterestForAllParticipants(self):
        """Add Black Pearl interest for all current participants"""
        for avatarId in list(self.participants):
            if avatarId not in self.air.doId2do:
                self.removeParticipant(avatarId)
                continue
            if avatarId in self.readyAvatars:
                self._addBlackPearlInterest(avatarId)

    def _refreshBlackPearlInterests(self, task):
        self._addBlackPearlInterestForAllParticipants()
        return Task.again

    # =========================================================================
    # Ship Creation
    # =========================================================================

    def _createBlackPearl(self):
        """Create the Black Pearl ship"""
        from pirates.ship.BlackPearlShipAI import BlackPearlShipAI

        self.notify.info('Creating Black Pearl ship...')
        self.notify.info('self.air = %s' % self.air)
        self.notify.info('self.oceanGrid = %s' % self.oceanGrid)

        self.blackPearl = BlackPearlShipAI(self.air)
        self.blackPearl.setQuestInstance(self)

        self.notify.info('Black Pearl ship created, setting properties...')
        self.blackPearl.setBaseTeam(ShipGlobals.PLAYER_TEAM)
        self.blackPearl.setLevel(50)
        self.blackPearl.setShipClass(ShipGlobals.BLACK_PEARL)
        self.blackPearl.setName(PLocalizer.TheBlackPearl)
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
        self.goliath.setBaseTeam(ShipGlobals.getShipTeam(ShipGlobals.GOLIATH))
        self.goliath.setLevel(ShipGlobals.getShipLevel(ShipGlobals.GOLIATH))
        self.goliath.setShipClass(ShipGlobals.GOLIATH)
        self.goliath.setName(PLocalizer.ShipClassNames.get(ShipGlobals.GOLIATH))
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
            self.goliath.startPosHprBroadcast()

            # the Goliath lies in wait out at sea until stage four:
            self.goliath.gameFSM.setSeaLane(TreasureMapBlackPearlGlobals.OPEN_SEA_LANE)
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

        attackShipClasses = TreasureMapBlackPearlGlobals.ATTACK_SHIP_CLASSES

        for i, (pos, hpr) in enumerate(self.ATTACK_SHIP_POSITIONS):
            shipClass = attackShipClasses[i % len(attackShipClasses)]

            ship = NPCShipAI(self.air)
            ship.setBaseTeam(ShipGlobals.getShipTeam(shipClass))
            ship.setLevel(ShipGlobals.getShipLevel(shipClass))
            ship.setShipClass(shipClass)
            ship.setName(PLocalizer.ShipClassNames.get(shipClass, ''))
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
                ship.startPosHprBroadcast()

                # the attack ships wait behind the drawbridges until stage two,
                # the channel keeps them off the island when they come for the Pearl:
                ship.gameFSM.setSeaLane(TreasureMapBlackPearlGlobals.CHANNEL_SEA_LANE)
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
            guard.setTeam(PiratesGlobals.NAVY_TEAM)
            guard.setCollisionMode(PiratesGlobals.COLL_MODE_FLOORS_CL)

            level = EnemyGlobals.getRandomEnemyLevel(avatarType)
            guard.setLevel(level)

            # armed like any other enemy of their type and level (see EnemySpawnNode),
            # the guard draws it's weapon once it goes into battle...
            weapons = list(EnemyGlobals.getEnemyWeapons(avatarType, level).keys())
            guard.setCurrentWeapon(random.choice(weapons), config.GetBool('want-enemy-weapons', False))

            # Get HP/MP from EnemyGlobals based on avatar type and level
            npcHp, npcMp = EnemyGlobals.getEnemyStats(avatarType, level)
            guard.setMaxHp(npcHp)
            guard.setHp(npcHp)
            guard.setMaxMojo(npcMp)
            guard.setMojo(npcMp)

            # Set name based on avatar type
            guard.setName(avatarType.getName())

            # the guards go after the crew boarding the Pearl like any other enemy
            # without an aggro radius of their own (see EnemySpawnNode)...
            aggroMode, aggroRadius = EnemyGlobals.determineAggroInfo(None)
            guard.setAggroMode(aggroMode)
            guard.setAggroRadius(aggroRadius)

            # Set spawn position
            sx, sy, sz = pos
            guard.setSpawnPos((sx, sy, sz))
            guard.setInitZ(sz)

            # Set animation and combat state
            guard.setAnimSet('default')
            guard.setStartState('Idle')

            # the guard's post on deck is it's spawn node, the gameFSM returns
            # the guard to it after a fight and reports it's death through it...
            guard.setSpawnNode(NavyGuardPost(self, i, pos, hpr))

            # Generate the guard as a child of the Black Pearl ship
            # This makes the guard move with the ship
            zoneId = PiratesGlobals.ShipZoneOnDeck
            self.blackPearl.generateChildWithRequired(guard, zoneId)

            # the guard stands on the ship's deck, it's position is relative to the ship
            # just as the client places it under the ship's root (and as the crew's
            # positions on deck are), not a position out on the ocean grid...
            guard.setPos(sx, sy, sz)
            h, p, r = hpr
            guard.setHpr(h, p, r)

            # Initialize guard state
            guard.d_setInitZ(sz)

            # the guard only broadcasts it's position while it moves, the state
            # server holds it's spawn position for the crew boarding the Pearl...
            guard.sendCurrentPosition()
            guard.d_setSpawnIn()
            guard.b_setGameState('Idle')

            # Store reference to this instance for death callback
            guard._blackPearlInstance = self

            self.navyGuards.append(guard)
            self.blackPearl.addNPCOnDeck(guard.doId)
            self.notify.debug('Spawned Navy guard %d (%s) at %s' % (i, avatarType.getName(), pos))

        self.notify.info('Spawned %d Navy guards on the Black Pearl' % len(self.navyGuards))

    def processDeath(self):
        """
        Called when a Navy guard's gameFSM enters Death state.
        This method is called because we set guard.setSpawnNode(self).
        """
        # The death FSM runs before the damage setter stores the new HP.
        taskMgr.doMethodLater(0, self._checkNavyGuards, self.uniqueName('checkNavyGuards'))

    def _checkNavyGuards(self, task):
        for guard in list(self.navyGuards):
            hp = guard.getHp()
            if isinstance(hp, (list, tuple)):
                hp = hp[0]
            if hp <= 0:
                self._onNavyGuardKilled(guard)
        return Task.done

    def _onNavyGuardKilled(self, guard):
        """Handle a Navy guard being killed"""
        if guard not in self.navyGuards:
            return
        self.navyGuardsKilled += 1
        self.notify.info('Navy guard killed: %d/%d' % (self.navyGuardsKilled, len(self.navyGuards)))

        if self.blackPearl:
            self.blackPearl.removeNPCOnDeck(guard.doId)

        # Remove the dead guard from our list
        if guard in self.navyGuards:
            self.navyGuards.remove(guard)
            self.deadNavyGuards.append(guard)

        # Check if all guards are killed
        if self.navyGuardsKilled >= self.NUM_NAVY_GUARDS:
            self.notify.info('All Navy guards killed! Ship captured!')
            self.handleNPCsKilledOnPearl()

    def _getBlackPearlIsland(self):
        """Get the Black Pearl island (standard DistributedIslandAI)"""
        # Search by UID for the Black Pearl island
        islandUid = TreasureMapBlackPearlGlobals.BLACKPEARL_ISLAND_UID
        return self.builder.getObject(uniqueId=islandUid)

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
        if avatarId not in self.participants or self.state != 'StageOne':
            return

        self.notify.info('Avatar %d triggered ship capture' % avatarId)

        if not self.shipCaptured:
            self.shipCaptured = True
            # Move to stage two after the NPCs are killed
            self._checkStageOneComplete()

    def requestShipAmbush(self):
        """Client requests ship ambush event"""
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.participants:
            return

        self.notify.info('Avatar %d triggered ship ambush' % avatarId)

    def requestEndCutscene(self):
        """Client requests to end the cutscene (cutscene finished or skipped)"""
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.participants or self.state != 'StageOne':
            return

        self.notify.info('Avatar %d finished cutscene' % avatarId)
        if avatarId in self.cutsceneEndedAvatars:
            return

        self.cutsceneEndedAvatars.add(avatarId)
        self._finishCutsceneIfReady()
        if self.cutsceneFinished:
            return

        # the crew boards the pearl together, let the avatar know it is waiting
        # on the rest of the crew, and the crew still watching that it is waiting...
        self.d_displayCutsceneMessage(avatarId, 1)
        for watchingId in self.participants:
            if watchingId not in self.cutsceneEndedAvatars:
                self.d_displayCutsceneMessage(watchingId, 0)

    def _finishCutsceneIfReady(self):
        if (not self.cutsceneFinished and self.state == 'StageOne' and self.participants and
                set(self.participants).issubset(self.cutsceneEndedAvatars)):
            taskMgr.remove(self.uniqueName('cutsceneTimeout'))
            self.cutsceneFinished = True
            self.d_endCutscene()
            self._addBlackPearlInterestForAllParticipants()

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
        if shipDoId not in self.attackShipIds or shipDoId in self.sunkAttackShipIds:
            return
        self.sunkAttackShipIds.add(shipDoId)
        self.attackShipsSunk = len(self.sunkAttackShipIds)
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
        # the Pearl still has to sail past the last drawbridge (see _checkStageThree):
        if self.state == 'StageThree':
            self._checkStageThree()

    def isBarricadePassable(self, barricadeId):
        # barricades 2 and 3 are left open, either of the drawbridges either
        # side of the island fort lets the Pearl into the channel:
        if barricadeId in self.barricadesDestroyed:
            return True

        if barricadeId not in TreasureMapBlackPearlGlobals.BlockingBarricades:
            return True

        if barricadeId in TreasureMapBlackPearlGlobals.ChannelEntranceBarricades:
            return any(entranceId in self.barricadesDestroyed
                       for entranceId in TreasureMapBlackPearlGlobals.ChannelEntranceBarricades)

        return False

    def isChannelOpen(self):
        return all(self.isBarricadePassable(barricadeId)
                   for barricadeId in TreasureMapBlackPearlGlobals.BlockingBarricades)

    def _getPearlDistance(self, pos):
        pearlPos = self.blackPearl.getPos(self.oceanGrid)
        return ((pearlPos[0] - pos[0]) ** 2 + (pearlPos[1] - pos[1]) ** 2) ** 0.5

    def _checkStageThree(self, task=None):
        if self.state != 'StageThree' or self.stageFourStarted or not self.blackPearl:
            return Task.done

        # warn the Pearl about drawbridges that are still in it's way:
        for barricadeId in TreasureMapBlackPearlGlobals.BlockingBarricades:
            if barricadeId in self.barricadesWarned or self.isBarricadePassable(barricadeId):
                continue

            if self._getPearlDistance(TreasureMapBlackPearlGlobals.BarricadePositions[barricadeId]) < \
                    TreasureMapBlackPearlGlobals.BARRICADE_WARNING_RADIUS:
                self.barricadesWarned.add(barricadeId)
                self.d_barricadeWarning(barricadeId)

        # with the drawbridges down, the Pearl sailing past the last one makes for the open sea:
        if self.isChannelOpen() and self._getPearlDistance(TreasureMapBlackPearlGlobals.STAGE_FOUR_TRIGGER_POS) < \
                TreasureMapBlackPearlGlobals.STAGE_FOUR_TRIGGER_RADIUS:
            self._moveToStageFour()
            return Task.done

        return Task.again

    def _moveToStageFour(self):
        """Move to stage four - final battle"""
        if self.stageFourStarted:
            return

        self.stageFourStarted = True
        self.notify.info('Moving to Stage Four - Final Battle!')
        taskMgr.remove(self.uniqueName('checkStageThree'))
        self._stopFortsAttacking()
        self.d_startStageFourCutscene()

        # the cutscene sails copies of the Pearl and the Goliath out of the channel,
        # the real ships are moved out to sea while the screen is faded out:
        taskMgr.doMethodLater(TreasureMapBlackPearlGlobals.STAGE_FOUR_MOVE_TIME, self._moveShipsOutToSea,
            self.uniqueName('moveShipsOutToSea'))
        taskMgr.doMethodLater(TreasureMapBlackPearlGlobals.STAGE_FOUR_CUTSCENE_TIME, self._startStageFour,
            self.uniqueName('stageFourCutscene'))

    def _moveShipsOutToSea(self, task=None):
        if self.blackPearl and self.blackPearl.isSailable():
            self.blackPearl.moveTo(TreasureMapBlackPearlGlobals.STAGE_FOUR_PEARL_POS,
                TreasureMapBlackPearlGlobals.STAGE_FOUR_PEARL_HPR)

        if self.goliath and self.goliath.isSailable():
            self.goliath.moveTo(TreasureMapBlackPearlGlobals.STAGE_FOUR_GOLIATH_POS,
                TreasureMapBlackPearlGlobals.STAGE_FOUR_GOLIATH_HPR)

        return Task.done

    def _startStageFour(self, task):
        # the helmsman's client may have still been sending the Pearl's
        # old position when it was moved, make sure it's out at sea:
        self._moveShipsOutToSea()
        self.d_stopStageFourCutscene()
        self.b_setState('StageFour')
        return Task.done

    def _startFortsAttacking(self):
        for fort in self.forts.values():
            if not fort.isDestroyed():
                fort.startAttacking(self.blackPearl)

    def _stopFortsAttacking(self):
        for fort in self.forts.values():
            if hasattr(fort, 'stopAttacking'):
                fort.stopAttacking()

    def _huntBlackPearl(self, ships):
        for ship in ships:
            if ship and not ship.isDeleted() and ship.isSailable() and self.blackPearl:
                ship.gameFSM.hunt(self.blackPearl)

    def _stopHunting(self):
        for ship in [self.goliath] + self.attackShips:
            if ship and not ship.isDeleted() and hasattr(ship, 'gameFSM'):
                ship.gameFSM.stopHunting()

    def handleGoliathDestroyed(self):
        """Called when the Goliath is destroyed - Victory!"""
        self.notify.info('Goliath destroyed! Victory!')
        if self.state == 'StageFour':
            self.b_setState('Reward')

    def handleBlackPearlDestroyed(self):
        """Called when the Black Pearl is destroyed - Defeat!"""
        if self.state not in ('StageOne', 'StageTwo', 'StageThree', 'StageFour'):
            return

        self.notify.info('Black Pearl destroyed! Defeat!')
        taskMgr.remove(self.uniqueName('stageFourCutscene'))
        taskMgr.remove(self.uniqueName('moveShipsOutToSea'))
        self._stopFortsAttacking()
        self._stopHunting()
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
        if self.state != 'WaitClientsReady':
            return Task.done
        if self.readyBarrier is not None:
            return Task.done
        if not self.participants or not set(self.participants).issubset(self.arrivedParticipants):
            return Task.again
        self.readyBarrier = self.beginBarrier(self.uniqueName('allAvatarsReady'),
            list(self.participants), self.CUTSCENE_WAIT_TIME, self._clientsReady)
        return Task.done

    def _clientsReady(self, readyAvatars):
        self.readyBarrier = None
        if self.state != 'WaitClientsReady':
            return
        if not set(readyAvatars).intersection(self.participants):
            self.notify.warning('No Black Pearl participants finished loading')
            taskMgr.doMethodLater(10.0, self._waitClientsReadyTimeout,
                self.uniqueName('waitClientsTimeout'))
            return
        self.readyAvatars = [avatarId for avatarId in readyAvatars
                             if avatarId in self.participants]
        self._addBlackPearlInterestForAllParticipants()
        self.d_setAllPlayersReady(1)
        self.b_setState('StageOne')

    def exitWaitClientsReady(self):
        taskMgr.remove(self.uniqueName('waitClientsTimeout'))
        if self.readyBarrier is not None:
            self.ignoreBarrier(self.readyBarrier)
            self.readyBarrier = None

    def enterStageOne(self):
        """Stage One: Cutscene and board the Black Pearl"""
        DistributedTreasureMapInstanceAI.enterStageOne(self)
        self.notify.info('Entering Stage One - Board the Black Pearl')

        # Start cutscene timeout
        taskMgr.doMethodLater(self.CUTSCENE_TIMEOUT, self._cutsceneTimeout,
            self.uniqueName('cutsceneTimeout'))

    def _cutsceneTimeout(self, task):
        """Cutscene timeout - force end cutscene for stragglers"""
        if not self.cutsceneFinished and self.state == 'StageOne':
            self.notify.info('Cutscene timeout, forcing end')
            self.cutsceneFinished = True
            self.d_endCutscene()
            self._addBlackPearlInterestForAllParticipants()
        return Task.done

    def exitStageOne(self):
        taskMgr.remove(self.uniqueName('cutsceneTimeout'))

    def enterStageTwo(self):
        """Stage Two: Fight attack ships"""
        DistributedTreasureMapInstanceAI.enterStageTwo(self)
        self.notify.info('Entering Stage Two - Defeat the attack ships')
        taskMgr.doMethodLater(1.0, self._checkAttackShips,
            self.uniqueName('checkAttackShips'))

        # the attack ships come out from behind the raised drawbridges for the Pearl:
        taskMgr.doMethodLater(self.ATTACK_SHIP_HUNT_DELAY, self._huntBlackPearl,
            self.uniqueName('huntBlackPearl'), extraArgs=[self.attackShips])

    def _checkAttackShips(self, task):
        for ship in self.attackShips:
            if ship.getHp() <= 0:
                self.handleAttackShipDestroyed(ship.doId)
        return Task.again if self.state == 'StageTwo' else Task.done

    def exitStageTwo(self):
        taskMgr.remove(self.uniqueName('checkAttackShips'))
        taskMgr.remove(self.uniqueName('huntBlackPearl'))

    def enterStageThree(self):
        """Stage Three: Destroy the barricades/drawbridges"""
        DistributedTreasureMapInstanceAI.enterStageThree(self)
        self.notify.info('Entering Stage Three - Destroy the barricades')

        # Enable barricade collisions
        for barricadeId in [0, 1, 4]:
            if barricadeId not in self.barricadesDestroyed:
                self.d_enableBarricadeCollisions(barricadeId)

        # the forts open fire on the Pearl, the Pearl has to fight it's way past them:
        self._startFortsAttacking()
        taskMgr.doMethodLater(self.SEA_CHECK_PERIOD, self._checkStageThree,
            self.uniqueName('checkStageThree'))

    def exitStageThree(self):
        taskMgr.remove(self.uniqueName('checkStageThree'))

    def enterStageFour(self):
        """Stage Four: Final battle with Goliath"""
        DistributedTreasureMapInstanceAI.enterStageFour(self)
        self.notify.info('Entering Stage Four - Destroy the Goliath!')
        self._stopFortsAttacking()
        self._huntBlackPearl([self.goliath])

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
        for avatarId in self.participants:
            avatar = self.air.doId2do.get(avatarId)
            if avatar:
                event = QuestEvent.BossBattleCompleted()
                event.setTreasureMapId(PiratesGlobals.GAME_STYLE_TM_BLACK_PEARL)
                self.air.questMgr.completeTaskState(avatar, event)
                self.sendUpdateToAvatarId(avatarId, 'setTMComplete', [[], []])

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
