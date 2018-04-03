# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.distributed.DistributedPopulationTracker
from direct.distributed.DistributedObject import DistributedObject

class DistributedPopulationTracker(DistributedObject):
    __module__ = __name__

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.shardId = 0
        self.population = 0
        self.popLimits = [0, 0]

    def __str__(self):
        return 'PopTracker(%s): %5s' % (self.shardId, self.population)

    def disable(self):
        messenger.send('ShardPopulationUpdate', sentArgs=[self.shardId, -1])
        DistributedObject.disable(self)

    def setShardId(self, shardId):
        self.shardId = shardId

    def getShardId(self):
        return self.shardId

    def setPopulation(self, population):
        self.population = population
        messenger.send('ShardPopulationUpdate', sentArgs=[self.shardId, self.population])

    def getPopulation(self):
        return self.population

    def setPopLimits(self, min, max):
        self.popLimits = (
         min, max)
        messenger.send('ShardPopLimitsUpdate', sentArgs=[self.shardId, min, max])

    def getPopLimits(self):
        return self.popLimits
# okay decompiling .\pirates\distributed\DistributedPopulationTracker.pyc
