from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals
import random

class BattleRandom:
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
    
    def getRandom(self, debugString = 'Unknown'):
        randVal = self.attackRandomGen.random()
        self.attackCounter += 1
        return randVal
    
    def makeRandomChoice(self, rList):
        self.attackCounter += 1
        return self.attackRandomGen.choice(rList)
    
    def resync(self, seed = None):
        if seed is None:
            seed = self.avId
        
        self.mainRandomGen.seed(self.avId)
        self.attackRandomGen.seed(self.avId)
        self.mainCounter = 0
        self.attackCounter = 0


