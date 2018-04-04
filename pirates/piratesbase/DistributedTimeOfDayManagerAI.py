from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
from pirates.piratesbase import TODGlobals

class DistributedTimeOfDayManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTimeOfDayManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.baseCycle = config.GetInt('tod-starting-cycle', TODGlobals.TOD_REGULAR_CYCLE)
        self.cycleType = self.baseCycle
        self.cycleSpeed = config.GetInt('tod-cycle-speed', 1)
        self.startingNetTime = globalClockDelta.getRealNetworkTime(bits=32)
        self.timeOffset = 0

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