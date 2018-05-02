from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
import random

class DistributedGameTableAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGameTableAI')

    def __init__(self, air, availableSeats=7, aiPlayers=3):
        DistributedInteractiveAI.__init__(self, air)
        self._availableSeats = availableSeats
        self._aiPlayers = aiPlayers
        self.dealerType = 1
        self.tableType = 1
        self.dealerName = 'Dealer'
        self.aiList = []

    def announceGenerate(self):
        DistributedInteractiveAI.announceGenerate(self)
        self.generatePlayers()

    def handleRequestInteraction(self, avatar, interactType, instant):
        result = DistributedInteractiveAI.handleRequestInteraction(self, avatar,
            interactType, instant)

        if not result:
            return self.DENY

        return self.ACCEPT

    @property
    def availableSeats(self):
        return self._availableSeats

    @property
    def aiPlayers(self):
        return self._aiPlayers

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

    def setAIList(self, list):
        self.aiList = list

    def d_setAIList(self, list):
        self.sendUpdate('setAIList', [list])

    def b_setAIList(self, list):
        self.setAIList(list)
        self.d_setAIList(list)

    def getAIList(self):
        return self.aiList

    def generatePlayers(self):
        players = [0] * self.availableSeats

        randomGen = random.Random()
        randomGen.seed(self.getUniqueId()) 

        if (self._aiPlayers > self.availableSeats):
            self.notify.warning("Cannot have more ai then seats! reducing to 5")
            self._aiPlayers = 5

        for i in range(0, self._aiPlayers):
            aiType = random.randint(0, 10)
            aiType = 1 if aiType > 0 else 0
            players[i] = aiType

        randomGen.shuffle(players)
        self.b_setAIList(players)