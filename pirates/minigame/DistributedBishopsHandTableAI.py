import random

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
from direct.task import Task
from direct.task.TaskManagerGlobal import *
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from pirates.minigame import BishopsHandGlobals


class DistributedBishopsHandTableAI(DistributedGameTableAI):
    """
    Bishop's Hand, the knife game.  Pirates pay to join a game, then play
    rounds where they must stab the knife between their fingers following
    a sequence.  Anyone who doesn't finish the sequence in time is out, and
    when everyone finishes the slowest is out.  The last pirate standing
    may leave with the stakes or keep playing for more.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBishopsHandTableAI')

    EntryFee = 2  # gold to join a game, the client's join button says so
    SequenceLength = 30  # steps in a round sequence
    MissPenalty = 1.0  # seconds added to a pirate's time for each miss

    # seat states sent in setTableState
    SeatEmpty = -1
    SeatUnjoined = 0
    SeatJoined = 1
    SeatPlaying = 2

    # table states
    TableIdle = 0
    TablePlaying = 1

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air, numberAI=0)
        self._parentingRules = ('', '')
        self._tableState = self.TableIdle
        self._seatStates = [self.SeatEmpty] * self._availableSeats
        self._pendingStakes = 0
        self._activeStakes = 0
        self._runningStakes = 0
        self._gameTimer = 0
        self._progress = {}            # seatIndex -> [step, misses, hits, elapsed]
        self._finished = {}            # seatIndex -> score
        self._roundSequence = []
        self._winnerSeat = None

    def delete(self):
        taskMgr.remove(self.uniqueName('bh-start'))
        taskMgr.remove(self.uniqueName('bh-round'))
        taskMgr.remove(self.uniqueName('bh-continue'))
        DistributedGameTableAI.delete(self)

    # ------------------------------------------------------------------
    # DC field accessors
    # ------------------------------------------------------------------

    def setParentingRules(self, rule1, rule2):
        self._parentingRules = (rule1, rule2)

    def getParentingRules(self):
        return list(self._parentingRules)

    def setTableState(self, tableState, seatStatus):
        self._tableState = tableState
        self._seatStates = [state for avId, state in seatStatus]

    def d_setTableState(self):
        self.sendUpdate('setTableState', self.getTableState())

    def getTableState(self):
        seatStatus = []
        for seatIndex in range(self._availableSeats):
            avId = self.seats[seatIndex].doId if self.isPlayerSeat(seatIndex) else 0
            seatStatus.append([avId, self._seatStates[seatIndex]])

        return [self._tableState, seatStatus]

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

    def d_setProgressReport(self):
        report = []
        for seatIndex, progress in sorted(self._progress.items()):
            report.append([seatIndex, self._getPercent(progress[0])])

        self.sendUpdate('setProgressReport', [report])

    def setGameTimer(self, time, timestamp):
        self._gameTimer = time

    def d_setGameTimer(self, time):
        self.setGameTimer(time, 0)
        self.sendUpdate('setGameTimer', [time, globalClockDelta.getRealNetworkTime(bits=16)])

    def getGameTimer(self):
        return [self._gameTimer, globalClockDelta.getRealNetworkTime(bits=16)]

    def d_askForClientAction(self, seatIndex, action, data, delay):
        # askForClientAction is meant for a single pirate's game gui
        if self.isPlayerSeat(seatIndex):
            self.sendUpdateToAvatarId(self.seats[seatIndex].doId, 'askForClientAction',
                [[action, data], int(delay), globalClockDelta.getRealNetworkTime(bits=16)])

    def d_startRound(self, seatIndex, delay):
        if self.isPlayerSeat(seatIndex):
            self.sendUpdateToAvatarId(self.seats[seatIndex].doId, 'startRound',
                [self._roundSequence, delay, globalClockDelta.getRealNetworkTime(bits=16)])

    def d_leftGame(self, seatIndex):
        if self.isPlayerSeat(seatIndex):
            self.sendUpdateToAvatarId(self.seats[seatIndex].doId, 'leftGame', [])

    def _setSeatState(self, seatIndex, state):
        self._seatStates[seatIndex] = state

    def _getSeatsInState(self, state):
        return [seatIndex for seatIndex in range(self._availableSeats)
                if self.isPlayerSeat(seatIndex) and self._seatStates[seatIndex] == state]

    # ------------------------------------------------------------------
    # Seat lifecycle
    # ------------------------------------------------------------------

    def announceGenerate(self):
        DistributedGameTableAI.announceGenerate(self)
        self.d_setTableState()

    def avatarSit(self, avatar, seatIndex):
        DistributedGameTableAI.avatarSit(self, avatar, seatIndex)
        self._setSeatState(seatIndex, self.SeatUnjoined)
        self.d_setTableState()

    def avatarStand(self, avatar, seatIndex):
        state = self._seatStates[seatIndex]
        DistributedGameTableAI.avatarStand(self, avatar, seatIndex)
        if state == self.SeatJoined and self._tableState == self.TableIdle:
            # never got to play, their entry fee is returned
            self.giveGoldToAvatar(avatar, self.EntryFee)
            self.b_setPendingStakes(max(0, self._pendingStakes - self.EntryFee))

        self._setSeatState(seatIndex, self.SeatEmpty)
        self._progress.pop(seatIndex, None)
        self._finished.pop(seatIndex, None)
        if self._winnerSeat == seatIndex:
            # walking away from the table counts as leaving with the winnings
            self.giveGoldToAvatar(avatar, self._runningStakes)
            self._winnerLeaves(seatIndex, paid=False)

        self.d_setTableState()
        self._checkRoundOver()
        if not self._getSeatsInState(self.SeatJoined):
            taskMgr.remove(self.uniqueName('bh-start'))

    def giveGoldToAvatar(self, avatar, amount):
        inv = self.air.inventoryManager.getInventory(avatar.doId)
        if inv and amount > 0:
            inv.setGoldInPocket(inv.getGoldInPocket() + amount)

    # ------------------------------------------------------------------
    # Client messages
    # ------------------------------------------------------------------

    def clientAction(self, action):
        seatIndex = self.getSenderSeatIndex()
        if seatIndex is None:
            return

        actionCode = action[0] if action else -1

        if actionCode in (BishopsHandGlobals.PLAYER_ACTIONS.JoinGame,
                          BishopsHandGlobals.PLAYER_ACTIONS.RejoinGame):
            self._playerJoin(seatIndex)

        elif actionCode == BishopsHandGlobals.PLAYER_ACTIONS.UnjoinGame:
            self._playerUnjoin(seatIndex)

        elif actionCode == BishopsHandGlobals.PLAYER_ACTIONS.Resign:
            self._playerResign(seatIndex)

        elif actionCode == BishopsHandGlobals.PLAYER_ACTIONS.Leave:
            if seatIndex == self._winnerSeat:
                self._winnerLeaves(seatIndex)

        elif actionCode == BishopsHandGlobals.PLAYER_ACTIONS.Continue:
            if seatIndex == self._winnerSeat:
                # the winner plays on, the stakes ride on the next game
                taskMgr.remove(self.uniqueName('bh-continue'))
                self._winnerSeat = None
                self._setSeatState(seatIndex, self.SeatJoined)
                self.d_setTableState()
                self._checkStartRound()
            # otherwise the pirate is just practicing on it's own

    def receiveProgress(self, step, misses, hits, elapsed):
        seatIndex = self.getSenderSeatIndex()
        if seatIndex is None or seatIndex not in self._progress or seatIndex in self._finished:
            return

        if self._tableState != self.TablePlaying:
            return

        step = min(step, len(self._roundSequence))
        self._progress[seatIndex] = [step, misses, hits, elapsed]
        self.d_setProgressReport()

        if step >= len(self._roundSequence):
            self._finished[seatIndex] = elapsed + misses * self.MissPenalty
            self._checkRoundOver()

    def leftGame(self):
        seatIndex = self.getSenderSeatIndex()
        if seatIndex is not None:
            self._playerResign(seatIndex)

    # ------------------------------------------------------------------
    # Internal game logic
    # ------------------------------------------------------------------

    def _playerJoin(self, seatIndex):
        if self._seatStates[seatIndex] != self.SeatUnjoined:
            return

        if self.takeSeatGold(seatIndex, self.EntryFee) < self.EntryFee:
            return

        self._setSeatState(seatIndex, self.SeatJoined)
        self.b_setPendingStakes(self._pendingStakes + self.EntryFee)
        self.d_setTableState()
        self._checkStartRound()

    def _playerUnjoin(self, seatIndex):
        if self._seatStates[seatIndex] != self.SeatJoined or seatIndex == self._winnerSeat:
            return

        self._setSeatState(seatIndex, self.SeatUnjoined)
        self.giveSeatGold(seatIndex, self.EntryFee)
        self.b_setPendingStakes(max(0, self._pendingStakes - self.EntryFee))
        self.d_setTableState()

    def _playerResign(self, seatIndex):
        if self._seatStates[seatIndex] != self.SeatPlaying:
            return

        self._setSeatState(seatIndex, self.SeatUnjoined)
        self._progress.pop(seatIndex, None)
        self._finished.pop(seatIndex, None)
        self.d_leftGame(seatIndex)
        self.d_setTableState()
        self._checkRoundOver()

    def _checkStartRound(self):
        if self._tableState == self.TablePlaying or self._winnerSeat is not None:
            return

        if not self._getSeatsInState(self.SeatJoined) and not self._getSeatsInState(self.SeatPlaying):
            return

        # Give a short window for others to join, then start
        taskMgr.remove(self.uniqueName('bh-start'))
        taskMgr.doMethodLater(BishopsHandGlobals.GameTimeDelay,
            self._startRoundTask, self.uniqueName('bh-start'), appendTask=True)

    def _startRoundTask(self, task=None):
        self._startRound()
        return Task.done

    def _startRound(self):
        # pirates that joined since the last round are dealt in now
        for seatIndex in self._getSeatsInState(self.SeatJoined):
            self._setSeatState(seatIndex, self.SeatPlaying)

        playing = self._getSeatsInState(self.SeatPlaying)
        if not playing:
            return

        if self._pendingStakes:
            self.b_setActiveStakes(self._activeStakes + self._pendingStakes)
            self.b_setRunningStakes(self._runningStakes + self._pendingStakes)
            self.b_setPendingStakes(0)

        self._tableState = self.TablePlaying
        self._progress = dict((seatIndex, [0, 0, 0, 0]) for seatIndex in playing)
        self._finished = {}
        self.d_setTableState()
        self.d_setProgressReport()

        # Generate a random sequence of target positions 0-4
        self._roundSequence = [random.randint(0, 4) for _ in range(self.SequenceLength)]
        delay = BishopsHandGlobals.RoundTimeDelay
        for seatIndex in playing:
            self.d_startRound(seatIndex, delay)

        self.d_setGameTimer(BishopsHandGlobals.RoundTimeLimit + delay)

        # Schedule round end
        taskMgr.remove(self.uniqueName('bh-round'))
        taskMgr.doMethodLater(BishopsHandGlobals.RoundTimeLimit + delay,
            self._endRoundTask, self.uniqueName('bh-round'), appendTask=True)

    def _checkRoundOver(self):
        if self._tableState != self.TablePlaying:
            return

        playing = self._getSeatsInState(self.SeatPlaying)
        if not playing:
            self._endRound()
            return

        for seatIndex in playing:
            if seatIndex not in self._finished:
                return

        self._endRound()

    def _endRoundTask(self, task=None):
        self._endRound()
        return Task.done

    def _endRound(self):
        taskMgr.remove(self.uniqueName('bh-round'))
        self._tableState = self.TableIdle
        self.d_setGameTimer(0)

        playing = self._getSeatsInState(self.SeatPlaying)
        finishers = sorted([seatIndex for seatIndex in playing if seatIndex in self._finished],
                           key=lambda seatIndex: self._finished[seatIndex])
        survivors = list(finishers)
        if len(survivors) > 1:
            # everyone made it, the slowest knife is out
            survivors = survivors[:-1]

        for seatIndex in playing:
            if seatIndex in survivors:
                continue

            self._setSeatState(seatIndex, self.SeatUnjoined)
            self.d_askForClientAction(seatIndex, BishopsHandGlobals.GAME_ACTIONS.NotifyOfLoss, 0, 0)
            self.d_askForClientAction(seatIndex, BishopsHandGlobals.GAME_ACTIONS.AskForContinue,
                BishopsHandGlobals.CONTINUE_OPTIONS.Rejoin, BishopsHandGlobals.RoundContinueWait)

        self._progress = {}
        self._finished = {}

        if not survivors:
            # nobody survived, the house keeps the stakes
            self.b_setActiveStakes(0)
            self.b_setRunningStakes(0)
        elif len(survivors) == 1:
            self._winnerSeat = survivors[0]
            self.d_askForClientAction(self._winnerSeat, BishopsHandGlobals.GAME_ACTIONS.NotifyOfWin, 1, 0)
            self.d_askForClientAction(self._winnerSeat, BishopsHandGlobals.GAME_ACTIONS.AskForContinue,
                BishopsHandGlobals.CONTINUE_OPTIONS.Leave, BishopsHandGlobals.RoundContinueWait)
            taskMgr.doMethodLater(BishopsHandGlobals.RoundContinueWait, self._winnerTimeoutTask,
                self.uniqueName('bh-continue'), appendTask=True)
        else:
            for seatIndex in survivors:
                self.d_askForClientAction(seatIndex, BishopsHandGlobals.GAME_ACTIONS.AskForContinue,
                    BishopsHandGlobals.CONTINUE_OPTIONS.Resign, BishopsHandGlobals.RoundTimeDelay)

        self.d_setTableState()
        self._checkStartRound()

    def _winnerTimeoutTask(self, task=None):
        # no answer from the winner, they take their winnings
        if self._winnerSeat is not None:
            self._winnerLeaves(self._winnerSeat)

        return Task.done

    def _winnerLeaves(self, seatIndex, paid=True):
        taskMgr.remove(self.uniqueName('bh-continue'))
        if paid:
            self.giveSeatGold(seatIndex, self._runningStakes)
            self._setSeatState(seatIndex, self.SeatUnjoined)
            self.d_leftGame(seatIndex)

        self._winnerSeat = None
        self.b_setActiveStakes(0)
        self.b_setRunningStakes(0)
        self.d_setTableState()
        self._checkStartRound()

    def _getPercent(self, step):
        if not self._roundSequence:
            return 0

        return min(100, int(step * 100 / len(self._roundSequence)))
