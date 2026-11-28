from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import globalClockDelta
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from direct.task import Task

from pirates.pvp import PVPGlobals


class PVPGameBaseAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameBaseAI')

    TimeLimit = 0
    ScoreLimit = 0

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, self.__class__.__name__)

        self.instanceId = 0
        self.players = []
        self.readyPlayers = []
        self.stats = {}
        self.gameStartTime = 0

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.request('WaitForServerStart')

    def delete(self):
        taskMgr.remove(self.uniqueName('readyTimeout'))
        taskMgr.remove(self.uniqueName('gameTimeLimit'))
        self.ignoreAll()
        self.demand('Off')
        DistributedObjectAI.delete(self)

    def getParentingRules(self):
        return ['', '']

    def setInstanceId(self, instanceId):
        self.instanceId = instanceId

    def getInstanceId(self):
        return self.instanceId

    def getInstance(self):
        return self.air.doId2do.get(self.instanceId)

    # -------------------------------------------------------------------
    # Players
    # -------------------------------------------------------------------

    def getInitialStats(self, avatarId):
        return {
            PVPGlobals.SCORE: 0,
            PVPGlobals.KILLS: 0,
            PVPGlobals.DEATHS: 0}

    def addPlayer(self, avatarId):
        if avatarId in self.players:
            return

        self.players.append(avatarId)
        self.stats[avatarId] = self.getInitialStats(avatarId)
        self.acceptOnce('distObjDelete-%d' % avatarId, self.removePlayer, extraArgs=[avatarId])

    def removePlayer(self, avatarId):
        if avatarId not in self.players:
            return

        self.players.remove(avatarId)
        if avatarId in self.readyPlayers:
            self.readyPlayers.remove(avatarId)

        self.ignore('distObjDelete-%d' % avatarId)
        self.handlePlayerLeft(avatarId)

    def handlePlayerLeft(self, avatarId):
        if not self.players and self.state in ('WaitForServerStart', 'Game'):
            self.request('Cleanup')
        elif self.state == 'WaitForServerStart':
            self.checkAllPresent()

    def getPlayers(self):
        return self.players

    def getTeam(self, avatarId):
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return 0

        return avatar.getPVPTeam()

    def setAvatarReady(self):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.players:
            self.notify.warning('Received setAvatarReady from unknown avatar %d' % avatarId)
            return

        if avatarId not in self.readyPlayers:
            self.readyPlayers.append(avatarId)

        self.checkAllPresent()

    def checkAllPresent(self):
        if self.state != 'WaitForServerStart' or not self.players:
            return

        for avatarId in self.players:
            if avatarId not in self.readyPlayers:
                return

        self.d_allPresent(self.players)
        self.request('Game')

    def __readyTimeout(self, task):
        for avatarId in list(self.players):
            if avatarId not in self.readyPlayers:
                self.removePlayer(avatarId)

        self.checkAllPresent()
        return Task.done

    def d_allPresent(self, avatarIds):
        self.sendUpdate('allPresent', [avatarIds])

    # -------------------------------------------------------------------
    # Stats
    # -------------------------------------------------------------------

    def getPlayerStat(self, avatarId, stat):
        return self.stats.get(avatarId, {}).get(stat, 0)

    def setPlayerStat(self, avatarId, stat, value):
        if avatarId not in self.stats:
            return

        self.stats[avatarId][stat] = value
        self.d_setPlayerStat(avatarId, stat, value)

    def addPlayerStat(self, avatarId, stat, amount):
        self.setPlayerStat(avatarId, stat, self.getPlayerStat(avatarId, stat) + amount)

    def d_setPlayerStat(self, avatarId, stat, value):
        self.sendUpdate('setPlayerStat', [avatarId, stat, value])

    def getStats(self):
        return [[playerId, [[stat, value] for stat, value in list(stats.items())]]
                for playerId, stats in list(self.stats.items())]

    def d_setStats(self, stats):
        self.sendUpdate('setStats', [stats])

    def getRank(self, avatarId):
        score = self.getPlayerStat(avatarId, PVPGlobals.SCORE)
        return 1 + len([playerId for playerId in self.players
                        if self.getPlayerStat(playerId, PVPGlobals.SCORE) > score])

    def d_setResults(self, avatarId, stats, rank):
        self.sendUpdateToAvatarId(avatarId, 'setResults', [stats, rank])

    def d_setGameStart(self, timestamp):
        self.sendUpdate('setGameStart', [timestamp])

    def d_setGameExit(self):
        self.sendUpdate('setGameExit', [])

    def d_setGameAbort(self):
        self.sendUpdate('setGameAbort', [])

    def d_setPvpEvent(self, eventId, data):
        self.sendUpdate('setPvpEvent', [eventId, data])

    def getTimeLimit(self):
        return self.TimeLimit

    # -------------------------------------------------------------------
    # Combat
    # -------------------------------------------------------------------

    def avatarDefeated(self, defeaterId, defeatedId):
        if self.state != 'Game' or defeatedId not in self.players:
            return

        if defeaterId not in self.players:
            defeaterId = defeatedId

        self.addPlayerStat(defeatedId, PVPGlobals.DEATHS, 1)
        if defeaterId != defeatedId:
            self.addPlayerStat(defeaterId, PVPGlobals.KILLS, 1)

        self.handleDefeat(defeaterId, defeatedId)
        self.d_setPvpEvent(PVPGlobals.EventDefeat, [defeaterId, defeatedId])
        self.checkWinCondition()

    def handleDefeat(self, defeaterId, defeatedId):
        pass

    def getTeamScores(self):
        teamScores = {}
        for avatarId in self.players:
            team = self.getTeam(avatarId)
            teamScores[team] = teamScores.get(team, 0) + self.getPlayerStat(avatarId,
                PVPGlobals.SCORE)

        return teamScores

    def checkWinCondition(self):
        if self.state != 'Game' or not self.ScoreLimit:
            return False

        for avatarId in self.players:
            if self.getPlayerStat(avatarId, PVPGlobals.SCORE) >= self.ScoreLimit:
                self.request('ScoreScreen')
                return True

        return False

    def __gameTimeLimit(self, task):
        self.request('ScoreScreen')
        return Task.done

    # -------------------------------------------------------------------
    # States
    # -------------------------------------------------------------------

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterWaitForServerStart(self):
        taskMgr.doMethodLater(PVPGlobals.ReadyBarrierTimeout, self.__readyTimeout,
            self.uniqueName('readyTimeout'))

    def exitWaitForServerStart(self):
        taskMgr.remove(self.uniqueName('readyTimeout'))

    def enterGame(self):
        self.gameStartTime = globalClock.getRealTime()
        self.d_setStats(self.getStats())
        self.d_setGameStart(globalClockDelta.getRealNetworkTime(bits=16))

        timeLimit = self.getTimeLimit()
        if timeLimit:
            taskMgr.doMethodLater(timeLimit, self.__gameTimeLimit,
                self.uniqueName('gameTimeLimit'))

    def exitGame(self):
        taskMgr.remove(self.uniqueName('gameTimeLimit'))

    def enterScoreScreen(self):
        stats = self.getStats()
        for avatarId in self.players:
            self.d_setResults(avatarId, stats, self.getRank(avatarId))

        self.d_setGameExit()

    def exitScoreScreen(self):
        pass

    def enterCleanup(self):
        self.d_setGameAbort()

    def exitCleanup(self):
        pass
