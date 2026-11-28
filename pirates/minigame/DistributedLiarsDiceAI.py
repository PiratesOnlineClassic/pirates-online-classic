import random

from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.task.TaskManagerGlobal import *
from pirates.minigame.DistributedDiceGameAI import DistributedDiceGameAI
from pirates.minigame import DiceGlobals


class DistributedLiarsDiceAI(DistributedDiceGameAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLiarsDiceAI')

    # how long the other pirates have to catch a cheater
    CatchWindow = 5
    # the cheatResult codes, see DistributedLiarsDice.tryToCheat
    CheatClean = 0
    CheatRough = 2
    CheatBotched = 4
    ClaimTimeout = 45.0
    ChallengeDelay = 8.0
    AITurnDelay = (2.0, 3.5)

    def __init__(self, air):
        DistributedDiceGameAI.__init__(self, air)
        self._currentBetDice = 0
        self._currentBetValue = 0
        self._lastBetSeat = -1
        self._eliminatedSeats = set()
        self._activeCheat = {}  # seatIndex -> dieValue, expires via task
        self._bettingActive = False

    def delete(self):
        taskMgr.remove(self.uniqueName('ld-turn'))
        taskMgr.remove(self.uniqueName('ld-catchexpire'))
        DistributedDiceGameAI.delete(self)

    def isSeatInGame(self, seatIndex):
        return seatIndex in self._readySeats and seatIndex not in self._eliminatedSeats

    def handleSeatLeft(self, seatIndex):
        self._activeCheat.pop(seatIndex, None)
        if not self._bettingActive:
            self._eliminatedSeats.discard(seatIndex)
            DistributedDiceGameAI.handleSeatLeft(self, seatIndex)
            return

        if not self.getPlayerSeats():
            self._resetRound()
            return

        wasActive = seatIndex == self._activeSeat
        self._eliminatedSeats.add(seatIndex)
        if self._lastBetSeat == seatIndex:
            self._lastBetSeat = -1

        if self._getActiveSeatCount() <= 1:
            self._resolveWinner()
        elif wasActive:
            self._advanceBettingTurn()

    def _resetRound(self):
        taskMgr.remove(self.uniqueName('ld-turn'))
        taskMgr.remove(self.uniqueName('ld-catchexpire'))
        self._eliminatedSeats = set()
        self._activeCheat = {}
        self._bettingActive = False
        self._currentBetDice = 0
        self._currentBetValue = 0
        self._lastBetSeat = -1
        DistributedDiceGameAI._resetRound(self)

    def _onAllRolled(self):
        self._currentBetDice = 0
        self._currentBetValue = 0
        self._lastBetSeat = -1
        self._bettingActive = True
        self.sendUpdate('tableStatus', [1, 1])

        firstSeat = self._getNextActiveSeat(-1)
        if firstSeat is None:
            self._resetRound()
            return

        self._startBettingTurn(firstSeat)

    def _startBettingTurn(self, seatIndex):
        taskMgr.remove(self.uniqueName('ld-turn'))
        self._activeSeat = seatIndex
        self.d_currentTurn(DiceGlobals.DSTATE_PLAY, seatIndex)
        self.d_yourTurn(seatIndex)

        if self.isAISeat(seatIndex):
            taskMgr.doMethodLater(random.uniform(*self.AITurnDelay), self._aiTakeTurn,
                self.uniqueName('ld-turn'), extraArgs=[seatIndex], appendTask=True)
        else:
            taskMgr.doMethodLater(self.ClaimTimeout, self._claimTimeoutTask,
                self.uniqueName('ld-turn'), extraArgs=[seatIndex], appendTask=True)

    def _claimTimeoutTask(self, seatIndex, task=None):
        # the pirate dawdled, make the smallest claim possible for them
        if self._activeSeat == seatIndex:
            self._makeClaim(seatIndex, *self._getMinimumClaim())

        return Task.done

    def _getNextActiveSeat(self, fromSeat):
        for i in range(1, self._availableSeats + 1):
            idx = (fromSeat + i) % self._availableSeats
            if self.seats[idx] is not None and self.isSeatInGame(idx):
                return idx

        return None

    def _getActiveSeatCount(self):
        count = 0
        for i in range(self._availableSeats):
            if self.seats[i] is not None and self.isSeatInGame(i):
                count += 1

        return count

    def _getSenderSeat(self, mySeat):
        seatIndex = self.getSenderSeatIndex()
        if seatIndex is None or seatIndex != mySeat:
            return None

        return seatIndex

    def betUpdate(self, mySeat, betDice, betValue):
        seatIndex = self._getSenderSeat(mySeat)
        if seatIndex is None or not self._bettingActive or seatIndex != self._activeSeat:
            return

        if not self._isValidClaim(betDice, betValue):
            return

        self._makeClaim(seatIndex, betDice, betValue)

    def callBluff(self, mySeat, oldDice, oldValue):
        seatIndex = self._getSenderSeat(mySeat)
        if seatIndex is None or not self._bettingActive or seatIndex != self._activeSeat:
            return

        if seatIndex == self._lastBetSeat or self._lastBetSeat < 0:
            return

        # always judge the claim the server knows about
        self._resolveChallenge(challenger=seatIndex, claimer=self._lastBetSeat,
            claimedDice=self._currentBetDice, claimedValue=self._currentBetValue)

    def cheatResult(self, seatIndex, dieValue, resultCode):
        if self._getSenderSeat(seatIndex) is None or not self._roundActive:
            return

        if resultCode == self.CheatBotched:
            # the whole table saw that one
            self._catchCheater(seatIndex)
            return

        if resultCode != self.CheatRough:
            return

        self._activeCheat[seatIndex] = dieValue
        # every other pirate gets a moment to catch the cheater at it
        for otherSeat in self.getPlayerSeats():
            if otherSeat != seatIndex and self.isSeatInGame(otherSeat):
                self.sendUpdate('incomingCheat', [otherSeat, self.CatchWindow, dieValue])

        taskMgr.remove(self.uniqueName('ld-catchexpire'))
        taskMgr.doMethodLater(self.CatchWindow + 1, self._cheatExpireTask,
            self.uniqueName('ld-catchexpire'), extraArgs=[seatIndex], appendTask=True)

    def catchCheater(self, mySeat):
        seatIndex = self._getSenderSeat(mySeat)
        if seatIndex is None:
            return

        cheaterSeat = None
        for cheatSeat in list(self._activeCheat.keys()):
            if cheatSeat != seatIndex:
                cheaterSeat = cheatSeat
                break

        if cheaterSeat is None:
            return

        self._catchCheater(cheaterSeat)

    def _catchCheater(self, cheaterSeat):
        self._activeCheat.pop(cheaterSeat, None)
        taskMgr.remove(self.uniqueName('ld-catchexpire'))
        self.sendUpdate('gotCaught', [cheaterSeat, self._getPlayerName(cheaterSeat)])

        # cheaters are thrown out of the game, their ante stays in the pot
        wasActive = cheaterSeat == self._activeSeat
        self._eliminateSeat(cheaterSeat)
        if self._lastBetSeat == cheaterSeat:
            self._lastBetSeat = -1

        if not self._bettingActive:
            if wasActive:
                taskMgr.remove(self.uniqueName('dice-roll'))
                self._advanceRollPhase(cheaterSeat)
            return

        if self._getActiveSeatCount() <= 1:
            self._resolveWinner()
        elif wasActive:
            self._advanceBettingTurn()

    def _getMaxDice(self):
        return self.NumDice * self._getActiveSeatCount()

    def _isValidClaim(self, numDice, dieValue):
        # mirrors DistributedLiarsDice.makeClaim on the client, which starts
        # every round with a claim of one 1
        if not (1 <= dieValue <= 6) or not (1 <= numDice <= self.NumDice * self._availableSeats):
            return False

        oldDice = max(1, self._currentBetDice)
        oldValue = max(1, self._currentBetValue)
        if numDice < oldDice:
            return False

        return numDice > oldDice or dieValue > oldValue

    def _getMinimumClaim(self):
        if self._currentBetDice == 0:
            return (1, 2)
        elif self._currentBetValue < 6:
            return (self._currentBetDice, self._currentBetValue + 1)

        return (self._currentBetDice + 1, 1)

    def _makeClaim(self, seatIndex, numDice, dieValue):
        taskMgr.remove(self.uniqueName('ld-turn'))
        self._currentBetDice = numDice
        self._currentBetValue = dieValue
        self._lastBetSeat = seatIndex
        self.sendUpdate('tableStatus', [numDice, dieValue])
        self._advanceBettingTurn()

    def _countDiceWithValue(self, value):
        total = 0
        for seatIndex, dice in self._rolledDice.items():
            if self.isSeatInGame(seatIndex):
                total += list(dice).count(value)

        return total

    def _resolveChallenge(self, challenger, claimer, claimedDice, claimedValue):
        taskMgr.remove(self.uniqueName('ld-turn'))
        actualCount = self._countDiceWithValue(claimedValue)
        if actualCount >= claimedDice:
            loserSeat = challenger
        else:
            loserSeat = claimer

        loserName = self._getPlayerName(loserSeat)
        self.sendUpdate('displayChallenge', [claimedDice, claimedValue,
            claimer, challenger, loserName])
        self._eliminateSeat(loserSeat)
        self._bettingActive = False
        self._activeSeat = -1

        if self._getActiveSeatCount() <= 1:
            self._resolveWinner()
        else:
            taskMgr.doMethodLater(self.ChallengeDelay, self._beginNewRound,
                self.uniqueName('ld-turn'), appendTask=True)

    def _eliminateSeat(self, seatIndex):
        self._eliminatedSeats.add(seatIndex)

    def _resolveWinner(self):
        winnerSeat = self._getNextActiveSeat(-1)
        if winnerSeat is None:
            # nobody left standing, the house keeps the pot
            self._resetRound()
            return

        self._payWinner(winnerSeat)

    def _beginNewRound(self, task=None):
        self.sendUpdate('newRound', [])
        self._currentBetDice = 0
        self._currentBetValue = 0
        self._lastBetSeat = -1
        self._bettingActive = False
        self._rolledDice = {}

        firstSeat = self._getNextActiveSeat(-1)
        if firstSeat is not None:
            self._activeSeat = firstSeat
            self._requestRoll(firstSeat)
        else:
            self._resetRound()

        return Task.done

    def _advanceBettingTurn(self):
        nextSeat = self._getNextActiveSeat(self._activeSeat)
        if nextSeat is None:
            self._resetRound()
            return

        self._startBettingTurn(nextSeat)

    def _cheatExpireTask(self, seatIndex, task=None):
        self._activeCheat.pop(seatIndex, None)
        return Task.done

    def _aiTakeTurn(self, seatIndex, task=None):
        if self._activeSeat != seatIndex or not self._bettingActive:
            return Task.done

        if self._lastBetSeat >= 0 and self._lastBetSeat != seatIndex and self._shouldAIChallenge(seatIndex):
            self._resolveChallenge(challenger=seatIndex, claimer=self._lastBetSeat,
                claimedDice=self._currentBetDice, claimedValue=self._currentBetValue)
        else:
            self._aiMakeClaim(seatIndex)

        return Task.done

    def _getExpectedCount(self, seatIndex, value):
        # the AI knows it's own dice and guesses at everyone else's
        ownDice = self._rolledDice.get(seatIndex, [])
        otherDice = self.NumDice * (self._getActiveSeatCount() - 1)
        return list(ownDice).count(value) + otherDice / 6.0

    def _shouldAIChallenge(self, seatIndex):
        expectedCount = self._getExpectedCount(seatIndex, self._currentBetValue)
        if self._currentBetDice > self._getMaxDice():
            return True
        if self._currentBetDice > expectedCount + 2:
            return random.random() < 0.8
        if self._currentBetDice > expectedCount + 1:
            return random.random() < 0.4
        return False

    def _aiMakeClaim(self, seatIndex):
        ownDice = list(self._rolledDice.get(seatIndex, []))
        # claim on the value we hold the most of
        favorite = max(range(1, 7), key=lambda value: (ownDice.count(value), random.random()))
        expected = int(self._getExpectedCount(seatIndex, favorite))

        newDice, newValue = self._getMinimumClaim()
        if self._isValidClaim(max(newDice, 1), favorite):
            newDice, newValue = max(newDice, 1), favorite
        elif self._isValidClaim(newDice + 1, favorite) and newDice + 1 <= expected + 1:
            newDice, newValue = newDice + 1, favorite

        if newDice > expected + 1 and self._lastBetSeat >= 0 and self._lastBetSeat != seatIndex:
            # nothing believable left to claim, call the bluff instead
            self._resolveChallenge(challenger=seatIndex, claimer=self._lastBetSeat,
                claimedDice=self._currentBetDice, claimedValue=self._currentBetValue)
            return

        self._makeClaim(seatIndex, newDice, newValue)
