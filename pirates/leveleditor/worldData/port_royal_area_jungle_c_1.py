# Embedded file name: pirates.leveleditor.worldData.port_royal_area_jungle_c_1
from pandac.PandaModules import Point3, VBase3, Vec4
objectStruct = {
    'AmbientColors': {
        0: Vec4(0.207843, 0.243137, 0.447059, 1),
        2: Vec4(0.666667, 0.721569, 0.792157, 1),
        4: Vec4(0.721569, 0.611765, 0.619608, 1),
        6: Vec4(0.207843, 0.243137, 0.447059, 1),
        8: Vec4(0.388235, 0.423529, 0.568627, 1)
    },
    'DirectionalColors': {
        0: Vec4(0.956863, 0.909804, 0.894118, 1),
        2: Vec4(1, 1, 1, 1),
        4: Vec4(0.439216, 0.176471, 0, 1),
        6: Vec4(0.513726, 0.482353, 0.639216, 1),
        8: Vec4(0.447059, 0.439216, 0.537255, 1)
    },
    'FogColors': {
        0: Vec4(0.172549, 0.180392, 0.290196, 1),
        2: Vec4(0.894118, 0.894118, 1, 1),
        4: Vec4(0.231373, 0.203922, 0.184314, 1),
        6: Vec4(0.172549, 0.180392, 0.290196, 1),
        8: Vec4(0.129412, 0.137255, 0.203922, 1)
    },
    'FogRanges': {
        0: 0.000699999975040555,
        2: 0.00019999999494757503,
        4: 0.00039999998989515007,
        6: 0.000699999975040555,
        8: 0.0
    },
    'Interact Links':
    [['1175892736.0dxschafe', '1165197469.59Shochet', 'Bi-directional'],
     ['1175892352.0dxschafe', '1175901184.0dxschafe', 'Bi-directional'],
     ['1165197301.95Shochet', '1165197288.56Shochet', 'Bi-directional'],
     ['1175901440.0dxschafe', '1175892736.0dxschafe2', 'Bi-directional'],
     ['1175901568.0dxschafe', '1165197257.5Shochet', 'Bi-directional'],
     ['1175892864.0dxschafe', '1175901952.0dxschafe', 'Bi-directional'],
     ['1175892352.0dxschafe0', '1175902080.0dxschafe', 'Bi-directional'],
     ['1165197451.89Shochet', '1175901312.0dxschafe', 'Bi-directional']],
    'Objects': {
        '1164141722.61sdnaik': {
            'Type': 'Island Game Area',
            'Name': 'port_royal_area_jungle_c_1',
            'File': '',
            'AdditionalData': ['JungleAreaC'],
            'Instanced': True,
            'Objects': {
                '1164141948.44sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_1',
                    'Hpr': VBase3(-4.256, 0.0, 0.0),
                    'Pos': Point3(-632.715, -263.407, 75.0),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1164141948.45sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_2',
                    'Hpr': VBase3(107.903, 0.0, 0.0),
                    'Pos': Point3(304.679, -408.087, 115.611),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1164939070.28Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(128.928, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-405.761, -124.137, 102.347),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164939086.73Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-67.644, 0.0, 0.0),
                    'Min Population': '3',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-372.829, -294.251, 101.077),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Idle',
                    'Team': '1',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164939103.3Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(93.878, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-268.592, -126.948, 117.51),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164939123.75Shochet': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-35.403, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-95.059, -37.62, 125.053),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164939230.45Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(263.794, -247.253, 107.899),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Ambush',
                    'Team': '1',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164939260.28Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(356.371, -315.345, 113.48),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Bat',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164939309.61Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(83.792, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-495.787, -282.083, 87.745),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Idle',
                    'Team': '1',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165197257.5Shochet': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-312.947, -311.051, 107.246),
                    'Priority': '1',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SpawnDelay': '300',
                    'Spawnables': 'Buried Treasure',
                    'Visual': {
                        'Color': (0.8, 0.2, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    },
                    'startingDepth': '30'
                },
                '1165197288.56Shochet': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(101.459, 2.186, 117.559),
                    'Priority': '1',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SpawnDelay': '300',
                    'Spawnables': 'Buried Treasure',
                    'Visual': {
                        'Color': (0.8, 0.2, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    },
                    'startingDepth': '30'
                },
                '1165197301.95Shochet': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-27.089, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(120.252, 15.244, 116.711),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Ambush',
                    'Team': '1',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165197323.8Shochet': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(206.942, 159.753, 91.973),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165197451.89Shochet': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(56.51, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-53.454, -120.773, 125.315),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Early Skeleton',
                    'Start State': 'Ambush',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165197469.59Shochet': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-122.368, -172.88, 128.692),
                    'Priority': '1',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SpawnDelay': '20',
                    'Spawnables': 'Buried Treasure',
                    'Visual': {
                        'Color': (0.8, 0.2, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    },
                    'startingDepth': '15'
                },
                '1175884544.0dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(157.983, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(302.559, -254.332, 115.068),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Idle',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175891840.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(158.581, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(211.261, 154.38, 106.955),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175891968.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_searching',
                    'Hpr': VBase3(-142.63, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(200.184, -277.719, 118.653),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Idle',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175892096.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_jump',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(208.428, -128.728, 117.24),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Muck',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175892224.0dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(56.444, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-44.099, -38.298, 123.644),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Bat',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175892352.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(133.582, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(242.505, 35.299, 112.175),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175892352.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(27.319, 152.447, 117.1),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175892352.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(18.93, 55.016, 119.339),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Ambush',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175892480.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-128.154, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-150.26, 2.243, 126.12),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Early Skeleton',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175892736.0dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-111.044, -187.834, 128.609),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175892736.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(99.868, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-370.686, -173.292, 104.821),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Idle',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175892736.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-390.404, -374.448, 96.8),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175892736.0dxschafe2': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '0.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '1.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-464.324, -399.697, 87.853),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Ambush',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175892864.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-163.473, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-463.553, -95.888, 96.742),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Bat',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175892864.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(104.19, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-103.04, -133.366, 127.245),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Early Skeleton',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175892992.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(144.263, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-550.463, -203.968, 83.951),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175901184.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(267.673, 32.442, 111.381),
                    'Priority': '1',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SpawnDelay': '20',
                    'Spawnables': 'Buried Treasure',
                    'Visual': {
                        'Color': (0.8, 0.2, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    },
                    'startingDepth': '15'
                },
                '1175901312.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-28.718, -99.13, 124.045),
                    'Priority': '1',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SpawnDelay': '20',
                    'Spawnables': 'Buried Treasure',
                    'Visual': {
                        'Color': (0.8, 0.2, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    },
                    'startingDepth': '15'
                },
                '1175901440.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-510.279, -361.398, 83.855),
                    'Priority': '1',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SpawnDelay': '20',
                    'Spawnables': 'Buried Treasure',
                    'Visual': {
                        'Color': (0.8, 0.2, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    },
                    'startingDepth': '15'
                },
                '1175901568.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(100.387, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-314.675, -287.615, 107.733),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Ambush',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175901696.0dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-143.198, -72.187, 127.375),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175901696.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(113.394, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(33.63, 114.009, 117.659),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Idle',
                    'Team': '1',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175901696.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(159.441, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(210.848, -47.225, 114.902),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175901696.0dxschafe2': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(175.144, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(272.21, -163.32, 115.157),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175901696.0dxschafe3': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(125.192, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(329.874, -354.521, 114.541),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Ambush',
                    'Team': '1',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175901952.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-492.95, -117.397, 92.852),
                    'Priority': '1',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SpawnDelay': '20',
                    'Spawnables': 'Buried Treasure',
                    'Visual': {
                        'Color': (0.8, 0.2, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    },
                    'startingDepth': '15'
                },
                '1175902080.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(27.056, 182.359, 116.509),
                    'Priority': '1',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SpawnDelay': '20',
                    'Spawnables': 'Buried Treasure',
                    'Visual': {
                        'Color': (0.8, 0.2, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    },
                    'startingDepth': '15'
                },
                '1179265791.47Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-56.324, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-205.82, -74.384, 126.01),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179265841.94Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-70.028, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-511.784, -195.934, 88.483),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179265866.19Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-68.126, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-303.287, -101.963, 114.378),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179265884.3Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-61.773, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-101.443, 8.502, 124.344),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179265965.55Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-37.707, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-361.817, -234.733, 104.026),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1188441856.0dxschafe': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(28.132, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(284.681, -333.714, 115.999),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1188441856.0dxschafe0': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-160.871, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(151.044, 73.064, 114.509),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189819008.0dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'attack_sword_slash',
                    'Hpr': VBase3(-122.355, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(243.322, -315.532, 117.335),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Clod',
                    'Start State': 'Idle',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189819008.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'attack_bayonetC',
                    'Hpr': VBase3(68.028, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(252.607, -319.177, 117.11),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Navy - Cadet',
                    'Start State': 'Idle',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189819136.0dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'attack_sword_slash',
                    'Hpr': VBase3(177.368, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(233.92, -159.567, 116.376),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Mire',
                    'Start State': 'Idle',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189819136.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'attack_bayonetA',
                    'Hpr': VBase3(-17.251, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(233.501, -166.277, 116.525),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Navy - Guard',
                    'Start State': 'Idle',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190846720.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(366.65, -267.765, 112.937),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190846720.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(317.426, -250.676, 114.547),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190846720.0dxschafe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(287.599, -303.44, 115.776),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190847360.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-533.511, -249.458, 84.517),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190847360.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-424.114, -319.024, 94.658),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190847360.0dxschafe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-339.944, -229.384, 106.61),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190847488.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(62.21, 124.587, 116.479),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190847488.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(165.604, -4.669, 115.577),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190847616.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-138.29, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(168.411, 140.387, 112.571),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192645760.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(255.886, 44.895, 111.53),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192645760.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(113.373, 14.589, 116.957),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192645888.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(213.904, -90.814, 115.673),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192645888.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(254.373, -135.103, 114.42),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192645888.0dxschafe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(246.683, -204.326, 116.771),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192646016.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(204.477, -332.773, 118.728),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192646016.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(305.498, -272.237, 115.041),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192646144.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(235.126, 51.284, 112.104),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192646144.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(63.87, 96.958, 116.978),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192646144.0dxschafe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(209.347, 178.181, 106.955),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192646400.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-1.619, 92.0, 119.292),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192646400.0dxschafe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-163.425, -120.076, 129.02),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192646400.0dxschafe2': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-504.682, -169.48, 90.039),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                }
            },
            'Visual': {
                'Model': 'models/jungles/jungle_c_zero'
            }
        }
    },
    'Node Links':
    [['1190846720.0dxschafe', '1164939260.28Shochet', 'Bi-directional'],
     ['1190846720.0dxschafe', '1190846720.0dxschafe0', 'Bi-directional'],
     ['1190846720.0dxschafe1', '1190846720.0dxschafe0', 'Bi-directional'],
     ['1190846720.0dxschafe1', '1164939260.28Shochet', 'Bi-directional'],
     ['1190847360.0dxschafe', '1175892864.0dxschafe', 'Bi-directional'],
     ['1190847360.0dxschafe', '1190847360.0dxschafe0', 'Bi-directional'],
     ['1190847360.0dxschafe1', '1190847360.0dxschafe0', 'Bi-directional'],
     ['1190847360.0dxschafe1', '1175892864.0dxschafe', 'Bi-directional'],
     ['1175892224.0dxschafe', '1190847488.0dxschafe0', 'Bi-directional'],
     ['1190847488.0dxschafe0', '1190847488.0dxschafe', 'Bi-directional'],
     ['1175892224.0dxschafe', '1190847488.0dxschafe', 'Bi-directional'],
     ['1192645760.0dxschafe0', '1175901696.0dxschafe1', 'Bi-directional'],
     ['1192645760.0dxschafe0', '1192645760.0dxschafe', 'Bi-directional'],
     ['1192645760.0dxschafe', '1175901696.0dxschafe1', 'Bi-directional'],
     ['1192645888.0dxschafe0', '1192645888.0dxschafe1', 'Bi-directional'],
     ['1192645888.0dxschafe0', '1192645888.0dxschafe', 'Bi-directional'],
     ['1192645888.0dxschafe', '1175892096.0dxschafe', 'Bi-directional'],
     ['1192645888.0dxschafe1', '1175892096.0dxschafe', 'Bi-directional'],
     ['1192646016.0dxschafe', '1175901696.0dxschafe2', 'Bi-directional'],
     ['1192646016.0dxschafe', '1192646016.0dxschafe0', 'Bi-directional'],
     ['1192646016.0dxschafe0', '1175901696.0dxschafe2', 'Bi-directional'],
     ['1192646144.0dxschafe', '1175891840.0dxschafe', 'Bi-directional'],
     ['1192646144.0dxschafe', '1192646144.0dxschafe1', 'Bi-directional'],
     ['1192646144.0dxschafe0', '1192646144.0dxschafe1', 'Bi-directional'],
     ['1192646144.0dxschafe0', '1192646144.0dxschafe', 'Bi-directional'],
     ['1192646144.0dxschafe0', '1190847616.0dxschafe', 'Bi-directional'],
     ['1164939086.73Shochet', '1190847360.0dxschafe0', 'Bi-directional'],
     ['1192646400.0dxschafe1', '1192646400.0dxschafe2', 'Bi-directional'],
     ['1192646400.0dxschafe0', '1192646400.0dxschafe1', 'Bi-directional'],
     ['1192646400.0dxschafe1', '1175892864.0dxschafe0', 'Bi-directional'],
     ['1175892480.0dxschafe', '1192646400.0dxschafe1', 'Bi-directional'],
     ['1175892736.0dxschafe0', '1190847360.0dxschafe1', 'Bi-directional'],
     ['1175892992.0dxschafe', '1190847360.0dxschafe', 'Bi-directional']],
    'Layers': {},
    'ObjectIds': {
        '1164141722.61sdnaik':
        '["Objects"]["1164141722.61sdnaik"]',
        '1164141948.44sdnaik':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1164141948.44sdnaik"]',
        '1164141948.45sdnaik':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1164141948.45sdnaik"]',
        '1164939070.28Shochet':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1164939070.28Shochet"]',
        '1164939086.73Shochet':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1164939086.73Shochet"]',
        '1164939103.3Shochet':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1164939103.3Shochet"]',
        '1164939123.75Shochet':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1164939123.75Shochet"]',
        '1164939230.45Shochet':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1164939230.45Shochet"]',
        '1164939260.28Shochet':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1164939260.28Shochet"]',
        '1164939309.61Shochet':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1164939309.61Shochet"]',
        '1165197257.5Shochet':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1165197257.5Shochet"]',
        '1165197288.56Shochet':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1165197288.56Shochet"]',
        '1165197301.95Shochet':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1165197301.95Shochet"]',
        '1165197323.8Shochet':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1165197323.8Shochet"]',
        '1165197451.89Shochet':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1165197451.89Shochet"]',
        '1165197469.59Shochet':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1165197469.59Shochet"]',
        '1175884544.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175884544.0dxschafe"]',
        '1175891840.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175891840.0dxschafe"]',
        '1175891968.0dxschafe0':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175891968.0dxschafe0"]',
        '1175892096.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175892096.0dxschafe"]',
        '1175892224.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175892224.0dxschafe"]',
        '1175892352.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175892352.0dxschafe"]',
        '1175892352.0dxschafe0':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175892352.0dxschafe0"]',
        '1175892352.0dxschafe1':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175892352.0dxschafe1"]',
        '1175892480.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175892480.0dxschafe"]',
        '1175892736.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175892736.0dxschafe"]',
        '1175892736.0dxschafe0':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175892736.0dxschafe0"]',
        '1175892736.0dxschafe1':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175892736.0dxschafe1"]',
        '1175892736.0dxschafe2':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175892736.0dxschafe2"]',
        '1175892864.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175892864.0dxschafe"]',
        '1175892864.0dxschafe0':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175892864.0dxschafe0"]',
        '1175892992.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175892992.0dxschafe"]',
        '1175901184.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175901184.0dxschafe"]',
        '1175901312.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175901312.0dxschafe"]',
        '1175901440.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175901440.0dxschafe"]',
        '1175901568.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175901568.0dxschafe"]',
        '1175901696.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175901696.0dxschafe"]',
        '1175901696.0dxschafe0':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175901696.0dxschafe0"]',
        '1175901696.0dxschafe1':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175901696.0dxschafe1"]',
        '1175901696.0dxschafe2':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175901696.0dxschafe2"]',
        '1175901696.0dxschafe3':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175901696.0dxschafe3"]',
        '1175901952.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175901952.0dxschafe"]',
        '1175902080.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1175902080.0dxschafe"]',
        '1179265791.47Aholdun':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1179265791.47Aholdun"]',
        '1179265841.94Aholdun':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1179265841.94Aholdun"]',
        '1179265866.19Aholdun':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1179265866.19Aholdun"]',
        '1179265884.3Aholdun':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1179265884.3Aholdun"]',
        '1179265965.55Aholdun':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1179265965.55Aholdun"]',
        '1188441856.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1188441856.0dxschafe"]',
        '1188441856.0dxschafe0':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1188441856.0dxschafe0"]',
        '1189819008.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1189819008.0dxschafe"]',
        '1189819008.0dxschafe0':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1189819008.0dxschafe0"]',
        '1189819136.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1189819136.0dxschafe"]',
        '1189819136.0dxschafe0':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1189819136.0dxschafe0"]',
        '1190846720.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1190846720.0dxschafe"]',
        '1190846720.0dxschafe0':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1190846720.0dxschafe0"]',
        '1190846720.0dxschafe1':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1190846720.0dxschafe1"]',
        '1190847360.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1190847360.0dxschafe"]',
        '1190847360.0dxschafe0':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1190847360.0dxschafe0"]',
        '1190847360.0dxschafe1':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1190847360.0dxschafe1"]',
        '1190847488.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1190847488.0dxschafe"]',
        '1190847488.0dxschafe0':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1190847488.0dxschafe0"]',
        '1190847616.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1190847616.0dxschafe"]',
        '1192645760.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1192645760.0dxschafe"]',
        '1192645760.0dxschafe0':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1192645760.0dxschafe0"]',
        '1192645888.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1192645888.0dxschafe"]',
        '1192645888.0dxschafe0':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1192645888.0dxschafe0"]',
        '1192645888.0dxschafe1':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1192645888.0dxschafe1"]',
        '1192646016.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1192646016.0dxschafe"]',
        '1192646016.0dxschafe0':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1192646016.0dxschafe0"]',
        '1192646144.0dxschafe':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1192646144.0dxschafe"]',
        '1192646144.0dxschafe0':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1192646144.0dxschafe0"]',
        '1192646144.0dxschafe1':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1192646144.0dxschafe1"]',
        '1192646400.0dxschafe0':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1192646400.0dxschafe0"]',
        '1192646400.0dxschafe1':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1192646400.0dxschafe1"]',
        '1192646400.0dxschafe2':
        '["Objects"]["1164141722.61sdnaik"]["Objects"]["1192646400.0dxschafe2"]'
    }
}
extraInfo = {
    'camPos': Point3(10.3654, 9.6539, 368.595),
    'camHpr': VBase3(-147.929, -49.1316, 0),
    'focalLength': 1.39999997616
}
