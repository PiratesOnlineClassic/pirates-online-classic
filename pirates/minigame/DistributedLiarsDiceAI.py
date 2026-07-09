import random

from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from panda3d.core import taskMgr
from pirates.minigame.DistributedDiceGameAI import DistributedDiceGameAI
from pirates.minigame import DiceGlobals


class DistributedLiarsDiceAI(DistributedDiceGameAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLiarsDiceAI')

    # How many seconds other players have to press "catch" after a cheat fires
    CatchWindow = 5

    def __init__(self, air):
        DistributedDiceGameAI.__init__(self, air)
        self._currentBetDice = 0
        self._currentBetValue = 0
        self._lastBetSeat = -1
        self._eliminatedSeats = set()
        self._activeCheat = {}  # seatIndex -> dieValue, expires via task

    def delete(self):
        taskMgr.remove(self.uniqueName('ld-turn'))
        taskMgr.remove(self.uniqueName('ld-catchexpire'))
        DistributedDiceGameAI.delete(self)

    # ------------------------------------------------------------------
    # Seat lifecycle
    # ------------------------------------------------------------------

    def avatarStand(self, avatar, seatIndex):
        self._eliminatedSeats.discard(seatIndex)
        self._activeCheat.pop(seatIndex, None)
        DistributedDiceGameAI.avatarStand(self, avatar, seatIndex)

    # ------------------------------------------------------------------
    # After all dice rolled, begin the betting phase
    # ------------------------------------------------------------------

    def _onAllRolled(self):
        self._currentBetDice = 0
        self._currentBetValue = 0
        self._lastBetSeat = -1

        firstSeat = self._getNextActiveSeat(-1)
        if firstSeat is None:
            return

        self._activeSeat = firstSeat
        name = self._getPlayerName(firstSeat)
        self.sendUpdate('currentTurn', [DiceGlobals.DSTATE_PLAY, firstSeat, name])

        if self.seats[firstSeat] == 1:
            taskMgr.doMethodLater(2.0, self._aiTakeTurn,
                self.uniqueName('ld-turn'), extraArgs=[firstSeat], appendTask=True)

    # ------------------------------------------------------------------
    # Seat helpers
    # ------------------------------------------------------------------

    def _getNextActiveSeat(self, fromSeat):
        for i in range(1, self._availableSeats + 1):
            idx = (fromSeat + i) % self._availableSeats
            if idx in self._eliminatedSeats:
                continue
            if self.seats[idx] is None:
                continue
            return idx
        return None

    def _getActiveSeatCount(self):
        count = 0
        for i in range(self._availableSeats):
            if i not in self._eliminatedSeats and self.seats[i] is not None:
                count += 1
        return count

    # ------------------------------------------------------------------
    # Client messages
    # ------------------------------------------------------------------

    def betUpdate(self, mySeat, betDice, betValue):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if self.getAvatarSeatIndex(avatar) != mySeat:
            return

        if mySeat != self._activeSeat:
            return

        if not self._isValidClaim(betDice, betValue):
            return

        self._currentBetDice = betDice
        self._currentBetValue = betValue
        self._lastBetSeat = mySeat
        self.sendUpdate('tableStatus', [betDice, betValue])
        self._advanceBettingTurn()

    def callBluff(self, mySeat, oldDice, oldValue):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if self.getAvatarSeatIndex(avatar) != mySeat:
            return

        if mySeat == self._lastBetSeat or self._lastBetSeat < 0:
            return

        self._resolveChallenge(challenger=mySeat, claimer=self._lastBetSeat,
            claimedDice=oldDice, claimedValue=oldValue)

    def cheatResult(self, seatIndex, dieValue, resultCode):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if self.getAvatarSeatIndex(avatar) != seatIndex:
            return

        self._activeCheat[seatIndex] = dieValue
        self.sendUpdate('incomingCheat', [seatIndex, self.CatchWindow, dieValue])
        taskMgr.doMethodLater(self.CatchWindow, self._cheatExpireTask,
            self.uniqueName('ld-catchexpire'), extraArgs=[seatIndex], appendTask=True)

    def catchCheater(self, mySeat):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if self.getAvatarSeatIndex(avatar) != mySeat:
            return

        # Find the most recent cheat from someone other than this player
        cheaterSeat = None
        for seatIndex in list(self._activeCheat.keys()):
            if seatIndex != mySeat:
                cheaterSeat = seatIndex
                break

        if cheaterSeat is None:
            return

        cheaterName = self._getPlayerName(cheaterSeat)
        self.sendUpdate('gotCaught', [cheaterSeat, cheaterName])
        self._activeCheat.pop(cheaterSeat, None)
        taskMgr.remove(self.uniqueName('ld-catchexpire'))

    # ------------------------------------------------------------------
    # Internal game logic
    # ------------------------------------------------------------------

    def _isValidClaim(self, numDice, dieValue):
        if not (1 <= dieValue <= 6):
            return False
        if self._currentBetDice == 0:
            return numDice >= 1
        if numDice > self._currentBetDice:
            return True
        if numDice == self._currentBetDice and dieValue > self._currentBetValue:
            return True
        return False

    def _countDiceWithValue(self, value):
        total = 0
        for seatIndex, dice in self._rolledDice.items():
            if seatIndex not in self._eliminatedSeats:
                for d in dice:
                    if d == value:
                        total += 1
        return total

    def _resolveChallenge(self, challenger, claimer, claimedDice, claimedValue):
        actualCount = self._countDiceWithValue(claimedValue)
        if actualCount >= claimedDice:
            # Claim was true - challenger loses
            loserSeat = challenger
        else:
            # Bluff called correctly - claimer loses
            loserSeat = claimer

        loserName = self._getPlayerName(loserSeat)
        self.sendUpdate('displayChallenge', [claimedDice, claimedValue,
            claimer, challenger, loserName])
        self._eliminateSeat(loserSeat)

        if self._getActiveSeatCount() <= 1:
            self._resolveWinner()
        else:
            taskMgr.doMethodLater(2.5, self._beginNewRound,
                self.uniqueName('ld-turn'), appendTask=True)

    def _eliminateSeat(self, seatIndex):
        self._eliminatedSeats.add(seatIndex)

    def _resolveWinner(self):
        for seatIndex in range(self._availableSeats):
            if seatIndex in self._eliminatedSeats:
                continue
            seat = self.seats[seatIndex]
            if seat and seat not in (0, 1):
                self._payWinner(seat.doId)
                self._eliminatedSeats.clear()
                return

        # AI wins; just reset
        self._eliminatedSeats.clear()
        self._resetRound()

    def _beginNewRound(self, task=None):
        self.sendUpdate('newRound', [])
        self._currentBetDice = 0
        self._currentBetValue = 0
        self._lastBetSeat = -1
        self._rolledDice = {}

        firstSeat = self._getNextActiveSeat(-1)
        if firstSeat is not None:
            self._activeSeat = firstSeat
            self._requestRoll(firstSeat)

        return Task.done

    def _advanceBettingTurn(self):
        nextSeat = self._getNextActiveSeat(self._activeSeat)
        if nextSeat is None:
            return

        self._activeSeat = nextSeat
        name = self._getPlayerName(nextSeat)
        self.sendUpdate('currentTurn', [DiceGlobals.DSTATE_PLAY, nextSeat, name])

        if self.seats[nextSeat] == 1:
            taskMgr.doMethodLater(2.0, self._aiTakeTurn,
                self.uniqueName('ld-turn'), extraArgs=[nextSeat], appendTask=True)

    def _cheatExpireTask(self, seatIndex, task=None):
        self._activeCheat.pop(seatIndex, None)
        return Task.done

    # ------------------------------------------------------------------
    # AI decision making
    # ------------------------------------------------------------------

    def _aiTakeTurn(self, seatIndex, task=None):
        if self._activeSeat != seatIndex:
            return Task.done

        # Decide whether to challenge or make a new claim
        if self._currentBetDice > 0 and self._shouldAIChallenge(seatIndex):
            self._resolveChallenge(challenger=seatIndex, claimer=self._lastBetSeat,
                claimedDice=self._currentBetDice, claimedValue=self._currentBetValue)
        else:
            self._aiMakeClaim(seatIndex)

        return Task.done

    def _shouldAIChallenge(self, seatIndex):
        activePlayers = self._getActiveSeatCount()
        totalDice = activePlayers * self.NumDice
        expectedCount = totalDice / 6.0
        # Challenge if claimed count is more than double the expected frequency
        if self._currentBetDice > expectedCount * 2.0:
            return random.random() < 0.7
        if self._currentBetDice > expectedCount * 1.5:
            return random.random() < 0.3
        return False

    def _aiMakeClaim(self, seatIndex):
        if self._currentBetDice == 0:
            # First claim: start conservatively
            newDice = max(1, self._getActiveSeatCount())
            newValue = random.randint(1, 6)
        elif random.random() < 0.5:
            # Raise the count
            newDice = self._currentBetDice + 1
            newValue = random.randint(1, 6)
        else:
            # Raise the value at same count
            newValue = self._currentBetValue + 1
            newDice = self._currentBetDice
            if newValue > 6:
                newValue = 1
                newDice += 1

        self._currentBetDice = newDice
        self._currentBetValue = newValue
        self._lastBetSeat = seatIndex
        self.sendUpdate('tableStatus', [newDice, newValue])
        self._advanceBettingTurn()
