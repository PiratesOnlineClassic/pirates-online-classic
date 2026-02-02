"""
FlagshipGlobals - Flagship Configuration and Data

Based on original POTCO flagship specifications from:
https://piratesonline.fandom.com/wiki/Flagships

Flagships are special enemy ships that must be:
1. Crippled (reduced to 0 hull HP)
2. Grappled using grappling hooks (ammo type 8)
3. Boarded and crew defeated

Special drops:
- EITC Flagships: Beckett's Spyglass
- Navy Flagships: Norrington's Spyglass
- EITC Defiance / Navy Formidable: The Sea Beast Vanquisher
- French/Spanish Undead: Bottle Rocket Cannon Ram
"""

from pirates.ship import ShipGlobals
from pirates.ship import ShipBalance
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PiratesGlobals


# ============================================================================
# Flagship Timing Constants
# ============================================================================
FLAGSHIP_CRIPPLED_TIMEOUT = 300.0  # 5 minutes to board after crippling
FLAGSHIP_GRAPPLE_PULL_TIME = 8.0   # Time to pull ship into boarding position
FLAGSHIP_BOARDING_PREP_TIME = 10.0 # Time crew has to prepare before boarding
FLAGSHIP_WAVE_COUNT = 2            # Number of enemy waves on flagship


# ============================================================================
# Flagship Combat Balance (references ShipBalance for NPC modifiers)
# ============================================================================

def getFlagshipArmorModifier():
    """
    Get armor modifier for flagships.
    Uses NPCArmorModifier from ShipBalance as base.
    Flagships have slightly more armor than regular NPCs.
    """
    baseArmor = ShipBalance.NPCArmorModifier.getValue()
    return baseArmor * 1.25  # 25% more armor for flagships


def getFlagshipDamageModifiers():
    """
    Get damage modifiers for flagships.
    Uses NPCDamageIn/Out from ShipBalance as base.
    
    Returns:
        tuple: (damageIn, damageOut) multipliers
    """
    damageIn = ShipBalance.NPCDamageIn.getValue()
    damageOut = ShipBalance.NPCDamageOut.getValue()
    # Flagships deal slightly more damage
    return (damageIn, damageOut * 1.15)


def getFlagshipRepairRate():
    """
    Get repair rate for flagships (if they have repair capability).
    Flagships repair slower than player ships.
    """
    baseRate = ShipBalance.RepairRate.getValue()
    return baseRate * 0.5  # Half repair rate


# ============================================================================
# Flagship Ship Classes
# ============================================================================

# EITC Flagships
EITC_FLAGSHIPS = [
    ShipGlobals.EITC_SENTINEL,    # Near Cutthroat Isle and Cuba
    ShipGlobals.EITC_CORVETTE,    # Near Port Royal
    ShipGlobals.EITC_BARRACUDA,   # Near Isla Perdida to Cuba
    # EITC Defiance - Near Raven's Cove (special flagship)
    # Note: EITC_BEHEMOTH used to be a flagship
]

# Navy Flagships
NAVY_FLAGSHIPS = [
    ShipGlobals.NAVY_KINGFISHER,  # Near Isla Perdida
    ShipGlobals.NAVY_MAN_O_WAR,   # Launches at Kingshead, near Ile D'Etable De Porc and Isla De La Avaricia
    ShipGlobals.NAVY_COLOSSUS,    # Launches at Outcast Isle, near Isla Tormenta or Cuba
    # Navy Formidable - Near Padres Del Fuego and Isla Tormenta (special flagship)
    # Note: Navy Bulwark, Greyhound, Vanguard, Centurion used to be flagships
]

# French Undead Flagships (all circle Isla Cangrejos)
FRENCH_UNDEAD_FLAGSHIPS = [
    ShipGlobals.SKEL_SHADOW_CROW_FR,   # French Shadow Crow
    ShipGlobals.SKEL_HELLHOUND_FR,     # French Cerberus  
    ShipGlobals.SKEL_BLOOD_SCOURGE_FR, # French Blood Scourge
]

# Spanish Undead Flagships (all near Cutthroat Isle)
SPANISH_UNDEAD_FLAGSHIPS = [
    ShipGlobals.SKEL_SHADOW_CROW_SP,   # Spanish Shadow Crow
    ShipGlobals.SKEL_HELLHOUND_SP,     # Spanish Cerberus
    ShipGlobals.SKEL_BLOOD_SCOURGE_SP, # Spanish Blood Scourge
]

# All flagship ship classes
ALL_FLAGSHIPS = (
    EITC_FLAGSHIPS + 
    NAVY_FLAGSHIPS + 
    FRENCH_UNDEAD_FLAGSHIPS + 
    SPANISH_UNDEAD_FLAGSHIPS
)

# Legendary/Pirate flagships (special spawning rules)
LEGENDARY_FLAGSHIPS = [
    # Queen Anne's Revenge - Found near Isla Cangrejos, Isla Perdida, and Isla Tormenta
    # Look for alerts as to where she is sailing
]


# ============================================================================
# Flagship Spawn Locations (Island Unique IDs / Area Names)
# ============================================================================

# Location constants for reference (match world creator data)
LOCATION_CUTTHROAT = 'Cutthroat'
LOCATION_PORT_ROYAL = 'PortRoyal'
LOCATION_CUBA = 'Cuba'
LOCATION_ISLA_PERDIDA = 'IslaPerdida'
LOCATION_RAVENS_COVE = 'RavensCove'
LOCATION_KINGSHEAD = 'Kingshead'
LOCATION_ILE_DETABLE = 'IleDEtable'
LOCATION_AVARICIA = 'Avaricia'
LOCATION_OUTCAST_ISLE = 'OutcastIsle'
LOCATION_ISLA_TORMENTA = 'IslaTormenta'
LOCATION_PADRES = 'Padres'
LOCATION_ISLA_CANGREJOS = 'IslaCangrejos'
LOCATION_TORTUGA = 'Tortuga'

# Flagship spawn location data: {shipClass: [list of spawn locations]}
FLAGSHIP_SPAWN_LOCATIONS = {
    # EITC Flagships
    ShipGlobals.EITC_SENTINEL: [LOCATION_CUTTHROAT, LOCATION_CUBA],
    ShipGlobals.EITC_CORVETTE: [LOCATION_PORT_ROYAL],
    ShipGlobals.EITC_BARRACUDA: [LOCATION_ISLA_PERDIDA, LOCATION_CUBA],
    
    # Navy Flagships
    ShipGlobals.NAVY_KINGFISHER: [LOCATION_ISLA_PERDIDA],
    ShipGlobals.NAVY_MAN_O_WAR: [LOCATION_KINGSHEAD, LOCATION_ILE_DETABLE, LOCATION_AVARICIA],
    ShipGlobals.NAVY_COLOSSUS: [LOCATION_OUTCAST_ISLE, LOCATION_ISLA_TORMENTA, LOCATION_CUBA],
    
    # French Undead (all circle Isla Cangrejos)
    ShipGlobals.SKEL_SHADOW_CROW_FR: [LOCATION_ISLA_CANGREJOS],
    ShipGlobals.SKEL_HELLHOUND_FR: [LOCATION_ISLA_CANGREJOS],
    ShipGlobals.SKEL_BLOOD_SCOURGE_FR: [LOCATION_ISLA_CANGREJOS],
    
    # Spanish Undead (all near Cutthroat Isle)
    ShipGlobals.SKEL_SHADOW_CROW_SP: [LOCATION_CUTTHROAT],
    ShipGlobals.SKEL_HELLHOUND_SP: [LOCATION_CUTTHROAT],
    ShipGlobals.SKEL_BLOOD_SCOURGE_SP: [LOCATION_CUTTHROAT],
}


# ============================================================================
# Flagship Crew Compositions
# ============================================================================

# Crew composition defines what enemies spawn when boarding a flagship
# Format: {shipClass: [(AvatarType, weight), ...]}
# Weight determines relative spawn probability

FLAGSHIP_CREW = {
    # EITC Sentinel - Thugs, Grunts, and Assassins
    ShipGlobals.EITC_SENTINEL: [
        (AvatarTypes.Thug, 3),
        (AvatarTypes.Grunt, 3),
        (AvatarTypes.Assassin, 2),
    ],
    
    # EITC Corvette - Thugs and Grunts
    ShipGlobals.EITC_CORVETTE: [
        (AvatarTypes.Thug, 5),
        (AvatarTypes.Grunt, 5),
    ],
    
    # EITC Barracuda - Hired-Guns, Mercenaries and sometimes Thugs
    ShipGlobals.EITC_BARRACUDA: [
        (AvatarTypes.Hiredgun, 4),
        (AvatarTypes.Mercenary, 4),
        (AvatarTypes.Thug, 2),
    ],
    
    # Navy Kingfisher - Veterans, Sergeants, and sometimes Guards
    ShipGlobals.NAVY_KINGFISHER: [
        (AvatarTypes.Veteran, 4),
        (AvatarTypes.Sergeant, 4),
        (AvatarTypes.Guard, 2),
    ],
    
    # Navy Man O' War - Veterans, Officers, Sergeants, and Guards
    ShipGlobals.NAVY_MAN_O_WAR: [
        (AvatarTypes.Veteran, 3),
        (AvatarTypes.Officer, 2),
        (AvatarTypes.Sergeant, 3),
        (AvatarTypes.Guard, 2),
    ],
    
    # Navy Colossus - Veterans, Officers and Sergeants
    ShipGlobals.NAVY_COLOSSUS: [
        (AvatarTypes.Veteran, 4),
        (AvatarTypes.Officer, 3),
        (AvatarTypes.Sergeant, 3),
    ],
    
    # French Undead flagships
    ShipGlobals.SKEL_SHADOW_CROW_FR: [
        (AvatarTypes.FrenchUndeadA, 3),
        (AvatarTypes.FrenchUndeadB, 3),
        (AvatarTypes.FrenchUndeadC, 2),
        (AvatarTypes.FrenchUndeadD, 2),
    ],
    ShipGlobals.SKEL_HELLHOUND_FR: [
        (AvatarTypes.FrenchUndeadA, 2),
        (AvatarTypes.FrenchUndeadB, 3),
        (AvatarTypes.FrenchUndeadC, 3),
        (AvatarTypes.FrenchUndeadD, 2),
    ],
    ShipGlobals.SKEL_BLOOD_SCOURGE_FR: [
        (AvatarTypes.FrenchUndeadA, 2),
        (AvatarTypes.FrenchUndeadB, 2),
        (AvatarTypes.FrenchUndeadC, 3),
        (AvatarTypes.FrenchUndeadD, 3),
    ],
    
    # Spanish Undead flagships  
    ShipGlobals.SKEL_SHADOW_CROW_SP: [
        (AvatarTypes.SpanishUndeadA, 3),
        (AvatarTypes.SpanishUndeadB, 3),
        (AvatarTypes.SpanishUndeadC, 2),
        (AvatarTypes.SpanishUndeadD, 2),
    ],
    ShipGlobals.SKEL_HELLHOUND_SP: [
        (AvatarTypes.SpanishUndeadA, 2),
        (AvatarTypes.SpanishUndeadB, 3),
        (AvatarTypes.SpanishUndeadC, 3),
        (AvatarTypes.SpanishUndeadD, 2),
    ],
    ShipGlobals.SKEL_BLOOD_SCOURGE_SP: [
        (AvatarTypes.SpanishUndeadA, 2),
        (AvatarTypes.SpanishUndeadB, 2),
        (AvatarTypes.SpanishUndeadC, 3),
        (AvatarTypes.SpanishUndeadD, 3),
    ],
}

# Default crew by team for flagships not explicitly defined
DEFAULT_CREW_BY_TEAM = {
    PiratesGlobals.NAVY_TEAM: [
        (AvatarTypes.Guard, 3),
        (AvatarTypes.Sergeant, 4),
        (AvatarTypes.Veteran, 3),
    ],
    PiratesGlobals.TRADING_CO_TEAM: [
        (AvatarTypes.Thug, 3),
        (AvatarTypes.Grunt, 4),
        (AvatarTypes.Hiredgun, 3),
    ],
    PiratesGlobals.UNDEAD_TEAM: [
        (AvatarTypes.EarthUndead[3], 3),
        (AvatarTypes.EarthUndead[4], 4),
        (AvatarTypes.EarthUndead[5], 3),
    ],
    PiratesGlobals.FRENCH_UNDEAD_TEAM: [
        (AvatarTypes.FrenchUndeadA, 3),
        (AvatarTypes.FrenchUndeadB, 3),
        (AvatarTypes.FrenchUndeadC, 2),
        (AvatarTypes.FrenchUndeadD, 2),
    ],
    PiratesGlobals.SPANISH_UNDEAD_TEAM: [
        (AvatarTypes.SpanishUndeadA, 3),
        (AvatarTypes.SpanishUndeadB, 3),
        (AvatarTypes.SpanishUndeadC, 2),
        (AvatarTypes.SpanishUndeadD, 2),
    ],
}


# ============================================================================
# Flagship Crew Size (based on ship class difficulty)
# ============================================================================

# Base crew size per wave
FLAGSHIP_CREW_SIZE = {
    # Smaller flagships
    ShipGlobals.EITC_CORVETTE: 6,
    ShipGlobals.NAVY_KINGFISHER: 6,
    ShipGlobals.SKEL_SHADOW_CROW_FR: 6,
    ShipGlobals.SKEL_SHADOW_CROW_SP: 6,
    
    # Medium flagships
    ShipGlobals.EITC_SENTINEL: 8,
    ShipGlobals.EITC_BARRACUDA: 8,
    ShipGlobals.NAVY_MAN_O_WAR: 8,
    ShipGlobals.SKEL_HELLHOUND_FR: 8,
    ShipGlobals.SKEL_HELLHOUND_SP: 8,
    
    # Large flagships
    ShipGlobals.NAVY_COLOSSUS: 10,
    ShipGlobals.SKEL_BLOOD_SCOURGE_FR: 10,
    ShipGlobals.SKEL_BLOOD_SCOURGE_SP: 10,
}

DEFAULT_CREW_SIZE = 8


# ============================================================================
# Flagship Special Loot
# ============================================================================

# Loot categories
LOOT_BECKETTS_SPYGLASS = 'becketts_spyglass'
LOOT_NORRINGTONS_SPYGLASS = 'norringtons_spyglass'
LOOT_SEA_BEAST_VANQUISHER = 'sea_beast_vanquisher'
LOOT_BOTTLE_ROCKET_RAM = 'bottle_rocket_ram'

# Special drops by ship class
FLAGSHIP_SPECIAL_LOOT = {
    # All EITC flagships can drop Beckett's Spyglass
    ShipGlobals.EITC_SENTINEL: [LOOT_BECKETTS_SPYGLASS],
    ShipGlobals.EITC_CORVETTE: [LOOT_BECKETTS_SPYGLASS],
    ShipGlobals.EITC_BARRACUDA: [LOOT_BECKETTS_SPYGLASS],
    
    # All Navy flagships can drop Norrington's Spyglass
    ShipGlobals.NAVY_KINGFISHER: [LOOT_NORRINGTONS_SPYGLASS],
    ShipGlobals.NAVY_MAN_O_WAR: [LOOT_NORRINGTONS_SPYGLASS],
    ShipGlobals.NAVY_COLOSSUS: [LOOT_NORRINGTONS_SPYGLASS],
    
    # French and Spanish Undead can drop Bottle Rocket Cannon Ram
    ShipGlobals.SKEL_SHADOW_CROW_FR: [LOOT_BOTTLE_ROCKET_RAM],
    ShipGlobals.SKEL_HELLHOUND_FR: [LOOT_BOTTLE_ROCKET_RAM],
    ShipGlobals.SKEL_BLOOD_SCOURGE_FR: [LOOT_BOTTLE_ROCKET_RAM],
    ShipGlobals.SKEL_SHADOW_CROW_SP: [LOOT_BOTTLE_ROCKET_RAM],
    ShipGlobals.SKEL_HELLHOUND_SP: [LOOT_BOTTLE_ROCKET_RAM],
    ShipGlobals.SKEL_BLOOD_SCOURGE_SP: [LOOT_BOTTLE_ROCKET_RAM],
}

# Loot drop chances (0.0 to 1.0)
SPECIAL_LOOT_CHANCES = {
    LOOT_BECKETTS_SPYGLASS: 0.05,      # 5% chance
    LOOT_NORRINGTONS_SPYGLASS: 0.05,   # 5% chance
    LOOT_SEA_BEAST_VANQUISHER: 0.02,   # 2% chance (only from special flagships)
    LOOT_BOTTLE_ROCKET_RAM: 0.08,      # 8% chance
}


# ============================================================================
# Flagship Enemy Level Scaling
# ============================================================================

# Enemy levels scale based on vessel class
# Format: {shipClass: (minLevel, maxLevel)}
FLAGSHIP_ENEMY_LEVELS = {
    # Lower tier
    ShipGlobals.EITC_CORVETTE: (8, 14),
    ShipGlobals.NAVY_KINGFISHER: (10, 16),
    
    # Mid tier
    ShipGlobals.EITC_SENTINEL: (14, 20),
    ShipGlobals.EITC_BARRACUDA: (16, 22),
    ShipGlobals.NAVY_MAN_O_WAR: (16, 22),
    
    # High tier
    ShipGlobals.NAVY_COLOSSUS: (20, 28),
    
    # French Undead (mid-high)
    ShipGlobals.SKEL_SHADOW_CROW_FR: (14, 20),
    ShipGlobals.SKEL_HELLHOUND_FR: (18, 24),
    ShipGlobals.SKEL_BLOOD_SCOURGE_FR: (22, 30),
    
    # Spanish Undead (mid-high)
    ShipGlobals.SKEL_SHADOW_CROW_SP: (14, 20),
    ShipGlobals.SKEL_HELLHOUND_SP: (18, 24),
    ShipGlobals.SKEL_BLOOD_SCOURGE_SP: (22, 30),
}

DEFAULT_ENEMY_LEVELS = (12, 18)


# ============================================================================
# Flagship Captain Data (for special flagships with named captains)
# ============================================================================

# EITC Defiance - Captain Clyne Culpepper (drops Sea Beast Vanquisher)
# Navy Formidable - Captain Benedict Bedford (drops Sea Beast Vanquisher)

FLAGSHIP_CAPTAINS = {
    # 'EITC_DEFIANCE': {
    #     'name': 'Captain Clyne Culpepper',
    #     'special_loot': [LOOT_SEA_BEAST_VANQUISHER, LOOT_BECKETTS_SPYGLASS],
    # },
    # 'NAVY_FORMIDABLE': {
    #     'name': 'Captain Benedict Bedford', 
    #     'special_loot': [LOOT_SEA_BEAST_VANQUISHER, LOOT_NORRINGTONS_SPYGLASS],
    # },
}


# ============================================================================
# Utility Functions
# ============================================================================

def isFlagship(shipClass):
    """Check if a ship class is a flagship"""
    return shipClass in ALL_FLAGSHIPS


def getFlagshipCrew(shipClass, team=None):
    """Get crew composition for a flagship"""
    crew = FLAGSHIP_CREW.get(shipClass)
    if crew:
        return crew
    
    # Fallback to team-based default
    if team is not None:
        return DEFAULT_CREW_BY_TEAM.get(team, DEFAULT_CREW_BY_TEAM[PiratesGlobals.NAVY_TEAM])
    
    return None


def getFlagshipCrewSize(shipClass):
    """Get crew size per wave for a flagship"""
    return FLAGSHIP_CREW_SIZE.get(shipClass, DEFAULT_CREW_SIZE)


def getFlagshipSpawnLocations(shipClass):
    """Get valid spawn locations for a flagship"""
    return FLAGSHIP_SPAWN_LOCATIONS.get(shipClass, [])


def getFlagshipEnemyLevels(shipClass):
    """Get enemy level range for a flagship"""
    return FLAGSHIP_ENEMY_LEVELS.get(shipClass, DEFAULT_ENEMY_LEVELS)


def getFlagshipSpecialLoot(shipClass):
    """Get list of special loot items that can drop from this flagship"""
    return FLAGSHIP_SPECIAL_LOOT.get(shipClass, [])


def getSpecialLootChance(lootType):
    """Get the drop chance for a special loot type"""
    return SPECIAL_LOOT_CHANCES.get(lootType, 0.01)


def getFlagshipTeam(shipClass):
    """Get the team for a flagship based on ship class"""
    if shipClass in EITC_FLAGSHIPS:
        return PiratesGlobals.TRADING_CO_TEAM
    elif shipClass in NAVY_FLAGSHIPS:
        return PiratesGlobals.NAVY_TEAM
    elif shipClass in FRENCH_UNDEAD_FLAGSHIPS:
        return PiratesGlobals.FRENCH_UNDEAD_TEAM
    elif shipClass in SPANISH_UNDEAD_FLAGSHIPS:
        return PiratesGlobals.SPANISH_UNDEAD_TEAM
    return PiratesGlobals.UNDEAD_TEAM


def pickCrewMember(shipClass, team=None):
    """Randomly pick a crew member type based on weights"""
    import random
    
    crew = getFlagshipCrew(shipClass, team)
    if not crew:
        return None
    
    # Weighted random selection
    total_weight = sum(weight for _, weight in crew)
    r = random.uniform(0, total_weight)
    cumulative = 0
    
    for avatarType, weight in crew:
        cumulative += weight
        if r <= cumulative:
            return avatarType
    
    return crew[0][0]  # Fallback
