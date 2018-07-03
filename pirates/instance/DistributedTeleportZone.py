# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.instance.DistributedTeleportZone
from pirates.instance import DistributedInstanceBase
from pandac.PandaModules import NodePath

class DistributedTeleportZone(DistributedInstanceBase.DistributedInstanceBase, NodePath):
    

    def __init__(self, cr):
        DistributedInstanceBase.DistributedInstanceBase.__init__(self, cr)

    def getInstanceNodePath(self):
        return self
# okay decompiling .\pirates\instance\DistributedTeleportZone.pyc
