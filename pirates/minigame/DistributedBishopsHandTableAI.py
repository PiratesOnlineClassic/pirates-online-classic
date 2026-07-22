import random

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
from direct.task import Task
from direct.task.TaskManagerGlobal import *
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from pirates.minigame import BishopsHandGlobals


class DistributedBishopsHandTableAI(DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBishopsHandTableAI')

    EntryFee = 2  # gold to join a round
    SequenceLength = 30  # steps in a round sequence

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air)
        self._tableState = 0           # 0=idle, 1=playing
        self._seatStatus = []          # [(avId, state), ...] per seat
        self._pendingStakes = 0
        self._activeStakes = 0
        self._runningStakes = 0
        self._gameTimer = 0
        self._joinedSeats = set()      # seats that paid and joined the current round
        self._progressReport = []      # [(seat, percent), ...]
        self._roundSequence = []

    def delete(self):
        taskMgr.remove(self.uniqueName('bh-start'))
        taskMgr.remove(self.uniqueName('bh-round'))
        DistributedGameTableAI.delete(self)

    # ------------------------------------------------------------------
    # DC field accessors
    # ------------------------------------------------------------------

    def setParentingRules(self, rule1, rule2):
        self._parentingRules = (rule1, rule2)

    def getParentingRules(self):
        rules = getattr(self, '_parentingRules', ('', ''))
        return list(rules)

    def setTableState(self, tableState, seatStatus):
        self._tableState = tableState
        self._seatStatus = list(seatStatus)

    def d_setTableState(self):
        self.sendUpdate('setTableState', [self._tableState, self._seatStatus])

    def getTableState(self):
        return [self._tableState, self._seatStatus]

    def setPendingStakes(self, stakes):
        self._pendingStakes = stakes

    def d_setPendingStakes(self, stakes):
        self.sendUpdate('setPendingStakes', [stakes])

    def b_setPendingStakes(self, stakes):
        self.setPendingStakes(stakes)
        self.d_setPendingStakes(stakes)

    def getPendingStakes(self):
        return self._pendingStakes

    def setActiveStakes(self, stakes):
        self._activeStakes = stakes

    def d_setActiveStakes(self, stakes):
        self.sendUpdate('setActiveStakes', [stakes])

    def b_setActiveStakes(self, stakes):
        self.setActiveStakes(stakes)
        self.d_setActiveStakes(stakes)

    def getActiveStakes(self):
        return self._activeStakes

    def setRunningStakes(self, stakes):
        self._runningStakes = stakes

    def d_setRunningStakes(self, stakes):
        self.sendUpdate('setRunningStakes', [stakes])

    def b_setRunningStakes(self, stakes):
        self.setRunningStakes(stakes)
        self.d_setRunningStakes(stakes)

    def getRunningStakes(self):
        return self._runningStakes

    def setProgressReport(self, report):
        self._progressReport = list(report)

    def d_setProgressReport(self, report):
        self.sendUpdate('setProgressReport', [report])

    def setGameTimer(self, time, timestamp):
        self._gameTimer = time

    def d_setGameTimer(self, time, timestamp):
        self.sendUpdate('setGameTimer', [time, timestamp])

    def getGameTimer(self):
        return [self._gameTimer,
            globalClockDelta.getRealNetworkTime(bits=16)]

    # ------------------------------------------------------------------
    # Seat lifecycle
    # ------------------------------------------------------------------

    def announceGenerate(self):
        DistributedGameTableAI.announceGenerate(self)
        self._rebuildSeatStatus()
        self.d_setTableState()
        self.b_setPendingStakes(0)
        self.b_setActiveStakes(0)
        self.b_setRunningStakes(0)

    def avatarSit(self, avatar, seatIndex):
        DistributedGameTableAI.avatarSit(self, avatar, seatIndex)
        self._rebuildSeatStatus()
        self.d_setTableState()

    def avatarStand(self, avatar, seatIndex):
        DistributedGameTableAI.avatarStand(self, avatar, seatIndex)
        self._joinedSeats.discard(seatIndex)
        self._rebuildSeatStatus()
        self.d_setTableState()

    def _rebuildSeatStatus(self):
        self._seatStatus = []
        for i in range(self._availableSeats):
            seat = self.seats[i]
            if seat is None:
                continue
            avId = seat.doId if seat not in (0, 1) else 0
            state = 2 if i in self._joinedSeats else 1
            self._seatStatus.append([avId, state])

    # ------------------------------------------------------------------
    # Client messages
    # ------------------------------------------------------------------

    def clientAction(self, action):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        seatIndex = self.getAvatarSeatIndex(avatar)
        if seatIndex is None:
            return

        actionCode = action[0] if action else -1

        if actionCode == BishopsHandGlobals.PLAYER_ACTIONS.JoinGame:
            self._playerJoin(avatar, seatIndex)

        elif actionCode == BishopsHandGlobals.PLAYER_ACTIONS.UnjoinGame:
            self._playerUnjoin(avatar, seatIndex)

        elif actionCode == BishopsHandGlobals.PLAYER_ACTIONS.RejoinGame:
            self._playerJoin(avatar, seatIndex)

        elif actionCode in (BishopsHandGlobals.PLAYER_ACTIONS.Resign,
                            BishopsHandGlobals.PLAYER_ACTIONS.Leave):
            self._playerLeave(avatar, seatIndex)

        elif actionCode == BishopsHandGlobals.PLAYER_ACTIONS.Continue:
            pass  # client practises locally; nothing to track server-side

    def receiveProgress(self, step, misses, hits, elapsed):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        seatIndex = self.getAvatarSeatIndex(avatar)
        if seatIndex is None:
            return

        percent = int((step / max(len(self._roundSequence), 1)) * 100)
        percent = min(percent, 100)

        # Update report for this seat
        updated = False
        for i, entry in enumerate(self._progressReport):
            if entry[0] == seatIndex:
                self._progressReport[i] = [seatIndex, percent]
                updated = True
                break
        if not updated:
            self._progressReport.append([seatIndex, percent])

        self.d_setProgressReport(self._progressReport)

        # If a player finishes, notify them
        if percent >= 100:
            action = {'action': BishopsHandGlobals.GAME_ACTIONS.NotifyOfWin, 'data': 0}
            self.sendUpdate('askForClientAction', [action, 0, 0])

    def leftGame(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        seatIndex = self.getAvatarSeatIndex(avatar)
        if seatIndex is not None:
            self._playerLeave(avatar, seatIndex)

    # ------------------------------------------------------------------
    # Internal game logic
    # ------------------------------------------------------------------

    def _playerJoin(self, avatar, seatIndex):
        if seatIndex in self._joinedSeats:
            return

        inv = self.air.inventoryManager.getInventory(avatar.doId)
        if not inv or inv.getGoldInPocket() < self.EntryFee:
            return

        inv.setGoldInPocket(inv.getGoldInPocket() - self.EntryFee)
        self._joinedSeats.add(seatIndex)
        self.b_setPendingStakes(self._pendingStakes + self.EntryFee)

        self._rebuildSeatStatus()
        self.d_setTableState()
        self._checkStartRound()

    def _playerUnjoin(self, avatar, seatIndex):
        if seatIndex not in self._joinedSeats:
            return

        self._joinedSeats.discard(seatIndex)
        inv = self.air.inventoryManager.getInventory(avatar.doId)
        if inv:
            inv.addGoldInPocket(self.EntryFee)

        self.b_setPendingStakes(max(0, self._pendingStakes - self.EntryFee))
        self._rebuildSeatStatus()
        self.d_setTableState()

    def _playerLeave(self, avatar, seatIndex):
        self._joinedSeats.discard(seatIndex)
        self.handleRequestExit(avatar)

    def _checkStartRound(self):
        if len(self._joinedSeats) < 1:
            return

        if self._tableState == 1:
            return  # already playing

        # Give a short window for others to join, then start
        taskMgr.remove(self.uniqueName('bh-start'))
        taskMgr.doMethodLater(BishopsHandGlobals.GameTimeDelay,
            self._startRoundTask, self.uniqueName('bh-start'), appendTask=True)

    def _startRoundTask(self, task=None):
        self._startRound()
        return Task.done

    def _startRound(self):
        self._tableState = 1
        self._progressReport = [[i, 0] for i in self._joinedSeats]
        self.b_setActiveStakes(self._pendingStakes)
        self.b_setRunningStakes(self._pendingStakes)
        self.b_setPendingStakes(0)

        self._rebuildSeatStatus()
        self.d_setTableState()

        # Generate a random sequence of target positions 0-4
        self._roundSequence = [random.randint(0, 4) for _ in range(self.SequenceLength)]
        delay = BishopsHandGlobals.RoundTimeDelay
        timestamp = globalClockDelta.getRealNetworkTime(bits=16)

        # Send round start to each joined seat
        for seatIndex in self._joinedSeats:
            seat = self.seats[seatIndex]
            if seat and seat not in (0, 1):
                self.sendUpdateToAvatarId(seat.doId, 'startRound',
                    [self._roundSequence, delay, timestamp])

        # Broadcast game timer
        self.d_setGameTimer(BishopsHandGlobals.RoundTimeLimit,
            globalClockDelta.getRealNetworkTime(bits=16))

        # Schedule round end
        totalTime = BishopsHandGlobals.RoundTimeLimit + BishopsHandGlobals.RoundTimeDelay
        taskMgr.doMethodLater(totalTime, self._endRoundTask,
            self.uniqueName('bh-round'), appendTask=True)

    def _endRoundTask(self, task=None):
        self._endRound()
        return Task.done

    def _endRound(self):
        self._tableState = 0
        self._rebuildSeatStatus()
        self.d_setTableState()

        # Pay out running stakes to whoever finished with the highest progress
        if not self._progressReport:
            self.b_setRunningStakes(0)
            self._joinedSeats.clear()
            return

        best = max(self._progressReport, key=lambda x: x[1])
        bestSeat = best[0]
        seat = self.seats[bestSeat]
        if seat and seat not in (0, 1):
            inv = self.air.inventoryManager.getInventory(seat.doId)
            if inv:
                inv.addGoldInPocket(self._runningStakes)

        action = [BishopsHandGlobals.GAME_ACTIONS.NotifyOfWin, 0]
        self.sendUpdate('askForClientAction', [action, 0, 0])
        self.b_setRunningStakes(0)
        self._joinedSeats.clear()
        self._progressReport = []