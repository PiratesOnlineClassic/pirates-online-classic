# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.world.DistributedLocatableObject
from direct.distributed.DistributedObject import DistributedObject
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals

class DistributedLocatableObject(DistributedObject):
    __module__ = __name__

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

    def locationChange(self, locationName):
        displayName = PLocalizer.LocationNames.get(locationName)
        if displayName:
            self.guiMgr.createTitle(displayName, PiratesGuiGlobals.TextFG2)
            localAvatar.guiMgr.radarGui.showLocation(locationName)
# okay decompiling .\pirates\world\DistributedLocatableObject.pyc
