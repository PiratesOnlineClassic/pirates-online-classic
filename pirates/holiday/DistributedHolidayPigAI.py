from direct.directnotify import DirectNotifyGlobal
from pirates.holiday.DistributedHolidayObjectAI import DistributedHolidayObjectAI


class DistributedHolidayPigAI(DistributedHolidayObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedHolidayPigAI')

    def __init__(self, air):
        DistributedHolidayObjectAI.__init__(self, air)
