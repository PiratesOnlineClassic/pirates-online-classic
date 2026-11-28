from direct.directnotify import DirectNotifyGlobal

from pirates.piratesbase import PiratesGlobals
from pirates.pvp import PVPGlobals
from pirates.pvp.DistributedPVPInstanceAI import DistributedPVPInstanceAI
from pirates.uberdog.UberDogGlobals import InventoryType


class DistributedPVPTeamBattleAI(DistributedPVPInstanceAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPVPTeamBattleAI')

    GameStyle = PiratesGlobals.GAME_STYLE_TEAM_BATTLE
    RankingType = InventoryType.TBTGame
    TimeLimit = config.GetInt('pvp-team-battle-time-limit', 600)
    ScoreLimit = config.GetInt('pvp-team-battle-score-limit', 25)
    NumTeams = 2

    def getPlayerTeam(self, avatar, team):
        # keep the teams within the number of teams this map supports,
        # any extra parties are placed on the smallest team...
        if team <= self.NumTeams:
            return team

        teamSizes = dict([(currTeam, 0) for currTeam in range(1, self.NumTeams + 1)])
        for name, playerTeam in list(self.players.values()):
            teamSizes[playerTeam] = teamSizes.get(playerTeam, 0) + 1

        return min(teamSizes, key=teamSizes.get)

    def getInitialStats(self, avatarId):
        stats = DistributedPVPInstanceAI.getInitialStats(self, avatarId)
        stats[PVPGlobals.TEAM] = 0
        return stats

    def addPlayer(self, avatar, team):
        DistributedPVPInstanceAI.addPlayer(self, avatar, team)
        if avatar.doId in self.stats:
            self.stats[avatar.doId][PVPGlobals.TEAM] = team
