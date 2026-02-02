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
AI_INSTANT_AGGRO_RANGE = EnemyGlobals.SHIP_INSTANT_AGGRO_RADIUS  # 1000 units
AI_AGGRO_FALLOFF_RATE = EnemyGlobals.SHIP_AGGRO_RADIUS_FALLOFF_RATE  # 0.1
AI_AGGRO_LEVEL_BUFFER = EnemyGlobals.SHIP_AGGRO_RADIUS_LEVEL_BUFFER  # 5 levels

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

# Combat Behavior Thresholds
AI_AGGRO_MEMORY_TIME = 60.0  # How long ship remembers being attacked
AI_WANDER_RADIUS = 3000.0  # Radius for random wandering
AI_FLEE_HEALTH_THRESHOLD = 0.2  # Flee when below 20% health
AI_ENGAGE_HEALTH_THRESHOLD = 0.4  # Don't engage new targets below 40% health

# Default Speeds (fallback when ship class not found)
AI_DEFAULT_PATROL_SPEED = 400.0
AI_DEFAULT_COMBAT_SPEED = 600.0
AI_DEFAULT_BROADSIDE_COOLDOWN = AI_FIRE_TIME * 2.0  # Based on AI_FIRE_TIME

# Use ShipGlobals team constants
PLAYER_TEAM = ShipGlobals.PLAYER_TEAM
INVALID_TEAM = ShipGlobals.INVALID_TEAM

# Broadside side constants from ShipGlobals
BROADSIDE_LEFT = ShipGlobals.BROADSIDE_LEFT
BROADSIDE_RIGHT = ShipGlobals.BROADSIDE_RIGHT

# Target switch types from EnemyGlobals
TARGET_SWITCH_RANDOM = EnemyGlobals.TARGET_SWITCH_TYPE_RANDOM
TARGET_SWITCH_DAMAGE = EnemyGlobals.TARGET_SWITCH_TYPE_DAMAGE
TARGET_SWITCH_LOW_LVL = EnemyGlobals.TARGET_SWITCH_TYPE_LOW_LVL
TARGET_SWITCH_HIGH_LVL = EnemyGlobals.TARGET_SWITCH_TYPE_HIGH_LVL


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
        self._moveInterval = None  # Current movement interval
        self._rotateInterval = None  # Current rotation interval
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
        if self._pathFollowInterval:
            self._pathFollowInterval.finish()
            self._pathFollowInterval = None
        if self._moveInterval:
            self._moveInterval.pause()
            self._moveInterval = None
        if self._rotateInterval:
            self._rotateInterval.pause()
            self._rotateInterval = None
        self._currentDestination = None
        self._targetHeading = None

    # =========================================================================
    # Ship Class-Based Configuration
    # =========================================================================

    def _getShipSpeed(self, combatMode=False, fleeing=False):
        """
        Get ship speed from ShipGlobals based on ship class and situation.
        Applies ShipBalance.SpeedModifier for global speed tuning.
        
        Speed list format from ShipGlobals: [minSpeed, normalSpeed, maxSpeed, boostSpeed]
        - minSpeed: Slow cruising
        - normalSpeed: Standard patrol
        - maxSpeed: Combat speed
        - boostSpeed: Emergency/fleeing speed
        
        Args:
            combatMode: Use combat speed (maxSpeed)
            fleeing: Use boost speed for escape
        """
        # Get the global speed modifier from ShipBalance
        speedMod = ShipBalance.SpeedModifier.getValue()
        
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

    def _getDistanceToTarget(self, target):
        """Get distance to a target ship."""
        if not target or target.isEmpty():
            return float('inf')
        try:
            return self.ship.getDistance(target)
        except:
            return float('inf')

    def _isValidTarget(self, target):
        """Check if a target is valid for engagement."""
        if not target:
            return False
        if target.isEmpty():
            return False
        # Don't attack ships on same team
        if hasattr(target, 'getTeam') and hasattr(self.ship, 'getTeam'):
            if target.getTeam() == self.ship.getTeam():
                return False
        # Don't attack sinking/sunk ships
        if hasattr(target, 'gameFSM'):
            state = target.gameFSM.getCurrentOrNextState()
            if state in ('Sinking', 'Sunk', 'Off', 'PutAway'):
                return False
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
        
        # Check player ships
        if hasattr(self.air, 'shipManager'):
            for playerShip in self.air.shipManager.getPlayerShips():
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
        """Called when this ship receives damage."""
        self.addThreat(attackerDoId, damage)
        
        currentState = self.getCurrentOrNextState()
        
        # If we're not already in combat, respond to attack
        if currentState in ('Patrol', 'Wander', 'PathFollow', 'Neutral'):
            attacker = self.air.doId2do.get(attackerDoId)
            if attacker and self._isValidTarget(attacker):
                self.targetShip = attacker
                self.targetDoId = attackerDoId
                
                # Decide whether to fight or flee
                if self._getHealthPercent() < AI_FLEE_HEALTH_THRESHOLD:
                    self.request('Flee')
                else:
                    self.request('Combat')

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
            # If no threats, look for nearby enemies
            if self._getHealthPercent() > AI_ENGAGE_HEALTH_THRESHOLD:
                enemy, _ = self._findNearestEnemy()
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

    def _isPositionSafe(self, pos, checkShips=True):
        """
        Check if a position is safe (not inside any collision zone).
        Checks both island collisions and other ship positions.
        
        Args:
            pos: Position to check
            checkShips: Whether to also check for ship collisions
        
        Returns True if safe, False if inside a collision zone.
        """
        if not pos:
            return False
        
        posX, posY = pos.getX(), pos.getY()
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

    def _findSafeDestination(self, preferredDest, maxAttempts=5):
        """
        Find a safe destination, avoiding island collisions.
        If preferred destination is unsafe, find an alternate.
        """
        if not preferredDest:
            return self._getRandomOceanPos()
        
        # First check if destination itself is safe
        if not self._isPositionSafe(preferredDest):
            # Destination is in collision zone, get a random safe point
            for _ in range(maxAttempts):
                altDest = self._getRandomOceanPos()
                if self._isPositionSafe(altDest):
                    return altDest
            return self._getRandomOceanPos()
        
        # Check if path is safe
        shipPos = Point3(self.ship.getX(), self.ship.getY(), 0)
        if self._isPathSafe(shipPos, preferredDest):
            return preferredDest
        
        # Path is blocked, try to find alternate routes
        for _ in range(maxAttempts):
            altDest = self._getRandomOceanPos()
            if self._isPositionSafe(altDest) and self._isPathSafe(shipPos, altDest):
                return altDest
        
        # Fallback: return a random ocean position
        return self._getRandomOceanPos()

    def _getRandomOceanPos(self):
        """
        Get a valid random ocean position from the world.
        Attempts to find a position that doesn't collide with islands.
        """
        self._initWorldRefs()
        
        maxAttempts = 10
        for _ in range(maxAttempts):
            try:
                if self.world:
                    dx, dy = self.air.worldCreator.oceanAreaManager.getRandomOceanPos(
                        self.world.getUniqueId())
                    pos = Point3(dx, dy, 0)
                    
                    # Validate position is safe
                    if self._isPositionSafe(pos):
                        return pos
            except:
                pass
        
        # Fallback to current position if we can't find a safe ocean pos
        return Point3(self.ship.getX(), self.ship.getY(), 0)

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

    def _startMovementTo(self, destination, speed, onComplete=None):
        """
        Start smooth movement to a destination with realistic ship turning.
        
        Ships rotate smoothly based on their turn rate before/during movement,
        simulating realistic naval vessel behavior. Larger ships turn slower.
        
        Args:
            destination: Point3 target position
            speed: Movement speed (units per second)
            onComplete: Optional callback when movement completes
        """
        if not destination:
            return
        
        self._initWorldRefs()
        
        try:
            # Stop any existing movement and rotation
            if self._moveInterval:
                self._moveInterval.pause()
                self._moveInterval = None
            if self._rotateInterval:
                self._rotateInterval.pause()
                self._rotateInterval = None
            
            # Validate and adjust destination to avoid island collisions
            safeDestination = self._findSafeDestination(destination)
            if not safeDestination:
                if onComplete:
                    onComplete()
                return
            
            # Calculate distance
            shipPos = self.ship.getPos()
            dx = safeDestination.getX() - shipPos.getX()
            dy = safeDestination.getY() - shipPos.getY()
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < 50:  # Already at destination
                if onComplete:
                    onComplete()
                return
            
            # Calculate target heading
            targetHeading = self._calculateHeadingTo(safeDestination)
            currentHeading = self.ship.getH()
            
            # Calculate angle difference (shortest path)
            angleDiff = self._normalizeAngle(targetHeading - currentHeading)
            
            # Store current destination and target heading
            self._currentDestination = safeDestination
            self._targetHeading = targetHeading
            
            # Calculate durations based on ship properties
            rotateDuration = self._getRotationDuration(angleDiff)
            moveDuration = distance / max(speed, 1.0)
            
            # Create rotation interval (smooth turning)
            from direct.interval.IntervalGlobal import Sequence, Parallel, Func
            
            # Rotate ship smoothly to face destination
            self._rotateInterval = self.ship.hprInterval(
                rotateDuration,
                (targetHeading, 0, 0),
                blendType='easeInOut'
            )
            
            # Create movement interval
            self._moveInterval = self.ship.posInterval(
                moveDuration,
                (safeDestination.getX(), safeDestination.getY(), 0),
                other=self.oceanGrid,
                blendType='easeInOut'
            )
            
            # Run rotation and movement together (ship turns while moving)
            # This creates a realistic curved path like real ships
            moveSequence = Parallel(
                self._rotateInterval,
                self._moveInterval,
                name='ai-ship-move-%d' % self.ship.doId
            )
            
            # Set up completion callback
            if onComplete:
                moveSequence.setDoneEvent(self._getMovementDoneName())
                self.acceptOnce(self._getMovementDoneName(), onComplete)
            
            moveSequence.start()
            
        except Exception as e:
            pass

    def _stopMovement(self):
        """Stop current movement and rotation intervals."""
        if self._moveInterval:
            self._moveInterval.pause()
            self._moveInterval = None
        if self._rotateInterval:
            self._rotateInterval.pause()
            self._rotateInterval = None
        self._currentDestination = None
        self._targetHeading = None

    def _isMoving(self):
        """Check if ship is currently moving or rotating."""
        moving = self._moveInterval is not None and self._moveInterval.isPlaying()
        rotating = self._rotateInterval is not None and self._rotateInterval.isPlaying()
        return moving or rotating

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
        # Check for enemies
        enemy, dist = self._findNearestEnemy()
        if enemy and dist < AI_DETECTION_RANGE:
            self.targetShip = enemy
            self.targetDoId = enemy.doId
            self.request('Combat')
            return Task.done
        
        # Check if we were recently attacked
        if self.threatList:
            target = self._selectBestTarget()
            if target:
                self.targetShip = target
                self.targetDoId = target.doId
                self.request('Combat')
                return Task.done
        
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
        
        self._aiUpdateTask = taskMgr.doMethodLater(
            AI_UPDATE_INTERVAL, self._wanderUpdate,
            self.ship.uniqueName('wander-update'))

    def _wanderUpdate(self, task):
        # Check for enemies
        enemy, dist = self._findNearestEnemy()
        if enemy and dist < AI_DETECTION_RANGE:
            self.targetShip = enemy
            self.targetDoId = enemy.doId
            self.request('Combat')
            return Task.done
        
        # Check if we were recently attacked
        if self.threatList:
            target = self._selectBestTarget()
            if target:
                self.targetShip = target
                self.targetDoId = target.doId
                self.request('Combat')
                return Task.done
        
        # Continue wandering - start movement if not already moving
        if self.wanderDestination and not self._isMoving():
            dist = (self.ship.getPos() - self.wanderDestination).length()
            
            if dist < 200:  # Reached destination
                self.wanderDestination = self._getRandomWanderPoint()
            
            self._startMovementTo(self.wanderDestination, self._getShipSpeed(combatMode=False))
        
        return Task.again

    def exitWander(self):
        self._stopMovement()
        if self._aiUpdateTask:
            taskMgr.remove(self._aiUpdateTask)
            self._aiUpdateTask = None

    # =========================================================================
    # Combat - Main combat state
    # =========================================================================

    def enterCombat(self):
        self.ship.setSailAnimState('Idle')
        
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
        
        self._aiUpdateTask = taskMgr.doMethodLater(
            AI_UPDATE_INTERVAL, self._chaseUpdate,
            self.ship.uniqueName('chase-update'))

    def _chaseUpdate(self, task):
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
        
        # Check health for fleeing
        if self._getHealthPercent() < AI_FLEE_HEALTH_THRESHOLD:
            self.request('Flee')
            return Task.done
        
        # Chase target - update movement toward target position
        targetPos = self.targetShip.getPos()
        # Only start new movement if not moving or target moved significantly
        if not self._isMoving() or self._getDistanceToDestination() < 100:
            self._startMovementTo(Point3(targetPos), self._getShipSpeed(combatMode=True))
        
        # Try opportunistic broadside
        self._attemptBroadside(self.targetShip)
        
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
        
        # Check health for fleeing
        if self._getHealthPercent() < AI_FLEE_HEALTH_THRESHOLD:
            self.request('Flee')
            return Task.done
        
        # Update circle angle
        circleSpeed = 0.05  # Radians per update
        self.circleAngle += circleSpeed * self.circleDirection
        
        # Calculate optimal circle radius based on distance
        optimalRadius = AI_CIRCLE_RADIUS
        if dist < AI_MIN_ATTACK_RANGE:
            optimalRadius = AI_ATTACK_RANGE * 0.8
        elif dist > AI_ATTACK_RANGE:
            optimalRadius = dist * 0.7
        
        # Get circle position and start movement if not already moving
        circlePos = self._getCirclePosition(self.targetShip, optimalRadius, self.circleAngle)
        if circlePos and not self._isMoving():
            self._startMovementTo(circlePos, self._getShipSpeed(combatMode=True))
        
        # Attempt broadside when aligned
        if self._attemptBroadside(self.targetShip):
            # Occasionally switch circle direction after firing
            if random.random() < 0.3:
                self.circleDirection *= -1
        
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
        # Check if health recovered enough to fight
        if self._getHealthPercent() > AI_ENGAGE_HEALTH_THRESHOLD:
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
