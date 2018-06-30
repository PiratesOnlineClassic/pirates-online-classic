import math

from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals


class FortBarricade:
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
