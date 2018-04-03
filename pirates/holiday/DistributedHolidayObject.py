# uncompyle6 version 3.1.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (default, Mar  9 2018, 23:57:12) 
# [GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.39.2)]
# Embedded file name: pirates.holiday.DistributedHolidayObject
from pandac.PandaModules import NodePath
from pirates.distributed.DistributedInteractive import DistributedInteractive

class DistributedHolidayObject(DistributedInteractive):
    __module__ = __name__

    def __init__(self, cr, proximityText):
        NodePath.__init__(self, self.__class__.__name__)
        DistributedInteractive.__init__(self, cr)
        self.holiday = ''
        self.interactRadius = 10
        self.interactMode = 0
        self.proximityText = proximityText

    def announceGenerate(self):
        DistributedInteractive.announceGenerate(self)

    def setHoliday(self, holiday):
        self.holiday = holiday

    def setInteractRadius(self, radius):
        self.interactRadius = radius
        self.diskRadius = radius * 2.0

    def setInteractMode(self, mode):
        if mode == 1 or mode == 2 and localAvatar.gmNameTagAllowed:
            self.setInteractOptions(proximityText=self.proximityText, sphereScale=self.interactRadius, diskRadius=self.diskRadius)
        else:
            self.setInteractOptions(allowInteract=False)
# okay decompiling DistributedHolidayObject.pyc
