# Embedded file name: pirates.leveleditor.worldData.RambleshackWorld
from pandac.PandaModules import Point3, VBase3
objectStruct = {
    'Objects': {
        '1115838788a.58jubutler': {
            'Type': 'Region',
            'Name': 'RambleshackWorld',
            'Objects': {
                '1115838800a.3jubutler': {
                    'Type': 'Island',
                    'Name': 'Rambleshack',
                    'File': 'Rambleshack',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Objects': {
                        '1157100709.96jubutler': {
                            'Type': 'LOD Sphere',
                            'Hpr': Point3(0.0, 0.0, 0.0),
                            'Pos': Point3(0.0, 0.0, -9.221),
                            'Radi': [11498, 12498, 13498],
                            'Scale': VBase3(1.0, 1.0, 1.0)
                        }
                    },
                    'Pos': Point3(0.0, 0.0, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/islands/rambleshack_zero'
                    }
                },
                '1124236671.37jubutler': {
                    'Type': 'Ship Part',
                    'Category': 'InterceptorTutorial',
                    'File': '',
                    'Flagship': False,
                    'Hpr': VBase3(-114.033, 0.0, 0.0),
                    'Pos': Point3(128.511, 152.104, 0.0),
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Idle',
                    'Team': 'Player',
                    'Visual': {
                        'Model': 'models/shipparts/interceptorL1'
                    }
                },
                '1125013326.85jubutler': {
                    'Type': 'Ship Movement Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(295.185, 181.66, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/misc/smiley'
                    }
                },
                '1171449664.73MAsaduzz': {
                    'Type': 'Ship Movement Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(672.532, 405.492, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1171449676.98MAsaduzz': {
                    'Type': 'Ship Movement Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(527.776, 787.869, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1171449691.62MAsaduzz': {
                    'Type': 'Ship Movement Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(101.138, 707.24, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                },
                '1171449714.51MAsaduzz': {
                    'Type': 'Ship Movement Node',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(-18.992, 322.654, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Color': (0.65, 0, 0, 1),
                        'Model': 'models/misc/smiley'
                    }
                }
            }
        }
    },
    'Node Links':
    [['1124236671.37jubutler', '1125013326.85jubutler', 'Direction 2'],
     ['1171449664.73MAsaduzz', '1125013326.85jubutler', 'Direction 1'],
     ['1171449664.73MAsaduzz', '1171449676.98MAsaduzz', 'Direction 2'],
     ['1171449676.98MAsaduzz', '1171449691.62MAsaduzz', 'Direction 2'],
     ['1171449714.51MAsaduzz', '1171449691.62MAsaduzz', 'Direction 1'],
     ['1171449714.51MAsaduzz', '1125013326.85jubutler', 'Direction 2']],
    'Layers': {},
    'ObjectIds': {
        '1115838788a.58jubutler':
        '["Objects"]["1115838788a.58jubutler"]',
        '1115838800a.3jubutler':
        '["Objects"]["1115838788a.58jubutler"]["Objects"]["1115838800a.3jubutler"]',
        '1124236671.37jubutler':
        '["Objects"]["1115838788a.58jubutler"]["Objects"]["1124236671.37jubutler"]',
        '1125013326.85jubutler':
        '["Objects"]["1115838788a.58jubutler"]["Objects"]["1125013326.85jubutler"]',
        '1157100709.96jubutler':
        '["Objects"]["1115838788a.58jubutler"]["Objects"]["1115838800a.3jubutler"]["Objects"]["1157100709.96jubutler"]',
        '1171449664.73MAsaduzz':
        '["Objects"]["1115838788a.58jubutler"]["Objects"]["1171449664.73MAsaduzz"]',
        '1171449676.98MAsaduzz':
        '["Objects"]["1115838788a.58jubutler"]["Objects"]["1171449676.98MAsaduzz"]',
        '1171449691.62MAsaduzz':
        '["Objects"]["1115838788a.58jubutler"]["Objects"]["1171449691.62MAsaduzz"]',
        '1171449714.51MAsaduzz':
        '["Objects"]["1115838788a.58jubutler"]["Objects"]["1171449714.51MAsaduzz"]'
    }
}
