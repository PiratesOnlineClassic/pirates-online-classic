# Embedded file name: pirates.leveleditor.worldData.pvpTest
from pandac.PandaModules import Point3, VBase3
objectStruct = {
    'Layers': {},
    'Objects': {
        '1126901258.68jubutler': {
            'Type': 'Region',
            'Name': 'pvpTest',
            'Objects': {
                '1126901305.54jubutler': {
                    'Type': 'Island',
                    'File': 'pvpTestIsle',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Objects': {},
                    'Pos': Point3(0.0, 0.0, 0.0),
                    'Visual': {
                        'Model': 'models/islands/Island_A'
                    }
                },
                '1127785102.03jubutler': {
                    'Type': 'Ship Spawn Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Level': '3',
                    'Pos': Point3(-471.499, -134.551, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Interceptor',
                    'Team': '0'
                },
                '1127785172.39jubutler': {
                    'Type': 'Ship Spawn Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Level': '3',
                    'Pos': Point3(556.542, 152.356, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Spawnables': 'Interceptor',
                    'Team': '0'
                }
            }
        }
    },
    'Node Links': [],
    'ObjectIds': {
        '1126901258.68jubutler':
        '["Objects"]["1126901258.68jubutler"]',
        '1126901305.54jubutler':
        '["Objects"]["1126901258.68jubutler"]["Objects"]["1126901305.54jubutler"]',
        '1127785102.03jubutler':
        '["Objects"]["1126901258.68jubutler"]["Objects"]["1127785102.03jubutler"]',
        '1127785172.39jubutler':
        '["Objects"]["1126901258.68jubutler"]["Objects"]["1127785172.39jubutler"]'
    }
}
