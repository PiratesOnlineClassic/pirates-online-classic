
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class NewsManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('NewsManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # holidayNotify() broadcast

    def holidayNotify(self, holidayNotify):
        self.sendUpdate('holidayNotify', [holidayNotify])

    # setHolidayIdList(NewsItem []) broadcast ram

    def setHolidayIdList(self, holidayIdList):
        self.sendUpdate('setHolidayIdList', [holidayIdList])

    # displayMessage(uint16) broadcast

    def displayMessage(self, displayMessage):
        self.sendUpdate('displayMessage', [displayMessage])


