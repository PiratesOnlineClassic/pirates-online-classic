# Embedded file name: pirates.leveleditor.worldData.tortuga_building_int_9
from pandac.PandaModules import Point3, VBase3, Vec4
objectStruct = {
    'Objects': {
        '1156207423.67dzlu0': {
            'Type': 'Building Interior',
            'Name': '',
            'AdditionalData': ['interior_spanish_doctor'],
            'Instanced': True,
            'Objects': {
                '1169068641.66mike': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'AnimSet': 'doctor_work',
                    'CustomModel': 'None',
                    'Hpr': VBase3(-35.951, 0.0, 0.0),
                    'Patrol Radius': 12,
                    'Pos': Point3(0.394, -6.076, 0.0),
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Idle',
                    'Team': 'Villager'
                },
                '1169069336.52mike': {
                    'Type': 'Furniture',
                    'DisableCollision': False,
                    'Hpr': Point3(0.0, 0.0, 0.0),
                    'Pos': Point3(0.966, -9.28, 0.0),
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Visual': {
                        'Model': 'models/props/table_bar_square'
                    }
                },
                '1169078025.53mike': {
                    'Type': 'Townsperson',
                    'Category': 'Commoner',
                    'AnimSet': 'patient_work',
                    'CustomModel': 'None',
                    'Hpr': VBase3(91.269, 0.0, 0.0),
                    'Patrol Radius': 12,
                    'Pos': Point3(9.713, 16.168, 0.322),
                    'Private Status': 'All',
                    'Respawns': True,
                    'Scale': VBase3(1.0, 1.0, 1.0),
                    'Start State': 'Idle',
                    'Team': 'Villager'
                },
                '1180115072.0dchiappe1': {
                    'Type': 'Mortar_Pestle',
                    'Hpr': VBase3(0.0, 0.0, 0.0),
                    'Pos': Point3(0.775, -8.512, 2.937),
                    'Scale': VBase3(0.703, 0.703, 0.703),
                    'Visual': {
                        'Model': 'models/props/mortar_pestle_stone'
                    }
                }
            },
            'Visual': {
                'Model': 'models/buildings/interior_spanish_npc'
            }
        }
    },
    'Node Links': [],
    'Layers': {},
    'ObjectIds': {
        '1156207423.67dzlu0':
        '["Objects"]["1156207423.67dzlu0"]',
        '1169068641.66mike':
        '["Objects"]["1156207423.67dzlu0"]["Objects"]["1169068641.66mike"]',
        '1169069336.52mike':
        '["Objects"]["1156207423.67dzlu0"]["Objects"]["1169069336.52mike"]',
        '1169078025.53mike':
        '["Objects"]["1156207423.67dzlu0"]["Objects"]["1169078025.53mike"]',
        '1180115072.0dchiappe1':
        '["Objects"]["1156207423.67dzlu0"]["Objects"]["1180115072.0dchiappe1"]'
    }
}
