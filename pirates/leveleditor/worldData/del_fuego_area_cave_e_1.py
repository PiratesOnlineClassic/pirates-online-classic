# Embedded file name: pirates.leveleditor.worldData.del_fuego_area_cave_e_1
from pandac.PandaModules import Point3, VBase3, Vec4
objectStruct = {
    'AmbientColors': {
        -1: Vec4(0.447059, 0.447059, 0.415686, 1),
        0: Vec4(0.496039, 0.568627, 0.67451, 1),
        2: Vec4(0.74902, 0.737255, 0.737255, 1),
        4: Vec4(0.721569, 0.611765, 0.619608, 1),
        6: Vec4(0.431373, 0.439216, 0.54902, 1),
        8: Vec4(0.389216, 0.426275, 0.569608, 1)
    },
    'DirectionalColors': {
        -1: Vec4(0.717647, 0.721569, 0.72549, 1),
        0: Vec4(0.960784, 0.913725, 0.894118, 1),
        2: Vec4(0.764706, 0.764706, 0.764706, 1),
        4: Vec4(0.439216, 0.176471, 0, 1),
        6: Vec4(0.513726, 0.482353, 0.639216, 1),
        8: Vec4(0.447059, 0.439216, 0.541176, 1)
    },
    'FogColors': {
        -1: Vec4(0.870588, 0.87451, 0.823529, 1),
        0: Vec4(0.27451, 0.192157, 0.211765, 0),
        2: Vec4(0.0313726, 0.054902, 0.0784314, 1),
        4: Vec4(0.231373, 0.203922, 0.184314, 0),
        6: Vec4(0.156863, 0.219608, 0.329412, 1),
        8: Vec4(0.129412, 0.137255, 0.207843, 0)
    },
    'FogRanges': {
        0: 0.0002,
        2: 0.0006000000284984708,
        4: 0.0004,
        6: 0.00039999998989515007,
        8: 0.0002
    },
    'Interact Links':
    [['1176248704.0dxschafe', '1176247936.0dxschafe', 'Bi-directional'],
     ['1176247936.0dxschafe5', '1176248704.0dxschafe3', 'Bi-directional'],
     ['1176247808.0dxschafe0', '1176248704.0dxschafe1', 'Bi-directional'],
     ['1176247936.0dxschafe3', '1176248704.0dxschafe0', 'Bi-directional'],
     ['1189788928.0dxschafe8', '1176248704.0dxschafe', 'Bi-directional']],
    'Objects': {
        '1168057131.73sdnaik': {
            'Type': 'Island Game Area',
            'Name': 'del_fuego_area_cave_e_1',
            'File': '',
            'Instanced': True,
            'Objects': {
                '1168057421.52sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_2',
                    'Hpr': VBase3(115.096, 0.0, 0.0),
                    'Pos': Point3(3.07, -362.101, 41.673),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1168057421.5sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_1',
                    'Hpr': VBase3(-145.621, 0.0, 0.0),
                    'Pos': Point3(296.45, 137.952, 2.31),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1176247808.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attack_sword_slash',
                    'Hpr': VBase3(174.395, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(81.606, -227.305, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Zombie',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176247808.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attack_sword_slash',
                    'Hpr': VBase3(-123.074, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(59.921, -159.973, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Zombie',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176247808.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_summon',
                    'Hpr': VBase3(58.537, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(183.394, -201.739, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Zombie',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176247936.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attack_sword_slash',
                    'Hpr': VBase3(152.42, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(136.056, -181.257, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Corpse',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176247936.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '31.9277',
                    'AnimSet': 'gp_jump',
                    'Hpr': VBase3(85.972, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '4.5482',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(217.096, -220.839, 26.51),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Elite Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176247936.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attack_sword_cleave',
                    'Hpr': VBase3(-162.365, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(218.309, 43.644, 0.079),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Corpse',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176247936.0dxschafe2': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attack_sword_slash',
                    'Hpr': VBase3(-96.37, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(106.666, -41.831, 0.079),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Corpse',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176247936.0dxschafe3': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attack_sword_thrust',
                    'Hpr': VBase3(-73.372, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(97.683, -287.87, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Zombie',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176247936.0dxschafe4': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '6.3253',
                    'AnimSet': 'gp_chant_b',
                    'Hpr': VBase3(120.007, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(172.622, -12.041, 0.079),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Skeleton',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176247936.0dxschafe5': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_summon',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(214.651, -42.64, 0.079),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Fierce Skeleton',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176247936.0dxschafe6': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '14.7590',
                    'AnimSet': 'gp_searching',
                    'Hpr': VBase3(-80.424, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '4.0904',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(184.687, -8.434, 0.079),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Fierce Skeleton',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176248064.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_summon',
                    'Hpr': VBase3(-147.294, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(168.973, -0.628, 0.079),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Elite Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176248192.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attack_sword_slash',
                    'Hpr': VBase3(-47.491, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(139.656, 46.883, 0.079),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Corpse',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176248704.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(205.26, -153.327, 12.235),
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
                '1176248704.0dxschafe0': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(185.893, -281.559, 12.235),
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
                '1176248704.0dxschafe1': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(80.819, -127.664, 12.234),
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
                '1176248704.0dxschafe3': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(253.004, -30.309, 0.079),
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
                '1176248960.0dxschafe': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-78.362, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-13.465, -284.852, 40.155),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176248960.0dxschafe2': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-177.792, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(153.589, -71.659, 0.079),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176249088.0dxschafe': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(15.314, -354.888, 34.471),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176249088.0dxschafe1': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-162.867, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(175.505, -137.258, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176249088.0dxschafe2': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(30.862, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(79.398, -302.776, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176249088.0dxschafe4': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(117.003, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(266.832, 121.962, 0.079),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189552000.0dxschafe': {
                    'Type': 'Effect Node',
                    'EffectName': 'steam_effect',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(66.628, -339.951, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189552000.0dxschafe0': {
                    'Type': 'Effect Node',
                    'EffectName': 'fireplace_effect',
                    'Hpr': VBase3(44.319, 4.807, -4.678),
                    'Pos': Point3(-31.93, -314.578, 42.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189552000.0dxschafe1': {
                    'Type': 'Effect Node',
                    'EffectName': 'fireplace_effect',
                    'Hpr': VBase3(44.319, 4.807, -4.678),
                    'Pos': Point3(15.991, -318.558, 24.168),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189552128.0dxschafe': {
                    'Type': 'Effect Node',
                    'EffectName': 'fireplace_effect',
                    'Hpr': VBase3(0.0, 6.703, 0.0),
                    'Pos': Point3(64.911, -333.134, 14.878),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189552128.0dxschafe0': {
                    'Type': 'Effect Node',
                    'EffectName': 'fireplace_effect',
                    'Hpr': VBase3(0.0, -1.46, 0.0),
                    'Pos': Point3(160.563, -295.535, 16.63),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189552256.0dxschafe': {
                    'Type': 'Effect Node',
                    'EffectName': 'bonfire_effect',
                    'Hpr': VBase3(0.0, -1.46, 0.0),
                    'Pos': Point3(222.279, -249.61, 26.818),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189552256.0dxschafe0': {
                    'Type': 'Effect Node',
                    'EffectName': 'bonfire_effect',
                    'Hpr': VBase3(0.0, -1.46, 0.0),
                    'Pos': Point3(229.057, -164.433, 26.493),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189552256.0dxschafe1': {
                    'Type': 'Effect Node',
                    'EffectName': 'fireplace_effect',
                    'Hpr': VBase3(0.0, -1.46, 0.0),
                    'Pos': Point3(216.206, -122.308, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189554048.0dxschafe': {
                    'Type': 'Effect Node',
                    'EffectName': 'darksteam_effect',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(224.401, -189.81, 24.896),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189554176.0dxschafe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(73.867, 0.0, 0.0),
                    'Pos': Point3(230.214, -165.115, 27.531),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/scorpion_nest'
                    }
                },
                '1189554304.0dxschafe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(159.05, 0.0, 0.0),
                    'Pos': Point3(224.588, -253.166, 26.859),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/scorpion_nest'
                    }
                },
                '1189554304.0dxschafe0': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-85.482, 0.0, 0.0),
                    'Pos': Point3(229.653, -165.732, 12.36),
                    'Scale': VBase3(7.014, 7.014, 7.014),
                    'Visual': {
                        'Model': 'models/props/bone_altar'
                    }
                },
                '1189554432.0dxschafe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-85.482, 0.0, 0.0),
                    'Pos': Point3(223.675, -252.95, 13.046),
                    'Scale': VBase3(7.014, 7.014, 7.014),
                    'Visual': {
                        'Model': 'models/props/bone_altar'
                    }
                },
                '1189554688.0dxschafe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(73.867, 0.0, 0.0),
                    'Pos': Point3(290.344, -185.253, 34.623),
                    'Scale': VBase3(2.283, 2.283, 2.283),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/scorpion_nest'
                    }
                },
                '1189554688.0dxschafe0': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-22.024, 0.0, -11.862),
                    'Pos': Point3(125.87, -256.987, 12.13),
                    'Scale': VBase3(2.283, 2.283, 2.283),
                    'Visual': {
                        'Model': 'models/props/scorpion_nest'
                    }
                },
                '1189554688.0dxschafe1': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(73.867, 0.0, 0.0),
                    'Pos': Point3(48.821, -123.674, 12.234),
                    'Scale': VBase3(2.283, 2.283, 2.283),
                    'Visual': {
                        'Model': 'models/props/scorpion_nest'
                    }
                },
                '1189554816.0dxschafe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(88.425, -3.163, -1.775),
                    'Pos': Point3(224.253, -86.736, -0.942),
                    'Scale': VBase3(2.283, 2.283, 2.283),
                    'Visual': {
                        'Model': 'models/props/scorpion_nest'
                    }
                },
                '1189554816.0dxschafe0': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(0.469, 1.664, -3.223),
                    'Pos': Point3(75.679, -69.866, -1.849),
                    'Scale': VBase3(2.283, 2.283, 2.283),
                    'Visual': {
                        'Model': 'models/props/scorpion_nest'
                    }
                },
                '1189555968.0dxschafe': {
                    'Type': 'Effect Node',
                    'EffectName': 'lavaburst_effect',
                    'Hpr': VBase3(-8.56, -1.443, -0.217),
                    'Pos': Point3(287.099, -187.067, 43.516),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189556736.0dxschafe': {
                    'Type': 'Effect Node',
                    'EffectName': 'lavaburst_effect',
                    'Hpr': VBase3(-8.56, -1.443, -0.217),
                    'Pos': Point3(222.945, -88.101, 6.908),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189556736.0dxschafe0': {
                    'Type': 'Effect Node',
                    'EffectName': 'lavaburst_effect',
                    'Hpr': VBase3(-20.655, -1.366, -0.515),
                    'Pos': Point3(124.715, -257.363, 19.113),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189556736.0dxschafe1': {
                    'Type': 'Effect Node',
                    'EffectName': 'lavaburst_effect',
                    'Hpr': VBase3(-0.531, -1.46, -0.014),
                    'Pos': Point3(49.346, -121.004, 21.978),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189556992.0dxschafe': {
                    'Type': 'Light_Fixtures',
                    'Hpr': VBase3(97.583, 0.0, 0.0),
                    'Pos': Point3(65.479, -282.937, 12.234),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1189557120.0dxschafe': {
                    'Type': 'Light_Fixtures',
                    'Hpr': VBase3(75.322, 0.0, 0.0),
                    'Pos': Point3(66.537, -256.934, 12.234),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1189557120.0dxschafe0': {
                    'Type': 'Light_Fixtures',
                    'Hpr': VBase3(75.322, 0.0, 0.0),
                    'Pos': Point3(56.876, -254.256, 25.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1189557120.0dxschafe2': {
                    'Type': 'Light_Fixtures',
                    'Hpr': VBase3(-159.166, 0.0, 0.0),
                    'Pos': Point3(9.473, -278.019, 39.754),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1189557120.0dxschafe3': {
                    'Type': 'Light_Fixtures',
                    'Hpr': VBase3(89.225, 0.0, 0.0),
                    'Pos': Point3(82.603, 62.681, 0.079),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1189788800.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attack_sword_slash',
                    'Hpr': VBase3(104.06, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(106.38, -285.773, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Navy - Officer',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189788928.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attack_bayonetB',
                    'Hpr': VBase3(109.333, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(115.47, -40.256, 0.079),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Navy - Veteran',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189788928.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attack_bayonetC',
                    'Hpr': VBase3(23.923, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(113.853, -47.059, 0.079),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Navy - Veteran',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189788928.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attack_sword_slash',
                    'Hpr': VBase3(23.923, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(221.451, 36.019, 0.079),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'EITC - Mercenary',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189788928.0dxschafe2': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attack_sword_slash',
                    'Hpr': VBase3(145.779, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(143.363, 51.281, 0.079),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'EITC - Grunt',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189788928.0dxschafe3': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attack_sword_cleave',
                    'Hpr': VBase3(-32.465, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(77.026, -231.648, 12.234),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Navy - Sergeant',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189788928.0dxschafe4': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attack_sword_slash',
                    'Hpr': VBase3(-36.563, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(131.543, -188.194, 12.234),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Navy - Sergeant',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189788928.0dxschafe5': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attack_sword_slash',
                    'Hpr': VBase3(23.923, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(64.926, -163.548, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'EITC - Mercenary',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189788928.0dxschafe6': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attack_sword_slash',
                    'Hpr': VBase3(23.923, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(83.756, -234.57, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Navy - Sergeant',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189788928.0dxschafe7': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '33.1325',
                    'AnimSet': 'gp_moaning',
                    'Hpr': VBase3(85.972, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '4.5482',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(223.584, -182.091, 27.229),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Elite Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189788928.0dxschafe8': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '21.9880',
                    'AnimSet': 'gp_jump',
                    'Hpr': VBase3(63.487, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '4.5482',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(232.274, -131.302, 28.191),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Elite Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189789056.0dxschafe': {
                    'Type': 'Effect Node',
                    'EffectName': 'lavaburst_effect',
                    'Hpr': VBase3(-8.56, -1.443, -0.217),
                    'Pos': Point3(75.321, -70.146, 0.079),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189789056.0dxschafe0': {
                    'Type': 'Effect Node',
                    'EffectName': 'lavaburst_effect',
                    'Hpr': VBase3(-21.994, -1.353, -0.546),
                    'Pos': Point3(72.54, -69.761, 3.444),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190055552.0dchiappe0': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(177.266, -20.683, 0.079),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/candle'
                    }
                },
                '1190055552.0dchiappe1': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(169.21, -13.719, 0.079),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/candle'
                    }
                },
                '1190055552.0dchiappe2': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(181.015, -1.445, 0.079),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/candle'
                    }
                },
                '1190055552.0dchiappe3': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(190.266, -5.582, 0.079),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/candle'
                    }
                },
                '1190055552.0dchiappe4': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(186.417, -16.446, 0.079),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/candle'
                    }
                },
                '1190055552.0dchiappe5': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(173.058, -3.842, 0.079),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/candle'
                    }
                },
                '1190055680.0dchiappe': {
                    'Type': 'Effect Node',
                    'EffectName': 'steam_effect',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(178.455, -11.491, 0.079),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190055680.0dchiappe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(179.244, -9.554, 0.079),
                    'Scale': VBase3(0.364, 0.364, 0.364),
                    'Visual': {
                        'Model': 'models/props/rock_group_1_floor'
                    }
                },
                '1190055808.0dchiappe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(162.409, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(175.969, -13.98, 0.079),
                    'Scale': VBase3(0.408, 0.408, 0.408),
                    'Visual': {
                        'Model': 'models/props/rock_group_2_floor'
                    }
                },
                '1190055808.0dchiappe0': {
                    'Type': 'Enemy_Props',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(177.654, -10.97, 0.079),
                    'Scale': VBase3(2.051, 2.051, 2.051),
                    'Visual': {
                        'Model': 'models/props/bone_altar'
                    }
                },
                '1190056192.0dchiappe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'gp_moaning',
                    'Hpr': VBase3(176.669, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(180.401, -15.297, 0.079),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Skeleton',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190060160.0dchiappe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(116.561, 0.0, 0.0),
                    'Pos': Point3(152.06, -122.704, 12.234),
                    'Scale': VBase3(0.731, 0.404, 1.54),
                    'Visual': {
                        'Color': (0.699999988079071, 0.699999988079071,
                                  0.699999988079071, 1.0),
                        'Model':
                        'models/props/rock_group_1_floor'
                    }
                },
                '1190060160.0dchiappe0': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'barrel_hide',
                    'Hpr': VBase3(-43.984, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '7.2952',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(148.414, -124.007, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Fierce Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190141952.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-56.008, 0.0, 0.0),
                    'Pos': Point3(5.191, -81.313, 36.918),
                    'Scale': VBase3(0.252, 0.252, 0.252),
                    'Visual': {
                        'Color': (0.30000001192092896, 0.30000001192092896,
                                  0.30000001192092896, 1.0),
                        'Model':
                        'models/props/mound_light_med2'
                    }
                },
                '1190142080.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(70.627, 0.0, 0.0),
                    'Pos': Point3(88.897, 78.57, -4.802),
                    'Scale': VBase3(0.265, 0.265, 0.265),
                    'Visual': {
                        'Color': (0.3, 0.3, 0.3, 1.0),
                        'Model': 'models/props/mound_light_med2'
                    }
                },
                '1190145792.0dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-142.387, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-40.972, -252.648, 40.011),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190145920.0dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(158.725, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(1.411, -225.774, 40.011),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190145920.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '2.4096',
                    'AnimSet': 'gp_searching',
                    'Hpr': VBase3(-89.556, -5.205, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-64.623, -212.652, 41.411),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Fierce Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190145920.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '6.9277',
                    'AnimSet': 'gp_jump',
                    'Hpr': VBase3(-86.692, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '6.9518',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(28.371, -230.761, 40.011),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Fierce Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190145920.0dxschafe2': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '2.4096',
                    'AnimSet': 'gp_handdig',
                    'Hpr': VBase3(-108.938, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-54.538, -138.831, 42.067),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190145920.0dxschafe3': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '3.3133',
                    'AnimSet': 'gp_handdig',
                    'Hpr': VBase3(-142.387, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-21.365, -184.488, 40.011),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190146048.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-155.088, 0.0, 0.0),
                    'Objects': {
                        '1190146688.0dxschafe1': {
                            'Type': 'Enemy_Props',
                            'Hpr': VBase3(144.361, 0.0, 0.0),
                            'Pos': Point3(-1.347, 3.117, 1.801),
                            'Scale': VBase3(0.929, 0.929, 0.929),
                            'Visual': {
                                'Model': 'models/props/bone_pile01'
                            }
                        },
                        '1190146688.0dxschafe7': {
                            'Type': 'Enemy_Props',
                            'Hpr': VBase3(-99.097, 0.0, 0.0),
                            'Pos': Point3(2.546, 4.056, 2.196),
                            'Scale': VBase3(0.929, 0.929, 0.929),
                            'Visual': {
                                'Model': 'models/props/bone_pile02'
                            }
                        }
                    },
                    'Pos': Point3(-50.675, -137.347, 40.011),
                    'Scale': VBase3(1.077, 1.077, 1.077),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave_volcano'
                    }
                },
                '1190146048.0dxschafe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(10.727, 0.0, 0.0),
                    'Objects': {
                        '1190146688.0dxschafe': {
                            'Type': 'Enemy_Props',
                            'Hpr': VBase3(-10.727, 0.0, 0.0),
                            'Pos': Point3(2.54, -4.321, 0.548),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/bone_pile01'
                            }
                        },
                        '1190146688.0dxschafe0': {
                            'Type': 'Enemy_Props',
                            'Hpr': VBase3(116.542, 0.0, 0.0),
                            'Pos': Point3(0.404, 4.166, 1.915),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/bone_pile01'
                            }
                        },
                        '1190146688.0dxschafe5': {
                            'Type': 'Enemy_Props',
                            'Hpr': VBase3(105.815, 0.0, 0.0),
                            'Pos': Point3(5.016, -0.123, 1.363),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/bone_pile02'
                            }
                        }
                    },
                    'Pos': Point3(-15.803, -189.526, 40.011),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave_volcano'
                    }
                },
                '1190146048.0dxschafe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(132.384, 0.0, 0.0),
                    'Objects': {
                        '1190146688.0dxschafe2': {
                            'Type': 'Enemy_Props',
                            'Hpr': VBase3(-139.94, 0.0, 0.0),
                            'Pos': Point3(3.884, -0.813, 1.766),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/bone_pile01'
                            }
                        },
                        '1190146816.0dxschafe': {
                            'Type': 'Enemy_Props',
                            'Hpr': VBase3(131.69, 0.0, 0.0),
                            'Pos': Point3(-2.079, -0.1, 2.432),
                            'Scale': VBase3(0.929, 0.929, 0.929),
                            'Visual': {
                                'Model': 'models/props/bone_pile02'
                            }
                        },
                        '1190148224.0dxschafe': {
                            'Type': 'Spawn Node',
                            'AnimSet': 'patient_work',
                            'Hpr': VBase3(-129.213, -1.26, 0.0),
                            'Min Population': '1',
                            'Patrol Radius': '12.0000',
                            'Pause Chance': 100,
                            'Pause Duration': 30,
                            'Pos': Point3(-1.321, 0.128, -2.08),
                            'PoseAnim': '',
                            'PoseFrame': '',
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Spawnables': 'Fierce Skeleton',
                            'Start State': 'Idle',
                            'StartFrame': '0',
                            'Team': 'default',
                            'TrailFX': 'None',
                            'Visual': {
                                'Color': (0, 0, 0.65, 1),
                                'Model': 'models/misc/smiley'
                            }
                        }
                    },
                    'Pos': Point3(-63.604, -207.922, 40.011),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave_volcano'
                    }
                },
                '1190146048.0dxschafe2': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-28.54, 0.0, 0.0),
                    'Objects': {
                        '1190146688.0dxschafe3': {
                            'Type': 'Enemy_Props',
                            'Hpr': VBase3(117.73, 0.0, 0.0),
                            'Pos': Point3(3.12, 2.556, 2.488),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/bone_pile01'
                            }
                        },
                        '1190146688.0dxschafe4': {
                            'Type': 'Enemy_Props',
                            'Hpr': VBase3(-48.541, 0.0, -17.353),
                            'Pos': Point3(-2.13, 3.089, 1.696),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/bone_pile01'
                            }
                        },
                        '1190146688.0dxschafe6': {
                            'Type': 'Enemy_Props',
                            'Hpr': VBase3(134.355, 0.0, 0.0),
                            'Pos': Point3(0.918, -3.171, 1.446),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/bone_pile02'
                            }
                        },
                        '1190146816.0dxschafe0': {
                            'Type': 'Enemy_Props',
                            'Hpr': VBase3(-70.557, 0.0, 0.0),
                            'Pos': Point3(1.331, 1.218, 2.628),
                            'Scale': VBase3(0.929, 0.929, 0.929),
                            'Visual': {
                                'Model': 'models/props/bone_pile02'
                            }
                        }
                    },
                    'Pos': Point3(22.629, -205.353, 40.011),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave_volcano'
                    }
                },
                '1190146048.0dxschafe3': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(147.261, 0.0, 0.0),
                    'Pos': Point3(-6.651, -87.508, 40.011),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.20000000298023224, 0.20000000298023224,
                                  0.20000000298023224, 1.0),
                        'Model':
                        'models/props/rockpile_cave_stone'
                    }
                },
                '1190146176.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(77.03, 0.0, 0.0),
                    'Pos': Point3(10.066, -96.286, 40.011),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.20000000298023224, 0.20000000298023224,
                                  0.20000000298023224, 1.0),
                        'Model':
                        'models/props/rockpile_cave_stone'
                    }
                },
                '1190146176.0dxschafe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(77.03, 0.0, 0.0),
                    'Pos': Point3(-50.142, -137.789, 40.011),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/rockpile_cave_volcano'
                    }
                },
                '1190146176.0dxschafe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-21.486, 0.0, 0.0),
                    'Pos': Point3(-65.394, -208.391, 40.011),
                    'Scale': VBase3(0.831, 0.831, 0.831),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/rockpile_cave_volcano'
                    }
                },
                '1190146432.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '6.0241',
                    'AnimSet': 'gp_handdig',
                    'Hpr': VBase3(117.414, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(25.086, -203.328, 41.831),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190146560.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '13.5542',
                    'AnimSet': 'sleep_sick',
                    'Hpr': VBase3(-160.934, 7.67, -2.98),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-18.491, -185.952, 40.43),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190667008.0dxschafe0': {
                    'Type': 'Animated Avatar',
                    'Category': 'cast',
                    'Animation Track': 'jr_look_idle',
                    'Effect Type': 'Ghost',
                    'Hpr': VBase3(72.0, 0.0, 0.0),
                    'Pos': Point3(220.0, -205.0, 26.832),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(5.0, 5.0, 5.0),
                    'StartFrame': '0',
                    'SubCategory': 'models/char/jr_2000',
                    'TrailFX': 'None'
                },
                '1191633650.61piwanow': {
                    'Type': 'Animated Avatar',
                    'Category': 'cast',
                    'Animation Track': 'jr_look_idle_2',
                    'Effect Type': 'Ghost',
                    'Hpr': VBase3(72.0, 0.0, 0.0),
                    'Pos': Point3(220.0, -205.0, 26.832),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(5.0, 5.0, 5.0),
                    'StartFrame': '0',
                    'SubCategory': 'models/char/jr_2000',
                    'TrailFX': 'None'
                },
                '1191633719.95piwanow': {
                    'Type': 'Effect Node',
                    'EffectName': 'mysticfire_effect',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(220.0, -205.0, 26.832),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1191633790.84piwanow': {
                    'Type': 'Effect Node',
                    'EffectName': 'mysticsmoke_effect',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(220.0, -205.0, 26.832),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193157673.08akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(177.469, -9.701, 0.079),
                    'Scale': VBase3(0.906, 0.906, 1.483),
                    'Visual': {
                        'Model': 'models/misc/coll_cube_barrier'
                    }
                },
                '1219426331.38mtucker': {
                    'Type': 'Skeleton',
                    'Aggro Radius': '7.5301',
                    'AnimSet': 'gp_summon',
                    'AvId': 4,
                    'AvTrack': 0,
                    'Boss': True,
                    'Hpr': VBase3(-104.598, 0.0, 0.0),
                    'Patrol Radius': '4.2048',
                    'Pos': Point3(24.4, -171.935, 40.011),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'TrailFX': 'None'
                }
            },
            'Visual': {
                'Model': 'models/caves/cave_e_zero'
            }
        }
    },
    'Node Links': [],
    'Layers': {
        'Collisions': [
            '1184008208.59kmuller', '1184016064.62kmuller',
            '1184013852.84kmuller', '1185822696.06kmuller',
            '1184006140.32kmuller', '1184002350.98kmuller',
            '1184007573.29kmuller', '1184021176.59kmuller',
            '1184005963.59kmuller', '1188324241.31akelts',
            '1184006537.34kmuller', '1184006605.81kmuller',
            '1187139568.33kmuller', '1188324186.98akelts',
            '1184006730.66kmuller', '1184007538.51kmuller',
            '1184006188.41kmuller', '1184021084.27kmuller',
            '1185824396.94kmuller', '1185824250.16kmuller',
            '1185823630.52kmuller', '1185823760.23kmuller',
            '1185824497.83kmuller', '1185824751.45kmuller',
            '1187739103.34akelts', '1188323993.34akelts',
            '1184016538.29kmuller', '1185822200.97kmuller',
            '1184016225.99kmuller', '1195241421.34akelts',
            '1195242796.08akelts', '1184020642.13kmuller',
            '1195237994.63akelts', '1184020756.88kmuller',
            '1184020833.4kmuller', '1185820992.97kmuller',
            '1185821053.83kmuller', '1184015068.54kmuller',
            '1184014935.82kmuller', '1185821432.88kmuller',
            '1185821701.86kmuller', '1195240137.55akelts',
            '1195241539.38akelts', '1195238422.3akelts', '1195238473.22akelts',
            '1185821453.17kmuller', '1184021269.96kmuller',
            '1185821310.89kmuller', '1185821165.59kmuller',
            '1185821199.36kmuller', '1185822035.98kmuller',
            '1184015806.59kmuller', '1185822059.48kmuller',
            '1185920461.76kmuller', '1194984449.66akelts',
            '1185824206.22kmuller', '1184003446.23kmuller',
            '1184003254.85kmuller', '1184003218.74kmuller',
            '1184002700.44kmuller', '1186705073.11kmuller',
            '1187658531.86akelts', '1186705214.3kmuller',
            '1185824927.28kmuller', '1184014204.54kmuller',
            '1184014152.84kmuller'
        ]
    },
    'ObjectIds': {
        '1168057131.73sdnaik':
        '["Objects"]["1168057131.73sdnaik"]',
        '1168057421.52sdnaik':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1168057421.52sdnaik"]',
        '1168057421.5sdnaik':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1168057421.5sdnaik"]',
        '1176247808.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176247808.0dxschafe"]',
        '1176247808.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176247808.0dxschafe0"]',
        '1176247808.0dxschafe1':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176247808.0dxschafe1"]',
        '1176247936.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176247936.0dxschafe"]',
        '1176247936.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176247936.0dxschafe0"]',
        '1176247936.0dxschafe1':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176247936.0dxschafe1"]',
        '1176247936.0dxschafe2':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176247936.0dxschafe2"]',
        '1176247936.0dxschafe3':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176247936.0dxschafe3"]',
        '1176247936.0dxschafe4':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176247936.0dxschafe4"]',
        '1176247936.0dxschafe5':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176247936.0dxschafe5"]',
        '1176247936.0dxschafe6':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176247936.0dxschafe6"]',
        '1176248064.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176248064.0dxschafe"]',
        '1176248192.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176248192.0dxschafe"]',
        '1176248704.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176248704.0dxschafe"]',
        '1176248704.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176248704.0dxschafe0"]',
        '1176248704.0dxschafe1':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176248704.0dxschafe1"]',
        '1176248704.0dxschafe3':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176248704.0dxschafe3"]',
        '1176248960.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176248960.0dxschafe"]',
        '1176248960.0dxschafe2':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176248960.0dxschafe2"]',
        '1176249088.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176249088.0dxschafe"]',
        '1176249088.0dxschafe1':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176249088.0dxschafe1"]',
        '1176249088.0dxschafe2':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176249088.0dxschafe2"]',
        '1176249088.0dxschafe4':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1176249088.0dxschafe4"]',
        '1189552000.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189552000.0dxschafe"]',
        '1189552000.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189552000.0dxschafe0"]',
        '1189552000.0dxschafe1':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189552000.0dxschafe1"]',
        '1189552128.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189552128.0dxschafe"]',
        '1189552128.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189552128.0dxschafe0"]',
        '1189552256.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189552256.0dxschafe"]',
        '1189552256.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189552256.0dxschafe0"]',
        '1189552256.0dxschafe1':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189552256.0dxschafe1"]',
        '1189554048.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189554048.0dxschafe"]',
        '1189554176.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189554176.0dxschafe"]',
        '1189554304.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189554304.0dxschafe"]',
        '1189554304.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189554304.0dxschafe0"]',
        '1189554432.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189554432.0dxschafe"]',
        '1189554688.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189554688.0dxschafe"]',
        '1189554688.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189554688.0dxschafe0"]',
        '1189554688.0dxschafe1':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189554688.0dxschafe1"]',
        '1189554816.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189554816.0dxschafe"]',
        '1189554816.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189554816.0dxschafe0"]',
        '1189555968.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189555968.0dxschafe"]',
        '1189556736.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189556736.0dxschafe"]',
        '1189556736.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189556736.0dxschafe0"]',
        '1189556736.0dxschafe1':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189556736.0dxschafe1"]',
        '1189556992.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189556992.0dxschafe"]',
        '1189557120.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189557120.0dxschafe"]',
        '1189557120.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189557120.0dxschafe0"]',
        '1189557120.0dxschafe2':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189557120.0dxschafe2"]',
        '1189557120.0dxschafe3':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189557120.0dxschafe3"]',
        '1189788800.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189788800.0dxschafe0"]',
        '1189788928.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189788928.0dxschafe"]',
        '1189788928.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189788928.0dxschafe0"]',
        '1189788928.0dxschafe1':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189788928.0dxschafe1"]',
        '1189788928.0dxschafe2':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189788928.0dxschafe2"]',
        '1189788928.0dxschafe3':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189788928.0dxschafe3"]',
        '1189788928.0dxschafe4':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189788928.0dxschafe4"]',
        '1189788928.0dxschafe5':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189788928.0dxschafe5"]',
        '1189788928.0dxschafe6':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189788928.0dxschafe6"]',
        '1189788928.0dxschafe7':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189788928.0dxschafe7"]',
        '1189788928.0dxschafe8':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189788928.0dxschafe8"]',
        '1189789056.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189789056.0dxschafe"]',
        '1189789056.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1189789056.0dxschafe0"]',
        '1190055552.0dchiappe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190055552.0dchiappe0"]',
        '1190055552.0dchiappe1':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190055552.0dchiappe1"]',
        '1190055552.0dchiappe2':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190055552.0dchiappe2"]',
        '1190055552.0dchiappe3':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190055552.0dchiappe3"]',
        '1190055552.0dchiappe4':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190055552.0dchiappe4"]',
        '1190055552.0dchiappe5':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190055552.0dchiappe5"]',
        '1190055680.0dchiappe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190055680.0dchiappe"]',
        '1190055680.0dchiappe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190055680.0dchiappe0"]',
        '1190055808.0dchiappe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190055808.0dchiappe"]',
        '1190055808.0dchiappe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190055808.0dchiappe0"]',
        '1190056192.0dchiappe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190056192.0dchiappe"]',
        '1190060160.0dchiappe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190060160.0dchiappe"]',
        '1190060160.0dchiappe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190060160.0dchiappe0"]',
        '1190141952.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190141952.0dxschafe"]',
        '1190142080.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190142080.0dxschafe"]',
        '1190145792.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190145792.0dxschafe"]',
        '1190145920.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190145920.0dxschafe"]',
        '1190145920.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190145920.0dxschafe0"]',
        '1190145920.0dxschafe1':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190145920.0dxschafe1"]',
        '1190145920.0dxschafe2':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190145920.0dxschafe2"]',
        '1190145920.0dxschafe3':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190145920.0dxschafe3"]',
        '1190146048.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146048.0dxschafe"]',
        '1190146048.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146048.0dxschafe0"]',
        '1190146048.0dxschafe1':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146048.0dxschafe1"]',
        '1190146048.0dxschafe2':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146048.0dxschafe2"]',
        '1190146048.0dxschafe3':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146048.0dxschafe3"]',
        '1190146176.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146176.0dxschafe"]',
        '1190146176.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146176.0dxschafe0"]',
        '1190146176.0dxschafe1':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146176.0dxschafe1"]',
        '1190146432.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146432.0dxschafe"]',
        '1190146560.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146560.0dxschafe"]',
        '1190146688.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146048.0dxschafe0"]["Objects"]["1190146688.0dxschafe"]',
        '1190146688.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146048.0dxschafe0"]["Objects"]["1190146688.0dxschafe0"]',
        '1190146688.0dxschafe1':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146048.0dxschafe"]["Objects"]["1190146688.0dxschafe1"]',
        '1190146688.0dxschafe2':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146048.0dxschafe1"]["Objects"]["1190146688.0dxschafe2"]',
        '1190146688.0dxschafe3':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146048.0dxschafe2"]["Objects"]["1190146688.0dxschafe3"]',
        '1190146688.0dxschafe4':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146048.0dxschafe2"]["Objects"]["1190146688.0dxschafe4"]',
        '1190146688.0dxschafe5':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146048.0dxschafe0"]["Objects"]["1190146688.0dxschafe5"]',
        '1190146688.0dxschafe6':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146048.0dxschafe2"]["Objects"]["1190146688.0dxschafe6"]',
        '1190146688.0dxschafe7':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146048.0dxschafe"]["Objects"]["1190146688.0dxschafe7"]',
        '1190146816.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146048.0dxschafe1"]["Objects"]["1190146816.0dxschafe"]',
        '1190146816.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146048.0dxschafe2"]["Objects"]["1190146816.0dxschafe0"]',
        '1190148224.0dxschafe':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190146048.0dxschafe1"]["Objects"]["1190148224.0dxschafe"]',
        '1190667008.0dxschafe0':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1190667008.0dxschafe0"]',
        '1191633650.61piwanow':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1191633650.61piwanow"]',
        '1191633719.95piwanow':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1191633719.95piwanow"]',
        '1191633790.84piwanow':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1191633790.84piwanow"]',
        '1193157673.08akelts':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1193157673.08akelts"]',
        '1219426331.38mtucker':
        '["Objects"]["1168057131.73sdnaik"]["Objects"]["1219426331.38mtucker"]'
    }
}
extraInfo = {
    'camPos': Point3(90.7549, -95.2631, 159.381),
    'camHpr': VBase3(146.655, -47.1371, -1.25509e-06),
    'focalLength': 1.39999997616,
    'skyState': 2,
    'fog': 0
}
