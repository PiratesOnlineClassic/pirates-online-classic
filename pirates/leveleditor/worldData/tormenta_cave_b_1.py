# Embedded file name: pirates.leveleditor.worldData.tormenta_cave_b_1
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
    [['1179946138.7Aholdun', '1186714240.0dxschafe0', 'Bi-directional']],
    'Objects': {
        '1172208344.92sdnaik': {
            'Type': 'Island Game Area',
            'Name': 'tormenta_isle_cave_b_1',
            'File': '',
            'Instanced': True,
            'Objects': {
                '1172208565.59sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_1',
                    'Hpr': VBase3(-98.823, 0.0, 0.0),
                    'Pos': Point3(407.795, 202.769, 1.938),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1172208565.61sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_2',
                    'Hpr': VBase3(-5.579, 0.0, 0.0),
                    'Pos': Point3(-535.718, 237.303, 77.641),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1178829600.66kmuller': {
                    'Type': 'Tunnel Cap',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(407.827, 202.103, 4.352),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/tunnels/tunnelcap_cave_interior'
                    }
                },
                '1178829636.06kmuller': {
                    'Type': 'Tunnel Cap',
                    'Hpr': VBase3(77.096, 0.0, 0.0),
                    'Pos': Point3(-534.993, 239.804, 80.614),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/tunnels/tunnelcap_cave_interior'
                    }
                },
                '1179861836.94Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(44.332, -205.084, 28.444),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Vampire Bat',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179861898.15Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-137.903, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-139.355, -3.74, 55.32),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Vampire Bat',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179861984.82Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-53.144, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(139.478, -179.77, 24.207),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Vampire Bat',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179862042.35Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-118.792, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(38.39, -143.154, 28.704),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid DJCrew',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946104.72Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'shovel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '17',
                    'Pos': Point3(-303.853, 15.733, 56.751),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Early DJCrew',
                    'Start State': 'Idle',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946138.7Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_searching',
                    'Hpr': VBase3(-179.901, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '3.8614',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-53.424, 72.301, 32.83),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Fierce DJCrew',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946169.66Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'shovel',
                    'Hpr': VBase3(-85.561, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-65.607, 126.244, 33.58),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Elite DJCrew',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946209.01Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-146.725, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-3.295, 18.954, 30.545),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mean DJCrew',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946254.11Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(171.747, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-303.704, 123.547, 65.861),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Vampire Bat',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946309.78Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '11.4458',
                    'AnimSet': 'shovel',
                    'Hpr': VBase3(146.988, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '9.2410',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-85.489, 18.824, 37.984),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High DJCrew',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946339.7Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'shovel',
                    'Hpr': VBase3(-145.199, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(32.659, -67.721, 28.952),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mean DJCrew',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946425.84Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'shovel',
                    'Hpr': VBase3(63.686, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(433.845, -166.544, 2.175),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High DJCrew',
                    'Start State': 'Idle',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946450.75Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_handdig',
                    'Hpr': VBase3(162.906, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(50.953, -1.346, 28.132),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Fierce DJCrew',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946516.51Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-461.531, 196.632, 78.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946525.14Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-138.93, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-367.727, 141.655, 70.346),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946536.17Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-458.979, 80.261, 78.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946544.58Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-300.304, 55.018, 63.481),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946559.31Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-287.353, -34.183, 55.796),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946567.39Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-52.399, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-231.503, -91.126, 55.796),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946574.14Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-70.34, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-170.68, -46.799, 57.597),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946583.05Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-0.439, -32.523, 30.423),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946592.47Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(82.67, -178.76, 26.736),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946606.01Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-46.496, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-306.155, -84.706, 55.796),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946619.58Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(160.744, -205.924, 21.02),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946626.42Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(46.372, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(367.556, -211.858, 2.175),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179946645.89Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(264.425, -166.671, 2.176),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186714240.0dxschafe0': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(22.886, 129.354, 29.37),
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
                '1189459263.3kmuller': {
                    'Type': 'Ship Wreck',
                    'Hpr': VBase3(-81.32, 2.787, 10.788),
                    'Pos': Point3(372.933, -105.617, -16.515),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.56, 0.69, 0.6862745098039216, 1.0),
                        'Model': 'models/shipparts/shipwreck_aft'
                    }
                },
                '1189459407.59kmuller': {
                    'Type': 'Ship Wreck',
                    'Hpr': VBase3(-4.112, -5.098, 37.189),
                    'Pos': Point3(5.689, 101.42, 6.249),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.57, 0.69, 0.65, 1.0),
                        'Model': 'models/shipparts/shipwreck_fore'
                    }
                },
                '1189459652.73kmuller': {
                    'Type': 'Searchable Container',
                    'Hpr': VBase3(-29.149, 0.0, 0.0),
                    'Pos': Point3(-108.077, 164.237, 35.198),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.4000000059604645, 0.4000000059604645,
                                  0.4000000059604645, 1.0),
                        'Model':
                        'models/props/crate_04'
                    },
                    'searchTime': '6.2',
                    'type': 'Crate'
                },
                '1189459701.39kmuller': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-29.987, -9.072, 0.0),
                    'Pos': Point3(2.54, 89.113, 29.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/barrel_sideways'
                    }
                },
                '1189459734.55kmuller': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-52.426, 5.012, 0.0),
                    'Pos': Point3(-39.837, 149.515, 32.161),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1189459903.72kmuller': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(37.051, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-451.183, 161.905, 78.064),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low DJCrew',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189460022.72kmuller': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(48.745, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(396.942, -16.408, -0.529),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High DJCrew',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189460063.77kmuller': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '9.0361',
                    'AnimSet': 'gp_handdig',
                    'Hpr': VBase3(4.756, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '8.5542',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(353.594, -121.522, -1.064),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Fierce DJCrew',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189643438.33kmuller': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(69.535, 0.0, 0.0),
                    'Pos': Point3(-339.537, -13.086, 55.613),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.7254902124404907, 0.8509804010391235,
                                  0.8823529481887817, 1.0),
                        'Model':
                        'models/props/dirt_pile_cave'
                    }
                },
                '1189643543.84kmuller': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(466.957, -173.215, 2.06),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6313725709915161, 0.772549033164978,
                                  0.7921568751335144, 1.0),
                        'Model':
                        'models/props/dirt_pile_cave'
                    }
                },
                '1189643569.14kmuller': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'shovel',
                    'Hpr': VBase3(-28.456, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(301.316, -192.776, 2.175),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid DJCrew',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192494720.0dxschafe': {
                    'Type': 'Ship Wreck',
                    'Hpr': VBase3(135.723, -2.0, -23.926),
                    'Pos': Point3(-119.015, 60.801, 32.512),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.57, 0.69, 0.65, 1.0),
                        'Model': 'models/shipparts/shipwreck_fore'
                    }
                },
                '1192494848.0dxschafe': {
                    'Type': 'Ship Wreck',
                    'Hpr': VBase3(58.171, 7.049, -18.544),
                    'Pos': Point3(-40.161, 163.342, 28.117),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.56, 0.69, 0.6862745098039216, 1.0),
                        'Model': 'models/shipparts/shipwreck_aft'
                    }
                },
                '1192495104.0dxschafe': {
                    'Type': 'Ship Wreck',
                    'Hpr': VBase3(-48.534, -5.8, 37.717),
                    'Pos': Point3(305.064, -52.442, 3.161),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.57, 0.69, 0.65, 1.0),
                        'Model': 'models/shipparts/shipwreck_fore'
                    }
                },
                '1192495232.0dxschafe': {
                    'Type': 'Ship Wreck',
                    'Hpr': VBase3(58.17, 7.049, -70.989),
                    'Pos': Point3(-118.394, 34.39, 63.913),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.56, 0.69, 0.6862745098039216, 1.0),
                        'Model': 'models/shipparts/shipwreck_aft'
                    }
                },
                '1192495744.0dxschafe': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(7.094, 2.547, -4.318),
                    'Pos': Point3(-46.959, 147.995, 32.478),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192495744.0dxschafe0': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-69.678, 2.391, -0.53),
                    'Pos': Point3(-79.768, 75.669, 34.149),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192495744.0dxschafe1': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-131.748, 0.931, 4.925),
                    'Pos': Point3(-80.286, 45.638, 33.971),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192495872.0dxschafe': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-56.12, 1.479, 6.97),
                    'Pos': Point3(37.939, 35.277, 28.709),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/barrel_sideways'
                    }
                },
                '1192497024.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'shovel',
                    'Hpr': VBase3(176.667, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-32.332, 81.422, 31.833),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Elite DJCrew',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192815360.0dxschafe': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(46.796, 24.951, 28.315),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/prop_group_A'
                    }
                },
                '1192815488.0dxschafe': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(157.601, -18.353, 10.543),
                    'Pos': Point3(-86.663, 65.793, 36.537),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/prop_group_D'
                    }
                },
                '1192815488.0dxschafe0': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-23.953, 0.0, 0.0),
                    'Pos': Point3(4.788, 153.504, 30.174),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.4000000059604645, 0.4000000059604645,
                                  0.4000000059604645, 1.0),
                        'Model':
                        'models/props/prop_group_F'
                    }
                },
                '1192815488.0dxschafe1': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-8.648, 0.0, 0.0),
                    'Pos': Point3(-51.049, 166.216, 32.829),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_B'
                    }
                },
                '1192815488.0dxschafe10': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(127.489, 0.0, 0.0),
                    'Pos': Point3(-2.168, 52.052, 30.493),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_G'
                    }
                },
                '1192815488.0dxschafe11': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(179.514, 0.0, 0.0),
                    'Pos': Point3(20.122, 23.272, 29.502),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_H'
                    }
                },
                '1192815488.0dxschafe12': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(58.571, 0.0, 0.0),
                    'Pos': Point3(10.974, 92.834, 29.904),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_A'
                    }
                },
                '1192815488.0dxschafe2': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(58.571, 2.446, 0.0),
                    'Pos': Point3(-33.063, 173.067, 31.857),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.4000000059604645, 0.4000000059604645,
                                  0.4000000059604645, 1.0),
                        'Model':
                        'models/props/prop_group_E'
                    }
                },
                '1192815488.0dxschafe3': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(101.122, -0.615, -0.67),
                    'Pos': Point3(-83.549, 97.457, 33.897),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_C'
                    }
                },
                '1192815488.0dxschafe4': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-73.363, 0.0, 0.0),
                    'Pos': Point3(72.731, 9.538, 27.162),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.4000000059604645, 0.4000000059604645,
                                  0.4000000059604645, 1.0),
                        'Model':
                        'models/props/prop_group_C'
                    }
                },
                '1192815488.0dxschafe5': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(58.571, 0.0, 6.277),
                    'Pos': Point3(-150.431, 13.388, 55.543),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_A'
                    }
                },
                '1192815488.0dxschafe6': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(58.571, 0.0, 0.0),
                    'Pos': Point3(-68.431, 88.807, 33.439),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_A'
                    }
                },
                '1192815488.0dxschafe7': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(58.571, 0.0, 0.0),
                    'Pos': Point3(-110.778, 166.463, 35.399),
                    'Scale': VBase3(1.258, 1.258, 1.258),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_A'
                    }
                },
                '1192815488.0dxschafe8': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(149.525, 0.0, -2.179),
                    'Pos': Point3(-72.26, 147.613, 33.661),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group03'
                    }
                },
                '1192815488.0dxschafe9': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-177.666, 0.0, 0.0),
                    'Pos': Point3(-11.085, 162.685, 30.765),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_G'
                    }
                },
                '1192815616.0dxschafe': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(112.589, 0.0, 0.0),
                    'Pos': Point3(-180.115, 29.348, 57.212),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_H'
                    }
                },
                '1192815616.0dxschafe0': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(112.47, 0.0, 0.0),
                    'Pos': Point3(-170.041, -18.392, 56.9),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_F'
                    }
                },
                '1192815616.0dxschafe1': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(58.571, 0.0, 0.0),
                    'Pos': Point3(-166.245, 15.917, 56.905),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_G'
                    }
                },
                '1192815616.0dxschafe2': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(59.05, 2.697, -49.881),
                    'Pos': Point3(-153.456, 43.53, 60.102),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_E'
                    }
                },
                '1192815616.0dxschafe3': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(58.571, 0.0, 0.0),
                    'Pos': Point3(-119.906, 70.981, 35.732),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_A'
                    }
                },
                '1192815616.0dxschafe4': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-67.021, 0.0, 0.0),
                    'Pos': Point3(-211.933, 9.805, 55.789),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_C'
                    }
                },
                '1192815616.0dxschafe5': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-32.742, -2.971, 0.0),
                    'Pos': Point3(-183.629, -25.549, 57.986),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_A'
                    }
                },
                '1192815616.0dxschafe6': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(58.571, 0.0, 0.0),
                    'Pos': Point3(76.572, -4.271, 26.992),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_A'
                    }
                },
                '1192815616.0dxschafe7': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-35.016, 0.0, 0.0),
                    'Pos': Point3(85.602, -1.002, 26.59),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/prop_group_B'
                    }
                },
                '1192815872.0dxschafe': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-57.436, 13.521, 12.212),
                    'Pos': Point3(-84.679, 62.633, 36.1),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816384.0dxschafe': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(112.733, 7.296, -1.312),
                    'Pos': Point3(-159.792, 35.946, 55.737),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816384.0dxschafe0': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-86.783, -7.316, -1.194),
                    'Pos': Point3(-165.163, 36.479, 56.295),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816384.0dxschafe1': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-122.987, -5.21, -5.279),
                    'Pos': Point3(-159.268, 35.658, 59.838),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816384.0dxschafe2': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(143.506, -50.512, -94.799),
                    'Pos': Point3(-165.61, 34.356, 58.614),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816512.0dxschafe': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(143.506, -50.512, -94.799),
                    'Pos': Point3(-151.374, 37.764, 56.246),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816512.0dxschafe0': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(58.571, 0.0, -13.908),
                    'Pos': Point3(-148.716, 31.4, 54.291),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_A'
                    }
                },
                '1192816512.0dxschafe1': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-3.472, -10.905, 5.734),
                    'Pos': Point3(-142.379, 34.054, 52.45),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_D'
                    }
                },
                '1192816640.0dxschafe': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.356, 4.115, -2.743),
                    'Pos': Point3(-198.822, 17.896, 57.51),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_B'
                    }
                },
                '1192816640.0dxschafe0': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(111.023, -1.499, 1.616),
                    'Pos': Point3(-189.405, -35.679, 57.753),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_B'
                    }
                },
                '1192816768.0dxschafe': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-122.987, -5.21, -5.279),
                    'Pos': Point3(-200.34, -38.248, 58.353),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816768.0dxschafe0': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(168.828, 2.991, -6.784),
                    'Pos': Point3(-177.605, 5.915, 57.346),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816768.0dxschafe1': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(155.851, 1.104, -5.95),
                    'Pos': Point3(-219.784, -15.467, 55.335),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816768.0dxschafe2': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-159.746, -3.386, -5.017),
                    'Pos': Point3(-237.461, -32.42, 54.923),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816768.0dxschafe3': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-82.128, -5.631, 2.219),
                    'Pos': Point3(-242.945, -42.064, 54.768),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816896.0dxschafe': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-82.128, -5.631, 2.219),
                    'Pos': Point3(-59.23, 34.689, 33.034),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816896.0dxschafe0': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-82.128, -5.631, 2.219),
                    'Pos': Point3(58.932, 9.357, 27.776),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816896.0dxschafe1': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-17.979, -0.455, 6.034),
                    'Pos': Point3(104.385, -25.798, 25.756),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816896.0dxschafe2': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(3.301, 1.773, 5.786),
                    'Pos': Point3(-13.385, 142.626, 30.984),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816896.0dxschafe3': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(3.301, 1.773, 5.786),
                    'Pos': Point3(-3.767, 36.083, 30.558),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816896.0dxschafe4': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(74.678, 6.048, 0.173),
                    'Pos': Point3(27.549, 8.541, 29.173),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816896.0dxschafe5': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(43.921, 5.114, 3.238),
                    'Pos': Point3(52.866, -41.751, 28.051),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816896.0dxschafe6': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(43.921, 5.114, 3.238),
                    'Pos': Point3(9.41, 6.032, 29.981),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192816896.0dxschafe7': {
                    'Type': 'Crate',
                    'DisableCollision': False,
                    'Hpr': VBase3(-8.954, 0.0, 0.0),
                    'Pos': Point3(17.726, -3.569, 29.612),
                    'Scale': VBase3(1.229, 1.229, 1.229),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1192816896.0dxschafe8': {
                    'Type': 'Crate',
                    'DisableCollision': False,
                    'Hpr': VBase3(-8.954, 0.0, 0.0),
                    'Pos': Point3(-56.013, 24.162, 32.892),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/crate'
                    }
                },
                '1192817024.0dxschafe': {
                    'Type': 'Crate',
                    'DisableCollision': False,
                    'Hpr': VBase3(22.895, 2.549, 19.454),
                    'Pos': Point3(-75.121, 20.162, 34.297),
                    'Scale': VBase3(1.571, 1.571, 1.571),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/crate'
                    }
                },
                '1192817024.0dxschafe0': {
                    'Type': 'Crate',
                    'DisableCollision': False,
                    'Hpr': VBase3(22.895, 2.549, 2.437),
                    'Pos': Point3(-75.848, 78.814, 33.77),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/crate'
                    }
                },
                '1192817024.0dxschafe1': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-87.164, -23.697, 25.596),
                    'Pos': Point3(-80.854, 61.701, 49.321),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.800000011920929, 1.0, 0.6000000238418579,
                                  1.0),
                        'Model': 'models/props/prop_group_F'
                    }
                },
                '1192817152.0dxschafe': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-66.813, -20.651, -4.457),
                    'Pos': Point3(-120.559, 21.006, 49.897),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_D'
                    }
                },
                '1192817152.0dxschafe0': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-177.287, 12.042, -20.535),
                    'Pos': Point3(-119.109, 27.756, 47.25),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/prop_group_F'
                    }
                },
                '1192817152.0dxschafe1': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-177.287, 12.042, -20.535),
                    'Pos': Point3(-120.133, 55.503, 35.744),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_F'
                    }
                },
                '1192817152.0dxschafe2': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-176.588, 13.319, -28.172),
                    'Pos': Point3(-111.421, 40.516, 40.232),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_G'
                    }
                },
                '1192817280.0dxschafe': {
                    'Type': 'Crate',
                    'DisableCollision': False,
                    'Hpr': VBase3(17.281, 0.0, 0.0),
                    'Pos': Point3(59.024, -37.536, 27.776),
                    'Scale': VBase3(1.602, 1.602, 1.602),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/crate'
                    }
                },
                '1192817280.0dxschafe0': {
                    'Type': 'Crate',
                    'DisableCollision': False,
                    'Hpr': VBase3(-8.954, 0.0, 0.0),
                    'Pos': Point3(-32.903, 140.73, 31.853),
                    'Scale': VBase3(1.229, 1.229, 1.229),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/crate'
                    }
                },
                '1192817280.0dxschafe1': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(134.699, 0.0, 0.0),
                    'Pos': Point3(-78.957, 65.311, 33.934),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group03'
                    }
                },
                '1192817408.0dxschafe': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(122.2, -0.815, -0.404),
                    'Pos': Point3(-115.982, 137.798, 35.217),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_F'
                    }
                },
                '1192817408.0dxschafe0': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-69.323, -2.569, -0.78),
                    'Pos': Point3(-91.251, 161.21, 33.84),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192817536.0dxschafe': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(33.727, 16.362, -14.413),
                    'Pos': Point3(-84.723, 160.77, 51.495),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_B'
                    }
                },
                '1192817536.0dxschafe0': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(86.135, -1.531, -14.741),
                    'Pos': Point3(-81.684, 148.93, 47.76),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192817792.0dxschafe': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-46.638, 12.945, 3.816),
                    'Pos': Point3(407.714, -94.369, 13.625),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_C'
                    }
                },
                '1192817792.0dxschafe0': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-33.237, 0.0, 0.0),
                    'Pos': Point3(417.244, -146.98, 2.124),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_B'
                    }
                },
                '1192817792.0dxschafe1': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, -9.134),
                    'Pos': Point3(366.981, -128.63, -0.894),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/prop_group_A'
                    }
                },
                '1192817792.0dxschafe10': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-73.363, -8.481, 0.0),
                    'Pos': Point3(410.439, -73.239, -3.094),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.4000000059604645, 0.4000000059604645,
                                  0.4000000059604645, 1.0),
                        'Model':
                        'models/props/prop_group_C'
                    }
                },
                '1192817792.0dxschafe11': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-7.912, 0.0, 0.0),
                    'Pos': Point3(331.904, -65.544, -1.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_B'
                    }
                },
                '1192817792.0dxschafe12': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(338.494, -23.933, -1.015),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/prop_group_A'
                    }
                },
                '1192817792.0dxschafe13': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(58.571, 0.0, -12.052),
                    'Pos': Point3(385.699, -94.582, -1.415),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_A'
                    }
                },
                '1192817792.0dxschafe14': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-82.128, -5.631, 2.219),
                    'Pos': Point3(350.269, -37.764, -1.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192817792.0dxschafe15': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(74.678, 6.048, 0.173),
                    'Pos': Point3(319.246, -40.343, -0.157),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192817792.0dxschafe16': {
                    'Type': 'Crate',
                    'DisableCollision': False,
                    'Hpr': VBase3(-8.954, 0.0, 0.0),
                    'Pos': Point3(309.526, -52.469, 2.016),
                    'Scale': VBase3(1.229, 1.229, 1.229),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/crate'
                    }
                },
                '1192817792.0dxschafe17': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(179.514, 0.0, 0.0),
                    'Pos': Point3(313.934, -25.743, -1.322),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_H'
                    }
                },
                '1192817792.0dxschafe18': {
                    'Type': 'Crate',
                    'DisableCollision': False,
                    'Hpr': VBase3(17.281, 0.0, 0.0),
                    'Pos': Point3(336.936, -78.372, -2.336),
                    'Scale': VBase3(1.602, 1.602, 1.602),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/crate'
                    }
                },
                '1192817792.0dxschafe19': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(43.921, 5.114, 3.238),
                    'Pos': Point3(330.778, -82.588, -2.061),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192817792.0dxschafe2': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(58.571, 0.0, 0.0),
                    'Pos': Point3(389.279, -157.933, 1.959),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_A'
                    }
                },
                '1192817792.0dxschafe20': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(43.921, 5.114, 3.238),
                    'Pos': Point3(302.016, -41.969, 2.175),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192817792.0dxschafe3': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-56.52, -4.123, 4.433),
                    'Pos': Point3(373.308, -155.089, 1.527),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192817792.0dxschafe4': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(128.351, 21.756, -5.011),
                    'Pos': Point3(345.862, -148.343, -1.461),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192817792.0dxschafe5': {
                    'Type': 'Crate',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.594, -0.742, 4.002),
                    'Pos': Point3(335.199, -164.84, 1.993),
                    'Scale': VBase3(1.229, 1.229, 1.229),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1192817792.0dxschafe6': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(179.514, 6.931, 0.0),
                    'Pos': Point3(332.778, -131.012, -2.383),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_H'
                    }
                },
                '1192817792.0dxschafe7': {
                    'Type': 'Crate',
                    'DisableCollision': False,
                    'Hpr': VBase3(17.281, 0.0, 0.0),
                    'Pos': Point3(371.781, -191.117, 1.685),
                    'Scale': VBase3(1.602, 1.602, 1.602),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/crate'
                    }
                },
                '1192817792.0dxschafe8': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(43.921, 5.114, 3.238),
                    'Pos': Point3(365.622, -195.332, 1.96),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192817792.0dxschafe9': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(43.921, 5.114, 3.238),
                    'Pos': Point3(324.714, -146.688, -1.826),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.4399999976158142,
                                  0.3700000047683716, 1.0),
                        'Model':
                        'models/props/barrel_sideways'
                    }
                },
                '1192818176.0dxschafe': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(111.584, 23.724, -15.188),
                    'Pos': Point3(292.467, -84.323, 7.358),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.4000000059604645, 0.4000000059604645,
                                  0.4000000059604645, 1.0),
                        'Model':
                        'models/props/prop_group_B'
                    }
                },
                '1192818816.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-9.857, -154.615, 30.705),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192818944.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(82.906, -73.698, 26.715),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192818944.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(3.123, -95.542, 30.269),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192818944.0dxschafe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(88.711, -236.69, 26.471),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819072.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-412.793, 201.143, 78.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819072.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-462.756, 117.504, 78.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819072.0dxschafe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-279.128, -100.922, 55.796),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819072.0dxschafe2': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-336.468, 6.872, 55.796),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819200.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-283.645, 88.154, 65.507),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819200.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-420.52, 95.772, 78.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819328.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '35',
                    'Pos': Point3(-309.434, -59.117, 55.797),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819328.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '41',
                    'Pos': Point3(-247.211, -32.431, 55.797),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819328.0dxschafe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(138.753, 0.0, 0.0),
                    'Pos': Point3(-317.489, -63.175, 55.602),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1192819328.0dxschafe2': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-242.943, -36.379, 55.796),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1192819456.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-310.976, 13.645, 55.946),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.8700000047683716, 1.0, 1.0, 1.0),
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1192819456.0dxschafe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-196.691, 3.047, 56.929),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1192819584.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '35',
                    'Pos': Point3(-35.162, -41.002, 31.97),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819584.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '35',
                    'Pos': Point3(46.561, -29.68, 28.331),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819584.0dxschafe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(138.753, 0.0, 0.0),
                    'Pos': Point3(41.535, -34.718, 28.554),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1192819584.0dxschafe2': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-83.906, 0.0, 0.0),
                    'Pos': Point3(-32.41, -47.367, 31.847),
                    'Scale': VBase3(1.225, 1.225, 1.225),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1192819584.0dxschafe3': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '35',
                    'Pos': Point3(-15.987, 131.212, 31.101),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819584.0dxschafe4': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '35',
                    'Pos': Point3(-108.507, 146.684, 35.218),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819584.0dxschafe5': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-83.906, 0.0, 0.0),
                    'Pos': Point3(-25.388, 78.599, 31.524),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1192819584.0dxschafe6': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(48.226, 0.0, 0.0),
                    'Pos': Point3(-17.96, 138.071, 31.352),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1192819712.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.24, 0.0, 0.0),
                    'Pos': Point3(-110.149, 153.712, 35.437),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1192819712.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_searching',
                    'Hpr': VBase3(-179.901, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '3.8614',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-135.157, 9.098, 54.045),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Fierce DJCrew',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819712.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_searching',
                    'Hpr': VBase3(-179.901, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '3.8614',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-199.045, -15.557, 58.514),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Fierce DJCrew',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819712.0dxschafe2': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_searching',
                    'Hpr': VBase3(-179.901, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '3.8614',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(341.953, -45.204, -1.064),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Fierce DJCrew',
                    'Start State': 'Patrol',
                    'Team': 'default',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819712.0dxschafe3': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(29.643, 0.0, 0.0),
                    'Pos': Point3(70.617, -15.281, 27.258),
                    'Scale': VBase3(0.833, 0.833, 0.833),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1192819712.0dxschafe4': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(96.241, 0.0, 0.0),
                    'Pos': Point3(29.822, -1.068, 29.073),
                    'Scale': VBase3(1.228, 1.228, 1.228),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1192819840.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '35',
                    'Pos': Point3(-9.283, -121.404, 30.823),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819840.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '35',
                    'Pos': Point3(61.794, -76.926, 27.654),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819840.0dxschafe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(29.643, 0.0, 0.0),
                    'Pos': Point3(-3.526, -120.815, 30.568),
                    'Scale': VBase3(0.833, 0.833, 0.833),
                    'Visual': {
                        'Color': (0.699999988079071, 0.699999988079071,
                                  0.699999988079071, 1.0),
                        'Model':
                        'models/props/dirt_pile_cave'
                    }
                },
                '1192819840.0dxschafe2': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(29.643, 0.0, 0.0),
                    'Pos': Point3(70.683, -72.909, 27.181),
                    'Scale': VBase3(1.614, 1.614, 1.614),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1192819968.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(195.054, -151.663, 14.227),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192819968.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(178.376, -206.534, 17.531),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192820096.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(404.179, 126.706, 2.175),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192820096.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(348.369, 25.39, -1.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192820096.0dxschafe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(395.944, -68.625, -1.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192820096.0dxschafe2': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(338.615, -186.189, 2.175),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192820224.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(301.628, -107.158, 2.176),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192820224.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(281.288, -184.426, 2.175),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192820352.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(48.226, 0.0, 0.0),
                    'Pos': Point3(-80.351, 102.636, 33.364),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (1.0, 1.0, 1.0, 1.0),
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1192820352.0dxschafe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(48.226, 0.0, 0.0),
                    'Pos': Point3(-50.417, 157.403, 32.453),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (1.0, 1.0, 1.0, 1.0),
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1192820352.0dxschafe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(48.226, 0.0, 0.0),
                    'Pos': Point3(-65.795, 163.924, 33.315),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (1.0, 1.0, 1.0, 1.0),
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1192820352.0dxschafe2': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(48.226, 0.0, 0.0),
                    'Pos': Point3(-72.309, 23.636, 33.391),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1192820480.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(18.681, -0.121, 13.604),
                    'Pos': Point3(-134.202, 23.829, 52.554),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/dirt_pile_cave'
                    }
                },
                '1195602087.77akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(146.238, 0.0, 0.0),
                    'Pos': Point3(285.987, -245.467, 2.175),
                    'Scale': VBase3(1.287, 1.287, 1.287),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1195602113.89akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-96.085, 0.0, 0.0),
                    'Pos': Point3(385.785, -224.926, 2.175),
                    'Scale': VBase3(1.555, 1.555, 1.555),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1195602149.33akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-153.454, 0.0, 0.0),
                    'Pos': Point3(500.632, -131.3, 2.175),
                    'Scale': VBase3(1.243, 1.243, 1.243),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1195602172.25akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-25.374, 0.0, 0.0),
                    'Pos': Point3(444.825, 128.89, 2.175),
                    'Scale': VBase3(1.442, 1.442, 1.442),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1195602201.94akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(164.528, 0.0, 0.0),
                    'Pos': Point3(298.604, -36.245, 2.175),
                    'Scale': VBase3(2.139, 2.139, 2.139),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1197593150.11akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-53.609, 0.0, 0.0),
                    'Pos': Point3(272.849, -87.868, 2.176),
                    'Scale': VBase3(3.624, 1.259, 1.259),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1197593235.17akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-5.799, 0.0, 0.0),
                    'Pos': Point3(290.334, -103.156, -0.588),
                    'Scale': VBase3(1.487, 1.0, 1.855),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1200009030.83akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(37.349, 0.0, 0.0),
                    'Pos': Point3(322.278, -88.593, -2.088),
                    'Scale': VBase3(2.135, 1.0, 1.914),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1200009238.81akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(28.661, 0.0, 0.0),
                    'Pos': Point3(305.828, -99.403, -0.139),
                    'Scale': VBase3(1.914, 1.0, 1.855),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1200009534.81akelts': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': True,
                    'Hpr': VBase3(34.57, 0.0, 0.0),
                    'Pos': Point3(274.168, -72.003, 2.175),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_B'
                    }
                },
                '1200009582.88akelts': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': True,
                    'Hpr': VBase3(131.696, 0.0, 0.0),
                    'Pos': Point3(281.454, -89.594, 2.175),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_F'
                    }
                },
                '1201813673.48akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-83.43, 0.0, 0.0),
                    'Pos': Point3(329.927, -77.423, -2.063),
                    'Scale': VBase3(1.0, 1.0, 1.241),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1201813751.39akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-52.938, 0.0, 0.0),
                    'Pos': Point3(316.016, -49.433, -1.262),
                    'Scale': VBase3(2.695, 1.0, 2.763),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1201813816.86akelts': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-159.652, 0.0, 0.0),
                    'Pos': Point3(292.131, -48.073, 2.175),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/props/prop_group_C'
                    }
                },
                '1205874059.53kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-172.423, 0.0, 0.0),
                    'Pos': Point3(18.79, 102.378, 28.165),
                    'Scale': VBase3(3.969, 1.781, 2.721),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                }
            },
            'Visual': {
                'Model': 'models/caves/cave_b_zero'
            }
        }
    },
    'Node Links':
    [['1192818816.0dxschafe', '1179861836.94Aholdun', 'Bi-directional'],
     ['1192818816.0dxschafe', '1192818944.0dxschafe', 'Bi-directional'],
     ['1192818944.0dxschafe', '1179861836.94Aholdun', 'Bi-directional'],
     ['1192818944.0dxschafe1', '1192818944.0dxschafe0', 'Bi-directional'],
     ['1192818944.0dxschafe0', '1179861984.82Aholdun', 'Bi-directional'],
     ['1192818944.0dxschafe1', '1179861984.82Aholdun', 'Bi-directional'],
     ['1179946254.11Aholdun', '1192819072.0dxschafe', 'Bi-directional'],
     ['1192819072.0dxschafe', '1192819072.0dxschafe0', 'Bi-directional'],
     ['1179946254.11Aholdun', '1192819072.0dxschafe0', 'Bi-directional'],
     ['1192819072.0dxschafe2', '1192819072.0dxschafe1', 'Bi-directional'],
     ['1179861898.15Aholdun', '1192819072.0dxschafe1', 'Bi-directional'],
     ['1179861898.15Aholdun', '1192819072.0dxschafe2', 'Bi-directional'],
     ['1189459903.72kmuller', '1192819200.0dxschafe0', 'Bi-directional'],
     ['1192819200.0dxschafe0', '1192819200.0dxschafe', 'Bi-directional'],
     ['1189459903.72kmuller', '1192819200.0dxschafe', 'Bi-directional'],
     ['1179946104.72Aholdun', '1192819328.0dxschafe', 'Bi-directional'],
     ['1192819328.0dxschafe0', '1192819328.0dxschafe', 'Bi-directional'],
     ['1192819328.0dxschafe0', '1179946104.72Aholdun', 'Bi-directional'],
     ['1179946309.78Aholdun', '1192819584.0dxschafe0', 'Bi-directional'],
     ['1192819584.0dxschafe', '1192819584.0dxschafe0', 'Bi-directional'],
     ['1192819584.0dxschafe', '1179946309.78Aholdun', 'Bi-directional'],
     ['1192497024.0dxschafe', '1192819584.0dxschafe4', 'Bi-directional'],
     ['1192497024.0dxschafe', '1192819584.0dxschafe3', 'Bi-directional'],
     ['1192819840.0dxschafe0', '1192819840.0dxschafe', 'Bi-directional'],
     ['1179946209.01Aholdun', '1192819840.0dxschafe', 'Bi-directional'],
     ['1179946209.01Aholdun', '1192819840.0dxschafe0', 'Bi-directional'],
     ['1192819968.0dxschafe0', '1192819968.0dxschafe', 'Bi-directional'],
     ['1192819968.0dxschafe0', '1179862042.35Aholdun', 'Bi-directional'],
     ['1192819968.0dxschafe', '1179862042.35Aholdun', 'Bi-directional'],
     ['1189460022.72kmuller', '1192820096.0dxschafe0', 'Bi-directional'],
     ['1192820096.0dxschafe', '1189460022.72kmuller', 'Bi-directional'],
     ['1192820096.0dxschafe', '1192820096.0dxschafe0', 'Bi-directional'],
     ['1192820096.0dxschafe2', '1192819712.0dxschafe2', 'Bi-directional'],
     ['1192820096.0dxschafe2', '1192820096.0dxschafe1', 'Bi-directional'],
     ['1192819712.0dxschafe2', '1192820096.0dxschafe1', 'Bi-directional'],
     ['1192820224.0dxschafe0', '1192820224.0dxschafe', 'Bi-directional'],
     ['1179946425.84Aholdun', '1192820224.0dxschafe', 'Bi-directional'],
     ['1179946425.84Aholdun', '1192820224.0dxschafe0', 'Bi-directional']],
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
        '1172208344.92sdnaik':
        '["Objects"]["1172208344.92sdnaik"]',
        '1172208565.59sdnaik':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1172208565.59sdnaik"]',
        '1172208565.61sdnaik':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1172208565.61sdnaik"]',
        '1178829600.66kmuller':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1178829600.66kmuller"]',
        '1178829636.06kmuller':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1178829636.06kmuller"]',
        '1179861836.94Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179861836.94Aholdun"]',
        '1179861898.15Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179861898.15Aholdun"]',
        '1179861984.82Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179861984.82Aholdun"]',
        '1179862042.35Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179862042.35Aholdun"]',
        '1179946104.72Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946104.72Aholdun"]',
        '1179946138.7Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946138.7Aholdun"]',
        '1179946169.66Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946169.66Aholdun"]',
        '1179946209.01Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946209.01Aholdun"]',
        '1179946254.11Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946254.11Aholdun"]',
        '1179946309.78Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946309.78Aholdun"]',
        '1179946339.7Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946339.7Aholdun"]',
        '1179946425.84Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946425.84Aholdun"]',
        '1179946450.75Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946450.75Aholdun"]',
        '1179946516.51Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946516.51Aholdun"]',
        '1179946525.14Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946525.14Aholdun"]',
        '1179946536.17Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946536.17Aholdun"]',
        '1179946544.58Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946544.58Aholdun"]',
        '1179946559.31Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946559.31Aholdun"]',
        '1179946567.39Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946567.39Aholdun"]',
        '1179946574.14Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946574.14Aholdun"]',
        '1179946583.05Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946583.05Aholdun"]',
        '1179946592.47Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946592.47Aholdun"]',
        '1179946606.01Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946606.01Aholdun"]',
        '1179946619.58Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946619.58Aholdun"]',
        '1179946626.42Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946626.42Aholdun"]',
        '1179946645.89Aholdun':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1179946645.89Aholdun"]',
        '1186714240.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1186714240.0dxschafe0"]',
        '1189459263.3kmuller':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1189459263.3kmuller"]',
        '1189459407.59kmuller':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1189459407.59kmuller"]',
        '1189459652.73kmuller':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1189459652.73kmuller"]',
        '1189459701.39kmuller':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1189459701.39kmuller"]',
        '1189459734.55kmuller':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1189459734.55kmuller"]',
        '1189459903.72kmuller':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1189459903.72kmuller"]',
        '1189460022.72kmuller':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1189460022.72kmuller"]',
        '1189460063.77kmuller':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1189460063.77kmuller"]',
        '1189643438.33kmuller':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1189643438.33kmuller"]',
        '1189643543.84kmuller':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1189643543.84kmuller"]',
        '1189643569.14kmuller':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1189643569.14kmuller"]',
        '1192494720.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192494720.0dxschafe"]',
        '1192494848.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192494848.0dxschafe"]',
        '1192495104.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192495104.0dxschafe"]',
        '1192495232.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192495232.0dxschafe"]',
        '1192495744.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192495744.0dxschafe"]',
        '1192495744.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192495744.0dxschafe0"]',
        '1192495744.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192495744.0dxschafe1"]',
        '1192495872.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192495872.0dxschafe"]',
        '1192497024.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192497024.0dxschafe"]',
        '1192815360.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815360.0dxschafe"]',
        '1192815488.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815488.0dxschafe"]',
        '1192815488.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815488.0dxschafe0"]',
        '1192815488.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815488.0dxschafe1"]',
        '1192815488.0dxschafe10':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815488.0dxschafe10"]',
        '1192815488.0dxschafe11':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815488.0dxschafe11"]',
        '1192815488.0dxschafe12':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815488.0dxschafe12"]',
        '1192815488.0dxschafe2':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815488.0dxschafe2"]',
        '1192815488.0dxschafe3':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815488.0dxschafe3"]',
        '1192815488.0dxschafe4':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815488.0dxschafe4"]',
        '1192815488.0dxschafe5':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815488.0dxschafe5"]',
        '1192815488.0dxschafe6':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815488.0dxschafe6"]',
        '1192815488.0dxschafe7':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815488.0dxschafe7"]',
        '1192815488.0dxschafe8':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815488.0dxschafe8"]',
        '1192815488.0dxschafe9':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815488.0dxschafe9"]',
        '1192815616.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815616.0dxschafe"]',
        '1192815616.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815616.0dxschafe0"]',
        '1192815616.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815616.0dxschafe1"]',
        '1192815616.0dxschafe2':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815616.0dxschafe2"]',
        '1192815616.0dxschafe3':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815616.0dxschafe3"]',
        '1192815616.0dxschafe4':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815616.0dxschafe4"]',
        '1192815616.0dxschafe5':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815616.0dxschafe5"]',
        '1192815616.0dxschafe6':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815616.0dxschafe6"]',
        '1192815616.0dxschafe7':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815616.0dxschafe7"]',
        '1192815872.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192815872.0dxschafe"]',
        '1192816384.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816384.0dxschafe"]',
        '1192816384.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816384.0dxschafe0"]',
        '1192816384.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816384.0dxschafe1"]',
        '1192816384.0dxschafe2':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816384.0dxschafe2"]',
        '1192816512.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816512.0dxschafe"]',
        '1192816512.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816512.0dxschafe0"]',
        '1192816512.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816512.0dxschafe1"]',
        '1192816640.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816640.0dxschafe"]',
        '1192816640.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816640.0dxschafe0"]',
        '1192816768.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816768.0dxschafe"]',
        '1192816768.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816768.0dxschafe0"]',
        '1192816768.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816768.0dxschafe1"]',
        '1192816768.0dxschafe2':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816768.0dxschafe2"]',
        '1192816768.0dxschafe3':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816768.0dxschafe3"]',
        '1192816896.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816896.0dxschafe"]',
        '1192816896.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816896.0dxschafe0"]',
        '1192816896.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816896.0dxschafe1"]',
        '1192816896.0dxschafe2':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816896.0dxschafe2"]',
        '1192816896.0dxschafe3':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816896.0dxschafe3"]',
        '1192816896.0dxschafe4':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816896.0dxschafe4"]',
        '1192816896.0dxschafe5':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816896.0dxschafe5"]',
        '1192816896.0dxschafe6':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816896.0dxschafe6"]',
        '1192816896.0dxschafe7':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816896.0dxschafe7"]',
        '1192816896.0dxschafe8':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192816896.0dxschafe8"]',
        '1192817024.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817024.0dxschafe"]',
        '1192817024.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817024.0dxschafe0"]',
        '1192817024.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817024.0dxschafe1"]',
        '1192817152.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817152.0dxschafe"]',
        '1192817152.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817152.0dxschafe0"]',
        '1192817152.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817152.0dxschafe1"]',
        '1192817152.0dxschafe2':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817152.0dxschafe2"]',
        '1192817280.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817280.0dxschafe"]',
        '1192817280.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817280.0dxschafe0"]',
        '1192817280.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817280.0dxschafe1"]',
        '1192817408.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817408.0dxschafe"]',
        '1192817408.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817408.0dxschafe0"]',
        '1192817536.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817536.0dxschafe"]',
        '1192817536.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817536.0dxschafe0"]',
        '1192817792.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe"]',
        '1192817792.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe0"]',
        '1192817792.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe1"]',
        '1192817792.0dxschafe10':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe10"]',
        '1192817792.0dxschafe11':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe11"]',
        '1192817792.0dxschafe12':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe12"]',
        '1192817792.0dxschafe13':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe13"]',
        '1192817792.0dxschafe14':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe14"]',
        '1192817792.0dxschafe15':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe15"]',
        '1192817792.0dxschafe16':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe16"]',
        '1192817792.0dxschafe17':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe17"]',
        '1192817792.0dxschafe18':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe18"]',
        '1192817792.0dxschafe19':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe19"]',
        '1192817792.0dxschafe2':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe2"]',
        '1192817792.0dxschafe20':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe20"]',
        '1192817792.0dxschafe3':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe3"]',
        '1192817792.0dxschafe4':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe4"]',
        '1192817792.0dxschafe5':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe5"]',
        '1192817792.0dxschafe6':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe6"]',
        '1192817792.0dxschafe7':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe7"]',
        '1192817792.0dxschafe8':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe8"]',
        '1192817792.0dxschafe9':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192817792.0dxschafe9"]',
        '1192818176.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192818176.0dxschafe"]',
        '1192818816.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192818816.0dxschafe"]',
        '1192818944.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192818944.0dxschafe"]',
        '1192818944.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192818944.0dxschafe0"]',
        '1192818944.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192818944.0dxschafe1"]',
        '1192819072.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819072.0dxschafe"]',
        '1192819072.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819072.0dxschafe0"]',
        '1192819072.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819072.0dxschafe1"]',
        '1192819072.0dxschafe2':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819072.0dxschafe2"]',
        '1192819200.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819200.0dxschafe"]',
        '1192819200.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819200.0dxschafe0"]',
        '1192819328.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819328.0dxschafe"]',
        '1192819328.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819328.0dxschafe0"]',
        '1192819328.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819328.0dxschafe1"]',
        '1192819328.0dxschafe2':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819328.0dxschafe2"]',
        '1192819456.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819456.0dxschafe"]',
        '1192819456.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819456.0dxschafe0"]',
        '1192819584.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819584.0dxschafe"]',
        '1192819584.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819584.0dxschafe0"]',
        '1192819584.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819584.0dxschafe1"]',
        '1192819584.0dxschafe2':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819584.0dxschafe2"]',
        '1192819584.0dxschafe3':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819584.0dxschafe3"]',
        '1192819584.0dxschafe4':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819584.0dxschafe4"]',
        '1192819584.0dxschafe5':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819584.0dxschafe5"]',
        '1192819584.0dxschafe6':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819584.0dxschafe6"]',
        '1192819712.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819712.0dxschafe"]',
        '1192819712.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819712.0dxschafe0"]',
        '1192819712.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819712.0dxschafe1"]',
        '1192819712.0dxschafe2':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819712.0dxschafe2"]',
        '1192819712.0dxschafe3':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819712.0dxschafe3"]',
        '1192819712.0dxschafe4':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819712.0dxschafe4"]',
        '1192819840.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819840.0dxschafe"]',
        '1192819840.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819840.0dxschafe0"]',
        '1192819840.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819840.0dxschafe1"]',
        '1192819840.0dxschafe2':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819840.0dxschafe2"]',
        '1192819968.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819968.0dxschafe"]',
        '1192819968.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192819968.0dxschafe0"]',
        '1192820096.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192820096.0dxschafe"]',
        '1192820096.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192820096.0dxschafe0"]',
        '1192820096.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192820096.0dxschafe1"]',
        '1192820096.0dxschafe2':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192820096.0dxschafe2"]',
        '1192820224.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192820224.0dxschafe"]',
        '1192820224.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192820224.0dxschafe0"]',
        '1192820352.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192820352.0dxschafe"]',
        '1192820352.0dxschafe0':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192820352.0dxschafe0"]',
        '1192820352.0dxschafe1':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192820352.0dxschafe1"]',
        '1192820352.0dxschafe2':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192820352.0dxschafe2"]',
        '1192820480.0dxschafe':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1192820480.0dxschafe"]',
        '1195602087.77akelts':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1195602087.77akelts"]',
        '1195602113.89akelts':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1195602113.89akelts"]',
        '1195602149.33akelts':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1195602149.33akelts"]',
        '1195602172.25akelts':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1195602172.25akelts"]',
        '1195602201.94akelts':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1195602201.94akelts"]',
        '1197593150.11akelts':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1197593150.11akelts"]',
        '1197593235.17akelts':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1197593235.17akelts"]',
        '1200009030.83akelts':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1200009030.83akelts"]',
        '1200009238.81akelts':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1200009238.81akelts"]',
        '1200009534.81akelts':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1200009534.81akelts"]',
        '1200009582.88akelts':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1200009582.88akelts"]',
        '1201813673.48akelts':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1201813673.48akelts"]',
        '1201813751.39akelts':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1201813751.39akelts"]',
        '1201813816.86akelts':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1201813816.86akelts"]',
        '1205874059.53kmuller':
        '["Objects"]["1172208344.92sdnaik"]["Objects"]["1205874059.53kmuller"]'
    }
}
extraInfo = {
    'camPos': Point3(-43.7998, 150.256, 191.937),
    'camHpr': VBase3(-134.922, -56.3315, 1.23203e-05),
    'focalLength': 1.39999997616
}
