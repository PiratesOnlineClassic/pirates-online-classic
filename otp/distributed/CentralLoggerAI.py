from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal


class CentralLoggerAI(DistributedObjectGlobalAI):
    """
    AI side of the central logger. Client events (sendMessage) go straight to
    the UberDOG; the AI only forwards exceptions so they end up in the same
    event log as everything else.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('CentralLoggerAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

    def d_reportException(self, sender, exception, isClient=False):
        self.sendUpdate('reportException', [sender, exception, isClient])

    # reportException is deliberately not defined here: every AI listens on
    # the logger's channel, and relaying a received report would bounce it
    # between districts forever.

    def reportServerException(self, exception):
        self.d_reportException('AI-%d' % self.air.ourChannel, exception, False)
