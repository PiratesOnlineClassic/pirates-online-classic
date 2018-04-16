import random

from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.instance.DistributedInstanceWorld import DistributedInstanceWorld
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.StatRowGui import StatRowGui
from pirates.piratesgui.StatRowHeadingGui import StatRowHeadingGui
from pirates.pvp import PVPGlobals
from pirates.pvp.PVPRulesPanel import PVPRulesPanel

EXITED = 0
EXPECTED = 1
JOINED = 2
READY = 3

class ScoreboardHolder:
    

    def __init__(self, game):
        self.game = game

    def getItemList(self):
        return self.game.getScoreList()

    def getItemChangeMsg(self):
        return self.game.taskName('scoreChanged')

    def createNewItem(self, item, parent, itemType=None, columnWidths=[], color=None):
        return self.game.createScoreboardItem(item, parent, itemType=None, columnWidths=[], color=None)


class StatsHolder:
    

    def __init__(self, game):
        self.game = game

    def createNewItem(self, item, parent, itemType=None, columnWidths=[], color=None):
        if itemType == PiratesGuiGlobals.UIListItemType_ColumHeadings:
            newItem = StatRowHeadingGui(item, self.game.getColumnLabels(), parent, itemHeight=PiratesGuiGlobals.TMCompletePageHeight / 16, itemWidths=columnWidths)
        else:
            newItem = StatRowGui(item, self.game.getColumnLabels(), parent, itemHeight=PiratesGuiGlobals.TMCompletePageHeight / 16, itemWidths=columnWidths, txtColor=color)
        newItem.setup()
        return newItem

    def getItemChangeMsg(self):
        return self.game.taskName('statsChanged')

    def getItemList(self):
        return self.game.getStats()

    def getRowTextColor(self, rowHeading):
        return self.game.rowColors.get(rowHeading)


class DistributedPVPInstance(DistributedInstanceWorld, FSM):
    
    notify = directNotify.newCategory('DistributedPVPInstance')
    RulesDoneEvent = 'rulesDone'

    def __init__(self, cr):
        DistributedInstanceWorld.__init__(self, cr)
        FSM.__init__(self, 'DistributedPVPInstance')
        self.teams = {}
        self.names = {}
        self.stats = {}
        self.completed = False
        self.goToSpawnIval = None
        self.scoreboardHolder = ScoreboardHolder(self)
        self.statsHolder = StatsHolder(self)
        localAvatar.guiMgr.radarGui.request('On')

    def generate(self):
        DistributedInstanceWorld.generate(self)
        localAvatar.gameFSM.setDefaultGameState('LandRoam')
        localAvatar.guiMgr.setSeaChestAllowed(False, True, 1)
        localAvatar.guiMgr.hideAvatarDetails()
        NametagGlobals.setMasterNametagsActive(0)
        localAvatar.gameFSM.setDefaultGameState('PVPWait')
        self.acceptOnce('localAvTeleportFinished', self.arrived)

    def announceGenerate(self):
        DistributedInstanceWorld.announceGenerate(self)
        self.eventRng = random.Random(self.doId)

    def disable(self):
        DistributedInstanceWorld.disable(self)
        NametagGlobals.setMasterNametagsActive(1)
        self.cleanupPVP()

    def delete(self):
        self.ignoreAll()
        DistributedInstanceWorld.delete(self)

    def enterWaitOnServer(self):
        if not self.completed:
            localAvatar.guiMgr.showPVPInstructions(self.getTitle(), self.getInstructions())

    def exitWaitOnServer(self):
        localAvatar.guiMgr.hidePVPInstructions()

    def enterGame(self):
        localAvatar.gameFSM.setDefaultGameState('LandRoam')
        localAvatar.gameFSM.request('LandRoam')

    def exitGame(self):
        pass

    def enterCleanup(self):
        pass

    def exitCleanup(self):
        pass

    def enterCompleted(self):
        pass

    def exitCompleted(self):
        pass

    def getTitle(self):
        return PLocalizer.PVPDefaultTitle

    def getInstructions(self):
        return PLocalizer.PVPDefaultInstructions

    def arrived(self):
        self.doneBarrier(self.uniqueName('avatarsReady'))
        if base.cr.activeWorld is self:
            self.request('WaitOnServer')

    def setMatchPlayers(self, players):
        for playerId, name, team in players:
            self.teams[playerId] = team
            self.names[playerId] = name
            self.addPlayerStats(playerId)

        localAvatar.guiMgr.createPVPUI(self.scoreboardHolder)
        localAvatar.guiMgr.createPVPStatus(self.statsHolder)

    def setGameStart(self, timestamp):
        self.gameStartTime = globalClockDelta.networkToLocalTime(timestamp)
        localAvatar.guiMgr.showPVPTimer(self)
        localAvatar.guiMgr.showPVPTeamIcon(self.teams[localAvatar.doId])
        localAvatar.guiMgr.createPVPUI(self.scoreboardHolder)
        localAvatar.guiMgr.createPVPStatus(self.statsHolder)
        self.statsChanged()
        self.scoreChanged()
        localAvatar.guiMgr.showPVPUI()
        self.accept('`', localAvatar.guiMgr.showPVPStatus)
        self.accept('`-up', localAvatar.guiMgr.hidePVPStatus)
        self.request('Game')

    def cleanupPVP(self):
        localAvatar.guiMgr.hidePVPInstructions()
        if self.goToSpawnIval:
            self.cleanupSpawnIval()
        if localAvatar and localAvatar.gameFSM.deathTrack:
            base.localAvatar.gameFSM.deathTrack.finish()
        if localAvatar:
            localAvatar.guiMgr.removePVPUI()

    def setPVPComplete(self):
        if self.completed == True:
            return
        self.cleanupPVP()
        self.completed = True
        self.request('Completed')
        self.ignore('`')
        self.ignore('`-up')
        if not base.cr.teleportMgr.amInTeleport():
            base.transitions.fadeIn(0)
            base.cr.loadingScreen.hide()
            self.lockdownAvatar()

    def lockdownAvatar(self):
        localAvatar.guiMgr.hideTrays()
        localAvatar.stopAutoRun()
        localAvatar.gameFSM.lockFSM = True
        localAvatar.gameFSM.request('PVPWait')
        localAvatar.cameraFSM.request('Control')

    def goToShip(self, pendingObj):
        pendingObj.localAvatarBoardShip()
        self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 'mainWorld')

    def localAvRespawn(self, av):
        self.sendUpdate('requestSpawnLoc')
        self.acceptOnce(self.cr.activeWorld.uniqueName('spawnInfoReceived'), self.requestSpawnLocResp)
        return [True, None]

    def requestSpawnLocResp(self):
        print '[rslr]'
        if self.completed:
            return
        self.goToSpawnIval = Sequence(Func(localAvatar.cameraFSM.request, 'Off'), Wait(2.1), Func(self.respawn), Func(self.cleanupSpawnIval))
        self.goToSpawnIval.start()

    def cleanupSpawnIval(self):
        if self.goToSpawnIval:
            self.goToSpawnIval.pause()
            self.goToSpawnIval = None

    def respawn(self):
        print '[respawn]'
        self.teleportToPosStep1()

    def teleportToPosStep1(self):
        print '[teleportToPosStep1]'
        if self.cr.activeWorld == None or self.cr.activeWorld.spawnInfo == None:
            return
        self.cr.teleportMgr.createSpawnInterests(self.cr.activeWorld.spawnInfo[2], self.teleportToPosStep2, self.worldGrid, localAvatar)

    def teleportToPosStep2(self, parentObj, teleportingObj):
        print '[teleportToPosStep2]'
        base.cr.teleportMgr.localTeleportPos(self.cr.activeWorld.spawnInfo[0], parentObj, smooth=True)

    def requestPVPLeave(self):
        self.sendUpdate('requestLeave', [])
        self.performLeave()

    def performAILeave(self):
        if base.cr.teleportMgr.amInTeleport():
            DelayedCall(Functor(self.performAILeave), delay=1)
            return
        self.performLeave()

    def performLeave(self):
        self.cleanupPVP()
        localAvatar.guiMgr.hidePVPCompleteUI()
        localAvatar.guiMgr.showTrays()
        localAvatar.guiMgr.removePVPStatus()
        localAvatar.guiMgr.removePVPCompleteUI()
        localAvatar.guiMgr.setSeaChestAllowed(True, False, 1, True)
        localAvatar.gameFSM.lockFSM = False
        base.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 'mainWorld', shardId=localAvatar.getDefaultShard())
        base.cr.loadingScreen.showTarget()

    def requestLeaveApproved(self):
        pass

    def requestPVPReplay(self):
        localAvatar.guiMgr.hidePVPCompleteUI()
        localAvatar.guiMgr.showTrays()
        self.localAvRespawn(localAvatar)
        localAvatar.guiMgr.removePVPCompleteUI()
        localAvatar.guiMgr.createPVPUI(self.scoreboardHolder)

    def setResults(self, stats, rank, teams, tie=False):
        for playerId, playerStats in stats:
            for stat, value in playerStats:
                self.stats[playerId][stat] = value

        self.statsChanged()
        localAvatar.guiMgr.createPVPCompleteUI(self)
        localAvatar.guiMgr.setPVPResult('player', rank, teams, tie)
        localAvatar.guiMgr.showPVPCompleteUI()

    def getMaxCarry(self):
        return 0

    def getAvTeam(self, av):
        avTeam = self.teams.get(av.getDoId())
        if avTeam:
            return [True, avTeam]
        return [False, None]

    def showDeathLoadingScreen(self, av):
        pass

    def hideDeathLoadingScreen(self, av):
        pass

    def updateShipProximityText(self, ship):
        pass

    def handleShipUse(self, ship):
        pass

    def updateTreasureProximityText(self, treasure):
        pass

    def handleTreasureUse(self, treasure):
        pass

    def setLocalAvatarDefaultGameState(self, loot):
        if localAvatar.lootCarried > 0:
            localAvatar.gameFSM.setDefaultGameState('LandTreasureRoam')
            return
        localAvatar.gameFSM.setDefaultGameState('LandRoam')

    def handleLocalAvatarEnterWater(self):
        if localAvatar.lootCarried > 0:
            localAvatar.b_setGameState('WaterTreasureRoam')
            return
        localAvatar.b_setGameState('WaterRoam')

    def handleLocalAvatarExitWater(self):
        if localAvatar.lootCarried > 0:
            localAvatar.b_setGameState('LandTreasureRoam')
            return
        localAvatar.b_setGameState('LandRoam')

    def handleDeposit(self, team, avId, bankId):
        pass

    def handleUseKey(self, interactiveObj):
        pass

    def localAvEnterDeath(self, av):
        DistributedInstanceWorld.localAvEnterDeath(self, av)
        if not self.completed:
            self.localAvRespawn(av)

    def localAvExitDeath(self, av):
        DistributedInstanceWorld.localAvExitDeath(self, av)
        self.cleanupSpawnIval()

    def hasTimeLimit(self):
        return False

    def getTimeLimit(self):
        return 0

    def setTimeLimit(self, timeLimit):
        self._timeLimit = timeLimit

    def scoreChanged(self):
        messenger.send(self.taskName('scoreChanged'))

    def sortScores(self, item1, item2):
        return item2.get('Score') - item1.get('Score')

    def getScoreList(self):
        return

    def createScoreboardItem(self):
        return

    def getScoreText(self, scoreValue):
        return ''

    def statsChanged(self):
        messenger.send(self.taskName('statsChanged'))

    def getColumnStats(self):
        return [PVPGlobals.KILLS, PVPGlobals.DEATHS]

    def getColumnLabels(self):
        return [PLocalizer.PVPPlayer, PLocalizer.PVPEnemiesDefeated, PLocalizer.PVPTimesDefeated]

    def addPlayerStats(self, playerId):
        pass

    def sortStats(self, stats):
        stats = sorted(stats, key=lambda x: x[1][PVPGlobals.SCORE])

    def setPlayerStat(self, playerId, stat, value):
        self.stats[playerId][stat] = value
        self.statsChanged()

    def setStats(self, stats):
        for playerId, playerStats in stats:
            if playerId not in self.stats:
                self.addPlayerStats(playerId)
            for stat, value in playerStats:
                self.stats[playerId][stat] = value

        self.statsChanged()

    def sortStats(self, stats):
        return sorted(stats, key=lambda x: x[1][PVPGlobals.SCORE])

    def getStats(self):
        return self.getPlayerStats()

    def getPlayerStats(self):
        displayStats = []
        for playerId, stats in self.stats.items():
            if playerId not in self.names:
                continue
            playerName = self.names[playerId]
            playerTeam = self.teams[playerId]
            playerStats = []
            for stat in self.getColumnStats():
                playerStats.append([PVPGlobals.statText[stat], str(stats[stat])])

            if playerId == localAvatar.doId:
                playerColor = (1, 1, 1, 1)
            else:
                playerColor = PVPGlobals.getTeamColor(playerTeam)
            displayStats.append([playerName, playerStats, ['color', playerColor]])

        displayStats = self.sortStats(displayStats)
        displayStats.insert(0, self.getColumnLabels())
        return displayStats

    def getTeamStats(self):
        displayStats = []
        teams = {}
        for playerId, stats in self.stats.items():
            if playerId not in self.names:
                continue
            playerName = self.names[playerId]
            playerTeam = self.teams[playerId]
            if not teams.get(playerTeam):
                teams[playerTeam] = []
            playerStats = []
            for stat in self.getColumnStats():
                playerStats.append([PVPGlobals.statText[stat], str(stats[stat])])

            if playerId == localAvatar.doId:
                playerColor = (1, 1, 1, 1)
            else:
                playerColor = None
            teams[playerTeam].append([playerName, playerStats, ['color', playerColor]])

        for team, teamStats in teams.items():
            teamTotals = []
            for stat in self.getColumnStats():
                teamTotals.append([PVPGlobals.statText[stat], 0])

            for playerName, playerStats, color in teamStats:
                for i in range(len(playerStats)):
                    teamTotals[i][1] = str(int(teamTotals[i][1]) + int(playerStats[i][1]))

            teamStat = [
             'Team %s' % team, teamTotals, ['color', PVPGlobals.getTeamColor(team)]]
            teamStats = self.sortStats(teamStats)
            teamStats.insert(0, teamStat)
            displayStats += teamStats

        displayStats.insert(0, self.getColumnLabels())
        return displayStats

    def setPvpEvent(self, eventId, data):
        if eventId is PVPGlobals.EventDefeat:
            defeaterId, defeatedId = data
            self.handleDefeatEvent(defeaterId, defeatedId)

    def handleDefeatEvent(self, defeaterId, defeatedId):
        if defeaterId == defeatedId:
            thirdPersonMsgs = [PLocalizer.PVPSuicide]
            if defeatedId == localAvatar.doId:
                firstPersonMsgs = [
                 PLocalizer.PVPYouSuicide]
            else:
                firstPersonMsgs = None
        else:
            thirdPersonMsgs = [
             PLocalizer.PVPDefeat]
            if defeatedId == localAvatar.doId:
                firstPersonMsgs = [
                 PLocalizer.PVPYouWereDefeated]
            elif defeaterId == localAvatar.doId:
                firstPersonMsgs = [
                 PLocalizer.PVPYouDefeated]
            else:
                firstPersonMsgs = None
        firstPersonMsg = None
        if firstPersonMsgs:
            firstPersonMsg = self.eventRng.choice(firstPersonMsgs)
        thirdPersonMsg = self.eventRng.choice(thirdPersonMsgs)
        defeaterName = self.names[defeaterId]
        defeatedName = self.names[defeatedId]
        d = {'defeater': defeaterName, 'defeated': defeatedName}
        if firstPersonMsg:
            firstPersonMsg = firstPersonMsg % d
        thirdPersonMsg = thirdPersonMsg % d
        if firstPersonMsg:
            localAvatar.guiMgr.messageStack.addTextMessage(firstPersonMsg)
        base.chatAssistant.receiveSystemMessage(thirdPersonMsg)