
from pirates.pvp.PVPGameBaseAI import PVPGameBaseAI
from direct.directnotify import DirectNotifyGlobal

class PVPGameTeamBattleAI(PVPGameBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameTeamBattleAI')

    def __init__(self, air):
        PVPGameBaseAI.__init__(self, air)
        self.timeLimit = 0


    # setTimeLimit(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setTimeLimit(self, timeLimit):
        self.timeLimit = timeLimit

    def d_setTimeLimit(self, timeLimit):
        self.sendUpdate('setTimeLimit', [timeLimit])

    def b_setTimeLimit(self, timeLimit):
        self.setTimeLimit(timeLimit)
        self.d_setTimeLimit(timeLimit)

    def getTimeLimit(self):
        return self.timeLimit


