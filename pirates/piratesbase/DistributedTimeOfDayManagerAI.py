from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from pirates.piratesbase import TODGlobals, PiratesGlobals
from direct.distributed.ClockDelta import globalClockDelta
import random
import time


class DistributedTimeOfDayManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTimeOfDayManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.cycleType = TODGlobals.TOD_REGULAR_CYCLE
        self.cycleSpeed = config.GetInt('tod-cycle-speed', 1)
        self.startingNetTime = globalClockDelta.getFrameNetworkTime(bits=32)
        self.timeOffset = time.time() % PiratesGlobals.TOD_CYCLE_DURATION

    def delete(self):
        DistributedObjectAI.delete(self)

    def sync(self, cycleType, cycleSpeed, startingNetTime, timeOffset):
        self.cycleType = cycleType
        self.cycleSpeed = cycleSpeed
        self.startingNetTime = startingNetTime
        self.timeOffset = timeOffset

    def d_sync(self, cycleType, cycleSpeed, startingNetTime, timeOffset):
        self.sendUpdate('syncTOD', [cycleType, cycleSpeed, startingNetTime, timeOffset])

    def b_sync(self, cycleType, cycleSpeed, startingNetTime, timeOffset):
        self.sync(cycleType, cycleSpeed, startingNetTime, timeOffset)
        self.d_sync(cycleType, cycleSpeed, startingNetTime, timeOffset)

    def getSync(self):
        return [self.cycleType, self.cycleSpeed, self.startingNetTime, self.timeOffset]
