import random

from direct.directnotify import DirectNotifyGlobal
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

        self.seats = [None] * self._availableSeats
        self._generatedAI = False

    def announceGenerate(self):
        DistributedInteractiveAI.announceGenerate(self)

    def handleRequestInteraction(self, avatar, interactType, instant):
        availableSeatIndex = self.getRandomOpenSeat()
        if self.getOpenSeatCount == 0:
            self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [3, 0])
            return self.DENY

        self.avatarSit(avatar, availableSeatIndex)
        self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [1, availableSeatIndex])
        return self.ACCEPT

    def handleRequestExit(self, avatar):
        seatIndex = self.getAvatarSeatIndex(avatar)
        if not seatIndex:
            return self.DENY

        self.avatarStand(avatar, seatIndex)
        self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [2, seatIndex])
        return self.ACCEPT

    @property
    def availableSeats(self):
        return self._availableSeats

    @property
    def numberAI(self):
        return self._numberAI

    def getAIPlayers(self):
        ai = []
        for seatIndex in range(len(self.seats)):
            seat = self.seats[seatIndex]
            if seat == 1:
                ai.append(seat)

        return ai

    def getAvatarSeatIndex(self, avatar):
        for seatIndex in range(len(self.seats)):
            seat = self.seats[seatIndex]
            if seat == avatar:
                return seatIndex

        return None

    def getAvailableSeatIndexes(self):
        available = []
        for seatIndex in range(len(self.seats)):
            seat = self.seats[seatIndex]
            if seat == None:
                available.append(seatIndex)

        return available

    def getRandomOpenSeat(self):
        seats = self.getAvailableSeatIndexes()
        if len(seats) == 0:
            return None

        return random.choice(seats)

    def getOpenSeatCount(self):
        return len(self.getAvailableSeatIndex)

    def avatarSit(self, avatar, seatIndex):
        currentSeat = self.seats[seatIndex]
        if currentSeat:
            self.notify.warning('Failed to seat avatar; Seat %d is already occupied!' % seatIndex)
            return

        self.seats[seatIndex] = avatar
        self.sendUpdate('avatarSit', [avatar.doId, seatIndex])

    def avatarStand(self, avatar, seatIndex):
        currentSeat = self.seats[seatIndex]
        if currentSeat != avatar:
            self.notify.warning('Failed to stand avatar; Seat %d is not occupied by avatar!' % seatIndex)
            return

        self.seats[seatIndex] = None
        self.sendUpdate('avatarStand', [avatar.doId, seatIndex])

    def setTableType(self, type):
        self.tableType = type

    def getTableType(self):
        return self.tableType

    def setGameVariation(self, variant):
        self.gameVariation = variant

    def d_setGameVariation(self, variant):
        self.sendUpdate('setGameVariation', [variant])

    def b_setGameVariant(self, variant):
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
        aiList = [0] * self._availableSeats
        aiPlayers = self.getAIPlayers()
        for seatIndex in range(len(aiPlayers)):
            ai = aiPlayers[seatIndex]
            aiList[seatIndex] = ai

        return aiList

    def generatePlayers(self):
        if self._generatedAI:
            self.notify.warning('Failed to generate table AI; AI players already generated!')
            return

        self._generatedAI = True

        randomGen = random.Random()
        randomGen.seed(self.getUniqueId())

        if self._numberAI > self._availableSeats:
            self.notify.warning("Cannot have more ai then seats! reducing to 5")
            self._numberAI = 5

        for i in range(self._numberAI):
            aiType = random.randint(0, 10)
            aiType = 1 if aiType > 0 else 0
            self.seats[i] = aiType

        randomGen.shuffle(self.seats)
