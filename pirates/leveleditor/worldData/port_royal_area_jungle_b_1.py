# Embedded file name: pirates.leveleditor.worldData.port_royal_area_jungle_b_1
from pandac.PandaModules import Point3, VBase3, Vec4
objectStruct = {
    'AmbientColors': {
        -1: Vec4(0.447059, 0.447059, 0.415686, 1),
        0: Vec4(0.494118, 0.564706, 0.67451, 1),
        2: Vec4(0, 0, 0, 1),
        4: Vec4(0.721569, 0.611765, 0.619608, 1),
        6: Vec4(0.437059, 0.446471, 0.556667, 1),
        8: Vec4(0.389216, 0.426275, 0.569608, 1)
    },
    'DirectionalColors': {
        -1: Vec4(0.717647, 0.721569, 0.72549, 1),
        0: Vec4(0.956863, 0.909804, 0.894118, 1),
        2: Vec4(0.537255, 0.403922, 0.411765, 1),
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
    [['1176161024.0dxschafe0', '1176161024.0dxschafe', 'Bi-directional'],
     ['1176160896.0dxschafe0', '1176160896.0dxschafe', 'Bi-directional'],
     ['1179346924.27Aholdun', '1176160768.0dxschafe', 'Bi-directional'],
     ['1176160640.0dxschafe1', '1176160640.0dxschafe0', 'Bi-directional'],
     ['1164936513.38Shochet', '1165197181.14Shochet', 'Bi-directional'],
     ['1165197002.81Shochet', '1165197032.86Shochet', 'Bi-directional'],
     ['1176160640.0dxschafe', '1165197123.73Shochet', 'Bi-directional'],
     ['1176160512.0dxschafe', '1165197146.75Shochet', 'Bi-directional']],
    'Objects': {
        '1161798288.34sdnaik': {
            'Type': 'Island Game Area',
            'Name': 'port_royal_area_jungle_b_1',
            'File': '',
            'AdditionalData': ['JungleAreaB'],
            'Instanced': True,
            'Objects': {
                '1154497344.0jubutlerPR': {
                    'Type': 'Townsperson',
                    'Category': 'Cast',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'CustomModel': 'models/char/td_2000',
                    'DNA': '1154497344.0jubutler',
                    'Hpr': VBase3(-178.991, 0.0, 0.0),
                    'Patrol Radius': '12.0000',
                    'Pos': Point3(-403.93, -407.894, 5.838),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Private Status': 'Private Only',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': 'Villager',
                    'TrailFX': 'None'
                },
                '1161798918.92sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_1',
                    'Hpr': VBase3(-90.0, 0.0, 0.0),
                    'Pos': Point3(498.114, 427.808, 45.336),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1161798918.94sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_2',
                    'Hpr': VBase3(121.61, 0.0, 0.0),
                    'Pos': Point3(-318.959, -565.768, 0.675),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1164936002.39Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-170.247, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-436.925, -254.243, 10.499),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164936245.39Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(44.734, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-130.752, 66.978, 19.389),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164936298.17Shochet': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-315.001, 252.472, 65.32),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Scorpion',
                    'Team': '1',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164936310.64Shochet': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-99.942, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-78.648, 282.321, 70.118),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Wasp',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164936338.17Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(42.289, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(97.822, -7.591, 30.56),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Noob Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164936402.78Shochet': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-92.415, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(80.857, 167.308, 43.453),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Noob Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164936419.63Shochet': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-87.141, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(268.191, 188.38, 39.959),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164936439.78Shochet': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-36.638, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(364.79, 128.085, 42.301),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164936491.86Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-360.694, 30.41, 13.43),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164936513.38Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '32.8313',
                    'AnimSet': 'default',
                    'Hpr': VBase3(165.843, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.5602',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-176.883, 258.25, 21.956),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164936682.44Shochet': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-356.575, 220.133, 52.372),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164936686.23Shochet': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-395.066, 164.528, 34.894),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1164936727.27Shochet': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-240.863, 263.979, 51.648),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165000116.13Shochet': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': True,
                    'Hpr': VBase3(166.317, 0.0, 0.0),
                    'Pos': Point3(-262.793, -143.577, 17.974),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/prop_group01'
                    }
                },
                '1165000125.38Shochet': {
                    'Type': 'Prop_Groups',
                    'DisableCollision': False,
                    'Hpr': VBase3(-38.156, 0.0, 1.136),
                    'Pos': Point3(-240.028, -139.121, 17.366),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.6000000238418579,
                                  0.6000000238418579, 1.0),
                        'Model':
                        'models/props/prop_group01'
                    }
                },
                '1165197002.81Shochet': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-240.854, -148.189, 17.532),
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
                '1165197032.86Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(109.626, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-248.044, -165.765, 16.839),
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
                '1165197123.73Shochet': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-76.488, -1.263, 0.303),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-476.838, -70.199, 18.075),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1165197146.75Shochet': {
                    'Type': 'Object Spawn Node',
                    'Hpr': VBase3(-53.837, 0.0, 0.0),
                    'Pos': Point3(-489.581, -229.365, 13.885),
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
                '1165197181.14Shochet': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-166.224, 143.454, 21.462),
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
                '1175806714.68dzlu': {
                    'Type': 'Light - Dynamic',
                    'Attenuation': '0.005',
                    'ConeAngle': '83.4091',
                    'DropOff': '5.4545',
                    'FlickRate': 0.5,
                    'Flickering': False,
                    'Hpr': VBase3(50.078, 3.335, -85.909),
                    'Intensity': '1.0606',
                    'LightType': 'SPOT',
                    'Pos': Point3(-385.442, -498.165, 8.691),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.47999998927116394, 0.699999988079071,
                                  0.8399999737739563, 1.0),
                        'Model':
                        'models/props/light_tool_bulb'
                    }
                },
                '1175806851.05dzlu': {
                    'Type': 'Light - Dynamic',
                    'Attenuation': '0.005',
                    'ConeAngle': '15.0000',
                    'DropOff': '73.6364',
                    'FlickRate': 0.5,
                    'Flickering': False,
                    'Hpr': VBase3(5.24, 0.0, 0.0),
                    'Intensity': '0.1515',
                    'LightType': 'POINT',
                    'Pos': Point3(-399.982, -498.94, 9.285),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/light_tool_bulb'
                    }
                },
                '1175882228.18dzlu': {
                    'Type': 'Light - Dynamic',
                    'Attenuation': '0.005',
                    'ConeAngle': '72.2727',
                    'DropOff': '90.0000',
                    'FlickRate': 0.5,
                    'Flickering': False,
                    'Hpr': VBase3(158.174, -9.988, -26.511),
                    'Intensity': '0.4848',
                    'LightType': 'SPOT',
                    'Pos': Point3(-386.209, -473.346, 12.285),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.9300000071525574, 0.75, 1.0, 1.0),
                        'Model': 'models/props/light_tool_bulb'
                    }
                },
                '1175884051.14dzlu': {
                    'Type': 'Light - Dynamic',
                    'Attenuation': '0.005',
                    'ConeAngle': '57.9545',
                    'DropOff': '47.7273',
                    'FlickRate': 0.5,
                    'Flickering': True,
                    'Hpr': VBase3(-78.898, 12.407, -85.181),
                    'Intensity': '0.9091',
                    'LightType': 'SPOT',
                    'Pos': Point3(-400.488, -493.036, 8.393),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6000000238418579, 0.800000011920929, 1.0,
                                  1.0),
                        'Model': 'models/props/light_tool_bulb'
                    }
                },
                '1175893134.2dzlu': {
                    'Type': 'Light - Dynamic',
                    'Attenuation': '0.005',
                    'ConeAngle': '15.0000',
                    'DropOff': '16.3636',
                    'FlickRate': 0.5,
                    'Flickering': True,
                    'Hpr': VBase3(34.514, 0.0, -9.825),
                    'Intensity': '0.6364',
                    'LightType': 'POINT',
                    'Pos': Point3(-393.934, -487.076, 11.204),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (1.0, 0.75, 0.8399999737739563, 1.0),
                        'Model': 'models/props/light_tool_bulb'
                    }
                },
                '1175911936.0dxschafe0': {
                    'Type': 'Cutscene Origin Node',
                    'CutsceneId': '2.2: Tia Dalma Compass',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-393.0, -487.0, 5.406),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176160384.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '26.5060',
                    'AnimSet': 'default',
                    'Hpr': VBase3(135.194, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(77.777, -117.871, 27.208),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Wasp',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176160512.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-170.699, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-472.561, -138.128, 15.719),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Noob Skeleton',
                    'Start State': 'Idle',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176160640.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-538.147, -99.547, 15.271),
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
                '1176160640.0dxschafe0': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-236.977, -74.728, 16.121),
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
                '1176160640.0dxschafe1': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-287.69, -72.214, 18.312),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176160768.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': VBase3(-20.193, 0.0, 0.0),
                    'Pos': Point3(-229.328, 307.395, 55.117),
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
                '1176160896.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': VBase3(163.269, 0.0, 0.0),
                    'Pos': Point3(39.245, -113.744, 25.483),
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
                '1176160896.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(57.202, -54.005, 27.665),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176161024.0dxschafe': {
                    'Type': 'Object Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(208.357, -10.579, 34.165),
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
                '1176161024.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '0.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-9.529, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(193.194, -71.992, 32.807),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Wasp',
                    'Start State': 'Ambush',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176161152.0dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-68.125, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(351.658, 181.191, 44.282),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Noob Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176161280.0dxschafe': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '12.0000',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-75.875, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-175.83, 70.058, 17.745),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Alligator',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176161280.0dxschafe0': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-168.768, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-308.037, 172.659, 33.907),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176161280.0dxschafe1': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-89.565, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-128.423, 113.785, 20.07),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176161280.0dxschafe2': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(167.436, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(463.513, 343.854, 49.092),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176161280.0dxschafe3': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(94.357, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(311.112, 149.706, 40.269),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176161280.0dxschafe4': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(68.141, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(265.852, 73.662, 37.388),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176161280.0dxschafe5': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(104.386, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(149.468, 167.886, 40.86),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176161408.0dxschafe0': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(145.469, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-237.139, 152.081, 24.37),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176161408.0dxschafe1': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-59.372, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-333.147, -43.811, 18.139),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176161408.0dxschafe2': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(-19.8, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-441.868, -204.639, 13.947),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176161408.0dxschafe3': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-408.548, -307.102, 7.897),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176161408.0dxschafe4': {
                    'Type': 'Player Spawn Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-450.758, -414.494, 2.338),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1176161408.0dxschafe5': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(27.533, 0.0, 0.0),
                    'Index': -1,
                    'Pos': Point3(-348.77, -529.235, 2.554),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'All',
                    'Visual': {
                        'Color': (0.5, 0.5, 0.5, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179346924.27Aholdun': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '5',
                    'Pos': Point3(-227.277, 294.105, 52.486),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Early Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1179346979.48Aholdun': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '100',
                    'Pause Duration': '30',
                    'Pos': Point3(-419.518, 107.494, 22.451),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Noob Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1187042944.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'Aggro Radius': '8.1325',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-179.143, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '1.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-6.6, 303.486, 83.247),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Wasp',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': 'default',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190664960.0dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(144.833, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-52.145, 183.325, 25.128),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190665088.0dxschafe': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(-73.53, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': 100,
                    'Pause Duration': 30,
                    'Pos': Point3(-333.287, 109.344, 22.97),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1190665088.0dxschafe0': {
                    'Type': 'Spawn Node',
                    'AnimSet': 'default',
                    'Hpr': VBase3(177.953, 0.0, 0.0),
                    'Min Population': '1',
                    'Patrol Radius': '12.0000',
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-406.858, 13.832, 16.119),
                    'PoseAnim': '',
                    'PoseFrame': '',
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Low Skeleton',
                    'Start State': 'Patrol',
                    'StartFrame': '0',
                    'Team': '1',
                    'TrailFX': 'None',
                    'Visual': {
                        'Color': (0, 0, 0.65, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1192740226.78akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-10.883, 0.0, 0.0),
                    'Pos': Point3(-261.982, -147.146, 17.547),
                    'Scale': VBase3(1.684, 1.0, 1.062),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1192837197.21kmuller': {
                    'Type': 'Tree',
                    'DisableCollision': True,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-223.748, 119.988, 20.469),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_a'
                    }
                },
                '1192837244.65kmuller': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(18.851, 0.0, 0.0),
                    'Pos': Point3(-228.899, 119.847, 18.448),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1192837255.66kmuller': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(-45.484, 0.0, 0.0),
                    'Pos': Point3(-221.514, 115.2, 20.477),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1192837271.26kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-223.835, 118.932, 23.227),
                    'Scale': VBase3(2.118, 2.118, 2.118),
                    'Visual': {
                        'Model': 'models/misc/coll_sphere_barrier'
                    }
                },
                '1192837304.93kmuller': {
                    'Type': 'Jungle_Props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-272.691, 175.783, 31.625),
                    'Scale': VBase3(1.247, 1.247, 1.247),
                    'Visual': {
                        'Color': (0.8999999761581421, 0.8999999761581421,
                                  0.8999999761581421, 1.0),
                        'Model':
                        'models/vegetation/jungle_fern_a'
                    }
                },
                '1192837313.66kmuller': {
                    'Type': 'Jungle_Props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-269.504, 171.906, 30.407),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/jungle_fern_b'
                    }
                },
                '1192837328.99kmuller': {
                    'Type': 'Jungle_Props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 11.43, 0.0),
                    'Pos': Point3(-279.593, 167.775, 30.319),
                    'Scale': VBase3(1.0, 1.0, 0.707),
                    'Visual': {
                        'Color': (0.699999988079071, 0.699999988079071,
                                  0.699999988079071, 1.0),
                        'Model':
                        'models/vegetation/jungle_fern_a'
                    }
                },
                '1192837377.15kmuller': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 5.301, 5.091),
                    'Pos': Point3(-284.641, 172.871, 31.164),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.8500000238418579, 0.9300000071525574, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1192837583.94kmuller': {
                    'Type': 'Jungle_Props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.281, 7.364, -2.192),
                    'Pos': Point3(-316.441, 150.331, 29.502),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5799999833106995, 0.5699999928474426,
                                  0.47999998927116394, 1.0),
                        'Model':
                        'models/vegetation/jungle_fern_a'
                    }
                },
                '1192837605.99kmuller': {
                    'Type': 'Jungle_Props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 12.353, 0.0),
                    'Pos': Point3(-322.101, 149.134, 30.126),
                    'Scale': VBase3(1.21, 1.21, 1.21),
                    'Visual': {
                        'Model': 'models/vegetation/jungle_fern_b'
                    }
                },
                '1192837619.09kmuller': {
                    'Type': 'Jungle_Props',
                    'DisableCollision': False,
                    'Hpr': VBase3(-14.875, 22.214, 15.667),
                    'Pos': Point3(-317.326, 146.542, 29.063),
                    'Scale': VBase3(0.717, 0.717, 0.717),
                    'Visual': {
                        'Model': 'models/vegetation/jungle_fern_b'
                    }
                },
                '1192837630.48kmuller': {
                    'Type': 'Jungle_Props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 8.437, 0.0),
                    'Pos': Point3(-328.988, 140.799, 27.984),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.8500000238418579, 0.8199999928474426,
                                  0.7300000190734863, 1.0),
                        'Model':
                        'models/vegetation/jungle_fern_b'
                    }
                },
                '1192837655.01kmuller': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 4.923, 0.0),
                    'Pos': Point3(-323.917, 147.953, 27.416),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6200000047683716, 0.6600000262260437,
                                  0.6200000047683716, 1.0),
                        'Model':
                        'models/vegetation/fern_tree_b'
                    }
                },
                '1192837730.34kmuller': {
                    'Type': 'Jungle_Props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-60.541, 203.401, 24.845),
                    'Scale': VBase3(1.0, 1.0, 0.748),
                    'Visual': {
                        'Model': 'models/vegetation/jungle_plant_a'
                    }
                },
                '1192837772.73kmuller': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-21.862, 163.732, 27.684),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_h'
                    }
                },
                '1192837827.37kmuller': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(-71.79, 7.431, 2.233),
                    'Pos': Point3(-29.976, 169.062, 26.125),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_c'
                    }
                },
                '1192837844.07kmuller': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(57.653, -1.45, 0.0),
                    'Pos': Point3(-22.002, 162.012, 27.77),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1192837883.85kmuller': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': VBase3(13.44, 3.982, -21.645),
                    'Pos': Point3(-16.467, 168.27, 30.325),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.5199999809265137, 0.5199999809265137,
                                  0.5299999713897705, 1.0),
                        'Model':
                        'models/props/rock_group_1_floor'
                    }
                },
                '1192837939.81kmuller': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(60.168, 0.0, 0.0),
                    'Pos': Point3(-12.269, 162.715, 30.235),
                    'Scale': VBase3(1.0, 1.0, 0.818),
                    'Visual': {
                        'Model': 'models/vegetation/bush_b'
                    }
                },
                '1192837969.85kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-29.06, 0.0, 0.0),
                    'Pos': Point3(-25.927, 160.378, 22.684),
                    'Scale': VBase3(3.891, 2.762, 3.863),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1192838000.69kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-167.075, 0.0, 0.0),
                    'Pos': Point3(-28.656, 173.26, 22.216),
                    'Scale': VBase3(3.087, 2.687, 3.76),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1192838043.24kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(100.63, 0.0, 0.0),
                    'Pos': Point3(-11.453, 163.587, 29.545),
                    'Scale': VBase3(2.701, 2.171, 2.171),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1192838190.18kmuller': {
                    'Type': 'Bush',
                    'DisableCollision': True,
                    'Hpr': VBase3(0.0, 5.832, 0.0),
                    'Pos': Point3(115.404, 185.44, 46.047),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1192838210.21kmuller': {
                    'Type': 'Bush',
                    'DisableCollision': False,
                    'Hpr': VBase3(-101.49, 0.0, 6.542),
                    'Pos': Point3(107.356, 181.692, 48.149),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1192838233.07kmuller': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': VBase3(0.0, 9.708, 0.0),
                    'Pos': Point3(114.051, 179.563, 45.182),
                    'Scale': VBase3(2.051, 2.051, 2.051),
                    'Visual': {
                        'Color': (0.5199999809265137, 0.5199999809265137,
                                  0.5299999713897705, 1.0),
                        'Model':
                        'models/props/rock_group_3_floor'
                    }
                },
                '1192838287.48kmuller': {
                    'Type': 'Jungle_Props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 13.807, 0.0),
                    'Pos': Point3(112.482, 172.598, 44.677),
                    'Scale': VBase3(1.409, 1.409, 1.409),
                    'Visual': {
                        'Color': (0.699999988079071, 0.699999988079071,
                                  0.699999988079071, 1.0),
                        'Model':
                        'models/vegetation/jungle_fern_a'
                    }
                },
                '1192838312.19kmuller': {
                    'Type': 'Jungle_Props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.147, 1.443, -5.819),
                    'Pos': Point3(99.551, 176.808, 45.871),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.8299999833106995, 0.800000011920929,
                                  0.6899999976158142, 1.0),
                        'Model':
                        'models/vegetation/jungle_fern_b'
                    }
                },
                '1192838329.48kmuller': {
                    'Type': 'Jungle_Props',
                    'DisableCollision': False,
                    'Hpr': VBase3(0.0, 8.891, 0.0),
                    'Pos': Point3(118.734, 170.744, 44.314),
                    'Scale': VBase3(0.746, 0.746, 0.746),
                    'Visual': {
                        'Model': 'models/vegetation/jungle_fern_b'
                    }
                },
                '1192838406.06kmuller': {
                    'Type': 'Jungle_Props',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(124.25, 178.796, 45.301),
                    'Scale': VBase3(0.863, 0.863, 0.863),
                    'Visual': {
                        'Model': 'models/vegetation/jungle_fern_b'
                    }
                },
                '1192838434.04kmuller': {
                    'Type': 'Grass',
                    'Hpr': VBase3(48.954, 0.0, 0.0),
                    'Pos': Point3(123.705, 174.922, 43.925),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6700000166893005, 0.7900000214576721,
                                  0.7799999713897705, 1.0),
                        'Model':
                        'models/vegetation/grass_3feet'
                    }
                },
                '1192838451.24kmuller': {
                    'Type': 'Grass',
                    'Hpr': VBase3(67.31, 0.0, 0.0),
                    'Pos': Point3(121.592, 174.416, 43.654),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.6700000166893005, 0.7900000214576721,
                                  0.7799999713897705, 1.0),
                        'Model':
                        'models/vegetation/grass_8feet'
                    }
                },
                '1192838492.21kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(5.148, 0.0, 0.0),
                    'Pos': Point3(112.57, 168.542, 42.358),
                    'Scale': VBase3(1.732, 1.723, 1.723),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1192838511.84kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(64.871, 0.0, 0.0),
                    'Pos': Point3(123.684, 174.896, 43.373),
                    'Scale': VBase3(1.328, 1.231, 1.799),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1192838526.71kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(124.866, 0.0, 0.0),
                    'Pos': Point3(121.85, 187.205, 45.756),
                    'Scale': VBase3(1.834, 1.834, 2.418),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1192838583.13kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-48.865, 0.0, 0.0),
                    'Pos': Point3(97.361, 175.67, 43.219),
                    'Scale': VBase3(2.146, 1.567, 2.048),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1192838638.44kmuller': {
                    'Type': 'Rock',
                    'DisableCollision': True,
                    'Hpr': VBase3(0.0, 0.0, -5.193),
                    'Pos': Point3(107.118, 188.82, 48.864),
                    'Scale': VBase3(2.046, 1.683, 1.683),
                    'Visual': {
                        'Color': (0.5199999809265137, 0.5199999809265137,
                                  0.5299999713897705, 1.0),
                        'Model':
                        'models/props/rock_2_sphere'
                    }
                },
                '1192838684.07kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-147.916, 0.0, 0.0),
                    'Pos': Point3(98.65, 188.743, 47.701),
                    'Scale': VBase3(1.969, 1.581, 2.267),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1192838739.04kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-175.172, 0.0, 0.0),
                    'Pos': Point3(111.651, 194.053, 50.267),
                    'Scale': VBase3(1.117, 1.117, 1.533),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1193074304.0dxschafe': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(106.646, 0.0, 0.0),
                    'Pos': Point3(-81.026, 18.962, 19.626),
                    'Scale': VBase3(2.701, 2.171, 3.069),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1193074304.0dxschafe0': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-92.109, 19.174, 21.837),
                    'Scale': VBase3(1.566, 1.566, 1.566),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_h'
                    }
                },
                '1193074304.0dxschafe1': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-167.075, 0.0, 0.0),
                    'Pos': Point3(-90.151, 30.306, 16.369),
                    'Scale': VBase3(1.173, 2.687, 3.76),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1193074304.0dxschafe2': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-91.811, 0.0, 0.0),
                    'Pos': Point3(-95.759, 9.769, 16.837),
                    'Scale': VBase3(3.891, 2.762, 3.863),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1193074432.0dxschafe': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(113.065, 0.0, 0.0),
                    'Pos': Point3(-370.532, -104.384, 16.831),
                    'Scale': VBase3(2.701, 2.171, 3.031),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1193074432.0dxschafe0': {
                    'Type': 'Tree',
                    'DisableCollision': True,
                    'Hpr': VBase3(-24.513, 0.0, 0.0),
                    'Pos': Point3(-383.577, -104.798, 19.299),
                    'Scale': VBase3(1.359, 1.359, 1.359),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_h'
                    }
                },
                '1193074432.0dxschafe1': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-167.075, 0.0, 0.0),
                    'Pos': Point3(-382.597, -94.188, 13.831),
                    'Scale': VBase3(1.504, 2.687, 3.76),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1193074432.0dxschafe2': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-92.408, 0.0, 0.0),
                    'Pos': Point3(-389.682, -114.221, 13.642),
                    'Scale': VBase3(3.891, 2.762, 3.863),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1193074432.0dxschafe3': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(89.157, 0.0, 0.0),
                    'Pos': Point3(-410.24, 31.169, 17.307),
                    'Scale': VBase3(1.75, 2.098, 2.945),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1193074432.0dxschafe4': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(-415.921, 28.879, 20.131),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_h'
                    }
                },
                '1193074432.0dxschafe5': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-149.461, 0.0, 0.0),
                    'Pos': Point3(-417.535, 35.441, 14.663),
                    'Scale': VBase3(1.766, 2.687, 3.76),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1193074432.0dxschafe6': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-29.06, 0.0, 0.0),
                    'Pos': Point3(-417.639, 26.933, 15.131),
                    'Scale': VBase3(1.661, 2.762, 3.863),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1193074560.0dxschafe0': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': VBase3(85.323, 0.0, 0.0),
                    'Pos': Point3(109.249, 60.368, 34.494),
                    'Scale': VBase3(1.386, 1.386, 1.386),
                    'Visual': {
                        'Model': 'models/vegetation/gen_tree_h'
                    }
                },
                '1193074560.0dxschafe1': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-141.58, 0.0, 0.0),
                    'Pos': Point3(108.233, 70.391, 29.028),
                    'Scale': VBase3(3.087, 2.687, 3.76),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1193074560.0dxschafe2': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-19.204, 0.0, 0.0),
                    'Pos': Point3(110.709, 55.771, 29.494),
                    'Scale': VBase3(3.071, 2.762, 3.863),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1193075072.0dxschafe': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': VBase3(55.576, 7.196, -1.475),
                    'Pos': Point3(-147.923, 228.911, 23.141),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.8500000238418579, 0.9300000071525574, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1193075072.0dxschafe0': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': VBase3(137.633, -0.473, -7.33),
                    'Pos': Point3(-153.481, 353.337, 70.516),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.8500000238418579, 0.9300000071525574, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1193075072.0dxschafe1': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': VBase3(55.576, 7.196, -1.475),
                    'Pos': Point3(-60.104, 313.031, 70.573),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.8500000238418579, 0.9300000071525574, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1193075072.0dxschafe2': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': VBase3(38.7, 1.164, -12.533),
                    'Pos': Point3(-101.584, 238.7, 50.335),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.8500000238418579, 0.9300000071525574, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1193075200.0dxschafe': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': VBase3(-72.265, 11.33, -2.533),
                    'Pos': Point3(-115.131, 281.848, 49.15),
                    'Scale': VBase3(0.914, 0.914, 0.914),
                    'Visual': {
                        'Color': (0.8500000238418579, 0.9300000071525574, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1193075200.0dxschafe0': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': VBase3(38.7, 1.164, -12.533),
                    'Pos': Point3(-182.107, 318.04, 57.169),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.8500000238418579, 0.9300000071525574, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1193075200.0dxschafe1': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': VBase3(38.7, 1.164, -12.533),
                    'Pos': Point3(-204.403, 252.868, 41.472),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.8500000238418579, 0.9300000071525574, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1193075200.0dxschafe2': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': VBase3(-32.818, 12.261, -2.865),
                    'Pos': Point3(-178.052, 326.076, 60.254),
                    'Scale': VBase3(1.349, 1.349, 1.349),
                    'Visual': {
                        'Color': (0.8500000238418579, 0.9300000071525574, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1193075328.0dxschafe': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': VBase3(38.7, 1.164, -12.533),
                    'Pos': Point3(-169.263, 354.06, 69.477),
                    'Scale': VBase3(1.349, 1.349, 1.349),
                    'Visual': {
                        'Color': (0.8500000238418579, 0.9300000071525574, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1193075328.0dxschafe0': {
                    'Type': 'Tree',
                    'DisableCollision': False,
                    'Hpr': VBase3(-103.78, 6.804, 10.614),
                    'Pos': Point3(-70.836, 337.044, 72.308),
                    'Scale': VBase3(1.93, 1.93, 1.93),
                    'Visual': {
                        'Color': (0.8500000238418579, 0.9300000071525574, 1.0,
                                  1.0),
                        'Model': 'models/vegetation/fern_tree_d'
                    }
                },
                '1193076608.0dxschafe': {
                    'Type': 'Bush',
                    'DisableCollision': False,
                    'Hpr': VBase3(31.284, 4.812, -4.438),
                    'Pos': Point3(327.92, 116.109, 40.339),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1193076736.0dxschafe': {
                    'Type': 'Bush',
                    'DisableCollision': False,
                    'Hpr': VBase3(-19.759, 6.475, 0.939),
                    'Pos': Point3(199.48, 127.202, 36.499),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1193076736.0dxschafe0': {
                    'Type': 'Bush',
                    'DisableCollision': False,
                    'Hpr': VBase3(-52.977, 4.91, 4.328),
                    'Pos': Point3(386.183, 217.295, 47.694),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1193076736.0dxschafe1': {
                    'Type': 'Bush',
                    'DisableCollision': False,
                    'Hpr': VBase3(-153.508, 0.31, 4.039),
                    'Pos': Point3(196.729, 86.997, 36.265),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1193076864.0dxschafe': {
                    'Type': 'Bush',
                    'DisableCollision': False,
                    'Hpr': VBase3(71.775, -0.777, -2.623),
                    'Pos': Point3(177.478, -21.122, 32.096),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1193076864.0dxschafe0': {
                    'Type': 'Bush',
                    'DisableCollision': False,
                    'Hpr': VBase3(71.775, -0.777, -2.623),
                    'Pos': Point3(272.024, 105.696, 35.442),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1193076864.0dxschafe1': {
                    'Type': 'Bush',
                    'DisableCollision': False,
                    'Hpr': VBase3(71.775, -0.777, -2.623),
                    'Pos': Point3(347.355, 146.445, 42.616),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1193076864.0dxschafe2': {
                    'Type': 'Bush',
                    'DisableCollision': False,
                    'Hpr': VBase3(-167.836, -1.87, 1.997),
                    'Pos': Point3(408.256, 233.837, 47.2),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1193076992.0dxschafe': {
                    'Type': 'Bush',
                    'DisableCollision': False,
                    'Hpr': VBase3(-97.806, 1.239, 2.439),
                    'Pos': Point3(440.762, 172.717, 44.748),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_a'
                    }
                },
                '1193076992.0dxschafe0': {
                    'Type': 'Bush',
                    'DisableCollision': False,
                    'Hpr': VBase3(-86.148, 1.707, 2.138),
                    'Pos': Point3(418.744, 227.643, 48.544),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1193076992.0dxschafe1': {
                    'Type': 'Bush',
                    'DisableCollision': False,
                    'Hpr': VBase3(61.104, -0.278, -2.721),
                    'Pos': Point3(463.289, 184.33, 45.655),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/vegetation/bush_d'
                    }
                },
                '1193077248.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(526.297, 229.125, 44.742),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193077376.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(524.809, 340.95, 46.12),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193077504.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(352.082, 130.899, 41.984),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193077632.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(45.327, 263.452, 76.18),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193077888.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(100.615, 31.605, 31.574),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193077888.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-155.031, 208.628, 24.222),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193078016.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-200.122, 215.454, 26.574),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193078144.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-201.665, 15.409, 14.781),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193078400.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(85.376, 75.555, 32.033),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193078656.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(32.503, 205.463, 50.816),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193078656.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-306.743, -116.685, 18.332),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193078784.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-480.48, -88.631, 16.576),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193078784.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-397.237, -258.695, 9.752),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193078784.0dxschafe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-302.522, -175.667, 15.662),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193078912.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-432.107, -385.46, 4.566),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193078912.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-424.34, 82.348, 21.628),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193079040.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(234.399, 161.309, 38.102),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193079040.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-238.569, 48.293, 14.955),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193079040.0dxschafe1': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-375.922, 104.745, 13.43),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193079168.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-312.338, 18.831, 15.017),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193079296.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-490.335, -264.596, 11.213),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193696256.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-258.963, -26.403, 17.249),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193696512.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-18.749, 227.963, 76.128),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193696512.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(24.583, 281.4, 81.289),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193696640.0dxschafe': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(-83.122, 244.701, 71.4),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1193696640.0dxschafe0': {
                    'Type': 'Movement Node',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pause Chance': '0',
                    'Pause Duration': '5',
                    'Pos': Point3(49.583, 254.889, 74.129),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1195599905.27akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(132.845, 0.0, 0.0),
                    'Pos': Point3(352.741, 91.443, 40.318),
                    'Scale': VBase3(0.609, 1.444, 1.444),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1205365360.84kmuller': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-164.024, 0.0, 0.0),
                    'Pos': Point3(-469.301, -285.196, 7.606),
                    'Scale': VBase3(1.0, 1.0, 3.359),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1213043604.3akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-16.712, 0.0, 0.0),
                    'Pos': Point3(-81.252, 209.984, 22.727),
                    'Scale': VBase3(0.646, 1.0, 1.337),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1213043637.89akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(-3.31, 0.0, 0.0),
                    'Pos': Point3(-131.121, 225.968, 27.452),
                    'Scale': VBase3(0.21, 1.0, 1.337),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                },
                '1213043680.69akelts': {
                    'Type': 'Collision Barrier',
                    'DisableCollision': False,
                    'Hpr': VBase3(84.028, 0.0, 0.0),
                    'Pos': Point3(-565.149, -87.833, 14.156),
                    'Scale': VBase3(1.35, 1.0, 1.723),
                    'Visual': {
                        'Model': 'models/misc/coll_plane_barrier'
                    }
                }
            },
            'Visual': {
                'Model': 'models/jungles/jungle_b_zero'
            }
        }
    },
    'Node Links':
    [['1164936686.23Shochet', '1164936682.44Shochet', 'Bi-directional'],
     ['1164936727.27Shochet', '1164936682.44Shochet', 'Bi-directional'],
     ['1164936298.17Shochet', '1164936682.44Shochet', 'Bi-directional'],
     ['1179346924.27Aholdun', '1164936727.27Shochet', 'Bi-directional'],
     ['1164936686.23Shochet', '1179346979.48Aholdun', 'Bi-directional'],
     ['1164936419.63Shochet', '1193077248.0dxschafe', 'Bi-directional'],
     ['1193077376.0dxschafe', '1164936439.78Shochet', 'Bi-directional'],
     ['1193077504.0dxschafe', '1164936402.78Shochet', 'Bi-directional'],
     ['1164936338.17Shochet', '1193077632.0dxschafe', 'Bi-directional'],
     ['1193077888.0dxschafe', '1193077888.0dxschafe0', 'Bi-directional'],
     ['1176160896.0dxschafe0', '1193077888.0dxschafe', 'Bi-directional'],
     ['1193078144.0dxschafe', '1193078016.0dxschafe', 'Bi-directional'],
     ['1164936513.38Shochet', '1193078016.0dxschafe', 'Bi-directional'],
     ['1193078400.0dxschafe', '1190665088.0dxschafe', 'Bi-directional'],
     ['1190664960.0dxschafe', '1193078656.0dxschafe0', 'Bi-directional'],
     ['1176160384.0dxschafe', '1193078656.0dxschafe', 'Bi-directional'],
     ['1176160640.0dxschafe1', '1193078784.0dxschafe1', 'Bi-directional'],
     ['1193078784.0dxschafe1', '1193078784.0dxschafe0', 'Bi-directional'],
     ['1193078784.0dxschafe0', '1193078784.0dxschafe', 'Bi-directional'],
     ['1176160640.0dxschafe1', '1193078784.0dxschafe', 'Bi-directional'],
     ['1193078912.0dxschafe', '1190665088.0dxschafe0', 'Bi-directional'],
     ['1176160512.0dxschafe', '1193078912.0dxschafe0', 'Bi-directional'],
     ['1193079040.0dxschafe', '1165197123.73Shochet', 'Bi-directional'],
     ['1193079168.0dxschafe', '1193079040.0dxschafe1', 'Bi-directional'],
     ['1193079168.0dxschafe', '1193079040.0dxschafe0', 'Bi-directional'],
     ['1193079296.0dxschafe', '1165197032.86Shochet', 'Bi-directional'],
     ['1193696256.0dxschafe', '1193079040.0dxschafe0', 'Bi-directional'],
     ['1164936245.39Shochet', '1193696256.0dxschafe', 'Bi-directional'],
     ['1164936310.64Shochet', '1193696512.0dxschafe0', 'Bi-directional'],
     ['1193696512.0dxschafe', '1164936310.64Shochet', 'Bi-directional'],
     ['1193696512.0dxschafe', '1193696512.0dxschafe0', 'Bi-directional'],
     ['1193696640.0dxschafe', '1193696640.0dxschafe0', 'Bi-directional'],
     ['1187042944.0dxschafe0', '1193696640.0dxschafe', 'Bi-directional'],
     ['1187042944.0dxschafe0', '1193696640.0dxschafe0', 'Bi-directional']],
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
        '1154497344.0jubutlerPR':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1154497344.0jubutlerPR"]',
        '1161798288.34sdnaik':
        '["Objects"]["1161798288.34sdnaik"]',
        '1161798918.92sdnaik':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1161798918.92sdnaik"]',
        '1161798918.94sdnaik':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1161798918.94sdnaik"]',
        '1164936002.39Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1164936002.39Shochet"]',
        '1164936245.39Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1164936245.39Shochet"]',
        '1164936298.17Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1164936298.17Shochet"]',
        '1164936310.64Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1164936310.64Shochet"]',
        '1164936338.17Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1164936338.17Shochet"]',
        '1164936402.78Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1164936402.78Shochet"]',
        '1164936419.63Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1164936419.63Shochet"]',
        '1164936439.78Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1164936439.78Shochet"]',
        '1164936491.86Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1164936491.86Shochet"]',
        '1164936513.38Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1164936513.38Shochet"]',
        '1164936682.44Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1164936682.44Shochet"]',
        '1164936686.23Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1164936686.23Shochet"]',
        '1164936727.27Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1164936727.27Shochet"]',
        '1165000116.13Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1165000116.13Shochet"]',
        '1165000125.38Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1165000125.38Shochet"]',
        '1165197002.81Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1165197002.81Shochet"]',
        '1165197032.86Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1165197032.86Shochet"]',
        '1165197123.73Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1165197123.73Shochet"]',
        '1165197146.75Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1165197146.75Shochet"]',
        '1165197181.14Shochet':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1165197181.14Shochet"]',
        '1175806714.68dzlu':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1175806714.68dzlu"]',
        '1175806851.05dzlu':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1175806851.05dzlu"]',
        '1175882228.18dzlu':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1175882228.18dzlu"]',
        '1175884051.14dzlu':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1175884051.14dzlu"]',
        '1175893134.2dzlu':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1175893134.2dzlu"]',
        '1175911936.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1175911936.0dxschafe0"]',
        '1176160384.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176160384.0dxschafe"]',
        '1176160512.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176160512.0dxschafe"]',
        '1176160640.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176160640.0dxschafe"]',
        '1176160640.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176160640.0dxschafe0"]',
        '1176160640.0dxschafe1':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176160640.0dxschafe1"]',
        '1176160768.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176160768.0dxschafe"]',
        '1176160896.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176160896.0dxschafe"]',
        '1176160896.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176160896.0dxschafe0"]',
        '1176161024.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176161024.0dxschafe"]',
        '1176161024.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176161024.0dxschafe0"]',
        '1176161152.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176161152.0dxschafe"]',
        '1176161280.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176161280.0dxschafe"]',
        '1176161280.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176161280.0dxschafe0"]',
        '1176161280.0dxschafe1':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176161280.0dxschafe1"]',
        '1176161280.0dxschafe2':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176161280.0dxschafe2"]',
        '1176161280.0dxschafe3':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176161280.0dxschafe3"]',
        '1176161280.0dxschafe4':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176161280.0dxschafe4"]',
        '1176161280.0dxschafe5':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176161280.0dxschafe5"]',
        '1176161408.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176161408.0dxschafe0"]',
        '1176161408.0dxschafe1':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176161408.0dxschafe1"]',
        '1176161408.0dxschafe2':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176161408.0dxschafe2"]',
        '1176161408.0dxschafe3':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176161408.0dxschafe3"]',
        '1176161408.0dxschafe4':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176161408.0dxschafe4"]',
        '1176161408.0dxschafe5':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1176161408.0dxschafe5"]',
        '1179346924.27Aholdun':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1179346924.27Aholdun"]',
        '1179346979.48Aholdun':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1179346979.48Aholdun"]',
        '1187042944.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1187042944.0dxschafe0"]',
        '1190664960.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1190664960.0dxschafe"]',
        '1190665088.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1190665088.0dxschafe"]',
        '1190665088.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1190665088.0dxschafe0"]',
        '1192740226.78akelts':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192740226.78akelts"]',
        '1192837197.21kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837197.21kmuller"]',
        '1192837244.65kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837244.65kmuller"]',
        '1192837255.66kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837255.66kmuller"]',
        '1192837271.26kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837271.26kmuller"]',
        '1192837304.93kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837304.93kmuller"]',
        '1192837313.66kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837313.66kmuller"]',
        '1192837328.99kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837328.99kmuller"]',
        '1192837377.15kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837377.15kmuller"]',
        '1192837583.94kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837583.94kmuller"]',
        '1192837605.99kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837605.99kmuller"]',
        '1192837619.09kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837619.09kmuller"]',
        '1192837630.48kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837630.48kmuller"]',
        '1192837655.01kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837655.01kmuller"]',
        '1192837730.34kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837730.34kmuller"]',
        '1192837772.73kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837772.73kmuller"]',
        '1192837827.37kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837827.37kmuller"]',
        '1192837844.07kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837844.07kmuller"]',
        '1192837883.85kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837883.85kmuller"]',
        '1192837939.81kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837939.81kmuller"]',
        '1192837969.85kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192837969.85kmuller"]',
        '1192838000.69kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838000.69kmuller"]',
        '1192838043.24kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838043.24kmuller"]',
        '1192838190.18kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838190.18kmuller"]',
        '1192838210.21kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838210.21kmuller"]',
        '1192838233.07kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838233.07kmuller"]',
        '1192838287.48kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838287.48kmuller"]',
        '1192838312.19kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838312.19kmuller"]',
        '1192838329.48kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838329.48kmuller"]',
        '1192838406.06kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838406.06kmuller"]',
        '1192838434.04kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838434.04kmuller"]',
        '1192838451.24kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838451.24kmuller"]',
        '1192838492.21kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838492.21kmuller"]',
        '1192838511.84kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838511.84kmuller"]',
        '1192838526.71kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838526.71kmuller"]',
        '1192838583.13kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838583.13kmuller"]',
        '1192838638.44kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838638.44kmuller"]',
        '1192838684.07kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838684.07kmuller"]',
        '1192838739.04kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1192838739.04kmuller"]',
        '1193074304.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193074304.0dxschafe"]',
        '1193074304.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193074304.0dxschafe0"]',
        '1193074304.0dxschafe1':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193074304.0dxschafe1"]',
        '1193074304.0dxschafe2':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193074304.0dxschafe2"]',
        '1193074432.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193074432.0dxschafe"]',
        '1193074432.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193074432.0dxschafe0"]',
        '1193074432.0dxschafe1':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193074432.0dxschafe1"]',
        '1193074432.0dxschafe2':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193074432.0dxschafe2"]',
        '1193074432.0dxschafe3':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193074432.0dxschafe3"]',
        '1193074432.0dxschafe4':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193074432.0dxschafe4"]',
        '1193074432.0dxschafe5':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193074432.0dxschafe5"]',
        '1193074432.0dxschafe6':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193074432.0dxschafe6"]',
        '1193074560.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193074560.0dxschafe0"]',
        '1193074560.0dxschafe1':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193074560.0dxschafe1"]',
        '1193074560.0dxschafe2':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193074560.0dxschafe2"]',
        '1193075072.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193075072.0dxschafe"]',
        '1193075072.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193075072.0dxschafe0"]',
        '1193075072.0dxschafe1':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193075072.0dxschafe1"]',
        '1193075072.0dxschafe2':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193075072.0dxschafe2"]',
        '1193075200.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193075200.0dxschafe"]',
        '1193075200.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193075200.0dxschafe0"]',
        '1193075200.0dxschafe1':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193075200.0dxschafe1"]',
        '1193075200.0dxschafe2':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193075200.0dxschafe2"]',
        '1193075328.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193075328.0dxschafe"]',
        '1193075328.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193075328.0dxschafe0"]',
        '1193076608.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193076608.0dxschafe"]',
        '1193076736.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193076736.0dxschafe"]',
        '1193076736.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193076736.0dxschafe0"]',
        '1193076736.0dxschafe1':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193076736.0dxschafe1"]',
        '1193076864.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193076864.0dxschafe"]',
        '1193076864.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193076864.0dxschafe0"]',
        '1193076864.0dxschafe1':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193076864.0dxschafe1"]',
        '1193076864.0dxschafe2':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193076864.0dxschafe2"]',
        '1193076992.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193076992.0dxschafe"]',
        '1193076992.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193076992.0dxschafe0"]',
        '1193076992.0dxschafe1':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193076992.0dxschafe1"]',
        '1193077248.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193077248.0dxschafe"]',
        '1193077376.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193077376.0dxschafe"]',
        '1193077504.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193077504.0dxschafe"]',
        '1193077632.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193077632.0dxschafe"]',
        '1193077888.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193077888.0dxschafe"]',
        '1193077888.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193077888.0dxschafe0"]',
        '1193078016.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193078016.0dxschafe"]',
        '1193078144.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193078144.0dxschafe"]',
        '1193078400.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193078400.0dxschafe"]',
        '1193078656.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193078656.0dxschafe"]',
        '1193078656.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193078656.0dxschafe0"]',
        '1193078784.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193078784.0dxschafe"]',
        '1193078784.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193078784.0dxschafe0"]',
        '1193078784.0dxschafe1':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193078784.0dxschafe1"]',
        '1193078912.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193078912.0dxschafe"]',
        '1193078912.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193078912.0dxschafe0"]',
        '1193079040.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193079040.0dxschafe"]',
        '1193079040.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193079040.0dxschafe0"]',
        '1193079040.0dxschafe1':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193079040.0dxschafe1"]',
        '1193079168.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193079168.0dxschafe"]',
        '1193079296.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193079296.0dxschafe"]',
        '1193696256.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193696256.0dxschafe"]',
        '1193696512.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193696512.0dxschafe"]',
        '1193696512.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193696512.0dxschafe0"]',
        '1193696640.0dxschafe':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193696640.0dxschafe"]',
        '1193696640.0dxschafe0':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1193696640.0dxschafe0"]',
        '1195599905.27akelts':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1195599905.27akelts"]',
        '1205365360.84kmuller':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1205365360.84kmuller"]',
        '1213043604.3akelts':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1213043604.3akelts"]',
        '1213043637.89akelts':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1213043637.89akelts"]',
        '1213043680.69akelts':
        '["Objects"]["1161798288.34sdnaik"]["Objects"]["1213043680.69akelts"]'
    }
}
extraInfo = {
    'camPos': Point3(-246.189, 7.43684, 79.9929),
    'camHpr': VBase3(158.364, -23.3602, -2.79002e-06),
    'focalLength': 1.39999997616,
    'skyState': 2,
    'fog': 0
}
