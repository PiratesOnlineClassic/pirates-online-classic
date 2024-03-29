# Embedded file name: pirates.leveleditor.worldData.shipSpanishInterceptorL3
from pandac.PandaModules import Point3, VBase3, Vec4
objectStruct = {
    'Objects': {
        '1209584640.0WDIG': {
            'Type': 'Ship Part',
            'Name': 'shipSpanishInterceptorL3',
            'Category': 'Interceptor',
            'File': '',
            'Flagship': False,
            'Objects': {
                '1209584768.0WDIG0': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(0.698, -0.05, 21.807),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Spanish Undead',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1209584768.0WDIG1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(1.293, -13.735, 21.785),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1209584768.0WDIG2': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(2.248, 48.311, 22.817),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1211501824.0WDIG0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(1.7, -54.679, 23.113),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1211501824.0WDIG1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-18.377, -32.621, 22.085),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1211501824.0WDIG2': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(20.179, -33.957, 22.14),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1211501824.0WDIG3': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-24.453, 0.376, 21.808),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1211501824.0WDIG4': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(22.215, 0.015, 21.783),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                }
            },
            'Respawns': True,
            'Team': 'Undead',
            'Visual': {
                'Model': [
                    'models/shipparts/-geometry_High',
                    'models/shipparts/skeletonInterceptorL3-collisions',
                    'models/shipparts/skeletonInterceptorL3-collisions',
                    'models/shipparts/skeletonInterceptorL3-geometry_High'
                ]
            }
        }
    },
    'Node Links':
    [['1209584768.0WDIG0', '1209584768.0WDIG2', 'Bi-directional'],
     ['1209584768.0WDIG0', '1209584768.0WDIG1', 'Bi-directional'],
     ['1211501824.0WDIG0', '1209584768.0WDIG1', 'Bi-directional'],
     ['1211501824.0WDIG4', '1209584768.0WDIG2', 'Bi-directional'],
     ['1211501824.0WDIG2', '1211501824.0WDIG4', 'Bi-directional'],
     ['1211501824.0WDIG0', '1211501824.0WDIG2', 'Bi-directional'],
     ['1211501824.0WDIG3', '1209584768.0WDIG2', 'Bi-directional'],
     ['1211501824.0WDIG3', '1211501824.0WDIG1', 'Bi-directional'],
     ['1211501824.0WDIG1', '1211501824.0WDIG0', 'Bi-directional'],
     ['1211501824.0WDIG1', '1211501824.0WDIG2', 'Bi-directional'],
     ['1211501824.0WDIG3', '1211501824.0WDIG4', 'Bi-directional'],
     ['1211501824.0WDIG3', '1209584768.0WDIG1', 'Bi-directional'],
     ['1211501824.0WDIG1', '1209584768.0WDIG1', 'Bi-directional'],
     ['1209584768.0WDIG1', '1211501824.0WDIG4', 'Bi-directional'],
     ['1209584768.0WDIG1', '1211501824.0WDIG2', 'Bi-directional']],
    'Layers': {},
    'ObjectIds': {
        '1209584640.0WDIG':
        '["Objects"]["1209584640.0WDIG"]',
        '1209584768.0WDIG0':
        '["Objects"]["1209584640.0WDIG"]["Objects"]["1209584768.0WDIG0"]',
        '1209584768.0WDIG1':
        '["Objects"]["1209584640.0WDIG"]["Objects"]["1209584768.0WDIG1"]',
        '1209584768.0WDIG2':
        '["Objects"]["1209584640.0WDIG"]["Objects"]["1209584768.0WDIG2"]',
        '1211501824.0WDIG0':
        '["Objects"]["1209584640.0WDIG"]["Objects"]["1211501824.0WDIG0"]',
        '1211501824.0WDIG1':
        '["Objects"]["1209584640.0WDIG"]["Objects"]["1211501824.0WDIG1"]',
        '1211501824.0WDIG2':
        '["Objects"]["1209584640.0WDIG"]["Objects"]["1211501824.0WDIG2"]',
        '1211501824.0WDIG3':
        '["Objects"]["1209584640.0WDIG"]["Objects"]["1211501824.0WDIG3"]',
        '1211501824.0WDIG4':
        '["Objects"]["1209584640.0WDIG"]["Objects"]["1211501824.0WDIG4"]'
    }
}
extraInfo = {
    'camPos': Point3(-70.984, -0.235405, 220.295),
    'camHpr': VBase3(-84.3865, -67.9897, 0.000173136),
    'focalLength': 1.39999997616,
    'skyState': 2,
    'fog': 0
}
