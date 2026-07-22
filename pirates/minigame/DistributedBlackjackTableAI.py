import random

from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.task.TaskManagerGlobal import *
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from pirates.minigame import PlayingCardGlobals
from pirates.uberdog.UberDogGlobals import InventoryType


class DistributedBlackjackTableAI(DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBlackjackTableAI')

    DealerSeat = 7  # Dealer is at the last index (one past the player seats)
    CheatingFine = PlayingCardGlobals.CheatingFine
    # Starting stack for AI seats so they can bid against the dealer.
    AIStartingChips = 200

    def __init__(self, air):
        # Original tables seat one AI pirate plus a separate dealer NPC.
        DistributedGameTableAI.__init__(self, air, numberAI=1)
        self.betMultiplier = 1

        # Per-seat state: each seat has a list of hands (for splits)
        self._allHands = [[[]] for _ in range(self._availableSeats + 1)]
        self._bids = {}       # seatIndex -> bid amount
        # Client updateStacks always indexes 0..NumSeats-1 (and pot may use +1),
        # so keep a full-length chips vector from generation onward.
        self._chipsCount = [0] * (self._availableSeats + 1)
        self._waitingBids = set()
        self._actionQueue = []
        self._deck = []
        self._deck2 = []      # second deck for reshuffle
        self._numSeats = self._availableSeats  # seats in use (dealer slot added)
        self._roundActive = False

    def delete(self):
        taskMgr.remove(self.uniqueName('bj-bid'))
        taskMgr.remove(self.uniqueName('bj-deal'))
        taskMgr.remove(self.uniqueName('bj-action'))
        taskMgr.remove(self.uniqueName('bj-start'))
        DistributedGameTableAI.delete(self)

    # ------------------------------------------------------------------
    # DC field accessors
    # ------------------------------------------------------------------

    def setBetMultiplier(self, multiplier):
        self.betMultiplier = multiplier

    def d_setBetMultiplier(self, multiplier):
        self.sendUpdate('setBetMultiplier', [multiplier])

    def b_setBetMultiplier(self, multiplier):
        self.setBetMultiplier(multiplier)
        self.d_setBetMultiplier(multiplier)

    def getBetMultiplier(self):
        return self.betMultiplier

    def setTableState(self, allHands, chipsCount):
        self._allHands = [list(h) for h in allHands]
        self._chipsCount = self._normalizeChipsCount(chipsCount)

    def d_setTableState(self):
        self._chipsCount = self._normalizeChipsCount(self._chipsCount)
        self.sendUpdate('setTableState', [self._allHands, self._chipsCount])

    def b_setTableState(self, allHands, chipsCount):
        self.setTableState(allHands, chipsCount)
        self.d_setTableState()

    def getTableState(self):
        return [self._allHands, self._normalizeChipsCount(self._chipsCount)]

    def _normalizeChipsCount(self, chipsCount=None):
        """Ensure chipsCount covers every player seat plus the dealer/pot slot."""
        needed = self._availableSeats + 1
        normalized = list(chipsCount or [])
        if len(normalized) < needed:
            normalized += [0] * (needed - len(normalized))
        elif len(normalized) > needed:
            normalized = normalized[:needed]
        return normalized

    # ------------------------------------------------------------------
    # Seat lifecycle
    # ------------------------------------------------------------------

    def avatarSit(self, avatar, seatIndex):
        DistributedGameTableAI.avatarSit(self, avatar, seatIndex)
        inv = self.air.inventoryManager.getInventory(avatar.doId) if avatar not in (0, 1) else None
        self._chipsCount = self._normalizeChipsCount(self._chipsCount)
        if inv:
            self._chipsCount[seatIndex] = inv.getGoldInPocket()
        elif avatar == 1:
            self._chipsCount[seatIndex] = max(self._chipsCount[seatIndex], self.AIStartingChips)
        else:
            self._chipsCount[seatIndex] = 0
        self.d_setTableState()
        self._scheduleRoundStart()

    def avatarStand(self, avatar, seatIndex):
        DistributedGameTableAI.avatarStand(self, avatar, seatIndex)
        self._bids.pop(seatIndex, None)
        self._waitingBids.discard(seatIndex)
        if seatIndex < len(self._chipsCount):
            self._chipsCount[seatIndex] = 0
        self.d_setTableState()

    # ------------------------------------------------------------------
    # Game lifecycle
    # ------------------------------------------------------------------

    def _buildDeck(self):
        self._deck = list(range(52)) * 2  # double deck
        random.shuffle(self._deck)

    def _dealCard(self):
        if not self._deck:
            self._buildDeck()
        return self._deck.pop()

    def _getTableBidAmount(self):
        return PlayingCardGlobals.BlackjackBidAmount * self.betMultiplier

    def _getOccupiedPlayerSeats(self):
        seats = []
        for i in range(self._availableSeats):
            if self.seats[i] is not None:
                seats.append(i)
        return seats

    def _seedAIChips(self):
        """Give AI seats a playable stack if they are empty or broke."""
        self._chipsCount = self._normalizeChipsCount(self._chipsCount)
        for seatIndex in self.getAIPlayers():
            if self._chipsCount[seatIndex] < self._getTableBidAmount():
                self._chipsCount[seatIndex] = self.AIStartingChips

    def _scheduleRoundStart(self, delay=1.0):
        """Start a round once seats are occupied and no hand is running."""
        if self._roundActive:
            return
        if not self._getOccupiedPlayerSeats():
            return
        taskMgr.remove(self.uniqueName('bj-start'))
        taskMgr.doMethodLater(delay, self._startRoundTask,
            self.uniqueName('bj-start'), appendTask=True)

    def _startRoundTask(self, task=None):
        if not self._roundActive and self._getOccupiedPlayerSeats():
            self._startRound()
        return Task.done

    def _startRound(self):
        occupied = self._getOccupiedPlayerSeats()
        if not occupied:
            self._roundActive = False
            return

        self._roundActive = True
        self._buildDeck()
        self._bids = {}
        self._actionQueue = []
        self._allHands = [[[]] for _ in range(self._availableSeats + 1)]  # +1 for dealer
        self._seedAIChips()
        self._chipsCount = self._normalizeChipsCount(self._chipsCount)

        self._collectBids()

    def _collectBids(self):
        occupied = self._getOccupiedPlayerSeats()
        if not occupied:
            self._roundActive = False
            return

        self._waitingBids = set(occupied)
        self._bids = {}
        bidAmount = self._getTableBidAmount()

        for seatIndex in occupied:
            if self.seats[seatIndex] == 1:
                # AI bids the default amount when it can afford it.
                if self._chipsCount[seatIndex] < bidAmount:
                    self._chipsCount[seatIndex] = self.AIStartingChips
                self._bids[seatIndex] = bidAmount
                self._waitingBids.discard(seatIndex)
                self.sendUpdate('setEvent', [seatIndex, [PlayingCardGlobals.Bid, bidAmount]])
            else:
                self.sendUpdate('setEvent', [seatIndex, [PlayingCardGlobals.AskForBid, 0]])

        # Start bid timeout
        taskMgr.doMethodLater(PlayingCardGlobals.BidTimeout + 1.0,
            self._bidTimeoutTask, self.uniqueName('bj-bid'), appendTask=True)

        self._checkAllBidsIn()

    def _bidTimeoutTask(self, task=None):
        # Auto-bid the minimum for anyone who hasn't bid
        for seatIndex in list(self._waitingBids):
            self._receiveBid(seatIndex, self._getTableBidAmount())
        return Task.done

    def _receiveBid(self, seatIndex, amount):
        bid = max(self._getTableBidAmount(), amount)
        inv = None
        seat = self.seats[seatIndex]
        if seat and seat not in (0, 1):
            inv = self.air.inventoryManager.getInventory(seat.doId)

        if inv and inv.getGoldInPocket() < bid:
            # Can't afford - stand them up
            self.avatarStand(seat, seatIndex)
            self._waitingBids.discard(seatIndex)
            self._checkAllBidsIn()
            return

        self._bids[seatIndex] = bid
        self._waitingBids.discard(seatIndex)
        self.sendUpdate('setEvent', [seatIndex, [PlayingCardGlobals.Bid, bid]])
        self._checkAllBidsIn()

    def _checkAllBidsIn(self):
        if self._waitingBids:
            return

        taskMgr.remove(self.uniqueName('bj-bid'))
        taskMgr.doMethodLater(PlayingCardGlobals.DealDelay,
            self._dealTask, self.uniqueName('bj-deal'), appendTask=True)

    def _dealTask(self, task=None):
        self._dealCards()
        return Task.done

    def _dealCards(self):
        occupied = list(self._bids.keys())
        dealerSeat = self._availableSeats

        # Deal two cards to each player and dealer
        for _ in range(2):
            for seatIndex in occupied:
                card = self._dealCard()
                self._allHands[seatIndex][0].append(card)
            self._allHands[dealerSeat][0].append(self._dealCard())

        # Second dealer card is face-down (Unknown)
        dealerVisible = [self._allHands[dealerSeat][0][0], PlayingCardGlobals.Unknown]
        self._allHands[dealerSeat][0] = dealerVisible

        self._broadcastTableState()
        taskMgr.doMethodLater(PlayingCardGlobals.DealCompleteDelay,
            self._startPlayerActionsTask, self.uniqueName('bj-action'), appendTask=True)

    def _startPlayerActionsTask(self, task=None):
        occupied = list(self._bids.keys())
        self._actionQueue = list(occupied)  # queue of seats still to act
        self._currentSplitIndex = {s: 0 for s in occupied}
        self._nextPlayerAction()
        return Task.done

    def _nextPlayerAction(self, task=None):
        taskMgr.remove(self.uniqueName('bj-action'))

        if not self._actionQueue:
            self._dealerPlay()
            return

        seatIndex = self._actionQueue[0]
        hand = self._getCurrentHand(seatIndex)
        handValue = self._handValue(hand)

        if handValue >= 21:
            # Auto-stay
            self.sendUpdate('setEvent', [seatIndex, [PlayingCardGlobals.AutoStay, handValue]])
            self._actionQueue.pop(0)
            self._nextPlayerAction()
            return

        if self.seats[seatIndex] == 1:
            # AI decision
            taskMgr.doMethodLater(1.0, self._aiBlackjackDecisionTask,
                self.uniqueName('bj-action'), extraArgs=[seatIndex], appendTask=True)
        else:
            self.sendUpdate('setEvent', [seatIndex, [PlayingCardGlobals.AskCard, 0]])
            taskMgr.doMethodLater(PlayingCardGlobals.AskCardTimeout + 1.0,
                self._playerActionTimeoutTask, self.uniqueName('bj-action'),
                extraArgs=[seatIndex], appendTask=True)

    def _playerActionTimeoutTask(self, seatIndex, task=None):
        # Auto-stay on timeout
        self._applyBlackjackAction(seatIndex, PlayingCardGlobals.Stay, 0)
        return Task.done

    def _aiBlackjackDecisionTask(self, seatIndex, task=None):
        hand = self._getCurrentHand(seatIndex)
        value = self._handValue(hand)
        # Simple AI: hit under 17, stay at 17+
        if value < 17:
            self._applyBlackjackAction(seatIndex, PlayingCardGlobals.Hit, 0)
        else:
            self._applyBlackjackAction(seatIndex, PlayingCardGlobals.Stay, 0)
        return Task.done

    def clientAction(self, action):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        seatIndex = self.getAvatarSeatIndex(avatar)
        if seatIndex is None:
            return

        taskMgr.remove(self.uniqueName('bj-action'))

        actionCode = action[0] if action else PlayingCardGlobals.Stay
        amount = action[1] if len(action) > 1 else 0

        if actionCode == PlayingCardGlobals.Bid:
            self._receiveBid(seatIndex, amount)
        else:
            self._applyBlackjackAction(seatIndex, actionCode, amount)

    def _applyBlackjackAction(self, seatIndex, actionCode, amount):
        if not self._actionQueue or self._actionQueue[0] != seatIndex:
            return

        hand = self._getCurrentHand(seatIndex)
        self.sendUpdate('setEvent', [seatIndex, [actionCode, amount]])

        if actionCode == PlayingCardGlobals.Hit:
            hand.append(self._dealCard())
            value = self._handValue(hand)
            self._broadcastTableState()
            if value >= 21:
                self._actionQueue.pop(0)
                self._nextPlayerAction()
            else:
                # Ask again
                taskMgr.doMethodLater(0.5, self._nextPlayerAction, self.uniqueName('bj-action'))

        elif actionCode == PlayingCardGlobals.Stay:
            self._actionQueue.pop(0)
            self._nextPlayerAction()

        elif actionCode == PlayingCardGlobals.DoubleDown:
            bid = self._bids.get(seatIndex, 0)
            self._bids[seatIndex] = bid * 2
            hand.append(self._dealCard())
            self._broadcastTableState()
            self._actionQueue.pop(0)
            self._nextPlayerAction()

        elif actionCode == PlayingCardGlobals.Split:
            if len(hand) == 2:
                # Split into two hands
                card2 = hand.pop()
                newHand = [card2, self._dealCard()]
                hand.append(self._dealCard())
                self._allHands[seatIndex].append(newHand)
                self._broadcastTableState()
                # Put seat back in queue for second hand
                self._actionQueue.insert(1, seatIndex)
            self._actionQueue.pop(0)
            self._nextPlayerAction()

        else:
            # Default: stay
            self._actionQueue.pop(0)
            self._nextPlayerAction()

    def _getCurrentHand(self, seatIndex):
        hands = self._allHands[seatIndex]
        # Current hand: last hand with fewer than 2 final cards, or first hand
        for hand in reversed(hands):
            if len(hand) < 2:
                return hand
        return hands[-1] if hands else []

    # ------------------------------------------------------------------
    # Dealer plays
    # ------------------------------------------------------------------

    def _dealerPlay(self):
        dealerSeat = self._availableSeats
        dealerHand = self._allHands[dealerSeat][0]

        # Reveal dealer hole card
        if len(dealerHand) >= 2 and dealerHand[1] == PlayingCardGlobals.Unknown:
            dealerHand[1] = self._dealCard()

        # Dealer hits until 17
        while self._handValue(dealerHand) < 17:
            dealerHand.append(self._dealCard())

        self._broadcastTableState()
        taskMgr.doMethodLater(PlayingCardGlobals.PayOutDelay,
            self._payoutTask, self.uniqueName('bj-deal'), appendTask=True)

    def _payoutTask(self, task=None):
        self._payout()
        return Task.done

    # ------------------------------------------------------------------
    # Payout
    # ------------------------------------------------------------------

    def _payout(self):
        dealerSeat = self._availableSeats
        dealerValue = self._handValue(self._allHands[dealerSeat][0])
        dealerBlackjack = self._isBlackjack(self._allHands[dealerSeat][0])
        results = [0] * self._availableSeats

        for seatIndex, bid in self._bids.items():
            seat = self.seats[seatIndex]
            totalWin = 0

            for hand in self._allHands[seatIndex]:
                playerValue = self._handValue(hand)
                playerBJ = self._isBlackjack(hand) and len(self._allHands[seatIndex]) == 1

                if playerValue > 21:
                    # Bust
                    win = -bid
                elif dealerBlackjack and not playerBJ:
                    win = -bid
                elif playerBJ and not dealerBlackjack:
                    win = int(bid * 1.5)  # Blackjack pays 3:2
                elif playerValue > dealerValue or dealerValue > 21:
                    win = bid
                elif playerValue == dealerValue:
                    win = 0  # Push
                else:
                    win = -bid

                totalWin += win

            results[seatIndex] = totalWin

            if seat and seat not in (0, 1):
                inv = self.air.inventoryManager.getInventory(seat.doId)
                if inv:
                    # Deduct bid then apply result
                    inv.setGoldInPocket(inv.getGoldInPocket() - bid)
                    if totalWin > 0:
                        inv.addGoldInPocket(bid + totalWin)

                    if totalWin > 0:
                        # Quest hook
                        if hasattr(self.air, 'questMgr'):
                            self.air.questMgr.blackjackHandWon(seat, totalWin)
                        # Reputation
                        current = 0
                        accumulators = inv.getAccumulators()
                        for accType, qty in accumulators:
                            if accType == InventoryType.BlackjackGame:
                                current = qty
                                break
                        inv.b_setAccumulator(InventoryType.BlackjackGame,
                            min(current + totalWin, 9999))

                    self._chipsCount[seatIndex] = inv.getGoldInPocket()
            elif seat == 1:
                # AI stack is table-local; apply net result and top up if broke.
                self._chipsCount[seatIndex] = max(0, self._chipsCount[seatIndex] + totalWin)
                if self._chipsCount[seatIndex] < self._getTableBidAmount():
                    self._chipsCount[seatIndex] = self.AIStartingChips

        self._chipsCount = self._normalizeChipsCount(self._chipsCount)
        self.sendUpdate('setHandResults', [results])
        self._broadcastTableState()
        self._roundActive = False

        taskMgr.doMethodLater(3.0, self._nextRoundTask,
            self.uniqueName('bj-deal'), appendTask=True)

    def _nextRoundTask(self, task=None):
        occupied = self._getOccupiedPlayerSeats()
        if occupied:
            self._startRound()
        else:
            self._roundActive = False
        return Task.done

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

        hand = self._getCurrentHand(seatIndex)
        if not hand:
            self.sendUpdateToAvatarId(avatar.doId, 'cheatResponse',
                [cheatType, cheatTarget, 0, []])
            return

        inv = self.air.inventoryManager.getInventory(avatar.doId)
        if not inv:
            self.sendUpdateToAvatarId(avatar.doId, 'cheatResponse',
                [cheatType, cheatTarget, 0, hand])
            return

        # Find a usable card from inventory
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

        if len(hand) >= 1:
            hand[0] = newCard
        self._broadcastTableState()
        self.sendUpdateToAvatarId(avatar.doId, 'cheatResponse',
            [cheatType, cheatTarget, 1, hand])

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _handValue(self, hand):
        # rank = card % 13: 0=2, 1=3, ..., 7=9, 8=10, 9=J, 10=Q, 11=K, 12=Ace
        value = 0
        aces = 0
        for card in hand:
            if card == PlayingCardGlobals.Unknown:
                continue
            rank = card % 13
            if rank == 12:   # Ace
                value += 11
                aces += 1
            elif rank >= 8:  # 10, J, Q, K
                value += 10
            else:
                value += rank + 2  # 0=2, 1=3, ..., 7=9

        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        return value

    def _isBlackjack(self, hand):
        if len(hand) != 2:
            return False
        return self._handValue(hand) == 21

    def _broadcastTableState(self):
        self.d_setTableState()

    def announceGenerate(self):
        DistributedGameTableAI.announceGenerate(self)
        self._seedAIChips()
        self._allHands = [[[]] for _ in range(self._availableSeats + 1)]
        self.sendUpdate('setBetMultiplier', [self.betMultiplier])
        self.d_setTableState()
        # Original tables deal once AI/players are seated.
        self._scheduleRoundStart(delay=2.0)
