# Embedded file name: pirates.leveleditor.worldData.tortuga_area_jungle_c_1
from pandac.PandaModules import Point3, VBase3, Vec4
objectStruct = {
    'Interact Links':
    [['1165205238.75Shochet', '1165205254.09Shochet', 'Bi-directional'],
     ['1165204787.52Shochet', '1177007104.0dxschafe', 'Bi-directional'],
     ['1165201844.27Shochet', '1165201826.06Shochet', 'Bi-directional']],
    'Objects': {
        '1165009873.53sdnaik': {
            'Type': 'Island Game Area',
            'Name': 'tortuga_area_jungle_c_1',
            'File': '',
            'AdditionalData': ['JungleAreaC'],
            'Instanced': True,
            'Objects': {
                '1165010142.69sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_1',
                    'Hpr': VBase3(-4.256, 0.0, 0.0),
                    'Pos': Point3(-632.715, -263.407, 75.0),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1165010142.7sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_2',
                    'Hpr': VBase3(107.903, 0.0, 0.0),
                    'Pos': Point3(304.679, -408.087, 115.611),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1165201042.14Shochet': {
                    'Type': 'Log_Stack',
                    'DisableCollision': False,
                    'Hpr': VBase3(23.025, 0.919, 2.162),
                    'Pos': Point3(178.612, -273.62, 119.385),
                    'Scale': VBase3(2.824, 2.824, 2.824),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/props/Log_stack_a'
                    }
                },
                '1165201068.44Shochet': {
                    'Type': 'Log_Stack',
                    'DisableCollision': False,
                    'Hpr': VBase3(-121.072, -2.013, -1.212),
                    'Pos': Point3(178.804, -287.506, 119.425),
                    'Scale': VBase3(4.017, 4.017, 4.017),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/props/Log_stack_a'
                    }
                },
                '1165201124.13Shochet': {
                    'Type': 'Log_Stack',
                    'DisableCollision': False,
                    'Hpr': VBase3(-141.558, -1.461, -1.84),
                    'Pos': Point3(274.822, -292.729, 109.917),
                    'Scale': VBase3(1.503, 1.503, 1.503),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/props/Log_stack_c'
                    }
                },
                '1165201195.67Shochet': {
                    'Type': 'Log_Stack',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(213.579, -400.928, 118.692),
                    'Scale': VBase3(2.342, 2.342, 2.342),
                    'Visual': {
                        'Color': (0.75, 0.9300000071525574, 1.0, 1.0),
                        'Model': 'models/vegetation/gen_log_group01'
                    }
                },
                '1165201347.11Shochet': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(316.072, -221.605, 104.243),
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
                '1165201410.28Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-63.924, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '46',
                    'Pause Duration': '19',
                    'Pos': Point3(255.149, -226.468, 116.571),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165201442.48Shochet': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-30.702, 0.0, 0.0),
                    'Pos': Point3(288.428, -198.993, 103.987),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.699999988079071, 0.699999988079071,
                                  0.699999988079071, 1.0),
                        'Model':
                        'models/props/barrel_group_1'
                    }
                },
                '1165201513.53Shochet': {
                    'Type': 'Building Exterior',
                    'File': 'tortuga_building_int_carver_shack',
                    'ExtUid': '1165201513.53Shochet0',
                    'Hpr': VBase3(-61.425, 0.0, 0.0),
                    'Objects': {
                        '1209063086.42dxschafe': {
                            'Type': 'Door Locator Node',
                            'Name': 'door_locator',
                            'Hpr': VBase3(-180.0, 0.0, 0.0),
                            'Pos': Point3(0.313, -4.016, 1.444),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(217.486, 104.983, 111.548),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Color': (0.6, 0.6, 0.6, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_npc_house',
                        'Model': 'models/buildings/shanty_npc_house_combo_J',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1165201589.0Shochet': {
                    'Type': 'Log_Stack',
                    'DisableCollision': False,
                    'Hpr': VBase3(62.794, -1.429, 3.183),
                    'Pos': Point3(228.571, 83.925, 111.67),
                    'Scale': VBase3(2.552, 2.552, 2.552),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/props/Log_stack_a'
                    }
                },
                '1165201756.11Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '16.8675',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-151.782, 0.297, -0.159),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(191.58, -50.226, 115.614),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165201826.06Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '0.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(51.462, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(10.264, -31.897, 121.377),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165201844.27Shochet': {
                    'Type': 'Object Spawn Node',
                    'Hpr': VBase3(3.058, 0.0, 0.0),
                    'Pos': Point3(-5.59, 9.835, 121.076),
                    'Priority': '1',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SpawnDelay': '600',
                    'Spawnables': 'Buried Treasure',
                    'Visual': {
                        'Color': (0.8, 0.2, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    },
                    'startingDepth': '30'
                },
                '1165204787.52Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '0.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-0.353, 7.845, 5.148),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-76.52, -151.051, 126.703),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165204830.8Shochet': {
                    'Type': 'Log_Stack',
                    'DisableCollision': False,
                    'Hpr': VBase3(-102.639, 0.0, 0.0),
                    'Pos': Point3(-145.278, 44.171, 121.352),
                    'Scale': VBase3(0.797, 0.797, 0.797),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/props/Log_stack_b'
                    }
                },
                '1165204880.11Shochet': {
                    'Type': 'Log_Stack',
                    'DisableCollision': False,
                    'Hpr': VBase3(-102.639, 0.0, 0.0),
                    'Pos': Point3(-164.608, 58.82, 126.386),
                    'Scale': VBase3(0.797, 0.797, 0.797),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/props/Log_stack_b'
                    }
                },
                '1165204922.81Shochet': {
                    'Type': 'Log_Stack',
                    'DisableCollision': False,
                    'Hpr': VBase3(89.168, -4.841, 3.433),
                    'Pos': Point3(237.852, 62.793, 111.78),
                    'Scale': VBase3(1.669, 1.669, 1.669),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/props/Log_stack_b'
                    }
                },
                '1165204924.0Shochet': {
                    'Type': 'Log_Stack',
                    'DisableCollision': False,
                    'Hpr': VBase3(89.126, -5.139, 0.202),
                    'Pos': Point3(234.462, 50.016, 112.151),
                    'Scale': VBase3(1.411, 1.411, 1.411),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/props/Log_stack_b'
                    }
                },
                '1165204925.3Shochet': {
                    'Type': 'Log_Stack',
                    'DisableCollision': False,
                    'Hpr': VBase3(156.308, -9.355, 1.597),
                    'Pos': Point3(251.59, 43.707, 111.7),
                    'Scale': VBase3(1.669, 1.669, 1.669),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/props/Log_stack_b'
                    }
                },
                '1165204937.89Shochet': {
                    'Type': 'Log_Stack',
                    'DisableCollision': False,
                    'Hpr': VBase3(77.818, 0.0, 0.0),
                    'Pos': Point3(260.131, 41.658, 111.451),
                    'Scale': VBase3(1.422, 1.422, 1.422),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/props/Log_stack_b'
                    }
                },
                '1165205036.69Shochet': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-78.572, 3.111, 0.103),
                    'Pos': Point3(221.385, 92.469, 111.741),
                    'Scale': VBase3(0.592, 0.592, 0.592),
                    'Visual': {
                        'Color': (0.44, 0.48, 0.44, 1.0),
                        'Model': 'models/props/barrel_grey'
                    }
                },
                '1165205050.64Shochet': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-78.123, 4.822, 3.298),
                    'Pos': Point3(216.684, 93.087, 111.888),
                    'Scale': VBase3(0.527, 0.527, 0.527),
                    'Visual': {
                        'Color': (0.4, 0.47, 0.43, 1.0),
                        'Model': 'models/props/barrel_grey'
                    }
                },
                '1165205051.89Shochet': {
                    'Type': 'Barrel',
                    'DisableCollision': False,
                    'Hpr': VBase3(-78.35, 6.75, -0.29),
                    'Pos': Point3(215.611, 88.437, 112.005),
                    'Scale': VBase3(0.592, 0.592, 0.592),
                    'Visual': {
                        'Color': (0.4, 0.47, 0.4196078431372549, 1.0),
                        'Model': 'models/props/barrel_grey'
                    }
                },
                '1165205129.2Shochet': {
                    'Type': 'Log_Stack',
                    'DisableCollision': False,
                    'Hpr': VBase3(-78.35, 6.75, -5.156),
                    'Pos': Point3(229.039, 64.477, 112.044),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/gen_log_group02'
                    }
                },
                '1165205186.47Shochet': {
                    'Type': 'Log_Stack',
                    'DisableCollision': False,
                    'Hpr': VBase3(-78.35, 6.75, -3.317),
                    'Pos': Point3(250.13, 32.387, 111.959),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/gen_log_group03'
                    }
                },
                '1165205238.75Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(100.926, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-303.686, -305.799, 108.427),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid Skeleton',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165205254.09Shochet': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-320.276, -327.929, 105.298),
                    'Priority': '1',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SpawnDelay': '600',
                    'Spawnables': 'Buried Treasure',
                    'Visual': {
                        'Color': (0.8, 0.2, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    },
                    'startingDepth': '30'
                },
                '1165205286.52Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(55.824, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-456.808, -329.909, 90.71),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1174694272.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(127.458, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(205.738, 148.383, 108.149),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1174694272.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(108.178, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(368.35, -313.826, 113.065),
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
                '1174695296.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_searching',
                    'Hpr': VBase3(139.498, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '6.2651',
                    'Pause Chance': '30',
                    'Pause Duration': '23',
                    'Pos': Point3(304.992, -324.756, 115.27),
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
                '1174695424.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(139.996, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(355.854, -244.838, 113.213),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Early Skeleton',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1174695552.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-38.044, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '29',
                    'Pause Duration': '9',
                    'Pos': Point3(93.339, 29.134, 117.9),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1174695552.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_moaning',
                    'Hpr': VBase3(-170.407, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '50',
                    'Pause Duration': '30',
                    'Pos': Point3(65.37, 162.718, 115.607),
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
                '1174695808.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(119.856, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-439.986, -90.311, 99.523),
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
                '1174695808.0dxschafe2': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-501.896, -399.502, 88.259),
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
                '1174695936.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'barrel_hide',
                    'Hpr': VBase3(-24.193, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-431.942, -356.887, 92.692),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Early Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1174695936.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_searching',
                    'Hpr': VBase3(160.311, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-347.248, -220.434, 106.06),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Early Skeleton',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1177007104.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': VBase3(-0.353, 7.845, 5.148),
                    'Pos': Point3(-132.462, -161.219, 128.8),
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
                '1178838478.15Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-42.558, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-63.847, -13.814, 123.52),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178838489.49Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-67.326, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-281.742, -102.459, 116.758),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178838490.49Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-58.045, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-367.144, -165.032, 105.454),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178838515.97Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-78.237, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-428.123, -95.217, 100.7),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178839494.44Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-60.499, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-556.433, -226.117, 82.646),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178839577.26Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(74.891, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-443.682, -291.798, 93.274),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178839623.63Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(9.537, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-492.256, -360.029, 85.897),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178839643.19Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(2.078, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-348.063, -271.563, 104.487),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178839698.85Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-62.454, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-208.913, -75.097, 125.646),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178839755.84Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-169.869, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(164.711, 134.656, 112.812),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178839777.6Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(6.266, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(199.668, -117.533, 116.691),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178841600.0dxschafe': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-74.481, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(5.986, 82.534, 119.225),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178841600.0dxschafe0': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-155.168, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(139.115, 88.715, 114.599),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178841600.0dxschafe1': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(26.082, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(264.383, -197.541, 116.109),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178841600.0dxschafe2': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-146.254, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(244.98, -327.035, 117.325),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178841728.0dxschafe': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(32.146, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(298.375, -237.037, 115.141),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1178841728.0dxschafe0': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-74.407, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-445.024, -169.678, 96.663),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186531328.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-162.888, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-99.646, -63.65, 125.73),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186531328.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'scorpion_rear_up',
                    'Hpr': VBase3(38.99, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-131.771, -68.14, 126.908),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0.81, 0.0, 0.0, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186531328.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-153.533, -86.349, 128.009),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186531328.0dxschafe2': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-106.452, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-165.444, -11.035, 126.9),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1186531328.0dxschafe4': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '3.3133',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-165.607, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-468.363, -63.15, 97.157),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190851840.0dchiappe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(207.017, 71.586, 112.646),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190851840.0dchiappe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(232.81, 9.291, 115.208),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190852096.0dchiappe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(265.982, -305.618, 116.523),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190852352.0dchiappe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(328.171, -321.116, 114.465),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190852352.0dchiappe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(288.913, -288.473, 115.671),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190852352.0dchiappe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(326.852, -257.893, 114.255),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190852480.0dchiappe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(357.932, -255.893, 113.187),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190852736.0dchiappe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(315.579, -236.975, 114.554),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190852992.0dchiappe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(63.423, 94.075, 117.051),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190853504.0dchiappe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-157.589, -51.495, 127.446),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190853504.0dchiappe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-131.248, -42.439, 126.374),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190853504.0dchiappe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-108.062, -61.621, 125.975),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190853632.0dchiappe': {
                    'Type': 'Movement Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-118.894, -91.519, 126.941),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190853760.0dchiappe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-105.159, -101.405, 126.675),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190853760.0dchiappe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-161.29, -100.412, 128.553),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190853760.0dchiappe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-177.232, -40.025, 127.88),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190853760.0dchiappe2': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-124.684, -29.353, 125.889),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190853888.0dchiappe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-117.038, -13.84, 125.319),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190853888.0dchiappe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-84.559, -59.432, 125.136),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190853888.0dchiappe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-86.898, -111.9, 126.268),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190853888.0dchiappe2': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-162.455, -107.396, 128.733),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190853888.0dchiappe3': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-200.026, -30.631, 127.921),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190855808.0dchiappe': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(47.707, 0.0, 0.0),
                    'Pos': Point3(-157.443, -122.947, 128.875),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1190855808.0dchiappe0': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-111.418, 0.0, 0.0),
                    'Pos': Point3(-149.522, -105.572, 128.259),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1190855808.0dchiappe1': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(-40.028, 0.0, 0.0),
                    'Pos': Point3(-124.352, -32.653, 124.92),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1190915072.0dchiappe1': {
                    'Type': 'Enemy_Props',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-184.542, -79.717, 128.22),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1190915328.0dchiappe': {
                    'Type': 'Effect Node',
                    'EffectName': 'steam_effect',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-142.453, -71.614, 127.338),
                    'Scale': VBase3(2.161, 2.161, 2.161),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190916224.0dchiappe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(37.322, -14.521, 3.038),
                    'Pos': Point3(18.511, -36.687, 119.511),
                    'Scale': VBase3(1.679, 1.162, 1.226),
                    'Visual': {
                        'Color': (0.25, 0.25, 0.25098039215686274, 1.0),
                        'Model': 'models/props/dirt_pile'
                    }
                },
                '1190916480.0dchiappe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, -6.934),
                    'Pos': Point3(10.639, -39.259, 121.287),
                    'Scale': VBase3(0.541, 0.541, 0.541),
                    'Visual': {
                        'Model': 'models/props/rock_1_floor'
                    }
                },
                '1190916480.0dchiappe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(11.954, -41.006, 121.28),
                    'Scale': VBase3(0.722, 0.722, 0.722),
                    'Visual': {
                        'Model': 'models/props/rock_4_floor'
                    }
                },
                '1190916480.0dchiappe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(17.925, -31.359, 121.107),
                    'Scale': VBase3(0.871, 0.871, 0.871),
                    'Visual': {
                        'Model': 'models/props/rock_4_sphere'
                    }
                },
                '1190916608.0dchiappe': {
                    'Type': 'Grass',
                    'Hpr': VBase3(56.781, 0.0, 0.0),
                    'Pos': Point3(15.492, -33.321, 120.809),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/grass_3feet'
                    }
                },
                '1190916864.0dchiappe': {
                    'Type': 'Enemy_Props',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-186.543, -56.459, 128.525),
                    'Scale': VBase3(0.683, 0.683, 0.683),
                    'Visual': {
                        'Model': 'models/props/bone_pile01'
                    }
                },
                '1190916864.0dchiappe0': {
                    'Type': 'Enemy_Props',
                    'Hpr': VBase3(67.51, 0.0, 0.0),
                    'Pos': Point3(-211.664, -52.299, 126.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bone_pile02'
                    }
                },
                '1190916992.0dchiappe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-235.416, -54.069, 123.31),
                    'Scale': VBase3(1.737, 1.737, 1.737),
                    'Visual': {
                        'Model': 'models/props/rock_group_1_sphere'
                    }
                },
                '1190916992.0dchiappe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(128.139, 0.0, 0.0),
                    'Pos': Point3(-61.281, 47.699, 122.199),
                    'Scale': VBase3(1.946, 1.946, 1.946),
                    'Visual': {
                        'Model': 'models/props/rock_group_2_sphere'
                    }
                },
                '1190916992.0dchiappe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-143.441, 0.0, 0.0),
                    'Pos': Point3(-51.87, -131.495, 125.477),
                    'Scale': VBase3(1.783, 1.435, 1.435),
                    'Visual': {
                        'Color': (1.0, 1.0, 1.0, 1.0),
                        'Model': 'models/props/rock_group_2_sphere'
                    }
                },
                '1190917120.0dchiappe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-108.058, 0.0, 0.0),
                    'Pos': Point3(16.296, 41.575, 119.698),
                    'Scale': VBase3(1.114, 1.114, 1.114),
                    'Visual': {
                        'Model': 'models/props/rock_group_4_sphere'
                    }
                },
                '1190917248.0dchiappe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(69.388, 0.0, 0.0),
                    'Pos': Point3(-111.389, -26.231, 125.377),
                    'Scale': VBase3(0.24, 0.24, 0.24),
                    'Visual': {
                        'Model': 'models/props/rock_group_4_sphere'
                    }
                },
                '1190917248.0dchiappe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-139.974, -40.548, 126.48),
                    'Scale': VBase3(0.2, 0.415, 0.2),
                    'Visual': {
                        'Model': 'models/props/rock_group_5_sphere'
                    }
                },
                '1190917504.0dchiappe': {
                    'Type': 'Movement Node',
                    'Hpr': VBase3(-77.366, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-497.206, -157.961, 91.204),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190917504.0dchiappe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-502.512, -221.083, 88.785),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190919296.0dchiappe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(122.453, 0.0, 0.0),
                    'Level': '3',
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-406.248, -140.531, 101.818),
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
                '1190932352.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'gp_searching',
                    'Hpr': VBase3(-170.407, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '50',
                    'Pause Duration': '30',
                    'Pos': Point3(-6.964, 114.483, 121.511),
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
                '1190932480.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-101.08, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '50',
                    'Pause Duration': '30',
                    'Pos': Point3(44.528, 113.334, 121.626),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Early Skeleton',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192745397.86akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(90.477, 0.0, 0.0),
                    'Pos': Point3(182.308, -281.314, 118.602),
                    'Scale': VBase3(0.541, 1.0, 1.153),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1192745436.22akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(132.569, 0.0, 0.0),
                    'Pos': Point3(185.945, -261.294, 118.445),
                    'Scale': VBase3(0.395, 1.0, 1.266),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1195599633.11akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(91.852, 0.0, 0.0),
                    'Pos': Point3(192.269, -165.341, 117.901),
                    'Scale': VBase3(0.294, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1195599701.06akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(53.809, 0.0, 0.0),
                    'Pos': Point3(171.524, -112.674, 117.545),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1209063091.44dxschafe': {
                    'Type': 'Door Locator Node',
                    'Name': 'door_locator',
                    'Hpr': VBase3(-180.0, 0.0, 0.0),
                    'Pos': Point3(0.313, -4.016, 1.444),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1209063257.17dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-119.786, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(190.85, -305.177, 119.082),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Noob Navy',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1209063337.38dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(223.894, -387.958, 118.289),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1209063610.3dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(193.347, -290.431, 118.936),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1209063626.67dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(149.686, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(266.725, -146.88, 115.012),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Noob Navy',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1209063669.72dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(222.796, -100.545, 115.568),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Noob Navy',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1209063694.75dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(201.402, 102.325, 112.219),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1218760328.71mtucker': {
                    'Type': 'Creature',
                    'Aggro Radius': '5.7229',
                    'Boss': True,
                    'Hpr': VBase3(10.803, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(-113.122, -179.814, 128.518),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Species': 'Dread Scorpion',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'VisSize': ''
                }
            },
            'VisSize': '',
            'Visual': {
                'Model': 'models/jungles/jungle_c_zero'
            }
        }
    },
    'Node Links':
    [['1174695552.0dxschafe', '1190851840.0dchiappe0', 'Bi-directional'],
     ['1190851840.0dchiappe1', '1190851840.0dchiappe0', 'Bi-directional'],
     ['1190851840.0dchiappe1', '1174695552.0dxschafe', 'Bi-directional'],
     ['1190852096.0dchiappe', '1174695296.0dxschafe0', 'Bi-directional'],
     ['1190852352.0dchiappe', '1174694272.0dxschafe0', 'Bi-directional'],
     ['1190852352.0dchiappe', '1190852352.0dchiappe0', 'Bi-directional'],
     ['1190852352.0dchiappe0', '1190852352.0dchiappe1', 'Bi-directional'],
     ['1190852480.0dchiappe', '1190852352.0dchiappe1', 'Bi-directional'],
     ['1190852480.0dchiappe', '1174694272.0dxschafe0', 'Bi-directional'],
     ['1190852736.0dchiappe', '1165201410.28Shochet', 'Bi-directional'],
     ['1190852992.0dchiappe', '1174695552.0dxschafe0', 'Bi-directional'],
     ['1186531328.0dxschafe1', '1190853504.0dchiappe', 'Bi-directional'],
     ['1190853504.0dchiappe0', '1190853504.0dchiappe', 'Bi-directional'],
     ['1190853504.0dchiappe0', '1190853504.0dchiappe1', 'Bi-directional'],
     ['1190853632.0dchiappe', '1190853504.0dchiappe1', 'Bi-directional'],
     ['1190853632.0dchiappe', '1186531328.0dxschafe1', 'Bi-directional'],
     ['1186531328.0dxschafe', '1190853760.0dchiappe', 'Bi-directional'],
     ['1190853760.0dchiappe', '1190853760.0dchiappe0', 'Bi-directional'],
     ['1190853760.0dchiappe1', '1190853760.0dchiappe0', 'Bi-directional'],
     ['1190853760.0dchiappe1', '1190853760.0dchiappe2', 'Bi-directional'],
     ['1186531328.0dxschafe', '1190853760.0dchiappe2', 'Bi-directional'],
     ['1186531328.0dxschafe2', '1190853888.0dchiappe', 'Bi-directional'],
     ['1190853888.0dchiappe0', '1190853888.0dchiappe', 'Bi-directional'],
     ['1190853888.0dchiappe0', '1190853888.0dchiappe1', 'Bi-directional'],
     ['1190853888.0dchiappe2', '1190853888.0dchiappe1', 'Bi-directional'],
     ['1190853888.0dchiappe2', '1190853888.0dchiappe3', 'Bi-directional'],
     ['1186531328.0dxschafe2', '1190853888.0dchiappe3', 'Bi-directional'],
     ['1174695808.0dxschafe0', '1190917504.0dchiappe', 'Bi-directional'],
     ['1190917504.0dchiappe0', '1190917504.0dchiappe', 'Bi-directional'],
     ['1174695808.0dxschafe0', '1190917504.0dchiappe0', 'Bi-directional'],
     ['1209063337.38dxschafe', '1209063257.17dxschafe', 'Bi-directional'],
     ['1209063610.3dxschafe', '1209063626.67dxschafe', 'Bi-directional'],
     ['1209063694.75dxschafe', '1209063669.72dxschafe', 'Bi-directional']],
    'Layers': {},
    'ObjectIds': {
        '1165009873.53sdnaik':
        '["Objects"]["1165009873.53sdnaik"]',
        '1165010142.69sdnaik':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165010142.69sdnaik"]',
        '1165010142.7sdnaik':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165010142.7sdnaik"]',
        '1165201042.14Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165201042.14Shochet"]',
        '1165201068.44Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165201068.44Shochet"]',
        '1165201124.13Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165201124.13Shochet"]',
        '1165201195.67Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165201195.67Shochet"]',
        '1165201347.11Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165201347.11Shochet"]',
        '1165201410.28Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165201410.28Shochet"]',
        '1165201442.48Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165201442.48Shochet"]',
        '1165201513.53Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165201513.53Shochet"]',
        '1165201513.53Shochet0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165201513.53Shochet"]',
        '1165201589.0Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165201589.0Shochet"]',
        '1165201756.11Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165201756.11Shochet"]',
        '1165201826.06Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165201826.06Shochet"]',
        '1165201844.27Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165201844.27Shochet"]',
        '1165204787.52Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165204787.52Shochet"]',
        '1165204830.8Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165204830.8Shochet"]',
        '1165204880.11Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165204880.11Shochet"]',
        '1165204922.81Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165204922.81Shochet"]',
        '1165204924.0Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165204924.0Shochet"]',
        '1165204925.3Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165204925.3Shochet"]',
        '1165204937.89Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165204937.89Shochet"]',
        '1165205036.69Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165205036.69Shochet"]',
        '1165205050.64Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165205050.64Shochet"]',
        '1165205051.89Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165205051.89Shochet"]',
        '1165205129.2Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165205129.2Shochet"]',
        '1165205186.47Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165205186.47Shochet"]',
        '1165205238.75Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165205238.75Shochet"]',
        '1165205254.09Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165205254.09Shochet"]',
        '1165205286.52Shochet':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165205286.52Shochet"]',
        '1174694272.0dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1174694272.0dxschafe"]',
        '1174694272.0dxschafe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1174694272.0dxschafe0"]',
        '1174695296.0dxschafe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1174695296.0dxschafe0"]',
        '1174695424.0dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1174695424.0dxschafe"]',
        '1174695552.0dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1174695552.0dxschafe"]',
        '1174695552.0dxschafe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1174695552.0dxschafe0"]',
        '1174695808.0dxschafe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1174695808.0dxschafe0"]',
        '1174695808.0dxschafe2':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1174695808.0dxschafe2"]',
        '1174695936.0dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1174695936.0dxschafe"]',
        '1174695936.0dxschafe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1174695936.0dxschafe0"]',
        '1177007104.0dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1177007104.0dxschafe"]',
        '1178838478.15Aholdun':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1178838478.15Aholdun"]',
        '1178838489.49Aholdun':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1178838489.49Aholdun"]',
        '1178838490.49Aholdun':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1178838490.49Aholdun"]',
        '1178838515.97Aholdun':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1178838515.97Aholdun"]',
        '1178839494.44Aholdun':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1178839494.44Aholdun"]',
        '1178839577.26Aholdun':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1178839577.26Aholdun"]',
        '1178839623.63Aholdun':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1178839623.63Aholdun"]',
        '1178839643.19Aholdun':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1178839643.19Aholdun"]',
        '1178839698.85Aholdun':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1178839698.85Aholdun"]',
        '1178839755.84Aholdun':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1178839755.84Aholdun"]',
        '1178839777.6Aholdun':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1178839777.6Aholdun"]',
        '1178841600.0dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1178841600.0dxschafe"]',
        '1178841600.0dxschafe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1178841600.0dxschafe0"]',
        '1178841600.0dxschafe1':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1178841600.0dxschafe1"]',
        '1178841600.0dxschafe2':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1178841600.0dxschafe2"]',
        '1178841728.0dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1178841728.0dxschafe"]',
        '1178841728.0dxschafe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1178841728.0dxschafe0"]',
        '1186531328.0dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1186531328.0dxschafe"]',
        '1186531328.0dxschafe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1186531328.0dxschafe0"]',
        '1186531328.0dxschafe1':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1186531328.0dxschafe1"]',
        '1186531328.0dxschafe2':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1186531328.0dxschafe2"]',
        '1186531328.0dxschafe4':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1186531328.0dxschafe4"]',
        '1190851840.0dchiappe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190851840.0dchiappe0"]',
        '1190851840.0dchiappe1':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190851840.0dchiappe1"]',
        '1190852096.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190852096.0dchiappe"]',
        '1190852352.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190852352.0dchiappe"]',
        '1190852352.0dchiappe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190852352.0dchiappe0"]',
        '1190852352.0dchiappe1':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190852352.0dchiappe1"]',
        '1190852480.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190852480.0dchiappe"]',
        '1190852736.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190852736.0dchiappe"]',
        '1190852992.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190852992.0dchiappe"]',
        '1190853504.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190853504.0dchiappe"]',
        '1190853504.0dchiappe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190853504.0dchiappe0"]',
        '1190853504.0dchiappe1':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190853504.0dchiappe1"]',
        '1190853632.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190853632.0dchiappe"]',
        '1190853760.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190853760.0dchiappe"]',
        '1190853760.0dchiappe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190853760.0dchiappe0"]',
        '1190853760.0dchiappe1':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190853760.0dchiappe1"]',
        '1190853760.0dchiappe2':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190853760.0dchiappe2"]',
        '1190853888.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190853888.0dchiappe"]',
        '1190853888.0dchiappe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190853888.0dchiappe0"]',
        '1190853888.0dchiappe1':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190853888.0dchiappe1"]',
        '1190853888.0dchiappe2':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190853888.0dchiappe2"]',
        '1190853888.0dchiappe3':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190853888.0dchiappe3"]',
        '1190855808.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190855808.0dchiappe"]',
        '1190855808.0dchiappe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190855808.0dchiappe0"]',
        '1190855808.0dchiappe1':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190855808.0dchiappe1"]',
        '1190915072.0dchiappe1':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190915072.0dchiappe1"]',
        '1190915328.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190915328.0dchiappe"]',
        '1190916224.0dchiappe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190916224.0dchiappe0"]',
        '1190916480.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190916480.0dchiappe"]',
        '1190916480.0dchiappe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190916480.0dchiappe0"]',
        '1190916480.0dchiappe1':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190916480.0dchiappe1"]',
        '1190916608.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190916608.0dchiappe"]',
        '1190916864.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190916864.0dchiappe"]',
        '1190916864.0dchiappe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190916864.0dchiappe0"]',
        '1190916992.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190916992.0dchiappe"]',
        '1190916992.0dchiappe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190916992.0dchiappe0"]',
        '1190916992.0dchiappe1':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190916992.0dchiappe1"]',
        '1190917120.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190917120.0dchiappe"]',
        '1190917248.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190917248.0dchiappe"]',
        '1190917248.0dchiappe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190917248.0dchiappe0"]',
        '1190917504.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190917504.0dchiappe"]',
        '1190917504.0dchiappe0':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190917504.0dchiappe0"]',
        '1190919296.0dchiappe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190919296.0dchiappe"]',
        '1190932352.0dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190932352.0dxschafe"]',
        '1190932480.0dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1190932480.0dxschafe"]',
        '1192745397.86akelts':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1192745397.86akelts"]',
        '1192745436.22akelts':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1192745436.22akelts"]',
        '1195599633.11akelts':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1195599633.11akelts"]',
        '1195599701.06akelts':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1195599701.06akelts"]',
        '1209063086.42dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1165201513.53Shochet"]["Objects"]["1209063086.42dxschafe"]',
        '1209063091.44dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1209063091.44dxschafe"]',
        '1209063257.17dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1209063257.17dxschafe"]',
        '1209063337.38dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1209063337.38dxschafe"]',
        '1209063610.3dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1209063610.3dxschafe"]',
        '1209063626.67dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1209063626.67dxschafe"]',
        '1209063669.72dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1209063669.72dxschafe"]',
        '1209063694.75dxschafe':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1209063694.75dxschafe"]',
        '1218760328.71mtucker':
        '["Objects"]["1165009873.53sdnaik"]["Objects"]["1218760328.71mtucker"]'
    }
}
extraInfo = {
    'camPos': Point3(-138.89, -69.2947, 203.504),
    'camHpr': VBase3(-170.379, -41.2963, -2.27277e-06),
    'focalLength': 1.39999997616,
    'skyState': 2,
    'fog': 0
}
