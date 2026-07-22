import random

from direct.directnotify import DirectNotifyGlobal
from direct.task.TaskManagerGlobal import *
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI


class DistributedGameTableAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGameTableAI')
    MULTIUSE = True

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
            if seat and seat not in (0, 1):
                self.ignore(seat.getDeleteEvent())

        DistributedInteractiveAI.delete(self)

    def handleRequestInteraction(self, avatar, interactType, instant):
        if self.getOpenSeatCount() == 0:
            self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [3, 0])
            return self.DENY

        availableSeatIndex = self.getRandomOpenSeat()
        if availableSeatIndex is None:
            self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [3, 0])
            return self.DENY

        self.avatarSit(avatar, availableSeatIndex)
        self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [1, availableSeatIndex])
        return self.ACCEPT

    def handleRequestExit(self, avatar):
        seatIndex = self.getAvatarSeatIndex(avatar)
        if seatIndex is None:
            return self.DENY

        self.avatarStand(avatar, seatIndex)
        self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [2, seatIndex])
        return self.ACCEPT

    def requestSeat(self, seatIndex, name):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if seatIndex >= self._availableSeats or self.seats[seatIndex] is not None:
            # Requested seat unavailable; try any open seat
            seatIndex = self.getRandomOpenSeat()
            if seatIndex is None:
                self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [3, 0])
                return

        self.avatarSit(avatar, seatIndex)
        self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [1, seatIndex])

    def _avatarUnexpectedExit(self, avatar):
        seatIndex = self.getAvatarSeatIndex(avatar)
        if seatIndex is not None:
            self.seats[seatIndex] = None
            self.sendUpdate('avatarStand', [avatar.doId, seatIndex])
            self.sendUpdate('setAvatarSeat', [self.getAvatarSeat()])

    @property
    def availableSeats(self):
        return self._availableSeats

    @property
    def numberAI(self):
        return self._numberAI

    def getAIPlayers(self):
        aiSeats = []
        for seatIndex in range(len(self.seats)):
            if self.seats[seatIndex] == 1:
                aiSeats.append(seatIndex)

        return aiSeats

    def getAvatarSeatIndex(self, avatar):
        for seatIndex in range(len(self.seats)):
            if self.seats[seatIndex] == avatar:
                return seatIndex

        return None

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
        for seat in self.seats:
            if seat is None or seat in (0, 1):
                result.append(0)
            else:
                result.append(seat.doId)
        return result

    def d_receiveAISpeech(self, seatIndex, message):
        self.sendUpdate('receiveAISpeech', [seatIndex, message])

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
            aiList.append(1 if self.seats[seatIndex] == 1 else 0)

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
            self.seats[i] = 1

        randomGen.shuffle(self.seats)
