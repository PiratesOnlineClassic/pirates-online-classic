# Embedded file name: pirates.leveleditor.worldData.shipNavyInterceptor1
from pandac.PandaModules import Point3, VBase3, Vec4
objectStruct = {
    'Objects': {
        '1189043220.64gjeon': {
            'Type': 'Ship Part',
            'Name': 'shipNavyInterceptor1',
            'Category': 'Interceptor',
            'File': '',
            'Flagship': True,
            'Objects': {
                '1189043343.25gjeon': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-2.023, 1.038, 8.925),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Area',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189043361.05gjeon': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-9.272, 27.981, 9.837),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189043362.59gjeon': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(7.945, 24.279, 9.436),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189043387.11gjeon': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-0.237, 46.19, 14.617),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189043457.31gjeon': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(8.287, -11.226, 9.412),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189043461.0gjeon': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-6.244, -12.124, 9.541),
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
                    'models/shipparts/interceptorL1-geometry_High',
                    'models/shipparts/interceptorL1-collisions'
                ]
            }
        }
    },
    'Node Links':
    [['1189043361.05gjeon', '1189043343.25gjeon', 'Bi-directional'],
     ['1189043361.05gjeon', '1189043387.11gjeon', 'Bi-directional'],
     ['1189043387.11gjeon', '1189043362.59gjeon', 'Bi-directional'],
     ['1189043343.25gjeon', '1189043362.59gjeon', 'Bi-directional'],
     ['1189043343.25gjeon', '1189043457.31gjeon', 'Bi-directional'],
     ['1189043343.25gjeon', '1189043461.0gjeon', 'Bi-directional']],
    'Layers': {},
    'ObjectIds': {
        '1189043220.64gjeon':
        '["Objects"]["1189043220.64gjeon"]',
        '1189043343.25gjeon':
        '["Objects"]["1189043220.64gjeon"]["Objects"]["1189043343.25gjeon"]',
        '1189043361.05gjeon':
        '["Objects"]["1189043220.64gjeon"]["Objects"]["1189043361.05gjeon"]',
        '1189043362.59gjeon':
        '["Objects"]["1189043220.64gjeon"]["Objects"]["1189043362.59gjeon"]',
        '1189043387.11gjeon':
        '["Objects"]["1189043220.64gjeon"]["Objects"]["1189043387.11gjeon"]',
        '1189043457.31gjeon':
        '["Objects"]["1189043220.64gjeon"]["Objects"]["1189043457.31gjeon"]',
        '1189043461.0gjeon':
        '["Objects"]["1189043220.64gjeon"]["Objects"]["1189043461.0gjeon"]'
    }
}
