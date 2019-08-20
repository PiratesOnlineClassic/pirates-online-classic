from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from pirates.holiday.DistributedHolidayObjectAI import DistributedHolidayObjectAI

class DistributedHolidayBonfireAI(DistributedHolidayObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHolidayBonfireAI')

    def __init__(self, air):
        DistributedHolidayObjectAI.__init__(self, air)
        self.fireStarted = False
    
    def setFireStarted(self, value):
        if value and not self.fireStarted:
            messenger.send('BonfireStarted', [])

        self.fireStarted = value
        
        island = self.getParentObj()
        island.b_setFeastFireEnabled(value)

    def d_setFireStarted(self, value):
        self.sendUpdate('setFireStarted', [value])

    def b_setFireStarted(self, value):
        self.setFireStarted(value)
        self.d_setFireStarted(value)

    def getFireStarted(self):
        return self.fireStarted

    def holidayEnd(self):
        # Stop the fire on holiday end
        self.b_setFireStarted(False)

    def d_finishInteraction(self, avatarId):
        self.sendUpdateToAvatarId(avatarId, 'finishInteraction', [])

    def handleHolidayInteract(self, avatar, interactType, instant):
        if self.fireStarted:
            return self.DENY

        lightTrack = Sequence(
            Wait(5.0),
            Func(self.b_setFireStarted, value=True),
            Wait(1.5),
            Func(self.d_finishInteraction, avatarId=avatar.doId))
        lightTrack.start()

        return self.ACCEPT