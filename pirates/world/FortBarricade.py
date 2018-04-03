# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.world.FortBarricade
import math

from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import (CollisionNode, CollisionPolygon, Geom,
                                 GeomNode, GeomTriangles, GeomVertexData,
                                 GeomVertexFormat, GeomVertexWriter, NodePath,
                                 Point3, Vec3, rad2Deg)
from pirates.piratesbase import PiratesGlobals


class FortBarricade:
    __module__ = __name__
    notify = directNotify.newCategory('FortBarricade')

    def __init__(self, island, barricadeIds):
        self.island = island
        self.barricadeIds = barricadeIds
        self.colNP = []
        self.loadBarricade()

    def unload(self):
        for coll in self.colNP:
            coll.removeNode()

        self.colNP = []

    def loadBarricade(self):
        colNP1 = self.island.find('**/' + self.barricadeIds[0])
        colNP2 = self.island.find('**/' + self.barricadeIds[1])
        self.colNP = [colNP1, colNP2]

    def disableCollisions(self):
        for coll in self.colNP:
            coll.stash()

    def enableCollisions(self):
        for coll in self.colNP:
            coll.unstash()
# okay decompiling .\pirates\world\FortBarricade.pyc
