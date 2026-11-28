from direct.directnotify import DirectNotifyGlobal

from pirates.pvp import PVPGlobals
from pirates.pvp.PVPGameTeamBattleAI import PVPGameTeamBattleAI


class PVPGameShipBattleAI(PVPGameTeamBattleAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameShipBattleAI')

    TimeLimit = config.GetInt('pvp-ship-battle-time-limit', 900)
    ScoreLimit = config.GetInt('pvp-ship-battle-score-limit', 5)

    def __init__(self, air):
        PVPGameTeamBattleAI.__init__(self, air)

        self.teamShips = {}
        self.boardedPlayers = []

    def delete(self):
        for ship in list(self.teamShips.values()):
            self.ignore(ship.getDeleteEvent())

        self.teamShips = {}
        PVPGameTeamBattleAI.delete(self)

    def removePlayer(self, avatarId):
        if avatarId in self.boardedPlayers:
            self.boardedPlayers.remove(avatarId)

        PVPGameTeamBattleAI.removePlayer(self, avatarId)

    def setTeamShip(self, team, ship):
        self.teamShips[team] = ship
        self.acceptOnce(ship.getDeleteEvent(), self.shipSunk, extraArgs=[team, ship])
        for avatarId in self.players:
            if self.getTeam(avatarId) == team:
                self.d_setShipDoId(avatarId, ship.doId)

    def getTeamShip(self, team):
        return self.teamShips.get(team)

    def shipSunk(self, team, ship):
        if self.teamShips.get(team) is not ship:
            return

        del self.teamShips[team]
        if self.state != 'Game':
            return

        for avatarId in self.players:
            if self.getTeam(avatarId) == team:
                if avatarId in self.boardedPlayers:
                    self.boardedPlayers.remove(avatarId)

                self.addPlayerStat(avatarId, PVPGlobals.DEATHS, 1)
            else:
                self.addPlayerStat(avatarId, PVPGlobals.SCORE, 1)

        self.checkWinCondition()

    def d_setShipDoId(self, avatarId, shipId):
        self.sendUpdateToAvatarId(avatarId, 'setShipDoId', [shipId])

    def setBoarded(self):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.players:
            return

        if avatarId not in self.boardedPlayers:
            self.boardedPlayers.append(avatarId)
