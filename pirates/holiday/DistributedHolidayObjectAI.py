from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI


class DistributedHolidayObjectAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedInteractiveAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)

    def announceGenerate(self):
        DistributedInteractiveAI.announceGenerate(self)
