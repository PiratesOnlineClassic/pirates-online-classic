from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.ClockDelta import globalClockDelta
from TimeOfDayManager import TimeOfDayManager
from pirates.piratesbase import TODGlobals

class DistributedTimeOfDayManager(DistributedObject, TimeOfDayManager):
    from direct.directnotify import DirectNotifyGlobal
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTimeOfDayManager')
    
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        TimeOfDayManager.__init__(self)

    def generate(self):
        self.cr.timeOfDayManager = self
        DistributedObject.generate(self)
    
    def disable(self):
        TimeOfDayManager.disable(self)
        DistributedObject.disable(self)
        if self.cr.timeOfDayManager == self:
            self.cr.timeOfDayManager = None
    
    def delete(self):
        TimeOfDayManager.delete(self)
        DistributedObject.delete(self)
    
    def sync(self, cycleType, startingState, startingTime, cycleDuration):
        self.cycleType = cycleType
        self.startingState = startingState
        self.startingTime = startingTime
        self.cycleDuration = cycleDuration
        self.enterInitState()


