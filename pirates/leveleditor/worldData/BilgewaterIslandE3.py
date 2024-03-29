# Embedded file name: pirates.leveleditor.worldData.BilgewaterIslandE3
from pandac.PandaModules import Point3, VBase3
objectStruct = {
    'Locator Links':
    [['1144695643.19sdnaik', '1144695785.47sdnaik', 'Bi-directional'],
     ['1144696042.95sdnaik', '1144695785.52sdnaik', 'Bi-directional'],
     ['1144695645.11sdnaik', '1144696208.66sdnaik', 'Bi-directional'],
     ['1144696205.36sdnaik', '1144696039.86sdnaik', 'Bi-directional']],
    'Objects': {
        '1135280776.06dzlu': {
            'Type': 'Island',
            'Name': 'Bilgewater',
            'File': '',
            'Objects': {
                '1136404579.56dzlu': {
                    'Type': 'Tree',
                    'Hpr': VBase3(2.663, -0.096, 0.553),
                    'Pos': Point3(403.816, 350.182, 54.6),
                    'Scale': VBase3(1.089, 1.089, 1.089),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1136404859.58dzlu': {
                    'Type': 'Building Exterior',
                    'Name': '',
                    'File': '',
                    'Hpr': VBase3(34.746, 0.0, 0.0),
                    'Objects': {
                        '1136404859.58dzlu0': {
                            'Type': 'Locator Node',
                            'Name': 'portal_exterior_1',
                            'GridPos': Point3(122.084, 275.185, 69.834),
                            'Hpr': VBase3(90.0, 0.0, 0.0),
                            'Pos': Point3(-0.365, -5.213, 0.955),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(119.413, 279.676, 68.879),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/buildings/shanty_tavern_exterior'
                    }
                },
                '1136406042.12dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(173.346, 143.694, 67.69),
                    'Scale': VBase3(1.317, 1.317, 1.317),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136406067.58dzlu': {
                    'Type': 'Tree',
                    'Hpr': VBase3(-12.942, 8.128, 0.0),
                    'Pos': Point3(200.423, 159.059, 62.4),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136406102.08dzlu': {
                    'Type': 'Tree',
                    'Hpr': VBase3(-12.942, 8.128, 0.0),
                    'Pos': Point3(215.391, 154.899, 59.549),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_d'
                    }
                },
                '1136406300.36dzlu': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(0.0, 0.0, 1.721),
                    'Pos': Point3(59.236, 208.391, 82.052),
                    'Scale': VBase3(1.071, 1.071, 1.071),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/fern_leaf_a_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(0.8, 0.8, 0.8)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/fern_trunk_a_idle',
                        'Model': 'models/vegetation/fern_trunk_c_hi',
                        'PartName': 'trunk'
                    }
                },
                '1136406305.84dzlu': {
                    'Type': 'Tree',
                    'Hpr': VBase3(-23.829, 0.688, 1.364),
                    'Pos': Point3(150.04, 317.674, 79.666),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136406445.48dzlu': {
                    'Type': 'Tree',
                    'Hpr': VBase3(166.825, -5.383, 0.0),
                    'Pos': Point3(93.676, 264.385, 68.748),
                    'Scale': VBase3(0.683, 0.683, 0.683),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_e'
                    }
                },
                '1136406479.8dzlu': {
                    'Type': 'Tree',
                    'Hpr': VBase3(104.938, 0.0, 0.0),
                    'Pos': Point3(247.154, 246.016, 65.624),
                    'Scale': VBase3(0.534, 0.534, 0.534),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_b'
                    }
                },
                '1136406533.92dzlu': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(-26.442, 0.0, 0.0),
                    'Pos': Point3(200.046, 297.437, 71.405),
                    'Scale': VBase3(0.658, 0.658, 0.658),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/tree_b_leaf_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/tree_b_leaf_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/tree_b_trunk_idle',
                        'Model': 'models/vegetation/tree_b_trunk_hi',
                        'PartName': 'trunk'
                    }
                },
                '1136406575.75dzlu': {
                    'Type': 'Bush',
                    'Hpr': VBase3(20.412, 4.933, 0.0),
                    'Pos': Point3(131.267, 295.128, 68.431),
                    'Scale': VBase3(0.977, 0.977, 0.977),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1136409327.53dzlu': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(363.691, 143.859, 40.0),
                    'Scale': VBase3(0.684, 0.684, 0.684),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/palm_leaf_b_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(2.067, 2.067, 2.067)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1136414736.41dzlu': {
                    'Type':
                    'Barrel',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(172.45, -75.325, -36.31),
                    'Pos':
                    Point3(133.811, 287.074, 68.873),
                    'Scale':
                    VBase3(0.696, 0.696, 0.696),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1136414752.22dzlu': {
                    'Type':
                    'Barrel',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(129.214, 280.857, 68.498),
                    'Scale':
                    VBase3(0.704, 0.704, 0.704),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1136414754.64dzlu': {
                    'Type': 'Barrel',
                    'Color': (0.75, 1.0, 0.8500000238418579, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(147.939, 295.403, 69.313),
                    'Scale': VBase3(0.735, 0.735, 0.735),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1136414802.88dzlu': {
                    'Type':
                    'Barrel',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(129.344, 285.622, 67.917),
                    'Scale':
                    VBase3(0.682, 0.682, 0.682),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1136415300.0dzlu': {
                    'Type': 'Building Exterior',
                    'Name': '',
                    'File': '',
                    'Hpr': VBase3(0.0, 0.0, 2.81),
                    'Objects': {
                        '1136415300.02dzlu': {
                            'Type': 'Locator Node',
                            'Name': 'portal_exterior_1',
                            'GridPos': Point3(164.181, 287.652, 69.552),
                            'Hpr': VBase3(90.0, 0.0, 0.0),
                            'Pos': Point3(3.987, -20.033, 0.0),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1137810131.5dxschafe': {
                            'Type': 'Rock',
                            'GridPos': Point3(159.741, 297.17, 64.92),
                            'Hpr': VBase3(-129.852, 1.887, 4.019),
                            'Pos': Point3(-0.221, -10.515, -4.844),
                            'Scale': VBase3(1.864, 1.864, 1.864),
                            'Visual': {
                                'Model':
                                'models/props/zz_dont_use_rocks_Dk_group_3F'
                            }
                        }
                    },
                    'Pos': Point3(160.199, 307.685, 69.747),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/buildings/shanty_npc_house_combo_H'
                    }
                },
                '1136416540.86dzlu': {
                    'Type': 'Rock',
                    'Hpr': VBase3(32.191, -6.354, 2.169),
                    'Pos': Point3(91.467, 257.4, 69.194),
                    'Scale': VBase3(1.875, 1.875, 1.875),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1136420549.03dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(188.178, 324.745, 98.525),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136420576.11dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(209.0, 325.129, 84.89),
                    'Scale': VBase3(1.207, 1.207, 1.207),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136420634.92dzlu': {
                    'Type':
                    'Tree',
                    'Color': (0.7699999809265137, 0.7599999904632568,
                              0.6800000071525574, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(370.727, 155.896, 40.426),
                    'Scale':
                    VBase3(1.207, 1.207, 1.207),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136420641.61dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(400.973, 288.917, 40.433),
                    'Scale': VBase3(1.207, 1.207, 1.207),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136420648.19dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(388.322, 238.284, 40.315),
                    'Scale': VBase3(1.207, 1.207, 1.207),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136420854.45dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(67.719, 250.038, 92.994),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1136420887.45dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(75.96, 279.432, 97.902),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1136420904.83dzlu': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(85.396, 296.367, 91.405),
                    'Scale': VBase3(0.963, 0.963, 0.963),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/tree_b_leaf_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/tree_b_leaf_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/tree_b_trunk_idle',
                        'Model': 'models/vegetation/tree_b_trunk_hi',
                        'PartName': 'trunk'
                    }
                },
                '1136420928.28dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(107.657, 339.434, 93.724),
                    'Scale': VBase3(0.876, 0.876, 0.876),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1136420937.08dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(141.177, 343.079, 85.88),
                    'Scale': VBase3(1.514, 1.514, 1.514),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_c'
                    }
                },
                '1136420991.55dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(169.437, 335.044, 69.038),
                    'Scale': VBase3(1.623, 1.623, 1.623),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_d'
                    }
                },
                '1136421052.95dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(13.863, 200.999, 76.664),
                    'Scale': VBase3(1.623, 1.623, 1.623),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1136421055.25dzlu': {
                    'Type': 'Tree',
                    'Hpr': VBase3(22.902, 0.0, 0.0),
                    'Pos': Point3(108.869, 321.147, 84.642),
                    'Scale': VBase3(1.46, 1.46, 1.46),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_d'
                    }
                },
                '1136421148.39dzlu': {
                    'Type': 'Tree',
                    'Hpr': VBase3(49.454, 0.0, 0.0),
                    'Pos': Point3(70.616, 239.568, 78.013),
                    'Scale': VBase3(1.393, 1.393, 1.393),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_d'
                    }
                },
                '1136421203.13dzlu': {
                    'Type': 'Bush',
                    'Hpr': VBase3(56.01, 0.0, 0.0),
                    'Pos': Point3(75.221, 241.675, 74.58),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1136421219.05dzlu': {
                    'Type': 'Bush',
                    'Hpr': VBase3(56.01, 12.592, 0.0),
                    'Pos': Point3(78.854, 259.047, 72.827),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1136421281.41dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(90.383, 269.014, 69.957),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_b'
                    }
                },
                '1136421368.44dzlu': {
                    'Type': 'Tree',
                    'Hpr': VBase3(-25.704, 0.0, 0.0),
                    'Pos': Point3(74.886, 251.376, 74.867),
                    'Scale': VBase3(1.111, 1.111, 1.111),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_b'
                    }
                },
                '1136421438.67dzlu': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(-25.704, -2.14, 0.0),
                    'Pos': Point3(179.517, 307.771, 64.407),
                    'Scale': VBase3(0.642, 0.642, 0.642),
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
                        'Model': 'models/vegetation/fern_trunk_b_hi',
                        'PartName': 'trunk'
                    }
                },
                '1136421473.47dzlu': {
                    'Type': 'Tree',
                    'Hpr': VBase3(-26.442, 0.0, 0.0),
                    'Pos': Point3(218.475, 280.826, 72.573),
                    'Scale': VBase3(0.658, 0.658, 0.658),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1136421514.02dzlu': {
                    'Type': 'Tree',
                    'Hpr': VBase3(-26.442, 0.0, 0.0),
                    'Pos': Point3(216.024, 303.996, 92.276),
                    'Scale': VBase3(0.658, 0.658, 0.658),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1136421687.55dzlu': {
                    'Type': 'Tree',
                    'Hpr': VBase3(-26.442, 0.0, 0.0),
                    'Pos': Point3(249.865, 242.457, 65.217),
                    'Scale': VBase3(0.658, 0.658, 0.658),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1136421948.91dzlu': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(-139.059, 0.0, 0.0),
                    'Pos': Point3(252.904, 164.327, 57.011),
                    'Scale': VBase3(0.86, 0.86, 0.86),
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
                '1136422148.89dzlu': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(-139.059, 0.0, 0.0),
                    'Pos': Point3(256.994, 168.049, 40.356),
                    'Scale': VBase3(0.898, 0.898, 0.898),
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
                '1136422899.75dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-318.086, -17.05, 58.843),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_c'
                    }
                },
                '1136422912.8dzlu': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-333.065, 13.689, 61.986),
                    'Scale': VBase3(0.931, 0.931, 0.931),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/tree_b_leaf_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/tree_b_leaf_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/tree_b_trunk_idle',
                        'Model': 'models/vegetation/tree_b_trunk_hi',
                        'PartName': 'trunk'
                    }
                },
                '1136422914.53dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-341.62, 39.425, 71.681),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_c'
                    }
                },
                '1136422915.92dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-334.597, 68.079, 73.463),
                    'Scale': VBase3(0.814, 0.814, 0.814),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_c'
                    }
                },
                '1136422957.22dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-329.244, 84.973, 73.936),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_c'
                    }
                },
                '1136422965.06dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-307.154, 98.955, 68.566),
                    'Scale': VBase3(0.856, 0.856, 0.856),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_c'
                    }
                },
                '1136422976.59dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-293.534, 114.608, 70.311),
                    'Scale': VBase3(0.716, 0.716, 0.716),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_c'
                    }
                },
                '1136422988.91dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-282.99, 134.083, 69.246),
                    'Scale': VBase3(1.093, 1.093, 1.093),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_c'
                    }
                },
                '1136422998.09dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-325.465, 53.237, 71.877),
                    'Scale': VBase3(0.871, 0.871, 0.871),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136423046.98dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-355.318, 56.948, 68.487),
                    'Scale': VBase3(1.021, 1.021, 1.021),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136423079.63dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-246.916, 129.769, 68.805),
                    'Scale': VBase3(1.021, 1.021, 1.021),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136423080.58dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-230.297, 108.779, 67.016),
                    'Scale': VBase3(1.021, 1.021, 1.021),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136423081.72dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-221.659, 121.591, 65.577),
                    'Scale': VBase3(1.021, 1.021, 1.021),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136423082.23dzlu': {
                    'Type': 'Tree',
                    'Hpr': VBase3(0.0, 0.0, 5.526),
                    'Pos': Point3(-201.426, 125.418, 58.743),
                    'Scale': VBase3(1.353, 1.353, 1.353),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1136423086.17dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-255.273, 154.302, 67.747),
                    'Scale': VBase3(1.021, 1.021, 1.021),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136423086.81dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-251.325, 168.405, 56.891),
                    'Scale': VBase3(1.021, 1.021, 1.021),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136423088.36dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-345.562, 197.779, 10.918),
                    'Scale': VBase3(1.021, 1.021, 1.021),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1136423088.98dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-313.65, 220.709, 9.951),
                    'Scale': VBase3(1.021, 1.021, 1.021),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136423089.81dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-265.432, 220.819, 25.23),
                    'Scale': VBase3(1.021, 1.021, 1.021),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136423090.83dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-268.725, 254.541, 9.432),
                    'Scale': VBase3(1.021, 1.021, 1.021),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136423091.41dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-222.158, 255.714, 28.981),
                    'Scale': VBase3(1.021, 1.021, 1.021),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136423092.0dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-224.133, 277.276, 20.08),
                    'Scale': VBase3(1.021, 1.021, 1.021),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136423092.95dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-140.266, 238.109, 66.372),
                    'Scale': VBase3(1.021, 1.021, 1.021),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1136423094.05dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-288.795, 199.107, 25.184),
                    'Scale': VBase3(1.021, 1.021, 1.021),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1136423162.5dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-205.12, 201.085, 50.625),
                    'Scale': VBase3(1.021, 1.021, 1.021),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1136423193.16dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-142.348, 220.086, 59.771),
                    'Scale': VBase3(0.802, 0.802, 0.802),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_d'
                    }
                },
                '1136423237.13dzlu': {
                    'Type': 'Rock',
                    'Hpr': VBase3(61.841, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(-90.148, 171.2, 65.438),
                    'Scale': VBase3(3.74, 3.74, 3.74),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_1F'
                    }
                },
                '1136423297.98dzlu': {
                    'Type': 'Rock',
                    'Hpr': VBase3(123.683, -8.334, 0.0),
                    'Pos': Point3(-165.915, 110.31, 57.844),
                    'Scale': VBase3(3.596, 3.596, 3.596),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_2F'
                    }
                },
                '1136423371.34dzlu': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-46.859, 0.0, 0.0),
                    'Pos': Point3(-98.134, 151.375, 65.723),
                    'Scale': VBase3(2.538, 2.538, 2.538),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1136423530.52dzlu': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-90.227, 156.301, 65.94),
                    'Scale': VBase3(1.077, 1.077, 1.077),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1136423563.91dzlu': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-81.552, 183.878, 64.95),
                    'Scale': VBase3(1.077, 1.077, 1.077),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1136423575.09dzlu': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-110.862, 194.519, 63.947),
                    'Scale': VBase3(1.235, 1.235, 1.235),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1136423593.38dzlu': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-69.362, -0.015, 10.419),
                    'Pos': Point3(-91.611, 225.058, 63.942),
                    'Scale': VBase3(3.168, 3.168, 3.168),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_1F'
                    }
                },
                '1136423697.94dzlu': {
                    'Type': 'Building Exterior',
                    'Name': '',
                    'File': '',
                    'Hpr': VBase3(35.683, 0.0, 0.0),
                    'Objects': {
                        '1136423697.94dzlu0': {
                            'Type': 'Locator Node',
                            'Name': 'portal_exterior_1',
                            'GridPos': Point3(-52.837, 165.002, 65.316),
                            'Hpr': VBase3(90.0, 0.0, 0.0),
                            'Pos': Point3(3.987, -20.033, 0.0),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-67.761, 178.948, 65.316),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/buildings/shanty_npc_house_a_exterior'
                    }
                },
                '1136423796.89dzlu': {
                    'Type': 'Building Exterior',
                    'Name': '',
                    'File': '',
                    'Hpr': VBase3(-50.773, 0.0, 0.0),
                    'Objects': {
                        '1136423697.94dzlu0': {
                            'Type': 'Locator Node',
                            'Name': 'portal_exterior_1',
                            'Hpr': VBase3(90.0, 0.0, 0.0),
                            'Pos': Point3(3.987, -20.033, 0.0),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-35.105, 186.473, 65.452),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/buildings/shanty_npc_house_combo_H'
                    }
                },
                '1136423902.0dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-52.231, 214.415, 63.382),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_a'
                    }
                },
                '1136423939.44dzlu': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-72.897, 210.315, 63.599),
                    'Scale': VBase3(0.8, 0.8, 0.8),
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
                        'Model': 'models/vegetation/fern_trunk_b_hi',
                        'PartName': 'trunk'
                    }
                },
                '1136423964.42dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-65.731, 207.031, 63.756),
                    'Scale': VBase3(0.814, 0.814, 0.814),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1136424011.34dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-104.128, 227.307, 66.245),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1136424056.56dzlu': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-84.236, 256.568, 80.964),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/tree_b_leaf_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/tree_b_leaf_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/tree_b_trunk_idle',
                        'Model': 'models/vegetation/tree_b_trunk_hi',
                        'PartName': 'trunk'
                    }
                },
                '1136424058.66dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-56.034, 264.438, 76.238),
                    'Scale': VBase3(1.016, 1.016, 1.016),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1136424103.94dzlu': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-169.155, 230.339, 50.972),
                    'Scale': VBase3(1.536, 1.536, 1.536),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1136424157.73dzlu': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-36.215, 3.77, 12.806),
                    'Objects': {},
                    'Pos': Point3(-223.368, 67.591, 56.016),
                    'Scale': VBase3(5.733, 5.733, 5.733),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_1F'
                    }
                },
                '1136424231.09dzlu': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-124.586, 4.107, -1.112),
                    'Pos': Point3(-128.432, 208.129, 61.014),
                    'Scale': VBase3(3.736, 3.736, 3.736),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_1F'
                    }
                },
                '1136424617.58dzlu': {
                    'Type': 'Bush',
                    'Hpr': VBase3(162.321, -6.017, 0.0),
                    'Pos': Point3(81.796, -32.658, 5.647),
                    'Scale': VBase3(0.795, 0.795, 0.795),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1136424781.72dzlu': {
                    'Type': 'Rock',
                    'Hpr': VBase3(101.64, -5.044, 0.0),
                    'Pos': Point3(-125.18, 142.052, 62.164),
                    'Scale': VBase3(6.054, 6.054, 6.054),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_1F'
                    }
                },
                '1136425088.27dzlu': {
                    'Type': 'Rock',
                    'Hpr': VBase3(101.64, 0.0, -1.409),
                    'Pos': Point3(-285.726, -23.079, 42.889),
                    'Scale': VBase3(6.054, 6.054, 6.054),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_1F'
                    }
                },
                '1136425095.08dzlu': {
                    'Type': 'Rock',
                    'Hpr': VBase3(137.302, 0.0, -4.231),
                    'Pos': Point3(-257.906, 21.205, 45.301),
                    'Scale': VBase3(5.33, 5.33, 5.33),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1136425234.44dzlu': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-46.226, -2.464, 14.288),
                    'Pos': Point3(-298.578, -8.822, 51.166),
                    'Scale': VBase3(5.796, 5.796, 5.796),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1136426351.31dzlu': {
                    'Type': 'Bush',
                    'Hpr': VBase3(102.186, 0.0, -4.988),
                    'Pos': Point3(-202.537, 90.08, 58.885),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1136426380.89dzlu': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-39.706, 0.0, 0.0),
                    'Pos': Point3(-187.495, 109.671, 59.547),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1136426422.47dzlu': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-39.706, 0.0, 0.0),
                    'Pos': Point3(-182.428, 102.934, 59.167),
                    'Scale': VBase3(1.447, 1.447, 1.447),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1136426725.14dzlu': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-295.177, -50.724, 43.351),
                    'Scale': VBase3(0.643, 0.643, 0.643),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1136426742.25dzlu': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-14.234, 5.769, 5.441),
                    'Pos': Point3(-262.793, -60.813, 42.423),
                    'Scale': VBase3(0.721, 0.721, 0.721),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1137608568.63dxschafe': {
                    'Type': 'Building Exterior',
                    'Name': '',
                    'File': '',
                    'Hpr': VBase3(-138.392, 2.568, 0.243),
                    'Objects': {
                        '1137608568.63dxschafe0': {
                            'Type': 'Locator Node',
                            'Name': 'portal_exterior_1',
                            'GridPos': Point3(605.445, -113.763, 3.264),
                            'Hpr': VBase3(90.0, 0.0, 0.0),
                            'Pos': Point3(3.987, -20.033, 0.0),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1137609001.86dxschafe': {
                            'Type': 'Crate',
                            'GridPos': Point3(594.61, -185.924, 3.845),
                            'Hpr': VBase3(138.382, 0.13, 12.182),
                            'Pos': Point3(60.011, 26.706, -1.277),
                            'Scale': VBase3(1.471, 1.471, 1.471),
                            'Visual': {
                                'Model': 'models/props/crate'
                            }
                        }
                    },
                    'Pos': Point3(621.715, -126.079, 4.178),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/buildings/shanty_repairshop_exterior'
                    }
                },
                '1137608982.7dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(-21.492, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(403.256, -76.642, 5.398),
                    'Scale':
                    VBase3(1.168, 1.168, 1.168),
                    'Visual': {
                        'Color': (0.699999988079071, 0.699999988079071,
                                  0.699999988079071, 1.0),
                        'Model':
                        'models/props/crates_group_1'
                    }
                },
                '1137608998.2dxschafe': {
                    'Type': 'Crate',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(509.34, -140.291, 5.461),
                    'Scale': VBase3(0.821, 0.821, 0.821),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1137609097.92dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.800000011920929, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(138.38, 1.499, 1.331),
                    'Objects': {
                        '1137609514.7dxschafe': {
                            'Type': 'Barrel',
                            'GridPos': Point3(506.625, -144.242, 8.45),
                            'Hpr': VBase3(-138.398, 2.005, 0.0),
                            'Pos': Point3(-0.667, -0.48, 2.732),
                            'Scale': VBase3(0.46, 0.46, 0.46),
                            'Visual': {
                                'Model': 'models/props/barrel_worn'
                            }
                        }
                    },
                    'Pos':
                    Point3(506.118, -144.249, 5.597),
                    'Scale':
                    VBase3(0.979, 0.979, 0.979),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1137609219.8dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': VBase3(55.719, 0.096, -0.14),
                    'Pos': Point3(581.564, -149.437, 4.362),
                    'Scale': VBase3(0.617, 0.617, 0.617),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1137609321.42dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(399.365, -125.397, 5.239),
                    'Scale':
                    VBase3(0.464, 0.464, 0.464),
                    'Visual': {
                        'Model': 'models/props/barrel_grey'
                    }
                },
                '1137609327.59dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.800000011920929, 0.800000011920929,
                              0.800000011920929, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(406.372, -144.289, 5.244),
                    'Scale':
                    VBase3(0.464, 0.464, 0.464),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1137609343.8dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(404.221, -146.105, 5.231),
                    'Scale':
                    VBase3(0.464, 0.464, 0.464),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1137609378.0dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(401.059, -87.436, 5.781),
                    'Scale':
                    VBase3(0.464, 0.464, 0.464),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1137609393.08dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.800000011920929, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(405.148, -84.434, 5.167),
                    'Scale':
                    VBase3(0.464, 0.464, 0.464),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1137609442.59dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(402.522, -84.672, 5.856),
                    'Scale': VBase3(0.464, 0.464, 0.464),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1137609481.81dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(415.418, -72.834, 5.144),
                    'Scale':
                    VBase3(0.464, 0.464, 0.464),
                    'Visual': {
                        'Model': 'models/props/barrel_grey'
                    }
                },
                '1137609719.03dxschafe': {
                    'Type':
                    'Rock',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(0.078, 29.074, -0.623),
                    'Objects': {},
                    'Pos':
                    Point3(522.641, -56.074, 5.121),
                    'Scale':
                    VBase3(2.546, 2.546, 2.546),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1137609795.34dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(176.6, -25.642, 3.502),
                    'Objects': {},
                    'Pos': Point3(515.944, -47.882, 5.459),
                    'Scale': VBase3(3.436, 3.436, 3.436),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_2F'
                    }
                },
                '1137610057.31dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(23.741, 1.104, 16.377),
                    'Objects': {
                        '1137610163.19dxschafe': {
                            'Type': 'Rock',
                            'GridPos': Point3(525.904, -98.61, -7.573),
                            'Hpr': VBase3(23.741, 1.104, 1.461),
                            'Pos': Point3(-0.867, -1.907, 0.446),
                            'Scale': VBase3(1.076, 1.076, 1.076),
                            'Visual': {
                                'Model': 'models/props/zz_dont_use_rock_Dk_4F'
                            }
                        }
                    },
                    'Pos': Point3(529.677, -75.888, -12.738),
                    'Scale': VBase3(8.312, 8.312, 8.312),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_3F'
                    }
                },
                '1137610228.36dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(525.445, 43.801, 24.286),
                    'Scale': VBase3(3.035, 3.035, 3.035),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1137610308.83dxschafe': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {
                        '1137610374.89dxschafe': {
                            'Type': 'Rock',
                            'GridPos': Point3(506.502, 45.109, 34.318),
                            'Hpr': VBase3(77.469, 0.0, -7.6),
                            'Pos': Point3(3.193, -2.581, 0.927),
                            'Scale': VBase3(0.661, 0.661, 0.661),
                            'Visual': {
                                'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                            }
                        },
                        '1138062671.39dxschafe': {
                            'Type':
                            'Bush',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'GridPos':
                            Point3(490.311, 42.534, 33.924),
                            'Hpr':
                            VBase3(0.0, 15.413, 0.0),
                            'Pos':
                            Point3(-0.215, -3.123, 0.844),
                            'Scale':
                            VBase3(0.21, 0.21, 0.21),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1138062672.88dxschafe': {
                            'Type': 'Bush',
                            'GridPos': Point3(490.035, 48.558, 40.281),
                            'Hpr': VBase3(0.0, 15.413, 0.0),
                            'Pos': Point3(-0.273, -1.855, 2.182),
                            'Scale': VBase3(0.044, 0.044, 0.044),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1138062672.89dxschafe': {
                            'Type': 'Bush',
                            'GridPos': Point3(490.035, 48.558, 40.281),
                            'Hpr': VBase3(0.0, 15.413, 0.0),
                            'Pos': Point3(-0.273, -1.855, 2.182),
                            'Scale': VBase3(0.01, 0.01, 0.01),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1138062672.92dxschafe': {
                            'Type': 'Bush',
                            'GridPos': Point3(490.035, 48.558, 40.281),
                            'Hpr': VBase3(0.0, 15.413, 0.0),
                            'Pos': Point3(-0.273, -1.855, 2.182),
                            'Scale': VBase3(0.01, 0.01, 0.01),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1138062672.95dxschafe': {
                            'Type': 'Bush',
                            'GridPos': Point3(490.035, 48.558, 40.281),
                            'Hpr': VBase3(0.0, 15.413, 0.0),
                            'Pos': Point3(-0.273, -1.855, 2.182),
                            'Scale': VBase3(0.01, 0.01, 0.01),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1138062672.98dxschafe': {
                            'Type': 'Bush',
                            'GridPos': Point3(490.035, 48.558, 40.281),
                            'Hpr': VBase3(0.0, 15.413, 0.0),
                            'Pos': Point3(-0.273, -1.855, 2.182),
                            'Scale': VBase3(0.01, 0.01, 0.01),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1138062673.06dxschafe': {
                            'Type': 'Bush',
                            'GridPos': Point3(489.603, 42.619, 34.09),
                            'Hpr': VBase3(0.0, 15.413, 0.0),
                            'Pos': Point3(-0.364, -3.105, 0.879),
                            'Scale': VBase3(0.01, 0.01, 0.01),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1138062673.09dxschafe': {
                            'Type': 'Bush',
                            'GridPos': Point3(489.603, 42.619, 34.09),
                            'Hpr': VBase3(0.0, 15.413, 0.0),
                            'Pos': Point3(-0.364, -3.105, 0.879),
                            'Scale': VBase3(0.01, 0.01, 0.01),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        }
                    },
                    'Pos': Point3(491.332, 57.371, 29.914),
                    'Scale': VBase3(4.751, 4.751, 4.751),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1137610441.08dxschafe': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(523.827, -38.53, 4.696),
                    'Scale': VBase3(9.855, 9.855, 9.855),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_4F'
                    }
                },
                '1137610539.64dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 41.769, 0.0),
                    'Objects': {
                        '1137610581.83dxschafe': {
                            'Type': 'Rock',
                            'GridPos': Point3(654.392, 69.826, 34.564),
                            'Hpr': VBase3(5.219, -17.289, 43.15),
                            'Pos': Point3(1.814, 2.326, -1.444),
                            'Scale': VBase3(0.443, 0.443, 0.443),
                            'Visual': {
                                'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                            }
                        }
                    },
                    'Pos': Point3(643.628, 53.824, 31.761),
                    'Scale': VBase3(5.934, 5.934, 5.934),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_4F'
                    }
                },
                '1137610675.58dxschafe': {
                    'Type': 'Tree - Animated',
                    'Animate': 'models/vegetation/palm_trunk_a_idle',
                    'Hpr': VBase3(-17.959, 0.0, 2.477),
                    'Pos': Point3(647.922, 61.217, 33.406),
                    'Scale': VBase3(0.835, 0.835, 0.835),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Color': (1.0, 0.7942, 0.7942, 1.0),
                                'Model': 'models/vegetation/palm_leaf_c_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(1.7, 1.7, 1.7)
                            }
                        }
                    },
                    'Visual': {
                        'Animate':
                        'models/vegetation/palm_trunk_a_idle',
                        'Color': (0.800000011920929, 0.800000011920929,
                                  0.800000011920929, 1.0),
                        'Model':
                        'models/vegetation/palm_trunk_b_hi',
                        'PartName':
                        'trunk'
                    }
                },
                '1137611262.78dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(-50.23, 2.081, 20.443),
                    'Pos': Point3(639.71, 57.06, 36.736),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Color': (0.817, 0.932, 0.7942, 1.0),
                                'Model': 'models/vegetation/palm_leaf_a_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(1.12, 1.12, 1.12)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Color': (0.7942, 1.0, 0.972, 1.0),
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137611361.14dxschafe': {
                    'Type':
                    'Tree - Animated',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(82.113, 0.0, 0.0),
                    'Pos':
                    Point3(632.238, -48.605, 2.937),
                    'Scale':
                    VBase3(1.644, 1.644, 1.644),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Color': (1.0, 1.0, 0.972, 1.0),
                                'Model': 'models/vegetation/palm_leaf_c_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(1.63, 1.63, 1.63)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Color': (1.0, 1.0, 1.0, 1.0),
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137611475.77dxschafe': {
                    'Type': 'Tree - Animated',
                    'Animate': 'models/vegetation/palm_trunk_a_idle',
                    'Hpr': VBase3(-102.01, -0.356, 11.354),
                    'Pos': Point3(535.48, -89.642, -7.614),
                    'Scale': VBase3(1.829, 1.829, 1.829),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Color': (0.817, 0.724, 0.724, 1.0),
                                'Model': 'models/vegetation/palm_leaf_c_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(0.842, 0.842, 0.842)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Color': (0.882, 0.932, 0.932, 1.0),
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137611477.19dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(544.567, -87.541, -9.29),
                    'Scale': VBase3(2.222, 2.222, 2.222),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Color': (0.817, 0.932, 0.932, 1.0),
                                'Model': 'models/vegetation/palm_leaf_a_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(1.385, 1.385, 1.385)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Color': (1.0, 1.0, 1.0, 1.0),
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137611660.95dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(539.665, -72.072, -8.435),
                    'Scale': VBase3(1.377, 1.377, 1.377),
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
                '1137611716.44dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(0.0, 0.0, 6.353),
                    'Pos': Point3(685.004, -17.803, 2.67),
                    'Scale': VBase3(1.44, 1.44, 1.44),
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
                        'Color': (1.0, 1.0, 1.0, 1.0),
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137611840.97dxschafe': {
                    'Type': 'Tree - Animated',
                    'Animate': 'models/vegetation/palm_trunk_a_idle',
                    'Hpr': VBase3(1.615, 0.0, 0.0),
                    'Pos': Point3(649.143, -139.364, 4.873),
                    'Scale': VBase3(1.093, 1.093, 1.093),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/palm_leaf_c_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(2.042, 2.042, 2.042)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Model': 'models/vegetation/palm_trunk_b_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137612056.77dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-29.542, 16.094, 0.0),
                    'Pos': Point3(432.851, 65.573, 33.884),
                    'Scale': VBase3(3.045, 3.045, 3.045),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1137612099.81dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-5.272, 24.168, 4.871),
                    'Objects': {
                        '1137612114.77dxschafe': {
                            'Type': 'Rock',
                            'GridPos': Point3(242.92, 7.514, -3.025),
                            'Hpr': VBase3(0.0, -4.834, 0.0),
                            'Pos': Point3(-2.909, -2.714, -1.867),
                            'Scale': VBase3(2.707, 2.707, 2.707),
                            'Visual': {
                                'Model': 'models/props/zz_dont_use_rock_Dk_3F'
                            }
                        }
                    },
                    'Pos': Point3(254.264, 12.909, 6.101),
                    'Scale': VBase3(3.533, 3.533, 3.533),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1137612356.78dxschafe': {
                    'Type':
                    'Tree - Animated',
                    'Animate':
                    'models/vegetation/palm_trunk_a_idle',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.8999999761581421, 1.0),
                    'Hpr':
                    VBase3(-74.425, 8.936, 1.368),
                    'Pos':
                    Point3(245.537, 17.033, 9.217),
                    'Scale':
                    VBase3(1.263, 1.263, 1.263),
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
                '1137612363.58dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(264.778, 22.222, 11.369),
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
                '1137612448.58dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(604.551, -182.933, 5.329),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach_small'],
                                'Model': 'models/vegetation/fern_leaf_b_hi',
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
                '1137612618.48dxschafe': {
                    'Type':
                    'Bush',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(-57.19, 2.939, 4.547),
                    'Pos':
                    Point3(509.249, 36.357, 30.025),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137612642.58dxschafe': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(451.226, 61.027, 33.652),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137612699.33dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-129.2, 0.0, 0.0),
                    'Pos': Point3(524.211, 49.18, 35.182),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137612755.67dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(76.488, 0.0, -11.539),
                    'Pos': Point3(385.7, 79.56, 38.412),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1137612764.56dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-129.2, 0.0, 0.0),
                    'Pos': Point3(300.36, 146.198, 48.732),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1137612843.73dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-16.717, 15.601, 0.0),
                    'Pos': Point3(377.716, 77.333, 37.228),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1137612891.16dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(0.0, 20.0, 0.0),
                    'Pos': Point3(373.49, 83.159, 37.578),
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
                        'Model': 'models/vegetation/fern_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137612944.11dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(516.995, 44.043, 32.282),
                    'Scale': VBase3(2.302, 2.302, 2.302),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach_small'],
                                'Model': 'models/vegetation/fern_leaf_b_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(0.5, 0.5, 0.5)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/fern_trunk_a_idle',
                        'Model': 'models/vegetation/fern_short_trunk_e_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137612995.44dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.800000011920929, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(165.452, 0.0, 0.0),
                    'Pos':
                    Point3(459.505, 61.885, 35.936),
                    'Scale':
                    VBase3(1.54, 1.54, 1.54),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_b'
                    }
                },
                '1137613150.16dxschafe': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(578.166, 57.511, 37.585),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_a'
                    }
                },
                '1137613211.3dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 3.981, 0.0),
                    'Pos': Point3(574.828, 49.066, 34.979),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1137613268.47dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-45.649, 0.0, 0.0),
                    'Pos': Point3(564.739, 54.009, 36.788),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137613342.45dxschafe': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(633.343, 58.63, 37.87),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137613458.7dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(19.832, 12.649, -0.051),
                    'Pos': Point3(454.592, 11.246, 21.082),
                    'Scale': VBase3(1.384, 1.384, 1.384),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1137613527.63dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(103.569, 0.0, -6.402),
                    'Pos': Point3(583.57, 52.104, 34.897),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1137613863.39dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(39.459, 12.206, 0.0),
                    'Pos': Point3(307.363, 133.557, 46.876),
                    'Scale': VBase3(1.226, 1.226, 1.226),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1137613928.72dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(70.727, 12.991, -7.647),
                    'Pos': Point3(310.554, 200.559, 57.468),
                    'Scale': VBase3(1.226, 1.226, 1.226),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1137614133.34dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(2.487, 16.71, -2.956),
                    'Pos': Point3(312.233, 195.686, 49.809),
                    'Scale': VBase3(4.492, 4.492, 4.492),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_3F'
                    }
                },
                '1137614533.53dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(206.657, -107.246, 4.715),
                    'Scale': VBase3(0.521, 0.521, 0.521),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1137614544.45dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(203.91, -107.489, 4.759),
                    'Scale':
                    VBase3(0.66, 0.66, 0.66),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1137614600.94dxschafe': {
                    'Type': 'Crate',
                    'Hpr': VBase3(35.42, 22.201, -10.302),
                    'Objects': {},
                    'Pos': Point3(184.156, -101.631, 1.794),
                    'Scale': VBase3(1.914, 1.914, 1.914),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1137614646.88dxschafe': {
                    'Type': 'Crate',
                    'Color': (0.800000011920929, 0.800000011920929, 1.0, 1.0),
                    'Hpr': VBase3(63.228, 6.475, 12.246),
                    'Pos': Point3(174.329, -104.677, -0.668),
                    'Scale': VBase3(1.278, 1.278, 1.278),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1137696037.8dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-7.797, 18.741, 23.082),
                    'Pos': Point3(653.408, 57.229, 27.642),
                    'Scale': VBase3(7.832, 7.832, 7.832),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_4F'
                    }
                },
                '1137786448.86dxschafe': {
                    'Type': 'Crane',
                    'Hpr': VBase3(-2.93, 0.0, 0.0),
                    'Pos': Point3(453.079, -165.832, 5.283),
                    'Scale': VBase3(0.606, 0.606, 0.606),
                    'Visual': {
                        'Model': 'models/props/Crane'
                    }
                },
                '1137786628.98dxschafe': {
                    'Type': 'Cart',
                    'Hpr': VBase3(153.468, 0.0, 0.0),
                    'Pos': Point3(402.452, -135.299, 5.211),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cart_reg'
                    }
                },
                '1137806137.89dxschafe': {
                    'Type': 'Sack',
                    'Hpr': VBase3(-45.821, -9.752, 2.229),
                    'Pos': Point3(110.652, 192.07, 74.847),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1137806149.67dxschafe': {
                    'Type': 'Sack',
                    'Color': (1.0, 1.0, 0.6000000238418579, 1.0),
                    'Hpr': VBase3(-60.62, -9.996, -0.323),
                    'Pos': Point3(112.146, 194.1, 75.476),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1137806158.56dxschafe': {
                    'Type':
                    'Sack',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(47.0, -19.144, 10.441),
                    'Pos':
                    Point3(109.907, 196.248, 75.73),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1137806228.33dxschafe': {
                    'Type': 'Sack',
                    'Hpr': VBase3(157.249, 14.314, -5.926),
                    'Pos': Point3(110.971, 193.898, 76.788),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1137806271.52dxschafe': {
                    'Type': 'Crate',
                    'Hpr': VBase3(0.789, -5.314, 8.461),
                    'Objects': {},
                    'Pos': Point3(114.71, 189.34, 74.676),
                    'Scale': VBase3(1.445, 1.445, 1.445),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1137806572.22dxschafe': {
                    'Type': 'LaundryRope',
                    'Hpr': VBase3(24.103, 0.0, 0.0),
                    'Pos': Point3(176.165, 151.12, 67.604),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/LaundryRope'
                    }
                },
                '1137807096.63dxschafe': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(271.29, 233.404, 60.473),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1137807403.13dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-1.762, 37.072, 11.793),
                    'Pos': Point3(155.527, 137.374, 67.343),
                    'Scale': VBase3(1.396, 1.396, 1.396),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1137807467.02dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 28.004, 0.0),
                    'Pos': Point3(152.086, 138.379, 68.776),
                    'Scale': VBase3(1.352, 1.352, 1.352),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1137807509.48dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(37.001, -2.419, -6.014),
                    'Pos': Point3(153.309, 139.437, 69.81),
                    'Scale': VBase3(1.668, 1.668, 1.668),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1137807585.05dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 31.381, 0.0),
                    'Pos': Point3(151.617, 128.671, 61.774),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137807622.05dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 11.578, 0.0),
                    'Pos': Point3(255.008, 163.079, 53.485),
                    'Scale': VBase3(1.358, 1.358, 1.358),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1137808334.67dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(156.524, 6.735, -3.327),
                    'Pos': Point3(81.083, 225.92, 74.175),
                    'Scale': VBase3(1.815, 1.815, 1.815),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1137809588.72dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(18.27, 0.0, 8.037),
                    'Pos': Point3(82.89, 221.067, 74.637),
                    'Scale': VBase3(1.381, 1.381, 1.381),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_2F'
                    }
                },
                '1137809702.98dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-15.281, 9.35, 7.783),
                    'Pos': Point3(83.71, 216.379, 75.663),
                    'Scale': VBase3(1.166, 1.166, 1.166),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1137809887.95dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 0.0, 16.083),
                    'Pos': Point3(84.826, 226.536, 74.615),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_f'
                    }
                },
                '1137810004.47dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(2.008, -8.135, 17.32),
                    'Objects': {},
                    'Pos': Point3(170.996, 297.092, 64.506),
                    'Scale': VBase3(1.464, 1.464, 1.464),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_2F'
                    }
                },
                '1137810301.38dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(101.767, 7.392, -9.082),
                    'Pos': Point3(160.95, 292.5, 67.989),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Lt_1F'
                    }
                },
                '1137810377.2dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(80.208, 1.871, 20.747),
                    'Pos': Point3(156.843, 292.649, 63.854),
                    'Scale': VBase3(2.416, 2.416, 2.416),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_3F'
                    }
                },
                '1137810791.5dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(36.141, 4.981, 1.142),
                    'Pos': Point3(179.255, 300.884, 65.077),
                    'Scale': VBase3(0.794, 0.794, 0.794),
                    'Visual': {
                        'Model': 'models/vegetation/bush_g'
                    }
                },
                '1137810869.36dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(92.017, -0.311, -3.75),
                    'Pos': Point3(188.585, 300.745, 65.061),
                    'Scale': VBase3(0.794, 0.794, 0.794),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137810917.73dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-100.05, 0.0, -1.001),
                    'Pos': Point3(209.087, 259.148, 65.756),
                    'Scale': VBase3(0.617, 0.617, 0.617),
                    'Visual': {
                        'Model': 'models/vegetation/bush_f'
                    }
                },
                '1137811234.52dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-60.422, -3.215, -1.431),
                    'Pos': Point3(116.413, 267.588, 69.0),
                    'Scale': VBase3(0.616, 0.616, 0.616),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1137811637.13dxschafe': {
                    'Type': 'Tree',
                    'Hpr': VBase3(0.021, -0.609, 2.011),
                    'Pos': Point3(143.132, -6.385, 12.14),
                    'Scale': VBase3(0.754, 0.754, 0.754),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_e'
                    }
                },
                '1137811756.92dxschafe': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(183.506, 103.712, 40.804),
                    'Scale': VBase3(0.61, 0.61, 0.61),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_e'
                    }
                },
                '1137811771.47dxschafe': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(233.507, 85.349, 29.792),
                    'Scale': VBase3(0.642, 0.642, 0.642),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_e'
                    }
                },
                '1137811785.95dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.4000000059604645, 0.4000000059604645,
                              0.4000000059604645, 1.0),
                    'Hpr':
                    VBase3(18.803, 0.0, 0.0),
                    'Pos':
                    Point3(118.642, 8.866, 9.653),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_e'
                    }
                },
                '1137811822.89dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(158.643, 0.0, 0.0),
                    'Pos':
                    Point3(137.764, 26.248, 15.209),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_e'
                    }
                },
                '1137811828.17dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.800000011920929, 0.800000011920929,
                              0.800000011920929, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(153.661, 3.854, 7.758),
                    'Scale':
                    VBase3(0.742, 0.742, 0.742),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_e'
                    }
                },
                '1137811838.45dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(164.425, 42.439, 23.135),
                    'Scale': VBase3(2.8, 2.8, 2.8),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach_small'],
                                'Model': 'models/vegetation/fern_leaf_b_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(0.5, 0.5, 0.5)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/fern_trunk_a_idle',
                        'Model': 'models/vegetation/fern_short_trunk_e_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137811843.08dxschafe': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(181.513, 74.315, 32.809),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_e'
                    }
                },
                '1137811850.0dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(44.813, 18.558, 0.0),
                    'Pos':
                    Point3(185.724, 54.738, 23.441),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_e'
                    }
                },
                '1137811916.13dxschafe': {
                    'Type': 'Tree',
                    'Color': (1.0, 0.800000011920929, 0.800000011920929, 1.0),
                    'Hpr': VBase3(25.01, 2.645, 5.649),
                    'Pos': Point3(167.47, 12.151, 13.284),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1137811971.63dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(115.197, -15.405, 10.068),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1137811974.33dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(59.433, -0.072, 0.122),
                    'Pos':
                    Point3(83.116, -38.217, 4.953),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1137811978.38dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(100.568, -11.018, 9.352),
                    'Scale':
                    VBase3(1.275, 1.275, 1.275),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1137811980.2dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(156.424, -2.016, -0.488),
                    'Pos': Point3(118.189, -32.226, 8.587),
                    'Scale': VBase3(1.191, 1.191, 1.191),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/fern_leaf_a_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(0.8, 0.8, 0.8)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/fern_trunk_a_idle',
                        'Model': 'models/vegetation/fern_trunk_c_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137811982.36dxschafe': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(187.795, 73.849, 32.771),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1137811983.89dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.800000011920929, 0.800000011920929,
                              0.800000011920929, 1.0),
                    'Hpr':
                    VBase3(21.755, 7.423, 0.0),
                    'Pos':
                    Point3(176.322, 49.117, 27.603),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1137811986.05dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(-38.185, -4.832, 0.0),
                    'Pos': Point3(135.026, 48.423, 20.353),
                    'Scale': VBase3(1.5, 1.5, 1.5),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/fern_leaf_a_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(0.8, 0.8, 0.8)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/fern_trunk_a_idle',
                        'Model': 'models/vegetation/fern_trunk_c_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137811999.59dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(155.213, 105.394, 49.23),
                    'Scale': VBase3(1.5, 1.5, 1.5),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/fern_leaf_a_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(0.8, 0.8, 0.8)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/fern_trunk_a_idle',
                        'Model': 'models/vegetation/fern_trunk_c_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137812004.25dxschafe': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(236.558, 162.018, 60.22),
                    'Scale': VBase3(0.625, 0.625, 0.625),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1137812037.88dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(-16.604, 0.0, 0.0),
                    'Pos': Point3(88.699, -5.145, 9.706),
                    'Scale': VBase3(0.625, 0.625, 0.625),
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
                        'Model': 'models/vegetation/fern_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137812040.5dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(37.879, 0.0, -5.207),
                    'Pos':
                    Point3(71.607, -65.78, 0.403),
                    'Scale':
                    VBase3(0.625, 0.625, 0.625),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_e'
                    }
                },
                '1137812042.97dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.800000011920929, 0.800000011920929,
                              0.800000011920929, 1.0),
                    'Hpr':
                    VBase3(53.217, 0.0, 0.0),
                    'Pos':
                    Point3(67.536, -35.952, 4.057),
                    'Scale':
                    VBase3(0.625, 0.625, 0.625),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1137812044.56dxschafe': {
                    'Type': 'Tree',
                    'Color': (0.5, 0.5, 0.5, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(98.684, -11.534, 9.149),
                    'Scale': VBase3(0.625, 0.625, 0.625),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1137812045.75dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.800000011920929, 0.800000011920929,
                              0.800000011920929, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(100.459, -38.081, 6.578),
                    'Scale':
                    VBase3(0.472, 0.472, 0.472),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_a'
                    }
                },
                '1137812047.31dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.800000011920929, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(128.899, -15.421, 11.175),
                    'Scale':
                    VBase3(0.751, 0.751, 0.751),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_a'
                    }
                },
                '1137812052.39dxschafe': {
                    'Type': 'Tree',
                    'Color': (0.9300000071525574, 0.75, 1.0, 1.0),
                    'Hpr': VBase3(0.0, 0.0, 9.009),
                    'Pos': Point3(164.334, 28.75, 20.793),
                    'Scale': VBase3(0.625, 0.625, 0.625),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1137812053.48dxschafe': {
                    'Type': 'Tree',
                    'Hpr': VBase3(27.803, 0.0, 4.559),
                    'Pos': Point3(177.847, 33.562, 23.11),
                    'Scale': VBase3(0.404, 0.404, 0.404),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_a'
                    }
                },
                '1137812055.06dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(27.635, 13.521, 0.0),
                    'Pos': Point3(164.35, 6.766, 14.768),
                    'Scale': VBase3(0.625, 0.625, 0.625),
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
                        'Model': 'models/vegetation/fern_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137812056.75dxschafe': {
                    'Type': 'Tree',
                    'Hpr': VBase3(23.766, 14.276, 0.0),
                    'Pos': Point3(199.268, 71.83, 31.474),
                    'Scale': VBase3(0.514, 0.514, 0.514),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1137812060.23dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(145.147, 1.301, 14.456),
                    'Scale': VBase3(0.938, 0.938, 0.938),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/fern_leaf_a_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(0.8, 0.8, 0.8)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/fern_trunk_a_idle',
                        'Model': 'models/vegetation/fern_trunk_c_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137812061.77dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(114.363, -6.835, 10.877),
                    'Scale': VBase3(0.938, 0.938, 0.938),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/fern_leaf_a_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(0.8, 0.8, 0.8)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/fern_trunk_a_idle',
                        'Model': 'models/vegetation/fern_trunk_c_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137812068.19dxschafe': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(167.467, 95.301, 43.265),
                    'Scale': VBase3(0.625, 0.625, 0.625),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1137812069.75dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(0.0, 0.0, 5.518),
                    'Pos':
                    Point3(173.193, 85.78, 37.736),
                    'Scale':
                    VBase3(0.625, 0.625, 0.625),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1137812071.73dxschafe': {
                    'Type': 'Tree',
                    'Hpr': VBase3(105.972, 3.074, -13.001),
                    'Pos': Point3(187.929, 143.05, 60.598),
                    'Scale': VBase3(0.888, 0.888, 0.888),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1137812077.53dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(162.601, 64.559, 30.041),
                    'Scale': VBase3(0.938, 0.938, 0.938),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/fern_leaf_a_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(0.8, 0.8, 0.8)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/fern_trunk_a_idle',
                        'Model': 'models/vegetation/fern_trunk_c_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137812079.69dxschafe': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(155.979, 63.358, 29.118),
                    'Scale': VBase3(0.625, 0.625, 0.625),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1137812083.2dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(0.0, 5.468, 0.0),
                    'Pos':
                    Point3(183.604, 10.487, 17.912),
                    'Scale':
                    VBase3(0.625, 0.625, 0.625),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1137812086.39dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.800000011920929, 0.800000011920929,
                              0.800000011920929, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(214.484, -2.972, 7.894),
                    'Scale':
                    VBase3(0.625, 0.625, 0.625),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1137812087.41dxschafe': {
                    'Type': 'Tree',
                    'Hpr': VBase3(0.0, 3.979, 0.0),
                    'Pos': Point3(159.588, -8.491, 11.996),
                    'Scale': VBase3(0.464, 0.464, 0.464),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1137812093.41dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(79.071, 9.826, -8.531),
                    'Pos': Point3(198.367, 98.869, 41.27),
                    'Scale': VBase3(0.938, 0.938, 0.938),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/fern_leaf_a_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(0.8, 0.8, 0.8)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/fern_trunk_a_idle',
                        'Model': 'models/vegetation/fern_trunk_c_hi',
                        'PartName': 'trunk'
                    }
                },
                '1137812094.86dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(56.461, 10.427, 6.841),
                    'Pos':
                    Point3(204.512, 74.527, 32.243),
                    'Scale':
                    VBase3(0.625, 0.625, 0.625),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_c'
                    }
                },
                '1137812153.95dxschafe': {
                    'Type':
                    'Bush',
                    'Color': (0.800000011920929, 0.800000011920929,
                              0.800000011920929, 1.0),
                    'Hpr':
                    VBase3(152.485, 0.0, 0.0),
                    'Pos':
                    Point3(114.867, -19.469, 9.626),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812161.56dxschafe': {
                    'Type': 'Bush',
                    'Color': (1.0, 1.0, 1.0, 1.0),
                    'Hpr': VBase3(105.956, 0.0, 0.0),
                    'Pos': Point3(108.358, -34.967, 2.463),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812163.47dxschafe': {
                    'Type':
                    'Bush',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(90.922, 0.0, 0.0),
                    'Pos':
                    Point3(68.255, -42.658, 3.113),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812165.38dxschafe': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(99.23, 11.426, 12.078),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812167.22dxschafe': {
                    'Type': 'Bush',
                    'Color': (0.5, 0.5, 0.5, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(138.243, 53.312, 22.685),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812169.88dxschafe': {
                    'Type': 'Bush',
                    'Color': (0.5, 0.5, 0.5, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(128.064, 51.263, 19.578),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812171.45dxschafe': {
                    'Type':
                    'Bush',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(119.202, 20.477, 14.257),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812172.67dxschafe': {
                    'Type':
                    'Bush',
                    'Color': (0.4000000059604645, 0.4000000059604645,
                              0.4000000059604645, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(107.747, 3.449, 11.51),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812177.41dxschafe': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(137.418, 73.96, 31.192),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812179.3dxschafe': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(150.857, 77.852, 33.589),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812182.5dxschafe': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(168.404, 105.877, 49.283),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812192.33dxschafe': {
                    'Type': 'Bush',
                    'Color': (0.800000011920929, 1.0, 0.6000000238418579, 1.0),
                    'Hpr': VBase3(-122.149, -0.165, -0.104),
                    'Pos': Point3(78.359, -41.748, 2.458),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812196.17dxschafe': {
                    'Type':
                    'Bush',
                    'Color': (0.4000000059604645, 0.4000000059604645,
                              0.4000000059604645, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(81.548, -11.728, 7.93),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812199.53dxschafe': {
                    'Type':
                    'Bush',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(87.826, -5.531, 9.201),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812203.89dxschafe': {
                    'Type':
                    'Bush',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(70.211, -19.024, 6.023),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812205.42dxschafe': {
                    'Type':
                    'Bush',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(56.411, -56.053, 1.608),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812210.59dxschafe': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(122.925, 35.976, 16.431),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812218.56dxschafe': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(141.104, 100.638, 46.824),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812221.2dxschafe': {
                    'Type':
                    'Bush',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(158.113, 69.423, 30.794),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812229.81dxschafe': {
                    'Type':
                    'Bush',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(102.812, -18.982, 8.717),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812264.89dxschafe': {
                    'Type': 'Bush',
                    'Color': (0.5, 0.5, 0.5, 1.0),
                    'Hpr': VBase3(0.0, 13.764, 0.0),
                    'Pos': Point3(151.144, 93.851, 44.047),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812267.86dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(-343.651, 152.496, 34.357),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812268.86dxschafe': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-350.298, 157.084, 26.102),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812273.73dxschafe': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(141.434, 92.017, 41.514),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812275.61dxschafe': {
                    'Type':
                    'Bush',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(0.0, 25.918, 0.0),
                    'Pos':
                    Point3(153.249, 86.998, 38.767),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812869.47dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 12.29, 0.0),
                    'Pos': Point3(438.737, 53.922, 34.043),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812873.55dxschafe': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(445.765, 42.046, 31.12),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812875.61dxschafe': {
                    'Type':
                    'Bush',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(455.821, 35.352, 29.891),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812877.02dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 10.201, 0.0),
                    'Pos': Point3(410.091, 70.824, 37.599),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812880.44dxschafe': {
                    'Type':
                    'Bush',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(0.0, 11.76, 0.0),
                    'Pos':
                    Point3(421.12, 57.182, 33.849),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812885.23dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 13.458, 0.0),
                    'Pos': Point3(446.718, 0.17, 19.269),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812886.06dxschafe': {
                    'Type':
                    'Bush',
                    'Color': (0.800000011920929, 0.800000011920929,
                              0.800000011920929, 1.0),
                    'Hpr':
                    VBase3(84.593, 1.488, -15.343),
                    'Pos':
                    Point3(428.072, 29.17, 26.188),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812887.13dxschafe': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(402.841, 56.533, 32.978),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1137812910.86dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(43.413, 14.224, -13.087),
                    'Pos': Point3(413.235, 47.42, 30.572),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1137812960.63dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(47.357, 13.397, -14.122),
                    'Pos': Point3(385.295, 66.392, 34.883),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1137812962.36dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-147.894, -9.683, 8.459),
                    'Pos': Point3(363.685, 83.306, 37.364),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1137812965.33dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(19.294, 17.241, -5.924),
                    'Pos': Point3(441.746, 28.19, 27.047),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1137812970.61dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.843, 0.0),
                    'Pos': Point3(459.286, 24.141, 26.913),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1137812972.64dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 12.481, 0.0),
                    'Pos': Point3(485.358, 40.065, 30.267),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1137812974.73dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(144.433, -11.35, -8.01),
                    'Pos': Point3(493.764, 32.292, 29.264),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1137812983.08dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(33.837, 11.43, -8.641),
                    'Pos': Point3(452.84, -29.124, 11.746),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1137812984.13dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 18.14, 0.0),
                    'Pos': Point3(454.798, -13.366, 15.893),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1137812990.39dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-8.912, 19.237, 2.958),
                    'Pos': Point3(368.932, 80.78, 37.733),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1137812992.0dxschafe': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(393.046, 73.868, 37.812),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1138062672.03dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(99.996, -2.74, -15.173),
                    'Pos': Point3(189.206, 33.693, 22.186),
                    'Scale': VBase3(0.641, 0.641, 0.641),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062672.0dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 13.851, 0.0),
                    'Pos': Point3(228.386, 3.241, 6.181),
                    'Scale': VBase3(0.672, 0.672, 0.672),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062672.14dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(155.012, -14.03, -6.446),
                    'Pos': Point3(257.277, 152.174, 52.716),
                    'Scale': VBase3(0.704, 0.704, 0.704),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062672.17dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-45.801, 10.879, 10.984),
                    'Pos': Point3(401.941, 44.342, 28.644),
                    'Scale': VBase3(0.574, 0.574, 0.574),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062672.28dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(266.105, 150.108, 50.152),
                    'Scale': VBase3(0.21, 0.21, 0.21),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062672.31dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(318.66, 129.493, 46.551),
                    'Scale': VBase3(0.71, 0.71, 0.71),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062672.34dxschafe': {
                    'Type': 'Bush',
                    'Color': (0.9300000071525574, 0.75, 1.0, 1.0),
                    'Hpr': VBase3(-5.49, 15.346, 1.457),
                    'Pos': Point3(129.682, -24.81, 9.442),
                    'Scale': VBase3(0.833, 0.833, 0.833),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062672.36dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(10.708, 11.018, -2.838),
                    'Pos': Point3(350.056, 96.558, 40.248),
                    'Scale': VBase3(0.499, 0.499, 0.499),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062672.48dxschafe': {
                    'Type': 'Bush',
                    'Color': (1.0, 0.75, 0.75, 1.0),
                    'Hpr': VBase3(78.676, 1.581, -7.845),
                    'Pos': Point3(141.164, -13.34, 12.205),
                    'Scale': VBase3(0.596, 0.596, 0.596),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062672.52dxschafe': {
                    'Type':
                    'Bush',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(0.0, 15.413, 0.0),
                    'Pos':
                    Point3(238.338, 153.972, 55.157),
                    'Scale':
                    VBase3(0.826, 0.826, 0.826),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062672.53dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(203.135, 75.305, 32.231),
                    'Scale': VBase3(0.479, 0.479, 0.479),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062672.56dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-29.304, 13.518, 7.474),
                    'Pos': Point3(268.568, 16.062, 8.792),
                    'Scale': VBase3(0.606, 0.606, 0.606),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062672.67dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(478.002, 60.873, 34.704),
                    'Scale': VBase3(0.21, 0.21, 0.21),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062672.69dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(478.002, 60.873, 34.704),
                    'Scale': VBase3(0.21, 0.21, 0.21),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062672.72dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(478.002, 60.873, 34.704),
                    'Scale': VBase3(0.21, 0.21, 0.21),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062672.75dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(478.002, 60.873, 34.704),
                    'Scale': VBase3(0.21, 0.21, 0.21),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062672.77dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(478.002, 60.873, 34.704),
                    'Scale': VBase3(0.21, 0.21, 0.21),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.13dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(489.602, 42.618, 34.09),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.16dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(489.602, 42.618, 34.09),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.22dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(485.219, 40.515, 30.348),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.25dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(485.219, 40.515, 30.348),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.28dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(485.219, 40.515, 30.348),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.31dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(485.219, 40.515, 30.348),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.38dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(482.278, 38.938, 29.893),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.41dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(482.278, 38.938, 29.893),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.44dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(482.278, 38.938, 29.893),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.45dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(482.278, 38.938, 29.893),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.53dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(478.659, 38.85, 29.697),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.55dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(478.659, 38.85, 29.697),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.58dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(478.659, 38.85, 29.697),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.66dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(477.106, 38.893, 29.629),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.67dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(477.106, 38.893, 29.629),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.78dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(473.399, 39.06, 29.479),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.7dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(477.106, 38.893, 29.629),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.83dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(473.399, 39.06, 29.479),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.89dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(472.939, 39.139, 29.472),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.8dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(473.399, 39.06, 29.479),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062673.92dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(472.939, 39.139, 29.472),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062674.02dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(475.071, 36.327, 36.247),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062674.05dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(475.071, 36.327, 36.247),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062674.08dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(475.071, 36.327, 36.247),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062674.19dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(475.071, 36.327, 36.247),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062674.22dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(475.071, 36.327, 36.247),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062674.25dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(475.071, 36.327, 36.247),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062674.28dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 15.413, 0.0),
                    'Pos': Point3(475.071, 36.327, 36.247),
                    'Scale': VBase3(0.01, 0.01, 0.01),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138062798.27dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(-42.408, 6.246, 5.675),
                    'Pos':
                    Point3(423.726, 39.144, 27.362),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1138062833.0dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(6.783, 8.373, -0.992),
                    'Pos':
                    Point3(399.838, 50.638, 29.772),
                    'Scale':
                    VBase3(0.791, 0.791, 0.791),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1138062835.84dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(53.184, 5.076, -6.741),
                    'Pos':
                    Point3(448.973, 14.864, 23.543),
                    'Scale':
                    VBase3(0.747, 0.747, 0.747),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1138062846.72dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(0.0, 8.431, 0.0),
                    'Pos':
                    Point3(388.006, 72.973, 37.103),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1138062881.41dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(0.0, 11.344, 0.0),
                    'Pos':
                    Point3(419.966, 64.807, 36.651),
                    'Scale':
                    VBase3(0.887, 0.887, 0.887),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1138062921.28dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(440.265, 37.857, 27.508),
                    'Scale':
                    VBase3(0.686, 0.686, 0.686),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_a'
                    }
                },
                '1138062964.36dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(410.114, 54.496, 32.622),
                    'Scale': VBase3(1.107, 1.107, 1.107),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/fern_leaf_a_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(0.8, 0.8, 0.8)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/fern_trunk_a_idle',
                        'Model': 'models/vegetation/fern_trunk_c_hi',
                        'PartName': 'trunk'
                    }
                },
                '1138063055.69dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(0.0, 0.0, -3.934),
                    'Pos': Point3(357.393, 87.403, 37.769),
                    'Scale': VBase3(1.5, 1.5, 1.5),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/fern_leaf_a_hi',
                                'PartName': 'leaf',
                                'Scale': VBase3(0.8, 0.8, 0.8)
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/fern_trunk_a_idle',
                        'Model': 'models/vegetation/fern_trunk_c_hi',
                        'PartName': 'trunk'
                    }
                },
                '1138063140.55dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(-48.982, 8.379, 0.0),
                    'Pos': Point3(368.466, 88.495, 38.52),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach_small'],
                                'Model': 'models/vegetation/fern_leaf_b_hi',
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
                '1138302709.13dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(440.393, -73.494, 5.268),
                    'Scale':
                    VBase3(1.238, 1.238, 1.238),
                    'Visual': {
                        'Model': 'models/props/crates_group_2'
                    }
                },
                '1138302819.44dxschafe': {
                    'Type': 'Crate',
                    'Color': (0.800000011920929, 1.0, 0.6000000238418579, 1.0),
                    'Hpr': VBase3(-29.228, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(450.406, -71.641, 5.221),
                    'Scale': VBase3(0.896, 0.896, 0.896),
                    'Visual': {
                        'Color': (1.0, 1.0, 1.0, 1.0),
                        'Model': 'models/props/crates_group_2'
                    }
                },
                '1138302833.38dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(454.463, -73.439, 5.227),
                    'Scale':
                    VBase3(1.028, 1.028, 1.028),
                    'Visual': {
                        'Model': 'models/props/crates_group_2'
                    }
                },
                '1138302835.94dxschafe': {
                    'Type': 'Crate',
                    'Color': (0.75, 0.9300000071525574, 1.0, 1.0),
                    'Hpr': VBase3(90.273, 0.0, 0.723),
                    'Objects': {},
                    'Pos': Point3(453.6, -80.003, 5.308),
                    'Scale': VBase3(0.856, 0.856, 0.856),
                    'Visual': {
                        'Model': 'models/props/crates_group_1'
                    }
                },
                '1138302857.72dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.8999999761581421, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(512.12, -90.447, 5.213),
                    'Scale':
                    VBase3(1.055, 1.055, 1.055),
                    'Visual': {
                        'Model': 'models/props/crates_group_2'
                    }
                },
                '1138302885.47dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(450.972, -140.916, 5.213),
                    'Scale':
                    VBase3(1.343, 1.343, 1.343),
                    'Visual': {
                        'Model': 'models/props/crate_group_net'
                    }
                },
                '1138302895.08dxschafe': {
                    'Type': 'Crate',
                    'Color': (0.5, 0.5, 0.5, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(341.413, -104.701, 4.452),
                    'Scale': VBase3(1.871, 1.871, 1.871),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138302898.14dxschafe': {
                    'Type': 'Crate',
                    'Color': (1.0, 1.0, 1.0, 1.0),
                    'Hpr': VBase3(27.107, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(359.274, -106.01, 4.189),
                    'Scale': VBase3(0.764, 0.764, 0.764),
                    'Visual': {
                        'Model': 'models/props/crates_group_2'
                    }
                },
                '1138302910.5dxschafe': {
                    'Type': 'Crate',
                    'Color': (0.75, 0.9300000071525574, 1.0, 1.0),
                    'Hpr': VBase3(-52.634, 0.0, 0.0),
                    'Objects': {
                        '1138320661.88dxschafe': {
                            'Type':
                            'Crate',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'GridPos':
                            Point3(500.065, -156.026, 13.599),
                            'Hpr':
                            VBase3(52.634, 0.0, 0.0),
                            'Pos':
                            Point3(-0.463, 0.444, 6.183),
                            'Scale':
                            VBase3(0.521, 0.521, 0.521),
                            'Visual': {
                                'Color':
                                (0.8999999761581421, 0.8999999761581421,
                                 0.699999988079071, 1.0),
                                'Model':
                                'models/props/crate'
                            }
                        }
                    },
                    'Pos': Point3(500.013, -156.485, 5.213),
                    'Scale': VBase3(1.017, 1.017, 1.017),
                    'Visual': {
                        'Model': 'models/props/crates_group_2'
                    }
                },
                '1138302929.81dxschafe': {
                    'Type': 'Crate',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(250.154, -105.8, 4.387),
                    'Scale': VBase3(1.225, 1.225, 1.225),
                    'Visual': {
                        'Model': 'models/props/crates_group_2'
                    }
                },
                '1138302931.58dxschafe': {
                    'Type': 'Crate',
                    'Color': (0.6000000238418579, 0.800000011920929, 1.0, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(268.979, -105.698, 4.387),
                    'Scale': VBase3(1.242, 1.242, 1.242),
                    'Visual': {
                        'Model': 'models/props/crates_group_2'
                    }
                },
                '1138302936.0dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(52.778, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(274.299, -105.963, 4.471),
                    'Scale':
                    VBase3(0.622, 0.622, 0.622),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138302984.48dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.800000011920929, 0.800000011920929,
                              0.800000011920929, 1.0),
                    'Hpr':
                    VBase3(-80.367, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(503.669, -150.116, 5.213),
                    'Scale':
                    VBase3(1.087, 1.087, 1.087),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/crates_group_1'
                    }
                },
                '1138302994.61dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.4000000059604645, 0.4000000059604645,
                              0.4000000059604645, 1.0),
                    'Hpr':
                    VBase3(2.181, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(244.263, -107.255, 4.387),
                    'Scale':
                    VBase3(0.958, 0.958, 0.958),
                    'Visual': {
                        'Model': 'models/props/crates_group_1'
                    }
                },
                '1138303002.52dxschafe': {
                    'Type': 'Crate',
                    'Color': (0.75, 0.9300000071525574, 1.0, 1.0),
                    'Hpr': VBase3(4.362, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(511.618, -104.554, 4.85),
                    'Scale': VBase3(1.077, 1.077, 1.077),
                    'Visual': {
                        'Model': 'models/props/crate_group_net'
                    }
                },
                '1138303005.69dxschafe': {
                    'Type': 'Crate',
                    'Hpr': VBase3(4.362, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(423.876, -162.984, 19.939),
                    'Scale': VBase3(0.865, 0.865, 0.865),
                    'Visual': {
                        'Model': 'models/props/crates_group_1'
                    }
                },
                '1138313303.97sdnaik': {
                    'Type': 'Island Game Area',
                    'File': 'BilgewaterCave1',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {
                        '1144696039.86sdnaik': {
                            'Type': 'Locator Node',
                            'Name': 'portal_interior_1',
                            'GridPos': Point3(-711.185, -553.42, 612.821),
                            'Hpr': VBase3(90.049, 0.0, 0.0),
                            'Pos': Point3(-152.635, -304.943, 170.576),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1144696042.95sdnaik': {
                            'Type': 'Locator Node',
                            'Name': 'portal_interior_2',
                            'GridPos': Point3(-372.751, 173.122, 657.362),
                            'Hpr': VBase3(-90.0, -2.136, 1.821),
                            'Pos': Point3(185.799, 421.599, 215.117),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-558.55, -248.477, 442.245),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/caves/cave_a_zero'
                    }
                },
                '1138320260.22dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(91.34, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(365.859, -105.024, 4.266),
                    'Scale':
                    VBase3(1.411, 1.411, 1.411),
                    'Visual': {
                        'Model': 'models/props/crate_group_net'
                    }
                },
                '1138320304.84dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Objects': {
                        '1138320526.06dxschafe': {
                            'Type':
                            'Crate',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'GridPos':
                            Point3(410.617, -74.702, 8.746),
                            'Hpr':
                            VBase3(34.943, 0.0, 0.0),
                            'Pos':
                            Point3(-0.09, -0.073, 2.82),
                            'Scale':
                            VBase3(0.504, 0.504, 0.504),
                            'Visual': {
                                'Model': 'models/props/crate'
                            }
                        }
                    },
                    'Pos':
                    Point3(410.727, -74.613, 5.311),
                    'Scale':
                    VBase3(1.218, 1.218, 1.218),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138320308.77dxschafe': {
                    'Type': 'Crate',
                    'Color': (0.5, 0.5, 0.5, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(442.39, -78.773, 5.228),
                    'Scale': VBase3(0.67, 0.67, 0.67),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138320333.78dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Objects': {
                        '1138320670.19dxschafe': {
                            'Type':
                            'Crate',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'GridPos':
                            Point3(511.163, -89.932, 9.058),
                            'Hpr':
                            VBase3(52.634, 0.0, 0.0),
                            'Pos':
                            Point3(0.567, -0.438, 2.714),
                            'Scale':
                            VBase3(0.471, 0.471, 0.471),
                            'Visual': {
                                'Model': 'models/props/crate'
                            }
                        }
                    },
                    'Pos':
                    Point3(512.822, -84.446, 5.169),
                    'Scale':
                    VBase3(1.402, 1.402, 1.402),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/crate'
                    }
                },
                '1138320357.89dxschafe': {
                    'Type': 'Crate',
                    'Color': (0.75, 0.9300000071525574, 1.0, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(425.623, -71.665, 5.074),
                    'Scale': VBase3(0.598, 0.598, 0.598),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/crate'
                    }
                },
                '1138320363.55dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(459.496, -79.334, 5.213),
                    'Scale':
                    VBase3(1.016, 1.016, 1.016),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138320366.47dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.800000011920929, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(-16.392, -0.075, 0.255),
                    'Objects': {},
                    'Pos':
                    Point3(506.659, -94.116, 5.257),
                    'Scale':
                    VBase3(0.93, 0.93, 0.93),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138320476.97dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(37.673, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(429.62, -81.564, 5.22),
                    'Scale':
                    VBase3(0.591, 0.591, 0.591),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138320490.22dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(455.279, -145.445, 5.213),
                    'Scale':
                    VBase3(0.507, 0.507, 0.507),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138320493.22dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(-30.13, 0.814, 0.473),
                    'Objects': {},
                    'Pos':
                    Point3(457.53, -140.353, 5.231),
                    'Scale':
                    VBase3(1.333, 1.333, 1.333),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138320513.19dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Objects': {
                        '1138320517.11dxschafe': {
                            'Type':
                            'Crate',
                            'Color': (0.6000000238418579, 0.6000000238418579,
                                      0.6000000238418579, 1.0),
                            'GridPos':
                            Point3(496.942, -151.738, 8.002),
                            'Hpr':
                            VBase3(72.454, 0.0, 0.0),
                            'Pos':
                            Point3(0.678, -0.596, 2.463),
                            'Scale':
                            VBase3(1.131, 1.131, 1.131),
                            'Visual': {
                                'Model': 'models/props/crate'
                            }
                        }
                    },
                    'Pos':
                    Point3(496.526, -151.372, 5.213),
                    'Scale':
                    VBase3(1.255, 1.255, 1.255),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138320636.58dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(22.185, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(372.261, -104.288, 4.359),
                    'Scale':
                    VBase3(0.831, 0.831, 0.831),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138320640.36dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(263.856, -106.875, 4.387),
                    'Scale':
                    VBase3(0.859, 0.859, 0.859),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138320649.98dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(435.669, -71.589, 5.251),
                    'Scale':
                    VBase3(1.231, 1.231, 1.231),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138320691.84dxschafe': {
                    'Type': 'Crate',
                    'Color': (1.0, 0.800000011920929, 0.6000000238418579, 1.0),
                    'Hpr': VBase3(52.634, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(419.389, -163.257, 19.676),
                    'Scale': VBase3(0.711, 0.711, 0.711),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138320711.06dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(105.268, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(449.902, -133.338, 5.213),
                    'Scale':
                    VBase3(0.587, 0.587, 0.587),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138320832.58dxschafe': {
                    'Type': 'Barrel',
                    'Color': (1.0, 0.800000011920929, 0.6000000238418579, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(455.589, -89.625, 5.213),
                    'Scale': VBase3(0.583, 0.583, 0.583),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1138320841.61dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(417.901, -70.931, 5.145),
                    'Scale': VBase3(0.583, 0.583, 0.583),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138320843.52dxschafe': {
                    'Type': 'Barrel',
                    'Color': (1.0, 1.0, 0.6000000238418579, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(459.965, -85.189, 5.213),
                    'Scale': VBase3(0.583, 0.583, 0.583),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138320844.67dxschafe': {
                    'Type': 'Barrel',
                    'Color': (0.800000011920929, 0.800000011920929, 1.0, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(453.505, -87.058, 5.213),
                    'Scale': VBase3(0.583, 0.583, 0.583),
                    'Visual': {
                        'Model': 'models/props/barrel_grey'
                    }
                },
                '1138320846.38dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(457.487, -86.106, 5.213),
                    'Scale':
                    VBase3(0.583, 0.583, 0.583),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138320920.13dxschafe': {
                    'Type': 'Barrel',
                    'Color': (0.800000011920929, 0.800000011920929, 1.0, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(451.206, -147.569, 5.213),
                    'Scale': VBase3(0.583, 0.583, 0.583),
                    'Visual': {
                        'Color': (0.63, 0.49, 0.0, 1.0),
                        'Model': 'models/props/barrel_grey'
                    }
                },
                '1138320920.5dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(451.667, -149.192, 5.213),
                    'Scale': VBase3(0.583, 0.583, 0.583),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138320920.92dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(453.402, -148.867, 5.213),
                    'Scale': VBase3(0.583, 0.583, 0.583),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138320921.48dxschafe': {
                    'Type': 'Barrel',
                    'Color': (0.5, 0.5, 0.5, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(453.165, -151.743, 5.213),
                    'Scale': VBase3(0.583, 0.583, 0.583),
                    'Visual': {
                        'Color': (0.79, 0.65, 0.45, 1.0),
                        'Model': 'models/props/barrel_grey'
                    }
                },
                '1138320922.39dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(454.774, -147.733, 5.213),
                    'Scale': VBase3(0.583, 0.583, 0.583),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1138320923.02dxschafe': {
                    'Type': 'Barrel',
                    'Color': (1.0, 1.0, 0.6000000238418579, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(454.812, -150.028, 5.213),
                    'Scale': VBase3(0.583, 0.583, 0.583),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138320941.11dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(488.065, -168.19, 5.213),
                    'Scale': VBase3(0.583, 0.583, 0.583),
                    'Visual': {
                        'Model': 'models/props/barrel_grey'
                    }
                },
                '1138320941.98dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(486.905, -164.617, 5.213),
                    'Scale': VBase3(0.583, 0.583, 0.583),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138320942.7dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(485.54, -166.86, 5.213),
                    'Scale': VBase3(0.583, 0.583, 0.583),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1138320943.48dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(485.433, -169.704, 5.213),
                    'Scale': VBase3(0.583, 0.583, 0.583),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138320944.53dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(493.72, -153.358, 5.213),
                    'Scale': VBase3(0.583, 0.583, 0.583),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138320945.41dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(487.432, -160.417, 5.213),
                    'Scale':
                    VBase3(0.583, 0.583, 0.583),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1138321117.05dxschafe': {
                    'Type': 'Crate',
                    'Color': (0.800000011920929, 0.800000011920929, 1.0, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {
                        '1138302961.81dxschafe': {
                            'Type': 'Crate',
                            'GridPos': Point3(259.842, -106.457, 4.851),
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(0.0, 0.0, 0.0),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/crates_group_2'
                            }
                        }
                    },
                    'Pos': Point3(259.842, -106.457, 4.851),
                    'Scale': VBase3(0.457, 0.457, 0.457),
                    'Visual': {
                        'Model': 'models/props/crates_group_2'
                    }
                },
                '1138321146.64dxschafe': {
                    'Type': 'Crate',
                    'Color': (0.800000011920929, 0.800000011920929, 1.0, 1.0),
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Objects': {
                        '1138302961.81dxschafe': {
                            'Type': 'Crate',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(0.0, 0.0, 0.0),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/crates_group_2'
                            }
                        }
                    },
                    'Pos': Point3(432.251, -72.03, 5.259),
                    'Scale': VBase3(0.822, 0.822, 0.822),
                    'Visual': {
                        'Model': 'models/props/crates_group_2'
                    }
                },
                '1138321241.02dxschafe': {
                    'Type': 'Crate',
                    'Color': (0.5, 0.5, 0.5, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(436.179, -71.498, 8.57),
                    'Scale': VBase3(0.953, 0.953, 0.953),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138321267.27dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(436.06, -74.608, 5.248),
                    'Scale': VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138321278.73dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.800000011920929, 0.800000011920929,
                              0.800000011920929, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(433.972, -74.829, 5.253),
                    'Scale':
                    VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1138321280.63dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(435.159, -80.581, 5.248),
                    'Scale':
                    VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel_grey'
                    }
                },
                '1138321281.98dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(433.236, -76.648, 5.253),
                    'Scale': VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138321296.0dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(483.9, -68.645, 5.213),
                    'Scale': VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138321296.64dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(483.441, -70.514, 5.213),
                    'Scale':
                    VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138321297.41dxschafe': {
                    'Type': 'Barrel',
                    'Color': (0.6000000238418579, 0.800000011920929, 1.0, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(487.344, -65.237, 5.213),
                    'Scale': VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1138321298.06dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': VBase3(0.0, -26.202, 0.0),
                    'Pos': Point3(481.041, -71.263, 5.213),
                    'Scale': VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138321298.98dxschafe': {
                    'Type': 'Barrel',
                    'Color': (0.800000011920929, 0.800000011920929, 1.0, 1.0),
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(481.767, -74.765, 5.215),
                    'Scale': VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel_grey'
                    }
                },
                '1138321299.7dxschafe': {
                    'Type': 'Barrel',
                    'Color': (1.0, 0.800000011920929, 0.6000000238418579, 1.0),
                    'Hpr': VBase3(0.0, 0.0, 18.203),
                    'Pos': Point3(480.12, -73.73, 5.545),
                    'Scale': VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1138321323.97dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(347.02, -105.281, 4.388),
                    'Scale': VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel_grey'
                    }
                },
                '1138321325.05dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(347.724, -107.647, 4.464),
                    'Scale':
                    VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1138321325.63dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(345.564, -106.827, 4.485),
                    'Scale': VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138321332.92dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(322.44, -122.968, 4.411),
                    'Scale':
                    VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1138321333.44dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.8999999761581421, 1.0),
                    'Hpr':
                    VBase3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(319.733, -123.477, 4.461),
                    'Scale':
                    VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1138321334.06dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(509.313, -82.634, 4.95),
                    'Scale':
                    VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1138321334.66dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(314.246, -123.538, 4.522),
                    'Scale': VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138321336.2dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(320.898, -125.417, 4.372),
                    'Scale':
                    VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1138321337.14dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(417.167, -74.791, 5.289),
                    'Scale': VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1138321337.91dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.8999999761581421, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(315.056, -125.343, 4.453),
                    'Scale':
                    VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138321347.94dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(259.078, -109.761, 4.387),
                    'Scale':
                    VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel_grey'
                    }
                },
                '1138321351.02dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(256.762, -109.232, 4.387),
                    'Scale': VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138321366.27dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': VBase3(64.1, 0.0, 0.0),
                    'Pos': Point3(504.711, -103.68, 5.213),
                    'Scale': VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel_group_1'
                    }
                },
                '1138321388.25dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': VBase3(143.685, 0.0, 0.0),
                    'Pos': Point3(504.847, -109.559, 5.213),
                    'Scale': VBase3(0.443, 0.443, 0.443),
                    'Visual': {
                        'Model': 'models/props/barrel_group_1'
                    }
                },
                '1138321521.69dxschafe': {
                    'Type':
                    'Crate',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(59.241, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(457.346, -79.553, 7.923),
                    'Scale':
                    VBase3(0.881, 0.881, 0.881),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138321535.25dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': VBase3(6.659, 0.0, 0.0),
                    'Pos': Point3(487.483, -79.886, 5.082),
                    'Scale': VBase3(0.446, 0.446, 0.446),
                    'Visual': {
                        'Model': 'models/props/barrel_group_1'
                    }
                },
                '1138322082.3dxschafe': {
                    'Type': 'Crane',
                    'Hpr': VBase3(93.687, 0.0, 0.0),
                    'Pos': Point3(239.242, -125.623, 4.066),
                    'Scale': VBase3(0.495, 0.495, 0.495),
                    'Visual': {
                        'Model': 'models/props/Crane'
                    }
                },
                '1138322153.2dxschafe': {
                    'Type':
                    'Rock',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(53.019, 3.91, -5.32),
                    'Objects': {},
                    'Pos':
                    Point3(326.352, -95.26, -0.157),
                    'Scale':
                    VBase3(1.154, 1.154, 1.154),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_LT_group_3F'
                    }
                },
                '1138322160.34dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 9.799, 0.0),
                    'Objects': {},
                    'Pos': Point3(369.578, -87.006, 0.551),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1138322161.17dxschafe': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(351.41, -95.478, -0.073),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1138322162.81dxschafe': {
                    'Type':
                    'Rock',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(-154.876, -13.398, -0.67),
                    'Objects': {},
                    'Pos':
                    Point3(361.653, -93.806, -0.671),
                    'Scale':
                    VBase3(1.319, 1.319, 1.319),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_LT_group_2F'
                    }
                },
                '1138322164.0dxschafe': {
                    'Type':
                    'Rock',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(55.496, 3.041, -5.889),
                    'Objects': {},
                    'Pos':
                    Point3(196.64, -96.134, 0.149),
                    'Scale':
                    VBase3(1.559, 1.559, 1.559),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_LT_group_2F'
                    }
                },
                '1138322170.58dxschafe': {
                    'Type': 'Rock',
                    'Color': (0.5, 0.5, 0.5, 1.0),
                    'Hpr': VBase3(0.0, 6.577, 0.0),
                    'Objects': {},
                    'Pos': Point3(394.152, -72.849, 3.405),
                    'Scale': VBase3(1.3, 1.3, 1.3),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Lt_1F'
                    }
                },
                '1138322171.02dxschafe': {
                    'Type':
                    'Rock',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(0.0, 5.43, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(390.802, -62.328, 4.404),
                    'Scale':
                    VBase3(1.349, 1.349, 1.349),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_LT_group_2F'
                    }
                },
                '1138322171.45dxschafe': {
                    'Type':
                    'Rock',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(384.221, -62.221, 4.504),
                    'Scale':
                    VBase3(2.639, 2.639, 2.639),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Lt_3F'
                    }
                },
                '1138322178.02dxschafe': {
                    'Type': 'Rock',
                    'Color': (0.5, 0.5, 0.5, 1.0),
                    'Hpr': VBase3(-4.698, 5.902, 0.0),
                    'Objects': {},
                    'Pos': Point3(73.865, -113.019, 2.431),
                    'Scale': VBase3(2.523, 2.523, 2.523),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_1F'
                    }
                },
                '1138322179.7dxschafe': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(135.472, -20.191, 10.586),
                    'Scale': VBase3(1.772, 1.772, 1.772),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1138322183.39dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(61.118, 9.31, 0.0),
                    'Objects': {},
                    'Pos': Point3(160.085, -61.819, 7.237),
                    'Scale': VBase3(1.748, 1.748, 1.748),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_2F'
                    }
                },
                '1138322184.19dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-91.565, -6.453, 0.0),
                    'Objects': {},
                    'Pos': Point3(216.851, -5.436, 5.864),
                    'Scale': VBase3(2.987, 2.987, 2.987),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_1F'
                    }
                },
                '1138322184.67dxschafe': {
                    'Type': 'Rock',
                    'Color': (0.5, 0.5, 0.5, 1.0),
                    'Hpr': VBase3(1.608, 4.341, -0.437),
                    'Objects': {},
                    'Pos': Point3(80.693, -135.397, 1.067),
                    'Scale': VBase3(1.417, 1.417, 1.417),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_LT_group_3F'
                    }
                },
                '1138322186.06dxschafe': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(60.52, -72.091, 1.076),
                    'Scale': VBase3(2.391, 2.391, 2.391),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1138322192.33dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(77.291, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(286.825, 155.747, 51.755),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1138322192.73dxschafe': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(347.609, 107.322, 42.593),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_2F'
                    }
                },
                '1138322193.17dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(62.423, 7.172, 0.0),
                    'Objects': {},
                    'Pos': Point3(356.164, 101.723, 40.845),
                    'Scale': VBase3(1.584, 1.584, 1.584),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_1F'
                    }
                },
                '1138322196.09dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-45.746, 17.13, 0.0),
                    'Objects': {},
                    'Pos': Point3(360.426, 66.068, 32.189),
                    'Scale': VBase3(2.617, 2.617, 2.617),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_3F'
                    }
                },
                '1138322206.23dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, -4.554, -1.779),
                    'Pos': Point3(642.321, -148.98, 5.697),
                    'Scale': VBase3(1.986, 1.986, 1.986),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_1F'
                    }
                },
                '1138322206.7dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(125.532, 0.322, -3.438),
                    'Objects': {},
                    'Pos': Point3(657.204, -134.403, 4.287),
                    'Scale': VBase3(1.957, 1.957, 1.957),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_2F'
                    }
                },
                '1138322208.19dxschafe': {
                    'Type':
                    'Rock',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(607.992, -185.909, 5.245),
                    'Scale':
                    VBase3(1.319, 1.319, 1.319),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_LT_group_2F'
                    }
                },
                '1138322209.14dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, -2.11, -1.487),
                    'Objects': {},
                    'Pos': Point3(654.209, -106.786, 3.55),
                    'Scale': VBase3(2.496, 2.496, 2.496),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1138322210.05dxschafe': {
                    'Type':
                    'Rock',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(0.0, 0.0, 12.333),
                    'Objects': {},
                    'Pos':
                    Point3(689.596, -206.364, 1.264),
                    'Scale':
                    VBase3(1.774, 1.774, 1.774),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_LT_group_2F'
                    }
                },
                '1138322213.67dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(38.481, 31.78, 18.92),
                    'Objects': {},
                    'Pos': Point3(661.765, 61.641, 29.377),
                    'Scale': VBase3(1.956, 1.956, 1.956),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1138322214.66dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 0.0, 6.891),
                    'Objects': {},
                    'Pos': Point3(679.712, -13.834, 1.353),
                    'Scale': VBase3(2.069, 2.069, 2.069),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_2F'
                    }
                },
                '1138322217.11dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 10.884, 5.42),
                    'Objects': {},
                    'Pos': Point3(541.402, -70.394, 2.023),
                    'Scale': VBase3(2.356, 2.356, 2.356),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1138322220.91dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-0.035, -2.308, -1.405),
                    'Pos': Point3(545.857, -94.351, 0.726),
                    'Scale': VBase3(1.923, 1.923, 1.923),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_2F'
                    }
                },
                '1138322221.28dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(87.03, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(621.453, -49.773, 2.907),
                    'Scale': VBase3(2.159, 2.159, 2.159),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1138322227.23dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 19.381, 0.0),
                    'Objects': {},
                    'Pos': Point3(481.41, -5.701, 19.854),
                    'Scale': VBase3(1.925, 1.925, 1.925),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_1F'
                    }
                },
                '1138322227.7dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(29.662, 20.267, -11.16),
                    'Objects': {},
                    'Pos': Point3(568.552, 43.002, 34.732),
                    'Scale': VBase3(1.506, 1.506, 1.506),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1138322228.13dxschafe': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(506.933, 31.941, 29.692),
                    'Scale': VBase3(2.786, 2.786, 2.786),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_3F'
                    }
                },
                '1138322228.63dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 25.907, 0.0),
                    'Objects': {},
                    'Pos': Point3(486.253, 6.518, 21.98),
                    'Scale': VBase3(2.291, 2.291, 2.291),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1138322229.2dxschafe': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(486.053, -3.207, 20.969),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1138322230.16dxschafe': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(455.667, -37.218, 9.953),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1138322230.55dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 19.361, 0.0),
                    'Objects': {},
                    'Pos': Point3(453.701, -42.734, 8.346),
                    'Scale': VBase3(1.877, 1.877, 1.877),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1138322230.91dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 9.295, 0.0),
                    'Objects': {},
                    'Pos': Point3(456.929, -47.63, 6.21),
                    'Scale': VBase3(2.524, 2.524, 2.524),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_3F'
                    }
                },
                '1138322231.42dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 14.029, 0.0),
                    'Objects': {},
                    'Pos': Point3(452.046, -35.949, 9.875),
                    'Scale': VBase3(3.706, 3.706, 3.706),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_4F'
                    }
                },
                '1138322232.47dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 19.008, 0.0),
                    'Objects': {},
                    'Pos': Point3(390.81, -3.488, 12.286),
                    'Scale': VBase3(1.85, 1.85, 1.85),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1138322232.8dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 21.385, 0.0),
                    'Objects': {},
                    'Pos': Point3(387.492, 0.219, 12.817),
                    'Scale': VBase3(5.406, 5.406, 5.406),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_4F'
                    }
                },
                '1138322233.06dxschafe': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(389.125, 35.048, 22.103),
                    'Scale': VBase3(2.377, 2.377, 2.377),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1138322233.64dxschafe': {
                    'Type': 'Rock',
                    'Color': (0.5, 0.5, 0.5, 1.0),
                    'Hpr': VBase3(0.0, 10.509, 0.0),
                    'Objects': {},
                    'Pos': Point3(381.781, 71.752, 34.601),
                    'Scale': VBase3(2.084, 2.084, 2.084),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1138322234.11dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(41.146, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(374.256, 28.55, 22.715),
                    'Scale': VBase3(1.689, 1.689, 1.689),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_2F'
                    }
                },
                '1138322234.53dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 19.424, 0.0),
                    'Objects': {},
                    'Pos': Point3(394.022, 4.082, 14.838),
                    'Scale': VBase3(2.837, 2.837, 2.837),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_3F'
                    }
                },
                '1138322238.98dxschafe': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(263.962, 13.806, 7.993),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1138322239.42dxschafe': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(273.014, 17.318, 9.313),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1138322239.84dxschafe': {
                    'Type':
                    'Rock',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(278.702, 27.255, 10.615),
                    'Scale':
                    VBase3(2.102, 2.102, 2.102),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/zz_dont_use_rocks_LT_group_2F'
                    }
                },
                '1138322243.48dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(18.738, 13.376, -25.264),
                    'Objects': {},
                    'Pos': Point3(329.013, 176.649, 47.39),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1138322245.98dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 0.0, 4.045),
                    'Objects': {
                        '1138322246.66dxschafe': {
                            'Type': 'Rock',
                            'GridPos': Point3(365.951, 145.975, 35.637),
                            'Hpr': VBase3(-0.185, -0.004, 1.09),
                            'Pos': Point3(44.593, -45.251, -13.868),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                            }
                        }
                    },
                    'Pos': Point3(322.447, 191.226, 52.616),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_2F'
                    }
                },
                '1138322247.14dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 23.1, -4.9),
                    'Objects': {
                        '1138402807.2dxschafe': {
                            'Type': 'Bush',
                            'GridPos': Point3(328.629, 183.779, 50.124),
                            'Hpr': VBase3(-2.467, -0.757, 5.946),
                            'Pos': Point3(-10.077, 8.035, -0.763),
                            'Scale': VBase3(0.417, 0.417, 0.417),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        }
                    },
                    'Pos': Point3(341.656, 173.296, 47.954),
                    'Scale': VBase3(1.306, 1.306, 1.306),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1138322252.73dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-32.679, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(269.383, 168.253, 54.925),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1138322259.48dxschafe': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(418.032, 41.105, 28.111),
                    'Scale': VBase3(2.709, 2.709, 2.709),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_3F'
                    }
                },
                '1138322259.92dxschafe': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(420.573, 28.052, 23.858),
                    'Scale': VBase3(2.349, 2.349, 2.349),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_2F'
                    }
                },
                '1138322260.36dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(0.0, 12.785, 0.0),
                    'Pos': Point3(443.521, -2.577, 17.608),
                    'Scale': VBase3(2.312, 2.312, 2.312),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                    }
                },
                '1138322915.58dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-96.934, 28.548, 13.896),
                    'Objects': {},
                    'Pos': Point3(364.094, 63.842, 31.939),
                    'Scale': VBase3(1.434, 1.434, 1.434),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_2F'
                    }
                },
                '1138324106.59dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': VBase3(23.952, 0.0, 0.0),
                    'Pos': Point3(498.499, -160.809, 5.213),
                    'Scale': VBase3(0.606, 0.606, 0.606),
                    'Visual': {
                        'Model': 'models/props/barrel_sideways'
                    }
                },
                '1138324126.88dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': VBase3(108.315, 0.0, 0.0),
                    'Pos': Point3(484.605, -162.793, 5.213),
                    'Scale': VBase3(0.606, 0.606, 0.606),
                    'Visual': {
                        'Model': 'models/props/barrel_sideways'
                    }
                },
                '1138324144.91dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': VBase3(159.646, 0.0, 0.0),
                    'Pos': Point3(495.513, -156.728, 5.213),
                    'Scale': VBase3(0.606, 0.606, 0.606),
                    'Visual': {
                        'Model': 'models/props/barrel_sideways'
                    }
                },
                '1138324161.06dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(90.544, 89.34, 162.223),
                    'Pos':
                    Point3(504.428, -146.789, 6.211),
                    'Scale':
                    VBase3(0.606, 0.606, 0.606),
                    'Visual': {
                        'Model': 'models/props/barrel_grey'
                    }
                },
                '1138324171.53dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': VBase3(-42.613, 88.838, -0.001),
                    'Pos': Point3(506.408, -97.68, 5.707),
                    'Scale': VBase3(0.405, 0.405, 0.405),
                    'Visual': {
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1138324180.14dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(-121.73, 0.0, 0.0),
                    'Pos':
                    Point3(508.593, -99.248, 5.213),
                    'Scale':
                    VBase3(0.422, 0.422, 0.422),
                    'Visual': {
                        'Model': 'models/props/barrel_grey'
                    }
                },
                '1138324211.02dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': VBase3(9.236, 17.911, 0.0),
                    'Pos': Point3(489.671, -79.014, 7.904),
                    'Scale': VBase3(0.422, 0.422, 0.422),
                    'Visual': {
                        'Model': 'models/props/barrel_sideways'
                    }
                },
                '1138324232.17dxschafe': {
                    'Type': 'Barrel',
                    'Color': (1.0, 1.0, 1.0, 1.0),
                    'Hpr': VBase3(14.701, 0.0, 0.0),
                    'Pos': Point3(501.663, -105.41, 5.213),
                    'Scale': VBase3(0.422, 0.422, 0.422),
                    'Visual': {
                        'Model': 'models/props/barrel_sideways'
                    }
                },
                '1138324258.89dxschafe': {
                    'Type':
                    'Barrel',
                    'Color': (0.800000011920929, 0.800000011920929,
                              0.800000011920929, 1.0),
                    'Hpr':
                    VBase3(-7.774, 27.276, 22.614),
                    'Pos':
                    Point3(483.844, -80.9, 5.841),
                    'Scale':
                    VBase3(0.422, 0.422, 0.422),
                    'Visual': {
                        'Model': 'models/props/barrel_sideways'
                    }
                },
                '1138324270.03dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': VBase3(130.252, 0.0, 0.0),
                    'Pos': Point3(480.299, -77.438, 5.08),
                    'Scale': VBase3(0.422, 0.422, 0.422),
                    'Visual': {
                        'Model': 'models/props/barrel_sideways'
                    }
                },
                '1138324271.88dxschafe': {
                    'Type': 'Barrel',
                    'Color': (1.0, 1.0, 1.0, 1.0),
                    'Hpr': VBase3(-20.064, 0.0, 0.0),
                    'Pos': Point3(482.837, -80.309, 5.213),
                    'Scale': VBase3(0.422, 0.422, 0.422),
                    'Visual': {
                        'Model': 'models/props/barrel_sideways'
                    }
                },
                '1138331394.53dxschafe': {
                    'Type':
                    'Cart',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(35.962, 0.0, 0.0),
                    'Pos':
                    Point3(510.222, -114.638, 5.213),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cart_reg'
                    }
                },
                '1138331701.25dxschafe': {
                    'Type':
                    'Sack',
                    'Color': (0.4000000059604645, 0.4000000059604645,
                              0.4000000059604645, 1.0),
                    'Hpr':
                    VBase3(20.051, 0.0, 0.0),
                    'Pos':
                    Point3(440.284, -139.099, 5.199),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138331811.16dxschafe': {
                    'Type':
                    'Sack',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(5.87, 0.0, 0.0),
                    'Pos':
                    Point3(445.542, -138.285, 5.316),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138331908.84dxschafe': {
                    'Type':
                    'Sack',
                    'Color': (0.800000011920929, 0.800000011920929,
                              0.800000011920929, 1.0),
                    'Hpr':
                    VBase3(145.211, 0.0, 0.0),
                    'Pos':
                    Point3(444.12, -138.952, 6.59),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138331929.81dxschafe': {
                    'Type':
                    'Sack',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(43.072, 0.53, -0.403),
                    'Pos':
                    Point3(439.259, -138.314, 6.513),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138331947.63dxschafe': {
                    'Type': 'Sack',
                    'Color': (0.5, 0.5, 0.5, 1.0),
                    'Hpr': VBase3(-18.972, 0.604, 0.28),
                    'Pos': Point3(435.134, -139.899, 5.257),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138331970.69dxschafe': {
                    'Type':
                    'Sack',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(-168.94, -0.663, 0.06),
                    'Pos':
                    Point3(441.46, -138.846, 7.737),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138332017.73dxschafe': {
                    'Type':
                    'Sack',
                    'Color': (0.800000011920929, 0.800000011920929,
                              0.800000011920929, 1.0),
                    'Hpr':
                    VBase3(-168.94, -0.663, 0.06),
                    'Pos':
                    Point3(442.973, -135.795, 5.114),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138332026.81dxschafe': {
                    'Type':
                    'Sack',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.8999999761581421, 1.0),
                    'Hpr':
                    VBase3(170.29, -0.641, -0.179),
                    'Pos':
                    Point3(437.907, -136.46, 5.102),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138332060.92dxschafe': {
                    'Type': 'Sack',
                    'Hpr': VBase3(170.29, -0.641, -0.179),
                    'Pos': Point3(438.187, -142.0, 5.213),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138332064.02dxschafe': {
                    'Type':
                    'Sack',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(170.29, -0.641, 19.58),
                    'Pos':
                    Point3(436.442, -139.949, 7.229),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138332091.67dxschafe': {
                    'Type': 'Sack',
                    'Hpr': VBase3(5.873, 0.419, -0.886),
                    'Pos': Point3(454.36, -136.707, 5.193),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138332164.23dxschafe': {
                    'Type':
                    'Sack',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(166.959, -0.684, 0.703),
                    'Pos':
                    Point3(454.392, -136.587, 6.534),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138332190.48dxschafe': {
                    'Type':
                    'Sack',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(-151.881, -0.052, 0.979),
                    'Pos':
                    Point3(502.636, -140.483, 5.213),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138332193.67dxschafe': {
                    'Type':
                    'Sack',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(-117.511, 0.51, 0.837),
                    'Pos':
                    Point3(505.153, -136.324, 5.237),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138332208.34dxschafe': {
                    'Type':
                    'Sack',
                    'Color': (0.800000011920929, 0.800000011920929,
                              0.800000011920929, 1.0),
                    'Hpr':
                    VBase3(-117.511, 0.51, 0.837),
                    'Pos':
                    Point3(504.218, -138.433, 6.501),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138332353.31dxschafe': {
                    'Type': 'Sack',
                    'Color': (0.5, 0.5, 0.5, 1.0),
                    'Hpr': VBase3(85.252, -0.794, -0.575),
                    'Pos': Point3(400.366, -91.939, 5.337),
                    'Scale': VBase3(0.719, 0.719, 0.719),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138332356.11dxschafe': {
                    'Type':
                    'Sack',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(83.074, 9.617, -6.82),
                    'Pos':
                    Point3(400.177, -93.475, 6.184),
                    'Scale':
                    VBase3(0.727, 0.727, 0.727),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138332435.56dxschafe': {
                    'Type': 'Sack',
                    'Color': (0.5, 0.5, 0.5, 1.0),
                    'Hpr': VBase3(49.647, -0.311, -0.93),
                    'Pos': Point3(399.611, -96.165, 5.34),
                    'Scale': VBase3(0.739, 0.739, 0.739),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138388719.81dxschafe': {
                    'Type': 'Sack',
                    'Hpr': VBase3(86.171, -9.594, 165.689),
                    'Pos': Point3(589.06, 183.765, 48.396),
                    'Scale': VBase3(0.614, 0.614, 0.614),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138389074.66dxschafe': {
                    'Type':
                    'Bucket',
                    'Color': (0.8999999761581421, 0.8999999761581421,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(-3.011, 7.112, 22.68),
                    'Pos':
                    Point3(484.994, -80.628, 7.238),
                    'Scale':
                    VBase3(0.754, 0.754, 0.754),
                    'Visual': {
                        'Model': 'models/props/bucket'
                    }
                },
                '1138389081.77dxschafe': {
                    'Type': 'Bucket',
                    'Hpr': VBase3(0.001, -0.122, 0.548),
                    'Pos': Point3(402.276, -97.232, 5.754),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bucket'
                    }
                },
                '1138389083.92dxschafe': {
                    'Type': 'Bucket',
                    'Hpr': VBase3(0.001, -0.122, 0.548),
                    'Pos': Point3(348.513, -127.149, 4.365),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/bucket'
                    }
                },
                '1138389207.69dxschafe': {
                    'Type':
                    'Rope',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(323.623, -125.268, 4.402),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rope_pile'
                    }
                },
                '1138389216.22dxschafe': {
                    'Type':
                    'Rope',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(290.799, -126.977, 4.546),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rope_pile'
                    }
                },
                '1138389247.94dxschafe': {
                    'Type':
                    'Rope',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(244.758, -124.199, 4.387),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rope_pile'
                    }
                },
                '1138389261.84dxschafe': {
                    'Type':
                    'Rope',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(409.238, -143.318, 5.306),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rope_pile'
                    }
                },
                '1138389275.91dxschafe': {
                    'Type':
                    'Rope',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(-108.642, 0.0, 0.0),
                    'Pos':
                    Point3(459.177, -167.081, 5.427),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rope_pile'
                    }
                },
                '1138389277.3dxschafe': {
                    'Type':
                    'Rope',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    Point3(0.0, 0.0, 0.0),
                    'Pos':
                    Point3(457.283, -162.514, 5.213),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rope_pile'
                    }
                },
                '1138389278.03dxschafe': {
                    'Type':
                    'Rope',
                    'Color': (0.800000011920929, 0.800000011920929,
                              0.800000011920929, 1.0),
                    'Hpr':
                    VBase3(72.229, 0.0, 0.0),
                    'Pos':
                    Point3(459.08, -164.235, 5.357),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rope_pile'
                    }
                },
                '1138389335.77dxschafe': {
                    'Type':
                    'Rope',
                    'Color': (0.800000011920929, 0.800000011920929,
                              0.800000011920929, 1.0),
                    'Hpr':
                    VBase3(72.229, 0.0, 0.0),
                    'Pos':
                    Point3(491.819, -157.3, 5.213),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rope_pile'
                    }
                },
                '1138389345.19dxschafe': {
                    'Type':
                    'Rope',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(72.229, 0.0, 0.0),
                    'Pos':
                    Point3(482.492, -168.43, 5.213),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rope_pile'
                    }
                },
                '1138389359.92dxschafe': {
                    'Type':
                    'Rope',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(72.229, 0.0, 0.0),
                    'Pos':
                    Point3(430.642, -141.276, 5.217),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rope_pile'
                    }
                },
                '1138389361.09dxschafe': {
                    'Type':
                    'Rope',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(72.229, 0.0, 0.0),
                    'Pos':
                    Point3(431.623, -138.694, 5.216),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rope_pile'
                    }
                },
                '1138389396.72dxschafe': {
                    'Type': 'Rope',
                    'Hpr': VBase3(72.054, 1.909, -3.887),
                    'Pos': Point3(430.308, 133.035, 46.533),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rope_pile'
                    }
                },
                '1138400345.72dxschafe': {
                    'Type': 'Creature',
                    'Hpr': VBase3(-102.243, 0.0, 0.0),
                    'Pos': Point3(-112.27, -313.908, 0.809),
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Species': 'Crab',
                    'Start State': 'Walk'
                },
                '1138400763.67dxschafe': {
                    'Type': 'Creature',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-27.049, -297.966, 1.728),
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Species': 'Crab',
                    'Start State': 'Walk'
                },
                '1138400773.91dxschafe': {
                    'Type': 'Creature',
                    'Hpr': VBase3(60.203, 0.0, 0.0),
                    'Pos': Point3(-154.66, -382.735, 0.31),
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Species': 'Crab',
                    'Start State': 'Walk'
                },
                '1138400798.94dxschafe': {
                    'Type': 'Creature',
                    'Hpr': VBase3(-146.112, 0.0, 0.0),
                    'Pos': Point3(-171.326, -282.684, 1.224),
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Species': 'Crab',
                    'Start State': 'Walk'
                },
                '1138402671.14dxschafe': {
                    'Type': 'Tree - Animated',
                    'Animate': 'models/vegetation/tree_b_trunk_idle',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(335.75, 193.12, 44.242),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_leaf_a_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/tree_b_leaf_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/palm_trunk_a_idle',
                        'Model': 'models/vegetation/tree_b_trunk_hi',
                        'PartName': 'trunk'
                    }
                },
                '1138403080.25dxschafe': {
                    'Type': 'Barrel',
                    'Hpr': VBase3(-176.262, 47.827, -164.108),
                    'Pos': Point3(387.022, 132.439, 46.513),
                    'Scale': VBase3(0.532, 0.532, 0.532),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    }
                },
                '1138404941.83dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(15.586, 0.0, 0.0),
                    'Pos': Point3(-218.82, -336.725, 0.489),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1138404947.05dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(65.384, 0.0, 0.0),
                    'Pos': Point3(-194.979, -236.708, 1.513),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138404952.7dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-69.085, 0.0, 0.0),
                    'Pos': Point3(-38.478, -188.329, -1.936),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138404955.5dxschafe': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-7.687, -195.324, 1.944),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138404962.61dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(128.461, 0.0, 0.0),
                    'Pos': Point3(-213.151, -398.985, 3.123),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138404962.67dxschafe': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-219.311, -375.049, 5.788),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138404965.13dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-31.764, 10.781, 9.844),
                    'Pos': Point3(54.835, -213.632, -2.98),
                    'Scale': VBase3(1.306, 1.306, 1.306),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138404966.3dxschafe': {
                    'Type': 'Bush',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-200.734, -277.555, 1.278),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1138404990.83dxschafe': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(-47.084, -197.603, 1.796),
                    'Scale': VBase3(1.969, 1.969, 1.969),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_2F'
                    }
                },
                '1138404993.45dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-58.061, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(-65.047, -212.22, 1.312),
                    'Scale': VBase3(2.385, 2.385, 2.385),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_1F'
                    }
                },
                '1138404994.17dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-12.507, 1.8, 0.0),
                    'Objects': {
                        '1138406441.97dxschafe': {
                            'Type': 'Tree',
                            'GridPos': Point3(-72.073, -232.934, 4.928),
                            'Hpr': VBase3(12.486, 2.246, 0.39),
                            'Pos': Point3(-0.926, 1.458, 0.952),
                            'Scale': VBase3(0.223, 0.223, 0.223),
                            'Visual': {
                                'Model': 'models/vegetation/fern_tree_c'
                            }
                        },
                        '1138406484.72dxschafe': {
                            'Type': 'Tree',
                            'GridPos': Point3(-74.156, -237.018, 4.704),
                            'Hpr': VBase3(24.771, 10.597, -4.865),
                            'Pos': Point3(-1.279, 0.092, 0.926),
                            'Scale': VBase3(0.146, 0.146, 0.146),
                            'Visual': {
                                'Model': 'models/vegetation/fern_tree_c'
                            }
                        },
                        '1138406506.36dxschafe': {
                            'Type': 'Tree',
                            'GridPos': Point3(-72.459, -235.423, 5.595),
                            'Hpr': VBase3(37.088, 9.163, 11.016),
                            'Pos': Point3(-0.876, 0.692, 1.181),
                            'Scale': VBase3(0.09, 0.09, 0.09),
                            'Visual': {
                                'Model': 'models/vegetation/fern_tree_c'
                            }
                        }
                    },
                    'Pos': Point3(-70.138, -238.119, 1.684),
                    'Scale': VBase3(3.253, 3.253, 3.253),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_1F'
                    }
                },
                '1138404996.56dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(34.668, 1.658, 1.066),
                    'Objects': {},
                    'Pos': Point3(44.756, -219.042, 0.752),
                    'Scale': VBase3(1.762, 1.762, 1.762),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_2F'
                    }
                },
                '1138404997.58dxschafe': {
                    'Type':
                    'Rock',
                    'Color': (0.4000000059604645, 0.4000000059604645,
                              0.4000000059604645, 1.0),
                    'Hpr':
                    VBase3(-33.902, -3.398, 17.03),
                    'Pos':
                    Point3(84.245, -225.375, -4.251),
                    'Scale':
                    VBase3(1.551, 1.551, 1.551),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_LT_group_2F'
                    }
                },
                '1138404998.63dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(84.152, 0.968, -9.366),
                    'Pos': Point3(70.077, -224.181, -0.431),
                    'Scale': VBase3(1.805, 1.805, 1.805),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1138405003.19dxschafe': {
                    'Type':
                    'Rock',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(79.685, 11.577, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(-86.451, -344.372, -0.256),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_LT_group_1F'
                    }
                },
                '1138405003.73dxschafe': {
                    'Type':
                    'Rock',
                    'Color': (0.800000011920929, 0.800000011920929,
                              0.800000011920929, 1.0),
                    'Hpr':
                    VBase3(0.0, 11.921, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(-76.024, -350.351, -2.912),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_LT_group_2F'
                    }
                },
                '1138405005.31dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-18.913, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(-214.797, -410.201, 2.149),
                    'Scale': VBase3(1.799, 1.799, 1.799),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1138405008.59dxschafe': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(-216.403, -419.293, 1.086),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_1F'
                    }
                },
                '1138405009.48dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(128.202, 20.66, -15.518),
                    'Objects': {},
                    'Pos': Point3(-211.436, -433.317, 0.125),
                    'Scale': VBase3(1.519, 1.519, 1.519),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_2F'
                    }
                },
                '1138405014.53dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-95.028, 0.0, 5.316),
                    'Objects': {},
                    'Pos': Point3(-147.351, -242.998, 2.185),
                    'Scale': VBase3(2.298, 2.298, 2.298),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1138405015.67dxschafe': {
                    'Type':
                    'Rock',
                    'Color': (0.4000000059604645, 0.4000000059604645,
                              0.4000000059604645, 1.0),
                    'Hpr':
                    VBase3(0.0, -10.056, 0.0),
                    'Objects': {},
                    'Pos':
                    Point3(-163.019, -233.492, -2.527),
                    'Scale':
                    VBase3(7.55, 7.55, 7.55),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_3F'
                    }
                },
                '1138405016.3dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(-34.022, 0.0, 0.0),
                    'Pos': Point3(-177.615, -238.454, 1.503),
                    'Scale': VBase3(2.146, 2.146, 2.146),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_2F'
                    }
                },
                '1138405255.73dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(116.892, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(-173.365, -230.044, 0.369),
                    'Scale': VBase3(7.454, 7.454, 7.454),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rock_Dk_3F'
                    }
                },
                '1138405427.22dxschafe': {
                    'Type':
                    'Rock',
                    'Color': (0.4000000059604645, 0.4000000059604645,
                              0.4000000059604645, 1.0),
                    'Hpr':
                    VBase3(-54.725, 0.0, 0.0),
                    'Pos':
                    Point3(-207.246, -292.729, 1.468),
                    'Scale':
                    VBase3(1.614, 1.614, 1.614),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_LT_group_2F'
                    }
                },
                '1138405547.0dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(38.179, 0.0, 0.0),
                    'Pos': Point3(-76.377, -244.608, 2.26),
                    'Scale': VBase3(1.462, 1.462, 1.462),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1138405584.83dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(7.343, 0.0, 0.0),
                    'Pos': Point3(-79.53, -225.681, 2.428),
                    'Scale': VBase3(1.462, 1.462, 1.462),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1138405639.5dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(-51.937, 0.0, 0.0),
                    'Pos': Point3(-147.535, -229.85, 1.961),
                    'Scale': VBase3(1.228, 1.228, 1.228),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1138405669.55dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(102.799, 0.0, 0.0),
                    'Pos': Point3(-133.393, -233.609, 1.008),
                    'Scale': VBase3(1.228, 1.228, 1.228),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1138406264.66dxschafe': {
                    'Type': 'Tree',
                    'Hpr': VBase3(0.0, 0.0, 5.151),
                    'Pos': Point3(-213.556, -387.863, 2.83),
                    'Scale': VBase3(0.774, 0.774, 0.774),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_e'
                    }
                },
                '1138406308.7dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(-67.178, -12.457, 5.187),
                    'Pos':
                    Point3(-214.423, -354.664, 4.023),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_e'
                    }
                },
                '1138406395.17dxschafe': {
                    'Type': 'Rock',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-224.082, -366.002, 4.032),
                    'Scale': VBase3(2.953, 2.953, 2.953),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_3F'
                    }
                },
                '1138406672.28dxschafe': {
                    'Type': 'Tree - Animated',
                    'Animate': 'models/vegetation/palm_trunk_a_idle',
                    'Hpr': VBase3(-36.777, -1.721, 12.417),
                    'Pos': Point3(-89.162, -348.602, -1.688),
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
                '1138406690.55dxschafe': {
                    'Type': 'Tree - Animated',
                    'Animate': 'models/vegetation/palm_trunk_a_idle',
                    'Hpr': VBase3(-62.829, -3.202, -1.475),
                    'Pos': Point3(-132.223, -356.378, 0.51),
                    'Scale': VBase3(1.185, 1.185, 1.185),
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
                '1138406692.61dxschafe': {
                    'Type': 'Tree - Animated',
                    'Animate': 'models/vegetation/palm_trunk_a_idle',
                    'Hpr': VBase3(81.816, 4.927, -7.169),
                    'Pos': Point3(-138.884, -355.391, 0.965),
                    'Scale': VBase3(0.823, 0.823, 0.823),
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
                '1138406753.16dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(0.0, 13.124, 0.0),
                    'Pos': Point3(-90.634, -340.533, -3.263),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_g'
                    }
                },
                '1138406774.14dxschafe': {
                    'Type': 'Bush',
                    'Color': (0.5, 0.5, 0.5, 1.0),
                    'Hpr': VBase3(0.0, 13.124, 0.0),
                    'Pos': Point3(-133.097, -353.011, -1.554),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_f'
                    }
                },
                '1138406776.23dxschafe': {
                    'Type':
                    'Bush',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(0.0, 13.124, 25.816),
                    'Pos':
                    Point3(-85.78, -343.5, -2.468),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_f'
                    }
                },
                '1138406881.92dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(44.795, -2.619, -2.635),
                    'Objects': {},
                    'Pos': Point3(-135.435, -350.571, 0.294),
                    'Scale': VBase3(1.751, 1.751, 1.751),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_LT_group_2F'
                    }
                },
                '1138407053.23dxschafe': {
                    'Type':
                    'Rock',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(89.648, -6.334, -2.658),
                    'Objects': {
                        '1138407116.95dxschafe': {
                            'Type': 'Bush',
                            'GridPos': Point3(-147.132, -339.872, 0.731),
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(0.555, -2.089, 0.361),
                            'Scale': VBase3(0.326, 0.326, 0.326),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        }
                    },
                    'Pos':
                    Point3(-153.377, -341.482, -1.153),
                    'Scale':
                    VBase3(3.066, 3.066, 3.066),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_LT_group_2F'
                    }
                },
                '1138407288.64dxschafe': {
                    'Type': 'Rock',
                    'Hpr': VBase3(47.773, 0.0, 0.0),
                    'Pos': Point3(-0.083, -203.712, 2.472),
                    'Scale': VBase3(1.679, 1.679, 1.679),
                    'Visual': {
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_2F'
                    }
                },
                '1138411180.17dxschafe': {
                    'Type': 'Light - Dynamic',
                    'Attenuation': '0.004',
                    'Flickering': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(410.187, 127.473, 52.13),
                    'Scale': VBase3(3.0, 3.0, 3.0),
                    'Visual': {
                        'Color': (1, 1, 1, 1),
                        'Model': 'icons/icon_lightbulb'
                    }
                },
                '1138411274.68dxschafe': {
                    'Type': 'Light - Dynamic',
                    'Attenuation': '0.004',
                    'Flickering': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(618.33, 99.599, 55.781),
                    'Scale': VBase3(3.0, 3.0, 3.0),
                    'Visual': {
                        'Color': (1, 1, 1, 1),
                        'Model': 'icons/icon_lightbulb'
                    }
                },
                '1138411280.35dxschafe': {
                    'Type': 'Light - Dynamic',
                    'Attenuation': '0.004',
                    'Flickering': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(585.969, 217.42, 58.998),
                    'Scale': VBase3(3.0, 3.0, 3.0),
                    'Visual': {
                        'Color': (1, 1, 1, 1),
                        'Model': 'icons/icon_lightbulb'
                    }
                },
                '1138411455.04dxschafe': {
                    'Type': 'Light - Dynamic',
                    'Attenuation': '0.004',
                    'Flickering': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(438.89, 251.886, 58.379),
                    'Scale': VBase3(3.0, 3.0, 3.0),
                    'Visual': {
                        'Color': (1, 1, 1, 1),
                        'Model': 'icons/icon_lightbulb'
                    }
                },
                '1138411521.86dxschafe': {
                    'Type': 'Light - Dynamic',
                    'Attenuation': '0.004',
                    'Flickering': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(463.064, 316.652, 61.517),
                    'Scale': VBase3(3.0, 3.0, 3.0),
                    'Visual': {
                        'Color': (1, 1, 1, 1),
                        'Model': 'icons/icon_lightbulb'
                    }
                },
                '1138418930.61dxschafe': {
                    'Type': 'Sack',
                    'Hpr': VBase3(-44.406, 0.0, 0.0),
                    'Pos': Point3(507.516, -93.573, 7.491),
                    'Scale': VBase3(0.638, 0.638, 0.638),
                    'Visual': {
                        'Model': 'models/props/Sack'
                    }
                },
                '1138647768.95dxschafe': {
                    'Type':
                    'Wall',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(-30.14, -2.937, 6.098),
                    'Pos':
                    Point3(290.519, 160.233, 51.959),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/buildings/woodfence_B'
                    }
                },
                '1138647970.19dxschafe': {
                    'Type':
                    'Wall',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(-57.196, -6.166, 7.478),
                    'Pos':
                    Point3(265.412, 234.453, 60.158),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/buildings/woodfence_B'
                    }
                },
                '1138648022.36dxschafe': {
                    'Type':
                    'Wall',
                    'Color': (0.699999988079071, 0.699999988079071,
                              0.699999988079071, 1.0),
                    'Hpr':
                    VBase3(-32.727, -6.056, 12.983),
                    'Pos':
                    Point3(249.263, 245.427, 65.713),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/buildings/woodfence_B'
                    }
                },
                '1138654942.33dxschafe': {
                    'Type':
                    'Wall',
                    'Color': (0.7699999809265137, 0.7599999904632568,
                              0.6800000071525574, 1.0),
                    'Hpr':
                    VBase3(-4.741, 0.0, 0.0),
                    'Pos':
                    Point3(459.749, 80.692, 40.279),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/buildings/TallWallStucco_10'
                    }
                },
                '1138655096.28dxschafe': {
                    'Type':
                    'Wall',
                    'Color': (0.7699999809265137, 0.7599999904632568,
                              0.6800000071525574, 1.0),
                    'Hpr':
                    VBase3(-19.474, 0.0, 0.0),
                    'Pos':
                    Point3(419.015, 87.212, 40.256),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/buildings/TallWallStucco_10'
                    }
                },
                '1138657546.06dxschafe': {
                    'Type': 'Tree',
                    'Hpr': VBase3(129.539, 0.0, 0.0),
                    'Pos': Point3(376.579, 214.601, 41.267),
                    'Scale': VBase3(1.737, 1.737, 1.737),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1138695512.45jubutler': {
                    'Type': 'Port Collision Sphere',
                    'Name': 'ArtPrototypePort',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(353.718, -171.804, 0.0),
                    'Scale': VBase3(159.917, 159.917, 159.917),
                    'Visual': {
                        'Color': (0.5, 0.5, 1.0, 0.2),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1138721865.99dxschafe': {
                    'Type': 'Light - Dynamic',
                    'Attenuation': '0.004',
                    'Flickering': True,
                    'Hpr': VBase3(-36.203, 0.0, 0.0),
                    'Pos': Point3(566.163, 282.06, 60.102),
                    'Scale': VBase3(3.0, 3.0, 3.0),
                    'Visual': {
                        'Color': (1, 1, 1, 1),
                        'Model': 'icons/icon_lightbulb'
                    }
                },
                '1138722751.38dxschafe': {
                    'Type': 'Building Exterior',
                    'Name': '',
                    'File': '',
                    'Hpr': VBase3(6.635, 0.0, 0.0),
                    'Objects': {
                        '1138722751.38dxschafe0': {
                            'Type': 'Locator Node',
                            'Name': 'portal_exterior_1',
                            'GridPos': Point3(508.118, -88.704, 5.213),
                            'Hpr': VBase3(90.0, 0.0, 0.0),
                            'Pos': Point3(3.987, -20.033, 0.0),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(501.897, -69.731, 5.213),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Model': 'models/buildings/shanty_npc_house_combo_J'
                    }
                },
                '1138726034.66dxschafe': {
                    'Type': 'Crate',
                    'Hpr': VBase3(-30.545, -8.931, -23.585),
                    'Pos': Point3(594.061, -197.557, 3.098),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/crate'
                    }
                },
                '1138732475.17dxschafe': {
                    'Type': 'Tree',
                    'Hpr': VBase3(-42.846, 6.187, 5.708),
                    'Pos': Point3(491.715, 37.317, 29.497),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/fern_tree_a'
                    }
                },
                '1138732592.53dxschafe': {
                    'Type': 'Tree',
                    'Hpr': VBase3(-131.937, -2.543, 2.828),
                    'Pos': Point3(361.039, 181.2, 26.607),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1138732687.6dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(0.0, 3.802, 0.0),
                    'Pos':
                    Point3(130.679, 327.734, 58.742),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1138732731.02dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(0.0, 3.802, 0.0),
                    'Pos':
                    Point3(76.817, 284.63, 49.647),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1138732820.2dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(0.0, 3.802, 0.0),
                    'Pos': Point3(36.778, 222.26, 66.97),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/tree_b_leaf_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/tree_b_leaf_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/tree_b_trunk_idle',
                        'Model': 'models/vegetation/tree_b_trunk_hi',
                        'PartName': 'trunk'
                    }
                },
                '1138732869.65dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(0.0, 3.802, 0.0),
                    'Pos': Point3(-14.902, 201.497, 53.892),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/tree_b_leaf_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/tree_b_leaf_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/tree_b_trunk_idle',
                        'Model': 'models/vegetation/tree_b_trunk_hi',
                        'PartName': 'trunk'
                    }
                },
                '1138733059.16dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(0.0, 3.802, 0.0),
                    'Pos': Point3(227.673, 276.552, 60.928),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/tree_b_leaf_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/tree_b_leaf_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/tree_b_trunk_idle',
                        'Model': 'models/vegetation/tree_b_trunk_hi',
                        'PartName': 'trunk'
                    }
                },
                '1138733108.16dxschafe': {
                    'Type':
                    'Tree',
                    'Color': (0.6000000238418579, 0.6000000238418579,
                              0.6000000238418579, 1.0),
                    'Hpr':
                    VBase3(0.0, 3.802, 0.0),
                    'Pos':
                    Point3(268.083, 258.86, 60.562),
                    'Scale':
                    VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_b'
                    }
                },
                '1138733146.24dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(0.0, 3.802, 0.0),
                    'Pos': Point3(292.865, 227.202, 51.246),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/tree_b_leaf_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/tree_b_leaf_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/tree_b_trunk_idle',
                        'Model': 'models/vegetation/tree_b_trunk_hi',
                        'PartName': 'trunk'
                    }
                },
                '1138733189.2dxschafe': {
                    'Type': 'Tree - Animated',
                    'Hpr': VBase3(0.0, 3.802, 0.0),
                    'Pos': Point3(325.588, 210.017, 44.932),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'SubObjs': {
                        'Top Model': {
                            'Visual': {
                                'Animate':
                                'models/vegetation/tree_b_leaf_idle',
                                'Attach': ['trunk', 'def_trunk_attach'],
                                'Model': 'models/vegetation/tree_b_leaf_hi',
                                'PartName': 'leaf'
                            }
                        }
                    },
                    'Visual': {
                        'Animate': 'models/vegetation/tree_b_trunk_idle',
                        'Model': 'models/vegetation/tree_b_trunk_hi',
                        'PartName': 'trunk'
                    }
                },
                '1138739708.58dxschafe': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(203.941, 290.44, 51.387),
                    'Scale': VBase3(0.911, 0.911, 0.911),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_d'
                    }
                },
                '1138739839.69dxschafe': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(183.138, 317.303, 56.097),
                    'Scale': VBase3(0.911, 0.911, 0.911),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_d'
                    }
                },
                '1138739944.52dxschafe': {
                    'Type': 'Tree',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(74.887, 267.648, 62.913),
                    'Scale': VBase3(0.911, 0.911, 0.911),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_d'
                    }
                },
                '1138740055.77dxschafe': {
                    'Type': 'Tree',
                    'Hpr': VBase3(0.0, -1.363, 0.0),
                    'Pos': Point3(27.414, 201.542, 67.906),
                    'Scale': VBase3(0.795, 0.795, 0.795),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_d'
                    }
                },
                '1138740107.6dxschafe': {
                    'Type': 'Tree',
                    'Hpr': VBase3(0.0, -1.363, 0.0),
                    'Pos': Point3(7.262, 211.095, 70.354),
                    'Scale': VBase3(0.795, 0.795, 0.795),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_d'
                    }
                },
                '1138740455.21dxschafe': {
                    'Type': 'Bush',
                    'Hpr': VBase3(103.779, 0.0, 0.0),
                    'Pos': Point3(342.947, 189.507, 48.183),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1144695643.19sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_exterior_1',
                    'Hpr': VBase3(-18.331, 0.0, 0.0),
                    'Pos': Point3(-219.917, -319.235, 0.595),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1144695645.11sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_exterior_2',
                    'Hpr': VBase3(68.97, 0.0, 0.0),
                    'Pos': Point3(-285.103, -58.817, 44.049),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1144695701.45sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_exterior_1',
                    'Hpr': VBase3(-18.331, 0.0, 0.0),
                    'Pos': Point3(-219.917, -319.235, 0.595),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1144695701.48sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_exterior_2',
                    'Hpr': VBase3(68.97, 0.0, 0.0),
                    'Pos': Point3(-285.103, -58.817, 44.049),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1144695785.45sdnaik': {
                    'Type': 'Connector Tunnel',
                    'File': '',
                    'Hpr': VBase3(0.0, 0.0, -1.061),
                    'Objects': {
                        '1144695785.47sdnaik': {
                            'Type': 'Locator Node',
                            'Name': 'portal_connector_1',
                            'GridPos': Point3(-102.288, -444.139, 343.526),
                            'Hpr': VBase3(-89.513, 0.0, 0.0),
                            'Pos': Point3(0.0, 0.0, 0.0),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1144695785.52sdnaik': {
                            'Type': 'Locator Node',
                            'Name': 'portal_connector_2',
                            'GridPos': Point3(-7.199, -294.139, 345.287),
                            'Hpr': VBase3(90.682, 0.0, 0.0),
                            'Pos': Point3(95.0, 150.0, 0.0),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-102.288, -444.139, 343.526),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/tunnels/tunnel_cave_left'
                    }
                },
                '1144696205.34sdnaik': {
                    'Type': 'Connector Tunnel',
                    'File': '',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {
                        '1144696205.36sdnaik': {
                            'Type': 'Locator Node',
                            'Name': 'portal_connector_1',
                            'GridPos': Point3(-470.085, -52.086, 146.016),
                            'Hpr': VBase3(-89.513, 0.0, 0.0),
                            'Pos': Point3(0.0, 0.0, 0.0),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1144696208.66sdnaik': {
                            'Type': 'Locator Node',
                            'Name': 'portal_connector_2',
                            'GridPos': Point3(-374.98, 97.914, 146.016),
                            'Hpr': VBase3(90.682, 0.0, 0.0),
                            'Pos': Point3(95.0, 150.0, 0.0),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-470.085, -52.086, 146.016),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/tunnels/tunnel_cave_left'
                    }
                },
                '1144798398.96jubutler': {
                    'Type': 'Cell Portal Area',
                    'Name': 'cell_spanish_town',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {
                        '1135281802.29dzlu': {
                            'Type': 'bilgewater_town',
                            'Hpr': VBase3(0.001, -0.122, 0.548),
                            'Objects': {
                                '1135282109.68dzlu': {
                                    'Type': 'Building Exterior',
                                    'Name': '',
                                    'File': '',
                                    'GridPos': Point3(503.06, 312.389, 53.682),
                                    'Hpr': VBase3(-4.033, 0.147, -0.647),
                                    'Objects': {
                                        '1135282109.68dzlu0': {
                                            'Type':
                                            'Locator Node',
                                            'Name':
                                            'portal_exterior_1',
                                            'GridPos':
                                            Point3(555.418, 286.295, 64.69),
                                            'Hpr':
                                            Point3(0.0, 0.0, 0.0),
                                            'Pos':
                                            Point3(54.084, -22.35, 10.9),
                                            'Scale':
                                            VBase3(1.0, 1.0, 1.0)
                                        }
                                    },
                                    'Pos': Point3(-10.487, 102.52, 54.754),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Name':
                                        '',
                                        'Door':
                                        'models/buildings/shanty_guildhall_door',
                                        'Model':
                                        'models/buildings/spanish_npc_house_j_exterior'
                                    }
                                },
                                '1135282286.59dzlu': {
                                    'Type':
                                    'Building Exterior',
                                    'Name':
                                    '',
                                    'File':
                                    '',
                                    'Color':
                                    (0.800000011920929, 0.800000011920929,
                                     0.800000011920929, 1.0),
                                    'GridPos':
                                    Point3(581.712, 260.74, 49.783),
                                    'Hpr':
                                    VBase3(96.478, -3.524, -0.826),
                                    'Objects': {
                                        '1135282286.59dzlu0': {
                                            'Type':
                                            'Locator Node',
                                            'Name':
                                            'portal_exterior_1',
                                            'GridPos':
                                            Point3(597.203, 316.781, 62.546),
                                            'Hpr':
                                            Point3(0.0, 0.0, 0.0),
                                            'Pos':
                                            Point3(54.084, -22.35, 10.9),
                                            'Scale':
                                            VBase3(1.0, 1.0, 1.0)
                                        }
                                    },
                                    'Pos':
                                    Point3(68.198, 50.878, 51.497),
                                    'Scale':
                                    VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model':
                                        'models/buildings/spanish_npc_house_i_exterior'
                                    }
                                },
                                '1135285775.21dzlu': {
                                    'Type': 'Building Exterior',
                                    'Name': '',
                                    'File': '',
                                    'GridPos': Point3(488.03, 189.598, 45.284),
                                    'Hpr': VBase3(-174.901, -1.856, -0.453),
                                    'Objects': {
                                        '1135285775.21dzlu0': {
                                            'Type':
                                            'Locator Node',
                                            'Name':
                                            'portal_exterior_1',
                                            'GridPos':
                                            Point3(432.412, 206.709, 57.825),
                                            'Hpr':
                                            Point3(0.0, 0.0, 0.0),
                                            'Pos':
                                            Point3(54.084, -22.35, 10.9),
                                            'Scale':
                                            VBase3(1.0, 1.0, 1.0)
                                        }
                                    },
                                    'Pos': Point3(-25.436, -20.253, 45.951),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model':
                                        'models/buildings/spanish_npc_house_d_exterior'
                                    }
                                },
                                '1135285791.23dzlu': {
                                    'Type': 'Building Exterior',
                                    'Name': '',
                                    'File': '',
                                    'GridPos': Point3(641.557, 197.268,
                                                      48.655),
                                    'Hpr': VBase3(-86.804, 0.257, -0.477),
                                    'Objects': {
                                        '1135285791.23dzlu0': {
                                            'Type':
                                            'Locator Node',
                                            'Name':
                                            'portal_exterior_1',
                                            'GridPos':
                                            Point3(622.311, 142.136, 60.206),
                                            'Hpr':
                                            Point3(0.0, 0.0, 0.0),
                                            'Pos':
                                            Point3(54.084, -22.35, 10.9),
                                            'Scale':
                                            VBase3(1.0, 1.0, 1.0)
                                        }
                                    },
                                    'Pos': Point3(128.052, -12.593, 50.806),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model':
                                        'models/buildings/spanish_npc_house_d_exterior'
                                    }
                                },
                                '1135285802.19dzlu': {
                                    'Type': 'Building Exterior',
                                    'Name': '',
                                    'File': '',
                                    'GridPos': Point3(516.479, 212.238, 47.86),
                                    'Hpr': VBase3(91.882, -2.064, 0.627),
                                    'Objects': {
                                        '1135285802.19dzlu0': {
                                            'Type':
                                            'Locator Node',
                                            'Name':
                                            'portal_exterior_1',
                                            'GridPos':
                                            Point3(536.756, 267.154, 58.655),
                                            'Hpr':
                                            Point3(0.0, 0.0, 0.0),
                                            'Pos':
                                            Point3(54.084, -22.35, 10.9),
                                            'Scale':
                                            VBase3(1.0, 1.0, 1.0)
                                        }
                                    },
                                    'Pos': Point3(2.987, 2.381, 48.847),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model':
                                        'models/buildings/spanish_npc_house_n_exterior'
                                    }
                                },
                                '1135287336.43dzlu': {
                                    'Type':
                                    'Building Exterior',
                                    'Name':
                                    '',
                                    'File':
                                    '',
                                    'Color':
                                    (0.8999999761581421, 0.8999999761581421,
                                     0.8999999761581421, 1.0),
                                    'GridPos':
                                    Point3(406.469, 144.216, 44.471),
                                    'Hpr':
                                    VBase3(-2.991, 0.0, 0.0),
                                    'Objects': {
                                        '1135287336.43dzlu0': {
                                            'Type':
                                            'Locator Node',
                                            'Name':
                                            'portal_exterior_1',
                                            'GridPos':
                                            Point3(459.416, 119.097, 54.918),
                                            'Hpr':
                                            Point3(0.0, 0.0, 0.0),
                                            'Pos':
                                            Point3(54.084, -22.35, 10.9),
                                            'Scale':
                                            VBase3(1.0, 1.0, 1.0)
                                        }
                                    },
                                    'Pos':
                                    Point3(-106.985, -65.632, 44.261),
                                    'Scale':
                                    VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model':
                                        'models/buildings/spanish_npc_house_e_exterior'
                                    }
                                },
                                '1135287679.84dzlu': {
                                    'Type': 'Building Exterior',
                                    'Name': '',
                                    'File': '',
                                    'GridPos': Point3(619.451, 239.603,
                                                      50.495),
                                    'Hpr': VBase3(-5.258, 0.446, 0.01),
                                    'Objects': {
                                        '1135287679.84dzlu0': {
                                            'Type':
                                            'Locator Node',
                                            'Name':
                                            'portal_exterior_1',
                                            'GridPos':
                                            Point3(671.354, 212.33, 60.773),
                                            'Hpr':
                                            Point3(0.0, 0.0, 0.0),
                                            'Pos':
                                            Point3(54.084, -22.35, 10.9),
                                            'Scale':
                                            VBase3(1.0, 1.0, 1.0)
                                        }
                                    },
                                    'Pos': Point3(105.929, 29.739, 52.525),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model':
                                        'models/buildings/spanish_npc_house_g_exterior'
                                    }
                                },
                                '1135288077.32dzlu': {
                                    'Type': 'Building Exterior',
                                    'Name': '',
                                    'File': '',
                                    'GridPos': Point3(582.3, 150.231, 42.845),
                                    'Hpr': VBase3(-162.14, -1.043, 0.95),
                                    'Objects': {
                                        '1135288077.32dzlu0': {
                                            'Type':
                                            'Locator Node',
                                            'Name':
                                            'portal_exterior_1',
                                            'GridPos':
                                            Point3(523.962, 154.709, 53.801),
                                            'Hpr':
                                            Point3(0.0, 0.0, 0.0),
                                            'Pos':
                                            Point3(54.084, -22.35, 10.9),
                                            'Scale':
                                            VBase3(1.0, 1.0, 1.0)
                                        }
                                    },
                                    'Pos': Point3(68.853, -59.616, 44.33),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model':
                                        'models/buildings/spanish_npc_house_n_exterior'
                                    }
                                },
                                '1135288180.4dzlu': {
                                    'Type': 'Building Exterior',
                                    'Name': '',
                                    'File': '',
                                    'GridPos': Point3(582.2, 238.079, 51.316),
                                    'Hpr': VBase3(-2.43, -0.247, -0.174),
                                    'Objects': {
                                        '1135288180.41dzlu': {
                                            'Type':
                                            'Locator Node',
                                            'Name':
                                            'portal_exterior_1',
                                            'GridPos':
                                            Point3(635.361, 213.529, 62.02),
                                            'Hpr':
                                            Point3(0.0, 0.0, 0.0),
                                            'Pos':
                                            Point3(54.084, -22.35, 10.9),
                                            'Scale':
                                            VBase3(1.0, 1.0, 1.0)
                                        }
                                    },
                                    'Pos': Point3(68.672, 28.213, 52.986),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model':
                                        'models/buildings/spanish_npc_house_i_exterior'
                                    }
                                },
                                '1135289191.98dzlu': {
                                    'Type': 'Building Exterior',
                                    'Name': '',
                                    'File': '',
                                    'GridPos': Point3(516.357, 182.851,
                                                      45.291),
                                    'Hpr': VBase3(111.244, -1.415, 0.064),
                                    'Objects': {
                                        '1135289191.98dzlu0': {
                                            'Type':
                                            'Locator Node',
                                            'Name':
                                            'portal_exterior_1',
                                            'GridPos':
                                            Point3(517.439, 241.295, 56.545),
                                            'Hpr':
                                            Point3(0.0, 0.0, 0.0),
                                            'Pos':
                                            Point3(54.084, -22.35, 10.9),
                                            'Scale':
                                            VBase3(1.0, 1.0, 1.0)
                                        }
                                    },
                                    'Pos': Point3(2.89, -27.0, 46.214),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Name':
                                        '',
                                        'Door':
                                        'models/buildings/shanty_guildhall_door',
                                        'Model':
                                        'models/buildings/spanish_npc_house_i_exterior'
                                    }
                                },
                                '1135290323.54dzlu': {
                                    'Type': 'Building Exterior',
                                    'Name': '',
                                    'File': '',
                                    'GridPos': Point3(552.065, 106.788,
                                                      41.813),
                                    'Hpr': VBase3(172.41, -1.842, 0.527),
                                    'Objects': {
                                        '1135290323.54dzlu0': {
                                            'Type':
                                            'Locator Node',
                                            'Name':
                                            'portal_exterior_1',
                                            'GridPos':
                                            Point3(501.372, 135.779, 53.352),
                                            'Hpr':
                                            Point3(0.0, 0.0, 0.0),
                                            'Pos':
                                            Point3(54.084, -22.35, 10.9),
                                            'Scale':
                                            VBase3(1.0, 1.0, 1.0)
                                        }
                                    },
                                    'Pos': Point3(38.629, -103.057, 42.916),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model':
                                        'models/buildings/spanish_npc_house_e_exterior'
                                    }
                                },
                                '1135290764.99dzlu': {
                                    'Type': 'Building Exterior',
                                    'File': '',
                                    'GridPos': Point3(599.232, 132.7, 42.701),
                                    'Hpr': VBase3(67.39, 0.789, -1.31),
                                    'Pos': Point3(85.786, -77.147, 44.31),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model':
                                        'models/buildings/6shanty_tents'
                                    }
                                },
                                '1135971052.31dzlu': {
                                    'Type': 'Building Exterior',
                                    'Name': '',
                                    'File': '',
                                    'GridPos': Point3(527.49, 238.624, 49.24),
                                    'Hpr': VBase3(174.045, -0.174, 0.146),
                                    'Objects': {
                                        '1135971052.31dzlu0': {
                                            'Type':
                                            'Locator Node',
                                            'Name':
                                            'portal_exterior_1',
                                            'GridPos':
                                            Point3(476.091, 266.458, 60.502),
                                            'Hpr':
                                            Point3(0.0, 0.0, 0.0),
                                            'Pos':
                                            Point3(54.084, -22.35, 10.9),
                                            'Scale':
                                            VBase3(1.0, 1.0, 1.0)
                                        }
                                    },
                                    'Pos': Point3(13.984, 28.764, 50.388),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model':
                                        'models/buildings/spanish_npc_house_l_exterior'
                                    }
                                },
                                '1135971384.22dzlu': {
                                    'Type':
                                    'Building Exterior',
                                    'Name':
                                    '',
                                    'File':
                                    '',
                                    'Color':
                                    (0.8999999761581421, 0.8999999761581421,
                                     0.8999999761581421, 1.0),
                                    'GridPos':
                                    Point3(396.529, 187.718, 44.809),
                                    'Hpr':
                                    VBase3(72.321, 0.0, 0.0),
                                    'Objects': {
                                        '1135971384.22dzlu0': {
                                            'Type':
                                            'Locator Node',
                                            'Name':
                                            'portal_exterior_1',
                                            'GridPos':
                                            Point3(434.35, 232.484, 55.253),
                                            'Hpr':
                                            Point3(0.0, 0.0, 0.0),
                                            'Pos':
                                            Point3(54.084, -22.35, 10.9),
                                            'Scale':
                                            VBase3(1.0, 1.0, 1.0)
                                        }
                                    },
                                    'Pos':
                                    Point3(-116.928, -22.13, 44.597),
                                    'Scale':
                                    VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Name':
                                        '',
                                        'Color':
                                        (0.800000011920929, 0.800000011920929,
                                         0.800000011920929, 1.0),
                                        'Door':
                                        'models/buildings/shanty_guildhall_door',
                                        'Model':
                                        'models/buildings/spanish_npc_house_p_exterior'
                                    }
                                },
                                '1136336439.97dzlu': {
                                    'Type': 'Building Exterior',
                                    'Name': '',
                                    'File': '',
                                    'GridPos': Point3(419.851, 230.327,
                                                      46.057),
                                    'Hpr': VBase3(-2.617, -0.553, 1.759),
                                    'Objects': {
                                        '1136336439.97dzlu0': {
                                            'Type':
                                            'Locator Node',
                                            'Name':
                                            'portal_exterior_1',
                                            'GridPos':
                                            Point3(422.919, 210.132, 46.141),
                                            'Hpr':
                                            VBase3(90.0, 0.0, 0.0),
                                            'Pos':
                                            Point3(3.987, -20.033, 0.0),
                                            'Scale':
                                            VBase3(1.0, 1.0, 1.0)
                                        }
                                    },
                                    'Pos': Point3(-93.619, 20.475, 46.158),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model':
                                        'models/buildings/spanish_npc_house_i_exterior'
                                    }
                                },
                                '1136337021.82dzlu': {
                                    'Type': 'Building Exterior',
                                    'Name': '',
                                    'File': '',
                                    'GridPos': Point3(561.343, 296.843,
                                                      52.798),
                                    'Hpr': VBase3(-32.272, 0.396, -0.398),
                                    'Objects': {
                                        '1136337021.82dzlu0': {
                                            'Type':
                                            'Locator Node',
                                            'Name':
                                            'portal_exterior_1',
                                            'GridPos':
                                            Point3(554.017, 277.776, 52.798),
                                            'Hpr':
                                            VBase3(90.0, 0.0, 0.0),
                                            'Pos':
                                            Point3(3.987, -20.033, 0.0),
                                            'Scale':
                                            VBase3(1.0, 1.0, 1.0)
                                        }
                                    },
                                    'Pos': Point3(47.801, 86.975, 54.394),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model':
                                        'models/buildings/spanish_npc_house_g_exterior'
                                    }
                                },
                                '1136338230.04dzlu': {
                                    'Type': 'Barrel',
                                    'GridPos': Point3(498.132, 119.056,
                                                      41.663),
                                    'Hpr': VBase3(28.818, -0.934, -88.39),
                                    'Pos': Point3(-15.3, -90.787, 42.276),
                                    'Scale': VBase3(0.794, 0.794, 0.794),
                                    'Visual': {
                                        'Model': 'models/props/barrel'
                                    }
                                },
                                '1136338238.24dzlu': {
                                    'Type':
                                    'Barrel',
                                    'Color':
                                    (0.699999988079071, 0.699999988079071,
                                     0.699999988079071, 1.0),
                                    'GridPos':
                                    Point3(474.969, 135.354, 45.141),
                                    'Hpr':
                                    VBase3(-0.017, -1.691, -0.548),
                                    'Pos':
                                    Point3(-38.495, -74.496, 45.567),
                                    'Scale':
                                    VBase3(0.58, 0.58, 0.58),
                                    'Visual': {
                                        'Model': 'models/props/barrel_worn'
                                    }
                                },
                                '1136338245.68dzlu': {
                                    'Type':
                                    'Barrel',
                                    'Color':
                                    (0.6000000238418579, 0.6000000238418579,
                                     0.6000000238418579, 1.0),
                                    'GridPos':
                                    Point3(474.349, 142.353, 45.097),
                                    'Hpr':
                                    VBase3(0.104, 10.896, 3.466),
                                    'Pos':
                                    Point3(-39.114, -67.497, 45.532),
                                    'Scale':
                                    VBase3(0.52, 0.52, 0.52),
                                    'Visual': {
                                        'Model': 'models/props/barrel'
                                    }
                                },
                                '1136338473.55dzlu': {
                                    'Type': 'Barrel',
                                    'GridPos': Point3(475.142, 139.879,
                                                      45.291),
                                    'Hpr': VBase3(0.0, 0.122, -0.548),
                                    'Pos': Point3(-38.323, -69.972, 45.729),
                                    'Scale': VBase3(0.58, 0.58, 0.58),
                                    'Visual': {
                                        'Model': 'models/props/barrel'
                                    }
                                },
                                '1136338506.65dzlu': {
                                    'Type':
                                    'Barrel',
                                    'Color':
                                    (0.800000011920929, 0.800000011920929,
                                     0.800000011920929, 1.0),
                                    'GridPos':
                                    Point3(474.321, 137.649, 45.182),
                                    'Hpr':
                                    VBase3(0.0, 0.122, 3.828),
                                    'Pos':
                                    Point3(-39.143, -72.201, 45.607),
                                    'Scale':
                                    VBase3(0.544, 0.544, 0.544),
                                    'Visual': {
                                        'Model': 'models/props/barrel_grey'
                                    }
                                },
                                '1136338558.54dzlu': {
                                    'Type': 'Barrel',
                                    'GridPos': Point3(499.824, 117.179,
                                                      40.061),
                                    'Hpr': VBase3(0.0, 0.122, -0.548),
                                    'Pos': Point3(-13.592, -92.661, 40.687),
                                    'Scale': VBase3(0.773, 0.773, 0.773),
                                    'Visual': {
                                        'Model': 'models/props/barrel'
                                    }
                                },
                                '1136338586.88dzlu': {
                                    'Type': 'Barrel',
                                    'GridPos': Point3(503.107, 114.501,
                                                      40.063),
                                    'Hpr': VBase3(-0.007, -0.627, -0.548),
                                    'Pos': Point3(-10.31, -95.339, 40.714),
                                    'Scale': VBase3(0.588, 0.588, 0.588),
                                    'Visual': {
                                        'Model': 'models/props/barrel'
                                    }
                                },
                                '1136338641.41dzlu': {
                                    'Type': 'Barrel',
                                    'GridPos': Point3(527.455, 172.964,
                                                      45.243),
                                    'Hpr': VBase3(0.0, 0.122, -0.527),
                                    'Pos': Point3(13.988, -36.888, 46.251),
                                    'Scale': VBase3(0.528, 0.528, 0.528),
                                    'Visual': {
                                        'Model': 'models/props/barrel'
                                    }
                                },
                                '1136338645.27dzlu': {
                                    'Type': 'Barrel',
                                    'Color': (1.0, 0.9599999785423279, 0.75,
                                              1.0),
                                    'GridPos': Point3(502.859, 121.101,
                                                      45.333),
                                    'Hpr': VBase3(-0.059, -5.981, -0.551),
                                    'Pos': Point3(-10.608, -88.75, 45.996),
                                    'Scale': VBase3(0.591, 0.591, 0.591),
                                    'Visual': {
                                        'Model': 'models/props/barrel_worn'
                                    }
                                },
                                '1136338940.62dzlu': {
                                    'Type': 'Building Exterior',
                                    'Name': '',
                                    'File': '',
                                    'GridPos': Point3(584.719, 73.425, 42.454),
                                    'Hpr': VBase3(-179.196, 0.0, 0.0),
                                    'Objects': {},
                                    'Pos': Point3(71.276, -136.421, 43.798),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model':
                                        'models/buildings/spanish_npc_house_e_exterior'
                                    }
                                },
                                '1136339511.38dzlu': {
                                    'Type': 'Building Exterior',
                                    'Name': '',
                                    'File': '',
                                    'GridPos': Point3(638.78, 148.621, 44.757),
                                    'Hpr': VBase3(-61.673, 0.54, -0.153),
                                    'Objects': {
                                        '1136339511.38dzlu0': {
                                            'Type':
                                            'Locator Node',
                                            'Name':
                                            'portal_exterior_1',
                                            'GridPos':
                                            Point3(636.681, 117.451, 44.757),
                                            'Hpr':
                                            VBase3(-90.0, 0.0, 0.0),
                                            'Pos':
                                            Point3(26.442, -16.638, 0.0),
                                            'Scale':
                                            VBase3(1.0, 1.0, 1.0)
                                        }
                                    },
                                    'Pos': Point3(125.312, -61.231, 46.778),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model':
                                        'models/buildings/spanish_npc_house_e_exterior'
                                    }
                                },
                                '1136339759.96dzlu': {
                                    'Type': 'Tree',
                                    'GridPos': Point3(615.757, 264.977,
                                                      49.551),
                                    'Hpr': VBase3(0.0, 0.122, -0.548),
                                    'Pos': Point3(102.244, 55.115, 51.6),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model': 'models/vegetation/gen_tree_a'
                                    }
                                },
                                '1136339824.68dzlu': {
                                    'Type': 'Tree - Animated',
                                    'GridPos': Point3(546.332, 117.937,
                                                      40.041),
                                    'Hpr': VBase3(108.822, -0.558, 0.061),
                                    'Pos': Point3(32.914, -91.904, 41.113),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'SubObjs': {
                                        'Top Model': {
                                            'Visual': {
                                                'Animate':
                                                'models/vegetation/palm_leaf_a_idle',
                                                'Attach':
                                                ['trunk', 'def_trunk_attach'],
                                                'Model':
                                                'models/vegetation/palm_leaf_a_hi',
                                                'PartName':
                                                'leaf'
                                            }
                                        }
                                    },
                                    'Visual': {
                                        'Animate':
                                        'models/vegetation/palm_trunk_a_idle',
                                        'Model':
                                        'models/vegetation/palm_trunk_a_hi',
                                        'PartName': 'trunk'
                                    }
                                },
                                '1136339875.1dzlu': {
                                    'Type': 'Tree - Animated',
                                    'GridPos': Point3(564.231, 114.596, 39.77),
                                    'Hpr': VBase3(0.027, 2.901, -0.549),
                                    'Pos': Point3(50.814, -95.244, 41.006),
                                    'Scale': VBase3(0.826, 0.826, 0.826),
                                    'SubObjs': {
                                        'Top Model': {
                                            'Visual': {
                                                'Animate':
                                                'models/vegetation/palm_leaf_a_idle',
                                                'Attach':
                                                ['trunk', 'def_trunk_attach'],
                                                'Model':
                                                'models/vegetation/palm_leaf_a_hi',
                                                'PartName':
                                                'leaf'
                                            }
                                        }
                                    },
                                    'Visual': {
                                        'Animate':
                                        'models/vegetation/palm_trunk_a_idle',
                                        'Model':
                                        'models/vegetation/palm_trunk_a_hi',
                                        'PartName': 'trunk'
                                    }
                                },
                                '1136340207.4dzlu': {
                                    'Type': 'Building Exterior',
                                    'File': '',
                                    'GridPos': Point3(576.109, 109.362,
                                                      41.797),
                                    'Hpr': VBase3(-117.778, -0.627, 1.792),
                                    'Pos': Point3(62.673, -100.483, 43.136),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model':
                                        'models/buildings/3shanty_tents'
                                    }
                                },
                                '1136340387.18dzlu': {
                                    'Type':
                                    'Crate',
                                    'Color':
                                    (0.8999999761581421, 0.8999999761581421,
                                     0.699999988079071, 1.0),
                                    'GridPos':
                                    Point3(430.617, 133.022, 43.903),
                                    'Hpr':
                                    VBase3(20.659, 2.457, -1.511),
                                    'Objects': {},
                                    'Pos':
                                    Point3(-82.833, -76.825, 43.9),
                                    'Scale':
                                    VBase3(0.94, 0.94, 0.94),
                                    'Visual': {
                                        'Model': 'models/props/crate'
                                    }
                                },
                                '1136340454.07dzlu': {
                                    'Type': 'Crate',
                                    'Color': (0.75, 0.9300000071525574, 1.0,
                                              1.0),
                                    'GridPos': Point3(426.339, 132.851,
                                                      44.587),
                                    'Hpr': VBase3(9.204, 0.795, -0.684),
                                    'Pos': Point3(-87.117, -76.997, 44.543),
                                    'Scale': VBase3(0.555, 0.555, 0.555),
                                    'Visual': {
                                        'Color': (0.6000000238418579,
                                                  0.6000000238418579,
                                                  0.6000000238418579, 1.0),
                                        'Model':
                                        'models/props/crate'
                                    }
                                },
                                '1136340700.6dzlu': {
                                    'Type': 'Fountain',
                                    'GridPos': Point3(470.517, 247.691,
                                                      49.825),
                                    'Hpr': Point3(0.0, 0.0, 0.0),
                                    'Pos': Point3(-42.992, 37.831, 50.448),
                                    'Scale': VBase3(0.646, 0.646, 0.646),
                                    'Visual': {
                                        'Model':
                                        'models/props/spanishtown_fountain'
                                    }
                                },
                                '1136340768.34dzlu': {
                                    'Type': 'Well',
                                    'GridPos': Point3(598.105, 204.825,
                                                      47.959),
                                    'Hpr': VBase3(-33.998, 0.0, 0.0),
                                    'Pos': Point3(84.608, -5.034, 49.711),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model': 'models/props/wellA'
                                    }
                                },
                                '1136404083.2dzlu': {
                                    'Type': 'Tree',
                                    'GridPos': Point3(357.154, 225.788, 53.23),
                                    'Hpr': VBase3(35.876, 0.0, 0.0),
                                    'Pos': Point3(-156.382, 15.922, 52.722),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model': 'models/vegetation/gen_tree_a'
                                    }
                                },
                                '1136404538.39dzlu': {
                                    'Type': 'Tree',
                                    'GridPos': Point3(443.81, 299.359, 55.443),
                                    'Hpr': Point3(0.0, 0.0, 0.0),
                                    'Pos': Point3(-69.752, 89.487, 55.92),
                                    'Scale': VBase3(0.778, 0.778, 0.778),
                                    'Visual': {
                                        'Model': 'models/vegetation/gen_tree_a'
                                    }
                                },
                                '1136404682.97dzlu': {
                                    'Type': 'Tree',
                                    'GridPos': Point3(390.02, 173.377, 43.451),
                                    'Hpr': Point3(0.0, 0.0, 0.0),
                                    'Pos': Point3(-123.424, -36.468, 43.146),
                                    'Scale': VBase3(0.322, 0.322, 0.322),
                                    'Visual': {
                                        'Model': 'models/vegetation/gen_tree_e'
                                    }
                                },
                                '1136419067.84dzlu': {
                                    'Type': 'Tree - Animated',
                                    'GridPos': Point3(639.67, 74.543, 40.46),
                                    'Hpr': VBase3(0.0, 0.122, -0.548),
                                    'Pos': Point3(126.244, -135.3, 42.332),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'SubObjs': {
                                        'Top Model': {
                                            'Visual': {
                                                'Animate':
                                                'models/vegetation/palm_leaf_a_idle',
                                                'Attach':
                                                ['trunk', 'def_trunk_attach'],
                                                'Color': (0.932, 0.724, 0.7942,
                                                          1.0),
                                                'Model':
                                                'models/vegetation/palm_leaf_a_hi',
                                                'PartName':
                                                'leaf',
                                                'Scale':
                                                VBase3(1.385, 1.385, 1.385)
                                            }
                                        }
                                    },
                                    'Visual': {
                                        'Animate':
                                        'models/vegetation/palm_trunk_a_idle',
                                        'Color': (0.972, 0.882, 0.7942, 1.0),
                                        'Model':
                                        'models/vegetation/palm_trunk_a_hi',
                                        'PartName': 'trunk'
                                    }
                                },
                                '1136419185.55dzlu': {
                                    'Type': 'Tree - Animated',
                                    'GridPos': Point3(635.321, 71.413, 40.49),
                                    'Hpr': VBase3(-33.403, 0.807, -0.781),
                                    'Pos': Point3(121.894, -138.43, 42.314),
                                    'Scale': VBase3(1.162, 1.162, 1.162),
                                    'SubObjs': {
                                        'Top Model': {
                                            'Visual': {
                                                'Animate':
                                                'models/vegetation/palm_leaf_a_idle',
                                                'Attach':
                                                ['trunk', 'def_trunk_attach'],
                                                'Color': (0.7942, 0.882, 0.724,
                                                          1.0),
                                                'Model':
                                                'models/vegetation/palm_leaf_c_hi',
                                                'PartName':
                                                'leaf',
                                                'Scale':
                                                VBase3(0.682, 0.682, 0.682)
                                            }
                                        }
                                    },
                                    'Visual': {
                                        'Animate':
                                        'models/vegetation/palm_trunk_a_idle',
                                        'Color':
                                        (0.800000011920929, 0.800000011920929,
                                         0.800000011920929, 1.0),
                                        'Model':
                                        'models/vegetation/palm_trunk_a_hi',
                                        'PartName':
                                        'trunk'
                                    }
                                },
                                '1136419382.98dzlu': {
                                    'Type': 'Tree',
                                    'GridPos': Point3(654.349, 163.765,
                                                      44.361),
                                    'Hpr': VBase3(-8.086, 0.14, -0.178),
                                    'Pos': Point3(140.884, -46.087, 46.564),
                                    'Scale': VBase3(0.828, 0.828, 0.828),
                                    'Visual': {
                                        'Model': 'models/vegetation/gen_tree_d'
                                    }
                                },
                                '1136419448.56dzlu': {
                                    'Type': 'Bush',
                                    'GridPos': Point3(451.824, 278.755,
                                                      49.872),
                                    'Hpr': VBase3(-29.914, 0.379, -0.414),
                                    'Pos': Point3(-61.685, 68.895, 50.382),
                                    'Scale': VBase3(0.467, 0.467, 0.467),
                                    'Visual': {
                                        'Model': 'models/vegetation/bush_a'
                                    }
                                },
                                '1136419544.14dzlu': {
                                    'Type': 'Bush',
                                    'GridPos': Point3(457.552, 278.378,
                                                      49.563),
                                    'Hpr': VBase3(-84.184, 1.115, 0.132),
                                    'Pos': Point3(-55.954, 68.518, 50.127),
                                    'Scale': VBase3(0.512, 0.512, 0.512),
                                    'Visual': {
                                        'Model': 'models/vegetation/bush_c'
                                    }
                                },
                                '1136419587.27dzlu': {
                                    'Type': 'Bush',
                                    'GridPos': Point3(563.602, 271.858,
                                                      49.612),
                                    'Hpr': VBase3(-90.934, 1.655, 1.773),
                                    'Pos': Point3(50.091, 61.996, 51.177),
                                    'Scale': VBase3(0.668, 0.668, 0.668),
                                    'Visual': {
                                        'Model': 'models/vegetation/bush_c'
                                    }
                                },
                                '1136419722.31dzlu': {
                                    'Type': 'Bush',
                                    'GridPos': Point3(496.456, 207.551,
                                                      45.224),
                                    'Hpr': VBase3(-166.72, -1.031, 3.29),
                                    'Pos': Point3(-17.01, -2.3, 46.01),
                                    'Scale': VBase3(0.668, 0.668, 0.668),
                                    'Visual': {
                                        'Model': 'models/vegetation/bush_c'
                                    }
                                }
                            },
                            'Pos': Point3(513.025, 209.753, -0.951),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/town/bilgewater_town'
                            }
                        },
                        '1135285783.04dzlu': {
                            'Type': 'Building Exterior',
                            'Name': '',
                            'File': '',
                            'Hpr': VBase3(-2.263, 0.0, 0.0),
                            'Objects': {
                                '1135285783.04dzlu0': {
                                    'Type': 'Locator Node',
                                    'Name': 'portal_exterior_1',
                                    'GridPos': Point3(512.619, 310.089,
                                                      64.879),
                                    'Hpr': Point3(0.0, 0.0, 0.0),
                                    'Pos': Point3(54.084, -22.35, 10.9),
                                    'Scale': VBase3(1.0, 1.0, 1.0)
                                }
                            },
                            'Pos': Point3(459.46, 334.557, 53.979),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/spanish_npc_house_i_exterior'
                            }
                        },
                        '1135286034.37dzlu': {
                            'Type': 'Building Exterior',
                            'Name': '',
                            'File': '',
                            'Hpr': VBase3(77.954, 0.0, 0.0),
                            'Objects': {
                                '1135286034.37dzlu0': {
                                    'Type': 'Locator Node',
                                    'Name': 'portal_exterior_1',
                                    'GridPos': Point3(459.748, 364.058,
                                                      64.925),
                                    'Hpr': Point3(0.0, 0.0, 0.0),
                                    'Pos': Point3(54.084, -22.35, 10.9),
                                    'Scale': VBase3(1.0, 1.0, 1.0)
                                }
                            },
                            'Pos': Point3(426.603, 315.829, 54.025),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/spanish_npc_house_k_exterior'
                            }
                        },
                        '1136336848.57dzlu': {
                            'Type': 'Building Exterior',
                            'Name': '',
                            'File': '',
                            'Hpr': VBase3(75.549, 0.5, 0.255),
                            'Objects': {
                                '1136336848.57dzlu0': {
                                    'Type': 'Locator Node',
                                    'Name': 'portal_exterior_1',
                                    'GridPos': Point3(448.612, 261.981, 49.97),
                                    'Hpr': VBase3(90.0, 0.0, 0.0),
                                    'Pos': Point3(3.987, -20.033, 0.0),
                                    'Scale': VBase3(1.0, 1.0, 1.0)
                                }
                            },
                            'Pos': Point3(428.219, 263.119, 50.163),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Name':
                                '',
                                'Door':
                                'models/buildings/shanty_guildhall_door',
                                'Model':
                                'models/buildings/spanish_npc_house_a_exterior'
                            }
                        },
                        '1136338602.99dzlu': {
                            'Type': 'Barrel',
                            'Hpr': VBase3(-4.126, 19.806, 1.4),
                            'Pos': Point3(505.653, 138.22, 45.39),
                            'Scale': VBase3(0.731, 0.731, 0.731),
                            'Visual': {
                                'Model': 'models/props/barrel'
                            }
                        },
                        '1136339970.12dzlu': {
                            'Type': 'Tree - Animated',
                            'Hpr': VBase3(-123.565, 0.0, 0.0),
                            'Pos': Point3(374.587, 141.25, 41.661),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'SubObjs': {
                                'Top Model': {
                                    'Visual': {
                                        'Animate':
                                        'models/vegetation/palm_leaf_a_idle',
                                        'Attach':
                                        ['trunk', 'def_trunk_attach'],
                                        'Model':
                                        'models/vegetation/palm_leaf_b_hi',
                                        'PartName': 'leaf'
                                    }
                                }
                            },
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_trunk_a_idle',
                                'Model': 'models/vegetation/palm_trunk_a_hi',
                                'PartName': 'trunk'
                            }
                        },
                        '1136339985.6dzlu': {
                            'Type': 'Bush',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(383.68, 154.043, 43.127),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1136340427.54dzlu': {
                            'Type': 'Crate',
                            'Color': (0.75, 0.9300000071525574, 1.0, 1.0),
                            'Hpr': VBase3(-9.454, 4.603, 0.22),
                            'Pos': Point3(427.801, 129.03, 43.794),
                            'Scale': VBase3(0.84, 0.84, 0.84),
                            'Visual': {
                                'Color':
                                (0.800000011920929, 0.8999999761581421,
                                 0.699999988079071, 1.0),
                                'Model':
                                'models/props/crate'
                            }
                        },
                        '1136419266.19dzlu': {
                            'Type': 'Tree',
                            'Hpr': VBase3(0.0, 0.0, 0.0),
                            'Pos': Point3(646.485, 92.688, 42.561),
                            'Scale': VBase3(0.604, 0.604, 0.604),
                            'Visual': {
                                'Model': 'models/vegetation/gen_tree_a'
                            }
                        },
                        '1136419312.06dzlu': {
                            'Type': 'Tree',
                            'Hpr': VBase3(-8.086, -0.058, 0.348),
                            'Pos': Point3(649.669, 135.611, 44.328),
                            'Scale': VBase3(0.604, 0.604, 0.604),
                            'Visual': {
                                'Model': 'models/vegetation/gen_tree_d'
                            }
                        },
                        '1137608349.11dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-175.5, 0.0, 0.0),
                            'Pos':
                            Point3(559.301, 66.133, 41.246),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1137613670.55dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(113.073, 0.0, 0.0),
                            'Pos': Point3(638.507, 136.319, 44.731),
                            'Scale': VBase3(0.426, 0.426, 0.426),
                            'Visual': {
                                'Model': 'models/vegetation/bush_d'
                            }
                        },
                        '1137613686.39dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(168.669, 0.42, 6.905),
                            'Pos': Point3(575.801, 78.805, 41.537),
                            'Scale': VBase3(0.743, 0.743, 0.743),
                            'Visual': {
                                'Model': 'models/vegetation/bush_f'
                            }
                        },
                        '1137613748.45dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(-152.41, -4.661, 1.499),
                            'Pos': Point3(527.16, 70.568, 40.087),
                            'Scale': VBase3(1.01, 1.01, 1.01),
                            'Visual': {
                                'Model': 'models/vegetation/bush_b'
                            }
                        },
                        '1137613781.44dxschafe': {
                            'Type':
                            'Bush',
                            'Color': (1.0, 0.6000000238418579,
                                      0.800000011920929, 1.0),
                            'Hpr':
                            VBase3(139.966, 0.0, 0.282),
                            'Pos':
                            Point3(535.399, 53.541, 40.263),
                            'Scale':
                            VBase3(1.01, 1.01, 1.01),
                            'Visual': {
                                'Model': 'models/vegetation/bush_h'
                            }
                        },
                        '1137613814.03dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(44.172, 0.0, 0.0),
                            'Pos': Point3(538.27, 101.971, 41.442),
                            'Scale': VBase3(0.518, 0.518, 0.518),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1137804872.88dxschafe': {
                            'Type': 'LaundryRope',
                            'Hpr': VBase3(77.156, 0.0, 0.0),
                            'Pos': Point3(404.656, 165.025, 42.997),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/LaundryRope'
                            }
                        },
                        '1137804943.44dxschafe': {
                            'Type': 'LaundryRope',
                            'Hpr': VBase3(75.678, 0.0, 0.0),
                            'Pos': Point3(651.0, 137.761, 44.289),
                            'Scale': VBase3(0.67, 0.67, 0.67),
                            'Visual': {
                                'Model': 'models/props/LaundryRope'
                            }
                        },
                        '1137805005.17dxschafe': {
                            'Type': 'Sack',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(482.945, 121.352, 45.323),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1137805054.53dxschafe': {
                            'Type': 'Sack',
                            'Hpr': VBase3(19.023, -24.32, 33.705),
                            'Pos': Point3(506.833, 140.298, 46.253),
                            'Scale': VBase3(0.786, 0.786, 0.786),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1137805058.5dxschafe': {
                            'Type': 'Sack',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(485.705, 122.092, 46.166),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1137805059.83dxschafe': {
                            'Type': 'Sack',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(488.618, 122.115, 45.292),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1137805186.67dxschafe': {
                            'Type': 'LaundryRope',
                            'Hpr': VBase3(91.633, 0.0, 0.0),
                            'Pos': Point3(505.019, 154.374, 44.946),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/LaundryRope'
                            }
                        },
                        '1137813455.63dxschafe': {
                            'Type': 'Sack',
                            'Hpr': VBase3(0.0, 0.0, 0.083),
                            'Pos': Point3(428.452, 126.163, 43.532),
                            'Scale': VBase3(0.53, 0.53, 0.53),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1137813468.52dxschafe': {
                            'Type': 'Sack',
                            'Hpr': VBase3(0.0, 0.0, 4.117),
                            'Pos': Point3(425.84, 126.292, 44.219),
                            'Scale': VBase3(0.743, 0.743, 0.743),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1137813471.66dxschafe': {
                            'Type': 'Sack',
                            'Hpr': VBase3(-48.602, 0.0, 0.0),
                            'Pos': Point3(424.388, 125.752, 43.35),
                            'Scale': VBase3(0.743, 0.743, 0.743),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1137813490.89dxschafe': {
                            'Type': 'Sack',
                            'Hpr': VBase3(-96.828, 4.593, 7.167),
                            'Pos': Point3(424.088, 129.133, 43.879),
                            'Scale': VBase3(0.743, 0.743, 0.743),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1137813494.5dxschafe': {
                            'Type': 'Sack',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(430.995, 126.569, 43.372),
                            'Scale': VBase3(0.562, 0.562, 0.562),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1137813533.91dxschafe': {
                            'Type': 'Sack',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(427.586, 124.754, 43.414),
                            'Scale': VBase3(0.562, 0.562, 0.562),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1137813537.39dxschafe': {
                            'Type': 'Sack',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(430.078, 125.18, 43.314),
                            'Scale': VBase3(0.562, 0.562, 0.562),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1137813540.08dxschafe': {
                            'Type': 'Sack',
                            'Hpr': VBase3(23.067, 5.617, 0.0),
                            'Pos': Point3(429.342, 125.93, 44.158),
                            'Scale': VBase3(0.581, 0.581, 0.581),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1137815176.44dxschafe': {
                            'Type':
                            'Bush',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            Point3(0.0, 0.0, 0.0),
                            'Pos':
                            Point3(524.834, 193.068, 48.362),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/vegetation/bush_h'
                            }
                        },
                        '1138234931.06dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(0.0, 0.0, 0.0),
                            'Pos':
                            Point3(421.714, 139.717, 44.575),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138234946.94dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(85.769, 0.0, 0.0),
                            'Pos':
                            Point3(422.419, 149.643, 44.574),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138234981.19dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(85.769, 0.0, 0.425),
                            'Pos':
                            Point3(423.219, 159.425, 44.595),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138235031.23dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(85.769, 0.0, 0.0),
                            'Pos':
                            Point3(423.925, 169.395, 44.55),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138235106.0dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(163.476, 0.0, 0.0),
                            'Pos':
                            Point3(414.049, 173.295, 44.606),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138235258.19dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(163.476, 0.0, 0.0),
                            'Pos':
                            Point3(404.554, 176.106, 44.599),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138235266.48dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(163.476, 0.0, 0.0),
                            'Pos':
                            Point3(395.007, 178.929, 44.603),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138235274.27dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(163.476, 0.0, 0.0),
                            'Pos':
                            Point3(385.667, 181.65, 44.629),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138235338.59dxschafe': {
                            'Type': 'Cart',
                            'Hpr': VBase3(151.911, 0.0, 0.0),
                            'Pos': Point3(387.425, 137.694, 44.575),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/cart_reg'
                            }
                        },
                        '1138235427.92dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(75.968, 0.0, 0.0),
                            'Pos':
                            Point3(387.369, 181.172, 44.575),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138235463.38dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(75.968, 0.0, 0.0),
                            'Pos':
                            Point3(385.51, 173.657, 44.595),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138235468.97dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(75.968, 0.0, 0.0),
                            'Pos':
                            Point3(383.116, 164.057, 44.589),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138235509.02dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(81.354, 0.0, 0.0),
                            'Pos':
                            Point3(380.749, 154.565, 44.412),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138235729.28dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(-179.991, 0.0, 0.0),
                            'Pos':
                            Point3(386.945, 144.916, 44.424),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138235815.63dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(-179.991, 0.0, 0.0),
                            'Pos':
                            Point3(377.455, 144.903, 44.446),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138236384.59dxschafe': {
                            'Type': 'Building Exterior',
                            'Name': '',
                            'File': '',
                            'Hpr': VBase3(178.804, 0.0, 0.0),
                            'Objects': {},
                            'Pos': Point3(538.137, 72.645, 41.113),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Door':
                                'models/buildings/shanty_guildhall_door',
                                'Model':
                                'models/buildings/spanish_npc_house_n_exterior'
                            }
                        },
                        '1138237076.48dxschafe': {
                            'Type': 'Well',
                            'Hpr': VBase3(70.739, 0.0, 0.0),
                            'Pos': Point3(437.947, 208.556, 46.21),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/wellA'
                            }
                        },
                        '1138237587.53dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-179.026, 0.0, 0.0),
                            'Pos':
                            Point3(549.729, 66.0, 41.229),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138237708.88dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-179.026, 0.0, 0.0),
                            'Pos':
                            Point3(568.525, 67.055, 41.175),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138237708.95dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.800000011920929, 0.800000011920929,
                                      0.800000011920929, 1.0),
                            'Hpr':
                            VBase3(-179.026, 0.0, 0.0),
                            'Pos':
                            Point3(595.721, 65.626, 42.206),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138320597.94dxschafe': {
                            'Type': 'Crate',
                            'Color': (0.75, 1.0, 0.8500000238418579, 1.0),
                            'Hpr': VBase3(-22.783, 5.949, 0.0),
                            'Objects': {},
                            'Pos': Point3(419.475, 128.22, 43.599),
                            'Scale': VBase3(1.03, 1.03, 1.03),
                            'Visual': {
                                'Model': 'models/props/crate'
                            }
                        },
                        '1138322207.67dxschafe': {
                            'Type': 'Rock',
                            'Hpr': VBase3(171.929, -0.375, 1.826),
                            'Pos': Point3(562.761, 118.062, 41.512),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/props/zz_dont_use_rocks_Dk_group_2F'
                            }
                        },
                        '1138331085.67dxschafe': {
                            'Type': 'Building Exterior',
                            'Name': '',
                            'File': '',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Objects': {
                                '1138331085.67dxschafe0': {
                                    'Type': 'Locator Node',
                                    'Name': 'portal_exterior_1',
                                    'GridPos': Point3(511.483, 119.419, 45.27),
                                    'Hpr': VBase3(-90.0, 0.0, 0.0),
                                    'Pos': Point3(26.442, -16.638, 0.0),
                                    'Scale': VBase3(1.0, 1.0, 1.0)
                                }
                            },
                            'Pos': Point3(485.041, 136.057, 45.27),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/spanish_tavern_exterior'
                            }
                        },
                        '1138333953.2dxschafe': {
                            'Type':
                            'TreeBase',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(23.584, 0.0, 0.0),
                            'Pos':
                            Point3(572.858, 207.144, 46.709),
                            'Scale':
                            VBase3(1.238, 1.238, 1.238),
                            'Visual': {
                                'Color': (0.55, 0.52, 0.48, 1.0),
                                'Model': 'models/props/TreeBase'
                            }
                        },
                        '1138333987.34dxschafe': {
                            'Type':
                            'TreeBase',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            Point3(0.0, 0.0, 0.0),
                            'Pos':
                            Point3(594.045, 182.287, 45.857),
                            'Scale':
                            VBase3(1.112, 1.112, 1.112),
                            'Visual': {
                                'Color':
                                (0.6000000238418579, 0.6000000238418579,
                                 0.6000000238418579, 1.0),
                                'Model':
                                'models/props/TreeBase'
                            }
                        },
                        '1138334081.11dxschafe': {
                            'Type': 'Tree - Animated',
                            'Animate': 'models/vegetation/tree_b_trunk_idle',
                            'Hpr': VBase3(0.0, 0.0, -1.148),
                            'Pos': Point3(573.161, 207.118, 50.366),
                            'Scale': VBase3(0.669, 0.669, 0.669),
                            'SubObjs': {
                                'Top Model': {
                                    'Visual': {
                                        'Animate':
                                        'models/vegetation/tree_b_leaf_idle',
                                        'Attach':
                                        ['trunk', 'def_trunk_attach'],
                                        'Model':
                                        'models/vegetation/tree_b_leaf_hi',
                                        'PartName': 'leaf'
                                    }
                                }
                            },
                            'Visual': {
                                'Animate':
                                'models/vegetation/tree_b_trunk_idle',
                                'Model': 'models/vegetation/tree_b_trunk_hi',
                                'PartName': 'trunk'
                            }
                        },
                        '1138334199.27dxschafe': {
                            'Type': 'Tree - Animated',
                            'Animate': 'models/vegetation/tree_b_trunk_idle',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(594.059, 182.306, 41.11),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'SubObjs': {
                                'Top Model': {
                                    'Visual': {
                                        'Animate':
                                        'models/vegetation/palm_leaf_a_idle',
                                        'Attach':
                                        ['trunk', 'def_trunk_attach'],
                                        'Model':
                                        'models/vegetation/tree_b_leaf_hi',
                                        'PartName': 'leaf'
                                    }
                                }
                            },
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_trunk_a_idle',
                                'Model': 'models/vegetation/tree_b_trunk_hi',
                                'PartName': 'trunk'
                            }
                        },
                        '1138387864.66dxschafe': {
                            'Type': 'Sack',
                            'Hpr': VBase3(64.547, 0.0, -35.645),
                            'Pos': Point3(482.048, 121.75, 46.598),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1138388039.38dxschafe': {
                            'Type': 'Barrel',
                            'Hpr': VBase3(0.0, -0.611, 0.0),
                            'Pos': Point3(512.194, 138.211, 45.305),
                            'Scale': VBase3(0.573, 0.573, 0.573),
                            'Visual': {
                                'Model': 'models/props/barrel_group_1'
                            }
                        },
                        '1138388168.08dxschafe': {
                            'Type': 'Barrel',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(486.744, 102.724, 41.133),
                            'Scale': VBase3(0.563, 0.563, 0.563),
                            'Visual': {
                                'Model': 'models/props/barrel_group_1'
                            }
                        },
                        '1138388213.14dxschafe': {
                            'Type': 'Barrel',
                            'Hpr': VBase3(-46.688, 0.0, 0.0),
                            'Pos': Point3(480.996, 103.329, 41.407),
                            'Scale': VBase3(0.65, 0.65, 0.65),
                            'Visual': {
                                'Model': 'models/props/barrel_sideways'
                            }
                        },
                        '1138388273.94dxschafe': {
                            'Type':
                            'Barrel',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(-42.137, 2.546, -0.232),
                            'Pos':
                            Point3(494.273, 103.665, 41.44),
                            'Scale':
                            VBase3(0.532, 0.532, 0.532),
                            'Visual': {
                                'Model': 'models/props/barrel_sideways'
                            }
                        },
                        '1138388277.56dxschafe': {
                            'Type': 'Barrel',
                            'Hpr': VBase3(10.811, 0.0, -0.166),
                            'Pos': Point3(480.503, 106.917, 45.297),
                            'Scale': VBase3(0.5, 0.5, 0.5),
                            'Visual': {
                                'Model': 'models/props/barrel_sideways'
                            }
                        },
                        '1138388281.3dxschafe': {
                            'Type':
                            'Barrel',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(37.899, 48.278, -8.229),
                            'Pos':
                            Point3(490.621, 104.726, 42.642),
                            'Scale':
                            VBase3(0.457, 0.457, 0.457),
                            'Visual': {
                                'Model': 'models/props/barrel_sideways'
                            }
                        },
                        '1138388418.02dxschafe': {
                            'Type':
                            'Barrel',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(32.51, 8.016, -5.52),
                            'Pos':
                            Point3(487.401, 106.626, 45.276),
                            'Scale':
                            VBase3(0.578, 0.578, 0.578),
                            'Visual': {
                                'Model': 'models/props/barrel_sideways'
                            }
                        },
                        '1138388461.27dxschafe': {
                            'Type': 'Bucket',
                            'Hpr': VBase3(0.0, -18.43, 0.0),
                            'Pos': Point3(480.578, 103.097, 43.948),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/bucket'
                            }
                        },
                        '1138388531.19dxschafe': {
                            'Type': 'Bucket',
                            'Hpr': VBase3(0.0, 2.32, 0.0),
                            'Pos': Point3(504.001, 118.66, 45.292),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/bucket'
                            }
                        },
                        '1138388588.09dxschafe': {
                            'Type':
                            'Bucket',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(0.0, 0.146, 0.0),
                            'Pos':
                            Point3(592.426, 204.037, 48.075),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/bucket'
                            }
                        },
                        '1138388642.84dxschafe': {
                            'Type': 'Cart',
                            'Hpr': VBase3(80.098, 0.0, 8.622),
                            'Pos': Point3(564.07, 206.389, 48.116),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/cart_reg'
                            }
                        },
                        '1138388723.69dxschafe': {
                            'Type': 'Sack',
                            'Hpr': VBase3(0.0, 0.0, -28.678),
                            'Pos': Point3(588.889, 183.68, 48.207),
                            'Scale': VBase3(0.729, 0.729, 0.729),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1138388725.05dxschafe': {
                            'Type': 'Sack',
                            'Hpr': VBase3(-50.912, 6.335, -34.909),
                            'Pos': Point3(589.528, 185.46, 48.74),
                            'Scale': VBase3(0.716, 0.716, 0.716),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1138389026.84dxschafe': {
                            'Type': 'Bucket',
                            'Hpr': VBase3(79.256, -4.032, -5.49),
                            'Pos': Point3(440.247, 209.653, 49.085),
                            'Scale': VBase3(0.852, 0.852, 0.852),
                            'Visual': {
                                'Model': 'models/props/bucket'
                            }
                        },
                        '1138389038.28dxschafe': {
                            'Type': 'Bucket',
                            'Color': (1.0, 0.9599999785423279, 0.75, 1.0),
                            'Hpr': VBase3(18.31, 0.0, 0.0),
                            'Pos': Point3(439.52, 203.527, 46.208),
                            'Scale': VBase3(0.824, 0.824, 0.824),
                            'Visual': {
                                'Model': 'models/props/bucket'
                            }
                        },
                        '1138389053.84dxschafe': {
                            'Type': 'Bucket',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(575.592, 114.787, 45.049),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/bucket'
                            }
                        },
                        '1138389054.97dxschafe': {
                            'Type': 'Bucket',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(548.444, 117.223, 42.821),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/bucket'
                            }
                        },
                        '1138389058.48dxschafe': {
                            'Type': 'Bucket',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(577.119, 136.791, 43.012),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/bucket'
                            }
                        },
                        '1138389425.27dxschafe': {
                            'Type':
                            'Rope',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(72.229, 0.0, 0.0),
                            'Pos':
                            Point3(478.209, 106.648, 45.292),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/rope_pile'
                            }
                        },
                        '1138389506.56dxschafe': {
                            'Type':
                            'Crate',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(22.633, 3.523, -0.965),
                            'Objects': {
                                '1138727460.57dxschafe': {
                                    'Type': 'ChickenCage',
                                    'GridPos': Point3(450.103, 87.215, 44.149),
                                    'Hpr': VBase3(19.053, -3.017, 2.06),
                                    'Pos': Point3(-0.013, 0.194, 5.431),
                                    'Scale': VBase3(1.384, 1.384, 1.384),
                                    'Visual': {
                                        'Model': 'models/props/ChickenCage'
                                    }
                                }
                            },
                            'Pos':
                            Point3(450.134, 87.338, 40.222),
                            'Scale':
                            VBase3(0.723, 0.723, 0.723),
                            'Visual': {
                                'Color':
                                (0.6000000238418579, 0.6000000238418579,
                                 0.6000000238418579, 1.0),
                                'Model':
                                'models/props/crate'
                            }
                        },
                        '1138389517.22dxschafe': {
                            'Type':
                            'Crate',
                            'Color': (0.6000000238418579, 0.6000000238418579,
                                      0.6000000238418579, 1.0),
                            'Hpr':
                            VBase3(41.741, 3.475, 0.0),
                            'Objects': {},
                            'Pos':
                            Point3(454.794, 88.86, 40.303),
                            'Scale':
                            VBase3(1.147, 1.147, 1.147),
                            'Visual': {
                                'Color': (0.800000011920929, 0.800000011920929,
                                          0.800000011920929, 1.0),
                                'Model':
                                'models/props/crate'
                            }
                        },
                        '1138389532.89dxschafe': {
                            'Type': 'Crate',
                            'Hpr': VBase3(83.482, 0.0, 0.0),
                            'Objects': {
                                '1138660462.68dxschafe': {
                                    'Type': 'Sack',
                                    'GridPos': Point3(518.425, 166.558,
                                                      48.874),
                                    'Hpr': VBase3(-62.421, 0.0, 0.0),
                                    'Pos': Point3(-0.121, 0.539, 2.747),
                                    'Scale': VBase3(0.785, 0.785, 0.785),
                                    'Visual': {
                                        'Model': 'models/props/Sack'
                                    }
                                }
                            },
                            'Pos': Point3(519.141, 166.635, 45.292),
                            'Scale': VBase3(1.304, 1.304, 1.304),
                            'Visual': {
                                'Model': 'models/props/crate'
                            }
                        },
                        '1138389571.83dxschafe': {
                            'Type': 'Cart',
                            'Hpr': VBase3(73.631, 3.467, 0.0),
                            'Pos': Point3(503.413, 241.128, 48.861),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/cart_reg'
                            }
                        },
                        '1138389651.89dxschafe': {
                            'Type': 'ChickenCage',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(585.744, 113.012, 41.966),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/ChickenCage'
                            }
                        },
                        '1138389671.64dxschafe': {
                            'Type': 'ChickenCage',
                            'Hpr': VBase3(-39.138, 0.0, 0.0),
                            'Pos': Point3(583.737, 106.726, 41.741),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/ChickenCage'
                            }
                        },
                        '1138389681.59dxschafe': {
                            'Type': 'ChickenCage',
                            'Hpr': VBase3(-25.461, 0.0, 0.0),
                            'Pos': Point3(566.612, 100.629, 41.66),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/ChickenCage'
                            }
                        },
                        '1138389697.72dxschafe': {
                            'Type': 'ChickenCage',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(580.444, 137.969, 43.182),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/ChickenCage'
                            }
                        },
                        '1138389731.03dxschafe': {
                            'Type': 'ChickenCage',
                            'Hpr': VBase3(4.15, 0.0, 0.0),
                            'Pos': Point3(599.079, 186.519, 47.456),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/ChickenCage'
                            }
                        },
                        '1138389735.67dxschafe': {
                            'Type':
                            'ChickenCage',
                            'Color': (0.800000011920929, 0.800000011920929,
                                      0.800000011920929, 1.0),
                            'Hpr':
                            Point3(0.0, 0.0, 0.0),
                            'Pos':
                            Point3(595.842, 187.738, 48.05),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/ChickenCage'
                            }
                        },
                        '1138389791.17dxschafe': {
                            'Type': 'Bush',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(593.748, 182.392, 48.47),
                            'Scale': VBase3(0.375, 0.375, 0.375),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1138389895.67dxschafe': {
                            'Type':
                            'Bush',
                            'Color': (0.6000000238418579, 0.6000000238418579,
                                      0.6000000238418579, 1.0),
                            'Hpr':
                            VBase3(-55.429, 0.0, 0.0),
                            'Pos':
                            Point3(585.666, 227.636, 51.086),
                            'Scale':
                            VBase3(0.48, 0.48, 0.48),
                            'Visual': {
                                'Model': 'models/vegetation/bush_h'
                            }
                        },
                        '1138389900.19dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(0.0, 1.049, 0.0),
                            'Pos': Point3(572.482, 207.237, 48.801),
                            'Scale': VBase3(0.376, 0.376, 0.376),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1138390629.63dxschafe': {
                            'Type': 'Trellis',
                            'Hpr': VBase3(24.744, 0.0, 0.0),
                            'Pos': Point3(525.441, 164.115, 44.557),
                            'Scale': VBase3(0.756, 0.756, 0.756),
                            'Visual': {
                                'Model': 'models/props/trellisB'
                            }
                        },
                        '1138390780.11dxschafe': {
                            'Type': 'Trellis',
                            'Hpr': VBase3(2.925, 0.0, 0.0),
                            'Pos': Point3(559.044, 67.043, 41.354),
                            'Scale': VBase3(0.641, 0.641, 0.641),
                            'Visual': {
                                'Model': 'models/props/trellisB'
                            }
                        },
                        '1138390880.48dxschafe': {
                            'Type': 'Trellis',
                            'Hpr': VBase3(76.12, 0.0, 0.0),
                            'Pos': Point3(422.773, 289.927, 53.924),
                            'Scale': VBase3(0.612, 0.612, 0.612),
                            'Visual': {
                                'Model': 'models/props/trellisA'
                            }
                        },
                        '1138391578.09dxschafe': {
                            'Type': 'Bucket',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(431.776, 263.947, 50.251),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/bucket'
                            }
                        },
                        '1138391585.31dxschafe': {
                            'Type': 'Bucket',
                            'Hpr': VBase3(-0.109, 1.187, 5.264),
                            'Pos': Point3(498.288, 237.312, 49.159),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/bucket'
                            }
                        },
                        '1138391627.27dxschafe': {
                            'Type': 'Sack',
                            'Hpr': VBase3(4.158, 14.616, -28.517),
                            'Pos': Point3(459.502, 244.538, 50.303),
                            'Scale': VBase3(0.546, 0.546, 0.546),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1138391644.33dxschafe': {
                            'Type': 'Sack',
                            'Hpr': VBase3(-63.641, 30.441, 13.577),
                            'Pos': Point3(460.311, 242.541, 50.162),
                            'Scale': VBase3(0.583, 0.583, 0.583),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1138391763.7dxschafe': {
                            'Type': 'ChickenCage',
                            'Hpr': VBase3(6.674, 0.0, 0.0),
                            'Pos': Point3(461.236, 238.953, 49.824),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/ChickenCage'
                            }
                        },
                        '1138391801.88dxschafe': {
                            'Type': 'TreeBase',
                            'Color': (1.0, 0.9599999785423279, 0.75, 1.0),
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(508.499, 281.587, 54.108),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/TreeBase'
                            }
                        },
                        '1138391811.81dxschafe': {
                            'Type': 'TreeBase',
                            'Color': (1.0, 0.9599999785423279, 0.75, 1.0),
                            'Hpr': VBase3(-2.634, 0.0, 0.0),
                            'Pos': Point3(484.452, 282.554, 54.038),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/TreeBase'
                            }
                        },
                        '1138391829.34dxschafe': {
                            'Type': 'TreeBase',
                            'Color': (1.0, 0.9599999785423279, 0.75, 1.0),
                            'Hpr': VBase3(-2.634, 0.0, 0.0),
                            'Pos': Point3(535.437, 279.938, 54.013),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/TreeBase'
                            }
                        },
                        '1138391837.23dxschafe': {
                            'Type':
                            'TreeBase',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-59.962, 0.0, 0.0),
                            'Pos':
                            Point3(529.697, 150.929, 44.442),
                            'Scale':
                            VBase3(0.97, 0.97, 0.97),
                            'Visual': {
                                'Color':
                                (0.8999999761581421, 0.8999999761581421,
                                 0.699999988079071, 1.0),
                                'Model':
                                'models/props/TreeBase'
                            }
                        },
                        '1138391837.27dxschafe': {
                            'Type': 'TreeBase',
                            'Color': (1.0, 0.9599999785423279, 0.75, 1.0),
                            'Hpr': VBase3(-2.634, 0.0, 0.0),
                            'Pos': Point3(461.183, 283.354, 54.056),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/TreeBase'
                            }
                        },
                        '1138391934.66dxschafe': {
                            'Type': 'Crate',
                            'Color': (0.75, 0.9300000071525574, 1.0, 1.0),
                            'Hpr': VBase3(-24.988, 0.0, 0.0),
                            'Pos': Point3(477.466, 120.53, 45.292),
                            'Scale': VBase3(0.682, 0.682, 0.682),
                            'Visual': {
                                'Color': (0.79, 0.73, 0.66, 1.0),
                                'Model': 'models/props/crate'
                            }
                        },
                        '1138392003.38dxschafe': {
                            'Type': 'Tree',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(528.933, 150.495, 47.234),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/vegetation/gen_tree_d'
                            }
                        },
                        '1138392072.44dxschafe': {
                            'Type': 'Building Exterior',
                            'Name': '',
                            'File': '',
                            'Hpr': VBase3(-162.926, -1.617, -0.543),
                            'Objects': {
                                '1138392072.44dxschafe0': {
                                    'Type': 'Locator Node',
                                    'Name': 'portal_exterior_1',
                                    'GridPos': Point3(607.944, 97.417, 43.188),
                                    'Hpr': VBase3(90.0, 0.0, 0.0),
                                    'Pos': Point3(3.987, -20.033, 0.0),
                                    'Scale': VBase3(1.0, 1.0, 1.0)
                                }
                            },
                            'Pos': Point3(617.634, 79.446, 42.585),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/spanish_npc_house_o_exterior'
                            }
                        },
                        '1138392261.67dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.800000011920929, 0.800000011920929,
                                      0.800000011920929, 1.0),
                            'Hpr':
                            VBase3(-179.026, 0.0, 0.087),
                            'Pos':
                            Point3(605.632, 65.832, 42.169),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138393769.47dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.800000011920929, 0.800000011920929,
                                      0.800000011920929, 1.0),
                            'Hpr':
                            VBase3(-91.898, 0.0, 0.0),
                            'Pos':
                            Point3(635.287, 180.304, 46.746),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138393826.88dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.800000011920929, 0.800000011920929,
                                      0.800000011920929, 1.0),
                            'Hpr':
                            VBase3(-90.776, 0.0, 0.0),
                            'Pos':
                            Point3(635.148, 170.312, 46.752),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138393837.09dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-0.602, 0.0, 0.0),
                            'Pos': Point3(646.071, 169.182, 46.827),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138393859.16dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-0.602, 0.0, 0.0),
                            'Pos': Point3(654.093, 169.119, 46.838),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138393933.52dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-89.388, 0.0, 0.0),
                            'Pos': Point3(653.833, 170.446, 46.81),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138393950.38dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(86.893, 0.0, 0.0),
                            'Pos': Point3(655.648, 170.407, 47.136),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/TallWallStucco_Column'
                            }
                        },
                        '1138393965.91dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-84.595, 0.0, 0.0),
                            'Pos': Point3(652.365, 190.291, 46.829),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138393973.61dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-80.755, 0.0, 0.0),
                            'Pos': Point3(651.458, 200.043, 46.825),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138394150.83dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-83.625, 0.0, 0.0),
                            'Pos': Point3(653.836, 179.903, 46.831),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138394281.47dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-80.2, 0.0, 0.0),
                            'Pos': Point3(649.885, 209.842, 46.827),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138394418.23dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.8999999761581421, 1.0),
                            'Hpr':
                            VBase3(-179.182, 0.0, 0.0),
                            'Pos':
                            Point3(635.205, 170.413, 46.005),
                            'Scale':
                            VBase3(1.213, 1.213, 1.213),
                            'Visual': {
                                'Model':
                                'models/buildings/LowWallStucco_column'
                            }
                        },
                        '1138394586.5dxschafe': {
                            'Type': 'LaundryRope',
                            'Hpr': VBase3(-83.031, 0.0, 0.0),
                            'Pos': Point3(645.338, 177.843, 47.23),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/LaundryRope'
                            }
                        },
                        '1138394804.84dxschafe': {
                            'Type':
                            'Barrel',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            Point3(0.0, 0.0, 0.0),
                            'Pos':
                            Point3(540.757, 109.26, 41.791),
                            'Scale':
                            VBase3(0.692, 0.692, 0.692),
                            'Visual': {
                                'Model': 'models/props/barrel_worn'
                            }
                        },
                        '1138394852.03dxschafe': {
                            'Type': 'Tree - Animated',
                            'Animate': 'models/vegetation/palm_trunk_a_idle',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(484.591, 283.645, 55.259),
                            'Scale': VBase3(0.24, 0.24, 0.24),
                            'SubObjs': {
                                'Top Model': {
                                    'Visual': {
                                        'Animate':
                                        'models/vegetation/palm_leaf_a_idle',
                                        'Attach':
                                        ['trunk', 'def_trunk_attach'],
                                        'Model':
                                        'models/vegetation/palm_leaf_c_hi',
                                        'PartName': 'leaf',
                                        'Scale': VBase3(3.084, 3.084, 3.084)
                                    }
                                }
                            },
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_trunk_a_idle',
                                'Model': 'models/vegetation/palm_trunk_b_hi',
                                'PartName': 'trunk'
                            }
                        },
                        '1138395108.81dxschafe': {
                            'Type': 'Tree - Animated',
                            'Animate': 'models/vegetation/palm_trunk_a_idle',
                            'Hpr': VBase3(70.721, 0.0, 0.0),
                            'Pos': Point3(508.472, 282.089, 54.019),
                            'Scale': VBase3(0.24, 0.24, 0.24),
                            'SubObjs': {
                                'Top Model': {
                                    'Visual': {
                                        'Animate':
                                        'models/vegetation/palm_leaf_a_idle',
                                        'Attach':
                                        ['trunk', 'def_trunk_attach'],
                                        'Model':
                                        'models/vegetation/palm_leaf_c_hi',
                                        'PartName': 'leaf',
                                        'Scale': VBase3(3.084, 3.084, 3.084)
                                    }
                                }
                            },
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_trunk_a_idle',
                                'Model': 'models/vegetation/palm_trunk_b_hi',
                                'PartName': 'trunk'
                            }
                        },
                        '1138395123.31dxschafe': {
                            'Type': 'Tree - Animated',
                            'Animate': 'models/vegetation/palm_trunk_a_idle',
                            'Hpr': VBase3(107.868, 0.0, 0.0),
                            'Pos': Point3(461.037, 283.646, 54.049),
                            'Scale': VBase3(0.281, 0.281, 0.281),
                            'SubObjs': {
                                'Top Model': {
                                    'Visual': {
                                        'Animate':
                                        'models/vegetation/palm_leaf_a_idle',
                                        'Attach':
                                        ['trunk', 'def_trunk_attach'],
                                        'Model':
                                        'models/vegetation/palm_leaf_c_hi',
                                        'PartName': 'leaf',
                                        'Scale': VBase3(3.084, 3.084, 3.084)
                                    }
                                }
                            },
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_trunk_a_idle',
                                'Model': 'models/vegetation/palm_trunk_b_hi',
                                'PartName': 'trunk'
                            }
                        },
                        '1138395147.94dxschafe': {
                            'Type': 'Tree - Animated',
                            'Animate': 'models/vegetation/palm_trunk_a_idle',
                            'Hpr': VBase3(166.852, 0.0, 0.0),
                            'Pos': Point3(535.837, 279.989, 54.013),
                            'Scale': VBase3(0.186, 0.186, 0.186),
                            'SubObjs': {
                                'Top Model': {
                                    'Visual': {
                                        'Animate':
                                        'models/vegetation/palm_leaf_a_idle',
                                        'Attach':
                                        ['trunk', 'def_trunk_attach'],
                                        'Model':
                                        'models/vegetation/palm_leaf_c_hi',
                                        'PartName': 'leaf',
                                        'Scale': VBase3(3.084, 3.084, 3.084)
                                    }
                                }
                            },
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_trunk_a_idle',
                                'Model': 'models/vegetation/palm_trunk_b_hi',
                                'PartName': 'trunk'
                            }
                        },
                        '1138395456.77dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(-92.957, 2.851, 0.0),
                            'Pos':
                            Point3(508.11, 232.111, 45.151),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138396021.42dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(175.318, -0.691, -0.931),
                            'Pos':
                            Point3(539.905, 227.078, 44.809),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Color': (0.699999988079071, 0.699999988079071,
                                          0.699999988079071, 1.0),
                                'Model':
                                'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138396274.88dxschafe': {
                            'Type':
                            'TreeBase',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            Point3(0.0, 0.0, 0.0),
                            'Pos':
                            Point3(443.767, 298.924, 53.962),
                            'Scale':
                            VBase3(0.828, 0.828, 0.828),
                            'Visual': {
                                'Model': 'models/props/TreeBase'
                            }
                        },
                        '1138396332.89dxschafe': {
                            'Type':
                            'Barrel',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            Point3(0.0, 0.0, 0.0),
                            'Pos':
                            Point3(446.644, 303.652, 54.055),
                            'Scale':
                            VBase3(0.429, 0.429, 0.429),
                            'Visual': {
                                'Model': 'models/props/barrel_worn'
                            }
                        },
                        '1138396364.92dxschafe': {
                            'Type': 'Barrel',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(514.161, 298.132, 54.021),
                            'Scale': VBase3(0.486, 0.486, 0.486),
                            'Visual': {
                                'Model': 'models/props/barrel'
                            }
                        },
                        '1138396646.31dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(-10.118, -1.171, -0.209),
                            'Pos':
                            Point3(423.976, 169.246, 44.95),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_Column'
                            }
                        },
                        '1138397707.13dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-23.529, 0.0, 0.0),
                            'Pos':
                            Point3(386.921, 179.721, 44.396),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/TallWallStucco_Column'
                            }
                        },
                        '1138401436.53dxschafe': {
                            'Type': 'Townsperson',
                            'Category': 'Commoner',
                            'DNA': '1138401436.53dxschafe',
                            'Hpr': VBase3(-126.964, 0.0, 0.0),
                            'Pos': Point3(606.292, 128.53, 42.33),
                            'Respawns': True,
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Start State': 'Idle'
                        },
                        '1138402892.06dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(-150.61, 0.0, 0.0),
                            'Pos': Point3(417.868, 146.465, 44.575),
                            'Scale': VBase3(0.776, 0.776, 0.776),
                            'Visual': {
                                'Model': 'models/vegetation/bush_c'
                            }
                        },
                        '1138402997.55dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(16.183, 0.0, 0.0),
                            'Pos': Point3(419.505, 164.464, 44.55),
                            'Scale': VBase3(0.776, 0.776, 0.776),
                            'Visual': {
                                'Model': 'models/vegetation/bush_c'
                            }
                        },
                        '1138403067.3dxschafe': {
                            'Type':
                            'Barrel',
                            'Color': (0.800000011920929, 0.800000011920929,
                                      0.800000011920929, 1.0),
                            'Hpr':
                            VBase3(0.0, -0.346, 0.0),
                            'Pos':
                            Point3(421.658, 124.647, 43.269),
                            'Scale':
                            VBase3(0.532, 0.532, 0.532),
                            'Visual': {
                                'Color': (0.67, 0.58, 0.31, 1.0),
                                'Model': 'models/props/barrel_grey'
                            }
                        },
                        '1138403165.69dxschafe': {
                            'Type': 'Bush',
                            'Color': (0.5, 0.5, 0.5, 1.0),
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(418.51, 136.938, 44.56),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/vegetation/bush_h'
                            }
                        },
                        '1138410072.17dxschafe': {
                            'Type':
                            'Rope',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            Point3(0.0, 0.0, 0.0),
                            'Pos':
                            Point3(462.694, 237.192, 49.721),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/rope_pile'
                            }
                        },
                        '1138410112.63dxschafe': {
                            'Type': 'Barrel',
                            'Hpr': VBase3(-6.216, 0.0, 0.0),
                            'Pos': Point3(438.061, 278.471, 50.169),
                            'Scale': VBase3(0.541, 0.541, 0.541),
                            'Visual': {
                                'Model': 'models/props/barrel_group_1'
                            }
                        },
                        '1138410625.44dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.800000011920929, 0.800000011920929,
                                      0.800000011920929, 1.0),
                            'Hpr':
                            VBase3(83.471, 0.0, 0.0),
                            'Pos':
                            Point3(408.928, 222.834, 46.227),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138410659.77dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.800000011920929, 0.800000011920929,
                                      0.800000011920929, 1.0),
                            'Hpr':
                            VBase3(83.471, 0.0, 0.0),
                            'Pos':
                            Point3(407.847, 213.013, 46.256),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138410666.5dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.800000011920929, 0.800000011920929,
                                      0.800000011920929, 1.0),
                            'Hpr':
                            VBase3(84.877, 0.0, 0.0),
                            'Pos':
                            Point3(406.774, 203.134, 46.253),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138410875.87dxschafe': {
                            'Type': 'Cart',
                            'Hpr': VBase3(-126.971, 0.159, 0.0),
                            'Pos': Point3(413.557, 198.195, 46.111),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/cart_reg'
                            }
                        },
                        '1138418428.85dxschafe': {
                            'Type': 'Crate',
                            'Hpr': VBase3(21.301, -5.437, 3.074),
                            'Pos': Point3(564.565, 210.019, 51.526),
                            'Scale': VBase3(0.5, 0.5, 0.5),
                            'Visual': {
                                'Model': 'models/props/crate'
                            }
                        },
                        '1138418666.85dxschafe': {
                            'Type': 'Bucket',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(402.366, 135.157, 44.575),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/bucket'
                            }
                        },
                        '1138418677.87dxschafe': {
                            'Type':
                            'Bush',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            Point3(0.0, 0.0, 0.0),
                            'Pos':
                            Point3(402.366, 135.157, 45.892),
                            'Scale':
                            VBase3(0.507, 0.507, 0.507),
                            'Visual': {
                                'Model': 'models/vegetation/bush_h'
                            }
                        },
                        '1138420222.41dxschafe': {
                            'Type': 'Building Exterior',
                            'File': '',
                            'Hpr': VBase3(2.096, 0.0, 0.0),
                            'Pos': Point3(471.497, 83.062, 39.754),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/spanish_archA'
                            }
                        },
                        '1138420265.62dxschafe': {
                            'Type': 'Building Exterior',
                            'File': '',
                            'Hpr': VBase3(84.245, 0.0, 0.0),
                            'Pos': Point3(380.148, 121.958, 41.664),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/spanish_archA'
                            }
                        },
                        '1138420321.09dxschafe': {
                            'Type':
                            'Building Exterior',
                            'File':
                            '',
                            'Color': (0.800000011920929, 0.800000011920929,
                                      0.800000011920929, 1.0),
                            'Hpr':
                            VBase3(0.901, 0.0, 0.0),
                            'Pos':
                            Point3(557.895, 238.356, 47.471),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Name':
                                '',
                                'Color': (0.88, 0.8899999999999999,
                                          0.8299999999999998, 1.0),
                                'Door':
                                'models/buildings/shanty_guildhall_door',
                                'Model':
                                'models/buildings/burned_gate'
                            }
                        },
                        '1138647059.31dxschafe': {
                            'Type':
                            'Rope',
                            'Color': (0.6000000238418579, 0.6000000238418579,
                                      0.6000000238418579, 1.0),
                            'Hpr':
                            Point3(0.0, 0.0, 0.0),
                            'Pos':
                            Point3(564.321, 202.968, 51.469),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/rope_pile'
                            }
                        },
                        '1138647125.22dxschafe': {
                            'Type': 'Crate',
                            'Color': (0.75, 0.9300000071525574, 1.0, 1.0),
                            'Hpr': VBase3(13.836, 0.0, 0.0),
                            'Pos': Point3(562.005, 196.806, 48.044),
                            'Scale': VBase3(0.497, 0.497, 0.497),
                            'Visual': {
                                'Color': (0.67, 0.73, 0.66, 1.0),
                                'Model': 'models/props/crate'
                            }
                        },
                        '1138648723.89dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-103.37, 0.0, 0.0),
                            'Pos': Point3(651.125, 124.002, 44.948),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138648754.45dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-96.245, 0.0, 0.0),
                            'Pos': Point3(653.351, 133.565, 44.948),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138648762.68dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-96.245, 0.0, 0.0),
                            'Pos': Point3(654.415, 143.424, 44.948),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138648765.79dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-96.245, 0.0, 0.0),
                            'Pos': Point3(655.598, 153.28, 44.948),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138648770.65dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-67.948, 0.0, 0.0),
                            'Pos': Point3(656.776, 162.74, 44.948),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138648980.13dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-98.272, 0.0, 0.0),
                            'Pos': Point3(645.568, 76.95, 42.677),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138648987.98dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-98.272, 0.0, 0.0),
                            'Pos': Point3(647.035, 86.687, 42.677),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138648995.2dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-98.272, 0.0, 0.0),
                            'Pos': Point3(648.447, 96.43, 42.677),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138649012.41dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(178.956, 0.0, 0.0),
                            'Pos': Point3(652.627, 125.544, 42.677),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_Column'
                            }
                        },
                        '1138649057.34dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-97.884, 0.0, 0.0),
                            'Pos': Point3(649.878, 106.208, 42.678),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138649219.47dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-98.462, 0.0, 0.0),
                            'Pos': Point3(651.131, 115.913, 42.677),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138649279.9dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-98.462, 0.0, 0.0),
                            'Pos': Point3(652.79, 125.607, 44.755),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_Column'
                            }
                        },
                        '1138649427.11dxschafe': {
                            'Type': 'Wall',
                            'Color': (1.0, 1.0, 1.0, 1.0),
                            'Hpr': VBase3(-89.266, -0.279, 1.529),
                            'Pos': Point3(614.742, 64.888, 42.677),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_Column'
                            }
                        },
                        '1138649483.26dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-96.402, -0.467, 1.482),
                            'Pos': Point3(644.5, 67.546, 42.427),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138649500.4dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-96.951, -0.481, 1.478),
                            'Pos': Point3(644.145, 66.475, 42.562),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_Column'
                            }
                        },
                        '1138649530.65dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(3.471, 1.54, 0.205),
                            'Pos': Point3(644.333, 66.523, 42.549),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138649548.09dxschafe': {
                            'Type': 'Wall',
                            'Color': (1.0, 1.0, 1.0, 1.0),
                            'Hpr': VBase3(1.766, 1.534, 0.251),
                            'Pos': Point3(625.624, 65.432, 42.659),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138649567.19dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(3.127, 1.539, 0.215),
                            'Pos': Point3(634.877, 65.96, 42.607),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138649836.96dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(-1.499, 0.0, 0.0),
                            'Pos': Point3(651.46, 184.535, 47.708),
                            'Scale': VBase3(0.902, 0.902, 0.902),
                            'Visual': {
                                'Model': 'models/vegetation/bush_d'
                            }
                        },
                        '1138650056.86dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(75.775, 0.0, 0.0),
                            'Pos': Point3(653.734, 165.339, 44.993),
                            'Scale': VBase3(0.839, 0.839, 0.839),
                            'Visual': {
                                'Model': 'models/vegetation/bush_b'
                            }
                        },
                        '1138650910.16dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(-63.739, 0.0, 0.0),
                            'Pos': Point3(545.986, 229.67, 48.487),
                            'Scale': VBase3(0.85, 0.85, 0.85),
                            'Visual': {
                                'Model': 'models/vegetation/bush_f'
                            }
                        },
                        '1138653812.79dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(88.09, -0.094, 0.0),
                            'Pos':
                            Point3(550.238, 235.635, 44.656),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138653878.91dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(88.09, -0.094, 0.0),
                            'Pos':
                            Point3(550.174, 226.207, 44.747),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStone_Column'
                            }
                        },
                        '1138654406.52dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-17.187, 0.0, 0.0),
                            'Pos':
                            Point3(492.155, 77.126, 40.222),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138654445.13dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-11.759, 0.0, 0.0),
                            'Pos':
                            Point3(530.677, 64.709, 40.239),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138654459.26dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-17.187, 0.0, 0.0),
                            'Pos':
                            Point3(521.277, 66.277, 40.21),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138654466.22dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-17.187, 0.0, 0.0),
                            'Pos':
                            Point3(512.03, 69.102, 40.112),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138654495.33dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-27.849, 0.0, 0.0),
                            'Pos':
                            Point3(500.581, 72.615, 40.231),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Color': (0.88, 0.89, 0.8299999999999998, 1.0),
                                'Model':
                                'models/buildings/TallWallStucco_broken10'
                            }
                        },
                        '1138654694.39dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-17.59, 0.0, 0.0),
                            'Pos':
                            Point3(502.706, 71.98, 40.278),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/TallWallStucco_Column'
                            }
                        },
                        '1138654960.52dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-17.59, 0.0, 0.0),
                            'Pos':
                            Point3(430.125, 83.564, 40.264),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/TallWallStucco_Column'
                            }
                        },
                        '1138655007.18dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-4.741, 0.0, 0.0),
                            'Pos':
                            Point3(449.985, 81.502, 40.219),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138655029.02dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-4.741, 0.0, 0.0),
                            'Pos':
                            Point3(440.032, 82.323, 40.268),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138655047.68dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-19.474, 0.0, 0.0),
                            'Pos':
                            Point3(428.428, 83.863, 40.292),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138655111.7dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-19.474, 0.0, 0.0),
                            'Pos':
                            Point3(409.708, 90.528, 40.309),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138655124.07dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-19.474, 0.0, 0.0),
                            'Pos':
                            Point3(400.313, 93.852, 40.306),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/TallWallStucco_broken10'
                            }
                        },
                        '1138655133.26dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-19.474, 0.0, 0.0),
                            'Pos':
                            Point3(390.909, 97.178, 40.248),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138655281.94dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-96.729, 0.0, 0.0),
                            'Pos': Point3(380.576, 102.572, 41.444),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Color':
                                (0.7699999999999999, 0.7599999999999998,
                                 0.6799999999999997, 1.0),
                                'Model':
                                'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138655487.29dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-100.037, 0.0, 0.0),
                            'Pos':
                            Point3(377.116, 133.622, 42.679),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/TallWallStucco_broken10'
                            }
                        },
                        '1138655678.03dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-100.037, 0.0, 0.0),
                            'Pos':
                            Point3(378.858, 143.513, 43.055),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/TallWallStucco_Column'
                            }
                        },
                        '1138656107.95dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.7699999809265137, 0.7599999904632568,
                                      0.6800000071525574, 1.0),
                            'Hpr':
                            VBase3(-23.529, 0.0, 0.0),
                            'Pos':
                            Point3(381.741, 100.559, 41.332),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/TallWallStucco_Column'
                            }
                        },
                        '1138657845.1dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(-109.364, -0.735, 0.0),
                            'Pos': Point3(432.904, 87.983, 39.832),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/vegetation/bush_d'
                            }
                        },
                        '1138658065.75dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(55.111, 0.708, 0.197),
                            'Pos': Point3(384.79, 103.927, 41.168),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/vegetation/bush_b'
                            }
                        },
                        '1138658204.28dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(-110.454, 0.0, 0.0),
                            'Pos': Point3(414.769, 189.853, 43.951),
                            'Scale': VBase3(0.629, 0.629, 0.629),
                            'Visual': {
                                'Model': 'models/vegetation/bush_d'
                            }
                        },
                        '1138660499.28dxschafe': {
                            'Type': 'Bush',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(528.948, 150.976, 46.911),
                            'Scale': VBase3(0.31, 0.31, 0.31),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1138660565.68dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(-122.345, 0.0, 0.0),
                            'Pos': Point3(486.529, 84.942, 40.511),
                            'Scale': VBase3(0.489, 0.489, 0.489),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1138660671.69dxschafe': {
                            'Type': 'Cart',
                            'Hpr': VBase3(-25.018, 0.0, 0.0),
                            'Pos': Point3(517.4, 72.714, 40.194),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/cart_reg'
                            }
                        },
                        '1138660730.71dxschafe': {
                            'Type': 'Barrel',
                            'Hpr': VBase3(-70.599, 0.0, 0.0),
                            'Pos': Point3(553.003, 68.864, 41.171),
                            'Scale': VBase3(0.633, 0.633, 0.633),
                            'Visual': {
                                'Model': 'models/props/barrel_group_2'
                            }
                        },
                        '1138660848.26dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-76.483, 0.0, 0.0),
                            'Pos': Point3(648.678, 218.785, 51.358),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/TallWallStucco_Column'
                            }
                        },
                        '1138660900.34dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-80.167, 0.0, 0.0),
                            'Pos': Point3(648.498, 219.07, 51.36),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138660918.74dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-80.167, 0.0, 0.0),
                            'Pos': Point3(646.816, 228.883, 51.36),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138660934.73dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-41.422, 0.0, 0.0),
                            'Pos': Point3(643.33, 247.493, 51.36),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138660934.79dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-80.167, 0.0, 0.0),
                            'Pos': Point3(645.103, 238.639, 51.36),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138661075.26dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-41.504, 0.0, 0.0),
                            'Pos': Point3(635.984, 253.958, 51.332),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138661095.45dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-41.504, 0.0, 0.0),
                            'Pos': Point3(628.55, 260.512, 51.308),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138661112.78dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-46.798, 0.0, 0.0),
                            'Pos': Point3(621.193, 266.956, 51.357),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138661174.33dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-41.504, 0.0, 0.0),
                            'Pos': Point3(644.149, 247.141, 51.36),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/TallWallStucco_Column'
                            }
                        },
                        '1138661379.77dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(141.657, 0.0, 0.0),
                            'Pos': Point3(615.13, 276.201, 51.359),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/TallWallStucco_Column'
                            }
                        },
                        '1138661665.88dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-42.647, 0.0, 0.0),
                            'Pos': Point3(614.281, 275.818, 54.007),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138661712.71dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-42.647, 0.0, 0.0),
                            'Pos': Point3(606.934, 282.537, 54.022),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138661916.96dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-42.647, 0.0, 0.0),
                            'Pos': Point3(599.6, 289.289, 54.005),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138661917.93dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-42.647, 0.0, 0.0),
                            'Pos': Point3(592.303, 295.988, 54.006),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138661933.68dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-42.647, 0.0, 0.0),
                            'Pos': Point3(584.992, 302.704, 54.004),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138661945.7dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-42.647, 0.0, 0.0),
                            'Pos': Point3(577.616, 309.488, 54.004),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138661954.82dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-14.004, 0.0, 0.0),
                            'Pos': Point3(569.777, 316.399, 53.985),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138661969.71dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-14.004, 0.0, 0.0),
                            'Pos': Point3(560.127, 318.827, 54.005),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138661976.46dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-14.004, 0.0, 0.0),
                            'Pos': Point3(550.462, 321.215, 54.003),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138661989.79dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(0.687, 0.0, 0.0),
                            'Pos': Point3(541.034, 323.562, 54.007),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138662146.61dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-10.777, 0.0, 0.0),
                            'Pos': Point3(488.717, 335.967, 54.006),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138662162.49dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-92.587, 0.0, 0.0),
                            'Pos': Point3(487.441, 326.664, 54.02),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138662175.92dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-9.621, 0.0, 0.0),
                            'Pos': Point3(478.944, 337.843, 53.997),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138662302.49dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-4.925, 0.0, 0.0),
                            'Pos': Point3(470.031, 340.347, 53.997),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138662442.07dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-4.925, 0.0, 0.0),
                            'Pos': Point3(460.094, 341.195, 53.998),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138662448.51dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-4.925, 0.0, 0.0),
                            'Pos': Point3(450.274, 342.05, 53.99),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138662477.73dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-99.802, 0.0, 0.0),
                            'Pos': Point3(440.315, 343.261, 53.987),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138662487.83dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-17.084, 0.0, 0.0),
                            'Pos': Point3(442.706, 351.993, 53.985),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138662582.92dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(78.488, 0.0, 0.0),
                            'Pos': Point3(426.372, 346.672, 53.984),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138662609.56dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(88.887, 0.0, 0.0),
                            'Pos': Point3(424.425, 337.396, 53.973),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138662966.03dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(88.887, 0.0, 0.0),
                            'Pos': Point3(530.845, 324.36, 54.005),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/LowWallStucco_column'
                            }
                        },
                        '1138663053.09dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(143.509, 0.0, 0.0),
                            'Pos': Point3(570.092, 317.538, 54.004),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/LowWallStucco_column'
                            }
                        },
                        '1138663093.3dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(178.64, 0.0, 0.0),
                            'Pos': Point3(487.884, 337.199, 54.012),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/LowWallStucco_column'
                            }
                        },
                        '1138663154.02dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(170.714, 0.0, 0.0),
                            'Pos': Point3(469.716, 341.366, 53.998),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/LowWallStucco_column'
                            }
                        },
                        '1138663183.22dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(174.1, 0.0, 0.0),
                            'Pos': Point3(440.277, 343.773, 53.984),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/LowWallStucco_column'
                            }
                        },
                        '1138663205.14dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(168.953, 0.0, 0.0),
                            'Pos': Point3(441.946, 353.093, 53.999),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/LowWallStucco_column'
                            }
                        },
                        '1138663279.71dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(168.953, 0.0, 0.0),
                            'Pos': Point3(427.148, 358.516, 53.994),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/TallWallStucco_Column'
                            }
                        },
                        '1138663287.74dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(76.344, 0.0, 0.0),
                            'Pos': Point3(428.753, 356.341, 53.996),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138663371.07dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(162.644, 0.0, 0.0),
                            'Pos': Point3(426.347, 358.079, 53.98),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138666284.38dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(-158.001, 0.0, 0.0),
                            'Pos': Point3(438.694, 221.735, 45.897),
                            'Scale': VBase3(0.503, 0.503, 0.503),
                            'Visual': {
                                'Model': 'models/vegetation/bush_c'
                            }
                        },
                        '1138666879.15dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(174.177, 0.0, 0.0),
                            'Pos': Point3(413.13, 283.964, 53.907),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138666979.31dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-105.763, 0.0, 0.0),
                            'Pos': Point3(413.04, 283.677, 53.906),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138667062.52dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-105.763, 0.0, 0.0),
                            'Pos': Point3(415.836, 293.258, 53.919),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138667090.27dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-105.763, 0.0, 0.0),
                            'Pos': Point3(418.611, 302.78, 53.931),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/LowWallStucco_10'
                            }
                        },
                        '1138667147.04dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(62.099, 0.0, 0.0),
                            'Pos': Point3(421.0, 253.847, 48.353),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138667270.49dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(57.268, 0.0, 0.0),
                            'Pos': Point3(416.354, 245.152, 48.361),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/TallWallStucco_10'
                            }
                        },
                        '1138667406.75dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(84.059, 0.0, 0.0),
                            'Pos':
                            Point3(425.531, 246.584, 47.667),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Color': (0.63, 0.53, 0.35, 1.0),
                                'Model': 'models/buildings/LowWallStone_10'
                            }
                        },
                        '1138667460.66dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(85.068, -0.352, 4.072),
                            'Pos': Point3(421.01, 240.989, 49.509),
                            'Scale': VBase3(0.499, 0.499, 0.499),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1138725193.96dxschafe': {
                            'Type': 'FountainSmall',
                            'Hpr': VBase3(0.051, 1.794, -1.632),
                            'Pos': Point3(556.539, 134.683, 43.097),
                            'Scale': VBase3(1.003, 1.003, 1.003),
                            'Visual': {
                                'Model': 'models/props/FountainSmall'
                            }
                        },
                        '1138725240.0dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(19.379, 0.0, 0.0),
                            'Pos': Point3(569.465, 151.042, 43.616),
                            'Scale': VBase3(0.425, 0.425, 0.425),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1138727343.41dxschafe': {
                            'Type': 'Tree - Animated',
                            'Animate': 'models/vegetation/palm_trunk_a_idle',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(487.619, 82.513, 39.809),
                            'Scale': VBase3(0.64, 0.64, 0.64),
                            'SubObjs': {
                                'Top Model': {
                                    'Visual': {
                                        'Animate':
                                        'models/vegetation/palm_leaf_a_idle',
                                        'Attach':
                                        ['trunk', 'def_trunk_attach'],
                                        'Model':
                                        'models/vegetation/palm_leaf_a_hi',
                                        'PartName': 'leaf'
                                    }
                                }
                            },
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_trunk_a_idle',
                                'Model': 'models/vegetation/palm_trunk_a_hi',
                                'PartName': 'trunk'
                            }
                        },
                        '1138728593.36dxschafe': {
                            'Type':
                            'Barrel',
                            'Color': (0.800000011920929, 1.0,
                                      0.6000000238418579, 1.0),
                            'Hpr':
                            VBase3(115.504, -0.605, -63.052),
                            'Pos':
                            Point3(625.564, 171.452, 44.87),
                            'Scale':
                            VBase3(0.776, 0.776, 0.776),
                            'Visual': {
                                'Model': 'models/props/barrel_sideways'
                            }
                        },
                        '1138728779.92dxschafe': {
                            'Type':
                            'Barrel',
                            'Color': (0.8999999761581421, 0.8999999761581421,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            Point3(0.0, 0.0, 0.0),
                            'Pos':
                            Point3(645.158, 89.7, 42.702),
                            'Scale':
                            VBase3(0.448, 0.448, 0.448),
                            'Visual': {
                                'Model': 'models/props/barrel_worn'
                            }
                        },
                        '1138729936.15dxschafe': {
                            'Type': 'Trellis',
                            'Hpr': VBase3(-12.679, 0.0, 0.0),
                            'Pos': Point3(550.811, 315.8, 54.031),
                            'Scale': VBase3(0.487, 0.487, 0.487),
                            'Visual': {
                                'Model': 'models/props/trellisB'
                            }
                        },
                        '1138730047.82dxschafe': {
                            'Type': 'Trellis',
                            'Hpr': VBase3(-2.286, 0.0, 0.0),
                            'Pos': Point3(534.903, 317.577, 53.926),
                            'Scale': VBase3(0.486, 0.486, 0.486),
                            'Visual': {
                                'Model': 'models/props/trellisB'
                            }
                        },
                        '1138730274.97dxschafe': {
                            'Type': 'FountainSmall',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(543.286, 319.368, 54.011),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/FountainSmall'
                            }
                        },
                        '1138730803.13dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(106.843, 0.0, 0.0),
                            'Pos': Point3(609.912, 253.935, 51.356),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/vegetation/bush_c'
                            }
                        },
                        '1138731189.79dxschafe': {
                            'Type': 'Wall',
                            'Hpr': VBase3(-83.134, 0.0, 0.0),
                            'Pos': Point3(652.705, 189.056, 48.014),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/TallWallStucco_Column'
                            }
                        },
                        '1138740545.15dxschafe': {
                            'Type': 'Wall',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(369.777, 105.06, 40.867),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/woodfence_B'
                            }
                        },
                        '1138742465.08dxschafe': {
                            'Type':
                            'TreeBase',
                            'Color': (0.800000011920929, 0.800000011920929,
                                      0.800000011920929, 1.0),
                            'Hpr':
                            VBase3(5.418, 0.0, 0.0),
                            'Pos':
                            Point3(591.902, 269.206, 51.357),
                            'Scale':
                            VBase3(0.638, 0.638, 0.638),
                            'Visual': {
                                'Model': 'models/props/TreeBase'
                            }
                        },
                        '1138742593.3dxschafe': {
                            'Type': 'Tree - Animated',
                            'Hpr': VBase3(72.508, 3.647, 1.148),
                            'Pos': Point3(591.87, 269.721, 52.606),
                            'Scale': VBase3(0.312, 0.312, 0.312),
                            'SubObjs': {
                                'Top Model': {
                                    'Visual': {
                                        'Animate':
                                        'models/vegetation/fern_leaf_a_idle',
                                        'Attach':
                                        ['trunk', 'def_trunk_attach'],
                                        'Model':
                                        'models/vegetation/fern_leaf_b_hi',
                                        'PartName': 'leaf'
                                    }
                                }
                            },
                            'Visual': {
                                'Animate':
                                'models/vegetation/fern_trunk_a_idle',
                                'Model': 'models/vegetation/fern_trunk_a_hi',
                                'PartName': 'trunk'
                            }
                        },
                        '1138742820.76dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(-102.655, 0.0, 0.0),
                            'Pos': Point3(639.296, 217.768, 48.521),
                            'Scale': VBase3(0.6, 0.6, 0.6),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1138743352.03dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(0.0, 0.0, 6.367),
                            'Pos': Point3(554.867, 134.472, 41.778),
                            'Scale': VBase3(0.384, 0.384, 0.384),
                            'Visual': {
                                'Model': 'models/vegetation/bush_f'
                            }
                        },
                        '1145031108.13dxschafe': {
                            'Type': 'Shanty Tents',
                            'Hpr': VBase3(-107.694, 0.0, 0.0),
                            'Pos': Point3(636.777, 104.301, 42.677),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/6shanty_tents'
                            }
                        },
                        '1145599967.98jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-1.894, 0.0, 0.0),
                            'Pos': Point3(471.624, 226.135, 49.014),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 4,
                                'Belt': 1,
                                'BeltColor': 6,
                                'Coat': 0,
                                'CoatColor': 14,
                                'Gender': 'm',
                                'Hair': 5,
                                'HairColor': 1,
                                'Hat': 1,
                                'Mustache': 1,
                                'Pants': 2,
                                'PantsColor': 1,
                                'Shape': 3,
                                'Shirt': 8,
                                'ShirtColor': 3,
                                'Shoe': 1,
                                'Skin': 2,
                                'Sock': 0
                            }
                        },
                        '1145599970.4jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-66.15, 0.0, 0.0),
                            'Pos': Point3(476.966, 210.588, 47.658),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 1,
                                'Belt': 1,
                                'BeltColor': 5,
                                'Coat': 0,
                                'CoatColor': 11,
                                'Gender': 'm',
                                'Hair': 1,
                                'HairColor': 2,
                                'Hat': 1,
                                'Mustache': 1,
                                'Pants': 2,
                                'PantsColor': 1,
                                'Shape': 1,
                                'Shirt': 5,
                                'ShirtColor': 3,
                                'Shoe': 1,
                                'Skin': 2,
                                'Sock': 0
                            }
                        },
                        '1145599974.12jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(56.141, 0.0, 0.0),
                            'Pos': Point3(454.602, 199.759, 46.173),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 6,
                                'Belt': 1,
                                'BeltColor': 4,
                                'Coat': 2,
                                'CoatColor': 13,
                                'Gender': 'f',
                                'Hair': 1,
                                'HairColor': 5,
                                'Hat': 1,
                                'Mustache': 1,
                                'Pants': 2,
                                'PantsColor': 3,
                                'Shape': 1,
                                'Shirt': 5,
                                'ShirtColor': 1,
                                'Shoe': 1,
                                'Skin': 2,
                                'Sock': 0
                            }
                        },
                        '1145599977.58jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-85.286, 0.0, 0.0),
                            'Pos': Point3(464.445, 199.854, 45.651),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 8,
                                'Belt': 1,
                                'BeltColor': 3,
                                'Coat': 1,
                                'CoatColor': 11,
                                'Gender': 'm',
                                'Hair': 5,
                                'HairColor': 7,
                                'Hat': 3,
                                'Mustache': 1,
                                'Pants': 2,
                                'PantsColor': 2,
                                'Shape': 3,
                                'Shirt': 5,
                                'ShirtColor': 3,
                                'Shoe': 1,
                                'Skin': 3,
                                'Sock': 0
                            }
                        },
                        '1145599985.09jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'run',
                            'Hpr': VBase3(-92.224, 0.0, 0.0),
                            'Pos': Point3(447.811, 293.355, 54.076),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 3,
                                'Belt': 1,
                                'BeltColor': 6,
                                'Coat': 2,
                                'CoatColor': 6,
                                'Gender': 'm',
                                'Hair': 1,
                                'HairColor': 1,
                                'Hat': 1,
                                'Mustache': 1,
                                'Pants': 2,
                                'PantsColor': 3,
                                'Shape': 1,
                                'Shirt': 5,
                                'ShirtColor': 3,
                                'Shoe': 1,
                                'Skin': 1,
                                'Sock': 1
                            }
                        },
                        '1145599999.11jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(8.432, 0.0, 0.0),
                            'Pos': Point3(464.563, 220.266, 48.433),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145600004.56jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(67.805, 0.0, 0.0),
                            'Pos': Point3(482.151, 213.794, 47.965),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145600011.59jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'run',
                            'Hpr': VBase3(146.585, 0.0, 0.0),
                            'Pos': Point3(483.336, 293.656, 53.662),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145600014.73jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(77.347, 0.0, 0.0),
                            'Pos': Point3(463.034, 178.944, 45.201),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145644673.0jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-88.938, 0.0, 0.0),
                            'Pos': Point3(475.074, 170.593, 45.292),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 3,
                                'Belt': 1,
                                'BeltColor': 7,
                                'Coat': 2,
                                'CoatColor': 9,
                                'Gender': 'm',
                                'Hair': 7,
                                'HairColor': 4,
                                'Hat': 2,
                                'Mustache': 1,
                                'Pants': 3,
                                'PantsColor': 3,
                                'Shape': 2,
                                'Shirt': 6,
                                'ShirtColor': 2,
                                'Shoe': 1,
                                'Skin': 2,
                                'Sock': 1
                            }
                        },
                        '1145644694.48jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-109.823, 0.0, 0.0),
                            'Pos': Point3(456.284, 180.592, 45.359),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 1,
                                'Belt': 1,
                                'BeltColor': 3,
                                'Coat': 2,
                                'CoatColor': 9,
                                'Gender': 'm',
                                'Hair': 4,
                                'HairColor': 5,
                                'Hat': 1,
                                'Mustache': 1,
                                'Pants': 2,
                                'PantsColor': 1,
                                'Shape': 1,
                                'Shirt': 6,
                                'ShirtColor': 3,
                                'Shoe': 1,
                                'Skin': 2,
                                'Sock': 1
                            }
                        },
                        '1145644708.43jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-49.936, 0.0, 0.0),
                            'Pos': Point3(453.698, 159.863, 44.72),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 1,
                                'Belt': 1,
                                'BeltColor': 5,
                                'Coat': 1,
                                'CoatColor': 14,
                                'Gender': 'm',
                                'Hair': 5,
                                'HairColor': 1,
                                'Hat': 3,
                                'Mustache': 1,
                                'Pants': 2,
                                'PantsColor': 2,
                                'Shape': 1,
                                'Shirt': 5,
                                'ShirtColor': 1,
                                'Shoe': 1,
                                'Skin': 2,
                                'Sock': 0
                            }
                        },
                        '1145644714.42jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(10.042, 0.0, 0.0),
                            'Pos': Point3(461.097, 157.488, 44.719),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 3,
                                'Belt': 1,
                                'BeltColor': 3,
                                'Coat': 0,
                                'CoatColor': 13,
                                'Gender': 'm',
                                'Hair': 4,
                                'HairColor': 7,
                                'Hat': 1,
                                'Mustache': 1,
                                'Pants': 2,
                                'PantsColor': 3,
                                'Shape': 3,
                                'Shirt': 2,
                                'ShirtColor': 2,
                                'Shoe': 1,
                                'Skin': 2,
                                'Sock': 0
                            }
                        },
                        '1145644715.95jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-45.436, 0.0, 0.0),
                            'Pos': Point3(459.153, 130.118, 43.043),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 5,
                                'Belt': 1,
                                'BeltColor': 3,
                                'Coat': 1,
                                'CoatColor': 8,
                                'Gender': 'f',
                                'Hair': 3,
                                'HairColor': 8,
                                'Hat': 3,
                                'Mustache': 1,
                                'Pants': 2,
                                'PantsColor': 2,
                                'Shape': 1,
                                'Shirt': 5,
                                'ShirtColor': 3,
                                'Shoe': 1,
                                'Skin': 3,
                                'Sock': 1
                            }
                        },
                        '1145644718.25jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-87.857, 0.0, 0.0),
                            'Pos': Point3(455.869, 134.806, 43.318),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 5,
                                'Belt': 1,
                                'BeltColor': 7,
                                'Coat': 2,
                                'CoatColor': 13,
                                'Gender': 'm',
                                'Hair': 3,
                                'HairColor': 7,
                                'Hat': 2,
                                'Mustache': 1,
                                'Pants': 2,
                                'PantsColor': 1,
                                'Shape': 3,
                                'Shirt': 5,
                                'ShirtColor': 2,
                                'Shoe': 1,
                                'Skin': 1,
                                'Sock': 1
                            }
                        },
                        '1145644720.37jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-47.657, 0.0, 0.0),
                            'Pos': Point3(476.045, 165.501, 45.292),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 2,
                                'Belt': 1,
                                'BeltColor': 7,
                                'Coat': 2,
                                'CoatColor': 13,
                                'Gender': 'm',
                                'Hair': 6,
                                'HairColor': 5,
                                'Hat': 1,
                                'Mustache': 1,
                                'Pants': 2,
                                'PantsColor': 3,
                                'Shape': 1,
                                'Shirt': 5,
                                'ShirtColor': 1,
                                'Shoe': 1,
                                'Skin': 3,
                                'Sock': 0
                            }
                        },
                        '1145644732.2jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-63.094, 0.0, 0.0),
                            'Pos': Point3(444.641, 120.342, 42.728),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 4,
                                'Belt': 1,
                                'BeltColor': 6,
                                'Coat': 2,
                                'CoatColor': 8,
                                'Gender': 'm',
                                'Hair': 6,
                                'HairColor': 1,
                                'Hat': 3,
                                'Mustache': 1,
                                'Pants': 3,
                                'PantsColor': 3,
                                'Shape': 1,
                                'Shirt': 6,
                                'ShirtColor': 4,
                                'Shoe': 1,
                                'Skin': 3,
                                'Sock': 1
                            }
                        },
                        '1145644734.42jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-63.094, 0.0, 0.0),
                            'Pos': Point3(473.967, 87.064, 40.234),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 5,
                                'Belt': 1,
                                'BeltColor': 4,
                                'Coat': 0,
                                'CoatColor': 11,
                                'Gender': 'm',
                                'Hair': 2,
                                'HairColor': 6,
                                'Hat': 3,
                                'Mustache': 1,
                                'Pants': 1,
                                'PantsColor': 2,
                                'Shape': 1,
                                'Shirt': 6,
                                'ShirtColor': 4,
                                'Shoe': 1,
                                'Skin': 2,
                                'Sock': 0
                            }
                        },
                        '1145652337.21jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'idle',
                            'Hpr': VBase3(13.364, 0.0, 0.0),
                            'Pos': Point3(474.94, 112.463, 45.292),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145652361.7jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(29.893, 0.0, 0.0),
                            'Pos': Point3(477.962, 96.316, 40.943),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145652403.71jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-125.22, 0.0, 0.0),
                            'Pos': Point3(474.005, 101.194, 41.208),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 8,
                                'Belt': 1,
                                'BeltColor': 5,
                                'Coat': 0,
                                'CoatColor': 11,
                                'Gender': 'm',
                                'Hair': 4,
                                'HairColor': 3,
                                'Hat': 3,
                                'Mustache': 1,
                                'Pants': 1,
                                'PantsColor': 2,
                                'Shape': 3,
                                'Shirt': 5,
                                'ShirtColor': 4,
                                'Shoe': 1,
                                'Skin': 2,
                                'Sock': 0
                            }
                        },
                        '1145919878.84jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'run',
                            'Hpr': VBase3(127.11, 0.0, 0.0),
                            'Pos': Point3(492.762, 168.143, 46.178),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 3,
                                'Belt': 1,
                                'BeltColor': 6,
                                'Coat': 2,
                                'CoatColor': 6,
                                'Gender': 'f',
                                'Hair': 1,
                                'HairColor': 8,
                                'Hat': 1,
                                'Mustache': 1,
                                'Pants': 1,
                                'PantsColor': 3,
                                'Shape': 2,
                                'Shirt': 4,
                                'ShirtColor': 2,
                                'Shoe': 1,
                                'Skin': 3,
                                'Sock': 1
                            }
                        },
                        '1145920929.06jubutler': {
                            'Type': 'Movement Node',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(405.365, 103.058, 42.379),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145920993.09jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'run',
                            'Hpr': VBase3(175.79, 0.0, 0.0),
                            'Pos': Point3(439.834, 186.3, 44.676),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 6,
                                'Belt': 1,
                                'BeltColor': 6,
                                'Coat': 2,
                                'CoatColor': 10,
                                'Gender': 'm',
                                'Hair': 3,
                                'HairColor': 7,
                                'Hat': 3,
                                'Mustache': 1,
                                'Pants': 2,
                                'PantsColor': 3,
                                'Shape': 1,
                                'Shirt': 4,
                                'ShirtColor': 4,
                                'Shoe': 1,
                                'Skin': 3,
                                'Sock': 0
                            }
                        },
                        '1145921024.01jubutler': {
                            'Type': 'Movement Node',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(433.462, 94.181, 42.36),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145921057.15jubutler': {
                            'Type': 'Movement Node',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(423.491, 97.91, 40.845),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145921068.83jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'run',
                            'Hpr': VBase3(85.638, 0.0, 0.0),
                            'Pos': Point3(518.505, 90.624, 40.956),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 6,
                                'Belt': 1,
                                'BeltColor': 7,
                                'Coat': 1,
                                'CoatColor': 9,
                                'Gender': 'm',
                                'Hair': 2,
                                'HairColor': 4,
                                'Hat': 1,
                                'Mustache': 1,
                                'Pants': 3,
                                'PantsColor': 3,
                                'Shape': 2,
                                'Shirt': 5,
                                'ShirtColor': 3,
                                'Shoe': 1,
                                'Skin': 2,
                                'Sock': 1
                            }
                        },
                        '1145921147.15jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'run',
                            'Hpr': VBase3(-92.552, 0.0, 0.0),
                            'Pos': Point3(436.17, 265.82, 50.161),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 3,
                                'Belt': 1,
                                'BeltColor': 4,
                                'Coat': 1,
                                'CoatColor': 7,
                                'Gender': 'm',
                                'Hair': 6,
                                'HairColor': 6,
                                'Hat': 1,
                                'Mustache': 1,
                                'Pants': 2,
                                'PantsColor': 1,
                                'Shape': 2,
                                'Shirt': 5,
                                'ShirtColor': 1,
                                'Shoe': 1,
                                'Skin': 2,
                                'Sock': 1
                            }
                        },
                        '1145921180.15jubutler': {
                            'Type': 'Movement Node',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(518.238, 262.796, 49.383),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145921407.98jubutler': {
                            'Type': 'Movement Node',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(523.748, 289.793, 54.098),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145930823.5jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-134.438, 0.0, 0.0),
                            'Pos': Point3(450.746, 203.779, 46.001),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145930831.86jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(146.403, 0.0, 0.0),
                            'Pos': Point3(461.825, 233.696, 49.73),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145930832.81jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(176.924, 0.0, 0.0),
                            'Pos': Point3(464.962, 232.218, 49.592),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145930834.79jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(175.529, 0.0, 0.0),
                            'Pos': Point3(471.918, 231.953, 49.579),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145930835.75jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(137.079, 0.0, 0.0),
                            'Pos': Point3(475.23, 231.974, 49.587),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145930836.67jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(145.696, 0.0, 0.0),
                            'Pos': Point3(480.013, 229.892, 49.393),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145930837.61jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(151.59, 0.0, 0.0),
                            'Pos': Point3(483.952, 228.529, 49.34),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145930838.71jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'run',
                            'Hpr': VBase3(146.384, 0.0, 0.0),
                            'Pos': Point3(516.32, 272.092, 49.47),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145930840.53jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(143.882, 0.0, 0.0),
                            'Pos': Point3(456.113, 237.832, 49.697),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145930841.65jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(137.085, 0.0, 0.0),
                            'Pos': Point3(452.242, 240.249, 49.616),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145930844.12jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-170.384, 0.0, 0.0),
                            'Pos': Point3(445.077, 241.998, 48.969),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145930976.73jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-31.563, 0.0, 0.0),
                            'Pos': Point3(477.132, 225.294, 48.948),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 4,
                                'Belt': 1,
                                'BeltColor': 7,
                                'Coat': 2,
                                'CoatColor': 6,
                                'Gender': 'm',
                                'Hair': 8,
                                'HairColor': 3,
                                'Hat': 1,
                                'Mustache': 1,
                                'Pants': 1,
                                'PantsColor': 2,
                                'Shape': 1,
                                'Shirt': 5,
                                'ShirtColor': 3,
                                'Shoe': 1,
                                'Skin': 1,
                                'Sock': 1
                            }
                        },
                        '1145930985.83jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(48.092, 0.0, 0.0),
                            'Pos': Point3(488.59, 225.599, 48.859),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 8,
                                'Belt': 1,
                                'BeltColor': 5,
                                'Coat': 1,
                                'CoatColor': 14,
                                'Gender': 'm',
                                'Hair': 2,
                                'HairColor': 2,
                                'Hat': 3,
                                'Mustache': 1,
                                'Pants': 1,
                                'PantsColor': 2,
                                'Shape': 3,
                                'Shirt': 4,
                                'ShirtColor': 2,
                                'Shoe': 1,
                                'Skin': 2,
                                'Sock': 0
                            }
                        },
                        '1145930998.28jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-12.454, 0.0, 0.0),
                            'Pos': Point3(455.359, 231.842, 49.143),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 8,
                                'Belt': 1,
                                'BeltColor': 6,
                                'Coat': 2,
                                'CoatColor': 7,
                                'Gender': 'm',
                                'Hair': 2,
                                'HairColor': 6,
                                'Hat': 1,
                                'Mustache': 1,
                                'Pants': 3,
                                'PantsColor': 1,
                                'Shape': 1,
                                'Shirt': 4,
                                'ShirtColor': 2,
                                'Shoe': 1,
                                'Skin': 3,
                                'Sock': 1
                            }
                        },
                        '1145931158.81jubutler': {
                            'Type': 'Movement Node',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(488.375, 229.527, 49.266),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145931183.31jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'run',
                            'Hpr': VBase3(147.415, 0.0, 0.0),
                            'Pos': Point3(511.308, 269.768, 49.42),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145931236.17jubutler': {
                            'Type': 'Movement Node',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(485.931, 231.297, 49.557),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145931239.87jubutler': {
                            'Type': 'Movement Node',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(483.407, 233.472, 49.746),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145931286.9jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'run',
                            'Hpr': VBase3(146.803, 0.0, 0.0),
                            'Pos': Point3(511.055, 275.634, 49.478),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145931323.76jubutler': {
                            'Type': 'Movement Node',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(415.995, 231.11, 47.363),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145931394.53jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'run',
                            'Hpr': VBase3(147.486, 0.0, 0.0),
                            'Pos': Point3(489.145, 301.72, 53.606),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145931537.46jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(105.426, 0.0, 0.0),
                            'Pos': Point3(470.803, 201.191, 45.451),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145931583.36jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'run',
                            'Hpr': VBase3(128.91, 0.0, 0.0),
                            'Pos': Point3(501.092, 175.552, 46.178),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145931649.51jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': Point3(128.141, 0.0, 0.0),
                            'Pos': Point3(481.719, 170.07, 45.292),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145931769.37jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(125.249, 0.0, 0.0),
                            'Pos': Point3(459.317, 165.054, 44.927),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145931836.01jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(142.516, 0.0, 0.0),
                            'Pos': Point3(462.342, 135.893, 43.568),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145931861.31jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(132.966, 0.0, 0.0),
                            'Pos': Point3(449.298, 125.352, 43.111),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1145931891.58jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-150.883, 0.0, 0.0),
                            'Pos': Point3(453.335, 111.215, 42.076),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 8,
                                'Belt': 1,
                                'BeltColor': 4,
                                'Coat': 2,
                                'CoatColor': 11,
                                'Gender': 'm',
                                'Hair': 8,
                                'HairColor': 6,
                                'Hat': 3,
                                'Mustache': 1,
                                'Pants': 1,
                                'PantsColor': 3,
                                'Shape': 2,
                                'Shirt': 4,
                                'ShirtColor': 4,
                                'Shoe': 1,
                                'Skin': 2,
                                'Sock': 0
                            }
                        },
                        '1146011197.26jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-29.705, 0.0, 0.0),
                            'Pos': Point3(461.736, 215.321, 47.948),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 0,
                                'Belt': 0,
                                'BeltColor': 4,
                                'Coat': 2,
                                'CoatColor': 13,
                                'Gender': 'm',
                                'Hair': 3,
                                'HairColor': 5,
                                'Hat': 2,
                                'Mustache': 3,
                                'Pants': 3,
                                'PantsColor': 1,
                                'Shape': 1,
                                'Shirt': 7,
                                'ShirtColor': 2,
                                'Shoe': 0,
                                'Skin': 6,
                                'Sock': 0
                            }
                        },
                        '1146011214.89jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-108.256, 0.0, 0.0),
                            'Pos': Point3(458.333, 222.306, 48.534),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 3,
                                'Belt': 2,
                                'BeltColor': 4,
                                'Coat': 2,
                                'CoatColor': 14,
                                'Gender': 'm',
                                'Hair': 0,
                                'HairColor': 4,
                                'Hat': 3,
                                'Mustache': 4,
                                'Pants': 1,
                                'PantsColor': 2,
                                'Shape': 3,
                                'Shirt': 8,
                                'ShirtColor': 0,
                                'Shoe': 0,
                                'Skin': 7,
                                'Sock': 0
                            }
                        },
                        '1146011218.15jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 2',
                            'Hpr': VBase3(-0.754, 0.0, 0.0),
                            'Pos': Point3(444.258, 237.574, 47.725),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 3,
                                'Belt': 3,
                                'BeltColor': 6,
                                'Coat': 0,
                                'CoatColor': 11,
                                'Gender': 'm',
                                'Hair': 13,
                                'HairColor': 1,
                                'Hat': 2,
                                'Mustache': 2,
                                'Pants': 2,
                                'PantsColor': 3,
                                'Shape': 1,
                                'Shirt': 1,
                                'ShirtColor': 4,
                                'Shoe': 1,
                                'Skin': 2,
                                'Sock': 0
                            }
                        },
                        '1146011235.48jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 2',
                            'Hpr': VBase3(-27.214, 0.0, 0.0),
                            'Pos': Point3(449.541, 235.952, 48.432),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 7,
                                'Belt': 0,
                                'BeltColor': 6,
                                'Coat': 2,
                                'CoatColor': 12,
                                'Gender': 'm',
                                'Hair': 14,
                                'HairColor': 4,
                                'Hat': 3,
                                'Mustache': 3,
                                'Pants': 0,
                                'PantsColor': 3,
                                'Shape': 1,
                                'Shirt': 1,
                                'ShirtColor': 2,
                                'Shoe': 2,
                                'Skin': 10,
                                'Sock': 0
                            }
                        },
                        '1146011711.61jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-23.295, 0.0, 0.0),
                            'Pos': Point3(463.506, 227.022, 49.086),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 4,
                                'Belt': 1,
                                'BeltColor': 7,
                                'Coat': 1,
                                'CoatColor': 13,
                                'Gender': 'm',
                                'Hair': 11,
                                'HairColor': 4,
                                'Hat': 3,
                                'Mustache': 1,
                                'Pants': 0,
                                'PantsColor': 2,
                                'Shape': 2,
                                'Shirt': 3,
                                'ShirtColor': 2,
                                'Shoe': 0,
                                'Skin': 6,
                                'Sock': 0
                            }
                        },
                        '1146011797.42jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 2',
                            'Hpr': VBase3(-31.159, 0.0, 0.0),
                            'Pos': Point3(459.162, 229.171, 49.286),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 4,
                                'Belt': 2,
                                'BeltColor': 7,
                                'Coat': 0,
                                'CoatColor': 15,
                                'Gender': 'f',
                                'Hair': 12,
                                'HairColor': 3,
                                'Hat': 3,
                                'Mustache': 5,
                                'Pants': 1,
                                'PantsColor': 3,
                                'Shape': 3,
                                'Shirt': 4,
                                'ShirtColor': 4,
                                'Shoe': 1,
                                'Skin': 11,
                                'Sock': 0
                            }
                        },
                        '1146011803.61jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 2',
                            'Hpr': VBase3(59.334, 0.0, 0.0),
                            'Pos': Point3(475.175, 215.333, 48.187),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 1,
                                'Belt': 1,
                                'BeltColor': 5,
                                'Coat': 0,
                                'CoatColor': 15,
                                'Gender': 'm',
                                'Hair': 0,
                                'HairColor': 6,
                                'Hat': 2,
                                'Mustache': 6,
                                'Pants': 1,
                                'PantsColor': 1,
                                'Shape': 1,
                                'Shirt': 5,
                                'ShirtColor': 2,
                                'Shoe': 1,
                                'Skin': 4,
                                'Sock': 0
                            }
                        },
                        '1146011819.12jubutler': {
                            'Type': 'Animated Avatar - Townfolk',
                            'Animation Track': 'Track 1',
                            'Hpr': VBase3(-39.229, 0.0, 0.0),
                            'Pos': Point3(480.752, 224.412, 48.97),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Beard': 1,
                                'Belt': 0,
                                'BeltColor': 3,
                                'Coat': 2,
                                'CoatColor': 11,
                                'Gender': 'm',
                                'Hair': 8,
                                'HairColor': 2,
                                'Hat': 3,
                                'Mustache': 3,
                                'Pants': 0,
                                'PantsColor': 1,
                                'Shape': 1,
                                'Shirt': 1,
                                'ShirtColor': 2,
                                'Shoe': 2,
                                'Skin': 7,
                                'Sock': 0
                            }
                        },
                        '1146013240.79jubutler': {
                            'Type': 'Animated Avatar - Navy',
                            'Animation Track': 'Track 2',
                            'Hpr': VBase3(-152.159, 0.0, 0.0),
                            'Pos': Point3(468.432, 232.157, 49.593),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(0.0, 0.0, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1144798399.79jubutler': {
                    'Type': 'Cell Portal Area',
                    'Name': 'cell_trail4',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {
                        '1136404761.9dzlu': {
                            'Type': 'Shanty Gypsywagon',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(-92.102, 102.145, 65.617),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/shanty_gypsywagon_exterior'
                            }
                        },
                        '1136415132.05dzlu': {
                            'Type': 'Crate',
                            'Hpr': VBase3(27.474, -1.035, 0.148),
                            'Objects': {},
                            'Pos': Point3(-81.874, 93.275, 65.617),
                            'Scale': VBase3(1.071, 1.071, 1.071),
                            'Visual': {
                                'Color':
                                (0.6000000238418579, 0.6000000238418579,
                                 0.6000000238418579, 1.0),
                                'Model':
                                'models/props/crate'
                            }
                        },
                        '1136415143.75dzlu': {
                            'Type': 'Crate',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Objects': {},
                            'Pos': Point3(-77.499, 87.932, 65.617),
                            'Scale': VBase3(0.991, 0.991, 0.991),
                            'Visual': {
                                'Color':
                                (0.6000000238418579, 0.6000000238418579,
                                 0.6000000238418579, 1.0),
                                'Model':
                                'models/props/crate'
                            }
                        },
                        '1136415145.64dzlu': {
                            'Type': 'Crate',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(-80.597, 89.785, 65.617),
                            'Scale': VBase3(0.743, 0.743, 0.743),
                            'Visual': {
                                'Color': (0.800000011920929, 0.800000011920929,
                                          0.800000011920929, 1.0),
                                'Model':
                                'models/props/crate'
                            }
                        },
                        '1136423361.78dzlu': {
                            'Type': 'Rock',
                            'Hpr': VBase3(-18.445, 0.0, 0.0),
                            'Objects': {},
                            'Pos': Point3(-169.169, 87.825, 59.012),
                            'Scale': VBase3(1.593, 1.593, 1.593),
                            'Visual': {
                                'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                            }
                        },
                        '1136424346.05dzlu': {
                            'Type': 'Rock',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(-116.127, 79.735, 60.285),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                            }
                        },
                        '1136424355.72dzlu': {
                            'Type': 'Rock',
                            'Hpr': VBase3(55.974, 0.0, 0.0),
                            'Objects': {},
                            'Pos': Point3(-65.312, 88.265, 65.616),
                            'Scale': VBase3(2.834, 2.834, 2.834),
                            'Visual': {
                                'Model': 'models/props/zz_dont_use_rock_Dk_4F'
                            }
                        },
                        '1136424363.86dzlu': {
                            'Type': 'Rock',
                            'Hpr': VBase3(111.948, 0.0, 0.0),
                            'Pos': Point3(-53.101, 83.125, 65.617),
                            'Scale': VBase3(0.736, 0.736, 0.736),
                            'Visual': {
                                'Model': 'models/props/zz_dont_use_rock_Dk_2F'
                            }
                        },
                        '1136424372.47dzlu': {
                            'Type': 'Rock',
                            'Hpr': VBase3(111.948, 0.0, 0.0),
                            'Pos': Point3(-58.935, 86.176, 64.859),
                            'Scale': VBase3(1.782, 1.782, 1.782),
                            'Visual': {
                                'Model': 'models/props/zz_dont_use_rock_Dk_2F'
                            }
                        },
                        '1136424437.36dzlu': {
                            'Type': 'Bush',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(-51.458, 81.867, 65.246),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/vegetation/bush_c'
                            }
                        },
                        '1136424475.03dzlu': {
                            'Type': 'Bush',
                            'Hpr': VBase3(95.647, 0.0, 0.0),
                            'Pos': Point3(-34.893, 82.145, 65.135),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/vegetation/bush_c'
                            }
                        },
                        '1136424504.92dzlu': {
                            'Type': 'Bush',
                            'Hpr': VBase3(-60.354, 0.0, 0.0),
                            'Pos': Point3(-18.995, 92.595, 65.621),
                            'Scale': VBase3(0.748, 0.748, 0.748),
                            'Visual': {
                                'Model': 'models/vegetation/bush_d'
                            }
                        },
                        '1136424561.63dzlu': {
                            'Type': 'Bush',
                            'Hpr': VBase3(136.167, 0.0, 0.0),
                            'Pos': Point3(-12.13, 96.672, 65.94),
                            'Scale': VBase3(0.795, 0.795, 0.795),
                            'Visual': {
                                'Model': 'models/vegetation/bush_d'
                            }
                        },
                        '1136424619.11dzlu': {
                            'Type': 'Bush',
                            'Hpr': VBase3(136.167, 0.0, 0.0),
                            'Pos': Point3(-43.346, 86.941, 65.617),
                            'Scale': VBase3(0.795, 0.795, 0.795),
                            'Visual': {
                                'Model': 'models/vegetation/bush_b'
                            }
                        },
                        '1136425587.55dzlu': {
                            'Type': 'Rock',
                            'Hpr': VBase3(-35.353, 0.0, 0.0),
                            'Pos': Point3(16.128, 125.687, 66.865),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                            }
                        },
                        '1136425599.94dzlu': {
                            'Type': 'Rock',
                            'Hpr': VBase3(91.121, -2.969, -10.734),
                            'Objects': {},
                            'Pos': Point3(29.83, 136.501, 66.996),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/props/zz_dont_use_rocks_Dk_group_3F'
                            }
                        },
                        '1136425680.08dzlu': {
                            'Type': 'Rock',
                            'Hpr': VBase3(-177.58, -3.376, 2.514),
                            'Pos': Point3(11.478, 122.264, 66.703),
                            'Scale': VBase3(1.835, 1.835, 1.835),
                            'Visual': {
                                'Model': 'models/props/zz_dont_use_rock_Dk_4F'
                            }
                        },
                        '1138404983.63dxschafe': {
                            'Type':
                            'Rock',
                            'Color': (0.6000000238418579, 0.6000000238418579,
                                      0.6000000238418579, 1.0),
                            'Hpr':
                            Point3(0.0, 0.0, 0.0),
                            'Objects': {},
                            'Pos':
                            Point3(-204.474, -267.29, 1.807),
                            'Scale':
                            VBase3(2.775, 2.775, 2.775),
                            'Visual': {
                                'Model':
                                'models/props/zz_dont_use_rocks_LT_group_1F'
                            }
                        },
                        '1138405610.27dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(21.284, 0.0, 0.0),
                            'Pos': Point3(-215.743, -249.013, 3.607),
                            'Scale': VBase3(1.462, 1.462, 1.462),
                            'Visual': {
                                'Model': 'models/vegetation/bush_c'
                            }
                        },
                        '1138405612.78dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(-145.925, 0.0, 0.0),
                            'Pos': Point3(-209.182, -251.936, 1.818),
                            'Scale': VBase3(1.348, 1.348, 1.348),
                            'Visual': {
                                'Model': 'models/vegetation/bush_c'
                            }
                        }
                    },
                    'Pos': Point3(0.0, 0.0, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1144798400.27jubutler': {
                    'Type': 'Cell Portal Area',
                    'Name': 'cell_shanty_town',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {
                        '1136405019.87dzlu': {
                            'Type': 'Building Exterior',
                            'Name': '',
                            'File': '',
                            'Hpr': VBase3(-3.94, 0.0, 0.0),
                            'Objects': {
                                '1136405019.87dzlu0': {
                                    'Type': 'Locator Node',
                                    'Name': 'portal_exterior_1',
                                    'Hpr': VBase3(90.0, 0.0, 0.0),
                                    'Pos': Point3(3.987, -20.033, 0.0),
                                    'Scale': VBase3(1.0, 1.0, 1.0)
                                }
                            },
                            'Pos': Point3(196.075, 264.07, 65.369),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/shanty_npc_house_combo_B'
                            }
                        },
                        '1136405045.67dzlu': {
                            'Type': 'Building Exterior',
                            'Name': '',
                            'File': '',
                            'Hpr': VBase3(-36.407, 0.0, 0.0),
                            'Objects': {
                                '1136405019.87dzlu0': {
                                    'Type': 'Locator Node',
                                    'Name': 'portal_exterior_1',
                                    'Hpr': VBase3(90.0, 0.0, 0.0),
                                    'Pos': Point3(3.987, -20.033, 0.0),
                                    'Scale': VBase3(1.0, 1.0, 1.0)
                                },
                                '1137811384.33dxschafe': {
                                    'Type': 'Bush',
                                    'GridPos': Point3(228.747, 237.555,
                                                      65.916),
                                    'Hpr': VBase3(107.596, 3.611, -3.72),
                                    'Pos': Point3(9.386, -10.777, 0.092),
                                    'Scale': VBase3(0.552, 0.552, 0.552),
                                    'Visual': {
                                        'Model': 'models/vegetation/bush_d'
                                    }
                                },
                                '1137811457.28dxschafe': {
                                    'Type': 'Tree',
                                    'GridPos': Point3(213.823, 246.641,
                                                      65.332),
                                    'Hpr': VBase3(34.613, 5.7, 0.0),
                                    'Pos': Point3(-8.47, -12.127, -3.271),
                                    'Scale': VBase3(1.043, 1.043, 1.043),
                                    'Visual': {
                                        'Model': 'models/vegetation/gen_tree_d'
                                    }
                                }
                            },
                            'Pos': Point3(227.589, 251.799, 65.824),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/shanty_npc_house_combo_G'
                            }
                        },
                        '1136405115.39dzlu': {
                            'Type': 'Building Exterior',
                            'Name': '',
                            'File': '',
                            'Hpr': VBase3(-152.173, 0.0, 0.0),
                            'Objects': {
                                '1136405019.87dzlu0': {
                                    'Type': 'Locator Node',
                                    'Name': 'portal_exterior_1',
                                    'Hpr': VBase3(90.0, 0.0, 0.0),
                                    'Pos': Point3(3.987, -20.033, 0.0),
                                    'Scale': VBase3(1.0, 1.0, 1.0)
                                },
                                '1138403904.88dxschafe': {
                                    'Type': 'Bucket',
                                    'GridPos': Point3(152.161, 164.5, 73.311),
                                    'Hpr': VBase3(152.173, 0.0, 0.0),
                                    'Pos': Point3(-3.736, -12.128, 2.621),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model': 'models/props/bucket'
                                    }
                                }
                            },
                            'Pos': Point3(154.518, 152.03, 70.69),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/shanty_npc_house_combo_H'
                            }
                        },
                        '1136405216.39dzlu': {
                            'Type': 'Building Exterior',
                            'Name': '',
                            'File': '',
                            'Hpr': VBase3(159.035, 0.0, -3.318),
                            'Objects': {
                                '1136405019.87dzlu0': {
                                    'Type': 'Locator Node',
                                    'Name': 'portal_exterior_1',
                                    'Hpr': VBase3(90.0, 0.0, 0.0),
                                    'Pos': Point3(3.987, -20.033, 0.0),
                                    'Scale': VBase3(1.0, 1.0, 1.0)
                                },
                                '1138402377.67dxschafe': {
                                    'Type': 'Barrel',
                                    'GridPos': Point3(199.962, 189.867,
                                                      78.516),
                                    'Hpr': VBase3(-159.067, -1.187, -3.099),
                                    'Pos': Point3(-10.254, -10.193, 12.792),
                                    'Scale': VBase3(0.71, 0.71, 0.71),
                                    'Visual': {
                                        'Model': 'models/props/barrel'
                                    }
                                }
                            },
                            'Pos': Point3(186.064, 184.276, 66.339),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/shanty_npc_house_combo_C'
                            }
                        },
                        '1136405358.8dzlu': {
                            'Type': 'Building Exterior',
                            'Name': '',
                            'File': '',
                            'Hpr': VBase3(141.858, 2.124, 0.788),
                            'Objects': {
                                '1136405019.87dzlu0': {
                                    'Type': 'Locator Node',
                                    'Name': 'portal_exterior_1',
                                    'Hpr': VBase3(-180.0, 0.0, 0.0),
                                    'Pos': Point3(-0.277, -13.756, 1.023),
                                    'Scale': VBase3(1.0, 1.0, 1.0)
                                },
                                '1137806371.73dxschafe': {
                                    'Type': 'Bush',
                                    'GridPos': Point3(134.801, 159.503,
                                                      75.352),
                                    'Hpr': VBase3(54.196, 0.0, 0.0),
                                    'Pos': Point3(-21.814, -6.083, 0.66),
                                    'Scale': VBase3(0.502, 0.502, 0.502),
                                    'Visual': {
                                        'Model': 'models/vegetation/bush_a'
                                    }
                                },
                                '1137806828.39dxschafe': {
                                    'Type': 'ChickenCage',
                                    'GridPos': Point3(115.422, 189.843,
                                                      78.449),
                                    'Hpr': VBase3(-161.918, -4.648, 2.808),
                                    'Pos': Point3(12.114, -17.853, 4.663),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model': 'models/props/ChickenCage'
                                    }
                                },
                                '1137806913.77dxschafe': {
                                    'Type': 'Tree',
                                    'GridPos': Point3(132.34, 148.196, 76.566),
                                    'Hpr': VBase3(-138.891, 0.0, 8.608),
                                    'Pos': Point3(-26.873, 4.368, 1.418),
                                    'Scale': VBase3(0.616, 0.616, 0.616),
                                    'Visual': {
                                        'Model': 'models/vegetation/gen_tree_d'
                                    }
                                },
                                '1138404226.92dxschafe': {
                                    'Type':
                                    'Rope',
                                    'Color': (0.800000011920929,
                                              0.800000011920929, 1.0, 1.0),
                                    'GridPos':
                                    Point3(139.165, 166.345, 74.177),
                                    'Hpr':
                                    VBase3(-101.498, 2.401, 3.752),
                                    'Pos':
                                    Point3(-21.009, -14.197, -0.204),
                                    'Scale':
                                    VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model': 'models/props/rope_pile'
                                    }
                                }
                            },
                            'Pos': Point3(113.877, 168.16, 74.618),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/shanty_guildhall_exterior'
                            }
                        },
                        '1136405421.64dzlu': {
                            'Type': 'Building Exterior',
                            'Name': '',
                            'File': '',
                            'Hpr': VBase3(72.446, 0.0, 2.517),
                            'Objects': {
                                '1136405019.87dzlu0': {
                                    'Type': 'Locator Node',
                                    'Name': 'portal_exterior_1',
                                    'Hpr': VBase3(0.0, 0.0, 0.0),
                                    'Pos': Point3(-0.277, -13.756, 1.023),
                                    'Scale': VBase3(1.0, 1.0, 1.0)
                                },
                                '1137809822.97dxschafe': {
                                    'Type': 'Bush',
                                    'GridPos': Point3(80.279, 212.567, 76.775),
                                    'Hpr': VBase3(107.52, -2.4, 0.757),
                                    'Pos': Point3(-6.112, -12.308, -1.592),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model': 'models/vegetation/bush_b'
                                    }
                                }
                            },
                            'Pos': Point3(70.407, 222.168, 78.097),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/shanty_npc_house_combo_I'
                            }
                        },
                        '1136405510.23dzlu': {
                            'Type': 'Building Exterior',
                            'Name': '',
                            'File': '',
                            'Hpr': VBase3(176.13, 0.0, 0.0),
                            'Objects': {
                                '1136405019.87dzlu0': {
                                    'Type': 'Locator Node',
                                    'Name': 'portal_exterior_1',
                                    'GridPos': Point3(216.239, 193.396,
                                                      63.885),
                                    'Hpr': VBase3(0.0, 0.0, 0.0),
                                    'Pos': Point3(-0.277, -13.756, 1.023),
                                    'Scale': VBase3(1.0, 1.0, 1.0)
                                },
                                '1137614361.77dxschafe': {
                                    'Type': 'Bush',
                                    'GridPos': Point3(226.388, 160.383,
                                                      57.084),
                                    'Hpr': VBase3(153.326, 9.923, 10.767),
                                    'Pos': Point3(-12.631, 18.497, -5.778),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model': 'models/vegetation/bush_a'
                                    }
                                },
                                '1137806519.13dxschafe': {
                                    'Type': 'Bush',
                                    'GridPos': Point3(201.125, 186.661, 66.36),
                                    'Hpr': VBase3(-176.13, 0.0, 0.0),
                                    'Pos': Point3(14.348, -6.016, 3.498),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Door':
                                        'models/buildings/shanty_guildhall_door',
                                        'Model': 'models/vegetation/bush_b'
                                    }
                                }
                            },
                            'Pos': Point3(215.034, 179.69, 61.171),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Name':
                                '',
                                'Model':
                                'models/buildings/shanty_npc_house_combo_D'
                            }
                        },
                        '1136405787.62dzlu': {
                            'Type': 'Building Exterior',
                            'Name': '',
                            'File': '',
                            'Hpr': VBase3(175.105, 0.0, 0.0),
                            'Objects': {
                                '1136405019.87dzlu0': {
                                    'Type': 'Locator Node',
                                    'Name': 'portal_exterior_1',
                                    'Hpr': VBase3(0.0, 0.0, 0.0),
                                    'Pos': Point3(-0.277, -13.756, 1.023),
                                    'Scale': VBase3(1.0, 1.0, 1.0)
                                },
                                '1137614451.89dxschafe': {
                                    'Type': 'Bush',
                                    'GridPos': Point3(256.285, 192.398,
                                                      58.085),
                                    'Hpr': VBase3(175.377, 0.0, 3.924),
                                    'Pos': Point3(-10.28, -7.707, 8.23),
                                    'Scale': VBase3(1.174, 1.174, 1.174),
                                    'Visual': {
                                        'Model': 'models/vegetation/bush_f'
                                    }
                                },
                                '1138403924.55dxschafe': {
                                    'Type': 'Bucket',
                                    'GridPos': Point3(251.81, 194.142, 67.36),
                                    'Hpr': VBase3(-22.932, 0.0, 0.0),
                                    'Pos': Point3(-5.672, -9.063, 17.505),
                                    'Scale': VBase3(1.0, 1.0, 1.0),
                                    'Visual': {
                                        'Model': 'models/props/bucket'
                                    }
                                }
                            },
                            'Pos': Point3(245.385, 185.596, 49.855),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/buildings/shanty_npc_house_combo_E'
                            }
                        },
                        '1136406250.43dzlu': {
                            'Type': 'Tree - Animated',
                            'Animate': 'models/vegetation/palm_trunk_a_idle',
                            'Color': (1.0, 1.0, 0.6000000238418579, 1.0),
                            'Hpr': VBase3(179.878, -7.928, 1.798),
                            'Pos': Point3(166.408, 181.16, 70.837),
                            'Scale': VBase3(1.376, 1.376, 1.376),
                            'SubObjs': {
                                'Top Model': {
                                    'Visual': {
                                        'Animate':
                                        'models/vegetation/palm_leaf_a_idle',
                                        'Attach':
                                        ['trunk', 'def_trunk_attach'],
                                        'Color': (0.724, 0.972, 0.724, 1.0),
                                        'Model':
                                        'models/vegetation/palm_leaf_b_hi',
                                        'PartName': 'leaf',
                                        'Scale': VBase3(1.252, 1.252, 1.252)
                                    }
                                }
                            },
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_trunk_a_idle',
                                'Color': (0.699999988079071, 0.699999988079071,
                                          0.699999988079071, 1.0),
                                'Model':
                                'models/vegetation/palm_trunk_a_hi',
                                'PartName':
                                'trunk'
                            }
                        },
                        '1136414829.41dzlu': {
                            'Type':
                            'Barrel',
                            'Color': (0.6000000238418579, 0.6000000238418579,
                                      0.6000000238418579, 1.0),
                            'Hpr':
                            VBase3(0.0, 0.0, 117.648),
                            'Pos':
                            Point3(130.5, 282.841, 71.616),
                            'Scale':
                            VBase3(0.648, 0.648, 0.648),
                            'Visual': {
                                'Model': 'models/props/barrel'
                            }
                        },
                        '1136416014.44dzlu': {
                            'Type': 'Tree',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(84.211, 154.518, 74.538),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/vegetation/gen_tree_a'
                            }
                        },
                        '1136416026.95dzlu': {
                            'Type': 'Tree',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(59.872, 156.373, 73.917),
                            'Scale': VBase3(1.043, 1.043, 1.043),
                            'Visual': {
                                'Model': 'models/vegetation/gen_tree_b'
                            }
                        },
                        '1136416077.39dzlu': {
                            'Type': 'Rock',
                            'Hpr': VBase3(60.977, -0.797, -9.551),
                            'Objects': {
                                '1137806724.17dxschafe': {
                                    'Type': 'Bush',
                                    'GridPos': Point3(94.3, 180.638, 80.824),
                                    'Hpr': VBase3(-103.298, -11.46, -0.26),
                                    'Pos': Point3(5.128, -2.258, 0.606),
                                    'Scale': VBase3(0.254, 0.254, 0.254),
                                    'Visual': {
                                        'Model': 'models/vegetation/bush_c'
                                    }
                                }
                            },
                            'Pos': Point3(84.247, 173.151, 77.413),
                            'Scale': VBase3(2.305, 2.305, 2.305),
                            'Visual': {
                                'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                            }
                        },
                        '1136421709.5dzlu': {
                            'Type': 'Tree',
                            'Hpr': VBase3(-26.442, 0.0, 0.0),
                            'Pos': Point3(244.021, 242.469, 65.671),
                            'Scale': VBase3(0.478, 0.478, 0.478),
                            'Visual': {
                                'Model': 'models/vegetation/fern_tree_d'
                            }
                        },
                        '1136421902.08dzlu': {
                            'Type': 'Tree - Animated',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(264.158, 171.193, 54.486),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'SubObjs': {
                                'Top Model': {
                                    'Visual': {
                                        'Animate':
                                        'models/vegetation/palm_leaf_a_idle',
                                        'Attach':
                                        ['trunk', 'def_trunk_attach'],
                                        'Model':
                                        'models/vegetation/palm_leaf_a_hi',
                                        'PartName': 'leaf'
                                    }
                                }
                            },
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_trunk_a_idle',
                                'Model': 'models/vegetation/palm_trunk_a_hi',
                                'PartName': 'trunk'
                            }
                        },
                        '1136426057.16dzlu': {
                            'Type': 'Rock',
                            'Hpr': VBase3(76.724, 12.383, -3.664),
                            'Pos': Point3(245.979, 238.396, 65.326),
                            'Scale': VBase3(1.509, 1.509, 1.509),
                            'Visual': {
                                'Model':
                                'models/props/zz_dont_use_rocks_Dk_group_1F'
                            }
                        },
                        '1137613374.63dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(19.954, -8.974, 0.0),
                            'Pos': Point3(370.225, 145.45, 40.851),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1137613970.36dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(76.203, 12.217, -8.842),
                            'Pos': Point3(300.974, 195.688, 50.062),
                            'Scale': VBase3(0.953, 0.953, 0.953),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1137614058.72dxschafe': {
                            'Type': 'Rock',
                            'Hpr': VBase3(0.0, 0.0, 9.865),
                            'Objects': {
                                '1137614074.95dxschafe': {
                                    'Type': 'Rock',
                                    'GridPos': Point3(290.622, 203.18, 49.937),
                                    'Hpr': VBase3(-154.682, -4.253, -8.909),
                                    'Pos': Point3(-11.44, 9.174, -1.67),
                                    'Scale': VBase3(1.634, 1.634, 1.634),
                                    'Visual': {
                                        'Model':
                                        'models/props/zz_dont_use_rock_Dk_1F'
                                    }
                                }
                            },
                            'Pos': Point3(309.506, 188.19, 49.423),
                            'Scale': VBase3(1.634, 1.634, 1.634),
                            'Visual': {
                                'Model': 'models/props/zz_dont_use_rock_Dk_1F'
                            }
                        },
                        '1137614246.41dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(0.503, -0.525, 1.736),
                            'Pos': Point3(285.17, 210.486, 53.79),
                            'Scale': VBase3(1.536, 1.536, 1.536),
                            'Visual': {
                                'Model': 'models/vegetation/bush_e'
                            }
                        },
                        '1137805871.28dxschafe': {
                            'Type': 'Well',
                            'Hpr': VBase3(53.569, 0.0, 0.0),
                            'Pos': Point3(89.439, 242.903, 71.636),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/wellA'
                            }
                        },
                        '1137805912.08dxschafe': {
                            'Type': 'Cart',
                            'Hpr': VBase3(91.38, 0.0, 0.0),
                            'Pos': Point3(101.478, 258.244, 70.319),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/cart_reg'
                            }
                        },
                        '1137806034.11dxschafe': {
                            'Type': 'ChickenCage',
                            'Hpr': VBase3(36.545, 0.0, 0.0),
                            'Pos': Point3(140.972, 161.049, 74.216),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/ChickenCage'
                            }
                        },
                        '1137806064.89dxschafe': {
                            'Type': 'ChickenCage',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(144.397, 161.658, 73.98),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/ChickenCage'
                            }
                        },
                        '1137806117.05dxschafe': {
                            'Type':
                            'Sack',
                            'Color': (1.0, 0.800000011920929,
                                      0.6000000238418579, 1.0),
                            'Hpr':
                            VBase3(-9.983, -17.673, 7.645),
                            'Pos':
                            Point3(113.479, 193.117, 74.308),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1137806141.44dxschafe': {
                            'Type':
                            'Sack',
                            'Color': (0.800000011920929, 0.800000011920929,
                                      1.0, 1.0),
                            'Hpr':
                            VBase3(-45.821, -9.752, 2.229),
                            'Pos':
                            Point3(110.547, 197.321, 74.201),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/Sack'
                            }
                        },
                        '1137806290.77dxschafe': {
                            'Type':
                            'Crate',
                            'Color': (0.6000000238418579, 0.800000011920929,
                                      1.0, 1.0),
                            'Hpr':
                            VBase3(146.717, 9.404, -3.854),
                            'Pos':
                            Point3(119.228, 189.027, 74.12),
                            'Scale':
                            VBase3(0.968, 0.968, 0.968),
                            'Visual': {
                                'Model': 'models/props/crate'
                            }
                        },
                        '1137806415.02dxschafe': {
                            'Type':
                            'Bush',
                            'Color': (0.6000000238418579, 0.6000000238418579,
                                      0.6000000238418579, 1.0),
                            'Hpr':
                            VBase3(-40.757, 0.0, 0.0),
                            'Pos':
                            Point3(168.441, 188.296, 70.046),
                            'Scale':
                            VBase3(1.674, 1.674, 1.674),
                            'Visual': {
                                'Model': 'models/vegetation/bush_h'
                            }
                        },
                        '1137806634.36dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(-42.304, -2.237, -1.905),
                            'Pos': Point3(154.954, 166.021, 72.771),
                            'Scale': VBase3(0.328, 0.328, 0.328),
                            'Visual': {
                                'Model': 'models/vegetation/bush_c'
                            }
                        },
                        '1137806680.44dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(-42.304, -2.237, -1.905),
                            'Pos': Point3(169.295, 192.582, 69.486),
                            'Scale': VBase3(0.585, 0.585, 0.585),
                            'Visual': {
                                'Model': 'models/vegetation/bush_c'
                            }
                        },
                        '1137808645.7dxschafe': {
                            'Type': 'Tree',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(45.436, 201.763, 82.502),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/vegetation/gen_tree_a'
                            }
                        },
                        '1137809784.5dxschafe': {
                            'Type': 'Rock',
                            'Hpr': VBase3(55.352, 26.27, 4.664),
                            'Pos': Point3(86.117, 219.566, 73.832),
                            'Scale': VBase3(1.166, 1.166, 1.166),
                            'Visual': {
                                'Model': 'models/props/zz_dont_use_rock_Dk_2F'
                            }
                        },
                        '1137810715.7dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(38.132, 1.015, 1.293),
                            'Pos': Point3(171.283, 291.984, 65.212),
                            'Scale': VBase3(0.606, 0.606, 0.606),
                            'Visual': {
                                'Model': 'models/vegetation/bush_g'
                            }
                        },
                        '1137811001.89dxschafe': {
                            'Type': 'Barrel',
                            'Color': (0.75, 1.0, 0.8500000238418579, 1.0),
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(234.945, 235.792, 66.291),
                            'Scale': VBase3(0.537, 0.537, 0.537),
                            'Visual': {
                                'Model': 'models/props/barrel'
                            }
                        },
                        '1137811014.39dxschafe': {
                            'Type': 'Barrel',
                            'Color': (1.0, 1.0, 0.6000000238418579, 1.0),
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(236.161, 238.373, 66.046),
                            'Scale': VBase3(0.537, 0.537, 0.537),
                            'Visual': {
                                'Model': 'models/props/barrel'
                            }
                        },
                        '1137811050.8dxschafe': {
                            'Type': 'Tree',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(108.747, 261.986, 69.603),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/vegetation/fern_tree_c'
                            }
                        },
                        '1137811149.09dxschafe': {
                            'Type': 'Tree - Animated',
                            'Animate': 'models/vegetation/palm_trunk_a_idle',
                            'Hpr': VBase3(0.0, 7.981, 0.0),
                            'Pos': Point3(110.882, 264.141, 68.715),
                            'Scale': VBase3(0.333, 0.333, 0.333),
                            'SubObjs': {
                                'Top Model': {
                                    'Visual': {
                                        'Animate':
                                        'models/vegetation/palm_leaf_a_idle',
                                        'Attach':
                                        ['trunk', 'def_trunk_attach'],
                                        'Color': (0.932, 0.817, 0.724, 1.0),
                                        'Model':
                                        'models/vegetation/palm_leaf_b_hi',
                                        'PartName': 'leaf',
                                        'Scale': VBase3(1.917, 1.917, 1.917)
                                    }
                                }
                            },
                            'Visual': {
                                'Animate':
                                'models/vegetation/palm_trunk_a_idle',
                                'Color':
                                (0.6000000238418579, 0.6000000238418579,
                                 0.6000000238418579, 1.0),
                                'Model':
                                'models/vegetation/palm_trunk_b_hi',
                                'PartName':
                                'trunk'
                            }
                        },
                        '1137811344.75dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(0.8, 4.719, 12.305),
                            'Pos': Point3(264.908, 181.102, 56.697),
                            'Scale': VBase3(1.116, 1.116, 1.116),
                            'Visual': {
                                'Model': 'models/vegetation/bush_d'
                            }
                        },
                        '1138322252.33dxschafe': {
                            'Type': 'Rock',
                            'Hpr': VBase3(-37.197, 0.0, 0.0),
                            'Objects': {},
                            'Pos': Point3(57.771, 206.513, 82.94),
                            'Scale': VBase3(1.34, 1.34, 1.34),
                            'Visual': {
                                'Model':
                                'models/props/zz_dont_use_rocks_Dk_group_1F'
                            }
                        },
                        '1138390465.09dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(-20.281, -1.846, 6.51),
                            'Pos':
                            Point3(352.373, 111.132, 42.134),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/woodfence_B'
                            }
                        },
                        '1138403541.34dxschafe': {
                            'Type': 'Bucket',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(91.779, 243.671, 74.527),
                            'Scale': VBase3(0.719, 0.719, 0.719),
                            'Visual': {
                                'Model': 'models/props/bucket'
                            }
                        },
                        '1138403956.05dxschafe': {
                            'Type':
                            'Bucket',
                            'Color': (0.6000000238418579, 0.6000000238418579,
                                      0.6000000238418579, 1.0),
                            'Hpr':
                            VBase3(-22.932, 0.0, 0.0),
                            'Pos':
                            Point3(187.556, 259.898, 65.741),
                            'Scale':
                            VBase3(1.278, 1.278, 1.278),
                            'Visual': {
                                'Model': 'models/props/bucket'
                            }
                        },
                        '1138404283.64dxschafe': {
                            'Type': 'LaundryRope',
                            'Hpr': VBase3(27.934, 0.0, 0.0),
                            'Pos': Point3(67.118, 203.949, 77.576),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/LaundryRope'
                            }
                        },
                        '1138404327.72dxschafe': {
                            'Type': 'Bucket',
                            'Hpr': VBase3(0.407, -5.599, 4.167),
                            'Pos': Point3(72.279, 206.064, 80.221),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/bucket'
                            }
                        },
                        '1138404604.47dxschafe': {
                            'Type': 'Townsperson',
                            'Category': 'Commoner',
                            'DNA': '1138404604.47dxschafe',
                            'Hpr': VBase3(-104.36, 0.0, 0.0),
                            'Pos': Point3(121.083, 261.771, 69.011),
                            'Respawns': True,
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Start State': 'Idle'
                        },
                        '1138647705.76dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(-39.827, -3.923, 5.517),
                            'Pos':
                            Point3(336.701, 124.634, 44.572),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/woodfence_B'
                            }
                        },
                        '1138647725.99dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(-40.696, -4.006, 5.456),
                            'Pos':
                            Point3(321.991, 137.455, 46.822),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/woodfence_B'
                            }
                        },
                        '1138647755.42dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(-40.696, -4.006, 5.456),
                            'Pos':
                            Point3(307.683, 149.966, 49.231),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/woodfence_B'
                            }
                        },
                        '1138647808.82dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(-19.781, -1.789, -7.1),
                            'Pos':
                            Point3(361.14, 141.897, 40.741),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/woodfence_B'
                            }
                        },
                        '1138647850.51dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(-33.917, -3.067, 4.842),
                            'Pos':
                            Point3(344.189, 153.325, 42.373),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/woodfence_B'
                            }
                        },
                        '1138647880.87dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(-38.694, -3.46, 6.031),
                            'Pos':
                            Point3(328.777, 165.743, 45.081),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/woodfence_B'
                            }
                        },
                        '1138647897.82dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(-38.694, -3.46, 8.538),
                            'Pos':
                            Point3(313.423, 178.258, 48.069),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/woodfence_B'
                            }
                        },
                        '1138647916.19dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(-38.694, -3.46, 8.538),
                            'Pos':
                            Point3(298.425, 190.416, 51.406),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/woodfence_B'
                            }
                        },
                        '1138647926.6dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(-26.566, -1.576, 8.249),
                            'Pos':
                            Point3(281.443, 198.97, 54.301),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/woodfence_B'
                            }
                        },
                        '1138647954.32dxschafe': {
                            'Type':
                            'Wall',
                            'Color': (0.699999988079071, 0.699999988079071,
                                      0.699999988079071, 1.0),
                            'Hpr':
                            VBase3(-71.521, -6.953, 6.745),
                            'Pos':
                            Point3(275.505, 217.939, 57.066),
                            'Scale':
                            VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/buildings/woodfence_B'
                            }
                        },
                        '1138648173.21dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(0.0, 0.0, 18.006),
                            'Pos': Point3(253.562, 236.647, 62.301),
                            'Scale': VBase3(0.5, 0.5, 0.5),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1138740198.35dxschafe': {
                            'Type': 'Tree',
                            'Hpr': VBase3(0.696, 6.058, -5.372),
                            'Pos': Point3(91.294, 147.6, 60.402),
                            'Scale': VBase3(0.795, 0.795, 0.795),
                            'Visual': {
                                'Model': 'models/vegetation/gen_tree_d'
                            }
                        },
                        '1138740362.12dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(-23.597, 0.0, 0.0),
                            'Pos': Point3(59.764, 160.633, 72.303),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        },
                        '1138741723.66dxschafe': {
                            'Type': 'Rock',
                            'Hpr': VBase3(-119.304, -8.216, 1.405),
                            'Pos': Point3(226.531, 200.111, 64.712),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model':
                                'models/props/zz_dont_use_rocks_Dk_group_2F'
                            }
                        },
                        '1138741910.42dxschafe': {
                            'Type': 'Bush',
                            'Hpr': VBase3(-11.978, 4.151, -0.638),
                            'Pos': Point3(221.617, 196.1, 65.553),
                            'Scale': VBase3(0.312, 0.312, 0.312),
                            'Visual': {
                                'Model': 'models/vegetation/bush_a'
                            }
                        }
                    },
                    'Pos': Point3(0.0, 0.0, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145034744.94dxschafe': {
                    'Type': 'Tree',
                    'Hpr': VBase3(-0.021, 2.305, 0.533),
                    'Pos': Point3(298.257, 154.285, 15.474),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_e'
                    }
                },
                '1145644725.87jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(177.172, 0.0, 0.0),
                    'Pos': Point3(477.464, 66.415, 38.198),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 6,
                        'Belt': 1,
                        'BeltColor': 6,
                        'Coat': 1,
                        'CoatColor': 12,
                        'Gender': 'm',
                        'Hair': 2,
                        'HairColor': 4,
                        'Hat': 1,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 2,
                        'Shape': 3,
                        'Shirt': 6,
                        'ShirtColor': 4,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 0
                    }
                },
                '1145644727.81jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-63.094, 0.0, 0.0),
                    'Pos': Point3(468.249, 27.047, 35.453),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 8,
                        'Belt': 1,
                        'BeltColor': 4,
                        'Coat': 2,
                        'CoatColor': 12,
                        'Gender': 'm',
                        'Hair': 4,
                        'HairColor': 8,
                        'Hat': 1,
                        'Mustache': 1,
                        'Pants': 2,
                        'PantsColor': 1,
                        'Shape': 1,
                        'Shirt': 6,
                        'ShirtColor': 1,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 1
                    }
                },
                '1145644729.96jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(48.535, 0.0, 0.0),
                    'Pos': Point3(475.864, 6.572, 34.799),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 5,
                        'Belt': 3,
                        'BeltColor': 6,
                        'Coat': 0,
                        'CoatColor': 11,
                        'Gender': 'm',
                        'Hair': 12,
                        'HairColor': 4,
                        'Hat': 2,
                        'Mustache': 1,
                        'Pants': 3,
                        'PantsColor': 3,
                        'Shape': 1,
                        'Shirt': 8,
                        'ShirtColor': 2,
                        'Shoe': 2,
                        'Skin': 10,
                        'Sock': 0
                    }
                },
                '1145644738.37jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': Point3(296.906, 0.0, 0.0),
                    'Pos': Point3(468.852, -9.806, 31.103),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 1,
                        'Belt': 1,
                        'BeltColor': 4,
                        'Coat': 1,
                        'CoatColor': 11,
                        'Gender': 'm',
                        'Hair': 6,
                        'HairColor': 5,
                        'Hat': 3,
                        'Mustache': 1,
                        'Pants': 3,
                        'PantsColor': 2,
                        'Shape': 2,
                        'Shirt': 5,
                        'ShirtColor': 1,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 0
                    }
                },
                '1145644740.7jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'GridPos': Point3(488.604, -14.147, 18.176),
                    'Hpr': VBase3(-63.094, 0.0, 0.0),
                    'Pos': Point3(488.903, -24.911, 15.312),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 8,
                        'Belt': 1,
                        'BeltColor': 5,
                        'Coat': 2,
                        'CoatColor': 11,
                        'Gender': 'm',
                        'Hair': 3,
                        'HairColor': 3,
                        'Hat': 2,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 3,
                        'Shape': 3,
                        'Shirt': 6,
                        'ShirtColor': 2,
                        'Shoe': 1,
                        'Skin': 1,
                        'Sock': 1
                    }
                },
                '1145644742.56jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(25.64, 0.0, 0.0),
                    'Pos': Point3(470.298, -47.009, 15.33),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 3,
                        'Belt': 1,
                        'BeltColor': 6,
                        'Coat': 0,
                        'CoatColor': 14,
                        'Gender': 'm',
                        'Hair': 3,
                        'HairColor': 1,
                        'Hat': 1,
                        'Mustache': 1,
                        'Pants': 3,
                        'PantsColor': 2,
                        'Shape': 1,
                        'Shirt': 6,
                        'ShirtColor': 4,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 0
                    }
                },
                '1145644744.28jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(109.949, 0.0, 0.0),
                    'Pos': Point3(475.238, -19.992, 27.22),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 8,
                        'Belt': 1,
                        'BeltColor': 3,
                        'Coat': 2,
                        'CoatColor': 15,
                        'Gender': 'm',
                        'Hair': 1,
                        'HairColor': 7,
                        'Hat': 1,
                        'Mustache': 1,
                        'Pants': 2,
                        'PantsColor': 2,
                        'Shape': 1,
                        'Shirt': 5,
                        'ShirtColor': 4,
                        'Shoe': 1,
                        'Skin': 3,
                        'Sock': 0
                    }
                },
                '1145644747.73jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(118.876, 0.0, 0.0),
                    'Pos': Point3(485.568, -108.022, 5.237),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 1,
                        'Belt': 1,
                        'BeltColor': 7,
                        'Coat': 1,
                        'CoatColor': 14,
                        'Gender': 'm',
                        'Hair': 7,
                        'HairColor': 5,
                        'Hat': 1,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 3,
                        'Shape': 1,
                        'Shirt': 6,
                        'ShirtColor': 1,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 1
                    }
                },
                '1145644749.65jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(101.123, 0.0, 0.0),
                    'Pos': Point3(470.008, -101.591, 5.231),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 3,
                        'Belt': 1,
                        'BeltColor': 5,
                        'Coat': 1,
                        'CoatColor': 11,
                        'Gender': 'm',
                        'Hair': 5,
                        'HairColor': 6,
                        'Hat': 3,
                        'Mustache': 1,
                        'Pants': 3,
                        'PantsColor': 1,
                        'Shape': 3,
                        'Shirt': 5,
                        'ShirtColor': 3,
                        'Shoe': 1,
                        'Skin': 1,
                        'Sock': 1
                    }
                },
                '1145644751.46jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-27.442, 0.0, 0.0),
                    'Pos': Point3(480.627, -128.074, 5.224),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 6,
                        'Belt': 1,
                        'BeltColor': 3,
                        'Coat': 0,
                        'CoatColor': 11,
                        'Gender': 'm',
                        'Hair': 2,
                        'HairColor': 1,
                        'Hat': 1,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 2,
                        'Shape': 1,
                        'Shirt': 5,
                        'ShirtColor': 1,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 0
                    }
                },
                '1145644753.17jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-63.094, 0.0, 0.0),
                    'Pos': Point3(473.348, -116.21, 5.231),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 6,
                        'Belt': 1,
                        'BeltColor': 3,
                        'Coat': 1,
                        'CoatColor': 6,
                        'Gender': 'm',
                        'Hair': 8,
                        'HairColor': 5,
                        'Hat': 2,
                        'Mustache': 1,
                        'Pants': 3,
                        'PantsColor': 3,
                        'Shape': 2,
                        'Shirt': 6,
                        'ShirtColor': 4,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 1
                    }
                },
                '1145644755.23jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-77.438, 0.0, 0.0),
                    'Pos': Point3(462.971, -138.24, 5.217),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 1,
                        'Belt': 1,
                        'BeltColor': 5,
                        'Coat': 0,
                        'CoatColor': 14,
                        'Gender': 'm',
                        'Hair': 5,
                        'HairColor': 3,
                        'Hat': 1,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 1,
                        'Shape': 2,
                        'Shirt': 5,
                        'ShirtColor': 3,
                        'Shoe': 1,
                        'Skin': 3,
                        'Sock': 0
                    }
                },
                '1145644757.28jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(59.409, 0.0, 0.0),
                    'Pos': Point3(489.587, -143.613, 5.215),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 4,
                        'Belt': 1,
                        'BeltColor': 3,
                        'Coat': 1,
                        'CoatColor': 9,
                        'Gender': 'm',
                        'Hair': 8,
                        'HairColor': 7,
                        'Hat': 2,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 2,
                        'Shape': 1,
                        'Shirt': 5,
                        'ShirtColor': 2,
                        'Shoe': 1,
                        'Skin': 3,
                        'Sock': 1
                    }
                },
                '1145644768.28jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-45.53, 0.0, 0.0),
                    'Pos': Point3(465.487, -83.066, 5.226),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 5,
                        'Belt': 1,
                        'BeltColor': 5,
                        'Coat': 2,
                        'CoatColor': 11,
                        'Gender': 'm',
                        'Hair': 5,
                        'HairColor': 7,
                        'Hat': 1,
                        'Mustache': 1,
                        'Pants': 3,
                        'PantsColor': 1,
                        'Shape': 1,
                        'Shirt': 6,
                        'ShirtColor': 4,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 0
                    }
                },
                '1145644769.93jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': Point3(296.906, 0.0, 0.0),
                    'Pos': Point3(460.887, -109.647, 5.223),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 7,
                        'Belt': 1,
                        'BeltColor': 3,
                        'Coat': 0,
                        'CoatColor': 15,
                        'Gender': 'm',
                        'Hair': 1,
                        'HairColor': 4,
                        'Hat': 1,
                        'Mustache': 1,
                        'Pants': 2,
                        'PantsColor': 3,
                        'Shape': 3,
                        'Shirt': 5,
                        'ShirtColor': 2,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 0
                    }
                },
                '1145644786.45jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': Point3(130.566, 0.0, 0.0),
                    'Pos': Point3(479.106, -111.606, 5.235),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145644791.54jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': Point3(130.566, 0.0, 0.0),
                    'Pos': Point3(469.707, -136.33, 5.218),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145644794.87jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-112.786, 0.0, 0.0),
                    'Pos': Point3(482.424, -140.246, 5.217),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145644798.12jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(149.925, 0.0, 0.0),
                    'Pos': Point3(484.495, -121.228, 5.229),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145644801.23jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(156.357, 0.0, 0.0),
                    'Pos': Point3(463.563, -103.838, 5.225),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145644804.93jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-141.828, 0.0, 0.0),
                    'Pos': Point3(468.553, -41.649, 18.907),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145644807.75jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(130.566, 0.0, 0.0),
                    'Pos': Point3(470.85, -77.539, 5.231),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145644820.61jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': Point3(130.566, 0.0, 0.0),
                    'Pos': Point3(492.046, -21.45, 16.392),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145644823.76jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-58.217, 0.0, 0.0),
                    'Pos': Point3(469.2, -22.516, 26.317),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145644828.26jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-135.134, 0.0, 0.0),
                    'Pos': Point3(470.963, 10.97, 35.048),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145644831.78jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': Point3(130.566, 0.0, 0.0),
                    'Pos': Point3(472.229, -6.791, 32.298),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145644835.54jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': Point3(130.566, 0.0, 0.0),
                    'Pos': Point3(471.317, 32.095, 36.012),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145644842.93jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-20.533, 0.0, 0.0),
                    'Pos': Point3(476.638, 59.146, 37.682),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145644861.42jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': Point3(130.566, 0.0, 0.0),
                    'Pos': Point3(478.263, 90.874, 40.519),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145652358.58jubutler': {
                    'Type': 'Animated Avatar - Navy',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(13.364, 0.0, 0.0),
                    'Pos': Point3(456.546, 105.728, 41.367),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145652635.43jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-71.927, 0.0, 0.0),
                    'Pos': Point3(463.446, -157.859, 5.213),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 5,
                        'Belt': 1,
                        'BeltColor': 5,
                        'Coat': 2,
                        'CoatColor': 12,
                        'Gender': 'm',
                        'Hair': 1,
                        'HairColor': 7,
                        'Hat': 1,
                        'Mustache': 1,
                        'Pants': 2,
                        'PantsColor': 3,
                        'Shape': 1,
                        'Shirt': 6,
                        'ShirtColor': 2,
                        'Shoe': 1,
                        'Skin': 3,
                        'Sock': 1
                    }
                },
                '1145921233.39jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'run',
                    'Hpr': VBase3(104.014, 0.0, 0.0),
                    'Pos': Point3(503.988, -83.734, 5.607),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 4,
                        'Belt': 1,
                        'BeltColor': 4,
                        'Coat': 2,
                        'CoatColor': 6,
                        'Gender': 'f',
                        'Hair': 6,
                        'HairColor': 2,
                        'Hat': 1,
                        'Mustache': 1,
                        'Pants': 2,
                        'PantsColor': 2,
                        'Shape': 2,
                        'Shirt': 5,
                        'ShirtColor': 4,
                        'Shoe': 1,
                        'Skin': 1,
                        'Sock': 1
                    }
                },
                '1145921264.95jubutler': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(381.645, -119.528, 4.778),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145932081.18jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(115.363, 0.0, 0.0),
                    'Pos': Point3(470.77, -154.535, 5.213),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145932089.36jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(61.431, 0.0, 0.0),
                    'Pos': Point3(470.779, -144.03, 5.213),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145932094.76jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-41.337, 0.0, 0.0),
                    'Pos': Point3(485.111, -149.273, 5.213),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145932097.84jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(61.33, 0.0, 0.0),
                    'Pos': Point3(486.091, -129.771, 5.223),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145932105.58jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(60.325, 0.0, 0.0),
                    'Pos': Point3(491.4, -111.444, 5.235),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145932108.31jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-57.449, 0.0, 0.0),
                    'Pos': Point3(468.762, -119.078, 5.229),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145932111.84jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-12.701, 0.0, 0.0),
                    'Pos': Point3(459.264, -115.991, 5.222),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145932115.11jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(121.868, 0.0, 0.0),
                    'Pos': Point3(475.816, -99.191, 5.236),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145932264.2jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(104.869, 0.0, 0.0),
                    'Pos': Point3(481.288, -98.235, 5.241),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 1,
                        'Belt': 1,
                        'BeltColor': 7,
                        'Coat': 1,
                        'CoatColor': 7,
                        'Gender': 'f',
                        'Hair': 4,
                        'HairColor': 6,
                        'Hat': 1,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 3,
                        'Shape': 2,
                        'Shirt': 4,
                        'ShirtColor': 3,
                        'Shoe': 1,
                        'Skin': 3,
                        'Sock': 1
                    }
                },
                '1145932271.86jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': Point3(125.039, 0.0, 0.0),
                    'Pos': Point3(496.203, -107.774, 5.238),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 4,
                        'Belt': 2,
                        'BeltColor': 5,
                        'Coat': 2,
                        'CoatColor': 7,
                        'Gender': 'm',
                        'Hair': 3,
                        'HairColor': 8,
                        'Hat': 2,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 3,
                        'Shape': 3,
                        'Shirt': 4,
                        'ShirtColor': 1,
                        'Shoe': 1,
                        'Skin': 3,
                        'Sock': 1
                    }
                },
                '1145932277.58jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(84.232, 0.0, 0.0),
                    'Pos': Point3(490.305, -121.928, 5.229),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 5,
                        'Belt': 1,
                        'BeltColor': 6,
                        'Coat': 2,
                        'CoatColor': 10,
                        'Gender': 'f',
                        'Hair': 2,
                        'HairColor': 3,
                        'Hat': 2,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 3,
                        'Shape': 1,
                        'Shirt': 4,
                        'ShirtColor': 1,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 1
                    }
                },
                '1145932280.26jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(88.905, 0.0, 0.0),
                    'Pos': Point3(490.782, -129.826, 5.224),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 7,
                        'Belt': 1,
                        'BeltColor': 5,
                        'Coat': 2,
                        'CoatColor': 14,
                        'Gender': 'm',
                        'Hair': 3,
                        'HairColor': 3,
                        'Hat': 1,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 3,
                        'Shape': 3,
                        'Shirt': 4,
                        'ShirtColor': 4,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 1
                    }
                },
                '1145932282.76jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(26.435, 0.0, 0.0),
                    'Pos': Point3(461.888, -122.346, 5.225),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 1,
                        'Belt': 1,
                        'BeltColor': 4,
                        'Coat': 0,
                        'CoatColor': 11,
                        'Gender': 'm',
                        'Hair': 1,
                        'HairColor': 7,
                        'Hat': 2,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 1,
                        'Shape': 2,
                        'Shirt': 5,
                        'ShirtColor': 2,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 0
                    }
                },
                '1145932290.11jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(36.793, 0.0, 0.0),
                    'Pos': Point3(488.838, -135.346, 5.22),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 5,
                        'Belt': 1,
                        'BeltColor': 3,
                        'Coat': 0,
                        'CoatColor': 11,
                        'Gender': 'm',
                        'Hair': 5,
                        'HairColor': 1,
                        'Hat': 1,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 2,
                        'Shape': 3,
                        'Shirt': 6,
                        'ShirtColor': 1,
                        'Shoe': 1,
                        'Skin': 3,
                        'Sock': 0
                    }
                },
                '1145932293.58jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(77.306, 0.0, 0.0),
                    'Pos': Point3(477.023, -156.049, 5.213),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 2,
                        'Belt': 1,
                        'BeltColor': 5,
                        'Coat': 1,
                        'CoatColor': 14,
                        'Gender': 'f',
                        'Hair': 8,
                        'HairColor': 5,
                        'Hat': 3,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 2,
                        'Shape': 1,
                        'Shirt': 4,
                        'ShirtColor': 1,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 1
                    }
                },
                '1145932305.95jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-40.893, 0.0, 0.0),
                    'Pos': Point3(466.752, -147.965, 5.213),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 2,
                        'Belt': 1,
                        'BeltColor': 6,
                        'Coat': 0,
                        'CoatColor': 11,
                        'Gender': 'm',
                        'Hair': 3,
                        'HairColor': 2,
                        'Hat': 3,
                        'Mustache': 1,
                        'Pants': 3,
                        'PantsColor': 1,
                        'Shape': 3,
                        'Shirt': 6,
                        'ShirtColor': 4,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 0
                    }
                },
                '1145932309.11jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-139.801, 0.0, 0.0),
                    'Pos': Point3(466.969, -132.518, 5.22),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 6,
                        'Belt': 1,
                        'BeltColor': 5,
                        'Coat': 1,
                        'CoatColor': 8,
                        'Gender': 'f',
                        'Hair': 5,
                        'HairColor': 1,
                        'Hat': 2,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 2,
                        'Shape': 1,
                        'Shirt': 4,
                        'ShirtColor': 2,
                        'Shoe': 1,
                        'Skin': 3,
                        'Sock': 1
                    }
                },
                '1145932315.51jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-64.329, 0.0, 0.0),
                    'Pos': Point3(451.757, -118.926, 5.216),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 8,
                        'Belt': 1,
                        'BeltColor': 6,
                        'Coat': 2,
                        'CoatColor': 14,
                        'Gender': 'f',
                        'Hair': 5,
                        'HairColor': 5,
                        'Hat': 2,
                        'Mustache': 1,
                        'Pants': 2,
                        'PantsColor': 2,
                        'Shape': 1,
                        'Shirt': 4,
                        'ShirtColor': 2,
                        'Shoe': 1,
                        'Skin': 1,
                        'Sock': 1
                    }
                },
                '1145932320.64jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-129.85, 0.0, 0.0),
                    'Pos': Point3(460.207, -99.75, 5.222),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 1,
                        'Belt': 1,
                        'BeltColor': 5,
                        'Coat': 1,
                        'CoatColor': 11,
                        'Gender': 'm',
                        'Hair': 8,
                        'HairColor': 8,
                        'Hat': 3,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 3,
                        'Shape': 2,
                        'Shirt': 5,
                        'ShirtColor': 4,
                        'Shoe': 1,
                        'Skin': 3,
                        'Sock': 1
                    }
                },
                '1145932347.87jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'run',
                    'Hpr': VBase3(103.955, 0.0, 0.0),
                    'Pos': Point3(496.423, -85.344, 5.606),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145938552.21jubutler': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(376.104, -120.835, 4.779),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145938845.92jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-38.63, 0.0, 0.0),
                    'Pos': Point3(447.189, -123.886, 5.213),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145938868.23jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(51.584, 0.0, 0.0),
                    'Pos': Point3(469.575, -86.042, 5.23),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145938882.87jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-120.762, 0.0, 0.0),
                    'Pos': Point3(447.236, -115.242, 5.213),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145938898.48jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-106.562, 0.0, 0.0),
                    'Pos': Point3(445.003, -92.832, 5.213),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145938954.73jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(94.818, 0.0, 0.0),
                    'Pos': Point3(457.745, -93.259, 5.22),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145938968.59jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(126.769, 0.0, 0.0),
                    'Pos': Point3(456.522, -105.153, 5.219),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145939021.37jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-99.498, 0.0, 0.0),
                    'Pos': Point3(460.753, -131.674, 5.221),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145939059.67jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(52.814, 0.0, 0.0),
                    'Pos': Point3(452.257, -128.178, 5.216),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 1,
                        'Belt': 1,
                        'BeltColor': 3,
                        'Coat': 2,
                        'CoatColor': 14,
                        'Gender': 'm',
                        'Hair': 3,
                        'HairColor': 5,
                        'Hat': 3,
                        'Mustache': 1,
                        'Pants': 2,
                        'PantsColor': 3,
                        'Shape': 3,
                        'Shirt': 5,
                        'ShirtColor': 1,
                        'Shoe': 1,
                        'Skin': 3,
                        'Sock': 1
                    }
                },
                '1145939098.46jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-103.44, 0.0, 0.0),
                    'Pos': Point3(440.246, -113.548, 5.213),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 5,
                        'Belt': 1,
                        'BeltColor': 7,
                        'Coat': 0,
                        'CoatColor': 11,
                        'Gender': 'm',
                        'Hair': 1,
                        'HairColor': 1,
                        'Hat': 3,
                        'Mustache': 1,
                        'Pants': 3,
                        'PantsColor': 2,
                        'Shape': 3,
                        'Shirt': 6,
                        'ShirtColor': 2,
                        'Shoe': 1,
                        'Skin': 1,
                        'Sock': 1
                    }
                },
                '1145939105.26jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(54.303, 0.0, 0.0),
                    'Pos': Point3(451.621, -93.657, 5.214),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 1,
                        'Belt': 1,
                        'BeltColor': 4,
                        'Coat': 2,
                        'CoatColor': 13,
                        'Gender': 'm',
                        'Hair': 6,
                        'HairColor': 8,
                        'Hat': 3,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 3,
                        'Shape': 1,
                        'Shirt': 6,
                        'ShirtColor': 3,
                        'Shoe': 1,
                        'Skin': 3,
                        'Sock': 1
                    }
                },
                '1145939112.4jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(54.303, 0.0, 0.0),
                    'Pos': Point3(452.905, -108.163, 5.216),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 4,
                        'Belt': 1,
                        'BeltColor': 3,
                        'Coat': 1,
                        'CoatColor': 7,
                        'Gender': 'm',
                        'Hair': 7,
                        'HairColor': 7,
                        'Hat': 3,
                        'Mustache': 1,
                        'Pants': 3,
                        'PantsColor': 1,
                        'Shape': 2,
                        'Shirt': 6,
                        'ShirtColor': 1,
                        'Shoe': 1,
                        'Skin': 3,
                        'Sock': 1
                    }
                },
                '1145939126.04jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-48.704, 0.0, 0.0),
                    'Pos': Point3(501.266, -130.208, 5.224),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 1,
                        'Belt': 1,
                        'BeltColor': 3,
                        'Coat': 2,
                        'CoatColor': 7,
                        'Gender': 'f',
                        'Hair': 4,
                        'HairColor': 6,
                        'Hat': 3,
                        'Mustache': 1,
                        'Pants': 2,
                        'PantsColor': 3,
                        'Shape': 2,
                        'Shirt': 5,
                        'ShirtColor': 2,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 1
                    }
                },
                '1145939134.12jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(121.884, 0.0, 0.0),
                    'Pos': Point3(511.837, -122.44, 5.229),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 3,
                        'Belt': 1,
                        'BeltColor': 5,
                        'Coat': 2,
                        'CoatColor': 11,
                        'Gender': 'm',
                        'Hair': 2,
                        'HairColor': 2,
                        'Hat': 2,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 2,
                        'Shape': 2,
                        'Shirt': 4,
                        'ShirtColor': 4,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 1
                    }
                },
                '1145939158.03jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-177.843, 0.0, 0.0),
                    'Pos': Point3(470.772, -72.153, 6.434),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 7,
                        'Belt': 1,
                        'BeltColor': 4,
                        'Coat': 2,
                        'CoatColor': 14,
                        'Gender': 'm',
                        'Hair': 8,
                        'HairColor': 4,
                        'Hat': 1,
                        'Mustache': 1,
                        'Pants': 3,
                        'PantsColor': 1,
                        'Shape': 3,
                        'Shirt': 6,
                        'ShirtColor': 2,
                        'Shoe': 1,
                        'Skin': 3,
                        'Sock': 1
                    }
                },
                '1145939227.86jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(-53.069, 0.0, 0.0),
                    'Pos': Point3(505.922, -126.938, 5.226),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145939355.92jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': Point3(339.63, 0.0, 0.0),
                    'Pos': Point3(446.673, -104.884, 5.221),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145942263.53jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 2',
                    'GridPos': Point3(461.851, -147.084, 5.213),
                    'Hpr': VBase3(-67.011, 0.0, 0.0),
                    'Pos': Point3(457.51, -140.745, 8.849),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145942341.11jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': Point3(155.808, 0.0, 0.0),
                    'Pos': Point3(421.598, -90.557, 5.288),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 3,
                        'Belt': 1,
                        'BeltColor': 7,
                        'Coat': 2,
                        'CoatColor': 13,
                        'Gender': 'm',
                        'Hair': 8,
                        'HairColor': 3,
                        'Hat': 3,
                        'Mustache': 1,
                        'Pants': 2,
                        'PantsColor': 3,
                        'Shape': 2,
                        'Shirt': 5,
                        'ShirtColor': 4,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 1
                    }
                },
                '1145942350.98jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 2',
                    'Hpr': Point3(155.808, 0.0, 0.0),
                    'Pos': Point3(426.356, -98.597, 5.256),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 3,
                        'Belt': 1,
                        'BeltColor': 6,
                        'Coat': 1,
                        'CoatColor': 12,
                        'Gender': 'm',
                        'Hair': 5,
                        'HairColor': 5,
                        'Hat': 2,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 2,
                        'Shape': 1,
                        'Shirt': 6,
                        'ShirtColor': 1,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 1
                    }
                },
                '1145942355.0jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 2',
                    'Hpr': VBase3(-77.171, 0.0, 0.0),
                    'Pos': Point3(414.872, -103.78, 5.282),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 7,
                        'Belt': 1,
                        'BeltColor': 3,
                        'Coat': 1,
                        'CoatColor': 13,
                        'Gender': 'f',
                        'Hair': 3,
                        'HairColor': 5,
                        'Hat': 1,
                        'Mustache': 1,
                        'Pants': 2,
                        'PantsColor': 1,
                        'Shape': 1,
                        'Shirt': 5,
                        'ShirtColor': 3,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 1
                    }
                },
                '1145942359.21jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 2',
                    'Hpr': VBase3(-92.95, 0.0, 0.0),
                    'Pos': Point3(407.799, -91.728, 5.308),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 8,
                        'Belt': 1,
                        'BeltColor': 6,
                        'Coat': 2,
                        'CoatColor': 8,
                        'Gender': 'm',
                        'Hair': 7,
                        'HairColor': 2,
                        'Hat': 2,
                        'Mustache': 1,
                        'Pants': 2,
                        'PantsColor': 1,
                        'Shape': 3,
                        'Shirt': 4,
                        'ShirtColor': 3,
                        'Shoe': 1,
                        'Skin': 1,
                        'Sock': 1
                    }
                },
                '1145942364.65jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 2',
                    'Hpr': VBase3(22.901, 0.0, 0.0),
                    'Pos': Point3(434.02, -97.724, 5.237),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 6,
                        'Belt': 1,
                        'BeltColor': 3,
                        'Coat': 1,
                        'CoatColor': 6,
                        'Gender': 'f',
                        'Hair': 6,
                        'HairColor': 6,
                        'Hat': 3,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 2,
                        'Shape': 1,
                        'Shirt': 5,
                        'ShirtColor': 3,
                        'Shoe': 1,
                        'Skin': 1,
                        'Sock': 0
                    }
                },
                '1145942368.34jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 2',
                    'Hpr': VBase3(-78.735, 0.0, 0.0),
                    'Pos': Point3(427.359, -112.311, 5.245),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 7,
                        'Belt': 1,
                        'BeltColor': 4,
                        'Coat': 1,
                        'CoatColor': 10,
                        'Gender': 'f',
                        'Hair': 8,
                        'HairColor': 8,
                        'Hat': 1,
                        'Mustache': 1,
                        'Pants': 1,
                        'PantsColor': 3,
                        'Shape': 2,
                        'Shirt': 5,
                        'ShirtColor': 2,
                        'Shoe': 1,
                        'Skin': 2,
                        'Sock': 1
                    }
                },
                '1145942374.51jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(31.187, 0.0, 0.0),
                    'Pos': Point3(413.41, -93.904, 5.292),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145942411.11jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 2',
                    'Hpr': VBase3(108.299, 0.0, 0.0),
                    'Pos': Point3(421.717, -101.368, 5.266),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145942432.17jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(241.527, 0.0, 0.0),
                    'Pos': Point3(427.17, -87.051, 5.262),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145942449.33jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(51.082, 0.0, 0.0),
                    'Pos': Point3(431.181, -102.332, 5.241),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145942455.51jubutler': {
                    'Type': 'Animated Avatar - Skeleton',
                    'Animation Track': 'Track 2',
                    'Hpr': VBase3(93.542, 0.0, 0.0),
                    'Pos': Point3(433.136, -111.666, 5.23),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1145942512.46jubutler': {
                    'Type': 'Animated Avatar - Townfolk',
                    'Animation Track': 'Track 1',
                    'Hpr': VBase3(22.901, 0.0, 0.0),
                    'Pos': Point3(435.917, -120.397, 5.217),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Beard': 1,
                        'Belt': 1,
                        'BeltColor': 4,
                        'Coat': 1,
                        'CoatColor': 13,
                        'Gender': 'm',
                        'Hair': 8,
                        'HairColor': 3,
                        'Hat': 3,
                        'Mustache': 1,
                        'Pants': 2,
                        'PantsColor': 3,
                        'Shape': 3,
                        'Shirt': 6,
                        'ShirtColor': 2,
                        'Shoe': 1,
                        'Skin': 3,
                        'Sock': 1
                    }
                }
            },
            'Visual': {
                'Model': 'models/islands/bilgewater_zero'
            }
        }
    },
    'Node Links':
    [['1145919878.84jubutler', '1145920929.06jubutler', 'Bi-directional'],
     ['1145920993.09jubutler', '1145921024.01jubutler', 'Bi-directional'],
     ['1145921057.15jubutler', '1145921068.83jubutler', 'Bi-directional'],
     ['1145921147.15jubutler', '1145921180.15jubutler', 'Bi-directional'],
     ['1145921233.39jubutler', '1145921264.95jubutler', 'Bi-directional'],
     ['1145921407.98jubutler', '1145599985.09jubutler', 'Bi-directional'],
     ['1145931158.81jubutler', '1145930838.71jubutler', 'Bi-directional'],
     ['1145600011.59jubutler', '1145931323.76jubutler', 'Bi-directional'],
     ['1145931323.76jubutler', '1145931394.53jubutler', 'Bi-directional'],
     ['1145931583.36jubutler', '1145920929.06jubutler', 'Bi-directional'],
     ['1145938552.21jubutler', '1145932347.87jubutler', 'Bi-directional'],
     ['1145931286.9jubutler', '1145931239.87jubutler', 'Bi-directional'],
     ['1145931236.17jubutler', '1145931183.31jubutler', 'Bi-directional']],
    'Layers': {},
    'ObjectIds': {
        '1135280776.06dzlu':
        '["Objects"]["1135280776.06dzlu"]',
        '1135281802.29dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]',
        '1135282109.68dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135282109.68dzlu"]',
        '1135282109.68dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135282109.68dzlu"]["Objects"]["1135282109.68dzlu0"]',
        '1135282286.59dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135282286.59dzlu"]',
        '1135282286.59dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135282286.59dzlu"]["Objects"]["1135282286.59dzlu0"]',
        '1135285775.21dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135285775.21dzlu"]',
        '1135285775.21dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135285775.21dzlu"]["Objects"]["1135285775.21dzlu0"]',
        '1135285783.04dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135285783.04dzlu"]',
        '1135285783.04dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135285783.04dzlu"]["Objects"]["1135285783.04dzlu0"]',
        '1135285791.23dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135285791.23dzlu"]',
        '1135285791.23dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135285791.23dzlu"]["Objects"]["1135285791.23dzlu0"]',
        '1135285802.19dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135285802.19dzlu"]',
        '1135285802.19dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135285802.19dzlu"]["Objects"]["1135285802.19dzlu0"]',
        '1135286034.37dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135286034.37dzlu"]',
        '1135286034.37dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135286034.37dzlu"]["Objects"]["1135286034.37dzlu0"]',
        '1135287336.43dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135287336.43dzlu"]',
        '1135287336.43dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135287336.43dzlu"]["Objects"]["1135287336.43dzlu0"]',
        '1135287679.84dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135287679.84dzlu"]',
        '1135287679.84dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135287679.84dzlu"]["Objects"]["1135287679.84dzlu0"]',
        '1135288077.32dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135288077.32dzlu"]',
        '1135288077.32dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135288077.32dzlu"]["Objects"]["1135288077.32dzlu0"]',
        '1135288180.41dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135288180.4dzlu"]["Objects"]["1135288180.41dzlu"]',
        '1135288180.4dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135288180.4dzlu"]',
        '1135289191.98dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135289191.98dzlu"]',
        '1135289191.98dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135289191.98dzlu"]["Objects"]["1135289191.98dzlu0"]',
        '1135290323.54dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135290323.54dzlu"]',
        '1135290323.54dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135290323.54dzlu"]["Objects"]["1135290323.54dzlu0"]',
        '1135290764.99dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135290764.99dzlu"]',
        '1135971052.31dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135971052.31dzlu"]',
        '1135971052.31dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135971052.31dzlu"]["Objects"]["1135971052.31dzlu0"]',
        '1135971384.22dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135971384.22dzlu"]',
        '1135971384.22dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1135971384.22dzlu"]["Objects"]["1135971384.22dzlu0"]',
        '1136336439.97dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136336439.97dzlu"]',
        '1136336439.97dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136336439.97dzlu"]["Objects"]["1136336439.97dzlu0"]',
        '1136336848.57dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1136336848.57dzlu"]',
        '1136336848.57dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1136336848.57dzlu"]["Objects"]["1136336848.57dzlu0"]',
        '1136337021.82dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136337021.82dzlu"]',
        '1136337021.82dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136337021.82dzlu"]["Objects"]["1136337021.82dzlu0"]',
        '1136338230.04dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136338230.04dzlu"]',
        '1136338238.24dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136338238.24dzlu"]',
        '1136338245.68dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136338245.68dzlu"]',
        '1136338473.55dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136338473.55dzlu"]',
        '1136338506.65dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136338506.65dzlu"]',
        '1136338558.54dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136338558.54dzlu"]',
        '1136338586.88dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136338586.88dzlu"]',
        '1136338602.99dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1136338602.99dzlu"]',
        '1136338641.41dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136338641.41dzlu"]',
        '1136338645.27dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136338645.27dzlu"]',
        '1136338940.62dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136338940.62dzlu"]',
        '1136339511.38dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136339511.38dzlu"]',
        '1136339511.38dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136339511.38dzlu"]["Objects"]["1136339511.38dzlu0"]',
        '1136339759.96dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136339759.96dzlu"]',
        '1136339824.68dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136339824.68dzlu"]',
        '1136339875.1dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136339875.1dzlu"]',
        '1136339970.12dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1136339970.12dzlu"]',
        '1136339985.6dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1136339985.6dzlu"]',
        '1136340207.4dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136340207.4dzlu"]',
        '1136340387.18dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136340387.18dzlu"]',
        '1136340427.54dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1136340427.54dzlu"]',
        '1136340454.07dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136340454.07dzlu"]',
        '1136340700.6dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136340700.6dzlu"]',
        '1136340768.34dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136340768.34dzlu"]',
        '1136404083.2dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136404083.2dzlu"]',
        '1136404538.39dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136404538.39dzlu"]',
        '1136404579.56dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136404579.56dzlu"]',
        '1136404682.97dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136404682.97dzlu"]',
        '1136404761.9dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1136404761.9dzlu"]',
        '1136404859.58dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136404859.58dzlu"]',
        '1136404859.58dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136404859.58dzlu"]["Objects"]["1136404859.58dzlu0"]',
        '1136405019.87dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405019.87dzlu"]',
        '1136405019.87dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405510.23dzlu"]["Objects"]["1136405019.87dzlu0"]',
        '1136405045.67dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405045.67dzlu"]',
        '1136405115.39dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405115.39dzlu"]',
        '1136405216.39dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405216.39dzlu"]',
        '1136405358.8dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405358.8dzlu"]',
        '1136405421.64dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405421.64dzlu"]',
        '1136405510.23dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405510.23dzlu"]',
        '1136405787.62dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405787.62dzlu"]',
        '1136406042.12dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136406042.12dzlu"]',
        '1136406067.58dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136406067.58dzlu"]',
        '1136406102.08dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136406102.08dzlu"]',
        '1136406250.43dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136406250.43dzlu"]',
        '1136406300.36dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136406300.36dzlu"]',
        '1136406305.84dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136406305.84dzlu"]',
        '1136406445.48dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136406445.48dzlu"]',
        '1136406479.8dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136406479.8dzlu"]',
        '1136406533.92dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136406533.92dzlu"]',
        '1136406575.75dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136406575.75dzlu"]',
        '1136409327.53dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136409327.53dzlu"]',
        '1136414736.41dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136414736.41dzlu"]',
        '1136414752.22dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136414752.22dzlu"]',
        '1136414754.64dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136414754.64dzlu"]',
        '1136414802.88dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136414802.88dzlu"]',
        '1136414829.41dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136414829.41dzlu"]',
        '1136415132.05dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1136415132.05dzlu"]',
        '1136415143.75dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1136415143.75dzlu"]',
        '1136415145.64dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1136415145.64dzlu"]',
        '1136415300.02dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136415300.0dzlu"]["Objects"]["1136415300.02dzlu"]',
        '1136415300.0dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136415300.0dzlu"]',
        '1136416014.44dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136416014.44dzlu"]',
        '1136416026.95dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136416026.95dzlu"]',
        '1136416077.39dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136416077.39dzlu"]',
        '1136416540.86dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136416540.86dzlu"]',
        '1136419067.84dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136419067.84dzlu"]',
        '1136419185.55dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136419185.55dzlu"]',
        '1136419266.19dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1136419266.19dzlu"]',
        '1136419312.06dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1136419312.06dzlu"]',
        '1136419382.98dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136419382.98dzlu"]',
        '1136419448.56dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136419448.56dzlu"]',
        '1136419544.14dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136419544.14dzlu"]',
        '1136419587.27dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136419587.27dzlu"]',
        '1136419722.31dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1135281802.29dzlu"]["Objects"]["1136419722.31dzlu"]',
        '1136420549.03dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136420549.03dzlu"]',
        '1136420576.11dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136420576.11dzlu"]',
        '1136420634.92dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136420634.92dzlu"]',
        '1136420641.61dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136420641.61dzlu"]',
        '1136420648.19dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136420648.19dzlu"]',
        '1136420854.45dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136420854.45dzlu"]',
        '1136420887.45dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136420887.45dzlu"]',
        '1136420904.83dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136420904.83dzlu"]',
        '1136420928.28dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136420928.28dzlu"]',
        '1136420937.08dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136420937.08dzlu"]',
        '1136420991.55dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136420991.55dzlu"]',
        '1136421052.95dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136421052.95dzlu"]',
        '1136421055.25dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136421055.25dzlu"]',
        '1136421148.39dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136421148.39dzlu"]',
        '1136421203.13dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136421203.13dzlu"]',
        '1136421219.05dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136421219.05dzlu"]',
        '1136421281.41dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136421281.41dzlu"]',
        '1136421368.44dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136421368.44dzlu"]',
        '1136421438.67dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136421438.67dzlu"]',
        '1136421473.47dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136421473.47dzlu"]',
        '1136421514.02dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136421514.02dzlu"]',
        '1136421687.55dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136421687.55dzlu"]',
        '1136421709.5dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136421709.5dzlu"]',
        '1136421902.08dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136421902.08dzlu"]',
        '1136421948.91dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136421948.91dzlu"]',
        '1136422148.89dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136422148.89dzlu"]',
        '1136422899.75dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136422899.75dzlu"]',
        '1136422912.8dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136422912.8dzlu"]',
        '1136422914.53dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136422914.53dzlu"]',
        '1136422915.92dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136422915.92dzlu"]',
        '1136422957.22dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136422957.22dzlu"]',
        '1136422965.06dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136422965.06dzlu"]',
        '1136422976.59dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136422976.59dzlu"]',
        '1136422988.91dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136422988.91dzlu"]',
        '1136422998.09dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136422998.09dzlu"]',
        '1136423046.98dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423046.98dzlu"]',
        '1136423079.63dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423079.63dzlu"]',
        '1136423080.58dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423080.58dzlu"]',
        '1136423081.72dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423081.72dzlu"]',
        '1136423082.23dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423082.23dzlu"]',
        '1136423086.17dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423086.17dzlu"]',
        '1136423086.81dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423086.81dzlu"]',
        '1136423088.36dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423088.36dzlu"]',
        '1136423088.98dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423088.98dzlu"]',
        '1136423089.81dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423089.81dzlu"]',
        '1136423090.83dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423090.83dzlu"]',
        '1136423091.41dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423091.41dzlu"]',
        '1136423092.0dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423092.0dzlu"]',
        '1136423092.95dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423092.95dzlu"]',
        '1136423094.05dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423094.05dzlu"]',
        '1136423162.5dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423162.5dzlu"]',
        '1136423193.16dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423193.16dzlu"]',
        '1136423237.13dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423237.13dzlu"]',
        '1136423297.98dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423297.98dzlu"]',
        '1136423361.78dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1136423361.78dzlu"]',
        '1136423371.34dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423371.34dzlu"]',
        '1136423530.52dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423530.52dzlu"]',
        '1136423563.91dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423563.91dzlu"]',
        '1136423575.09dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423575.09dzlu"]',
        '1136423593.38dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423593.38dzlu"]',
        '1136423697.94dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423697.94dzlu"]',
        '1136423697.94dzlu0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423697.94dzlu"]["Objects"]["1136423697.94dzlu0"]',
        '1136423796.89dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423796.89dzlu"]',
        '1136423902.0dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423902.0dzlu"]',
        '1136423939.44dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423939.44dzlu"]',
        '1136423964.42dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136423964.42dzlu"]',
        '1136424011.34dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136424011.34dzlu"]',
        '1136424056.56dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136424056.56dzlu"]',
        '1136424058.66dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136424058.66dzlu"]',
        '1136424103.94dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136424103.94dzlu"]',
        '1136424157.73dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136424157.73dzlu"]',
        '1136424231.09dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136424231.09dzlu"]',
        '1136424346.05dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1136424346.05dzlu"]',
        '1136424355.72dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1136424355.72dzlu"]',
        '1136424363.86dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1136424363.86dzlu"]',
        '1136424372.47dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1136424372.47dzlu"]',
        '1136424437.36dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1136424437.36dzlu"]',
        '1136424475.03dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1136424475.03dzlu"]',
        '1136424504.92dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1136424504.92dzlu"]',
        '1136424561.63dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1136424561.63dzlu"]',
        '1136424617.58dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136424617.58dzlu"]',
        '1136424619.11dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1136424619.11dzlu"]',
        '1136424781.72dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136424781.72dzlu"]',
        '1136425088.27dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136425088.27dzlu"]',
        '1136425095.08dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136425095.08dzlu"]',
        '1136425234.44dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136425234.44dzlu"]',
        '1136425587.55dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1136425587.55dzlu"]',
        '1136425599.94dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1136425599.94dzlu"]',
        '1136425680.08dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1136425680.08dzlu"]',
        '1136426057.16dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136426057.16dzlu"]',
        '1136426351.31dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136426351.31dzlu"]',
        '1136426380.89dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136426380.89dzlu"]',
        '1136426422.47dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136426422.47dzlu"]',
        '1136426725.14dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136426725.14dzlu"]',
        '1136426742.25dzlu':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136426742.25dzlu"]',
        '1137608349.11dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137608349.11dxschafe"]',
        '1137608568.63dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137608568.63dxschafe"]',
        '1137608568.63dxschafe0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137608568.63dxschafe"]["Objects"]["1137608568.63dxschafe0"]',
        '1137608982.7dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137608982.7dxschafe"]',
        '1137608998.2dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137608998.2dxschafe"]',
        '1137609001.86dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137608568.63dxschafe"]["Objects"]["1137609001.86dxschafe"]',
        '1137609097.92dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137609097.92dxschafe"]',
        '1137609219.8dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137609219.8dxschafe"]',
        '1137609321.42dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137609321.42dxschafe"]',
        '1137609327.59dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137609327.59dxschafe"]',
        '1137609343.8dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137609343.8dxschafe"]',
        '1137609378.0dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137609378.0dxschafe"]',
        '1137609393.08dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137609393.08dxschafe"]',
        '1137609442.59dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137609442.59dxschafe"]',
        '1137609481.81dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137609481.81dxschafe"]',
        '1137609514.7dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137609097.92dxschafe"]["Objects"]["1137609514.7dxschafe"]',
        '1137609719.03dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137609719.03dxschafe"]',
        '1137609795.34dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137609795.34dxschafe"]',
        '1137610057.31dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137610057.31dxschafe"]',
        '1137610163.19dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137610057.31dxschafe"]["Objects"]["1137610163.19dxschafe"]',
        '1137610228.36dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137610228.36dxschafe"]',
        '1137610308.83dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137610308.83dxschafe"]',
        '1137610374.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137610308.83dxschafe"]["Objects"]["1137610374.89dxschafe"]',
        '1137610441.08dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137610441.08dxschafe"]',
        '1137610539.64dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137610539.64dxschafe"]',
        '1137610581.83dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137610539.64dxschafe"]["Objects"]["1137610581.83dxschafe"]',
        '1137610675.58dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137610675.58dxschafe"]',
        '1137611262.78dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137611262.78dxschafe"]',
        '1137611361.14dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137611361.14dxschafe"]',
        '1137611475.77dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137611475.77dxschafe"]',
        '1137611477.19dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137611477.19dxschafe"]',
        '1137611660.95dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137611660.95dxschafe"]',
        '1137611716.44dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137611716.44dxschafe"]',
        '1137611840.97dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137611840.97dxschafe"]',
        '1137612056.77dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137612056.77dxschafe"]',
        '1137612099.81dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137612099.81dxschafe"]',
        '1137612114.77dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137612099.81dxschafe"]["Objects"]["1137612114.77dxschafe"]',
        '1137612356.78dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137612356.78dxschafe"]',
        '1137612363.58dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137612363.58dxschafe"]',
        '1137612448.58dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137612448.58dxschafe"]',
        '1137612618.48dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137612618.48dxschafe"]',
        '1137612642.58dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137612642.58dxschafe"]',
        '1137612699.33dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137612699.33dxschafe"]',
        '1137612755.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137612755.67dxschafe"]',
        '1137612764.56dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137612764.56dxschafe"]',
        '1137612843.73dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137612843.73dxschafe"]',
        '1137612891.16dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137612891.16dxschafe"]',
        '1137612944.11dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137612944.11dxschafe"]',
        '1137612995.44dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137612995.44dxschafe"]',
        '1137613150.16dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137613150.16dxschafe"]',
        '1137613211.3dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137613211.3dxschafe"]',
        '1137613268.47dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137613268.47dxschafe"]',
        '1137613342.45dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137613342.45dxschafe"]',
        '1137613374.63dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137613374.63dxschafe"]',
        '1137613458.7dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137613458.7dxschafe"]',
        '1137613527.63dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137613527.63dxschafe"]',
        '1137613670.55dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137613670.55dxschafe"]',
        '1137613686.39dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137613686.39dxschafe"]',
        '1137613748.45dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137613748.45dxschafe"]',
        '1137613781.44dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137613781.44dxschafe"]',
        '1137613814.03dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137613814.03dxschafe"]',
        '1137613863.39dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137613863.39dxschafe"]',
        '1137613928.72dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137613928.72dxschafe"]',
        '1137613970.36dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137613970.36dxschafe"]',
        '1137614058.72dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137614058.72dxschafe"]',
        '1137614074.95dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137614058.72dxschafe"]["Objects"]["1137614074.95dxschafe"]',
        '1137614133.34dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137614133.34dxschafe"]',
        '1137614246.41dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137614246.41dxschafe"]',
        '1137614361.77dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405510.23dzlu"]["Objects"]["1137614361.77dxschafe"]',
        '1137614451.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405787.62dzlu"]["Objects"]["1137614451.89dxschafe"]',
        '1137614533.53dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137614533.53dxschafe"]',
        '1137614544.45dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137614544.45dxschafe"]',
        '1137614600.94dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137614600.94dxschafe"]',
        '1137614646.88dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137614646.88dxschafe"]',
        '1137696037.8dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137696037.8dxschafe"]',
        '1137786448.86dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137786448.86dxschafe"]',
        '1137786628.98dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137786628.98dxschafe"]',
        '1137804872.88dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137804872.88dxschafe"]',
        '1137804943.44dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137804943.44dxschafe"]',
        '1137805005.17dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137805005.17dxschafe"]',
        '1137805054.53dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137805054.53dxschafe"]',
        '1137805058.5dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137805058.5dxschafe"]',
        '1137805059.83dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137805059.83dxschafe"]',
        '1137805186.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137805186.67dxschafe"]',
        '1137805871.28dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137805871.28dxschafe"]',
        '1137805912.08dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137805912.08dxschafe"]',
        '1137806034.11dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137806034.11dxschafe"]',
        '1137806064.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137806064.89dxschafe"]',
        '1137806117.05dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137806117.05dxschafe"]',
        '1137806137.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137806137.89dxschafe"]',
        '1137806141.44dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137806141.44dxschafe"]',
        '1137806149.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137806149.67dxschafe"]',
        '1137806158.56dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137806158.56dxschafe"]',
        '1137806228.33dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137806228.33dxschafe"]',
        '1137806271.52dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137806271.52dxschafe"]',
        '1137806290.77dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137806290.77dxschafe"]',
        '1137806371.73dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405358.8dzlu"]["Objects"]["1137806371.73dxschafe"]',
        '1137806415.02dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137806415.02dxschafe"]',
        '1137806519.13dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405510.23dzlu"]["Objects"]["1137806519.13dxschafe"]',
        '1137806572.22dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137806572.22dxschafe"]',
        '1137806634.36dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137806634.36dxschafe"]',
        '1137806680.44dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137806680.44dxschafe"]',
        '1137806724.17dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136416077.39dzlu"]["Objects"]["1137806724.17dxschafe"]',
        '1137806828.39dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405358.8dzlu"]["Objects"]["1137806828.39dxschafe"]',
        '1137806913.77dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405358.8dzlu"]["Objects"]["1137806913.77dxschafe"]',
        '1137807096.63dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137807096.63dxschafe"]',
        '1137807403.13dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137807403.13dxschafe"]',
        '1137807467.02dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137807467.02dxschafe"]',
        '1137807509.48dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137807509.48dxschafe"]',
        '1137807585.05dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137807585.05dxschafe"]',
        '1137807622.05dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137807622.05dxschafe"]',
        '1137808334.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137808334.67dxschafe"]',
        '1137808645.7dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137808645.7dxschafe"]',
        '1137809588.72dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137809588.72dxschafe"]',
        '1137809702.98dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137809702.98dxschafe"]',
        '1137809784.5dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137809784.5dxschafe"]',
        '1137809822.97dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405421.64dzlu"]["Objects"]["1137809822.97dxschafe"]',
        '1137809887.95dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137809887.95dxschafe"]',
        '1137810004.47dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137810004.47dxschafe"]',
        '1137810131.5dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1136415300.0dzlu"]["Objects"]["1137810131.5dxschafe"]',
        '1137810301.38dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137810301.38dxschafe"]',
        '1137810377.2dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137810377.2dxschafe"]',
        '1137810715.7dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137810715.7dxschafe"]',
        '1137810791.5dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137810791.5dxschafe"]',
        '1137810869.36dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137810869.36dxschafe"]',
        '1137810917.73dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137810917.73dxschafe"]',
        '1137811001.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137811001.89dxschafe"]',
        '1137811014.39dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137811014.39dxschafe"]',
        '1137811050.8dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137811050.8dxschafe"]',
        '1137811149.09dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137811149.09dxschafe"]',
        '1137811234.52dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811234.52dxschafe"]',
        '1137811344.75dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1137811344.75dxschafe"]',
        '1137811384.33dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405045.67dzlu"]["Objects"]["1137811384.33dxschafe"]',
        '1137811457.28dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405045.67dzlu"]["Objects"]["1137811457.28dxschafe"]',
        '1137811637.13dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811637.13dxschafe"]',
        '1137811756.92dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811756.92dxschafe"]',
        '1137811771.47dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811771.47dxschafe"]',
        '1137811785.95dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811785.95dxschafe"]',
        '1137811822.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811822.89dxschafe"]',
        '1137811828.17dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811828.17dxschafe"]',
        '1137811838.45dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811838.45dxschafe"]',
        '1137811843.08dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811843.08dxschafe"]',
        '1137811850.0dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811850.0dxschafe"]',
        '1137811916.13dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811916.13dxschafe"]',
        '1137811971.63dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811971.63dxschafe"]',
        '1137811974.33dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811974.33dxschafe"]',
        '1137811978.38dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811978.38dxschafe"]',
        '1137811980.2dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811980.2dxschafe"]',
        '1137811982.36dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811982.36dxschafe"]',
        '1137811983.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811983.89dxschafe"]',
        '1137811986.05dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811986.05dxschafe"]',
        '1137811999.59dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137811999.59dxschafe"]',
        '1137812004.25dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812004.25dxschafe"]',
        '1137812037.88dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812037.88dxschafe"]',
        '1137812040.5dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812040.5dxschafe"]',
        '1137812042.97dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812042.97dxschafe"]',
        '1137812044.56dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812044.56dxschafe"]',
        '1137812045.75dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812045.75dxschafe"]',
        '1137812047.31dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812047.31dxschafe"]',
        '1137812052.39dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812052.39dxschafe"]',
        '1137812053.48dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812053.48dxschafe"]',
        '1137812055.06dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812055.06dxschafe"]',
        '1137812056.75dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812056.75dxschafe"]',
        '1137812060.23dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812060.23dxschafe"]',
        '1137812061.77dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812061.77dxschafe"]',
        '1137812068.19dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812068.19dxschafe"]',
        '1137812069.75dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812069.75dxschafe"]',
        '1137812071.73dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812071.73dxschafe"]',
        '1137812077.53dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812077.53dxschafe"]',
        '1137812079.69dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812079.69dxschafe"]',
        '1137812083.2dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812083.2dxschafe"]',
        '1137812086.39dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812086.39dxschafe"]',
        '1137812087.41dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812087.41dxschafe"]',
        '1137812093.41dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812093.41dxschafe"]',
        '1137812094.86dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812094.86dxschafe"]',
        '1137812153.95dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812153.95dxschafe"]',
        '1137812161.56dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812161.56dxschafe"]',
        '1137812163.47dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812163.47dxschafe"]',
        '1137812165.38dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812165.38dxschafe"]',
        '1137812167.22dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812167.22dxschafe"]',
        '1137812169.88dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812169.88dxschafe"]',
        '1137812171.45dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812171.45dxschafe"]',
        '1137812172.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812172.67dxschafe"]',
        '1137812177.41dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812177.41dxschafe"]',
        '1137812179.3dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812179.3dxschafe"]',
        '1137812182.5dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812182.5dxschafe"]',
        '1137812192.33dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812192.33dxschafe"]',
        '1137812196.17dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812196.17dxschafe"]',
        '1137812199.53dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812199.53dxschafe"]',
        '1137812203.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812203.89dxschafe"]',
        '1137812205.42dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812205.42dxschafe"]',
        '1137812210.59dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812210.59dxschafe"]',
        '1137812218.56dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812218.56dxschafe"]',
        '1137812221.2dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812221.2dxschafe"]',
        '1137812229.81dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812229.81dxschafe"]',
        '1137812264.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812264.89dxschafe"]',
        '1137812267.86dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812267.86dxschafe"]',
        '1137812268.86dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812268.86dxschafe"]',
        '1137812273.73dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812273.73dxschafe"]',
        '1137812275.61dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812275.61dxschafe"]',
        '1137812869.47dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812869.47dxschafe"]',
        '1137812873.55dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812873.55dxschafe"]',
        '1137812875.61dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812875.61dxschafe"]',
        '1137812877.02dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812877.02dxschafe"]',
        '1137812880.44dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812880.44dxschafe"]',
        '1137812885.23dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812885.23dxschafe"]',
        '1137812886.06dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812886.06dxschafe"]',
        '1137812887.13dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812887.13dxschafe"]',
        '1137812910.86dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812910.86dxschafe"]',
        '1137812960.63dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812960.63dxschafe"]',
        '1137812962.36dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812962.36dxschafe"]',
        '1137812965.33dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812965.33dxschafe"]',
        '1137812970.61dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812970.61dxschafe"]',
        '1137812972.64dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812972.64dxschafe"]',
        '1137812974.73dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812974.73dxschafe"]',
        '1137812983.08dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812983.08dxschafe"]',
        '1137812984.13dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812984.13dxschafe"]',
        '1137812990.39dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812990.39dxschafe"]',
        '1137812992.0dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137812992.0dxschafe"]',
        '1137813455.63dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137813455.63dxschafe"]',
        '1137813468.52dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137813468.52dxschafe"]',
        '1137813471.66dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137813471.66dxschafe"]',
        '1137813490.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137813490.89dxschafe"]',
        '1137813494.5dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137813494.5dxschafe"]',
        '1137813533.91dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137813533.91dxschafe"]',
        '1137813537.39dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137813537.39dxschafe"]',
        '1137813540.08dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137813540.08dxschafe"]',
        '1137815176.44dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1137815176.44dxschafe"]',
        '1138062671.39dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137610308.83dxschafe"]["Objects"]["1138062671.39dxschafe"]',
        '1138062672.03dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062672.03dxschafe"]',
        '1138062672.0dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062672.0dxschafe"]',
        '1138062672.14dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062672.14dxschafe"]',
        '1138062672.17dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062672.17dxschafe"]',
        '1138062672.28dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062672.28dxschafe"]',
        '1138062672.31dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062672.31dxschafe"]',
        '1138062672.34dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062672.34dxschafe"]',
        '1138062672.36dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062672.36dxschafe"]',
        '1138062672.48dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062672.48dxschafe"]',
        '1138062672.52dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062672.52dxschafe"]',
        '1138062672.53dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062672.53dxschafe"]',
        '1138062672.56dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062672.56dxschafe"]',
        '1138062672.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062672.67dxschafe"]',
        '1138062672.69dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062672.69dxschafe"]',
        '1138062672.72dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062672.72dxschafe"]',
        '1138062672.75dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062672.75dxschafe"]',
        '1138062672.77dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062672.77dxschafe"]',
        '1138062672.88dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137610308.83dxschafe"]["Objects"]["1138062672.88dxschafe"]',
        '1138062672.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137610308.83dxschafe"]["Objects"]["1138062672.89dxschafe"]',
        '1138062672.92dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137610308.83dxschafe"]["Objects"]["1138062672.92dxschafe"]',
        '1138062672.95dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137610308.83dxschafe"]["Objects"]["1138062672.95dxschafe"]',
        '1138062672.98dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137610308.83dxschafe"]["Objects"]["1138062672.98dxschafe"]',
        '1138062673.06dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137610308.83dxschafe"]["Objects"]["1138062673.06dxschafe"]',
        '1138062673.09dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1137610308.83dxschafe"]["Objects"]["1138062673.09dxschafe"]',
        '1138062673.13dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.13dxschafe"]',
        '1138062673.16dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.16dxschafe"]',
        '1138062673.22dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.22dxschafe"]',
        '1138062673.25dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.25dxschafe"]',
        '1138062673.28dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.28dxschafe"]',
        '1138062673.31dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.31dxschafe"]',
        '1138062673.38dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.38dxschafe"]',
        '1138062673.41dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.41dxschafe"]',
        '1138062673.44dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.44dxschafe"]',
        '1138062673.45dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.45dxschafe"]',
        '1138062673.53dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.53dxschafe"]',
        '1138062673.55dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.55dxschafe"]',
        '1138062673.58dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.58dxschafe"]',
        '1138062673.66dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.66dxschafe"]',
        '1138062673.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.67dxschafe"]',
        '1138062673.78dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.78dxschafe"]',
        '1138062673.7dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.7dxschafe"]',
        '1138062673.83dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.83dxschafe"]',
        '1138062673.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.89dxschafe"]',
        '1138062673.8dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.8dxschafe"]',
        '1138062673.92dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062673.92dxschafe"]',
        '1138062674.02dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062674.02dxschafe"]',
        '1138062674.05dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062674.05dxschafe"]',
        '1138062674.08dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062674.08dxschafe"]',
        '1138062674.19dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062674.19dxschafe"]',
        '1138062674.22dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062674.22dxschafe"]',
        '1138062674.25dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062674.25dxschafe"]',
        '1138062674.28dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062674.28dxschafe"]',
        '1138062798.27dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062798.27dxschafe"]',
        '1138062833.0dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062833.0dxschafe"]',
        '1138062835.84dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062835.84dxschafe"]',
        '1138062846.72dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062846.72dxschafe"]',
        '1138062881.41dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062881.41dxschafe"]',
        '1138062921.28dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062921.28dxschafe"]',
        '1138062964.36dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138062964.36dxschafe"]',
        '1138063055.69dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138063055.69dxschafe"]',
        '1138063140.55dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138063140.55dxschafe"]',
        '1138234931.06dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138234931.06dxschafe"]',
        '1138234946.94dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138234946.94dxschafe"]',
        '1138234981.19dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138234981.19dxschafe"]',
        '1138235031.23dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138235031.23dxschafe"]',
        '1138235106.0dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138235106.0dxschafe"]',
        '1138235258.19dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138235258.19dxschafe"]',
        '1138235266.48dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138235266.48dxschafe"]',
        '1138235274.27dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138235274.27dxschafe"]',
        '1138235338.59dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138235338.59dxschafe"]',
        '1138235427.92dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138235427.92dxschafe"]',
        '1138235463.38dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138235463.38dxschafe"]',
        '1138235468.97dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138235468.97dxschafe"]',
        '1138235509.02dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138235509.02dxschafe"]',
        '1138235729.28dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138235729.28dxschafe"]',
        '1138235815.63dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138235815.63dxschafe"]',
        '1138236384.59dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138236384.59dxschafe"]',
        '1138237076.48dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138237076.48dxschafe"]',
        '1138237587.53dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138237587.53dxschafe"]',
        '1138237708.88dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138237708.88dxschafe"]',
        '1138237708.95dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138237708.95dxschafe"]',
        '1138302709.13dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138302709.13dxschafe"]',
        '1138302819.44dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138302819.44dxschafe"]',
        '1138302833.38dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138302833.38dxschafe"]',
        '1138302835.94dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138302835.94dxschafe"]',
        '1138302857.72dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138302857.72dxschafe"]',
        '1138302885.47dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138302885.47dxschafe"]',
        '1138302895.08dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138302895.08dxschafe"]',
        '1138302898.14dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138302898.14dxschafe"]',
        '1138302910.5dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138302910.5dxschafe"]',
        '1138302929.81dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138302929.81dxschafe"]',
        '1138302931.58dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138302931.58dxschafe"]',
        '1138302936.0dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138302936.0dxschafe"]',
        '1138302961.81dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321117.05dxschafe"]["Objects"]["1138302961.81dxschafe"]',
        '1138302984.48dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138302984.48dxschafe"]',
        '1138302994.61dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138302994.61dxschafe"]',
        '1138303002.52dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138303002.52dxschafe"]',
        '1138303005.69dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138303005.69dxschafe"]',
        '1138313303.97sdnaik':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138313303.97sdnaik"]',
        '1138320260.22dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320260.22dxschafe"]',
        '1138320304.84dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320304.84dxschafe"]',
        '1138320308.77dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320308.77dxschafe"]',
        '1138320333.78dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320333.78dxschafe"]',
        '1138320357.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320357.89dxschafe"]',
        '1138320363.55dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320363.55dxschafe"]',
        '1138320366.47dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320366.47dxschafe"]',
        '1138320476.97dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320476.97dxschafe"]',
        '1138320490.22dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320490.22dxschafe"]',
        '1138320493.22dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320493.22dxschafe"]',
        '1138320513.19dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320513.19dxschafe"]',
        '1138320517.11dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320513.19dxschafe"]["Objects"]["1138320517.11dxschafe"]',
        '1138320526.06dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320304.84dxschafe"]["Objects"]["1138320526.06dxschafe"]',
        '1138320597.94dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138320597.94dxschafe"]',
        '1138320636.58dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320636.58dxschafe"]',
        '1138320640.36dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320640.36dxschafe"]',
        '1138320649.98dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320649.98dxschafe"]',
        '1138320661.88dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138302910.5dxschafe"]["Objects"]["1138320661.88dxschafe"]',
        '1138320670.19dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320333.78dxschafe"]["Objects"]["1138320670.19dxschafe"]',
        '1138320691.84dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320691.84dxschafe"]',
        '1138320711.06dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320711.06dxschafe"]',
        '1138320832.58dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320832.58dxschafe"]',
        '1138320841.61dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320841.61dxschafe"]',
        '1138320843.52dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320843.52dxschafe"]',
        '1138320844.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320844.67dxschafe"]',
        '1138320846.38dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320846.38dxschafe"]',
        '1138320920.13dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320920.13dxschafe"]',
        '1138320920.5dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320920.5dxschafe"]',
        '1138320920.92dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320920.92dxschafe"]',
        '1138320921.48dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320921.48dxschafe"]',
        '1138320922.39dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320922.39dxschafe"]',
        '1138320923.02dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320923.02dxschafe"]',
        '1138320941.11dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320941.11dxschafe"]',
        '1138320941.98dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320941.98dxschafe"]',
        '1138320942.7dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320942.7dxschafe"]',
        '1138320943.48dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320943.48dxschafe"]',
        '1138320944.53dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320944.53dxschafe"]',
        '1138320945.41dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138320945.41dxschafe"]',
        '1138321117.05dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321117.05dxschafe"]',
        '1138321146.64dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321146.64dxschafe"]',
        '1138321241.02dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321241.02dxschafe"]',
        '1138321267.27dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321267.27dxschafe"]',
        '1138321278.73dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321278.73dxschafe"]',
        '1138321280.63dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321280.63dxschafe"]',
        '1138321281.98dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321281.98dxschafe"]',
        '1138321296.0dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321296.0dxschafe"]',
        '1138321296.64dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321296.64dxschafe"]',
        '1138321297.41dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321297.41dxschafe"]',
        '1138321298.06dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321298.06dxschafe"]',
        '1138321298.98dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321298.98dxschafe"]',
        '1138321299.7dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321299.7dxschafe"]',
        '1138321323.97dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321323.97dxschafe"]',
        '1138321325.05dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321325.05dxschafe"]',
        '1138321325.63dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321325.63dxschafe"]',
        '1138321332.92dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321332.92dxschafe"]',
        '1138321333.44dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321333.44dxschafe"]',
        '1138321334.06dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321334.06dxschafe"]',
        '1138321334.66dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321334.66dxschafe"]',
        '1138321336.2dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321336.2dxschafe"]',
        '1138321337.14dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321337.14dxschafe"]',
        '1138321337.91dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321337.91dxschafe"]',
        '1138321347.94dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321347.94dxschafe"]',
        '1138321351.02dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321351.02dxschafe"]',
        '1138321366.27dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321366.27dxschafe"]',
        '1138321388.25dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321388.25dxschafe"]',
        '1138321521.69dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321521.69dxschafe"]',
        '1138321535.25dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138321535.25dxschafe"]',
        '1138322082.3dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322082.3dxschafe"]',
        '1138322153.2dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322153.2dxschafe"]',
        '1138322160.34dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322160.34dxschafe"]',
        '1138322161.17dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322161.17dxschafe"]',
        '1138322162.81dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322162.81dxschafe"]',
        '1138322164.0dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322164.0dxschafe"]',
        '1138322170.58dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322170.58dxschafe"]',
        '1138322171.02dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322171.02dxschafe"]',
        '1138322171.45dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322171.45dxschafe"]',
        '1138322178.02dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322178.02dxschafe"]',
        '1138322179.7dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322179.7dxschafe"]',
        '1138322183.39dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322183.39dxschafe"]',
        '1138322184.19dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322184.19dxschafe"]',
        '1138322184.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322184.67dxschafe"]',
        '1138322186.06dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322186.06dxschafe"]',
        '1138322192.33dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322192.33dxschafe"]',
        '1138322192.73dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322192.73dxschafe"]',
        '1138322193.17dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322193.17dxschafe"]',
        '1138322196.09dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322196.09dxschafe"]',
        '1138322206.23dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322206.23dxschafe"]',
        '1138322206.7dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322206.7dxschafe"]',
        '1138322207.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138322207.67dxschafe"]',
        '1138322208.19dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322208.19dxschafe"]',
        '1138322209.14dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322209.14dxschafe"]',
        '1138322210.05dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322210.05dxschafe"]',
        '1138322213.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322213.67dxschafe"]',
        '1138322214.66dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322214.66dxschafe"]',
        '1138322217.11dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322217.11dxschafe"]',
        '1138322220.91dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322220.91dxschafe"]',
        '1138322221.28dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322221.28dxschafe"]',
        '1138322227.23dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322227.23dxschafe"]',
        '1138322227.7dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322227.7dxschafe"]',
        '1138322228.13dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322228.13dxschafe"]',
        '1138322228.63dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322228.63dxschafe"]',
        '1138322229.2dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322229.2dxschafe"]',
        '1138322230.16dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322230.16dxschafe"]',
        '1138322230.55dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322230.55dxschafe"]',
        '1138322230.91dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322230.91dxschafe"]',
        '1138322231.42dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322231.42dxschafe"]',
        '1138322232.47dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322232.47dxschafe"]',
        '1138322232.8dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322232.8dxschafe"]',
        '1138322233.06dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322233.06dxschafe"]',
        '1138322233.64dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322233.64dxschafe"]',
        '1138322234.11dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322234.11dxschafe"]',
        '1138322234.53dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322234.53dxschafe"]',
        '1138322238.98dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322238.98dxschafe"]',
        '1138322239.42dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322239.42dxschafe"]',
        '1138322239.84dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322239.84dxschafe"]',
        '1138322243.48dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322243.48dxschafe"]',
        '1138322245.98dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322245.98dxschafe"]',
        '1138322246.66dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322245.98dxschafe"]["Objects"]["1138322246.66dxschafe"]',
        '1138322247.14dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322247.14dxschafe"]',
        '1138322252.33dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138322252.33dxschafe"]',
        '1138322252.73dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322252.73dxschafe"]',
        '1138322259.48dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322259.48dxschafe"]',
        '1138322259.92dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322259.92dxschafe"]',
        '1138322260.36dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322260.36dxschafe"]',
        '1138322915.58dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322915.58dxschafe"]',
        '1138324106.59dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138324106.59dxschafe"]',
        '1138324126.88dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138324126.88dxschafe"]',
        '1138324144.91dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138324144.91dxschafe"]',
        '1138324161.06dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138324161.06dxschafe"]',
        '1138324171.53dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138324171.53dxschafe"]',
        '1138324180.14dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138324180.14dxschafe"]',
        '1138324211.02dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138324211.02dxschafe"]',
        '1138324232.17dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138324232.17dxschafe"]',
        '1138324258.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138324258.89dxschafe"]',
        '1138324270.03dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138324270.03dxschafe"]',
        '1138324271.88dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138324271.88dxschafe"]',
        '1138331085.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138331085.67dxschafe"]',
        '1138331085.67dxschafe0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138331085.67dxschafe"]["Objects"]["1138331085.67dxschafe0"]',
        '1138331394.53dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138331394.53dxschafe"]',
        '1138331701.25dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138331701.25dxschafe"]',
        '1138331811.16dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138331811.16dxschafe"]',
        '1138331908.84dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138331908.84dxschafe"]',
        '1138331929.81dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138331929.81dxschafe"]',
        '1138331947.63dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138331947.63dxschafe"]',
        '1138331970.69dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138331970.69dxschafe"]',
        '1138332017.73dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138332017.73dxschafe"]',
        '1138332026.81dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138332026.81dxschafe"]',
        '1138332060.92dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138332060.92dxschafe"]',
        '1138332064.02dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138332064.02dxschafe"]',
        '1138332091.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138332091.67dxschafe"]',
        '1138332164.23dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138332164.23dxschafe"]',
        '1138332190.48dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138332190.48dxschafe"]',
        '1138332193.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138332193.67dxschafe"]',
        '1138332208.34dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138332208.34dxschafe"]',
        '1138332353.31dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138332353.31dxschafe"]',
        '1138332356.11dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138332356.11dxschafe"]',
        '1138332435.56dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138332435.56dxschafe"]',
        '1138333953.2dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138333953.2dxschafe"]',
        '1138333987.34dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138333987.34dxschafe"]',
        '1138334081.11dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138334081.11dxschafe"]',
        '1138334199.27dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138334199.27dxschafe"]',
        '1138387864.66dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138387864.66dxschafe"]',
        '1138388039.38dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138388039.38dxschafe"]',
        '1138388168.08dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138388168.08dxschafe"]',
        '1138388213.14dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138388213.14dxschafe"]',
        '1138388273.94dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138388273.94dxschafe"]',
        '1138388277.56dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138388277.56dxschafe"]',
        '1138388281.3dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138388281.3dxschafe"]',
        '1138388418.02dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138388418.02dxschafe"]',
        '1138388461.27dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138388461.27dxschafe"]',
        '1138388531.19dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138388531.19dxschafe"]',
        '1138388588.09dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138388588.09dxschafe"]',
        '1138388642.84dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138388642.84dxschafe"]',
        '1138388719.81dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138388719.81dxschafe"]',
        '1138388723.69dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138388723.69dxschafe"]',
        '1138388725.05dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138388725.05dxschafe"]',
        '1138389026.84dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389026.84dxschafe"]',
        '1138389038.28dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389038.28dxschafe"]',
        '1138389053.84dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389053.84dxschafe"]',
        '1138389054.97dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389054.97dxschafe"]',
        '1138389058.48dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389058.48dxschafe"]',
        '1138389074.66dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138389074.66dxschafe"]',
        '1138389081.77dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138389081.77dxschafe"]',
        '1138389083.92dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138389083.92dxschafe"]',
        '1138389207.69dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138389207.69dxschafe"]',
        '1138389216.22dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138389216.22dxschafe"]',
        '1138389247.94dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138389247.94dxschafe"]',
        '1138389261.84dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138389261.84dxschafe"]',
        '1138389275.91dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138389275.91dxschafe"]',
        '1138389277.3dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138389277.3dxschafe"]',
        '1138389278.03dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138389278.03dxschafe"]',
        '1138389335.77dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138389335.77dxschafe"]',
        '1138389345.19dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138389345.19dxschafe"]',
        '1138389359.92dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138389359.92dxschafe"]',
        '1138389361.09dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138389361.09dxschafe"]',
        '1138389396.72dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138389396.72dxschafe"]',
        '1138389425.27dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389425.27dxschafe"]',
        '1138389506.56dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389506.56dxschafe"]',
        '1138389517.22dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389517.22dxschafe"]',
        '1138389532.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389532.89dxschafe"]',
        '1138389571.83dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389571.83dxschafe"]',
        '1138389651.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389651.89dxschafe"]',
        '1138389671.64dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389671.64dxschafe"]',
        '1138389681.59dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389681.59dxschafe"]',
        '1138389697.72dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389697.72dxschafe"]',
        '1138389731.03dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389731.03dxschafe"]',
        '1138389735.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389735.67dxschafe"]',
        '1138389791.17dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389791.17dxschafe"]',
        '1138389895.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389895.67dxschafe"]',
        '1138389900.19dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389900.19dxschafe"]',
        '1138390465.09dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138390465.09dxschafe"]',
        '1138390629.63dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138390629.63dxschafe"]',
        '1138390780.11dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138390780.11dxschafe"]',
        '1138390880.48dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138390880.48dxschafe"]',
        '1138391578.09dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138391578.09dxschafe"]',
        '1138391585.31dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138391585.31dxschafe"]',
        '1138391627.27dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138391627.27dxschafe"]',
        '1138391644.33dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138391644.33dxschafe"]',
        '1138391763.7dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138391763.7dxschafe"]',
        '1138391801.88dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138391801.88dxschafe"]',
        '1138391811.81dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138391811.81dxschafe"]',
        '1138391829.34dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138391829.34dxschafe"]',
        '1138391837.23dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138391837.23dxschafe"]',
        '1138391837.27dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138391837.27dxschafe"]',
        '1138391934.66dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138391934.66dxschafe"]',
        '1138392003.38dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138392003.38dxschafe"]',
        '1138392072.44dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138392072.44dxschafe"]',
        '1138392072.44dxschafe0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138392072.44dxschafe"]["Objects"]["1138392072.44dxschafe0"]',
        '1138392261.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138392261.67dxschafe"]',
        '1138393769.47dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138393769.47dxschafe"]',
        '1138393826.88dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138393826.88dxschafe"]',
        '1138393837.09dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138393837.09dxschafe"]',
        '1138393859.16dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138393859.16dxschafe"]',
        '1138393933.52dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138393933.52dxschafe"]',
        '1138393950.38dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138393950.38dxschafe"]',
        '1138393965.91dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138393965.91dxschafe"]',
        '1138393973.61dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138393973.61dxschafe"]',
        '1138394150.83dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138394150.83dxschafe"]',
        '1138394281.47dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138394281.47dxschafe"]',
        '1138394418.23dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138394418.23dxschafe"]',
        '1138394586.5dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138394586.5dxschafe"]',
        '1138394804.84dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138394804.84dxschafe"]',
        '1138394852.03dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138394852.03dxschafe"]',
        '1138395108.81dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138395108.81dxschafe"]',
        '1138395123.31dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138395123.31dxschafe"]',
        '1138395147.94dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138395147.94dxschafe"]',
        '1138395456.77dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138395456.77dxschafe"]',
        '1138396021.42dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138396021.42dxschafe"]',
        '1138396274.88dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138396274.88dxschafe"]',
        '1138396332.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138396332.89dxschafe"]',
        '1138396364.92dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138396364.92dxschafe"]',
        '1138396646.31dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138396646.31dxschafe"]',
        '1138397707.13dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138397707.13dxschafe"]',
        '1138400345.72dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138400345.72dxschafe"]',
        '1138400763.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138400763.67dxschafe"]',
        '1138400773.91dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138400773.91dxschafe"]',
        '1138400798.94dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138400798.94dxschafe"]',
        '1138401436.53dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138401436.53dxschafe"]',
        '1138402377.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405216.39dzlu"]["Objects"]["1138402377.67dxschafe"]',
        '1138402671.14dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138402671.14dxschafe"]',
        '1138402807.2dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138322247.14dxschafe"]["Objects"]["1138402807.2dxschafe"]',
        '1138402892.06dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138402892.06dxschafe"]',
        '1138402997.55dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138402997.55dxschafe"]',
        '1138403067.3dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138403067.3dxschafe"]',
        '1138403080.25dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138403080.25dxschafe"]',
        '1138403165.69dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138403165.69dxschafe"]',
        '1138403541.34dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138403541.34dxschafe"]',
        '1138403904.88dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405115.39dzlu"]["Objects"]["1138403904.88dxschafe"]',
        '1138403924.55dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405787.62dzlu"]["Objects"]["1138403924.55dxschafe"]',
        '1138403956.05dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138403956.05dxschafe"]',
        '1138404226.92dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1136405358.8dzlu"]["Objects"]["1138404226.92dxschafe"]',
        '1138404283.64dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138404283.64dxschafe"]',
        '1138404327.72dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138404327.72dxschafe"]',
        '1138404604.47dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138404604.47dxschafe"]',
        '1138404941.83dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138404941.83dxschafe"]',
        '1138404947.05dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138404947.05dxschafe"]',
        '1138404952.7dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138404952.7dxschafe"]',
        '1138404955.5dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138404955.5dxschafe"]',
        '1138404962.61dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138404962.61dxschafe"]',
        '1138404962.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138404962.67dxschafe"]',
        '1138404965.13dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138404965.13dxschafe"]',
        '1138404966.3dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138404966.3dxschafe"]',
        '1138404983.63dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1138404983.63dxschafe"]',
        '1138404990.83dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138404990.83dxschafe"]',
        '1138404993.45dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138404993.45dxschafe"]',
        '1138404994.17dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138404994.17dxschafe"]',
        '1138404996.56dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138404996.56dxschafe"]',
        '1138404997.58dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138404997.58dxschafe"]',
        '1138404998.63dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138404998.63dxschafe"]',
        '1138405003.19dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138405003.19dxschafe"]',
        '1138405003.73dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138405003.73dxschafe"]',
        '1138405005.31dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138405005.31dxschafe"]',
        '1138405008.59dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138405008.59dxschafe"]',
        '1138405009.48dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138405009.48dxschafe"]',
        '1138405014.53dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138405014.53dxschafe"]',
        '1138405015.67dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138405015.67dxschafe"]',
        '1138405016.3dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138405016.3dxschafe"]',
        '1138405255.73dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138405255.73dxschafe"]',
        '1138405427.22dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138405427.22dxschafe"]',
        '1138405547.0dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138405547.0dxschafe"]',
        '1138405584.83dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138405584.83dxschafe"]',
        '1138405610.27dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1138405610.27dxschafe"]',
        '1138405612.78dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]["Objects"]["1138405612.78dxschafe"]',
        '1138405639.5dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138405639.5dxschafe"]',
        '1138405669.55dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138405669.55dxschafe"]',
        '1138406264.66dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138406264.66dxschafe"]',
        '1138406308.7dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138406308.7dxschafe"]',
        '1138406395.17dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138406395.17dxschafe"]',
        '1138406441.97dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138404994.17dxschafe"]["Objects"]["1138406441.97dxschafe"]',
        '1138406484.72dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138404994.17dxschafe"]["Objects"]["1138406484.72dxschafe"]',
        '1138406506.36dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138404994.17dxschafe"]["Objects"]["1138406506.36dxschafe"]',
        '1138406672.28dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138406672.28dxschafe"]',
        '1138406690.55dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138406690.55dxschafe"]',
        '1138406692.61dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138406692.61dxschafe"]',
        '1138406753.16dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138406753.16dxschafe"]',
        '1138406774.14dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138406774.14dxschafe"]',
        '1138406776.23dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138406776.23dxschafe"]',
        '1138406881.92dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138406881.92dxschafe"]',
        '1138407053.23dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138407053.23dxschafe"]',
        '1138407116.95dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138407053.23dxschafe"]["Objects"]["1138407116.95dxschafe"]',
        '1138407288.64dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138407288.64dxschafe"]',
        '1138410072.17dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138410072.17dxschafe"]',
        '1138410112.63dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138410112.63dxschafe"]',
        '1138410625.44dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138410625.44dxschafe"]',
        '1138410659.77dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138410659.77dxschafe"]',
        '1138410666.5dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138410666.5dxschafe"]',
        '1138410875.87dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138410875.87dxschafe"]',
        '1138411180.17dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138411180.17dxschafe"]',
        '1138411274.68dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138411274.68dxschafe"]',
        '1138411280.35dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138411280.35dxschafe"]',
        '1138411455.04dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138411455.04dxschafe"]',
        '1138411521.86dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138411521.86dxschafe"]',
        '1138418428.85dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138418428.85dxschafe"]',
        '1138418666.85dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138418666.85dxschafe"]',
        '1138418677.87dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138418677.87dxschafe"]',
        '1138418930.61dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138418930.61dxschafe"]',
        '1138420222.41dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138420222.41dxschafe"]',
        '1138420265.62dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138420265.62dxschafe"]',
        '1138420321.09dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138420321.09dxschafe"]',
        '1138647059.31dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138647059.31dxschafe"]',
        '1138647125.22dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138647125.22dxschafe"]',
        '1138647705.76dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138647705.76dxschafe"]',
        '1138647725.99dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138647725.99dxschafe"]',
        '1138647755.42dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138647755.42dxschafe"]',
        '1138647768.95dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138647768.95dxschafe"]',
        '1138647808.82dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138647808.82dxschafe"]',
        '1138647850.51dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138647850.51dxschafe"]',
        '1138647880.87dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138647880.87dxschafe"]',
        '1138647897.82dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138647897.82dxschafe"]',
        '1138647916.19dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138647916.19dxschafe"]',
        '1138647926.6dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138647926.6dxschafe"]',
        '1138647954.32dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138647954.32dxschafe"]',
        '1138647970.19dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138647970.19dxschafe"]',
        '1138648022.36dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138648022.36dxschafe"]',
        '1138648173.21dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138648173.21dxschafe"]',
        '1138648723.89dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138648723.89dxschafe"]',
        '1138648754.45dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138648754.45dxschafe"]',
        '1138648762.68dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138648762.68dxschafe"]',
        '1138648765.79dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138648765.79dxschafe"]',
        '1138648770.65dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138648770.65dxschafe"]',
        '1138648980.13dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138648980.13dxschafe"]',
        '1138648987.98dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138648987.98dxschafe"]',
        '1138648995.2dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138648995.2dxschafe"]',
        '1138649012.41dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138649012.41dxschafe"]',
        '1138649057.34dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138649057.34dxschafe"]',
        '1138649219.47dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138649219.47dxschafe"]',
        '1138649279.9dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138649279.9dxschafe"]',
        '1138649427.11dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138649427.11dxschafe"]',
        '1138649483.26dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138649483.26dxschafe"]',
        '1138649500.4dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138649500.4dxschafe"]',
        '1138649530.65dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138649530.65dxschafe"]',
        '1138649548.09dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138649548.09dxschafe"]',
        '1138649567.19dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138649567.19dxschafe"]',
        '1138649836.96dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138649836.96dxschafe"]',
        '1138650056.86dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138650056.86dxschafe"]',
        '1138650910.16dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138650910.16dxschafe"]',
        '1138653812.79dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138653812.79dxschafe"]',
        '1138653878.91dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138653878.91dxschafe"]',
        '1138654406.52dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138654406.52dxschafe"]',
        '1138654445.13dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138654445.13dxschafe"]',
        '1138654459.26dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138654459.26dxschafe"]',
        '1138654466.22dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138654466.22dxschafe"]',
        '1138654495.33dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138654495.33dxschafe"]',
        '1138654694.39dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138654694.39dxschafe"]',
        '1138654942.33dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138654942.33dxschafe"]',
        '1138654960.52dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138654960.52dxschafe"]',
        '1138655007.18dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138655007.18dxschafe"]',
        '1138655029.02dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138655029.02dxschafe"]',
        '1138655047.68dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138655047.68dxschafe"]',
        '1138655096.28dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138655096.28dxschafe"]',
        '1138655111.7dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138655111.7dxschafe"]',
        '1138655124.07dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138655124.07dxschafe"]',
        '1138655133.26dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138655133.26dxschafe"]',
        '1138655281.94dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138655281.94dxschafe"]',
        '1138655487.29dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138655487.29dxschafe"]',
        '1138655678.03dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138655678.03dxschafe"]',
        '1138656107.95dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138656107.95dxschafe"]',
        '1138657546.06dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138657546.06dxschafe"]',
        '1138657845.1dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138657845.1dxschafe"]',
        '1138658065.75dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138658065.75dxschafe"]',
        '1138658204.28dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138658204.28dxschafe"]',
        '1138660462.68dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389532.89dxschafe"]["Objects"]["1138660462.68dxschafe"]',
        '1138660499.28dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138660499.28dxschafe"]',
        '1138660565.68dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138660565.68dxschafe"]',
        '1138660671.69dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138660671.69dxschafe"]',
        '1138660730.71dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138660730.71dxschafe"]',
        '1138660848.26dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138660848.26dxschafe"]',
        '1138660900.34dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138660900.34dxschafe"]',
        '1138660918.74dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138660918.74dxschafe"]',
        '1138660934.73dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138660934.73dxschafe"]',
        '1138660934.79dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138660934.79dxschafe"]',
        '1138661075.26dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138661075.26dxschafe"]',
        '1138661095.45dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138661095.45dxschafe"]',
        '1138661112.78dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138661112.78dxschafe"]',
        '1138661174.33dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138661174.33dxschafe"]',
        '1138661379.77dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138661379.77dxschafe"]',
        '1138661665.88dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138661665.88dxschafe"]',
        '1138661712.71dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138661712.71dxschafe"]',
        '1138661916.96dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138661916.96dxschafe"]',
        '1138661917.93dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138661917.93dxschafe"]',
        '1138661933.68dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138661933.68dxschafe"]',
        '1138661945.7dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138661945.7dxschafe"]',
        '1138661954.82dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138661954.82dxschafe"]',
        '1138661969.71dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138661969.71dxschafe"]',
        '1138661976.46dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138661976.46dxschafe"]',
        '1138661989.79dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138661989.79dxschafe"]',
        '1138662146.61dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138662146.61dxschafe"]',
        '1138662162.49dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138662162.49dxschafe"]',
        '1138662175.92dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138662175.92dxschafe"]',
        '1138662302.49dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138662302.49dxschafe"]',
        '1138662442.07dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138662442.07dxschafe"]',
        '1138662448.51dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138662448.51dxschafe"]',
        '1138662477.73dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138662477.73dxschafe"]',
        '1138662487.83dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138662487.83dxschafe"]',
        '1138662582.92dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138662582.92dxschafe"]',
        '1138662609.56dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138662609.56dxschafe"]',
        '1138662966.03dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138662966.03dxschafe"]',
        '1138663053.09dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138663053.09dxschafe"]',
        '1138663093.3dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138663093.3dxschafe"]',
        '1138663154.02dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138663154.02dxschafe"]',
        '1138663183.22dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138663183.22dxschafe"]',
        '1138663205.14dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138663205.14dxschafe"]',
        '1138663279.71dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138663279.71dxschafe"]',
        '1138663287.74dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138663287.74dxschafe"]',
        '1138663371.07dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138663371.07dxschafe"]',
        '1138666284.38dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138666284.38dxschafe"]',
        '1138666879.15dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138666879.15dxschafe"]',
        '1138666979.31dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138666979.31dxschafe"]',
        '1138667062.52dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138667062.52dxschafe"]',
        '1138667090.27dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138667090.27dxschafe"]',
        '1138667147.04dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138667147.04dxschafe"]',
        '1138667270.49dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138667270.49dxschafe"]',
        '1138667406.75dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138667406.75dxschafe"]',
        '1138667460.66dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138667460.66dxschafe"]',
        '1138695512.45jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138695512.45jubutler"]',
        '1138721865.99dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138721865.99dxschafe"]',
        '1138722751.38dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138722751.38dxschafe"]',
        '1138722751.38dxschafe0':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138722751.38dxschafe"]["Objects"]["1138722751.38dxschafe0"]',
        '1138725193.96dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138725193.96dxschafe"]',
        '1138725240.0dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138725240.0dxschafe"]',
        '1138726034.66dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138726034.66dxschafe"]',
        '1138727343.41dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138727343.41dxschafe"]',
        '1138727460.57dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138389506.56dxschafe"]["Objects"]["1138727460.57dxschafe"]',
        '1138728593.36dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138728593.36dxschafe"]',
        '1138728779.92dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138728779.92dxschafe"]',
        '1138729936.15dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138729936.15dxschafe"]',
        '1138730047.82dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138730047.82dxschafe"]',
        '1138730274.97dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138730274.97dxschafe"]',
        '1138730803.13dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138730803.13dxschafe"]',
        '1138731189.79dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138731189.79dxschafe"]',
        '1138732475.17dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138732475.17dxschafe"]',
        '1138732592.53dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138732592.53dxschafe"]',
        '1138732687.6dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138732687.6dxschafe"]',
        '1138732731.02dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138732731.02dxschafe"]',
        '1138732820.2dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138732820.2dxschafe"]',
        '1138732869.65dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138732869.65dxschafe"]',
        '1138733059.16dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138733059.16dxschafe"]',
        '1138733108.16dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138733108.16dxschafe"]',
        '1138733146.24dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138733146.24dxschafe"]',
        '1138733189.2dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138733189.2dxschafe"]',
        '1138739708.58dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138739708.58dxschafe"]',
        '1138739839.69dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138739839.69dxschafe"]',
        '1138739944.52dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138739944.52dxschafe"]',
        '1138740055.77dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138740055.77dxschafe"]',
        '1138740107.6dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138740107.6dxschafe"]',
        '1138740198.35dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138740198.35dxschafe"]',
        '1138740362.12dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138740362.12dxschafe"]',
        '1138740455.21dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138740455.21dxschafe"]',
        '1138740545.15dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138740545.15dxschafe"]',
        '1138741723.66dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138741723.66dxschafe"]',
        '1138741910.42dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]["Objects"]["1138741910.42dxschafe"]',
        '1138742465.08dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138742465.08dxschafe"]',
        '1138742593.3dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138742593.3dxschafe"]',
        '1138742820.76dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138742820.76dxschafe"]',
        '1138743352.03dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1138743352.03dxschafe"]',
        '1144695643.19sdnaik':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144695643.19sdnaik"]',
        '1144695645.11sdnaik':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144695645.11sdnaik"]',
        '1144695701.45sdnaik':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144695701.45sdnaik"]',
        '1144695701.48sdnaik':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144695701.48sdnaik"]',
        '1144695785.45sdnaik':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144695785.45sdnaik"]',
        '1144695785.47sdnaik':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144695785.45sdnaik"]["Objects"]["1144695785.47sdnaik"]',
        '1144695785.52sdnaik':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144695785.45sdnaik"]["Objects"]["1144695785.52sdnaik"]',
        '1144696039.86sdnaik':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138313303.97sdnaik"]["Objects"]["1144696039.86sdnaik"]',
        '1144696042.95sdnaik':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1138313303.97sdnaik"]["Objects"]["1144696042.95sdnaik"]',
        '1144696205.34sdnaik':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144696205.34sdnaik"]',
        '1144696205.36sdnaik':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144696205.34sdnaik"]["Objects"]["1144696205.36sdnaik"]',
        '1144696208.66sdnaik':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144696205.34sdnaik"]["Objects"]["1144696208.66sdnaik"]',
        '1144798398.96jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]',
        '1144798399.79jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798399.79jubutler"]',
        '1144798400.27jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798400.27jubutler"]',
        '1145031108.13dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145031108.13dxschafe"]',
        '1145034744.94dxschafe':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145034744.94dxschafe"]',
        '1145599967.98jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145599967.98jubutler"]',
        '1145599970.4jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145599970.4jubutler"]',
        '1145599974.12jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145599974.12jubutler"]',
        '1145599977.58jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145599977.58jubutler"]',
        '1145599985.09jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145599985.09jubutler"]',
        '1145599999.11jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145599999.11jubutler"]',
        '1145600004.56jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145600004.56jubutler"]',
        '1145600011.59jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145600011.59jubutler"]',
        '1145600014.73jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145600014.73jubutler"]',
        '1145644673.0jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145644673.0jubutler"]',
        '1145644694.48jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145644694.48jubutler"]',
        '1145644708.43jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145644708.43jubutler"]',
        '1145644714.42jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145644714.42jubutler"]',
        '1145644715.95jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145644715.95jubutler"]',
        '1145644718.25jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145644718.25jubutler"]',
        '1145644720.37jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145644720.37jubutler"]',
        '1145644725.87jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644725.87jubutler"]',
        '1145644727.81jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644727.81jubutler"]',
        '1145644729.96jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644729.96jubutler"]',
        '1145644732.2jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145644732.2jubutler"]',
        '1145644734.42jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145644734.42jubutler"]',
        '1145644738.37jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644738.37jubutler"]',
        '1145644740.7jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644740.7jubutler"]',
        '1145644742.56jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644742.56jubutler"]',
        '1145644744.28jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644744.28jubutler"]',
        '1145644747.73jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644747.73jubutler"]',
        '1145644749.65jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644749.65jubutler"]',
        '1145644751.46jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644751.46jubutler"]',
        '1145644753.17jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644753.17jubutler"]',
        '1145644755.23jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644755.23jubutler"]',
        '1145644757.28jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644757.28jubutler"]',
        '1145644768.28jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644768.28jubutler"]',
        '1145644769.93jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644769.93jubutler"]',
        '1145644786.45jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644786.45jubutler"]',
        '1145644791.54jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644791.54jubutler"]',
        '1145644794.87jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644794.87jubutler"]',
        '1145644798.12jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644798.12jubutler"]',
        '1145644801.23jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644801.23jubutler"]',
        '1145644804.93jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644804.93jubutler"]',
        '1145644807.75jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644807.75jubutler"]',
        '1145644820.61jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644820.61jubutler"]',
        '1145644823.76jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644823.76jubutler"]',
        '1145644828.26jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644828.26jubutler"]',
        '1145644831.78jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644831.78jubutler"]',
        '1145644835.54jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644835.54jubutler"]',
        '1145644842.93jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644842.93jubutler"]',
        '1145644861.42jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145644861.42jubutler"]',
        '1145652337.21jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145652337.21jubutler"]',
        '1145652358.58jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145652358.58jubutler"]',
        '1145652361.7jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145652361.7jubutler"]',
        '1145652403.71jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145652403.71jubutler"]',
        '1145652635.43jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145652635.43jubutler"]',
        '1145919878.84jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145919878.84jubutler"]',
        '1145920929.06jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145920929.06jubutler"]',
        '1145920993.09jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145920993.09jubutler"]',
        '1145921024.01jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145921024.01jubutler"]',
        '1145921057.15jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145921057.15jubutler"]',
        '1145921068.83jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145921068.83jubutler"]',
        '1145921147.15jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145921147.15jubutler"]',
        '1145921180.15jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145921180.15jubutler"]',
        '1145921233.39jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145921233.39jubutler"]',
        '1145921264.95jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145921264.95jubutler"]',
        '1145921407.98jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145921407.98jubutler"]',
        '1145930823.5jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145930823.5jubutler"]',
        '1145930831.86jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145930831.86jubutler"]',
        '1145930832.81jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145930832.81jubutler"]',
        '1145930834.79jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145930834.79jubutler"]',
        '1145930835.75jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145930835.75jubutler"]',
        '1145930836.67jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145930836.67jubutler"]',
        '1145930837.61jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145930837.61jubutler"]',
        '1145930838.71jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145930838.71jubutler"]',
        '1145930840.53jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145930840.53jubutler"]',
        '1145930841.65jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145930841.65jubutler"]',
        '1145930844.12jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145930844.12jubutler"]',
        '1145930976.73jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145930976.73jubutler"]',
        '1145930985.83jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145930985.83jubutler"]',
        '1145930998.28jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145930998.28jubutler"]',
        '1145931158.81jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145931158.81jubutler"]',
        '1145931183.31jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145931183.31jubutler"]',
        '1145931236.17jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145931236.17jubutler"]',
        '1145931239.87jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145931239.87jubutler"]',
        '1145931286.9jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145931286.9jubutler"]',
        '1145931323.76jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145931323.76jubutler"]',
        '1145931394.53jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145931394.53jubutler"]',
        '1145931537.46jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145931537.46jubutler"]',
        '1145931583.36jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145931583.36jubutler"]',
        '1145931649.51jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145931649.51jubutler"]',
        '1145931769.37jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145931769.37jubutler"]',
        '1145931836.01jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145931836.01jubutler"]',
        '1145931861.31jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145931861.31jubutler"]',
        '1145931891.58jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1145931891.58jubutler"]',
        '1145932081.18jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932081.18jubutler"]',
        '1145932089.36jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932089.36jubutler"]',
        '1145932094.76jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932094.76jubutler"]',
        '1145932097.84jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932097.84jubutler"]',
        '1145932105.58jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932105.58jubutler"]',
        '1145932108.31jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932108.31jubutler"]',
        '1145932111.84jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932111.84jubutler"]',
        '1145932115.11jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932115.11jubutler"]',
        '1145932264.2jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932264.2jubutler"]',
        '1145932271.86jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932271.86jubutler"]',
        '1145932277.58jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932277.58jubutler"]',
        '1145932280.26jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932280.26jubutler"]',
        '1145932282.76jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932282.76jubutler"]',
        '1145932290.11jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932290.11jubutler"]',
        '1145932293.58jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932293.58jubutler"]',
        '1145932305.95jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932305.95jubutler"]',
        '1145932309.11jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932309.11jubutler"]',
        '1145932315.51jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932315.51jubutler"]',
        '1145932320.64jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932320.64jubutler"]',
        '1145932347.87jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145932347.87jubutler"]',
        '1145938552.21jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145938552.21jubutler"]',
        '1145938845.92jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145938845.92jubutler"]',
        '1145938868.23jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145938868.23jubutler"]',
        '1145938882.87jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145938882.87jubutler"]',
        '1145938898.48jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145938898.48jubutler"]',
        '1145938954.73jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145938954.73jubutler"]',
        '1145938968.59jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145938968.59jubutler"]',
        '1145939021.37jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145939021.37jubutler"]',
        '1145939059.67jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145939059.67jubutler"]',
        '1145939098.46jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145939098.46jubutler"]',
        '1145939105.26jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145939105.26jubutler"]',
        '1145939112.4jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145939112.4jubutler"]',
        '1145939126.04jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145939126.04jubutler"]',
        '1145939134.12jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145939134.12jubutler"]',
        '1145939158.03jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145939158.03jubutler"]',
        '1145939227.86jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145939227.86jubutler"]',
        '1145939355.92jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145939355.92jubutler"]',
        '1145942263.53jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145942263.53jubutler"]',
        '1145942341.11jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145942341.11jubutler"]',
        '1145942350.98jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145942350.98jubutler"]',
        '1145942355.0jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145942355.0jubutler"]',
        '1145942359.21jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145942359.21jubutler"]',
        '1145942364.65jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145942364.65jubutler"]',
        '1145942368.34jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145942368.34jubutler"]',
        '1145942374.51jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145942374.51jubutler"]',
        '1145942411.11jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145942411.11jubutler"]',
        '1145942432.17jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145942432.17jubutler"]',
        '1145942449.33jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145942449.33jubutler"]',
        '1145942455.51jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145942455.51jubutler"]',
        '1145942512.46jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1145942512.46jubutler"]',
        '1146011197.26jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1146011197.26jubutler"]',
        '1146011214.89jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1146011214.89jubutler"]',
        '1146011218.15jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1146011218.15jubutler"]',
        '1146011235.48jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1146011235.48jubutler"]',
        '1146011711.61jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1146011711.61jubutler"]',
        '1146011797.42jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1146011797.42jubutler"]',
        '1146011803.61jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1146011803.61jubutler"]',
        '1146011819.12jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1146011819.12jubutler"]',
        '1146013240.79jubutler':
        '["Objects"]["1135280776.06dzlu"]["Objects"]["1144798398.96jubutler"]["Objects"]["1146013240.79jubutler"]'
    }
}
