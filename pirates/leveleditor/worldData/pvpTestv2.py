# Embedded file name: pirates.leveleditor.worldData.pvpTestv2
from pandac.PandaModules import Point3, VBase3
objectStruct = {
    'Objects': {
        '1128540775.81jubutler': {
            'Type': 'Region',
            'Name': 'pvpCTLw00',
            'Objects': {
                '1128540801.88jubutler': {
                    'Type': 'Island',
                    'File': 'pvpTestIslev2',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Objects': {
                        '1128541283.64jubutler': {
                            'Type': 'LOD Sphere',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(98.71, 144.17, 137.56),
                            'Radi': [1973, 2273, 2573],
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(-20.329, 208.386, 0.348),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/islands/pvp_b_zero'
                    }
                },
                '1128545304.45jubutler': {
                    'Type': 'Ship Spawn Node',
                    'Hpr': VBase3(174.311, 0.0, 0.0),
                    'Level': '3',
                    'Pos': Point3(-340.74, 879.055, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Merchant',
                    'Team': '0'
                },
                '1128545309.55jubutler': {
                    'Type': 'Ship Spawn Node',
                    'Hpr': VBase3(-166.14, 0.0, 0.0),
                    'Level': '3',
                    'Pos': Point3(306.496, 929.333, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Merchant',
                    'Team': '0'
                }
            }
        }
    },
    'Node Links': [],
    'Layers': {},
    'ObjectIds': {
        '1128540775.81jubutler':
        '["Objects"]["1128540775.81jubutler"]',
        '1128540801.88jubutler':
        '["Objects"]["1128540775.81jubutler"]["Objects"]["1128540801.88jubutler"]',
        '1128541283.64jubutler':
        '["Objects"]["1128540775.81jubutler"]["Objects"]["1128540801.88jubutler"]["Objects"]["1128541283.64jubutler"]',
        '1128545304.45jubutler':
        '["Objects"]["1128540775.81jubutler"]["Objects"]["1128545304.45jubutler"]',
        '1128545309.55jubutler':
        '["Objects"]["1128540775.81jubutler"]["Objects"]["1128545309.55jubutler"]'
    }
}
