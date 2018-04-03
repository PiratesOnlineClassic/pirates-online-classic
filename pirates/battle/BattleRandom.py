# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.battle.BattleRandom
import random

from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals


class BattleRandom:
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleRandom')

    def __init__(self, avId):
        self.avId = avId
        self.mainRandomGen = random.Random()
        self.mainRandomGen.seed(self.avId)
        self.attackRandomGen = random.Random()
        self.attackRandomGen.seed(self.avId)
        self.mainCounter = 0
        self.attackCounter = 0

    def delete(self):
        del self.mainRandomGen
        del self.attackRandomGen

    def advanceAttackSeed(self):
        r = self.mainRandomGen.random()
        self.mainCounter += 1
        self.attackCounter = 0
        self.attackRandomGen.seed(int(self.avId * r))

    def getRandom(self, debugString='Unknown'):
        randVal = self.attackRandomGen.random()
        self.attackCounter += 1
        return randVal

    def makeRandomChoice(self, rList):
        self.attackCounter += 1
        return self.attackRandomGen.choice(rList)

    def resync(self, seed=None):
        if seed is None:
            seed = self.avId
        self.mainRandomGen.seed(self.avId)
        self.attackRandomGen.seed(self.avId)
        self.mainCounter = 0
        self.attackCounter = 0
        return
# okay decompiling .\pirates\battle\BattleRandom.pyc
