"""
GameFSMShipAI - Advanced NPC Ship AI State Machine

Provides POTCO-style ship AI behaviors including:
- Intelligent patrol and wander patterns
- Target acquisition and pursuit with proper aggro mechanics
- Circling attack maneuvers for broadside positioning
- Threat assessment and prioritization
- Level-based damage modifiers
- Evasive maneuvers when damaged
- Formation behaviors with other ships

This AI uses authentic POTCO constants from:
- EnemyGlobals: Ship aggro radius and falloff mechanics
- CannonGlobals: AI fire timing and velocity
- PiratesGlobals: Cannon heading/distance ranges
- WeaponGlobals: Level-based damage modifiers
- ShipGlobals: Ship speeds, stats, and collision data
- ShipBalance: Damage modifiers and armor mechanics
"""
import random
import math

from panda3d.core import *

from direct.fsm import FSM
from direct.task import Task

from pirates.ship import ShipGlobals
from pirates.ship import FlagshipGlobals
from pirates.ship import ShipBalance
from pirates.battle import EnemyGlobals
from pirates.battle import CannonGlobals
from pirates.battle import WeaponGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.world import WorldGlobals


# ===========================================================================
# POTCO-Authentic AI Configuration Constants
# These values are sourced from the original game's configuration files
# ===========================================================================

# AI Update Rate
AI_UPDATE_INTERVAL = 0.5  # How often AI updates its state (seconds)

# Aggro and Detection Ranges (from EnemyGlobals)
# SHIP_SEARCH_RADIUS: Maximum distance to search for targets
# SHIP_MIN_SEARCH_RADIUS: Minimum search radius
# SHIP_INSTANT_AGGRO_RADIUS: Distance within which ships instantly aggro
AI_DETECTION_RANGE = EnemyGlobals.SHIP_SEARCH_RADIUS  # 4000 units
AI_MIN_DETECTION_RANGE = EnemyGlobals.SHIP_MIN_SEARCH_RADIUS  # 1000 units
AI_INSTANT_AGGRO_RANGE = EnemyGlobals.SHIP_INSTANT_AGGRO_RADIUS * 1.5  # 1500 units (50% larger)
AI_AGGRO_FALLOFF_RATE = EnemyGlobals.SHIP_AGGRO_RADIUS_FALLOFF_RATE * 0.5  # 0.05 (slower falloff)
AI_AGGRO_LEVEL_BUFFER = EnemyGlobals.SHIP_AGGRO_RADIUS_LEVEL_BUFFER + 3  # 8 levels (attack wider level range)

# Attack Ranges
AI_ATTACK_RANGE = ShipGlobals.BROADSIDE_MAX_AUTOAIM_DIST * 0.6  # Optimal broadside attack range (1200)
AI_MIN_ATTACK_RANGE = ShipGlobals.AVOID_SPHERE_RADIUS * 4  # Minimum distance to maintain (400)
AI_MAX_CHASE_RANGE = AI_DETECTION_RANGE  # Same as detection range (4000)
AI_CIRCLE_RADIUS = ShipGlobals.BROADSIDE_MAX_AUTOAIM_DIST * 0.4  # Radius for circling maneuvers (800)

# Cannon Configuration (from PiratesGlobals)
AI_CANNON_HEADING_RANGE = PiratesGlobals.AI_CANNON_HEADING_RANGE  # 45 degrees
AI_CANNON_DIST_RANGE = PiratesGlobals.AI_CANNON_DIST_RANGE  # 6000 units

# Broadside Timing (from CannonGlobals)
AI_FIRE_TIME = CannonGlobals.AI_FIRE_TIME  # 3.0 seconds between fires
AI_BROADSIDE_FIRE_VELOCITY = CannonGlobals.AI_BROADSIDE_FIRE_VELOCITY  # 200.0
BROADSIDE_POWERMOD = CannonGlobals.BROADSIDE_POWERMOD  # 0.7

# Individual Cannon Timing (simulated crew firing deck cannons)
AI_INDIVIDUAL_CANNON_FIRE_INTERVAL = 1.5  # Seconds between individual cannon shots
AI_INDIVIDUAL_CANNON_SALVO_SIZE = 3  # Number of cannons to fire per salvo
AI_INDIVIDUAL_CANNON_DAMAGE = 15  # Base damage per individual cannon hit

# Combat Behavior Thresholds
AI_AGGRO_MEMORY_TIME = 120.0  # How long ship remembers being attacked (2 minutes)
AI_WANDER_RADIUS = 3000.0  # Radius for random wandering

# Base flee/engage thresholds - AGGRESSIVE SETTINGS
# Ships are very aggressive and rarely flee
AI_BASE_FLEE_HEALTH_THRESHOLD = 0.05  # Base: flee only at 5% health (nearly dead)
AI_MIN_FLEE_HEALTH_THRESHOLD = 0.0    # Minimum: high-level ships NEVER flee
AI_MAX_FLEE_HEALTH_THRESHOLD = 0.15   # Maximum: even outmatched ships fight to 15%
AI_BASE_ENGAGE_HEALTH_THRESHOLD = 0.10  # Base: engage new targets even at 10% health
AI_LEVEL_THRESHOLD = EnemyGlobals.ENEMY_LEVEL_THRESHOLD  # 3 levels difference for modifier

# Aggression modifiers
AI_AGGRESSION_MULTIPLIER = 1.5  # Ships are 50% more likely to engage

# Default Speeds (fallback when ship class not found)
# These values are tuned to match player ship effective movement speed
# Player ships use physics with acceleration/drag, while AI uses direct interpolation
# SLOW VALUES - ships should be easy to track and hit
AI_DEFAULT_PATROL_SPEED = 20.0   # Very slow patrol
AI_DEFAULT_COMBAT_SPEED = 35.0   # Slow combat speed
AI_DEFAULT_BROADSIDE_COOLDOWN = AI_FIRE_TIME * 2.0  # Based on AI_FIRE_TIME

# Speed multiplier applied to all AI ship movement
# Set lower to make ships easier to hit
AI_SPEED_MULTIPLIER = 0.25  # 25% of normal speed

# Use ShipGlobals team constants
PLAYER_TEAM = ShipGlobals.PLAYER_TEAM
INVALID_TEAM = ShipGlobals.INVALID_TEAM
NAVY_TEAM = ShipGlobals.NAVY_TEAM
TRADING_CO_TEAM = ShipGlobals.TRADING_CO_TEAM
UNDEAD_TEAM = ShipGlobals.UNDEAD_TEAM
FRENCH_UNDEAD_TEAM = ShipGlobals.FRENCH_UNDEAD_TEAM
SPANISH_UNDEAD_TEAM = ShipGlobals.SPANISH_UNDEAD_TEAM

# All undead teams (for faction checks)
ALL_UNDEAD_TEAMS = (UNDEAD_TEAM, FRENCH_UNDEAD_TEAM, SPANISH_UNDEAD_TEAM)

# Gang-up behavior - AGGRESSIVE SETTINGS
# When an ally is attacked, nearby same-team ships WILL join the fight
AI_GANGUP_CHANCE = 75  # 75% chance to help ally (was 25%)
AI_GANGUP_LIMIT = 8    # Max 8 ships attacking one target (was 5)
AI_GANGUP_RANGE = AI_INSTANT_AGGRO_RANGE * 3  # 4500 units - large range to notice ally under attack

# Collision Avoidance
AI_COLLISION_CHECK_RANGE = 500.0  # Range to look ahead for obstacles
AI_COLLISION_AVOIDANCE_RANGE = 300.0  # Distance at which to start avoiding
AI_COLLISION_TURN_ANGLE = 45.0  # Degrees to turn when avoiding

# Despawn Configuration
# Ships will despawn after a period of idle time (no combat) to cycle variety
# This ensures newer/varied ships spawn for different player levels
AI_SHIP_MAX_LIFETIME = 600.0  # Maximum lifetime in seconds (10 minutes)
AI_SHIP_IDLE_DESPAWN_TIME = 300.0  # Despawn after 5 minutes without combat
AI_DESPAWN_CHECK_INTERVAL = 30.0  # Check despawn conditions every 30 seconds
AI_DESPAWN_MIN_DISTANCE_FROM_PLAYER = 2000.0  # Don't despawn if player ships nearby
AI_COLLISION_CHECK_INTERVAL = 0.5  # Seconds between collision checks

# Broadside side constants from ShipGlobals
BROADSIDE_LEFT = ShipGlobals.BROADSIDE_LEFT
BROADSIDE_RIGHT = ShipGlobals.BROADSIDE_RIGHT

# Target switch types from EnemyGlobals
TARGET_SWITCH_RANDOM = EnemyGlobals.TARGET_SWITCH_TYPE_RANDOM
TARGET_SWITCH_DAMAGE = EnemyGlobals.TARGET_SWITCH_TYPE_DAMAGE
TARGET_SWITCH_LOW_LVL = EnemyGlobals.TARGET_SWITCH_TYPE_LOW_LVL
TARGET_SWITCH_HIGH_LVL = EnemyGlobals.TARGET_SWITCH_TYPE_HIGH_LVL

from direct.directnotify import DirectNotifyGlobal

class GameFSMShipAI(FSM.FSM):
    """
    Advanced AI state machine for NPC ships.
    
    Uses authentic POTCO mechanics for:
    - Aggro detection with level-based falloff (EnemyGlobals)
    - Broadside timing and velocity (CannonGlobals)
    - Level-based damage modifiers (WeaponGlobals)
    - Ship balance and armor (ShipBalance)
    
    States:
    - Off: Ship is inactive
    - Neutral: Ship is idle, not moving
    - Spawn: Ship just spawned
    - PathFollow: Simple path following (legacy)
    - Patrol: Intelligent patrol pattern
    - Wander: Random wandering behavior
    - Combat: Engaged in ship-to-ship combat
    - AttackChase: Pursuing a target
    - CircleAttack: Circling target for broadside attacks
    - Flee: Retreating from combat
    - Sinking: Ship is sinking
    - Sunk: Ship has sunk
    
    Flagship States:
    - WaitingForGrapple: Flagship is crippled, waiting for grappling hooks
    - GrappleLerping: Flagship being pulled into boarding position
    - InPosition: Flagship in boarding position, waiting to be boarded
    - Boarded: Pirates are fighting the crew on the flagship
    - Defeated: Crew defeated, loot being collected
    """
    
    notify = DirectNotifyGlobal.directNotify.newCategory('GameFSMShipAI')

    def __init__(self, air, ship):
        FSM.FSM.__init__(self, 'GameFSMShipAI')

        self.air = air
        self.ship = ship

        self.oceanGrid = None
        self.world = None
        
        # Combat state
        self.targetShip = None
        self.targetDoId = 0
        self.threatList = {}  # {doId: (threat_level, last_attack_time)}
        self.lastBroadsideTime = 0
        self.lastIndividualCannonTime = 0  # Track individual cannon fire timing
        self.lastAttackedTime = 0
        self.attackerId = 0
        
        # Ship level for damage calculations
        self._shipLevel = None
        
        # Target switch behavior (from EnemyGlobals)
        self.targetSwitchType = TARGET_SWITCH_DAMAGE  # Default: prefer highest damage dealers
        
        # Movement state
        self.homePos = None
        self.wanderDestination = None
        self.circleAngle = 0
        self.circleDirection = 1  # 1 = clockwise, -1 = counter-clockwise
        
        # Task references
        self._sinkingTask = None
        self._pathFollowInterval = None
        self._aiUpdateTask = None
        self._movementTask = None
        self._broadsideTask = None
        self._despawnCheckTask = None
        
        # Despawn tracking
        self._spawnTime = globalClock.getFrameTime()  # When ship was spawned
        self._lastCombatTime = 0.0  # Last time ship was in combat
        self._moveInterval = None  # Current movement interval
        self._movementCallback = None  # Callback for when movement completes
        self._currentDestination = None  # Current movement target
        self._targetHeading = None  # Target heading for rotation
        
        # Patrol waypoints
        self._patrolWaypoints = []
        self._currentWaypointIndex = 0

    def _initWorldRefs(self):
        """Initialize world references safely."""
        if self.oceanGrid is None:
            self.oceanGrid = self.ship.getParentObj()
        if self.world is None and self.oceanGrid:
            self.world = self.oceanGrid.getParentObj()

    def cleanup(self):
        """Clean up all tasks and state."""
        self._stopAllTasks()
        self.targetShip = None
        self.targetDoId = 0
        self.threatList.clear()

    def _stopAllTasks(self):
        """Stop all running tasks and intervals."""
        if self._aiUpdateTask:
            taskMgr.remove(self._aiUpdateTask)
            self._aiUpdateTask = None
        if self._movementTask:
            taskMgr.remove(self._movementTask)
            self._movementTask = None
        if self._broadsideTask:
            taskMgr.remove(self._broadsideTask)
            self._broadsideTask = None
        if self._despawnCheckTask:
            taskMgr.remove(self._despawnCheckTask)
            self._despawnCheckTask = None
        if self._pathFollowInterval:
            self._pathFollowInterval.finish()
            self._pathFollowInterval = None
        if self._moveInterval:
            self._moveInterval.pause()
            self._moveInterval = None
        # Clean up broadside heading task
        taskMgr.remove(self.ship.uniqueName('broadside-heading'))
        # Clean up any individual cannon fire tasks (dynamically based on actual cannon count)
        numCannons = len(self.ship.cannons) if hasattr(self.ship, 'cannons') and self.ship.cannons else 0
        for i in range(numCannons):
            taskMgr.remove(self.ship.uniqueName('individual-cannon-%d' % i))
        self.ship.ignore(self._getMovementDoneName())
        self._currentDestination = None
        self._targetHeading = None
        self._movementCallback = None
        self._broadsideTarget = None

    # =========================================================================
    # Despawn System - Cycle AI ships for variety
    # =========================================================================

    def _startDespawnCheck(self):
        """Start the despawn check task for idle ships."""
        if self._despawnCheckTask:
            taskMgr.remove(self._despawnCheckTask)
        self._despawnCheckTask = taskMgr.doMethodLater(
            AI_DESPAWN_CHECK_INTERVAL, self._checkDespawn,
            self.ship.uniqueName('despawn-check'))

    def _stopDespawnCheck(self):
        """Stop the despawn check task."""
        if self._despawnCheckTask:
            taskMgr.remove(self._despawnCheckTask)
            self._despawnCheckTask = None

    def _checkDespawn(self, task):
        """
        Check if this ship should despawn to allow new ships to spawn.
        Ships despawn if:
        1. They've exceeded maximum lifetime, OR
        2. They've been idle (no combat) for too long
        
        Ships will NOT despawn if:
        - They are currently in combat
        - Player ships are nearby (would look strange)
        - They are a flagship (handled separately)
        """
        currentTime = globalClock.getFrameTime()
        
        # Don't despawn flagships - they have their own lifecycle
        if hasattr(self.ship, 'isFlagship') and self.ship.isFlagship:
            return Task.again
        
        # Check if in combat state - don't despawn during combat
        currentState = self.state
        if currentState in ('Combat', 'AttackChase', 'CircleAttack', 'Flee'):
            return Task.again
        
        # Check if any player ships are nearby - don't despawn in front of players
        if self._isPlayerShipNearby(AI_DESPAWN_MIN_DISTANCE_FROM_PLAYER):
            return Task.again
        
        # Check maximum lifetime
        lifetime = currentTime - self._spawnTime
        if lifetime > AI_SHIP_MAX_LIFETIME:
            self._despawnShip('max_lifetime')
            return Task.done
        
        # Check idle time (no combat)
        if self._lastCombatTime > 0:
            idleTime = currentTime - self._lastCombatTime
            if idleTime > AI_SHIP_IDLE_DESPAWN_TIME:
                self._despawnShip('idle_timeout')
                return Task.done
        else:
            # Never been in combat - check time since spawn
            if lifetime > AI_SHIP_IDLE_DESPAWN_TIME:
                self._despawnShip('never_engaged')
                return Task.done
        
        return Task.again

    def _isPlayerShipNearby(self, distance):
        """Check if any player ships are within the given distance."""
        if not hasattr(self.air, 'shipManager'):
            return False
        
        shipPos = self.ship.getPos()
        
        # Check all player ships via shipManager
        for playerShip in self.air.shipManager.getPlayerShips():
            try:
                if not playerShip or playerShip == self.ship:
                    continue
                if playerShip.isEmpty():
                    continue
                
                otherPos = playerShip.getPos()
                dist = (shipPos - otherPos).length()
                if dist < distance:
                    return True
            except:
                continue
        
        return False

    def _despawnShip(self, reason='unknown'):
        """
        Despawn this ship to make room for new varied ships.
        Handles cleanup and deletion gracefully.
        """
        try:
            # Log the despawn for debugging
            shipClass = getattr(self.ship, 'shipClass', 'Unknown')
            shipLevel = self._getShipLevel()
            self.notify.debug(f'Despawning ship {self.ship.doId} (class={shipClass}, level={shipLevel}) reason={reason}')
            
            # Stop all AI activity
            self._stopAllTasks()
            
            # Request deletion through the ship
            if hasattr(self.ship, 'requestDelete'):
                self.ship.requestDelete()
        except Exception as e:
            self.notify.warning(f'Error during despawn: {e}')

    def _updateLastCombatTime(self):
        """Update the last combat time to now. Called when entering combat."""
        self._lastCombatTime = globalClock.getFrameTime()

    # =========================================================================
    # Ship Class-Based Configuration
    # =========================================================================

    def _getShipSpeed(self, combatMode=False, fleeing=False):
        """
        Get ship speed from ShipGlobals based on ship class and situation.
        Applies ShipBalance.SpeedModifier for global speed tuning.
        Also applies AI_SPEED_MULTIPLIER for overall AI speed control.
        
        Speed list format from ShipGlobals: [minSpeed, normalSpeed, maxSpeed, boostSpeed]
        - minSpeed: Slow cruising
        - normalSpeed: Standard patrol
        - maxSpeed: Combat speed
        - boostSpeed: Emergency/fleeing speed
        
        Note: AI ships use direct position interpolation (posInterval), not physics.
        Player ships use physics with acceleration/drag which results in slower
        effective movement. ShipGlobals AI speeds (50-150 range) are tuned for
        the interpolation approach to look comparable to player physics movement.
        
        Args:
            combatMode: Use combat speed (maxSpeed)
            fleeing: Use boost speed for escape
        """
        # Get the global speed modifier from ShipBalance
        speedMod = ShipBalance.SpeedModifier.getValue()
        
        # Apply AI speed multiplier for overall control
        speedMod = speedMod * AI_SPEED_MULTIPLIER
        
        try:
            shipClass = self.ship.shipClass
            speedData = ShipGlobals.getAIShipSpeed(shipClass)
            if speedData and len(speedData) >= 1 and len(speedData[0]) >= 4:
                speeds = speedData[0]
                # speeds = [minSpeed, normalSpeed, maxSpeed, boostSpeed]
                if fleeing:
                    # Use boost speed for fleeing (fastest)
                    return speeds[3] * speedMod
                elif combatMode:
                    # Use max speed for combat
                    return speeds[2] * speedMod
                else:
                    # Use normal speed for patrol/wander
                    return speeds[1] * speedMod
        except:
            pass
        
        # Fallback defaults (also apply speed modifier)
        if fleeing:
            return AI_DEFAULT_COMBAT_SPEED * 1.2 * speedMod
        elif combatMode:
            return AI_DEFAULT_COMBAT_SPEED * speedMod
        return AI_DEFAULT_PATROL_SPEED * speedMod

    def _getTurnRate(self):
        """
        Get ship turn rate from ShipGlobals based on ship class.
        Turn rate is in degrees per second.
        Larger ships turn slower, smaller ships are more agile.
        """
        try:
            shipClass = self.ship.shipClass
            speedData = ShipGlobals.getAIShipSpeed(shipClass)
            if speedData and len(speedData) >= 2 and len(speedData[1]) >= 1:
                # Turn rate from ShipGlobals
                return float(speedData[1][0])
        except:
            pass
        return 10.0  # Default turn rate (degrees per second)

    def _getRotationDuration(self, angleDiff):
        """
        Calculate how long it takes to rotate a given angle based on turn rate.
        Returns duration in seconds.
        """
        turnRate = self._getTurnRate()
        if turnRate <= 0:
            turnRate = 10.0
        
        # Duration = angle / rate (degrees / degrees-per-second = seconds)
        duration = abs(angleDiff) / turnRate
        
        # Minimum rotation time for smoothness
        return max(0.5, duration)

    def _getBroadsideCooldown(self):
        """
        Get broadside cooldown based on AI_FIRE_TIME and ship class.
        Uses CannonGlobals.AI_FIRE_TIME as base.
        Larger ships have longer cooldowns, smaller ships are faster.
        """
        try:
            shipClass = self.ship.shipClass
            modelClass = ShipGlobals.getModelClass(shipClass)
            delay = ShipGlobals.getBroadsideMaxDelay(modelClass)
            if delay and delay > 0:
                # Scale relative to AI_FIRE_TIME (3.0 seconds)
                # Multiply by delay factor for ship size variation
                return max(AI_FIRE_TIME, AI_FIRE_TIME * delay * 2.0)
        except:
            pass
        return AI_DEFAULT_BROADSIDE_COOLDOWN

    # =========================================================================
    # Ship Level and Stats (POTCO-Authentic)
    # =========================================================================

    def _getShipLevel(self):
        """
        Get the ship's combat level.
        Uses ShipGlobals.getShipLevel() for proper level calculation.
        Caches the result for performance.
        """
        if self._shipLevel is not None:
            return self._shipLevel
        
        try:
            if hasattr(self.ship, 'shipClass'):
                self._shipLevel = ShipGlobals.getShipLevel(self.ship.shipClass)
                return self._shipLevel
        except:
            pass
        
        # Default level based on ship type
        self._shipLevel = 10
        return self._shipLevel

    def _getShipStatMultiplier(self, level=None):
        """
        Get stat multiplier for the ship's level.
        Uses ShipGlobals.__shipLevelStatMultiplier for authentic scaling.
        Returns (hp_mult, unknown, exp) tuple or defaults.
        """
        if level is None:
            level = self._getShipLevel()
        
        try:
            return ShipGlobals.getModifiedShipStats(level)
        except:
            pass
        
        return (1.0, 0, 10)  # Default multiplier

    def _getShipExperience(self):
        """
        Get the experience reward for defeating this ship.
        Uses ShipGlobals.getShipExp() for authentic values.
        """
        level = self._getShipLevel()
        try:
            return ShipGlobals.getShipExp(level)
        except:
            pass
        return level * 5  # Fallback: 5 exp per level

    # =========================================================================
    # Level-Based Damage Modifiers (from WeaponGlobals)
    # =========================================================================

    def _getLevelBasedDamageModifier(self, defender):
        """
        Calculate damage modifier based on level difference.
        Uses WeaponGlobals.getComparativeShipLevelDamageModifier() logic.
        
        NPC ships deal more damage to lower level targets and
        less damage to higher level targets (with 5-level threshold).
        
        Args:
            defender: The ship being attacked
            
        Returns:
            Damage multiplier (1.0 = normal, >1.0 = bonus, <1.0 = penalty)
        """
        attackerLevel = self._getShipLevel()
        
        # Get defender level
        defenderLevel = 10  # Default
        if hasattr(defender, 'gameFSM') and hasattr(defender.gameFSM, '_getShipLevel'):
            defenderLevel = defender.gameFSM._getShipLevel()
        elif hasattr(defender, 'getLevel'):
            defenderLevel = defender.getLevel()
        
        # Use WeaponGlobals formula (adapted for NPC ships)
        # THRESHOLD = 5.0 levels before modifiers kick in
        THRESHOLD = 5.0
        
        if attackerLevel > defenderLevel:
            # NPC attacking lower level: bonus damage after threshold
            mod = max(0, attackerLevel - defenderLevel - THRESHOLD) * 0.06 + 1.0
        else:
            # NPC attacking higher level: reduced damage
            mod = min(0, (attackerLevel - defenderLevel) + THRESHOLD) * 0.06 + 1.0
        
        return max(0.0, mod)

    # =========================================================================
    # Aggro Range Calculation (from EnemyGlobals)
    # =========================================================================

    def _getEffectiveAggroRange(self, targetLevel=None):
        """
        Calculate effective aggro range based on level difference.
        Uses EnemyGlobals ship aggro constants for authentic behavior.
        
        Higher level difference = smaller effective aggro range.
        Ships within SHIP_INSTANT_AGGRO_RADIUS always aggro immediately.
        
        Args:
            targetLevel: Level of potential target (for falloff calculation)
            
        Returns:
            Effective aggro range in units
        """
        baseRange = AI_DETECTION_RANGE  # SHIP_SEARCH_RADIUS = 4000
        
        if targetLevel is None:
            return baseRange
        
        myLevel = self._getShipLevel()
        levelDiff = abs(myLevel - targetLevel)
        
        # Apply level buffer (5 levels before falloff applies)
        effectiveDiff = max(0, levelDiff - AI_AGGRO_LEVEL_BUFFER)
        
        if effectiveDiff <= 0:
            return baseRange
        
        # Apply falloff: range decreases as level difference increases
        # Formula from EnemyGlobals: searchDist / max(1.0, levelDiff / FALLOFF_RATE)
        falloffDivisor = max(1.0, effectiveDiff / max(0.01, AI_AGGRO_FALLOFF_RATE))
        effectiveRange = baseRange / falloffDivisor
        
        # Never go below minimum search radius
        return max(AI_MIN_DETECTION_RANGE, effectiveRange)

    def _shouldInstantAggro(self, target):
        """
        Check if target is within instant aggro range.
        Ships within SHIP_INSTANT_AGGRO_RADIUS (1000) always aggro immediately
        regardless of level difference.
        """
        dist = self._getDistanceToTarget(target)
        return dist <= AI_INSTANT_AGGRO_RANGE

    # =========================================================================
    # ShipBalance Integration
    # =========================================================================

    def _calculateDamageFalloff(self, distance):
        """
        Calculate damage falloff based on distance.
        Uses ShipBalance.FalloffShift and FalloffMultiplier.
        
        Damage is reduced based on distance from target:
        - No falloff within FalloffShift distance (500 units)
        - Linear falloff beyond that using FalloffMultiplier
        
        Args:
            distance: Distance to target in units
            
        Returns:
            Damage multiplier (0.0 to 1.0)
        """
        falloffShift = ShipBalance.FalloffShift.getValue()  # 500
        falloffMult = ShipBalance.FalloffMultiplier.getValue()  # 0.000339683
        
        if distance <= falloffShift:
            return 1.0
        
        excessDistance = distance - falloffShift
        falloff = 1.0 - (excessDistance * falloffMult)
        
        return max(0.1, min(1.0, falloff))  # Clamp between 10% and 100%

    def _getNPCDamageModifiers(self):
        """
        Get NPC damage input and output modifiers from ShipBalance.
        
        Returns:
            Tuple of (damageIn, damageOut) modifiers
            - damageIn: Multiplier for damage received (2.6 = takes 260% damage)
            - damageOut: Multiplier for damage dealt (1.8 = deals 180% damage)
        """
        damageIn = ShipBalance.NPCDamageIn.getValue()  # 2.6
        damageOut = ShipBalance.NPCDamageOut.getValue()  # 1.8
        return (damageIn, damageOut)

    def _getArmorAbsorption(self):
        """
        Get armor absorption values from ShipBalance.
        
        Returns:
            Tuple of (absorb, bounce, npcMod)
            - absorb: Fraction of damage absorbed by armor (0.7 = 70%)
            - bounce: Fraction of shots that bounce off (0.2 = 20%)
            - npcMod: NPC-specific armor modifier (0.5 = 50% effective)
        """
        absorb = ShipBalance.ArmorAbsorb.getValue()  # 0.7
        bounce = ShipBalance.ArmorBounce.getValue()  # 0.2
        npcMod = ShipBalance.NPCArmorModifier.getValue()  # 0.5
        return (absorb, bounce, npcMod)
    
    def _getHealthPercent(self):
        """Get ship's health as a percentage."""
        if self.ship.maxHp <= 0:
            return 1.0
        return self.ship.hp / self.ship.maxHp

    def _getFleeThreshold(self, targetLevel=None):
        """
        Calculate dynamic flee threshold based on level difference.
        Ships with level advantage are more aggressive (lower flee threshold).
        Ships with level disadvantage are more cautious (higher flee threshold).
        
        Uses EnemyGlobals.ENEMY_LEVEL_THRESHOLD (3) for significant difference.
        """
        if targetLevel is None:
            return AI_BASE_FLEE_HEALTH_THRESHOLD
        
        myLevel = self._getShipLevel()
        levelDiff = myLevel - targetLevel  # Positive = we're higher level
        
        # Adjust threshold based on level difference
        # Each 3 levels of advantage = 5% lower flee threshold
        # Each 3 levels of disadvantage = 5% higher flee threshold
        levelFactor = levelDiff / max(1, AI_LEVEL_THRESHOLD)
        adjustment = levelFactor * 0.05
        
        threshold = AI_BASE_FLEE_HEALTH_THRESHOLD - adjustment
        
        # Clamp to valid range
        return max(AI_MIN_FLEE_HEALTH_THRESHOLD, 
                   min(AI_MAX_FLEE_HEALTH_THRESHOLD, threshold))

    def _getEngageThreshold(self, targetLevel=None):
        """
        Calculate dynamic engage threshold based on level difference.
        Ships with level advantage engage more readily (lower health needed).
        """
        if targetLevel is None:
            return AI_BASE_ENGAGE_HEALTH_THRESHOLD
        
        myLevel = self._getShipLevel()
        levelDiff = myLevel - targetLevel
        
        # Higher level ships engage even when damaged
        levelFactor = levelDiff / max(1, AI_LEVEL_THRESHOLD)
        adjustment = levelFactor * 0.1
        
        threshold = AI_BASE_ENGAGE_HEALTH_THRESHOLD - adjustment
        
        return max(0.1, min(0.6, threshold))

    def _shouldFlee(self, target=None):
        """
        Determine if ship should flee from combat.
        AGGRESSIVE: Ships rarely flee - they fight until nearly destroyed.
        
        Returns:
            True if ship should flee, False if should continue fighting
        """
        healthPct = self._getHealthPercent()
        
        # Very aggressive - only flee when almost dead
        # High level ships may NEVER flee (threshold can be 0)
        targetLevel = None
        if target:
            if hasattr(target, 'getLevel'):
                targetLevel = target.getLevel()
            elif hasattr(target, 'gameFSM') and hasattr(target.gameFSM, '_getShipLevel'):
                targetLevel = target.gameFSM._getShipLevel()
        elif self.targetShip:
            if hasattr(self.targetShip, 'getLevel'):
                targetLevel = self.targetShip.getLevel()
            elif hasattr(self.targetShip, 'gameFSM') and hasattr(self.targetShip.gameFSM, '_getShipLevel'):
                targetLevel = self.targetShip.gameFSM._getShipLevel()
        
        fleeThreshold = self._getFleeThreshold(targetLevel)
        
        # Add a random chance to NOT flee even when below threshold (fighting spirit)
        if healthPct < fleeThreshold:
            import random
            # 50% chance to keep fighting anyway
            if random.random() < 0.5:
                return False
        
        return healthPct < fleeThreshold

    def _shouldEngage(self, target=None):
        """
        Determine if ship should engage a new target.
        AGGRESSIVE: Ships almost always engage, even when damaged.
        
        Returns:
            True if ship should engage, False if should avoid combat
        """
        healthPct = self._getHealthPercent()
        
        # Very aggressive - engage even at low health
        targetLevel = None
        if target:
            if hasattr(target, 'getLevel'):
                targetLevel = target.getLevel()
            elif hasattr(target, 'gameFSM') and hasattr(target.gameFSM, '_getShipLevel'):
                targetLevel = target.gameFSM._getShipLevel()
        
        engageThreshold = self._getEngageThreshold(targetLevel)
        
        # Aggressive ships have a chance to engage even below threshold
        if healthPct <= engageThreshold:
            import random
            # 30% chance to engage anyway
            if random.random() < 0.3:
                return True
        
        return healthPct > engageThreshold

    def _getDistanceToTarget(self, target):
        """Get distance to a target ship."""
        if not target or target.isEmpty():
            return float('inf')
        try:
            return self.ship.getDistance(target)
        except:
            return float('inf')

    def _getShipTeam(self, ship=None):
        """
        Get the team of a ship.
        Uses ShipGlobals team constants (PLAYER_TEAM, NAVY_TEAM, etc).
        """
        if ship is None:
            ship = self.ship
        
        # Check if ship has getTeam or getBaseTeam method
        if hasattr(ship, 'getTeam'):
            team = ship.getTeam()
            if team != INVALID_TEAM:
                return team
        
        # NPC ships use getBaseTeam
        if hasattr(ship, 'getBaseTeam'):
            team = ship.getBaseTeam()
            if team is not None and team != INVALID_TEAM:
                return team
        
        # Check baseTeam attribute directly
        if hasattr(ship, 'baseTeam'):
            team = ship.baseTeam
            if team is not None and team != INVALID_TEAM:
                return team
        
        # Check if this is a player ship (PlayerShipAI or has player crew)
        # Player ships have captainId or crew members
        if hasattr(ship, 'captainId') or hasattr(ship, 'getCaptainId'):
            return PLAYER_TEAM
        if hasattr(ship, 'crewDoIds') or hasattr(ship, 'getCrewDoIds'):
            return PLAYER_TEAM
        # Check class name as fallback
        className = ship.__class__.__name__
        if 'Player' in className:
            return PLAYER_TEAM
        
        # Try to determine team from ship class (for NPC ships)
        if hasattr(ship, 'shipClass'):
            try:
                shipData = ShipGlobals.shipData.get(ship.shipClass)
                if shipData:
                    return shipData[ShipGlobals.TEAM_INDEX]
            except:
                pass
        
        return INVALID_TEAM

    def _isSameTeam(self, otherShip):
        """
        Check if another ship is on the same team.
        Ships on the same team should NEVER attack each other.
        """
        if not otherShip:
            return False
        
        myTeam = self._getShipTeam(self.ship)
        otherTeam = self._getShipTeam(otherShip)
        
        # Invalid team ships are neutral
        if myTeam == INVALID_TEAM or otherTeam == INVALID_TEAM:
            return False
        
        # Player ships are never same team as NPC ships
        if myTeam == PLAYER_TEAM or otherTeam == PLAYER_TEAM:
            return myTeam == otherTeam
        
        return myTeam == otherTeam

    def _isEnemy(self, otherShip):
        """
        Check if another ship is an enemy.
        All non-same-team ships are enemies (except for special alliances).
        """
        if not otherShip:
            return False
        
        myTeam = self._getShipTeam(self.ship)
        otherTeam = self._getShipTeam(otherShip)
        
        # NPC ships (this AI) should attack player ships regardless of team issues
        # This is a safety fallback - NPC ships are always hostile to players
        if otherTeam == PLAYER_TEAM:
            return True
        
        # Invalid team = neutral, not enemy
        if myTeam == INVALID_TEAM or otherTeam == INVALID_TEAM:
            return False
        
        # Player ships are always enemies to NPC faction ships
        if otherTeam == PLAYER_TEAM and myTeam != PLAYER_TEAM:
            return True
        
        # NPC factions are enemies of players
        if myTeam == PLAYER_TEAM:
            return otherTeam != PLAYER_TEAM
        
        # Same NPC faction = allies, not enemies
        if myTeam == otherTeam:
            return False
        
        # Different NPC factions could be enemies or neutral
        # Navy and EITC work together against pirates (not enemies)
        # All undead factions are enemies of everyone including each other
        # (French Undead, Spanish Undead, and regular Undead all fight everyone)
        if myTeam in (NAVY_TEAM, TRADING_CO_TEAM):
            if otherTeam in (NAVY_TEAM, TRADING_CO_TEAM):
                return False  # Navy and EITC are allies
            return True  # Enemies with undead and players
        
        # All undead teams fight everyone (including other undead factions)
        if myTeam in ALL_UNDEAD_TEAMS:
            # Undead of same faction are allies
            if myTeam == otherTeam:
                return False
            return True  # Fight everyone else including other undead factions
        
        return myTeam != otherTeam

    def _isValidTarget(self, target):
        """Check if a target is valid for engagement."""
        if not target:
            return False
        if target.isEmpty():
            return False
        # Don't attack ships on same team (uses faction alliance logic)
        if self._isSameTeam(target):
            return False
        # Only attack enemies (respects faction alliances like Navy/EITC)
        if not self._isEnemy(target):
            return False
        # Don't attack sinking/sunk ships
        if hasattr(target, 'gameFSM'):
            state = target.gameFSM.getCurrentOrNextState()
            if state in ('Sinking', 'Sunk', 'Off', 'PutAway'):
                return False
        return True

    def _findNearbyAllies(self, range=None):
        """
        Find allied ships within range that could assist in combat.
        Uses AI_GANGUP_RANGE by default.
        Returns list of allied ship AI instances.
        """
        if range is None:
            range = AI_GANGUP_RANGE
        
        allies = []
        self._initWorldRefs()
        
        if not hasattr(self.air, 'shipManager'):
            return allies
        
        # Check NPC ships for allies
        for npcShip in self.air.shipManager.getShips():
            if npcShip == self.ship:
                continue
            if not npcShip or npcShip.isEmpty():
                continue
            if not self._isSameTeam(npcShip):
                continue
            
            dist = self._getDistanceToTarget(npcShip)
            if dist <= range:
                # Get the ship's AI/FSM if available
                if hasattr(npcShip, 'gameFSM'):
                    allies.append(npcShip.gameFSM)
                else:
                    allies.append(npcShip)
        
        return allies

    def _notifyAlliesOfAttack(self, attackerDoId):
        """
        Notify nearby allies that we're being attacked.
        Implements POTCO gang-up behavior where nearby faction ships
        may join the fight when one is attacked.
        
        Uses AI_GANGUP_CHANCE to determine if each ally responds.
        Respects AI_GANGUP_LIMIT to prevent too many ships piling on.
        """
        import random
        
        if not attackerDoId:
            return
        
        # Get the attacker ship
        attacker = None
        if hasattr(self.air, 'doId2do'):
            attacker = self.air.doId2do.get(attackerDoId)
        
        if not attacker:
            return
        
        # Count how many ships are already targeting this attacker
        currentTargeters = 0
        allies = self._findNearbyAllies()
        
        for ally in allies:
            if hasattr(ally, 'currentTarget'):
                if ally.currentTarget and hasattr(ally.currentTarget, 'doId'):
                    if ally.currentTarget.doId == attackerDoId:
                        currentTargeters += 1
        
        # Include ourselves in the count
        currentTargeters += 1
        
        if currentTargeters >= AI_GANGUP_LIMIT:
            return  # Already at gang-up limit
        
        # Notify each ally with gangup chance
        for ally in allies:
            if currentTargeters >= AI_GANGUP_LIMIT:
                break
            
            # Skip allies already in combat with something else important
            if hasattr(ally, 'currentTarget') and ally.currentTarget:
                continue
            
            # Roll for gangup chance
            if random.randint(1, 100) <= AI_GANGUP_CHANCE:
                # Have this ally engage the attacker
                if hasattr(ally, 'engageTarget'):
                    ally.engageTarget(attacker)
                    currentTargeters += 1
                elif hasattr(ally, 'setTarget'):
                    ally.setTarget(attacker)
                    currentTargeters += 1

    def engageTarget(self, target):
        """
        Force this ship to engage a specific target.
        Used by gang-up system when allies call for help.
        Immediately breaks current movement to respond.
        """
        if not self._isValidTarget(target):
            return False
        
        # Stop current movement immediately to engage
        self._stopMovement()
        
        self.targetShip = target
        if hasattr(target, 'doId'):
            self.targetDoId = target.doId
        
        currentState = self.getCurrentOrNextState()
        
        # Transition to combat if not already fighting
        if currentState not in ('Attacking', 'Engaged', 'Combat', 'AttackChase', 'CircleAttack'):
            self.request('Combat')
        
        return True

    def _findNearestEnemy(self):
        """
        Find the nearest enemy ship within detection range.
        Uses POTCO-authentic aggro mechanics:
        - Instant aggro within SHIP_INSTANT_AGGRO_RADIUS (1000)
        - Level-based aggro falloff beyond that
        - Maximum search at SHIP_SEARCH_RADIUS (4000)
        """
        self._initWorldRefs()
        
        nearestEnemy = None
        nearestDist = AI_DETECTION_RANGE
        instantAggroTarget = None
        
        myTeam = self._getShipTeam(self.ship)
        
        # Check player ships
        if hasattr(self.air, 'shipManager'):
            playerShips = self.air.shipManager.getPlayerShips()
            for playerShip in playerShips:
                if not self._isValidTarget(playerShip):
                    continue
                
                dist = self._getDistanceToTarget(playerShip)
                
                # Check for instant aggro first (highest priority)
                if dist <= AI_INSTANT_AGGRO_RANGE:
                    if instantAggroTarget is None or dist < self._getDistanceToTarget(instantAggroTarget):
                        instantAggroTarget = playerShip
                    continue
                
                # Get target level for aggro range calculation
                targetLevel = 10  # Default
                if hasattr(playerShip, 'getLevel'):
                    targetLevel = playerShip.getLevel()
                elif hasattr(playerShip, 'gameFSM') and hasattr(playerShip.gameFSM, '_getShipLevel'):
                    targetLevel = playerShip.gameFSM._getShipLevel()
                
                # Calculate effective aggro range with level falloff
                effectiveRange = self._getEffectiveAggroRange(targetLevel)
                
                if dist < effectiveRange and dist < nearestDist:
                    nearestDist = dist
                    nearestEnemy = playerShip
        
        # Instant aggro targets take priority
        if instantAggroTarget:
            return instantAggroTarget, self._getDistanceToTarget(instantAggroTarget)
        
        return nearestEnemy, nearestDist

    def _updateThreatList(self):
        """Update and clean threat list."""
        currentTime = globalClock.getFrameTime()
        expiredThreats = []
        
        for doId, (threatLevel, lastTime) in self.threatList.items():
            if currentTime - lastTime > AI_AGGRO_MEMORY_TIME:
                expiredThreats.append(doId)
        
        for doId in expiredThreats:
            del self.threatList[doId]

    def addThreat(self, attackerDoId, damage=0):
        """Add or update a threat in the threat list."""
        currentTime = globalClock.getFrameTime()
        
        if attackerDoId in self.threatList:
            oldThreat, _ = self.threatList[attackerDoId]
            self.threatList[attackerDoId] = (oldThreat + damage + 10, currentTime)
        else:
            self.threatList[attackerDoId] = (damage + 10, currentTime)
        
        self.lastAttackedTime = currentTime
        self.attackerId = attackerDoId

    def onDamageReceived(self, attackerDoId, damage):
        """Called when this ship receives damage. ALWAYS responds to attacks."""
        self.notify.debug('onDamageReceived: ship=%d attacker=%d damage=%d state=%s' % (
            self.ship.doId, attackerDoId, damage, self.state))
        
        self.addThreat(attackerDoId, damage)
        
        # Update combat time for despawn tracking
        self._updateLastCombatTime()
        
        currentState = self.getCurrentOrNextState()
        
        # Notify nearby allies of the attack (gang-up behavior)
        self._notifyAlliesOfAttack(attackerDoId)
        
        # Get attacker from doId2do
        attacker = self.air.doId2do.get(attackerDoId)
        
        # ALWAYS respond to attacks - don't just sit there!
        # Even if already in combat, switch to the new attacker if they're hurting us
        if currentState in ('Patrol', 'Wander', 'PathFollow', 'Neutral', 'Off'):
            if attacker:
                self.notify.debug('onDamageReceived: Engaging attacker! Switching to Combat')
                # Stop current movement immediately to respond to attack
                self._stopMovement()
                
                self.targetShip = attacker
                self.targetDoId = attackerDoId
                
                # Immediately turn toward the attacker for counterattack
                # This makes the ship visibly respond to being shot
                self._turnTowardTarget(attacker)
                
                # Aggressive ships almost always fight back
                if self._shouldFlee(attacker):
                    self.request('Flee')
                else:
                    self.request('Combat')
        elif currentState in ('Combat', 'AttackChase', 'CircleAttack'):
            # Already in combat - update target if this is a new/more dangerous threat
            if attacker and attacker != self.targetShip:
                # Switch to new attacker if they're doing significant damage
                if damage > 50:  # Significant damage threshold
                    self.targetShip = attacker
                    self.targetDoId = attackerDoId
                    # Turn toward new threat
                    self._turnTowardTarget(attacker)

    def _turnTowardTarget(self, target):
        """
        Immediately turn the ship to face toward the target.
        Used when initially responding to an attack.
        """
        if not target:
            return
        
        try:
            # Calculate heading to target
            shipPos = self.ship.getPos()
            targetPos = target.getPos()
            dx = targetPos.getX() - shipPos.getX()
            dy = targetPos.getY() - shipPos.getY()
            
            # Calculate heading (Panda3D: 0 = +Y, 90 = -X)
            headingToTarget = -math.degrees(math.atan2(dx, dy))
            
            # Set ship heading to face target directly
            self.ship.setH(headingToTarget)
        except:
            pass

    def _selectBestTarget(self):
        """
        Select the best target based on threat, proximity, and switch type.
        Uses EnemyGlobals TARGET_SWITCH_TYPE for authentic behavior:
        - TARGET_SWITCH_DAMAGE: Prefer highest damage dealers (default)
        - TARGET_SWITCH_RANDOM: Random selection
        - TARGET_SWITCH_LOW_LVL: Prefer lower level targets
        - TARGET_SWITCH_HIGH_LVL: Prefer higher level targets
        """
        self._updateThreatList()
        
        validTargets = []
        
        for doId, (threatLevel, lastTime) in self.threatList.items():
            target = self.air.doId2do.get(doId)
            if not self._isValidTarget(target):
                continue
            
            dist = self._getDistanceToTarget(target)
            if dist > AI_MAX_CHASE_RANGE:
                continue
            
            # Get target level
            targetLevel = 10
            if hasattr(target, 'getLevel'):
                targetLevel = target.getLevel()
            
            validTargets.append({
                'target': target,
                'threat': threatLevel,
                'dist': dist,
                'level': targetLevel
            })
        
        if not validTargets:
            # If no threats, look for nearby enemies (level-aware engagement)
            enemy, _ = self._findNearestEnemy()
            if enemy and self._shouldEngage(enemy):
                return enemy
            return None
        
        # Apply target switch type scoring
        bestTarget = None
        bestScore = -float('inf')
        
        myLevel = self._getShipLevel()
        
        for info in validTargets:
            score = 0
            
            # Base proximity score
            proximityScore = max(0, AI_MAX_CHASE_RANGE - info['dist']) / AI_MAX_CHASE_RANGE * 50
            
            if self.targetSwitchType & TARGET_SWITCH_DAMAGE:
                # Prefer targets that dealt most damage
                score = info['threat'] + proximityScore
            elif self.targetSwitchType & TARGET_SWITCH_RANDOM:
                # Random scoring
                score = random.random() * 100 + proximityScore
            elif self.targetSwitchType & TARGET_SWITCH_LOW_LVL:
                # Prefer lower level targets (easier kills)
                levelScore = max(0, myLevel - info['level']) * 10
                score = levelScore + proximityScore
            elif self.targetSwitchType & TARGET_SWITCH_HIGH_LVL:
                # Prefer higher level targets (bigger threats)
                levelScore = max(0, info['level'] - myLevel) * 10
                score = levelScore + info['threat'] + proximityScore
            else:
                # Default: threat + proximity
                score = info['threat'] + proximityScore
            
            if score > bestScore:
                bestScore = score
                bestTarget = info['target']
        
        return bestTarget

    # =========================================================================
    # Movement and Navigation
    # =========================================================================

    def _getShipCollisionRadius(self, ship=None):
        """
        Get the collision radius for a ship based on its class/size.
        Larger ships have bigger collision radii.
        """
        if ship is None:
            ship = self.ship
        
        try:
            shipClass = ship.shipClass
            # Base radius varies by ship type
            # Warships are largest, interceptors smallest
            if shipClass in (ShipGlobals.WARSHIPL1, ShipGlobals.WARSHIPL2, 
                            ShipGlobals.WARSHIPL3, ShipGlobals.WARSHIPL4):
                return 150.0  # Large warship
            elif shipClass in (ShipGlobals.MERCHANTL1, ShipGlobals.MERCHANTL2,
                              ShipGlobals.MERCHANTL3, ShipGlobals.MERCHANTL4):
                return 120.0  # Medium merchant
            elif shipClass in (ShipGlobals.INTERCEPTORL1, ShipGlobals.INTERCEPTORL2,
                              ShipGlobals.INTERCEPTORL3, ShipGlobals.INTERCEPTORL4):
                return 80.0  # Small interceptor
            elif shipClass >= 80 and shipClass <= 91:
                # Navy ships
                return 140.0
            elif shipClass >= 100 and shipClass <= 115:
                # EITC ships
                return 130.0
            elif shipClass in (ShipGlobals.BLACK_PEARL, ShipGlobals.FLYING_DUTCHMAN,
                              ShipGlobals.GOLIATH):
                return 180.0  # Boss ships are huge
        except:
            pass
        
        return 100.0  # Default radius

    def _getNearbyShips(self, maxRange=2000.0):
        """
        Get all nearby ships (both NPC and player) within range.
        Returns list of (ship, x, y, radius) tuples.
        Excludes self and sinking/sunk ships.
        """
        self._initWorldRefs()
        nearbyShips = []
        
        try:
            shipPos = self.ship.getPos()
            shipX, shipY = shipPos.getX(), shipPos.getY()
            
            # Get NPC ships from ship manager
            if hasattr(self.air, 'shipManager'):
                for otherShip in self.air.shipManager.getShips():
                    if otherShip == self.ship or not otherShip:
                        continue
                    
                    # Skip sinking/sunk ships
                    if hasattr(otherShip, 'gameFSM'):
                        state = otherShip.gameFSM.getCurrentOrNextState()
                        if state in ('Sinking', 'Sunk', 'Off', 'PutAway'):
                            continue
                    
                    try:
                        otherPos = otherShip.getPos()
                        ox, oy = otherPos.getX(), otherPos.getY()
                        
                        # Check if within range
                        dx = ox - shipX
                        dy = oy - shipY
                        distSq = dx * dx + dy * dy
                        
                        if distSq < maxRange * maxRange:
                            radius = self._getShipCollisionRadius(otherShip)
                            nearbyShips.append((otherShip, ox, oy, radius))
                    except:
                        continue
            
            # Get player ships
            if hasattr(self.air, 'shipManager'):
                for playerShip in self.air.shipManager.getPlayerShips():
                    if playerShip == self.ship or not playerShip:
                        continue
                    
                    # Skip sinking/sunk ships
                    if hasattr(playerShip, 'gameFSM'):
                        state = playerShip.gameFSM.getCurrentOrNextState()
                        if state in ('Sinking', 'Sunk', 'Off', 'PutAway'):
                            continue
                    
                    try:
                        otherPos = playerShip.getPos()
                        ox, oy = otherPos.getX(), otherPos.getY()
                        
                        # Check if within range
                        dx = ox - shipX
                        dy = oy - shipY
                        distSq = dx * dx + dy * dy
                        
                        if distSq < maxRange * maxRange:
                            radius = self._getShipCollisionRadius(playerShip)
                            nearbyShips.append((playerShip, ox, oy, radius))
                    except:
                        continue
        except:
            pass
        
        return nearbyShips

    def _getIslandCollisionSpheres(self):
        """
        Get all island collision spheres from the world.
        Returns list of (centerX, centerY, radius) tuples.
        """
        self._initWorldRefs()
        collisionSpheres = []
        
        try:
            if self.world and hasattr(self.world, 'builder'):
                islands = self.world.builder.getIslands()
                for island in islands:
                    if not island:
                        continue
                    
                    # Get island position from transform
                    islandTransform = island.getIslandTransform()
                    islandX, islandY = islandTransform[0], islandTransform[1]
                    
                    # Get port collision spheres
                    portSpheres = island.getPortCollisionSpheres()
                    if portSpheres:
                        for sphere in portSpheres:
                            # PortCollisionSphere has radius and pos (x, y, z)
                            radius = sphere.get('radius', 0)
                            pos = sphere.get('pos', (0, 0, 0))
                            # Add island offset to sphere position
                            centerX = islandX + pos[0]
                            centerY = islandY + pos[1]
                            collisionSpheres.append((centerX, centerY, radius))
                    
                    # Also add the island's zone sphere as a collision area
                    # The inner sphere radius (sphereRadii[0]) is the docking area
                    sphereCenter = island.sphereCenter
                    sphereRadii = island.sphereRadii
                    if sphereRadii and len(sphereRadii) > 0:
                        # Use inner radius as collision zone (ships shouldn't sail through island)
                        innerRadius = sphereRadii[0]
                        centerX = islandX + sphereCenter[0]
                        centerY = islandY + sphereCenter[1]
                        collisionSpheres.append((centerX, centerY, innerRadius))
        except Exception as e:
            pass
        
        return collisionSpheres

    # =========================================================================
    # Ocean Grid Bounds
    # =========================================================================

    def _getGridBounds(self):
        """
        Get the ocean grid boundaries.
        Grid is centered at origin with size = gridSize * cellWidth.
        
        Returns: (minX, maxX, minY, maxY) tuple
        """
        gridSize = WorldGlobals.OCEAN_GRID_SIZE
        cellWidth = WorldGlobals.OCEAN_CELL_SIZE
        halfSize = (gridSize * cellWidth) / 2.0
        
        # Add a small margin so ships don't get too close to edge
        margin = 2000.0  # 1 cell margin
        
        return (-halfSize + margin, halfSize - margin, 
                -halfSize + margin, halfSize - margin)

    def _isWithinGridBounds(self, x, y):
        """
        Check if a position is within the ocean grid bounds.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns: True if within bounds, False otherwise
        """
        minX, maxX, minY, maxY = self._getGridBounds()
        return minX <= x <= maxX and minY <= y <= maxY

    def _clampToGridBounds(self, x, y):
        """
        Clamp a position to be within the ocean grid bounds.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns: (clampedX, clampedY) tuple
        """
        minX, maxX, minY, maxY = self._getGridBounds()
        clampedX = max(minX, min(maxX, x))
        clampedY = max(minY, min(maxY, y))
        return clampedX, clampedY

    def _clampDestinationToGrid(self, destination):
        """
        Clamp a Point3 destination to be within grid bounds.
        
        Args:
            destination: Point3 position
            
        Returns: Point3 with clamped coordinates
        """
        if not destination:
            return None
        
        x, y = self._clampToGridBounds(destination.getX(), destination.getY())
        return Point3(x, y, 0)

    def _isApproachingGridEdge(self, margin=5000.0):
        """
        Check if the ship is approaching the edge of the ocean grid.
        Useful for triggering a turn-around before hitting the boundary.
        
        Args:
            margin: Distance from edge to start turning (default 5000 units)
            
        Returns: True if near edge, False otherwise
        """
        shipX = self.ship.getX()
        shipY = self.ship.getY()
        minX, maxX, minY, maxY = self._getGridBounds()
        
        # Check if within margin of any edge
        nearEdge = (shipX <= minX + margin or shipX >= maxX - margin or
                    shipY <= minY + margin or shipY >= maxY - margin)
        return nearEdge

    def _getDirectionAwayFromEdge(self):
        """
        Get a destination point that moves the ship away from the grid edge.
        Used when a ship gets too close to the boundary.
        
        Returns: Point3 destination toward grid center
        """
        shipX = self.ship.getX()
        shipY = self.ship.getY()
        
        # Move toward center (0, 0)
        dirX = -shipX
        dirY = -shipY
        
        # Normalize and scale
        length = math.sqrt(dirX * dirX + dirY * dirY)
        if length > 0:
            dirX /= length
            dirY /= length
        
        # Move a reasonable distance toward center
        moveDistance = 3000.0
        newX = shipX + dirX * moveDistance
        newY = shipY + dirY * moveDistance
        
        return Point3(newX, newY, 0)

    def _isPositionSafe(self, pos, checkShips=True):
        """
        Check if a position is safe (not inside any collision zone).
        Checks grid bounds, island collisions, and other ship positions.
        
        Args:
            pos: Position to check
            checkShips: Whether to also check for ship collisions
        
        Returns True if safe, False if inside a collision zone or outside grid.
        """
        if not pos:
            return False
        
        posX, posY = pos.getX(), pos.getY()
        
        # Check if position is within ocean grid bounds
        if not self._isWithinGridBounds(posX, posY):
            return False
        myRadius = self._getShipCollisionRadius()
        
        # Check island collisions
        collisionSpheres = self._getIslandCollisionSpheres()
        for centerX, centerY, radius in collisionSpheres:
            # Add a safety buffer to the radius
            safetyBuffer = 200.0
            effectiveRadius = radius + safetyBuffer
            
            # Calculate distance to sphere center
            dx = posX - centerX
            dy = posY - centerY
            distSq = dx * dx + dy * dy
            
            if distSq < effectiveRadius * effectiveRadius:
                return False
        
        # Check ship collisions
        if checkShips:
            nearbyShips = self._getNearbyShips(maxRange=1500.0)
            for otherShip, shipX, shipY, shipRadius in nearbyShips:
                # Combined radius (my ship + other ship + buffer)
                safetyBuffer = 100.0
                effectiveRadius = myRadius + shipRadius + safetyBuffer
                
                dx = posX - shipX
                dy = posY - shipY
                distSq = dx * dx + dy * dy
                
                if distSq < effectiveRadius * effectiveRadius:
                    return False
        
        return True

    def _isPathSafe(self, startPos, endPos, checkShips=True):
        """
        Check if a path between two points is safe.
        Checks both island and ship collisions using line-circle intersection.
        
        Args:
            startPos: Starting position
            endPos: Ending position
            checkShips: Whether to also check for ship collisions
        """
        if not startPos or not endPos:
            return False
        
        sx, sy = startPos.getX(), startPos.getY()
        ex, ey = endPos.getX(), endPos.getY()
        
        # Direction vector
        dx = ex - sx
        dy = ey - sy
        pathLengthSq = dx * dx + dy * dy
        
        if pathLengthSq < 1:
            return True  # Start and end are same point
        
        myRadius = self._getShipCollisionRadius()
        
        # Check island collisions
        collisionSpheres = self._getIslandCollisionSpheres()
        for centerX, centerY, radius in collisionSpheres:
            safetyBuffer = 200.0
            effectiveRadius = radius + safetyBuffer + myRadius
            
            if not self._lineCircleIntersection(sx, sy, dx, dy, pathLengthSq, 
                                                 centerX, centerY, effectiveRadius):
                return False
        
        # Check ship collisions
        if checkShips:
            nearbyShips = self._getNearbyShips(maxRange=1500.0)
            for otherShip, shipX, shipY, shipRadius in nearbyShips:
                safetyBuffer = 100.0
                effectiveRadius = myRadius + shipRadius + safetyBuffer
                
                if not self._lineCircleIntersection(sx, sy, dx, dy, pathLengthSq,
                                                     shipX, shipY, effectiveRadius):
                    return False
        
        return True

    def _lineCircleIntersection(self, sx, sy, dx, dy, pathLengthSq, 
                                 centerX, centerY, radius):
        """
        Check if a line segment intersects a circle.
        Returns True if NO intersection (path is clear), False if blocked.
        
        Args:
            sx, sy: Start point
            dx, dy: Direction vector (end - start)
            pathLengthSq: Squared length of path
            centerX, centerY: Circle center
            radius: Circle radius
        """
        # Vector from start to circle center
        fx = sx - centerX
        fy = sy - centerY
        
        # Quadratic equation coefficients for line-circle intersection
        a = pathLengthSq
        b = 2 * (fx * dx + fy * dy)
        c = fx * fx + fy * fy - radius * radius
        
        discriminant = b * b - 4 * a * c
        
        if discriminant >= 0:
            # Path intersects circle, check if intersection is on the segment
            sqrtDisc = math.sqrt(discriminant)
            t1 = (-b - sqrtDisc) / (2 * a)
            t2 = (-b + sqrtDisc) / (2 * a)
            
            # Check if intersection points are within the segment [0, 1]
            if (0 <= t1 <= 1) or (0 <= t2 <= 1) or (t1 < 0 and t2 > 1):
                return False  # Path is blocked
        
        return True  # Path is clear

    # =========================================================================
    # Real-Time Collision Avoidance
    # =========================================================================

    def _checkCollisionAhead(self):
        """
        Check if there's an imminent collision with another ship or obstacle
        directly ahead of the current heading.
        
        Returns: (hasCollision, obstacleInfo) where obstacleInfo is 
                 (obstaclePos, obstacleRadius, distance) or None
        """
        try:
            shipPos = self.ship.getPos()
            shipHeading = self.ship.getH()
            
            # Get forward direction vector from heading
            headingRad = math.radians(shipHeading)
            forwardX = -math.sin(headingRad)
            forwardY = math.cos(headingRad)
            
            shipX, shipY = shipPos.getX(), shipPos.getY()
            myRadius = self._getShipCollisionRadius()
            
            nearestObstacle = None
            nearestDist = AI_COLLISION_CHECK_RANGE
            
            # Check nearby ships
            nearbyShips = self._getNearbyShips(maxRange=AI_COLLISION_CHECK_RANGE)
            for otherShip, ox, oy, otherRadius in nearbyShips:
                # Vector to other ship
                toShipX = ox - shipX
                toShipY = oy - shipY
                
                # Project onto forward direction
                forwardDist = toShipX * forwardX + toShipY * forwardY
                
                # Only check things ahead of us
                if forwardDist <= 0:
                    continue
                
                # Perpendicular distance (how far off to the side)
                perpDist = abs(toShipX * forwardY - toShipY * forwardX)
                
                # Combined radius for collision
                combinedRadius = myRadius + otherRadius + 50.0  # Buffer
                
                # Will we collide?
                if perpDist < combinedRadius and forwardDist < nearestDist:
                    nearestDist = forwardDist
                    nearestObstacle = (Point3(ox, oy, 0), otherRadius, forwardDist)
            
            # Check islands
            collisionSpheres = self._getIslandCollisionSpheres()
            for centerX, centerY, radius in collisionSpheres:
                toIslandX = centerX - shipX
                toIslandY = centerY - shipY
                
                forwardDist = toIslandX * forwardX + toIslandY * forwardY
                
                if forwardDist <= 0:
                    continue
                
                perpDist = abs(toIslandX * forwardY - toIslandY * forwardX)
                combinedRadius = myRadius + radius + 100.0  # Larger buffer for islands
                
                if perpDist < combinedRadius and forwardDist < nearestDist:
                    nearestDist = forwardDist
                    nearestObstacle = (Point3(centerX, centerY, 0), radius, forwardDist)
            
            if nearestObstacle and nearestDist < AI_COLLISION_AVOIDANCE_RANGE:
                return (True, nearestObstacle)
            
            return (False, None)
            
        except Exception as e:
            return (False, None)

    def _getAvoidanceDirection(self, obstaclePos):
        """
        Calculate which direction to turn to avoid an obstacle.
        Returns: 1 for right turn, -1 for left turn
        """
        try:
            shipPos = self.ship.getPos()
            shipHeading = self.ship.getH()
            
            # Vector to obstacle
            toObstX = obstaclePos.getX() - shipPos.getX()
            toObstY = obstaclePos.getY() - shipPos.getY()
            
            # Get right direction from heading
            headingRad = math.radians(shipHeading)
            rightX = math.cos(headingRad)
            rightY = math.sin(headingRad)
            
            # If obstacle is to our right, turn left; if left, turn right
            side = toObstX * rightX + toObstY * rightY
            
            return -1 if side > 0 else 1
            
        except:
            return 1  # Default to right turn

    def _calculateAvoidanceDestination(self, turnDirection):
        """
        Calculate a new destination to avoid the obstacle.
        Turns away from the obstacle at AI_COLLISION_TURN_ANGLE.
        
        Args:
            turnDirection: 1 for right, -1 for left
        
        Returns: Point3 of new destination
        """
        try:
            shipPos = self.ship.getPos()
            shipHeading = self.ship.getH()
            
            # Turn by avoidance angle
            newHeading = shipHeading + (AI_COLLISION_TURN_ANGLE * turnDirection)
            headingRad = math.radians(newHeading)
            
            # New forward direction
            forwardX = -math.sin(headingRad)
            forwardY = math.cos(headingRad)
            
            # Set destination some distance ahead in new direction
            avoidDist = AI_COLLISION_CHECK_RANGE * 1.5
            newX = shipPos.getX() + forwardX * avoidDist
            newY = shipPos.getY() + forwardY * avoidDist
            
            # Clamp to grid bounds
            newX, newY = self._clampToGridBounds(newX, newY)
            
            return Point3(newX, newY, 0)
            
        except:
            return self._getRandomOceanPos()

    def _performCollisionAvoidance(self):
        """
        Check for imminent collisions and adjust course if needed.
        Called periodically during movement.
        
        Returns: True if avoidance maneuver was triggered
        """
        hasCollision, obstacleInfo = self._checkCollisionAhead()
        
        if not hasCollision:
            return False
        
        obstaclePos, _, dist = obstacleInfo
        
        # Determine turn direction
        turnDir = self._getAvoidanceDirection(obstaclePos)
        
        # Calculate avoidance destination
        avoidDest = self._calculateAvoidanceDestination(turnDir)
        
        # Check if avoidance destination is safe
        if self._isPositionSafe(avoidDest):
            # Re-route to avoidance destination
            currentState = self.getCurrentOrNextState()
            speed = self._getShipSpeed(combatMode=(currentState in ('Combat', 'Attacking', 'Engaged')))
            
            # Store original destination to return to later
            if self._currentDestination and not hasattr(self, '_originalDestination'):
                self._originalDestination = self._currentDestination
            
            self._startMovementTo(avoidDest, speed, onComplete=self._onAvoidanceComplete)
            return True
        
        # If avoidance path is blocked, try the other direction
        turnDir = -turnDir
        avoidDest = self._calculateAvoidanceDestination(turnDir)
        
        if self._isPositionSafe(avoidDest):
            if self._currentDestination and not hasattr(self, '_originalDestination'):
                self._originalDestination = self._currentDestination
            
            currentState = self.getCurrentOrNextState()
            speed = self._getShipSpeed(combatMode=(currentState in ('Combat', 'Attacking', 'Engaged')))
            self._startMovementTo(avoidDest, speed, onComplete=self._onAvoidanceComplete)
            return True
        
        return False

    def _onAvoidanceComplete(self):
        """
        Called when collision avoidance maneuver completes.
        Attempts to resume original course if available.
        """
        if hasattr(self, '_originalDestination') and self._originalDestination:
            originalDest = self._originalDestination
            self._originalDestination = None
            
            # Check if original destination is now reachable
            shipPos = Point3(self.ship.getX(), self.ship.getY(), 0)
            if self._isPathSafe(shipPos, originalDest):
                currentState = self.getCurrentOrNextState()
                speed = self._getShipSpeed(combatMode=(currentState in ('Combat', 'Attacking', 'Engaged')))
                self._startMovementTo(originalDest, speed)
                return
        
        # No original destination or not safe, continue current state behavior
        pass

    def _findSafeDestination(self, preferredDest, maxAttempts=5):
        """
        Find a safe destination, avoiding island collisions and grid bounds.
        If preferred destination is unsafe, find an alternate.
        """
        if not preferredDest:
            return self._getRandomOceanPos()
        
        # First clamp destination to grid bounds
        clampedDest = self._clampDestinationToGrid(preferredDest)
        if not clampedDest:
            return self._getRandomOceanPos()
        
        # Check if clamped destination itself is safe
        if not self._isPositionSafe(clampedDest):
            # Destination is in collision zone, get a random safe point
            for _ in range(maxAttempts):
                altDest = self._getRandomOceanPos()
                if self._isPositionSafe(altDest):
                    return altDest
            return self._getRandomOceanPos()
        
        # Check if path is safe
        shipPos = Point3(self.ship.getX(), self.ship.getY(), 0)
        if self._isPathSafe(shipPos, clampedDest):
            return clampedDest
        
        # Path is blocked, try to find alternate routes
        for _ in range(maxAttempts):
            altDest = self._getRandomOceanPos()
            if self._isPositionSafe(altDest) and self._isPathSafe(shipPos, altDest):
                return altDest
        
        # Fallback: return a random ocean position
        return self._getRandomOceanPos()

    def _getRandomOceanPos(self):
        """
        Get a valid random ocean position within the Cartesian grid bounds.
        Attempts to find a position that doesn't collide with islands.
        """
        self._initWorldRefs()
        
        maxAttempts = 10
        for _ in range(maxAttempts):
            try:
                if self.world:
                    dx, dy = self.air.worldCreator.oceanAreaManager.getRandomOceanPos(
                        self.world.getUniqueId())
                    
                    # Clamp to grid bounds first
                    dx, dy = self._clampToGridBounds(dx, dy)
                    pos = Point3(dx, dy, 0)
                    
                    # Validate position is safe (includes grid bounds check)
                    if self._isPositionSafe(pos):
                        return pos
            except:
                pass
        
        # Fallback: generate random position within grid bounds
        minX, maxX, minY, maxY = self._getGridBounds()
        for _ in range(maxAttempts):
            dx = random.uniform(minX, maxX)
            dy = random.uniform(minY, maxY)
            pos = Point3(dx, dy, 0)
            if self._isPositionSafe(pos):
                return pos
        
        # Final fallback: center of grid (always valid)
        return Point3(0, 0, 0)

    def _getRandomWanderPoint(self):
        """Get a random point for wandering using valid ocean positions."""
        # Use oceanAreaManager for valid ocean positions
        return self._getRandomOceanPos()

    def _getCirclePosition(self, target, radius, angle):
        """Get a position on a circle around the target."""
        if not target:
            return None
        
        try:
            targetPos = target.getPos()
            x = targetPos.getX() + math.cos(angle) * radius
            y = targetPos.getY() + math.sin(angle) * radius
            return Point3(x, y, 0)
        except:
            return None

    def _getMovementDoneName(self):
        """Get unique event name for movement completion."""
        return 'ai-move-done-%d' % self.ship.doId

    def _getRotationDoneName(self):
        """Get unique event name for rotation completion."""
        return 'ai-rotate-done-%d' % self.ship.doId

    def _calculateHeadingTo(self, destination):
        """
        Calculate the heading angle to face a destination.
        Returns heading in degrees.
        """
        if not destination:
            return self.ship.getH()
        
        try:
            shipPos = self.ship.getPos()
            dx = destination.getX() - shipPos.getX()
            dy = destination.getY() - shipPos.getY()
            
            # atan2 gives angle from positive Y axis, clockwise
            # Panda3D heading: 0 = +Y, 90 = -X, 180 = -Y, 270 = +X
            heading = -math.degrees(math.atan2(dx, dy))
            return heading
        except:
            return self.ship.getH()

    def _normalizeAngle(self, angle):
        """Normalize angle to -180 to 180 range."""
        while angle > 180:
            angle -= 360
        while angle < -180:
            angle += 360
        return angle

    def _calculateBroadsideHeading(self, target, preferSide=None):
        """
        Calculate the heading that positions our broadside facing the target.
        
        For broadside combat, we want the target at ±90° from our bow.
        This calculates the ship heading needed to achieve that positioning.
        
        Args:
            target: The target ship to face with broadside
            preferSide: BROADSIDE_LEFT or BROADSIDE_RIGHT preference, or None for nearest
            
        Returns:
            (heading, side) tuple where heading is the desired ship heading
            and side is which broadside will face the target (LEFT or RIGHT)
        """
        if not target:
            return (self.ship.getH(), BROADSIDE_LEFT)
        
        try:
            # Get world positions
            shipPos = self.ship.getPos()
            targetPos = target.getPos()
            
            # Calculate angle from ship to target in world space
            dx = targetPos.getX() - shipPos.getX()
            dy = targetPos.getY() - shipPos.getY()
            angleToTarget = math.degrees(math.atan2(dx, dy))
            
            # To put target at our LEFT broadside (-90°), our heading should be:
            # heading = angleToTarget + 90 (target ends up at -90° relative to us)
            leftBroadsideHeading = self._normalizeAngle(-angleToTarget + 90)
            
            # To put target at our RIGHT broadside (+90°), our heading should be:
            # heading = angleToTarget - 90 (target ends up at +90° relative to us)
            rightBroadsideHeading = self._normalizeAngle(-angleToTarget - 90)
            
            # If side preference given, use it
            if preferSide == BROADSIDE_LEFT:
                return (leftBroadsideHeading, BROADSIDE_LEFT)
            elif preferSide == BROADSIDE_RIGHT:
                return (rightBroadsideHeading, BROADSIDE_RIGHT)
            
            # Otherwise, pick whichever requires less turning
            currentHeading = self.ship.getH()
            leftTurn = abs(self._normalizeAngle(leftBroadsideHeading - currentHeading))
            rightTurn = abs(self._normalizeAngle(rightBroadsideHeading - currentHeading))
            
            if leftTurn <= rightTurn:
                return (leftBroadsideHeading, BROADSIDE_LEFT)
            else:
                return (rightBroadsideHeading, BROADSIDE_RIGHT)
                
        except Exception as e:
            return (self.ship.getH(), BROADSIDE_LEFT)

    def _orientForBroadside(self, target, preferSide=None):
        """
        Rotate the ship to face its broadside at the target.
        
        This immediately sets the ship heading to position the broadside
        toward the target. Call this during combat positioning.
        
        Args:
            target: The target ship to face with broadside
            preferSide: Optional preferred broadside side
            
        Returns:
            The broadside side now facing the target (LEFT or RIGHT)
        """
        if not target:
            return BROADSIDE_LEFT
        
        try:
            heading, side = self._calculateBroadsideHeading(target, preferSide)
            self.ship.setH(heading)
            return side
        except:
            return BROADSIDE_LEFT

    def _getBroadsidePosition(self, target, distance, side=None):
        """
        Calculate a position that allows broadside fire at the target.
        
        Returns a position that is 'distance' units away from target,
        positioned to allow the specified broadside side to fire.
        
        Args:
            target: The target ship
            distance: Desired distance from target
            side: BROADSIDE_LEFT or BROADSIDE_RIGHT, or None for auto
            
        Returns:
            Point3 position for optimal broadside attack
        """
        if not target:
            return None
        
        try:
            targetPos = target.getPos()
            shipPos = self.ship.getPos()
            
            # Get angle from target to our current position
            dx = shipPos.getX() - targetPos.getX()
            dy = shipPos.getY() - targetPos.getY()
            currentAngle = math.atan2(dy, dx)
            
            # Calculate position at the desired distance
            # Move along the same angle but at the specified distance
            newX = targetPos.getX() + math.cos(currentAngle) * distance
            newY = targetPos.getY() + math.sin(currentAngle) * distance
            
            return Point3(newX, newY, 0)
            
        except:
            return None

    def _startMovementTo(self, destination, speed, onComplete=None):
        """
        Start smooth movement to a destination using position intervals.
        
        Uses Panda3D intervals for smooth movement with messenger events
        for completion notification.
        
        Args:
            destination: Point3 target position
            speed: Movement speed (units per second)
            onComplete: Optional callback when movement completes
        """
        if not destination:
            return
        
        self._initWorldRefs()
        
        try:
            # Stop any existing movement
            self._stopMovement()
            
            # Validate and adjust destination to avoid island collisions
            safeDestination = self._findSafeDestination(destination)
            if not safeDestination:
                if onComplete:
                    onComplete()
                return
            
            # Store movement parameters
            self._currentDestination = safeDestination
            self._movementCallback = onComplete
            
            # Calculate distance
            shipPos = self.ship.getPos()
            dx = safeDestination.getX() - shipPos.getX()
            dy = safeDestination.getY() - shipPos.getY()
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < 50:  # Already at destination
                if onComplete:
                    onComplete()
                return
            
            # Create destination node for lookAt
            destNode = NodePath('dest-node-%d' % self.ship.doId)
            destNode.setPos(safeDestination.getX(), safeDestination.getY(), 0)
            
            # Face the destination
            self.ship.lookAt(destNode)
            destNode.removeNode()
            
            # Calculate movement duration based on speed
            moveDuration = distance / max(speed, 1.0)
            
            # Create movement interval using ship's posInterval with oceanGrid reference
            self._moveInterval = self.ship.posInterval(
                moveDuration,
                (safeDestination.getX(), safeDestination.getY(), 0),
                other=self.oceanGrid
            )
            
            # Set up completion event
            self._moveInterval.setDoneEvent(self._getMovementDoneName())
            self.ship.acceptOnce(self._getMovementDoneName(), self._onMovementComplete)
            
            # Start the movement
            self._moveInterval.start()
            
        except Exception as e:
            if onComplete:
                onComplete()

    def _onMovementComplete(self):
        """Called when movement interval completes via messenger event."""
        self._moveInterval = None
        self._currentDestination = None
        self._targetHeading = None
        
        # Safety check: ensure ship is still within grid bounds
        shipX = self.ship.getX()
        shipY = self.ship.getY()
        if not self._isWithinGridBounds(shipX, shipY):
            # Clamp position back into grid
            clampedX, clampedY = self._clampToGridBounds(shipX, shipY)
            self.ship.setPos(clampedX, clampedY, 0)
        
        if self._movementCallback:
            callback = self._movementCallback
            self._movementCallback = None
            callback()

    def _stopMovement(self):
        """Stop current movement interval."""
        if self._moveInterval:
            self._moveInterval.pause()
            self._moveInterval = None
        self.ship.ignore(self._getMovementDoneName())
        self._currentDestination = None
        self._targetHeading = None
        self._movementCallback = None
        self._broadsideTarget = None
        # Also stop the broadside heading update task
        taskMgr.remove(self.ship.uniqueName('broadside-heading'))

    def _isMoving(self):
        """Check if ship is currently moving."""
        return self._moveInterval is not None and self._moveInterval.isPlaying()

    def _startBroadsideMovement(self, destination, speed, target):
        """
        Move toward destination while keeping broadside facing the target.
        
        Unlike _startMovementTo which faces the bow toward destination,
        this method maintains broadside orientation toward the target while
        moving toward the destination position.
        
        Args:
            destination: Point3 target position to move toward
            speed: Movement speed (units per second)
            target: The ship we want to keep our broadside aimed at
        """
        if not destination or not target:
            return
        
        self._initWorldRefs()
        
        try:
            # Stop any existing movement
            self._stopMovement()
            
            # Validate and adjust destination to avoid island collisions
            safeDestination = self._findSafeDestination(destination)
            if not safeDestination:
                return
            
            # Store movement parameters
            self._currentDestination = safeDestination
            self._broadsideTarget = target
            
            # Calculate distance
            shipPos = self.ship.getPos()
            dx = safeDestination.getX() - shipPos.getX()
            dy = safeDestination.getY() - shipPos.getY()
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < 50:  # Already at destination
                return
            
            # Orient for broadside FIRST, before moving
            self._orientForBroadside(target)
            
            # Calculate movement duration based on speed
            moveDuration = distance / max(speed, 1.0)
            
            # Create movement interval - position only, heading already set
            self._moveInterval = self.ship.posInterval(
                moveDuration,
                (safeDestination.getX(), safeDestination.getY(), 0),
                other=self.oceanGrid
            )
            
            # Set up completion event
            self._moveInterval.setDoneEvent(self._getMovementDoneName())
            self.ship.acceptOnce(self._getMovementDoneName(), self._onMovementComplete)
            
            # Start the movement
            self._moveInterval.start()
            
            # Start a task to continuously update heading during movement
            # This keeps the broadside facing the target as we move
            taskMgr.remove(self.ship.uniqueName('broadside-heading'))
            taskMgr.doMethodLater(
                0.2, self._updateBroadsideHeading,
                self.ship.uniqueName('broadside-heading'))
            
        except Exception as e:
            pass

    def _updateBroadsideHeading(self, task):
        """
        Task to continuously update ship heading during broadside movement.
        Keeps the broadside facing the target as the ship moves.
        """
        # Stop if not moving anymore
        if not self._isMoving():
            return Task.done
        
        # Get the broadside target
        target = getattr(self, '_broadsideTarget', None)
        if not target or not self._isValidTarget(target):
            return Task.done
        
        # Re-orient for broadside
        self._orientForBroadside(target)
        
        # Continue until movement completes
        return Task.again

    def _getDistanceToDestination(self):
        """Get distance to current movement destination."""
        if not self._currentDestination:
            return 0
        try:
            return (self.ship.getPos() - self._currentDestination).length()
        except:
            return 0

    def _getBroadsideFacing(self, target):
        """
        Determine which broadside is facing the target.
        Uses AI_CANNON_HEADING_RANGE (45 degrees) from PiratesGlobals.
        
        Returns: BROADSIDE_LEFT (0), BROADSIDE_RIGHT (1), or -1 if neither aligned
        """
        if not target:
            return -1
        
        try:
            # Get relative position of target
            targetPos = target.getPos(self.ship)
            angle = math.degrees(math.atan2(targetPos.getX(), targetPos.getY()))
            
            # Use AI_CANNON_HEADING_RANGE for valid firing arc
            # Left broadside is at -90 degrees, right is at +90 degrees
            headingRange = AI_CANNON_HEADING_RANGE  # 45 degrees
            
            # Left broadside faces targets at roughly -90 degrees
            if -90 - headingRange < angle < -90 + headingRange:
                return BROADSIDE_LEFT
            # Right broadside faces targets at roughly +90 degrees
            elif 90 - headingRange < angle < 90 + headingRange:
                return BROADSIDE_RIGHT
            else:
                return -1  # No good broadside angle
        except:
            return -1

    def _isInCannonRange(self, target):
        """
        Check if target is within AI cannon distance range.
        Uses AI_CANNON_DIST_RANGE (6000) from PiratesGlobals.
        """
        dist = self._getDistanceToTarget(target)
        return dist <= AI_CANNON_DIST_RANGE

    # =========================================================================
    # Combat Actions
    # =========================================================================

    def _attemptBroadside(self, target):
        """
        Attempt to fire a broadside at the target.
        Uses POTCO-authentic timing from CannonGlobals.AI_FIRE_TIME.
        Applies level-based and distance-based damage modifiers.
        """
        if not target or not self._isValidTarget(target):
            return False
        
        currentTime = globalClock.getFrameTime()
        broadsideCooldown = self._getBroadsideCooldown()
        if currentTime - self.lastBroadsideTime < broadsideCooldown:
            return False
        
        dist = self._getDistanceToTarget(target)
        
        # Check cannon distance range
        if dist < AI_MIN_ATTACK_RANGE or dist > AI_CANNON_DIST_RANGE:
            return False
        
        # Check if we have a good broadside angle
        broadsideSide = self._getBroadsideFacing(target)
        if broadsideSide < 0:
            return False
        
        # Calculate damage modifiers for logging/debugging
        distanceMod = self._calculateDamageFalloff(dist)
        levelMod = self._getLevelBasedDamageModifier(target)
        _, damageOutMod = self._getNPCDamageModifiers()
        
        # Fire broadside using the proper AI method
        if self.ship.broadside:
            try:
                if self.ship.broadside.fireAtTarget(target, broadsideSide):
                    self.lastBroadsideTime = currentTime
                    return True
            except Exception as e:
                pass
        
        return False

    def _attemptIndividualCannons(self, target):
        """
        Fire individual deck cannons at the target, simulating crew aboard.
        This fires a salvo of cannons staggered over time for a more realistic
        ship-to-ship combat feel, as if skeleton/navy crew are manning the guns.
        """
        if not target or not self._isValidTarget(target):
            return False
        
        currentTime = globalClock.getFrameTime()
        
        # Check cooldown
        if currentTime - self.lastIndividualCannonTime < AI_INDIVIDUAL_CANNON_FIRE_INTERVAL:
            return False
        
        dist = self._getDistanceToTarget(target)
        
        # Check range - individual cannons have similar range to broadside
        if dist < AI_MIN_ATTACK_RANGE or dist > AI_CANNON_DIST_RANGE:
            return False
        
        # Get the ship's cannons
        if not hasattr(self.ship, 'cannons') or not self.ship.cannons:
            return False
        
        numCannons = len(self.ship.cannons)
        if numCannons == 0:
            return False
        
        try:
            # Get target position for aiming
            targetPos = target.getPos()
            
            # Determine which cannons can fire (based on facing)
            # Get angle to target relative to ship
            shipPos = self.ship.getPos()
            dx = targetPos.getX() - shipPos.getX()
            dy = targetPos.getY() - shipPos.getY()
            angleToTarget = math.degrees(math.atan2(dx, dy))
            shipHeading = self.ship.getH()
            relativeAngle = self._normalizeAngle(angleToTarget - shipHeading)
            
            # Determine which side can fire
            # Left side: target at roughly -90 degrees
            # Right side: target at roughly +90 degrees
            # Front/rear cannons: target at 0 or 180 degrees
            canFire = []
            for i, cannon in enumerate(self.ship.cannons):
                # All deck cannons can potentially fire if target is in a reasonable arc
                # Front cannons (chase guns) fire forward, others fire broadside
                if abs(relativeAngle) < 60:  # Front arc
                    canFire.append(i)
                elif abs(relativeAngle) > 120:  # Rear arc
                    canFire.append(i)
                elif relativeAngle < 0 and abs(relativeAngle + 90) < 60:  # Left broadside
                    canFire.append(i)
                elif relativeAngle > 0 and abs(relativeAngle - 90) < 60:  # Right broadside
                    canFire.append(i)
            
            if not canFire:
                return False
            
            # Pick cannons to fire (up to salvo size)
            import random
            salvoSize = min(AI_INDIVIDUAL_CANNON_SALVO_SIZE, len(canFire))
            cannonsToFire = random.sample(canFire, salvoSize)
            
            # Fire the cannons with staggered timing
            for i, cannonIndex in enumerate(cannonsToFire):
                delay = i * 0.3  # Stagger shots
                taskMgr.doMethodLater(
                    delay, 
                    self._fireIndividualCannon,
                    self.ship.uniqueName('individual-cannon-%d' % cannonIndex),
                    extraArgs=[target, cannonIndex, dist]
                )
            
            self.lastIndividualCannonTime = currentTime
            return True
            
        except Exception as e:
            return False

    def _fireIndividualCannon(self, target, cannonIndex, dist):
        """
        Fire a single cannon at the target and apply damage.
        Uses the actual DistributedShipCannonAI to trigger visual effects on clients.
        """
        if not target or not self._isValidTarget(target):
            return
        
        try:
            # Get the actual cannon distributed object
            if cannonIndex < len(self.ship.cannons):
                cannon = self.ship.cannons[cannonIndex]
                
                # Get target position with some spread for realism
                import random
                targetPos = target.getPos()
                spreadX = random.gauss(0, 15)
                spreadY = random.gauss(0, 15)
                spreadZ = random.gauss(0, 5)
                
                from panda3d.core import Point3
                aimPos = Point3(
                    targetPos.getX() + spreadX,
                    targetPos.getY() + spreadY,
                    targetPos.getZ() + spreadZ if hasattr(targetPos, 'getZ') else spreadZ
                )
                
                # Fire the cannon (sends visual effect to clients)
                if hasattr(cannon, 'fireAtPosition'):
                    cannon.fireAtPosition(aimPos)
            
            # Calculate accuracy based on distance
            accuracy = max(0.3, 1.0 - (dist / AI_CANNON_DIST_RANGE) * 0.5)
            
            import random
            if random.random() > accuracy:
                # Miss - no damage but visual was still fired
                return
            
            # Calculate damage
            baseDamage = AI_INDIVIDUAL_CANNON_DAMAGE
            levelMod = self._getLevelBasedDamageModifier(target)
            distMod = self._calculateDamageFalloff(dist)
            _, damageOutMod = self._getNPCDamageModifiers()
            
            totalDamage = int(baseDamage * levelMod * distMod * damageOutMod)
            
            if totalDamage > 0:
                # Apply damage to target
                if hasattr(target, 'takeDamage'):
                    target.takeDamage(self.ship.doId, totalDamage, 0)
                elif hasattr(target, 'hull') and target.hull:
                    hull = target.hull
                    if hasattr(hull, 'takeDamage'):
                        hull.takeDamage(self.ship.doId, totalDamage, 0)
        except:
            pass

    # =========================================================================
    # State Handlers
    # =========================================================================

    def enterOff(self):
        self._stopAllTasks()

    def exitOff(self):
        pass

    def enterNeutral(self):
        self._stopAllTasks()

    def exitNeutral(self):
        pass

    def enterSpawn(self):
        # After spawning, transition to patrol
        taskMgr.doMethodLater(2.0, lambda t: self.request('Patrol'), 
                             self.ship.uniqueName('spawn-to-patrol'))

    def exitSpawn(self):
        taskMgr.remove(self.ship.uniqueName('spawn-to-patrol'))

    def enterAdrift(self):
        self._stopAllTasks()

    def exitAdrift(self):
        pass

    def enterAISteering(self, avId):
        pass

    def exitAISteering(self):
        pass

    def enterDocked(self):
        self._stopAllTasks()

    def exitDocked(self):
        pass

    def enterPinned(self):
        self._stopAllTasks()

    def exitPinned(self):
        pass

    def enterEnsnared(self):
        self._stopAllTasks()

    def exitEnsnared(self):
        pass

    def enterShoveOff(self):
        pass

    def exitShoveOff(self):
        pass

    def enterSinking(self):
        self._stopAllTasks()
        self.targetShip = None

        def _shipSunk(task):
            self.ship.requestDelete()
            return Task.done

        self._sinkingTask = taskMgr.doMethodLater(60, _shipSunk, 
                                                   self.ship.uniqueName('shipSunk'))
    def exitSinking(self):
        if self._sinkingTask is not None:
            taskMgr.remove(self._sinkingTask)
            self._sinkingTask = None

    def enterSunk(self):
        self._stopAllTasks()

    def exitSunk(self):
        pass

    def enterRecoverFromSunk(self):
        pass

    def exitRecoverFromSunk(self):
        pass

    def enterInBoardingPosition(self):
        self._stopAllTasks()

    def exitInBoardingPosition(self):
        pass

    # =========================================================================
    # Flagship States - Crippling, Grappling, and Boarding
    # =========================================================================

    def enterWaitingForGrapple(self):
        """
        Flagship has been crippled (hull at 0).
        Players have 5 minutes to grapple and board before it sinks.
        """
        self._stopAllTasks()
        self.targetShip = None
        
        # Set up the 5-minute timeout
        def _crippledTimeout(task):
            # Time's up - ship sinks without being boarded
            if self.ship:
                self.request('Sinking')
            return Task.done
        
        self._crippledTimeoutTask = taskMgr.doMethodLater(
            FlagshipGlobals.FLAGSHIP_CRIPPLED_TIMEOUT,
            _crippledTimeout,
            self.ship.uniqueName('crippled-timeout'))

    def exitWaitingForGrapple(self):
        if hasattr(self, '_crippledTimeoutTask') and self._crippledTimeoutTask:
            taskMgr.remove(self._crippledTimeoutTask)
            self._crippledTimeoutTask = None

    def enterGrappleLerping(self):
        """
        Flagship is being pulled into boarding position by grappling hooks.
        """
        self._stopAllTasks()
        # The actual lerping is handled by the client/DC field updates

    def exitGrappleLerping(self):
        pass

    def enterInPosition(self):
        """
        Flagship is in boarding position, ready to be boarded.
        Captain can order crew to board or parley.
        """
        self._stopAllTasks()

    def exitInPosition(self):
        pass

    def enterBoarded(self):
        """
        Pirates have boarded the flagship and are fighting the crew.
        Spawn waves of enemies based on flagship type.
        """
        self._stopAllTasks()
        
        # Get crew composition for this flagship
        shipClass = self.ship.getShipClass() if hasattr(self.ship, 'getShipClass') else None
        team = self.ship.getTeam() if hasattr(self.ship, 'getTeam') else None
        
        crewConfig = FlagshipGlobals.getFlagshipCrew(shipClass, team)
        crewSize = FlagshipGlobals.getFlagshipCrewSize(shipClass)
        minLevel, maxLevel = FlagshipGlobals.getFlagshipEnemyLevels(shipClass)
        
        # Store for spawn logic (actual spawning done by boarding manager)
        self._flagshipCrewConfig = crewConfig
        self._flagshipCrewSize = crewSize
        self._flagshipEnemyLevelRange = (minLevel, maxLevel)
        self._flagshipWaveCount = FlagshipGlobals.FLAGSHIP_WAVE_COUNT
        self._currentWave = 0

    def exitBoarded(self):
        pass

    def enterDefeated(self):
        """
        All crew on the flagship has been defeated.
        Loot is distributed and ship will sink.
        """
        self._stopAllTasks()
        
        # Roll for special loot
        shipClass = self.ship.getShipClass() if hasattr(self.ship, 'getShipClass') else None
        specialLoot = FlagshipGlobals.getFlagshipSpecialLoot(shipClass)
        
        self._droppedSpecialLoot = []
        for lootType in specialLoot:
            chance = FlagshipGlobals.getSpecialLootChance(lootType)
            if random.random() < chance:
                self._droppedSpecialLoot.append(lootType)
        
        # Schedule transition to sinking after loot collection time
        def _defeatToSink(task):
            if self.ship:
                self.request('Sinking')
            return Task.done
        
        self._defeatSinkTask = taskMgr.doMethodLater(
            30.0,  # 30 seconds to collect loot
            _defeatToSink,
            self.ship.uniqueName('defeat-to-sink'))

    def exitDefeated(self):
        if hasattr(self, '_defeatSinkTask') and self._defeatSinkTask:
            taskMgr.remove(self._defeatSinkTask)
            self._defeatSinkTask = None

    def enterParley(self):
        """
        Captain chose to parley - ship sinks but loot is still gained (TLOPO behavior).
        """
        self._stopAllTasks()
        
        # Give minimal loot, then sink
        def _parleyToSink(task):
            if self.ship:
                self.request('Sinking')
            return Task.done
        
        self._parleySinkTask = taskMgr.doMethodLater(
            5.0,  # Brief delay before sinking
            _parleyToSink,
            self.ship.uniqueName('parley-to-sink'))

    def exitParley(self):
        if hasattr(self, '_parleySinkTask') and self._parleySinkTask:
            taskMgr.remove(self._parleySinkTask)
            self._parleySinkTask = None

    # =========================================================================
    # Flagship Utility Methods
    # =========================================================================

    def isFlagship(self):
        """Check if this ship is a flagship."""
        if hasattr(self.ship, 'isFlagship'):
            return self.ship.isFlagship
        shipClass = self.ship.getShipClass() if hasattr(self.ship, 'getShipClass') else None
        return FlagshipGlobals.isFlagship(shipClass)

    def getFlagshipCrewMember(self):
        """Pick a random crew member type for this flagship."""
        shipClass = self.ship.getShipClass() if hasattr(self.ship, 'getShipClass') else None
        team = self.ship.getTeam() if hasattr(self.ship, 'getTeam') else None
        return FlagshipGlobals.pickCrewMember(shipClass, team)

    def spawnNextFlagshipWave(self):
        """
        Spawn the next wave of enemies on the flagship.
        Called by the boarding manager.
        """
        if not hasattr(self, '_currentWave'):
            return []
        
        if self._currentWave >= self._flagshipWaveCount:
            return []  # No more waves
        
        self._currentWave += 1
        
        crewToSpawn = []
        for _ in range(self._flagshipCrewSize):
            avatarType = self.getFlagshipCrewMember()
            if avatarType:
                minLevel, maxLevel = self._flagshipEnemyLevelRange
                level = random.randint(minLevel, maxLevel)
                crewToSpawn.append((avatarType, level))
        
        return crewToSpawn

    def getDroppedSpecialLoot(self):
        """Get list of special loot items that dropped from this flagship."""
        return getattr(self, '_droppedSpecialLoot', [])

    def enterPutAway(self):
        self._stopAllTasks()

    def exitPutAway(self):
        pass

    # =========================================================================
    # PathFollow (Legacy) - Simple path following
    # =========================================================================

    def getPathFollowDoneName(self):
        return 'path-follow-done-%d' % self.ship.doId

    def enterPathFollow(self):
        self._followPath()

    def _followPath(self):
        self._initWorldRefs()
        
        followSpeed = 800.0
        dx, dy = self.air.worldCreator.oceanAreaManager.getRandomOceanPos(
            self.world.getUniqueId())

        destNode = NodePath('dest-node-%d' % self.ship.doId)
        destNode.setPos(dx, dy, 0)

        self.ship.setSailAnimState('Idle')
        self.ship.lookAt(destNode)

        self._pathFollowInterval = self.ship.posInterval(
            followSpeed, (dx, dy, 0), other=self.oceanGrid)
        self._pathFollowInterval.setDoneEvent(self.getPathFollowDoneName())

        self.acceptOnce(self.getPathFollowDoneName(), self._pathFollowDone)
        self._pathFollowInterval.start()

    def _pathFollowDone(self):
        self._followPath()

    def exitPathFollow(self):
        self._stopMovement()
        if self._pathFollowInterval is not None:
            self._pathFollowInterval.finish()
            self._pathFollowInterval = None

    # =========================================================================
    # Patrol - Intelligent patrol behavior
    # =========================================================================

    def enterPatrol(self):
        self._initWorldRefs()
        # Set home position to a valid ocean location
        self.homePos = self._getRandomOceanPos()
        self.ship.setSailAnimState('Idle')
        
        # Generate patrol waypoints in a circuit
        self._generatePatrolWaypoints()
        self._currentWaypointIndex = 0
        
        # Start despawn check for idle ships
        self._startDespawnCheck()
        
        self._aiUpdateTask = taskMgr.doMethodLater(
            AI_UPDATE_INTERVAL, self._patrolUpdate, 
            self.ship.uniqueName('patrol-update'))

    def _generatePatrolWaypoints(self):
        """Generate a set of patrol waypoints using valid ocean positions."""
        self._patrolWaypoints = []
        numWaypoints = random.randint(4, 8)
        
        # Generate waypoints using valid ocean positions
        for i in range(numWaypoints):
            waypoint = self._getRandomOceanPos()
            self._patrolWaypoints.append(waypoint)

    def _patrolUpdate(self, task):
        # Safety check: if ship is outside grid, immediately move it back
        shipX = self.ship.getX()
        shipY = self.ship.getY()
        if not self._isWithinGridBounds(shipX, shipY):
            clampedX, clampedY = self._clampToGridBounds(shipX, shipY)
            self.ship.setPos(clampedX, clampedY, 0)
            # Stop current movement and head toward center
            self._stopMovement()
            self._startMovementTo(self._getDirectionAwayFromEdge(), self._getShipSpeed())
            return Task.again
        
        # Check for imminent collisions and avoid
        if self._performCollisionAvoidance():
            return Task.again  # Collision avoidance triggered, skip other updates
        
        # Check for enemies
        enemy, dist = self._findNearestEnemy()
        if enemy and dist < AI_DETECTION_RANGE:
            self._stopMovement()  # Break current movement to engage
            self.targetShip = enemy
            self.targetDoId = enemy.doId
            self.request('Combat')
            return Task.done
        
        # Check if we were recently attacked
        if self.threatList:
            target = self._selectBestTarget()
            if target:
                self._stopMovement()  # Break current movement to engage
                self.targetShip = target
                self.targetDoId = target.doId
                self.request('Combat')
                return Task.done
        
        # Check if approaching grid edge - turn back
        if self._isApproachingGridEdge() and not self._isMoving():
            turnBackDest = self._getDirectionAwayFromEdge()
            self._startMovementTo(turnBackDest, self._getShipSpeed(combatMode=False))
            return Task.again
        
        # Continue patrol - start movement if not already moving
        if self._patrolWaypoints and not self._isMoving():
            destination = self._patrolWaypoints[self._currentWaypointIndex]
            dist = (self.ship.getPos() - destination).length()
            
            if dist < 200:  # Reached waypoint
                self._currentWaypointIndex = (self._currentWaypointIndex + 1) % len(self._patrolWaypoints)
                destination = self._patrolWaypoints[self._currentWaypointIndex]
            
            self._startMovementTo(destination, self._getShipSpeed(combatMode=False))
        
        return Task.again

    def exitPatrol(self):
        self._stopMovement()
        self._stopDespawnCheck()
        if self._aiUpdateTask:
            taskMgr.remove(self._aiUpdateTask)
            self._aiUpdateTask = None

    # =========================================================================
    # Wander - Random wandering behavior
    # =========================================================================

    def enterWander(self):
        self._initWorldRefs()
        # Set home position to a valid ocean location
        self.homePos = self._getRandomOceanPos()
        self.wanderDestination = self._getRandomWanderPoint()
        self.ship.setSailAnimState('Idle')
        
        # Start despawn check for idle ships
        self._startDespawnCheck()
        
        self._aiUpdateTask = taskMgr.doMethodLater(
            AI_UPDATE_INTERVAL, self._wanderUpdate,
            self.ship.uniqueName('wander-update'))

    def _wanderUpdate(self, task):
        # Safety check: if ship is outside grid, immediately move it back
        shipX = self.ship.getX()
        shipY = self.ship.getY()
        if not self._isWithinGridBounds(shipX, shipY):
            clampedX, clampedY = self._clampToGridBounds(shipX, shipY)
            self.ship.setPos(clampedX, clampedY, 0)
            # Stop current movement and head toward center
            self._stopMovement()
            self._startMovementTo(self._getDirectionAwayFromEdge(), self._getShipSpeed())
            return Task.again
        
        # Check for imminent collisions and avoid
        if self._performCollisionAvoidance():
            return Task.again  # Collision avoidance triggered, skip other updates
        
        # Check for enemies
        enemy, dist = self._findNearestEnemy()
        if enemy and dist < AI_DETECTION_RANGE:
            self._stopMovement()  # Break current movement to engage
            self.targetShip = enemy
            self.targetDoId = enemy.doId
            self.request('Combat')
            return Task.done
        
        # Check if we were recently attacked
        if self.threatList:
            target = self._selectBestTarget()
            if target:
                self._stopMovement()  # Break current movement to engage
                self.targetShip = target
                self.targetDoId = target.doId
                self.request('Combat')
                return Task.done
        
        # Check if approaching grid edge - turn back
        if self._isApproachingGridEdge() and not self._isMoving():
            turnBackDest = self._getDirectionAwayFromEdge()
            self._startMovementTo(turnBackDest, self._getShipSpeed(combatMode=False))
            return Task.again
        
        # Continue wandering - start movement if not already moving
        if self.wanderDestination and not self._isMoving():
            dist = (self.ship.getPos() - self.wanderDestination).length()
            
            if dist < 200:  # Reached destination
                self.wanderDestination = self._getRandomWanderPoint()
            
            self._startMovementTo(self.wanderDestination, self._getShipSpeed(combatMode=False))
        
        return Task.again

    def exitWander(self):
        self._stopMovement()
        self._stopDespawnCheck()
        if self._aiUpdateTask:
            taskMgr.remove(self._aiUpdateTask)
            self._aiUpdateTask = None

    # =========================================================================
    # Combat - Main combat state
    # =========================================================================

    def enterCombat(self):
        self.ship.setSailAnimState('Idle')
        
        # Update last combat time for despawn tracking
        self._updateLastCombatTime()
        
        # Choose initial combat behavior - delay to avoid nested FSM transition
        def _selectCombatBehavior(task):
            if self.targetShip:
                self.request('CircleAttack')
            else:
                self.request('AttackChase')
            return task.done
        
        taskMgr.doMethodLater(0.1, _selectCombatBehavior, 
                              self.ship.uniqueName('combat-select'))

    def exitCombat(self):
        taskMgr.remove(self.ship.uniqueName('combat-select'))

    # =========================================================================
    # AttackChase - Pursuing a target
    # =========================================================================

    def enterAttackChase(self):
        self.ship.setSailAnimState('Idle')
        
        # Update last combat time for despawn tracking
        self._updateLastCombatTime()
        
        self._aiUpdateTask = taskMgr.doMethodLater(
            AI_UPDATE_INTERVAL, self._chaseUpdate,
            self.ship.uniqueName('chase-update'))

    def _chaseUpdate(self, task):
        # Check for imminent collisions with non-targets and avoid
        hasCollision, obstacleInfo = self._checkCollisionAhead()
        if hasCollision and obstacleInfo:
            obstaclePos, _, _ = obstacleInfo
            # Only avoid if it's not our target
            if self.targetShip:
                targetPos = self.targetShip.getPos()
                obstacleDist = (obstaclePos - targetPos).length()
                if obstacleDist > 100:  # Not our target, avoid it
                    if self._performCollisionAvoidance():
                        return Task.again
        
        # Validate target
        if not self._isValidTarget(self.targetShip):
            self.targetShip = self._selectBestTarget()
            if not self.targetShip:
                self.request('Patrol')
                return Task.done
        
        dist = self._getDistanceToTarget(self.targetShip)
        
        # Check if too far
        if dist > AI_MAX_CHASE_RANGE:
            self.targetShip = None
            self.targetDoId = 0
            self.request('Patrol')
            return Task.done
        
        # Check if in attack range
        if AI_MIN_ATTACK_RANGE < dist < AI_ATTACK_RANGE:
            self.request('CircleAttack')
            return Task.done
        
        # Check health for fleeing (level-aware)
        if self._shouldFlee():
            self.request('Flee')
            return Task.done
        
        # Chase target - ALWAYS head toward target aggressively
        # Turn to face target first, then move toward them
        self._turnTowardTarget(self.targetShip)
        
        targetPos = self.targetShip.getPos()
        # Continuously update movement toward target - don't wait for movement to complete
        # Stop current movement and recalculate path to target's current position
        if self._isMoving():
            # Check if target moved significantly from our destination
            if self._currentDestination:
                destToTarget = (Point3(targetPos) - self._currentDestination).length()
                if destToTarget > 200:  # Target moved, update course
                    self._stopMovement()
                    self._startMovementTo(Point3(targetPos), self._getShipSpeed(combatMode=True) * 1.5)
        else:
            # Not moving, start chasing at increased speed
            self._startMovementTo(Point3(targetPos), self._getShipSpeed(combatMode=True) * 1.5)
        
        # Try opportunistic broadside while chasing
        self._attemptBroadside(self.targetShip)
        
        # Also fire individual deck cannons while chasing (crew fires at will)
        self._attemptIndividualCannons(self.targetShip)
        
        return Task.again

    def exitAttackChase(self):
        self._stopMovement()
        if self._aiUpdateTask:
            taskMgr.remove(self._aiUpdateTask)
            self._aiUpdateTask = None

    # =========================================================================
    # CircleAttack - Circling for broadside attacks (POTCO-style)
    # =========================================================================

    def enterCircleAttack(self):
        self.ship.setSailAnimState('Idle')
        
        # Update last combat time for despawn tracking
        self._updateLastCombatTime()
        
        # Choose circle direction based on which broadside is healthier/loaded
        self.circleDirection = random.choice([1, -1])
        
        # Start with angle toward target
        if self.targetShip:
            try:
                targetPos = self.targetShip.getPos()
                shipPos = self.ship.getPos()
                self.circleAngle = math.atan2(
                    shipPos.getY() - targetPos.getY(),
                    shipPos.getX() - targetPos.getX()
                )
            except:
                self.circleAngle = 0
        
        self._aiUpdateTask = taskMgr.doMethodLater(
            AI_UPDATE_INTERVAL, self._circleAttackUpdate,
            self.ship.uniqueName('circle-attack-update'))

    def _circleAttackUpdate(self, task):
        # Check for imminent collisions with non-targets and avoid
        hasCollision, obstacleInfo = self._checkCollisionAhead()
        if hasCollision and obstacleInfo:
            obstaclePos, _, _ = obstacleInfo
            # Only avoid if it's not our target (we want to get close to target)
            if self.targetShip:
                targetPos = self.targetShip.getPos()
                obstacleDist = (obstaclePos - targetPos).length()
                if obstacleDist > 100:  # Not our target, avoid it
                    if self._performCollisionAvoidance():
                        return Task.again
        
        # Validate target
        if not self._isValidTarget(self.targetShip):
            self.targetShip = self._selectBestTarget()
            if not self.targetShip:
                self.request('Patrol')
                return Task.done
        
        dist = self._getDistanceToTarget(self.targetShip)
        
        # Check if target fled
        if dist > AI_MAX_CHASE_RANGE:
            self.request('AttackChase')
            return Task.done
        
        # Check health for fleeing (level-aware)
        if self._shouldFlee():
            self.request('Flee')
            return Task.done
        
        # Calculate optimal attack distance
        optimalDist = AI_ATTACK_RANGE * 0.6  # Optimal broadside range
        if dist < AI_MIN_ATTACK_RANGE:
            optimalDist = AI_MIN_ATTACK_RANGE * 1.5
        elif dist > AI_ATTACK_RANGE:
            optimalDist = AI_ATTACK_RANGE * 0.8
        
        # Orient ship for broadside attack - rotate to face broadside at target
        # This is the KEY fix: ship rotates so its SIDE faces the target
        broadsideSide = self._orientForBroadside(self.targetShip)
        
        # If we're not at optimal distance, move to get there
        # But maintain broadside orientation while moving
        if not self._isMoving():
            if dist > optimalDist * 1.2:
                # Too far - move closer while maintaining broadside angle
                # Move perpendicular to target (parallel path) to close distance
                broadsidePos = self._getBroadsidePosition(self.targetShip, optimalDist)
                if broadsidePos:
                    self._startBroadsideMovement(broadsidePos, self._getShipSpeed(combatMode=True), self.targetShip)
            elif dist < AI_MIN_ATTACK_RANGE:
                # Too close - back off
                broadsidePos = self._getBroadsidePosition(self.targetShip, optimalDist)
                if broadsidePos:
                    self._startBroadsideMovement(broadsidePos, self._getShipSpeed(combatMode=True), self.targetShip)
            else:
                # At good range - circle slowly while keeping broadside aimed
                circleSpeed = 0.03  # Slower circling for better aim
                self.circleAngle += circleSpeed * self.circleDirection
                circlePos = self._getCirclePosition(self.targetShip, dist, self.circleAngle)
                if circlePos:
                    self._startBroadsideMovement(circlePos, self._getShipSpeed(combatMode=True) * 0.5, self.targetShip)
        
        # Attempt broadside - should now be properly aligned
        if self._attemptBroadside(self.targetShip):
            # Occasionally switch circle direction after firing
            if random.random() < 0.3:
                self.circleDirection *= -1
        
        # Also fire individual deck cannons (simulated crew aboard)
        # This happens independently of broadsides for continuous fire
        self._attemptIndividualCannons(self.targetShip)
        
        # Occasionally switch to chase if target is getting away
        if dist > AI_ATTACK_RANGE * 1.5 and random.random() < 0.1:
            self.request('AttackChase')
            return Task.done
        
        return Task.again

    def exitCircleAttack(self):
        self._stopMovement()
        if self._aiUpdateTask:
            taskMgr.remove(self._aiUpdateTask)
            self._aiUpdateTask = None

    # =========================================================================
    # Flee - Retreating from combat
    # =========================================================================

    def enterFlee(self):
        self.ship.setSailAnimState('Idle')
        
        # Update last combat time for despawn tracking (fleeing is still combat)
        self._updateLastCombatTime()
        
        # Calculate flee direction (away from threats)
        self._calculateFleeDestination()
        
        self._aiUpdateTask = taskMgr.doMethodLater(
            AI_UPDATE_INTERVAL, self._fleeUpdate,
            self.ship.uniqueName('flee-update'))

    def _calculateFleeDestination(self):
        """Calculate a destination away from all threats using valid ocean positions."""
        shipPos = self.ship.getPos()
        
        # Average position of all threats
        threatX, threatY = 0, 0
        threatCount = 0
        
        for doId in self.threatList:
            threat = self.air.doId2do.get(doId)
            if threat:
                threatPos = threat.getPos()
                threatX += threatPos.getX()
                threatY += threatPos.getY()
                threatCount += 1
        
        if threatCount > 0:
            threatX /= threatCount
            threatY /= threatCount
            
            # Get a valid ocean position and bias it away from threats
            oceanPos = self._getRandomOceanPos()
            
            # Check if this ocean position is generally away from the threat
            # If not, try a few more times to find a better flee point
            for _ in range(3):
                toOcean = (oceanPos.getX() - shipPos.getX(), oceanPos.getY() - shipPos.getY())
                toThreat = (threatX - shipPos.getX(), threatY - shipPos.getY())
                
                # Dot product - if negative, we're going away from threat
                dot = toOcean[0] * toThreat[0] + toOcean[1] * toThreat[1]
                if dot < 0:
                    break  # Good flee direction
                oceanPos = self._getRandomOceanPos()
            
            self.wanderDestination = oceanPos
        else:
            # Random flee direction using valid ocean position
            self.wanderDestination = self._getRandomOceanPos()

    def _fleeUpdate(self, task):
        # Check for imminent collisions and avoid (even while fleeing)
        if self._performCollisionAvoidance():
            return Task.again  # Collision avoidance triggered
        
        # Check if health recovered enough to fight (level-aware)
        # Ships only return to combat if healthy enough based on situation
        if not self._shouldFlee():
            # Clear threats and return to patrol
            self.threatList.clear()
            self.targetShip = None
            self.request('Patrol')
            return Task.done
        
        # Check if we've escaped
        nearestThreatDist = float('inf')
        for doId in self.threatList:
            threat = self.air.doId2do.get(doId)
            if threat:
                dist = self._getDistanceToTarget(threat)
                if dist < nearestThreatDist:
                    nearestThreatDist = dist
        
        if nearestThreatDist > AI_MAX_CHASE_RANGE:
            self.threatList.clear()
            self.targetShip = None
            self.request('Patrol')
            return Task.done
        
        # Continue fleeing - start movement if not already moving
        if self.wanderDestination and not self._isMoving():
            dist = (self.ship.getPos() - self.wanderDestination).length()
            if dist < 200:
                self._calculateFleeDestination()
            
            # Use boost/fleeing speed for emergency retreat
            self._startMovementTo(self.wanderDestination, self._getShipSpeed(fleeing=True))
        
        return Task.again

    def exitFlee(self):
        self._stopMovement()
        if self._aiUpdateTask:
            taskMgr.remove(self._aiUpdateTask)
            self._aiUpdateTask = None

    def enterScriptedMovement(self):
        pass

    def exitScriptedMovement(self):
        pass
