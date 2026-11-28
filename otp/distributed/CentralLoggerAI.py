from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal


class CentralLoggerAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('CentralLoggerAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

    def d_reportException(self, sender, exception, isClient=False):
        self.sendUpdate('reportException', [sender, exception, isClient])

    # reportException is not handled here, every AI listens on the logger's
    # channel and relaying a received report would bounce it between districts...
