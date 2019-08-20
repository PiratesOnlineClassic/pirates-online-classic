# Embedded file name: pirates.leveleditor.worldData.singleShipWorld
from pandac.PandaModules import Point3, VBase3
objectStruct = {
    'Objects': {
        '1156905185.74jubutler': {
            'Type': 'Region',
            'Name': 'default',
            'Objects': {
                '1156905402.6jubutler': {
                    'Type': 'Ship Part',
                    'Category': 'Merchant',
                    'File': '',
                    'Flagship': False,
                    'Hpr': VBase3(-67.7, 0.0, 0.0),
                    'Pos': Point3(12.872, 197.322, 0.0),
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Idle',
                    'Team': 'Player',
                    'Visual': {
                        'Model': [
                            'models/shipparts/merchantL2-geometry_High',
                            'models/shipparts/merchantL2-collisions',
                            'models/shipparts/merchantCabinAL2-collisions',
                            'models/shipparts/merchantCabinAL2-geometry_High'
                        ]
                    }
                },
                '1156905870.58jubutler': {
                    'Type': 'Island',
                    'File': '',
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(0.559, -6.692, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/islands/Tiny_island_A'
                    }
                }
            },
            'Visual': {}
        }
    },
    'Layers': {},
    'ObjectIds': {
        '1156905185.74jubutler':
        '["Objects"]["1156905185.74jubutler"]',
        '1156905402.6jubutler':
        '["Objects"]["1156905185.74jubutler"]["Objects"]["1156905402.6jubutler"]',
        '1156905870.58jubutler':
        '["Objects"]["1156905185.74jubutler"]["Objects"]["1156905870.58jubutler"]'
    }
}
