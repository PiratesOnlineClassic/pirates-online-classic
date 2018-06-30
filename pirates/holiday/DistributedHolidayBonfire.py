from pirates.holiday.DistributedHolidayObject import DistributedHolidayObject
from pirates.piratesbase import PLocalizer
from pirates.effects.FeastFire import FeastFire


class DistributedHolidayBonfire(DistributedHolidayObject):

    def __init__(self, cr):
        DistributedHolidayObject.__init__(
            self, cr, proximityText=PLocalizer.InteractHolidayBonfire)
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
