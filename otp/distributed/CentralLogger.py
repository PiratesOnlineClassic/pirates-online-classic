from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal

REPORT_PLAYER = 'REPORT_PLAYER'
ReportFoulLanguage = 'MODERATION_FOUL_LANGUAGE'
ReportPersonalInfo = 'MODERATION_PERSONAL_INFO'
ReportRudeBehavior = 'MODERATION_RUDE_BEHAVIOR'
ReportBadName = 'MODERATION_BAD_NAME'


class CentralLogger(DistributedObjectGlobal):
    PlayersReportedThisSession = {}

    def hasReportedPlayer(self, targetDISLId, targetAvId):
        return (targetDISLId, targetAvId) in self.PlayersReportedThisSession

    def reportPlayer(self, category, targetDISLId, targetAvId):
        if self.hasReportedPlayer(targetDISLId, targetAvId):
            return False

        self.PlayersReportedThisSession[(targetDISLId, targetAvId)] = 1
        self.sendUpdate('sendMessage', [category, REPORT_PLAYER, targetDISLId, targetAvId])
        return True

    def writeClientEvent(self, eventString, targetDISLId = 0, targetAvId = 0):
        self.sendUpdate('sendMessage', ['ClientEvent', eventString, targetDISLId, targetAvId])
