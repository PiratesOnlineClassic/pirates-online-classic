# Embedded file name: pirates.leveleditor.worldData.del_fuego_building_int_weapons_2
from pandac.PandaModules import Point3, VBase3, Vec4
objectStruct = {
    'Objects': {
        '1153437552.45dzlu0': {
            'Type': 'Building Interior',
            'Name': 'del_fuego_building_int_weapons_2',
            'AdditionalData': ['interior_spanish_store_weapons'],
            'Instanced': True,
            'Objects': {
                '1157098120.05jasyeung': {
                    'Type': 'Townsperson',
                    'Category': 'Gunsmith',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'bar_wipe',
                    'CustomModel': 'None',
                    'DNA': '1157098120.05jasyeung',
                    'Hpr': VBase3(43.419, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(16.378, -15.048, 0.0),
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Idle',
                    'Team': 'Villager'
                }
            },
            'Visual': {
                'Model': 'models/buildings/interior_spanish_store'
            }
        }
    },
    'Node Links': [],
    'Layers': {},
    'ObjectIds': {
        '1153437552.45dzlu0':
        '["Objects"]["1153437552.45dzlu0"]',
        '1157098120.05jasyeung':
        '["Objects"]["1153437552.45dzlu0"]["Objects"]["1157098120.05jasyeung"]'
    }
}
