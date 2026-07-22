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

    # Default ante list: [ante, small blind, big blind]
    DefaultAnteList = [5, 10, 20]
    # Number of betting rounds including round 0 (between hands)
    NumRounds = 5  # Holdem; 7Stud sub-class overrides
    GameType = PlayingCardGlobals.Holdem

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air)
        self.potSize = 0
        self.anteList = list(self.DefaultAnteList)
        self.betMultiplier = 1
        self.gameType = self.GameType

        # Table state components
        self._round = 0
        self._buttonSeat = 0
        self._communityCards = []
        self._playerHands = [[] for _ in range(self._availableSeats)]
        self._chipsCount = [0] * self._availableSeats
        self._totalWinnings = [PlayingCardGlobals.PlayerInactive] * self._availableSeats
        self._playerActions = [[PlayingCardGlobals.NoAction, 0]] * self._availableSeats
        self._maxBet = 0

        # Betting round tracking
        self._deck = []
        self._activeBettors = []  # seat indexes still in the hand
        self._bettingOrder = []   # remaining bettors this round
        self._timeouts = {}       # seatIndex -> consecutive timeout count

    def delete(self):
        taskMgr.remove(self.uniqueName('poker-turn'))
        taskMgr.remove(self.uniqueName('poker-timeout'))
        DistributedGameTableAI.delete(self)

    # ------------------------------------------------------------------
    # DC field accessors
    # ------------------------------------------------------------------

    def setGameType(self, gameType):
        self.gameType = gameType

    def getGameType(self):
        return self.gameType

    def setBetMultiplier(self, multiplier):
        self.betMultiplier = multiplier

    def d_setBetMultiplier(self, multiplier):
        self.sendUpdate('setBetMultiplier', [multiplier])

    def b_setBetMultiplier(self, multiplier):
        self.setBetMultiplier(multiplier)
        self.d_setBetMultiplier(multiplier)

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
        self._chipsCount = list(chipsCount)

    def d_setTableState(self):
        self.sendUpdate('setTableState', [
            self._round,
            self._buttonSeat,
            self._communityCards,
            self._playerHands,
            self._totalWinnings,
            self._chipsCount,
        ])

    def getTableState(self):
        return (self._round, self._buttonSeat, self._communityCards,
                self._playerHands, self._totalWinnings, self._chipsCount)

    def setPotSize(self, potSize):
        self.potSize = potSize

    def d_setPotSize(self, potSize):
        self.sendUpdate('setPotSize', [potSize])

    def b_setPotSize(self, potSize):
        self.setPotSize(potSize)
        self.d_setPotSize(potSize)

    def getPotSize(self):
        return self.potSize

    # ------------------------------------------------------------------
    # Seat lifecycle
    # ------------------------------------------------------------------

    def handleRequestInteraction(self, avatar, interactType, instant):
        # Enforce minimum chips to sit down
        minChips = 10 * (self.anteList[2] if len(self.anteList) >= 3 else
                         (self.anteList[0] if self.anteList else 20))
        inv = self.air.inventoryManager.getInventory(avatar.doId)
        if inv and inv.getGoldInPocket() < minChips:
            self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [4, 0])
            return self.DENY

        return DistributedGameTableAI.handleRequestInteraction(self, avatar, interactType, instant)

    def avatarSit(self, avatar, seatIndex):
        DistributedGameTableAI.avatarSit(self, avatar, seatIndex)
        inv = self.air.inventoryManager.getInventory(avatar.doId) if avatar not in (0, 1) else None
        self._chipsCount[seatIndex] = inv.getGoldInPocket() if inv else 0
        self._totalWinnings[seatIndex] = PlayingCardGlobals.PlayerLost

    def avatarStand(self, avatar, seatIndex):
        DistributedGameTableAI.avatarStand(self, avatar, seatIndex)
        self._totalWinnings[seatIndex] = PlayingCardGlobals.PlayerInactive
        self._chipsCount[seatIndex] = 0
        if seatIndex in self._activeBettors:
            self._activeBettors.remove(seatIndex)

    # ------------------------------------------------------------------
    # Hand management
    # ------------------------------------------------------------------

    def _buildDeck(self):
        self._deck = list(range(52))
        random.shuffle(self._deck)

    def _dealCard(self):
        return self._deck.pop()

    def _getOccupiedSeats(self):
        seats = []
        for i in range(self._availableSeats):
            if self.seats[i] is not None:
                seats.append(i)
        return seats

    def _startHand(self):
        self._buildDeck()
        self._playerHands = [[] for _ in range(self._availableSeats)]
        self._communityCards = []
        self._activeBettors = list(self._getOccupiedSeats())
        self._timeouts = {s: 0 for s in self._activeBettors}

        # Advance button
        occupied = self._getOccupiedSeats()
        if occupied:
            pos = occupied.index(self._buttonSeat) if self._buttonSeat in occupied else 0
            self._buttonSeat = occupied[(pos + 1) % len(occupied)]

        self._totalWinnings = [PlayingCardGlobals.PlayerInactive] * self._availableSeats
        for s in self._activeBettors:
            self._totalWinnings[s] = PlayingCardGlobals.PlayerLost

        self._collectBlindsAndAntes()
        self._dealInitialCards()
        self._broadcastTableState(1)
        self._broadcastPlayerHands()
        self._startBettingRound(2)

    def _collectBlindsAndAntes(self):
        occupied = self._activeBettors
        if not occupied:
            return

        ante = self.anteList[0] if self.anteList else 0
        smallBlind = self.anteList[1] if len(self.anteList) > 1 else 0
        bigBlind = self.anteList[2] if len(self.anteList) > 2 else 0

        buttonPos = occupied.index(self._buttonSeat) if self._buttonSeat in occupied else 0
        sbSeat = occupied[(buttonPos + 1) % len(occupied)]
        bbSeat = occupied[(buttonPos + 2) % len(occupied)]

        pot = 0
        for s in occupied:
            cost = self._deductChips(s, ante)
            pot += cost
            self._playerActions[s] = [PlayingCardGlobals.Ante, ante]

        # Post blinds
        self._deductChips(sbSeat, smallBlind)
        self._playerActions[sbSeat] = [PlayingCardGlobals.SmallBlind, smallBlind]
        pot += smallBlind

        self._deductChips(bbSeat, bigBlind)
        self._playerActions[bbSeat] = [PlayingCardGlobals.BigBlind, bigBlind]
        pot += bigBlind

        self._maxBet = bigBlind
        self.b_setPotSize(self.potSize + pot)

    def _deductChips(self, seatIndex, amount):
        amount = min(amount, self._chipsCount[seatIndex])
        self._chipsCount[seatIndex] -= amount
        return amount

    def _dealInitialCards(self):
        occupied = self._activeBettors
        # Holdem: 2 hole cards each; 7Stud sub-class overrides
        for _ in range(2):
            for s in occupied:
                self._playerHands[s].append(self._dealCard())

    def _broadcastTableState(self, round):
        self._round = round
        self.d_setTableState()

    def _broadcastPlayerHands(self):
        # Send each player their private hand; all others see face-down cards
        for seatIndex in self._activeBettors:
            seat = self.seats[seatIndex]
            if seat and seat not in (0, 1):
                self.sendUpdateToAvatarId(seat.doId, 'setLocalAvatarHand',
                    [self._playerHands[seatIndex]])

    # ------------------------------------------------------------------
    # Betting round
    # ------------------------------------------------------------------

    def _startBettingRound(self, round):
        self._round = round
        self._bettingOrder = list(self._activeBettors)

        # Community card dealing for Holdem
        if self.gameType == PlayingCardGlobals.Holdem:
            if round == 2:
                pass  # cards already dealt pre-flop
            elif round == 3:
                for _ in range(3):
                    self._communityCards.append(self._dealCard())
            elif round in (4, 5):
                self._communityCards.append(self._dealCard())

        self._broadcastTableState(round)
        self._broadcastPlayerActions()
        self._nextBettingAction()

    def _broadcastPlayerActions(self):
        self.sendUpdate('setPlayerActions', [
            self._maxBet,
            self._playerActions,
            self._chipsCount,
        ])

    def _nextBettingAction(self):
        taskMgr.remove(self.uniqueName('poker-timeout'))

        if not self._bettingOrder:
            self._onBettingRoundComplete()
            return

        seatIndex = self._bettingOrder[0]

        if self.seats[seatIndex] == 1:
            # AI acts after a short delay
            taskMgr.doMethodLater(1.5, self._aiActTask,
                self.uniqueName('poker-turn'), extraArgs=[seatIndex], appendTask=True)
        else:
            # Human: ask for action and start timeout
            self.sendUpdate('askForClientAction', [seatIndex])
            taskMgr.doMethodLater(
                PlayingCardGlobals.SecondsPerHand,
                self._playerTimeoutTask,
                self.uniqueName('poker-timeout'),
                extraArgs=[seatIndex], appendTask=True)

        self.sendUpdate('requestAIPlayerTurn', [seatIndex])

    def _playerTimeoutTask(self, seatIndex, task=None):
        self._timeouts[seatIndex] = self._timeouts.get(seatIndex, 0) + 1
        if self._timeouts[seatIndex] >= PlayingCardGlobals.MaximumTimeouts:
            self._applyAction(seatIndex, PlayingCardGlobals.Fold, 0)
        else:
            # Auto-check / call with zero
            self._applyAction(seatIndex, PlayingCardGlobals.CheckCall, 0)
        return Task.done

    def _aiActTask(self, seatIndex, task=None):
        self._aiDecide(seatIndex)
        return Task.done

    def _aiDecide(self, seatIndex):
        callAmount = max(0, self._maxBet - self._playerActions[seatIndex][1])
        chips = self._chipsCount[seatIndex]

        # Simple AI: call if can afford, otherwise fold
        if callAmount == 0:
            self._applyAction(seatIndex, PlayingCardGlobals.Check, 0)
        elif callAmount <= chips // 4:
            self._applyAction(seatIndex, PlayingCardGlobals.CheckCall, callAmount)
        elif chips > 0 and callAmount <= chips:
            self._applyAction(seatIndex, PlayingCardGlobals.CheckCall, callAmount)
        else:
            self._applyAction(seatIndex, PlayingCardGlobals.Fold, 0)

    def clientAction(self, round, action):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        seatIndex = self.getAvatarSeatIndex(avatar)
        if seatIndex is None:
            return

        taskMgr.remove(self.uniqueName('poker-timeout'))

        actionCode = action[0] if action else PlayingCardGlobals.Fold
        amount = action[1] if len(action) > 1 else 0
        self._applyAction(seatIndex, actionCode, amount)

    def _applyAction(self, seatIndex, actionCode, amount):
        if seatIndex not in self._bettingOrder:
            return

        self._bettingOrder.pop(0)

        if actionCode == PlayingCardGlobals.Fold:
            self._playerActions[seatIndex] = [PlayingCardGlobals.Fold, 0]
            if seatIndex in self._activeBettors:
                self._activeBettors.remove(seatIndex)
            # Remove remaining turns for this seat in this round
            while seatIndex in self._bettingOrder:
                self._bettingOrder.remove(seatIndex)

        elif actionCode in (PlayingCardGlobals.CheckCall, PlayingCardGlobals.AllIn):
            callAmount = max(0, self._maxBet - self._playerActions[seatIndex][1])
            paid = self._deductChips(seatIndex, callAmount)
            self.b_setPotSize(self.potSize + paid)
            self._playerActions[seatIndex] = [PlayingCardGlobals.CheckCall, self._maxBet]

        elif actionCode == PlayingCardGlobals.BetRaise:
            minBet = self.anteList[2] if len(self.anteList) > 2 else 2
            if self._round >= 3:
                minBet *= 2
            betAmount = max(minBet, amount)
            paid = self._deductChips(seatIndex, betAmount)
            self.b_setPotSize(self.potSize + paid)
            self._maxBet = self._playerActions[seatIndex][1] + paid
            self._playerActions[seatIndex] = [PlayingCardGlobals.BetRaise, self._maxBet]
            # Others who already acted need to act again
            for s in self._activeBettors:
                if s != seatIndex and s not in self._bettingOrder:
                    self._bettingOrder.append(s)

        elif actionCode == PlayingCardGlobals.Check:
            self._playerActions[seatIndex] = [PlayingCardGlobals.Check, 0]

        self._broadcastPlayerActions()
        self._broadcastTableState(self._round)

        if len(self._activeBettors) <= 1:
            self._endHand()
            return

        self._nextBettingAction()

    def _onBettingRoundComplete(self):
        taskMgr.remove(self.uniqueName('poker-turn'))
        nextRound = self._round + 1
        if nextRound > self.NumRounds or len(self._activeBettors) <= 1:
            self._endHand()
        else:
            taskMgr.doMethodLater(1.0, self._startNextRoundTask,
                self.uniqueName('poker-turn'), extraArgs=[nextRound], appendTask=True)

    def _startNextRoundTask(self, nextRound, task=None):
        self._maxBet = 0
        for s in self._activeBettors:
            self._playerActions[s] = [PlayingCardGlobals.NoAction, 0]
        self._startBettingRound(nextRound)
        return Task.done

    # ------------------------------------------------------------------
    # Showdown and payout
    # ------------------------------------------------------------------

    def _endHand(self):
        taskMgr.remove(self.uniqueName('poker-turn'))
        taskMgr.remove(self.uniqueName('poker-timeout'))

        if len(self._activeBettors) == 1:
            winner = self._activeBettors[0]
            self._payoutWinner(winner)
            return

        # Showdown
        bestScore = None
        winner = None
        handIds = [0] * self._availableSeats
        handCards = [[] for _ in range(self._availableSeats)]

        for seatIndex in self._activeBettors:
            allCards = self._playerHands[seatIndex] + self._communityCards
            handId, best5 = self._bestHandFrom(allCards)
            handIds[seatIndex] = handId
            handCards[seatIndex] = best5
            score = self._scoreHand(best5)
            if bestScore is None or score > bestScore:
                bestScore = score
                winner = seatIndex

        # Reveal hands
        self.sendUpdate('setAllHandValues', [handIds, handCards])
        for seatIndex in self._activeBettors:
            seat = self.seats[seatIndex]
            if seat and seat not in (0, 1):
                self.sendUpdateToAvatarId(seat.doId, 'setLocalAvatarHandValue',
                    [handIds[seatIndex], handCards[seatIndex]])

        self._payoutWinner(winner)

    def _payoutWinner(self, winnerSeat):
        seat = self.seats[winnerSeat]
        winnings = self.potSize

        if seat and seat not in (0, 1):
            inv = self.air.inventoryManager.getInventory(seat.doId)
            if inv:
                inv.addGoldInPocket(winnings)
                # Quest hook
                if hasattr(self.air, 'questMgr'):
                    self.air.questMgr.pokerHandWon(seat, winnings)
                # Reputation
                repInv = self.air.inventoryManager.getInventory(seat.doId)
                if repInv:
                    current = repInv.getAccumulators().get(InventoryType.PokerGame, 0)
                    repInv.b_setAccumulator(InventoryType.PokerGame,
                        min(current + winnings, 9999))

        self._totalWinnings[winnerSeat] = winnings
        for s in self._activeBettors:
            if s != winnerSeat:
                self._totalWinnings[s] = PlayingCardGlobals.PlayerLost

        self.b_setPotSize(0)
        self._broadcastTableState(self.NumRounds)

        # Start next hand after a pause
        taskMgr.doMethodLater(3.0, self._startHandTask,
            self.uniqueName('poker-turn'), appendTask=True)

    def _startHandTask(self, task=None):
        occupied = self._getOccupiedSeats()
        if len(occupied) >= 2:
            self._startHand()
        return Task.done

    # ------------------------------------------------------------------
    # Hand evaluator
    # ------------------------------------------------------------------

    def _rankFiveCards(self, cards):
        """Return a sortable score tuple for a 5-card hand."""
        ranks = sorted([c % 13 for c in cards], reverse=True)
        suits = [c // 13 for c in cards]

        is_flush = len(set(suits)) == 1

        is_straight = False
        if len(set(ranks)) == 5:
            if ranks[0] - ranks[4] == 4:
                is_straight = True
            elif ranks == [12, 3, 2, 1, 0]:  # Ace-low straight
                is_straight = True
                ranks = [3, 2, 1, 0, -1]    # treat Ace as low for ordering

        cnt = Counter(ranks)
        groups = sorted(cnt.items(), key=lambda x: (x[1], x[0]), reverse=True)
        group_counts = [c for _, c in groups]
        ordered = [r for r, c in groups for _ in range(c)]

        if is_straight and is_flush:
            handId = PlayingCardGlobals.StFlush
        elif group_counts[0] == 4:
            handId = PlayingCardGlobals.Quads
        elif group_counts[0] == 3 and group_counts[1] == 2:
            handId = PlayingCardGlobals.FlHouse
        elif is_flush:
            handId = PlayingCardGlobals.Flush
        elif is_straight:
            handId = PlayingCardGlobals.Straight
        elif group_counts[0] == 3:
            handId = PlayingCardGlobals.Trips
        elif group_counts[0] == 2 and len(group_counts) > 1 and group_counts[1] == 2:
            handId = PlayingCardGlobals.TwoPair
        elif group_counts[0] == 2:
            handId = PlayingCardGlobals.OnePair
        else:
            handId = PlayingCardGlobals.NoPair

        return [handId] + ordered, list(cards)

    def _scoreHand(self, cards):
        score, _ = self._rankFiveCards(cards)
        return score

    def _bestHandFrom(self, cards):
        """Find the best 5-card hand from any number of cards."""
        if len(cards) <= 5:
            handId = self._rankFiveCards(cards)[0][0]
            return handId, list(cards)

        bestScore = None
        bestHand = None
        for combo in combinations(cards, 5):
            score, hand = self._rankFiveCards(list(combo))
            if bestScore is None or score > bestScore:
                bestScore = score
                bestHand = hand

        return bestScore[0], bestHand

    # ------------------------------------------------------------------
    # Cheat handling
    # ------------------------------------------------------------------

    def requestCheat(self, cheatType, cheatTarget):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        seatIndex = self.getAvatarSeatIndex(avatar)
        if seatIndex is None:
            return

        inv = self.air.inventoryManager.getInventory(avatar.doId)
        if not inv:
            self.sendUpdateToAvatarId(avatar.doId, 'cheatResponse',
                [cheatType, cheatTarget, 0, []])
            return

        # Resolve which card to replace based on cheat type
        hand = list(self._playerHands[seatIndex])
        cardIndex = {PlayingCardGlobals.ReplaceHoleCardOneCheat: 0,
                     PlayingCardGlobals.ReplaceHoleCardTwoCheat: 1,
                     PlayingCardGlobals.ReplaceHoleCardSevenCheat: 6}.get(cheatType, -1)

        if cardIndex < 0 or cardIndex >= len(hand):
            self.sendUpdateToAvatarId(avatar.doId, 'cheatResponse',
                [cheatType, cheatTarget, 0, hand])
            return

        # Find the card in the player's inventory
        newCard = -1
        for cardId in range(52):
            qty = inv.getStackQuantity(InventoryType.begin_Cards + cardId)
            if qty > 0:
                newCard = cardId
                inv.b_setStackQuantity(InventoryType.begin_Cards + cardId, qty - 1)
                break

        if newCard < 0:
            self.sendUpdateToAvatarId(avatar.doId, 'cheatResponse',
                [cheatType, cheatTarget, 0, hand])
            return

        hand[cardIndex] = newCard
        self._playerHands[seatIndex] = hand
        self.sendUpdateToAvatarId(avatar.doId, 'cheatResponse',
            [cheatType, cheatTarget, 1, hand])
        self.sendUpdateToAvatarId(avatar.doId, 'setLocalAvatarHand', [hand])

    # ------------------------------------------------------------------
    # Table startup
    # ------------------------------------------------------------------

    def announceGenerate(self):
        DistributedGameTableAI.announceGenerate(self)
        self.sendUpdate('setAnteList', [self.anteList])
        self.d_setTableState()
        self.d_setPotSize(self.potSize)
