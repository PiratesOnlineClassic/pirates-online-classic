# Embedded file name: pirates.leveleditor.worldData.del_fuego_area_cave_d_1
from pandac.PandaModules import Point3, VBase3, Vec4
objectStruct = {
    'AmbientColors': {
        -1: Vec4(0.447059, 0.447059, 0.415686, 1),
        0: Vec4(0.494118, 0.564706, 0.67451, 1),
        2: Vec4(0.74902, 0.737255, 0.737255, 1),
        4: Vec4(0.721569, 0.611765, 0.619608, 1),
        6: Vec4(0.437059, 0.446471, 0.556667, 1),
        8: Vec4(0.389216, 0.426275, 0.569608, 1)
    },
    'DirectionalColors': {
        -1: Vec4(0.717647, 0.721569, 0.72549, 1),
        0: Vec4(0.956863, 0.909804, 0.894118, 1),
        2: Vec4(0.764706, 0.764706, 0.764706, 1),
        4: Vec4(0.439216, 0.176471, 0, 1),
        6: Vec4(0.513726, 0.482353, 0.643137, 1),
        8: Vec4(0.447059, 0.439216, 0.541176, 1)
    },
    'FogColors': {
        -1: Vec4(0.870588, 0.87451, 0.823529, 1),
        0: Vec4(0.27451, 0.192157, 0.211765, 1),
        2: Vec4(0.0313726, 0.054902, 0.0784314, 1),
        4: Vec4(0.231373, 0.203922, 0.184314, 1),
        6: Vec4(0.156863, 0.219608, 0.329412, 0),
        8: Vec4(0.129412, 0.137255, 0.207843, 0)
    },
    'FogRanges': {
        0: 0.00019999999494757503,
        2: 0.0006000000284984708,
        4: 0.00039999998989515007,
        6: 0.0004,
        8: 0.0002
    },
    'Interact Links':
    [['1176249984.0dxschafe', '1176249856.0dxschafe', 'Bi-directional'],
     ['1176322304.0dxschafe3', '1176322048.0dxschafe0', 'Bi-directional'],
     ['1175816960.0dxschafe', '1175817216.0dxschafe0', 'Bi-directional'],
     ['1176322048.0dxschafe', '1176322176.0dxschafe0', 'Bi-directional'],
     ['1176322176.0dxschafe', '1176249984.0dxschafe1', 'Bi-directional'],
     ['1176322304.0dxschafe', '1176249984.0dxschafe2', 'Bi-directional'],
     ['1176322304.0dxschafe2', '1176322816.0dxschafe1', 'Bi-directional'],
     ['1176322816.0dxschafe', '1176322432.0dxschafe2', 'Bi-directional'],
     ['1187656704.0dxschafe0', '1176249984.0dxschafe0', 'Bi-directional']],
    'Objects': {
        '1167862588.52sdnaik': {
            'Type': 'Island Game Area',
            'Name': 'del_fuego_area_cave_d_1',
            'File': '',
            'Instanced': True,
            'Objects': {
                '1167889596.27sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_1',
                    'Hpr': VBase3(16.688, 0.0, 0.0),
                    'Pos': Point3(123.68, 4.822, 47.3),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1167889596.28sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_2',
                    'Hpr': VBase3(-155.353, 0.0, 0.0),
                    'Pos': Point3(740.592, 53.189, 56.852),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1167889596.31sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_3',
                    'Hpr': VBase3(164.008, 0.0, 0.0),
                    'Pos': Point3(539.448, -174.203, 39.295),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1175816960.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(419.323, -34.838, 7.801),
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
                '1175817216.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(362.669, -21.358, 7.801),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid EITC',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1175817216.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-98.096, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(376.691, -99.668, 29.212),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Vampire Bat',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0.0, 0.0, 0.65, 1.0),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176249856.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'attention',
                    'Hpr': VBase3(19.667, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '6.5663',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(284.51, -6.053, 17.602),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Navy - Veteran',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176249984.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(215.685, 14.373, 21.432),
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
                '1176249984.0dxschafe0': {
                    'Type': 'Object Spawn Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(248.193, -32.923, 16.732),
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
                '1176249984.0dxschafe1': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(512.477, 76.924, 12.235),
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
                '1176249984.0dxschafe2': {
                    'Type': 'Object Spawn Node',
                    'Hpr': VBase3(-179.291, 0.0, 0.0),
                    'Pos': Point3(410.356, 210.636, 12.235),
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
                '1176249984.0dxschafe3': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(35.595, 0.0, 0.0),
                    'Pos': Point3(446.426, 260.517, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_1long'
                    }
                },
                '1176250112.0dxschafe': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(-50.824, 0.0, 0.0),
                    'Pos': Point3(500.017, 221.115, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_2long'
                    }
                },
                '1176250112.0dxschafe0': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(-53.765, 0.0, 0.0),
                    'Pos': Point3(434.087, 257.631, 12.233),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_2long'
                    }
                },
                '1176250112.0dxschafe1': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(36.418, 0.0, 0.0),
                    'Objects': {
                        '1176322432.0dxschafe1': {
                            'Type': 'Spawn Node',
                            'Aggro Radius': '12.0000',
                            'AnimSet': 'default',
                            'Hpr': VBase3(-159.418, 0.0, 0.0),
                            'Min Population': '1',
                            'Patrol Radius': '1.7289',
                            'Pause Chance': 100,
                            'Pause Duration': '30',
                            'Pos': Point3(-13.383, -11.71, 12.108),
                            'PoseAnim': '',
                            'PoseFrame': '',
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Spawnables': 'Low EITC',
                            'Start State': 'Idle',
                            'StartFrame': '0',
                            'Team': 'default',
                            'TrailFX': 'None',
                            'Visual': {
                                'Color': (0, 0, 0.65, 1),
                                'Model': 'models/misc/smiley'
                            }
                        },
                        '1187657344.0dxschafe': {
                            'Type': 'Rock',
                            'DisableCollision': False,
                            'Hpr': VBase3(49.884, 0.0, 0.0),
                            'Pos': Point3(418.659, 234.433, 12.234),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/rockpile_cave_volcano'
                            }
                        }
                    },
                    'Pos': Point3(424.111, 244.061, 12.234),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_1long'
                    }
                },
                '1176250240.0dxschafe': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(-54.549, 0.0, 0.0),
                    'Pos': Point3(428.778, 263.991, 27.743),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_2long'
                    }
                },
                '1176250240.0dxschafe0': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(-50.797, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(500.039, 220.638, 27.987),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.4000000059604645, 0.4000000059604645,
                                  0.4000000059604645, 1.0),
                        'Model':
                        'models/islands/pier_scaffold_2long'
                    }
                },
                '1176250368.0dxschafe': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(-53.443, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(391.112, 225.117, 12.236),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_2long'
                    }
                },
                '1176250368.0dxschafe0': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(39.791, 0.0, 0.0),
                    'Objects': {
                        '1176322688.0dxschafe': {
                            'Type': 'Searchable Container',
                            'Aggro Radius': 5.0,
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(-29.669, -2.032, 12.064),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Color': (0.5, 0.5, 0.5, 1.0),
                                'Model': 'models/props/barrel'
                            },
                            'searchTime': '10.0',
                            'type': 'Crate'
                        }
                    },
                    'Pos': Point3(566.555, 242.533, 12.949),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_2long'
                    }
                },
                '1176250752.0dxschafe': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1176250752.0dxschafe0',
                    'Hpr': VBase3(-86.754, 0.0, 0.0),
                    'Objects': {
                        '1205365556.53kmuller': {
                            'Type': 'Door Locator Node',
                            'Name': 'door_locator',
                            'Hpr': VBase3(-180.0, 0.0, 0.0),
                            'Pos': Point3(0.162, -4.354, 0.599),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(559.943, 146.147, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/shanty_npc_house_combo_G',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1176250752.0dxschafe1': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1176250752.0dxschafe2',
                    'Hpr': VBase3(42.161, 0.0, 0.0),
                    'Objects': {
                        '1205365549.31kmuller': {
                            'Type': 'Door Locator Node',
                            'Name': 'door_locator',
                            'Hpr': VBase3(-180.0, 0.0, 0.0),
                            'Pos': Point3(0.313, -4.016, 1.444),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(343.231, 52.923, 7.372),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/shanty_npc_house_combo_J',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1176250752.0dxschafe3': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1176250752.0dxschafe4',
                    'Hpr': VBase3(-51.272, 0.0, 0.0),
                    'Objects': {
                        '1176322304.0dxschafe1': {
                            'Type': 'Spawn Node',
                            'Aggro Radius': '3.9157',
                            'AnimSet': 'default',
                            'Hpr': VBase3(-149.11, 0.0, 0.0),
                            'Min Population': '1',
                            'Patrol Radius': '1.6627',
                            'Pause Chance': 100,
                            'Pause Duration': 30,
                            'Pos': Point3(13.513, -4.044, 15.548),
                            'PoseAnim': '',
                            'PoseFrame': '',
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Spawnables': 'Mid Navy',
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
                    'Pos': Point3(511.449, 202.737, 9.013),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/shanty_npc_house_combo_D',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1176251008.0dxschafe': {
                    'Type': 'Building Exterior',
                    'File': '',
                    'ExtUid': '1176251008.0dxschafe0',
                    'Hpr': VBase3(125.912, 0.0, 0.0),
                    'Objects': {
                        '1205365552.68kmuller': {
                            'Type': 'Door Locator Node',
                            'Name': 'door_locator',
                            'Hpr': VBase3(-180.0, 0.0, 0.0),
                            'Pos': Point3(0.161, -4.399, 16.391),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(406.226, 210.147, 8.834),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Name': '',
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Door': 'models/buildings/shanty_guildhall_door',
                        'Interior':
                        'models/buildings/interior_shanty_guildhall',
                        'Model': 'models/buildings/shanty_npc_house_combo_E',
                        'SignImage':
                        'models/buildings/sign1_eng_a_icon_blacksmith'
                    }
                },
                '1176251264.0dxschafe': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(-143.832, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(401.513, 210.854, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/islands/pier_scaffold_landing'
                    }
                },
                '1176251264.0dxschafe0': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(-142.141, 0.0, 0.0),
                    'Pos': Point3(457.864, 251.467, 12.234),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_landing'
                    }
                },
                '1176251392.0dxschafe': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(129.273, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(415.372, 190.262, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_2long'
                    }
                },
                '1176251392.0dxschafe0': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(129.675, 0.0, 0.0),
                    'Objects': {
                        '1187657216.0dxschafe8': {
                            'Type': 'Rock',
                            'DisableCollision': False,
                            'Hpr': VBase3(0.0, 0.0, 0.0),
                            'Pos': Point3(457.986, 150.255, 12.235),
                            'Scale': VBase3(1.0, 1.0, 1.0),
                            'Visual': {
                                'Model': 'models/props/rockpile_cave_volcano'
                            }
                        }
                    },
                    'Pos': Point3(449.896, 148.397, 12.233),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_2long'
                    }
                },
                '1176251392.0dxschafe1': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(129.872, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(484.508, 106.828, 12.234),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_1long'
                    }
                },
                '1176251392.0dxschafe2': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(-141.753, 0.0, 0.0),
                    'Pos': Point3(449.837, 245.496, 27.818),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_2long'
                    }
                },
                '1176251648.0dxschafe': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(-51.553, 0.0, 0.0),
                    'Pos': Point3(444.13, 244.717, 27.767),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_1long'
                    }
                },
                '1176251776.0dxschafe': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(38.464, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(477.436, 284.62, 43.765),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_2long'
                    }
                },
                '1176254720.0dxschafe': {
                    'Type': 'Crane',
                    'Hpr': VBase3(-140.322, 0.0, 0.0),
                    'Pos': Point3(417.556, 187.805, 5.472),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/Crane_A'
                    }
                },
                '1176254848.0dxschafe': {
                    'Type': 'Crane',
                    'Hpr': VBase3(-144.498, 0.0, 0.0),
                    'Pos': Point3(554.696, 225.121, 27.855),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/Crane_B'
                    }
                },
                '1176254848.0dxschafe0': {
                    'Type': 'Crane',
                    'Hpr': VBase3(42.832, 0.0, 0.0),
                    'Pos': Point3(505.073, 92.4, 8.548),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/Crane'
                    }
                },
                '1176254976.0dxschafe': {
                    'Type': 'Crane',
                    'Hpr': VBase3(130.409, 0.0, 0.0),
                    'Pos': Point3(427.978, 253.529, 12.087),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/Crane'
                    }
                },
                '1176255232.0dxschafe': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(-48.163, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(514.666, 92.431, 12.236),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_end'
                    }
                },
                '1176317440.0dxschafe': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(-48.163, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(506.992, 212.667, 28.019),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_end'
                    }
                },
                '1176320128.0dxschafe': {
                    'Type': 'Military_props',
                    'Hpr': VBase3(38.564, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(479.056, 285.893, 12.234),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/islands/pier_scaffold_1long'
                    }
                },
                '1176322048.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(534.338, 224.134, 12.234),
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
                '1176322048.0dxschafe0': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(320.23, 37.338, 7.801),
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
                '1176322176.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '6.5000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(461.857, 87.428, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Navy',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176322176.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'idleB',
                    'Hpr': VBase3(105.416, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '1.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(552.231, 151.205, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'EITC - Assassin',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176322304.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'idleC',
                    'Hpr': VBase3(-59.316, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '1.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(427.065, 200.584, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Navy',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176322304.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-46.496, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '1.2651',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(458.299, 160.303, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low EITC',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176322304.0dxschafe2': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-123.674, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '1.6627',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(355.546, 48.719, 7.801),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low EITC',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176322304.0dxschafe3': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-126.557, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '1.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(309.199, 20.262, 7.801),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Navy',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176322304.0dxschafe4': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '15.1515',
                    'AnimSet': 'attention_cutlass',
                    'Hpr': VBase3(-134.096, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '1.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(582.995, 95.984, 38.064),
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
                '1176322304.0dxschafe5': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '2.1265',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(505.991, 106.094, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High EITC',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176322432.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-162.979, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '2.0602',
                    'Pause Chance': 100,
                    'Pause Duration': '30',
                    'Pos': Point3(416.439, 180.092, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Navy',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176322432.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(129.273, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '1.9277',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(418.211, 81.419, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Mid EITC',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176322432.0dxschafe2': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(140.028, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '1.7289',
                    'Pause Chance': 100,
                    'Pause Duration': '30',
                    'Pos': Point3(493.283, 204.522, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'High Navy',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176322816.0dxschafe': {
                    'Type': 'Searchable Container',
                    'Aggro Radius': 5.0,
                    'Hpr': VBase3(154.745, 0.0, 0.0),
                    'Pos': Point3(505.384, 188.463, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/barrel'
                    },
                    'searchTime': '10.0',
                    'type': 'Crate'
                },
                '1176322816.0dxschafe0': {
                    'Type': 'Searchable Container',
                    'Aggro Radius': 5.0,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(505.361, 99.419, 24.159),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.699999988079071, 0.699999988079071,
                                  0.699999988079071, 1.0),
                        'Model':
                        'models/props/barrel'
                    },
                    'searchTime': '10.0',
                    'type': 'Crate'
                },
                '1176322816.0dxschafe1': {
                    'Type': 'Searchable Container',
                    'Aggro Radius': 5.0,
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(374.448, 68.707, 7.801),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/barrel'
                    },
                    'searchTime': '10.0',
                    'type': 'Crate'
                },
                '1176322816.0dxschafe2': {
                    'Type': 'Searchable Container',
                    'Aggro Radius': 5.0,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(401.663, 224.288, 24.272),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/barrel'
                    },
                    'searchTime': '10.0',
                    'type': 'Crate'
                },
                '1176322816.0dxschafe3': {
                    'Type': 'Searchable Container',
                    'Aggro Radius': 5.0,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(461.082, 265.829, 24.246),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/barrel'
                    },
                    'searchTime': '10.0',
                    'type': 'Crate'
                },
                '1176322816.0dxschafe4': {
                    'Type': 'Searchable Container',
                    'Aggro Radius': 5.0,
                    'Hpr': VBase3(-74.81, 0.0, 0.0),
                    'Pos': Point3(333.674, 41.289, 7.722),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.3100000023841858, 0.25999999046325684,
                                  0.25, 1.0),
                        'Model':
                        'models/props/crate_04'
                    },
                    'searchTime': '10.0',
                    'type': 'Crate'
                },
                '1176322816.0dxschafe5': {
                    'Type': 'Searchable Container',
                    'Aggro Radius': 5.0,
                    'Hpr': VBase3(37.461, 0.0, 0.0),
                    'Pos': Point3(487.974, 216.164, 24.565),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.4000000059604645, 0.4000000059604645,
                                  0.4000000059604645, 1.0),
                        'Model':
                        'models/props/crate_04'
                    },
                    'searchTime': '10.0',
                    'type': 'Crate'
                },
                '1176322816.0dxschafe6': {
                    'Type': 'Searchable Container',
                    'Aggro Radius': 5.0,
                    'Hpr': VBase3(-51.268, 0.0, 0.0),
                    'Pos': Point3(531.826, 212.008, 25.155),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/crate_04'
                    },
                    'searchTime': '10.0',
                    'type': 'Crate'
                },
                '1176322816.0dxschafe7': {
                    'Type': 'Searchable Container',
                    'Aggro Radius': 5.0,
                    'Hpr': VBase3(-143.77, 0.0, 0.0),
                    'Pos': Point3(413.52, 196.469, 24.359),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.4000000059604645, 0.4000000059604645,
                                  0.4000000059604645, 1.0),
                        'Model':
                        'models/props/crate_04'
                    },
                    'searchTime': '10.0',
                    'type': 'Crate'
                },
                '1176322816.0dxschafe8': {
                    'Type': 'Searchable Container',
                    'Aggro Radius': 5.0,
                    'Hpr': VBase3(40.371, 0.0, 0.0),
                    'Pos': Point3(466.52, 139.129, 24.17),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/crate_04'
                    },
                    'searchTime': '10.0',
                    'type': 'Crate'
                },
                '1176323200.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': VBase3(129.273, 0.0, 0.0),
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(431.349, 198.492, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176323328.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(490.216, 95.038, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176323328.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(551.386, 206.273, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176323456.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': VBase3(38.464, 0.0, 0.0),
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(457.565, 243.873, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179433459.59Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-36.432, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(325.562, -72.795, 12.975),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179433471.55Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(428.41, -135.588, 28.869),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179433481.05Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(86.288, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(476.299, -165.165, 22.35),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179433494.72Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(93.571, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(440.395, 21.813, 7.801),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179433506.16Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(4.521, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(566.544, 57.282, 35.371),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179433521.63Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-83.327, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(404.208, 135.878, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179433548.52Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-98.534, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(165.437, 72.523, 21.874),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179433561.2Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-45.205, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(151.053, 18.54, 46.91),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179433672.64Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(31.074, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(633.109, 33.973, 41.063),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179433739.83Aholdun': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(79.352, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(685.847, 21.345, 41.457),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1187045504.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(40.654, 0.0, 0.0),
                    'Pos': Point3(451.049, 249.588, 40.193),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1187045504.0dxschafe0': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(40.654, 0.0, 0.0),
                    'Pos': Point3(443.539, 243.207, 40.192),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1187045504.0dxschafe1': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(40.654, 0.0, 0.0),
                    'Pos': Point3(436.345, 236.793, 40.193),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1187045760.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-51.223, 0.0, 0.0),
                    'Pos': Point3(484.778, 225.308, 39.972),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1187045760.0dxschafe0': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-51.223, 0.0, 0.0),
                    'Pos': Point3(490.953, 217.909, 39.972),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1187045760.0dxschafe1': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-51.223, 0.0, 0.0),
                    'Pos': Point3(497.084, 210.193, 39.972),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1187045760.0dxschafe2': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(39.364, 0.0, 0.0),
                    'Pos': Point3(558.169, 222.168, 24.921),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1187045760.0dxschafe3': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(39.364, 0.0, 0.0),
                    'Pos': Point3(565.505, 228.418, 24.921),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1187045760.0dxschafe4': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(39.364, 0.0, 0.0),
                    'Pos': Point3(573.157, 234.628, 24.921),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1187045888.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(39.551, 0.0, 0.0),
                    'Pos': Point3(364.694, 60.799, 8.05),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cave_conveyor_tower'
                    }
                },
                '1187046016.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-79.809, 0.0, 0.0),
                    'Pos': Point3(559.057, 170.44, 12.234),
                    'Scale': VBase3(1.308, 1.308, 1.308),
                    'Visual': {
                        'Model': 'models/props/cave_conveyor_tower'
                    }
                },
                '1187046144.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-53.694, 0.0, 0.0),
                    'Pos': Point3(476.13, 275.584, 39.53),
                    'Scale': VBase3(1.151, 1.151, 1.151),
                    'Visual': {
                        'Model': 'models/props/cave_conveyor_tower'
                    }
                },
                '1187046272.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(129.359, 0.0, 0.0),
                    'Pos': Point3(369.087, 242.213, 25.139),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1187046656.0dxschafe': {
                    'Type': 'Simple Fort',
                    'Hpr': VBase3(-167.268, 0.813, -1.63),
                    'Objects': {},
                    'Pos': Point3(286.001, -12.001, 16.978),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/buildings/fort_guardhouse'
                    }
                },
                '1187656320.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-31.229, 0.0, 0.0),
                    'Pos': Point3(424.671, -2.335, 5.592),
                    'Scale': VBase3(1.74, 1.74, 1.74),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave_volcano'
                    }
                },
                '1187656320.0dxschafe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-31.229, 0.0, 0.0),
                    'Pos': Point3(383.155, 56.019, 7.801),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave_volcano'
                    }
                },
                '1187656320.0dxschafe2': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-99.3, 0.0, 0.0),
                    'Pos': Point3(395.952, -9.31, 7.801),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave_volcano'
                    }
                },
                '1187656448.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-31.229, 0.0, 0.0),
                    'Pos': Point3(335.89, -7.945, 7.801),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave_volcano'
                    }
                },
                '1187656448.0dxschafe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-74.671, 0.0, 0.0),
                    'Pos': Point3(351.827, 5.133, 6.709),
                    'Scale': VBase3(1.527, 1.527, 1.527),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave_volcano'
                    }
                },
                '1187656448.0dxschafe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(9.024, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(415.55, 122.62, 12.234),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave_volcano'
                    }
                },
                '1187656448.0dxschafe2': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-54.143, 0.0, 0.0),
                    'Pos': Point3(424.68, 156.615, 12.234),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave_volcano'
                    }
                },
                '1187656448.0dxschafe3': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-75.756, 0.0, 0.0),
                    'Pos': Point3(443.521, 100.043, 12.234),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave_volcano'
                    }
                },
                '1187656448.0dxschafe4': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(136.683, 0.0, 0.0),
                    'Pos': Point3(543.099, 164.075, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187656448.0dxschafe5': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-31.229, 0.0, 0.0),
                    'Pos': Point3(553.166, 195.333, 12.234),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187656448.0dxschafe6': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(37.675, 0.0, 0.0),
                    'Pos': Point3(497.897, 244.224, 12.234),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave_volcano'
                    }
                },
                '1187656448.0dxschafe7': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-31.229, 0.0, 0.0),
                    'Pos': Point3(475.973, 257.702, 12.234),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave_volcano'
                    }
                },
                '1187656704.0dxschafe': {
                    'Type': 'Simple Fort',
                    'Hpr': VBase3(11.264, 0.588, 0.0),
                    'Objects': {},
                    'Pos': Point3(280.633, 17.425, 16.774),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/buildings/fort_guardhouse'
                    }
                },
                '1187656704.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '15.1515',
                    'AnimSet': 'attention',
                    'Hpr': VBase3(-165.627, -0.587, 0.032),
                    'Min Population': '1',
                    'Patrol Radius': '1.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(282.303, 11.555, 17.158),
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
                '1187657088.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(514.751, 180.026, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187657216.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(74.725, 0.0, 0.0),
                    'Pos': Point3(449.619, 233.87, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187657216.0dxschafe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(397.091, 112.692, 12.234),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187657216.0dxschafe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(407.587, 149.23, 12.234),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187657216.0dxschafe2': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(443.009, 81.455, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187657216.0dxschafe3': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(61.517, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(404.951, 19.314, 7.801),
                    'Scale': VBase3(1.148, 1.148, 1.148),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187657216.0dxschafe4': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(442.231, -15.795, 7.801),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187657216.0dxschafe5': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(329.624, -30.99, 7.801),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187657216.0dxschafe6': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(415.083, -46.162, 7.801),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187657216.0dxschafe7': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(484.179, 88.734, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187657216.0dxschafe9': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(49.884, 0.0, 0.0),
                    'Pos': Point3(472.557, 132.13, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187657344.0dxschafe0': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(49.884, 0.0, 0.0),
                    'Pos': Point3(415.134, 228.901, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187657344.0dxschafe1': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(19.215, 0.0, 0.0),
                    'Pos': Point3(490.718, 262.026, 12.234),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187657344.0dxschafe2': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(19.215, 0.0, 0.0),
                    'Pos': Point3(522.744, 229.571, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187657344.0dxschafe3': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(19.215, 0.0, 0.0),
                    'Objects': {
                        '1205365699.31kmuller': {
                            'Type': 'Collision Barrier',
                            'DisableCollision': False,
                            'Hpr': VBase3(0.387, 0.0, 0.0),
                            'Pos': Point3(-7.758, 0.103, -0.607),
                            'Scale': VBase3(0.669, 1.0, 1.644),
                            'Visual': {
                                'Model': 'models/misc/coll_plane_barrier'
                            }
                        }
                    },
                    'Pos': Point3(381.668, 68.846, 7.801),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187657344.0dxschafe4': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-106.623, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(420.496, 37.452, 7.801),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187657344.0dxschafe5': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(112.353, 0.0, 0.0),
                    'Pos': Point3(525.049, 103.02, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187657600.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-74.058, 0.0, 0.0),
                    'Pos': Point3(412.569, 42.035, 7.801),
                    'Scale': VBase3(0.703, 0.703, 0.703),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1187657600.0dxschafe0': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-74.058, 0.0, 0.0),
                    'Pos': Point3(324.197, -10.973, 7.801),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1187657600.0dxschafe1': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-102.374, 0.0, 0.0),
                    'Pos': Point3(408.944, 164.039, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/cave_mine_cart'
                    }
                },
                '1187657728.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-102.374, 0.0, 0.0),
                    'Pos': Point3(509.029, 172.85, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/wheelbarrow'
                    }
                },
                '1187657728.0dxschafe0': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-102.374, 0.0, 0.0),
                    'Pos': Point3(433.579, 153.395, 12.235),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/wheelbarrow'
                    }
                },
                '1187657728.0dxschafe1': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-102.374, 0.0, 0.0),
                    'Pos': Point3(394.601, 15.977, 7.801),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/wheelbarrow'
                    }
                },
                '1187657728.0dxschafe2': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(82.816, 0.0, 0.0),
                    'Pos': Point3(357.458, -6.035, 7.801),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/wheelbarrow'
                    }
                },
                '1187657728.0dxschafe3': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-166.351, 0.0, 0.0),
                    'Pos': Point3(454.819, 83.93, 12.234),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/wheelbarrow'
                    }
                },
                '1187657728.0dxschafe4': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-102.374, 0.0, 0.0),
                    'Pos': Point3(406.174, -39.921, 7.801),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/wheelbarrow'
                    }
                },
                '1187657728.0dxschafe7': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-48.122, 0.0, 0.0),
                    'Pos': Point3(373.647, 62.402, 19.561),
                    'Scale': VBase3(1.513, 1.513, 1.513),
                    'Visual': {
                        'Model': 'models/props/cave_big_wheel'
                    }
                },
                '1187657856.0dxschafe': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-74.619, 0.0, 0.0),
                    'Pos': Point3(552.632, 163.22, 30.396),
                    'Scale': VBase3(1.513, 1.513, 1.513),
                    'Visual': {
                        'Model': 'models/props/cave_big_wheel'
                    }
                },
                '1187657856.0dxschafe0': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-48.559, 0.0, 0.0),
                    'Pos': Point3(353.329, 68.101, 7.324),
                    'Scale': VBase3(2.975, 2.975, 2.975),
                    'Visual': {
                        'Model': 'models/props/cave_big_wheel'
                    }
                },
                '1187658112.0dxschafe0': {
                    'Type': 'Mining_props',
                    'Hpr': VBase3(-48.122, 0.0, 0.0),
                    'Pos': Point3(363.973, 55.275, 16.181),
                    'Scale': VBase3(1.859, 1.859, 1.859),
                    'Visual': {
                        'Model': 'models/props/cave_big_wheel'
                    }
                },
                '1187658240.0dxschafe': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'shovel',
                    'CustomModel': 'None',
                    'HelpID': 'NONE',
                    'Hpr': VBase3(116.748, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(414.84, -3.671, 7.801),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'ShopID': 'PORT_ROYAL_DEFAULTS',
                    'Start State': 'Walk',
                    'StartFrame': '0',
                    'Team': 'Villager',
                    'TrailFX': 'None'
                },
                '1187658240.0dxschafe0': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'axe_chop',
                    'CustomModel': 'None',
                    'Hpr': VBase3(-90.882, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(396.808, 22.933, 7.801),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Walk',
                    'StartFrame': '0',
                    'Team': 'Villager',
                    'TrailFX': 'None'
                },
                '1187658240.0dxschafe1': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'shovel',
                    'CustomModel': 'None',
                    'Hpr': VBase3(120.909, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(377.142, 51.921, 7.801),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Walk',
                    'StartFrame': '0',
                    'Team': 'Villager',
                    'TrailFX': 'None'
                },
                '1187658368.0dxschafe': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'shovel',
                    'CustomModel': 'None',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(361.084, -4.183, 7.801),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Walk',
                    'StartFrame': '0',
                    'Team': 'Villager',
                    'TrailFX': 'None'
                },
                '1187658368.0dxschafe0': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'axe_chop',
                    'CustomModel': 'None',
                    'Hpr': VBase3(166.829, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(331.505, -20.295, 7.801),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Walk',
                    'StartFrame': '0',
                    'Team': 'Villager',
                    'TrailFX': 'None'
                },
                '1187658368.0dxschafe1': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'shovel',
                    'CustomModel': 'None',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(420.159, 130.837, 12.235),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Walk',
                    'StartFrame': '0',
                    'Team': 'Villager',
                    'TrailFX': 'None'
                },
                '1187658496.0dxschafe': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'shovel',
                    'CustomModel': 'None',
                    'HelpID': 'NONE',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(445.724, 90.742, 12.234),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'ShopID': 'PORT_ROYAL_DEFAULTS',
                    'Start State': 'Walk',
                    'StartFrame': '0',
                    'Team': 'Villager',
                    'TrailFX': 'None'
                },
                '1187658496.0dxschafe0': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'shovel',
                    'CustomModel': 'None',
                    'Hpr': VBase3(131.085, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(503.69, 176.954, 12.234),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Walk',
                    'StartFrame': '0',
                    'Team': 'Villager',
                    'TrailFX': 'None'
                },
                '1187658496.0dxschafe1': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'shovel',
                    'CustomModel': 'None',
                    'Hpr': VBase3(-132.966, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(450.596, 224.491, 12.234),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Walk',
                    'StartFrame': '0',
                    'Team': 'Villager',
                    'TrailFX': 'None'
                },
                '1187732480.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(109.772, 1.798, -1.181),
                    'Objects': {},
                    'Pos': Point3(394.977, 16.766, 9.281),
                    'Scale': VBase3(0.181, 0.181, 0.181),
                    'Visual': {
                        'Model': 'models/props/rockpile_cave_volcano'
                    }
                },
                '1187732608.0dxschafe': {
                    'Type': 'Rock',
                    'DisableCollision': False,
                    'Hpr': VBase3(-74.671, 0.0, 0.0),
                    'Pos': Point3(357.131, -7.06, 9.328),
                    'Scale': VBase3(0.199, 0.199, 0.199),
                    'Visual': {
                        'Model': 'models/props/dirt_pile_cave_volcano'
                    }
                },
                '1189548928.0dxschafe': {
                    'Type': 'Arch',
                    'Hpr': VBase3(-30.591, 0.0, 0.0),
                    'Pos': Point3(340.915, -50.312, 10.041),
                    'Scale': VBase3(0.819, 0.819, 0.819),
                    'Visual': {
                        'Color': (0.35, 0.44, 0.4, 1.0),
                        'Model': 'models/buildings/spanish_archC'
                    }
                },
                '1189549568.0dxschafe': {
                    'Type': 'Effect Node',
                    'EffectName': 'steam_effect',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(694.411, 73.154, 51.181),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189549696.0dxschafe': {
                    'Type': 'Effect Node',
                    'EffectName': 'steam_effect',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(675.746, 64.892, 33.676),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189549696.0dxschafe0': {
                    'Type': 'Effect Node',
                    'EffectName': 'steam_effect',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(654.959, -19.676, 33.207),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189549824.0dxschafe': {
                    'Type': 'Effect Node',
                    'EffectName': 'fireplace_effect',
                    'Hpr': VBase3(0.0, 2.379, 0.0),
                    'Pos': Point3(180.57, 25.474, 60.395),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189549952.0dxschafe1': {
                    'Type': 'Effect Node',
                    'EffectName': 'fireplace_effect',
                    'Hpr': VBase3(0.0, 2.379, 0.0),
                    'Pos': Point3(157.443, 46.69, 62.812),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189550336.0dxschafe': {
                    'Type': 'Effect Node',
                    'EffectName': 'steam_effect',
                    'Hpr': VBase3(0.0, 0.878, 0.0),
                    'Pos': Point3(722.734, 42.998, 57.38),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189551232.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '0.0000',
                    'AnimSet': 'attack_sword_slash',
                    'Hpr': VBase3(185.672, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '1.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(207.571, 51.415, 21.591),
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
                '1189551360.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '0.0000',
                    'AnimSet': 'attack_sword_cleave',
                    'Hpr': VBase3(2.027, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '1.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(207.564, 43.811, 21.567),
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
                '1189551488.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '0.0000',
                    'AnimSet': 'attack_sword_cleave',
                    'Hpr': VBase3(-81.281, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '1.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(198.745, 69.104, 21.692),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Undead - Corpse',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1189551488.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '0.0000',
                    'AnimSet': 'attack_sword_lunge',
                    'Hpr': VBase3(80.064, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '1.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(208.789, 68.733, 21.639),
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
                '1192671104.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(427.209, -118.457, 28.912),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192671104.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(439.246, -170.262, 28.738),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192671104.0dxschafe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(484.842, -167.325, 20.886),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1205365556.89kmuller': {
                    'Type': 'Door Locator Node',
                    'Name': 'door_locator',
                    'Hpr': VBase3(-180.0, 0.0, 0.0),
                    'Pos': Point3(0.162, -4.354, 0.599),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1205365635.84kmuller': {
                    'Type': 'Barrel',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(370.837, 67.142, 7.792),
                    'Scale': VBase3(0.722, 0.722, 0.722),
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1.0),
                        'Model': 'models/props/barrel_worn'
                    }
                },
                '1219339266.79mtucker': {
                    'Type': 'NavySailor',
                    'AnimSet': 'default',
                    'AvId': 1,
                    'AvTrack': 0,
                    'Boss': True,
                    'DNA': '1219339266.79mtucker',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'NavyFaction': 'TradingCo',
                    'Patrol Radius': '4.6627',
                    'Pos': Point3(427.321, -32.485, 10.963),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'TrailFX': 'None'
                },
                '1219352693.09mtucker': {
                    'Type': 'NavySailor',
                    'Aggro Radius': '3.9157',
                    'AnimSet': 'default',
                    'AvId': 4,
                    'AvTrack': 0,
                    'Boss': True,
                    'DNA': '1219352693.09mtucker',
                    'Hpr': VBase3(139.058, 0.0, 0.0),
                    'NavyFaction': 'TradingCo',
                    'Patrol Radius': '1.9157',
                    'Pos': Point3(485.627, 220.674, 25.384),
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
                'Model': 'models/caves/cave_d_zero'
            }
        }
    },
    'Node Links':
    [['1176323200.0dxschafe', '1176322304.0dxschafe5', 'Bi-directional'],
     ['1176323328.0dxschafe', '1176322432.0dxschafe', 'Bi-directional'],
     ['1176322432.0dxschafe2', '1176323328.0dxschafe0', 'Bi-directional'],
     ['1176323456.0dxschafe', '1176322432.0dxschafe1', 'Bi-directional'],
     ['1175817216.0dxschafe1', '1192671104.0dxschafe', 'Bi-directional'],
     ['1192671104.0dxschafe0', '1192671104.0dxschafe', 'Bi-directional'],
     ['1192671104.0dxschafe0', '1192671104.0dxschafe1', 'Bi-directional']],
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
        '1167862588.52sdnaik':
        '["Objects"]["1167862588.52sdnaik"]',
        '1167889596.27sdnaik':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1167889596.27sdnaik"]',
        '1167889596.28sdnaik':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1167889596.28sdnaik"]',
        '1167889596.31sdnaik':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1167889596.31sdnaik"]',
        '1175816960.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1175816960.0dxschafe"]',
        '1175817216.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1175817216.0dxschafe0"]',
        '1175817216.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1175817216.0dxschafe1"]',
        '1176249856.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176249856.0dxschafe"]',
        '1176249984.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176249984.0dxschafe"]',
        '1176249984.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176249984.0dxschafe0"]',
        '1176249984.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176249984.0dxschafe1"]',
        '1176249984.0dxschafe2':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176249984.0dxschafe2"]',
        '1176249984.0dxschafe3':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176249984.0dxschafe3"]',
        '1176250112.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250112.0dxschafe"]',
        '1176250112.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250112.0dxschafe0"]',
        '1176250112.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250112.0dxschafe1"]',
        '1176250240.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250240.0dxschafe"]',
        '1176250240.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250240.0dxschafe0"]',
        '1176250368.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250368.0dxschafe"]',
        '1176250368.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250368.0dxschafe0"]',
        '1176250752.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250752.0dxschafe"]',
        '1176250752.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250752.0dxschafe"]',
        '1176250752.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250752.0dxschafe1"]',
        '1176250752.0dxschafe2':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250752.0dxschafe1"]',
        '1176250752.0dxschafe3':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250752.0dxschafe3"]',
        '1176250752.0dxschafe4':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250752.0dxschafe3"]',
        '1176251008.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176251008.0dxschafe"]',
        '1176251008.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176251008.0dxschafe"]',
        '1176251264.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176251264.0dxschafe"]',
        '1176251264.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176251264.0dxschafe0"]',
        '1176251392.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176251392.0dxschafe"]',
        '1176251392.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176251392.0dxschafe0"]',
        '1176251392.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176251392.0dxschafe1"]',
        '1176251392.0dxschafe2':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176251392.0dxschafe2"]',
        '1176251648.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176251648.0dxschafe"]',
        '1176251776.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176251776.0dxschafe"]',
        '1176254720.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176254720.0dxschafe"]',
        '1176254848.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176254848.0dxschafe"]',
        '1176254848.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176254848.0dxschafe0"]',
        '1176254976.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176254976.0dxschafe"]',
        '1176255232.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176255232.0dxschafe"]',
        '1176317440.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176317440.0dxschafe"]',
        '1176320128.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176320128.0dxschafe"]',
        '1176322048.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322048.0dxschafe"]',
        '1176322048.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322048.0dxschafe0"]',
        '1176322176.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322176.0dxschafe"]',
        '1176322176.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322176.0dxschafe0"]',
        '1176322304.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322304.0dxschafe"]',
        '1176322304.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322304.0dxschafe0"]',
        '1176322304.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250752.0dxschafe3"]["Objects"]["1176322304.0dxschafe1"]',
        '1176322304.0dxschafe2':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322304.0dxschafe2"]',
        '1176322304.0dxschafe3':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322304.0dxschafe3"]',
        '1176322304.0dxschafe4':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322304.0dxschafe4"]',
        '1176322304.0dxschafe5':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322304.0dxschafe5"]',
        '1176322432.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322432.0dxschafe"]',
        '1176322432.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322432.0dxschafe0"]',
        '1176322432.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250112.0dxschafe1"]["Objects"]["1176322432.0dxschafe1"]',
        '1176322432.0dxschafe2':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322432.0dxschafe2"]',
        '1176322688.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250368.0dxschafe0"]["Objects"]["1176322688.0dxschafe"]',
        '1176322816.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322816.0dxschafe"]',
        '1176322816.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322816.0dxschafe0"]',
        '1176322816.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322816.0dxschafe1"]',
        '1176322816.0dxschafe2':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322816.0dxschafe2"]',
        '1176322816.0dxschafe3':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322816.0dxschafe3"]',
        '1176322816.0dxschafe4':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322816.0dxschafe4"]',
        '1176322816.0dxschafe5':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322816.0dxschafe5"]',
        '1176322816.0dxschafe6':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322816.0dxschafe6"]',
        '1176322816.0dxschafe7':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322816.0dxschafe7"]',
        '1176322816.0dxschafe8':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176322816.0dxschafe8"]',
        '1176323200.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176323200.0dxschafe"]',
        '1176323328.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176323328.0dxschafe"]',
        '1176323328.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176323328.0dxschafe0"]',
        '1176323456.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176323456.0dxschafe"]',
        '1179433459.59Aholdun':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1179433459.59Aholdun"]',
        '1179433471.55Aholdun':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1179433471.55Aholdun"]',
        '1179433481.05Aholdun':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1179433481.05Aholdun"]',
        '1179433494.72Aholdun':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1179433494.72Aholdun"]',
        '1179433506.16Aholdun':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1179433506.16Aholdun"]',
        '1179433521.63Aholdun':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1179433521.63Aholdun"]',
        '1179433548.52Aholdun':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1179433548.52Aholdun"]',
        '1179433561.2Aholdun':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1179433561.2Aholdun"]',
        '1179433672.64Aholdun':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1179433672.64Aholdun"]',
        '1179433739.83Aholdun':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1179433739.83Aholdun"]',
        '1187045504.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187045504.0dxschafe"]',
        '1187045504.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187045504.0dxschafe0"]',
        '1187045504.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187045504.0dxschafe1"]',
        '1187045760.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187045760.0dxschafe"]',
        '1187045760.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187045760.0dxschafe0"]',
        '1187045760.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187045760.0dxschafe1"]',
        '1187045760.0dxschafe2':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187045760.0dxschafe2"]',
        '1187045760.0dxschafe3':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187045760.0dxschafe3"]',
        '1187045760.0dxschafe4':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187045760.0dxschafe4"]',
        '1187045888.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187045888.0dxschafe"]',
        '1187046016.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187046016.0dxschafe"]',
        '1187046144.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187046144.0dxschafe"]',
        '1187046272.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187046272.0dxschafe"]',
        '1187046656.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187046656.0dxschafe"]',
        '1187656320.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187656320.0dxschafe"]',
        '1187656320.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187656320.0dxschafe0"]',
        '1187656320.0dxschafe2':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187656320.0dxschafe2"]',
        '1187656448.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187656448.0dxschafe"]',
        '1187656448.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187656448.0dxschafe0"]',
        '1187656448.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187656448.0dxschafe1"]',
        '1187656448.0dxschafe2':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187656448.0dxschafe2"]',
        '1187656448.0dxschafe3':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187656448.0dxschafe3"]',
        '1187656448.0dxschafe4':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187656448.0dxschafe4"]',
        '1187656448.0dxschafe5':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187656448.0dxschafe5"]',
        '1187656448.0dxschafe6':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187656448.0dxschafe6"]',
        '1187656448.0dxschafe7':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187656448.0dxschafe7"]',
        '1187656704.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187656704.0dxschafe"]',
        '1187656704.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187656704.0dxschafe0"]',
        '1187657088.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657088.0dxschafe"]',
        '1187657216.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657216.0dxschafe"]',
        '1187657216.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657216.0dxschafe0"]',
        '1187657216.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657216.0dxschafe1"]',
        '1187657216.0dxschafe2':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657216.0dxschafe2"]',
        '1187657216.0dxschafe3':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657216.0dxschafe3"]',
        '1187657216.0dxschafe4':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657216.0dxschafe4"]',
        '1187657216.0dxschafe5':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657216.0dxschafe5"]',
        '1187657216.0dxschafe6':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657216.0dxschafe6"]',
        '1187657216.0dxschafe7':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657216.0dxschafe7"]',
        '1187657216.0dxschafe8':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176251392.0dxschafe0"]["Objects"]["1187657216.0dxschafe8"]',
        '1187657216.0dxschafe9':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657216.0dxschafe9"]',
        '1187657344.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250112.0dxschafe1"]["Objects"]["1187657344.0dxschafe"]',
        '1187657344.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657344.0dxschafe0"]',
        '1187657344.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657344.0dxschafe1"]',
        '1187657344.0dxschafe2':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657344.0dxschafe2"]',
        '1187657344.0dxschafe3':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657344.0dxschafe3"]',
        '1187657344.0dxschafe4':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657344.0dxschafe4"]',
        '1187657344.0dxschafe5':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657344.0dxschafe5"]',
        '1187657600.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657600.0dxschafe"]',
        '1187657600.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657600.0dxschafe0"]',
        '1187657600.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657600.0dxschafe1"]',
        '1187657728.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657728.0dxschafe"]',
        '1187657728.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657728.0dxschafe0"]',
        '1187657728.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657728.0dxschafe1"]',
        '1187657728.0dxschafe2':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657728.0dxschafe2"]',
        '1187657728.0dxschafe3':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657728.0dxschafe3"]',
        '1187657728.0dxschafe4':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657728.0dxschafe4"]',
        '1187657728.0dxschafe7':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657728.0dxschafe7"]',
        '1187657856.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657856.0dxschafe"]',
        '1187657856.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657856.0dxschafe0"]',
        '1187658112.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187658112.0dxschafe0"]',
        '1187658240.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187658240.0dxschafe"]',
        '1187658240.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187658240.0dxschafe0"]',
        '1187658240.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187658240.0dxschafe1"]',
        '1187658368.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187658368.0dxschafe"]',
        '1187658368.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187658368.0dxschafe0"]',
        '1187658368.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187658368.0dxschafe1"]',
        '1187658496.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187658496.0dxschafe"]',
        '1187658496.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187658496.0dxschafe0"]',
        '1187658496.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187658496.0dxschafe1"]',
        '1187732480.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187732480.0dxschafe"]',
        '1187732608.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187732608.0dxschafe"]',
        '1189548928.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1189548928.0dxschafe"]',
        '1189549568.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1189549568.0dxschafe"]',
        '1189549696.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1189549696.0dxschafe"]',
        '1189549696.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1189549696.0dxschafe0"]',
        '1189549824.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1189549824.0dxschafe"]',
        '1189549952.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1189549952.0dxschafe1"]',
        '1189550336.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1189550336.0dxschafe"]',
        '1189551232.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1189551232.0dxschafe"]',
        '1189551360.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1189551360.0dxschafe"]',
        '1189551488.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1189551488.0dxschafe0"]',
        '1189551488.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1189551488.0dxschafe1"]',
        '1192671104.0dxschafe':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1192671104.0dxschafe"]',
        '1192671104.0dxschafe0':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1192671104.0dxschafe0"]',
        '1192671104.0dxschafe1':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1192671104.0dxschafe1"]',
        '1205365549.31kmuller':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250752.0dxschafe1"]["Objects"]["1205365549.31kmuller"]',
        '1205365552.68kmuller':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176251008.0dxschafe"]["Objects"]["1205365552.68kmuller"]',
        '1205365556.53kmuller':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1176250752.0dxschafe"]["Objects"]["1205365556.53kmuller"]',
        '1205365556.89kmuller':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1205365556.89kmuller"]',
        '1205365635.84kmuller':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1205365635.84kmuller"]',
        '1205365699.31kmuller':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1187657344.0dxschafe3"]["Objects"]["1205365699.31kmuller"]',
        '1219339266.79mtucker':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1219339266.79mtucker"]',
        '1219352693.09mtucker':
        '["Objects"]["1167862588.52sdnaik"]["Objects"]["1219352693.09mtucker"]'
    }
}
extraInfo = {
    'camPos': Point3(435.629, 108.667, 118.5),
    'camHpr': VBase3(-21.2761, -41.8142, 1.14553e-06),
    'focalLength': 1.39999997616,
    'skyState': 2,
    'fog': 0
}
