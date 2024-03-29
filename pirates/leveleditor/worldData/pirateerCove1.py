# Embedded file name: pirates.leveleditor.worldData.pirateerCove1
from pandac.PandaModules import Point3, VBase3
objectStruct = {
    'Objects': {
        '1151689233.71hreister': {
            'Type': 'Island',
            'Name': 'pirateerCove1',
            'File': '',
            'Objects': {
                '1151689490.21hreister': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(35.883, 16.415, 140.855),
                    'Scale': VBase3(0.728, 0.728, 0.728),
                    'Spawnables': 'Team 2'
                },
                '1151690471.18hreister': {
                    'Type': 'Event Sphere',
                    'Collide Type': 'Object',
                    'Event Type': 'Port',
                    'Extra Param': 'Team 2',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(223.914, 0.066, -15.4),
                    'Scale': VBase3(120.0, 120.0, 120.0)
                },
                '1156210410.53bbathen': {
                    'Type': 'Rock',
                    'GridPos': Point3(17.228, -264.876, 16.741),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(17.228, -291.741, -14.091),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1156210474.53bbathen': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(21.102, 1.441, 0.0),
                    'Pos': Point3(-12.591, -122.127, 110.864),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/fern_leaf_a_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/fern_trunk_a_idle',
                        'Model': 'models/vegetation/fern_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1156271007.17bbathen': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-155.654, -11.41, 24.698),
                    'Objects': {},
                    'Pos': Point3(-326.2, -131.985, 44.308),
                    'Scale': VBase3(4.051, 4.051, 4.051),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/rock_group_3_sphere'
                    }
                },
                '1156272251.25bbathen': {
                    'Type': 'Tree',
                    'Hpr': VBase3(42.505, 0.0, 0.0),
                    'Pos': Point3(-11.67, -145.644, 98.273),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1156356079.1bbathen': {
                    'Type': 'Tree - Animated',
                    'GridPos': Point3(-11.726, -142.15, 101.938),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-16.169, -132.358, 106.323),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/palm_leaf_a_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1159462943.35kmuller': {
                    'Type': 'Pier',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {
                        '1159571614.58kmuller': {
                            'Type': 'Ship_Props',
                            'GridPos': Point3(134.836, -22.903, 6.186),
                            'Hpr': VBase3(121.828, -23.344, 6.864),
                            'Pos': Point3(10.316, -14.347, 9.907),
                            'Scale': VBase3(1.953, 1.953, 1.953),
                            'Visual': {
                                'Model': 'models/props/anchor'
                            }
                        },
                        '1159577833.43kmuller': {
                            'Type': 'Rope',
                            'GridPos': Point3(144.404, 3.072, 5.414),
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(29.005, 36.385, 8.398),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/rope_pile'
                            }
                        },
                        '1159577902.76kmuller': {
                            'Type': 'Barrel',
                            'GridPos': Point3(136.747, 0.721, 5.601),
                            'Hpr': VBase3(65.711, 0.0, 0.0),
                            'Pos': Point3(14.048, 31.793, 8.764),
                            'Scale': VBase3(0.66, 0.66, 0.66),
                            'Visual': {
                                'Model': 'models/props/barrel_group_3'
                            }
                        },
                        '1159578015.84kmuller': {
                            'Type': 'Prop_Groups',
                            'GridPos': Point3(118.205, -12.353, 5.461),
                            'Hpr': VBase3(-167.721, 0.0, 0.0),
                            'Pos': Point3(-22.167, 6.258, 8.489),
                            'Scale': VBase3(1.953, 1.953, 1.953),
                            'Visual': {
                                'Color':
                                (0.8999999761581421, 0.8999999761581421,
                                 0.699999988079071, 1.0),
                                'Model':
                                'models/props/prop_group_A'
                            }
                        }
                    },
                    'Pos': Point3(127.819, -11.909, 1.114),
                    'Scale': VBase3(0.512, 0.512, 0.512),
                    'Visual': {
                        'Model': 'models/islands/pier_platform'
                    }
                },
                '1159552023.43kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-139.427, 0.0, 0.0),
                    'Pos': Point3(482.128, 143.608, -16.095),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.75, 0.9300000071525574, 1.0, 1.0),
                        'Model': 'models/props/mound_brown_small'
                    }
                },
                '1159552271.06kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-8.308, -0.089, 5.907),
                    'Pos': Point3(-308.509, 139.874, -167.699),
                    'Scale': VBase3(1.052, 1.052, 1.052),
                    'Visual': {
                        'Color': (0.800000011920929, 0.800000011920929,
                                  0.800000011920929, 1.0),
                        'Model':
                        'models/props/mound_light_lrg'
                    }
                },
                '1159552371.25kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-28.803, 6.184, -1.43),
                    'Pos': Point3(-310.336, 1.171, 31.467),
                    'Scale': VBase3(1.09, 1.09, 1.09),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/mound_light_small'
                    }
                },
                '1159552461.11kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(31.714, 3.739, 13.474),
                    'Pos': Point3(-98.402, 82.96, 52.168),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.9882352948188782, 0.9411764740943909,
                                  0.46666666865348816, 1.0),
                        'Model':
                        'models/props/madre_mound_small'
                    }
                },
                '1159552660.83kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-63.724, 0.0, 0.0),
                    'Pos': Point3(-255.717, -175.363, 30.531),
                    'Scale': VBase3(10.561, 10.561, 10.561),
                    'Visual': {
                        'Color': (0.7490196228027344, 0.7137255072593689,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/rock_4_sphere'
                    }
                },
                '1159552691.26kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-8.099, 21.335, -10.206),
                    'Pos': Point3(-229.114, -135.798, 55.034),
                    'Scale': VBase3(5.431, 5.431, 5.431),
                    'Visual': {
                        'Color': (0.7686274647712708, 0.7333333492279053,
                                  0.6117647290229797, 1.0),
                        'Model':
                        'models/props/rock_group_5_sphere'
                    }
                },
                '1159552807.56kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-71.639, 12.297, 0.0),
                    'Pos': Point3(136.747, -316.567, 19.022),
                    'Scale': VBase3(2.649, 2.649, 2.649),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/rock_group_5_sphere'
                    }
                },
                '1159555763.83kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-66.696, -3.435, 9.957),
                    'Pos': Point3(-1.867, -124.827, 107.033),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1159555884.76kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(76.199, -189.379, 59.386),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1159556024.17kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-62.252, 19.06, 9.901),
                    'Pos': Point3(-251.057, -160.83, 43.217),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1159567540.84kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(333.215, 135.68, 58.149),
                    'Scale': VBase3(0.797, 0.797, 0.797),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_d'
                    }
                },
                '1159567716.55kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(39.472, 0.0, 0.0),
                    'Pos': Point3(297.822, -257.311, -14.094),
                    'Scale': VBase3(0.467, 0.467, 0.467),
                    'Visual': {
                        'Model': 'models/props/mound_light_med'
                    }
                },
                '1159567796.47kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-45.29, -9.57, 0.0),
                    'Pos': Point3(304.914, -299.34, 16.798),
                    'Scale': VBase3(4.539, 4.539, 4.539),
                    'Visual': {
                        'Color': (0.699999988079071, 0.699999988079071,
                                  0.699999988079071, 1.0),
                        'Model':
                        'models/props/rock_1_sphere'
                    }
                },
                '1159568081.89kmuller': {
                    'Type': 'Treasure Duck',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(276.485, -380.981, 9.725),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/islands/treasureDuck'
                    }
                },
                '1159568276.33kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(-26.052, 0.0, 0.0),
                    'Pos': Point3(-187.158, -214.384, 27.33),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.800000011920929, 1.0, 0.6000000238418579,
                                  1.0),
                        'Model': 'models/vegetation/gen_tree_d'
                    }
                },
                '1159568349.97kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(-50.85, -0.147, -0.135),
                    'Pos': Point3(-241.507, -140.072, 56.57),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.800000011920929, 0.6000000238418579, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1159568456.23kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(-287.462, -139.622, 40.603),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/gen_tree_c'
                    }
                },
                '1159569544.56kmuller': {
                    'Type': 'Cart',
                    'Hpr': VBase3(56.416, 0.0, 0.0),
                    'Pos': Point3(94.718, 91.434, 93.657),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cart_flat'
                    }
                },
                '1159569614.05kmuller': {
                    'Type': 'Cart',
                    'Hpr': VBase3(-145.546, 0.0, 0.0),
                    'Pos': Point3(184.031, 159.463, 50.767),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cart_broken'
                    }
                },
                '1159569712.45kmuller': {
                    'Type': 'Crate',
                    'Hpr': VBase3(-12.104, 0.0, 0.0),
                    'Pos': Point3(131.149, 231.726, 94.608),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.8999999761581421, 0.8999999761581421,
                                  0.699999988079071, 1.0),
                        'Model':
                        'models/props/crates_group_1'
                    }
                },
                '1159569773.83kmuller': {
                    'Type': 'Crate',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(129.324, 225.442, 94.664),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.800000011920929, 0.800000011920929,
                                  0.800000011920929, 1.0),
                        'Model':
                        'models/props/crate'
                    }
                },
                '1159569900.09kmuller': {
                    'Type': 'Prop_Groups',
                    'Hpr': VBase3(134.877, 0.0, 0.0),
                    'Pos': Point3(155.355, 227.199, 94.949),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/prop_group01'
                    }
                },
                '1159570204.98kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(1.691, 0.0, 0.0),
                    'Pos': Point3(90.689, 57.114, 26.048),
                    'Scale': VBase3(1.08, 1.08, 1.08),
                    'Visual': {
                        'Model': 'models/props/rock_1_sphere'
                    }
                },
                '1159570260.37kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(37.952, 0.0, -17.231),
                    'Pos': Point3(92.15, 53.89, 29.103),
                    'Scale': VBase3(2.63, 2.63, 2.63),
                    'Visual': {
                        'Model': 'models/props/rock_3_sphere'
                    }
                },
                '1159571261.97kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(59.691, 0.0, 0.0),
                    'Pos': Point3(81.947, 43.111, 27.714),
                    'Scale': VBase3(3.17, 3.17, 3.17),
                    'Visual': {
                        'Model': 'models/props/rock_4_sphere'
                    }
                },
                '1159571492.72kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(154.83, 39.311, -20.125),
                    'Pos': Point3(80.323, 40.333, 39.115),
                    'Scale': VBase3(3.693, 3.693, 3.693),
                    'Visual': {
                        'Model': 'models/props/rock_2_floor'
                    }
                },
                '1159572021.7kmuller': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(258.714, -335.027, 22.12),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_b'
                    }
                },
                '1159572104.36kmuller': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(287.88, -336.186, 25.75),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1159572148.33kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 3.927, 0.0),
                    'Pos': Point3(297.844, -354.741, 16.787),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1159572175.89kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(106.77, -1.135, -15.362),
                    'Pos': Point3(281.254, -342.8, 26.356),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1159572361.37kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-54.794, -9.998, 1.844),
                    'Pos': Point3(313.846, -289.618, 9.503),
                    'Scale': VBase3(0.727, 0.727, 0.727),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1159572620.67kmuller': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(460.879, 93.691, 27.747),
                    'Scale': VBase3(1.938, 1.938, 1.938),
                    'Visual': {
                        'Model': 'models/vegetation/palm_tree_d'
                    }
                },
                '1159572763.56kmuller': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(461.453, 93.801, 28.456),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_i'
                    }
                },
                '1159572937.51kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 0.0, 12.267),
                    'Pos': Point3(481.777, 79.103, 25.15),
                    'Scale': VBase3(1.532, 1.532, 1.532),
                    'Visual': {
                        'Model': 'models/props/rock_4_floor'
                    }
                },
                '1159572983.98kmuller': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(476.518, 81.198, 27.329),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rock_1_floor'
                    }
                },
                '1159573082.42kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-42.664, -2.98, -0.456),
                    'Pos': Point3(449.88, 82.217, 30.68),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1159573356.83kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(427.429, 84.88, 32.386),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1159573502.25kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-28.985, 0.262, 1.882),
                    'Pos': Point3(370.483, 73.795, 40.539),
                    'Scale': VBase3(0.598, 0.598, 0.598),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1159573636.08kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(378.551, 76.318, 41.402),
                    'Scale': VBase3(1.286, 1.286, 1.286),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_d'
                    }
                },
                '1159573702.3kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(0.0, -0.247, 0.0),
                    'Pos': Point3(387.469, 58.977, 37.659),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1159573798.31kmuller': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(379.555, 70.661, 39.143),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rock_group_5_floor'
                    }
                },
                '1159573818.67kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-30.933, 0.0, 3.472),
                    'Pos': Point3(367.928, 90.031, 40.487),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rock_group_3_floor'
                    }
                },
                '1159574029.58kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(95.713, 7.08, -14.89),
                    'Pos': Point3(367.985, 135.344, 49.503),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rock_group_3_sphere'
                    }
                },
                '1159574144.55kmuller': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-332.954, -94.582, 43.9),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.699999988079071, 0.699999988079071,
                                  0.699999988079071, 1.0),
                        'Model':
                        'models/vegetation/gen_tree_e'
                    }
                },
                '1159574235.97kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-131.798, 0.0, 0.0),
                    'Pos': Point3(-421.345, 36.296, -71.178),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/mound_light_med2'
                    }
                },
                '1159574274.31kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-88.205, 0.0, 0.0),
                    'Pos': Point3(-461.749, 192.478, -61.648),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/mound_light_med'
                    }
                },
                '1159574356.55kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-15.824, 0.0, 0.0),
                    'Pos': Point3(-254.932, 311.446, -77.905),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/mound_light_med2'
                    }
                },
                '1159574445.28kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-177.502, 8.982, 0.0),
                    'Pos': Point3(-228.172, 278.025, 21.224),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/mound_light_small'
                    }
                },
                '1159574480.65kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-81.97, -2.253, -50.614),
                    'Pos': Point3(-27.56, 335.38, -0.739),
                    'Scale': VBase3(1.627, 1.627, 1.627),
                    'Visual': {
                        'Model': 'models/props/mound_light_small'
                    }
                },
                '1159574574.47kmuller': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-79.187, 272.353, -23.692),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/mound_light_med2'
                    }
                },
                '1159574802.43kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(40.671, 0.789, 2.772),
                    'Pos': Point3(-151.379, 299.774, 33.119),
                    'Scale': VBase3(1.076, 1.076, 1.076),
                    'Visual': {
                        'Model': 'models/props/rock_group_2_sphere'
                    }
                },
                '1159575469.14kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-125.848, 12.939, -9.174),
                    'Pos': Point3(76.62, 369.604, 20.759),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_leaves'
                    }
                },
                '1159576451.58kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(0.0, 4.113, 0.0),
                    'Pos': Point3(287.95, -351.596, 21.63),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1159576510.05kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 16.11, 0.0),
                    'Objects': {
                        '1159576548.67kmuller': {
                            'Type': 'Bush',
                            'GridPos': Point3(312.343, -358.994, 14.296),
                            'Hpr': VBase3(82.232, 4.091, 10.747),
                            'Pos': Point3(2.667, -0.516, -2.022),
                            'Scale': VBase3(0.849, 0.849, 0.849),
                            'Visual': {
                                'Model': 'models/vegetation/bush_leaves'
                            }
                        }
                    },
                    'Pos': Point3(309.676, -359.059, 16.382),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rock_group_2_floor'
                    }
                },
                '1159576738.75kmuller': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-332.517, -120.151, 47.565),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_f'
                    }
                },
                '1159576857.62kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-20.565, 0.715, 0.268),
                    'Pos': Point3(-313.366, -131.837, 45.137),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1159576923.68kmuller': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-359.438, -93.135, 38.731),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1159577147.55kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(10.256, 3.661, 10.531),
                    'Objects': {
                        '1159828247.64kmuller': {
                            'Type': 'Bush',
                            'GridPos': Point3(487.764, 89.707, 24.025),
                            'Hpr': VBase3(90.909, -7.786, -0.979),
                            'Pos': Point3(3.466, -0.432, -1.202),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/vegetation/bush_leaves'
                            }
                        }
                    },
                    'Pos': Point3(484.571, 89.45, 25.864),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rock_group_2_floor'
                    }
                },
                '1159577236.53kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(36.561, 5.564, 7.449),
                    'Pos': Point3(490.406, 112.076, 14.661),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_g'
                    }
                },
                '1159577268.76kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(40.854, 0.0, 2.729),
                    'Pos': Point3(493.761, 107.048, 17.629),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/bush_h'
                    }
                },
                '1159577448.97kmuller': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(460.697, 55.325, 25.766),
                    'Scale': VBase3(0.773, 0.773, 0.773),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/vegetation/gen_tree_b'
                    }
                },
                '1159808554.82kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(-46.878, 298.399, 33.572),
                    'Scale': VBase3(4.718, 4.718, 4.718),
                    'Visual': {
                        'Color': (0.4000000059604645, 0.4000000059604645,
                                  0.4000000059604645, 1.0),
                        'Model':
                        'models/props/rock_4_floor'
                    }
                },
                '1159808801.91kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(11.058, 0.0, 0.0),
                    'Pos': Point3(25.29, 310.044, -10.128),
                    'Scale': VBase3(1.122, 1.122, 1.122),
                    'Visual': {
                        'Model': 'models/props/mound_light_med'
                    }
                },
                '1159809088.41kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(64.69, -9.114, 38.091),
                    'Pos': Point3(91.719, 320.447, 56.257),
                    'Scale': VBase3(0.81, 0.81, 0.81),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/rock_group_2_sphere'
                    }
                },
                '1159809108.24kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, -40.398, 0.0),
                    'Pos': Point3(68.354, 367.771, 21.083),
                    'Scale': VBase3(2.398, 2.398, 2.398),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/rock_group_2_sphere'
                    }
                },
                '1159809191.47kmuller': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(66.68, 360.422, 28.137),
                    'Scale': VBase3(1.936, 1.936, 1.936),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/vegetation/gen_tree_a'
                    }
                },
                '1159809750.24kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(36.344, 0.0, 0.0),
                    'Pos': Point3(-150.182, 284.433, 35.556),
                    'Scale': VBase3(0.638, 0.638, 0.638),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_e'
                    }
                },
                '1159809773.05kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(-176.594, 0.0, 0.0),
                    'Pos': Point3(-56.8, 347.546, 18.756),
                    'Scale': VBase3(1.216, 1.216, 1.216),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_a'
                    }
                },
                '1159809939.04kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(38.122, 0.997, 15.621),
                    'Pos': Point3(87.827, 338.347, 43.079),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_f'
                    }
                },
                '1159810168.47kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-161.519, 0.0, 0.0),
                    'Pos': Point3(91.219, 38.666, 24.772),
                    'Scale': VBase3(3.902, 3.902, 3.902),
                    'Visual': {
                        'Model': 'models/props/rock_group_4_sphere'
                    }
                },
                '1159812067.85kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.847, 0.0, 0.0),
                    'Pos': Point3(-188.45, -213.776, 27.064),
                    'Scale': VBase3(0.43, 0.43, 0.43),
                    'Visual': {
                        'Model': 'models/vegetation/bush_i'
                    }
                },
                '1159812173.0kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-62.908, 19.034, 16.857),
                    'Pos': Point3(-212.63, -153.108, 52.036),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1159812223.8kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.378, 14.587, -7.248),
                    'Pos': Point3(-196.219, -217.006, 26.664),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rock_group_4_floor'
                    }
                },
                '1159812273.94kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(86.074, 8.015, -2.859),
                    'Pos': Point3(-299.491, -77.724, 57.469),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1159812329.64kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-80.966, 16.721, 4.683),
                    'Pos': Point3(-247.082, -112.864, 57.642),
                    'Scale': VBase3(1.819, 1.819, 1.819),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1159812384.66kmuller': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-252.112, -132.109, 48.897),
                    'Scale': VBase3(0.822, 0.822, 0.822),
                    'Visual': {
                        'Model': 'models/vegetation/bush_i'
                    }
                },
                '1159812656.82kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-116.023, 24.946, -18.809),
                    'Pos': Point3(-335.786, -76.784, 52.621),
                    'Scale': VBase3(4.449, 4.449, 4.449),
                    'Visual': {
                        'Model': 'models/props/rock_group_5_sphere'
                    }
                },
                '1159812708.97kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(36.99, -5.562, -4.527),
                    'Pos': Point3(-361.984, 13.21, -5.355),
                    'Scale': VBase3(8.631, 8.631, 8.631),
                    'Visual': {
                        'Color': (0.6705882549285889, 0.6705882549285889,
                                  0.6705882549285889, 1.0),
                        'Model':
                        'models/props/rock_group_3_sphere'
                    }
                },
                '1159814714.5kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(176.778, 22.743, -3.894),
                    'Pos': Point3(-65.084, 335.703, 29.852),
                    'Scale': VBase3(0.894, 0.894, 0.894),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1159814783.22kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-9.354, -35.868, -2.865),
                    'Pos': Point3(-63.517, 353.738, 20.357),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1159819753.96kmuller': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(115.525, 0.0, 1.451),
                    'Pos': Point3(-21.01, -139.996, 103.038),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/palm_leaf_b_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1159820042.97kmuller': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(467.778, 107.141, 25.246),
                    'Scale': VBase3(1.356, 1.356, 1.356),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/palm_leaf_a_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1159820087.38kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 0.0, 9.138),
                    'Pos': Point3(475.576, 102.853, 27.603),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1159820178.24kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 0.0, 9.138),
                    'Pos': Point3(460.584, 109.293, 28.609),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1159820306.86kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-51.943, 0.0, 0.0),
                    'Pos': Point3(258.881, -321.821, 33.683),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1159820328.55kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-128.738, 0.0, 0.0),
                    'Pos': Point3(254.1, -318.721, 34.735),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_f'
                    }
                },
                '1159820372.1kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-128.738, -13.356, -0.084),
                    'Pos': Point3(279.214, -347.268, 23.679),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_f'
                    }
                },
                '1159820467.16kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(163.803, -20.131, 0.0),
                    'Pos': Point3(193.28, -286.762, 54.438),
                    'Scale': VBase3(2.047, 2.047, 2.047),
                    'Visual': {
                        'Model': 'models/props/rock_group_3_sphere'
                    }
                },
                '1159820521.38kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(43.525, 8.369, -1.748),
                    'Pos': Point3(192.872, -284.627, 53.821),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_leaves'
                    }
                },
                '1159820544.63kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(109.042, 11.347, -7.123),
                    'Pos': Point3(194.502, -286.57, 52.933),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_leaves'
                    }
                },
                '1159821155.19kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(87.755, 2.718, 0.0),
                    'Pos': Point3(203.988, -245.912, 56.101),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_f'
                    }
                },
                '1159821184.77kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-102.246, -11.31, -3.197),
                    'Pos': Point3(197.977, -237.111, 57.174),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1159821255.02kmuller': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(-11.216, -0.799, 8.465),
                    'Pos': Point3(209.01, -232.51, 51.212),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/fern_leaf_a_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/fern_trunk_a_idle',
                        'Model': 'models/vegetation/fern_short_trunk_d_hi',
                        'PartName': 'trunk'
                    }
                },
                '1159821341.21kmuller': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(367.125, 181.357, 48.787),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/palm_leaf_b_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1159821381.68kmuller': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(2.12, 0.0, 0.0),
                    'Pos': Point3(358.179, 182.72, 53.266),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/fern_leaf_b_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/fern_trunk_a_idle',
                        'Model': 'models/vegetation/fern_trunk_b_hi',
                        'PartName': 'trunk'
                    }
                },
                '1159821449.39kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-42.971, -34.689, 15.005),
                    'Pos': Point3(368.039, 176.25, 51.189),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1159821504.97kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-8.487, -23.767, 16.603),
                    'Pos': Point3(361.676, 181.613, 53.312),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1159821539.46kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(-12.131, -17.119, 6.713),
                    'Pos': Point3(347.297, 188.563, 56.616),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1159822396.69kmuller': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(184.142, 250.274, 71.366),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_d'
                    }
                },
                '1159822453.88kmuller': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(484.603, 114.667, 17.269),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_e'
                    }
                },
                '1159822498.43kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-35.889, -19.917, 0.0),
                    'Pos': Point3(486.79, 97.751, 23.769),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1159823503.19kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-123.596, 0.0, 0.0),
                    'Pos': Point3(-204.617, 336.811, -59.27),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/mound_light_med'
                    }
                },
                '1159826560.75kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-27.273, -6.604, 12.575),
                    'Pos': Point3(185.669, 227.143, 72.26),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rock_group_2_floor'
                    }
                },
                '1159826605.86kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 8.144, 0.0),
                    'Pos': Point3(187.952, 214.812, 68.462),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1159826648.83kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, -2.983, 0.0),
                    'Pos': Point3(185.402, 251.315, 69.997),
                    'Scale': VBase3(0.401, 0.401, 0.401),
                    'Visual': {
                        'Model': 'models/vegetation/bush_i'
                    }
                },
                '1159826706.13kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(8.512, -5.819, 0.869),
                    'Pos': Point3(191.333, 249.819, 69.992),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rock_group_5_floor'
                    }
                },
                '1159827084.23kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-39.77, 0.0, 10.969),
                    'Pos': Point3(-313.101, -78.912, 60.218),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1159827151.34kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-69.277, 1.86, 4.904),
                    'Pos': Point3(-27.955, -122.044, 110.206),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1159827194.69kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(160.039, -12.502, -20.801),
                    'Pos': Point3(-22.702, -135.602, 107.363),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1159827293.19kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-0.563, 6.241, 7.712),
                    'Pos': Point3(76.331, -195.286, 56.012),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1159827323.89kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-5.138, 14.019, 17.371),
                    'Pos': Point3(79.282, -176.275, 60.144),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1159827433.94kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(45.58, 5.441, 0.0),
                    'Pos': Point3(67.603, -196.317, 58.222),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1159827751.34kmuller': {
                    'Type': 'Prop_Groups',
                    'Hpr': VBase3(60.287, 0.0, 0.0),
                    'Pos': Point3(411.49, 183.338, 75.91),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/prop_group01'
                    }
                },
                '1159827773.75kmuller': {
                    'Type': 'Prop_Groups',
                    'Hpr': VBase3(109.138, 0.0, 0.0),
                    'Pos': Point3(403.011, 178.893, 75.91),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.8500000238418579, 0.8199999928474426,
                                  0.7300000190734863, 1.0),
                        'Model':
                        'models/props/prop_group_A'
                    }
                },
                '1159827833.78kmuller': {
                    'Type': 'Crate',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(403.815, 181.844, 75.91),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.699999988079071, 0.7300000190734863,
                                  0.5799999833106995, 1.0),
                        'Model':
                        'models/props/crates_group_2'
                    }
                },
                '1159827876.98kmuller': {
                    'Type': 'Furniture',
                    'Hpr': VBase3(-145.221, 0.0, 0.0),
                    'Pos': Point3(389.397, 129.714, 75.91),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.7960784435272217, 0.7764706015586853,
                                  0.7019608020782471, 1.0),
                        'Model':
                        'models/props/bench'
                    }
                },
                '1159827903.44kmuller': {
                    'Type': 'Furniture',
                    'Hpr': VBase3(32.707, 0.0, 0.0),
                    'Pos': Point3(394.271, 122.577, 75.91),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.7058823704719543, 0.7882353067398071,
                                  0.6666666865348816, 1.0),
                        'Model':
                        'models/props/bench'
                    }
                },
                '1159827998.0kmuller': {
                    'Type': 'Furniture',
                    'Hpr': VBase3(37.743, 0.0, 0.0),
                    'Pos': Point3(391.822, 125.737, 75.91),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/table_bar_square'
                    }
                },
                '1159828030.8kmuller': {
                    'Type': 'Prop_Groups',
                    'Hpr': VBase3(-25.905, 0.0, 0.0),
                    'Pos': Point3(377.95, 142.431, 75.91),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/prop_group01'
                    }
                },
                '1159828201.78kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 0.0, 6.067),
                    'Pos': Point3(465.253, 55.653, 27.113),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1159828344.08kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-87.173, 0.0, 0.0),
                    'Pos': Point3(330.892, 154.941, 60.615),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1159828386.05kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(58.076, 1.617, 1.007),
                    'Pos': Point3(370.342, 135.758, 46.48),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_leaves'
                    }
                },
                '1159828411.23kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(18.434, 0.571, 0.0),
                    'Pos': Point3(159.237, -226.309, 61.708),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1159828441.53kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-117.172, -0.779, -0.4),
                    'Pos': Point3(147.033, -207.249, 62.23),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1159828498.22kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 0.0, -0.741),
                    'Pos': Point3(151.879, -215.029, 61.947),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rock_group_3_floor'
                    }
                },
                '1159828544.45kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(120.408, -25.837, -5.285),
                    'Pos': Point3(113.723, -317.952, 12.713),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1159828600.58kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(86.481, -23.93, -6.345),
                    'Pos': Point3(136.749, -311.776, 24.563),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1159828637.78kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(126.899, -325.687, 15.514),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1159828651.77kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(99.108, -13.292, 0.809),
                    'Pos': Point3(120.99, -302.217, 22.85),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_f'
                    }
                },
                '1159828984.64kmuller': {
                    'Type': 'Furniture',
                    'Hpr': VBase3(75.94, 0.0, 0.0),
                    'Pos': Point3(161.967, 220.075, 111.562),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bench'
                    }
                },
                '1159829030.14kmuller': {
                    'Type': 'Furniture',
                    'Hpr': VBase3(-123.404, 0.0, 0.0),
                    'Pos': Point3(155.981, 178.044, 92.52),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/chair_bar'
                    }
                },
                '1159830989.97kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(18.391, 0.0, 0.0),
                    'Pos': Point3(-157.11, -78.605, 71.481),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/mound_light_small'
                    }
                },
                '1159831127.78kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(97.739, 2.075, 14.42),
                    'Pos': Point3(-64.863, -139.701, 19.733),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/mound_light_med'
                    }
                },
                '1159831207.56kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-113.716, 0.0, 0.0),
                    'Pos': Point3(-99.249, -258.392, -128.399),
                    'Scale': VBase3(0.685, 0.685, 0.685),
                    'Visual': {
                        'Model': 'models/props/mound_light_lrg'
                    }
                },
                '1159831276.59kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(-108.252, -141.273, 28.97),
                    'Scale': VBase3(0.737, 0.737, 0.737),
                    'Visual': {
                        'Model': 'models/props/mound_light_med'
                    }
                },
                '1159831347.58kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(31.206, -1.822, 0.0),
                    'Pos': Point3(-207.837, -244.945, -59.017),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/mound_light_med'
                    }
                },
                '1159832143.33kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(42.755, 0.0, 0.0),
                    'Pos': Point3(2.128, 225.682, 109.946),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_d'
                    }
                },
                '1159832489.52kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(110.524, 0.0, 8.257),
                    'Pos': Point3(163.037, 52.918, -17.865),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/mound_light_small'
                    }
                },
                '1159832534.78kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(117.743, -33.477, -12.57),
                    'Pos': Point3(297.542, 129.293, -19.814),
                    'Scale': VBase3(0.817, 0.817, 0.817),
                    'Visual': {
                        'Model': 'models/props/mound_light_med'
                    }
                },
                '1159832722.92kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(105.568, -0.389, 0.108),
                    'Pos': Point3(442.51, 230.912, -69.489),
                    'Scale': VBase3(0.745, 0.745, 0.745),
                    'Visual': {
                        'Model': 'models/props/mound_light_med2'
                    }
                },
                '1159833586.94kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(50.779, 0.0, 0.0),
                    'Pos': Point3(-144.587, -312.324, -56.736),
                    'Scale': VBase3(0.601, 0.601, 0.601),
                    'Visual': {
                        'Color': (0.7176470756530762, 0.7176470756530762,
                                  0.7176470756530762, 1.0),
                        'Model':
                        'models/props/mound_light_med2'
                    }
                },
                '1159834163.33kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(166.234, 3.648, -5.821),
                    'Pos': Point3(592.769, 14.332, -16.615),
                    'Scale': VBase3(0.839, 0.839, 0.839),
                    'Visual': {
                        'Model': 'models/props/mound_light_small'
                    }
                },
                '1159834265.98kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(103.64, -2.721, -7.064),
                    'Pos': Point3(258.667, 135.252, 8.28),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/mound_light_small'
                    }
                },
                '1159834457.55kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(30.882, 0.0, 1.471),
                    'Pos': Point3(149.0, 142.897, 40.431),
                    'Scale': VBase3(0.554, 0.554, 0.554),
                    'Visual': {
                        'Color': (0.8999999761581421, 0.8999999761581421,
                                  0.699999988079071, 1.0),
                        'Model':
                        'models/vegetation/gen_tree_e'
                    }
                },
                '1159834611.28kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(47.935, 3.347, 0.0),
                    'Pos': Point3(165.714, 73.388, 7.98),
                    'Scale': VBase3(0.674, 0.674, 0.674),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1159912937.08kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(167.116, 7.695, 9.833),
                    'Pos': Point3(-176.683, 267.52, 38.502),
                    'Scale': VBase3(3.54, 3.54, 3.54),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/rock_group_5_sphere'
                    }
                },
                '1159912990.38kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-152.567, 8.94, 4.223),
                    'Pos': Point3(-187.428, 268.756, 31.111),
                    'Scale': VBase3(1.777, 1.777, 1.777),
                    'Visual': {
                        'Color': (0.8700000047683716, 1.0, 1.0, 1.0),
                        'Model': 'models/props/rock_group_4_sphere'
                    }
                },
                '1159913095.53kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-44.579, -9.046, -4.602),
                    'Pos': Point3(-140.682, 298.474, 33.247),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1159913183.77kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(0.0, -24.218, -8.714),
                    'Pos': Point3(-65.78, 345.019, 25.998),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1159913401.3kmuller': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(110.831, -3.394, 0.0),
                    'Pos': Point3(-202.798, 305.088, 18.795),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/palm_leaf_c_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1159913473.06kmuller': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(1.956, 0.0, -0.289),
                    'Pos': Point3(-189.168, 318.947, 17.287),
                    'Scale': VBase3(1.267, 1.267, 1.267),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/palm_leaf_b_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1159913539.72kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-43.296, -3.1, -17.568),
                    'Pos': Point3(-195.041, 309.961, 20.883),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1159913592.2kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-43.296, -3.1, -17.568),
                    'Pos': Point3(-224.083, 303.182, 11.905),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1159913595.05kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(18.381, -11.018, -6.88),
                    'Pos': Point3(-201.045, 300.626, 21.689),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1159913660.17kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-97.365, 17.154, -6.866),
                    'Pos': Point3(-186.627, 324.02, 17.8),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1159913690.28kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(48.941, -8.388, 9.337),
                    'Pos': Point3(-181.292, 283.792, 35.341),
                    'Scale': VBase3(0.725, 0.725, 0.725),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1159913748.98kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-154.032, 26.916, 4.68),
                    'Pos': Point3(-151.372, 373.87, 3.101),
                    'Scale': VBase3(1.387, 1.387, 1.387),
                    'Visual': {
                        'Color': (0.8700000047683716, 1.0, 1.0, 1.0),
                        'Model': 'models/props/rock_group_4_floor'
                    }
                },
                '1159913793.27kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-117.579, 26.127, -10.932),
                    'Pos': Point3(-29.31, 278.539, 75.934),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1159913823.23kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(30.575, -27.93, -3.844),
                    'Pos': Point3(-23.562, 278.278, 78.982),
                    'Scale': VBase3(1.144, 1.144, 1.144),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1159913908.91kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(7.595, -24.364, -2.264),
                    'Pos': Point3(-116.457, 326.733, 22.485),
                    'Scale': VBase3(1.387, 1.387, 1.387),
                    'Visual': {
                        'Color': (0.8700000047683716, 1.0, 1.0, 1.0),
                        'Model': 'models/props/rock_group_3_floor'
                    }
                },
                '1159913947.89kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-87.319, 0.0, -3.113),
                    'Pos': Point3(-115.845, 325.598, 22.084),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_leaves'
                    }
                },
                '1159913989.36kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(61.097, -8.618, -1.661),
                    'Pos': Point3(53.457, 371.094, 16.622),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_f'
                    }
                },
                '1159917200.94kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-26.538, 0.0, 0.0),
                    'Pos': Point3(396.6, 288.952, -54.291),
                    'Scale': VBase3(2.45, 2.45, 2.45),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/rock_3_sphere'
                    }
                },
                '1159917206.78kmuller': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(176.497, 293.636, 46.513),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rock_4_sphere'
                    }
                },
                '1159917616.31kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(81.42, 6.136, 3.088),
                    'Pos': Point3(568.159, -21.685, -6.078),
                    'Scale': VBase3(0.839, 0.839, 0.839),
                    'Visual': {
                        'Model': 'models/props/mound_light_small'
                    }
                },
                '1159917662.67kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(148.573, -7.706, -3.331),
                    'Pos': Point3(579.654, -7.339, -81.373),
                    'Scale': VBase3(0.839, 0.839, 0.839),
                    'Visual': {
                        'Model': 'models/props/mound_light_med2'
                    }
                },
                '1159917738.92kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(58.089, 0.0, 0.0),
                    'Pos': Point3(133.622, 62.732, 13.312),
                    'Scale': VBase3(4.566, 4.566, 4.566),
                    'Visual': {
                        'Model': 'models/props/rock_2_sphere'
                    }
                },
                '1159917787.83kmuller': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(144.995, 73.164, 14.415),
                    'Scale': VBase3(2.178, 2.178, 2.178),
                    'Visual': {
                        'Model': 'models/props/rock_1_sphere'
                    }
                },
                '1159917813.75kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(47.935, 0.0, 0.0),
                    'Pos': Point3(152.797, 74.686, 11.916),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_d'
                    }
                },
                '1159918638.5kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-164.953, 0.0, 0.0),
                    'Pos': Point3(149.991, 141.971, 42.132),
                    'Scale': VBase3(0.712, 0.712, 0.712),
                    'Visual': {
                        'Model': 'models/vegetation/bush_i'
                    }
                },
                '1159918680.19kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 12.568, 6.465),
                    'Pos': Point3(137.868, 138.017, 44.949),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1159918741.19kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-103.561, -6.367, 14.382),
                    'Pos': Point3(155.275, 137.902, 42.846),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rock_group_1_floor'
                    }
                },
                '1159918798.39kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(146.347, 0.0, 0.0),
                    'Pos': Point3(92.347, 50.207, 25.482),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_leaves'
                    }
                },
                '1159918978.5kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(154.542, 14.416, 1.551),
                    'Pos': Point3(105.949, -79.001, 6.427),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/mound_light_small'
                    }
                },
                '1159919310.08kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(99.949, 20.596, 0.0),
                    'Pos': Point3(275.573, -320.84, 31.628),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1159919559.91kmuller': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(-141.343, -90.859, 89.967),
                    'Scale': VBase3(1.299, 1.299, 1.299),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/palm_leaf_a_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1159919583.97kmuller': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(-60.644, 0.0, 0.0),
                    'Pos': Point3(-147.45, -100.54, 82.823),
                    'Scale': VBase3(0.894, 0.894, 0.894),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/palm_leaf_b_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1159919634.6kmuller': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(45.064, 0.0, 0.0),
                    'Pos': Point3(-186.163, -66.379, 83.155),
                    'Scale': VBase3(1.338, 1.338, 1.338),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/palm_leaf_b_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1159919687.5kmuller': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-68.744, -201.864, 66.476),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/fern_leaf_a_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/fern_trunk_a_idle',
                        'Model': 'models/vegetation/fern_trunk_c_hi',
                        'PartName': 'trunk'
                    }
                },
                '1159919795.94kmuller': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(0.0, 0.0, -1.68),
                    'Pos': Point3(30.606, 175.428, 84.544),
                    'Scale': VBase3(1.067, 1.067, 1.067),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/palm_leaf_a_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1159920106.33kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(-0.293, 3.062, 0.0),
                    'Pos': Point3(-58.034, -200.938, 70.547),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1159920148.22kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(0.925, 10.71, -9.065),
                    'Pos': Point3(-79.415, -211.143, 59.016),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1159920200.38kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(5.537, 27.77, -12.63),
                    'Pos': Point3(-70.865, -206.744, 63.862),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1159920269.8kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(117.464, -22.189, -17.828),
                    'Pos': Point3(-61.44, -203.152, 67.952),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1159920322.94kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(56.84, 7.568, -0.182),
                    'Pos': Point3(-81.338, -203.099, 62.548),
                    'Scale': VBase3(1.352, 1.352, 1.352),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1159920574.38kmuller': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(62.221, 0.0, 0.0),
                    'Pos': Point3(34.175, 190.252, 95.205),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/palm_leaf_b_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1159920599.42kmuller': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(-12.946, 4.002, -4.919),
                    'Pos': Point3(42.604, 187.594, 89.553),
                    'Scale': VBase3(0.855, 0.855, 0.855),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/palm_leaf_b_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1159921189.28kmuller': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-87.948, -2.131, -14.869),
                    'Pos': Point3(-71.205, 214.894, 72.706),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/mound_light_small'
                    }
                },
                '1159921248.73kmuller': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-58.488, 241.946, 70.98),
                    'Scale': VBase3(10.153, 10.153, 10.153),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/rock_3_sphere'
                    }
                },
                '1159921298.16kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(-64.364, -2.983, -6.19),
                    'Pos': Point3(-52.353, 257.554, 75.371),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_e'
                    }
                },
                '1159921345.22kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(0.0, -1.726, -0.862),
                    'Pos': Point3(-47.664, 236.709, 82.071),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1159921380.86kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(0.0, -0.465, 0.0),
                    'Pos': Point3(-38.168, 224.468, 90.676),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_b'
                    }
                },
                '1159921428.73kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(36.407, -8.748, 0.0),
                    'Pos': Point3(-44.119, 235.112, 85.168),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_f'
                    }
                },
                '1159921478.91kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(95.808, -20.747, 0.0),
                    'Pos': Point3(-37.562, 230.369, 90.373),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1159921592.83kmuller': {
                    'Type': 'Bush',
                    'Hpr': VBase3(25.997, -7.256, -6.681),
                    'Pos': Point3(-32.695, 215.169, 94.173),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1159921717.38kmuller': {
                    'Type': 'Tree',
                    'Hpr': VBase3(122.231, -0.854, -2.306),
                    'Pos': Point3(380.527, 185.392, 36.331),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_e'
                    }
                }
            },
            'Visual': {
                'Model': 'models/islands/pvpcove_zero'
            }
        }
    },
    'Node Links': [],
    'Layers': {},
    'ObjectIds': {
        '1151689233.71hreister':
        '["Objects"]["1151689233.71hreister"]',
        '1151689490.21hreister':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1151689490.21hreister"]',
        '1151690471.18hreister':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1151690471.18hreister"]',
        '1156210410.53bbathen':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1156210410.53bbathen"]',
        '1156210474.53bbathen':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1156210474.53bbathen"]',
        '1156271007.17bbathen':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1156271007.17bbathen"]',
        '1156272251.25bbathen':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1156272251.25bbathen"]',
        '1156356079.1bbathen':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1156356079.1bbathen"]',
        '1159462943.35kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159462943.35kmuller"]',
        '1159552023.43kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159552023.43kmuller"]',
        '1159552271.06kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159552271.06kmuller"]',
        '1159552371.25kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159552371.25kmuller"]',
        '1159552461.11kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159552461.11kmuller"]',
        '1159552660.83kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159552660.83kmuller"]',
        '1159552691.26kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159552691.26kmuller"]',
        '1159552807.56kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159552807.56kmuller"]',
        '1159555763.83kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159555763.83kmuller"]',
        '1159555884.76kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159555884.76kmuller"]',
        '1159556024.17kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159556024.17kmuller"]',
        '1159567540.84kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159567540.84kmuller"]',
        '1159567716.55kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159567716.55kmuller"]',
        '1159567796.47kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159567796.47kmuller"]',
        '1159568081.89kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159568081.89kmuller"]',
        '1159568276.33kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159568276.33kmuller"]',
        '1159568349.97kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159568349.97kmuller"]',
        '1159568456.23kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159568456.23kmuller"]',
        '1159569544.56kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159569544.56kmuller"]',
        '1159569614.05kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159569614.05kmuller"]',
        '1159569712.45kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159569712.45kmuller"]',
        '1159569773.83kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159569773.83kmuller"]',
        '1159569900.09kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159569900.09kmuller"]',
        '1159570204.98kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159570204.98kmuller"]',
        '1159570260.37kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159570260.37kmuller"]',
        '1159571261.97kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159571261.97kmuller"]',
        '1159571492.72kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159571492.72kmuller"]',
        '1159571614.58kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159462943.35kmuller"]["Objects"]["1159571614.58kmuller"]',
        '1159572021.7kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159572021.7kmuller"]',
        '1159572104.36kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159572104.36kmuller"]',
        '1159572148.33kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159572148.33kmuller"]',
        '1159572175.89kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159572175.89kmuller"]',
        '1159572361.37kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159572361.37kmuller"]',
        '1159572620.67kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159572620.67kmuller"]',
        '1159572763.56kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159572763.56kmuller"]',
        '1159572937.51kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159572937.51kmuller"]',
        '1159572983.98kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159572983.98kmuller"]',
        '1159573082.42kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159573082.42kmuller"]',
        '1159573356.83kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159573356.83kmuller"]',
        '1159573502.25kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159573502.25kmuller"]',
        '1159573636.08kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159573636.08kmuller"]',
        '1159573702.3kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159573702.3kmuller"]',
        '1159573798.31kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159573798.31kmuller"]',
        '1159573818.67kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159573818.67kmuller"]',
        '1159574029.58kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159574029.58kmuller"]',
        '1159574144.55kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159574144.55kmuller"]',
        '1159574235.97kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159574235.97kmuller"]',
        '1159574274.31kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159574274.31kmuller"]',
        '1159574356.55kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159574356.55kmuller"]',
        '1159574445.28kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159574445.28kmuller"]',
        '1159574480.65kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159574480.65kmuller"]',
        '1159574574.47kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159574574.47kmuller"]',
        '1159574802.43kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159574802.43kmuller"]',
        '1159575469.14kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159575469.14kmuller"]',
        '1159576451.58kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159576451.58kmuller"]',
        '1159576510.05kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159576510.05kmuller"]',
        '1159576548.67kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159576510.05kmuller"]["Objects"]["1159576548.67kmuller"]',
        '1159576738.75kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159576738.75kmuller"]',
        '1159576857.62kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159576857.62kmuller"]',
        '1159576923.68kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159576923.68kmuller"]',
        '1159577147.55kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159577147.55kmuller"]',
        '1159577236.53kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159577236.53kmuller"]',
        '1159577268.76kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159577268.76kmuller"]',
        '1159577448.97kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159577448.97kmuller"]',
        '1159577833.43kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159462943.35kmuller"]["Objects"]["1159577833.43kmuller"]',
        '1159577902.76kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159462943.35kmuller"]["Objects"]["1159577902.76kmuller"]',
        '1159578015.84kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159462943.35kmuller"]["Objects"]["1159578015.84kmuller"]',
        '1159808554.82kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159808554.82kmuller"]',
        '1159808801.91kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159808801.91kmuller"]',
        '1159809088.41kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159809088.41kmuller"]',
        '1159809108.24kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159809108.24kmuller"]',
        '1159809191.47kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159809191.47kmuller"]',
        '1159809750.24kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159809750.24kmuller"]',
        '1159809773.05kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159809773.05kmuller"]',
        '1159809939.04kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159809939.04kmuller"]',
        '1159810168.47kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159810168.47kmuller"]',
        '1159812067.85kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159812067.85kmuller"]',
        '1159812173.0kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159812173.0kmuller"]',
        '1159812223.8kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159812223.8kmuller"]',
        '1159812273.94kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159812273.94kmuller"]',
        '1159812329.64kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159812329.64kmuller"]',
        '1159812384.66kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159812384.66kmuller"]',
        '1159812656.82kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159812656.82kmuller"]',
        '1159812708.97kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159812708.97kmuller"]',
        '1159814714.5kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159814714.5kmuller"]',
        '1159814783.22kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159814783.22kmuller"]',
        '1159819753.96kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159819753.96kmuller"]',
        '1159820042.97kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159820042.97kmuller"]',
        '1159820087.38kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159820087.38kmuller"]',
        '1159820178.24kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159820178.24kmuller"]',
        '1159820306.86kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159820306.86kmuller"]',
        '1159820328.55kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159820328.55kmuller"]',
        '1159820372.1kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159820372.1kmuller"]',
        '1159820467.16kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159820467.16kmuller"]',
        '1159820521.38kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159820521.38kmuller"]',
        '1159820544.63kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159820544.63kmuller"]',
        '1159821155.19kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159821155.19kmuller"]',
        '1159821184.77kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159821184.77kmuller"]',
        '1159821255.02kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159821255.02kmuller"]',
        '1159821341.21kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159821341.21kmuller"]',
        '1159821381.68kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159821381.68kmuller"]',
        '1159821449.39kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159821449.39kmuller"]',
        '1159821504.97kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159821504.97kmuller"]',
        '1159821539.46kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159821539.46kmuller"]',
        '1159822396.69kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159822396.69kmuller"]',
        '1159822453.88kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159822453.88kmuller"]',
        '1159822498.43kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159822498.43kmuller"]',
        '1159823503.19kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159823503.19kmuller"]',
        '1159826560.75kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159826560.75kmuller"]',
        '1159826605.86kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159826605.86kmuller"]',
        '1159826648.83kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159826648.83kmuller"]',
        '1159826706.13kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159826706.13kmuller"]',
        '1159827084.23kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159827084.23kmuller"]',
        '1159827151.34kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159827151.34kmuller"]',
        '1159827194.69kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159827194.69kmuller"]',
        '1159827293.19kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159827293.19kmuller"]',
        '1159827323.89kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159827323.89kmuller"]',
        '1159827433.94kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159827433.94kmuller"]',
        '1159827751.34kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159827751.34kmuller"]',
        '1159827773.75kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159827773.75kmuller"]',
        '1159827833.78kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159827833.78kmuller"]',
        '1159827876.98kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159827876.98kmuller"]',
        '1159827903.44kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159827903.44kmuller"]',
        '1159827998.0kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159827998.0kmuller"]',
        '1159828030.8kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159828030.8kmuller"]',
        '1159828201.78kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159828201.78kmuller"]',
        '1159828247.64kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159577147.55kmuller"]["Objects"]["1159828247.64kmuller"]',
        '1159828344.08kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159828344.08kmuller"]',
        '1159828386.05kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159828386.05kmuller"]',
        '1159828411.23kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159828411.23kmuller"]',
        '1159828441.53kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159828441.53kmuller"]',
        '1159828498.22kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159828498.22kmuller"]',
        '1159828544.45kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159828544.45kmuller"]',
        '1159828600.58kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159828600.58kmuller"]',
        '1159828637.78kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159828637.78kmuller"]',
        '1159828651.77kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159828651.77kmuller"]',
        '1159828984.64kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159828984.64kmuller"]',
        '1159829030.14kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159829030.14kmuller"]',
        '1159830989.97kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159830989.97kmuller"]',
        '1159831127.78kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159831127.78kmuller"]',
        '1159831207.56kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159831207.56kmuller"]',
        '1159831276.59kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159831276.59kmuller"]',
        '1159831347.58kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159831347.58kmuller"]',
        '1159832143.33kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159832143.33kmuller"]',
        '1159832489.52kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159832489.52kmuller"]',
        '1159832534.78kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159832534.78kmuller"]',
        '1159832722.92kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159832722.92kmuller"]',
        '1159833586.94kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159833586.94kmuller"]',
        '1159834163.33kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159834163.33kmuller"]',
        '1159834265.98kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159834265.98kmuller"]',
        '1159834457.55kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159834457.55kmuller"]',
        '1159834611.28kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159834611.28kmuller"]',
        '1159912937.08kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159912937.08kmuller"]',
        '1159912990.38kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159912990.38kmuller"]',
        '1159913095.53kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159913095.53kmuller"]',
        '1159913183.77kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159913183.77kmuller"]',
        '1159913401.3kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159913401.3kmuller"]',
        '1159913473.06kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159913473.06kmuller"]',
        '1159913539.72kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159913539.72kmuller"]',
        '1159913592.2kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159913592.2kmuller"]',
        '1159913595.05kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159913595.05kmuller"]',
        '1159913660.17kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159913660.17kmuller"]',
        '1159913690.28kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159913690.28kmuller"]',
        '1159913748.98kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159913748.98kmuller"]',
        '1159913793.27kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159913793.27kmuller"]',
        '1159913823.23kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159913823.23kmuller"]',
        '1159913908.91kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159913908.91kmuller"]',
        '1159913947.89kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159913947.89kmuller"]',
        '1159913989.36kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159913989.36kmuller"]',
        '1159917200.94kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159917200.94kmuller"]',
        '1159917206.78kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159917206.78kmuller"]',
        '1159917616.31kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159917616.31kmuller"]',
        '1159917662.67kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159917662.67kmuller"]',
        '1159917738.92kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159917738.92kmuller"]',
        '1159917787.83kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159917787.83kmuller"]',
        '1159917813.75kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159917813.75kmuller"]',
        '1159918638.5kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159918638.5kmuller"]',
        '1159918680.19kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159918680.19kmuller"]',
        '1159918741.19kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159918741.19kmuller"]',
        '1159918798.39kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159918798.39kmuller"]',
        '1159918978.5kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159918978.5kmuller"]',
        '1159919310.08kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159919310.08kmuller"]',
        '1159919559.91kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159919559.91kmuller"]',
        '1159919583.97kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159919583.97kmuller"]',
        '1159919634.6kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159919634.6kmuller"]',
        '1159919687.5kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159919687.5kmuller"]',
        '1159919795.94kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159919795.94kmuller"]',
        '1159920106.33kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159920106.33kmuller"]',
        '1159920148.22kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159920148.22kmuller"]',
        '1159920200.38kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159920200.38kmuller"]',
        '1159920269.8kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159920269.8kmuller"]',
        '1159920322.94kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159920322.94kmuller"]',
        '1159920574.38kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159920574.38kmuller"]',
        '1159920599.42kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159920599.42kmuller"]',
        '1159921189.28kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159921189.28kmuller"]',
        '1159921248.73kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159921248.73kmuller"]',
        '1159921298.16kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159921298.16kmuller"]',
        '1159921345.22kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159921345.22kmuller"]',
        '1159921380.86kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159921380.86kmuller"]',
        '1159921428.73kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159921428.73kmuller"]',
        '1159921478.91kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159921478.91kmuller"]',
        '1159921592.83kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159921592.83kmuller"]',
        '1159921717.38kmuller':
        '["Objects"]["1151689233.71hreister"]["Objects"]["1159921717.38kmuller"]'
    }
}
