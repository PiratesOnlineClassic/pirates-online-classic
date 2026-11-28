import random

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
from direct.fsm.FSM import FSM
from direct.task import Task

from otp.ai import AIInterestHandles

from pirates.battle import WeaponGlobals
from pirates.instance.DistributedInstanceWorldAI import DistributedInstanceWorldAI
from pirates.piratesbase import PiratesGlobals
from pirates.pvp import PVPGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.world import WorldGlobals

EXITED = 0
EXPECTED = 1
JOINED = 2
READY = 3


class DistributedPVPInstanceAI(DistributedInstanceWorldAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPVPInstanceAI')

    GameStyle = PiratesGlobals.GAME_STYLE_BATTLE
    RankingType = InventoryType.BTLGame
    InfamyType = InventoryType.PVPTotalInfamyLand
    TimeLimit = 0
    ScoreLimit = 0
    MinTeams = 2
    SetupDelay = 1.0
    CompletedLeaveDelay = config.GetFloat('pvp-completed-leave-delay', 60.0)

    # the client teleports itself back to the main world when it leaves the
    # instance (see DistributedPVPInstance.performLeave), we only step in when
    # it has not started doing so by itself after this amount of time...
    LeaveTeleportTimeout = config.GetFloat('pvp-leave-teleport-timeout', 5.0)

    # respawned players are given the temporary spawning invulnerability
    # skill effect (WeaponGlobals.C_SPAWN) the client already understands...
    RespawnInvulnerabilityDuration = config.GetFloat('pvp-respawn-invulnerability-duration', 5.0)

    def __init__(self, air):
        DistributedInstanceWorldAI.__init__(self, air)
        FSM.__init__(self, self.__class__.__name__)

        self.type = PiratesGlobals.INSTANCE_PVP

        self.isReady = False
        self.pendingTeleportCallbacks = []
        self.pendingTeams = None

        # avatarId -> [name, team]
        self.players = {}
        self.playerStates = {}
        self.stats = {}
        self.lastAttackers = {}
        self.instanceInterests = set()
        self.teamSpawnPts = {}
        self.spawnProtected = set()

        self.readyBarrier = None
        self.gameStartTime = 0
        self.completed = False

    # -------------------------------------------------------------------
    # Generation
    # -------------------------------------------------------------------

    def generateWithRequired(self, zoneId, optionalFields=[]):
        # PvP instances are only ever visible to the players taking part in
        # the match. Rather than living in the district's management zone,
        # which every client has interest in, we give each match it's own
        # zone and open interest on the behalf of each participant...
        DistributedInstanceWorldAI.generateWithRequired(self, self.air.allocateZone(),
            optionalFields)

    def announceGenerate(self):
        DistributedInstanceWorldAI.announceGenerate(self)

        # the world creator loads the instance's children after the
        # instance itself has been generated, wait until they exist...
        taskMgr.doMethodLater(self.SetupDelay, self.__setupInstance,
            self.uniqueName('setupInstance'))

    def __setupInstance(self, task):
        self.loadSpawnPoints()
        self.setupGame()

        self.isReady = True
        callbacks, self.pendingTeleportCallbacks = self.pendingTeleportCallbacks, []
        for callback in callbacks:
            callback()

        if self.pendingTeams is not None:
            teams, self.pendingTeams = self.pendingTeams, None
            self.startMatch(teams)

        return Task.done

    def setupGame(self):
        pass

    def delete(self):
        taskMgr.remove(self.uniqueName('setupInstance'))
        taskMgr.remove(self.uniqueName('gameTimeLimit'))
        taskMgr.remove(self.uniqueName('completedLeave'))
        taskMgr.remove(self.uniqueName('cleanupInstance'))
        if self.readyBarrier is not None:
            self.ignoreBarrier(self.readyBarrier)
            self.readyBarrier = None

        for avatarId in list(self.players.keys()):
            self.removePlayer(avatarId)

        for avatarId in list(self.instanceInterests):
            taskMgr.remove(self.uniqueName('leaveTeleport-%d' % avatarId))

        for avatarId in list(self.instanceInterests):
            self.removeInstanceInterest(avatarId)

        self.ignoreAll()
        self.pendingTeleportCallbacks = []
        self.demand('Off')
        DistributedInstanceWorldAI.delete(self)

    def getParentingRules(self):
        return ['', '']

    # -------------------------------------------------------------------
    # Spawn points
    # -------------------------------------------------------------------

    def loadSpawnPoints(self):
        # The world data player spawn nodes are tagged with the team that
        # may use them, we need to keep track of these in order to spawn
        # each team at their own side of the map...
        self.teamSpawnPts = {}
        worldCreator = self.air.worldCreator
        fileData = worldCreator.openFile(self.getFileName() + '.py')
        if not fileData:
            self.notify.warning('Cannot load spawn points for %s, no world data found!' %
                self.getFileName())

            return

        for regionUid, regionData in list(fileData.get('Objects', {}).items()):
            for objKey, objData in list(regionData.get('Objects', {}).items()):
                objType = objData.get('Type')
                if objType == 'Island':
                    islandData = objData
                    islandFile = objData.get('File')
                    if islandFile:
                        islandFileData = worldCreator.openFile(islandFile + '.py')
                        if islandFileData:
                            islandData = islandFileData.get('Objects', {}).get(objKey, objData)

                    self.findSpawnNodes(objKey, islandData)
                elif objType == 'Player Spawn Node':
                    self.addTeamSpawnPt(self.getUniqueId(), objData)

    def findSpawnNodes(self, areaUid, objData):
        for objKey, childData in list(objData.get('Objects', {}).items()):
            objType = childData.get('Type')
            if objType == 'Player Spawn Node':
                self.addTeamSpawnPt(areaUid, childData)
            elif objType == 'Island Game Area':
                # the deathmatch and mayhem maps only place their spawn nodes
                # within the island's game areas, which live in their own files...
                areaFile = childData.get('File')
                if areaFile:
                    areaFileData = self.air.worldCreator.openFile(areaFile + '.py')
                    if areaFileData:
                        childData = areaFileData.get('Objects', {}).get(objKey, childData)

                self.findSpawnNodes(objKey, childData)
                continue

            self.findSpawnNodes(areaUid, childData)

    def addTeamSpawnPt(self, areaUid, objData):
        team = self.getSpawnTeam(objData.get('Spawnables', 'All'))
        x, y, z = objData.get('GridPos', objData.get('Pos', (0, 0, 0)))
        h = objData.get('Hpr', (0, 0, 0))[0]
        self.teamSpawnPts.setdefault(team, []).append((areaUid, (x, y, z, h)))

    def getSpawnTeam(self, spawnables):
        if spawnables.startswith('Team '):
            try:
                return int(spawnables[5:])
            except ValueError:
                pass

        return 0

    def getSpawnArea(self, areaUid):
        if areaUid == self.getUniqueId():
            return self.oceanGrid

        return self.builder.getObject(uniqueId=areaUid)

    def getPlayerSpawnPt(self, team):
        # free for all games use every spawn point available
        # in the map regardless of which team it belongs to...
        if self.GameStyle == PiratesGlobals.GAME_STYLE_BATTLE:
            candidates = []
            for spawnPts in list(self.teamSpawnPts.values()):
                candidates.extend(spawnPts)
        else:
            candidates = self.teamSpawnPts.get(team, []) + self.teamSpawnPts.get(0, [])

        candidates = [(self.getSpawnArea(areaUid), spawnPt) for areaUid, spawnPt in candidates]
        candidates = [candidate for candidate in candidates if candidate[0] is not None]
        if candidates:
            return random.choice(candidates)

        islands = self.builder.getIslands()
        if not islands:
            return (None, None)

        island = islands[0]
        return (island, self.getSpawnPt(island.getUniqueId()))

    # -------------------------------------------------------------------
    # Players
    # -------------------------------------------------------------------

    def setupMatch(self, teams):
        if not self.isReady:
            self.pendingTeams = teams
            return

        self.startMatch(teams)

    def startMatch(self, teams):
        for team, avatarIds in enumerate(teams):
            for avatarId in avatarIds:
                avatar = self.air.doId2do.get(avatarId)
                if not avatar:
                    self.notify.warning('Cannot add avatar %d to pvp instance %d, '
                        'avatar no longer exists!' % (avatarId, self.doId))

                    continue

                self.addPlayer(avatar, self.getPlayerTeam(avatar, team + 1))

        if not self.players:
            self.notify.warning('Pvp instance %d has no players, cleaning up!' % self.doId)
            self.request('Cleanup')
            return

        self.d_setMatchPlayers(self.getMatchPlayers())
        self.d_setStats(self.getStats())
        self.request('WaitClientsReady')

        for avatarId in list(self.players.keys()):
            self.sendPlayerToInstance(avatarId)

    def getPlayerTeam(self, avatar, team):
        return team

    def getInitialStats(self, avatarId):
        return {
            PVPGlobals.SCORE: 0,
            PVPGlobals.KILLS: 0,
            PVPGlobals.DEATHS: 0}

    def addPlayer(self, avatar, team):
        if avatar.doId in self.players:
            return

        self.players[avatar.doId] = [avatar.getName(), team]
        self.playerStates[avatar.doId] = EXPECTED
        self.stats[avatar.doId] = self.getInitialStats(avatar.doId)
        avatar.b_setPVPTeam(team)

        self.addInstanceInterest(avatar.doId)
        self.acceptOnce(avatar.getDeleteEvent(), self.__playerDeleted, extraArgs=[avatar.doId])
        self.notify.info('Added avatar %d to pvp instance %d on team %d' % (avatar.doId,
            self.doId, team))

    def removePlayer(self, avatarId):
        if avatarId not in self.players:
            return

        del self.players[avatarId]
        self.playerStates[avatarId] = EXITED
        self.lastAttackers.pop(avatarId, None)
        self.ignore('distObjDelete-%d' % avatarId)
        self.ignore('teleportDone-%d' % avatarId)
        self.removeSpawnProtection(avatarId)

        avatar = self.air.doId2do.get(avatarId)
        if avatar:
            avatar.b_setPVPTeam(0)

        self.notify.info('Removed avatar %d from pvp instance %d' % (avatarId, self.doId))

    def __playerDeleted(self, avatarId):
        self.removePlayer(avatarId)
        self.instanceInterests.discard(avatarId)
        taskMgr.remove(self.uniqueName('leaveTeleport-%d' % avatarId))
        self.handlePlayerLeft(avatarId)

    def handlePlayerLeft(self, avatarId):
        if self.state == 'Game' and len(self.getActiveTeams()) < self.MinTeams:
            self.notify.info('Not enough teams remaining in pvp instance %d, '
                'ending game early...' % self.doId)

            self.request('Completed')
        elif self.state in ('Completed', 'WaitClientsReady') and not self.players:
            self.request('Cleanup')

    def hasPlayer(self, avatarId):
        return avatarId in self.players

    def getTeam(self, avatarId):
        player = self.players.get(avatarId)
        if not player:
            return 0

        return player[1]

    def getActiveTeams(self):
        teams = []
        for name, team in list(self.players.values()):
            if team not in teams:
                teams.append(team)

        return teams

    def getTeamPlayers(self, team):
        return [avatarId for avatarId, (name, playerTeam) in list(self.players.items())
                if playerTeam == team]

    def addInstanceInterest(self, avatarId):
        if avatarId in self.instanceInterests:
            return

        clientChannel = self.GetPuppetConnectionChannel(avatarId)
        self.air.clientAddInterest(clientChannel, AIInterestHandles.PIRATES_PVP_INSTANCE,
            self.parentId, self.zoneId, False)

        self.instanceInterests.add(avatarId)

    def removeInstanceInterest(self, avatarId):
        if avatarId not in self.instanceInterests:
            return

        self.instanceInterests.discard(avatarId)
        clientChannel = self.GetPuppetConnectionChannel(avatarId)
        self.air.clientRemoveInterest(clientChannel, AIInterestHandles.PIRATES_PVP_INSTANCE, False)

    def sendPlayerToInstance(self, avatarId):
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return

        area, spawnPt = self.getPlayerSpawnPt(self.getTeam(avatarId))
        if not area or not spawnPt:
            self.notify.warning('Cannot send avatar %d to pvp instance %d, '
                'no spawn point available!' % (avatarId, self.doId))

            return

        self.acceptOnce('teleportDone-%d' % avatarId, self._playerArrived, extraArgs=[avatarId])
        self.air.teleportMgr.d_initiateTeleport(avatar,
            instanceType=self.getType(),
            instanceName=self.getFileName(),
            locationUid=area.getUniqueId(),
            spawnPt=spawnPt,
            targetWorld=self)

    def _playerArrived(self, avatarId):
        if avatarId not in self.players:
            return

        self.playerStates[avatarId] = JOINED
        self.handlePlayerArrived(avatarId)

    def handlePlayerArrived(self, avatarId):
        pass

    def waitForPlayerLeave(self, avatarId):
        # the client always initiates it's own teleport back to the main world
        # when leaving (DistributedPVPInstance.performLeave), so we must not start
        # a second teleport which would collide with it. Once the avatar has
        # left the instance they no longer need to see it, close the interest
        # we opened for them...
        self.acceptOnce('teleportDone-%d' % avatarId, self.__playerLeft,
            extraArgs=[avatarId])

        taskName = self.uniqueName('leaveTeleport-%d' % avatarId)
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(self.LeaveTeleportTimeout, self.__leaveTeleportTimeout,
            taskName, extraArgs=[avatarId])

    def __playerLeft(self, avatarId):
        taskMgr.remove(self.uniqueName('leaveTeleport-%d' % avatarId))
        self.removeInstanceInterest(avatarId)

    def isAvatarInInstance(self, avatar):
        return avatar.getWorld() is self

    def __leaveTeleportTimeout(self, avatarId):
        avatar = self.air.doId2do.get(avatarId)
        if not avatar or avatarId in self.players:
            return Task.done

        if avatarId in self.air.teleportMgr.avatar2fsm:
            # the avatar's own teleport is still in progress...
            return Task.done

        if not self.isAvatarInInstance(avatar):
            self.__playerLeft(avatarId)
            return Task.done

        self.notify.info('Avatar %d never left pvp instance %d, sending them home...' % (
            avatarId, self.doId))

        self.sendPlayerToMainWorld(avatarId)
        return Task.done

    def sendPlayerToMainWorld(self, avatarId):
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return

        self.ignore('teleportDone-%d' % avatarId)
        self.acceptOnce('teleportDone-%d' % avatarId, self.__playerLeft,
            extraArgs=[avatarId])

        self.air.teleportMgr.d_initiateTeleport(avatar,
            instanceType=PiratesGlobals.INSTANCE_MAIN,
            instanceName=WorldGlobals.PiratesWorldSceneFileBase,
            locationUid=avatar.getReturnLocation())

    # -------------------------------------------------------------------
    # DC fields
    # -------------------------------------------------------------------

    def getMatchPlayers(self):
        return [[avatarId, name, team] for avatarId, (name, team) in list(self.players.items())]

    def d_setMatchPlayers(self, players):
        self.sendUpdate('setMatchPlayers', [players])

    def d_setGameStart(self, timestamp):
        self.sendUpdate('setGameStart', [timestamp])

    def d_setPlayerStat(self, playerId, stat, value):
        self.sendUpdate('setPlayerStat', [playerId, stat, value])

    def getStats(self):
        return [[playerId, [[stat, value] for stat, value in list(stats.items())]]
                for playerId, stats in list(self.stats.items())]

    def d_setStats(self, stats):
        self.sendUpdate('setStats', [stats])

    def d_setResults(self, avatarId, stats, rank, teams, tie):
        self.sendUpdateToAvatarId(avatarId, 'setResults', [stats, rank, teams, tie])

    def d_setPVPComplete(self):
        self.sendUpdate('setPVPComplete', [])

    def d_performAILeave(self, avatarId):
        self.sendUpdateToAvatarId(avatarId, 'performAILeave', [])

    def d_requestLeaveApproved(self, avatarId):
        self.sendUpdateToAvatarId(avatarId, 'requestLeaveApproved', [])

    def d_setPvpEvent(self, eventId, data):
        self.sendUpdate('setPvpEvent', [eventId, data])

    def getTimeLimit(self):
        return self.TimeLimit

    def setAvatarReady(self):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.players:
            return

        self.playerStates[avatarId] = READY

    def requestSpawnLoc(self):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return

        if avatarId not in self.players:
            self.air.logPotentialHacker(
                message='Received requestSpawnLoc from avatar not in pvp instance',
                targetAvId=avatarId,
                instanceId=self.doId)

            return

        if self.completed:
            return

        self.respawnPlayer(avatar)

    def respawnPlayer(self, avatar):
        area, spawnPt = self.getPlayerSpawnPt(self.getTeam(avatar.doId))
        if not area or not spawnPt:
            self.notify.warning('Cannot respawn avatar %d, no spawn point available!' %
                avatar.doId)

            return

        avatar.b_setHp(avatar.getMaxHp())
        avatar.b_setMojo(avatar.getMaxMojo())
        self.addSpawnProtection(avatar)

        x, y, z, h = spawnPt
        self.d_setSpawnInfo(avatar.doId, x, y, z, h, 0, [area.doId, area.zoneId,
            area.parentId])

    def addSpawnProtection(self, avatar):
        duration = self.RespawnInvulnerabilityDuration
        if duration <= 0:
            return

        self.removeSpawnProtection(avatar.doId)
        self.spawnProtected.add(avatar.doId)
        avatar.addSkillEffect(WeaponGlobals.C_SPAWN, duration, avatar.doId)
        taskMgr.doMethodLater(duration, self.__spawnProtectionExpired,
            self.uniqueName('spawnProtection-%d' % avatar.doId), extraArgs=[avatar.doId])

    def removeSpawnProtection(self, avatarId):
        taskMgr.remove(self.uniqueName('spawnProtection-%d' % avatarId))
        if avatarId not in self.spawnProtected:
            return

        self.spawnProtected.discard(avatarId)
        avatar = self.air.doId2do.get(avatarId)
        if avatar:
            avatar.removeSkillEffect(WeaponGlobals.C_SPAWN)

    def hasSpawnProtection(self, avatarId):
        return avatarId in self.spawnProtected

    def __spawnProtectionExpired(self, avatarId):
        self.removeSpawnProtection(avatarId)
        return Task.done

    def avatarDied(self):
        pass

    def requestLeave(self):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.players:
            return

        self.notify.info('Avatar %d requested to leave pvp instance %d' % (avatarId,
            self.doId))

        self.d_requestLeaveApproved(avatarId)
        self.removePlayer(avatarId)
        self.waitForPlayerLeave(avatarId)
        self.handlePlayerLeft(avatarId)

    # -------------------------------------------------------------------
    # Combat
    # -------------------------------------------------------------------

    def isDamageAllowed(self, attacker, target):
        if self.state != 'Game':
            return False

        if attacker.doId not in self.players or target.doId not in self.players:
            return False

        if attacker.doId == target.doId:
            return True

        # the client treats spawning players as unattackable, see BattleManager.doAttack
        if self.hasSpawnProtection(target.doId):
            return False

        return self.getTeam(attacker.doId) != self.getTeam(target.doId)

    def avatarAttacked(self, attacker, target):
        self.lastAttackers[target.doId] = attacker.doId

    def avatarDefeated(self, avatar):
        defeatedId = avatar.doId
        if defeatedId not in self.players or self.state != 'Game':
            return

        defeaterId = self.lastAttackers.pop(defeatedId, defeatedId)
        if defeaterId not in self.players:
            defeaterId = defeatedId

        self.addPlayerStat(defeatedId, PVPGlobals.DEATHS, 1)
        if defeaterId != defeatedId:
            self.addPlayerStat(defeaterId, PVPGlobals.KILLS, 1)

        self.handleDefeat(defeaterId, defeatedId)
        self.d_setPvpEvent(PVPGlobals.EventDefeat, [defeaterId, defeatedId])
        self.checkWinCondition()

    def handleDefeat(self, defeaterId, defeatedId):
        if defeaterId != defeatedId:
            self.addPlayerStat(defeaterId, PVPGlobals.SCORE, 1)

    # -------------------------------------------------------------------
    # Scoring
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

    def getTeamScores(self):
        teamScores = {}
        for avatarId, (name, team) in list(self.players.items()):
            teamScores[team] = teamScores.get(team, 0) + self.getPlayerStat(avatarId,
                PVPGlobals.SCORE)

        return teamScores

    def getTeamRank(self, team, teamScores):
        score = teamScores.get(team, 0)
        return 1 + len([otherScore for otherScore in list(teamScores.values())
                        if otherScore > score])

    def isTie(self, teamScores):
        if len(teamScores) < 2:
            return False

        bestScore = max(teamScores.values())
        return list(teamScores.values()).count(bestScore) > 1

    def checkWinCondition(self):
        if self.state != 'Game' or not self.ScoreLimit:
            return False

        for team, score in list(self.getTeamScores().items()):
            if score >= self.ScoreLimit:
                self.request('Completed')
                return True

        return False

    def __gameTimeLimit(self, task):
        self.notify.info('Pvp instance %d reached it\'s time limit' % self.doId)
        self.request('Completed')
        return Task.done

    # -------------------------------------------------------------------
    # States
    # -------------------------------------------------------------------

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterWaitClientsReady(self):
        self.readyBarrier = self.beginBarrier(self.uniqueName('avatarsReady'),
            list(self.players.keys()), PVPGlobals.ReadyBarrierTimeout, self.__clientsReady)

    def __clientsReady(self, readyAvatars):
        self.readyBarrier = None
        if self.state != 'WaitClientsReady':
            return

        readyAvatars = [avatarId for avatarId in readyAvatars if avatarId in self.players]
        for avatarId in readyAvatars:
            self.playerStates[avatarId] = READY

        if not readyAvatars:
            self.notify.warning('No players arrived in pvp instance %d!' % self.doId)
            self.request('Cleanup')
            return

        self.request('Game')

    def exitWaitClientsReady(self):
        if self.readyBarrier is not None:
            self.ignoreBarrier(self.readyBarrier)
            self.readyBarrier = None

    def enterGame(self):
        self.gameStartTime = globalClock.getRealTime()
        self.d_setGameStart(globalClockDelta.getRealNetworkTime(bits=16))

        timeLimit = self.getTimeLimit()
        if timeLimit:
            taskMgr.doMethodLater(timeLimit, self.__gameTimeLimit,
                self.uniqueName('gameTimeLimit'))

    def exitGame(self):
        taskMgr.remove(self.uniqueName('gameTimeLimit'))

    def enterCompleted(self):
        self.completed = True
        teamScores = self.getTeamScores()
        tie = self.isTie(teamScores)
        numTeams = max(len(teamScores), len(self.getActiveTeams()))
        stats = self.getStats()

        for avatarId, (name, team) in list(self.players.items()):
            rank = self.getTeamRank(team, teamScores)
            self.d_setResults(avatarId, stats, rank, numTeams, tie)
            self.rewardPlayer(avatarId, rank, tie)

        self.d_setPVPComplete()
        taskMgr.doMethodLater(self.CompletedLeaveDelay, self.__completedLeave,
            self.uniqueName('completedLeave'))

    def rewardPlayer(self, avatarId, rank, tie):
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return

        inventory = avatar.getInventory()
        if not inventory:
            self.notify.warning('Cannot reward avatar %d, no inventory found!' % avatarId)
            return

        infamy = max(0, self.getPlayerStat(avatarId, PVPGlobals.SCORE))
        if rank == 1 and not tie:
            if self.RankingType:
                inventory.b_setStackQuantity(self.RankingType,
                    inventory.getStackQuantity(self.RankingType) + 1)

            infamy += PVPGlobals.TeamBalanceValues.Player

        if infamy and self.InfamyType:
            inventory.b_setStackQuantity(self.InfamyType,
                inventory.getStackQuantity(self.InfamyType) + infamy)

            inventory.b_setStackQuantity(InventoryType.PVPCurrentInfamy,
                inventory.getStackQuantity(InventoryType.PVPCurrentInfamy) + infamy)

    def __completedLeave(self, task):
        for avatarId in list(self.players.keys()):
            self.d_performAILeave(avatarId)
            self.removePlayer(avatarId)
            self.waitForPlayerLeave(avatarId)

        self.request('Cleanup')
        return Task.done

    def exitCompleted(self):
        taskMgr.remove(self.uniqueName('completedLeave'))

    def enterCleanup(self):
        # give the avatars enough time to finish teleporting
        # out of the instance before it is removed...
        taskMgr.doMethodLater(PVPGlobals.RulesDuration, self.__cleanupInstance,
            self.uniqueName('cleanupInstance'))

    def __cleanupInstance(self, task):
        for avatarId in list(self.players.keys()):
            self.removePlayer(avatarId)

        # the islands and their game areas are all generated beneath us, along
        # with any sub instance a game area may have been given by the builder...
        for subInstance in self.getSubInstances():
            self.removeSubInstance(subInstance)
            for object in list(subInstance.builder.objectList.values()):
                subInstance.builder.removeObject(object)

            subInstance.requestDelete()

        for object in list(self.builder.objectList.values()):
            self.builder.removeObject(object)
            object.requestDelete()

        if self.oceanGrid:
            self.oceanGrid.requestDelete()

        if self.air.uidMgr.getDoId(self.getUniqueId()) == self.doId:
            self.air.uidMgr.removeUid(self.getUniqueId())

        self.requestDelete()
        return Task.done

    def exitCleanup(self):
        taskMgr.remove(self.uniqueName('cleanupInstance'))
