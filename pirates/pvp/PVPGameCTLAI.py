from direct.directnotify import DirectNotifyGlobal

from pirates.pvp import PVPGlobals
from pirates.pvp.PVPGameBaseAI import PVPGameBaseAI


class PVPGameCTLAI(PVPGameBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameCTLAI')

    TimeLimit = config.GetInt('pvp-ctl-time-limit', 900)
    MaxCarry = config.GetInt('pvp-ctl-max-carry', 20)
    MaxTeamScore = config.GetInt('pvp-ctl-max-team-score', 200)

    def __init__(self, air):
        PVPGameBaseAI.__init__(self, air)

        self.maxCarry = self.MaxCarry
        self.maxTeamScore = self.MaxTeamScore
        self.banks = {}
        self.lootCarried = {}
        self.shipLoot = {}
        self.shipsNearBase = {}

    def delete(self):
        self.banks = {}
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

    def d_shipDeposited(self, avatarId, shipId):
        self.sendUpdateToAvatarId(avatarId, 'shipDeposited', [shipId])

    def addBank(self, bank):
        self.banks[bank.doId] = bank
        bank.setGameRules(self)

    def removeBank(self, bank):
        self.banks.pop(bank.doId, None)

    def getTeamBank(self, team):
        for bank in list(self.banks.values()):
            if bank.getBelongsToTeam() == team:
                return bank

        return None

    def getLootCarried(self, avatarId):
        return self.lootCarried.get(avatarId, 0)

    def setLootCarried(self, avatarId, amount):
        self.lootCarried[avatarId] = amount
        avatar = self.air.doId2do.get(avatarId)
        if avatar:
            avatar.b_setLootCarried(amount, self.maxCarry)

    def addLoot(self, avatarId, amount):
        # returns the amount of loot the avatar was actually able to carry
        if self.state != 'Game' or avatarId not in self.players:
            return 0

        carried = self.getLootCarried(avatarId)
        amount = max(0, min(amount, self.maxCarry - carried))
        if amount:
            self.setLootCarried(avatarId, carried + amount)

        return amount

    def removePlayer(self, avatarId):
        self.dropTreasure(avatarId)
        PVPGameBaseAI.removePlayer(self, avatarId)

    def dropTreasure(self, avatarId):
        # dropped treasure is returned to the bank it was taken from,
        # we don't track the origin so it is returned to the enemy...
        amount = self.getLootCarried(avatarId)
        if not amount:
            return

        self.setLootCarried(avatarId, 0)
        team = self.getTeam(avatarId)
        for bank in list(self.banks.values()):
            if bank.getBelongsToTeam() != team:
                bank.addValue(amount)
                break

    def depositLoot(self, avatarId, team, amount):
        bank = self.getTeamBank(team)
        if not bank or not amount:
            return False

        bank.addValue(amount)
        self.addPlayerStat(avatarId, PVPGlobals.SCORE, amount)
        self.checkWinCondition()
        return True

    def treasureDeposited(self, bankId):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.players or self.state != 'Game':
            return

        bank = self.banks.get(bankId)
        if not bank:
            self.notify.warning('Avatar %d deposited into unknown bank %d' % (avatarId, bankId))
            return

        team = self.getTeam(avatarId)
        if bank.getBelongsToTeam() != team:
            self.air.logPotentialHacker(
                message='Avatar deposited treasure into an enemy bank',
                targetAvId=avatarId,
                bankId=bankId)

            return

        amount = self.getLootCarried(avatarId)
        if not amount:
            return

        self.setLootCarried(avatarId, 0)
        self.depositLoot(avatarId, team, amount)

    def requestDropTreasure(self):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.players:
            return

        self.dropTreasure(avatarId)

    def shipDeposit(self, shipId):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.players or self.state != 'Game':
            return

        ship = self.air.doId2do.get(shipId)
        if not ship or ship.getPVPTeam() != self.getTeam(avatarId):
            return

        amount = self.getLootCarried(avatarId)
        if not amount:
            return

        self.setLootCarried(avatarId, 0)
        self.shipLoot[shipId] = self.shipLoot.get(shipId, 0) + amount
        self.d_shipDeposited(avatarId, shipId)
        self.checkShipDeposit(shipId, avatarId)

    def checkShipDeposit(self, shipId, avatarId):
        ship = self.air.doId2do.get(shipId)
        if not ship:
            return

        if self.shipsNearBase.get(shipId) != self.getTeamName(ship.getPVPTeam()):
            return

        amount = self.shipLoot.pop(shipId, 0)
        self.depositLoot(avatarId, ship.getPVPTeam(), amount)

    def portEntered(self, baseTeam, shipId):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.players:
            return

        ship = self.air.doId2do.get(shipId)
        if not ship:
            return

        self.shipsNearBase[shipId] = baseTeam
        self.d_setShipsNearBase()
        self.checkShipDeposit(shipId, avatarId)

    def portExited(self, baseTeam, shipId):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.players:
            return

        if self.shipsNearBase.pop(shipId, None) is not None:
            self.d_setShipsNearBase()

    def getTeamScores(self):
        teamScores = {}
        for bank in list(self.banks.values()):
            team = bank.getBelongsToTeam()
            teamScores[team] = teamScores.get(team, 0) + bank.getValue()

        return teamScores

    def getRank(self, avatarId):
        teamScores = self.getTeamScores()
        score = teamScores.get(self.getTeam(avatarId), 0)
        return 1 + len([otherScore for otherScore in list(teamScores.values())
                        if otherScore > score])

    def checkWinCondition(self):
        if self.state != 'Game':
            return False

        for team, score in list(self.getTeamScores().items()):
            if score >= self.maxTeamScore:
                self.request('ScoreScreen')
                return True

        return False

    def enterScoreScreen(self):
        for avatarId in list(self.lootCarried.keys()):
            if self.lootCarried[avatarId]:
                self.setLootCarried(avatarId, 0)

        PVPGameBaseAI.enterScoreScreen(self)
