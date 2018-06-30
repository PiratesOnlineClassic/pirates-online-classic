from direct.directnotify import DirectNotifyGlobal
from pirates.holiday.DistributedHolidayObjectAI import DistributedHolidayObjectAI


class DistributedHolidayBonfireAI(DistributedHolidayObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedHolidayBonfireAI')

    def __init__(self, air):
        DistributedHolidayObjectAI.__init__(self, air)
