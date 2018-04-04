
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class ScoreboardAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('ScoreboardAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.stats = 0
        self.scores = []


    # setStats(uint8 []) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setStats(self, stats):
        self.stats = stats

    def d_setStats(self, stats):
        self.sendUpdate('setStats', [stats])

    def b_setStats(self, stats):
        self.setStats(stats)
        self.d_setStats(stats)

    def getStats(self):
        return self.stats

    # setScores(pvpScoreItem []) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setScores(self, scores):
        self.scores = scores

    def d_setScores(self, scores):
        self.sendUpdate('setScores', [scores])

    def b_setScores(self, scores):
        self.setScores(scores)
        self.d_setScores(scores)

    def getScores(self):
        return self.scores

    # setScore(uint32, int32) broadcast

    def setScore(self, score, todo_int32_1):
        self.sendUpdate('setScore', [score, todo_int32_1])

    # setStat(uint32, uint8, int32) broadcast

    def setStat(self, stat, todo_uint8_1, todo_int32_2):
        self.sendUpdate('setStat', [stat, todo_uint8_1, todo_int32_2])


