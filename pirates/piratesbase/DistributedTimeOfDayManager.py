# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesbase.DistributedTimeOfDayManager
from direct.distributed.ClockDelta import globalClockDelta
from direct.distributed.DistributedObject import DistributedObject
from pirates.piratesbase import TODGlobals
from TimeOfDayManager import TimeOfDayManager


class DistributedTimeOfDayManager(DistributedObject, TimeOfDayManager):
    __module__ = __name__
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
        return

    def delete(self):
        TimeOfDayManager.delete(self)
        DistributedObject.delete(self)

    def sync(self, cycleType, startingState, startingTime, cycleDuration):
        self.cycleType = cycleType
        self.startingState = startingState
        self.startingTime = startingTime
        self.cycleDuration = cycleDuration
        self.enterInitState()
# okay decompiling .\pirates\piratesbase\DistributedTimeOfDayManager.pyc
