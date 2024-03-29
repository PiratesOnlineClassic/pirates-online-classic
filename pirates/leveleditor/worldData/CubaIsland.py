# Embedded file name: pirates.leveleditor.worldData.CubaIsland
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
    'Locator Links':
    [['1161732578.11sdnaik', '1161732370.86sdnaik', 'Bi-directional'],
     ['1161732317.95sdnaik', '1161732370.88sdnaik', 'Bi-directional'],
     ['1161732322.52sdnaik', '1161732705.72sdnaik', 'Bi-directional'],
     ['1161732578.08sdnaik', '1161732705.7sdnaik', 'Bi-directional']],
    'Objects': {
        '1160614528.73sdnaik': {
            'Type': 'Island',
            'Name': 'CubaIsland',
            'File': '',
            'Objects': {
                '1161732317.95sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_exterior_1',
                    'Hpr': VBase3(180.0, 0.0, 0.0),
                    'Pos': Point3(471.383, -559.794, -2.597),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (1.0, 1.0, 1.0, 1.0)
                    }
                },
                '1161732322.52sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_exterior_2',
                    'Hpr': VBase3(-101.237, 0.0, 0.0),
                    'Pos': Point3(107.301, -127.258, 0.205),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1161732370.84sdnaik': {
                    'Type': 'Connector Tunnel',
                    'File': '',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {
                        '1161732370.86sdnaik': {
                            'Type': 'Locator Node',
                            'Name': 'portal_connector_1',
                            'GridPos': Point3(1127.779, -170.628, 33.329),
                            'Hpr': VBase3(-88.748, 0.0, 0.0),
                            'Pos': Point3(-3.613, 0.304, 4.651),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1161732370.88sdnaik': {
                            'Type': 'Locator Node',
                            'Name': 'portal_connector_2',
                            'GridPos': Point3(1061.428, -327.097, 32.474),
                            'Hpr': VBase3(72.65, -1.426, -0.516),
                            'Pos': Point3(-103.188, 135.024, 3.777),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(95.277, -622.544, 241.267),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/tunnels/tunnel_swamp'
                    }
                },
                '1161732578.06sdnaik': {
                    'Type': 'Island Game Area',
                    'File': 'cuba_area_swamp_1',
                    'Hpr': VBase3(83.644, 0.105, -0.94),
                    'Objects': {
                        '1161732578.08sdnaik': {
                            'Type': 'Locator Node',
                            'Name': 'portal_interior_1',
                            'GridPos': Point3(1533.649, 436.867, 94.327),
                            'Hpr': VBase3(-177.386, -0.684, -0.017),
                            'Pos': Point3(400.751, 192.485, 6.419),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1161732578.11sdnaik': {
                            'Type': 'Locator Node',
                            'Name': 'portal_interior_2',
                            'GridPos': Point3(900.096, 220.241, 102.291),
                            'Hpr': VBase3(2.192, 0.683, 0.039),
                            'Pos': Point3(-232.802, -24.141, 14.383),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(1132.898, 244.382, 597.635),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/swamps/swampA'
                    }
                },
                '1161732705.67sdnaik': {
                    'Type': 'Connector Tunnel',
                    'File': '',
                    'Hpr': VBase3(-47.944, -3.89, 3.503),
                    'Objects': {
                        '1161732705.72sdnaik': {
                            'Type': 'Locator Node',
                            'Name': 'portal_connector_2',
                            'GridPos': Point3(708.83, 396.283, 89.205),
                            'Hpr': VBase3(72.65, -1.426, -0.516),
                            'Pos': Point3(-103.188, 135.024, 3.777),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1161732705.7sdnaik': {
                            'Type': 'Locator Node',
                            'Name': 'portal_connector_1',
                            'GridPos': Point3(775.181, 552.752, 90.061),
                            'Hpr': VBase3(-88.748, 0.0, 0.0),
                            'Pos': Point3(-3.613, 0.304, 4.651),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-163.185, 26.795, 316.996),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/tunnels/tunnel_swamp'
                    }
                },
                '1162496104.57dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-121.98, 5.318, 2.905),
                    'Pos': Point3(194.391, -145.836, 1.786),
                    'Scale': VBase3(1.14, 1.14, 1.14),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162496561.59dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-174.43, 3.494, 3.134),
                    'Pos': Point3(248.807, -187.757, -1.425),
                    'Scale': VBase3(1.749, 1.749, 1.749),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.5699999928474426,
                                  0.5600000023841858, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162496585.79dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(102.954, -3.649, 0.624),
                    'Pos': Point3(228.148, -194.805, -0.104),
                    'Scale': VBase3(1.749, 1.749, 1.749),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162496638.89dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-178.512, 0.068, -5.979),
                    'Pos': Point3(221.706, -161.475, -3.687),
                    'Scale': VBase3(1.212, 1.212, 1.212),
                    'Visual': {
                        'Color': (0.800000011920929, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162496693.54dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-81.75, 5.236, 2.288),
                    'Pos': Point3(306.624, -244.912, 2.29),
                    'Scale': VBase3(1.846, 1.846, 1.846),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162496757.15dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-162.582, -1.433, 5.53),
                    'Pos': Point3(288.119, -213.242, 5.442),
                    'Scale': VBase3(1.846, 1.846, 1.846),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162496818.98dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-95.42, 2.604, -0.358),
                    'Pos': Point3(262.002, -197.86, -1.237),
                    'Scale': VBase3(1.813, 1.813, 1.813),
                    'Visual': {
                        'Color': (0.800000011920929, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162496857.71dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-49.89, 1.57, -2.109),
                    'Pos': Point3(290.286, -233.631, 1.056),
                    'Scale': VBase3(1.685, 1.685, 1.685),
                    'Visual': {
                        'Color': (0.800000011920929, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162496880.34dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-49.89, 1.57, -2.109),
                    'Pos': Point3(203.311, -212.777, 2.077),
                    'Scale': VBase3(1.685, 1.685, 1.685),
                    'Visual': {
                        'Color': (0.800000011920929, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162496889.81dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-132.466, 2.295, 1.283),
                    'Pos': Point3(159.066, -132.814, 2.534),
                    'Scale': VBase3(1.685, 1.685, 1.685),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.5699999928474426,
                                  0.5600000023841858, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162496999.35dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-76.632, 2.351, -1.177),
                    'Pos': Point3(185.402, -156.567, -1.333),
                    'Scale': VBase3(1.181, 1.181, 1.181),
                    'Visual': {
                        'Color': (0.8, 0.87, 1.0, 1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162497015.78dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(175.664, -2.875, 4.677),
                    'Pos': Point3(132.299, -158.771, 0.088),
                    'Scale': VBase3(1.181, 1.181, 1.181),
                    'Visual': {
                        'Color': (0.8, 0.87, 1.0, 1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162497038.53dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-93.151, 1.894, 1.69),
                    'Pos': Point3(174.318, -174.436, -2.428),
                    'Scale': VBase3(1.477, 1.477, 1.477),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162497249.64dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-27.472, 2.32, -1.029),
                    'Pos': Point3(61.752, -128.37, 0.0),
                    'Scale': VBase3(2.466, 2.466, 2.466),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162497329.21dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-55.834, 1.221, 0.0),
                    'Pos': Point3(86.467, -131.751, -2.015),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_a'
                    }
                },
                '1162497460.96dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(158.083, -7.978, -0.962),
                    'Pos': Point3(28.162, -66.255, -8.54),
                    'Scale': VBase3(2.788, 2.788, 2.788),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162497568.12dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(16.872, -119.363, -2.0),
                    'Scale': VBase3(0.895, 0.895, 0.895),
                    'Visual': {
                        'Color': (1.0, 0.9900000095367432, 1.0, 1.0),
                        'Model': 'models/vegetation/swamp_tree_a'
                    }
                },
                '1162497591.24dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-27.12, 0.0, 0.0),
                    'Pos': Point3(-9.666, -73.007, -2.0),
                    'Scale': VBase3(0.872, 0.872, 0.872),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_b'
                    }
                },
                '1162497648.96dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-96.431, -90.501, -2.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.8500000238418579, 0.8199999928474426,
                                  0.7300000190734863, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_thin'
                    }
                },
                '1162497681.26dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-6.462, -124.144, -2.0),
                    'Scale': VBase3(1.172, 1.172, 1.172),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.5699999928474426,
                                  0.5600000023841858, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_thin'
                    }
                },
                '1162497693.48dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(11.047, -132.343, 1.061),
                    'Scale': VBase3(1.172, 1.172, 1.172),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_thin'
                    }
                },
                '1162497709.17dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-7.714, -131.882, -4.475),
                    'Scale': VBase3(1.018, 1.018, 1.018),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.5699999928474426,
                                  0.5600000023841858, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_thin'
                    }
                },
                '1162498231.46dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(92.824, 1.752, 1.371),
                    'Pos': Point3(289.328, -322.038, -1.973),
                    'Scale': VBase3(2.391, 2.391, 2.391),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162498233.67dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-81.75, 5.236, 2.288),
                    'Pos': Point3(311.02, -330.127, -2.0),
                    'Scale': VBase3(1.846, 1.846, 1.846),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162498236.93dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-81.75, 5.236, 2.288),
                    'Pos': Point3(291.992, -284.872, -2.0),
                    'Scale': VBase3(1.846, 1.846, 1.846),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162498256.79dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-175.195, -2.608, 5.084),
                    'Pos': Point3(351.684, -338.435, 6.714),
                    'Scale': VBase3(2.484, 2.484, 2.484),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162498287.12dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-55.834, 0.0, 0.0),
                    'Pos': Point3(330.397, -323.928, -2.0),
                    'Scale': VBase3(0.868, 0.868, 0.868),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_a'
                    }
                },
                '1162498321.2dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-163.404, -2.394, 1.296),
                    'Pos': Point3(-105.028, -386.378, -0.932),
                    'Scale': VBase3(1.729, 1.729, 1.729),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162498369.29dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-156.824, -2.23, 1.562),
                    'Pos': Point3(-39.408, -430.211, -4.527),
                    'Scale': VBase3(1.942, 1.942, 1.942),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162498390.34dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(56.286, 1.014, -2.526),
                    'Pos': Point3(-12.316, -534.81, -2.0),
                    'Scale': VBase3(2.072, 2.072, 2.072),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162498400.56dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-138.604, -1.63, 4.472),
                    'Pos': Point3(-6.568, -563.456, -2.0),
                    'Scale': VBase3(1.924, 1.924, 1.924),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162498416.74dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-115.464, 0.262, -0.36),
                    'Pos': Point3(-32.335, -543.622, 0.636),
                    'Scale': VBase3(2.21, 2.21, 2.21),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162498428.64dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(177.628, -4.27, 2.103),
                    'Pos': Point3(-37.621, -560.769, 0.288),
                    'Scale': VBase3(1.591, 1.591, 1.591),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162498500.51dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-125.283, -101.993, -2.0),
                    'Scale': VBase3(0.779, 0.779, 0.779),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_a'
                    }
                },
                '1162498514.14dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-96.751, 0.0, 0.0),
                    'Pos': Point3(-133.251, -114.765, -2.0),
                    'Scale': VBase3(0.7, 0.7, 0.7),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.5699999928474426,
                                  0.5600000023841858, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_a'
                    }
                },
                '1162498585.56dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-131.038, -155.049, -2.0),
                    'Scale': VBase3(1.276, 1.276, 1.276),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162498611.99dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-95.057, 0.0, 0.0),
                    'Pos': Point3(-122.674, -137.024, 3.248),
                    'Scale': VBase3(1.372, 1.372, 1.372),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162498633.87dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-89.806, -151.497, -2.0),
                    'Scale': VBase3(0.745, 0.745, 0.745),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_a'
                    }
                },
                '1162498653.28dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-106.137, -96.349, -1.129),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.5699999928474426,
                                  0.5600000023841858, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_thin'
                    }
                },
                '1162501202.2dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-58.658, 0.0, 0.0),
                    'Pos': Point3(-257.241, -565.015, 15.245),
                    'Scale': VBase3(1.692, 1.692, 1.692),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.5699999928474426,
                                  0.5600000023841858, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501211.4dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-290.342, -852.048, 8.106),
                    'Scale': VBase3(1.364, 1.364, 1.364),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501216.51dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-283.447, -583.547, 20.569),
                    'Scale': VBase3(1.364, 1.364, 1.364),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501218.89dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-276.987, -1036.227, -2.0),
                    'Scale': VBase3(1.364, 1.364, 1.364),
                    'Visual': {
                        'Color': (0.72, 0.79, 0.788235294117647, 1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501221.32dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(86.035, 0.0, 0.0),
                    'Pos': Point3(-247.343, -951.268, -1.225),
                    'Scale': VBase3(1.364, 1.364, 1.364),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501223.18dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(31.708, -1.565, -0.47),
                    'Pos': Point3(-279.114, -872.037, 2.431),
                    'Scale': VBase3(1.278, 1.278, 1.278),
                    'Visual': {
                        'Color': (0.75, 0.75, 0.7529411764705882, 1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501264.03dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(174.015, -1.384, -1.516),
                    'Pos': Point3(-275.049, -895.262, 2.226),
                    'Scale': VBase3(1.324, 1.324, 1.324),
                    'Visual': {
                        'Color': (0.699999988079071, 0.7300000190734863,
                                  0.5799999833106995, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501292.92dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(2.058, 1.989, 3.485),
                    'Pos': Point3(-269.343, -916.458, 2.4),
                    'Scale': VBase3(1.845, 1.845, 1.845),
                    'Visual': {
                        'Color': (0.71, 0.82, 0.7019607843137254, 1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501329.71dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-95.508, -3.718, 1.51),
                    'Pos': Point3(-269.887, -984.059, -1.318),
                    'Scale': VBase3(1.431, 1.431, 1.431),
                    'Visual': {
                        'Color': (0.78, 0.77, 0.5058823529411764, 1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501346.57dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(86.721, 3.656, -1.653),
                    'Pos': Point3(-23.837, -466.188, -7.102),
                    'Scale': VBase3(1.546, 1.546, 1.546),
                    'Visual': {
                        'Color': (0.75, 0.98, 1.0, 1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501361.39dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-103.846, -3.897, 0.955),
                    'Pos': Point3(-217.634, -540.937, 18.079),
                    'Scale': VBase3(1.479, 1.479, 1.479),
                    'Visual': {
                        'Color': (0.800000011920929, 0.8700000047683716, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501378.34dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-96.283, -3.737, 1.459),
                    'Pos': Point3(-357.62, -161.217, -2.0),
                    'Scale': VBase3(1.624, 1.624, 1.624),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501380.67dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-96.283, -3.737, 1.459),
                    'Pos': Point3(-357.62, -161.217, -2.0),
                    'Scale': VBase3(1.624, 1.624, 1.624),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501506.98dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-61.432, -3.526, 1.918),
                    'Pos': Point3(-230.972, -1023.899, -2.592),
                    'Scale': VBase3(1.479, 1.479, 1.479),
                    'Visual': {
                        'Color': (0.62, 0.72, 0.7568627450980392, 1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501515.84dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(88.974, 3.588, -1.795),
                    'Pos': Point3(-290.512, -1072.11, -8.037),
                    'Scale': VBase3(1.479, 1.479, 1.479),
                    'Visual': {
                        'Color': (1.0, 0.9900000095367432, 1.0, 1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501551.93dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(28.831, 3.346, 2.215),
                    'Pos': Point3(-274.776, -943.157, 1.978),
                    'Scale': VBase3(1.479, 1.479, 1.479),
                    'Visual': {
                        'Color': (0.87, 0.87, 0.6196078431372549, 1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501577.87dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(13.203, -3.603, 3.052),
                    'Pos': Point3(-164.497, -476.962, 8.161),
                    'Scale': VBase3(1.489, 1.489, 1.489),
                    'Visual': {
                        'Color': (1.0, 0.9900000095367432, 1.0, 1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501603.15dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-59.997, -3.967, -2.561),
                    'Pos': Point3(-188.222, -504.262, 14.045),
                    'Scale': VBase3(1.275, 1.275, 1.275),
                    'Visual': {
                        'Color': (1.0, 0.9900000095367432, 1.0, 1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162501641.98dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-90.357, -94.791, -2.0),
                    'Scale': VBase3(0.86, 0.86, 0.86),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_thin'
                    }
                },
                '1162501646.46dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-48.359, -71.927, -2.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_thin'
                    }
                },
                '1162501650.07dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-38.622, 0.0, 0.0),
                    'Pos': Point3(-46.673, -61.255, -2.0),
                    'Scale': VBase3(0.93, 0.93, 0.93),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_thin'
                    }
                },
                '1162501671.89dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-6.162, 0.0, 0.0),
                    'Pos': Point3(-109.827, -75.473, -1.193),
                    'Scale': VBase3(0.563, 0.563, 0.563),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_a'
                    }
                },
                '1162501689.73dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-33.613, 0.0, 0.0),
                    'Pos': Point3(-44.023, -93.572, -2.0),
                    'Scale': VBase3(0.605, 0.605, 0.605),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.5699999928474426,
                                  0.5600000023841858, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_a'
                    }
                },
                '1162501722.73dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-140.898, 0.105, 1.216),
                    'Pos': Point3(-40.76, -76.109, -2.0),
                    'Scale': VBase3(0.822, 0.822, 0.822),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_a'
                    }
                },
                '1162501750.34dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-32.019, 0.0, 0.0),
                    'Pos': Point3(-117.391, -205.372, -2.0),
                    'Scale': VBase3(0.745, 0.745, 0.745),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/vegetation/swamp_tree_a'
                    }
                },
                '1162501776.62dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-13.269, 0.0, 0.0),
                    'Pos': Point3(-72.482, -272.37, -2.0),
                    'Scale': VBase3(0.745, 0.745, 0.745),
                    'Visual': {
                        'Color': (0.800000011920929, 0.800000011920929,
                                  0.800000011920929, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_a'
                    }
                },
                '1162501796.43dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-13.269, 0.0, 0.0),
                    'Pos': Point3(56.456, -177.916, 0.0),
                    'Scale': VBase3(0.745, 0.745, 0.745),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_a'
                    }
                },
                '1162501799.67dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-13.269, 0.0, 0.0),
                    'Pos': Point3(-49.421, -254.503, -2.0),
                    'Scale': VBase3(0.745, 0.745, 0.745),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_a'
                    }
                },
                '1162501880.84dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-55.834, 1.221, 0.0),
                    'Pos': Point3(64.544, -147.513, -2.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_a'
                    }
                },
                '1162502780.21dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-56.618, 0.0, 0.0),
                    'Pos': Point3(238.848, -441.555, 0.0),
                    'Scale': VBase3(0.868, 0.868, 0.868),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_a'
                    }
                },
                '1162504044.29dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(80.734, -0.123, -2.72),
                    'Pos': Point3(-119.407, -428.205, 0.956),
                    'Scale': VBase3(1.729, 1.729, 1.729),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504062.54dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-18.895, 2.702, 0.334),
                    'Pos': Point3(-141.666, -446.35, 7.427),
                    'Scale': VBase3(1.488, 1.488, 1.488),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504090.14dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-13.269, 0.0, 0.0),
                    'Pos': Point3(-67.554, -342.621, -2.0),
                    'Scale': VBase3(0.745, 0.745, 0.745),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_a'
                    }
                },
                '1162504101.34dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-13.269, 0.0, 0.0),
                    'Pos': Point3(-71.952, -260.648, -2.0),
                    'Scale': VBase3(0.745, 0.745, 0.745),
                    'Visual': {
                        'Color': (0.7900000214576721, 0.6499999761581421,
                                  0.5299999713897705, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_a'
                    }
                },
                '1162504103.39dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-13.269, 0.0, 0.0),
                    'Pos': Point3(-83.681, -350.664, -2.0),
                    'Scale': VBase3(0.641, 0.641, 0.641),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.5699999928474426,
                                  0.5600000023841858, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_a'
                    }
                },
                '1162504362.84dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-55.834, 1.221, 0.0),
                    'Pos': Point3(109.058, -288.79, -2.0),
                    'Scale': VBase3(0.877, 0.877, 0.877),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_a'
                    }
                },
                '1162504374.53dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-134.441, 0.241, 1.197),
                    'Pos': Point3(-57.046, -228.005, 0.0),
                    'Scale': VBase3(0.804, 0.804, 0.804),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_a'
                    }
                },
                '1162504384.23dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-142.166, 0.095, 1.217),
                    'Pos': Point3(227.3, -465.162, 0.0),
                    'Scale': VBase3(0.804, 0.804, 0.804),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_a'
                    }
                },
                '1162504406.53dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-145.594, 0.251, 5.707),
                    'Pos': Point3(185.073, -205.108, -2.0),
                    'Scale': VBase3(2.21, 2.21, 2.21),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504452.48dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(175.153, -3.425, 4.575),
                    'Pos': Point3(-107.083, -370.161, -3.838),
                    'Scale': VBase3(2.408, 2.408, 2.408),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504463.24dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(55.708, -2.313, -5.225),
                    'Pos': Point3(-36.583, -340.483, -2.0),
                    'Scale': VBase3(2.228, 2.228, 2.228),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504470.51dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(55.708, -2.313, -5.225),
                    'Pos': Point3(-108.99, -412.732, -0.098),
                    'Scale': VBase3(2.012, 2.012, 2.012),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504493.21dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-115.124, 3.117, 4.789),
                    'Pos': Point3(-112.092, -484.478, -9.504),
                    'Scale': VBase3(2.128, 2.128, 2.128),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504510.79dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-111.991, 3.374, 4.612),
                    'Pos': Point3(375.199, -363.599, -2.0),
                    'Scale': VBase3(2.128, 2.128, 2.128),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504512.71dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-111.991, 3.374, 4.612),
                    'Pos': Point3(379.228, -395.531, -2.0),
                    'Scale': VBase3(2.128, 2.128, 2.128),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504513.99dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-111.991, 3.374, 4.612),
                    'Pos': Point3(344.415, -416.725, -3.103),
                    'Scale': VBase3(2.128, 2.128, 2.128),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504515.7dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-111.991, 3.374, 4.612),
                    'Pos': Point3(392.737, -486.368, -2.0),
                    'Scale': VBase3(2.128, 2.128, 2.128),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504517.18dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-111.991, 3.374, 4.612),
                    'Pos': Point3(408.232, -487.761, -2.0),
                    'Scale': VBase3(2.128, 2.128, 2.128),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504518.45dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-156.061, -0.793, 5.657),
                    'Pos': Point3(420.874, -500.259, -2.0),
                    'Scale': VBase3(1.819, 1.819, 1.819),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504520.09dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-111.991, 3.374, 4.612),
                    'Pos': Point3(457.577, -504.001, -2.0),
                    'Scale': VBase3(2.128, 2.128, 2.128),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504563.18dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-174.648, -2.559, 5.108),
                    'Pos': Point3(380.532, -434.393, -1.918),
                    'Scale': VBase3(1.819, 1.819, 1.819),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504565.28dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(161.081, -4.434, 3.606),
                    'Pos': Point3(376.171, -469.964, -2.0),
                    'Scale': VBase3(2.094, 2.094, 2.094),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504579.32dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(161.081, -4.434, 3.606),
                    'Pos': Point3(412.314, -435.24, -2.0),
                    'Scale': VBase3(2.094, 2.094, 2.094),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.5699999928474426,
                                  0.5600000023841858, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504581.82dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(161.081, -4.434, 3.606),
                    'Pos': Point3(470.863, -525.388, -2.0),
                    'Scale': VBase3(2.094, 2.094, 2.094),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504589.29dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(161.081, -4.434, 3.606),
                    'Pos': Point3(507.166, -510.536, -2.0),
                    'Scale': VBase3(2.094, 2.094, 2.094),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504613.95dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(53.269, 0.0, 0.0),
                    'Pos': Point3(473.617, -539.435, -0.625),
                    'Scale': VBase3(0.868, 0.868, 0.868),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_a'
                    }
                },
                '1162504615.65dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-55.834, 0.0, 0.0),
                    'Pos': Point3(470.252, -579.967, -2.0),
                    'Scale': VBase3(0.868, 0.868, 0.868),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_a'
                    }
                },
                '1162504622.87dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-111.991, 3.374, 4.612),
                    'Pos': Point3(460.295, -590.002, 0.0),
                    'Scale': VBase3(1.417, 1.417, 1.417),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504625.28dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-148.266, -6.577, -3.666),
                    'Pos': Point3(442.589, -600.058, 0.0),
                    'Scale': VBase3(2.128, 2.128, 2.128),
                    'Visual': {
                        'Color': (0.8500000238418579, 0.8199999928474426,
                                  0.7300000190734863, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504626.54dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-111.991, 3.374, 4.612),
                    'Pos': Point3(464.441, -643.422, -2.0),
                    'Scale': VBase3(2.128, 2.128, 2.128),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504628.01dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-111.991, 3.374, 4.612),
                    'Pos': Point3(513.888, -652.936, -2.0),
                    'Scale': VBase3(2.128, 2.128, 2.128),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.5699999928474426,
                                  0.5600000023841858, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504629.42dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-111.991, 3.374, 4.612),
                    'Pos': Point3(493.592, -653.513, -2.0),
                    'Scale': VBase3(2.128, 2.128, 2.128),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504630.82dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-111.991, 3.374, 4.612),
                    'Pos': Point3(545.894, -678.517, -2.0),
                    'Scale': VBase3(2.128, 2.128, 2.128),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504635.54dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-55.834, 0.0, 0.0),
                    'Pos': Point3(471.228, -729.263, -2.0),
                    'Scale': VBase3(0.868, 0.868, 0.868),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_a'
                    }
                },
                '1162504651.18dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-55.834, 0.0, 0.0),
                    'Pos': Point3(-131.543, -219.835, -2.0),
                    'Scale': VBase3(0.868, 0.868, 0.868),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_a'
                    }
                },
                '1162504683.95dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-130.455, 16.842, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.5699999928474426,
                                  0.5600000023841858, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_thin'
                    }
                },
                '1162504691.23dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-126.7, -27.748, -2.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_thin'
                    }
                },
                '1162504697.12dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-76.974, 58.572, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.5699999928474426,
                                  0.5600000023841858, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_thin'
                    }
                },
                '1162504701.23dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-44.268, 51.753, -2.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_thin'
                    }
                },
                '1162504709.56dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-45.704, 57.451, -2.0),
                    'Scale': VBase3(0.546, 0.546, 0.546),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_a'
                    }
                },
                '1162504732.4dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-156.623, -31.079, -2.0),
                    'Scale': VBase3(0.546, 0.546, 0.546),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_a'
                    }
                },
                '1162504754.37dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-76.495, -286.104, -2.0),
                    'Scale': VBase3(0.546, 0.546, 0.546),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_a'
                    }
                },
                '1162504802.04dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-25.52, 27.068, -2.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504808.48dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-141.043, 0.0, 0.0),
                    'Pos': Point3(-21.642, 11.532, -2.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162504824.68dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-31.21, 4.01, -2.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_thin'
                    }
                },
                '1162505050.93dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(190.77, -487.635, -1.37),
                    'Scale': VBase3(1.454, 1.454, 1.454),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162505128.43dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(69.079, 0.0, 0.0),
                    'Pos': Point3(191.501, -487.204, -0.256),
                    'Scale': VBase3(1.114, 1.114, 1.114),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162505210.81dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(43.056, 0.0, 0.0),
                    'Pos': Point3(191.159, -481.078, -1.405),
                    'Scale': VBase3(0.935, 0.935, 0.935),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162505214.28dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(46.454, 0.0, 0.0),
                    'Pos': Point3(190.649, -479.107, -0.431),
                    'Scale': VBase3(0.893, 0.893, 0.893),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162505293.49dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-10.798, 0.0, 0.0),
                    'Pos': Point3(191.62, -486.729, -0.14),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162505296.51dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(46.454, 0.0, 0.0),
                    'Pos': Point3(190.472, -488.612, -0.203),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162505308.45dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(46.454, 0.0, 0.0),
                    'Pos': Point3(185.497, -478.535, -2.29),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162505330.64dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(46.454, 0.0, 0.0),
                    'Pos': Point3(294.657, -542.887, -0.842),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162505333.48dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(46.454, 0.0, 0.0),
                    'Pos': Point3(300.606, -545.852, -0.915),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162575738.25dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(92.147, 5.514, -7.297),
                    'Pos': Point3(-203.283, -515.135, 5.177),
                    'Scale': VBase3(1.794, 1.794, 1.794),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162575755.71dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(148.307, 4.157, -19.181),
                    'Pos': Point3(-249.184, -557.096, 12.971),
                    'Scale': VBase3(2.029, 2.029, 2.029),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162575900.62dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-17.49, 0.0, 0.0),
                    'Pos': Point3(-324.384, -1095.936, -3.407),
                    'Scale': VBase3(1.811, 1.811, 1.811),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162576043.68dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, -3.114),
                    'Pos': Point3(121.584, -137.254, -2.913),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.5699999928474426,
                                  0.5600000023841858, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_a'
                    }
                },
                '1162576078.71dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(145.113, -134.736, 0.0),
                    'Scale': VBase3(0.525, 0.525, 0.525),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_b'
                    }
                },
                '1162576335.14dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(315.575, -271.262, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162576483.87dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(301.403, -323.476, 0.0),
                    'Scale': VBase3(1.869, 1.869, 1.869),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162576530.06dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(482.967, -204.012, 0.0),
                    'Scale': VBase3(1.869, 1.869, 1.869),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162576533.54dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(290.001, -326.597, -4.449),
                    'Scale': VBase3(1.869, 1.869, 1.869),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162576597.46dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(324.318, -253.808, 54.758),
                    'Scale': VBase3(1.869, 1.869, 1.869),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162576602.98dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(277.52, -268.28, -3.084),
                    'Scale': VBase3(1.869, 1.869, 1.869),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162576619.82dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, -3.866, 0.0),
                    'Pos': Point3(354.38, -394.409, -4.883),
                    'Scale': VBase3(1.869, 1.869, 1.869),
                    'Visual': {
                        'Color': (0.800000011920929, 0.6000000238418579, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162576649.89dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, -3.866, 0.0),
                    'Pos': Point3(349.251, -444.049, 5.853),
                    'Scale': VBase3(1.869, 1.869, 1.869),
                    'Visual': {
                        'Color': (0.75, 0.9300000071525574, 1.0, 1.0),
                        'Model': 'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162576682.79dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 3.651, 3.614),
                    'Pos': Point3(386.805, -407.068, -26.618),
                    'Scale': VBase3(1.869, 1.869, 1.869),
                    'Visual': {
                        'Color': (0.800000011920929, 0.6000000238418579, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162576722.81dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(79.561, 4.221, -2.928),
                    'Pos': Point3(363.335, -465.418, -1.41),
                    'Scale': VBase3(1.34, 1.34, 1.34),
                    'Visual': {
                        'Color': (0.800000011920929, 0.6000000238418579, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162576805.98dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, -1.758, 0.0),
                    'Pos': Point3(-86.915, -90.111, -2.123),
                    'Scale': VBase3(0.797, 0.797, 0.797),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.5699999928474426,
                                  0.5600000023841858, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_canopy'
                    }
                },
                '1162576816.26dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-108.078, -105.697, -62.869),
                    'Scale': VBase3(0.936, 0.936, 0.936),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_canopy'
                    }
                },
                '1162576895.73dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.06, 0.0),
                    'Pos': Point3(-41.678, -102.308, -8.363),
                    'Scale': VBase3(0.736, 0.736, 0.736),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_canopy'
                    }
                },
                '1162576950.03dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, -1.758, 0.0),
                    'Pos': Point3(-116.174, -26.237, -3.135),
                    'Scale': VBase3(0.643, 0.643, 0.643),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_canopy'
                    }
                },
                '1162576969.61dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-24.171, -1.604, -0.72),
                    'Pos': Point3(-29.692, 31.725, 0.102),
                    'Scale': VBase3(0.643, 0.643, 0.643),
                    'Visual': {
                        'Color': (0.75, 0.9300000071525574, 1.0, 1.0),
                        'Model': 'models/vegetation/swamp_tree_canopy'
                    }
                },
                '1162576986.5dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-24.171, -1.604, -0.72),
                    'Pos': Point3(-182.008, 71.806, -63.602),
                    'Scale': VBase3(0.643, 0.643, 0.643),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_canopy'
                    }
                },
                '1162576998.25dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-24.171, -1.604, -0.72),
                    'Pos': Point3(-181.717, 29.795, -70.83),
                    'Scale': VBase3(0.643, 0.643, 0.643),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_canopy'
                    }
                },
                '1162577044.42dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-41.182, -1.323, -1.157),
                    'Pos': Point3(-82.963, -195.76, 0.0),
                    'Scale': VBase3(0.732, 0.732, 0.732),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.5699999928474426,
                                  0.5600000023841858, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_canopy'
                    }
                },
                '1162577094.82dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-39.645, -240.447, -20.215),
                    'Scale': VBase3(0.956, 0.956, 0.956),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_canopy'
                    }
                },
                '1162577152.48dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-8.806, -279.214, -36.906),
                    'Scale': VBase3(0.854, 0.854, 0.854),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_canopy'
                    }
                },
                '1162577320.84dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(108.215, 5.123, -3.235),
                    'Pos': Point3(449.692, -619.545, -0.489),
                    'Scale': VBase3(1.84, 1.84, 1.84),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162577355.15dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(437.004, -609.408, 20.708),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162577566.42dzlu': {
                    'Type': 'Swamp_props_small',
                    'DisableCollision': False,
                    'Hpr': VBase3(-158.68, 0.0, 0.0),
                    'Pos': Point3(379.469, -503.431, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/swamp_boat'
                    }
                },
                '1162577813.76dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(285.231, -543.089, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162577835.12dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(283.706, -542.153, -0.659),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162577839.92dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(286.137, -546.313, -1.246),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162577843.75dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(276.088, -544.595, -0.828),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162577867.18dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(370.702, -485.211, 0.0),
                    'Scale': VBase3(2.209, 2.209, 2.209),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162577870.71dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(367.014, -487.09, -2.071),
                    'Scale': VBase3(1.998, 1.998, 1.998),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162577884.96dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(370.107, -479.469, 0.0),
                    'Scale': VBase3(2.209, 2.209, 2.209),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162577982.15dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(276.339, -548.121, -1.189),
                    'Scale': VBase3(1.583, 1.583, 1.583),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162577996.29dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-72.138, -11.409, 0.0),
                    'Pos': Point3(280.375, -555.086, -1.704),
                    'Scale': VBase3(1.583, 1.583, 1.583),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578006.14dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-40.563, 0.0, 0.0),
                    'Pos': Point3(276.393, -550.524, 0.0),
                    'Scale': VBase3(1.399, 1.399, 1.399),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578016.5dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-40.563, 0.0, 0.0),
                    'Pos': Point3(292.14, -570.623, -1.631),
                    'Scale': VBase3(1.399, 1.399, 1.399),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578019.04dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-40.563, 0.0, 0.0),
                    'Pos': Point3(294.999, -577.17, -0.541),
                    'Scale': VBase3(1.399, 1.399, 1.399),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578024.62dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-40.563, 0.0, 0.0),
                    'Pos': Point3(320.253, -629.48, 0.0),
                    'Scale': VBase3(1.399, 1.399, 1.399),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578025.75dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-40.563, 0.0, 0.0),
                    'Pos': Point3(323.649, -628.406, -1.866),
                    'Scale': VBase3(1.399, 1.399, 1.399),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578026.78dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-30.189, 0.0, 0.0),
                    'Pos': Point3(321.532, -628.769, -1.643),
                    'Scale': VBase3(2.112, 2.112, 2.112),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578038.0dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-38.112, 0.0, -13.852),
                    'Pos': Point3(316.948, -625.273, -1.35),
                    'Scale': VBase3(1.198, 1.198, 1.198),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578047.75dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-125.812, 0.0, 0.0),
                    'Pos': Point3(311.178, -627.427, -1.526),
                    'Scale': VBase3(1.198, 1.198, 1.198),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578056.12dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-38.112, 0.0, 0.0),
                    'Pos': Point3(309.187, -573.984, -1.051),
                    'Scale': VBase3(1.198, 1.198, 1.198),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578057.4dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-38.112, 0.0, 0.0),
                    'Pos': Point3(309.738, -573.679, -0.606),
                    'Scale': VBase3(1.198, 1.198, 1.198),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578070.86dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-38.112, 0.0, 0.0),
                    'Pos': Point3(283.348, -383.938, -1.192),
                    'Scale': VBase3(1.198, 1.198, 1.198),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578075.4dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-38.112, 0.0, 0.0),
                    'Pos': Point3(282.696, -382.364, -0.641),
                    'Scale': VBase3(1.198, 1.198, 1.198),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578081.51dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-40.563, 0.0, 0.0),
                    'Pos': Point3(332.729, -462.495, -1.052),
                    'Scale': VBase3(1.399, 1.399, 1.399),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578094.39dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-40.563, 0.0, 0.0),
                    'Pos': Point3(334.295, -461.528, -0.914),
                    'Scale': VBase3(1.399, 1.399, 1.399),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578096.17dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-106.705, 0.0, 0.0),
                    'Pos': Point3(333.465, -465.382, -0.852),
                    'Scale': VBase3(1.399, 1.399, 1.399),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578108.39dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-61.921, 0.0, 0.0),
                    'Pos': Point3(340.54, -464.982, -1.988),
                    'Scale': VBase3(1.931, 1.931, 1.506),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578113.9dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-124.097, 0.0, 0.0),
                    'Pos': Point3(331.864, -453.649, -1.143),
                    'Scale': VBase3(1.199, 1.199, 1.166),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578121.26dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-124.097, 0.0, 0.0),
                    'Pos': Point3(284.828, -383.294, 0.0),
                    'Scale': VBase3(1.152, 1.152, 1.152),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578126.61dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-74.895, 0.0, 0.0),
                    'Pos': Point3(289.473, -386.795, -1.012),
                    'Scale': VBase3(1.152, 1.152, 1.152),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162578259.32dzlu': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': VBase3(164.725, 1.618, -0.376),
                    'Pos': Point3(437.692, -501.002, -4.014),
                    'Scale': VBase3(3.887, 3.887, 3.887),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/props/rock_group_4_sphere'
                    }
                },
                '1162578426.64dzlu': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': VBase3(128.086, 0.0, 0.0),
                    'Pos': Point3(478.996, -632.527, -0.866),
                    'Scale': VBase3(1.523, 1.523, 1.523),
                    'Visual': {
                        'Color': (0.45, 0.54, 0.82, 1.0),
                        'Model': 'models/props/zz_dont_use_rocks_Dk_group_2F'
                    }
                },
                '1162578793.03dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-78.746, 3.272, 3.365),
                    'Pos': Point3(510.015, -662.867, -2.009),
                    'Scale': VBase3(2.049, 2.049, 2.049),
                    'Visual': {
                        'Color': (0.7900000214576721, 0.6499999761581421,
                                  0.5299999713897705, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162578861.75dzlu': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-11.629, -3.641, -0.749),
                    'Pos': Point3(525.404, -675.711, -0.473),
                    'Scale': VBase3(2.523, 2.523, 2.523),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/props/rock_group_2_sphere'
                    }
                },
                '1162578920.61dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(479.384, -666.297, 21.059),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162578961.18dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(541.198, -708.802, 27.942),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162578998.36dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-28.111, 4.951, 2.127),
                    'Pos': Point3(583.253, -677.403, 15.897),
                    'Scale': VBase3(1.911, 1.911, 1.911),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162579001.46dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-112.519, 9.832, 4.673),
                    'Pos': Point3(546.451, -711.086, -5.558),
                    'Scale': VBase3(2.128, 2.128, 2.128),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162579041.9dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-32.947, 5.173, -2.425),
                    'Pos': Point3(587.067, -740.43, 17.701),
                    'Scale': VBase3(2.128, 2.128, 2.128),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162579056.73dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-32.947, 5.173, -2.425),
                    'Pos': Point3(645.594, -605.485, 0.0),
                    'Scale': VBase3(2.128, 2.128, 2.128),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162579058.98dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-32.947, 5.173, -2.425),
                    'Pos': Point3(611.287, -573.076, -1.942),
                    'Scale': VBase3(2.128, 2.128, 2.128),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162579060.73dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-28.111, 4.951, -2.852),
                    'Pos': Point3(636.011, -642.186, 0.0),
                    'Scale': VBase3(2.128, 2.128, 2.128),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162579199.21dzlu': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(47.744, -6.893, -24.723),
                    'Pos': Point3(580.916, -732.395, 8.128),
                    'Scale': VBase3(4.334, 4.334, 4.334),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/props/rock_group_1_sphere'
                    }
                },
                '1162579331.75dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-73.655, 5.504, 1.529),
                    'Pos': Point3(632.005, -818.121, 0.0),
                    'Scale': VBase3(2.296, 2.296, 2.296),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162579341.32dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-73.655, 5.504, 1.529),
                    'Pos': Point3(610.397, -807.52, 3.503),
                    'Scale': VBase3(2.296, 2.296, 2.296),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162579346.82dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-74.018, 3.433, -9.889),
                    'Pos': Point3(611.612, -780.956, 6.711),
                    'Scale': VBase3(2.296, 2.296, 2.296),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162579382.68dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-73.655, 5.504, 1.529),
                    'Pos': Point3(587.418, -775.26, 0.386),
                    'Scale': VBase3(2.758, 2.758, 2.758),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162579401.92dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-33.558, -9.216, -2.447),
                    'Pos': Point3(578.094, -713.307, 12.02),
                    'Scale': VBase3(3.5, 3.5, 3.5),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots'
                    }
                },
                '1162579450.07dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-32.512, 4.664, 0.0),
                    'Pos': Point3(593.209, -787.988, 3.967),
                    'Scale': VBase3(2.178, 2.178, 2.178),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162579477.28dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(29.511, -3.952, 7.392),
                    'Pos': Point3(541.052, -765.265, 23.137),
                    'Scale': VBase3(2.178, 2.178, 2.178),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162579495.23dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(29.511, -3.952, 7.392),
                    'Pos': Point3(586.636, -636.216, 0.0),
                    'Scale': VBase3(2.178, 2.178, 2.178),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162579496.87dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-31.653, -8.376, 0.125),
                    'Pos': Point3(532.338, -673.668, 24.436),
                    'Scale': VBase3(2.178, 2.178, 2.178),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162579552.36dzlu': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-51.838, 0.0, 0.0),
                    'Pos': Point3(564.672, -764.757, 0.0),
                    'Scale': VBase3(4.098, 4.098, 4.098),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/props/rock_1_sphere'
                    }
                },
                '1162579651.42dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-32.512, -5.078, 0.0),
                    'Pos': Point3(497.166, -662.155, -17.54),
                    'Scale': VBase3(2.178, 2.178, 2.178),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1162579990.07dzlu': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(66.911, -2.792, 6.518),
                    'Pos': Point3(207.844, -185.499, -2.0),
                    'Scale': VBase3(0.659, 0.659, 0.659),
                    'Visual': {
                        'Color': (0.25999999046325684, 0.3499999940395355,
                                  0.38999998569488525, 1.0),
                        'Model':
                        'models/props/rock_2_sphere'
                    }
                },
                '1162580050.34dzlu': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': VBase3(66.911, -2.792, 6.518),
                    'Pos': Point3(243.967, -201.603, -3.383),
                    'Scale': VBase3(3.035, 3.035, 3.035),
                    'Visual': {
                        'Color': (0.25999999046325684, 0.3499999940395355,
                                  0.38999998569488525, 1.0),
                        'Model':
                        'models/props/rock_2_sphere'
                    }
                },
                '1162580134.26dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-160.943, 112.688, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.44999998807907104, 0.5400000214576721,
                                  0.8199999928474426, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_thin'
                    }
                },
                '1162580160.11dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-44.49, 0.0, 0.0),
                    'Pos': Point3(-156.604, 163.007, 0.0),
                    'Scale': VBase3(0.8, 0.8, 0.8),
                    'Visual': {
                        'Color': (0.44999998807907104, 0.5400000214576721,
                                  0.8199999928474426, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_thin'
                    }
                },
                '1162580232.92dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(24.147, 0.0, 0.0),
                    'Pos': Point3(-18.696, -38.561, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.5699999928474426,
                                  0.5600000023841858, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_thin'
                    }
                },
                '1162580882.43dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-141.382, 0.095, 1.217),
                    'Pos': Point3(356.264, -488.07, 0.0),
                    'Scale': VBase3(0.804, 0.804, 0.804),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_a'
                    }
                },
                '1162580923.68dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-164.53, -0.392, 1.157),
                    'Pos': Point3(78.234, -365.675, 0.0),
                    'Scale': VBase3(0.804, 0.804, 0.804),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_a'
                    }
                },
                '1162581117.26dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(398.317, -600.067, -2.702),
                    'Scale': VBase3(1.469, 1.469, 1.469),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581120.68dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(405.001, -605.904, -2.763),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581126.39dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-34.585, 0.0, 0.0),
                    'Pos': Point3(404.004, -604.363, -0.572),
                    'Scale': VBase3(0.795, 0.795, 0.795),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581133.0dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(395.308, -597.602, -1.009),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581141.04dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(384.9, -610.758, -1.807),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581144.36dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(389.232, -621.779, -1.571),
                    'Scale': VBase3(1.668, 1.668, 1.668),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581145.98dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(387.319, -620.824, 0.0),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581162.73dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(395.799, -619.491, -2.062),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581164.37dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(366.265, -648.756, 0.0),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581164.98dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(371.651, -649.648, -2.216),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581166.56dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(407.408, -608.957, 0.0),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581167.39dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(403.408, -607.635, -0.981),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581168.25dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(412.959, -610.534, 0.0),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581168.79dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(418.696, -611.483, -1.508),
                    'Scale': VBase3(0.86, 0.86, 0.86),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581169.65dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(406.897, -618.523, -1.178),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581170.36dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(409.577, -609.645, 0.0),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581171.11dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(411.358, -611.579, -1.948),
                    'Scale': VBase3(1.149, 1.149, 0.93),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581171.96dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(409.626, -611.292, 0.0),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581173.79dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(407.546, -610.948, 0.0),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581176.57dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(424.085, -612.375, 0.0),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581177.9dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(413.632, -616.473, -3.38),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581181.67dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(375.524, -597.658, -1.887),
                    'Scale': VBase3(0.906, 0.906, 0.906),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581182.32dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(380.798, -605.211, -1.342),
                    'Scale': VBase3(1.66, 1.66, 1.66),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581183.29dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(390.45, -599.788, -0.824),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581183.73dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(390.136, -604.776, -1.205),
                    'Scale': VBase3(1.085, 1.085, 1.085),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581184.18dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(396.887, -598.459, 0.0),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581185.78dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(346.427, -619.499, -2.216),
                    'Scale': VBase3(2.001, 2.001, 2.001),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581187.11dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(290.641, -614.373, -1.295),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581188.48dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, -20.885),
                    'Pos': Point3(292.543, -612.486, -1.215),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581188.82dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(291.46, -614.799, 0.0),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581189.76dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, -12.712, 0.0),
                    'Pos': Point3(295.874, -614.075, -1.646),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581190.51dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 28.677),
                    'Pos': Point3(293.445, -615.906, -0.884),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581192.04dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(292.871, -599.964, -1.685),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581194.96dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(435.95, -631.628, 0.0),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581195.62dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(446.847, -628.558, 0.0),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581196.4dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(414.889, -679.682, 0.0),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581198.9dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-36.591, -4.63, 0.0),
                    'Pos': Point3(369.75, -647.131, -1.782),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581199.73dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-98.678, 0.0, 0.0),
                    'Pos': Point3(366.458, -646.173, -1.448),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581201.07dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 20.788, 0.0),
                    'Pos': Point3(364.402, -649.497, -1.48),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581201.68dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.303, 0.0, 0.0),
                    'Pos': Point3(366.828, -649.107, -1.439),
                    'Scale': VBase3(0.781, 0.781, 0.781),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581202.34dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-53.777, 0.0, 0.0),
                    'Pos': Point3(364.625, -649.767, 0.0),
                    'Scale': VBase3(1.149, 1.149, 1.149),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581230.31dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-30.189, 0.0, 0.0),
                    'Pos': Point3(366.756, -488.935, 0.0),
                    'Scale': VBase3(1.273, 1.273, 1.273),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581230.92dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-30.189, 0.0, 0.0),
                    'Pos': Point3(368.096, -489.157, 0.0),
                    'Scale': VBase3(1.273, 1.273, 1.273),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162581234.92dzlu': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-30.189, 0.0, 0.0),
                    'Pos': Point3(375.018, -513.072, -1.199),
                    'Scale': VBase3(1.273, 1.273, 1.273),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1162600301.39sdnaik': {
                    'Type': 'Port Collision Sphere',
                    'Name': '',
                    'Hpr': VBase3(-21.848, 0.0, 0.0),
                    'Pos': Point3(174.854, -853.185, -2.0),
                    'Scale': VBase3(1079.46, 1079.46, 1079.46),
                    'Visual': {
                        'Color': (0.5, 0.5, 1.0, 0.2),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1163119773.31sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_exterior_1',
                    'Hpr': VBase3(-180.0, 0.0, 0.0),
                    'Pos': Point3(471.383, -559.794, -2.597),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1163119776.08sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_exterior_2',
                    'Hpr': VBase3(-101.237, 0.0, 0.0),
                    'Pos': Point3(103.631, -123.494, -2.529),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1163130907.42sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_exterior_1',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(471.383, -559.794, -2.597),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1163130908.98sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_exterior_2',
                    'Hpr': VBase3(-101.237, 0.0, 0.0),
                    'Pos': Point3(103.631, -123.494, -2.529),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1163462918.28sdnaik': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(194.884, -615.123, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1171314304.0dxschafe': {
                    'Type': 'Building Exterior',
                    'File': 'Cuba_jail_interior',
                    'ExtUid': '1171314304.0dxschafe0',
                    'Hpr': VBase3(58.558, 0.0, 1.06),
                    'Objects': {
                        '1201041678.38dxschafe': {
                            'Type': 'Door Locator Node',
                            'Name': 'door_locator',
                            'Hpr': VBase3(-180.0, 0.0, 0.0),
                            'Pos': Point3(12.899, -22.494, 0.283),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-333.987, -619.709, 27.958),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Color': (0.7, 0.7, 0.7, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior': 'models/buildings/navy_jail_interior',
                        'Model': 'models/buildings/jail_exterior',
                        'SignImage': 'models/buildings/sign1_eng_a_icon_doctor'
                    }
                },
                '1171315072.0dxschafe': {
                    'Type': 'Tree - Animated',
                    'DisableCollision': False,
                    'Hpr': VBase3(-6.279, -0.862, 7.781),
                    'Pos': Point3(-199.537, -773.193, 2.416),
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
                '1171315200.0dxschafe': {
                    'Type': 'Tree - Animated',
                    'DisableCollision': False,
                    'Hpr': VBase3(-76.672, 5.284, 1.846),
                    'Pos': Point3(-285.512, -606.503, 25.88),
                    'Scale': VBase3(0.829, 0.829, 0.829),
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
                '1171315200.0dxschafe0': {
                    'Type': 'Tree - Animated',
                    'DisableCollision': True,
                    'Hpr': VBase3(-35.024, 12.51, 17.522),
                    'Pos': Point3(-202.949, -789.058, 0.554),
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
                '1171315200.0dxschafe1': {
                    'Type': 'Tree - Animated',
                    'DisableCollision': False,
                    'Hpr': VBase3(-17.26, 5.387, 7.542),
                    'Pos': Point3(-193.68, -788.419, 1.426),
                    'Scale': VBase3(0.744, 0.744, 0.744),
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
                        'Color': (1.0, 0.93, 0.8509803921568627, 1.0),
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1171315200.0dxschafe2': {
                    'Type': 'Tree - Animated',
                    'DisableCollision': True,
                    'Hpr': VBase3(-20.254, -3.793, 13.121),
                    'Pos': Point3(-192.776, -633.153, 11.116),
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
                '1171315200.0dxschafe3': {
                    'Type': 'Tree - Animated',
                    'DisableCollision': False,
                    'Hpr': VBase3(-36.173, -4.639, 19.768),
                    'Pos': Point3(-347.684, -752.909, 24.386),
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
                        'Color': (0.55, 0.67, 0.6901960784313725, 1.0),
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1171315200.0dxschafe4': {
                    'Type': 'Tree - Animated',
                    'DisableCollision': True,
                    'Hpr': VBase3(74.217, 13.753, 4.957),
                    'Pos': Point3(-379.833, -728.54, 26.258),
                    'Scale': VBase3(1.176, 1.176, 1.176),
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
                        'Color': (0.71, 0.67, 0.5686274509803921, 1.0),
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1171315200.0dxschafe5': {
                    'Type': 'Tree - Animated',
                    'DisableCollision': False,
                    'Hpr': VBase3(76.729, 7.622, 1.792),
                    'Pos': Point3(-339.218, -732.857, 23.816),
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
                        'Color': (0.93, 0.87, 0.7764705882352941, 1.0),
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1171315200.0dxschafe6': {
                    'Type': 'Tree - Animated',
                    'DisableCollision': False,
                    'Hpr': VBase3(-1.294, 5.793, 12.616),
                    'Pos': Point3(-334.943, -742.422, 22.706),
                    'Scale': VBase3(0.856, 0.856, 0.856),
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
                '1171315200.0dxschafe7': {
                    'Type': 'Tree - Animated',
                    'DisableCollision': True,
                    'Hpr': VBase3(0.0, 0.0, 7.829),
                    'Pos': Point3(-293.975, -605.243, 26.434),
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
                        'Color': (1.0, 1.0, 0.8509803921568627, 1.0),
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1171315200.0dxschafe8': {
                    'Type': 'Tree - Animated',
                    'DisableCollision': True,
                    'Hpr': VBase3(8.838, -2.369, 4.157),
                    'Pos': Point3(-372.098, -650.87, 27.918),
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
                '1171315200.0dxschafe9': {
                    'Type': 'Tree - Animated',
                    'DisableCollision': False,
                    'Hpr': VBase3(-49.999, 9.933, 5.223),
                    'Pos': Point3(-374.047, -662.824, 27.26),
                    'Scale': VBase3(0.72, 0.72, 0.72),
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
                        'Color': (0.75, 0.72, 0.6352941176470588, 1.0),
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1171315200.0dxschafe:': {
                    'Type': 'Tree - Animated',
                    'DisableCollision': True,
                    'Hpr': VBase3(-101.309, -4.414, -1.533),
                    'Pos': Point3(-206.707, -559.092, 18.329),
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
                '1171315200.0dxschafe;': {
                    'Type': 'Tree - Animated',
                    'DisableCollision': True,
                    'Hpr': VBase3(0.0, 0.0, 13.303),
                    'Pos': Point3(-204.403, -564.043, 17.606),
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
                        'Color': (1.0, 1.0, 0.8509803921568627, 1.0),
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1171315200.0dxschafe<': {
                    'Type': 'Tree - Animated',
                    'DisableCollision': False,
                    'Hpr': VBase3(-48.156, -6.558, 4.285),
                    'Pos': Point3(-157.612, -591.007, 3.037),
                    'Scale': VBase3(0.74, 0.74, 0.74),
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
                '1171315200.0dxschafe=': {
                    'Type': 'Tree - Animated',
                    'DisableCollision': False,
                    'Hpr': VBase3(8.576, 0.0, 20.786),
                    'Pos': Point3(-159.203, -583.839, 3.061),
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
                        'Color': (1.0, 1.0, 0.8509803921568627, 1.0),
                        'Model': 'models/vegetation/palm_trunk_a_hi',
                        'PartName': 'trunk'
                    }
                },
                '1171315712.0dxschafe': {
                    'Type': 'Well',
                    'DisableCollision': False,
                    'Hpr': VBase3(48.58, 0.0, 0.0),
                    'Pos': Point3(-282.536, -681.893, 24.96),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/wellA'
                    }
                },
                '1171315840.0dxschafe': {
                    'Type': 'Trellis',
                    'DisableCollision': True,
                    'Hpr': VBase3(-13.255, -8.917, 0.0),
                    'Pos': Point3(-340.755, -651.328, 24.456),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/trellis_d'
                    }
                },
                '1171315968.0dxschafe': {
                    'Type': 'Swamp_props_small',
                    'DisableCollision': False,
                    'Hpr': VBase3(44.133, -0.124, 0.95),
                    'Pos': Point3(-299.978, -615.327, 26.982),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/swamp_bench'
                    }
                },
                '1171315968.0dxschafe1': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-284.632, -885.184, -15.189),
                    'Scale': VBase3(2.831, 2.831, 2.831),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1171316096.0dxschafe': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, 3.63),
                    'Pos': Point3(-264.811, -579.308, -4.364),
                    'Scale': VBase3(2.831, 2.831, 2.831),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1171316096.0dxschafe0': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, -2.013),
                    'Pos': Point3(-175.505, -498.597, -37.061),
                    'Scale': VBase3(3.643, 3.643, 3.643),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1171316096.0dxschafe1': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, -2.013),
                    'Pos': Point3(-82.649, -424.379, -34.183),
                    'Scale': VBase3(3.643, 3.643, 3.643),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1171316224.0dxschafe': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, -2.013),
                    'Pos': Point3(-242.122, -980.327, -54.296),
                    'Scale': VBase3(3.643, 3.643, 3.643),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1171316224.0dxschafe0': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, -2.013),
                    'Pos': Point3(-311.461, -827.956, -42.249),
                    'Scale': VBase3(3.643, 3.643, 3.643),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_roots_canopy'
                    }
                },
                '1171316224.0dxschafe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-33.626, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(-201.285, -785.155, 1.43),
                    'Scale': VBase3(1.935, 1.935, 1.935),
                    'Visual': {
                        'Model': 'models/props/rock_group_1_floor'
                    }
                },
                '1171316224.0dxschafe2': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-33.626, 0.0, 0.0),
                    'Objects': {
                        '1184718841.62kmuller': {
                            'Type': 'Collision Barrier',
                            'DisableCollision': False,
                            'GridPos': Point3(-341.25, -726.337, 26.104),
                            'Hpr': VBase3(165.261, 0.0, 0.0),
                            'Pos': Point3(-5.829, 5.141, 1.051),
                            'Scale': VBase3(0.725, 0.616, 0.689),
                            'Visual': {
                                'Model': 'models/misc/coll_plane_barrier'
                            }
                        }
                    },
                    'Pos': Point3(-337.368, -740.866, 24.07),
                    'Scale': VBase3(1.935, 1.935, 1.935),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/rock_group_1_floor'
                    }
                },
                '1171316224.0dxschafe3': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-25.05, 0.0, 0.0),
                    'Pos': Point3(-158.907, -596.686, 2.573),
                    'Scale': VBase3(1.935, 1.935, 1.935),
                    'Visual': {
                        'Model': 'models/props/rock_group_1_floor'
                    }
                },
                '1171316224.0dxschafe4': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': VBase3(154.877, 2.608, -3.7),
                    'Pos': Point3(-284.701, -836.427, 10.167),
                    'Scale': VBase3(1.222, 1.222, 1.222),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/rock_group_1_sphere'
                    }
                },
                '1171316224.0dxschafe5': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': VBase3(94.132, -0.065, -0.006),
                    'Pos': Point3(-265.121, -576.052, 25.379),
                    'Scale': VBase3(1.935, 1.935, 1.935),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/rock_group_1_floor'
                    }
                },
                '1171316224.0dxschafe6': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-44.627, 0.0, 0.0),
                    'Pos': Point3(-293.592, -601.992, 25.908),
                    'Scale': VBase3(1.165, 1.165, 1.165),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/rock_group_1_sphere'
                    }
                },
                '1171316352.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': VBase3(104.908, 0.301, -3.731),
                    'Pos': Point3(-374.373, -657.124, 27.514),
                    'Scale': VBase3(1.124, 1.124, 1.124),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/rock_group_2_sphere'
                    }
                },
                '1171316480.0dxschafe0': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': VBase3(104.908, 0.301, -3.731),
                    'Pos': Point3(-349.236, -752.373, 25.045),
                    'Scale': VBase3(1.53, 1.53, 1.53),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/rock_group_2_sphere'
                    }
                },
                '1171316480.0dxschafe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(40.562, 5.236, 8.064),
                    'Pos': Point3(-194.106, -627.554, 13.373),
                    'Scale': VBase3(2.034, 2.034, 2.034),
                    'Visual': {
                        'Model': 'models/props/rock_group_2_sphere'
                    }
                },
                '1171316480.0dxschafe2': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': VBase3(-141.706, -6.318, -7.136),
                    'Pos': Point3(-177.118, -636.279, 11.289),
                    'Scale': VBase3(1.572, 1.572, 1.572),
                    'Visual': {
                        'Model': 'models/props/rock_group_5_floor'
                    }
                },
                '1171316864.0dxschafe': {
                    'Type': 'Building Exterior',
                    'File': 'cuba_building_int_tailor',
                    'ExtUid': '1171316864.0dxschafe0',
                    'Hpr': VBase3(88.811, 0.0, 0.0),
                    'Objects': {
                        '1201041677.5dxschafe': {
                            'Type': 'Door Locator Node',
                            'Name': 'door_locator',
                            'Hpr': VBase3(-180.0, 0.0, 0.0),
                            'Pos': Point3(0.162, -4.354, 0.599),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-368.014, -694.339, 28.233),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Color': (0.85, 0.83, 0.7411764705882353, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/shanty_npc_house_combo_G',
                        'SignFrame': 'models/buildings/sign1_shanty_a_frame',
                        'SignImage': 'models/buildings/sign1_eng_a_icon_tailor'
                    }
                },
                '1171316864.0dxschafe1': {
                    'Type': 'Building Exterior',
                    'File': 'cuba_building_int_tattoo',
                    'ExtUid': '1171316864.0dxschafe2',
                    'Hpr': VBase3(67.089, 0.0, 4.171),
                    'Objects': {
                        '1201041678.91dxschafe': {
                            'Type': 'Door Locator Node',
                            'Name': 'door_locator',
                            'Hpr': VBase3(-180.0, 0.0, 0.0),
                            'Pos': Point3(0.313, -4.016, 1.444),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-165.409, -499.223, 9.61),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Color': (0.86, 0.86, 0.8588235294117647, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/shanty_npc_house_combo_J',
                        'SignFrame': 'models/buildings/sign1_shanty_a_frame',
                        'SignImage': 'models/buildings/sign1_eng_a_icon_tattoo'
                    }
                },
                '1171317248.0dxschafe': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1171317248.0dxschafe0',
                    'Hpr': VBase3(110.324, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(-289.272, -827.364, 11.794),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Color': (0.7, 0.7, 0.7, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/shanty_npc_house_combo_D',
                        'SignImage': 'models/buildings/sign1_eng_a_icon_doctor'
                    }
                },
                '1171317760.0dxschafe': {
                    'Type': 'Wall',
                    'Hpr': VBase3(76.725, 0.0, 0.417),
                    'Pos': Point3(-364.738, -682.879, 27.909),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/buildings/woodfence_60'
                    }
                },
                '1171317760.0dxschafe0': {
                    'Type': 'Wall',
                    'Hpr': VBase3(100.931, -0.147, -2.003),
                    'Pos': Point3(-354.916, -759.608, 25.737),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.699999988079071, 0.699999988079071,
                                  0.699999988079071, 1.0),
                        'Model':
                        'models/buildings/woodfence_60'
                    }
                },
                '1171318016.0dxschafe': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(174.015, -1.384, -1.516),
                    'Pos': Point3(-315.867, -807.895, 18.608),
                    'Scale': VBase3(1.324, 1.324, 1.324),
                    'Visual': {
                        'Color': (0.7019607843137254, 0.84, 0.6509803921568628,
                                  1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots'
                    }
                },
                '1171318016.0dxschafe0': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(42.53, 2.053, 12.816),
                    'Pos': Point3(-332.123, -785.348, 18.625),
                    'Scale': VBase3(1.324, 1.324, 1.324),
                    'Visual': {
                        'Color': (0.96, 0.96, 0.9372549019607843, 1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1171318016.0dxschafe1': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(174.015, -1.384, -12.349),
                    'Pos': Point3(-372.147, -615.81, 20.95),
                    'Scale': VBase3(1.739, 1.739, 1.739),
                    'Visual': {
                        'Color': (0.699999988079071, 0.7300000190734863,
                                  0.5799999833106995, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots'
                    }
                },
                '1171318016.0dxschafe2': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-104.832, 6.689, -11.126),
                    'Pos': Point3(-342.548, -770.489, 23.537),
                    'Scale': VBase3(1.324, 1.324, 1.324),
                    'Visual': {
                        'Color': (0.699999988079071, 0.7300000190734863,
                                  0.5799999833106995, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots'
                    }
                },
                '1171318144.0dxschafe': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(174.015, -1.384, -1.516),
                    'Pos': Point3(-242.418, -547.412, 21.945),
                    'Scale': VBase3(1.324, 1.324, 1.324),
                    'Visual': {
                        'Color': (0.699999988079071, 0.7300000190734863,
                                  0.5799999833106995, 1.0),
                        'Model':
                        'models/vegetation/swamp_tree_roots'
                    }
                },
                '1171318144.0dxschafe0': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(-102.342, -1.661, 1.207),
                    'Pos': Point3(-308.624, -582.81, 23.457),
                    'Scale': VBase3(1.324, 1.324, 1.324),
                    'Visual': {
                        'Color': (0.7, 0.73, 0.58, 1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1171319168.0dxschafe': {
                    'Type': 'Wall',
                    'Hpr': VBase3(73.631, 0.036, -0.668),
                    'Pos': Point3(-333.435, -684.617, 27.253),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/buildings/woodfence_60'
                    }
                },
                '1171319168.0dxschafe0': {
                    'Type': 'Wall',
                    'Hpr': VBase3(1.345, 0.862, 0.28),
                    'Pos': Point3(-393.734, -685.211, 27.965),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/buildings/woodfence_60'
                    }
                },
                '1171319424.0dxschafe': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(134.89, -3.563, -3.569),
                    'Pos': Point3(-371.999, -713.504, 27.482),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1171319424.0dxschafe0': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(154.824, -4.565, -2.142),
                    'Pos': Point3(-370.918, -635.954, 28.577),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1171319424.0dxschafe1': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(-142.021, -3.978, 3.1),
                    'Pos': Point3(-374.971, -674.349, 28.074),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1171319424.0dxschafe2': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(-142.021, -3.978, 3.1),
                    'Pos': Point3(-364.271, -744.154, 26.403),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1171319552.0dxschafe0': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(89.587, 0.0, 0.0),
                    'Pos': Point3(-345.824, -763.628, 24.667),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1171319680.0dxschafe': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(70.418, 0.0, -5.372),
                    'Pos': Point3(-375.646, -731.158, 26.489),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1171319680.0dxschafe0': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(-82.382, 2.461, 4.776),
                    'Pos': Point3(-379.378, -723.104, 27.348),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1171319680.0dxschafe2': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(-133.989, -5.375, 0.099),
                    'Pos': Point3(-341.151, -750.03, 25.761),
                    'Scale': VBase3(1.251, 1.251, 1.251),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/vegetation/bush_b'
                    }
                },
                '1171319808.0dxschafe': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(-155.254, -1.124, 5.253),
                    'Pos': Point3(-303.177, -809.415, 15.781),
                    'Scale': VBase3(1.935, 1.935, 1.935),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1171319808.0dxschafe2': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(175.717, -1.124, 5.253),
                    'Pos': Point3(592.907, -798.972, 0.159),
                    'Scale': VBase3(1.935, 1.935, 1.935),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1171319808.0dxschafe4': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(36.364, -1.124, 5.253),
                    'Pos': Point3(592.284, -797.455, -1.197),
                    'Scale': VBase3(1.935, 1.935, 1.935),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1171319808.0dxschafe5': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'GridPos': Point3(-280.878, -837.764, 10.574),
                    'Hpr': VBase3(30.143, 0.0, 0.0),
                    'Pos': Point3(-280.878, -837.764, 10.574),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1171319808.0dxschafe6': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'GridPos': Point3(-277.701, -841.101, 10.574),
                    'Hpr': VBase3(10.396, 0.0, 0.0),
                    'Pos': Point3(-264.55, -577.318, 24.378),
                    'Scale': VBase3(1.595, 1.595, 1.595),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1171319936.0dxschafe': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'GridPos': Point3(-277.701, -841.101, 10.574),
                    'Hpr': VBase3(10.396, 0.0, 4.167),
                    'Pos': Point3(-188.435, -515.677, 13.628),
                    'Scale': VBase3(1.595, 1.595, 1.595),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1171319936.0dxschafe0': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'GridPos': Point3(-277.701, -841.101, 10.574),
                    'Hpr': VBase3(10.396, 0.0, 4.167),
                    'Pos': Point3(-290.971, -585.907, 26.919),
                    'Scale': VBase3(1.775, 1.775, 1.775),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1171319936.0dxschafe1': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'GridPos': Point3(-277.701, -841.101, 10.574),
                    'Hpr': VBase3(10.396, 0.0, 4.167),
                    'Pos': Point3(-290.971, -864.503, 8.611),
                    'Scale': VBase3(1.775, 1.775, 1.775),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1171319936.0dxschafe2': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'GridPos': Point3(-277.701, -841.101, 10.574),
                    'Hpr': VBase3(103.439, 4.161, -0.221),
                    'Pos': Point3(-203.235, -560.818, 17.232),
                    'Scale': VBase3(1.775, 1.775, 1.775),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1171319936.0dxschafe3': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'GridPos': Point3(-277.701, -841.101, 10.574),
                    'Hpr': VBase3(24.204, 0.996, 4.046),
                    'Pos': Point3(-205.917, -569.068, 17.84),
                    'Scale': VBase3(1.775, 1.775, 1.775),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1171319936.0dxschafe4': {
                    'Type': 'Bush',
                    'DisableCollision': False,
                    'GridPos': Point3(-277.701, -841.101, 10.574),
                    'Hpr': VBase3(100.939, 4.126, 0.582),
                    'Pos': Point3(-188.231, -638.274, 14.392),
                    'Scale': VBase3(1.775, 1.775, 1.775),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1171320064.0dxschafe': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'GridPos': Point3(-277.701, -841.101, 10.574),
                    'Hpr': VBase3(24.5, 1.023, 5.25),
                    'Pos': Point3(-160.085, -485.298, 9.374),
                    'Scale': VBase3(1.391, 1.391, 1.391),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1171320064.0dxschafe0': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'GridPos': Point3(-277.701, -841.101, 10.574),
                    'Hpr': VBase3(-153.042, -1.248, -5.202),
                    'Pos': Point3(-156.365, -467.801, 9.347),
                    'Scale': VBase3(1.391, 1.391, 1.391),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1171320832.0dxschafe': {
                    'Type': 'Bush',
                    'DisableCollision': False,
                    'Hpr': VBase3(22.759, 10.417, -1.703),
                    'Pos': Point3(-206.729, -777.82, 5.521),
                    'Scale': VBase3(0.739, 0.739, 0.739),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1171320832.0dxschafe0': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(-1.712, 10.196, 2.741),
                    'Pos': Point3(-294.622, -833.425, 13.44),
                    'Scale': VBase3(1.16, 1.16, 1.16),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1171320832.0dxschafe1': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(132.892, 4.002, -1.679),
                    'Pos': Point3(606.193, -837.635, -3.384),
                    'Scale': VBase3(1.16, 1.16, 1.16),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1171320832.0dxschafe2': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(-116.594, 10.417, -1.703),
                    'Pos': Point3(620.037, -845.385, -0.281),
                    'Scale': VBase3(1.16, 1.16, 1.16),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1171320832.0dxschafe3': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(-157.241, -5.59, -6.894),
                    'Pos': Point3(-300.613, -827.068, 15.281),
                    'Scale': VBase3(1.16, 1.16, 1.16),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1171320832.0dxschafe4': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(-120.691, -8.586, -2.225),
                    'Pos': Point3(-319.293, -796.378, 20.273),
                    'Scale': VBase3(1.16, 1.16, 1.16),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1171320960.0dxschafe': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(-77.26, -7.782, 4.264),
                    'Pos': Point3(-212.568, -526.755, 17.857),
                    'Scale': VBase3(1.16, 1.16, 1.16),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1171320960.0dxschafe0': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(170.705, -1.059, -8.804),
                    'Pos': Point3(-151.201, -460.804, 9.186),
                    'Scale': VBase3(1.16, 1.16, 1.16),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1171321088.0dxschafe': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(-165.437, -4.549, -7.62),
                    'Pos': Point3(-342.28, -739.438, 26.037),
                    'Scale': VBase3(1.16, 1.16, 1.16),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1171321088.0dxschafe0': {
                    'Type': 'Animal',
                    'Hpr': VBase3(-169.923, 0.0, 0.0),
                    'Patrol Radius': '5.1084',
                    'Pos': Point3(-342.453, -681.228, 28.032),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Species': 'Pig',
                    'Start State': 'Idle',
                    'StartFrame': '0'
                },
                '1171321216.0dxschafe': {
                    'Type': 'Animal',
                    'Hpr': VBase3(-101.132, 0.0, 0.0),
                    'Patrol Radius': '5.2410',
                    'Pos': Point3(-336.727, -661.427, 28.026),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Species': 'Pig',
                    'Start State': 'Walk',
                    'StartFrame': '0'
                },
                '1171321216.0dxschafe0': {
                    'Type': 'Animal',
                    'Hpr': VBase3(-101.132, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(-281.902, -692.238, 24.702),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Species': 'Rooster',
                    'Start State': 'Walk',
                    'StartFrame': '0'
                },
                '1171321216.0dxschafe1': {
                    'Type': 'Animal',
                    'Hpr': VBase3(-101.132, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(-266.781, -682.498, 23.137),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Species': 'Chicken',
                    'Start State': 'Walk',
                    'StartFrame': '0'
                },
                '1171321216.0dxschafe2': {
                    'Type': 'Animal',
                    'Hpr': VBase3(-101.132, 0.0, 0.0),
                    'Patrol Radius': 12,
                    'Pos': Point3(-261.136, -659.03, 23.744),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Species': 'Rooster',
                    'Start State': 'Walk',
                    'StartFrame': '0'
                },
                '1172863796.36kmuller': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(66.911, -2.792, 6.518),
                    'Pos': Point3(326.362, 26.621, -2.0),
                    'Scale': VBase3(6.057, 6.057, 6.057),
                    'Visual': {
                        'Color': (0.25999999046325684, 0.3499999940395355,
                                  0.38999998569488525, 1.0),
                        'Model':
                        'models/props/rock_2_sphere'
                    }
                },
                '1172863850.45kmuller': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(3.368, -0.137, 4.704),
                    'Pos': Point3(212.361, -229.269, -0.091),
                    'Scale': VBase3(5.606, 5.606, 5.606),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/props/rock_4_sphere'
                    }
                },
                '1176186151.42mike': {
                    'Type': 'Townsperson',
                    'Category': 'Gypsy',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'bar_talk03',
                    'CustomModel': 'None',
                    'Hpr': VBase3(-143.238, 0.0, 0.0),
                    'Patrol Radius': '8.0904',
                    'Pos': Point3(-329.212, -675.215, 27.384),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(0.867, 0.867, 0.867),
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'Villager',
                    'TrailFX': 'None'
                },
                '1176258388.82kmuller': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(41.325, -124.235, -4.357),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_a'
                    }
                },
                '1176258538.6kmuller': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-27.599, -86.053, -4.727),
                    'Scale': VBase3(4.077, 4.077, 4.077),
                    'Visual': {
                        'Color': (0.41999998688697815, 0.5799999833106995,
                                  0.7200000286102295, 1.0),
                        'Model':
                        'models/props/rock_2_sphere'
                    }
                },
                '1176258603.27kmuller': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-49.053, -100.206, -2.976),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1176258613.43kmuller': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-57.458, -105.108, -6.347),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1176258631.8kmuller': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-67.927, -105.152, -1.229),
                    'Scale': VBase3(3.271, 3.271, 3.271),
                    'Visual': {
                        'Color': (0.49000000953674316, 0.6100000143051147,
                                  0.9200000166893005, 1.0),
                        'Model':
                        'models/props/rock_3_sphere'
                    }
                },
                '1176258756.88kmuller': {
                    'Type': 'Swamp_props',
                    'DisableCollision': True,
                    'Hpr': VBase3(5.171, 41.577, -84.933),
                    'Pos': Point3(-57.645, -109.688, -1.483),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_tree_thin'
                    }
                },
                '1176258807.22kmuller': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-122.855, -123.625, -1.68),
                    'Scale': VBase3(2.1, 2.1, 2.1),
                    'Visual': {
                        'Model': 'models/props/rock_2_sphere'
                    }
                },
                '1176258867.93kmuller': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-40.483, -109.599, -2.4),
                    'Scale': VBase3(0.648, 0.648, 0.648),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1176258898.99kmuller': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(0.702, -87.743, -1.109),
                    'Scale': VBase3(1.0, 1.0, 1.383),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1176258906.33kmuller': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(3.118, -96.117, -1.037),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1176258927.07kmuller': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(17.995, -107.384, -0.878),
                    'Scale': VBase3(3.296, 3.296, 2.501),
                    'Visual': {
                        'Model': 'models/vegetation/swamp_bush_a'
                    }
                },
                '1176258938.58kmuller': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': VBase3(-92.166, 0.0, 0.0),
                    'Pos': Point3(8.119, -104.756, -3.156),
                    'Scale': VBase3(7.184, 7.184, 7.184),
                    'Visual': {
                        'Color': (0.5, 0.5799999833106995, 0.5899999737739563,
                                  1.0),
                        'Model': 'models/props/rock_4_sphere'
                    }
                },
                '1179791064.29Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-108.17, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-319.939, -759.868, 22.895),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179791120.18Aholdun': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-272.299, -807.439, 12.475),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179791134.46Aholdun': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-262.084, -857.896, 6.657),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179791701.57Aholdun': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-161.67, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '7.2952',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-10.276, -477.541, -1.327),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179791720.71Aholdun': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-154.229, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-198.082, -553.234, 16.188),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179793974.72Aholdun': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(144.658, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '6.2651',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-112.853, -459.391, -0.618),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1184716513.73kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(118.656, 0.0, 0.0),
                    'Pos': Point3(-282.475, -860.838, 6.787),
                    'Scale': VBase3(1.0, 1.0, 3.146),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184716531.9kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(116.072, 0.0, 0.0),
                    'Pos': Point3(-274.672, -882.702, 3.365),
                    'Scale': VBase3(1.0, 1.0, 3.497),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184716542.28kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(118.023, 0.0, 0.0),
                    'Pos': Point3(-267.455, -902.252, -0.361),
                    'Scale': VBase3(1.0, 1.0, 3.619),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184717296.78kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'GridPos': Point3(-279.242, -841.955, 8.594),
                    'Hpr': VBase3(77.613, 0.0, 0.0),
                    'Pos': Point3(-279.242, -841.955, 8.594),
                    'Scale': VBase3(1.975, 1.807, 2.096),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184717358.28kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'GridPos': Point3(-286.708, -832.001, 11.316),
                    'Hpr': VBase3(-179.707, 0.0, 0.0),
                    'Pos': Point3(-286.708, -832.001, 11.316),
                    'Scale': VBase3(1.792, 1.792, 1.792),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184717384.58kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'GridPos': Point3(-296.947, -819.412, 12.195),
                    'Hpr': VBase3(119.548, 0.0, -4.688),
                    'Pos': Point3(-296.947, -819.412, 12.195),
                    'Scale': VBase3(2.894, 1.46, 2.73),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184717452.25kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(137.257, 0.0, -3.56),
                    'Pos': Point3(-312.435, -799.391, 16.132),
                    'Scale': VBase3(2.564, 1.997, 3.379),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184717774.17kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(38.538, 0.0, 0.0),
                    'Pos': Point3(-253.242, -575.139, 15.784),
                    'Scale': VBase3(8.433, 5.903, 5.903),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184717903.14kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(8.489, 0.0, 0.0),
                    'Pos': Point3(-204.222, -564.756, 11.991),
                    'Scale': VBase3(2.01, 4.119, 2.361),
                    'Visual': {
                        'Model': 'models/misc/coll_cube_barrier'
                    }
                },
                '1184717982.65kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(31.759, 0.0, 0.0),
                    'Pos': Point3(-197.119, -523.265, 12.405),
                    'Scale': VBase3(3.446, 3.446, 1.862),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184718346.58kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(50.493, 0.0, 0.0),
                    'Pos': Point3(-143.146, -459.234, 4.424),
                    'Scale': VBase3(5.785, 2.186, 2.186),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184718408.0kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(80.042, 0.0, 0.0),
                    'Pos': Point3(-156.558, -481.447, 7.87),
                    'Scale': VBase3(1.647, 1.586, 1.586),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184718756.09kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(116.714, 0.0, 0.0),
                    'Pos': Point3(-336.226, -767.127, 23.465),
                    'Scale': VBase3(2.559, 1.888, 1.888),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184718783.67kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(81.452, 0.0, 0.0),
                    'Pos': Point3(-338.845, -744.705, 23.506),
                    'Scale': VBase3(2.877, 1.685, 1.685),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184718870.54kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-166.203, 0.0, 0.0),
                    'Pos': Point3(-348.336, -721.977, 26.051),
                    'Scale': VBase3(0.602, 1.0, 1.335),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184718946.59kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-85.948, 0.0, 0.0),
                    'Pos': Point3(-350.32, -732.694, 25.196),
                    'Scale': VBase3(1.995, 1.429, 1.429),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184719009.84kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-176.754, 0.0, 0.0),
                    'Pos': Point3(-352.852, -742.675, 25.386),
                    'Scale': VBase3(1.0, 1.0, 1.386),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184719101.83kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(11.051, 0.0, 0.0),
                    'Pos': Point3(-294.921, -607.314, 26.788),
                    'Scale': VBase3(0.801, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184719164.21kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-72.385, 0.0, 0.0),
                    'Pos': Point3(-46.593, -542.406, -18.838),
                    'Scale': VBase3(2.647, 2.647, 8.776),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184719190.71kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-22.245, -563.691, -4.271),
                    'Scale': VBase3(1.0, 1.0, 4.834),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184719277.87kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(100.696, 0.0, 0.0),
                    'Pos': Point3(-2.572, -548.712, -3.941),
                    'Scale': VBase3(0.488, 1.0, 2.697),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184719296.98kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(172.417, 0.0, 0.0),
                    'Pos': Point3(-36.554, -532.038, -0.105),
                    'Scale': VBase3(2.779, 2.476, 5.133),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184720985.21kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(35.205, 0.0, 0.0),
                    'Pos': Point3(79.502, -138.629, -6.594),
                    'Scale': VBase3(2.293, 2.293, 4.515),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184721040.78kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(243.699, -207.921, 0.0),
                    'Scale': VBase3(2.704, 2.704, 2.704),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184721161.87kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-20.497, 0.0, 0.0),
                    'Pos': Point3(395.657, -500.026, -12.135),
                    'Scale': VBase3(6.587, 4.342, 4.342),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184721215.28kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-26.999, 0.0, 0.0),
                    'Pos': Point3(445.877, -510.059, -7.858),
                    'Scale': VBase3(3.986, 3.696, 3.696),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184721233.95kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(41.742, 0.0, 0.0),
                    'Pos': Point3(430.517, -507.735, -2.914),
                    'Scale': VBase3(1.222, 1.0, 3.159),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184721291.89kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(165.907, 0.0, 0.0),
                    'Pos': Point3(418.533, -477.362, -11.395),
                    'Scale': VBase3(8.882, 8.419, 8.419),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184721406.87kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(132.152, 0.0, 0.0),
                    'Pos': Point3(489.104, -633.97, 0.0),
                    'Scale': VBase3(3.714, 2.777, 2.777),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184721426.18kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(164.262, 0.0, 0.0),
                    'Pos': Point3(469.196, -633.133, -1.26),
                    'Scale': VBase3(1.726, 2.464, 2.901),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184721812.36kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-11.304, 0.0, 0.0),
                    'Pos': Point3(465.739, -655.873, -4.272),
                    'Scale': VBase3(2.878, 2.878, 2.878),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184721823.17kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-71.597, 0.0, 0.0),
                    'Pos': Point3(445.567, -632.786, -1.355),
                    'Scale': VBase3(4.425, 2.405, 2.405),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184721880.11kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(96.012, 0.0, 0.0),
                    'Pos': Point3(461.205, -615.181, -3.647),
                    'Scale': VBase3(3.559, 3.159, 3.159),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184721907.79kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-123.568, 0.0, 0.0),
                    'Pos': Point3(471.884, -627.656, -9.972),
                    'Scale': VBase3(1.863, 1.863, 4.774),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184721953.51kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(45.775, 0.0, 0.0),
                    'Pos': Point3(466.141, -594.241, -3.326),
                    'Scale': VBase3(2.179, 2.179, 3.091),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184721971.46kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-151.881, 0.0, 0.0),
                    'Pos': Point3(454.64, -582.71, -8.004),
                    'Scale': VBase3(1.789, 1.405, 4.494),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184722024.71kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-35.565, 0.0, 0.0),
                    'Pos': Point3(500.403, -671.125, -8.22),
                    'Scale': VBase3(1.919, 2.373, 4.389),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1184722304.54kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(5.496, 0.0, 0.0),
                    'Pos': Point3(604.613, -839.789, -5.012),
                    'Scale': VBase3(1.288, 1.288, 1.288),
                    'Visual': {
                        'Model': 'models/misc/coll_cube_barrier'
                    }
                },
                '1184891648.0dxschafe': {
                    'Type': 'Dinghy',
                    'Aggro Radius': 20,
                    'Hpr': VBase3(40.217, 5.058, 0.0),
                    'Location': 'Water',
                    'Pos': Point3(-144.25, -717.336, 1.117),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/shipparts/dingy-geometry_High'
                    }
                },
                '1184891776.0dxschafe0': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': 1,
                    'Pos': Point3(-140.128, -651.976, 2.377),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1184891776.0dxschafe1': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': 1,
                    'Pos': Point3(-184.722, -758.28, 2.699),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1185921614.52kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(18.837, 0.0, 0.0),
                    'Pos': Point3(-305.391, -813.387, 26.631),
                    'Scale': VBase3(1.59, 1.59, 1.59),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1186006891.46kmuller': {
                    'Type': 'Crate',
                    'DisableCollision': True,
                    'Hpr': VBase3(69.221, 0.0, 0.0),
                    'Pos': Point3(-306.308, -819.284, 27.342),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.72, 0.78, 0.7529411764705882, 1.0),
                        'Model': 'models/props/crate_04'
                    }
                },
                '1186007092.14kmuller': {
                    'Type': 'Crate',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-304.305, -823.26, 29.649),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.71, 0.8, 0.7607843137254902, 1.0),
                        'Model': 'models/props/crate'
                    }
                },
                '1186007187.37kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(108.406, 0.0, 0.0),
                    'Pos': Point3(-301.8, -822.736, 26.72),
                    'Scale': VBase3(1.0, 1.0, 1.955),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1186007215.54kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(161.324, 0.0, 0.0),
                    'Pos': Point3(-307.586, -817.184, 26.407),
                    'Scale': VBase3(1.0, 1.0, 2.024),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1186007267.03kmuller': {
                    'Type': 'Crate',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(-292.103, -841.622, 27.342),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.73, 0.78, 0.7568627450980392, 1.0),
                        'Model': 'models/props/crates_group_1'
                    }
                },
                '1186007415.7kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(98.834, 0.0, 0.0),
                    'Pos': Point3(-289.516, -840.404, 26.219),
                    'Scale': VBase3(1.0, 1.0, 1.651),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1187913949.14akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-128.874, 0.0, 0.0),
                    'Pos': Point3(454.734, -484.921, -11.51),
                    'Scale': VBase3(1.878, 1.878, 8.431),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1187914011.44akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-42.248, 0.0, 0.0),
                    'Pos': Point3(358.995, -356.361, -4.153),
                    'Scale': VBase3(1.0, 1.0, 2.585),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1187914045.25akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-67.838, 0.0, 0.0),
                    'Pos': Point3(369.831, -379.882, -2.0),
                    'Scale': VBase3(1.0, 1.0, 2.585),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1187914073.11akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(110.197, 0.0, 0.0),
                    'Pos': Point3(384.244, -377.965, -2.0),
                    'Scale': VBase3(1.0, 1.0, 2.585),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1187914104.39akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-42.248, 0.0, 0.0),
                    'Pos': Point3(347.259, -341.046, -2.0),
                    'Scale': VBase3(1.0, 1.0, 2.585),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1187914121.33akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-6.709, 0.0, 0.0),
                    'Pos': Point3(327.875, -338.618, -2.0),
                    'Scale': VBase3(1.796, 1.796, 3.425),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1187914162.75akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-26.96, 0.0, 0.0),
                    'Pos': Point3(271.414, -210.79, -2.0),
                    'Scale': VBase3(2.704, 2.704, 2.704),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1187914199.86akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-110.168, 0.0, 0.0),
                    'Pos': Point3(293.678, -262.519, 0.0),
                    'Scale': VBase3(2.101, 2.101, 2.101),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1187914236.7akelts': {
                    'Type': 'Swamp_props',
                    'DisableCollision': False,
                    'Hpr': VBase3(178.851, -3.122, 4.786),
                    'Pos': Point3(301.413, -302.12, -1.385),
                    'Scale': VBase3(1.846, 1.846, 1.846),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/swamp_tree_roots'
                    }
                },
                '1187914264.97akelts': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(3.368, -0.137, 4.704),
                    'Pos': Point3(302.212, -264.111, -7.994),
                    'Scale': VBase3(10.072, 10.072, 10.072),
                    'Visual': {
                        'Color': (0.28999999165534973, 0.4000000059604645,
                                  0.46000000834465027, 1.0),
                        'Model':
                        'models/props/rock_4_sphere'
                    }
                },
                '1187914386.67akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(17.622, 0.0, 0.0),
                    'Pos': Point3(206.577, -145.923, -0.939),
                    'Scale': VBase3(1.346, 1.346, 1.346),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1187914411.34akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-64.455, 0.0, 0.0),
                    'Pos': Point3(184.517, -137.759, -1.635),
                    'Scale': VBase3(1.346, 1.346, 1.346),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1187914475.81akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-67.009, 0.0, 0.0),
                    'Pos': Point3(0.822, -105.142, -1.998),
                    'Scale': VBase3(3.006, 0.257, 1.385),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1187914641.95akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-16.882, 0.0, 0.0),
                    'Pos': Point3(27.072, -124.314, -4.181),
                    'Scale': VBase3(0.678, 0.372, 2.225),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1187914830.53akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(77.413, 0.0, 0.0),
                    'Pos': Point3(-73.571, -407.45, 0.0),
                    'Scale': VBase3(0.525, 1.259, 1.259),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1187914874.69akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(4.408, 0.0, 0.0),
                    'Pos': Point3(-95.124, -422.22, -2.0),
                    'Scale': VBase3(0.468, 1.123, 1.123),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1187993555.97akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(-193.985, -788.725, 1.073),
                    'Scale': VBase3(0.711, 0.719, 1.871),
                    'Visual': {
                        'Model': 'models/misc/coll_cube_barrier'
                    }
                },
                '1187993700.22akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(39.363, 0.0, 0.0),
                    'Pos': Point3(-198.947, -773.149, 3.772),
                    'Scale': VBase3(1.0, 1.0, 1.854),
                    'Visual': {
                        'Model': 'models/misc/coll_cube_barrier'
                    }
                },
                '1187995354.27akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'GridPos': Point3(-199.38, -789.316, 2.818),
                    'Hpr': VBase3(0.0, 14.537, 5.684),
                    'Pos': Point3(-202.599, -789.944, 2.707),
                    'Scale': VBase3(0.598, 0.819, 1.733),
                    'Visual': {
                        'Model': 'models/misc/coll_cube_barrier'
                    }
                },
                '1189212260.31kmuller': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1189212260.31kmuller0',
                    'Hpr': VBase3(-128.508, 0.527, -1.189),
                    'Objects': {
                        '1189456314.77kmuller': {
                            'Type': 'Collision Barrier',
                            'DisableCollision': False,
                            'GridPos': Point3(-33.474, -435.681, -3.906),
                            'Hpr': VBase3(-153.807, 1.678, 3.406),
                            'Pos': Point3(-44.556, -4.536, -8.628),
                            'Scale': VBase3(2.298, 1.0, 4.74),
                            'Visual': {
                                'Model': 'models/misc/coll_plane_barrier'
                            }
                        },
                        '1189456447.08kmuller': {
                            'Type': 'Townsperson',
                            'Category': 'Shipwright',
                            'Aggro Radius': '12.0000',
                            'AnimSet': 'default',
                            'CustomModel': 'None',
                            'GridPos': Point3(-72.355, -489.439, 0.343),
                            'Hpr': VBase3(-70.979, 3.589, -1.236),
                            'Patrol Radius': '1.0000',
                            'Pos': Point3(21.292, -1.475, 0.0),
                            'PoseAnim': '',
                            'PoseFrame': '',
                            'Private Status': 'All',
                            'Respawns': True,
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Start State': 'Idle',
                            'StartFrame': '0',
                            'Team': 'Villager',
                            'TrailFX': 'None'
                        }
                    },
                    'Pos': Point3(-66.869, -484.894, -0.298),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Model': 'models/buildings/shanty_repairshop_exterior',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1189456366.97kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-97.966, 0.0, 0.0),
                    'Pos': Point3(-52.47, -435.448, -2.687),
                    'Scale': VBase3(1.19, 1.19, 3.973),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1190666496.0dxschafe': {
                    'Type': 'Animated Avatar - Navy',
                    'Animation Track': 'sit_sleep',
                    'Hpr': VBase3(-35.554, 28.688, 2.895),
                    'Pos': Point3(-299.244, -614.407, 27.064),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1190666880.0dxschafe': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-31.482, 0.0, 0.0),
                    'Pos': Point3(-300.724, -614.498, 26.702),
                    'Scale': VBase3(1.242, 1.488, 1.205),
                    'Visual': {
                        'Model': 'models/misc/coll_cube_barrier'
                    }
                },
                '1190741504.0dxschafe': {
                    'Type': 'Building Exterior',
                    'File': 'cuba_building_int_tavern',
                    'ExtUid': '1190741504.0dxschafe0',
                    'Hpr': VBase3(43.111, 0.0, 2.086),
                    'Objects': {
                        '1201041675.97dxschafe': {
                            'Type': 'Door Locator Node',
                            'Name': 'door_locator',
                            'Hpr': VBase3(-179.829, 0.0, 0.0),
                            'Pos': Point3(-0.498, -4.479, 0.952),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1201041677.36dxschafe': {
                            'Type': 'Door Locator Node',
                            'Name': 'door_locator_2',
                            'Hpr': VBase3(0.0, 0.0, 0.0),
                            'Pos': Point3(-6.626, 20.841, 1.006),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-166.222, -609.364, 14.521),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0.67, 0.7254901960784313, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Model': 'models/buildings/shanty_tavern_exterior',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1191629336.42kmuller': {
                    'Type': 'Stairs',
                    'Hpr': VBase3(41.465, 0.0, 0.0),
                    'Pos': Point3(-154.369, -622.269, 8.323),
                    'Scale': VBase3(0.973, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.36, 0.44, 0.5, 1.0),
                        'Model': 'models/buildings/stone_stairs_double'
                    }
                },
                '1191629553.64kmuller': {
                    'Type': 'Stairs',
                    'Hpr': VBase3(42.295, 0.0, 0.0),
                    'Pos': Point3(-146.961, -630.23, 1.915),
                    'Scale': VBase3(0.762, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.36000001430511475, 0.4399999976158142, 0.5,
                                  1.0),
                        'Model':
                        'models/buildings/stone_stairs_double'
                    }
                },
                '1191629599.67kmuller': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(36.897, 0.0, 0.0),
                    'Pos': Point3(-153.414, -608.288, 7.57),
                    'Scale': VBase3(0.76, 0.76, 0.76),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1191629616.42kmuller': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(-18.577, 0.0, 0.0),
                    'Pos': Point3(-165.963, -624.1, 10.167),
                    'Scale': VBase3(0.659, 0.659, 0.659),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1191629698.66kmuller': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-158.788, -598.788, 8.404),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1191629817.2kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(126.054, 0.0, 0.0),
                    'Pos': Point3(-151.785, -598.595, 6.556),
                    'Scale': VBase3(2.507, 2.507, 2.507),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1191629838.92kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(43.161, 0.0, 0.0),
                    'Pos': Point3(-148.854, -612.866, 5.699),
                    'Scale': VBase3(1.225, 1.225, 2.864),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1191629854.09kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-43.63, 0.0, 0.0),
                    'Pos': Point3(-156.953, -613.242, 8.88),
                    'Scale': VBase3(1.09, 1.09, 3.751),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1191629933.37kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(45.217, 0.0, 0.0),
                    'Pos': Point3(-169.664, -631.311, 8.863),
                    'Scale': VBase3(2.621, 1.855, 2.096),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1191629959.37kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-7.406, 0.0, 0.0),
                    'Pos': Point3(-182.264, -640.102, 12.636),
                    'Scale': VBase3(0.724, 1.0, 1.333),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1191629982.17kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(125.106, 0.0, 0.0),
                    'Pos': Point3(-163.15, -618.235, 8.931),
                    'Scale': VBase3(1.0, 1.0, 3.513),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1191630016.62kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-106.537, 0.0, 0.0),
                    'Pos': Point3(-190.914, -616.698, 15.546),
                    'Scale': VBase3(1.0, 1.0, 2.315),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1192043971.0kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-79.363, 0.0, 0.0),
                    'Pos': Point3(175.154, -189.323, -2.684),
                    'Scale': VBase3(1.674, 1.674, 4.468),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1192044061.55kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-66.827, 0.0, 0.0),
                    'Pos': Point3(126.316, -150.761, -1.654),
                    'Scale': VBase3(1.0, 1.0, 3.962),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1192044102.02kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(53.799, 0.0, 0.0),
                    'Pos': Point3(143.19, -154.164, -2.369),
                    'Scale': VBase3(1.0, 1.0, 2.87),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1192228480.0dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(26.869, -359.892, -2.0),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192228608.0dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(148.457, -233.669, -2.0),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192228608.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-27.17, -156.317, -2.0),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Big Gator',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192228608.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(51.014, -214.437, -2.0),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192228608.0dxschafe2': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(363.513, -547.292, -2.0),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192228608.0dxschafe3': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(409.275, -595.765, -1.327),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192228608.0dxschafe4': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(330.853, -437.092, -2.0),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192228608.0dxschafe5': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(223.516, -546.544, -2.0),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192228608.0dxschafe6': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(215.664, -309.744, -2.0),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192228608.0dxschafe7': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-69.322, -165.851, -2.0),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Big Gator',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192228608.0dxschafe8': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-90.742, -210.405, -2.0),
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
                '1192228736.0dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(255.22, -245.849, -2.0),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192228736.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(325.088, -639.495, -2.0),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192228736.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(265.244, -605.764, -1.327),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192228736.0dxschafe2': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(310.809, -372.223, -2.0),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192228736.0dxschafe3': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-49.478, -297.461, -2.0),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192228736.0dxschafe4': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-22.994, -218.547, -2.0),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192228736.0dxschafe5': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(76.849, -324.094, -1.327),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192733824.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-212.788, -770.382, 7.013),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192733952.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-225.931, -895.237, -5.479),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192836222.09kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-11.592, 0.0, 0.0),
                    'Pos': Point3(-337.636, -684.906, 27.34),
                    'Scale': VBase3(0.811, 1.0, 2.125),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1201041679.88dxschafe': {
                    'Type': 'Door Locator Node',
                    'Name': 'door_locator',
                    'Hpr': VBase3(-180.0, 0.0, 0.0),
                    'Pos': Point3(0.313, -4.016, 1.444),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1201041679.89dxschafe': {
                    'Type': 'Door Locator Node',
                    'Name': 'door_locator_2',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(-6.626, 20.841, 1.006),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1210704118.17kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-97.912, 0.0, 0.0),
                    'Pos': Point3(460.304, -573.978, -2.094),
                    'Scale': VBase3(1.86, 1.86, 3.402),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1210704165.86kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-82.933, -0.0, -2.169),
                    'Pos': Point3(457.725, -535.476, -3.064),
                    'Scale': VBase3(4.18, 3.824, 3.824),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                }
            },
            'Phase': 1,
            'Undockable': False,
            'Visual': {
                'Model': 'models/islands/cuba_zero'
            }
        }
    },
    'Node Links':
    [['1192733952.0dxschafe', '1192733824.0dxschafe', 'Bi-directional'],
     ['1179791064.29Aholdun', '1192733824.0dxschafe', 'Bi-directional'],
     ['1179791064.29Aholdun', '1192733952.0dxschafe', 'Bi-directional']],
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
        '1160614528.73sdnaik':
        '["Objects"]["1160614528.73sdnaik"]',
        '1161732317.95sdnaik':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1161732317.95sdnaik"]',
        '1161732322.52sdnaik':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1161732322.52sdnaik"]',
        '1161732370.84sdnaik':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1161732370.84sdnaik"]',
        '1161732370.86sdnaik':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1161732370.84sdnaik"]["Objects"]["1161732370.86sdnaik"]',
        '1161732370.88sdnaik':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1161732370.84sdnaik"]["Objects"]["1161732370.88sdnaik"]',
        '1161732578.06sdnaik':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1161732578.06sdnaik"]',
        '1161732578.08sdnaik':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1161732578.06sdnaik"]["Objects"]["1161732578.08sdnaik"]',
        '1161732578.11sdnaik':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1161732578.06sdnaik"]["Objects"]["1161732578.11sdnaik"]',
        '1161732705.67sdnaik':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1161732705.67sdnaik"]',
        '1161732705.72sdnaik':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1161732705.67sdnaik"]["Objects"]["1161732705.72sdnaik"]',
        '1161732705.7sdnaik':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1161732705.67sdnaik"]["Objects"]["1161732705.7sdnaik"]',
        '1162496104.57dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162496104.57dzlu"]',
        '1162496561.59dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162496561.59dzlu"]',
        '1162496585.79dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162496585.79dzlu"]',
        '1162496638.89dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162496638.89dzlu"]',
        '1162496693.54dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162496693.54dzlu"]',
        '1162496757.15dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162496757.15dzlu"]',
        '1162496818.98dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162496818.98dzlu"]',
        '1162496857.71dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162496857.71dzlu"]',
        '1162496880.34dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162496880.34dzlu"]',
        '1162496889.81dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162496889.81dzlu"]',
        '1162496999.35dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162496999.35dzlu"]',
        '1162497015.78dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162497015.78dzlu"]',
        '1162497038.53dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162497038.53dzlu"]',
        '1162497249.64dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162497249.64dzlu"]',
        '1162497329.21dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162497329.21dzlu"]',
        '1162497460.96dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162497460.96dzlu"]',
        '1162497568.12dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162497568.12dzlu"]',
        '1162497591.24dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162497591.24dzlu"]',
        '1162497648.96dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162497648.96dzlu"]',
        '1162497681.26dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162497681.26dzlu"]',
        '1162497693.48dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162497693.48dzlu"]',
        '1162497709.17dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162497709.17dzlu"]',
        '1162498231.46dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162498231.46dzlu"]',
        '1162498233.67dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162498233.67dzlu"]',
        '1162498236.93dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162498236.93dzlu"]',
        '1162498256.79dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162498256.79dzlu"]',
        '1162498287.12dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162498287.12dzlu"]',
        '1162498321.2dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162498321.2dzlu"]',
        '1162498369.29dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162498369.29dzlu"]',
        '1162498390.34dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162498390.34dzlu"]',
        '1162498400.56dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162498400.56dzlu"]',
        '1162498416.74dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162498416.74dzlu"]',
        '1162498428.64dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162498428.64dzlu"]',
        '1162498500.51dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162498500.51dzlu"]',
        '1162498514.14dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162498514.14dzlu"]',
        '1162498585.56dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162498585.56dzlu"]',
        '1162498611.99dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162498611.99dzlu"]',
        '1162498633.87dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162498633.87dzlu"]',
        '1162498653.28dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162498653.28dzlu"]',
        '1162501202.2dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501202.2dzlu"]',
        '1162501211.4dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501211.4dzlu"]',
        '1162501216.51dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501216.51dzlu"]',
        '1162501218.89dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501218.89dzlu"]',
        '1162501221.32dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501221.32dzlu"]',
        '1162501223.18dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501223.18dzlu"]',
        '1162501264.03dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501264.03dzlu"]',
        '1162501292.92dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501292.92dzlu"]',
        '1162501329.71dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501329.71dzlu"]',
        '1162501346.57dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501346.57dzlu"]',
        '1162501361.39dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501361.39dzlu"]',
        '1162501378.34dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501378.34dzlu"]',
        '1162501380.67dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501380.67dzlu"]',
        '1162501506.98dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501506.98dzlu"]',
        '1162501515.84dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501515.84dzlu"]',
        '1162501551.93dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501551.93dzlu"]',
        '1162501577.87dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501577.87dzlu"]',
        '1162501603.15dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501603.15dzlu"]',
        '1162501641.98dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501641.98dzlu"]',
        '1162501646.46dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501646.46dzlu"]',
        '1162501650.07dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501650.07dzlu"]',
        '1162501671.89dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501671.89dzlu"]',
        '1162501689.73dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501689.73dzlu"]',
        '1162501722.73dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501722.73dzlu"]',
        '1162501750.34dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501750.34dzlu"]',
        '1162501776.62dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501776.62dzlu"]',
        '1162501796.43dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501796.43dzlu"]',
        '1162501799.67dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501799.67dzlu"]',
        '1162501880.84dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162501880.84dzlu"]',
        '1162502780.21dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162502780.21dzlu"]',
        '1162504044.29dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504044.29dzlu"]',
        '1162504062.54dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504062.54dzlu"]',
        '1162504090.14dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504090.14dzlu"]',
        '1162504101.34dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504101.34dzlu"]',
        '1162504103.39dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504103.39dzlu"]',
        '1162504362.84dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504362.84dzlu"]',
        '1162504374.53dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504374.53dzlu"]',
        '1162504384.23dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504384.23dzlu"]',
        '1162504406.53dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504406.53dzlu"]',
        '1162504452.48dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504452.48dzlu"]',
        '1162504463.24dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504463.24dzlu"]',
        '1162504470.51dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504470.51dzlu"]',
        '1162504493.21dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504493.21dzlu"]',
        '1162504510.79dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504510.79dzlu"]',
        '1162504512.71dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504512.71dzlu"]',
        '1162504513.99dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504513.99dzlu"]',
        '1162504515.7dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504515.7dzlu"]',
        '1162504517.18dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504517.18dzlu"]',
        '1162504518.45dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504518.45dzlu"]',
        '1162504520.09dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504520.09dzlu"]',
        '1162504563.18dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504563.18dzlu"]',
        '1162504565.28dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504565.28dzlu"]',
        '1162504579.32dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504579.32dzlu"]',
        '1162504581.82dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504581.82dzlu"]',
        '1162504589.29dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504589.29dzlu"]',
        '1162504613.95dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504613.95dzlu"]',
        '1162504615.65dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504615.65dzlu"]',
        '1162504622.87dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504622.87dzlu"]',
        '1162504625.28dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504625.28dzlu"]',
        '1162504626.54dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504626.54dzlu"]',
        '1162504628.01dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504628.01dzlu"]',
        '1162504629.42dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504629.42dzlu"]',
        '1162504630.82dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504630.82dzlu"]',
        '1162504635.54dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504635.54dzlu"]',
        '1162504651.18dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504651.18dzlu"]',
        '1162504683.95dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504683.95dzlu"]',
        '1162504691.23dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504691.23dzlu"]',
        '1162504697.12dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504697.12dzlu"]',
        '1162504701.23dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504701.23dzlu"]',
        '1162504709.56dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504709.56dzlu"]',
        '1162504732.4dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504732.4dzlu"]',
        '1162504754.37dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504754.37dzlu"]',
        '1162504802.04dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504802.04dzlu"]',
        '1162504808.48dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504808.48dzlu"]',
        '1162504824.68dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162504824.68dzlu"]',
        '1162505050.93dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162505050.93dzlu"]',
        '1162505128.43dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162505128.43dzlu"]',
        '1162505210.81dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162505210.81dzlu"]',
        '1162505214.28dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162505214.28dzlu"]',
        '1162505293.49dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162505293.49dzlu"]',
        '1162505296.51dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162505296.51dzlu"]',
        '1162505308.45dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162505308.45dzlu"]',
        '1162505330.64dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162505330.64dzlu"]',
        '1162505333.48dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162505333.48dzlu"]',
        '1162575738.25dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162575738.25dzlu"]',
        '1162575755.71dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162575755.71dzlu"]',
        '1162575900.62dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162575900.62dzlu"]',
        '1162576043.68dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576043.68dzlu"]',
        '1162576078.71dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576078.71dzlu"]',
        '1162576335.14dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576335.14dzlu"]',
        '1162576483.87dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576483.87dzlu"]',
        '1162576530.06dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576530.06dzlu"]',
        '1162576533.54dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576533.54dzlu"]',
        '1162576597.46dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576597.46dzlu"]',
        '1162576602.98dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576602.98dzlu"]',
        '1162576619.82dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576619.82dzlu"]',
        '1162576649.89dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576649.89dzlu"]',
        '1162576682.79dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576682.79dzlu"]',
        '1162576722.81dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576722.81dzlu"]',
        '1162576805.98dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576805.98dzlu"]',
        '1162576816.26dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576816.26dzlu"]',
        '1162576895.73dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576895.73dzlu"]',
        '1162576950.03dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576950.03dzlu"]',
        '1162576969.61dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576969.61dzlu"]',
        '1162576986.5dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576986.5dzlu"]',
        '1162576998.25dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162576998.25dzlu"]',
        '1162577044.42dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162577044.42dzlu"]',
        '1162577094.82dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162577094.82dzlu"]',
        '1162577152.48dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162577152.48dzlu"]',
        '1162577320.84dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162577320.84dzlu"]',
        '1162577355.15dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162577355.15dzlu"]',
        '1162577566.42dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162577566.42dzlu"]',
        '1162577813.76dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162577813.76dzlu"]',
        '1162577835.12dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162577835.12dzlu"]',
        '1162577839.92dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162577839.92dzlu"]',
        '1162577843.75dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162577843.75dzlu"]',
        '1162577867.18dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162577867.18dzlu"]',
        '1162577870.71dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162577870.71dzlu"]',
        '1162577884.96dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162577884.96dzlu"]',
        '1162577982.15dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162577982.15dzlu"]',
        '1162577996.29dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162577996.29dzlu"]',
        '1162578006.14dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578006.14dzlu"]',
        '1162578016.5dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578016.5dzlu"]',
        '1162578019.04dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578019.04dzlu"]',
        '1162578024.62dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578024.62dzlu"]',
        '1162578025.75dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578025.75dzlu"]',
        '1162578026.78dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578026.78dzlu"]',
        '1162578038.0dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578038.0dzlu"]',
        '1162578047.75dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578047.75dzlu"]',
        '1162578056.12dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578056.12dzlu"]',
        '1162578057.4dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578057.4dzlu"]',
        '1162578070.86dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578070.86dzlu"]',
        '1162578075.4dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578075.4dzlu"]',
        '1162578081.51dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578081.51dzlu"]',
        '1162578094.39dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578094.39dzlu"]',
        '1162578096.17dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578096.17dzlu"]',
        '1162578108.39dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578108.39dzlu"]',
        '1162578113.9dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578113.9dzlu"]',
        '1162578121.26dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578121.26dzlu"]',
        '1162578126.61dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578126.61dzlu"]',
        '1162578259.32dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578259.32dzlu"]',
        '1162578426.64dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578426.64dzlu"]',
        '1162578793.03dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578793.03dzlu"]',
        '1162578861.75dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578861.75dzlu"]',
        '1162578920.61dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578920.61dzlu"]',
        '1162578961.18dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578961.18dzlu"]',
        '1162578998.36dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162578998.36dzlu"]',
        '1162579001.46dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579001.46dzlu"]',
        '1162579041.9dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579041.9dzlu"]',
        '1162579056.73dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579056.73dzlu"]',
        '1162579058.98dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579058.98dzlu"]',
        '1162579060.73dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579060.73dzlu"]',
        '1162579199.21dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579199.21dzlu"]',
        '1162579331.75dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579331.75dzlu"]',
        '1162579341.32dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579341.32dzlu"]',
        '1162579346.82dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579346.82dzlu"]',
        '1162579382.68dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579382.68dzlu"]',
        '1162579401.92dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579401.92dzlu"]',
        '1162579450.07dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579450.07dzlu"]',
        '1162579477.28dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579477.28dzlu"]',
        '1162579495.23dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579495.23dzlu"]',
        '1162579496.87dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579496.87dzlu"]',
        '1162579552.36dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579552.36dzlu"]',
        '1162579651.42dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579651.42dzlu"]',
        '1162579990.07dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162579990.07dzlu"]',
        '1162580050.34dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162580050.34dzlu"]',
        '1162580134.26dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162580134.26dzlu"]',
        '1162580160.11dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162580160.11dzlu"]',
        '1162580232.92dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162580232.92dzlu"]',
        '1162580882.43dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162580882.43dzlu"]',
        '1162580923.68dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162580923.68dzlu"]',
        '1162581117.26dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581117.26dzlu"]',
        '1162581120.68dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581120.68dzlu"]',
        '1162581126.39dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581126.39dzlu"]',
        '1162581133.0dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581133.0dzlu"]',
        '1162581141.04dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581141.04dzlu"]',
        '1162581144.36dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581144.36dzlu"]',
        '1162581145.98dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581145.98dzlu"]',
        '1162581162.73dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581162.73dzlu"]',
        '1162581164.37dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581164.37dzlu"]',
        '1162581164.98dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581164.98dzlu"]',
        '1162581166.56dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581166.56dzlu"]',
        '1162581167.39dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581167.39dzlu"]',
        '1162581168.25dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581168.25dzlu"]',
        '1162581168.79dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581168.79dzlu"]',
        '1162581169.65dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581169.65dzlu"]',
        '1162581170.36dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581170.36dzlu"]',
        '1162581171.11dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581171.11dzlu"]',
        '1162581171.96dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581171.96dzlu"]',
        '1162581173.79dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581173.79dzlu"]',
        '1162581176.57dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581176.57dzlu"]',
        '1162581177.9dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581177.9dzlu"]',
        '1162581181.67dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581181.67dzlu"]',
        '1162581182.32dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581182.32dzlu"]',
        '1162581183.29dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581183.29dzlu"]',
        '1162581183.73dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581183.73dzlu"]',
        '1162581184.18dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581184.18dzlu"]',
        '1162581185.78dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581185.78dzlu"]',
        '1162581187.11dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581187.11dzlu"]',
        '1162581188.48dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581188.48dzlu"]',
        '1162581188.82dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581188.82dzlu"]',
        '1162581189.76dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581189.76dzlu"]',
        '1162581190.51dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581190.51dzlu"]',
        '1162581192.04dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581192.04dzlu"]',
        '1162581194.96dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581194.96dzlu"]',
        '1162581195.62dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581195.62dzlu"]',
        '1162581196.4dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581196.4dzlu"]',
        '1162581198.9dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581198.9dzlu"]',
        '1162581199.73dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581199.73dzlu"]',
        '1162581201.07dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581201.07dzlu"]',
        '1162581201.68dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581201.68dzlu"]',
        '1162581202.34dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581202.34dzlu"]',
        '1162581230.31dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581230.31dzlu"]',
        '1162581230.92dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581230.92dzlu"]',
        '1162581234.92dzlu':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162581234.92dzlu"]',
        '1162600301.39sdnaik':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1162600301.39sdnaik"]',
        '1163119773.31sdnaik':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1163119773.31sdnaik"]',
        '1163119776.08sdnaik':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1163119776.08sdnaik"]',
        '1163130907.42sdnaik':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1163130907.42sdnaik"]',
        '1163130908.98sdnaik':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1163130908.98sdnaik"]',
        '1163462918.28sdnaik':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1163462918.28sdnaik"]',
        '1171314304.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171314304.0dxschafe"]',
        '1171314304.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171314304.0dxschafe"]',
        '1171315072.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315072.0dxschafe"]',
        '1171315200.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315200.0dxschafe"]',
        '1171315200.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315200.0dxschafe0"]',
        '1171315200.0dxschafe1':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315200.0dxschafe1"]',
        '1171315200.0dxschafe2':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315200.0dxschafe2"]',
        '1171315200.0dxschafe3':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315200.0dxschafe3"]',
        '1171315200.0dxschafe4':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315200.0dxschafe4"]',
        '1171315200.0dxschafe5':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315200.0dxschafe5"]',
        '1171315200.0dxschafe6':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315200.0dxschafe6"]',
        '1171315200.0dxschafe7':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315200.0dxschafe7"]',
        '1171315200.0dxschafe8':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315200.0dxschafe8"]',
        '1171315200.0dxschafe9':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315200.0dxschafe9"]',
        '1171315200.0dxschafe:':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315200.0dxschafe:"]',
        '1171315200.0dxschafe;':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315200.0dxschafe;"]',
        '1171315200.0dxschafe<':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315200.0dxschafe<"]',
        '1171315200.0dxschafe=':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315200.0dxschafe="]',
        '1171315712.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315712.0dxschafe"]',
        '1171315840.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315840.0dxschafe"]',
        '1171315968.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315968.0dxschafe"]',
        '1171315968.0dxschafe1':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171315968.0dxschafe1"]',
        '1171316096.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316096.0dxschafe"]',
        '1171316096.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316096.0dxschafe0"]',
        '1171316096.0dxschafe1':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316096.0dxschafe1"]',
        '1171316224.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316224.0dxschafe"]',
        '1171316224.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316224.0dxschafe0"]',
        '1171316224.0dxschafe1':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316224.0dxschafe1"]',
        '1171316224.0dxschafe2':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316224.0dxschafe2"]',
        '1171316224.0dxschafe3':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316224.0dxschafe3"]',
        '1171316224.0dxschafe4':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316224.0dxschafe4"]',
        '1171316224.0dxschafe5':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316224.0dxschafe5"]',
        '1171316224.0dxschafe6':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316224.0dxschafe6"]',
        '1171316352.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316352.0dxschafe"]',
        '1171316480.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316480.0dxschafe0"]',
        '1171316480.0dxschafe1':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316480.0dxschafe1"]',
        '1171316480.0dxschafe2':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316480.0dxschafe2"]',
        '1171316864.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316864.0dxschafe"]',
        '1171316864.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316864.0dxschafe"]',
        '1171316864.0dxschafe1':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316864.0dxschafe1"]',
        '1171316864.0dxschafe2':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316864.0dxschafe1"]',
        '1171317248.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171317248.0dxschafe"]',
        '1171317248.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171317248.0dxschafe"]',
        '1171317760.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171317760.0dxschafe"]',
        '1171317760.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171317760.0dxschafe0"]',
        '1171318016.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171318016.0dxschafe"]',
        '1171318016.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171318016.0dxschafe0"]',
        '1171318016.0dxschafe1':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171318016.0dxschafe1"]',
        '1171318016.0dxschafe2':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171318016.0dxschafe2"]',
        '1171318144.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171318144.0dxschafe"]',
        '1171318144.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171318144.0dxschafe0"]',
        '1171319168.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319168.0dxschafe"]',
        '1171319168.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319168.0dxschafe0"]',
        '1171319424.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319424.0dxschafe"]',
        '1171319424.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319424.0dxschafe0"]',
        '1171319424.0dxschafe1':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319424.0dxschafe1"]',
        '1171319424.0dxschafe2':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319424.0dxschafe2"]',
        '1171319552.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319552.0dxschafe0"]',
        '1171319680.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319680.0dxschafe"]',
        '1171319680.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319680.0dxschafe0"]',
        '1171319680.0dxschafe2':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319680.0dxschafe2"]',
        '1171319808.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319808.0dxschafe"]',
        '1171319808.0dxschafe2':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319808.0dxschafe2"]',
        '1171319808.0dxschafe4':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319808.0dxschafe4"]',
        '1171319808.0dxschafe5':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319808.0dxschafe5"]',
        '1171319808.0dxschafe6':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319808.0dxschafe6"]',
        '1171319936.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319936.0dxschafe"]',
        '1171319936.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319936.0dxschafe0"]',
        '1171319936.0dxschafe1':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319936.0dxschafe1"]',
        '1171319936.0dxschafe2':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319936.0dxschafe2"]',
        '1171319936.0dxschafe3':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319936.0dxschafe3"]',
        '1171319936.0dxschafe4':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171319936.0dxschafe4"]',
        '1171320064.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171320064.0dxschafe"]',
        '1171320064.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171320064.0dxschafe0"]',
        '1171320832.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171320832.0dxschafe"]',
        '1171320832.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171320832.0dxschafe0"]',
        '1171320832.0dxschafe1':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171320832.0dxschafe1"]',
        '1171320832.0dxschafe2':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171320832.0dxschafe2"]',
        '1171320832.0dxschafe3':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171320832.0dxschafe3"]',
        '1171320832.0dxschafe4':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171320832.0dxschafe4"]',
        '1171320960.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171320960.0dxschafe"]',
        '1171320960.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171320960.0dxschafe0"]',
        '1171321088.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171321088.0dxschafe"]',
        '1171321088.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171321088.0dxschafe0"]',
        '1171321216.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171321216.0dxschafe"]',
        '1171321216.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171321216.0dxschafe0"]',
        '1171321216.0dxschafe1':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171321216.0dxschafe1"]',
        '1171321216.0dxschafe2':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171321216.0dxschafe2"]',
        '1172863796.36kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1172863796.36kmuller"]',
        '1172863850.45kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1172863850.45kmuller"]',
        '1176186151.42mike':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1176186151.42mike"]',
        '1176258388.82kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1176258388.82kmuller"]',
        '1176258538.6kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1176258538.6kmuller"]',
        '1176258603.27kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1176258603.27kmuller"]',
        '1176258613.43kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1176258613.43kmuller"]',
        '1176258631.8kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1176258631.8kmuller"]',
        '1176258756.88kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1176258756.88kmuller"]',
        '1176258807.22kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1176258807.22kmuller"]',
        '1176258867.93kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1176258867.93kmuller"]',
        '1176258898.99kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1176258898.99kmuller"]',
        '1176258906.33kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1176258906.33kmuller"]',
        '1176258927.07kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1176258927.07kmuller"]',
        '1176258938.58kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1176258938.58kmuller"]',
        '1179791064.29Aholdun':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1179791064.29Aholdun"]',
        '1179791120.18Aholdun':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1179791120.18Aholdun"]',
        '1179791134.46Aholdun':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1179791134.46Aholdun"]',
        '1179791701.57Aholdun':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1179791701.57Aholdun"]',
        '1179791720.71Aholdun':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1179791720.71Aholdun"]',
        '1179793974.72Aholdun':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1179793974.72Aholdun"]',
        '1184716513.73kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184716513.73kmuller"]',
        '1184716531.9kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184716531.9kmuller"]',
        '1184716542.28kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184716542.28kmuller"]',
        '1184717296.78kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184717296.78kmuller"]',
        '1184717358.28kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184717358.28kmuller"]',
        '1184717384.58kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184717384.58kmuller"]',
        '1184717452.25kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184717452.25kmuller"]',
        '1184717774.17kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184717774.17kmuller"]',
        '1184717903.14kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184717903.14kmuller"]',
        '1184717982.65kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184717982.65kmuller"]',
        '1184718346.58kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184718346.58kmuller"]',
        '1184718408.0kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184718408.0kmuller"]',
        '1184718756.09kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184718756.09kmuller"]',
        '1184718783.67kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184718783.67kmuller"]',
        '1184718841.62kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316224.0dxschafe2"]["Objects"]["1184718841.62kmuller"]',
        '1184718870.54kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184718870.54kmuller"]',
        '1184718946.59kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184718946.59kmuller"]',
        '1184719009.84kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184719009.84kmuller"]',
        '1184719101.83kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184719101.83kmuller"]',
        '1184719164.21kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184719164.21kmuller"]',
        '1184719190.71kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184719190.71kmuller"]',
        '1184719277.87kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184719277.87kmuller"]',
        '1184719296.98kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184719296.98kmuller"]',
        '1184720985.21kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184720985.21kmuller"]',
        '1184721040.78kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184721040.78kmuller"]',
        '1184721161.87kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184721161.87kmuller"]',
        '1184721215.28kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184721215.28kmuller"]',
        '1184721233.95kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184721233.95kmuller"]',
        '1184721291.89kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184721291.89kmuller"]',
        '1184721406.87kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184721406.87kmuller"]',
        '1184721426.18kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184721426.18kmuller"]',
        '1184721812.36kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184721812.36kmuller"]',
        '1184721823.17kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184721823.17kmuller"]',
        '1184721880.11kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184721880.11kmuller"]',
        '1184721907.79kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184721907.79kmuller"]',
        '1184721953.51kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184721953.51kmuller"]',
        '1184721971.46kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184721971.46kmuller"]',
        '1184722024.71kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184722024.71kmuller"]',
        '1184722304.54kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184722304.54kmuller"]',
        '1184891648.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184891648.0dxschafe"]',
        '1184891776.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184891776.0dxschafe0"]',
        '1184891776.0dxschafe1':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1184891776.0dxschafe1"]',
        '1185921614.52kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1185921614.52kmuller"]',
        '1186006891.46kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1186006891.46kmuller"]',
        '1186007092.14kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1186007092.14kmuller"]',
        '1186007187.37kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1186007187.37kmuller"]',
        '1186007215.54kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1186007215.54kmuller"]',
        '1186007267.03kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1186007267.03kmuller"]',
        '1186007415.7kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1186007415.7kmuller"]',
        '1187913949.14akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187913949.14akelts"]',
        '1187914011.44akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187914011.44akelts"]',
        '1187914045.25akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187914045.25akelts"]',
        '1187914073.11akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187914073.11akelts"]',
        '1187914104.39akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187914104.39akelts"]',
        '1187914121.33akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187914121.33akelts"]',
        '1187914162.75akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187914162.75akelts"]',
        '1187914199.86akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187914199.86akelts"]',
        '1187914236.7akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187914236.7akelts"]',
        '1187914264.97akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187914264.97akelts"]',
        '1187914386.67akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187914386.67akelts"]',
        '1187914411.34akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187914411.34akelts"]',
        '1187914475.81akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187914475.81akelts"]',
        '1187914641.95akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187914641.95akelts"]',
        '1187914830.53akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187914830.53akelts"]',
        '1187914874.69akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187914874.69akelts"]',
        '1187993555.97akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187993555.97akelts"]',
        '1187993700.22akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187993700.22akelts"]',
        '1187995354.27akelts':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1187995354.27akelts"]',
        '1189212260.31kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1189212260.31kmuller"]',
        '1189212260.31kmuller0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1189212260.31kmuller"]',
        '1189456314.77kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1189212260.31kmuller"]["Objects"]["1189456314.77kmuller"]',
        '1189456366.97kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1189456366.97kmuller"]',
        '1189456447.08kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1189212260.31kmuller"]["Objects"]["1189456447.08kmuller"]',
        '1190666496.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1190666496.0dxschafe"]',
        '1190666880.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1190666880.0dxschafe"]',
        '1190741504.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1190741504.0dxschafe"]',
        '1190741504.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1190741504.0dxschafe"]',
        '1191629336.42kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1191629336.42kmuller"]',
        '1191629553.64kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1191629553.64kmuller"]',
        '1191629599.67kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1191629599.67kmuller"]',
        '1191629616.42kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1191629616.42kmuller"]',
        '1191629698.66kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1191629698.66kmuller"]',
        '1191629817.2kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1191629817.2kmuller"]',
        '1191629838.92kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1191629838.92kmuller"]',
        '1191629854.09kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1191629854.09kmuller"]',
        '1191629933.37kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1191629933.37kmuller"]',
        '1191629959.37kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1191629959.37kmuller"]',
        '1191629982.17kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1191629982.17kmuller"]',
        '1191630016.62kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1191630016.62kmuller"]',
        '1192043971.0kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192043971.0kmuller"]',
        '1192044061.55kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192044061.55kmuller"]',
        '1192044102.02kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192044102.02kmuller"]',
        '1192228480.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228480.0dxschafe"]',
        '1192228608.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228608.0dxschafe"]',
        '1192228608.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228608.0dxschafe0"]',
        '1192228608.0dxschafe1':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228608.0dxschafe1"]',
        '1192228608.0dxschafe2':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228608.0dxschafe2"]',
        '1192228608.0dxschafe3':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228608.0dxschafe3"]',
        '1192228608.0dxschafe4':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228608.0dxschafe4"]',
        '1192228608.0dxschafe5':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228608.0dxschafe5"]',
        '1192228608.0dxschafe6':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228608.0dxschafe6"]',
        '1192228608.0dxschafe7':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228608.0dxschafe7"]',
        '1192228608.0dxschafe8':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228608.0dxschafe8"]',
        '1192228736.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228736.0dxschafe"]',
        '1192228736.0dxschafe0':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228736.0dxschafe0"]',
        '1192228736.0dxschafe1':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228736.0dxschafe1"]',
        '1192228736.0dxschafe2':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228736.0dxschafe2"]',
        '1192228736.0dxschafe3':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228736.0dxschafe3"]',
        '1192228736.0dxschafe4':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228736.0dxschafe4"]',
        '1192228736.0dxschafe5':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192228736.0dxschafe5"]',
        '1192733824.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192733824.0dxschafe"]',
        '1192733952.0dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192733952.0dxschafe"]',
        '1192836222.09kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1192836222.09kmuller"]',
        '1201041675.97dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1190741504.0dxschafe"]["Objects"]["1201041675.97dxschafe"]',
        '1201041677.36dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1190741504.0dxschafe"]["Objects"]["1201041677.36dxschafe"]',
        '1201041677.5dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316864.0dxschafe"]["Objects"]["1201041677.5dxschafe"]',
        '1201041678.38dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171314304.0dxschafe"]["Objects"]["1201041678.38dxschafe"]',
        '1201041678.91dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1171316864.0dxschafe1"]["Objects"]["1201041678.91dxschafe"]',
        '1201041679.88dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1201041679.88dxschafe"]',
        '1201041679.89dxschafe':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1201041679.89dxschafe"]',
        '1210704118.17kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1210704118.17kmuller"]',
        '1210704165.86kmuller':
        '["Objects"]["1160614528.73sdnaik"]["Objects"]["1210704165.86kmuller"]'
    }
}
extraInfo = {
    'camPos': Point3(368.88, -551.862, 60.7199),
    'camHpr': VBase3(-91.2358, -26.5104, -1.90819e-06),
    'focalLength': 1.39999997616,
    'skyState': 2,
    'fog': 0
}
