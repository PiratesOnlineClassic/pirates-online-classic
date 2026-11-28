from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from pirates.pvp import PVPGlobals


class ScoreboardAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('ScoreboardAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.statTypes = []
        # id -> [name, score, team, type, {stat: value}]
        self.scores = {}

    def setStats(self, statTypes):
        self.statTypes = list(statTypes)

    def getStats(self):
        return self.statTypes

    def setScores(self, scores):
        self.scores = {}
        for id, name, score, team, type, stats in scores:
            self.scores[id] = [name, score, team, type, dict(stats)]

    def d_setScores(self, scores):
        self.sendUpdate('setScores', [scores])

    def getScores(self):
        scores = []
        for id, (name, score, team, type, stats) in list(self.scores.items()):
            scores.append([id, name, score, team, type,
                [[stat, stats.get(stat, 0)] for stat in self.statTypes]])

        return scores

    def d_setScore(self, id, score):
        self.sendUpdate('setScore', [id, score])

    def d_setStat(self, id, stat, value):
        self.sendUpdate('setStat', [id, stat, value])

    def hasScore(self, id):
        return id in self.scores

    def addScore(self, id, name, team, type=PVPGlobals.SHIP_SCORE, score=0):
        self.scores[id] = [name, score, team, type, dict([(stat, 0) for stat in self.statTypes])]
        self.d_setScores(self.getScores())

    def removeScore(self, id):
        if id not in self.scores:
            return

        del self.scores[id]
        self.d_setScores(self.getScores())

    def getScore(self, id):
        if id not in self.scores:
            return 0

        return self.scores[id][1]

    def setScore(self, id, score):
        if id not in self.scores:
            return

        self.scores[id][1] = score
        self.d_setScore(id, score)

    def addToScore(self, id, amount):
        self.setScore(id, self.getScore(id) + amount)

    def getStat(self, id, stat):
        if id not in self.scores:
            return 0

        return self.scores[id][4].get(stat, 0)

    def setStat(self, id, stat, value):
        if id not in self.scores or stat not in self.statTypes:
            return

        self.scores[id][4][stat] = value
        self.d_setStat(id, stat, value)

    def addToStat(self, id, stat, amount):
        self.setStat(id, stat, self.getStat(id, stat) + amount)

    def getTeamScore(self, team):
        return sum([score for name, score, scoreTeam, type, stats in list(self.scores.values())
                    if scoreTeam == team])
