from direct.directnotify import DirectNotifyGlobal
from pirates.minigame.DistributedPokerTableAI import DistributedPokerTableAI
from pirates.minigame import PlayingCardGlobals


class Distributed7StudTableAI(DistributedPokerTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('Distributed7StudTableAI')

    NumRounds = 6
    GameType = PlayingCardGlobals.SevenStud

    def __init__(self, air):
        DistributedPokerTableAI.__init__(self, air)
        self.setTableType(1)

    def _dealInitialCards(self):
        # 7 Stud: 3 cards initially (2 hole, 1 up)
        occupied = self._activeBettors
        for _ in range(3):
            for s in occupied:
                self._playerHands[s].append(self._dealCard())

    def _startBettingRound(self, round):
        # 7 Stud: one additional card dealt per round after the first
        if round >= 2:
            for s in self._activeBettors:
                self._playerHands[s].append(self._dealCard())
        DistributedPokerTableAI._startBettingRound(self, round)