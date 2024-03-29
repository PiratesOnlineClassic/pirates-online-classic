# Embedded file name: pirates.leveleditor.worldData.SwampTestIslandA
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
            'Name': 'SwampTestIslandA',
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
                    'File': 'SwampTemplateA',
                    'Hpr': VBase3(120.19, 0.0, 0.0),
                    'Objects': {
                        '1152910301.05sdnaik0': {
                            'Type': 'Locator Node',
                            'Name': 'portal_interior_1',
                            'GridPos': Point3(-606.498, -425.911, 232.255),
                            'Hpr': VBase3(-177.386, -0.684, -0.017),
                            'Pos': Point3(400.751, 192.485, 6.419),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1152910307.13sdnaik': {
                            'Type': 'Locator Node',
                            'Name': 'portal_interior_2',
                            'GridPos': Point3(-27.183, -186.116, 232.255),
                            'Hpr': VBase3(2.192, 0.683, 0.039),
                            'Pos': Point3(-232.802, -24.141, 14.383),
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
                            'Hpr': VBase3(126.22, 0.0, 0.0),
                            'Pos': Point3(465.537, 517.058, 2.343),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1153868315.8sdnaik1': {
                            'Type': 'Locator Node',
                            'Name': 'portal_connector_2',
                            'GridPos': Point3(-155.156, -163.935, 227.03),
                            'Hpr': VBase3(-148.231, 0.0, 0.0),
                            'Pos': Point3(453.452, 255.559, 12.06),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-220.044, -854.574, 86.948),
                    'Scale': VBase3(1.0, 1.0, 1.0),
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
                            'Hpr': VBase3(126.22, 0.0, 0.0),
                            'Pos': Point3(465.537, 517.058, 2.343),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        },
                        '1153868634.75sdnaik1': {
                            'Type': 'Locator Node',
                            'Name': 'portal_connector_2',
                            'GridPos': Point3(-291.911, 214.833, 0.664),
                            'Hpr': VBase3(-148.231, 0.0, 0.0),
                            'Pos': Point3(453.452, 255.559, 12.06),
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-604.3, 157.509, -2.025),
                    'Scale': VBase3(1.0, 1.0, 1.0),
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
