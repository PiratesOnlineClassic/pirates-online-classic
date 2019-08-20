from direct.distributed import DistributedNode
from direct.task import Task
from direct.distributed.ClockDelta import *
from pirates.ship import ShipGlobals

class DistributedCharterableObject(DistributedNode.DistributedNode):
    notify = directNotify.newCategory('DistributedCharterableObject')
    
    def __init__(self, cr):
        DistributedNode.DistributedNode.__init__(self, cr)
        self.isInPort = ''
        self.charterTimestamp = 0
        self.ownerId = 0
        self.timerTime = 0
        self.timerTimestamp = 0
        self.charter = 0

    def setCharterTimestamp(self, val):
        self.charterTimestamp = val
        if self.charterTimestamp != 0:
            self.startCharterTask()
        else:
            self.stopCharterTask()

    def getCharterTimestamp(self):
        return self.charterTimestamp

    def startCharterTask(self):
        taskMgr.add(self.charterTask, self.uniqueName('shipCharterTask'))

    def stopCharterTask(self):
        taskMgr.remove(self.uniqueName('shipCharterTask'))
    
    def charterTask(self, task):
        ts = globalClockDelta.localElapsedTime(self.charterTimestamp)
        if ts >= ShipGlobals.CHARTER_DURATION:
            return Task.done
        else:
            return Task.cont
    
    def setOwnerId(self, doId):
        self.ownerId = doId

    def getOwnerId(self):
        return self.ownerId
    
    def setCharter(self, val):
        self.charter = val
    
    def getCharter(self):
        return self.charter

    def setTimer(self, time, timestamp):
        elapsedTime = globalClockDelta.localElapsedTime(timestamp)
        localTime = globalClock.getFrameTime()
        self.timerTimestamp = localTime - elapsedTime
        self.timerTime = time
    
    def getTimer(self):
        return self.timerTimestamp

    def getTimeLeft(self):
        timePassed = globalClock.getFrameTime() - self.timerTimestamp
        return max(0, self.timerTime - timePassed)


