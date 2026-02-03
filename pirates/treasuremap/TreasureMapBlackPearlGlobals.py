"""
TreasureMapBlackPearlGlobals - Constants and configuration for the Black Pearl Treasure Map Instance

This module contains all the UIDs, configurations, and mappings needed for the
Black Pearl treasure map instance, including fort pairs, drawbridge mappings,
and collision dictionaries.
"""

# =============================================================================
# Island and Region UIDs
# =============================================================================

# The region UID for the Black Pearl world
BLACKPEARL_REGION_UID = '1171761196.78sdnaik'

# The island UID for Black Pearl Island
BLACKPEARL_ISLAND_UID = '1171761224.13sdnaik'

# =============================================================================
# Fort Configuration
# =============================================================================

# All fort UIDs in the Black Pearl instance
ALL_FORT_UIDS = [
    '1175905981.42kmuller',  # Fort 0A
    '1175907906.7kmuller',   # Fort 0B / Fort 1A
    '1171851678.08sdnaik',   # Fort 1B
    '1175906682.53kmuller',  # Fort 2A
    '1171851805.17sdnaik',   # Fort 2B
    '1175906834.64kmuller',  # Fort 3A
    '1175907071.31kmuller',  # Fort 3B
    '1175908312.45kmuller',  # Fort 4A
    '1175907230.14kmuller',  # Fort 4B (medium fort)
]

# Fort pairs that form barricades/drawbridges
# Key: barricade ID, Value: tuple of (fort UID 1, fort UID 2)
FortPairsDict = {
    0: ('1175905981.42kmuller', '1175907906.7kmuller'),
    1: ('1175907906.7kmuller', '1171851678.08sdnaik'),
    2: ('1175906682.53kmuller', '1171851805.17sdnaik'),
    3: ('1175906834.64kmuller', '1175907071.31kmuller'),
    4: ('1175908312.45kmuller', '1175907230.14kmuller')
}

# Fort HP configuration by level
FORT_HP_BY_LEVEL = {
    1: 5000,   # Small fort
    2: 7500,   # Medium fort
    3: 10000,  # Large fort
}

# =============================================================================
# Drawbridge Configuration
# =============================================================================

# Drawbridge node names for each fort
DrawbridgeDict = {
    '1175905981.42kmuller': ('drawbridge_pier_1175905981',),
    '1175907906.7kmuller': ('drawbridge_pier_1175907906_B', 'drawbridge_pier_1175907906_A'),
    '1171851678.08sdnaik': ('drawbridge_pier_1171851678',),
    '1175906682.53kmuller': ('drawbridge_pier_1175906682',),
    '1171851805.17sdnaik': ('drawbridge_pier_1171851805',),
    '1175906834.64kmuller': ('drawbridge_pier_1175906834',),
    '1175907071.31kmuller': ('drawbridge_pier_1175907071',),
    '1175908312.45kmuller': ('drawbridge_pier_1175908312',),
    '1175907230.14kmuller': ('drawbridge_pier_1175907230',)
}

# Ship collision nodes for each barricade
DrawbridgeCollisionDict = {
    0: [
        'col_shipcollide_1175905981',
        'col_shipcollide_1175907906_B'],
    1: [
        'col_shipcollide_1175907906_A',
        'col_shipcollide_1171851678'],
    2: [
        'col_shipcollide_1175906682',
        'col_shipcollide_1171851805'],
    3: [
        'col_shipcollide_1175906834',
        'col_shipcollide_1175907071'],
    4: [
        'col_shipcollide_1175908312',
        'col_shipcollide_1175907230']
}

# =============================================================================
# Spawn Node Configuration
# =============================================================================

# Player spawn node UID on Black Pearl Island
PLAYER_SPAWN_NODE_UID = '1171763150.73sdnaik'

# =============================================================================
# Cutscene Configuration
# =============================================================================

# Cutscene node UIDs and their cutscene IDs
CUTSCENE_NODES = {
    '1172737415.16sdnaik': '3.1: Sneaking to BlackPearl',
}

# =============================================================================
# Pier Configuration
# =============================================================================

# Pier UID on Black Pearl Island
PIER_UID = '1171761787.95sdnaik'

