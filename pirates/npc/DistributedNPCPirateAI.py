
from pirates.battle.DistributedBattleNPCAI import DistributedBattleNPCAI
from direct.directnotify import DirectNotifyGlobal

class DistributedNPCPirateAI(DistributedBattleNPCAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCPirateAI')

    def __init__(self, air):
        DistributedBattleNPCAI.__init__(self, air)
        self.dNAString = ''


    # setDNAString(blob) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setDNAString(self, dNAString):
        self.dNAString = dNAString

    def d_setDNAString(self, dNAString):
        self.sendUpdate('setDNAString', [dNAString])

    def b_setDNAString(self, dNAString):
        self.setDNAString(dNAString)
        self.d_setDNAString(dNAString)

    def getDNAString(self):
        return self.dNAString


