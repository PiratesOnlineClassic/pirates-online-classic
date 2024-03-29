# Embedded file name: pirates.leveleditor.worldData.SwampTestIsland
from pandac.PandaModules import Point3, VBase3
objectStruct = {
    'Locator Links':
    [['1153868315.8sdnaik0', '1152910060.11sdnaik', 'Bi-directional'],
     ['1153868315.8sdnaik1', '1152910301.05sdnaik0', 'Bi-directional'],
     ['1153868634.75sdnaik0', '1152910060.11sdnaik0', 'Bi-directional'],
     ['1152910307.13sdnaik', '1153868634.75sdnaik1', 'Bi-directional']],
    'Objects': {
        '1152909972.77sdnaik': {
            'Type': 'Island',
            'Name': 'SwampTestIsland',
            'File': '',
            'Objects': {
                '1152910060.11sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_exterior_1',
                    'Hpr': VBase3(-18.331, 0.0, 0.0),
                    'Pos': Point3(-219.917, -319.235, 0.595),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1152910060.11sdnaik0': {
                    'Type': 'Locator Node',
                    'Name': 'portal_exterior_2',
                    'Hpr': VBase3(68.97, 0.0, 0.0),
                    'Pos': Point3(-285.103, -58.817, 44.049),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1152910301.05sdnaik': {
                    'Type': 'Island Game Area',
                    'File': 'SwampAreaA',
                    'Hpr': VBase3(120.19, 0.0, 0.0),
                    'Objects': {
                        '1152910301.05sdnaik0': {
                            'Type': 'Locator Node',
                            'Name': 'portal_interior_1',
                            'GridPos': Point3(-606.498, -425.911, 232.255),
                            'Hpr': VBase3(-7.207, 0.0, 0.0),
                            'Pos': Point3(-228.544, -32.226, 9.648),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1152910307.13sdnaik': {
                            'Type': 'Locator Node',
                            'Name': 'portal_interior_2',
                            'GridPos': Point3(-27.183, -186.116, 232.255),
                            'Hpr': VBase3(172.793, 0.0, 0.0),
                            'Pos': Point3(350.771, 207.569, 9.648),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-678.389, -998.616, 222.606),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/swamps/swampA'
                    }
                },
                '1153868315.8sdnaik': {
                    'Type': 'Connector Tunnel',
                    'File': '',
                    'Hpr': VBase3(-166.005, 0.0, 0.0),
                    'Objects': {
                        '1153868315.8sdnaik0': {
                            'Type': 'Locator Node',
                            'Name': 'portal_connector_1',
                            'Hpr': VBase3(-89.513, 0.0, 0.0),
                            'Pos': Point3(0.0, 0.0, 0.0),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1153868315.8sdnaik1': {
                            'Type': 'Locator Node',
                            'Name': 'portal_connector_2',
                            'GridPos': Point3(-155.156, -163.935, 227.03),
                            'Hpr': VBase3(90.682, 0.0, 0.0),
                            'Pos': Point3(162.228, 206.91, 9.831),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-220.044, -854.574, 86.948),
                    'Visual': {
                        'Model': 'models/tunnels/tunnel_swamp_cave'
                    }
                },
                '1153868634.75sdnaik': {
                    'Type': 'Connector Tunnel',
                    'File': '',
                    'Hpr': VBase3(107.362, 0.0, 0.0),
                    'Objects': {
                        '1153868634.75sdnaik0': {
                            'Type': 'Locator Node',
                            'Name': 'portal_connector_1',
                            'Hpr': VBase3(-89.513, 0.0, 0.0),
                            'Pos': Point3(0.0, 0.0, 0.0),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1153868634.75sdnaik1': {
                            'Type': 'Locator Node',
                            'Name': 'portal_connector_2',
                            'GridPos': Point3(-291.911, 214.833, 0.664),
                            'Hpr': VBase3(90.682, 0.0, 0.0),
                            'Pos': Point3(162.228, 206.91, 9.831),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-604.3, 157.509, -2.025),
                    'Visual': {
                        'Model': 'models/tunnels/tunnel_swamp_cave'
                    }
                }
            },
            'Visual': {
                'Model': 'models/islands/bilgewater_zero'
            }
        }
    },
    'Node Links': [],
    'Layers': {},
    'ObjectIds': {
        '1152909972.77sdnaik':
        '["Objects"]["1152909972.77sdnaik"]',
        '1152910060.11sdnaik':
        '["Objects"]["1152909972.77sdnaik"]["Objects"]["1152910060.11sdnaik"]',
        '1152910060.11sdnaik0':
        '["Objects"]["1152909972.77sdnaik"]["Objects"]["1152910060.11sdnaik0"]',
        '1152910301.05sdnaik':
        '["Objects"]["1152909972.77sdnaik"]["Objects"]["1152910301.05sdnaik"]',
        '1152910301.05sdnaik0':
        '["Objects"]["1152909972.77sdnaik"]["Objects"]["1152910301.05sdnaik"]["Objects"]["1152910301.05sdnaik0"]',
        '1152910307.13sdnaik':
        '["Objects"]["1152909972.77sdnaik"]["Objects"]["1152910301.05sdnaik"]["Objects"]["1152910307.13sdnaik"]',
        '1153868315.8sdnaik':
        '["Objects"]["1152909972.77sdnaik"]["Objects"]["1153868315.8sdnaik"]',
        '1153868315.8sdnaik0':
        '["Objects"]["1152909972.77sdnaik"]["Objects"]["1153868315.8sdnaik"]["Objects"]["1153868315.8sdnaik0"]',
        '1153868315.8sdnaik1':
        '["Objects"]["1152909972.77sdnaik"]["Objects"]["1153868315.8sdnaik"]["Objects"]["1153868315.8sdnaik1"]',
        '1153868634.75sdnaik':
        '["Objects"]["1152909972.77sdnaik"]["Objects"]["1153868634.75sdnaik"]',
        '1153868634.75sdnaik0':
        '["Objects"]["1152909972.77sdnaik"]["Objects"]["1153868634.75sdnaik"]["Objects"]["1153868634.75sdnaik0"]',
        '1153868634.75sdnaik1':
        '["Objects"]["1152909972.77sdnaik"]["Objects"]["1153868634.75sdnaik"]["Objects"]["1153868634.75sdnaik1"]'
    }
}
