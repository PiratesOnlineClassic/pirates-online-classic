from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.ClockDelta import globalClockDelta
from otp.ai.MagicWordGlobal import *
from .TimeOfDayManager import TimeOfDayManager
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
        self.stormEye = None
        self.stormRing = None

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

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def storm(grid,):
    """
    Toggles the local storm state
    """

    if base.cr.timeOfDayManager.stormEye:
        base.cr.timeOfDayManager.stormEye.stopLoop()
        base.cr.timeOfDayManager.stormEye = None
        if base.cr.timeOfDayManager.stormRing:
            base.cr.timeOfDayManager.stormRing.stopLoop()
            base.cr.timeOfDayManager.stormRing = None

    else:
        pos = Vec3(base.cr.doId2do[201100017].getZoneCellOrigin(grid)[0], base.cr.doId2do[201100017].getZoneCellOrigin(grid)[1], base.cr.doId2do[201100017].getZoneCellOrigin(grid)[2])
        from pirates.effects.StormEye import StormEye
        base.cr.timeOfDayManager.stormEye = StormEye()
        base.cr.timeOfDayManager.stormEye.reparentTo(render)
        base.cr.timeOfDayManager.stormEye.startLoop()
        from pirates.effects.StormRing import StormRing
        base.cr.timeOfDayManager.stormRing = StormRing()
        base.cr.timeOfDayManager.stormRing.reparentTo(render)
        base.cr.timeOfDayManager.stormRing.setZ(100)
        base.cr.timeOfDayManager.stormRing.startLoop()

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[float, float, float])
def alight(red, green, blue):
    """
    Sets the alight value of the scene
    """

    color = Vec4(red, green, blue, 1)
    base.cr.timeOfDayManager.alight.node().setColor(color)

    return 'Alight set to (%s, %s, %s, 1)' % (red, green, blue)

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[float, float, float])
def dlight(red, green, blue):
    """
    Sets the dlight value of the scene
    """

    color = Vec4(red, green, blue, 1)
    base.cr.timeOfDayManager.dlight.node().setColor(color)

    return 'Dlight set to (%s, %s, %s, 1)' % (red, green, blue)

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def todpanel():
    """
    Loads the client Time of Day editor panel
    """

    tod = base.cr.timeOfDayManager
    from pirates.leveleditor import TimeOfDayPanel
    p = TimeOfDayPanel.TimeOfDayPanel(tod)

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def fogColor(red, green, blue):
    """
    Sets the local fog's color
    """

    color = Vec4(red, green, blue, 1)
    base.cr.timeOfDayManager.fog.setColor(color)

    return 'Local fog color set to (%s, %s, %s, 1)' % (red, green, blue)

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def fogDensity(density):
    """
    Sets the local fog's density
    """

    base.cr.timeOfDayManager.fog.setExpDensity(density)

    return 'Local fog density set to %s' % density