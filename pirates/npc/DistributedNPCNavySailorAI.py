
from pirates.battle.DistributedBattleNPCAI import DistributedBattleNPCAI
from direct.directnotify import DirectNotifyGlobal

class DistributedNPCNavySailorAI(DistributedBattleNPCAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCNavySailorAI')

    def __init__(self, air):
        DistributedBattleNPCAI.__init__(self, air)
        self.dNAId = ''


    # setDNAId(string) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setDNAId(self, dNAId):
        self.dNAId = dNAId

    def d_setDNAId(self, dNAId):
        self.sendUpdate('setDNAId', [dNAId])

    def b_setDNAId(self, dNAId):
        self.setDNAId(dNAId)
        self.d_setDNAId(dNAId)

    def getDNAId(self):
        return self.dNAId


