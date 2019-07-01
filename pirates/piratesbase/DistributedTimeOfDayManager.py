from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.ClockDelta import globalClockDelta
from otp.ai.MagicWordGlobal import *
from TimeOfDayManager import TimeOfDayManager
from pirates.piratesbase import TODGlobals
from pirates.effects.FireworkGlobals import *


class DistributedTimeOfDayManager(DistributedObject, TimeOfDayManager):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTimeOfDayManager')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        TimeOfDayManager.__init__(self)

        self.rainDrops = None
        self.rainMist = None
        self.rainSplashes = None
        self.rainSplashes2 = None

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


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def clouds(level):
    """
    Locally sets the timeOfDayManager cloud state
    """

    base.cr.timeOfDayManager.skyGroup.transitionClouds(level).start()
    return 'Transitioning clouds to %d.' % level


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def fireworks(showType=FireworkShowType.FourthOfJuly):
    """
    Locally enables or disables Fourth of July fireworks
    """

    timestamp = globalClockDelta.localElapsedTime(base.cr.timeOfDayManager.startingTime, bits=32)
    if base.cr.activeWorld:
        if not base.cr.activeWorld.fireworkShowMgr:
            base.cr.activeWorld.enableFireworkShow(timestamp, showType)
        else:
            base.cr.activeWorld.disableFireworkShow()

    return "Toggled fireworks show with type: %d" % showType

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def rain():
    """
    Toggles local rain state
    """

    if base.cr.timeOfDayManager.rainDrops:
        base.cr.timeOfDayManager.rainDrops.stopLoop()
        base.cr.timeOfDayManager.rainDrops = None
        if base.cr.timeOfDayManager.rainMist:
            base.cr.timeOfDayManager.rainMist.stopLoop()
            base.cr.timeOfDayManager.rainMist = None

        if base.cr.timeOfDayManager.rainSplashes:
            base.cr.timeOfDayManager.rainSplashes.stopLoop()
            base.cr.timeOfDayManager.rainSplashes = None

        if base.cr.timeOfDayManager.rainSplashes2:
            base.cr.timeOfDayManager.rainSplashes2.stopLoop()
            base.cr.timeOfDayManager.rainSplashes2 = None

    else:
        from pirates.effects.RainDrops import RainDrops
        base.cr.timeOfDayManager.rainDrops = RainDrops(base.camera)
        base.cr.timeOfDayManager.rainDrops.reparentTo(render)
        base.cr.timeOfDayManager.rainDrops.startLoop()
        from pirates.effects.RainMist import RainMist
        base.cr.timeOfDayManager.rainMist = RainMist(base.camera)
        base.cr.timeOfDayManager.rainMist.reparentTo(render)
        base.cr.timeOfDayManager.rainMist.startLoop()
        from pirates.effects.RainSplashes import RainSplashes
        base.cr.timeOfDayManager.rainSplashes = RainSplashes(base.camera)
        base.cr.timeOfDayManager.rainSplashes.reparentTo(render)
        base.cr.timeOfDayManager.rainSplashes.startLoop()
        from pirates.effects.RainSplashes2 import RainSplashes2
        base.cr.timeOfDayManager.rainSplashes2 = RainSplashes2(base.camera)
        base.cr.timeOfDayManager.rainSplashes2.reparentTo(render)
        base.cr.timeOfDayManager.rainSplashes2.startLoop()