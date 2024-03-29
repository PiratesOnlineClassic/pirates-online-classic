# Embedded file name: pirates.leveleditor.worldData.GameAreaSandboxSwampA
from pandac.PandaModules import Point3, VBase3
objectStruct = {
    'Objects': {
        '1163554577.81sdnaik': {
            'Type': 'Island Game Area',
            'Name': 'GameAreaSandboxSwampA',
            'Objects': {
                '1163719088.81sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_1',
                    'Hpr': VBase3(-177.386, -0.684, -0.017),
                    'Pos': Point3(400.751, 192.485, 6.419),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                },
                '1163719088.83sdnaik': {
                    'Type': 'Locator Node',
                    'Name': 'portal_interior_2',
                    'Hpr': VBase3(2.192, 0.683, 0.039),
                    'Pos': Point3(-232.802, -24.141, 14.383),
                    'Scale': VBase3(1.0, 1.0, 1.0)
                }
            },
            'Visual': {
                'Model': 'models/swamps/swampA'
            }
        }
    },
    'Node Links': [],
    'Layers': {},
    'ObjectIds': {
        '1163554577.81sdnaik':
        '["Objects"]["1163554577.81sdnaik"]',
        '1163719088.81sdnaik':
        '["Objects"]["1163554577.81sdnaik"]["Objects"]["1163719088.81sdnaik"]',
        '1163719088.83sdnaik':
        '["Objects"]["1163554577.81sdnaik"]["Objects"]["1163719088.83sdnaik"]'
    }
}
