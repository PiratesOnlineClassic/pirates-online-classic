# Embedded file name: pirates.leveleditor.worldData.port_royal_area_cave_a_1
from pandac.PandaModules import Point3, VBase3, Vec4
objectStruct = {
    'AmbientColors': {
        -1: Vec4(0.447059, 0.447059, 0.415686, 1),
        0: Vec4(0.496039, 0.568627, 0.67451, 1),
        2: Vec4(0.74902, 0.737255, 0.737255, 1),
        4: Vec4(0.721569, 0.611765, 0.619608, 1),
        6: Vec4(0.437059, 0.446471, 0.556667, 1),
        8: Vec4(0.389216, 0.426275, 0.569608, 1)
    },
    'DirectionalColors': {
        -1: Vec4(0.717647, 0.721569, 0.72549, 1),
        0: Vec4(0.960784, 0.913725, 0.894118, 1),
        2: Vec4(0.764706, 0.764706, 0.764706, 1),
        4: Vec4(0.439216, 0.176471, 0, 1),
        6: Vec4(0.513726, 0.482353, 0.643137, 1),
        8: Vec4(0.447059, 0.439216, 0.541176, 1)
    },
    'FogColors': {
        -1: Vec4(0.870588, 0.87451, 0.823529, 1),
        0: Vec4(0.27451, 0.192157, 0.211765, 0),
        2: Vec4(0.0313726, 0.054902, 0.0784314, 1),
        4: Vec4(0.231373, 0.203922, 0.184314, 0),
        6: Vec4(0.156863, 0.219608, 0.329412, 0),
        8: Vec4(0.129412, 0.137255, 0.207843, 0)
    },
    'FogRanges': {
        0: 0.0002,
        2: 0.0006000000284984708,
        4: 0.0004,
        6: 0.0004,
        8: 0.0002
    },
    'Interact Links':
    [['1165019105.05Shochet', '1164999287.17Shochet', 'Bi-directional'],
     ['1165197639.41Shochet', '1165019166.08Shochet', 'Bi-directional'],
     ['1164999249.69Shochet', '1175898752.0dxschafe0', 'Bi-directional'],
     ['1165197708.75Shochet', '1165019132.53Shochet', 'Bi-directional'],
     ['1190851456.0dxschafe', '1190851200.0dxschafe', 'Bi-directional']],
    'Objects': {
        '1164952144.06sdnaik': {
            'Type': 'Island Game Area',
            'Name': 'port_royal_area_cave_a_1',
            'File': '',
            'Instanced': True,
            'Objects': {
                '1164953534.72sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_1',
                    'Hpr': VBase3(77.758, 0.0, 0.0),
                    'Pos': Point3(519.133, -416.793, 52.235),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1164953534.72sdnaik0': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_2',
                    'Hpr': VBase3(-90.0, 0.0, 0.0),
                    'Pos': Point3(513.096, 103.973, 88.586),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1164953534.73sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_3',
                    'Hpr': VBase3(1.188, -1.45, -0.338),
                    'Pos': Point3(105.468, -363.345, 0.358),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1164999249.69Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-85.329, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '5.3333',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(154.859, -86.828, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164999287.17Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'bar_talk02',
                    'Hpr': VBase3(94.418, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(286.839, -185.413, 4.222),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Navy',
                    'Start State': 'Idle',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164999438.31Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'bar_talk01',
                    'Hpr': VBase3(-89.947, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '5.8333',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(281.026, -186.473, 4.222),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Navy',
                    'Start State': 'Idle',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164999523.0Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-12.518, 0.0, 0.0),
                    'Level': '8',
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(391.392, -212.677, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'EITC - Thug',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164999574.83Shochet': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-38.958, 0.0, 0.0),
                    'Pos': Point3(283.982, -182.296, 4.223),
                    'Scale': VBase3(0.654, 0.654, 0.654),
                    'Visual': {
                        'Color': (0.67, 0.61, 0.5019607843137255, 1.0),
                        'Model': 'models/props/barrel_group_2'
                    }
                },
                '1164999709.16Shochet': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-24.461, 0.0, 0.0),
                    'Pos': Point3(298.718, -240.245, 4.223),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/prop_group03'
                    }
                },
                '1164999816.83Shochet': {
                    'Type': 'Rope',
                    'DisableCollision': False,
                    'Hpr': VBase3(46.197, 0.0, 0.0),
                    'Pos': Point3(272.674, -186.729, 4.242),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/rope_pile'
                    }
                },
                '1165019105.05Shochet': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(291.257, -228.587, 4.223),
                    'Priority': '1',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SpawnDelay': '600',
                    'Spawnables': 'Buried Treasure',
                    'Visual': {
                        'Color': (0.8, 0.2, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    },
                    'startingDepth': '15'
                },
                '1165019132.53Shochet': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(132.418, -187.845, 2.566),
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
                '1165019166.08Shochet': {
                    'Type': 'Object Spawn Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(425.745, -138.81, 2.566),
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
                '1165197613.83Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(53.272, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(565.237, -276.309, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Bat',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165197639.41Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(139.069, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(369.88, -164.715, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Bat',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165197665.86Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-91.705, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(180.345, -89.168, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Bat',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165197708.75Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(166.662, -258.654, 0.154),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Bat',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1169616862.13sdnaik': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(35.07, 0.0, 0.0),
                    'Pos': Point3(105.177, -357.658, -4.364),
                    'Scale': VBase3(0.818, 0.818, 0.818),
                    'Visual': {
                        'Color': (0.16, 0.2, 0.19, 1.0),
                        'Model': 'models/props/mound_cave_med'
                    }
                },
                '1169617104.89sdnaik': {
                    'Type': 'Pier',
                    'Hpr': VBase3(-131.294, -0.158, -0.083),
                    'Objects': {},
                    'Pos': Point3(197.195, -148.231, -1.939),
                    'Scale': VBase3(0.683, 0.683, 0.683),
                    'Visual': {
                        'Color': (0.7200000286102295, 0.699999988079071,
                                  0.5899999737739563, 1.0),
                        'Model':
                        'models/islands/pier_walkway'
                    }
                },
                '1169617420.52sdnaik': {
                    'Type': 'Pier',
                    'Hpr': VBase3(3.973, -0.041, 0.057),
                    'Objects': {
                        '1175900928.0dxschafe6': {
                            'Type': 'Player Spawn Node',
                            'Hpr': VBase3(91.456, -0.058, -0.04),
                            'Index': -1,
                            'Pos': Point3(-84.732, 7.167, 7.683),
                            'Scale': VBase3(2.87, 2.87, 2.87),
                            'Spawnables': 'All',
                            'Visual': {
                                'Color': (0.5, 0.5, 0.5, 1),
                                'Model': 'models/misc/smiley'
                            }
                        }
                    },
                    'Pos': Point3(543.334, -276.544, -1.818),
                    'Scale': VBase3(0.629, 0.629, 0.629),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/islands/pier_walkway'
                    }
                },
                '1169617816.94sdnaik': {
                    'Type': 'Pier',
                    'Hpr': VBase3(95.087, 0.669, -0.623),
                    'Objects': {
                        '1175900928.0dxschafe': {
                            'Type': 'Player Spawn Node',
                            'Hpr': VBase3(-128.896, 0.0, 0.0),
                            'Index': -1,
                            'Pos': Point3(-37.801, 20.558, 8.513),
                            'Scale': VBase3(1.805, 1.805, 1.805),
                            'Spawnables': 'All',
                            'Visual': {
                                'Color': (0.5, 0.5, 0.5, 1),
                                'Model': 'models/misc/smiley'
                            }
                        }
                    },
                    'Pos': Point3(382.439, -229.931, -1.673),
                    'Scale': VBase3(0.554, 0.554, 0.554),
                    'Visual': {
                        'Color': (0.72, 0.7, 0.59, 1.0),
                        'Model': 'models/islands/pier_platform'
                    }
                },
                '1169854524.59kmuller': {
                    'Type': 'Tunnel Cap',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(511.878, 100.457, 89.359),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6600000262260437, 0.5600000023841858,
                                  0.550000011920929, 1.0),
                        'Model':
                        'models/tunnels/tunnelcap_cave_interior'
                    }
                },
                '1169854987.12kmuller': {
                    'Type': 'Tunnel Cap',
                    'Hpr': VBase3(-171.104, 1.715, 0.0),
                    'Pos': Point3(519.631, -419.873, 53.731),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/tunnels/tunnelcap_cave_interior'
                    }
                },
                '1169858880.15kmuller': {
                    'Type': 'Bridge',
                    'Hpr': VBase3(10.428, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(230.492, -203.011, -8.696),
                    'Scale': VBase3(0.785, 0.407, 0.785),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/islands/pier_bridge'
                    }
                },
                '1169859228.91kmuller': {
                    'Type': 'Crane',
                    'Hpr': VBase3(94.565, 0.667, 0.297),
                    'Pos': Point3(359.839, -214.151, 5.693),
                    'Scale': VBase3(0.665, 0.665, 0.665),
                    'Visual': {
                        'Color': (0.49000000953674316, 0.47999998927116394,
                                  0.5400000214576721, 1.0),
                        'Model':
                        'models/props/Crane_A'
                    }
                },
                '1169859338.24kmuller': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(6.125, -0.279, 0.675),
                    'Pos': Point3(370.488, -213.235, 3.432),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.8299999833106995, 0.7900000214576721,
                                  0.7799999713897705, 1.0),
                        'Model':
                        'models/props/prop_group_A'
                    }
                },
                '1169859488.49kmuller': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-74.42, -0.71, -0.165),
                    'Pos': Point3(396.718, -208.994, 3.061),
                    'Scale': VBase3(0.666, 0.666, 0.666),
                    'Visual': {
                        'Color': (0.6700000166893005, 0.7900000214576721,
                                  0.7799999713897705, 1.0),
                        'Model':
                        'models/props/prop_group_B'
                    }
                },
                '1169859883.62kmuller': {
                    'Type': 'Cart',
                    'DisableCollision': False,
                    'Hpr': VBase3(82.887, -7.995, -4.267),
                    'Pos': Point3(478.978, -0.626, 56.753),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cart_broken'
                    }
                },
                '1169859922.96kmuller': {
                    'Type': 'Log_Stack',
                    'DisableCollision': False,
                    'Hpr': VBase3(-164.03, -14.152, 6.74),
                    'Pos': Point3(468.139, -5.425, 55.133),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/Log_stack_a'
                    }
                },
                '1169860010.41kmuller': {
                    'Type': 'Shanty Tents',
                    'Hpr': VBase3(-76.72, 0.0, 0.0),
                    'Pos': Point3(131.063, -217.518, 2.366),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.8999999761581421, 0.8999999761581421,
                                  0.699999988079071, 1.0),
                        'Model':
                        'models/buildings/shanty_tent_house_body'
                    }
                },
                '1169860119.63kmuller': {
                    'Type': 'Log_Stack',
                    'DisableCollision': False,
                    'Hpr': VBase3(154.702, 0.0, 0.0),
                    'Pos': Point3(120.885, -201.849, 2.333),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Log_stack_c'
                    }
                },
                '1169860195.24kmuller': {
                    'Type': 'Jugs_and_Jars',
                    'Hpr': VBase3(154.702, 0.0, 0.0),
                    'Pos': Point3(141.273, -226.473, 2.2),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bottle_tan'
                    }
                },
                '1169860225.98kmuller': {
                    'Type': 'Crate',
                    'DisableCollision': False,
                    'Hpr': VBase3(154.702, 0.0, 0.0),
                    'Pos': Point3(118.922, -214.506, 2.2),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.49000000953674316, 0.47999998927116394,
                                  0.5400000214576721, 1.0),
                        'Model':
                        'models/props/crate_04'
                    }
                },
                '1169860247.62kmuller': {
                    'Type': 'Jugs_and_Jars',
                    'Hpr': VBase3(154.702, 0.0, 0.0),
                    'Pos': Point3(120.075, -213.737, 5.07),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/winebottle_A'
                    }
                },
                '1169860275.4kmuller': {
                    'Type': 'Food',
                    'Hpr': VBase3(-176.233, 0.0, 0.0),
                    'Pos': Point3(120.283, -210.642, 2.107),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/potatobucket'
                    }
                },
                '1169861731.56kmuller': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-151.416, 0.0, 0.0),
                    'Pos': Point3(115.763, -195.809, 2.2),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/barrel_group_2'
                    }
                },
                '1169862562.79kmuller': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-80.32, -1.997, -7.195),
                    'Pos': Point3(519.78, -101.229, 25.869),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/prop_group04'
                    }
                },
                '1175898368.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-39.332, -0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '2.8313',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(254.614, -86.706, 3.88),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Navy',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175898496.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-170.651, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(253.838, -13.395, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Bat',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175898624.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attention',
                    'Hpr': VBase3(-43.498, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '6.8373',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(432.878, -295.055, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Navy',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175898752.0dxschafe0': {
                    'Type': 'Object Spawn Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(200.942, -115.27, 2.566),
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
                '1175900928.0dxschafe0': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-88.105, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(174.539, -206.423, 2.566),
                    'Scale': VBase3(1.805, 1.805, 1.805),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175900928.0dxschafe1': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(36.972, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(428.334, -377.584, 14.155),
                    'Scale': VBase3(1.805, 1.805, 1.805),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175900928.0dxschafe3': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(106.961, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(456.448, -14.73, 52.101),
                    'Scale': VBase3(1.805, 1.805, 1.805),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175900928.0dxschafe4': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-45.385, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(266.174, -224.5, 4.222),
                    'Scale': VBase3(1.805, 1.805, 1.805),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175900928.0dxschafe5': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(153.349, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(287.154, -40.422, 2.563),
                    'Scale': VBase3(1.805, 1.805, 1.805),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1185562752.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(99.39, 0.0, 0.0),
                    'Pos': Point3(362.73, -218.618, 3.409),
                    'Scale': VBase3(0.65, 0.65, 0.65),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1185562752.0dxschafe1': {
                    'Type': 'Mining_props',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(365.286, -215.554, 3.16),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cave_rusty_bucket'
                    }
                },
                '1185562880.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(99.39, 0.0, 0.0),
                    'Pos': Point3(364.003, -224.934, 3.409),
                    'Scale': VBase3(0.65, 0.65, 0.65),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1185821184.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(12.534, 0.0, 0.001),
                    'Pos': Point3(398.86, -254.34, 2.616),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (1.0, 0.9599999785423279, 0.75, 1.0),
                        'Model': 'models/props/cave_conveyor_tower'
                    }
                },
                '1185828608.0dxschafe': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(-75.009, 0.0, 0.0),
                    'Objects': {
                        '1191004544.0dxschafe': {
                            'Type': 'Mining_props',
                            'Hpr': VBase3(167.156, 0.0, -0.215),
                            'Pos': Point3(55.478, 67.407, 15.81),
                            'Scale': VBase3(0.65, 0.65, 0.65),
                            'Visual': {
                                'Model': 'models/props/cave_mine_cart'
                            }
                        }
                    },
                    'Pos': Point3(439.208, -177.682, 2.318),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_2long'
                    }
                },
                '1185828736.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-73.082, -0.79, -0.459),
                    'Pos': Point3(416.777, -124.371, 14.182),
                    'Scale': VBase3(0.871, 0.871, 0.871),
                    'Visual': {
                        'Color': (1.0, 0.800000011920929, 0.6000000238418579,
                                  1.0),
                        'Model': 'models/props/cave_conveyor_tower'
                    }
                },
                '1185828864.0dxschafe': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(14.784, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(419.379, -116.358, 1.604),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_2long'
                    }
                },
                '1185828992.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(106.361, 0.0, 0.0),
                    'Pos': Point3(426.385, -167.92, 14.249),
                    'Scale': VBase3(0.65, 0.65, 0.65),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1185828992.0dxschafe0': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(106.834, 0.0, 0.0),
                    'Pos': Point3(428.353, -174.581, 14.249),
                    'Scale': VBase3(0.65, 0.65, 0.65),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1185828992.0dxschafe1': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(105.471, 0.0, 0.0),
                    'Pos': Point3(424.374, -161.16, 14.249),
                    'Scale': VBase3(0.65, 0.65, 0.65),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1185829120.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-66.658, 0.0, 0.0),
                    'Pos': Point3(314.086, -221.959, 14.57),
                    'Scale': VBase3(1.74, 1.74, 1.74),
                    'Visual': {
                        'Model': 'models/props/cave_big_wheel'
                    }
                },
                '1185829248.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-75.543, 0.0, 0.0),
                    'Pos': Point3(414.302, -132.378, 21.783),
                    'Scale': VBase3(1.481, 1.481, 1.481),
                    'Visual': {
                        'Model': 'models/props/cave_big_wheel'
                    }
                },
                '1185829376.0dxschafe': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(-75.116, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(452.805, -230.076, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_2long'
                    }
                },
                '1185829376.0dxschafe0': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(-166.28, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(409.831, -259.786, 2.567),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_2long'
                    }
                },
                '1185829888.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(387.066, -145.416, 2.194),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1185830272.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-63.439, 0.0, 0.0),
                    'Pos': Point3(411.61, -121.245, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1185830272.0dxschafe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-123.866, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(425.63, -164.561, 2.375),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1185830272.0dxschafe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-135.824, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(366.801, -180.431, 2.366),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1185830272.0dxschafe2': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-138.827, 2.182, 0.0),
                    'Objects': {},
                    'Pos': Point3(428.399, -230.659, 2.566),
                    'Scale': VBase3(1.186, 1.186, 1.186),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1185830272.0dxschafe3': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-47.924, -0.034, -2.182),
                    'Pos': Point3(416.043, -212.679, 2.566),
                    'Scale': VBase3(0.793, 0.793, 0.793),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1185830272.0dxschafe4': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(104.518, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(407.694, -265.31, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_2long'
                    }
                },
                '1185830400.0dxschafe': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(104.518, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(421.611, -317.68, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_2long'
                    }
                },
                '1185830400.0dxschafe0': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(114.484, 0.844, 0.351),
                    'Pos': Point3(307.63, -230.754, 3.749),
                    'Scale': VBase3(1.073, 1.073, 1.073),
                    'Visual': {
                        'Color': (1.0, 0.800000011920929, 0.6000000238418579,
                                  1.0),
                        'Model': 'models/props/cave_conveyor_tower'
                    }
                },
                '1185830656.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(49.677, 0.0, 0.0),
                    'Pos': Point3(258.055, -96.572, 3.078),
                    'Scale': VBase3(0.65, 0.65, 0.65),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1185830656.0dxschafe0': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-81.617, -0.166, 0.067),
                    'Pos': Point3(33.684, -242.562, 0.625),
                    'Scale': VBase3(0.444, 0.444, 0.444),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1185830656.0dxschafe1': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(49.677, 0.0, 0.0),
                    'Pos': Point3(262.468, -91.052, 2.942),
                    'Scale': VBase3(0.65, 0.65, 0.65),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1185830656.0dxschafe2': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(13.181, 0.0, 0.0),
                    'Pos': Point3(292.125, -180.33, 4.209),
                    'Scale': VBase3(0.65, 0.65, 0.65),
                    'Visual': {
                        'Color': (1.0, 0.79, 0.6901960784313725, 1.0),
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1185830784.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(103.085, 0.0, 0.0),
                    'Pos': Point3(413.882, -277.471, 14.551),
                    'Scale': VBase3(0.65, 0.65, 0.65),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1185830784.0dxschafe1': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(103.085, 0.0, 0.0),
                    'Pos': Point3(415.778, -283.514, 14.551),
                    'Scale': VBase3(0.65, 0.65, 0.65),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1185830784.0dxschafe2': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(103.085, 0.0, 0.0),
                    'Pos': Point3(417.196, -289.584, 14.551),
                    'Scale': VBase3(0.65, 0.65, 0.65),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1185830784.0dxschafe3': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(103.085, 0.0, 0.0),
                    'Pos': Point3(418.77, -295.698, 14.551),
                    'Scale': VBase3(0.65, 0.65, 0.65),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1185830912.0dxschafe': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-169.509, -0.166, -0.899),
                    'Pos': Point3(534.197, -276.242, 2.897),
                    'Scale': VBase3(0.838, 0.838, 0.838),
                    'Visual': {
                        'Color': (0.6700000166893005, 0.7900000214576721,
                                  0.7799999713897705, 1.0),
                        'Model':
                        'models/props/prop_group_B'
                    }
                },
                '1185830912.0dxschafe0': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': True,
                    'Hpr': VBase3(146.165, -14.006, -9.398),
                    'Pos': Point3(488.475, -22.164, 51.169),
                    'Scale': VBase3(0.838, 0.838, 0.838),
                    'Visual': {
                        'Color': (0.77, 0.83, 0.8196078431372549, 1.0),
                        'Model': 'models/props/prop_group_B'
                    }
                },
                '1185830912.0dxschafe1': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-169.509, -0.166, -0.899),
                    'Pos': Point3(435.384, -354.461, 14.558),
                    'Scale': VBase3(0.838, 0.838, 0.838),
                    'Visual': {
                        'Color': (0.6700000166893005, 0.7900000214576721,
                                  0.7799999713897705, 1.0),
                        'Model':
                        'models/props/prop_group_B'
                    }
                },
                '1185830912.0dxschafe2': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(108.624, -0.911, 0.079),
                    'Pos': Point3(153.162, -165.156, 2.566),
                    'Scale': VBase3(1.437, 1.437, 1.437),
                    'Visual': {
                        'Color': (0.7900000214576721, 0.7799999713897705,
                                  0.699999988079071, 1.0),
                        'Model':
                        'models/props/prop_group_A'
                    }
                },
                '1185830912.0dxschafe3': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-88.965, -0.914, 0.017),
                    'Pos': Point3(441.616, -246.79, 14.609),
                    'Scale': VBase3(1.331, 1.331, 1.331),
                    'Visual': {
                        'Color': (0.8299999833106995, 0.7900000214576721,
                                  0.7799999713897705, 1.0),
                        'Model':
                        'models/props/prop_group_A'
                    }
                },
                '1185831040.0dxschafe': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'Aggro Radius': '11.1446',
                    'AnimSet': 'shovel',
                    'CustomModel': 'None',
                    'Hpr': VBase3(-65.875, 0.0, 0.0),
                    'Patrol Radius': '6.1687',
                    'Pos': Point3(374.373, -177.471, 2.881),
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Walk',
                    'Team': 'Villager'
                },
                '1185831296.0dxschafe': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'shovel',
                    'CustomModel': 'None',
                    'Hpr': VBase3(119.005, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(416.002, -162.14, 2.566),
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Walk',
                    'Team': 'Villager'
                },
                '1185831680.0dxschafe0': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'shovel',
                    'CustomModel': 'None',
                    'Hpr': VBase3(104.378, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(417.115, -227.849, 2.566),
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Walk',
                    'Team': 'Villager'
                },
                '1185832064.0dxschafe': {
                    'Type': 'Furniture',
                    'DisableCollision': False,
                    'Hpr': VBase3(12.392, 0.0, 0.0),
                    'Pos': Point3(134.994, -179.561, 2.566),
                    'Scale': VBase3(1.313, 1.313, 1.313),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/bed_shanty'
                    }
                },
                '1185832064.0dxschafe0': {
                    'Type': 'Furniture',
                    'DisableCollision': False,
                    'Hpr': VBase3(104.475, 0.0, 0.0),
                    'Pos': Point3(133.504, -208.576, 2.421),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bed_shantyB'
                    }
                },
                '1185832192.0dxschafe': {
                    'Type': 'Furniture',
                    'DisableCollision': False,
                    'Hpr': VBase3(-167.923, 0.0, 0.0),
                    'Pos': Point3(129.431, -225.357, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bed_shantyB'
                    }
                },
                '1185832192.0dxschafe0': {
                    'Type': 'Furniture',
                    'DisableCollision': False,
                    'Hpr': VBase3(-165.827, 0.0, 0.0),
                    'Pos': Point3(135.994, -223.33, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bed_shantyB'
                    }
                },
                '1185832192.0dxschafe1': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'sit_sleep',
                    'CustomModel': 'None',
                    'Hpr': VBase3(-15.208, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(138.793, -225.279, 3.083),
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Walk',
                    'Team': 'Villager'
                },
                '1185832448.0dxschafe': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'sleep_sick',
                    'CustomModel': 'None',
                    'Hpr': VBase3(-141.725, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(134.033, -208.556, 4.431),
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Walk',
                    'Team': 'Villager'
                },
                '1185921536.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-168.229, 0.0, 0.0),
                    'Pos': Point3(392.929, -250.411, 11.849),
                    'Scale': VBase3(1.481, 1.481, 1.481),
                    'Visual': {
                        'Model': 'models/props/cave_big_wheel'
                    }
                },
                '1185921536.0dxschafe0': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(51.799, 0.0, 0.0),
                    'Pos': Point3(372.149, -274.321, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/wheelbarrow'
                    }
                },
                '1185921536.0dxschafe1': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(51.799, 0.0, 0.0),
                    'Pos': Point3(391.09, -154.407, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/wheelbarrow'
                    }
                },
                '1185921536.0dxschafe2': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(51.799, 0.0, 0.0),
                    'Pos': Point3(291.137, -184.531, 4.222),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/wheelbarrow'
                    }
                },
                '1185921536.0dxschafe3': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(155.365, 0.0, 0.0),
                    'Pos': Point3(266.659, -207.611, 4.222),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/wheelbarrow'
                    }
                },
                '1185921920.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(191.771, 0.0, 341.894),
                    'Pos': Point3(393.22, -265.395, 10.141),
                    'Scale': VBase3(2.412, 2.412, 2.412),
                    'Visual': {
                        'Model': 'models/props/cave_big_wheel'
                    }
                },
                '1185922304.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-15.925, -29.635, -37.86),
                    'Pos': Point3(393.429, -155.992, 2.723),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/prop_pick_axe'
                    }
                },
                '1185922304.0dxschafe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(69.334, 0.0, 0.0),
                    'Pos': Point3(391.323, -154.487, 3.859),
                    'Scale': VBase3(0.166, 0.166, 0.166),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_stone'
                    }
                },
                '1188442752.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '13.5542',
                    'AnimSet': 'bar_talk01',
                    'Hpr': VBase3(-149.891, -0.848, -0.343),
                    'Min Population': '1',
                    'Patrol Radius': '1.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(390.594, -208.577, 3.104),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Navy',
                    'Start State': 'Idle',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1188442880.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.3494',
                    'AnimSet': 'bar_talk02',
                    'Hpr': VBase3(91.807, 0.704, -0.584),
                    'Min Population': '1',
                    'Patrol Radius': '1.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(395.545, -211.948, 2.903),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Navy',
                    'Start State': 'Idle',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190849920.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': VBase3(-158.809, 0.0, 0.0),
                    'Pos': Point3(509.993, -32.207, 45.088),
                    'Scale': VBase3(0.228, 0.228, 0.228),
                    'Visual': {
                        'Color': (0.31, 0.37, 0.37, 1.0),
                        'Model': 'models/props/mound_lavacave_med'
                    }
                },
                '1190850176.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': VBase3(-3.805, 0.0, 0.0),
                    'Pos': Point3(530.061, -163.72, -0.397),
                    'Scale': VBase3(0.429, 0.429, 0.429),
                    'Visual': {
                        'Color': (0.44, 0.6, 0.6, 1.0),
                        'Model': 'models/props/mound_lavacave_med'
                    }
                },
                '1190850432.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(521.915, -197.112, 18.669),
                    'Scale': VBase3(0.869, 0.869, 0.869),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5019607843137255, 1.0),
                        'Model': 'models/props/cave_conveyor_tower'
                    }
                },
                '1190850560.0dxschafe': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(-87.516, 0.0, 0.0),
                    'Objects': {
                        '1191004544.0dxschafe0': {
                            'Type': 'Mining_props',
                            'Hpr': VBase3(-173.787, -0.025, -0.214),
                            'Pos': Point3(-5.981, -10.553, 12.019),
                            'Scale': VBase3(0.65, 0.65, 0.65),
                            'Visual': {
                                'Model': 'models/props/cave_mine_cart'
                            }
                        }
                    },
                    'Pos': Point3(529.574, -225.705, 6.085),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_2long'
                    }
                },
                '1190850560.0dxschafe0': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(-87.516, 0.0, 0.0),
                    'Objects': {
                        '1190851072.0dxschafe': {
                            'Type': 'Prop_Groups',
                            'DisableCollision': False,
                            'Hpr': VBase3(105.482, 0.282, 0.869),
                            'Pos': Point3(-34.191, 14.525, -3.928),
                            'Scale': VBase3(1.331, 1.331, 1.331),
                            'Visual': {
                                'Color': (0.5, 0.5, 0.5, 1.0),
                                'Model': 'models/props/prop_group_A'
                            }
                        }
                    },
                    'Pos': Point3(532.042, -279.683, 6.068),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_2long'
                    }
                },
                '1190850816.0dxschafe': {
                    'Type': 'Cart',
                    'DisableCollision': False,
                    'Hpr': VBase3(-135.998, -12.927, 12.131),
                    'Pos': Point3(501.938, -15.087, 52.926),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.76, 0.8, 0.807843137254902, 1.0),
                        'Model': 'models/props/cart_flat'
                    }
                },
                '1190850944.0dxschafe': {
                    'Type': 'Log_Stack',
                    'DisableCollision': True,
                    'Hpr': VBase3(-164.03, -14.152, -3.66),
                    'Pos': Point3(504.489, -15.574, 56.073),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.79, 0.79, 0.792156862745098, 1.0),
                        'Model': 'models/props/Log_stack_a'
                    }
                },
                '1190851200.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attention',
                    'Hpr': VBase3(129.261, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(499.954, -243.075, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Navy',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190851456.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(526.751, -214.911, 2.566),
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
                '1190851584.0dxschafe': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(3.052, 0.0, 0.0),
                    'Pos': Point3(524.288, -204.813, 1.98),
                    'Scale': VBase3(2.642, 1.0, 2.212),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1190851712.0dxschafe': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-155.528, 0.0, 8.605),
                    'Pos': Point3(494.85, -14.45, 50.879),
                    'Scale': VBase3(4.547, 1.0, 2.692),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1191003904.0dxschafe': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(45.193, 0.0, 0.0),
                    'Pos': Point3(277.579, -185.177, 4.222),
                    'Scale': VBase3(0.654, 0.654, 0.654),
                    'Visual': {
                        'Color': (1.0, 0.76, 0.6509803921568628, 1.0),
                        'Model': 'models/props/barrel_group_3'
                    }
                },
                '1191624448.0dxschafe': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1191624448.0dxschafe0',
                    'Hpr': VBase3(83.665, 0.0, 0.0),
                    'Pos': Point3(325.806, -318.193, 2.714),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Model': 'models/buildings/fort_eitc',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1191624832.0dxschafe': {
                    'Type': 'Bridge',
                    'Hpr': VBase3(-4.871, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(356.979, -322.177, 2.509),
                    'Scale': VBase3(0.519, 0.519, 0.519),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/buildings/bridge_port_royal'
                    }
                },
                '1191624960.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'idleB',
                    'Hpr': VBase3(-97.372, 0.0, 0.0),
                    'Level': '10',
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(352.71, -321.958, 3.866),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'EITC - Thug',
                    'Start State': 'Idle',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1191624960.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '21.0843',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-96.895, 0.0, 0.0),
                    'Level': '9',
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(441.267, -318.512, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'EITC - Thug',
                    'Start State': 'Idle',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192136704.0dxschafe': {
                    'Type': 'Bridge',
                    'Hpr': VBase3(18.172, -3.463, 2.663),
                    'Pos': Point3(332.212, -178.693, -6.984),
                    'Scale': VBase3(0.797, 0.406, 0.712),
                    'Visual': {
                        'Model': 'models/islands/pier_bridge'
                    }
                },
                '1192139776.0dxschafe1': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(8.317, 0.0, 0.0),
                    'Pos': Point3(370.434, -175.604, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cave_rusty_bucket'
                    }
                },
                '1192139776.0dxschafe2': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(270.738, -210.947, 3.942),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.71, 0.96, 0.6941176470588235, 1.0),
                        'Model': 'models/props/cave_rusty_bucket'
                    }
                },
                '1192140288.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attention',
                    'Hpr': VBase3(-162.131, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(384.986, -136.759, 14.379),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Navy',
                    'Start State': 'Idle',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192140416.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attention',
                    'Hpr': VBase3(101.548, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(439.638, -219.553, 15.793),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Navy',
                    'Start State': 'Idle',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192578304.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(160.763, -167.474, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192578304.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(205.676, -222.125, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192578304.0dxschafe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(308.216, -27.333, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192578304.0dxschafe2': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(180.502, -177.483, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192578432.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(148.457, -211.503, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192578432.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(296.837, -33.556, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192578432.0dxschafe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(388.013, -280.688, 2.567),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192578432.0dxschafe2': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(510.6, -210.778, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192578688.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(375.962, -276.779, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192578688.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(412.827, -172.408, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192578816.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(376.265, -321.171, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192578816.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': VBase3(0.0, 0.0, 1.869),
                    'Pause Chance': '43',
                    'Pause Duration': '12',
                    'Pos': Point3(359.43, -321.344, 4.703),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192578944.0dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(105.558, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '48',
                    'Pause Duration': '9',
                    'Pos': Point3(409.983, -154.904, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Navy',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192578944.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '46',
                    'Pause Duration': '5',
                    'Pos': Point3(141.307, -215.913, 2.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192579072.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': VBase3(109.071, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '9',
                    'Pos': Point3(284.387, -190.212, 4.222),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192579200.0dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'sit_sleep',
                    'Hpr': VBase3(-3.78, 8.114, -2.884),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(502.385, -10.561, 54.38),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Navy',
                    'Start State': 'Idle',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192579328.0dxschafe': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-78.519, 1.757, 11.531),
                    'Pos': Point3(502.616, -10.459, 54.216),
                    'Scale': VBase3(0.53, 0.53, 0.53),
                    'Visual': {
                        'Model': 'models/props/barrel_sideways'
                    }
                },
                '1193083904.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': VBase3(0.0, 0.0, 1.869),
                    'Pause Chance': '43',
                    'Pause Duration': '12',
                    'Pos': Point3(359.118, -325.095, 3.459),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193084032.0dxschafe': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-169.509, -0.166, -0.899),
                    'Pos': Point3(446.934, -323.819, 2.279),
                    'Scale': VBase3(0.838, 0.838, 0.838),
                    'Visual': {
                        'Color': (0.6700000166893005, 0.7900000214576721,
                                  0.7799999713897705, 1.0),
                        'Model':
                        'models/props/prop_group_B'
                    }
                }
            },
            'Visual': {
                'Model': 'models/caves/cave_a_zero'
            }
        }
    },
    'Node Links':
    [['1192578304.0dxschafe0', '1165197708.75Shochet', 'Bi-directional'],
     ['1192578304.0dxschafe0', '1192578304.0dxschafe', 'Bi-directional'],
     ['1192578304.0dxschafe', '1165197708.75Shochet', 'Bi-directional'],
     ['1192578304.0dxschafe2', '1192578304.0dxschafe1', 'Bi-directional'],
     ['1175898496.0dxschafe', '1192578304.0dxschafe1', 'Bi-directional'],
     ['1175898496.0dxschafe', '1192578304.0dxschafe2', 'Bi-directional'],
     ['1192578432.0dxschafe', '1192578432.0dxschafe0', 'Bi-directional'],
     ['1192578432.0dxschafe', '1165197665.86Shochet', 'Bi-directional'],
     ['1192578432.0dxschafe0', '1165197665.86Shochet', 'Bi-directional'],
     ['1192578432.0dxschafe1', '1192578432.0dxschafe2', 'Bi-directional'],
     ['1192578432.0dxschafe1', '1165197613.83Shochet', 'Bi-directional'],
     ['1192578432.0dxschafe2', '1165197613.83Shochet', 'Bi-directional'],
     ['1192578688.0dxschafe0', '1165197639.41Shochet', 'Bi-directional'],
     ['1192578688.0dxschafe', '1192578688.0dxschafe0', 'Bi-directional'],
     ['1192578688.0dxschafe', '1165197639.41Shochet', 'Bi-directional'],
     ['1192578816.0dxschafe', '1164999523.0Shochet', 'Bi-directional'],
     ['1192578816.0dxschafe', '1192578816.0dxschafe0', 'Bi-directional'],
     ['1192578944.0dxschafe', '1192579072.0dxschafe', 'Bi-directional'],
     ['1192578944.0dxschafe0', '1192579072.0dxschafe', 'Bi-directional'],
     ['1193083904.0dxschafe', '1191624960.0dxschafe0', 'Bi-directional']],
    'Layers': {},
    'ObjectIds': {
        '1164952144.06sdnaik':
        '["Objects"]["1164952144.06sdnaik"]',
        '1164953534.72sdnaik':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1164953534.72sdnaik"]',
        '1164953534.72sdnaik0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1164953534.72sdnaik0"]',
        '1164953534.73sdnaik':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1164953534.73sdnaik"]',
        '1164999249.69Shochet':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1164999249.69Shochet"]',
        '1164999287.17Shochet':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1164999287.17Shochet"]',
        '1164999438.31Shochet':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1164999438.31Shochet"]',
        '1164999523.0Shochet':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1164999523.0Shochet"]',
        '1164999574.83Shochet':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1164999574.83Shochet"]',
        '1164999709.16Shochet':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1164999709.16Shochet"]',
        '1164999816.83Shochet':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1164999816.83Shochet"]',
        '1165019105.05Shochet':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1165019105.05Shochet"]',
        '1165019132.53Shochet':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1165019132.53Shochet"]',
        '1165019166.08Shochet':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1165019166.08Shochet"]',
        '1165197613.83Shochet':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1165197613.83Shochet"]',
        '1165197639.41Shochet':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1165197639.41Shochet"]',
        '1165197665.86Shochet':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1165197665.86Shochet"]',
        '1165197708.75Shochet':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1165197708.75Shochet"]',
        '1169616862.13sdnaik':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169616862.13sdnaik"]',
        '1169617104.89sdnaik':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169617104.89sdnaik"]',
        '1169617420.52sdnaik':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169617420.52sdnaik"]',
        '1169617816.94sdnaik':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169617816.94sdnaik"]',
        '1169854524.59kmuller':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169854524.59kmuller"]',
        '1169854987.12kmuller':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169854987.12kmuller"]',
        '1169858880.15kmuller':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169858880.15kmuller"]',
        '1169859228.91kmuller':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169859228.91kmuller"]',
        '1169859338.24kmuller':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169859338.24kmuller"]',
        '1169859488.49kmuller':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169859488.49kmuller"]',
        '1169859883.62kmuller':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169859883.62kmuller"]',
        '1169859922.96kmuller':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169859922.96kmuller"]',
        '1169860010.41kmuller':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169860010.41kmuller"]',
        '1169860119.63kmuller':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169860119.63kmuller"]',
        '1169860195.24kmuller':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169860195.24kmuller"]',
        '1169860225.98kmuller':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169860225.98kmuller"]',
        '1169860247.62kmuller':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169860247.62kmuller"]',
        '1169860275.4kmuller':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169860275.4kmuller"]',
        '1169861731.56kmuller':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169861731.56kmuller"]',
        '1169862562.79kmuller':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169862562.79kmuller"]',
        '1175898368.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1175898368.0dxschafe"]',
        '1175898496.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1175898496.0dxschafe"]',
        '1175898624.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1175898624.0dxschafe0"]',
        '1175898752.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1175898752.0dxschafe0"]',
        '1175900928.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169617816.94sdnaik"]["Objects"]["1175900928.0dxschafe"]',
        '1175900928.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1175900928.0dxschafe0"]',
        '1175900928.0dxschafe1':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1175900928.0dxschafe1"]',
        '1175900928.0dxschafe3':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1175900928.0dxschafe3"]',
        '1175900928.0dxschafe4':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1175900928.0dxschafe4"]',
        '1175900928.0dxschafe5':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1175900928.0dxschafe5"]',
        '1175900928.0dxschafe6':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1169617420.52sdnaik"]["Objects"]["1175900928.0dxschafe6"]',
        '1185562752.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185562752.0dxschafe"]',
        '1185562752.0dxschafe1':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185562752.0dxschafe1"]',
        '1185562880.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185562880.0dxschafe"]',
        '1185821184.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185821184.0dxschafe"]',
        '1185828608.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185828608.0dxschafe"]',
        '1185828736.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185828736.0dxschafe"]',
        '1185828864.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185828864.0dxschafe"]',
        '1185828992.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185828992.0dxschafe"]',
        '1185828992.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185828992.0dxschafe0"]',
        '1185828992.0dxschafe1':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185828992.0dxschafe1"]',
        '1185829120.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185829120.0dxschafe"]',
        '1185829248.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185829248.0dxschafe"]',
        '1185829376.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185829376.0dxschafe"]',
        '1185829376.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185829376.0dxschafe0"]',
        '1185829888.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185829888.0dxschafe"]',
        '1185830272.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830272.0dxschafe"]',
        '1185830272.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830272.0dxschafe0"]',
        '1185830272.0dxschafe1':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830272.0dxschafe1"]',
        '1185830272.0dxschafe2':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830272.0dxschafe2"]',
        '1185830272.0dxschafe3':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830272.0dxschafe3"]',
        '1185830272.0dxschafe4':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830272.0dxschafe4"]',
        '1185830400.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830400.0dxschafe"]',
        '1185830400.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830400.0dxschafe0"]',
        '1185830656.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830656.0dxschafe"]',
        '1185830656.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830656.0dxschafe0"]',
        '1185830656.0dxschafe1':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830656.0dxschafe1"]',
        '1185830656.0dxschafe2':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830656.0dxschafe2"]',
        '1185830784.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830784.0dxschafe"]',
        '1185830784.0dxschafe1':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830784.0dxschafe1"]',
        '1185830784.0dxschafe2':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830784.0dxschafe2"]',
        '1185830784.0dxschafe3':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830784.0dxschafe3"]',
        '1185830912.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830912.0dxschafe"]',
        '1185830912.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830912.0dxschafe0"]',
        '1185830912.0dxschafe1':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830912.0dxschafe1"]',
        '1185830912.0dxschafe2':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830912.0dxschafe2"]',
        '1185830912.0dxschafe3':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185830912.0dxschafe3"]',
        '1185831040.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185831040.0dxschafe"]',
        '1185831296.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185831296.0dxschafe"]',
        '1185831680.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185831680.0dxschafe0"]',
        '1185832064.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185832064.0dxschafe"]',
        '1185832064.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185832064.0dxschafe0"]',
        '1185832192.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185832192.0dxschafe"]',
        '1185832192.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185832192.0dxschafe0"]',
        '1185832192.0dxschafe1':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185832192.0dxschafe1"]',
        '1185832448.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185832448.0dxschafe"]',
        '1185921536.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185921536.0dxschafe"]',
        '1185921536.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185921536.0dxschafe0"]',
        '1185921536.0dxschafe1':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185921536.0dxschafe1"]',
        '1185921536.0dxschafe2':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185921536.0dxschafe2"]',
        '1185921536.0dxschafe3':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185921536.0dxschafe3"]',
        '1185921920.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185921920.0dxschafe"]',
        '1185922304.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185922304.0dxschafe"]',
        '1185922304.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185922304.0dxschafe0"]',
        '1188442752.0dxschafe1':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1188442752.0dxschafe1"]',
        '1188442880.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1188442880.0dxschafe"]',
        '1190849920.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1190849920.0dxschafe"]',
        '1190850176.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1190850176.0dxschafe"]',
        '1190850432.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1190850432.0dxschafe"]',
        '1190850560.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1190850560.0dxschafe"]',
        '1190850560.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1190850560.0dxschafe0"]',
        '1190850816.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1190850816.0dxschafe"]',
        '1190850944.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1190850944.0dxschafe"]',
        '1190851072.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1190850560.0dxschafe0"]["Objects"]["1190851072.0dxschafe"]',
        '1190851200.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1190851200.0dxschafe"]',
        '1190851456.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1190851456.0dxschafe"]',
        '1190851584.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1190851584.0dxschafe"]',
        '1190851712.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1190851712.0dxschafe"]',
        '1191003904.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1191003904.0dxschafe"]',
        '1191004544.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1185828608.0dxschafe"]["Objects"]["1191004544.0dxschafe"]',
        '1191004544.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1190850560.0dxschafe"]["Objects"]["1191004544.0dxschafe0"]',
        '1191624448.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1191624448.0dxschafe"]',
        '1191624448.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1191624448.0dxschafe"]',
        '1191624832.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1191624832.0dxschafe"]',
        '1191624960.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1191624960.0dxschafe"]',
        '1191624960.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1191624960.0dxschafe0"]',
        '1192136704.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192136704.0dxschafe"]',
        '1192139776.0dxschafe1':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192139776.0dxschafe1"]',
        '1192139776.0dxschafe2':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192139776.0dxschafe2"]',
        '1192140288.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192140288.0dxschafe"]',
        '1192140416.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192140416.0dxschafe"]',
        '1192578304.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192578304.0dxschafe"]',
        '1192578304.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192578304.0dxschafe0"]',
        '1192578304.0dxschafe1':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192578304.0dxschafe1"]',
        '1192578304.0dxschafe2':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192578304.0dxschafe2"]',
        '1192578432.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192578432.0dxschafe"]',
        '1192578432.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192578432.0dxschafe0"]',
        '1192578432.0dxschafe1':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192578432.0dxschafe1"]',
        '1192578432.0dxschafe2':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192578432.0dxschafe2"]',
        '1192578688.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192578688.0dxschafe"]',
        '1192578688.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192578688.0dxschafe0"]',
        '1192578816.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192578816.0dxschafe"]',
        '1192578816.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192578816.0dxschafe0"]',
        '1192578944.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192578944.0dxschafe"]',
        '1192578944.0dxschafe0':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192578944.0dxschafe0"]',
        '1192579072.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192579072.0dxschafe"]',
        '1192579200.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192579200.0dxschafe"]',
        '1192579328.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1192579328.0dxschafe"]',
        '1193083904.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1193083904.0dxschafe"]',
        '1193084032.0dxschafe':
        '["Objects"]["1164952144.06sdnaik"]["Objects"]["1193084032.0dxschafe"]'
    }
}
