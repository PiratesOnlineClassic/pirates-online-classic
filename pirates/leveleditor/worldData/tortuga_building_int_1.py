# Embedded file name: pirates.leveleditor.worldData.tortuga_building_int_1
from pandac.PandaModules import Point3, VBase3, Vec4
objectStruct = {
    'Objects': {
        '1156371286.47dzlu0': {
            'Type': 'Building Interior',
            'Name': '',
            'AdditionalData': ['interior_shanty_npc_house_b'],
            'Instanced': True,
            'Objects': {
                '1169076564.88mike': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'AnimSet': 'default',
                    'CustomModel': 'None',
                    'DNA': '1169076564.88mike',
                    'HelpID': 'NONE',
                    'Hpr': VBase3(-163.875, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(-9.811, 5.244, 0.0),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'ShopID': 'PORT_ROYAL_DEFAULTS',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'Villager',
                    'TrailFX': 'None',
                    'VisSize': ''
                },
                '1172091668.71kmuller': {
                    'Type': 'Furniture',
                    'DisableCollision': False,
                    'Hpr': VBase3(-83.938, 0.0, 0.0),
                    'Pos': Point3(17.166, 13.319, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bed_shanty'
                    }
                },
                '1221246805.52WDIG': {
                    'Type': 'Door Locator Node',
                    'Name': 'door_locator',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(0.047, -29.861, 0.067),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                }
            },
            'VisSize': '',
            'Visual': {
                'Model': 'models/buildings/interior_shanty_npc_house'
            }
        }
    },
    'Node Links': [],
    'Layers': {},
    'ObjectIds': {
        '1156371286.47dzlu0':
        '["Objects"]["1156371286.47dzlu0"]',
        '1169076564.88mike':
        '["Objects"]["1156371286.47dzlu0"]["Objects"]["1169076564.88mike"]',
        '1172091668.71kmuller':
        '["Objects"]["1156371286.47dzlu0"]["Objects"]["1172091668.71kmuller"]',
        '1221246805.52WDIG':
        '["Objects"]["1156371286.47dzlu0"]["Objects"]["1221246805.52WDIG"]'
    }
}
extraInfo = {
    'camPos': Point3(8.8658, -36.5501, 52.358),
    'camHpr': VBase3(27.4882, -41.9919, 0),
    'focalLength': 1.39999997616,
    'skyState': -1,
    'fog': 0
}
