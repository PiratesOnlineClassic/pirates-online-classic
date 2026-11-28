import random
from collections import Counter
from itertools import combinations

from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.task.TaskManagerGlobal import *
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from pirates.minigame import PlayingCardGlobals
from pirates.uberdog.UberDogGlobals import InventoryType


class DistributedPokerTableAI(DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPokerTableAI')

    # [ante, small blind, big blind]
    DefaultAnteList = [0, 1, 2]
    # the final round of a hand, the showdown
    NumRounds = 5
    GameType = PlayingCardGlobals.Holdem
    # the stack AI seats post their blinds and antes from
    AIStartingChips = 500
    # the number of bets allowed in a single betting round
    MaxRaises = 4
    # how long a client has to act before it folds
    ActionTimeout = PlayingCardGlobals.SecondsPerHand + 5.0
    # delays for the client animations to play
    NewHandDelay = 2.0
    BlindsDelay = 1.5
    DealCardDelay = 0.6
    RoundDelay = 1.5
    ShowdownDelay = 8.0
    AIThinkTime = (1.0, 3.0)

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air)
        self.potSize = 0
        self.anteList = list(self.DefaultAnteList)
        self.betMultiplier = 1
        self.gameType = self.GameType

        self._round = 0
        self._buttonSeat = 0
        self._communityCards = []
        self._playerHands = [[] for _ in range(self._availableSeats)]
        self._chipsCount = [0] * self._availableSeats
        self._totalWinnings = [PlayingCardGlobals.PlayerInactive] * self._availableSeats
        self._playerActions = [[PlayingCardGlobals.NoAction, 0] for _ in range(self._availableSeats)]
        self._maxBet = 0
        self._numRaises = 0
        self._handActive = False
        self._showdown = False

        self._deck = []
        self._handSeats = []        # seats that were dealt into this hand
        self._activeBettors = []    # seats still in the hand (not folded)
        self._allInSeats = set()    # seats which have no more chips to bet
        self._bettingOrder = []     # remaining bettors this round
        self._contributions = {}    # seatIndex -> total gold put in the pot
        self._timeouts = {}         # seatIndex -> consecutive timeout count
        self._cheaters = {}         # seatIndex -> swapped in card
        self._caughtCheating = set()

    def delete(self):
        taskMgr.remove(self.uniqueName('poker-turn'))
        taskMgr.remove(self.uniqueName('poker-timeout'))
        taskMgr.remove(self.uniqueName('poker-start'))
        DistributedGameTableAI.delete(self)

    def setGameType(self, gameType):
        # the level editor passes the category name of the table here,
        # the poker variation is decided by the table's class instead...
        if isinstance(gameType, int):
            self.gameType = gameType

    def getGameType(self):
        return self.gameType

    def setBetMultiplier(self, multiplier):
        self.betMultiplier = max(1, multiplier)
        self.anteList = [ante * self.betMultiplier for ante in self.DefaultAnteList]

    def getBetMultiplier(self):
        return self.betMultiplier

    def setAnteList(self, anteList):
        self.anteList = list(anteList)

    def d_setAnteList(self, anteList):
        self.sendUpdate('setAnteList', [anteList])

    def b_setAnteList(self, anteList):
        self.setAnteList(anteList)
        self.d_setAnteList(anteList)

    def getAnteList(self):
        return list(self.anteList)

    def setTableState(self, round, buttonSeat, communityCards, playerHands,
                      totalWinningsArray, chipsCount):
        self._round = round
        self._buttonSeat = buttonSeat
        self._communityCards = list(communityCards)
        self._playerHands = [list(h) for h in playerHands]
        self._totalWinnings = list(totalWinningsArray)
        self._chipsCount = self._normalizeChipsCount(chipsCount)

    def d_setTableState(self):
        self.sendUpdate('setTableState', list(self.getTableState()))

    def getTableState(self):
        self._updateChipsCount()
        return (self._round, self._buttonSeat, list(self._communityCards),
                self.getPublicPlayerHands(),
                list(self._totalWinnings),
                list(self._chipsCount))

    def _normalizePlayerHands(self, playerHands=None):
        needed = self._availableSeats
        normalized = [list(h) for h in (playerHands or [])]
        if len(normalized) < needed:
            normalized += [[] for _ in range(needed - len(normalized))]
        elif len(normalized) > needed:
            normalized = normalized[:needed]
        return normalized

    def _normalizeChipsCount(self, chipsCount=None):
        needed = self._availableSeats
        normalized = list(chipsCount or [])
        if len(normalized) < needed:
            normalized += [0] * (needed - len(normalized))
        elif len(normalized) > needed:
            normalized = normalized[:needed]
        return normalized

    def isCardVisible(self, cardIndex):
        # pocket cards dealt face up are seen by everybody at the table...
        return False

    def getPublicPlayerHands(self):
        # face down cards are hidden until they are revealed at the showdown...
        hands = []
        for seatIndex in range(self._availableSeats):
            hand = self._playerHands[seatIndex] if seatIndex < len(self._playerHands) else []
            if not hand or seatIndex not in self._activeBettors:
                hands.append([])
                continue

            if self._showdown:
                hands.append(list(hand))
                continue

            publicHand = []
            for cardIndex in range(len(hand)):
                if self.isCardVisible(cardIndex):
                    publicHand.append(hand[cardIndex])
                else:
                    publicHand.append(PlayingCardGlobals.Unknown)

            hands.append(publicHand)

        return hands

    def setPotSize(self, potSize):
        self.potSize = potSize

    def d_setPotSize(self, potSize):
        self.sendUpdate('setPotSize', [potSize])

    def b_setPotSize(self, potSize):
        self.setPotSize(potSize)
        self.d_setPotSize(potSize)

    def getPotSize(self):
        return self.potSize

    def d_setPlayerActions(self):
        self._updateChipsCount()
        self.sendUpdate('setPlayerActions', [
            self._maxBet,
            self._playerActions,
            self._chipsCount,
        ])

    def d_askForClientAction(self, seatIndex):
        self.sendUpdate('askForClientAction', [seatIndex])

    def d_requestAIPlayerTurn(self, seatIndex):
        self.sendUpdate('requestAIPlayerTurn', [seatIndex])

    def d_setLocalAvatarHand(self, seatIndex):
        if self.isPlayerSeat(seatIndex):
            self.sendUpdateToAvatarId(self.seats[seatIndex].doId, 'setLocalAvatarHand',
                [self._playerHands[seatIndex]])

    def d_setLocalAvatarHandValue(self, seatIndex):
        if not self.isPlayerSeat(seatIndex):
            return

        handId, sortedCards = self.getHandValue(seatIndex)
        self.sendUpdateToAvatarId(self.seats[seatIndex].doId, 'setLocalAvatarHandValue',
            [handId, sortedCards])

    def d_setAllHandValues(self, handIds, sortedCards):
        self.sendUpdate('setAllHandValues', [handIds, sortedCards])

    def getMinimumBetAmount(self):
        # mirrors PokerBase.getMinimumBetAmount on the client
        bet = self.anteList[2] if len(self.anteList) > 2 else 0
        if bet:
            if self._round >= 3:
                bet = bet * 2
        else:
            bet = self.anteList[0] if self.anteList else 0
            if not bet:
                bet = PlayingCardGlobals.DefaultBetAmount

        return bet

    def minimumChipsToSitDown(self):
        # mirrors PokerBase.minimumChipsToSitDown on the client
        minimumChips = 20
        if len(self.anteList) > 2 and self.anteList[2] > 0:
            minimumChips = 10 * self.anteList[2]
        elif self.anteList and self.anteList[0] > 0:
            minimumChips = 10 * self.anteList[0]

        return minimumChips

    def _minChipsToPlay(self):
        ante = self.anteList[0] if self.anteList else 0
        bigBlind = self.anteList[2] if len(self.anteList) > 2 else 0
        return max(1, ante + bigBlind)

    def getSeatChips(self, seatIndex):
        if self.isPlayerSeat(seatIndex):
            return self.getSeatGold(seatIndex)

        if self.isAISeat(seatIndex):
            return self._chipsCount[seatIndex]

        return 0

    def _updateChipsCount(self):
        self._chipsCount = self._normalizeChipsCount(self._chipsCount)
        for seatIndex in range(self._availableSeats):
            if self.isPlayerSeat(seatIndex):
                self._chipsCount[seatIndex] = self.getSeatGold(seatIndex)
            elif not self.isAISeat(seatIndex):
                self._chipsCount[seatIndex] = 0

    def _seedAIChips(self):
        self._chipsCount = self._normalizeChipsCount(self._chipsCount)
        minChips = self._minChipsToPlay()
        for seatIndex in self.getAIPlayers():
            if self._chipsCount[seatIndex] < minChips:
                self._chipsCount[seatIndex] = self.AIStartingChips * self.betMultiplier

    def _deductChips(self, seatIndex, amount):
        if amount <= 0:
            return 0

        if self.isPlayerSeat(seatIndex):
            paid = self.takeSeatGold(seatIndex, amount)
        elif self.isAISeat(seatIndex):
            paid = min(amount, self._chipsCount[seatIndex])
            self._chipsCount[seatIndex] -= paid
        else:
            paid = 0

        self._contributions[seatIndex] = self._contributions.get(seatIndex, 0) + paid
        self.potSize += paid
        if self.getSeatChips(seatIndex) <= 0 and seatIndex in self._activeBettors:
            self._allInSeats.add(seatIndex)

        return paid

    def _payChips(self, seatIndex, amount):
        if amount <= 0:
            return

        if self.isPlayerSeat(seatIndex):
            self.giveSeatGold(seatIndex, amount)
        elif self.isAISeat(seatIndex):
            self._chipsCount[seatIndex] += amount

    def handleRequestInteraction(self, avatar, interactType, instant):
        inv = self.air.inventoryManager.getInventory(avatar.doId)
        if not inv or inv.getGoldInPocket() < self.minimumChipsToSitDown():
            self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [self.SeatResponseNoGold, 0])
            return self.DENY

        return DistributedGameTableAI.handleRequestInteraction(self, avatar, interactType, instant)

    def avatarSit(self, avatar, seatIndex):
        DistributedGameTableAI.avatarSit(self, avatar, seatIndex)
        self._timeouts[seatIndex] = 0
        self._totalWinnings[seatIndex] = PlayingCardGlobals.PlayerInactive
        self._playerHands[seatIndex] = []
        self.d_setTableState()
        self._scheduleHandStart()

    def avatarStand(self, avatar, seatIndex):
        # a player leaving the table forfeits the hand in play...
        if self._handActive and seatIndex in self._activeBettors:
            self._foldSeat(seatIndex)

        DistributedGameTableAI.avatarStand(self, avatar, seatIndex)
        self._totalWinnings[seatIndex] = PlayingCardGlobals.PlayerInactive
        self._playerHands[seatIndex] = []
        self._timeouts.pop(seatIndex, None)
        self._chipsCount[seatIndex] = 0

        if not self._handActive:
            self.d_setTableState()
            return

        if not self.getPlayerSeats():
            # nobody is left to watch the hand, abandon it
            self._abortHand()
            return

        self.d_setPlayerActions()
        self.d_setTableState()
        if len(self._activeBettors) <= 1:
            self._endHand()
        elif self._bettingOrder and self._bettingOrder[0] == seatIndex:
            self._bettingOrder.pop(0)
            self._nextBettingAction()
        else:
            while seatIndex in self._bettingOrder:
                self._bettingOrder.remove(seatIndex)

    def _buildDeck(self):
        self._deck = list(range(52))
        random.shuffle(self._deck)

    def _dealCard(self):
        return self._deck.pop()

    def getRoundDeal(self, round):
        # returns the number of (pocket cards, community cards) dealt this round...
        if round == 1:
            return (2, 0)
        elif round == 2:
            return (0, 3)
        elif round in (3, 4):
            return (0, 1)

        return (0, 0)

    def _scheduleHandStart(self, delay=NewHandDelay):
        if self._handActive:
            return

        if not self._canStartHand():
            return

        taskMgr.remove(self.uniqueName('poker-start'))
        taskMgr.doMethodLater(delay, self._startHandTask,
            self.uniqueName('poker-start'), appendTask=True)

    def _canStartHand(self):
        # don't bother dealing unless a pirate is sitting at the table...
        if not self.getPlayerSeats():
            return False

        return len(self._getPlayableSeats()) >= 2

    def _getPlayableSeats(self):
        minChips = self._minChipsToPlay()
        playable = []
        for seatIndex in self.getOccupiedSeats():
            if self.isAISeat(seatIndex) or self.getSeatChips(seatIndex) >= minChips:
                playable.append(seatIndex)

        return playable

    def _startHandTask(self, task=None):
        if self._canStartHand():
            self._startHand()
        else:
            self._handActive = False

        return Task.done

    def _startHand(self):
        self._seedAIChips()
        occupied = self._getPlayableSeats()
        if len(occupied) < 2:
            self._handActive = False
            return

        self._handActive = True
        self._showdown = False
        self._buildDeck()
        self._playerHands = self._normalizePlayerHands([])
        self._communityCards = []
        self._playerActions = [[PlayingCardGlobals.NoAction, 0] for _ in range(self._availableSeats)]
        self._totalWinnings = [PlayingCardGlobals.PlayerLost] * self._availableSeats
        self._handSeats = list(occupied)
        self._activeBettors = list(occupied)
        self._allInSeats = set()
        self._contributions = {}
        self._cheaters = {}
        self._caughtCheating = set()
        self._bettingOrder = []
        self._maxBet = 0
        self._numRaises = 0
        self.b_setPotSize(0)

        # advance the dealer button...
        pos = occupied.index(self._buttonSeat) if self._buttonSeat in occupied else -1
        self._buttonSeat = occupied[(pos + 1) % len(occupied)]

        # round 0 clears the table on the client
        self._round = 0
        self.d_setTableState()
        self.d_setPlayerActions()

        taskMgr.doMethodLater(self.BlindsDelay, self._postBlindsTask,
            self.uniqueName('poker-turn'), appendTask=True)

    def _postBlindsTask(self, task=None):
        self._collectBlindsAndAntes()
        taskMgr.doMethodLater(self.BlindsDelay, self._startRoundTask,
            self.uniqueName('poker-turn'), extraArgs=[1], appendTask=True)
        return Task.done

    def _getSeatAfter(self, seatIndex, seats):
        ordered = self.getSeatsAfter(seatIndex, seats)
        if not ordered:
            return None

        return ordered[0]

    def _getBlindSeats(self):
        occupied = self._handSeats
        if len(occupied) == 2:
            # heads up, the button posts the small blind
            sbSeat = self._buttonSeat
        else:
            sbSeat = self._getSeatAfter(self._buttonSeat, occupied)

        bbSeat = self._getSeatAfter(sbSeat, occupied)
        return sbSeat, bbSeat

    def _collectBlindsAndAntes(self):
        occupied = self._activeBettors
        if not occupied:
            return

        ante = self.anteList[0] if self.anteList else 0
        smallBlind = self.anteList[1] if len(self.anteList) > 1 else 0
        bigBlind = self.anteList[2] if len(self.anteList) > 2 else 0

        # the client has no display for the ante action, so the antes
        # are simply added to the pot...
        if ante:
            for seatIndex in occupied:
                self._deductChips(seatIndex, ante)

        sbSeat, bbSeat = self._getBlindSeats()
        if smallBlind:
            paid = self._deductChips(sbSeat, smallBlind)
            self._playerActions[sbSeat] = [PlayingCardGlobals.SmallBlind, paid]

        if bigBlind:
            paid = self._deductChips(bbSeat, bigBlind)
            self._playerActions[bbSeat] = [PlayingCardGlobals.BigBlind, paid]

        self._maxBet = bigBlind
        self.d_setPotSize(self.potSize)
        self.d_setPlayerActions()

    def _startRoundTask(self, round, task=None):
        self._startBettingRound(round)
        return Task.done

    def _dealRoundCards(self, round):
        numPlayerCards, numCommunityCards = self.getRoundDeal(round)
        dealOrder = self.getSeatsAfter(self._buttonSeat, self._activeBettors)
        for i in range(numPlayerCards):
            for seatIndex in dealOrder:
                self._playerHands[seatIndex].append(self._dealCard())

        for i in range(numCommunityCards):
            self._communityCards.append(self._dealCard())

        return numPlayerCards * len(dealOrder) + numCommunityCards

    def _startBettingRound(self, round):
        self._round = round
        if round > 1:
            # new betting round, everybody starts fresh
            self._maxBet = 0
            self._playerActions = [[PlayingCardGlobals.NoAction, 0] for _ in range(self._availableSeats)]

        self._numRaises = 0 if round > 1 else 1
        numCards = self._dealRoundCards(round)
        self._updateTells(round)

        # send the pirates their private cards before the table state,
        # the client builds it's hand display when the table updates.
        for seatIndex in self._activeBettors:
            self.d_setLocalAvatarHand(seatIndex)
            if round > 1:
                self.d_setLocalAvatarHandValue(seatIndex)

        self.d_setTableState()
        if round > 1:
            self.d_setPlayerActions()

        if round == 1:
            firstSeat = self._getSeatAfter(self._getBlindSeats()[1], self._activeBettors)
        else:
            firstSeat = self._getSeatAfter(self._buttonSeat, self._activeBettors)

        self._bettingOrder = [seatIndex for seatIndex in self.getSeatsAfter(
            (firstSeat - 1) % self._availableSeats, self._activeBettors)
            if seatIndex not in self._allInSeats]

        if len(self._bettingOrder) == 1 and self._getCallAmount(self._bettingOrder[0]) <= 0:
            # everyone else is all-in, there is nothing left to bet on
            self._bettingOrder = []

        delay = self.DealCardDelay * numCards + self.RoundDelay
        taskMgr.doMethodLater(delay, self._nextBettingActionTask,
            self.uniqueName('poker-turn'), appendTask=True)

    def _updateTells(self, round):
        # while a hand is in play the totalWinnings array carries the
        # tells the client animates when the AI pirates look at their cards...
        for seatIndex in range(self._availableSeats):
            self._totalWinnings[seatIndex] = PlayingCardGlobals.NoTell

        if round >= self.NumRounds:
            return

        numPlayerCards, numCommunityCards = self.getRoundDeal(round)
        if not numPlayerCards and not numCommunityCards:
            return

        for seatIndex in self._activeBettors:
            if not self.isAISeat(seatIndex):
                continue

            if random.random() > PlayingCardGlobals.BaseTellChanceAI:
                continue

            if self._getHandStrength(seatIndex) >= 0.5:
                self._totalWinnings[seatIndex] = PlayingCardGlobals.GoodTell
            else:
                self._totalWinnings[seatIndex] = PlayingCardGlobals.BadTell

    def _getCallAmount(self, seatIndex):
        return max(0, self._maxBet - self._playerActions[seatIndex][1])

    def _nextBettingActionTask(self, task=None):
        self._nextBettingAction()
        return Task.done

    def _nextBettingAction(self):
        taskMgr.remove(self.uniqueName('poker-timeout'))
        taskMgr.remove(self.uniqueName('poker-turn'))

        # skip anyone that has since gone all-in or left
        while self._bettingOrder and (self._bettingOrder[0] not in self._activeBettors or
                                      self._bettingOrder[0] in self._allInSeats):
            self._bettingOrder.pop(0)

        if not self._bettingOrder:
            self._onBettingRoundComplete()
            return

        seatIndex = self._bettingOrder[0]
        if self.isAISeat(seatIndex):
            self.d_requestAIPlayerTurn(seatIndex)
            taskMgr.doMethodLater(random.uniform(*self.AIThinkTime), self._aiActTask,
                self.uniqueName('poker-turn'), extraArgs=[seatIndex], appendTask=True)
        else:
            self.d_askForClientAction(seatIndex)
            taskMgr.doMethodLater(self.ActionTimeout, self._playerTimeoutTask,
                self.uniqueName('poker-timeout'), extraArgs=[seatIndex], appendTask=True)

    def _playerTimeoutTask(self, seatIndex, task=None):
        self._timeouts[seatIndex] = self._timeouts.get(seatIndex, 0) + 1
        self._applyAction(seatIndex, PlayingCardGlobals.Fold, 0)
        if self._timeouts.get(seatIndex, 0) >= PlayingCardGlobals.MaximumTimeouts:
            # the client should have left by now, make them get up.
            self.standPlayer(seatIndex)

        return Task.done

    def clientAction(self, round, action):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        seatIndex = self.getAvatarSeatIndex(avatar)
        if (seatIndex is None or round != self._round or
                not self._bettingOrder or self._bettingOrder[0] != seatIndex):
            return

        taskMgr.remove(self.uniqueName('poker-timeout'))
        self._timeouts[seatIndex] = 0

        actionCode = action[0] if action else PlayingCardGlobals.Fold
        amount = action[1] if len(action) > 1 else 0
        self._applyAction(seatIndex, actionCode, amount)

    def _applyAction(self, seatIndex, actionCode, amount):
        if not self._bettingOrder or self._bettingOrder[0] != seatIndex:
            return

        self._bettingOrder.pop(0)
        callAmount = self._getCallAmount(seatIndex)
        alreadyBet = self._playerActions[seatIndex][1]

        if actionCode == PlayingCardGlobals.Check and callAmount > 0:
            # can't check facing a bet, treat it as a call
            actionCode = PlayingCardGlobals.CheckCall

        if actionCode == PlayingCardGlobals.BetRaise and self._numRaises >= self.MaxRaises:
            # the betting is capped for this round
            actionCode = PlayingCardGlobals.CheckCall

        if actionCode == PlayingCardGlobals.Fold:
            self._foldSeat(seatIndex)

        elif actionCode == PlayingCardGlobals.Check:
            self._playerActions[seatIndex] = [PlayingCardGlobals.Check, alreadyBet]

        elif actionCode == PlayingCardGlobals.CheckCall:
            paid = self._deductChips(seatIndex, callAmount)
            if seatIndex in self._allInSeats:
                self._playerActions[seatIndex] = [PlayingCardGlobals.AllIn, alreadyBet + paid]
            else:
                self._playerActions[seatIndex] = [PlayingCardGlobals.CheckCall, alreadyBet + paid]

        elif actionCode == PlayingCardGlobals.BetRaise:
            betAmount = callAmount + self.getMinimumBetAmount()
            paid = self._deductChips(seatIndex, betAmount)
            self._raiseTo(seatIndex, alreadyBet + paid)

        elif actionCode == PlayingCardGlobals.AllIn:
            paid = self._deductChips(seatIndex, self.getSeatChips(seatIndex))
            self._allInSeats.add(seatIndex)
            self._raiseTo(seatIndex, alreadyBet + paid, PlayingCardGlobals.AllIn)

        else:
            self.notify.warning('Received unknown poker action %s from seat %d!' % (actionCode, seatIndex))
            self._foldSeat(seatIndex)

        self.d_setPotSize(self.potSize)
        self.d_setPlayerActions()

        if len(self._activeBettors) <= 1:
            self.d_setTableState()
            self._endHand()
            return

        self._nextBettingAction()

    def _raiseTo(self, seatIndex, totalBet, actionCode=PlayingCardGlobals.BetRaise):
        if totalBet > self._maxBet:
            self._maxBet = totalBet
            self._numRaises += 1
            # everybody who already acted must act again...
            self._bettingOrder = [s for s in self.getSeatsAfter(seatIndex, self._activeBettors)
                                  if s != seatIndex and s not in self._allInSeats]
            self._playerActions[seatIndex] = [actionCode, totalBet]
        else:
            # an all-in for less than the current bet is just a call
            self._playerActions[seatIndex] = [PlayingCardGlobals.AllIn, totalBet]

    def _foldSeat(self, seatIndex):
        self._playerActions[seatIndex] = [PlayingCardGlobals.Fold, 0]
        if seatIndex in self._activeBettors:
            self._activeBettors.remove(seatIndex)

        self._allInSeats.discard(seatIndex)
        while seatIndex in self._bettingOrder:
            self._bettingOrder.remove(seatIndex)

    def _onBettingRoundComplete(self):
        taskMgr.remove(self.uniqueName('poker-turn'))
        nextRound = self._round + 1
        if nextRound >= self.NumRounds or len(self._activeBettors) <= 1:
            self._endHand()
        else:
            taskMgr.doMethodLater(self.RoundDelay, self._startNextRoundTask,
                self.uniqueName('poker-turn'), extraArgs=[nextRound], appendTask=True)

    def _startNextRoundTask(self, nextRound, task=None):
        self._startBettingRound(nextRound)
        return Task.done

    def _aiActTask(self, seatIndex, task=None):
        self._aiDecide(seatIndex)
        return Task.done

    def _getHandStrength(self, seatIndex):
        # a rough 0.0 - 1.0 estimate of how good the seat's hand is...
        cards = self._playerHands[seatIndex] + self._communityCards
        if not cards:
            return 0.0

        if len(cards) <= 2:
            ranks = sorted([card % 13 for card in cards], reverse=True)
            strength = (ranks[0] + (ranks[1] if len(ranks) > 1 else 0)) / 48.0
            if len(ranks) > 1 and ranks[0] == ranks[1]:
                strength += 0.35 + ranks[0] / 40.0
            if len(cards) > 1 and cards[0] // 13 == cards[1] // 13:
                strength += 0.05
            return min(strength, 1.0)

        handId, sortedCards = self._bestHandFrom(cards)
        strength = (handId - PlayingCardGlobals.NoPair) / 5.0
        if sortedCards:
            strength += (sortedCards[0] % 13) / 60.0
        return min(strength, 1.0)

    def _aiDecide(self, seatIndex):
        callAmount = self._getCallAmount(seatIndex)
        chips = self.getSeatChips(seatIndex)
        strength = self._getHandStrength(seatIndex) + random.uniform(-0.15, 0.15)
        bluff = random.random() < 0.05

        if callAmount >= chips:
            # calling would put us all-in
            if strength > 0.55 or bluff:
                self._applyAction(seatIndex, PlayingCardGlobals.AllIn, chips)
            else:
                self._applyAction(seatIndex, PlayingCardGlobals.Fold, 0)
            return

        if (strength > 0.65 or bluff) and self._numRaises < self.MaxRaises and \
                chips > callAmount + self.getMinimumBetAmount():
            self._applyAction(seatIndex, PlayingCardGlobals.BetRaise, 0)
        elif callAmount == 0:
            self._applyAction(seatIndex, PlayingCardGlobals.Check, 0)
        elif strength > 0.25 or callAmount <= self.getMinimumBetAmount() and strength > 0.1:
            self._applyAction(seatIndex, PlayingCardGlobals.CheckCall, callAmount)
        else:
            self._applyAction(seatIndex, PlayingCardGlobals.Fold, 0)

    def _endHand(self):
        taskMgr.remove(self.uniqueName('poker-turn'))
        taskMgr.remove(self.uniqueName('poker-timeout'))
        self._bettingOrder = []

        handIds = [PlayingCardGlobals.Nothing] * self._availableSeats
        handCards = [[] for _ in range(self._availableSeats)]
        scores = {}

        if len(self._activeBettors) > 1:
            # deal out whatever cards are left when everyone is all-in
            for round in range(self._round + 1, self.NumRounds):
                self._dealRoundCards(round)

            self._showdown = True
            for seatIndex in self._activeBettors:
                allCards = self._playerHands[seatIndex] + self._communityCards
                handId, best5 = self._bestHandFrom(allCards)
                handIds[seatIndex] = handId
                handCards[seatIndex] = best5
                scores[seatIndex] = self._scoreHand(best5)

            self._checkForCheaters()
        else:
            for seatIndex in self._activeBettors:
                scores[seatIndex] = [0]

        winnings = self._distributePot(scores)

        for seatIndex in range(self._availableSeats):
            if seatIndex not in self._handSeats:
                self._totalWinnings[seatIndex] = PlayingCardGlobals.PlayerInactive
            elif seatIndex in self._caughtCheating:
                self._totalWinnings[seatIndex] = PlayingCardGlobals.PlayerCaughtCheating
            elif winnings.get(seatIndex, 0) > 0:
                self._totalWinnings[seatIndex] = winnings[seatIndex]
            else:
                self._totalWinnings[seatIndex] = PlayingCardGlobals.PlayerLost

        for seatIndex in self._handSeats:
            self._payoutSeat(seatIndex, winnings.get(seatIndex, 0))

        # pirates without enough gold for another hand must leave the table...
        minChips = self._minChipsToPlay()
        for seatIndex in self._handSeats:
            if self._totalWinnings[seatIndex] <= PlayingCardGlobals.PlayerLost and \
                    self.isPlayerSeat(seatIndex) and self.getSeatGold(seatIndex) < minChips:
                self._totalWinnings[seatIndex] = PlayingCardGlobals.PlayerOutOfChips

        if self._showdown:
            self.d_setAllHandValues(handIds, handCards)
            for seatIndex in self._activeBettors:
                if self.isPlayerSeat(seatIndex):
                    self.sendUpdateToAvatarId(self.seats[seatIndex].doId, 'setLocalAvatarHandValue',
                        [handIds[seatIndex], handCards[seatIndex]])

        self._round = self.NumRounds
        self.b_setPotSize(0)
        self.d_setTableState()

        self._handActive = False
        taskMgr.doMethodLater(self.ShowdownDelay, self._startHandTask,
            self.uniqueName('poker-start'), appendTask=True)

    def _distributePot(self, scores):
        # side pots are created for any seat that was all-in for less than the others...
        winnings = {}
        eligible = [seatIndex for seatIndex in scores if seatIndex not in self._caughtCheating]
        if not eligible:
            # everyone left in the hand was caught cheating, the house keeps the pot
            return winnings

        contributions = dict(self._contributions)
        levels = sorted(set([amount for amount in contributions.values() if amount > 0]))
        previousLevel = 0
        for level in levels:
            potAmount = 0
            for seatIndex, amount in contributions.items():
                potAmount += max(0, min(amount, level) - previousLevel)

            contenders = [seatIndex for seatIndex in eligible
                          if contributions.get(seatIndex, 0) >= level]
            if not contenders:
                contenders = eligible

            bestScore = max([scores[seatIndex] for seatIndex in contenders])
            winners = [seatIndex for seatIndex in self.getSeatsAfter(self._buttonSeat, contenders)
                       if scores[seatIndex] == bestScore]

            share, remainder = divmod(potAmount, len(winners))
            for seatIndex in winners:
                winnings[seatIndex] = winnings.get(seatIndex, 0) + share

            # odd chips go to the first winner after the button
            if remainder:
                winnings[winners[0]] += remainder

            previousLevel = level

        return winnings

    def _payoutSeat(self, seatIndex, winnings):
        contribution = self._contributions.get(seatIndex, 0)
        if seatIndex in self._caughtCheating:
            fine = PlayingCardGlobals.CheatingFine
            if self.isPlayerSeat(seatIndex):
                fine = self.takeSeatGold(seatIndex, fine)
            self.notify.info('Seat %d was caught cheating and fined %d gold.' % (seatIndex, fine))
            return

        if winnings <= 0:
            return

        self._payChips(seatIndex, winnings)
        if not self.isPlayerSeat(seatIndex):
            return

        avatar = self.seats[seatIndex]
        profit = winnings - contribution
        if profit <= 0:
            return

        self.air.questMgr.pokerHandWon(avatar, profit)

        # track the pirate's poker winnings for the rankings...
        inventory = self.getSeatInventory(seatIndex)
        if inventory:
            current = inventory.getStackQuantity(InventoryType.PokerGame)
            inventory.b_setStackQuantity(InventoryType.PokerGame, min(current + profit, 9999))

    def _abortHand(self):
        taskMgr.remove(self.uniqueName('poker-turn'))
        taskMgr.remove(self.uniqueName('poker-timeout'))

        # return any chips the AI seats have in the pot
        for seatIndex, amount in self._contributions.items():
            if self.isAISeat(seatIndex):
                self._chipsCount[seatIndex] += amount

        self._handActive = False
        self._showdown = False
        self._handSeats = []
        self._activeBettors = []
        self._bettingOrder = []
        self._contributions = {}
        self._playerHands = self._normalizePlayerHands([])
        self._communityCards = []
        self._totalWinnings = [PlayingCardGlobals.PlayerInactive] * self._availableSeats
        self._round = 0
        self.b_setPotSize(0)
        self.d_setTableState()

    def _rankFiveCards(self, cards):
        # returns a sortable score for a hand of up to 5 cards, and the cards
        # sorted the way PLocalizer.getHandNameFull expects them...
        ranks = sorted([c % 13 for c in cards], reverse=True)
        suits = [c // 13 for c in cards]

        isFlush = len(cards) == 5 and len(set(suits)) == 1
        isStraight = False
        aceLow = False
        if len(cards) == 5 and len(set(ranks)) == 5:
            if ranks[0] - ranks[4] == 4:
                isStraight = True
            elif ranks == [12, 3, 2, 1, 0]:  # Ace-low straight
                isStraight = True
                aceLow = True
                ranks = [3, 2, 1, 0, -1]    # treat Ace as low for ordering

        cnt = Counter(ranks)
        groups = sorted(list(cnt.items()), key=lambda x: (x[1], x[0]), reverse=True)
        groupCounts = [c for _, c in groups]
        ordered = [r for r, c in groups for _ in range(c)]

        if isStraight and isFlush:
            handId = PlayingCardGlobals.StFlush
        elif groupCounts[0] == 4:
            handId = PlayingCardGlobals.Quads
        elif groupCounts[0] == 3 and len(groupCounts) > 1 and groupCounts[1] == 2:
            handId = PlayingCardGlobals.FlHouse
        elif isFlush:
            handId = PlayingCardGlobals.Flush
        elif isStraight:
            handId = PlayingCardGlobals.Straight
        elif groupCounts[0] == 3:
            handId = PlayingCardGlobals.Trips
        elif groupCounts[0] == 2 and len(groupCounts) > 1 and groupCounts[1] == 2:
            handId = PlayingCardGlobals.TwoPair
        elif groupCounts[0] == 2:
            handId = PlayingCardGlobals.OnePair
        else:
            handId = PlayingCardGlobals.NoPair

        # sort the actual cards to match the ordered ranks
        remaining = list(cards)
        sortedCards = []
        for rank in ordered:
            if aceLow and rank == -1:
                rank = 12

            for card in remaining:
                if card % 13 == rank:
                    sortedCards.append(card)
                    remaining.remove(card)
                    break

        return [handId] + ordered, sortedCards

    def _scoreHand(self, cards):
        score, _ = self._rankFiveCards(cards)
        return score

    def _bestHandFrom(self, cards):
        cards = [card for card in cards if card != PlayingCardGlobals.Unknown]
        if not cards:
            return PlayingCardGlobals.Nothing, []

        if len(cards) <= 5:
            score, hand = self._rankFiveCards(cards)
            return score[0], hand

        bestScore = None
        bestHand = None
        for combo in combinations(cards, 5):
            score, hand = self._rankFiveCards(list(combo))
            if bestScore is None or score > bestScore:
                bestScore = score
                bestHand = hand

        return bestScore[0], bestHand

    def getHandValue(self, seatIndex):
        return self._bestHandFrom(self._playerHands[seatIndex] + self._communityCards)

    CheatCardIndex = {
        PlayingCardGlobals.ReplaceHoleCardOneCheat: 0,
        PlayingCardGlobals.ReplaceHoleCardTwoCheat: 1,
        PlayingCardGlobals.ReplaceHoleCardSevenCheat: 6}

    def requestCheat(self, cheatType, cheatTarget):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        seatIndex = self.getAvatarSeatIndex(avatar)
        if seatIndex is None:
            return

        hand = list(self._playerHands[seatIndex])
        cardIndex = self.CheatCardIndex.get(cheatType, -1)
        if (not self._handActive or self._showdown or seatIndex not in self._activeBettors or
                seatIndex in self._cheaters or cardIndex < 0 or cardIndex >= len(hand) or
                not 0 <= cheatTarget < 52):
            self.d_cheatResponse(seatIndex, cheatType, cheatTarget, 0, hand)
            return

        # the card being swapped in must come from the pirate's inventory
        inv = self.air.inventoryManager.getInventory(avatar.doId)
        cardType = InventoryType.begin_Cards + cheatTarget
        quantity = inv.getStackQuantity(cardType) if inv else 0
        if quantity <= 0:
            self.air.logPotentialHacker(
                message='Requested poker card swap with card not in inventory',
                targetAvId=avatar.doId,
                cardId=cheatTarget)

            self.d_cheatResponse(seatIndex, cheatType, cheatTarget, 0, hand)
            return

        inv.b_setStackQuantity(cardType, quantity - 1)
        hand[cardIndex] = cheatTarget
        self._playerHands[seatIndex] = hand
        self._cheaters[seatIndex] = cheatTarget

        self.d_cheatResponse(seatIndex, cheatType, cheatTarget, 1, hand)
        if self._round > 1:
            self.d_setLocalAvatarHandValue(seatIndex)

    def _checkForCheaters(self):
        # anyone holding a card that turns up twice on the table
        # at the showdown has been caught cheating...
        for seatIndex, cheatCard in list(self._cheaters.items()):
            if seatIndex not in self._activeBettors:
                continue

            visibleCards = list(self._communityCards)
            for otherSeat in self._activeBettors:
                visibleCards += self._playerHands[otherSeat]

            if visibleCards.count(cheatCard) > 1:
                self._caughtCheating.add(seatIndex)

    def announceGenerate(self):
        DistributedGameTableAI.announceGenerate(self)
        self._seedAIChips()
        self._scheduleHandStart()
