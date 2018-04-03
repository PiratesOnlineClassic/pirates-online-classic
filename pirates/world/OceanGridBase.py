# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.world.OceanGridBase
from pandac.PandaModules import *


class OceanGridBase:
    __module__ = __name__

    def __init__(self):
        NodePath.__init__(self, 'OceanGrid')

    def setWorld(self, world):
        self.world = world
        self.parentNP = world.getInstanceNodePath()
        self.reparentTo(self.parentNP)

    def addObjectToOceanGrid(self, av):
        pass

    def removeObjectFromOceanGrid(self, av):
        pass
# okay decompiling .\pirates\world\OceanGridBase.pyc
