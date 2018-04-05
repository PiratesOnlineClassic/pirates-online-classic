from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.distributed.ClockDelta import globalClockDelta
from pirates.piratesbase import TODGlobals, PiratesGlobals
import random
import time


class DistributedTimeOfDayManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTimeOfDayManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.cycleType = config.GetInt('tod-starting-cycle', TODGlobals.TOD_REGULAR_CYCLE)
        self.startingState = TODGlobals.getStartingState(self.cycleType)
        self.startingTime = globalClockDelta.getFrameNetworkTime(bits=32)
        self.cycleDuration = TODGlobals.getStateDuration(self.cycleType, self.startingState)
        self.cycleTask = None
   
    def sync(self, cycleType, startingState, startingTime, cycleDuration):
        self.cycleType = cycleType
        self.startingState = startingState
        self.startingTime = startingTime
        self.cycleDuration = cycleDuration

    def d_sync(self, cycleType, startingState, startingTime, cycleDuration):
        self.sendUpdate('syncTOD', [cycleType, startingState, startingTime, cycleDuration])

    def b_sync(self, cycleType, startingState, startingTime, cycleDuration):
        self.sync(cycleType, startingState, startingTime, cycleDuration)
        self.d_sync(cycleType, startingState, startingTime, cycleDuration)

    def getSync(self):
        return [self.cycleType, self.startingState, self.startingTime, self.cycleDuration]
