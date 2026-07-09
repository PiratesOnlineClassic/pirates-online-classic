from direct.directnotify import DirectNotifyGlobal
from pirates.minigame.DistributedPokerTableAI import DistributedPokerTableAI
from pirates.minigame import PlayingCardGlobals


class DistributedHoldemTableAI(DistributedPokerTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHoldemTableAI')

    NumRounds = 5
    GameType = PlayingCardGlobals.Holdem

    def __init__(self, air):
        DistributedPokerTableAI.__init__(self, air)
        self.setTableType(1)
