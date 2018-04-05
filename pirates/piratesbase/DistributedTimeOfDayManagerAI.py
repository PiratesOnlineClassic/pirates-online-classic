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
        self.timeOffset = 0
        self.cycleTask = None

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.cycleTask = taskMgr.doMethodLater(1, self.__runCycle, self.uniqueName('runCycle'))

    def delete(self):
        DistributedObjectAI.delete(self)

        if self.cycleTask:
            taskMgr.remove(self.cycleTask)

    def __runCycle(self, task):
        REALSECONDS_PER_GAMEHOUR = PiratesGlobals.TOD_CYCLE_DURATION / self.cycleSpeed
        self.timeOffset += REALSECONDS_PER_GAMEHOUR 

        if self.getCurrentIngameTime() >= 24:
            self.timeOffset = 0

        return task.again

    def getCurrentIngameTime(self, time=None):
        cycleSpeed = self.cycleSpeed
        if cycleSpeed <= 0:
            cycleSpeed = 1

        if time is None:
            currentTime = globalClockDelta.networkToLocalTime(
                globalClockDelta.getFrameNetworkTime(bits=32))
        else:
            currentTime = time
       
        REALSECONDS_PER_GAMEDAY = PiratesGlobals.TOD_CYCLE_DURATION / cycleSpeed
        REALSECONDS_PER_GAMEHOUR = float(REALSECONDS_PER_GAMEDAY / 24)
        cycleDuration = REALSECONDS_PER_GAMEHOUR * 24
        timeElapsed = currentTime - self.startingNetTime
        timeIntoCycle = (timeElapsed + self.timeOffset) % cycleDuration
        hoursIntoCycle = timeIntoCycle / REALSECONDS_PER_GAMEHOUR
        return hoursIntoCycle


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
