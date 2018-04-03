# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.distributed.CentralLogger
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal

REPORT_PLAYER = 'REPORT_PLAYER'
ReportFoulLanguage = 'MODERATION_FOUL_LANGUAGE'
ReportPersonalInfo = 'MODERATION_PERSONAL_INFO'
ReportRudeBehavior = 'MODERATION_RUDE_BEHAVIOR'
ReportBadName = 'MODERATION_BAD_NAME'

class CentralLogger(DistributedObjectGlobal):
    __module__ = __name__
    PlayersReportedThisSession = {}

    def hasReportedPlayer(self, targetDISLId, targetAvId):
        return self.PlayersReportedThisSession.has_key((targetDISLId, targetAvId))

    def reportPlayer(self, category, targetDISLId, targetAvId):
        if self.hasReportedPlayer(targetDISLId, targetAvId):
            return False
        self.PlayersReportedThisSession[(targetDISLId, targetAvId)] = 1
        self.sendUpdate('sendMessage', [category, REPORT_PLAYER, targetDISLId, targetAvId])
        return True

    def writeClientEvent(self, eventString):
        self.sendUpdate('sendMessage', ['ClientEvent', eventString, 0, 0])
# okay decompiling .\otp\distributed\CentralLogger.pyc
