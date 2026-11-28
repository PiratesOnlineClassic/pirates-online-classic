from direct.directnotify import DirectNotifyGlobal

from pirates.battle.DistributedBattleNPCAI import DistributedBattleNPCAI


class DistributedNPCPirateAI(DistributedBattleNPCAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCPirateAI')

    def __init__(self, air):
        DistributedBattleNPCAI.__init__(self, air)
        self.dnaString = b''

    def setDNAString(self, dnaString):
        self.dnaString = dnaString

    def d_setDNAString(self, dnaString):
        self.sendUpdate('setDNAString', [dnaString])

    def b_setDNAString(self, dnaString):
        self.setDNAString(dnaString)
        self.d_setDNAString(dnaString)

    def getDNAString(self):
        return self.dnaString
