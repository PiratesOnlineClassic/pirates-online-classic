
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPopulationTrackerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPopulationTrackerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.shardId = 0
        self.population = 0
        self.popLimits = [0, 0]


    # setShardId(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setShardId(self, shardId):
        self.shardId = shardId

    def d_setShardId(self, shardId):
        self.sendUpdate('setShardId', [shardId])

    def b_setShardId(self, shardId):
        self.setShardId(shardId)
        self.d_setShardId(shardId)

    def getShardId(self):
        return self.shardId

    # setPopulation(uint16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setPopulation(self, population):
        self.population = population

    def d_setPopulation(self, population):
        self.sendUpdate('setPopulation', [population])

    def b_setPopulation(self, population):
        self.setPopulation(population)
        self.d_setPopulation(population)

    def getPopulation(self):
        return self.population

    # setPopLimits(uint16, uint16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setPopLimits(self, popLimits, todo_uint16_1):
        self.popLimits = popLimits

    def d_setPopLimits(self, popLimits, todo_uint16_1):
        self.sendUpdate('setPopLimits', [popLimits, todo_uint16_1])

    def b_setPopLimits(self, popLimits, todo_uint16_1):
        self.setPopLimits(popLimits, todo_uint16_1)
        self.d_setPopLimits(popLimits, todo_uint16_1)

    def getPopLimits(self):
        return self.popLimits


