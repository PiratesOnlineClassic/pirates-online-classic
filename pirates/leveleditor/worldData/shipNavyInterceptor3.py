# Embedded file name: pirates.leveleditor.worldData.shipNavyInterceptor3
from pandac.PandaModules import Point3, VBase3, Vec4
objectStruct = {
    'Objects': {
        '1189043800.81gjeon': {
            'Type': 'Ship Part',
            'Name': 'shipNavyInterceptor3',
            'Category': 'Interceptor',
            'File': '',
            'Flagship': True,
            'Objects': {
                '1189043889.08gjeon': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-3.172, -20.94, 21.729),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Area',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189043903.0gjeon': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(24.052, 8.729, 21.944),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189043905.31gjeon': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-30.379, 11.257, 22.066),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189043907.17gjeon': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(0.169, 26.698, 23.017),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189043910.66gjeon': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-24.742, -40.966, 22.191),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189043913.14gjeon': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(26.44, -40.612, 22.182),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                }
            },
            'Respawns': True,
            'Team': 'EvilNavy',
            'Visual': {
                'Model': [
                    'models/shipparts/interceptorL3-geometry_High',
                    'models/shipparts/interceptorL3-collisions'
                ]
            }
        }
    },
    'Node Links':
    [['1189043889.08gjeon', '1189043905.31gjeon', 'Bi-directional'],
     ['1189043907.17gjeon', '1189043905.31gjeon', 'Bi-directional'],
     ['1189043907.17gjeon', '1189043903.0gjeon', 'Bi-directional'],
     ['1189043903.0gjeon', '1189043889.08gjeon', 'Bi-directional'],
     ['1189043903.0gjeon', '1189043913.14gjeon', 'Bi-directional'],
     ['1189043910.66gjeon', '1189043905.31gjeon', 'Bi-directional']],
    'Layers': {},
    'ObjectIds': {
        '1189043800.81gjeon':
        '["Objects"]["1189043800.81gjeon"]',
        '1189043889.08gjeon':
        '["Objects"]["1189043800.81gjeon"]["Objects"]["1189043889.08gjeon"]',
        '1189043903.0gjeon':
        '["Objects"]["1189043800.81gjeon"]["Objects"]["1189043903.0gjeon"]',
        '1189043905.31gjeon':
        '["Objects"]["1189043800.81gjeon"]["Objects"]["1189043905.31gjeon"]',
        '1189043907.17gjeon':
        '["Objects"]["1189043800.81gjeon"]["Objects"]["1189043907.17gjeon"]',
        '1189043910.66gjeon':
        '["Objects"]["1189043800.81gjeon"]["Objects"]["1189043910.66gjeon"]',
        '1189043913.14gjeon':
        '["Objects"]["1189043800.81gjeon"]["Objects"]["1189043913.14gjeon"]'
    }
}
