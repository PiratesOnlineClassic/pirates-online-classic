# Embedded file name: pirates.leveleditor.worldData.del_fuego_building_int_tavern_2
from pandac.PandaModules import Point3, VBase3, Vec4
objectStruct = {
    'Interact Links':
    [['1173147520.0mike', '1175734272.0dxschafe', 'Bi-directional']],
    'Objects': {
        '1153434762.53dzlu0': {
            'Type': 'Building Interior',
            'Name': '',
            'AdditionalData': ['interior_tavern'],
            'Instanced': True,
            'Objects': {
                '1173146624.0mike0': {
                    'Type': 'Townsperson',
                    'Category': 'Cast',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'CustomModel': 'None',
                    'DNA': '1173146624.0mike0',
                    'Hpr': VBase3(137.001, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(15.159, 29.178, 1.0),
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Idle',
                    'Team': 'Villager'
                },
                '1173147520.0mike': {
                    'Type': 'Townsperson',
                    'Category': 'Cast',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'CustomModel': 'None',
                    'DNA': '1173147520.0mike',
                    'Hpr': VBase3(-72.34, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(-35.705, 17.063, 1.0),
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Idle',
                    'Team': 'Villager'
                },
                '1175730944.0dxschafe': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'CustomModel': 'None',
                    'DNA': '1175730944.0dxschafe',
                    'Hpr': VBase3(176.925, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(-9.627, 34.661, 1.0),
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Walk',
                    'Team': 'Villager'
                },
                '1175734272.0dxschafe': {
                    'Type': 'Interactive Prop',
                    'Hpr': VBase3(54.862, 0.0, 0.0),
                    'Pos': Point3(-33.495, 9.386, 1.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/chair_shanty'
                    },
                    'interactAble': 'npc',
                    'interactType': 'sit'
                },
                '1190746009.86dxschafe': {
                    'Type': 'Parlor Game',
                    'Category': 'Blackjack',
                    'BetMultiplier': '10',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-40.043, -3.797, 1.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/table_bar_round_parlor'
                    }
                },
                '1190746177.47dxschafe': {
                    'Type': 'Parlor Game',
                    'Category': 'Holdem',
                    'BetMultiplier': '10',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-16.957, -7.529, 1.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/table_bar_round_parlor'
                    }
                }
            },
            'Visual': {
                'Model': 'models/buildings/interior_tavern'
            }
        }
    },
    'Node Links': [],
    'Layers': {},
    'ObjectIds': {
        '1153434762.53dzlu0':
        '["Objects"]["1153434762.53dzlu0"]',
        '1173146624.0mike0':
        '["Objects"]["1153434762.53dzlu0"]["Objects"]["1173146624.0mike0"]',
        '1173147520.0mike':
        '["Objects"]["1153434762.53dzlu0"]["Objects"]["1173147520.0mike"]',
        '1175730944.0dxschafe':
        '["Objects"]["1153434762.53dzlu0"]["Objects"]["1175730944.0dxschafe"]',
        '1175734272.0dxschafe':
        '["Objects"]["1153434762.53dzlu0"]["Objects"]["1175734272.0dxschafe"]',
        '1190746009.86dxschafe':
        '["Objects"]["1153434762.53dzlu0"]["Objects"]["1190746009.86dxschafe"]',
        '1190746177.47dxschafe':
        '["Objects"]["1153434762.53dzlu0"]["Objects"]["1190746177.47dxschafe"]'
    }
}
