# Embedded file name: pirates.leveleditor.worldData.treasureMapCove
from pandac.PandaModules import Point3, VBase3
objectStruct = {
    'Objects': {
        '1115838788.58jubutler': {
            'Type': 'Region',
            'Name': 'treasureMapCove',
            'Objects': {
                '1115838800.3jubutler': {
                    'Type': 'Island',
                    'File': 'treasureMapIsle',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(3.2, 36.198, -2.048),
                    'Visual': {
                        'Model': 'models/islands/wild_island_a_zero'
                    }
                },
                '1121231173.75jubutler': {
                    'Type': 'Player Spawn Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(-311.209, -1780.159, 0.0)
                }
            }
        }
    },
    'Node Links': [],
    'ObjectIds': {
        '1115838788.58jubutler':
        '["Objects"]["1115838788.58jubutler"]',
        '1115838800.3jubutler':
        '["Objects"]["1115838788.58jubutler"]["Objects"]["1115838800.3jubutler"]',
        '1121231173.75jubutler':
        '["Objects"]["1115838788.58jubutler"]["Objects"]["1121231173.75jubutler"]'
    }
}
