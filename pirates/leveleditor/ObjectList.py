from pirates.npc import Skeleton
from pirates.npc import Townfolk
from pirates.npc import NavySailor
from pirates.pirate import Pirate
from pirates.creature import Creature
from pirates.cutscene import CutsceneData
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.leveleditor import EditorGlobals
from pirates.leveleditor import WorldDataGlobals
from pirates.ship import ShipGlobals
from pirates.effects.EnvironmentEffects import EnvironmentEffects
from pirates.pirate import AvatarTypes
from pirates.leveleditor import CustomAnims
from pirates.leveleditor import SFXList
from pirates.effects import ObjectEffects
OBJECT_INFO_NODE_IDX = 0
OBJECT_INFO_DATA_IDX = 1
OBJECT_INFO_ID_IDX = 2
AREA_TYPE_WORLD_REGION = 'Region'
AREA_TYPE_ISLAND = 'Island'
AREA_TYPE_ISLAND_REGION = 'Island Game Area'
AREA_TYPE_SHIP_PART = 'Ship Part'
AREA_TYPE_BUILDING_INTERIOR = 'Building Interior'
CONNECTOR_TUNNEL = 'Connector Tunnel'
CONNECTOR_DOOR = 'Connector Door'
PORT_COLLISION = 'Port Collision Sphere'
LOCATOR_NODE = 'Locator Node'
DOOR_LOCATOR_NODE = 'Door Locator Node'
COLLISION_BARRIER_NODE = 'Collision Barrier'
D_LIGHT = 'Light - Dynamic'
PROP_UI_ENTRY = 'Prop_UI_Entry'
PROP_UI_COMBO = 'Prop_UI_ComboBox'
PROP_UI_RADIO = 'Prop_UI_Radio'
PROP_UI_CHECK = 'PROP_UI_CheckBox'
PROP_UI_ELIST = 'PROP_UI_Edit_List'
PROP_UI_SLIDE = 'PROP_UI_Slider'
PROP_UI_SLIDE_DISABLE = 'PROP_UI_Slider_Disable'
NPC_TYPES = [
    'Undead',
    'Evil Navy']
START_STATES = [
    'Idle',
    'Walk']
DEF_START_STATE = 'Walk'
WAVE_TYPE_LIST = [
    'none',
    'default.spf',
    'calmday.spf',
    'evening.spf',
    'coolnight.spf',
    'stormynight.spf']
BUILDING_INTERIOR_LIST = [
    'models/buildings/interior_shanty_guildhall',
    'models/buildings/interior_tavern',
    'models/buildings/interior_tavern_b',
    'models/buildings/interior_tavern_c',
    'models/buildings/interior_spanish_npc',
    'models/buildings/interior_shanty_npc_house',
    'models/buildings/interior_shanty_store',
    'models/buildings/interior_shanty_cellar',
    'models/buildings/interior_spanish_store',
    'models/buildings/navy_jail_interior',
    'models/buildings/navy_jail_interior_stairless',
    'models/buildings/marketing_jail_interior',
    'models/buildings/interior_storage',
    'models/buildings/interior_storage_tutorial',
    'models/buildings/interior_vip_room',
    'models/town/texture_density',
    'models/buildings/interior_mansion_gov',
    'models/buildings/interior_shanty_store']
RPM_ONLY_LIST = [
    'models/buildings/marketing_jail_interior',
    'models/props/marketing_jail_column']
CAST_MODELS = [
    'models/char/js_2000',
    'models/char/wt_2000',
    'models/char/td_2000',
    'models/char/es_2000',
    'models/char/jg_2000',
    'models/char/cb_2000',
    'models/char/jr_2000',
    'models/char/pls_zero',
    'models/char/plf_zero']
SHOP_ID_LIST = [
    'PORT_ROYAL_DEFAULTS',
    'PORT_ROYAL_THRIFT',
    'TORTUGA_DEFAULTS',
    'CUBA_DEFAULTS',
    'DEL_FUEGO_DEFAULTS',
    'PORT_ROYAL_ALL',
    'PRIVATEER_TATTOOS']
HELP_ID_LIST = [
    'NONE',
    'SHIP_PVP_HELP_FRENCH_A',
    'SHIP_PVP_HELP_SPAINISH_A',
    'SHIP_PVP_HELP_FRENCH_B',
    'SHIP_PVP_HELP_SPAINISH_B']

AVAIL_OBJ_LIST = {
  'AI_NODE': {
    'Dock Node': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'UI Name': 'NPC Ship Dock Node',
      'Visual': {
        'Color': (1.0, 0.75, 0, 1),
        'Models': ['models/misc/smiley'],
        'Offset': (0, 0, 1.0)
      }
    },
    'Movement Node': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'UI Name': 'NPC Move Node',
      'Visual': {
        'Color': (0.65, 0, 0, 1),
        'Scale': 2.0,
        'Models': ['models/misc/smiley'],
        'Offset': (0, 0, 1.0)
      },
      'Properties': {
        'Pause Duration': [PROP_UI_SLIDE, [300, 5, 1]],
        'Pause Chance': [PROP_UI_SLIDE, [100, 0, 1]]
      },
      'Defaults': {
        'Pause Duration': 30,
        'Pause Chance': 100
      }
    },
    'Patrol Node': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'UI Name': 'NPC Patrol Node',
      'Visual': {
        'Color': (0, 0.65, 0, 1),
        'Scale': 2.0,
        'Models': ['models/misc/smiley'],
        'Offset': (0, 0, 1.0)
      }
    },
    'Player Spawn Node': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Color': (0.5, 0.5, 0.5, 1),
        'Models': ['models/misc/smiley'],
        'Scale': 2.0,
        'Offset': (0, 0, 1.0)
      },
      'Properties': {
        'Spawnables': [PROP_UI_COMBO, ['All', 'Team 1', 'Team 2']],
        'Index': [PROP_UI_COMBO, [x
          for x in range(-1, 10)
        ]]
      },
      'Defaults': {
        'Spawnables': 'All',
        'Index': -1
      }
    },
    'Player Boot Node': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Color': (0.5, 1.0, 0.5, 1),
        'Models': ['models/misc/smiley'],
        'Scale': 2.0,
        'Offset': (0, 0, 1.0)
      },
      'Properties': {
        'AreaUid': [PROP_UI_ENTRY]
      },
      'Defaults': {
        'AreaUid': ''
      }
    },
    'Quest Node': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'UI Name': 'Quest Node',
      'Visual': {
        'Offset': (0, 0, 1.0),
        'Scale': 10,
        'Models': ['models/misc/smiley']
      }
    },
    'Harbor Node': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'UI Name': 'Ship Harbor Node',
      'Visual': {
        'Offset': (0, 0, 1.0),
        'Models': [
          [PROP_UI_COMBO, {
            '["SubType"]': [
              [
                ['Ship Spawn'],
                ['models/misc/smiley', 'models/shipparts/warshipL1-geometry_High', 'models/shipparts/warshipL2-geometry_High', 'models/shipparts/warshipL3-geometry_High']
              ]
            ]
          }]
        ]
      },
      'Properties': {
        'SubType': [PROP_UI_COMBO, ['Ship Spawn']],
        'Station': [PROP_UI_COMBO, ['0', '1', '2', '3']],
        'ShipSize': [PROP_UI_COMBO, ['None', 'Small', 'Medium', 'Large']]
      },
      'Defaults': {
        'SubType': 'Ship Spawn',
        'Station': '0'
      }
    },
    'Ship Movement Node': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'UI Name': 'SHIP Move Node',
      'Properties': {
        'Direction': [PROP_UI_RADIO, ['Bi-directional', 'Direction 1', 'Direction 2']]
      },
      'Visual': {
        'Color': (0.65, 0, 0, 1),
        'Model': 'models/misc/smiley',
        'Models': ['models/misc/smiley'],
        'Offset': (0, 0, 1.0)
      }
    },
    'Ship Spawn Node': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'UI Name': 'SHIP Spawn Node',
      'Visual': {
        'Color': (0, 0, 0.65, 1),
        'Model': 'models/misc/smiley',
        'Models': ['models/misc/smiley'],
        'Offset': (0, 0, 1.0)
      },
      'Properties': {
        'Level': [PROP_UI_COMBO, ['1', '2', '3', '4']],
        'Spawnables': [PROP_UI_COMBO, ShipGlobals.SHIP_CLASS_LIST],
        'Team': [PROP_UI_COMBO, ['default', '0', '1', '2', '3']],
        'Flagship': [PROP_UI_CHECK]
      },
      'Defaults': {
        'Spawnables': 'MERCHANTL1',
        'Level': '3',
        'Flagship': False
      }
    },
    'Spawn Node': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'UI Name': 'NPC Spawn Node',
      'Visual': {
        'Color': (0, 0, 0.65, 1),
        'Models': ['models/misc/smiley'],
        'Scale': 2.0,
        'Offset': (0, 0, 1.0)
      },
      'Properties': {
        'Spawnables': [PROP_UI_COMBO, AvatarTypes.NPC_SPAWNABLES_KEYS, 'self.setSpawnables'],
        'Team': [PROP_UI_COMBO, ['default', '0', '1', '2', '3']],
        'Level': [PROP_UI_SLIDE_DISABLE, [40, 1, 1]],
        'Min Population': [PROP_UI_ENTRY],
        'Patrol Radius': [PROP_UI_SLIDE, [20, 1], 'self.setPatrolRadius'],
        'Aggro Radius': [PROP_UI_SLIDE_DISABLE, [50, 0, 0.0001, 12], 'self.setAggroRadius'],
        'Start State': [PROP_UI_RADIO, ['Idle', 'Patrol', 'Ambush']],
        'AnimSet': [PROP_UI_COMBO, CustomAnims.INTERACT_ANIM_NAMES, 'self.setAnimSet'],
        'PoseAnim': [PROP_UI_ENTRY],
        'PoseFrame': [PROP_UI_ENTRY],
        'StartFrame': [PROP_UI_ENTRY],
        'TrailFX': [PROP_UI_COMBO, ['None', 'Sword', 'Dagger'], 'self.setTrailFX'],
        'Pause Duration': [PROP_UI_SLIDE, [300, 5, 1]],
        'Pause Chance': [PROP_UI_SLIDE, [100, 0, 1]]
      },
      'PropertiesList': ['Spawnables', 'Team', 'Min Population', 'Patrol Radius', 'Aggro Radius', 'Start State', 'AnimSet', 'Pause Duration', 'Pause Chance', 'Level', 'TrailFX', 'StartFrame', 'PoseAnim', 'PoseFrame'],
      'RpmOnlyPropList': ['PoseAnim', 'PoseFrame', 'StartFrame', 'TrailFX'],
      'Defaults': {
        'PoseAnim': '',
        'PoseFrame': '',
        'StartFrame': '0',
        'TrailFX': 'None',
        'Min Population': '1',
        'Spawnables': 'Noob Skeleton',
        'AnimSet': 'default',
        'Patrol Radius': 12,
        'Pause Duration': 30,
        'Pause Chance': 100,
        'Start State': 'Patrol'
      }
    },
    'Cutscene Origin Node': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'UI Name': 'Cutscene Origin Node',
      'Visual': {
        'Color': (0, 0, 0.65, 1),
        'Models': ['models/misc/smiley'],
        'Offset': (0, 0, 1.0)
      },
      'Properties': {
        'CutsceneId': [PROP_UI_COMBO, CutsceneData.CutsceneIds]
      },
      'Defaults': {
        'CutsceneId': CutsceneData.CutsceneIds[0]
      }
    },
    'Effect Node': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'UI Name': 'Effect Node',
      'Visual': {
        'Color': (0, 0, 0.65, 1),
        'Models': ['models/misc/smiley'],
        'Offset': (0, 0, 1.0)
      },
      'Properties': {
        'EffectName': [PROP_UI_COMBO, EnvironmentEffects.EffectNodeNames, 'self.setEffects']
      },
      'Defaults': {
        'EffectName': EnvironmentEffects.EffectNodeNames[0]
      }
    },
    'Object Spawn Node': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Linkable': 1,
      'UI Name': 'Object Spawn Node',
      'Visual': {
        'Color': (0.8, 0.2, 0.65, 1),
        'Models': ['models/misc/smiley'],
        'Scale': 2.0,
        'Offset': (0, 0, 1.0)
      },
      'Properties': {
        'Spawnables': [PROP_UI_COMBO, ['Buried Treasure', 'Surface Treasure']],
        'SpawnDelay': [PROP_UI_ENTRY],
        'startingDepth': [PROP_UI_ENTRY],
        'Priority': [PROP_UI_ENTRY]
      },
      'Defaults': {
        'Spawnables': 'Buried Treasure',
        'SpawnDelay': '20',
        'startingDepth': '15',
        'Priority': '1'
      }
    },
    'Node Link': {
      'NonRpmNode': 1,
      'Virtual': 1,
      'Properties': {
        'Direction': [PROP_UI_RADIO, ['Bi-directional', 'Direction 1', 'Direction 2']]
      }
    }
  },
  'AI_OBJ': {
    CONNECTOR_TUNNEL: {
      'NonRpmNode': 1,
      'AreaType': CONNECTOR_TUNNEL,
      'Create': None,
      'Entrance': 'portal_connector_',
      'EntranceSuffix': '1',
      'External': 1,
      'Raycast': 0,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/tunnels/tunnel_swamp', 'models/tunnels/tunnel_swamp_cave', 'models/tunnels/tunnel_swamp_jungle', 'models/tunnels/tunnel_jungle', 'models/tunnels/tunnel_cave_left', 'models/tunnels/tunnel_volcano_left']
      }
    },
    CONNECTOR_DOOR: {
      'NonRpmNode': 1,
      'AreaType': CONNECTOR_DOOR,
      'Create': None,
      'Entrance': 'door_locator_',
      'EntranceSuffix': '1',
      'External': 1,
      'Raycast': 0,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/buildings/shanty_guildhall_door']
      }
    },
    'Cannon': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Properties': {
        'MinPower': [PROP_UI_ENTRY],
        'MaxPower': [PROP_UI_ENTRY]
      },
      'Defaults': {
        'MinPower': '0.2',
        'MaxPower': '1.0'
      },
      'Visual': {
        'Models': ['models/shipparts/cannon_hi', 'models/shipparts/cannon_great_hi', 'models/shipparts/cannon_bronze_hi', 'models/shipparts/cannon_heavy_hi', 'models/shipparts/cannon_skull_hi']
      }
    },
    'Dinghy': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Properties': {
        'Aggro Radius': [PROP_UI_SLIDE, [100, 0], 'self.setAggroRadius'],
        'Location': [PROP_UI_COMBO, ['Water', 'Land']]
      },
      'Defaults': {
        'Aggro Radius': 20,
        'Location': 'Water'
      },
      'Visual': {
        'Models': ['models/shipparts/dingy-geometry_High']
      }
    },
    'BuriedTreasure': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Linkable': 1,
      'Properties': {
        'startingDepth': [PROP_UI_ENTRY]
      },
      'Visual': {
        'Models': ['models/props/treasureChest']
      }
    },
    'Searchable Container': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Linkable': 1,
      'Properties': {
        'Aggro Radius': [PROP_UI_SLIDE, [10, 0], 'self.setAggroRadius'],
        'searchTime': [PROP_UI_ENTRY],
        'type': [PROP_UI_COMBO, list(PiratesGlobals.SearchableModels.keys())]
      },
      'Defaults': {
        'Aggro Radius': 5.0,
        'searchTime': '6.2',
        'type': 'Crate'
      },
      'Visual': {
        'Models': list(PiratesGlobals.SearchableModels.values())
      }
    },
    'Treasure Bank': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Properties': {
        'Team': [PROP_UI_COMBO, ['Team 1', 'Team 2']],
        'InitVal': [PROP_UI_ENTRY]
      },
      'Defaults': {
        'InitVal': '0'
      },
      'Visual': {
        'Models': ['models/props/treasureTrough']
      }
    },
    'bilgewater_town': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/town/bilgewater_town']
      }
    },
    PORT_COLLISION: {
      'NonRpmNode': 1,
      'Create': None,
      'Properties': {
        'Name': [PROP_UI_ENTRY]
      },
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Color': (0.5, 0.5, 1.0, 0.2),
        'Scale': 1.0,
        'Models': ['models/misc/smiley']
      }
    },
    AREA_TYPE_ISLAND: {
      'NonRpmNode': 1,
      'AreaType': AREA_TYPE_ISLAND,
      'Create': None,
      'InteriorNodes': 'portal_exterior_',
      'EntranceSuffix': '1',
      'External': 1,
      'Raycast': 0,
      'Selectable': 1,
      'Properties': {
        'Wave Type': [PROP_UI_COMBO, WAVE_TYPE_LIST, 'self.setWaveType'],
        'Undockable': [PROP_UI_CHECK]
      },
      'NonAreaProps': ['Undockable'],
      'PropertiesList': ['Undockable'],
      'RpmOnlyPropList': ['Wave Type'],
      'Defaults': {
        'Undockable': False
      },
      'Visual': {
        'Model': 'models/islands/Island_A',
        'Models': ['models/islands/Big_island_A', 'models/islands/Island_A', 'models/islands/Mid_island_A', 'models/islands/Small_island_A', 'models/islands/Tiny_island_A', 'models/islands/testsimple', 'models/islands/bilgewater_zero', 'models/islands/pvp_a_zero', 'models/islands/pvp_b_zero', 'models/islands/pvpcove_zero', 'models/islands/pvpFortress', 'models/islands/pvp_rock_sml_zero', 'models/islands/pvp_rock_med_zero', 'models/islands/pvp_rock_big_zero', 'models/props/bilgewater_gameArea_test', 'models/islands/rambleshack_zero', 'models/islands/madre_del_fuego_zero', 'models/islands/padre_del_fuego', 'models/islands/port_royal_zero', 'models/islands/pir_m_are_isl_portRoyal_zero', 'models/islands/tortuga_zero', 'models/islands/wild_island_a_zero', 'models/islands/wild_island_b_zero', 'models/islands/wild_island_c_zero', 'models/islands/wild_island_d_zero', 'models/islands/wild_island_e_zero', 'models/islands/wild_island_f_zero', 'models/islands/kingshead_zero', 'models/islands/cuba_zero', 'models/islands/rum_runner_zero', 'models/islands/gameAreaSandbox', 'models/islands/pearl_island_zero']
      }
    },
    AREA_TYPE_ISLAND_REGION: {
      'NonRpmNode': 1,
      'AreaType': AREA_TYPE_ISLAND_REGION,
      'Create': None,
      'Entrance': 'portal_interior_',
      'EntranceSuffix': '1',
      'External': 1,
      'Raycast': 0,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/swamps/swampA', 'models/swamps/swampB', 'models/swamps/swampC', 'models/caves/cave_a_zero', 'models/caves/cave_b_zero', 'models/caves/cave_c_zero', 'models/caves/cave_d_zero', 'models/caves/cave_e_zero', 'models/caves/cave_barbossa_zero', 'models/jungles/jungle_a_zero', 'models/jungles/jungle_b_zero', 'models/jungles/jungle_c_zero', 'models/islands/kingshead_zero'],
        'Scale': 1.0
      },
      'Properties': {
        'Instanced': [PROP_UI_CHECK]
      },
      'Defaults': {
        'Instanced': False
      }
    },
    'Parlor Game': {
      'NonRpmNode': 1,
      'Properties': {
        'Category': [PROP_UI_COMBO, ['Blackjack', 'Holdem', '7Stud']],
        'BetMultiplier': [PROP_UI_ENTRY]
      },
      'Create': None,
      'Defaults': {
        'Category': 'Blackjack',
        'BetMultiplier': '1'
      },
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/table_bar_round_parlor']
      }
    },
    'Pirate': {
      'Create': Pirate.Pirate,
      'Raycast': 1,
      'Selectable': 1,
      'Properties': {
        'Start State': [PROP_UI_RADIO, START_STATES],
        'Patrol Radius': [PROP_UI_SLIDE, [20, 1], 'self.setPatrolRadius'],
        'Aggro Radius': [PROP_UI_SLIDE_DISABLE, [50, 0, 0.0001, 12], 'self.setAggroRadius'],
        'AnimSet': [PROP_UI_COMBO, CustomAnims.INTERACT_ANIM_NAMES, 'self.setAnimSet'],
        'Zombie': [PROP_UI_CHECK, 'self.setZombie'],
        'StaffFX': [PROP_UI_COMBO, ['None', 'ChargeWither', 'ChargeSoulflay', 'ChargePestilence', 'ChargeHellfire', 'ChargeBanish', 'ChargeDesolation'], 'self.setStaffFX'],
        'AttuneFX': [PROP_UI_COMBO, ['None', 'Hostile', 'Friendly', 'Both'], 'self.setAttuneFX'],
        'TrailFX': [PROP_UI_COMBO, ['None', 'Sword', 'Dagger'], 'self.setTrailFX'],
        'PoseAnim': [PROP_UI_ENTRY],
        'PoseFrame': [PROP_UI_ENTRY],
        'StartFrame': [PROP_UI_ENTRY],
        'Respawns': [PROP_UI_CHECK]
      },
      'PropertiesList': ['Patrol Radius', 'Aggro Radius', 'Start State', 'AnimSet', 'StaffFX', 'AttuneFX', 'TrailFX', 'StartFrame', 'PoseAnim', 'PoseFrame', 'Zombie', 'Respawns'],
      'RpmOnlyPropList': ['Zombie', 'StaffFX', 'AttuneFX', 'TrailFX', 'PoseAnim', 'PoseFrame', 'StartFrame'],
      'Defaults': {
        'Zombie': False,
        'StaffFX': 'None',
        'AttuneFX': 'None',
        'TrailFX': 'None',
        'PoseAnim': '',
        'PoseFrame': '',
        'StartFrame': '0',
        'Prop': None,
        'Start State': DEF_START_STATE,
        'Patrol Radius': 12,
        'Respawns': True
      }
    },
    'Jack Sparrow Standin': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/char/js_2000']
      }
    },
    AREA_TYPE_SHIP_PART: {
      'AreaType': AREA_TYPE_SHIP_PART,
      'Create': None,
      'External': 1,
      'Raycast': 1,
      'Selectable': 1,
      'UI Name': 'Ship',
      'Visual': {
        'Models': [
          [PROP_UI_COMBO, {
            '["Team"]': [
              [
                [PiratesGlobals.PLAYER_TEAM_STR, PiratesGlobals.NAVY_TEAM_STR],
                [{
                  'InterceptorL1': ['models/shipparts/interceptorL1-geometry_High', 'models/shipparts/interceptorL1-collisions'],
                  'InterceptorL2': ['models/shipparts/interceptorL2-geometry_High', 'models/shipparts/interceptorL2-collisions'],
                  'InterceptorL3': ['models/shipparts/interceptorL3-geometry_High', 'models/shipparts/interceptorL3-collisions'],
                  'MerchantL1': ['models/shipparts/merchantL1-geometry_High', 'models/shipparts/merchantL1-collisions', 'models/shipparts/merchantCabinAL1-collisions', 'models/shipparts/merchantCabinAL1-geometry_High'],
                  'MerchantL2': ['models/shipparts/merchantL2-geometry_High', 'models/shipparts/merchantL2-collisions', 'models/shipparts/merchantCabinAL2-collisions', 'models/shipparts/merchantCabinAL2-geometry_High'],
                  'MerchantL3': ['models/shipparts/merchantL3-geometry_High', 'models/shipparts/merchantL3-collisions', 'models/shipparts/merchantCabinAL3-collisions', 'models/shipparts/merchantCabinAL3-geometry_High'],
                  'WarshipL1': ['models/shipparts/warshipL1-geometry_High', 'models/shipparts/warshipL1-collisions', 'models/shipparts/warCabinAL1-collisions', 'models/shipparts/warCabinAL1-geometry_High'],
                  'WarshipL2': ['models/shipparts/warshipL2-geometry_High', 'models/shipparts/warshipL2-collisions', 'models/shipparts/warCabinAL2-collisions', 'models/shipparts/warCabinAL2-geometry_High'],
                  'WarshipL3': ['models/shipparts/warshipL3-geometry_High', 'models/shipparts/warshipL3-collisions', 'models/shipparts/warCabinAL3-collisions', 'models/shipparts/warCabinAL3-geometry_High'],
                  'BlackPearl': ['models/shipparts/blackpearl-geometry_High', 'models/shipparts/blackpearl-collisions', 'models/shipparts/blackpearlCabin-collisions', 'models/shipparts/blackpearlCabin-geometry_High'],
                  'Goliath': ['models/shipparts/goliath-geometry_High', 'models/shipparts/goliath-collisions', 'models/shipparts/goliath-collisions', 'models/shipparts/goliath-geometry_High']
                }]
              ],
              [
                [PiratesGlobals.FRENCH_UNDEAD_TEAM_STR, PiratesGlobals.SPANISH_UNDEAD_TEAM_STR],
                [{
                  'SkeletonInterceptorL3': ['models/shipparts/-geometry_High', 'models/shipparts/skeletonInterceptorL3-collisions', 'models/shipparts/skeletonInterceptorL3-collisions', 'models/shipparts/skeletonInterceptorL3-geometry_High']
                }]
              ],
              [
                [PiratesGlobals.UNDEAD_TEAM_STR],
                [{
                  'Warship': ['models/shipparts/skeletonWarshipL3-geometry_High', 'models/shipparts/skeletonWarshipL3-collisions', 'models/shipparts/skeletonWarCabinAL3-geometry_High', 'models/shipparts/skeletonWarCabinAL3-collisions'],
                  'SkeletonInterceptorL3': ['models/shipparts/-geometry_High', 'models/shipparts/skeletonInterceptorL3-collisions', 'models/shipparts/skeletonInterceptorL3-collisions', 'models/shipparts/skeletonInterceptorL3-geometry_High']
                }]
              ]
            ]
          }]
        ]
      },
      'Properties': {
        'Category': [PROP_UI_COMBO, ['Interceptor', 'InterceptorTutorial', 'Merchant', 'MerchantTutorial', 'Warship'] + EditorGlobals.shipList, 'self.setShip'],
        'Team': [PROP_UI_COMBO, [PiratesGlobals.PLAYER_TEAM_STR, PiratesGlobals.UNDEAD_TEAM_STR, PiratesGlobals.NAVY_TEAM_STR, PiratesGlobals.FRENCH_UNDEAD_TEAM_STR, PiratesGlobals.SPANISH_UNDEAD_TEAM_STR]],
        'Start State': [PROP_UI_RADIO, ['Idle', 'Sail']],
        'Respawns': [PROP_UI_CHECK],
        'ForwardVelocity': [PROP_UI_SLIDE, [30, 6], 'self.setForwardVelocity'],
        'RotationalVelocity': [PROP_UI_SLIDE, [10, 0], 'self.setRotationalVelocity'],
        'SailLogo': [PROP_UI_COMBO, ['None', 'French', 'Spanish'], 'self.setShipSailLogo'],
        'Flagship': [PROP_UI_CHECK]
      },
      'NonAreaProps': ['Category', 'Team', 'Start State', 'Respawns', 'Flagship'],
      'NonRpmPropList': ['Team', 'Flagship', 'Start State', 'Respawns'],
      'RpmOnlyPropList': ['ForwardVelocity', 'RotationalVelocity', 'SailLogo'],
      'Defaults': {
        'Category': 'Interceptor',
        'Start State': 'Idle',
        'Respawns': True,
        'Flagship': False
      }
    },
    'Skeleton': {
      'Create': Skeleton.Skeleton,
      'AvatarTypes': {
        'Id': 'range(0,10)',
        'Track': '[0,1,2,3,6,7]'
      },
      'Raycast': 1,
      'Selectable': 1,
      'Properties': {
        'Start State': [PROP_UI_RADIO, START_STATES],
        'Patrol Radius': [PROP_UI_SLIDE, [20, 1], 'self.setPatrolRadius'],
        'Aggro Radius': [PROP_UI_SLIDE_DISABLE, [50, 0, 0.0001, 12], 'self.setAggroRadius'],
        'AnimSet': [PROP_UI_COMBO, CustomAnims.INTERACT_ANIM_NAMES, 'self.setAnimSet'],
        'PoseAnim': [PROP_UI_ENTRY],
        'PoseFrame': [PROP_UI_ENTRY],
        'StartFrame': [PROP_UI_ENTRY],
        'TrailFX': [PROP_UI_COMBO, ['None', 'Sword', 'Dagger'], 'self.setTrailFX'],
        'Respawns': [PROP_UI_CHECK],
        'Boss': [PROP_UI_CHECK]
      },
      'PropertiesList': ['Patrol Radius', 'Aggro Radius', 'Start State', 'AnimSet', 'TrailFX', 'StartFrame', 'PoseAnim', 'PoseFrame', 'Respawns', 'Boss'],
      'RpmOnlyPropList': ['PoseAnim', 'PoseFrame', 'StartFrame', 'TrailFX'],
      'Defaults': {
        'PoseAnim': '',
        'PoseFrame': '',
        'StartFrame': '0',
        'TrailFX': 'None',
        'Start State': DEF_START_STATE,
        'Patrol Radius': 12,
        'Respawns': True,
        'Boss': False
      }
    },
    'Creature': {
      'Create': EditorGlobals.CreateCreature,
      'Raycast': 1,
      'Selectable': 1,
      'Properties': {
        'Start State': [PROP_UI_RADIO, START_STATES],
        'Patrol Radius': [PROP_UI_SLIDE, [20, 1], 'self.setPatrolRadius'],
        'Aggro Radius': [PROP_UI_SLIDE_DISABLE, [50, 0, 0.0001, 12], 'self.setAggroRadius'],
        'Respawns': [PROP_UI_CHECK],
        'PoseAnim': [PROP_UI_ENTRY],
        'PoseFrame': [PROP_UI_ENTRY],
        'StartFrame': [PROP_UI_ENTRY],
        'Species': [PROP_UI_COMBO, ['Crab', 'Rock Crab', 'Giant Crab', 'Alligator', 'Big Gator', 'Huge Gator', 'Scorpion', 'Dread Scorpion', 'Bat', 'Vampire Bat', 'Wasp', 'Angry Wasp', 'FlyTrap', 'Stump'], 'self.setCreatureType'],
        'Boss': [PROP_UI_CHECK]
      },
      'PropertiesList': ['Species', 'StartFrame', 'PoseAnim', 'PoseFrame', 'Patrol Radius', 'Aggro Radius', 'Start State', 'Respawns', 'Boss'],
      'RpmOnlyPropList': ['PoseAnim', 'PoseFrame', 'StartFrame'],
      'Defaults': {
        'PoseAnim': '',
        'PoseFrame': '',
        'StartFrame': '0',
        'Start State': DEF_START_STATE,
        'Patrol Radius': 12,
        'Respawns': True,
        'Species': 'Crab',
        'Boss': False
      }
    },
    'Animal': {
      'Create': EditorGlobals.CreateAnimal,
      'Raycast': 1,
      'Selectable': 1,
      'Properties': {
        'Start State': [PROP_UI_RADIO, START_STATES],
        'Patrol Radius': [PROP_UI_SLIDE, [20, 1], 'self.setPatrolRadius'],
        'Respawns': [PROP_UI_CHECK],
        'PoseAnim': [PROP_UI_ENTRY],
        'PoseFrame': [PROP_UI_ENTRY],
        'StartFrame': [PROP_UI_ENTRY],
        'Species': [PROP_UI_COMBO, ['Chicken', 'Dog', 'Pig', 'Rooster', 'Seagull', 'Monkey'], 'self.setAnimalType']
      },
      'PropertiesList': ['Species', 'StartFrame', 'PoseAnim', 'PoseFrame', 'Patrol Radius', 'Start State', 'Respawns'],
      'RpmOnlyPropList': ['PoseAnim', 'PoseFrame', 'StartFrame'],
      'Defaults': {
        'PoseAnim': '',
        'PoseFrame': '',
        'StartFrame': '0',
        'Start State': DEF_START_STATE,
        'Patrol Radius': 12,
        'Respawns': True,
        'Species': 'Pig'
      }
    },
    'NavySailor': {
      'Create': NavySailor.NavySailor,
      'AvatarTypes': {
        'Id': 'range(0,5)',
        'Track': '[0,1,2]'
      },
      'Raycast': 1,
      'Selectable': 1,
      'Properties': {
        'Start State': [PROP_UI_RADIO, START_STATES],
        'Patrol Radius': [PROP_UI_SLIDE, [20, 1], 'self.setPatrolRadius'],
        'Aggro Radius': [PROP_UI_SLIDE_DISABLE, [50, 0, 0.0001, 12], 'self.setAggroRadius'],
        'AnimSet': [PROP_UI_COMBO, CustomAnims.INTERACT_ANIM_NAMES, 'self.setAnimSet'],
        'PoseAnim': [PROP_UI_ENTRY],
        'PoseFrame': [PROP_UI_ENTRY],
        'StartFrame': [PROP_UI_ENTRY],
        'TrailFX': [PROP_UI_COMBO, ['None', 'Sword', 'Dagger'], 'self.setTrailFX'],
        'NavyFaction': [PROP_UI_COMBO, ['Navy', 'TradingCo'], 'self.setNavyFaction'],
        'Respawns': [PROP_UI_CHECK],
        'Boss': [PROP_UI_CHECK]
      },
      'PropertiesList': ['Patrol Radius', 'Aggro Radius', 'Start State', 'AnimSet', 'TrailFX', 'StartFrame', 'PoseAnim', 'PoseFrame', 'Respawns', 'Boss', 'NavyFaction'],
      'RpmOnlyPropList': ['PoseAnim', 'PoseFrame', 'StartFrame', 'TrailFX'],
      'Defaults': {
        'PoseAnim': '',
        'PoseFrame': '',
        'StartFrame': '0',
        'TrailFX': 'None',
        'NavyFaction': 'Navy',
        'Start State': DEF_START_STATE,
        'Patrol Radius': 12,
        'Respawns': True,
        'Boss': False
      }
    },
    'Townsperson': {
      'Create': Townfolk.Townfolk,
      'Raycast': 1,
      'Selectable': 1,
      'Properties': {
        'Start State': [PROP_UI_RADIO, START_STATES],
        'Category': [PROP_UI_COMBO, ['Commoner', 'Gypsy', 'Blacksmith', 'Shipwright', 'Merchant', 'Bartender', 'Cannoneer', 'Gunsmith', 'Grenadier', 'MedicineMan', 'Cast', 'Tailor', 'Barber', 'Jeweler', 'Tattoo', 'Trainer', 'PvPRewards']],
        'Respawns': [PROP_UI_CHECK],
        'ShopInv': [PROP_UI_ELIST],
        'ShopID': [PROP_UI_COMBO, SHOP_ID_LIST],
        'HelpID': [PROP_UI_COMBO, HELP_ID_LIST],
        'Team': [PROP_UI_COMBO, ['Villager', 'Player']],
        'CustomModel': [PROP_UI_COMBO, ['None'] + CAST_MODELS, 'self.setCustomModel'],
        'Private Status': [PROP_UI_RADIO, ['All', 'Private Only', 'MMP Only']],
        'Patrol Radius': [PROP_UI_SLIDE, [20, 1], 'self.setPatrolRadius'],
        'Aggro Radius': [PROP_UI_SLIDE_DISABLE, [50, 0, 0.0001, 12], 'self.setAggroRadius'],
        'AnimSet': [PROP_UI_COMBO, CustomAnims.INTERACT_ANIM_NAMES, 'self.setAnimSet'],
        'PoseAnim': [PROP_UI_ENTRY],
        'PoseFrame': [PROP_UI_ENTRY],
        'StartFrame': [PROP_UI_ENTRY],
        'TrailFX': [PROP_UI_COMBO, ['None', 'Sword', 'Dagger'], 'self.setTrailFX']
      },
      'PropertiesList': ['Category', 'CustomModel', 'Private Status', 'ShopID', 'HelpID', 'Team', 'Patrol Radius', 'Aggro Radius', 'Start State', 'AnimSet', 'Respawns', 'TrailFX', 'StartFrame', 'PoseAnim', 'PoseFrame'],
      'NonRpmPropList': ['Private Status', 'ShopInv', 'ShopID', 'HelpID', 'Team', 'Patrol Radius', 'Aggro Radius', 'Start State', 'Respawns'],
      'RpmOnlyPropList': ['PoseAnim', 'PoseFrame', 'StartFrame', 'TrailFX'],
      'Defaults': {
        'Start State': DEF_START_STATE,
        'Category': 'Commoner',
        'Team': 'Player',
        'Patrol Radius': 12,
        'PoseAnim': '',
        'PoseFrame': '',
        'StartFrame': '0',
        'TrailFX': 'None',
        'Respawns': True
      }
    },
    'Interactive Prop': {
      'NonRpmNode': 1,
      'Raycast': 1,
      'Selectable': 1,
      'Linkable': 1,
      'Properties': {
        'interactAble': [PROP_UI_COMBO, {
          '["Visual"]["Model"]': [
            [
              ['models/props/barrel', 'models/props/jar', 'models/props/chair_bank', 'models/props/chair_bar', 'models/props/chair_fancy', 'models/props/chair_shanty', 'models/islands/pier_stockade', 'models/props/shop_bsmith_anvilblock_interactive', 'models/props/broom'],
              ['npc']
            ],
            [
              ['models/props/dummy_zero'],
              ['player']
            ]
          ]
        }],
        'interactType': [PROP_UI_COMBO, {
          '["Visual"]["Model"]': [
            [
              ['models/props/barrel', 'models/props/jar', 'models/props/dummy_zero'],
              ['hit']
            ],
            [
              ['models/props/chair_bank', 'models/props/chair_bar', 'models/props/chair_fancy', 'models/props/chair_shanty'],
              ['sit']
            ],
            [
              ['models/islands/pier_stockade'],
              ['stockade']
            ],
            [
              ['models/props/shop_bsmith_anvilblock_interactive'],
              ['smith']
            ],
            [
              ['models/props/broom'],
              ['sweep']
            ]
          ]
        }]
      },
      'Visual': {
        'Models': ['models/props/barrel', 'models/props/jar', 'models/props/chair_bank', 'models/props/chair_bar', 'models/props/chair_fancy', 'models/props/chair_shanty', 'models/islands/pier_stockade', 'models/props/dummy_zero', 'models/props/shop_bsmith_anvilblock_interactive']
      }
    },
    'InternObject': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/barrel']
      }
    },
    'Jail Cell Door': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Properties': {
        'Cell Index': [PROP_UI_COMBO, [x
          for x in range(0, 10)
        ]],
        'Level': [PROP_UI_COMBO, [x
          for x in range(1, 6)
        ]]
      },
      'Defaults': {
        'Cell Index': 0,
        'Level': 1
      },
      'Visual': {
        'Models': ['models/misc/smiley'],
        'Color': (1, 0.5, 0.5, 1.0)
      }
    }
  },
  'BUILDING_OBJ': {
    'Arch': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/buildings/spanish_archA',
        'Models': ['models/buildings/spanish_archA', 'models/buildings/spanish_archB', 'models/buildings/spanish_archC', 'models/buildings/english_arch_a', 'models/buildings/smallstucco_arch'],
        'Scale': 1.0
      }
    },
    'Shanty Gypsywagon': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/buildings/shanty_gypsywagon_exterior',
        'Models': ['models/buildings/shanty_gypsywagon_exterior'],
        'Scale': 1.0
      }
    },
    'Shanty Tents': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/buildings/6shanty_tents',
        'Models': ['models/buildings/6shanty_tents', 'models/buildings/3shanty_tents', 'models/buildings/1shanty_tents_empty', 'models/buildings/shanty_tent_house_facade', 'models/buildings/shanty_tent_house_body'],
        'Scale': 1.0
      }
    },
    'Building Exterior': {
      'Create': None,
      'Raycast': 1,
      'External': 1,
      'AllowChildren': 1,
      'ExtUnique': 1,
      'AreaType': AREA_TYPE_BUILDING_INTERIOR,
      'Entrance': 'portal_exterior_',
      'EntranceSuffix': '1',
      'Selectable': 1,
      'Visual': {
        'Model': 'models/buildings/jail_exterior',
        'Models': ['models/buildings/jail_exterior', 'models/buildings/fort_door', 'models/buildings/shanty_cellar_door', 'models/buildings/shanty_guildhall_exterior', 'models/buildings/shanty_gypsywagon_exterior', 'models/buildings/shanty_tavern_exterior', 'models/buildings/shanty_repairshop_exterior', 'models/buildings/shanty_leanto_A', 'models/buildings/shanty_leanto_B', 'models/buildings/shanty_npc_house_a_exterior', 'models/buildings/shanty_npc_house_combo_A', 'models/buildings/shanty_npc_house_combo_B', 'models/buildings/shanty_npc_house_combo_C', 'models/buildings/shanty_npc_house_combo_D', 'models/buildings/shanty_npc_house_combo_E', 'models/buildings/shanty_npc_house_combo_F', 'models/buildings/shanty_npc_house_combo_G', 'models/buildings/shanty_npc_house_combo_H', 'models/buildings/shanty_npc_house_combo_I', 'models/buildings/shanty_npc_house_combo_J', 'models/buildings/shanty_npc_house_combo_Platform', 'models/buildings/shanty_signpost', 'models/buildings/spanish_npc_house_a_exterior', 'models/buildings/spanish_npc_house_b_exterior', 'models/buildings/spanish_npc_house_c_exterior', 'models/buildings/spanish_npc_house_d_exterior', 'models/buildings/spanish_npc_house_e_exterior', 'models/buildings/spanish_npc_house_f_exterior', 'models/buildings/spanish_npc_house_g_exterior', 'models/buildings/spanish_npc_house_i_exterior', 'models/buildings/spanish_npc_house_j_exterior', 'models/buildings/spanish_npc_house_k_exterior', 'models/buildings/spanish_npc_house_l_exterior', 'models/buildings/spanish_npc_house_n_exterior', 'models/buildings/spanish_npc_house_o_exterior', 'models/buildings/spanish_npc_house_p_exterior', 'models/buildings/spanish_tavern_exterior', 'models/town/bar_exterior', 'models/buildings/spanish_npc_attach_fullarchL', 'models/buildings/spanish_npc_attach_fullarchR', 'models/buildings/spanish_npc_attach_fullnostonearchL', 'models/buildings/spanish_npc_attach_fullnostonearchR', 'models/buildings/spanish_npc_attach_halfarchL', 'models/buildings/spanish_npc_attach_halfarchR', 'models/buildings/spanish_npc_attach_halfarchflatL', 'models/buildings/spanish_npc_attach_halfarchflatR', 'models/buildings/spanish_npc_attach_halfarchwindowL', 'models/buildings/spanish_npc_attach_halfarchwindowR', 'models/buildings/spanish_npc_attach_halfporchL', 'models/buildings/spanish_npc_attach_halfporchR', 'models/buildings/burned_gate', 'models/buildings/burned_half_house', 'models/buildings/burned_house', 'models/buildings/burned_woods', 'models/buildings/english_a', 'models/buildings/english_b', 'models/buildings/english_c', 'models/buildings/english_d', 'models/buildings/english_e', 'models/buildings/english_f', 'models/buildings/english_g', 'models/buildings/english_h', 'models/buildings/english_i', 'models/buildings/english_j', 'models/buildings/english_k', 'models/buildings/english_k_tutorial', 'models/buildings/english_l', 'models/buildings/english_m', 'models/buildings/english_n', 'models/buildings/english_corner_a', 'models/buildings/english_corner_b', 'models/buildings/english_corner_c', 'models/buildings/english_corner_c2', 'models/buildings/english_corner_d', 'models/buildings/english_corner_e', 'models/buildings/english_corner_f', 'models/buildings/english_mansion', 'models/buildings/fort_eitc', 'models/buildings/fort_small_cave', 'models/islands/kingshead_zero'],
        'Properties': {
          'Interior': [PROP_UI_COMBO, BUILDING_INTERIOR_LIST],
          'Door': [PROP_UI_COMBO, ['models/buildings/shanty_guildhall_door']],
          'Name': [PROP_UI_ENTRY],
          'SignFrame': [PROP_UI_COMBO, {
            '["Visual"]["Model"]': [
              [
                ['models/buildings/english_a', 'models/buildings/english_b', 'models/buildings/english_c', 'models/buildings/english_d', 'models/buildings/english_h', 'models/buildings/english_n', 'models/buildings/english_corner_b', 'models/buildings/english_corner_c', 'models/buildings/english_corner_c2', 'models/buildings/fort_door', 'models/buildings/fort_door_kings', 'models/buildings/fort_small_cave', 'models/buildings/fort_eitc'],
                ['', 'models/buildings/sign1_eng_a_frame']
              ],
              [
                ['models/buildings/english_mansion', 'models/buildings/english_e', 'models/buildings/english_g', 'models/buildings/english_i', 'models/buildings/english_j'],
                ['', 'models/buildings/sign1_eng_b_frame']
              ],
              [
                ['models/buildings/english_f', 'models/buildings/english_k', 'models/buildings/english_l', 'models/buildings/english_m', 'models/buildings/english_corner_a', 'models/buildings/english_corner_d', 'models/buildings/english_corner_e', 'models/buildings/english_corner_f'],
                ['', 'models/buildings/sign1_eng_c_frame']
              ],
              [
                ['models/buildings/spanish_npc_house_a_exterior', 'models/buildings/spanish_npc_house_c_exterior', 'models/buildings/spanish_npc_house_e_exterior', 'models/buildings/spanish_npc_house_j_exterior', 'models/buildings/spanish_npc_house_l_exterior', 'models/buildings/spanish_npc_house_p_exterior'],
                ['', 'models/buildings/sign1_spanish_a_frame']
              ],
              [
                ['models/buildings/spanish_npc_house_b_exterior', 'models/buildings/spanish_npc_house_d_exterior', 'models/buildings/spanish_npc_house_g_exterior', 'models/buildings/spanish_npc_house_i_exterior', 'models/buildings/spanish_npc_house_k_exterior', 'models/buildings/spanish_npc_house_n_exterior', 'models/buildings/spanish_npc_house_o_exterior'],
                ['', 'models/buildings/sign1_spanish_b_frame']
              ],
              [
                ['models/buildings/spanish_tavern_exterior'],
                ['models/buildings/sign1_spanish_c_frame']
              ],
              [
                ['models/buildings/shanty_guildhall_exterior', 'models/buildings/shanty_tavern_exterior', 'models/buildings/shanty_repairshop_exterior'],
                ['', 'models/buildings/sign1_shanty_a_frame']
              ],
              [
                ['models/buildings/shanty_npc_house_a_exterior', 'models/buildings/shanty_npc_house_combo_A', 'models/buildings/shanty_npc_house_combo_B', 'models/buildings/shanty_npc_house_combo_C', 'models/buildings/shanty_npc_house_combo_D', 'models/buildings/shanty_npc_house_combo_E', 'models/buildings/shanty_npc_house_combo_F', 'models/buildings/shanty_npc_house_combo_G', 'models/buildings/shanty_npc_house_combo_H', 'models/buildings/shanty_npc_house_combo_I', 'models/buildings/shanty_npc_house_combo_J', 'models/buildings/shanty_leanto_B', 'models/buildings/shanty_signpost'],
                ['', 'models/buildings/sign1_shanty_a_frame']
              ]
            ]
          }, 'self.setSignFrame'],
          'SignImage': [PROP_UI_COMBO, {
            '["SignFrame"]': [
              [
                ['models/buildings/sign1_eng_a_frame'],
                ['models/buildings/sign1_eng_a_icon_barber', 'models/buildings/sign1_eng_a_icon_blacksmith', 'models/buildings/sign1_eng_a_icon_butcher', 'models/buildings/sign1_eng_a_icon_chemist', 'models/buildings/sign1_eng_a_icon_doctor', 'models/buildings/sign1_eng_a_icon_eitc', 'models/buildings/sign1_eng_a_icon_jeweler', 'models/buildings/sign1_eng_a_icon_shipwright', 'models/buildings/sign1_eng_a_icon_storage', 'models/buildings/sign1_eng_a_icon_store', 'models/buildings/sign1_eng_a_icon_tailor', 'models/buildings/sign1_eng_a_icon_tattoo', 'models/buildings/sign1_eng_a_icon_tavern', 'models/buildings/sign1_eng_a_icon_voodoo', 'models/buildings/sign1_eng_a_icon_weapons']
              ],
              [
                ['models/buildings/sign1_eng_b_frame'],
                ['models/buildings/sign1_eng_b_icon_barbermodels/buildings/sign1_eng_b_icon_blacksmith', 'models/buildings/sign1_eng_b_icon_butcher', 'models/buildings/sign1_eng_b_icon_chemist', 'models/buildings/sign1_eng_b_icon_doctor', 'models/buildings/sign1_eng_b_icon_eitc', 'models/buildings/sign1_eng_b_icon_jeweler', 'models/buildings/sign1_eng_b_icon_shipwright', 'models/buildings/sign1_eng_b_icon_storage', 'models/buildings/sign1_eng_b_icon_store', 'models/buildings/sign1_eng_b_icon_tailor', 'models/buildings/sign1_eng_b_icon_tattoo', 'models/buildings/sign1_eng_b_icon_tavern', 'models/buildings/sign1_eng_b_icon_voodoo', 'models/buildings/sign1_eng_b_icon_weapons']
              ],
              [
                ['models/buildings/sign1_eng_c_frame'],
                ['models/buildings/sign1_eng_c_icon_barber', 'models/buildings/sign1_eng_c_icon_blacksmith', 'models/buildings/sign1_eng_c_icon_butcher', 'models/buildings/sign1_eng_c_icon_chemist', 'models/buildings/sign1_eng_c_icon_doctor', 'models/buildings/sign1_eng_c_icon_eitc', 'models/buildings/sign1_eng_c_icon_jeweler', 'models/buildings/sign1_eng_c_icon_shipwright', 'models/buildings/sign1_eng_c_icon_storage', 'models/buildings/sign1_eng_c_icon_store', 'models/buildings/sign1_eng_c_icon_tailor', 'models/buildings/sign1_eng_c_icon_tattoo', 'models/buildings/sign1_eng_c_icon_tavern', 'models/buildings/sign1_eng_c_icon_voodoo', 'models/buildings/sign1_eng_c_icon_weapons']
              ],
              [
                ['models/buildings/sign1_spanish_a_frame'],
                ['models/buildings/sign1_spanish_a_icon_barber', 'models/buildings/sign1_spanish_a_icon_blacksmith', 'models/buildings/sign1_spanish_a_icon_butcher', 'models/buildings/sign1_spanish_a_icon_chemist', 'models/buildings/sign1_spanish_a_icon_doctor', 'models/buildings/sign1_spanish_a_icon_eitc', 'models/buildings/sign1_spanish_a_icon_jeweler', 'models/buildings/sign1_spanish_a_icon_shipwright', 'models/buildings/sign1_spanish_a_icon_storage', 'models/buildings/sign1_spanish_a_icon_store', 'models/buildings/sign1_spanish_a_icon_tailor', 'models/buildings/sign1_spanish_a_icon_tattoo', 'models/buildings/sign1_spanish_a_icon_tavern', 'models/buildings/sign1_spanish_a_icon_voodoo', 'models/buildings/sign1_spanish_a_icon_weapons']
              ],
              [
                ['models/buildings/sign1_spanish_b_frame'],
                ['models/buildings/sign1_spanish_b_icon_barber', 'models/buildings/sign1_spanish_b_icon_blacksmith', 'models/buildings/sign1_spanish_b_icon_butcher', 'models/buildings/sign1_spanish_b_icon_chemist', 'models/buildings/sign1_spanish_b_icon_doctor', 'models/buildings/sign1_spanish_b_icon_eitc', 'models/buildings/sign1_spanish_b_icon_jeweler', 'models/buildings/sign1_spanish_b_icon_shipwright', 'models/buildings/sign1_spanish_b_icon_storage', 'models/buildings/sign1_spanish_b_icon_store', 'models/buildings/sign1_spanish_b_icon_tailor', 'models/buildings/sign1_spanish_b_icon_tattoo', 'models/buildings/sign1_spanish_b_icon_tavern', 'models/buildings/sign1_spanish_b_icon_voodoo', 'models/buildings/sign1_spanish_b_icon_weapons']
              ],
              [
                ['models/buildings/sign1_spanish_c_frame'],
                ['models/buildings/sign1_spanish_c_icon_barber', 'models/buildings/sign1_spanish_c_icon_blacksmith', 'models/buildings/sign1_spanish_c_icon_butcher', 'models/buildings/sign1_spanish_c_icon_chemist', 'models/buildings/sign1_spanish_c_icon_doctor', 'models/buildings/sign1_spanish_c_icon_eitc', 'models/buildings/sign1_spanish_c_icon_jeweler', 'models/buildings/sign1_spanish_c_icon_shipwright', 'models/buildings/sign1_spanish_c_icon_storage', 'models/buildings/sign1_spanish_c_icon_store', 'models/buildings/sign1_spanish_c_icon_tailor', 'models/buildings/sign1_spanish_c_icon_tattoo', 'models/buildings/sign1_spanish_c_icon_tavern', 'models/buildings/sign1_spanish_c_icon_voodoo', 'models/buildings/sign1_spanish_c_icon_weapons']
              ],
              [
                ['models/buildings/sign1_shanty_a_frame'],
                ['models/buildings/sign1_shanty_a_icon_barber', 'models/buildings/sign1_shanty_a_icon_blacksmith', 'models/buildings/sign1_shanty_a_icon_butcher', 'models/buildings/sign1_shanty_a_icon_chemist', 'models/buildings/sign1_shanty_a_icon_doctor', 'models/buildings/sign1_shanty_a_icon_eitc', 'models/buildings/sign1_shanty_a_icon_jeweler', 'models/buildings/sign1_shanty_a_icon_shipwright', 'models/buildings/sign1_shanty_a_icon_storage', 'models/buildings/sign1_shanty_a_icon_store', 'models/buildings/sign1_shanty_a_icon_tailor', 'models/buildings/sign1_shanty_a_icon_tattoo', 'models/buildings/sign1_shanty_a_icon_tavern', 'models/buildings/sign1_shanty_a_icon_voodoo', 'models/buildings/sign1_shanty_a_icon_weapons']
              ]
            ]
          }, 'self.setSignImage']
        },
        'Scale': 1.0
      }
    },
    AREA_TYPE_BUILDING_INTERIOR: {
      'AreaType': AREA_TYPE_BUILDING_INTERIOR,
      'Create': None,
      'Raycast': 0,
      'Entrance': 'portal_interior_',
      'EntranceSuffix': '1',
      'Selectable': 1,
      'Visual': {
        'Model': 'models/buildings/navy_jail_interior',
        'Models': BUILDING_INTERIOR_LIST,
        'Scale': 1.0
      },
      'Properties': {
        'Instanced': [PROP_UI_CHECK],
        'Name': [PROP_UI_COMBO, [''] + list(PLocalizer.LocationNames.keys())]
      },
      'Defaults': {
        'Instanced': False,
        'Name': ''
      }
    },
    'Jail Interior': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Properties': {
        'JailCells': [PROP_UI_ENTRY]
      },
      'Defaults': {
        'JailCells': '0'
      },
      'Visual': {
        'Model': 'models/buildings/navy_jail_interior',
        'Models': ['models/buildings/navy_jail_interior', 'models/buildings/navy_jail_interior_stairless'],
        'Scale': 1.0
      }
    },
    'Sword Tutorial Interior': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/buildings/shanty_guildhall_interior',
        'Models': ['models/buildings/shanty_guildhall_interior'],
        'Scale': 1.0
      }
    },
    'Spanish Tavern': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/town/bar_exterior'],
        'Scale': 1.0
      }
    },
    'Spanish Walls': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/buildings/LowWallStone_10', 'models/buildings/LowWallStone_100', 'models/buildings/LowWallStone_20', 'models/buildings/LowWallStone_60', 'models/buildings/LowWallStone_Column', 'models/buildings/LowWallStone_Corner', 'models/buildings/LowWallStucco_10', 'models/buildings/LowWallStucco_100', 'models/buildings/LowWallStucco_20', 'models/buildings/LowWallStucco_60', 'models/buildings/LowWallStucco_Column', 'models/buildings/LowWallStucco_Corner', 'models/buildings/TallWallStone_10', 'models/buildings/TallWallStone_100', 'models/buildings/TallWallStone_20', 'models/buildings/TallWallStone_60', 'models/buildings/TallWallStone_Broken10', 'models/buildings/TallWallStone_Column', 'models/buildings/TallWallStone_Corner', 'models/buildings/TallWallStucco_10', 'models/buildings/TallWallStucco_100', 'models/buildings/TallWallStucco_20', 'models/buildings/TallWallStucco_60', 'models/buildings/TallWallStucco_Broken10', 'models/buildings/TallWallStucco_Broken20', 'models/buildings/TallWallStucco_Column', 'models/buildings/TallWallStucco_Corner', 'models/buildings/TallWallStucco_Cracked10', 'models/buildings/TallWallStucco_Cracked20'],
        'Scale': 1.0
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Simple Fort': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/buildings/fort_small', 'models/buildings/fort_medium', 'models/buildings/fort_mid_kings', 'models/buildings/fort_colonnade_kings', 'models/buildings/fort_pier_kings', 'models/buildings/fort_top_kings', 'models/buildings/fort_charles', 'models/buildings/fort_tower', 'models/buildings/pir_m_bld_frt_innerWall_100', 'models/buildings/pir_m_bld_frt_innerWall_200', 'models/buildings/pir_m_bld_frt_innerWall_300', 'models/buildings/pir_m_bld_frt_outerWall_100', 'models/buildings/pir_m_bld_frt_outerWall_200', 'models/buildings/pir_m_bld_frt_outerWall_300', 'models/buildings/pir_m_bld_frt_tower_100', 'models/buildings/pir_m_bld_frt_tower_50'],
        'Scale': 1.0
      }
    },
    'Ship Wreck': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/shipparts/shipwreck_aft',
        'Models': ['models/shipparts/shipwreck_aft', 'models/shipparts/shipwreck_fore']
      }
    },
    'Stairs': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/buildings/brick_stairs_', 'models/buildings/brick_stairs_single', 'models/buildings/brick_stairs_double', 'models/buildings/brick_stairs_quadruple', 'models/buildings/dirt_ramp', 'models/buildings/fort_stair_med', 'models/buildings/landing_single', 'models/buildings/landing_double', 'models/buildings/stone_stairs', 'models/buildings/stone_stairs_single', 'models/buildings/stone_stairs_double', 'models/buildings/stone_stairs_quadruple', 'models/buildings/stone_ramp_single', 'models/buildings/stone_ramp_double', 'models/buildings/stone_ramp_quadruple', 'models/buildings/navy_jail_interior_stairs'],
        'Scale': 1.0
      }
    },
    'Wall': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/buildings/woodfence_B',
        'Models': ['models/buildings/woodfence_B', 'models/buildings/wall_mossy_stone', 'models/buildings/wall_corner_mossy_stone', 'models/buildings/english_wall_10', 'models/buildings/english_wall_20', 'models/buildings/english_wall_60', 'models/buildings/english_wall_100', 'models/buildings/english_wall_col', 'models/buildings/english_wall_no_col_60', 'models/buildings/english_wall_gate', 'models/buildings/english_wall_gate_l', 'models/buildings/english_wall_gate_r', 'models/buildings/woodfence_20', 'models/buildings/woodfence_60'],
        'Scale': 1.0
      }
    }
  },
  'COLL_OBJ': {
    'LOD Sphere': {
      'Create': None,
      'Raycast': 0,
      'Selectable': 1,
      'Visual': {
        'Color': (0.5, 0.5, 0.5, 0.5)
      }
    },
    'Event Sphere': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/misc/smiley'],
        'Color': (0.5, 1.0, 0.5, 0.5)
      },
      'Properties': {
        'Event Type': [PROP_UI_COMBO, ['Capture', 'Port', 'Dock', 'Sneak']],
        'Extra Param': [PROP_UI_ENTRY],
        'Collide Type': [PROP_UI_COMBO, ['Wall', 'Ship', 'Object']]
      },
      'Defaults': {
        'Event Type': 'Capture',
        'Extra Param': '',
        'Collide Type': 'Wall'
      }
    },
    'Avoid Sphere': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/misc/smiley'],
        'Scale': 1.0,
        'Color': (0.75, 0.75, 0.5, 0.5)
      },
      'Properties': {
        'Object Avoided': [PROP_UI_ENTRY]
      }
    },
    'Location Sphere': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/misc/smiley'],
        'Color': (0.5, 0.5, 0.5, 0.5)
      },
      'Properties': {
        'Area Name': [PROP_UI_ENTRY]
      }
    }
  },
  'IMPORT_OBJ': {},
  'MISC_OBJ': {
    LOCATOR_NODE: {
      'Create': None,
      'Movable': 0,
      'Raycast': 0,
      'Selectable': 1,
      'Visual': {
        'Color': (1.0, 1.0, 1.0, 0.5),
        'Scale': 3.0,
        'Models': ['models/misc/smiley']
      }
    },
    DOOR_LOCATOR_NODE: {
      'Create': None,
      'Movable': 0,
      'Raycast': 0,
      'Selectable': 1,
      'Visual': {
        'Color': (1.0, 1.0, 1.0, 0.5),
        'Scale': 3.0,
        'Models': ['models/misc/smiley']
      }
    },
    AREA_TYPE_WORLD_REGION: {
      'AreaType': AREA_TYPE_WORLD_REGION,
      'Create': None,
      'Raycast': 0,
      'Selectable': 0,
      'Visual': {},
      'Properties': {
        'Wave Type': [PROP_UI_COMBO, WAVE_TYPE_LIST, 'self.setWaveType']
      },
      'RpmOnlyPropList': ['Wave Type'],
      'Virtual': 0
    },
    'Ship Model': {
      'Selectable': 0,
      'Visual': {}
    },
    'Shore Wave': {
      'Selectable': 0,
      'Visual': {}
    },
    'Cell Portal Area': {
      'Selectable': 0,
      'Display Data': 0,
      'Visual': {}
    }
  },
  'PROP_OBJ': {
    'Animated Avatar - Skeleton': {
      'Create': Skeleton.Skeleton,
      'NonRpmNode': 1,
      'Raycast': 1,
      'Selectable': 1,
      'Properties': {
        'Animation Track': [PROP_UI_COMBO, ['idle', 'walk', 'run', 'Track 1', 'Track 2'] + CustomAnims.INTERACT_ANIM_NAMES, 'self.setAnimTrack']
      },
      'RandomDefaults': {
        'Animation Track': ['Track 1', 'Track 2'],
        'Hpr': []
      }
    },
    'Animated Avatar - Navy': {
      'Create': NavySailor.NavySailor,
      'NonRpmNode': 1,
      'Raycast': 1,
      'Selectable': 1,
      'Properties': {
        'Animation Track': [PROP_UI_COMBO, ['idle', 'walk', 'run', 'Track 1', 'Track 2'] + CustomAnims.INTERACT_ANIM_NAMES, 'self.setAnimTrack']
      },
      'RandomDefaults': {
        'Animation Track': ['Track 1', 'Track 2', 'idle'],
        'Hpr': []
      }
    },
    'Animated Avatar - Townfolk': {
      'NonRpmNode': 1,
      'Create': Townfolk.Townfolk,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Properties': {
          'Gender': [PROP_UI_COMBO, ['m', 'f']],
          'Shape': [PROP_UI_COMBO, [1, 2, 3]],
          'Hair': [PROP_UI_COMBO, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]],
          'Beard': [PROP_UI_COMBO, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]],
          'Mustache': [PROP_UI_COMBO, [0, 1, 2, 3, 4, 5, 6]],
          'HairColor': [PROP_UI_COMBO, [1, 2, 3, 4, 5, 6, 7, 8]],
          'Skin': [PROP_UI_COMBO, [2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]],
          'Coat': [PROP_UI_COMBO, [0, 1, 2]],
          'CoatColor': [PROP_UI_COMBO, [11, 12, 13, 14, 15]],
          'Shirt': [PROP_UI_COMBO, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]],
          'ShirtColor': [PROP_UI_COMBO, [0, 1, 2, 3, 4]],
          'Pants': [PROP_UI_COMBO, [0, 1, 2, 3]],
          'PantsColor': [PROP_UI_COMBO, [1, 2, 3]],
          'Sock': [PROP_UI_COMBO, [0]],
          'Shoe': [PROP_UI_COMBO, [0, 1, 2]],
          'Belt': [PROP_UI_COMBO, [0, 1, 2, 3]],
          'BeltColor': [PROP_UI_COMBO, [3, 4, 5, 6, 7]],
          'Hat': [PROP_UI_COMBO, [1, 2, 3]]
        },
        'RandomDefaults': {
          'Gender': [],
          'Shape': [],
          'Hair': [],
          'Beard': [],
          'Mustache': [],
          'HairColor': [],
          'Skin': [],
          'Coat': [],
          'CoatColor': [],
          'Shirt': [],
          'ShirtColor': [],
          'Pants': [],
          'PantsColor': [],
          'Sock': [],
          'Shoe': [],
          'Belt': [],
          'BeltColor': [],
          'Hat': []
        }
      },
      'Properties': {
        'Animation Track': [PROP_UI_COMBO, ['idle', 'walk', 'run', 'Track 1', 'Track 2'] + CustomAnims.INTERACT_ANIM_NAMES, 'self.setAnimTrack']
      },
      'RandomDefaults': {
        'Animation Track': ['Track 1', 'Track 2'],
        'Hpr': []
      }
    },
    'Animated Avatar': {
      'Create': 'self.setAnimAvSubCategory',
      'Raycast': 1,
      'Selectable': 1,
      'Properties': {
        'Animation Track': [PROP_UI_COMBO, ['idle', 'walk', 'run', 'Track 1', 'Track 2'] + CustomAnims.INTERACT_ANIM_NAMES, 'self.setAnimTrack'],
        'Category': [PROP_UI_COMBO, ['cast']],
        'SubCategory': [PROP_UI_COMBO, {
          '["Category"]': [
            [
              ['cast'], CAST_MODELS
            ]
          ]
        }, 'self.setAnimAvSubCategory'],
        'Effect Type': [PROP_UI_COMBO, list(ObjectEffects.OBJECT_EFFECTS.keys()), 'self.applyObjectEffects'],
        'PoseAnim': [PROP_UI_ENTRY],
        'PoseFrame': [PROP_UI_ENTRY],
        'StartFrame': [PROP_UI_ENTRY],
        'TrailFX': [PROP_UI_COMBO, ['None', 'Sword', 'Dagger'], 'self.setTrailFX']
      },
      'PropertiesList': ['Category', 'SubCategory', 'Effect Type', 'Animation Track', 'TrailFX', 'StartFrame', 'PoseAnim', 'PoseFrame'],
      'NonRpmPropList': ['Category'],
      'RpmOnlyPropList': ['PoseAnim', 'PoseFrame', 'StartFrame', 'TrailFX'],
      'RandomDefaults': {
        'Animation Track': ['idle'],
        'Hpr': []
      },
      'Defaults': {
        'Category': 'cast',
        'SubCategory': CAST_MODELS[0],
        'PoseAnim': '',
        'PoseFrame': '',
        'StartFrame': '0',
        'TrailFX': 'None',
        'Effect Type': 'None'
      }
    },
    'Animated Prop': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': list(CustomAnims.PROP_ANIMS.keys()),
        'Properties': {
          'Animate': [PROP_UI_COMBO, CustomAnims.getPropAnimList()]
        }
      }
    },
    'Light - Dynamic': {
      'Create': EditorGlobals.LightDynamic,
      'CreateInfo': True,
      'Raycast': 0,
      'Selectable': 1,
      'UprightModel': 'lightbulb',
      'Properties': {
        'Intensity': [PROP_UI_SLIDE, [2]],
        'FlickRate': [PROP_UI_SLIDE],
        'ConeAngle': [PROP_UI_SLIDE, [120, 15]],
        'DropOff': [PROP_UI_SLIDE, [90]],
        'Attenuation': [PROP_UI_SLIDE, [0.5, 0]],
        'LightType': [PROP_UI_COMBO, ['AMBIENT', 'DIRECTIONAL', 'POINT', 'SPOT'], 'self.setLightType']
      },
      'Defaults': {
        'Attenuation': '0.005',
        'ConeAngle': '60.0',
        'DropOff': '0.0',
        'FlickRate': 0.5
      },
      'RpmOnlyPropList': ['Attenuation'],
      'Visual': {
        'Color': (1, 1, 1, 1),
        'Model': 'models/props/light_tool_bulb',
        'Models': ['models/props/light_tool_bulb']
      }
    },
    'Barrel': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/barrel',
        'Models': ['models/props/barrel', 'models/props/barrel_sideways', 'models/props/barrel_group_1', 'models/props/barrel_group_2', 'models/props/barrel_group_3', 'models/props/barrel_worn', 'models/props/barrel_grey']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Baskets': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/basket',
        'Models': ['models/props/basket', 'models/props/basket_rope', 'models/props/box_for_letters', 'models/props/crab_pot']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Bridge': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/buildings/bridge_port_royal',
        'Models': ['models/buildings/bridge_port_royal', 'models/buildings/bridge_columned', 'models/islands/pier_bridge', 'models/buildings/pier_small_wood_bridge', 'models/props/shanty_rope_bridge', 'models/props/shanty_rope_bridge_post']
      }
    },
    'Bucket': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/bucket',
        'Models': ['models/props/bucket', 'models/props/bucket_handles', 'models/props/washtub']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Buoy': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/barrel',
        'Models': ['models/props/barrel', 'models/props/barrel_sideways', 'models/props/barrel_worn', 'models/props/barrel_grey']
      },
      'Properties': {
        'Floating': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'Floating': False
      }
    },
    'Burnt_Props': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/buildings/english_m_burned',
        'Models': ['models/buildings/english_m_burned', 'models/buildings/english_n_burned', 'models/buildings/fort_eitc', 'models/buildings/fort_eitc_burned', 'models/buildings/fort_eitc_annex_1', 'models/buildings/fort_eitc_annex_2', 'models/buildings/fort_eitc_annex_1_burned', 'models/buildings/fort_eitc_annex_2_burned', 'models/buildings/fort_guardhouse', 'models/vegetation/gen_tree_trunk_only_burnt', 'models/vegetation/gen_tree_trunk_only_tall_burnt']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Bush': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/vegetation/bush_a',
        'Models': ['models/vegetation/bush_a', 'models/vegetation/bush_b', 'models/vegetation/bush_c', 'models/vegetation/bush_d', 'models/vegetation/bush_e', 'models/vegetation/bush_f', 'models/vegetation/bush_g', 'models/vegetation/bush_h', 'models/vegetation/bush_i', 'models/vegetation/bush_half_a', 'models/vegetation/bush_half_b', 'models/vegetation/bush_half_c', 'models/vegetation/bush_half_d', 'models/vegetation/bush_leaves', 'models/vegetation/hedge_6', 'models/vegetation/hedge_12']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Cacti': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/vegetation/Cactus_a',
        'Models': ['models/vegetation/Cactus_a', 'models/vegetation/Cactus_b', 'models/vegetation/rock_cacti_group_circle', 'models/vegetation/rock_cacti_group_linear']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Cart': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/cart_reg',
        'Models': ['models/props/cart_reg', 'models/props/cart_flat', 'models/props/cart_broken']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Catapult': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/catapult',
        'Models': ['models/props/catapult']
      }
    },
    'Cemetary': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/crypt1',
        'Models': ['models/props/crypt1', 'models/props/crypt2', 'models/props/headstonesGroup1', 'models/props/headstonesGroup2', 'models/props/headstonesGroup3', 'models/props/headstonesGroup4']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'ChickenCage': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/ChickenCage',
        'Models': ['models/props/ChickenCage']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Chimney': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/buildings/english_chimney',
        'Models': ['models/buildings/english_chimney']
      }
    },
    'Collision Barrier': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/misc/coll_plane_barrier',
        'Models': ['models/misc/coll_plane_barrier', 'models/misc/coll_sphere_barrier', 'models/misc/coll_tube_barrier', 'models/misc/coll_cube_barrier']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Crane': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/Crane',
        'Models': ['models/props/2cranes', 'models/props/Crane', 'models/props/Crane_A', 'models/props/Crane_B']
      }
    },
    'Crate': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/crate', 'models/props/crates_group_1', 'models/props/crates_group_2', 'models/props/crate_net', 'models/props/crate_04', 'models/props/crate_group_net']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Cups': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/cup_tin',
        'Models': ['models/props/cup_tin', 'models/props/cup_tin-old', 'models/props/beerstein']
      }
    },
    'Enemy_Props': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/bone_pile01', 'models/props/bone_pile02', 'models/props/bone_altar', 'models/props/scorpion_nest', 'models/props/wasp_nest']
      }
    },
    'Flower_Pots': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/FlowerPot1', 'models/props/FlowerPot2']
      }
    },
    'Food': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/garlicString', 'models/props/bread_group1', 'models/props/breadbasket', 'models/props/cornbasket', 'models/props/eggbasket', 'models/props/fishbasket', 'models/props/greenbeanbasket', 'models/props/ham', 'models/props/mangobasket', 'models/props/orangebasket', 'models/props/potatobucket', 'models/props/ribs', 'models/props/sausage', 'models/props/tomatobasket']
      }
    },
    'Fountain': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/spanishtown_fountain']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'FountainSmall': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/FountainSmall']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Furniture': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/bed_shanty', 'models/props/bed_shantyB', 'models/props/bed_spanish', 'models/props/bench', 'models/props/bench_bank', 'models/props/bench_shanty_1', 'models/props/bench_shanty_2', 'models/props/bench_stone', 'models/props/bookshelf_shanty', 'models/props/bookshelf_spanish', 'models/props/cabinet_jeweler_caseShort', 'models/props/cabinet_jeweler_caseTall', 'models/props/cabinet_jeweler_cabinetShort', 'models/props/cabinet_jeweler_cabinetTall', 'models/props/cabinet_jeweler_shanty_caseShort', 'models/props/cabinet_jeweler_shanty_cabinetTall', 'models/props/cabinet_jeweler_shanty_cabinetShort', 'models/props/cabinet_shanty', 'models/props/cabinet_shanty_low', 'models/props/cabinet_spanish', 'models/props/cabinet_spanish_low', 'models/props/chair_bank', 'models/props/chair_barber', 'models/props/chair_bar', 'models/props/chair_shanty', 'models/props/counter_shanty', 'models/props/counter_spanish', 'models/props/desk_shanty', 'models/props/stool_bar', 'models/props/stool_bar_tall', 'models/props/stool_shanty', 'models/props/table_bar_round', 'models/props/table_bar_square', 'models/props/table_barber_tools1', 'models/props/table_barber_tools2', 'models/props/table_dice', 'models/props/table_shanty', 'models/props/table_shanty_2']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Furniture - Fancy': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/bookshelf_fancy', 'models/props/cabinet_fancy_low', 'models/props/cabinet_fancy_tall', 'models/props/chair_fancy', 'models/props/clock_fancy_tall', 'models/props/desk_gov', 'models/props/rug_oriental', 'models/props/sofa_fancy', 'models/props/stool_fancy']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Grass': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/vegetation/grass_3feet', 'models/vegetation/grass_8feet', 'models/vegetation/grass_18feet']
      }
    },
    'Hay': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/haystack']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Horse_trough': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/horse_trough']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Interior_furnishings': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/cauldron', 'models/props/fireplace_stucco', 'models/props/interior_column_fort', 'models/props/interior_wall_shanty', 'models/props/interior_wall_spanish', 'models/props/interior_wall_fort', 'models/props/interior_wall_fort_brick', 'models/props/prop_parrot_stand', 'models/props/shop_bsmith_anvilA', 'models/props/shop_bsmith_anvil_block', 'models/props/shop_bsmith_anvilblock', 'models/props/shop_bsmith_anvilblock_interactive', 'models/props/shop_bsmith_bellows', 'models/props/shop_bsmith_bottleA', 'models/props/shop_bsmith_bottleB', 'models/props/shop_bsmith_bucket_swords', 'models/props/shop_bsmith_cutlass', 'models/props/shop_bsmith_cutlass_shiny', 'models/props/shop_bsmith_dagger', 'models/props/shop_bsmith_furness', 'models/props/shop_bsmith_hammerA', 'models/props/shop_bsmith_hammerB', 'models/props/shop_bsmith_hot_iron', 'models/props/shop_bsmith_rack', 'models/props/shop_bsmith_rack_swords', 'models/props/shop_butcher_hanger', 'models/props/shop_butcher_table', 'models/props/shop_doctor_bottles', 'models/props/shop_doctor_bowl', 'models/props/shop_doctor_cabinet', 'models/props/shop_doctor_cabinet_spanish', 'models/props/shop_doctor_table', 'models/props/shop_doctor_table_spanish', 'models/props/shop_doctor_tools', 'models/props/shop_sail_roll', 'models/props/shop_sail_weaver', 'models/props/shop_tatoo_bottles', 'models/props/shop_tatoo_heater', 'models/props/shop_tatoo_sample', 'models/props/shop_voodoo_doll', 'models/props/shop_voodoo_staff', 'models/props/shop_voodoo_staff_skull', 'models/props/shop_weapons_bayonet', 'models/props/shop_weapons_bucket_guns', 'models/props/shop_weapons_double_pistol', 'models/props/shop_weapons_grenade', 'models/props/shop_weapons_pistol', 'models/props/shop_weapons_pistol_cb', 'models/props/shop_weapons_rack_floor', 'models/props/shop_weapons_rack_floor_guns', 'models/props/shop_weapons_rack_table', 'models/props/shop_weapons_rack_table_gun', 'models/props/shop_weapons_rack_wall', 'models/props/shop_weapons_rack_wall_guns', 'models/props/shop_weapons_triple_pistol', 'models/props/stove_potbelly', 'models/props/marketing_jail_column']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Jugs_and_Jars': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/jar', 'models/props/jug', 'models/props/jug_hanging', 'models/props/largejug_A', 'models/props/largejug_A2', 'models/props/largejug_B', 'models/props/pitcher_brown', 'models/props/waterpitcher', 'models/props/winebottle_A', 'models/props/winebottle_B', 'models/props/bottle_brown', 'models/props/bottle_green', 'models/props/bottle_red', 'models/props/bottle_tan']
      }
    },
    'Jungle_Props': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/jungle_fern_a',
        'Models': ['models/vegetation/jungle_fern_a', 'models/vegetation/jungle_fern_b', 'models/vegetation/jungle_fern_c', 'models/vegetation/jungle_plant_a', 'models/vegetation/jungle_plant_b', 'models/vegetation/jungle_plant_c', 'models/vegetation/jungle_plant_d']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Jungle_Props_large': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/cliff_jungle_high',
        'Models': ['models/props/cliff_jungle_high', 'models/props/cliff_jungle_low', 'models/vegetation/jungle_canopy', 'models/vegetation/jungle_canopy_half', 'models/vegetation/jungle_canopy_single']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'LaundryRope': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/LaundryRope',
        'Models': ['models/props/LaundryRope']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Light_Fixtures': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/candle',
        'Models': ['models/props/candle', 'models/props/candle_holder', 'models/props/chandelier_jail', 'models/props/chandelier_govs', 'models/props/lamp', 'models/props/lamp_candle', 'models/props/lamp_hurricane', 'models/props/lamp_over_table', 'models/props/lamp_table_hurricane_candle', 'models/props/lamp_table_hurricane_oil', 'models/props/lamp_wall_hurricane_candle', 'models/props/lamp_wall_hurricane_oil', 'models/props/sconce_govs', 'models/props/torch', 'models/props/torch_no_glow']
      }
    },
    'Log_Stack': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/Log_stack_a',
        'Models': ['models/props/Log_stack_a', 'models/props/Log_stack_b', 'models/props/Log_stack_c', 'models/vegetation/gen_log01', 'models/vegetation/gen_log02', 'models/vegetation/gen_log03', 'models/vegetation/gen_log04', 'models/vegetation/gen_log05', 'models/vegetation/gen_log06', 'models/vegetation/gen_log07', 'models/vegetation/gen_log_group01', 'models/vegetation/gen_log_group02', 'models/vegetation/gen_log_group03']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Military_props': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/islands/pier_gallows',
        'Models': ['models/islands/pier_gallows', 'models/islands/pier_scaffold_1long', 'models/islands/pier_scaffold_2long', 'models/islands/pier_scaffold_end', 'models/islands/pier_scaffold_landing', 'models/islands/pier_scaffold_stairs', 'models/islands/pier_stockade']
      }
    },
    'Mining_props': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/cave_mine_cart', 'models/props/cave_big_wheel', 'models/props/cave_conveyor_tower', 'models/props/cave_rusty_bucket', 'models/props/prop_pick_axe', 'models/props/wheelbarrow']
      }
    },
    'Mortar_Pestle': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/mortar_pestle_stone',
        'Models': ['models/props/mortar_pestle_stone', 'models/props/mortar_pestle_wood']
      }
    },
    'Paddle': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/paddle_A', 'models/props/paddle_B']
      }
    },
    'Pan': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/pan']
      }
    },
    'Pier': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/islands/pier_port_royal_2deck', 'models/islands/pier_platform', 'models/islands/pier_1_kings', 'models/islands/pier_2_kings', 'models/islands/pier_port_royal_1deck', 'models/islands/pier_walkway', 'models/props/ship_parking_booth', 'models/props/ship_valet', 'models/islands/pier_midisland']
      }
    },
    'Pig_stuff': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/pig_pen', 'models/props/pig_pen_b', 'models/props/pigtrough']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Pots': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/pot_A', 'models/props/pot_B']
      }
    },
    'Prop_Groups': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/prop_group01', 'models/props/prop_group02', 'models/props/prop_group03', 'models/props/prop_group04', 'models/props/prop_group_A', 'models/props/prop_group_B', 'models/props/prop_group_C', 'models/props/prop_group_D', 'models/props/prop_group_E', 'models/props/prop_group_F', 'models/props/prop_group_G', 'models/props/prop_group_H']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Prop_Island': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/islands/Big_island_A', 'models/islands/Island_A', 'models/islands/Mid_island_A', 'models/islands/Small_island_A', 'models/islands/Tiny_island_A', 'models/islands/testsimple', 'models/islands/bilgewater_zero', 'models/islands/pvp_a_zero', 'models/islands/pvp_b_zero', 'models/islands/pvpcove_zero', 'models/islands/pvpFortress', 'models/props/bilgewater_gameArea_test', 'models/islands/rambleshack_zero', 'models/islands/madre_del_fuego_zero', 'models/islands/padre_del_fuego', 'models/islands/port_royal_zero', 'models/islands/pir_m_are_isl_portRoyal_zero', 'models/islands/tortuga_zero', 'models/islands/wild_island_a_zero', 'models/islands/wild_island_b_zero', 'models/islands/wild_island_c_zero', 'models/islands/wild_island_d_zero', 'models/islands/wild_island_e_zero', 'models/islands/wild_island_f_zero', 'models/islands/kingshead_zero', 'models/islands/cuba_zero', 'models/islands/rum_runner_zero', 'models/islands/gameAreaSandbox', 'models/islands/pearl_island_zero']
      }
    },
    'Rock': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/rock_group_1_floor',
        'Models': ['models/props/rock_group_1_floor', 'models/props/rock_group_2_floor', 'models/props/rock_group_3_floor', 'models/props/rock_group_5_floor', 'models/props/rock_group_4_floor', 'models/props/rock_group_3_sphere', 'models/props/rock_group_2_sphere', 'models/props/rock_group_1_sphere', 'models/props/rock_group_4_sphere', 'models/props/rock_group_5_sphere', 'models/props/rock_caveA_floor', 'models/props/rock_caveB_sphere', 'models/props/rock_caveC_sphere', 'models/props/rock_1_floor', 'models/props/rock_2_floor', 'models/props/rock_3_floor', 'models/props/rock_4_floor', 'models/props/rock_4_sphere', 'models/props/rock_2_sphere', 'models/props/rock_3_sphere', 'models/props/rock_1_sphere', 'models/props/rockpile_cave_stone', 'models/props/rockpile_cave_volcano', 'models/props/dirt_pile', 'models/props/dirt_pile_cave', 'models/props/dirt_pile_cave_volcano', 'models/props/mound_cave_med', 'models/props/mound_lavacave_med', 'models/props/madre_mound_small', 'models/props/madre_mound_med', 'models/props/madre_mound_large', 'models/props/mound_brown_small', 'models/props/mound_brown_med', 'models/props/mound_brown_large', 'models/props/mound_light_small', 'models/props/mound_light_med', 'models/props/mound_light_med2', 'models/props/mound_light_lrg', 'models/props/volcanomound', 'models/props/zz_dont_use_rock_Dk_1F', 'models/props/zz_dont_use_rock_Dk_2F', 'models/props/zz_dont_use_rock_Dk_3F', 'models/props/zz_dont_use_rock_Dk_4F', 'models/props/zz_dont_use_rock_Lt_1F', 'models/props/zz_dont_use_rock_Lt_2F', 'models/props/zz_dont_use_rock_Lt_3F', 'models/props/zz_dont_use_rock_Lt_4F', 'models/props/zz_dont_use_rocks_Dk_group_1F', 'models/props/zz_dont_use_rocks_Dk_group_2F', 'models/props/zz_dont_use_rocks_Dk_group_3F', 'models/props/zz_dont_use_rocks_LT_group_1F', 'models/props/zz_dont_use_rocks_LT_group_1G', 'models/props/zz_dont_use_rocks_LT_group_2F', 'models/props/zz_dont_use_rocks_LT_group_2G', 'models/props/zz_dont_use_rocks_LT_group_3F', 'models/props/zz_dont_use_rocks_LT_group_3G']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Rope': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/rope_pile',
        'Models': ['models/props/rope_pile']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Sack': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/Sack',
        'Models': ['models/props/Sack', 'models/props/sack_6stack', 'models/props/package_sack', 'models/props/sack_18stack']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Ship_Props': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/anchor',
        'Models': ['models/props/anchor', 'models/ammunition/cannonball', 'models/props/cannonball_stack_square', 'models/props/cannonball_stack_triangle', 'models/props/cannon_broken_prop', 'models/props/cannon_stack_01', 'models/props/cannon_stack_02', 'models/props/plank_zero', 'models/props/wheel_wallprop', 'models/props/mast_broken_prop', 'models/props/mast_broken_prop_2']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Shop - Barber': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/shop_barber_straightRazorOpen',
        'Models': ['models/props/shop_barber_straightRazorOpen', 'models/props/shop_barber_straightRazorClosed', 'models/props/shop_barber_strop', 'models/props/shop_barber_hairClippings', 'models/props/shop_barber_shaveBrushStand', 'models/props/shop_barber_handMirrorSilver', 'models/props/shop_barber_handMirrorWood', 'models/props/shop_barber_hairBrushSilver', 'models/props/shop_barber_hairBrushWood', 'models/props/shop_barber_basin']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Shop - Jeweler': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/shop_jeweler_braceletStand',
        'Models': ['models/props/shop_jeweler_braceletStand', 'models/props/shop_jeweler_braceletStandShanty', 'models/props/shop_jeweler_bust', 'models/props/shop_jeweler_bustShanty', 'models/props/shop_jeweler_junkBarrel01', 'models/props/shop_jeweler_junkBox01', 'models/props/shop_jeweler_ringBox01', 'models/props/shop_jeweler_ringBox02', 'models/props/shop_jeweler_ringBox03', 'models/props/shop_jeweler_ringBoxShanty01', 'models/props/shop_jeweler_ringBoxShanty02', 'models/props/shop_jeweler_ringBoxShanty03']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Shop - Tailor': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/shop_tailor_coatRack_empty',
        'Models': ['models/props/shop_tailor_coatRack_empty', 'models/props/shop_tailor_fabricBolt01', 'models/props/shop_tailor_fabricBolt02', 'models/props/shop_tailor_fabricBolt03', 'models/props/shop_tailor_fabricScraps01', 'models/props/shop_tailor_hatBox_3pile', 'models/props/shop_tailor_hatBox_3stack', 'models/props/shop_tailor_hatStand', 'models/props/shop_tailor_hatStandSkull', 'models/props/shop_tailor_hat_captain', 'models/props/shop_tailor_hat_dressHat', 'models/props/shop_tailor_hat_dressHatFeather', 'models/props/shop_tailor_hat_india', 'models/props/shop_tailor_hat_navyHat', 'models/props/shop_tailor_hat_navyHatFeather', 'models/props/shop_tailor_hat_tricorn', 'models/props/shop_tailor_mannequinFemaleCoat01', 'models/props/shop_tailor_mannequinFemaleNaked', 'models/props/shop_tailor_mannequinFemaleShirt01', 'models/props/shop_tailor_mannequinMaleCoat01', 'models/props/shop_tailor_mannequinMaleNaked', 'models/props/shop_tailor_mannequinMaleShirt01', 'models/props/shop_tailor_scissors', 'models/props/shop_tailor_spinningWheel', 'models/props/shop_tailor_threadPile', 'models/props/shop_tailor_threadRack', 'models/props/shop_tailor_yarnBasket']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Special': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/cave_rock_patron',
        'Models': ['models/props/cave_rock_patron', 'models/misc/smiley']
      }
    },
    'Swamp_props': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/swamp_bush_a',
        'Models': ['models/vegetation/swamp_bush_a', 'models/vegetation/swamp_canopy', 'models/vegetation/swamp_tree_a', 'models/vegetation/swamp_tree_b', 'models/vegetation/swamp_tree_canopy', 'models/vegetation/swamp_tree_roots', 'models/vegetation/swamp_tree_roots_canopy', 'models/vegetation/swamp_stick', 'models/vegetation/swamp_tree_swap_1', 'models/vegetation/swamp_tree_swap_2', 'models/vegetation/swamp_tree_swap_3', 'models/vegetation/swamp_tree_swap_4', 'models/vegetation/swamp_tree_swap_5', 'models/vegetation/swamp_tree_swap_6', 'models/vegetation/swamp_tree_thin']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Swamp_props_small': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/swamp_bench',
        'Models': ['models/props/swamp_bench', 'models/props/swamp_boat', 'models/props/swamp_chair']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Tools': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/broom',
        'Models': ['models/props/broom', 'models/props/butter_churn', 'models/props/prop_keys_dog', 'models/props/rake', 'models/props/pitchfork', 'models/props/wooden_spoon']
      }
    },
    'Treasure Chest': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/prop_coinstack_small', 'models/props/prop_coinstack_large', 'models/props/treasureChest_closed', 'models/props/treasureChest_open', 'models/props/treasure_chandelier', 'models/props/treasure_sconce', 'models/props/treasureTrough', 'models/props/treasureTrough_single']
      }
    },
    'Treasure Duck': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/islands/treasureDuck']
      }
    },
    'Tree': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/vegetation/gen_tree_a',
        'Models': ['models/vegetation/gen_tree_a', 'models/vegetation/gen_tree_b', 'models/vegetation/gen_tree_c', 'models/vegetation/gen_tree_canopy', 'models/vegetation/gen_tree_d', 'models/vegetation/gen_tree_e', 'models/vegetation/gen_tree_f', 'models/vegetation/gen_tree_g', 'models/vegetation/gen_tree_h', 'models/vegetation/gen_tree_trunk_only', 'models/vegetation/gen_tree_trunk_only_tall', 'models/vegetation/fern_tree_a', 'models/vegetation/fern_tree_b', 'models/vegetation/fern_tree_c', 'models/vegetation/fern_tree_d', 'models/vegetation/fern_tree_e', 'models/vegetation/jungle_tree_a', 'models/vegetation/jungle_tree_b', 'models/vegetation/jungle_tree_c', 'models/vegetation/jungle_branch_a', 'models/vegetation/palm_tree_a', 'models/vegetation/palm_tree_b', 'models/vegetation/palm_tree_c', 'models/vegetation/palm_tree_d', 'models/vegetation/palm_tree_e', 'models/vegetation/palm_tree_f', 'models/vegetation/palm_static_sml_a', 'models/vegetation/palm_static_sml_b']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Tree - Animated': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/vegetation/palm_trunk_a_hi',
        'PartName': 'trunk',
        'Models': ['models/vegetation/palm_trunk_a_hi', 'models/vegetation/palm_trunk_b_hi', 'models/vegetation/tree_b_trunk_hi', 'models/vegetation/fern_trunk_a_hi', 'models/vegetation/fern_trunk_b_hi', 'models/vegetation/fern_trunk_c_hi', 'models/vegetation/fern_short_trunk_d_hi', 'models/vegetation/fern_short_trunk_e_hi'],
        'Properties': {
          'Animate': [PROP_UI_COMBO, {
            '["Visual"]["Model"]': [
              [
                ['models/vegetation/palm_trunk_a_hi', 'models/vegetation/palm_trunk_b_hi'],
                ['models/vegetation/palm_trunk_a_idle']
              ],
              [
                ['models/vegetation/tree_b_trunk_hi'],
                ['models/vegetation/tree_b_trunk_idle']
              ],
              [
                ['models/vegetation/fern_trunk_a_hi', 'models/vegetation/fern_trunk_b_hi', 'models/vegetation/fern_trunk_c_hi'],
                ['models/vegetation/fern_trunk_a_idle']
              ],
              [
                ['models/vegetation/fern_short_trunk_d_hi', 'models/vegetation/fern_short_trunk_e_hi'],
                ['models/vegetation/fern_short_trunk_d_idle']
              ]
            ]
          }]
        }
      },
      'SubObjs': {
        'Top Model': {
          'SubObjType': 'Attached',
          'Visual': {
            'Model': 'models/vegetation/palm_leaf_a_hi',
            'Attach': ['trunk', {
              '["Visual"]["Model"]': [
                [
                  ['models/vegetation/fern_short_trunk_d_hi', 'models/vegetation/fern_short_trunk_e_hi'], 'def_trunk_attach_small'
                ]
              ],
              'Default': ['def_trunk_attach']
            }],
            'PartName': 'leaf',
            'Models': ['models/vegetation/palm_leaf_a_hi', 'models/vegetation/palm_leaf_b_hi', 'models/vegetation/palm_leaf_c_hi', 'models/vegetation/tree_b_leaf_hi', 'models/vegetation/fern_leaf_a_hi', 'models/vegetation/fern_leaf_b_hi', 'models/vegetation/fern_short_leaf_c_hi', 'models/vegetation/fern_short_leaf_d_hi'],
            'Properties': {
              'Animate': [PROP_UI_COMBO, {
                '["SubObjs"]["Top Model"]["Visual"]["Model"]': [
                  [
                    ['models/vegetation/palm_leaf_a_hi', 'models/vegetation/palm_leaf_b_hi', 'models/vegetation/palm_leaf_c_hi'],
                    ['models/vegetation/palm_leaf_a_idle']
                  ],
                  [
                    ['models/vegetation/tree_b_leaf_hi'],
                    ['models/vegetation/tree_b_leaf_idle']
                  ],
                  [
                    ['models/vegetation/fern_leaf_a_hi', 'models/vegetation/fern_leaf_b_hi'],
                    ['models/vegetation/fern_leaf_a_idle']
                  ],
                  [
                    ['models/vegetation/fern_short_leaf_c_hi', 'models/vegetation/fern_short_leaf_d_hi'],
                    ['models/vegetation/fern_short_leaf_c_idle']
                  ]
                ]
              }]
            }
          }
        }
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'TreeBase': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/props/TreeBase', 'models/props/planter', 'models/props/planter_straight']
      }
    },
    'Trellis': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/trellisA',
        'Models': ['models/props/trellisA', 'models/props/trellisB', 'models/props/trellis_c', 'models/props/trellis_d', 'models/props/trellis_e']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Trunks': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/Trunk_square',
        'Models': ['models/props/Trunk_square', 'models/props/Trunk_rounded', 'models/props/Trunk_rounded_2']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Tunnel Cap': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Properties': {
        'AltBlockerId': [PROP_UI_ENTRY, '']
      },
      'Visual': {
        'Model': 'models/tunnels/tunnelcap_volcano',
        'Models': ['models/tunnels/tunnelcap_volcano', 'models/tunnels/tunnelcap_jungle', 'models/tunnels/tunnelcap_jungle_cave', 'models/tunnels/tunnelcap_cave_interior', 'models/tunnels/tunnelcap_cave_exterior', 'models/tunnels/tunnelcap_beach_cave']
      }
    },
    'Tunnel Block': {
      'NonRpmNode': 1,
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/tunnels/tunnel_block_cave_big',
        'Models': ['models/tunnels/tunnel_block_cave_big', 'models/tunnels/tunnel_block_cave_small', 'models/tunnels/tunnel_block_cave_lava', 'models/tunnels/tunnel_block_swamp']
      }
    },
    'Vines': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/vegetation/jungle_vine_a',
        'Models': ['models/vegetation/jungle_vine_a', 'models/vegetation/jungle_vine_a_200', 'models/vegetation/jungle_vine_b', 'models/vegetation/jungle_vine_b_150', 'models/vegetation/jungle_vine_b_200', 'models/vegetation/jungle_vine_b_300', 'models/vegetation/moss_a', 'models/vegetation/moss_b']
      }
    },
    'Wall_Hangings': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/Map_01',
        'Models': ['models/props/Map_01', 'models/props/Map_01_unframed', 'models/props/Map_02', 'models/props/Map_02_unframed', 'models/props/Map_03', 'models/props/flag_hanging_spanish', 'models/props/flag_hanging_french', 'models/props/portrait_gov', 'models/props/seascape_battle', 'models/props/seascape_port']
      }
    },
    'Well': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Model': 'models/props/wellA',
        'Models': ['models/props/wellA', 'models/buildings/WellStucco', 'models/props/well_Bstucco']
      },
      'Properties': {
        'DisableCollision': [PROP_UI_CHECK, 'self.setDisableCollision']
      },
      'Defaults': {
        'DisableCollision': False
      }
    },
    'Writing_Paper': {
      'Create': None,
      'Raycast': 1,
      'Selectable': 1,
      'Visual': {
        'Models': ['models/handheld/writing_paper']
      }
    },
    'SFX Node': {
      'NonRpmNode': 1,
      'Create': EditorGlobals.CreateSFX,
      'Raycast': 1,
      'Selectable': 1,
      'UI Name': 'SFX Node',
      'Visual': {
        'Color': (0, 0.65, 0, 1),
        'Model': 'models/misc/smiley',
        'Scale': 1.0,
        'Offset': (0, 0, 1.0)
      },
      'Properties': {
        'SFX Group': [PROP_UI_COMBO, list(SFXList.SOUND_FX_LIST.keys()), 'self.setSfxGroup'],
        'SoundFX': [PROP_UI_COMBO, SFXList.getSFXList(), 'self.setSoundFX'],
        'Volume': [PROP_UI_SLIDE, [1, 0, 0.01], 'self.setSoundFX'],
        'DelayMin': [PROP_UI_SLIDE, [60.0, 0.0, 0.1], 'self.setSoundFX'],
        'DelayMax': [PROP_UI_SLIDE, [60.0, 0.0, 0.1], 'self.setSoundFX']
      },
      'PropertiesList': ['SFX Group', 'SoundFX', 'Volume', 'DelayMin', 'DelayMax'],
      'Defaults': {
        'SFX Group': 'Sword',
        'SoundFX': SFXList.SOUND_FX_LIST['Sword'][0],
        'Volume': 0.5,
        'DelayMin': 0.0,
        'DelayMax': 0.0
      }
    },
    'Imported Object': {
      'NonRpmNode': 1,
      'Selectable': 1,
      'Raycast': 1,
      'Visual': {}
    }
  }
}