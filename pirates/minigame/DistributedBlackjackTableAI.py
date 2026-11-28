import random

from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.task.TaskManagerGlobal import *
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from pirates.minigame import PlayingCardGlobals
from pirates.uberdog.UberDogGlobals import InventoryType


class DistributedBlackjackTableAI(DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBlackjackTableAI')

    CheatingFine = PlayingCardGlobals.CheatingFine
    # the stack AI seats bid against the dealer from
    AIStartingChips = 200
    # the client bid slider tops out at 50 times the bet multiplier
    MaxBidMultiplier = 50
    DealerStandValue = 17
    # how long past the client timers we wait before acting for it
    TimeoutPadding = 3.0
    NextRoundDelay = 4.0
    AIThinkTime = (1.0, 2.0)

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air, numberAI=1)
        self.betMultiplier = 1
        self.DealerSeat = self._availableSeats

        # each seat has a list of hands for splits, the last entry is the dealer's hand...
        self._allHands = [[[]] for _ in range(self._availableSeats + 1)]
        self._bids = {}             # seatIndex -> [bid per hand]
        self._chipsCount = [0] * (self._availableSeats + 1)
        self._waitingBids = set()
        self._actionQueue = []      # seats still to play this round
        self._currentHand = {}      # seatIndex -> index of the hand being played
        self._finishedHands = {}    # seatIndex -> set of hand indexes that are done
        self._deck = []
        self._dealerHoleCard = None
        self._roundActive = False
        self._bidding = False
        self._cheaters = {}         # seatIndex -> swapped in card
        self._caughtCheating = set()
        self._missedBids = {}       # seatIndex -> consecutive rounds without bidding

    def delete(self):
        taskMgr.remove(self.uniqueName('bj-bid'))
        taskMgr.remove(self.uniqueName('bj-deal'))
        taskMgr.remove(self.uniqueName('bj-action'))
        taskMgr.remove(self.uniqueName('bj-start'))
        DistributedGameTableAI.delete(self)

    def setBetMultiplier(self, multiplier):
        self.betMultiplier = max(1, multiplier)

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
        self.sendUpdate('setTableState', self.getTableState())

    def getTableState(self):
        self._updateChipsCount()
        hands = [[list(hand) for hand in seatHands] for seatHands in self._allHands]
        return [hands, list(self._chipsCount)]

    def d_setEvent(self, seatIndex, action, amount=0):
        self.sendUpdate('setEvent', [seatIndex, [action, amount]])

    def d_setHandResults(self, results):
        self.sendUpdate('setHandResults', [results])

    def _normalizeChipsCount(self, chipsCount=None):
        needed = self._availableSeats + 1
        normalized = list(chipsCount or [])
        if len(normalized) < needed:
            normalized += [0] * (needed - len(normalized))
        elif len(normalized) > needed:
            normalized = normalized[:needed]
        return normalized

    def _updateChipsCount(self):
        self._chipsCount = self._normalizeChipsCount(self._chipsCount)
        for seatIndex in range(self._availableSeats):
            if self.isPlayerSeat(seatIndex):
                self._chipsCount[seatIndex] = self.getSeatGold(seatIndex)
            elif not self.isAISeat(seatIndex):
                self._chipsCount[seatIndex] = 0

    def avatarSit(self, avatar, seatIndex):
        DistributedGameTableAI.avatarSit(self, avatar, seatIndex)
        self._missedBids[seatIndex] = 0
        self.d_setTableState()
        self._scheduleRoundStart()

    def avatarStand(self, avatar, seatIndex):
        DistributedGameTableAI.avatarStand(self, avatar, seatIndex)

        # anything bid on the hand in play is forfeit to the house
        self._bids.pop(seatIndex, None)
        self._waitingBids.discard(seatIndex)
        self._missedBids.pop(seatIndex, None)
        self._cheaters.pop(seatIndex, None)
        self._allHands[seatIndex] = [[]]
        self._chipsCount[seatIndex] = 0

        wasActing = self._actionQueue and self._actionQueue[0] == seatIndex
        while seatIndex in self._actionQueue:
            self._actionQueue.remove(seatIndex)

        self.d_setTableState()
        if not self._roundActive:
            return

        if not self.getPlayerSeats():
            self._abortRound()
        elif self._bidding:
            self._checkAllBidsIn()
        elif wasActing:
            self._nextPlayerAction()

    def _buildDeck(self):
        self._deck = list(range(52))
        random.shuffle(self._deck)

    def _dealCard(self):
        if not self._deck:
            # reshuffle everything that isn't on the table
            inPlay = set()
            for seatHands in self._allHands:
                for hand in seatHands:
                    inPlay.update(hand)
            inPlay.add(self._dealerHoleCard)
            self._deck = [card for card in range(52) if card not in inPlay]
            random.shuffle(self._deck)

        return self._deck.pop()

    def _getTableBidAmount(self):
        return PlayingCardGlobals.BlackjackBidAmount * self.betMultiplier

    def _getMaxBidAmount(self):
        return self.MaxBidMultiplier * self.betMultiplier

    def getSeatChips(self, seatIndex):
        if self.isPlayerSeat(seatIndex):
            return self.getSeatGold(seatIndex)
        elif self.isAISeat(seatIndex):
            return self._chipsCount[seatIndex]

        return 0

    def _takeChips(self, seatIndex, amount):
        if self.isPlayerSeat(seatIndex):
            return self.takeSeatGold(seatIndex, amount)
        elif self.isAISeat(seatIndex):
            amount = min(amount, self._chipsCount[seatIndex])
            self._chipsCount[seatIndex] -= amount
            return amount

        return 0

    def _payChips(self, seatIndex, amount):
        if amount <= 0:
            return

        if self.isPlayerSeat(seatIndex):
            self.giveSeatGold(seatIndex, amount)
        elif self.isAISeat(seatIndex):
            self._chipsCount[seatIndex] += amount

    def _seedAIChips(self):
        self._chipsCount = self._normalizeChipsCount(self._chipsCount)
        for seatIndex in self.getAIPlayers():
            if self._chipsCount[seatIndex] < self._getTableBidAmount():
                self._chipsCount[seatIndex] = self.AIStartingChips * self.betMultiplier

    def _scheduleRoundStart(self, delay=1.0):
        if self._roundActive:
            return

        if not self.getPlayerSeats():
            return

        taskMgr.remove(self.uniqueName('bj-start'))
        taskMgr.doMethodLater(delay, self._startRoundTask,
            self.uniqueName('bj-start'), appendTask=True)

    def _startRoundTask(self, task=None):
        if not self._roundActive and self.getPlayerSeats():
            self._startRound()

        return Task.done

    def _startRound(self):
        self._roundActive = True
        self._buildDeck()
        self._bids = {}
        self._actionQueue = []
        self._currentHand = {}
        self._finishedHands = {}
        self._cheaters = {}
        self._caughtCheating = set()
        self._dealerHoleCard = None
        self._allHands = [[[]] for _ in range(self._availableSeats + 1)]
        self._seedAIChips()
        self.d_setTableState()
        self._collectBids()

    def _collectBids(self):
        occupied = self.getOccupiedSeats()
        if not occupied:
            self._roundActive = False
            return

        self._waitingBids = set()
        self._bidding = True
        bidAmount = self._getTableBidAmount()

        for seatIndex in occupied:
            if self.isAISeat(seatIndex):
                # the AI bids the default amount, a little more when it's flush...
                bid = bidAmount
                if self._chipsCount[seatIndex] > bidAmount * 20 and random.random() < 0.3:
                    bid = bidAmount * random.randint(2, 5)
                self._placeBid(seatIndex, bid)
            else:
                self._waitingBids.add(seatIndex)
                self.d_setEvent(seatIndex, PlayingCardGlobals.AskForBid, 0)

        taskMgr.doMethodLater(PlayingCardGlobals.BidTimeout + self.TimeoutPadding,
            self._bidTimeoutTask, self.uniqueName('bj-bid'), appendTask=True)

        self._checkAllBidsIn()

    def _bidTimeoutTask(self, task=None):
        # anyone who hasn't bid sits this round out
        for seatIndex in list(self._waitingBids):
            self._sitOutRound(seatIndex)

        self._waitingBids = set()
        self._checkAllBidsIn()
        return Task.done

    def _sitOutRound(self, seatIndex):
        self._waitingBids.discard(seatIndex)
        self.d_setEvent(seatIndex, PlayingCardGlobals.Bid, 0)
        self._missedBids[seatIndex] = self._missedBids.get(seatIndex, 0) + 1
        if self._missedBids[seatIndex] > PlayingCardGlobals.MaximumTimeouts:
            # the pirate has walked away from the table
            self.standPlayer(seatIndex)

    def _receiveBid(self, seatIndex, amount):
        if seatIndex not in self._waitingBids:
            return

        self._waitingBids.discard(seatIndex)
        self._missedBids[seatIndex] = 0
        bid = min(max(self._getTableBidAmount(), amount), self._getMaxBidAmount())
        if self.getSeatChips(seatIndex) < self._getTableBidAmount():
            self.d_setEvent(seatIndex, PlayingCardGlobals.Bid, 0)
        else:
            self._placeBid(seatIndex, min(bid, self.getSeatChips(seatIndex)))

        self._checkAllBidsIn()

    def _placeBid(self, seatIndex, bid):
        bid = self._takeChips(seatIndex, bid)
        if bid <= 0:
            self.d_setEvent(seatIndex, PlayingCardGlobals.Bid, 0)
            return

        self._bids[seatIndex] = [bid]
        self.d_setEvent(seatIndex, PlayingCardGlobals.Bid, bid)

    def _checkAllBidsIn(self):
        if self._waitingBids:
            return

        taskMgr.remove(self.uniqueName('bj-bid'))
        self._bidding = False
        if not [seatIndex for seatIndex in self._bids if self.isPlayerSeat(seatIndex)]:
            # no pirate bid on this round; refund the AI and try again later.
            self._abortRound()
            self._scheduleRoundStart(self.NextRoundDelay)
            return

        taskMgr.doMethodLater(PlayingCardGlobals.DealDelay,
            self._dealTask, self.uniqueName('bj-deal'), appendTask=True)

    def _dealTask(self, task=None):
        self._dealCards()
        return Task.done

    def _getBiddingSeats(self):
        return sorted(self._bids.keys())

    def _dealCards(self):
        bidders = self._getBiddingSeats()

        # the dealer's second card is dealt face down...
        for i in range(2):
            for seatIndex in bidders:
                self._allHands[seatIndex][0].append(self._dealCard())

            if i == 0:
                self._allHands[self.DealerSeat][0].append(self._dealCard())
            else:
                self._dealerHoleCard = self._dealCard()
                self._allHands[self.DealerSeat][0].append(PlayingCardGlobals.Unknown)

        for seatIndex in bidders:
            self._currentHand[seatIndex] = 0
            self._finishedHands[seatIndex] = set()

        self.d_setTableState()

        if self._isBlackjack(self._getDealerHand()):
            # the dealer peeks at a blackjack, nobody gets to play
            delay = PlayingCardGlobals.DealCompleteDelay * len(bidders)
            taskMgr.doMethodLater(delay, self._dealerPlayTask,
                self.uniqueName('bj-action'), appendTask=True)
            return

        delay = PlayingCardGlobals.DealCompleteDelay * (len(bidders) + 1)
        taskMgr.doMethodLater(delay, self._startPlayerActionsTask,
            self.uniqueName('bj-action'), appendTask=True)

    def _getDealerHand(self):
        hand = list(self._allHands[self.DealerSeat][0])
        if self._dealerHoleCard is not None and PlayingCardGlobals.Unknown in hand:
            hand[hand.index(PlayingCardGlobals.Unknown)] = self._dealerHoleCard

        return hand

    def _startPlayerActionsTask(self, task=None):
        self._actionQueue = self._getBiddingSeats()
        self._nextPlayerAction()
        return Task.done

    def _nextPlayerAction(self, task=None):
        taskMgr.remove(self.uniqueName('bj-action'))

        while self._actionQueue:
            seatIndex = self._actionQueue[0]
            if seatIndex not in self._bids:
                self._actionQueue.pop(0)
                continue

            hand = self._getCurrentHand(seatIndex)
            if len(hand) < 2:
                # second hand of a split, it gets it's next card now
                hand.append(self._dealCard())
                self.d_setTableState()

            if self._handValue(hand) >= 21:
                if not self._advanceHand(seatIndex):
                    self._actionQueue.pop(0)
                continue

            break

        if not self._actionQueue:
            self._dealerPlay()
            return

        seatIndex = self._actionQueue[0]
        if self.isAISeat(seatIndex):
            self.d_setEvent(seatIndex, PlayingCardGlobals.AskCard, 0)
            taskMgr.doMethodLater(random.uniform(*self.AIThinkTime), self._aiBlackjackDecisionTask,
                self.uniqueName('bj-action'), extraArgs=[seatIndex], appendTask=True)
        else:
            self.d_setEvent(seatIndex, PlayingCardGlobals.AskCard, 0)
            taskMgr.doMethodLater(PlayingCardGlobals.AskCardTimeout + self.TimeoutPadding,
                self._playerActionTimeoutTask, self.uniqueName('bj-action'),
                extraArgs=[seatIndex], appendTask=True)

    def _nextPlayerActionTask(self, task=None):
        self._nextPlayerAction()
        return Task.done

    def _advanceHand(self, seatIndex):
        # returns True if the seat still has a split hand left to play...
        self._finishedHands.setdefault(seatIndex, set()).add(self._currentHand.get(seatIndex, 0))
        hands = self._allHands[seatIndex]
        for handIndex in range(len(hands)):
            if handIndex not in self._finishedHands[seatIndex]:
                self._currentHand[seatIndex] = handIndex
                return True

        return False

    def _playerActionTimeoutTask(self, seatIndex, task=None):
        self._applyBlackjackAction(seatIndex, PlayingCardGlobals.Stay, 0)
        return Task.done

    def _aiBlackjackDecisionTask(self, seatIndex, task=None):
        hand = self._getCurrentHand(seatIndex)
        value = self._handValue(hand)
        dealerUp = self._handValue(self._allHands[self.DealerSeat][0][:1])
        bid = self._bids[seatIndex][self._currentHand[seatIndex]]

        if len(hand) == 2 and value in (10, 11) and dealerUp < value and \
                self.getSeatChips(seatIndex) >= bid:
            self._applyBlackjackAction(seatIndex, PlayingCardGlobals.DoubleDown, bid)
        elif value < 12 or (value < 17 and dealerUp >= 7):
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

        actionCode = action[0] if action else PlayingCardGlobals.Stay
        amount = action[1] if len(action) > 1 else 0

        if actionCode == PlayingCardGlobals.Bid:
            self._receiveBid(seatIndex, amount)
        else:
            self._applyBlackjackAction(seatIndex, actionCode, amount)

    def _applyBlackjackAction(self, seatIndex, actionCode, amount):
        if not self._actionQueue or self._actionQueue[0] != seatIndex:
            return

        taskMgr.remove(self.uniqueName('bj-action'))
        hand = self._getCurrentHand(seatIndex)
        handIndex = self._currentHand.get(seatIndex, 0)
        bid = self._bids[seatIndex][handIndex]

        if actionCode == PlayingCardGlobals.DoubleDown and \
                (len(hand) != 2 or self.getSeatChips(seatIndex) < bid):
            actionCode = PlayingCardGlobals.Hit

        if actionCode == PlayingCardGlobals.Split and \
                (len(hand) != 2 or not self._isSplittable(hand) or self.getSeatChips(seatIndex) < bid):
            actionCode = PlayingCardGlobals.Hit

        if actionCode == PlayingCardGlobals.Hit:
            self.d_setEvent(seatIndex, PlayingCardGlobals.Hit, 0)
            hand.append(self._dealCard())
            self.d_setTableState()
            if self._handValue(hand) >= 21:
                self._finishHand(seatIndex)
            else:
                self._askAgain(seatIndex)

        elif actionCode == PlayingCardGlobals.DoubleDown:
            self.d_setEvent(seatIndex, PlayingCardGlobals.DoubleDown, bid)
            self._bids[seatIndex][handIndex] += self._takeChips(seatIndex, bid)
            hand.append(self._dealCard())
            self.d_setTableState()
            self._finishHand(seatIndex)

        elif actionCode == PlayingCardGlobals.Split:
            self.d_setEvent(seatIndex, PlayingCardGlobals.Split, bid)
            self._bids[seatIndex].append(self._takeChips(seatIndex, bid))
            card = hand.pop()
            self._allHands[seatIndex].append([card])
            hand.append(self._dealCard())
            self.d_setTableState()
            if self._handValue(hand) >= 21:
                self._finishHand(seatIndex)
            else:
                self._askAgain(seatIndex)

        else:
            # stay, auto stay and anything we don't understand...
            self.d_setEvent(seatIndex, PlayingCardGlobals.Stay, 0)
            self._finishHand(seatIndex)

    def _askAgain(self, seatIndex):
        taskMgr.doMethodLater(0.5, self._nextPlayerActionTask,
            self.uniqueName('bj-action'), appendTask=True)

    def _finishHand(self, seatIndex):
        if not self._advanceHand(seatIndex):
            self._actionQueue.pop(0)

        taskMgr.doMethodLater(PlayingCardGlobals.DealDelay, self._nextPlayerActionTask,
            self.uniqueName('bj-action'), appendTask=True)

    def _getCurrentHand(self, seatIndex):
        hands = self._allHands[seatIndex]
        handIndex = self._currentHand.get(seatIndex, 0)
        if handIndex >= len(hands):
            handIndex = len(hands) - 1

        return hands[handIndex]

    def _dealerPlayTask(self, task=None):
        self._dealerPlay()
        return Task.done

    def _dealerPlay(self):
        taskMgr.remove(self.uniqueName('bj-action'))

        dealerHand = self._getDealerHand()
        self._allHands[self.DealerSeat][0] = dealerHand
        self._dealerHoleCard = None

        # the dealer only draws when somebody is still standing...
        live = False
        for seatIndex in self._bids:
            for hand in self._allHands[seatIndex]:
                if self._handValue(hand) <= 21:
                    live = True

        if live and not self._isBlackjack(dealerHand):
            while self._handValue(dealerHand) < self.DealerStandValue:
                dealerHand.append(self._dealCard())

        self.d_setEvent(self.DealerSeat, PlayingCardGlobals.Stay, 0)
        self.d_setTableState()
        taskMgr.doMethodLater(PlayingCardGlobals.PayOutDelay * len(dealerHand),
            self._payoutTask, self.uniqueName('bj-deal'), appendTask=True)

    def _payoutTask(self, task=None):
        self._payout()
        return Task.done

    def _getHandPayout(self, hand, bid, split, dealerHand):
        playerValue = self._handValue(hand)
        dealerValue = self._handValue(dealerHand)
        playerBJ = self._isBlackjack(hand) and not split
        dealerBJ = self._isBlackjack(dealerHand)

        if playerValue > 21:
            return 0
        elif playerBJ and dealerBJ:
            return bid
        elif dealerBJ:
            return 0
        elif playerBJ:
            # blackjack pays 3:2...
            return bid + (bid * 3) // 2
        elif dealerValue > 21 or playerValue > dealerValue:
            return bid * 2
        elif playerValue == dealerValue:
            return bid

        return 0

    def _payout(self):
        dealerHand = self._allHands[self.DealerSeat][0]
        self._checkForCheaters()
        results = [0] * self._availableSeats

        for seatIndex in self._getBiddingSeats():
            bids = self._bids[seatIndex]
            hands = self._allHands[seatIndex]
            split = len(hands) > 1
            totalBid = sum(bids)

            if seatIndex in self._caughtCheating:
                # the bid is forfeit, the fine was taken when they were caught
                results[seatIndex] = PlayingCardGlobals.PlayerCaughtCheating
                continue

            totalPayout = 0
            for handIndex in range(len(hands)):
                totalPayout += self._getHandPayout(hands[handIndex], bids[handIndex], split, dealerHand)

            self._payChips(seatIndex, totalPayout)
            profit = totalPayout - totalBid
            results[seatIndex] = profit
            if profit > 0 and self.isPlayerSeat(seatIndex):
                avatar = self.seats[seatIndex]
                self.air.questMgr.blackjackHandWon(avatar, profit)

                # track the pirate's blackjack winnings for the rankings...
                inventory = self.getSeatInventory(seatIndex)
                if inventory:
                    current = inventory.getStackQuantity(InventoryType.BlackjackGame)
                    inventory.b_setStackQuantity(InventoryType.BlackjackGame, min(current + profit, 9999))

        self._seedAIChips()
        self.d_setHandResults(results)
        self.d_setTableState()
        self._roundActive = False
        self._bids = {}

        taskMgr.doMethodLater(self.NextRoundDelay, self._nextRoundTask,
            self.uniqueName('bj-start'), appendTask=True)

    def _nextRoundTask(self, task=None):
        if self.getPlayerSeats():
            self._startRound()
        else:
            self._roundActive = False

        return Task.done

    def _abortRound(self):
        taskMgr.remove(self.uniqueName('bj-bid'))
        taskMgr.remove(self.uniqueName('bj-deal'))
        taskMgr.remove(self.uniqueName('bj-action'))

        # the AI gets it's bids back; pirates that left forfeit theirs
        for seatIndex, bids in list(self._bids.items()):
            if self.isAISeat(seatIndex) or self.isPlayerSeat(seatIndex):
                self._payChips(seatIndex, sum(bids))

        self._bids = {}
        self._waitingBids = set()
        self._bidding = False
        self._actionQueue = []
        self._dealerHoleCard = None
        self._allHands = [[[]] for _ in range(self._availableSeats + 1)]
        self._roundActive = False
        self.d_setTableState()

    def requestCheat(self, cheatType, cheatTarget):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        seatIndex = self.getAvatarSeatIndex(avatar)
        if seatIndex is None:
            return

        hand = self._getCurrentHand(seatIndex)
        cardIndex = {PlayingCardGlobals.ReplaceHoleCardOneCheat: 0,
                     PlayingCardGlobals.ReplaceHoleCardTwoCheat: 1}.get(cheatType, -1)

        # card swaps are only allowed while it's the pirate's turn
        if (not self._actionQueue or self._actionQueue[0] != seatIndex or seatIndex in self._cheaters or
                cardIndex < 0 or cardIndex >= len(hand) or not 0 <= cheatTarget < 52):
            self.d_cheatResponse(seatIndex, cheatType, cheatTarget, 0, list(hand))
            return

        inv = self.air.inventoryManager.getInventory(avatar.doId)
        cardType = InventoryType.begin_Cards + cheatTarget
        quantity = inv.getStackQuantity(cardType) if inv else 0
        if quantity <= 0:
            self.air.logPotentialHacker(
                message='Requested blackjack card swap with card not in inventory',
                targetAvId=avatar.doId,
                cardId=cheatTarget)

            self.d_cheatResponse(seatIndex, cheatType, cheatTarget, 0, list(hand))
            return

        inv.b_setStackQuantity(cardType, quantity - 1)
        hand[cardIndex] = cheatTarget
        self._cheaters[seatIndex] = cheatTarget

        if self._isCardDuplicated(cheatTarget):
            # the swapped card is already showing on the table, the
            # dealer spots it straight away.
            self._caughtCheating.add(seatIndex)
            self._takeChips(seatIndex, self.CheatingFine)
            self.d_cheatResponse(seatIndex, PlayingCardGlobals.CaughtCheating, cheatTarget, 0, list(hand))
            return

        self.d_cheatResponse(seatIndex, cheatType, cheatTarget, 1, list(hand))
        self.d_setTableState()

        # the player's turn timer restarts with the swapped hand
        taskMgr.remove(self.uniqueName('bj-action'))
        taskMgr.doMethodLater(PlayingCardGlobals.AskCardTimeout + self.TimeoutPadding,
            self._playerActionTimeoutTask, self.uniqueName('bj-action'),
            extraArgs=[seatIndex], appendTask=True)

    def _isCardDuplicated(self, card):
        count = 0
        for seatHands in self._allHands:
            for hand in seatHands:
                count += hand.count(card)

        if self._dealerHoleCard == card:
            count += 1

        return count > 1

    def _checkForCheaters(self):
        for seatIndex, card in list(self._cheaters.items()):
            if seatIndex in self._caughtCheating:
                continue

            if self._isCardDuplicated(card):
                self._caughtCheating.add(seatIndex)
                self._takeChips(seatIndex, self.CheatingFine)
                if self.isPlayerSeat(seatIndex):
                    hand = self._getCurrentHand(seatIndex)
                    self.d_cheatResponse(seatIndex, PlayingCardGlobals.CaughtCheating, card, 0, list(hand))

    def _handValue(self, hand):
        return PlayingCardGlobals.getBlackjackHandValue(
            [card for card in hand if card != PlayingCardGlobals.Unknown])

    def _isBlackjack(self, hand):
        if len(hand) != 2:
            return False

        return self._handValue(hand) == 21

    def _isSplittable(self, hand):
        # mirrors BlackjackTableGUI.splitableHand on the client
        rank1 = hand[0] % 13
        rank2 = hand[1] % 13
        if rank1 == rank2:
            return True

        return 8 <= rank1 <= 11 and 8 <= rank2 <= 11

    def announceGenerate(self):
        DistributedGameTableAI.announceGenerate(self)
        self._seedAIChips()
        self._scheduleRoundStart(delay=2.0)
