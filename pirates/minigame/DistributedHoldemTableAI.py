from direct.directnotify import DirectNotifyGlobal
from pirates.minigame.DistributedPokerTableAI import DistributedPokerTableAI
from pirates.minigame import PlayingCardGlobals


class DistributedHoldemTableAI(DistributedPokerTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHoldemTableAI')

    # rounds: 1 pocket cards, 2 flop, 3 turn, 4 river, 5 showdown
    NumRounds = 5
    GameType = PlayingCardGlobals.Holdem

    def __init__(self, air):
        DistributedPokerTableAI.__init__(self, air)
        self.setTableType(1)

    def getRoundDeal(self, round):
        if round == 1:
            return (2, 0)
        elif round == 2:
            return (0, 3)
        elif round in (3, 4):
            return (0, 1)

        return (0, 0)

    def isCardVisible(self, cardIndex):
        # both pocket cards are dealt face down
        return False
