import random

from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.task.TaskManagerGlobal import *
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from pirates.minigame import DiceGlobals


class DistributedDiceGameAI(DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDiceGameAI')

    NumDice = 5
    Ante = 10

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air)
        self._readySeats = set()
        self._rolledDice = {}   # seatIndex -> [die values]
        self._activeSeat = 0
        self._roundActive = False
        self._pots = {}         # avId -> gold contributed

    def delete(self):
        taskMgr.remove(self.uniqueName('dice-roll'))
        DistributedGameTableAI.delete(self)

    # ------------------------------------------------------------------
    # Seat lifecycle hooks
    # ------------------------------------------------------------------

    def avatarSit(self, avatar, seatIndex):
        DistributedGameTableAI.avatarSit(self, avatar, seatIndex)

    def avatarStand(self, avatar, seatIndex):
        DistributedGameTableAI.avatarStand(self, avatar, seatIndex)
        self._readySeats.discard(seatIndex)
        self._rolledDice.pop(seatIndex, None)

    def _avatarUnexpectedExit(self, avatar):
        seatIndex = self.getAvatarSeatIndex(avatar)
        if seatIndex is not None:
            self._readySeats.discard(seatIndex)
            self._rolledDice.pop(seatIndex, None)
        DistributedGameTableAI._avatarUnexpectedExit(self, avatar)

    # ------------------------------------------------------------------
    # Ready / round start
    # ------------------------------------------------------------------

    def playerIsReady(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        seatIndex = self.getAvatarSeatIndex(avatar)
        if seatIndex is None:
            return

        inv = self.air.inventoryManager.getInventory(avatar.doId)
        if not inv or inv.getGoldInPocket() < self.Ante:
            return

        inv.setGoldInPocket(inv.getGoldInPocket() - self.Ante)
        self._pots[avatar.doId] = self._pots.get(avatar.doId, 0) + self.Ante
        self._readySeats.add(seatIndex)
        self._checkAllReady()

    def _getHumanSeats(self):
        seats = []
        for seatIndex in range(self._availableSeats):
            seat = self.seats[seatIndex]
            if seat and seat not in (0, 1):
                seats.append(seatIndex)
        return seats

    def _checkAllReady(self):
        humanSeats = self._getHumanSeats()
        if not humanSeats:
            return

        if not all(s in self._readySeats for s in humanSeats):
            return

        # AI players are always ready
        for seatIndex in self.getAIPlayers():
            self._readySeats.add(seatIndex)

        self._startRollPhase()

    def _getOccupiedSeats(self):
        occupied = []
        for seatIndex in range(self._availableSeats):
            if self.seats[seatIndex] is not None:
                occupied.append(seatIndex)
        return occupied

    def _startRollPhase(self):
        self._roundActive = True
        self._rolledDice = {}
        occupied = self._getOccupiedSeats()
        if not occupied:
            return

        self._activeSeat = occupied[0]
        self._requestRoll(self._activeSeat)

    def _getPlayerName(self, seatIndex):
        seat = self.seats[seatIndex]
        if seat == 1:
            return 'AI Player'
        if seat:
            return seat.getName()
        return ''

    def _requestRoll(self, seatIndex):
        name = self._getPlayerName(seatIndex)
        self.sendUpdate('currentTurn', [DiceGlobals.DSTATE_DOROLL, seatIndex, name])
        self.sendUpdate('yourTurn', [seatIndex])

        if self.seats[seatIndex] == 1:
            taskMgr.doMethodLater(1.5, self._aiRollTask, self.uniqueName('dice-roll'),
                extraArgs=[seatIndex], appendTask=True)

    def _aiRollTask(self, seatIndex, task):
        dice = [random.randint(1, 6) for _ in range(self.NumDice)]
        self._receiveDiceRoll(seatIndex, dice)
        return Task.done

    # ------------------------------------------------------------------
    # Client messages
    # ------------------------------------------------------------------

    def playerHasRolled(self, seatIndex, dice):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if self.getAvatarSeatIndex(avatar) != seatIndex:
            return

        self._receiveDiceRoll(seatIndex, dice)

    def sendChat(self, chatType, avId):
        # Relay: just re-broadcast roll results so chat references valid dice
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        seatIndex = self.getAvatarSeatIndex(avatar)
        if seatIndex is None:
            return

        dice = self._rolledDice.get(seatIndex, [])
        if dice:
            self.sendUpdate('rollResults', [seatIndex, dice])

    def changeDice(self, seatIndex, dice):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if self.getAvatarSeatIndex(avatar) != seatIndex:
            return

        self._rolledDice[seatIndex] = list(dice)
        self.sendUpdate('rollResults', [seatIndex, dice])

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _receiveDiceRoll(self, seatIndex, dice):
        self._rolledDice[seatIndex] = list(dice)
        self.sendUpdate('rollResults', [seatIndex, dice])
        self._advanceRollPhase(seatIndex)

    def _advanceRollPhase(self, justRolled):
        occupied = self._getOccupiedSeats()
        startPos = (occupied.index(justRolled) + 1) % len(occupied) if justRolled in occupied else 0

        for i in range(len(occupied)):
            idx = occupied[(startPos + i) % len(occupied)]
            if idx not in self._rolledDice:
                self._activeSeat = idx
                self._requestRoll(idx)
                return

        # Everyone has rolled
        self._onAllRolled()

    def _onAllRolled(self):
        # Base class does nothing; sub-classes implement game-specific logic
        pass

    # ------------------------------------------------------------------
    # Payout helpers shared by sub-classes
    # ------------------------------------------------------------------

    def _payWinner(self, winnerAvId):
        winner = self.air.doId2do.get(winnerAvId)
        if not winner:
            return

        totalPot = sum(self._pots.values())
        if totalPot > 0:
            inv = self.air.inventoryManager.getInventory(winnerAvId)
            if inv:
                inv.addGoldInPocket(totalPot)

        self.sendUpdate('youWin', [winnerAvId, winner.getName()])
        self._resetRound()

    def _resetRound(self):
        self._roundActive = False
        self._readySeats = set()
        self._rolledDice = {}
        self._pots = {}
        taskMgr.remove(self.uniqueName('dice-roll'))
