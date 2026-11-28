import random

from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.task.TaskManagerGlobal import *
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from pirates.minigame import DiceGlobals
from pirates.piratesbase import PLocalizer


class DistributedDiceGameAI(DistributedGameTableAI):
    """
    Base dice table.  Every pirate pays the ante and readies up, then each
    seat takes it's turn rolling (the client rolls the dice with it's physics
    and reports the faces).  The plain dice game pays the pot to the highest
    roll; sub-classes replace _onAllRolled with their own rules.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDiceGameAI')

    NumDice = 5
    Ante = 10
    RollTimeout = 30.0
    AIRollDelay = (1.5, 3.0)
    AIName = 'Pirate'

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air)
        self._readySeats = set()
        self._rolledDice = {}   # seatIndex -> [die values]
        self._activeSeat = -1
        self._roundActive = False
        self._pots = {}         # seatIndex -> gold contributed

    def delete(self):
        taskMgr.remove(self.uniqueName('dice-roll'))
        DistributedGameTableAI.delete(self)

    # ------------------------------------------------------------------
    # DC senders
    # ------------------------------------------------------------------

    def d_currentTurn(self, state, seatIndex):
        self.sendUpdate('currentTurn', [state, seatIndex, self._getPlayerName(seatIndex)])

    def d_yourTurn(self, seatIndex):
        self.sendUpdate('yourTurn', [seatIndex])

    def d_rollResults(self, seatIndex, dice):
        self.sendUpdate('rollResults', [seatIndex, dice])

    # ------------------------------------------------------------------
    # Seat lifecycle hooks
    # ------------------------------------------------------------------

    def avatarStand(self, avatar, seatIndex):
        DistributedGameTableAI.avatarStand(self, avatar, seatIndex)
        self._readySeats.discard(seatIndex)
        self._rolledDice.pop(seatIndex, None)
        # an ante already paid stays in the pot
        self.handleSeatLeft(seatIndex)

    def handleSeatLeft(self, seatIndex):
        if not self._roundActive:
            self._checkAllReady()
            return

        if not self.getPlayerSeats():
            self._resetRound()
            return

        if seatIndex == self._activeSeat:
            taskMgr.remove(self.uniqueName('dice-roll'))
            self._advanceRollPhase(seatIndex)

    # ------------------------------------------------------------------
    # Ready / round start
    # ------------------------------------------------------------------

    def playerIsReady(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        seatIndex = self.getAvatarSeatIndex(avatar)
        if seatIndex is None or self._roundActive or seatIndex in self._readySeats:
            return

        if self.takeSeatGold(seatIndex, self.Ante) < self.Ante:
            self.notify.warning('Avatar %d readied without enough gold for the ante!' % avatar.doId)
            return

        self._pots[seatIndex] = self._pots.get(seatIndex, 0) + self.Ante
        self._readySeats.add(seatIndex)
        self._checkAllReady()

    def _getHumanSeats(self):
        return self.getPlayerSeats()

    def _checkAllReady(self):
        if self._roundActive:
            return

        humanSeats = self._getHumanSeats()
        if not humanSeats:
            return

        if not all(s in self._readySeats for s in humanSeats):
            return

        # AI players are always ready
        for seatIndex in self.getAIPlayers():
            self._readySeats.add(seatIndex)

        if len(self._readySeats) < 2:
            # nobody to play against yet
            return

        self.sendUpdate('newRound', [])
        self._startRollPhase()

    def _getOccupiedSeats(self):
        return [seatIndex for seatIndex in self.getOccupiedSeats() if self.isSeatInGame(seatIndex)]

    def isSeatInGame(self, seatIndex):
        return seatIndex in self._readySeats

    def _startRollPhase(self):
        self._roundActive = True
        self._rolledDice = {}
        occupied = self._getOccupiedSeats()
        if not occupied:
            return

        self._activeSeat = occupied[0]
        self._requestRoll(self._activeSeat)

    def _getPlayerName(self, seatIndex):
        if self.isAISeat(seatIndex):
            return self.AIName

        return self.getSeatName(seatIndex)

    def _requestRoll(self, seatIndex):
        taskMgr.remove(self.uniqueName('dice-roll'))
        self.d_currentTurn(DiceGlobals.DSTATE_DOROLL, seatIndex)
        self.d_yourTurn(seatIndex)

        if self.isAISeat(seatIndex):
            taskMgr.doMethodLater(random.uniform(*self.AIRollDelay), self._aiRollTask,
                self.uniqueName('dice-roll'), extraArgs=[seatIndex], appendTask=True)
        else:
            # the server rolls for pirates that take too long
            taskMgr.doMethodLater(self.RollTimeout, self._aiRollTask,
                self.uniqueName('dice-roll'), extraArgs=[seatIndex], appendTask=True)

    def _aiRollTask(self, seatIndex, task=None):
        self.aiSpeak(seatIndex, PLocalizer.DiceText_Roll_Chat, 0.5)
        dice = [random.randint(1, 6) for _ in range(self.NumDice)]
        self._receiveDiceRoll(seatIndex, dice)
        return Task.done

    # ------------------------------------------------------------------
    # Client messages
    # ------------------------------------------------------------------

    def _isValidDice(self, dice):
        if len(dice) != self.NumDice:
            return False

        for value in dice:
            if not 1 <= value <= 6:
                return False

        return True

    def playerHasRolled(self, seatIndex, dice):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if self.getAvatarSeatIndex(avatar) != seatIndex or seatIndex != self._activeSeat or \
                seatIndex in self._rolledDice:
            return

        if not self._isValidDice(dice):
            self.air.logPotentialHacker(
                message='Received invalid dice roll',
                targetAvId=avatar.doId,
                dice=list(dice))

            return

        taskMgr.remove(self.uniqueName('dice-roll'))
        self._receiveDiceRoll(seatIndex, dice)

    def sendChat(self, chatType, avId):
        # The client shows it's own chatter when the pirate fiddles with the
        # dice, the AI pirates at the table chime in now and then.
        if chatType == DiceGlobals.CHAT_ROLL:
            phrases = PLocalizer.DiceText_Roll_Chat
        elif chatType == DiceGlobals.CHAT_DICEUP:
            phrases = PLocalizer.DiceText_DiceUp_Chat
        elif chatType == DiceGlobals.CHAT_DICEDOWN:
            phrases = PLocalizer.DiceText_DiceDown_Chat
        else:
            return

        aiSeats = self.getAIPlayers()
        if aiSeats:
            self.aiSpeak(random.choice(aiSeats), phrases, 0.1)

    def changeDice(self, seatIndex, dice):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if self.getAvatarSeatIndex(avatar) != seatIndex or seatIndex not in self._rolledDice:
            return

        if not self._isValidDice(dice):
            return

        # a nudge of the table can only move a single die
        changed = [i for i in range(self.NumDice) if dice[i] != self._rolledDice[seatIndex][i]]
        if len(changed) > 1:
            self.air.logPotentialHacker(
                message='Received dice change for more than one die',
                targetAvId=avatar.doId,
                dice=list(dice))

            return

        self._rolledDice[seatIndex] = list(dice)
        self.d_rollResults(seatIndex, list(dice))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _receiveDiceRoll(self, seatIndex, dice):
        self._rolledDice[seatIndex] = list(dice)
        self.d_rollResults(seatIndex, list(dice))
        self._advanceRollPhase(seatIndex)

    def _advanceRollPhase(self, justRolled):
        occupied = self._getOccupiedSeats()
        if not occupied:
            self._resetRound()
            return

        for seatIndex in self._getSeatsAfter(justRolled, occupied):
            if seatIndex not in self._rolledDice:
                self._activeSeat = seatIndex
                self._requestRoll(seatIndex)
                return

        # Everyone has rolled
        self._activeSeat = -1
        self._onAllRolled()

    def _getSeatsAfter(self, seatIndex, seats):
        ordered = []
        for offset in range(1, self._availableSeats + 1):
            nextSeat = (seatIndex + offset) % self._availableSeats
            if nextSeat in seats:
                ordered.append(nextSeat)

        return ordered

    def _onAllRolled(self):
        # The plain dice game; the highest total takes the pot
        best = None
        winners = []
        for seatIndex, dice in self._rolledDice.items():
            total = sum(dice)
            if best is None or total > best:
                best = total
                winners = [seatIndex]
            elif total == best:
                winners.append(seatIndex)

        if len(winners) != 1:
            # a tie, everyone rolls again
            self.sendUpdate('newRound', [])
            self._rolledDice = {}
            occupied = self._getOccupiedSeats()
            self._activeSeat = occupied[0]
            self._requestRoll(self._activeSeat)
            return

        self._payWinner(winners[0])

    # ------------------------------------------------------------------
    # Payout helpers shared by sub-classes
    # ------------------------------------------------------------------

    def _payWinner(self, winnerSeat):
        totalPot = sum(self._pots.values())
        if self.isPlayerSeat(winnerSeat):
            winner = self.seats[winnerSeat]
            self.giveSeatGold(winnerSeat, totalPot)
            self.sendUpdate('youWin', [winner.doId, winner.getName()])
        else:
            # the house keeps the pot when an AI pirate wins
            self.sendUpdate('youWin', [0, self._getPlayerName(winnerSeat)])

        self._resetRound()

    def _resetRound(self):
        taskMgr.remove(self.uniqueName('dice-roll'))
        self._roundActive = False
        self._readySeats = set()
        self._rolledDice = {}
        self._pots = {}
        self._activeSeat = -1
