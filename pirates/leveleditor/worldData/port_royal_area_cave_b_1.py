# Embedded file name: pirates.leveleditor.worldData.port_royal_area_cave_b_1
from pandac.PandaModules import Point3, VBase3, Vec4
objectStruct = {
    'AmbientColors': {
        0: Vec4(0.572549, 0.219608, 0.364706, 1),
        2: Vec4(0.564706, 0.219608, 0.364706, 1),
        4: Vec4(0.572549, 0.219608, 0.364706, 1),
        6: Vec4(0.572549, 0.219608, 0.364706, 1),
        8: Vec4(0.572549, 0.219608, 0.364706, 1)
    },
    'DirectionalColors': {
        0: Vec4(0.133333, 0.2, 0, 1),
        2: Vec4(0.129412, 0.2, 0, 1),
        4: Vec4(0.133333, 0.2, 0, 1),
        6: Vec4(0.133333, 0.2, 0, 1),
        8: Vec4(0.133333, 0.2, 0, 1)
    },
    'FogColors': {
        0: Vec4(0.0313726, 0.0509804, 0.0745098, 0),
        2: Vec4(0.0313726, 0.0509804, 0.0666667, 1),
        4: Vec4(0.0313726, 0.0509804, 0.0745098, 0),
        6: Vec4(0.0313726, 0.0509804, 0.0745098, 0),
        8: Vec4(0.0313726, 0.0509804, 0.0745098, 0)
    },
    'FogRanges': {
        0: 0.0,
        2: 0.0,
        4: 0.0,
        6: 0.0,
        8: 0.0
    },
    'Interact Links':
    [['1176159360.0dxschafe', '1165019476.34Shochet', 'Bi-directional'],
     ['1176159104.0dxschafe0', '1176159104.0dxschafe', 'Bi-directional'],
     ['1176158080.0dxschafe', '1165019328.28Shochet', 'Bi-directional']],
    'Objects': {
        '1165001772.05sdnaik': {
            'Type': 'Island Game Area',
            'Name': 'port_royal_area_cave_b_1',
            'File': '',
            'Instanced': True,
            'Objects': {
                '1165001975.75sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_1',
                    'Hpr': VBase3(-98.823, 0.0, 0.0),
                    'Pos': Point3(407.795, 202.769, 1.938),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1165001975.77sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_2',
                    'Hpr': VBase3(-5.579, 0.0, 0.0),
                    'Pos': Point3(-535.718, 237.303, 77.641),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1165019328.28Shochet': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-43.12, -160.704, 32.334),
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
                '1165019476.34Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(65.172, 19.812, 27.497),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Vampire Bat',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165019501.84Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '6.0241',
                    'AnimSet': 'gp_chant_b',
                    'Hpr': VBase3(-22.353, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(29.027, -179.993, 28.77),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Corpse',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165019770.53Shochet': {
                    'Type': 'Rope',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(99.322, -114.135, 23.919),
                    'Scale': VBase3(1.404, 1.404, 1.404),
                    'Visual': {
                        'Model': 'models/props/rope_pile'
                    }
                },
                '1165197827.77Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-219.829, -109.567, 55.796),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Vampire Bat',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175127779.71kmuller': {
                    'Type': 'Tunnel Cap',
                    'Hpr': VBase3(91.976, 0.0, 0.0),
                    'Pos': Point3(-534.106, 237.425, 79.975),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/tunnels/tunnelcap_cave_interior'
                    }
                },
                '1175127913.08kmuller': {
                    'Type': 'Tunnel Cap',
                    'Hpr': VBase3(-16.185, 0.0, 0.0),
                    'Pos': Point3(404.179, 196.552, 3.342),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/tunnels/tunnelcap_cave_interior'
                    }
                },
                '1176158080.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '4.2169',
                    'AnimSet': 'gp_chant_b',
                    'Hpr': VBase3(-73.885, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(21.138, -169.644, 29.474),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Corpse',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176158208.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '4.5181',
                    'AnimSet': 'gp_jump',
                    'Hpr': VBase3(-145.121, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(24.083, -152.619, 28.92),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176158976.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(452.012, -157.684, 2.175),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Bat',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176159104.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(212.821, -253.894, 12.337),
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
                '1176159104.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(181.049, -227.371, 17.005),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Vampire Bat',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176159232.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_searching',
                    'Hpr': VBase3(94.892, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-165.66, -15.591, 57.078),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176159360.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(114.081, -30.115, 25.324),
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
                '1176159360.0dxschafe0': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(53.311, -39.351, 28.03),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176159360.0dxschafe1': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-148.284, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-35.011, 131.798, 31.948),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176159360.0dxschafe10': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-44.592, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(280.801, 63.668, 2.175),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176159360.0dxschafe2': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(52.227, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-303.428, 54.994, 63.492),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176159360.0dxschafe3': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(31.799, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-238.203, -61.675, 55.796),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176159360.0dxschafe4': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(70.486, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-376.883, 178.419, 72.713),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176159360.0dxschafe5': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-121.675, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-471.14, 200.606, 78.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176159360.0dxschafe6': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-63.038, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-65.347, 8.507, 33.309),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176159360.0dxschafe7': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(27.133, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(67.029, -215.335, 27.435),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176159360.0dxschafe8': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(86.406, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(179.483, -182.58, 17.311),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176159360.0dxschafe9': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-18.497, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(299.135, -133.258, 2.175),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176159488.0dxschafe': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(157.518, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(393.404, 153.79, 2.175),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176159488.0dxschafe0': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(91.238, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(395.981, -169.326, 2.175),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176159488.0dxschafe1': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(128.459, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(235.776, -105.144, 6.165),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176159488.0dxschafe2': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-89.342, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-211.451, 9.695, 55.796),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1185388672.0dxschafe003': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(12.899, 0.0, 0.0),
                    'Pos': Point3(78.013, 15.294, 28.345),
                    'Scale': VBase3(0.699, 0.699, 0.699),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe004': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(32.503, 0.0, 0.0),
                    'Pos': Point3(-133.238, 174.148, 38.334),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe006': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(32.133, 4.364, 9.679),
                    'Pos': Point3(204.27, -118.338, 14.387),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe007': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-21.535, 0.0, 0.0),
                    'Pos': Point3(100.272, -134.885, 27.977),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe008': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(75.316, 0.0, 0.0),
                    'Pos': Point3(33.036, -166.186, 30.099),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe010': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-9.25, 0.0, 0.0),
                    'Pos': Point3(-39.647, 92.595, 34.444),
                    'Scale': VBase3(1.125, 1.125, 1.125),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe03': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-118.045, 0.0, -32.883),
                    'Pos': Point3(76.471, 16.057, 28.728),
                    'Scale': VBase3(0.699, 0.699, 0.699),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe04': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-98.441, 0.0, -32.883),
                    'Pos': Point3(-135.682, 174.437, 38.883),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe06': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-98.712, -10.166, -35.934),
                    'Pos': Point3(201.967, -118.029, 15.364),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe07': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-152.479, 0.0, -32.883),
                    'Pos': Point3(99.071, -132.737, 28.526),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe08': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-55.628, 0.0, -32.883),
                    'Pos': Point3(31.097, -167.599, 30.634),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe10': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-140.194, 0.0, -32.883),
                    'Pos': Point3(-41.482, 94.669, 35.061),
                    'Scale': VBase3(1.125, 1.125, 1.125),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe103': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(114.371, 0.0, 0.0),
                    'Pos': Point3(74.404, 13.624, 28.054),
                    'Scale': VBase3(0.699, 0.699, 0.699),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1185388672.0dxschafe105': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(3.757, 0.0, 0.0),
                    'Pos': Point3(1.107, 66.794, 30.738),
                    'Scale': VBase3(0.639, 0.639, 0.358),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1185388672.0dxschafe106': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(133.975, 0.0, 0.0),
                    'Pos': Point3(-137.301, 170.165, 37.918),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1185388672.0dxschafe108': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(134.445, 8.579, -6.265),
                    'Pos': Point3(200.209, -122.32, 14.821),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1185388672.0dxschafe109': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(79.937, 0.0, 0.0),
                    'Pos': Point3(94.663, -133.935, 27.561),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1185388672.0dxschafe110': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(176.788, 0.0, 0.0),
                    'Pos': Point3(32.769, -171.726, 29.693),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1185388672.0dxschafe112': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(92.222, 0.0, 0.0),
                    'Pos': Point3(-46.001, 92.27, 33.976),
                    'Scale': VBase3(1.125, 1.125, 1.125),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1185388672.0dxschafe113': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(41.818, 0.0, 0.0),
                    'Pos': Point3(34.4, 44.666, 30.279),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1185388672.0dxschafe303': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(78.488, 0.0, 0.0),
                    'Pos': Point3(77.42, 18.539, 27.692),
                    'Scale': VBase3(0.699, 0.699, 0.699),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe304': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(98.092, 0.0, 0.0),
                    'Pos': Point3(-135.595, 178.237, 37.401),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe306': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(98.092, 10.609, 0.0),
                    'Pos': Point3(201.773, -114.269, 13.793),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe307': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(44.054, 0.0, 0.0),
                    'Pos': Point3(102.198, -130.576, 27.044),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe308': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(140.905, 0.0, 0.0),
                    'Pos': Point3(28.641, -164.823, 29.189),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe403': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(78.488, 0.0, 0.0),
                    'Pos': Point3(73.848, 16.365, 28.276),
                    'Scale': VBase3(0.699, 0.699, 0.699),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe404': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(98.092, 0.0, 0.0),
                    'Pos': Point3(-139.365, 173.593, 38.236),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe406': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(98.092, 10.609, 0.0),
                    'Pos': Point3(198.23, -118.881, 15.421),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe407': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(44.054, 0.0, 0.0),
                    'Pos': Point3(96.225, -130.252, 27.879),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe408': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(140.905, 0.0, 0.0),
                    'Pos': Point3(29.022, -170.643, 30.003),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185388672.0dxschafe503': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(41.878, 0.0, 0.0),
                    'Pos': Point3(77.857, 13.001, 28.137),
                    'Scale': VBase3(0.699, 0.699, 0.699),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1185388672.0dxschafe504': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(61.482, 0.0, 0.0),
                    'Pos': Point3(107.673, -92.252, 28.345),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1185388672.0dxschafe505': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-68.736, 0.0, 0.0),
                    'Pos': Point3(-0.537, 64.039, 30.781),
                    'Scale': VBase3(0.639, 0.639, 0.358),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1185388672.0dxschafe506': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(61.482, 0.0, 0.0),
                    'Pos': Point3(-132.348, 170.984, 38.037),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1185388672.0dxschafe508': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(61.008, 8.499, 6.374),
                    'Pos': Point3(205.099, -121.511, 14.014),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1185388672.0dxschafe509': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(7.444, 0.0, 0.0),
                    'Pos': Point3(98.234, -137.464, 27.68),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1185388672.0dxschafe510': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(104.295, 0.0, 0.0),
                    'Pos': Point3(35.77, -167.859, 29.809),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1185388672.0dxschafe512': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(19.729, 0.0, 0.0),
                    'Pos': Point3(-41.271, 89.273, 34.11),
                    'Scale': VBase3(1.125, 1.125, 1.125),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1185388672.0dxschafe513': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-30.675, 0.0, 0.0),
                    'Pos': Point3(35.031, 39.686, 30.398),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1185388800.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '4.5181',
                    'AnimSet': 'gp_jump',
                    'Hpr': VBase3(-158.397, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '11.1867',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-99.23, 158.427, 34.804),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1185388800.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '3.0120',
                    'AnimSet': 'gp_chant_b',
                    'Hpr': VBase3(41.536, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-88.438, 161.895, 34.323),
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
                '1185388800.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '4.5181',
                    'AnimSet': 'gp_chant_a',
                    'Hpr': VBase3(159.219, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-85.771, 152.767, 34.206),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1185388800.0dxschafe2': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '3.9157',
                    'AnimSet': 'gp_chant_a',
                    'Hpr': VBase3(-75.327, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-90.252, 139.508, 34.406),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1185925504.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(56.339, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(-41.513, 92.759, 32.241),
                    'Scale': VBase3(1.125, 1.125, 1.125),
                    'Visual': {
                        'Color': (0.84, 0.75, 0.75, 1.0),
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1185925504.0dxschafe0': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(77.007, -4.049, 8.379),
                    'Pos': Point3(-124.799, 113.211, 35.854),
                    'Scale': VBase3(2.728, 2.728, 2.728),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1185925504.0dxschafe1': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-0.55, 0.0, 0.0),
                    'Pos': Point3(-39.16, 89.937, 34.099),
                    'Scale': VBase3(1.125, 1.125, 1.125),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186083737.45kmuller': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': VBase3(80.589, 0.0, 0.0),
                    'Pos': Point3(122.451, -149.448, 19.487),
                    'Scale': VBase3(0.728, 0.804, 0.804),
                    'Visual': {
                        'Model': 'models/props/rock_caveC_sphere'
                    }
                },
                '1186172544.0dxschafe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-0.549, 0.0, 0.0),
                    'Pos': Point3(85.757, -12.307, 29.473),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186172544.0dxschafe0': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-135.0, 0.0, 0.0),
                    'Pos': Point3(78.727, -18.168, 28.178),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186172672.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(78.839, -9.639, 27.697),
                    'Scale': VBase3(1.385, 1.385, 1.385),
                    'Visual': {
                        'Color': (0.85, 0.72, 0.66, 1.0),
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1186173056.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(78.488, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(76.901, 14.951, 26.976),
                    'Scale': VBase3(0.699, 0.699, 0.699),
                    'Visual': {
                        'Color': (0.85, 0.72, 0.66, 1.0),
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1186173056.0dxschafe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(98.092, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(-134.572, 173.152, 36.376),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.85, 0.72, 0.66, 1.0),
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1186173056.0dxschafe2': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-32.126, 0.0, 0.0),
                    'Objects': {
                        '1186773504.0dchiappe': {
                            'Type': 'Rock',
                            'DisableCollision': False,
                            'Hpr': VBase3(32.126, 0.0, 0.0),
                            'Pos': Point3(5.679, -4.248, 0.376),
                            'Scale': VBase3(0.522, 0.522, 0.522),
                            'Visual': {
                                'Model': 'models/props/rock_group_5_sphere'
                            }
                        }
                    },
                    'Pos': Point3(1.439, 64.23, 30.186),
                    'Scale': VBase3(0.639, 0.639, 0.358),
                    'Visual': {
                        'Color': (0.85, 0.79, 0.82, 1.0),
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1186173440.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(5.935, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(37.282, 41.827, 28.737),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.85, 0.72, 0.66, 1.0),
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1186173824.0dxschafe1': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(53.755, 0.0, 0.0),
                    'Pos': Point3(4.028, 66.386, 30.751),
                    'Scale': VBase3(0.818, 0.818, 0.458),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186174208.0dxschafe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(163.468, 0.0, 6.237),
                    'Pos': Point3(0.569, 66.102, 30.862),
                    'Scale': VBase3(0.808, 0.818, 0.464),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186174464.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(140.905, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(32.742, -167.782, 28.19),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Color': (0.85, 0.72, 0.66, 1.0),
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1186174464.0dxschafe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(98.092, 10.609, 0.0),
                    'Objects': {},
                    'Pos': Point3(202.604, -119.381, 12.731),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.85, 0.98, 0.98, 1.0),
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1186174464.0dxschafe2': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(44.054, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(98.683, -134.39, 26.019),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (1.0, 0.9, 0.94, 1.0),
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1186174592.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(98.092, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(105.449, -90.084, 26.684),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/props/rock_caveB_sphere'
                    }
                },
                '1186174720.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-90.493, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(-1.431, -55.158, 26.435),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.85, 0.98, 0.98, 1.0),
                        'Model': 'models/props/rock_caveC_sphere'
                    }
                },
                '1186174720.0dxschafe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-61.92, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(89.951, -92.312, 20.955),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.52, 0.69, 0.81, 1.0),
                        'Model': 'models/props/rock_caveB_sphere'
                    }
                },
                '1186174976.0dxschafe0': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(133.974, 0.0, 0.0),
                    'Pos': Point3(-42.415, 92.616, 35.106),
                    'Scale': VBase3(1.125, 1.125, 1.125),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186175104.0dxschafe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(163.468, 0.0, -19.911),
                    'Pos': Point3(1.98, 62.046, 30.707),
                    'Scale': VBase3(0.731, 0.818, 0.513),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186176640.0dxschafe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(8.092, 0.0, 0.0),
                    'Pos': Point3(-134.929, 171.449, 38.82),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186176640.0dxschafe0': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-65.589, 0.0, 0.0),
                    'Pos': Point3(-136.538, 166.715, 37.143),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186176640.0dxschafe1': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(23.092, 0.0, 0.0),
                    'Pos': Point3(-130.708, 170.735, 36.888),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186176640.0dxschafe10': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-150.0, 0.0, 0.0),
                    'Pos': Point3(70.043, -5.983, 28.644),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186176640.0dxschafe11': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-65.589, 0.0, 0.0),
                    'Pos': Point3(80.745, -6.057, 31.313),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186176640.0dxschafe12': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-161.512, 0.0, 0.0),
                    'Pos': Point3(74.782, 11.053, 27.516),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186176640.0dxschafe13': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(63.488, 0.0, 0.0),
                    'Pos': Point3(79.838, 16.596, 27.646),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186176640.0dxschafe14': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-65.589, 0.0, 0.0),
                    'Pos': Point3(76.635, 15.219, 28.707),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186176640.0dxschafe2': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(50.935, 0.0, 0.0),
                    'Pos': Point3(37.298, 42.935, 31.383),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186176640.0dxschafe22': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-56.889, 0.0, 0.0),
                    'Pos': Point3(-138.749, 174.63, 38.523),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176640.0dxschafe23': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(128.092, 0.0, 0.0),
                    'Pos': Point3(-133.124, 177.966, 37.658),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176640.0dxschafe24': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(143.092, 0.0, 0.0),
                    'Pos': Point3(-137.623, 170.782, 37.994),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176640.0dxschafe25': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-56.889, 0.0, 0.0),
                    'Pos': Point3(-132.716, 170.917, 38.308),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176640.0dxschafe3': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-65.589, 0.0, 0.0),
                    'Pos': Point3(36.483, 38.302, 30.204),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186176640.0dxschafe30': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-98.577, 0.0, 0.0),
                    'Pos': Point3(0.141, 67.596, 30.53),
                    'Scale': VBase3(0.818, 0.818, 0.458),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176640.0dxschafe31': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-56.888, 0.0, 0.0),
                    'Pos': Point3(-1.803, 65.85, 30.296),
                    'Scale': VBase3(0.818, 0.818, 0.458),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176640.0dxschafe32': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-2.126, 0.0, 0.0),
                    'Pos': Point3(2.946, 64.901, 31.172),
                    'Scale': VBase3(0.818, 0.818, 0.458),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176640.0dxschafe33': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(42.874, 0.0, 0.0),
                    'Pos': Point3(0.42, 63.973, 30.946),
                    'Scale': VBase3(0.818, 0.818, 0.458),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176640.0dxschafe38': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(3.488, 0.0, 0.0),
                    'Pos': Point3(75.851, 18.695, 27.903),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176640.0dxschafe39': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-56.888, 0.0, 0.0),
                    'Pos': Point3(79.28, 18.396, 27.69),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176640.0dxschafe4': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(20.935, 0.0, 0.0),
                    'Pos': Point3(33.634, 42.73, 30.572),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186176640.0dxschafe40': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(78.488, 0.0, 0.0),
                    'Pos': Point3(73.784, 16.282, 28.266),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176640.0dxschafe41': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(48.488, 0.0, 0.0),
                    'Pos': Point3(78.786, 15.28, 28.106),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176640.0dxschafe42': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-9.065, 0.0, 0.0),
                    'Pos': Point3(40.732, 38.676, 29.755),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176640.0dxschafe43': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-56.889, 0.0, 0.0),
                    'Pos': Point3(37.371, 46.055, 30.665),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176640.0dxschafe44': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-56.889, 0.0, 0.0),
                    'Pos': Point3(39.968, 41.823, 30.807),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176640.0dxschafe45': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-56.889, 0.0, 0.0),
                    'Pos': Point3(33.984, 40.119, 30.24),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176640.0dxschafe46': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-9.065, 0.0, 0.0),
                    'Pos': Point3(39.611, 44.277, 31.54),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176640.0dxschafe8': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-65.589, 0.0, 0.0),
                    'Pos': Point3(82.142, -15.503, 28.896),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186176640.0dxschafe9': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(135.0, 0.0, 0.0),
                    'Pos': Point3(74.745, -12.765, 29.384),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186176768.0dxschafe16': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(164.054, 0.0, 0.0),
                    'Pos': Point3(101.34, -128.882, 26.925),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176768.0dxschafe17': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(59.054, 0.0, 0.0),
                    'Pos': Point3(101.314, -136.258, 27.505),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176768.0dxschafe18': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(14.054, 0.0, 0.0),
                    'Pos': Point3(93.55, -134.974, 27.182),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176768.0dxschafe19': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-0.946, 0.0, 0.0),
                    'Pos': Point3(102.204, -131.158, 27.529),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176768.0dxschafe20': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-56.889, 0.0, 0.0),
                    'Pos': Point3(96.329, -129.042, 27.251),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176768.0dxschafe21': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-56.889, 0.0, 0.0),
                    'Pos': Point3(96.715, -132.902, 28.236),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176768.0dxschafe22': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-174.095, 0.0, 0.0),
                    'Pos': Point3(31.325, -163.467, 29.394),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176768.0dxschafe23': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-56.889, 0.0, 0.0),
                    'Pos': Point3(31.437, -171.34, 29.817),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176768.0dxschafe24': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-56.889, 0.0, 0.0),
                    'Pos': Point3(34.934, -168.632, 30.414),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176768.0dxschafe25': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(155.905, 0.0, 0.0),
                    'Pos': Point3(28.008, -165.849, 29.508),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176768.0dxschafe26': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-56.889, 0.0, 0.0),
                    'Pos': Point3(34.132, -164.894, 29.512),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176768.0dxschafe27': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(155.905, 0.0, 0.0),
                    'Pos': Point3(31.642, -167.594, 30.606),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176768.0dxschafe3': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-56.889, 0.0, 0.0),
                    'Pos': Point3(80.194, -7.314, 31.515),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176768.0dxschafe4': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-165.0, 0.0, 0.0),
                    'Pos': Point3(76.946, -7.618, 30.824),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176768.0dxschafe5': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-56.889, 0.0, 0.0),
                    'Pos': Point3(72.05, -6.686, 29.25),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176768.0dxschafe6': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-56.889, 0.0, 0.0),
                    'Pos': Point3(77.505, -12.794, 30.252),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186176768.0dxschafe7': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(180.0, 0.0, 0.0),
                    'Pos': Point3(76.814, -5.069, 30.09),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186177536.0dxschafe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(164.054, 0.0, 0.0),
                    'Pos': Point3(100.968, -132.37, 28.085),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186177536.0dxschafe0': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(120.0, 0.0, 0.0),
                    'Pos': Point3(98.853, -134.32, 28.371),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_altar'
                    }
                },
                '1186177664.0dxschafe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(104.054, 0.0, 0.0),
                    'Pos': Point3(97.401, -137.957, 27.358),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186177664.0dxschafe0': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(59.054, 0.0, 0.0),
                    'Pos': Point3(100.461, -131.853, 28.296),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186177664.0dxschafe1': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-45.946, 0.0, 0.0),
                    'Pos': Point3(97.223, -131.572, 28.381),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186177664.0dxschafe2': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-162.114, 0.0, 0.0),
                    'Pos': Point3(98.747, -129.032, 27.653),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186177664.0dxschafe21': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-81.908, -10.609, 0.0),
                    'Pos': Point3(205.475, -117.605, 13.658),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186177664.0dxschafe22': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(75.599, 9.818, 4.039),
                    'Pos': Point3(201.284, -115.876, 15.114),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186177664.0dxschafe23': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(8.092, 0.0, 10.609),
                    'Pos': Point3(202.563, -120.13, 15.365),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186177664.0dxschafe24': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-97.157, -10.244, -2.775),
                    'Pos': Point3(198.805, -117.265, 15.473),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186177664.0dxschafe25': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(75.945, 0.0, 0.0),
                    'Pos': Point3(35.272, -166.652, 29.938),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186177664.0dxschafe3': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(125.905, 0.0, 0.0),
                    'Pos': Point3(32.596, -169.122, 30.627),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186177664.0dxschafe4': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(75.945, 0.0, 0.0),
                    'Pos': Point3(27.037, -167.605, 29.352),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186177664.0dxschafe5': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(75.945, 0.0, 0.0),
                    'Pos': Point3(33.344, -161.335, 28.453),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186177664.0dxschafe6': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-159.095, 0.0, 0.0),
                    'Pos': Point3(32.963, -167.658, 30.451),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186177664.0dxschafe7': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(75.945, 0.0, 0.0),
                    'Pos': Point3(28.718, -167.857, 30.562),
                    'Scale': VBase3(0.975, 0.975, 0.975),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186177792.0dxschafe10': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(75.599, 9.818, 4.039),
                    'Pos': Point3(203.514, -120.904, 15.021),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186177792.0dxschafe5': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(75.599, 9.818, 4.039),
                    'Pos': Point3(202.916, -113.732, 13.588),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186177792.0dxschafe6': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-51.478, -9.174, 5.35),
                    'Pos': Point3(204.213, -118.559, 14.459),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186177792.0dxschafe7': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(75.599, 9.818, 4.039),
                    'Pos': Point3(201.384, -118.11, 15.679),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186177792.0dxschafe8': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-6.663, -2.731, 10.255),
                    'Pos': Point3(204.495, -115.866, 13.777),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186177792.0dxschafe9': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(75.599, 9.818, 4.039),
                    'Pos': Point3(206.913, -115.635, 12.426),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186435200.0dchiappe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '3.0120',
                    'AnimSet': 'gp_summon',
                    'Hpr': VBase3(-74.038, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-104.244, 144.474, 35.029),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186435200.0dchiappe0': {
                    'Type': 'Effect Node',
                    'EffectName': 'fireplace_effect',
                    'Hpr': VBase3(180.844, 0.0, 0.0),
                    'Pos': Point3(-94.302, 152.61, 34.585),
                    'Scale': VBase3(0.35, 0.35, 0.35),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186508544.0dchiappe': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-30.197, 156.445, 31.731),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1186508672.0dchiappe1': {
                    'Type': 'Log_Stack',
                    'DisableCollision': False,
                    'Hpr': VBase3(29.131, 0.0, 0.0),
                    'Pos': Point3(-96.947, 153.687, 34.703),
                    'Scale': VBase3(0.844, 0.844, 0.844),
                    'Visual': {
                        'Model': 'models/props/Log_stack_c'
                    }
                },
                '1186508800.0dchiappe': {
                    'Type': 'Effect Node',
                    'EffectName': 'cratersmoke_effect',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-93.598, 152.481, 34.554),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186615808.0dchiappe': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-132.205, 112.308, 36.276),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1186617088.0dchiappe0': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(-136.597, 111.647, 35.956),
                    'Scale': VBase3(0.574, 0.574, 0.574),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1186617216.0dchiappe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-56.522, -0.006, -0.02),
                    'Pos': Point3(-53.873, 200.881, 31.989),
                    'Scale': VBase3(3.216, 3.216, 3.216),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1186617600.0dchiappe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-49.072, 0.0, 0.0),
                    'Pos': Point3(-122.923, 152.445, 35.859),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.56, 0.73, 0.7, 1.0),
                        'Model': 'models/props/rock_group_3_sphere'
                    }
                },
                '1186619008.0dchiappe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-98.008, 93.826, 33.958),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.7, 0.69, 0.59, 1.0),
                        'Model': 'models/props/rockpile_cave_stone'
                    }
                },
                '1186695680.0dchiappe': {
                    'Type': 'Light - Dynamic',
                    'Attenuation': '0.005',
                    'ConeAngle': '15.0000',
                    'DropOff': '0.0000',
                    'FlickRate': '0.0000',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Intensity': '0.7952',
                    'LightType': 'AMBIENT',
                    'Pos': Point3(-94.62, 105.058, 121.6),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.54, 0.4, 0.51, 1.0),
                        'Model': 'models/props/light_tool_bulb'
                    }
                },
                '1186695936.0dchiappe': {
                    'Type': 'Light - Dynamic',
                    'Attenuation': '0.005',
                    'ConeAngle': '89.0060',
                    'DropOff': '2.7108',
                    'FlickRate': '0.5000',
                    'Hpr': VBase3(-98.05, -82.774, -95.961),
                    'Intensity': '1.0120',
                    'LightType': 'SPOT',
                    'Pos': Point3(-44.718, -3.163, 183.599),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (1.0, 0.48, 0.3, 1.0),
                        'Model': 'models/props/light_tool_bulb'
                    }
                },
                '1186705968.08dchiappe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(102.405, 0.0, 0.0),
                    'Pos': Point3(-135.835, 140.126, 17.017),
                    'Scale': VBase3(14.497, 14.497, 14.497),
                    'Visual': {
                        'Model': 'models/props/bone_altar'
                    }
                },
                '1186706066.42dchiappe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(312.554, 0.0, 0.0),
                    'Pos': Point3(65.0, 50.0, 48.0),
                    'Scale': VBase3(8.25, 8.25, 8.25),
                    'Visual': {
                        'Model': 'models/props/bone_altar'
                    }
                },
                '1186706108.61dchiappe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(278.482, 358.281, 349.683),
                    'Pos': Point3(49.0, 79.0, 46.5),
                    'Scale': VBase3(8.25, 8.25, 8.25),
                    'Visual': {
                        'Model': 'models/props/bone_altar'
                    }
                },
                '1186707328.0dchiappe': {
                    'Type': 'Light_Fixtures',
                    'Hpr': VBase3(79.435, 0.0, 0.0),
                    'Pos': Point3(45.503, 89.499, 45.747),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1186707328.0dchiappe0': {
                    'Type': 'Light_Fixtures',
                    'Hpr': VBase3(-102.219, 0.0, 0.0),
                    'Pos': Point3(36.468, 70.655, 46.666),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1186707328.0dchiappe1': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(55.169, 46.773, 46.18),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1186707328.0dchiappe2': {
                    'Type': 'Light_Fixtures',
                    'Hpr': VBase3(-14.267, 0.0, 0.0),
                    'Pos': Point3(67.351, 38.959, 49.791),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1186707456.0dchiappe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '3.3133',
                    'AnimSet': 'gp_chant_b',
                    'Hpr': VBase3(-149.57, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '4.7771',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(7.119, 82.826, 30.076),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186707456.0dchiappe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '3.3133',
                    'AnimSet': 'gp_jump',
                    'Hpr': VBase3(-134.556, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '5.3494',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-17.609, 78.199, 31.178),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Early Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186707456.0dchiappe2': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '3.3133',
                    'AnimSet': 'gp_chant_a',
                    'Hpr': VBase3(35.895, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '5.6928',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(16.835, 48.664, 29.647),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186707968.0dchiappe': {
                    'Type': 'Light - Dynamic',
                    'Attenuation': '0.005',
                    'ConeAngle': '50.4217',
                    'DropOff': '3.2530',
                    'FlickRate': '0.1867',
                    'Hpr': VBase3(87.374, 20.872, 82.511),
                    'Intensity': '1.2771',
                    'LightType': 'SPOT',
                    'Pos': Point3(70.18, 72.966, 53.438),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.49, 0.33, 0.35, 1.0),
                        'Model': 'models/props/light_tool_bulb'
                    }
                },
                '1186708736.0dchiappe': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(19.62, -107.291, 29.536),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1186708736.0dchiappe0': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(5.322, -125.837, 30.174),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1186708736.0dchiappe1': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(86.305, -103.83, 26.567),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1186708736.0dchiappe2': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(107.321, -125.605, 25.633),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1186708736.0dchiappe4': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '2.4096',
                    'AnimSet': 'gp_chant_a',
                    'Hpr': VBase3(-56.936, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '5.2349',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-0.783, 41.494, 30.432),
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
                '1186709120.0dchiappe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '25.0000',
                    'AnimSet': 'crazy',
                    'Hpr': VBase3(-85.303, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(31.519, -167.839, 29.011),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Early Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186709120.0dchiappe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '4.5181',
                    'AnimSet': 'gp_summon',
                    'Hpr': VBase3(134.713, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '6.3795',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(37.487, -153.333, 28.333),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Early Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186709376.0dchiappe': {
                    'Type': 'Effect Node',
                    'EffectName': 'bonfire_effect',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(31.864, -167.314, 28.996),
                    'Scale': VBase3(0.5, 0.5, 0.5),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186709632.0dchiappe': {
                    'Type': 'Light - Dynamic',
                    'Attenuation': '0.005',
                    'ConeAngle': '51.6867',
                    'DropOff': '14.0964',
                    'FlickRate': '0.7727',
                    'Hpr': VBase3(-93.607, 64.731, -75.424),
                    'Intensity': '0.9036',
                    'LightType': 'SPOT',
                    'Pos': Point3(18.689, 68.718, 30.999),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (1.0, 0.32, 0.13, 1.0),
                        'Model': 'models/props/light_tool_bulb'
                    }
                },
                '1186710400.0dchiappe': {
                    'Type': 'Light - Dynamic',
                    'Attenuation': '0.005',
                    'ConeAngle': '109.8795',
                    'DropOff': '2.7108',
                    'FlickRate': '0.0000',
                    'Hpr': VBase3(1.397, -83.595, 76.223),
                    'Intensity': '0.8675',
                    'LightType': 'SPOT',
                    'Pos': Point3(412.265, -16.052, 200.312),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.13, 0.58, 0.63, 1.0),
                        'Model': 'models/props/light_tool_bulb'
                    }
                },
                '1186710528.0dchiappe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(104.276, 0.0, 0.0),
                    'Pos': Point3(239.452, -165.185, 4.711),
                    'Scale': VBase3(1.996, 1.996, 1.996),
                    'Visual': {
                        'Model': 'models/props/bone_altar'
                    }
                },
                '1186710656.0dchiappe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(63.969, 1.641, 0.0),
                    'Pos': Point3(239.274, -120.513, 4.398),
                    'Scale': VBase3(2.443, 2.443, 2.443),
                    'Visual': {
                        'Model': 'models/props/bone_altar'
                    }
                },
                '1186710784.0dchiappe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(91.409, 0.0, 0.0),
                    'Pos': Point3(236.705, -173.016, 5.981),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186710784.0dchiappe0': {
                    'Type': 'Enemy_Props',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(242.681, -124.992, 4.79),
                    'Scale': VBase3(1.248, 1.248, 1.248),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186710912.0dchiappe': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(218.683, -182.113, 9.554),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1186710912.0dchiappe0': {
                    'Type': 'Light_Fixtures',
                    'Hpr': VBase3(76.651, 0.0, 0.0),
                    'Pos': Point3(229.149, -92.65, 7.539),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1186710912.0dchiappe1': {
                    'Type': 'Light_Fixtures',
                    'Hpr': VBase3(168.421, 0.0, 0.0),
                    'Pos': Point3(242.273, -126.922, 4.881),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1186710912.0dchiappe2': {
                    'Type': 'Light_Fixtures',
                    'Hpr': VBase3(83.642, 0.0, 0.0),
                    'Pos': Point3(248.09, -154.691, 3.733),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1186772608.0dchiappe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, 333.435),
                    'Pos': Point3(55.0, 55.178, 48.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rock_group_5_sphere'
                    }
                },
                '1186772608.0dchiappe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '29.5455',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-68.187, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(216.529, -155.418, 11.579),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186772608.0dchiappe1': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '30.3030',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-111.022, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(215.006, -128.243, 10.983),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186773120.0dchiappe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-7.132, 83.374, 30.711),
                    'Scale': VBase3(0.096, 0.096, 0.096),
                    'Visual': {
                        'Model': 'models/props/rock_caveB_sphere'
                    }
                },
                '1186773120.0dchiappe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-16.953, 65.127, 31.149),
                    'Scale': VBase3(0.141, 0.141, 0.141),
                    'Visual': {
                        'Model': 'models/props/rock_caveA_floor'
                    }
                },
                '1186773120.0dchiappe2': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-6.548, 46.657, 30.688),
                    'Scale': VBase3(0.35, 0.35, 0.35),
                    'Visual': {
                        'Model': 'models/props/rock_1_floor'
                    }
                },
                '1186773120.0dchiappe3': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(9.02, 43.576, 29.995),
                    'Scale': VBase3(0.365, 0.365, 0.365),
                    'Visual': {
                        'Model': 'models/props/rock_group_2_sphere'
                    }
                },
                '1186773248.0dchiappe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(13.233, 76.724, 29.805),
                    'Scale': VBase3(0.558, 0.558, 0.558),
                    'Visual': {
                        'Model': 'models/props/rock_group_3_sphere'
                    }
                },
                '1186773248.0dchiappe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(78.813, 0.0, 0.0),
                    'Pos': Point3(23.389, 62.215, 29.354),
                    'Scale': VBase3(3.742, 3.742, 3.742),
                    'Visual': {
                        'Model': 'models/props/rock_4_sphere'
                    }
                },
                '1186773248.0dchiappe3': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-94.034, 0.0, 0.0),
                    'Pos': Point3(21.722, 85.523, 29.426),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rock_group_2_sphere'
                    }
                },
                '1186773376.0dchiappe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(33.982, 36.613, 28.885),
                    'Scale': VBase3(0.714, 0.714, 0.714),
                    'Visual': {
                        'Model': 'models/props/rock_group_4_sphere'
                    }
                },
                '1186773504.0dchiappe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-169.93, 0.0, 0.0),
                    'Pos': Point3(-2.297, 67.161, 30.501),
                    'Scale': VBase3(0.422, 0.422, 0.422),
                    'Visual': {
                        'Model': 'models/props/rock_group_5_sphere'
                    }
                },
                '1186773504.0dchiappe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-99.428, 1.815, 0.0),
                    'Pos': Point3(7.607, 64.685, 30.056),
                    'Scale': VBase3(0.56, 0.56, 0.56),
                    'Visual': {
                        'Model': 'models/props/rock_group_3_sphere'
                    }
                },
                '1186773632.0dchiappe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '25.6024',
                    'AnimSet': 'default',
                    'Hpr': VBase3(102.246, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(2.658, 64.391, 30.2),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186773760.0dchiappe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-75.003, -68.092, 33.745),
                    'Scale': VBase3(2.992, 2.992, 2.992),
                    'Visual': {
                        'Color': (0.4000000059604645, 0.4000000059604645,
                                  0.4000000059604645, 1.0),
                        'Model':
                        'models/props/rock_group_3_sphere'
                    }
                },
                '1186773888.0dchiappe': {
                    'Type': 'Light - Dynamic',
                    'Attenuation': '0.005',
                    'ConeAngle': '63.0723',
                    'DropOff': '21.1446',
                    'FlickRate': '0.5000',
                    'Hpr': VBase3(160.111, -66.135, 155.023),
                    'Intensity': '0.8916',
                    'LightType': 'SPOT',
                    'Pos': Point3(-402.77, 160.505, 184.123),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.39, 0.54, 0.3, 1.0),
                        'Model': 'models/props/light_tool_bulb'
                    }
                },
                '1186774400.0dchiappe': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-148.969, 10.764, 55.521),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1186774400.0dchiappe0': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-154.249, 27.944, 55.607),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1186774400.0dchiappe1': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-134.633, -37.883, 54.371),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1186774528.0dchiappe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.8788',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(294.6, 88.108, 0.051),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Bat',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186774656.0dchiappe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '10',
                    'Pause Duration': '5',
                    'Pos': Point3(297.243, 141.236, 2.175),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186774656.0dchiappe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '9',
                    'Pause Duration': '5',
                    'Pos': Point3(347.458, 150.88, 2.175),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186774656.0dchiappe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '21',
                    'Pause Duration': '5',
                    'Pos': Point3(383.064, 104.951, -0.903),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186775552.0dchiappe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(337.808, 66.194, -1.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186775680.0dchiappe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-26.342, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(422.612, 14.172, -1.064),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Vampire Bat',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186775680.0dchiappe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(391.651, 17.326, -1.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186775680.0dchiappe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '12',
                    'Pause Duration': '5',
                    'Pos': Point3(356.358, 46.652, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186775680.0dchiappe2': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '11',
                    'Pause Duration': '5',
                    'Pos': Point3(374.564, 71.058, -1.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186775680.0dchiappe3': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '11',
                    'Pause Duration': '5',
                    'Pos': Point3(414.774, 69.509, -1.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186776192.0dchiappe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-34.787, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(289.976, -102.96, 2.175),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Bat',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186776192.0dchiappe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(299.025, -67.605, 2.175),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186776192.0dchiappe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '2',
                    'Pause Duration': '5',
                    'Pos': Point3(346.936, -62.288, -1.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186776192.0dchiappe2': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '5',
                    'Pause Duration': '5',
                    'Pos': Point3(344.111, -103.143, -1.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186776192.0dchiappe3': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '5',
                    'Pause Duration': '5',
                    'Pos': Point3(328.364, -115.715, -1.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186776448.0dchiappe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(126.63, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(376.642, 6.438, -1.064),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Bat',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186776448.0dchiappe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(343.609, -14.216, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186776448.0dchiappe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(376.549, -36.377, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186776448.0dchiappe2': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(401.339, -4.471, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186776704.0dchiappe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '7',
                    'Pause Duration': '5',
                    'Pos': Point3(454.435, -86.606, 2.175),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186776704.0dchiappe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '11',
                    'Pause Duration': '5',
                    'Pos': Point3(403.299, -120.2, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186776832.0dchiappe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(365.448, -159.466, 2.175),
                    'Scale': VBase3(1.438, 1.438, 1.438),
                    'Visual': {
                        'Model': 'models/props/rock_group_3_sphere'
                    }
                },
                '1186776960.0dchiappe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_handdig',
                    'Hpr': VBase3(78.559, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-149.775, -34.843, 56.323),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Early Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186776960.0dchiappe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(140.47, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-153.242, 17.713, 55.589),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186777088.0dchiappe0': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-81.477, 0.0, 0.0),
                    'Pos': Point3(-155.623, 0.679, 56.458),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1186777088.0dchiappe1': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(77.874, 0.0, 0.0),
                    'Pos': Point3(-156.667, 11.319, 56.135),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1186777216.0dchiappe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-74.291, 0.0, 0.0),
                    'Pos': Point3(-151.7, -12.149, 56.436),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_altar'
                    }
                },
                '1186777216.0dchiappe0': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-99.431, 0.0, 0.0),
                    'Pos': Point3(-143.916, -33.183, 55.993),
                    'Scale': VBase3(1.287, 1.287, 1.287),
                    'Visual': {
                        'Model': 'models/props/bone_altar'
                    }
                },
                '1186777216.0dchiappe1': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-4.195, 73.676, 32.051),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/candle'
                    }
                },
                '1186777344.0dchiappe': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-7.296, 62.736, 30.72),
                    'Scale': VBase3(1.369, 1.369, 1.369),
                    'Visual': {
                        'Model': 'models/props/candle'
                    }
                },
                '1186777344.0dchiappe0': {
                    'Type': 'Light_Fixtures',
                    'Hpr': VBase3(-56.066, 0.0, 0.0),
                    'Pos': Point3(0.973, 54.742, 30.362),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/candle'
                    }
                },
                '1186777344.0dchiappe1': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(14.187, 60.779, 29.764),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/candle'
                    }
                },
                '1186777344.0dchiappe2': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(12.152, 72.876, 29.853),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/candle'
                    }
                },
                '1186777344.0dchiappe3': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(50.263, 50.664, 45.207),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/candle'
                    }
                },
                '1186777344.0dchiappe4': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(50.438, 51.198, 45.531),
                    'Scale': VBase3(1.391, 1.391, 1.391),
                    'Visual': {
                        'Model': 'models/props/candle'
                    }
                },
                '1186777344.0dchiappe5': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-141.013, 3.983, 55.14),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/candle'
                    }
                },
                '1186777344.0dchiappe6': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-140.087, -6.036, 55.475),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/candle'
                    }
                },
                '1186777344.0dchiappe7': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-133.546, -17.925, 53.965),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/candle'
                    }
                },
                '1186777472.0dchiappe': {
                    'Type': 'Light_Fixtures',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-120.561, -31.547, 50.217),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/candle'
                    }
                },
                '1186777472.0dchiappe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-260.41, 120.94, 65.999),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Bat',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186777600.0dchiappe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-264.173, 178.677, 66.689),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Bat',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186777600.0dchiappe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-337.272, 87.457, 65.29),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Bat',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186777600.0dchiappe1': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-414.38, 146.844, 78.064),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Bat',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186777600.0dchiappe2': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '7',
                    'Pause Duration': '5',
                    'Pos': Point3(-452.116, 152.338, 78.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186777600.0dchiappe3': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '2',
                    'Pause Duration': '5',
                    'Pos': Point3(-444.58, 109.904, 78.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186777728.0dchiappe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '2',
                    'Pause Duration': '5',
                    'Pos': Point3(-387.548, 128.077, 76.723),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186777728.0dchiappe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '11',
                    'Pause Duration': '5',
                    'Pos': Point3(-397.695, 90.793, 78.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186777728.0dchiappe2': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-289.14, 91.456, 65.526),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186777728.0dchiappe3': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-299.61, 133.143, 65.995),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186777856.0dchiappe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-283.196, 143.493, 66.185),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186777984.0dchiappe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-304.303, -76.528, 55.796),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1187044224.0dchiappe': {
                    'Type': 'Animated Avatar',
                    'Category': 'cast',
                    'Animation Track': 'jr_look_idle',
                    'Effect Type': 'Ghost',
                    'Hpr': VBase3(100.0, 0.0, 0.0),
                    'Pos': Point3(57.0, 65.0, 48.5),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(5.0, 5.0, 5.0),
                    'StartFrame': '0',
                    'SubCategory': 'models/char/jr_2000',
                    'TrailFX': 'None'
                },
                '1189820800.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-38.392, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-359.098, -44.118, 55.796),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Vampire Bat',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1191458849.03piwanow': {
                    'Type': 'Effect Node',
                    'EffectName': 'fireplace_effect',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(2.5, 64.23, 30.0),
                    'Scale': VBase3(0.65, 0.65, 0.65),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1191459065.14piwanow': {
                    'Type': 'Effect Node',
                    'EffectName': 'lightsmoke_effect',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(2.5, 64.0, 31.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1191606122.25piwanow': {
                    'Type': 'Animated Avatar',
                    'Category': 'cast',
                    'Animation Track': 'jr_look_idle_2',
                    'Effect Type': 'Ghost',
                    'Hpr': VBase3(100.0, 0.0, 0.0),
                    'Pos': Point3(57.0, 65.0, 48.5),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(5.0, 5.0, 5.0),
                    'StartFrame': '0',
                    'SubCategory': 'models/char/jr_2000',
                    'TrailFX': 'None'
                },
                '1191617419.92piwanow': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(55.0, 90.0, 46.0),
                    'Scale': VBase3(1.6, 1.6, 1.6),
                    'Visual': {
                        'Model': 'models/props/rock_group_4_sphere'
                    }
                },
                '1191617843.77piwanow': {
                    'Type': 'Effect Node',
                    'EffectName': 'mysticsmoke_effect',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(57.0, 65.0, 48.0),
                    'Scale': VBase3(1.5, 1.5, 1.5),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1191617912.0piwanow': {
                    'Type': 'Effect Node',
                    'EffectName': 'mysticfire_effect',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(58.0, 65.5, 48.0),
                    'Scale': VBase3(1.3, 1.3, 1.3),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1191617993.28piwanow': {
                    'Type': 'Effect Node',
                    'EffectName': 'blacksmoke_effect',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(59.0, 66.0, 48.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193160704.0dxschafe0': {
                    'Type': 'Light_Fixtures',
                    'Hpr': VBase3(105.422, 0.0, 0.0),
                    'Pos': Point3(-343.593, 57.178, 64.077),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1193160704.0dxschafe1': {
                    'Type': 'Light_Fixtures',
                    'Hpr': VBase3(60.288, 0.0, 0.0),
                    'Pos': Point3(-349.759, 13.843, 56.669),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1193160832.0dxschafe': {
                    'Type': 'Light_Fixtures',
                    'Hpr': VBase3(60.288, 0.0, 0.0),
                    'Pos': Point3(-340.101, 39.116, 58.832),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/torch'
                    }
                },
                '1193161344.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(135.025, 0.0, 0.0),
                    'Pos': Point3(-327.026, -2.036, 53.129),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rock_caveC_sphere'
                    }
                },
                '1193161472.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-14.954, 0.0, 0.0),
                    'Pos': Point3(-387.112, 52.923, 60.099),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rock_caveC_sphere'
                    }
                },
                '1195173919.03akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(107.106, 0.0, 0.0),
                    'Pos': Point3(-132.446, 112.622, 36.021),
                    'Scale': VBase3(1.0, 1.0, 1.094),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1202318017.91akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-41.697, 0.0, 0.0),
                    'Pos': Point3(-72.153, 190.004, 33.044),
                    'Scale': VBase3(1.724, 1.6, 1.566),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1205364942.37kmuller': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(288.938, -242.423, 1.269),
                    'Scale': VBase3(0.816, 0.816, 0.816),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/rock_caveB_sphere'
                    }
                },
                '1205364972.93kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(154.899, 0.0, 0.0),
                    'Pos': Point3(292.952, -236.139, 2.03),
                    'Scale': VBase3(1.84, 1.84, 4.686),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1213146168.22akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-144.036, 0.0, 0.0),
                    'Pos': Point3(502.115, -133.302, 2.175),
                    'Scale': VBase3(0.339, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1219428571.98mtucker': {
                    'Type': 'Skeleton',
                    'Aggro Radius': '9.9398',
                    'AnimSet': 'idleB',
                    'AvId': 4,
                    'AvTrack': 0,
                    'Boss': True,
                    'Hpr': VBase3(-63.189, 0.0, 0.0),
                    'Patrol Radius': '3.7470',
                    'Pos': Point3(-14.519, 54.042, 31.042),
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
                'Model': 'models/caves/cave_b_zero'
            }
        }
    },
    'Node Links':
    [['1186774656.0dchiappe', '1186774528.0dchiappe', 'Bi-directional'],
     ['1186774656.0dchiappe', '1186774656.0dchiappe0', 'Bi-directional'],
     ['1186774656.0dchiappe1', '1186774656.0dchiappe0', 'Bi-directional'],
     ['1186774656.0dchiappe1', '1186775552.0dchiappe', 'Bi-directional'],
     ['1186774528.0dchiappe', '1186775552.0dchiappe', 'Bi-directional'],
     ['1186775680.0dchiappe0', '1186775680.0dchiappe', 'Bi-directional'],
     ['1186775680.0dchiappe0', '1186775680.0dchiappe1', 'Bi-directional'],
     ['1186775680.0dchiappe1', '1186775680.0dchiappe2', 'Bi-directional'],
     ['1186775680.0dchiappe3', '1186775680.0dchiappe2', 'Bi-directional'],
     ['1186775680.0dchiappe3', '1186775680.0dchiappe', 'Bi-directional'],
     ['1186776192.0dchiappe', '1186776192.0dchiappe0', 'Bi-directional'],
     ['1186776192.0dchiappe1', '1186776192.0dchiappe0', 'Bi-directional'],
     ['1186776192.0dchiappe1', '1186776192.0dchiappe2', 'Bi-directional'],
     ['1186776192.0dchiappe2', '1186776192.0dchiappe3', 'Bi-directional'],
     ['1186776192.0dchiappe', '1186776192.0dchiappe3', 'Bi-directional'],
     ['1186776448.0dchiappe', '1186776448.0dchiappe2', 'Bi-directional'],
     ['1186776448.0dchiappe2', '1186776448.0dchiappe1', 'Bi-directional'],
     ['1186776448.0dchiappe0', '1186776448.0dchiappe1', 'Bi-directional'],
     ['1186776448.0dchiappe', '1186776448.0dchiappe0', 'Bi-directional'],
     ['1186776704.0dchiappe0', '1176158976.0dxschafe', 'Bi-directional'],
     ['1186776704.0dchiappe', '1186776704.0dchiappe0', 'Bi-directional'],
     ['1186776704.0dchiappe', '1176158976.0dxschafe', 'Bi-directional'],
     ['1186777600.0dchiappe1', '1186777600.0dchiappe2', 'Bi-directional'],
     ['1186777600.0dchiappe3', '1186777600.0dchiappe2', 'Bi-directional'],
     ['1186777600.0dchiappe3', '1186777600.0dchiappe1', 'Bi-directional'],
     ['1186777728.0dchiappe0', '1186777600.0dchiappe0', 'Bi-directional'],
     ['1186777728.0dchiappe0', '1186777728.0dchiappe1', 'Bi-directional'],
     ['1186777728.0dchiappe1', '1186777600.0dchiappe0', 'Bi-directional'],
     ['1186777472.0dchiappe0', '1186777728.0dchiappe2', 'Bi-directional'],
     ['1186777728.0dchiappe2', '1186777728.0dchiappe3', 'Bi-directional'],
     ['1186777472.0dchiappe0', '1186777728.0dchiappe3', 'Bi-directional'],
     ['1186777856.0dchiappe0', '1186777600.0dchiappe', 'Bi-directional'],
     ['1165197827.77Shochet', '1186777984.0dchiappe', 'Bi-directional']],
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
        '1165001772.05sdnaik':
        '["Objects"]["1165001772.05sdnaik"]',
        '1165001975.75sdnaik':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1165001975.75sdnaik"]',
        '1165001975.77sdnaik':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1165001975.77sdnaik"]',
        '1165019328.28Shochet':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1165019328.28Shochet"]',
        '1165019476.34Shochet':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1165019476.34Shochet"]',
        '1165019501.84Shochet':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1165019501.84Shochet"]',
        '1165019770.53Shochet':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1165019770.53Shochet"]',
        '1165197827.77Shochet':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1165197827.77Shochet"]',
        '1175127779.71kmuller':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1175127779.71kmuller"]',
        '1175127913.08kmuller':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1175127913.08kmuller"]',
        '1176158080.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176158080.0dxschafe"]',
        '1176158208.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176158208.0dxschafe"]',
        '1176158976.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176158976.0dxschafe"]',
        '1176159104.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159104.0dxschafe"]',
        '1176159104.0dxschafe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159104.0dxschafe0"]',
        '1176159232.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159232.0dxschafe"]',
        '1176159360.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159360.0dxschafe"]',
        '1176159360.0dxschafe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159360.0dxschafe0"]',
        '1176159360.0dxschafe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159360.0dxschafe1"]',
        '1176159360.0dxschafe10':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159360.0dxschafe10"]',
        '1176159360.0dxschafe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159360.0dxschafe2"]',
        '1176159360.0dxschafe3':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159360.0dxschafe3"]',
        '1176159360.0dxschafe4':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159360.0dxschafe4"]',
        '1176159360.0dxschafe5':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159360.0dxschafe5"]',
        '1176159360.0dxschafe6':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159360.0dxschafe6"]',
        '1176159360.0dxschafe7':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159360.0dxschafe7"]',
        '1176159360.0dxschafe8':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159360.0dxschafe8"]',
        '1176159360.0dxschafe9':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159360.0dxschafe9"]',
        '1176159488.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159488.0dxschafe"]',
        '1176159488.0dxschafe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159488.0dxschafe0"]',
        '1176159488.0dxschafe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159488.0dxschafe1"]',
        '1176159488.0dxschafe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1176159488.0dxschafe2"]',
        '1185388672.0dxschafe003':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe003"]',
        '1185388672.0dxschafe004':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe004"]',
        '1185388672.0dxschafe006':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe006"]',
        '1185388672.0dxschafe007':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe007"]',
        '1185388672.0dxschafe008':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe008"]',
        '1185388672.0dxschafe010':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe010"]',
        '1185388672.0dxschafe03':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe03"]',
        '1185388672.0dxschafe04':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe04"]',
        '1185388672.0dxschafe06':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe06"]',
        '1185388672.0dxschafe07':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe07"]',
        '1185388672.0dxschafe08':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe08"]',
        '1185388672.0dxschafe10':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe10"]',
        '1185388672.0dxschafe103':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe103"]',
        '1185388672.0dxschafe105':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe105"]',
        '1185388672.0dxschafe106':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe106"]',
        '1185388672.0dxschafe108':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe108"]',
        '1185388672.0dxschafe109':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe109"]',
        '1185388672.0dxschafe110':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe110"]',
        '1185388672.0dxschafe112':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe112"]',
        '1185388672.0dxschafe113':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe113"]',
        '1185388672.0dxschafe303':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe303"]',
        '1185388672.0dxschafe304':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe304"]',
        '1185388672.0dxschafe306':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe306"]',
        '1185388672.0dxschafe307':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe307"]',
        '1185388672.0dxschafe308':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe308"]',
        '1185388672.0dxschafe403':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe403"]',
        '1185388672.0dxschafe404':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe404"]',
        '1185388672.0dxschafe406':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe406"]',
        '1185388672.0dxschafe407':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe407"]',
        '1185388672.0dxschafe408':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe408"]',
        '1185388672.0dxschafe503':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe503"]',
        '1185388672.0dxschafe504':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe504"]',
        '1185388672.0dxschafe505':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe505"]',
        '1185388672.0dxschafe506':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe506"]',
        '1185388672.0dxschafe508':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe508"]',
        '1185388672.0dxschafe509':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe509"]',
        '1185388672.0dxschafe510':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe510"]',
        '1185388672.0dxschafe512':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe512"]',
        '1185388672.0dxschafe513':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388672.0dxschafe513"]',
        '1185388800.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388800.0dxschafe"]',
        '1185388800.0dxschafe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388800.0dxschafe0"]',
        '1185388800.0dxschafe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388800.0dxschafe1"]',
        '1185388800.0dxschafe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185388800.0dxschafe2"]',
        '1185925504.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185925504.0dxschafe"]',
        '1185925504.0dxschafe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185925504.0dxschafe0"]',
        '1185925504.0dxschafe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1185925504.0dxschafe1"]',
        '1186083737.45kmuller':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186083737.45kmuller"]',
        '1186172544.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186172544.0dxschafe"]',
        '1186172544.0dxschafe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186172544.0dxschafe0"]',
        '1186172672.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186172672.0dxschafe"]',
        '1186173056.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186173056.0dxschafe"]',
        '1186173056.0dxschafe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186173056.0dxschafe1"]',
        '1186173056.0dxschafe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186173056.0dxschafe2"]',
        '1186173440.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186173440.0dxschafe"]',
        '1186173824.0dxschafe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186173824.0dxschafe1"]',
        '1186174208.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186174208.0dxschafe"]',
        '1186174464.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186174464.0dxschafe"]',
        '1186174464.0dxschafe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186174464.0dxschafe0"]',
        '1186174464.0dxschafe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186174464.0dxschafe2"]',
        '1186174592.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186174592.0dxschafe"]',
        '1186174720.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186174720.0dxschafe"]',
        '1186174720.0dxschafe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186174720.0dxschafe0"]',
        '1186174976.0dxschafe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186174976.0dxschafe0"]',
        '1186175104.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186175104.0dxschafe"]',
        '1186176640.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe"]',
        '1186176640.0dxschafe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe0"]',
        '1186176640.0dxschafe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe1"]',
        '1186176640.0dxschafe10':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe10"]',
        '1186176640.0dxschafe11':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe11"]',
        '1186176640.0dxschafe12':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe12"]',
        '1186176640.0dxschafe13':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe13"]',
        '1186176640.0dxschafe14':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe14"]',
        '1186176640.0dxschafe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe2"]',
        '1186176640.0dxschafe22':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe22"]',
        '1186176640.0dxschafe23':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe23"]',
        '1186176640.0dxschafe24':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe24"]',
        '1186176640.0dxschafe25':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe25"]',
        '1186176640.0dxschafe3':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe3"]',
        '1186176640.0dxschafe30':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe30"]',
        '1186176640.0dxschafe31':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe31"]',
        '1186176640.0dxschafe32':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe32"]',
        '1186176640.0dxschafe33':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe33"]',
        '1186176640.0dxschafe38':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe38"]',
        '1186176640.0dxschafe39':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe39"]',
        '1186176640.0dxschafe4':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe4"]',
        '1186176640.0dxschafe40':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe40"]',
        '1186176640.0dxschafe41':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe41"]',
        '1186176640.0dxschafe42':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe42"]',
        '1186176640.0dxschafe43':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe43"]',
        '1186176640.0dxschafe44':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe44"]',
        '1186176640.0dxschafe45':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe45"]',
        '1186176640.0dxschafe46':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe46"]',
        '1186176640.0dxschafe8':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe8"]',
        '1186176640.0dxschafe9':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176640.0dxschafe9"]',
        '1186176768.0dxschafe16':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176768.0dxschafe16"]',
        '1186176768.0dxschafe17':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176768.0dxschafe17"]',
        '1186176768.0dxschafe18':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176768.0dxschafe18"]',
        '1186176768.0dxschafe19':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176768.0dxschafe19"]',
        '1186176768.0dxschafe20':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176768.0dxschafe20"]',
        '1186176768.0dxschafe21':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176768.0dxschafe21"]',
        '1186176768.0dxschafe22':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176768.0dxschafe22"]',
        '1186176768.0dxschafe23':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176768.0dxschafe23"]',
        '1186176768.0dxschafe24':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176768.0dxschafe24"]',
        '1186176768.0dxschafe25':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176768.0dxschafe25"]',
        '1186176768.0dxschafe26':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176768.0dxschafe26"]',
        '1186176768.0dxschafe27':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176768.0dxschafe27"]',
        '1186176768.0dxschafe3':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176768.0dxschafe3"]',
        '1186176768.0dxschafe4':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176768.0dxschafe4"]',
        '1186176768.0dxschafe5':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176768.0dxschafe5"]',
        '1186176768.0dxschafe6':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176768.0dxschafe6"]',
        '1186176768.0dxschafe7':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186176768.0dxschafe7"]',
        '1186177536.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177536.0dxschafe"]',
        '1186177536.0dxschafe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177536.0dxschafe0"]',
        '1186177664.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177664.0dxschafe"]',
        '1186177664.0dxschafe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177664.0dxschafe0"]',
        '1186177664.0dxschafe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177664.0dxschafe1"]',
        '1186177664.0dxschafe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177664.0dxschafe2"]',
        '1186177664.0dxschafe21':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177664.0dxschafe21"]',
        '1186177664.0dxschafe22':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177664.0dxschafe22"]',
        '1186177664.0dxschafe23':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177664.0dxschafe23"]',
        '1186177664.0dxschafe24':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177664.0dxschafe24"]',
        '1186177664.0dxschafe25':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177664.0dxschafe25"]',
        '1186177664.0dxschafe3':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177664.0dxschafe3"]',
        '1186177664.0dxschafe4':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177664.0dxschafe4"]',
        '1186177664.0dxschafe5':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177664.0dxschafe5"]',
        '1186177664.0dxschafe6':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177664.0dxschafe6"]',
        '1186177664.0dxschafe7':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177664.0dxschafe7"]',
        '1186177792.0dxschafe10':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177792.0dxschafe10"]',
        '1186177792.0dxschafe5':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177792.0dxschafe5"]',
        '1186177792.0dxschafe6':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177792.0dxschafe6"]',
        '1186177792.0dxschafe7':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177792.0dxschafe7"]',
        '1186177792.0dxschafe8':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177792.0dxschafe8"]',
        '1186177792.0dxschafe9':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186177792.0dxschafe9"]',
        '1186435200.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186435200.0dchiappe"]',
        '1186435200.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186435200.0dchiappe0"]',
        '1186508544.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186508544.0dchiappe"]',
        '1186508672.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186508672.0dchiappe1"]',
        '1186508800.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186508800.0dchiappe"]',
        '1186615808.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186615808.0dchiappe"]',
        '1186617088.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186617088.0dchiappe0"]',
        '1186617216.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186617216.0dchiappe"]',
        '1186617600.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186617600.0dchiappe"]',
        '1186619008.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186619008.0dchiappe"]',
        '1186695680.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186695680.0dchiappe"]',
        '1186695936.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186695936.0dchiappe"]',
        '1186705968.08dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186705968.08dchiappe"]',
        '1186706066.42dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186706066.42dchiappe"]',
        '1186706108.61dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186706108.61dchiappe"]',
        '1186707328.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186707328.0dchiappe"]',
        '1186707328.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186707328.0dchiappe0"]',
        '1186707328.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186707328.0dchiappe1"]',
        '1186707328.0dchiappe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186707328.0dchiappe2"]',
        '1186707456.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186707456.0dchiappe"]',
        '1186707456.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186707456.0dchiappe0"]',
        '1186707456.0dchiappe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186707456.0dchiappe2"]',
        '1186707968.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186707968.0dchiappe"]',
        '1186708736.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186708736.0dchiappe"]',
        '1186708736.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186708736.0dchiappe0"]',
        '1186708736.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186708736.0dchiappe1"]',
        '1186708736.0dchiappe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186708736.0dchiappe2"]',
        '1186708736.0dchiappe4':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186708736.0dchiappe4"]',
        '1186709120.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186709120.0dchiappe"]',
        '1186709120.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186709120.0dchiappe0"]',
        '1186709376.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186709376.0dchiappe"]',
        '1186709632.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186709632.0dchiappe"]',
        '1186710400.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186710400.0dchiappe"]',
        '1186710528.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186710528.0dchiappe"]',
        '1186710656.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186710656.0dchiappe"]',
        '1186710784.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186710784.0dchiappe"]',
        '1186710784.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186710784.0dchiappe0"]',
        '1186710912.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186710912.0dchiappe"]',
        '1186710912.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186710912.0dchiappe0"]',
        '1186710912.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186710912.0dchiappe1"]',
        '1186710912.0dchiappe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186710912.0dchiappe2"]',
        '1186772608.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186772608.0dchiappe"]',
        '1186772608.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186772608.0dchiappe0"]',
        '1186772608.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186772608.0dchiappe1"]',
        '1186773120.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186773120.0dchiappe"]',
        '1186773120.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186773120.0dchiappe1"]',
        '1186773120.0dchiappe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186773120.0dchiappe2"]',
        '1186773120.0dchiappe3':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186773120.0dchiappe3"]',
        '1186773248.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186773248.0dchiappe"]',
        '1186773248.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186773248.0dchiappe1"]',
        '1186773248.0dchiappe3':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186773248.0dchiappe3"]',
        '1186773376.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186773376.0dchiappe"]',
        '1186773504.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186173056.0dxschafe2"]["Objects"]["1186773504.0dchiappe"]',
        '1186773504.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186773504.0dchiappe0"]',
        '1186773504.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186773504.0dchiappe1"]',
        '1186773632.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186773632.0dchiappe"]',
        '1186773760.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186773760.0dchiappe"]',
        '1186773888.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186773888.0dchiappe"]',
        '1186774400.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186774400.0dchiappe"]',
        '1186774400.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186774400.0dchiappe0"]',
        '1186774400.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186774400.0dchiappe1"]',
        '1186774528.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186774528.0dchiappe"]',
        '1186774656.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186774656.0dchiappe"]',
        '1186774656.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186774656.0dchiappe0"]',
        '1186774656.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186774656.0dchiappe1"]',
        '1186775552.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186775552.0dchiappe"]',
        '1186775680.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186775680.0dchiappe"]',
        '1186775680.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186775680.0dchiappe0"]',
        '1186775680.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186775680.0dchiappe1"]',
        '1186775680.0dchiappe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186775680.0dchiappe2"]',
        '1186775680.0dchiappe3':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186775680.0dchiappe3"]',
        '1186776192.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186776192.0dchiappe"]',
        '1186776192.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186776192.0dchiappe0"]',
        '1186776192.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186776192.0dchiappe1"]',
        '1186776192.0dchiappe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186776192.0dchiappe2"]',
        '1186776192.0dchiappe3':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186776192.0dchiappe3"]',
        '1186776448.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186776448.0dchiappe"]',
        '1186776448.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186776448.0dchiappe0"]',
        '1186776448.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186776448.0dchiappe1"]',
        '1186776448.0dchiappe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186776448.0dchiappe2"]',
        '1186776704.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186776704.0dchiappe"]',
        '1186776704.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186776704.0dchiappe0"]',
        '1186776832.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186776832.0dchiappe"]',
        '1186776960.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186776960.0dchiappe"]',
        '1186776960.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186776960.0dchiappe0"]',
        '1186777088.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777088.0dchiappe0"]',
        '1186777088.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777088.0dchiappe1"]',
        '1186777216.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777216.0dchiappe"]',
        '1186777216.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777216.0dchiappe0"]',
        '1186777216.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777216.0dchiappe1"]',
        '1186777344.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777344.0dchiappe"]',
        '1186777344.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777344.0dchiappe0"]',
        '1186777344.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777344.0dchiappe1"]',
        '1186777344.0dchiappe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777344.0dchiappe2"]',
        '1186777344.0dchiappe3':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777344.0dchiappe3"]',
        '1186777344.0dchiappe4':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777344.0dchiappe4"]',
        '1186777344.0dchiappe5':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777344.0dchiappe5"]',
        '1186777344.0dchiappe6':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777344.0dchiappe6"]',
        '1186777344.0dchiappe7':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777344.0dchiappe7"]',
        '1186777472.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777472.0dchiappe"]',
        '1186777472.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777472.0dchiappe0"]',
        '1186777600.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777600.0dchiappe"]',
        '1186777600.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777600.0dchiappe0"]',
        '1186777600.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777600.0dchiappe1"]',
        '1186777600.0dchiappe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777600.0dchiappe2"]',
        '1186777600.0dchiappe3':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777600.0dchiappe3"]',
        '1186777728.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777728.0dchiappe0"]',
        '1186777728.0dchiappe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777728.0dchiappe1"]',
        '1186777728.0dchiappe2':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777728.0dchiappe2"]',
        '1186777728.0dchiappe3':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777728.0dchiappe3"]',
        '1186777856.0dchiappe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777856.0dchiappe0"]',
        '1186777984.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1186777984.0dchiappe"]',
        '1187044224.0dchiappe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1187044224.0dchiappe"]',
        '1189820800.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1189820800.0dxschafe"]',
        '1191458849.03piwanow':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1191458849.03piwanow"]',
        '1191459065.14piwanow':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1191459065.14piwanow"]',
        '1191606122.25piwanow':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1191606122.25piwanow"]',
        '1191617419.92piwanow':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1191617419.92piwanow"]',
        '1191617843.77piwanow':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1191617843.77piwanow"]',
        '1191617912.0piwanow':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1191617912.0piwanow"]',
        '1191617993.28piwanow':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1191617993.28piwanow"]',
        '1193160704.0dxschafe0':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1193160704.0dxschafe0"]',
        '1193160704.0dxschafe1':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1193160704.0dxschafe1"]',
        '1193160832.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1193160832.0dxschafe"]',
        '1193161344.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1193161344.0dxschafe"]',
        '1193161472.0dxschafe':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1193161472.0dxschafe"]',
        '1195173919.03akelts':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1195173919.03akelts"]',
        '1202318017.91akelts':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1202318017.91akelts"]',
        '1205364942.37kmuller':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1205364942.37kmuller"]',
        '1205364972.93kmuller':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1205364972.93kmuller"]',
        '1213146168.22akelts':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1213146168.22akelts"]',
        '1219428571.98mtucker':
        '["Objects"]["1165001772.05sdnaik"]["Objects"]["1219428571.98mtucker"]'
    }
}
extraInfo = {
    'camPos': Point3(-83.3313, -16.9737, 158.952),
    'camHpr': VBase3(-48.6579, -44.5115, 0),
    'focalLength': 1.39999997616,
    'skyState': 2,
    'fog': 0
}
