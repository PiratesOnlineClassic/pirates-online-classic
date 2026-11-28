from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class SiegeAnnouncerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('SiegeAnnouncerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def d_announceSink(self, team, shipName, sunkTeam, sunkShipName):
        self.sendUpdate('announceSink', [team, shipName, sunkTeam, sunkShipName])

    def d_announceSinkWithAssist(self, team, shipName, assistTeam, assistShipName, sunkTeam, sunkShipName):
        self.sendUpdate('announceSinkWithAssist', [team, shipName, assistTeam,
            assistShipName, sunkTeam, sunkShipName])

    def d_announceSinkStreak(self, team, shipName, amount):
        self.sendUpdate('announceSinkStreak', [team, shipName, amount])
