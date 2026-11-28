"""
TreasureMapBlackPearlGlobals - Constants and configuration for the Black Pearl Treasure Map Instance

This module contains all the UIDs, configurations, and mappings needed for the
Black Pearl treasure map instance, including fort pairs, drawbridge mappings,
and collision dictionaries.
"""

from pirates.ship import ShipGlobals

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


# =============================================================================
# Sea Configuration
# =============================================================================

# The island is a ring around a lagoon, the Black Pearl is moored by the pier
# in the lagoon (where cutscene 3.1 leaves it) and the only way out to sea is
# the channel guarded by the forts' drawbridges. The channel's mouth is walled
# off (col_shipcollide_7), the stage four cutscene sails the Pearl and the
# Goliath out to sea (see TreasureMapBlackPearl.startPearlAndGoliathCopy).
BLACK_PEARL_SPAWN_POS = (200.6, -639.0, 0)
BLACK_PEARL_SPAWN_HPR = (242.9, 0, 0)

# the ship models are turned around underneath a DistributedShip, these are the
# positions the cutscene's copies of the ships end up at:
STAGE_FOUR_PEARL_POS = (-815, -8200, 0)
STAGE_FOUR_PEARL_HPR = (160, 0, 0)
STAGE_FOUR_GOLIATH_POS = (-224, -8780, 0)
STAGE_FOUR_GOLIATH_HPR = (148, 0, 0)

# the Goliath waits out at sea where it's copy starts the stage four cutscene:
GOLIATH_WAIT_POS = (1672, -6688, 0)
GOLIATH_WAIT_HPR = (138, 0, 0)

# the time into the stage four cutscene at which the screen has faded out and
# the Pearl and the Goliath are moved out to sea:
STAGE_FOUR_CUTSCENE_TIME = 20.0
STAGE_FOUR_MOVE_TIME = 1.0

# once the last drawbridge is down, the Pearl sailing past it starts stage four
# (the Pearl's copy starts the cutscene just past the last drawbridge):
STAGE_FOUR_TRIGGER_POS = (-483, -5813, 0)
STAGE_FOUR_TRIGGER_RADIUS = 450

# Navy attack ships, they wait in the channel behind the drawbridges and come
# through them into the lagoon once the drawbridges are raised in stage two:
ATTACK_SHIP_SPAWNS = [
    ((1600, -2950, 0), (20, 0, 0)),
    ((1600, -3300, 0), (5, 0, 0)),
    ((1430, -3900, 0), (35, 0, 0)),
    ((1180, -4200, 0), (40, 0, 0)),
]

ATTACK_SHIP_CLASSES = [
    ShipGlobals.NAVY_PREDATOR,
    ShipGlobals.NAVY_MAN_O_WAR,
    ShipGlobals.NAVY_PREDATOR,
    ShipGlobals.NAVY_COLOSSUS,
]

# sea lanes the AI ships sail along, (x, y, radius) points, the radius is how
# far either side of the lane the ship may stray. The channel lane runs from
# the pier out through the drawbridges (barricade 1, then 2, 3 and 4) to the
# open sea past the channel's mouth:
CHANNEL_SEA_LANE = [
    (200, -639, 200),
    (600, -1300, 650),
    (1100, -1900, 300),
    (1300, -2300, 70),
    (1350, -2450, 40),
    (1550, -2700, 200),
    (1600, -3300, 200),
    (1580, -3640, 40),
    (1430, -3900, 150),
    (1180, -4200, 150),
    (1050, -4370, 100),
    (800, -4600, 200),
    (400, -4850, 180),
    (0, -5100, 160),
    (-300, -5350, 80),
    (-450, -5600, 100),
    (-520, -6000, 250),
    (-540, -6400, 280),
]

# the open sea outside the channel's mouth where the Goliath is fought:
OPEN_SEA_LANE = [
    (-500, -8700, 1700),
]

# the middle of each drawbridge, the Pearl is warned about a drawbridge that is
# still blocking it's way when it comes within the warning radius:
BarricadePositions = {
    0: (1755, -2265),
    1: (1275, -2390),
    2: (1587, -3646),
    3: (1001, -4411),
    4: (-372, -5410),
}

BARRICADE_WARNING_RADIUS = 500

# the drawbridges that block the channel, barricades 2 and 3 stay open
# (see TreasureMapBlackPearl.setupBarricades), either of the two drawbridges
# either side of the island fort (0 or 1) opens the way into the channel:
BlockingBarricades = (0, 1, 4)
ChannelEntranceBarricades = (0, 1)
ChannelExitBarricade = 4
