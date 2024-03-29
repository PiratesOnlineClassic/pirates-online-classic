# Embedded file name: pirates.leveleditor.worldData.tortuga_area_swamp_c_1
from pandac.PandaModules import Point3, VBase3, Vec4
objectStruct = {
    'AmbientColors': {
        0: Vec4(0.207843, 0.243137, 0.447059, 1),
        2: Vec4(0.666667, 0.721569, 0.792157, 1),
        4: Vec4(0.721569, 0.611765, 0.619608, 1),
        6: Vec4(0.207843, 0.243137, 0.447059, 1),
        8: Vec4(0.384314, 0.419608, 0.564706, 1)
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
    [['1177021184.0dxschafe', '1172635262.83sdnaik', 'Bi-directional'],
     ['1177021312.0dxschafe', '1174698240.0dxschafe', 'Bi-directional'],
     ['1174698368.0dxschafe', '1177022208.0dxschafe', 'Bi-directional'],
     ['1178932046.6Aholdun', '1177019776.0dxschafe', 'Bi-directional']],
    'Objects': {
        '1169179552.88sdnaik': {
            'Type': 'Island Game Area',
            'Name': 'tortuga_area_swamp_c_1',
            'File': '',
            'AdditionalData': ['SwampTemplateC'],
            'Instanced': True,
            'Objects': {
                '1169179824.05sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_2',
                    'Hpr': VBase3(135.469, 0.0, 0.0),
                    'Pos': Point3(557.708, 254.891, 12.365),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1172635262.83sdnaik': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '1.5152',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-26.089, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-153.977, 95.511, 1.212),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'FlyTrap',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1172635301.08sdnaik': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '8.7831',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-230.988, 207.76, 3.792),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Rock Crab',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1172635315.69sdnaik': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-188.439, 183.603, -0.631),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Big Gator',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1172635343.66sdnaik': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-229.324, 236.333, 0.082),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Team': '1',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1174697600.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '6.0241',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-130.206, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '5.8072',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(451.398, 342.89, 2.808),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Rock Crab',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1174697984.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '13.5542',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-125.436, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '2.7169',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-384.489, 228.911, 2.068),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Crab',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1174697984.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '4.8193',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-162.221, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '5.4639',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-379.715, 241.428, 3.504),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Rock Crab',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1174698112.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-169.427, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(116.172, 161.318, -1.349),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Big Gator',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1174698240.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(182.162, 100.369, 3.047),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Giant Crab',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1174698368.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(120.808, 9.164, -0.234),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Huge Gator',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1174698624.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-45.999, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(351.979, 226.381, -0.533),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1177017472.0dxschafe': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1177017472.0dxschafe0',
                    'Hpr': VBase3(117.501, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(-251.263, 211.356, -0.483),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Color': (0.56, 0.82, 1.0, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/shanty_npc_house_combo_D',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1177017600.0dxschafe': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1177017600.0dxschafe0',
                    'Hpr': VBase3(0.913, 0.0, 0.0),
                    'Objects': {
                        '1219428691.07mtucker': {
                            'Type': 'Door Locator Node',
                            'Name': 'door_locator',
                            'Hpr': VBase3(-180.0, 0.0, 0.0),
                            'Pos': Point3(0.313, -4.016, 1.444),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(10.454, 224.167, 13.962),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Color': (0.56, 0.82, 0.84, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/shanty_npc_house_combo_J',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1177017728.0dxschafe': {
                    'Type': 'Searchable Container',
                    'Aggro Radius': 5.0,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(26.894, 230.022, 13.72),
                    'Scale': VBase3(0.834, 0.834, 0.834),
                    'Visual': {
                        'Color': (0.5, 0.7, 1.0, 1.0),
                        'Model': 'models/props/barrel'
                    },
                    'searchTime': '10.0',
                    'type': 'Barrel'
                },
                '1177018112.0dxschafe0': {
                    'Type': 'Crate',
                    'DisableCollision': False,
                    'Hpr': VBase3(122.096, 3.053, -2.342),
                    'Pos': Point3(87.827, 216.328, 4.029),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.44, 0.59, 0.66, 1.0),
                        'Model': 'models/props/crates_group_1'
                    }
                },
                '1177018240.0dxschafe': {
                    'Type': 'Furniture',
                    'DisableCollision': False,
                    'Hpr': VBase3(78.134, 0.577, -1.185),
                    'Pos': Point3(75.046, 208.581, 3.34),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.41, 0.65, 0.71, 1.0),
                        'Model': 'models/props/table_shanty_2'
                    }
                },
                '1177018240.0dxschafe0': {
                    'Type': 'Furniture',
                    'DisableCollision': False,
                    'Hpr': VBase3(73.099, 0.679, -1.13),
                    'Pos': Point3(70.562, 210.462, 3.553),
                    'Scale': VBase3(1.129, 1.129, 1.129),
                    'Visual': {
                        'Color': (0.41, 0.66, 0.67, 1.0),
                        'Model': 'models/props/stool_shanty'
                    }
                },
                '1177018240.0dxschafe1': {
                    'Type': 'Furniture',
                    'DisableCollision': False,
                    'Hpr': VBase3(39.46, 4.297, -2.121),
                    'Pos': Point3(96.77, 214.266, 3.571),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.41, 0.66, 0.7, 1.0),
                        'Model': 'models/props/table_shanty_2'
                    }
                },
                '1177018368.0dxschafe': {
                    'Type': 'Furniture',
                    'DisableCollision': False,
                    'Hpr': VBase3(-23.66, 3.392, -28.93),
                    'Pos': Point3(62.134, 214.338, 4.821),
                    'Scale': VBase3(1.129, 1.129, 1.129),
                    'Visual': {
                        'Color': (0.41, 0.66, 0.67, 1.0),
                        'Model': 'models/props/chair_shanty'
                    }
                },
                '1177018368.0dxschafe0': {
                    'Type': 'Furniture',
                    'DisableCollision': False,
                    'Hpr': VBase3(14.873, 3.267, 0.071),
                    'Pos': Point3(80.702, 209.236, 3.388),
                    'Scale': VBase3(1.129, 1.129, 1.129),
                    'Visual': {
                        'Color': (0.41, 0.66, 0.67, 1.0),
                        'Model': 'models/props/chair_shanty'
                    }
                },
                '1177018368.0dxschafe1': {
                    'Type': 'Furniture',
                    'DisableCollision': False,
                    'Hpr': VBase3(35.651, 1.226, -0.484),
                    'Pos': Point3(76.49, 204.391, 2.951),
                    'Scale': VBase3(1.129, 1.129, 1.129),
                    'Visual': {
                        'Color': (0.41, 0.66, 0.67, 1.0),
                        'Model': 'models/props/stool_shanty'
                    }
                },
                '1177018624.0dxschafe': {
                    'Type': 'Jugs_and_Jars',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(72.455, 208.619, 6.286),
                    'Scale': VBase3(1.407, 1.407, 1.407),
                    'Visual': {
                        'Model': 'models/props/winebottle_B'
                    }
                },
                '1177018624.0dxschafe0': {
                    'Type': 'Jugs_and_Jars',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(85.771, 215.596, 7.194),
                    'Scale': VBase3(1.407, 1.407, 1.407),
                    'Visual': {
                        'Model': 'models/props/waterpitcher'
                    }
                },
                '1177018624.0dxschafe1': {
                    'Type': 'Jugs_and_Jars',
                    'Hpr': VBase3(0.0, 0.0, 5.299),
                    'Pos': Point3(64.118, 216.061, 4.847),
                    'Scale': VBase3(1.407, 1.407, 1.407),
                    'Visual': {
                        'Color': (0.4, 0.93, 0.57, 1.0),
                        'Model': 'models/props/bottle_brown'
                    }
                },
                '1177018880.0dxschafe': {
                    'Type': 'Pots',
                    'Hpr': VBase3(37.896, 4.177, -1.422),
                    'Pos': Point3(-3.376, 219.111, 14.159),
                    'Scale': VBase3(0.985, 0.985, 0.985),
                    'Visual': {
                        'Color': (0.69, 0.71, 1.0, 1.0),
                        'Model': 'models/props/pot_B'
                    }
                },
                '1177019008.0dxschafe': {
                    'Type': 'Jugs_and_Jars',
                    'Hpr': VBase3(0.0, 0.0, 25.966),
                    'Pos': Point3(-8.263, 220.826, 13.509),
                    'Scale': VBase3(2.628, 2.628, 2.628),
                    'Visual': {
                        'Color': (0.68, 1.0, 1.0, 1.0),
                        'Model': 'models/props/jar'
                    }
                },
                '1177019136.0dxschafe': {
                    'Type': 'Swamp_props_small',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(17.432, 218.161, 13.661),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/swamp_bench'
                    }
                },
                '1177019264.0dxschafe': {
                    'Type': 'Swamp_props_small',
                    'DisableCollision': False,
                    'Hpr': VBase3(1.8, 0.0, 0.0),
                    'Pos': Point3(5.868, 217.102, 13.793),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/swamp_chair'
                    }
                },
                '1177019264.0dxschafe0': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(25.207, 0.0, 0.0),
                    'Pos': Point3(-29.595, 200.54, 9.884),
                    'Scale': VBase3(0.77, 0.77, 0.77),
                    'Visual': {
                        'Color': (0.4, 0.66, 1.0, 1.0),
                        'Model': 'models/props/barrel_group_3'
                    }
                },
                '1177019776.0dxschafe': {
                    'Type': 'Searchable Container',
                    'Aggro Radius': '5.0000',
                    'Hpr': VBase3(-36.929, 0.0, 0.0),
                    'Pos': Point3(-288.923, 294.396, 11.066),
                    'Scale': VBase3(1.606, 1.606, 1.606),
                    'Visual': {
                        'Color': (0.7, 1.0, 1.0, 1.0),
                        'Model': 'models/props/crate_04'
                    },
                    'searchTime': '10.0',
                    'type': 'Crate'
                },
                '1177019904.0dxschafe1': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-58.379, 0.0, 0.0),
                    'Pos': Point3(-270.355, 213.557, 15.024),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.52, 1.0, 1.0, 1.0),
                        'Model': 'models/props/barrel_group_3'
                    }
                },
                '1177020032.0dxschafe': {
                    'Type': 'Baskets',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-239.019, 205.845, 14.995),
                    'Scale': VBase3(1.432, 1.432, 1.432),
                    'Visual': {
                        'Color': (0.78, 1.0, 1.0, 1.0),
                        'Model': 'models/props/crab_pot'
                    }
                },
                '1177020032.0dxschafe1': {
                    'Type': 'Baskets',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-240.877, 200.719, 15.011),
                    'Scale': VBase3(3.916, 3.916, 3.916),
                    'Visual': {
                        'Color': (0.7, 1.0, 1.0, 1.0),
                        'Model': 'models/props/crab_pot'
                    }
                },
                '1177020160.0dxschafe': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1177020160.0dxschafe0',
                    'Hpr': VBase3(145.559, 0.0, 0.0),
                    'Objects': {
                        '1219428691.87mtucker': {
                            'Type': 'Door Locator Node',
                            'Name': 'door_locator',
                            'Hpr': VBase3(-180.0, 0.0, 0.0),
                            'Pos': Point3(0.161, -4.399, 16.391),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(129.519, -23.344, -5.899),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Color': (0.59, 1.0, 1.0, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/shanty_npc_house_combo_E',
                        'SignFrame': '',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1177020416.0dxschafe': {
                    'Type': 'Swamp_props_small',
                    'DisableCollision': False,
                    'Hpr': VBase3(92.414, -1.868, 7.592),
                    'Pos': Point3(-249.132, 227.421, 0.517),
                    'Scale': VBase3(0.608, 0.608, 0.608),
                    'Visual': {
                        'Model': 'models/props/swamp_boat'
                    }
                },
                '1177020544.0dxschafe': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1177020544.0dxschafe0',
                    'Hpr': VBase3(98.83, -0.264, 0.95),
                    'Objects': {
                        '1219428690.76mtucker': {
                            'Type': 'Door Locator Node',
                            'Name': 'door_locator',
                            'Hpr': VBase3(-180.0, 0.0, 0.0),
                            'Pos': Point3(0.162, -4.354, 0.599),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-311.149, 253.852, 13.356),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Color': (0.66, 1.0, 1.0, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/shanty_npc_house_combo_G',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1177020928.0dxschafe': {
                    'Type': 'Sack',
                    'DisableCollision': False,
                    'Hpr': VBase3(-28.82, 0.0, 0.0),
                    'Pos': Point3(-292.866, 290.222, 11.275),
                    'Scale': VBase3(4.481, 4.481, 4.481),
                    'Visual': {
                        'Color': (0.73, 1.0, 1.0, 1.0),
                        'Model': 'models/props/package_sack'
                    }
                },
                '1177020928.0dxschafe0': {
                    'Type': 'Crate',
                    'DisableCollision': False,
                    'Hpr': VBase3(-83.106, 0.0, 0.0),
                    'Pos': Point3(-279.334, 295.732, 11.146),
                    'Scale': VBase3(1.718, 1.718, 1.718),
                    'Visual': {
                        'Color': (0.58, 0.69, 0.68, 1.0),
                        'Model': 'models/props/crate_net'
                    }
                },
                '1177021184.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-142.93, 114.664, 2.92),
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
                '1177021312.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': VBase3(8.087, 0.0, 0.0),
                    'Pos': Point3(167.218, 94.702, 3.46),
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
                '1177022208.0dxschafe': {
                    'Type': 'Searchable Container',
                    'Aggro Radius': 5.0,
                    'Hpr': VBase3(49.643, -38.129, 35.504),
                    'Pos': Point3(147.003, -33.281, -2.087),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.48, 1.0, 1.0, 1.0),
                        'Model': 'models/props/barrel'
                    },
                    'searchTime': '10.0',
                    'type': 'Barrel'
                },
                '1177022464.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'tatoo',
                    'Hpr': VBase3(82.894, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(288.395, 111.651, -2.351),
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
                '1177022464.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'coin_flip_old',
                    'Hpr': VBase3(163.133, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(318.714, 140.418, -2.351),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mean Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1177022464.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'tatoo',
                    'Hpr': VBase3(156.354, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(316.459, 136.395, -2.351),
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
                '1177022592.0dxschafe': {
                    'Type': 'Cemetary',
                    'DisableCollision': False,
                    'Hpr': VBase3(-166.776, 7.387, -3.907),
                    'Pos': Point3(303.6, 107.26, -0.846),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.23, 0.31, 0.32, 1.0),
                        'Model': 'models/props/crypt1'
                    }
                },
                '1177022592.0dxschafe0': {
                    'Type': 'Cemetary',
                    'DisableCollision': False,
                    'Hpr': VBase3(-129.109, -0.917, 5.989),
                    'Pos': Point3(318.212, 124.19, -0.473),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.23, 0.31, 0.32, 1.0),
                        'Model': 'models/props/crypt2'
                    }
                },
                '1177022720.0dxschafe': {
                    'Type': 'Cemetary',
                    'DisableCollision': False,
                    'Hpr': VBase3(-100.509, 0.0, 2.334),
                    'Pos': Point3(320.953, 140.415, 0.136),
                    'Scale': VBase3(0.843, 0.843, 0.843),
                    'Visual': {
                        'Color': (0.4000000059604645, 0.4000000059604645,
                                  0.4000000059604645, 1.0),
                        'Model':
                        'models/props/headstonesGroup1'
                    }
                },
                '1177022720.0dxschafe0': {
                    'Type': 'Cemetary',
                    'DisableCollision': False,
                    'Hpr': VBase3(175.642, 0.0, 6.384),
                    'Pos': Point3(288.189, 108.52, -0.237),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.4000000059604645, 0.4000000059604645,
                                  0.4000000059604645, 1.0),
                        'Model':
                        'models/props/headstonesGroup4'
                    }
                },
                '1177031680.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '8.3333',
                    'AnimSet': 'default',
                    'Hpr': VBase3(175.546, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '2.3333',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(67.463, 206.422, 3.395),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Carrion',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'VisSize': '',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178932046.6Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-294.907, 231.332, 11.256),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178933125.99Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(114.577, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(478.303, 308.228, -0.255),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178933169.54Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-68.173, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(413.95, 290.728, 8.219),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178933178.97Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(137.118, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(393.981, 229.341, 0.911),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178933275.85Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(124.719, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(321.201, 181.655, 0.215),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178933287.18Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-67.293, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(231.146, 117.355, -0.517),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178933303.32Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(16.25, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(92.655, 135.768, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178933320.47Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(94.105, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(90.09, 203.366, 8.115),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'VisSize': '',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178933349.1Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-44.207, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-109.058, 131.81, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178933396.94Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-60.885, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-383.523, 194.568, 0.521),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178933540.46Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-12.556, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-377.906, 144.118, 8.564),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178934334.96Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(19.183, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(160.298, -27.133, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178934392.12Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-111.886, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(264.683, 149.988, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178934512.15Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(366.601, 108.259, 0.229),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186519296.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '8.7349',
                    'AnimSet': 'default',
                    'Hpr': VBase3(125.981, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-154.148, 197.562, -2.194),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'FlyTrap',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186519296.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '3.0303',
                    'AnimSet': 'default',
                    'Hpr': VBase3(10.586, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-55.098, 142.82, -1.353),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1187145344.0dchiappe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'idleB',
                    'Hpr': VBase3(102.014, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(293.263, 112.951, -2.35),
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
                '1187145600.0dchiappe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_handdig',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(220.581, 108.349, -4.165),
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
                '1188587776.0dxschafe0': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_1',
                    'Hpr': VBase3(81.569, 0.0, 0.0),
                    'Pos': Point3(-383.486, 124.706, 9.45),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1190746487.03dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'gp_handdig',
                    'Hpr': VBase3(-175.655, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(472.494, 349.847, 1.917),
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
                '1190746626.47dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'gp_moaning',
                    'Hpr': VBase3(-40.651, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(420.919, 285.634, -2.367),
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
                '1190746895.41dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '13.2530',
                    'AnimSet': 'gp_searching',
                    'Hpr': VBase3(68.827, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '11.1867',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-344.268, 195.655, -2.194),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Early Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1191625984.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '3.0303',
                    'AnimSet': 'default',
                    'Hpr': VBase3(10.586, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(199.708, -29.35, -2.268),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'FlyTrap',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1191626112.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '3.0303',
                    'AnimSet': 'default',
                    'Hpr': VBase3(71.657, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(368.273, 45.618, -2.309),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'FlyTrap',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193356928.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '6.0241',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-130.206, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '5.8072',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(405.167, 321.919, -1.347),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Crab',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1195164400.84kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-293.585, 290.855, 13.091),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/misc/coll_sphere_barrier'
                    }
                },
                '1205785910.16kmuller': {
                    'Type': 'Door Locator Node',
                    'Name': 'door_locator',
                    'Hpr': VBase3(-34.441, 0.0, 0.0),
                    'Pos': Point3(131.874, -19.625, 10.492),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1205785912.94kmuller': {
                    'Type': 'Door Locator Node',
                    'Name': 'door_locator',
                    'Hpr': VBase3(-179.087, 0.0, 0.0),
                    'Pos': Point3(10.831, 220.157, 15.406),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1205785914.08kmuller': {
                    'Type': 'Door Locator Node',
                    'Name': 'door_locator',
                    'Hpr': VBase3(-81.17, 0.264, -0.95),
                    'Pos': Point3(-306.876, 254.689, 13.972),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1205785914.16kmuller': {
                    'Type': 'Door Locator Node',
                    'Name': 'door_locator',
                    'Hpr': VBase3(-180.0, 0.0, 0.0),
                    'Pos': Point3(0.161, -4.399, 16.391),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1205786740.47kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(126.235, 0.0, 0.0),
                    'Pos': Point3(189.741, -36.273, 0.0),
                    'Scale': VBase3(1.0, 1.0, 2.832),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1210614483.52akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(115.739, 0.0, 0.0),
                    'Pos': Point3(134.992, -41.021, 9.36),
                    'Scale': VBase3(0.357, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1210614527.64akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(170.759, 0.0, 0.0),
                    'Pos': Point3(111.864, -24.561, 9.518),
                    'Scale': VBase3(0.357, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1210618115.94akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(55.587, 0.0, 0.0),
                    'Pos': Point3(142.425, -35.127, 0.054),
                    'Scale': VBase3(2.563, 1.0, 1.491),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1210618152.66akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(145.618, 0.0, 0.0),
                    'Pos': Point3(144.112, -20.786, -0.048),
                    'Scale': VBase3(1.353, 1.0, 1.515),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1210618186.63akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(145.806, 0.0, 0.0),
                    'Pos': Point3(126.455, -8.132, -3.401),
                    'Scale': VBase3(1.495, 1.0, 1.968),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1210618218.27akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-124.371, 0.0, 0.0),
                    'Pos': Point3(113.983, -13.329, -3.391),
                    'Scale': VBase3(2.236, 1.0, 1.953),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1210618283.5akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(56.879, 0.0, 0.0),
                    'Pos': Point3(139.975, -15.109, -0.548),
                    'Scale': VBase3(0.503, 0.664, 1.006),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1210618339.03akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-121.576, 0.0, 0.0),
                    'Pos': Point3(133.366, -10.738, -1.192),
                    'Scale': VBase3(0.503, 0.664, 1.006),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1210618418.84akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(170.759, 0.0, 0.0),
                    'Pos': Point3(110.884, -16.358, -2.738),
                    'Scale': VBase3(0.357, 1.0, 1.801),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1220896448.28mtucker': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '7.2289',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-155.266, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '3.4036',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-29.376, 194.121, 10.164),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Carrion',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'VisSize': '',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1220896713.35mtucker': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '6.9277',
                    'AnimSet': 'default',
                    'Hpr': VBase3(166.613, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '3.4036',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(80.955, 198.563, 2.023),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Carrion',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'VisSize': '',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1220906480.53mtucker': {
                    'Type': 'Skeleton',
                    'Aggro Radius': '5.7229',
                    'AnimSet': 'default',
                    'AvId': 4,
                    'AvTrack': 0,
                    'Boss': True,
                    'Hpr': VBase3(-178.147, 0.0, 0.0),
                    'Patrol Radius': '2.4880',
                    'Pos': Point3(6.736, 210.86, 13.964),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'TrailFX': 'None',
                    'VisSize': ''
                }
            },
            'VisSize': '',
            'Visual': {
                'Model': 'models/swamps/swampC'
            }
        }
    },
    'Node Links':
    [['1172635343.66sdnaik', '1172635315.69sdnaik', 'Bi-directional']],
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
        '1169179552.88sdnaik':
        '["Objects"]["1169179552.88sdnaik"]',
        '1169179824.05sdnaik':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1169179824.05sdnaik"]',
        '1172635262.83sdnaik':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1172635262.83sdnaik"]',
        '1172635301.08sdnaik':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1172635301.08sdnaik"]',
        '1172635315.69sdnaik':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1172635315.69sdnaik"]',
        '1172635343.66sdnaik':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1172635343.66sdnaik"]',
        '1174697600.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1174697600.0dxschafe"]',
        '1174697984.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1174697984.0dxschafe"]',
        '1174697984.0dxschafe0':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1174697984.0dxschafe0"]',
        '1174698112.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1174698112.0dxschafe"]',
        '1174698240.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1174698240.0dxschafe"]',
        '1174698368.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1174698368.0dxschafe"]',
        '1174698624.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1174698624.0dxschafe"]',
        '1177017472.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177017472.0dxschafe"]',
        '1177017472.0dxschafe0':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177017472.0dxschafe"]',
        '1177017600.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177017600.0dxschafe"]',
        '1177017600.0dxschafe0':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177017600.0dxschafe"]',
        '1177017728.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177017728.0dxschafe"]',
        '1177018112.0dxschafe0':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177018112.0dxschafe0"]',
        '1177018240.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177018240.0dxschafe"]',
        '1177018240.0dxschafe0':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177018240.0dxschafe0"]',
        '1177018240.0dxschafe1':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177018240.0dxschafe1"]',
        '1177018368.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177018368.0dxschafe"]',
        '1177018368.0dxschafe0':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177018368.0dxschafe0"]',
        '1177018368.0dxschafe1':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177018368.0dxschafe1"]',
        '1177018624.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177018624.0dxschafe"]',
        '1177018624.0dxschafe0':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177018624.0dxschafe0"]',
        '1177018624.0dxschafe1':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177018624.0dxschafe1"]',
        '1177018880.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177018880.0dxschafe"]',
        '1177019008.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177019008.0dxschafe"]',
        '1177019136.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177019136.0dxschafe"]',
        '1177019264.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177019264.0dxschafe"]',
        '1177019264.0dxschafe0':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177019264.0dxschafe0"]',
        '1177019776.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177019776.0dxschafe"]',
        '1177019904.0dxschafe1':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177019904.0dxschafe1"]',
        '1177020032.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177020032.0dxschafe"]',
        '1177020032.0dxschafe1':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177020032.0dxschafe1"]',
        '1177020160.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177020160.0dxschafe"]',
        '1177020160.0dxschafe0':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177020160.0dxschafe"]',
        '1177020416.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177020416.0dxschafe"]',
        '1177020544.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177020544.0dxschafe"]',
        '1177020544.0dxschafe0':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177020544.0dxschafe"]',
        '1177020928.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177020928.0dxschafe"]',
        '1177020928.0dxschafe0':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177020928.0dxschafe0"]',
        '1177021184.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177021184.0dxschafe"]',
        '1177021312.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177021312.0dxschafe"]',
        '1177022208.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177022208.0dxschafe"]',
        '1177022464.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177022464.0dxschafe"]',
        '1177022464.0dxschafe0':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177022464.0dxschafe0"]',
        '1177022464.0dxschafe1':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177022464.0dxschafe1"]',
        '1177022592.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177022592.0dxschafe"]',
        '1177022592.0dxschafe0':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177022592.0dxschafe0"]',
        '1177022720.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177022720.0dxschafe"]',
        '1177022720.0dxschafe0':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177022720.0dxschafe0"]',
        '1177031680.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177031680.0dxschafe"]',
        '1178932046.6Aholdun':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1178932046.6Aholdun"]',
        '1178933125.99Aholdun':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1178933125.99Aholdun"]',
        '1178933169.54Aholdun':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1178933169.54Aholdun"]',
        '1178933178.97Aholdun':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1178933178.97Aholdun"]',
        '1178933275.85Aholdun':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1178933275.85Aholdun"]',
        '1178933287.18Aholdun':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1178933287.18Aholdun"]',
        '1178933303.32Aholdun':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1178933303.32Aholdun"]',
        '1178933320.47Aholdun':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1178933320.47Aholdun"]',
        '1178933349.1Aholdun':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1178933349.1Aholdun"]',
        '1178933396.94Aholdun':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1178933396.94Aholdun"]',
        '1178933540.46Aholdun':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1178933540.46Aholdun"]',
        '1178934334.96Aholdun':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1178934334.96Aholdun"]',
        '1178934392.12Aholdun':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1178934392.12Aholdun"]',
        '1178934512.15Aholdun':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1178934512.15Aholdun"]',
        '1186519296.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1186519296.0dxschafe"]',
        '1186519296.0dxschafe0':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1186519296.0dxschafe0"]',
        '1187145344.0dchiappe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1187145344.0dchiappe"]',
        '1187145600.0dchiappe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1187145600.0dchiappe"]',
        '1188587776.0dxschafe0':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1188587776.0dxschafe0"]',
        '1190746487.03dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1190746487.03dxschafe"]',
        '1190746626.47dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1190746626.47dxschafe"]',
        '1190746895.41dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1190746895.41dxschafe"]',
        '1191625984.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1191625984.0dxschafe"]',
        '1191626112.0dxschafe':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1191626112.0dxschafe"]',
        '1193356928.0dxschafe1':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1193356928.0dxschafe1"]',
        '1195164400.84kmuller':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1195164400.84kmuller"]',
        '1205785910.16kmuller':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1205785910.16kmuller"]',
        '1205785912.94kmuller':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1205785912.94kmuller"]',
        '1205785914.08kmuller':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1205785914.08kmuller"]',
        '1205785914.16kmuller':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1205785914.16kmuller"]',
        '1205786740.47kmuller':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1205786740.47kmuller"]',
        '1210614483.52akelts':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1210614483.52akelts"]',
        '1210614527.64akelts':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1210614527.64akelts"]',
        '1210618115.94akelts':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1210618115.94akelts"]',
        '1210618152.66akelts':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1210618152.66akelts"]',
        '1210618186.63akelts':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1210618186.63akelts"]',
        '1210618218.27akelts':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1210618218.27akelts"]',
        '1210618283.5akelts':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1210618283.5akelts"]',
        '1210618339.03akelts':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1210618339.03akelts"]',
        '1210618418.84akelts':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1210618418.84akelts"]',
        '1219428690.76mtucker':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177020544.0dxschafe"]["Objects"]["1219428690.76mtucker"]',
        '1219428691.07mtucker':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177017600.0dxschafe"]["Objects"]["1219428691.07mtucker"]',
        '1219428691.87mtucker':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1177020160.0dxschafe"]["Objects"]["1219428691.87mtucker"]',
        '1220896448.28mtucker':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1220896448.28mtucker"]',
        '1220896713.35mtucker':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1220896713.35mtucker"]',
        '1220906480.53mtucker':
        '["Objects"]["1169179552.88sdnaik"]["Objects"]["1220906480.53mtucker"]'
    }
}
extraInfo = {
    'camPos': Point3(-21.1505, 189.826, 41.6458),
    'camHpr': VBase3(-53.3008, -29.2777, 0),
    'focalLength': 1.39999997616,
    'skyState': 8,
    'fog': 0
}
