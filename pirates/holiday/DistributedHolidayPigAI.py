from direct.directnotify import DirectNotifyGlobal
from pirates.holiday.DistributedHolidayObjectAI import DistributedHolidayObjectAI

class DistributedHolidayPigAI(DistributedHolidayObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHolidayPigAI')

    ROAST_FULL = 0
    ROAST_GIVEN = 1
    ROAST_ERROR = 2

    def __init__(self, air):
        DistributedHolidayObjectAI.__init__(self, air)
        self.pigRoasting = False

    def announceGenerate(self):
        DistributedHolidayObjectAI.announceGenerate(self)

        self.accept('BonfireStarted', self.bonfireStarted)

    def delete(self):
        DistributedHolidayObjectAI.delete(self)
        self.ignore('BonfireStarted')

    def setPigRoasting(self, value):
        self.pigRoasting = value

    def d_setPigRoasting(self, value):
        self.sendUpdate('setPigRoasting', [value])

    def b_setPigRoasting(self, value):
        self.setPigRoasting(value)
        self.d_setPigRoasting(value)

    def getPigRoasting(self):
        return self.pigRoasting

    def d_makeTradeResponse(self, avatarId, value):
        self.sendUpdateToAvatarId(avatarId, 'makeTradeResponse', [value])

    def holidayEnd(self):
        # Reset pig roast on end
        self.b_setPigRoasting(False)

    def bonfireStarted(self):
        # Handle bonfire lighting
        if not self.getPigRoasting():
            self.b_setPigRoasting(True)

    def handleHolidayInteract(self, avatar, interactType, instant):
        # Verify the pig is currently roasting
        if not self.pigRoasting:
            self.notify.warning('Attempted to interact with an unroasted pig!')
            return self.DENY

        try:
            #TODO: write proper inventory code
            self.d_makeTradeResponse(avatar.doId, self.ROAST_GIVEN)
        except Exception as e:
            self.d_makeTradeResponse(avatar.doId, self.ROAST_ERROR)

        return self.ACCEPT
        