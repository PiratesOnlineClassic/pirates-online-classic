import random

from direct.directnotify import DirectNotifyGlobal
from direct.task.TaskManagerGlobal import *
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI


class DistributedGameTableAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGameTableAI')
    MULTIUSE = True

    # requestSeatResponse answer codes understood by DistributedGameTable
    SeatResponseDeny = 0
    SeatResponseSit = 1
    SeatResponseStand = 2
    SeatResponseFull = 3
    SeatResponseNoGold = 4
    SeatResponseNonPayer = 5

    # seat place holders; anything else in a seat is a player avatar
    EmptySeat = None
    AISeat = 1

    def __init__(self, air, availableSeats=7, numberAI=3):
        DistributedInteractiveAI.__init__(self, air)
        self._availableSeats = availableSeats
        self._numberAI = numberAI
        self.dealerType = 1
        self.tableType = 1
        self.dealerName = 'Dealer'
        self.gameVariation = 0

        self.seats = [None] * self._availableSeats
        self._generatedAI = False

    def announceGenerate(self):
        DistributedInteractiveAI.announceGenerate(self)
        self.sendUpdate('setAvatarSeat', [self.getAvatarSeat()])

    def delete(self):
        for seatIndex in range(self._availableSeats):
            seat = self.seats[seatIndex]
            if self.isPlayerSeat(seatIndex):
                self.ignore(seat.getDeleteEvent())

        DistributedInteractiveAI.delete(self)

    def handleRequestInteraction(self, avatar, interactType, instant):
        if self.getAvatarSeatIndex(avatar) is not None:
            # this avatar is already seated at our table...
            self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [self.SeatResponseDeny, 0])
            return self.DENY

        if self.getOpenSeatCount() == 0:
            self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [self.SeatResponseFull, 0])
            return self.DENY

        availableSeatIndex = self.getRandomOpenSeat()
        if availableSeatIndex is None:
            self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [self.SeatResponseFull, 0])
            return self.DENY

        self.avatarSit(avatar, availableSeatIndex)
        self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [self.SeatResponseSit, availableSeatIndex])
        return self.ACCEPT

    def handleRequestExit(self, avatar):
        seatIndex = self.getAvatarSeatIndex(avatar)
        if seatIndex is None:
            return self.DENY

        self.avatarStand(avatar, seatIndex)
        self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [self.SeatResponseStand, seatIndex])
        return self.ACCEPT

    def requestSeat(self, seatIndex, name):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if self.getAvatarSeatIndex(avatar) is not None:
            return

        if seatIndex >= self._availableSeats or self.seats[seatIndex] is not None:
            # Requested seat unavailable; try any open seat
            seatIndex = self.getRandomOpenSeat()
            if seatIndex is None:
                self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [self.SeatResponseFull, 0])
                return

        self.avatarSit(avatar, seatIndex)
        self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [self.SeatResponseSit, seatIndex])

    def standPlayer(self, seatIndex):
        """
        Forces the player in the specified seat to get up from the table,
        used when a player runs out of gold, times out or gets caught cheating.
        """

        if not self.isPlayerSeat(seatIndex):
            return

        avatar = self.seats[seatIndex]
        self.avatarStand(avatar, seatIndex)
        self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [self.SeatResponseStand, seatIndex])
        self.sendUpdateToAvatarId(avatar.doId, 'setUserId', [0])

    def _avatarUnexpectedExit(self, avatar):
        seatIndex = self.getAvatarSeatIndex(avatar)
        if seatIndex is not None:
            self.avatarStand(avatar, seatIndex)

    @property
    def availableSeats(self):
        return self._availableSeats

    @property
    def numberAI(self):
        return self._numberAI

    def isAISeat(self, seatIndex):
        return self.seats[seatIndex] is not None and self.seats[seatIndex] == self.AISeat

    def isPlayerSeat(self, seatIndex):
        seat = self.seats[seatIndex]
        return seat is not None and seat not in (0, 1)

    def getAIPlayers(self):
        aiSeats = []
        for seatIndex in range(len(self.seats)):
            if self.isAISeat(seatIndex):
                aiSeats.append(seatIndex)

        return aiSeats

    def getPlayerSeats(self):
        playerSeats = []
        for seatIndex in range(len(self.seats)):
            if self.isPlayerSeat(seatIndex):
                playerSeats.append(seatIndex)

        return playerSeats

    def getOccupiedSeats(self):
        occupied = []
        for seatIndex in range(len(self.seats)):
            if self.seats[seatIndex] is not None:
                occupied.append(seatIndex)

        return occupied

    def getAvatarSeatIndex(self, avatar):
        for seatIndex in range(len(self.seats)):
            if self.isPlayerSeat(seatIndex) and self.seats[seatIndex] == avatar:
                return seatIndex

        return None

    def getSenderSeatIndex(self):
        """
        Returns the seat index of the avatar that sent the current field update,
        or None if the sender is not seated at this table.
        """

        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return None

        return self.getAvatarSeatIndex(avatar)

    def getAvailableSeatIndexes(self):
        available = []
        for seatIndex in range(len(self.seats)):
            if self.seats[seatIndex] is None:
                available.append(seatIndex)

        return available

    def getRandomOpenSeat(self):
        seats = self.getAvailableSeatIndexes()
        if not seats:
            return None

        return random.choice(seats)

    def getOpenSeatCount(self):
        return len(self.getAvailableSeatIndexes())

    def getSeatName(self, seatIndex):
        if self.isPlayerSeat(seatIndex):
            return self.seats[seatIndex].getName()

        return ''

    def avatarSit(self, avatar, seatIndex):
        if self.seats[seatIndex] is not None:
            self.notify.warning('Failed to seat avatar; Seat %d is already occupied!' % seatIndex)
            return

        self.seats[seatIndex] = avatar
        self.acceptOnce(avatar.getDeleteEvent(), self._avatarUnexpectedExit, extraArgs=[avatar])
        self.sendUpdate('avatarSit', [avatar.doId, seatIndex])
        self.sendUpdate('setAvatarSeat', [self.getAvatarSeat()])

    def avatarStand(self, avatar, seatIndex):
        if self.seats[seatIndex] != avatar:
            self.notify.warning('Failed to stand avatar; Seat %d is not occupied by avatar!' % seatIndex)
            return

        self.ignore(avatar.getDeleteEvent())
        self.seats[seatIndex] = None
        self.sendUpdate('avatarStand', [avatar.doId, seatIndex])
        self.sendUpdate('setAvatarSeat', [self.getAvatarSeat()])

    def setAvatarSeat(self, seatList):
        # Server-side state is managed via self.seats; this is a no-op receiver
        pass

    def getAvatarSeat(self):
        result = []
        for seatIndex in range(len(self.seats)):
            if self.isPlayerSeat(seatIndex):
                result.append(self.seats[seatIndex].doId)
            else:
                result.append(0)

        return result

    # ------------------------------------------------------------------
    # Gold helpers; table games are played with the gold in the
    # avatar's pocket, which the client reads directly from it's inventory
    # ------------------------------------------------------------------

    def getSeatInventory(self, seatIndex):
        if not self.isPlayerSeat(seatIndex):
            return None

        return self.air.inventoryManager.getInventory(self.seats[seatIndex].doId)

    def getSeatGold(self, seatIndex):
        inventory = self.getSeatInventory(seatIndex)
        if not inventory:
            return 0

        return inventory.getGoldInPocket()

    def takeSeatGold(self, seatIndex, amount):
        """
        Removes up to amount gold from the player in the seat, returns the
        amount of gold that was actually taken.
        """

        inventory = self.getSeatInventory(seatIndex)
        if not inventory or amount <= 0:
            return 0

        amount = min(amount, inventory.getGoldInPocket())
        inventory.setGoldInPocket(inventory.getGoldInPocket() - amount)
        return amount

    def giveSeatGold(self, seatIndex, amount):
        inventory = self.getSeatInventory(seatIndex)
        if not inventory or amount <= 0:
            return False

        inventory.setGoldInPocket(inventory.getGoldInPocket() + amount)
        return True

    def d_receiveAISpeech(self, seatIndex, message):
        self.sendUpdate('receiveAISpeech', [seatIndex, message])

    def d_receiveAIThoughts(self, seatIndex, message):
        self.sendUpdate('receiveAIThoughts', [seatIndex, message])

    def aiSpeak(self, seatIndex, phrases, chance=1.0):
        """
        Has the AI player sitting in the seat say a random phrase from the
        list of phrases specified, when the random chance succeeds.
        """

        if not phrases or not self.isAISeat(seatIndex):
            return

        if random.random() > chance:
            return

        self.d_receiveAISpeech(seatIndex, random.choice(phrases))

    def setTableType(self, type):
        self.tableType = type

    def d_setTableType(self, type):
        self.sendUpdate('setTableType', [type])

    def b_setTableType(self, type):
        self.setTableType(type)
        self.d_setTableType(type)

    def getTableType(self):
        return self.tableType

    def setGameVariation(self, variant):
        self.gameVariation = variant

    def d_setGameVariation(self, variant):
        self.sendUpdate('setGameVariation', [variant])

    def b_setGameVariation(self, variant):
        self.setGameVariation(variant)
        self.d_setGameVariation(variant)

    def getGameVariation(self):
        return self.gameVariation

    def setDealerName(self, name):
        self.dealerName = name

    def d_setDealerName(self, name):
        self.sendUpdate('setDealerName', [name])

    def b_setDealerName(self, name):
        self.setDealerName(name)
        self.d_setDealerName(name)

    def getDealerName(self):
        return self.dealerName

    def setDealerType(self, type):
        self.dealerType = type

    def d_setDealerType(self, type):
        self.sendUpdate('setDealerType', [type])

    def b_setDealerType(self, type):
        self.setDealerType(type)
        self.d_setDealerType(type)

    def getDealerType(self):
        return self.dealerType

    def getAIList(self):
        aiList = []
        for seatIndex in range(self._availableSeats):
            aiList.append(1 if self.isAISeat(seatIndex) else 0)

        return aiList

    def generatePlayers(self):
        if self._generatedAI:
            self.notify.warning('Failed to generate table AI; AI players already generated!')
            return

        self._generatedAI = True

        randomGen = random.Random()
        randomGen.seed(self.getUniqueId())

        if self._numberAI > self._availableSeats:
            self.notify.warning('Cannot have more AI than seats! Reducing to %d.' % self._availableSeats)
            self._numberAI = self._availableSeats

        for i in range(self._numberAI):
            self.seats[i] = self.AISeat

        randomGen.shuffle(self.seats)
