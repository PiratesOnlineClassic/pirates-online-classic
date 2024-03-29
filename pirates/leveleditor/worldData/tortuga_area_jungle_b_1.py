# Embedded file name: pirates.leveleditor.worldData.tortuga_area_jungle_b_1
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
    [['1173409763.27sdnaik', '1176169728.0dxschafe', 'Bi-directional'],
     ['1176169088.0dxschafe0', '1176169600.0dxschafe0', 'Bi-directional'],
     ['1165200225.19Shochet', '1165200204.91Shochet', 'Bi-directional'],
     ['1176169344.0dxschafe', '1176169344.0dxschafe0', 'Bi-directional'],
     ['1176169344.0dxschafe1', '1165200514.06Shochet', 'Bi-directional'],
     ['1165200790.84Shochet', '1165200809.17Shochet', 'Bi-directional'],
     ['1176169472.0dxschafe', '1165200531.55Shochet', 'Bi-directional'],
     ['1177016704.0dxschafe', '1178916678.43Aholdun', 'Bi-directional'],
     ['1186698880.0dxschafe', '1178915376.46Aholdun', 'Bi-directional']],
    'Objects': {
        '1165009856.72sdnaik': {
            'Type': 'Island Game Area',
            'Name': 'tortuga_area_jungle_b_1',
            'File': '',
            'AdditionalData': ['JungleAreaB'],
            'Instanced': True,
            'Objects': {
                '1165010106.39sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_1',
                    'Hpr': VBase3(-90.0, 0.0, 0.0),
                    'Pos': Point3(498.114, 427.808, 45.336),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1165010106.41sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_2',
                    'Hpr': VBase3(121.61, 0.0, 0.0),
                    'Pos': Point3(-318.959, -565.768, 0.675),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1165200151.98Shochet': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1165200151.98Shochet0',
                    'Hpr': VBase3(-73.575, 0.0, 0.0),
                    'Pos': Point3(-234.599, 77.478, 20.39),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/burned_half_house',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1165200173.75Shochet': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1165200173.75Shochet0',
                    'Hpr': VBase3(-103.026, 0.0, 0.0),
                    'Pos': Point3(-245.091, 79.617, 18.146),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/burned_half_house',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1165200204.91Shochet': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-12.638, 306.002, 82.558),
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
                '1165200225.19Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-38.511, 270.307, 78.081),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Vampire Bat',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'VisSize': '',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165200271.41Shochet': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1165200271.41Shochet0',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-305.091, 67.266, 18.144),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/burned_gate',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1165200310.56Shochet': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1165200310.56Shochet0',
                    'Hpr': VBase3(-61.457, 0.0, 0.0),
                    'Pos': Point3(-312.393, 68.858, 18.532),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/burned_woods',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1165200329.72Shochet': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1165200329.72Shochet0',
                    'Hpr': VBase3(27.845, 0.0, 0.0),
                    'Pos': Point3(-290.873, 74.692, 18.353),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/burned_woods',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1165200349.66Shochet': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1165200349.66Shochet0',
                    'Hpr': VBase3(83.938, 0.0, 0.0),
                    'Pos': Point3(-311.895, 77.442, 16.26),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/burned_house',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1165200425.84Shochet': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1165200425.84Shochet0',
                    'Hpr': VBase3(9.841, 0.0, 0.0),
                    'Pos': Point3(-503.428, -280.146, 12.279),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/burned_house'
                    }
                },
                '1165200473.67Shochet': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1165200473.67Shochet0',
                    'Hpr': VBase3(105.488, 0.0, 0.0),
                    'Pos': Point3(-396.739, -271.24, 8.904),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/burned_half_house'
                    }
                },
                '1165200494.64Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(53.373, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-211.723, -90.867, 16.409),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Big Gator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165200514.06Shochet': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-377.874, -272.95, 9.689),
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
                '1165200531.55Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-506.821, -167.794, 14.504),
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
                '1165200567.16Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_chant_a',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-410.963, -50.866, 18.199),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165200596.5Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_jump',
                    'Hpr': VBase3(-37.681, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-102.074, 134.324, 22.451),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mean Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165200616.31Shochet': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1165200616.31Shochet0',
                    'Hpr': VBase3(92.507, 0.0, 0.0),
                    'Pos': Point3(243.786, 179.352, 39.036),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/burned_gate'
                    }
                },
                '1165200651.05Shochet': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1165200651.05Shochet0',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(247.57, 104.723, 37.349),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/burned_house'
                    }
                },
                '1165200700.2Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_handdig',
                    'Hpr': VBase3(-50.057, 0.187, -0.157),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '45',
                    'Pause Duration': '5',
                    'Pos': Point3(339.103, 134.999, 41.952),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165200751.17Shochet': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1165200751.17Shochet0',
                    'Hpr': VBase3(-100.425, 0.0, 0.0),
                    'Pos': Point3(43.884, -132.692, 25.405),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/burned_house',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1165200790.84Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(55.668, -53.33, 29.266),
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
                '1165200809.17Shochet': {
                    'Type': 'Object Spawn Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(42.226, -125.644, 25.345),
                    'Priority': '1',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SpawnDelay': '1200',
                    'Spawnables': 'Buried Treasure',
                    'Visual': {
                        'Color': (0.8, 0.2, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    },
                    'startingDepth': '30'
                },
                '1165200852.94Shochet': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'gp_jump',
                    'Hpr': VBase3(101.618, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-201.845, 38.966, 14.614),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1173409685.38sdnaik': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '22.5904',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-111.621, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(10.5, 268.406, 79.812),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Corpse',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'VisSize': '',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1173409763.27sdnaik': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(263.726, 62.374, 37.103),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1173409796.13sdnaik': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-61.456, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-112.346, 96.061, 19.848),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169088.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(215.037, -23.041, 33.398),
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
                '1176169344.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-283.807, -187.856, 14.407),
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
                '1176169344.0dxschafe0': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-238.076, -167.871, 16.813),
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
                '1176169344.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(155.315, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-390.938, -295.239, 9.163),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169472.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-520.431, -186.306, 13.824),
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
                '1176169600.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-61.967, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-336.567, 21.799, 13.43),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Big Gator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169600.0dxschafe0': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(198.424, -56.627, 33.181),
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
                '1176169728.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(287.943, 59.076, 37.604),
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
                '1176169728.0dxschafe0': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(101.722, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(405.718, 180.146, 46.483),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169728.0dxschafe1': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(139.3, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(460.249, 246.317, 46.941),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169728.0dxschafe10': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(38.782, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(55.703, 44.765, 28.806),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169728.0dxschafe11': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-12.318, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-450.987, -174.642, 15.556),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169728.0dxschafe12': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-10.519, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-438.563, 25.63, 17.761),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169728.0dxschafe13': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(25.439, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-384.345, -482.418, 4.123),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169728.0dxschafe14': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-22.568, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-440.895, -349.606, 5.308),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169728.0dxschafe2': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(165.864, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(493.026, 382.129, 45.388),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169728.0dxschafe3': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(110.795, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(294.614, 174.232, 40.383),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169728.0dxschafe4': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(116.944, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(142.821, 194.848, 49.909),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169728.0dxschafe5': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(125.783, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(31.707, 199.9, 51.144),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169728.0dxschafe7': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-28.55, 40.621, 25.333),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169728.0dxschafe8': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-79.058, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-298.101, 108.845, 21.75),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169856.0dxschafe': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-48.294, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-487.753, -58.48, 17.328),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169856.0dxschafe0': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-434.492, -402.964, 3.622),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169856.0dxschafe1': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-45.639, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-355.347, -248.81, 11.656),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169856.0dxschafe2': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-173.499, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-380.339, 200.151, 44.862),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169856.0dxschafe3': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(51.801, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(99.909, 7.587, 31.736),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169984.0dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-420.706, -223.175, 12.561),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176169984.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-448.365, -403.216, 2.792),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1177010048.0dxschafe': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1177010048.0dxschafe0',
                    'Hpr': VBase3(7.903, 3.059, 2.739),
                    'Objects': {
                        '1212799917.05akelts': {
                            'Type': 'Door Locator Node',
                            'Name': 'door_locator',
                            'Hpr': VBase3(-180.0, 0.0, 0.0),
                            'Pos': Point3(-4.482, -5.123, -0.112),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-214.775, 181.271, 26.781),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model':
                        'models/buildings/spanish_npc_house_b_exterior',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1177010048.0dxschafe1': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1177010048.0dxschafe2',
                    'Hpr': VBase3(88.873, 1.872, -2.166),
                    'Objects': {
                        '1212799922.7akelts': {
                            'Type': 'Door Locator Node',
                            'Name': 'door_locator',
                            'Hpr': VBase3(-180.0, 0.0, 0.0),
                            'Pos': Point3(2.885, -7.231, 0.0),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-159.716, 179.274, 23.792),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model':
                        'models/buildings/spanish_npc_house_p_exterior',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1177012992.0dxschafe': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1177012992.0dxschafe0',
                    'Hpr': VBase3(15.583, 0.0, 0.0),
                    'Pos': Point3(17.169, 167.376, 37.632),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior': 'models/buildings/interior_spanish_npc',
                        'Model': 'models/buildings/burned_woods',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1177013376.0dxschafe': {
                    'Type': 'Searchable Container',
                    'Aggro Radius': 5.0,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-146.679, 118.155, 19.358),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.58, 0.68, 0.6, 1.0),
                        'Model': 'models/props/wellA'
                    },
                    'searchTime': '10.0',
                    'type': 'WellA'
                },
                '1177013632.0dxschafe0': {
                    'Type': 'Searchable Container',
                    'Aggro Radius': 5.0,
                    'Hpr': VBase3(85.994, 0.0, 0.0),
                    'Pos': Point3(-101.131, 35.582, 18.866),
                    'Scale': VBase3(2.581, 2.581, 2.581),
                    'Visual': {
                        'Color': (0.699999988079071, 0.699999988079071,
                                  0.699999988079071, 1.0),
                        'Model':
                        'models/props/haystack'
                    },
                    'searchTime': '10.0',
                    'type': 'Haystack'
                },
                '1177013760.0dxschafe0': {
                    'Type': 'Jungle_Props_large',
                    'DisableCollision': False,
                    'Hpr': VBase3(-77.016, 23.115, 0.243),
                    'Pos': Point3(-345.342, 153.614, 112.35),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/jungle_canopy'
                    }
                },
                '1177014016.0dxschafe': {
                    'Type': 'Wall',
                    'Hpr': VBase3(-172.366, -3.625, -1.01),
                    'Pos': Point3(-156.719, 188.758, 23.928),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/buildings/woodfence_60'
                    }
                },
                '1177014144.0dxschafe': {
                    'Type': 'Wall',
                    'Hpr': VBase3(-175.12, -2.805, 1.636),
                    'Pos': Point3(-92.072, 70.466, 19.761),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/buildings/woodfence_60'
                    }
                },
                '1177015424.0dxschafe': {
                    'Type': 'Barrel',
                    'DisableCollision': True,
                    'Hpr': VBase3(85.384, 0.0, -0.203),
                    'Pos': Point3(-180.272, 175.776, 23.504),
                    'Scale': VBase3(0.703, 0.703, 0.703),
                    'Visual': {
                        'Model': 'models/props/barrel_group_2'
                    }
                },
                '1177015424.0dxschafe0': {
                    'Type': 'Crate',
                    'DisableCollision': True,
                    'Hpr': VBase3(111.212, 0.474, -1.389),
                    'Pos': Point3(-187.559, 178.024, 24.223),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.7, 0.7, 0.7, 1.0),
                        'Model': 'models/props/crates_group_1'
                    }
                },
                '1177015680.0dxschafe': {
                    'Type': 'Jungle_Props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-5.586, 7.614, 10.618),
                    'Pos': Point3(-226.602, 172.881, 27.031),
                    'Scale': VBase3(0.506, 0.506, 0.506),
                    'Visual': {
                        'Model': 'models/vegetation/jungle_plant_b'
                    }
                },
                '1177015680.0dxschafe0': {
                    'Type': 'Jungle_Props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-29.282, 14.829, 8.167),
                    'Pos': Point3(-171.554, 172.519, 24.295),
                    'Scale': VBase3(0.303, 0.303, 0.303),
                    'Visual': {
                        'Model': 'models/vegetation/jungle_plant_b'
                    }
                },
                '1177015680.0dxschafe1': {
                    'Type': 'Jungle_Props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-29.282, 14.829, 10.87),
                    'Pos': Point3(-298.405, 172.265, 33.161),
                    'Scale': VBase3(1.78, 1.78, 1.78),
                    'Visual': {
                        'Model': 'models/vegetation/jungle_plant_d'
                    }
                },
                '1177015808.0dxschafe': {
                    'Type': 'Jungle_Props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-46.731, 0.25, 3.704),
                    'Pos': Point3(-307.124, 157.79, 31.501),
                    'Scale': VBase3(1.643, 1.643, 1.643),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/vegetation/jungle_fern_a'
                    }
                },
                '1177015808.0dxschafe0': {
                    'Type': 'Jungle_Props',
                    'DisableCollision': False,
                    'Hpr': VBase3(76.84, 2.028, -3.567),
                    'Pos': Point3(-198.367, 177.248, 24.896),
                    'Scale': VBase3(1.629, 1.629, 1.629),
                    'Visual': {
                        'Model': 'models/vegetation/jungle_fern_a'
                    }
                },
                '1177015936.0dxschafe': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, 7.358),
                    'Pos': Point3(-260.087, 191.98, 32.252),
                    'Scale': VBase3(0.752, 0.752, 0.752),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1177015936.0dxschafe0': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': VBase3(-143.626, 2.912, 3.946),
                    'Pos': Point3(-303.401, 166.282, 32.533),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_b'
                    }
                },
                '1177016064.0dxschafe': {
                    'Type': 'Bush',
                    'DisableCollision': False,
                    'Hpr': VBase3(-1.118, 0.0, 0.0),
                    'Pos': Point3(-299.598, 169.216, 32.7),
                    'Scale': VBase3(1.074, 1.074, 1.074),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1177016064.0dxschafe0': {
                    'Type': 'Bush',
                    'DisableCollision': False,
                    'Hpr': VBase3(124.866, 3.447, -1.406),
                    'Pos': Point3(-263.994, 189.333, 31.818),
                    'Scale': VBase3(0.692, 0.692, 0.692),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1177016192.0dxschafe': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': VBase3(-108.699, 4.645, 1.57),
                    'Pos': Point3(-173.56, 7.948, 13.674),
                    'Scale': VBase3(0.751, 0.751, 0.751),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1177016320.0dxschafe': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(168.732, -1.331, -0.356),
                    'Pos': Point3(-153.989, 62.421, 18.673),
                    'Scale': VBase3(0.692, 0.692, 0.692),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1177016704.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': VBase3(0.375, -7.344, 5.844),
                    'Pos': Point3(-138.317, 74.208, 19.108),
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
                '1178915376.46Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-127.26, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-111.535, 138.811, 20.636),
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
                '1178916678.43Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(138.585, 9.362, 0.506),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-137.203, 160.049, 22.171),
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
                '1186599168.0dxschafe': {
                    'Type': 'Burnt_Props',
                    'DisableCollision': False,
                    'Hpr': VBase3(171.927, 0.0, 0.0),
                    'Pos': Point3(-83.838, 51.822, 21.599),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/buildings/english_m_burned'
                    }
                },
                '1186599168.0dxschafe0': {
                    'Type': 'Burnt_Props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-95.787, 0.0, 0.0),
                    'Pos': Point3(94.015, 109.058, 34.85),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/buildings/english_n_burned'
                    }
                },
                '1186599296.0dxschafe': {
                    'Type': 'Burnt_Props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(125.977, 216.369, 55.312),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model':
                        'models/vegetation/gen_tree_trunk_only_tall_burnt'
                    }
                },
                '1186599296.0dxschafe0': {
                    'Type': 'Burnt_Props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-7.827, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(-61.674, 169.747, 22.417),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/buildings/fort_eitc_burned'
                    }
                },
                '1186599424.0dxschafe0': {
                    'Type': 'Burnt_Props',
                    'DisableCollision': False,
                    'Hpr': VBase3(149.583, 0.0, 0.0),
                    'Pos': Point3(-86.124, 195.83, 23.291),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/buildings/fort_eitc_annex_2_burned'
                    }
                },
                '1186608896.0dxschafe': {
                    'Type': 'Effect Node',
                    'EffectName': 'bonfire_effect',
                    'Hpr': VBase3(0.0, -3.316, 0.0),
                    'Pos': Point3(-78.889, 66.453, 36.607),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186609024.0dxschafe': {
                    'Type': 'Effect Node',
                    'EffectName': 'bonfire_effect',
                    'Hpr': VBase3(0.0, -2.777, 0.0),
                    'Pos': Point3(-81.148, 155.099, 36.812),
                    'Scale': VBase3(1.111, 1.111, 1.111),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186609024.0dxschafe0': {
                    'Type': 'Effect Node',
                    'EffectName': 'bonfire_effect',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-78.549, 184.315, 37.176),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186609024.0dxschafe1': {
                    'Type': 'Effect Node',
                    'EffectName': 'bonfire_effect',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(-93.894, 190.927, 33.564),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186609024.0dxschafe2': {
                    'Type': 'Effect Node',
                    'EffectName': 'bonfire_effect',
                    'Hpr': VBase3(0.0, -2.777, 0.0),
                    'Pos': Point3(100.557, 110.944, 52.524),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186609024.0dxschafe3': {
                    'Type': 'Effect Node',
                    'EffectName': 'bonfire_effect',
                    'Hpr': VBase3(0.0, -2.777, 0.0),
                    'Pos': Point3(-87.484, 40.845, 39.763),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186609024.0dxschafe4': {
                    'Type': 'Effect Node',
                    'EffectName': 'bonfire_effect',
                    'Hpr': VBase3(0.0, -2.777, 0.0),
                    'Pos': Point3(-249.089, 82.116, 18.325),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186612864.0dxschafe0': {
                    'Type': 'Effect Node',
                    'EffectName': 'bonfire_effect',
                    'Hpr': VBase3(0.0, -2.777, 0.0),
                    'Pos': Point3(254.227, 109.289, 37.689),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186612864.0dxschafe1': {
                    'Type': 'Effect Node',
                    'EffectName': 'fireplace_effect',
                    'Hpr': VBase3(0.0, -2.777, 0.0),
                    'Pos': Point3(240.544, 184.423, 39.064),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186612992.0dxschafe': {
                    'Type': 'Effect Node',
                    'EffectName': 'cratersmoke_effect',
                    'Hpr': VBase3(0.0, -2.777, 0.0),
                    'Pos': Point3(-300.074, 69.768, 19.275),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186617984.0dxschafe': {
                    'Type': 'Wall',
                    'Hpr': VBase3(178.635, -3.587, -4.99),
                    'Pos': Point3(-228.515, 186.535, 28.52),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/buildings/woodfence_60'
                    }
                },
                '1186617984.0dxschafe0': {
                    'Type': 'Wall',
                    'Hpr': VBase3(-124.922, -5.9, 4.064),
                    'Pos': Point3(-286.933, 187.214, 34.25),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Model': 'models/buildings/woodfence_20'
                    }
                },
                '1186618752.0dxschafe': {
                    'Type': 'Wall',
                    'Hpr': VBase3(-92.526, -2.805, 5.18),
                    'Pos': Point3(-229.43, 150.149, 23.33),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/buildings/woodfence_20'
                    }
                },
                '1186618880.0dxschafe': {
                    'Type': 'Wall',
                    'Hpr': VBase3(87.659, 2.775, -9.129),
                    'Pos': Point3(-227.462, 161.667, 25.803),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/buildings/woodfence_20'
                    }
                },
                '1186698880.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-287.775, 159.053, 30.161),
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
                '1186710912.0dxschafe': {
                    'Type': 'Wall',
                    'Hpr': VBase3(178.635, -3.587, -1.974),
                    'Pos': Point3(-230.149, 130.245, 21.46),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/buildings/woodfence_60'
                    }
                },
                '1186711040.0dxschafe': {
                    'Type': 'Wall',
                    'Hpr': VBase3(178.635, -3.587, -2.171),
                    'Pos': Point3(-288.506, 131.377, 23.511),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/buildings/woodfence_20'
                    }
                },
                '1186711040.0dxschafe0': {
                    'Type': 'Wall',
                    'Hpr': VBase3(77.269, 11.066, -13.467),
                    'Pos': Point3(-308.549, 131.85, 24.441),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/buildings/woodfence_20'
                    }
                },
                '1186711168.0dxschafe': {
                    'Type': 'Wall',
                    'Hpr': VBase3(78.128, 12.828, -8.99),
                    'Pos': Point3(-303.561, 150.552, 29.04),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/buildings/woodfence_20'
                    }
                },
                '1186711424.0dxschafe': {
                    'Type': 'Wall',
                    'Hpr': VBase3(-83.501, 1.717, 14.123),
                    'Pos': Point3(-152.038, 66.038, 18.542),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/buildings/woodfence_20'
                    }
                },
                '1187139456.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_jump',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(84.652, 122.85, 35.464),
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
                '1187139584.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-263.558, 58.505, 16.8),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1187139712.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(246.883, 173.391, 38.982),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1187139712.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_jump',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-62.634, 76.913, 21.63),
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
                '1187139968.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-66.928, 135.343, 21.784),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1187739648.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-250.97, 89.995, 19.302),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1187739648.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-82.83, 80.903, 20.245),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1187739776.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-71.004, 144.212, 21.824),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1187739776.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-182.179, 158.407, 22.739),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1187739904.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-68.333, 81.061, 21.317),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1187739904.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-8.002, 93.149, 30.013),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1187739904.0dxschafe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(66.19, 139.803, 32.794),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1187739904.0dxschafe2': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(67.119, 112.064, 32.706),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1188322935.39akelts': {
                    'Type': 'Wall',
                    'Hpr': VBase3(-83.501, 1.717, -0.578),
                    'Pos': Point3(-149.588, 46.474, 13.436),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/buildings/woodfence_20'
                    }
                },
                '1188322967.17akelts': {
                    'Type': 'Wall',
                    'Hpr': VBase3(-86.669, 1.746, -0.482),
                    'Pos': Point3(-147.302, 26.729, 13.404),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/buildings/woodfence_20'
                    }
                },
                '1188323235.58akelts': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(-0.2, 17.064, 0.0),
                    'Pos': Point3(-152.498, 58.792, 17.28),
                    'Scale': VBase3(0.964, 0.964, 0.964),
                    'Visual': {
                        'Model': 'models/vegetation/bush_f'
                    }
                },
                '1188323430.63akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-153.56, 65.481, 15.485),
                    'Scale': VBase3(1.0, 2.777, 1.926),
                    'Visual': {
                        'Model': 'models/misc/coll_cube_barrier'
                    }
                },
                '1188497596.71kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-111.008, 0.0, 0.0),
                    'Pos': Point3(-376.901, -326.642, 9.465),
                    'Scale': VBase3(3.379, 1.566, 1.566),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1188497674.4kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-147.984, 0.0, 0.0),
                    'Pos': Point3(-335.606, -250.995, 9.219),
                    'Scale': VBase3(1.873, 1.342, 2.765),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1192836682.05dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(212.613, 13.57, 35.871),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192836741.05dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-309.282, -63.136, 18.26),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192836742.89dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-440.5, -99.515, 17.009),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192836744.89dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-384.796, -237.31, 11.009),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192836812.52dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-435.407, -432.456, 2.38),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192836857.23dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-395.395, -303.098, 8.86),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192836891.03dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-326.141, -219.369, 12.73),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192836897.05dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-241.989, -74.92, 16.367),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192836905.77dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-405.784, 4.389, 16.401),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192837021.86dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-282.374, -28.714, 18.015),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192837026.19dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-168.271, 1.383, 14.504),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192837138.92dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-211.715, 74.007, 19.425),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192837151.92dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-331.713, -13.641, 22.079),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192837205.91dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(489.093, 309.684, 47.092),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192837213.89dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(200.4, 186.878, 41.808),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192837233.55dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(208.135, 90.731, 36.081),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192837280.38dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(91.012, 137.591, 37.536),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192837335.11dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-284.414, 265.069, 62.225),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192837354.08dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-440.747, 73.237, 20.965),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192837400.44dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(108.091, 225.776, 58.022),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192837412.7dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-61.141, 98.192, 21.546),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192837594.48dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-129.78, 202.897, 26.824),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192837601.11dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-222.506, 224.073, 18.051),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192837787.25dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(187.36, 168.339, 37.808),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192837795.75dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-22.758, 142.493, 28.786),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193687936.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(99.561, 35.377, 31.623),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193688192.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(179.331, 24.625, 34.123),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193688320.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-124.023, 133.287, 20.127),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193688576.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-293.317, 167.299, 31.902),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193688576.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-131.416, 124.906, 19.628),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193688576.0dxschafe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-248.406, -50.258, 17.197),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193688704.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-361.887, -491.855, 5.203),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193688832.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_jump',
                    'Hpr': VBase3(-50.057, 0.187, -0.157),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '45',
                    'Pause Duration': '5',
                    'Pos': Point3(222.285, 127.672, 37.17),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193688960.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(42.018, 252.701, 75.196),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193688960.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-248.606, 283.77, 55.301),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193689088.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-127.672, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-77.247, 277.345, 70.704),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Corpse',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'VisSize': '',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1212799923.14akelts': {
                    'Type': 'Door Locator Node',
                    'Name': 'door_locator',
                    'Hpr': VBase3(-180.0, 0.0, 0.0),
                    'Pos': Point3(2.885, -7.231, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1212800423.64akelts': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(124.024, 0.0, 0.0),
                    'Pos': Point3(61.953, -123.727, 26.323),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1219434293.16mtucker': {
                    'Type': 'Skeleton',
                    'Aggro Radius': '6.9277',
                    'AnimSet': 'gp_jump',
                    'AvId': 4,
                    'AvTrack': 0,
                    'Boss': True,
                    'DNA': '1219434293.16mtucker',
                    'Hpr': VBase3(154.804, 0.0, 0.0),
                    'Patrol Radius': '3.5181',
                    'Pos': Point3(-65.594, 241.079, 73.767),
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
                'Model': 'models/jungles/jungle_b_zero'
            }
        }
    },
    'Node Links':
    [['1187139712.0dxschafe0', '1187139712.0dxschafe', 'Bi-directional'],
     ['1187139968.0dxschafe', '1165200567.16Shochet', 'Bi-directional'],
     ['1187739776.0dxschafe', '1187139456.0dxschafe', 'Bi-directional'],
     ['1187739776.0dxschafe', '1187739648.0dxschafe0', 'Bi-directional'],
     ['1187739776.0dxschafe0', '1187739648.0dxschafe0', 'Bi-directional'],
     ['1187739776.0dxschafe0', '1187739648.0dxschafe', 'Bi-directional'],
     ['1187739648.0dxschafe', '1187139584.0dxschafe', 'Bi-directional'],
     ['1187739904.0dxschafe', '1187139968.0dxschafe', 'Bi-directional'],
     ['1187739904.0dxschafe', '1187739904.0dxschafe2', 'Bi-directional'],
     ['1192836744.89dxschafe', '1176169344.0dxschafe', 'Bi-directional'],
     ['1176169344.0dxschafe', '1192836741.05dxschafe', 'Bi-directional'],
     ['1192836742.89dxschafe', '1192836741.05dxschafe', 'Bi-directional'],
     ['1192836744.89dxschafe', '1192836742.89dxschafe', 'Bi-directional'],
     ['1176169984.0dxschafe', '1192836812.52dxschafe', 'Bi-directional'],
     ['1192836857.23dxschafe', '1176169984.0dxschafe0', 'Bi-directional'],
     ['1192836897.05dxschafe', '1192836905.77dxschafe', 'Bi-directional'],
     ['1192836891.03dxschafe', '1165200531.55Shochet', 'Bi-directional'],
     ['1165200531.55Shochet', '1192836905.77dxschafe', 'Bi-directional'],
     ['1192837026.19dxschafe', '1192837021.86dxschafe', 'Bi-directional'],
     ['1176169600.0dxschafe', '1192837021.86dxschafe', 'Bi-directional'],
     ['1192837138.92dxschafe', '1192837151.92dxschafe', 'Bi-directional'],
     ['1192837233.55dxschafe', '1173409763.27sdnaik', 'Bi-directional'],
     ['1192837233.55dxschafe', '1192837213.89dxschafe', 'Bi-directional'],
     ['1192837280.38dxschafe', '1165200700.2Shochet', 'Bi-directional'],
     ['1192837335.11dxschafe', '1192837354.08dxschafe', 'Bi-directional'],
     ['1192837400.44dxschafe', '1173409685.38sdnaik', 'Bi-directional'],
     ['1192837400.44dxschafe', '1192837412.7dxschafe', 'Bi-directional'],
     ['1192837594.48dxschafe', '1192837601.11dxschafe', 'Bi-directional'],
     ['1192837787.25dxschafe', '1192837795.75dxschafe', 'Bi-directional'],
     ['1165200790.84Shochet', '1193687936.0dxschafe', 'Bi-directional'],
     ['1193687936.0dxschafe', '1187739904.0dxschafe0', 'Bi-directional'],
     ['1192836682.05dxschafe', '1193687936.0dxschafe', 'Bi-directional'],
     ['1193688192.0dxschafe', '1176169088.0dxschafe0', 'Bi-directional'],
     ['1193688320.0dxschafe', '1193688192.0dxschafe', 'Bi-directional'],
     ['1165200700.2Shochet', '1192837205.91dxschafe', 'Bi-directional'],
     ['1165200596.5Shochet', '1193688576.0dxschafe', 'Bi-directional'],
     ['1192837594.48dxschafe', '1193688576.0dxschafe0', 'Bi-directional'],
     ['1165200852.94Shochet', '1193688576.0dxschafe0', 'Bi-directional'],
     ['1192837138.92dxschafe', '1193688576.0dxschafe1', 'Bi-directional'],
     ['1165200494.64Shochet', '1193688576.0dxschafe1', 'Bi-directional'],
     ['1193688704.0dxschafe', '1176169984.0dxschafe0', 'Bi-directional'],
     ['1193688960.0dxschafe', '1193688832.0dxschafe0', 'Bi-directional'],
     ['1193688960.0dxschafe0', '1165200225.19Shochet', 'Bi-directional'],
     ['1193689088.0dxschafe0', '1192837335.11dxschafe', 'Bi-directional']],
    'Layers': {},
    'ObjectIds': {
        '1165009856.72sdnaik':
        '["Objects"]["1165009856.72sdnaik"]',
        '1165010106.39sdnaik':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165010106.39sdnaik"]',
        '1165010106.41sdnaik':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165010106.41sdnaik"]',
        '1165200151.98Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200151.98Shochet"]',
        '1165200151.98Shochet0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200151.98Shochet"]',
        '1165200173.75Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200173.75Shochet"]',
        '1165200173.75Shochet0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200173.75Shochet"]',
        '1165200204.91Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200204.91Shochet"]',
        '1165200225.19Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200225.19Shochet"]',
        '1165200271.41Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200271.41Shochet"]',
        '1165200271.41Shochet0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200271.41Shochet"]',
        '1165200310.56Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200310.56Shochet"]',
        '1165200310.56Shochet0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200310.56Shochet"]',
        '1165200329.72Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200329.72Shochet"]',
        '1165200329.72Shochet0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200329.72Shochet"]',
        '1165200349.66Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200349.66Shochet"]',
        '1165200349.66Shochet0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200349.66Shochet"]',
        '1165200425.84Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200425.84Shochet"]',
        '1165200425.84Shochet0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200425.84Shochet"]',
        '1165200473.67Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200473.67Shochet"]',
        '1165200473.67Shochet0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200473.67Shochet"]',
        '1165200494.64Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200494.64Shochet"]',
        '1165200514.06Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200514.06Shochet"]',
        '1165200531.55Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200531.55Shochet"]',
        '1165200567.16Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200567.16Shochet"]',
        '1165200596.5Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200596.5Shochet"]',
        '1165200616.31Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200616.31Shochet"]',
        '1165200616.31Shochet0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200616.31Shochet"]',
        '1165200651.05Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200651.05Shochet"]',
        '1165200651.05Shochet0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200651.05Shochet"]',
        '1165200700.2Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200700.2Shochet"]',
        '1165200751.17Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200751.17Shochet"]',
        '1165200751.17Shochet0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200751.17Shochet"]',
        '1165200790.84Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200790.84Shochet"]',
        '1165200809.17Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200809.17Shochet"]',
        '1165200852.94Shochet':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1165200852.94Shochet"]',
        '1173409685.38sdnaik':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1173409685.38sdnaik"]',
        '1173409763.27sdnaik':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1173409763.27sdnaik"]',
        '1173409796.13sdnaik':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1173409796.13sdnaik"]',
        '1176169088.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169088.0dxschafe0"]',
        '1176169344.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169344.0dxschafe"]',
        '1176169344.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169344.0dxschafe0"]',
        '1176169344.0dxschafe1':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169344.0dxschafe1"]',
        '1176169472.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169472.0dxschafe"]',
        '1176169600.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169600.0dxschafe"]',
        '1176169600.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169600.0dxschafe0"]',
        '1176169728.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169728.0dxschafe"]',
        '1176169728.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169728.0dxschafe0"]',
        '1176169728.0dxschafe1':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169728.0dxschafe1"]',
        '1176169728.0dxschafe10':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169728.0dxschafe10"]',
        '1176169728.0dxschafe11':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169728.0dxschafe11"]',
        '1176169728.0dxschafe12':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169728.0dxschafe12"]',
        '1176169728.0dxschafe13':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169728.0dxschafe13"]',
        '1176169728.0dxschafe14':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169728.0dxschafe14"]',
        '1176169728.0dxschafe2':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169728.0dxschafe2"]',
        '1176169728.0dxschafe3':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169728.0dxschafe3"]',
        '1176169728.0dxschafe4':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169728.0dxschafe4"]',
        '1176169728.0dxschafe5':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169728.0dxschafe5"]',
        '1176169728.0dxschafe7':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169728.0dxschafe7"]',
        '1176169728.0dxschafe8':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169728.0dxschafe8"]',
        '1176169856.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169856.0dxschafe"]',
        '1176169856.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169856.0dxschafe0"]',
        '1176169856.0dxschafe1':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169856.0dxschafe1"]',
        '1176169856.0dxschafe2':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169856.0dxschafe2"]',
        '1176169856.0dxschafe3':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169856.0dxschafe3"]',
        '1176169984.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169984.0dxschafe"]',
        '1176169984.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1176169984.0dxschafe0"]',
        '1177010048.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177010048.0dxschafe"]',
        '1177010048.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177010048.0dxschafe"]',
        '1177010048.0dxschafe1':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177010048.0dxschafe1"]',
        '1177010048.0dxschafe2':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177010048.0dxschafe1"]',
        '1177012992.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177012992.0dxschafe"]',
        '1177012992.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177012992.0dxschafe"]',
        '1177013376.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177013376.0dxschafe"]',
        '1177013632.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177013632.0dxschafe0"]',
        '1177013760.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177013760.0dxschafe0"]',
        '1177014016.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177014016.0dxschafe"]',
        '1177014144.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177014144.0dxschafe"]',
        '1177015424.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177015424.0dxschafe"]',
        '1177015424.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177015424.0dxschafe0"]',
        '1177015680.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177015680.0dxschafe"]',
        '1177015680.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177015680.0dxschafe0"]',
        '1177015680.0dxschafe1':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177015680.0dxschafe1"]',
        '1177015808.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177015808.0dxschafe"]',
        '1177015808.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177015808.0dxschafe0"]',
        '1177015936.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177015936.0dxschafe"]',
        '1177015936.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177015936.0dxschafe0"]',
        '1177016064.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177016064.0dxschafe"]',
        '1177016064.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177016064.0dxschafe0"]',
        '1177016192.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177016192.0dxschafe"]',
        '1177016320.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177016320.0dxschafe"]',
        '1177016704.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177016704.0dxschafe"]',
        '1178915376.46Aholdun':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1178915376.46Aholdun"]',
        '1178916678.43Aholdun':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1178916678.43Aholdun"]',
        '1186599168.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186599168.0dxschafe"]',
        '1186599168.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186599168.0dxschafe0"]',
        '1186599296.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186599296.0dxschafe"]',
        '1186599296.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186599296.0dxschafe0"]',
        '1186599424.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186599424.0dxschafe0"]',
        '1186608896.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186608896.0dxschafe"]',
        '1186609024.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186609024.0dxschafe"]',
        '1186609024.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186609024.0dxschafe0"]',
        '1186609024.0dxschafe1':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186609024.0dxschafe1"]',
        '1186609024.0dxschafe2':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186609024.0dxschafe2"]',
        '1186609024.0dxschafe3':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186609024.0dxschafe3"]',
        '1186609024.0dxschafe4':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186609024.0dxschafe4"]',
        '1186612864.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186612864.0dxschafe0"]',
        '1186612864.0dxschafe1':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186612864.0dxschafe1"]',
        '1186612992.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186612992.0dxschafe"]',
        '1186617984.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186617984.0dxschafe"]',
        '1186617984.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186617984.0dxschafe0"]',
        '1186618752.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186618752.0dxschafe"]',
        '1186618880.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186618880.0dxschafe"]',
        '1186698880.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186698880.0dxschafe"]',
        '1186710912.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186710912.0dxschafe"]',
        '1186711040.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186711040.0dxschafe"]',
        '1186711040.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186711040.0dxschafe0"]',
        '1186711168.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186711168.0dxschafe"]',
        '1186711424.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1186711424.0dxschafe"]',
        '1187139456.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1187139456.0dxschafe"]',
        '1187139584.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1187139584.0dxschafe"]',
        '1187139712.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1187139712.0dxschafe"]',
        '1187139712.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1187139712.0dxschafe0"]',
        '1187139968.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1187139968.0dxschafe"]',
        '1187739648.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1187739648.0dxschafe"]',
        '1187739648.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1187739648.0dxschafe0"]',
        '1187739776.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1187739776.0dxschafe"]',
        '1187739776.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1187739776.0dxschafe0"]',
        '1187739904.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1187739904.0dxschafe"]',
        '1187739904.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1187739904.0dxschafe0"]',
        '1187739904.0dxschafe1':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1187739904.0dxschafe1"]',
        '1187739904.0dxschafe2':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1187739904.0dxschafe2"]',
        '1188322935.39akelts':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1188322935.39akelts"]',
        '1188322967.17akelts':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1188322967.17akelts"]',
        '1188323235.58akelts':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1188323235.58akelts"]',
        '1188323430.63akelts':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1188323430.63akelts"]',
        '1188497596.71kmuller':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1188497596.71kmuller"]',
        '1188497674.4kmuller':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1188497674.4kmuller"]',
        '1192836682.05dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192836682.05dxschafe"]',
        '1192836741.05dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192836741.05dxschafe"]',
        '1192836742.89dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192836742.89dxschafe"]',
        '1192836744.89dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192836744.89dxschafe"]',
        '1192836812.52dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192836812.52dxschafe"]',
        '1192836857.23dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192836857.23dxschafe"]',
        '1192836891.03dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192836891.03dxschafe"]',
        '1192836897.05dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192836897.05dxschafe"]',
        '1192836905.77dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192836905.77dxschafe"]',
        '1192837021.86dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192837021.86dxschafe"]',
        '1192837026.19dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192837026.19dxschafe"]',
        '1192837138.92dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192837138.92dxschafe"]',
        '1192837151.92dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192837151.92dxschafe"]',
        '1192837205.91dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192837205.91dxschafe"]',
        '1192837213.89dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192837213.89dxschafe"]',
        '1192837233.55dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192837233.55dxschafe"]',
        '1192837280.38dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192837280.38dxschafe"]',
        '1192837335.11dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192837335.11dxschafe"]',
        '1192837354.08dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192837354.08dxschafe"]',
        '1192837400.44dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192837400.44dxschafe"]',
        '1192837412.7dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192837412.7dxschafe"]',
        '1192837594.48dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192837594.48dxschafe"]',
        '1192837601.11dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192837601.11dxschafe"]',
        '1192837787.25dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192837787.25dxschafe"]',
        '1192837795.75dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1192837795.75dxschafe"]',
        '1193687936.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1193687936.0dxschafe"]',
        '1193688192.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1193688192.0dxschafe"]',
        '1193688320.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1193688320.0dxschafe"]',
        '1193688576.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1193688576.0dxschafe"]',
        '1193688576.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1193688576.0dxschafe0"]',
        '1193688576.0dxschafe1':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1193688576.0dxschafe1"]',
        '1193688704.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1193688704.0dxschafe"]',
        '1193688832.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1193688832.0dxschafe0"]',
        '1193688960.0dxschafe':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1193688960.0dxschafe"]',
        '1193688960.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1193688960.0dxschafe0"]',
        '1193689088.0dxschafe0':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1193689088.0dxschafe0"]',
        '1212799917.05akelts':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177010048.0dxschafe"]["Objects"]["1212799917.05akelts"]',
        '1212799922.7akelts':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1177010048.0dxschafe1"]["Objects"]["1212799922.7akelts"]',
        '1212799923.14akelts':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1212799923.14akelts"]',
        '1212800423.64akelts':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1212800423.64akelts"]',
        '1219434293.16mtucker':
        '["Objects"]["1165009856.72sdnaik"]["Objects"]["1219434293.16mtucker"]'
    }
}
extraInfo = {
    'camPos': Point3(-233.509, 159.005, 175.448),
    'camHpr': VBase3(-65.561, -20.898, 0),
    'focalLength': 1.39999997616,
    'skyState': 2,
    'fog': 0
}
