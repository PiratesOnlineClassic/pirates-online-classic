# uncompyle6 version 3.1.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (default, Mar  9 2018, 23:57:12)
# [GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.39.2)]
# Embedded file name: pirates.holiday.DistributedHolidayBonfire
from pirates.holiday.DistributedHolidayObject import DistributedHolidayObject
from pirates.piratesbase import PLocalizer
from pirates.effects.FeastFire import FeastFire

class DistributedHolidayBonfire(DistributedHolidayObject):
    

    def __init__(self, cr):
        DistributedHolidayObject.__init__(self, cr, proximityText=PLocalizer.InteractHolidayBonfire)
        self.fireStarted = False

    def setFireStarted(self, value=False):
        self.fireStarted = value

    def getFireStarted(self):
        return self.fireStarted

    def acceptInteraction(self):
        DistributedHolidayObject.acceptInteraction(self)
        localAvatar.b_setGameState('BeginFeast')

    def rejectInteraction(self):
        DistributedHolidayObject.rejectInteraction(self)
        localAvatar.guiMgr.createWarning(PLocalizer.BonfireAlreadyStarted)

    def finishInteraction(self):
        localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)
# okay decompiling DistributedHolidayBonfire.pyc
