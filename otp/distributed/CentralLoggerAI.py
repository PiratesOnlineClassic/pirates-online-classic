from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal


class CentralLoggerAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('CentralLoggerAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

    def sendMessage(self, category, message, targetDISLid, targetAvId):
        self.notify.debug('Received message from client')

    def reportException(self, sender, exception, isClient=False):
        self.sendUpdate('reportException', [sender, exception, isClient])