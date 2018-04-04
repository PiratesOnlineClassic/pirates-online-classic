
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBuriedTreasureAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBuriedTreasureAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.startingDepth = 0
        self.currentDepth = 0


    # setStartingDepth(uint16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setStartingDepth(self, startingDepth):
        self.startingDepth = startingDepth

    def d_setStartingDepth(self, startingDepth):
        self.sendUpdate('setStartingDepth', [startingDepth])

    def b_setStartingDepth(self, startingDepth):
        self.setStartingDepth(startingDepth)
        self.d_setStartingDepth(startingDepth)

    def getStartingDepth(self):
        return self.startingDepth

    # setCurrentDepth(uint16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setCurrentDepth(self, currentDepth):
        self.currentDepth = currentDepth

    def d_setCurrentDepth(self, currentDepth):
        self.sendUpdate('setCurrentDepth', [currentDepth])

    def b_setCurrentDepth(self, currentDepth):
        self.setCurrentDepth(currentDepth)
        self.d_setCurrentDepth(currentDepth)

    def getCurrentDepth(self):
        return self.currentDepth

    # showTreasure(uint16) broadcast

    def showTreasure(self, showTreasure):
        self.sendUpdate('showTreasure', [showTreasure])

    # startDigging()

    def startDigging(self, startDigging):
        self.sendUpdate('startDigging', [startDigging])

    # stopDigging(uint16)

    def stopDigging(self, stopDigging):
        self.sendUpdate('stopDigging', [stopDigging])


