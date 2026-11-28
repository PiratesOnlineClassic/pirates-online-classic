from direct.directnotify import DirectNotifyGlobal
from direct.task import Task

from pirates.pvp import PVPGlobals
from pirates.pvp.PVPGameBaseAI import PVPGameBaseAI


class PVPGamePirateerAI(PVPGameBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGamePirateerAI')

    TimeLimit = config.GetInt('pvp-pirateer-time-limit', 900)
    MaxCarry = config.GetInt('pvp-pirateer-max-carry', 1)
    MaxTeamScore = config.GetInt('pvp-pirateer-max-team-score', 5)
    LoadTime = config.GetFloat('pvp-pirateer-load-time', 1.0)
    LoadSteps = 5

    def __init__(self, air):
        PVPGameBaseAI.__init__(self, air)

        self.maxCarry = self.MaxCarry
        self.maxTeamScore = self.MaxTeamScore
        self.wrecks = {}
        self.coinCarriers = []
        self.shipLoot = {}
        self.loading = {}
        self.teamScores = {}
        self.shipsNearBase = {}

    def delete(self):
        for shipId in list(self.loading.keys()):
            self.stopLoading(shipId)

        for shipId in list(self.coinCarriers):
            self.ignore('distObjDelete-%d' % shipId)

        self.wrecks = {}
        PVPGameBaseAI.delete(self)

    def getTeamName(self, team):
        return 'Team %s' % team

    def setMaxCarry(self, maxCarry):
        self.maxCarry = maxCarry

    def d_setMaxCarry(self, maxCarry):
        self.sendUpdate('setMaxCarry', [maxCarry])

    def b_setMaxCarry(self, maxCarry):
        self.setMaxCarry(maxCarry)
        self.d_setMaxCarry(maxCarry)

    def getMaxCarry(self):
        return self.maxCarry

    def setMaxTeamScore(self, maxTeamScore):
        self.maxTeamScore = maxTeamScore

    def d_setMaxTeamScore(self, maxTeamScore):
        self.sendUpdate('setMaxTeamScore', [maxTeamScore])

    def b_setMaxTeamScore(self, maxTeamScore):
        self.setMaxTeamScore(maxTeamScore)
        self.d_setMaxTeamScore(maxTeamScore)

    def getMaxTeamScore(self):
        return self.maxTeamScore

    def getShipsNearBase(self):
        shipIds = list(self.shipsNearBase.keys())
        return [shipIds, [self.shipsNearBase[shipId] for shipId in shipIds]]

    def d_setShipsNearBase(self):
        self.sendUpdate('setShipsNearBase', self.getShipsNearBase())

    def getDisplayCoins(self):
        return self.coinCarriers

    def d_displayCoins(self, shipIds):
        self.sendUpdate('displayCoins', [shipIds])

    def d_unDisplayCoin(self, shipId):
        self.sendUpdate('unDisplayCoin', [shipId])

    def d_coinCaptured(self, shipId):
        self.sendUpdate('coinCaptured', [shipId])

    def addWreck(self, wreck):
        self.wrecks[wreck.doId] = wreck

    def removeWreck(self, wreck):
        self.wrecks.pop(wreck.doId, None)

    def getShip(self, shipId):
        ship = self.air.doId2do.get(shipId)
        if not ship or not hasattr(ship, 'getPVPTeam'):
            return None

        return ship

    def lootWreck(self, wreckId, shipId):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.players or self.state != 'Game':
            return

        wreck = self.wrecks.get(wreckId)
        ship = self.getShip(shipId)
        if not wreck or not ship:
            return

        if shipId in self.loading or self.shipLoot.get(shipId, 0) >= self.maxCarry:
            return

        self.loading[shipId] = [wreckId, 0]
        taskMgr.doMethodLater(self.LoadTime, self.__loadTask,
            self.uniqueName('load-%d' % shipId), extraArgs=[shipId], appendTask=True)

    def unLootWreck(self, wreckId, shipId):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.players:
            return

        loading = self.loading.get(shipId)
        if loading and loading[0] == wreckId:
            self.stopLoading(shipId)

    def stopLoading(self, shipId):
        taskMgr.remove(self.uniqueName('load-%d' % shipId))
        self.loading.pop(shipId, None)

    def __loadTask(self, shipId, task):
        loading = self.loading.get(shipId)
        wreck = loading and self.wrecks.get(loading[0])
        ship = self.getShip(shipId)
        if not loading or not wreck or not ship or self.state != 'Game':
            self.stopLoading(shipId)
            return Task.done

        loading[1] += 1
        if loading[1] < self.LoadSteps:
            return Task.again

        self.stopLoading(shipId)
        if wreck.takeValue(1):
            self.shipLoot[shipId] = self.shipLoot.get(shipId, 0) + 1
            self.addCoinCarrier(shipId)

        return Task.done

    def addCoinCarrier(self, shipId):
        if shipId in self.coinCarriers:
            return

        self.coinCarriers.append(shipId)
        self.acceptOnce('distObjDelete-%d' % shipId, self.removeCoinCarrier, extraArgs=[shipId])
        self.d_displayCoins(self.coinCarriers)

    def removeCoinCarrier(self, shipId):
        if shipId not in self.coinCarriers:
            return

        self.coinCarriers.remove(shipId)
        self.shipLoot.pop(shipId, None)
        self.ignore('distObjDelete-%d' % shipId)
        self.d_unDisplayCoin(shipId)

    def portEntered(self, baseTeam, shipId):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.players:
            return

        ship = self.getShip(shipId)
        if not ship:
            return

        self.shipsNearBase[shipId] = baseTeam
        self.d_setShipsNearBase()

        team = ship.getPVPTeam()
        if baseTeam != self.getTeamName(team) or self.state != 'Game':
            return

        amount = self.shipLoot.get(shipId, 0)
        if not amount:
            return

        self.removeCoinCarrier(shipId)
        self.teamScores[team] = self.teamScores.get(team, 0) + amount
        self.addPlayerStat(avatarId, PVPGlobals.SCORE, amount)
        self.d_coinCaptured(shipId)
        self.checkWinCondition()

    def portExited(self, baseTeam, shipId):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.players:
            return

        if self.shipsNearBase.pop(shipId, None) is not None:
            self.d_setShipsNearBase()

    def getTeamScores(self):
        return dict(self.teamScores)

    def getRank(self, avatarId):
        score = self.teamScores.get(self.getTeam(avatarId), 0)
        return 1 + len([otherScore for otherScore in list(self.teamScores.values())
                        if otherScore > score])

    def checkWinCondition(self):
        if self.state != 'Game':
            return False

        for team, score in list(self.teamScores.items()):
            if score >= self.maxTeamScore:
                self.request('ScoreScreen')
                return True

        return False
