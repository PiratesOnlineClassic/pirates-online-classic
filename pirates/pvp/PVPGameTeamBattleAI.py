from direct.directnotify import DirectNotifyGlobal

from pirates.pvp import PVPGlobals
from pirates.pvp.PVPGameBaseAI import PVPGameBaseAI


class PVPGameTeamBattleAI(PVPGameBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameTeamBattleAI')

    TimeLimit = config.GetInt('pvp-team-battle-time-limit', 600)
    ScoreLimit = config.GetInt('pvp-team-battle-score-limit', 25)

    def getInitialStats(self, avatarId):
        stats = PVPGameBaseAI.getInitialStats(self, avatarId)
        stats[PVPGlobals.TEAM] = self.getTeam(avatarId)
        return stats

    def handleDefeat(self, defeaterId, defeatedId):
        if defeaterId == defeatedId:
            return

        if self.getTeam(defeaterId) == self.getTeam(defeatedId):
            return

        self.addPlayerStat(defeaterId, PVPGlobals.SCORE, 1)

    def getRank(self, avatarId):
        teamScores = self.getTeamScores()
        score = teamScores.get(self.getTeam(avatarId), 0)
        return 1 + len([otherScore for otherScore in list(teamScores.values())
                        if otherScore > score])

    def checkWinCondition(self):
        if self.state != 'Game' or not self.ScoreLimit:
            return False

        for team, score in list(self.getTeamScores().items()):
            if score >= self.ScoreLimit:
                self.request('ScoreScreen')
                return True

        return False
