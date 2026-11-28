from direct.directnotify import DirectNotifyGlobal
from direct.task import Task

from otp.ai import AIInterestHandles

from pirates.piratesbase import PiratesGlobals
from pirates.pvp import PVPGlobals
from pirates.pvp.DistributedPVPInstanceAI import DistributedPVPInstanceAI, JOINED, READY
from pirates.ship import ShipGlobals
from pirates.uberdog.UberDogGlobals import InventoryType


class DistributedPVPShipBattleAI(DistributedPVPInstanceAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPVPShipBattleAI')

    GameStyle = PiratesGlobals.GAME_STYLE_SHIP_BATTLE
    RankingType = InventoryType.SBTGame
    InfamyType = InventoryType.PVPTotalInfamySea
    TimeLimit = config.GetInt('pvp-ship-battle-time-limit', 900)
    ScoreLimit = config.GetInt('pvp-ship-battle-score-limit', 5)
    ShipRespawnDelay = config.GetFloat('pvp-ship-battle-respawn-delay', 20.0)
    NumTeams = 2
    ShipClass = ShipGlobals.INTERCEPTORL1

    def __init__(self, air):
        DistributedPVPInstanceAI.__init__(self, air)

        self.teamShips = {}
        self.boardedPlayers = set()
        self.shipInterests = {}

    def delete(self):
        for team in list(self.teamShips.keys()):
            taskMgr.remove(self.uniqueName('respawnShip-%d' % team))

        for avatarId in list(self.shipInterests.keys()):
            self.removeShipInterest(avatarId)

        for ship in list(self.teamShips.values()):
            self.ignore(ship.getDeleteEvent())
            ship.requestDelete()

        self.teamShips = {}
        DistributedPVPInstanceAI.delete(self)

    def getPlayerTeam(self, avatar, team):
        return min(team, self.NumTeams)

    def getInitialStats(self, avatarId):
        stats = DistributedPVPInstanceAI.getInitialStats(self, avatarId)
        stats[PVPGlobals.TEAM] = 0
        return stats

    def addPlayer(self, avatar, team):
        DistributedPVPInstanceAI.addPlayer(self, avatar, team)
        if avatar.doId in self.stats:
            self.stats[avatar.doId][PVPGlobals.TEAM] = team

    def removePlayer(self, avatarId):
        DistributedPVPInstanceAI.removePlayer(self, avatarId)
        self.boardedPlayers.discard(avatarId)
        self.removeShipInterest(avatarId)

    def startMatch(self, teams):
        DistributedPVPInstanceAI.startMatch(self, teams)
        for team in self.getActiveTeams():
            if team not in self.teamShips:
                self.createTeamShip(team)

    def createTeamShip(self, team):
        from pirates.ship.DistributedShipAI import DistributedShipAI

        if not self.oceanGrid:
            self.notify.warning('Cannot create ship for team %d, no ocean grid!' % team)
            return None

        shipClass = self.ShipClass
        shipConfig = ShipGlobals.getShipConfig(shipClass)
        hullConfig = ShipGlobals.getHullConfig(shipClass)
        if shipConfig is None or hullConfig is None:
            self.notify.warning('Cannot create ship for team %d, invalid ship class %d!' % (
                team, shipClass))

            return None

        x, y, z, h = self.getPlayerSpawnPt(team)[1] or (0, 0, 0, 0)

        ship = DistributedShipAI(self.air)
        ship.setBaseTeam(ShipGlobals.PLAYER_TEAM)
        ship.setPVPTeam(team)
        ship.setLevel(1)
        ship.setShipClass(shipConfig['setShipClass'][0])
        ship.setName(PVPGlobals.siegeTeamNames.get(team, ''))
        ship.setIsBoardable(1)
        ship.setMaxHp(shipConfig['setMaxHp'][0])
        ship.setHp(shipConfig['setHp'][0])
        ship.setMaxSp(hullConfig['setMaxSp'][0])
        ship.setSp(hullConfig['setSp'][0])
        ship.setHullCondition(1 << 7)

        zoneId = self.oceanGrid.getZoneFromXYZ((x, y, 0))
        self.oceanGrid.generateChildWithRequired(ship, zoneId)
        ship.setPos(self.oceanGrid, x, y, 0)
        ship.setH(h)
        self.oceanGrid.addObjectToOceanGrid(ship)
        ship.sendCurrentPosition()
        ship.b_setGameState('Adrift', 0)

        self.teamShips[team] = ship
        self.acceptOnce(ship.getDeleteEvent(), self.handleShipSunk, extraArgs=[team, ship])

        for avatarId in self.getTeamPlayers(team):
            if self.playerStates.get(avatarId) in (JOINED, READY):
                self.sendPlayerToShip(avatarId)

        return ship

    def handleShipSunk(self, team, ship):
        if self.teamShips.get(team) is not ship:
            return

        del self.teamShips[team]
        for avatarId in self.getTeamPlayers(team):
            self.boardedPlayers.discard(avatarId)

        if self.state != 'Game':
            return

        # every pirate on the opposing teams is credited with the sinking,
        # the team score shown to the clients is the sum of their scores...
        for avatarId, (name, playerTeam) in list(self.players.items()):
            if playerTeam != team:
                self.addPlayerStat(avatarId, PVPGlobals.SCORE, 1)
            else:
                self.addPlayerStat(avatarId, PVPGlobals.DEATHS, 1)

        if self.checkWinCondition():
            return

        taskMgr.doMethodLater(self.ShipRespawnDelay, self.__respawnShip,
            self.uniqueName('respawnShip-%d' % team), extraArgs=[team])

    def __respawnShip(self, team):
        if self.state != 'Game' or team in self.teamShips:
            return Task.done

        if not self.getTeamPlayers(team):
            return Task.done

        self.createTeamShip(team)
        return Task.done

    def getTeamShip(self, team):
        return self.teamShips.get(team)

    def addShipInterest(self, avatarId, ship):
        clientChannel = self.GetPuppetConnectionChannel(avatarId)
        self.air.clientAddInterest(clientChannel, AIInterestHandles.PIRATES_SHIPPVP,
            ship.parentId, ship.zoneId, False)

        self.shipInterests[avatarId] = ship.doId

    def removeShipInterest(self, avatarId):
        if avatarId not in self.shipInterests:
            return

        del self.shipInterests[avatarId]
        clientChannel = self.GetPuppetConnectionChannel(avatarId)
        self.air.clientRemoveInterest(clientChannel, AIInterestHandles.PIRATES_SHIPPVP, False)

    def sendPlayerToShip(self, avatarId):
        ship = self.getTeamShip(self.getTeam(avatarId))
        if not ship:
            return

        self.addShipInterest(avatarId, ship)
        self.d_setShipDoId(avatarId, ship.doId)

    def d_setShipDoId(self, avatarId, shipId):
        self.sendUpdateToAvatarId(avatarId, 'setShipDoId', [shipId])

    def setBoarded(self):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.players:
            return

        self.boardedPlayers.add(avatarId)

    def sendPlayerToInstance(self, avatarId):
        from pirates.instance.DistributedTeleportMgrAI import TeleportFSM

        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return

        teleportMgr = self.air.teleportMgr
        if avatarId in teleportMgr.avatar2fsm:
            self.notify.warning('Cannot send avatar %d to ship battle %d, '
                'already teleporting!' % (avatarId, self.doId))

            return

        # the ship battle maps have no islands to teleport to, players arrive
        # in the ocean beside their team's ship and are placed on board it...
        area, spawnPt = self.getPlayerSpawnPt(self.getTeam(avatarId))
        if not area or not spawnPt:
            area, spawnPt = self.oceanGrid, (0, 0, 0, 0)

        self.acceptOnce('teleportDone-%d' % avatarId, self._playerArrived,
            extraArgs=[avatarId])

        teleportMgr.avatar2fsm[avatarId] = TeleportFSM(self.air, avatar, self, area, spawnPt)
        teleportMgr.avatar2fsm[avatarId].request('Teleporting')

    def handlePlayerArrived(self, avatarId):
        self.sendPlayerToShip(avatarId)

    def respawnPlayer(self, avatar):
        DistributedPVPInstanceAI.respawnPlayer(self, avatar)
        self.sendPlayerToShip(avatar.doId)
