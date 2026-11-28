from direct.directnotify import DirectNotifyGlobal
from pirates.minigame.DistributedPokerTableAI import DistributedPokerTableAI
from pirates.minigame import PlayingCardGlobals


class Distributed7StudTableAI(DistributedPokerTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('Distributed7StudTableAI')

    # rounds: 1 two down and one up, 2-4 one up each, 5 one down, 6 showdown
    NumRounds = 6
    GameType = PlayingCardGlobals.SevenStud

    def __init__(self, air):
        DistributedPokerTableAI.__init__(self, air)
        self.setTableType(1)

    def getRoundDeal(self, round):
        if round == 1:
            return (3, 0)
        elif round in (2, 3, 4, 5):
            return (1, 0)

        return (0, 0)

    def isCardVisible(self, cardIndex):
        # third through sixth street are dealt face up; the first two
        # cards and the river card are the pirate's hole cards.
        return 2 <= cardIndex <= 5
