import unittest
from types import SimpleNamespace

from pirates.minigame import PlayingCardGlobals
from pirates.minigame.PlayingCard import PlayingCardBase


class PlayingCardTests(unittest.TestCase):
    # a card's value is suit * 13 + rank, both used as indices into the card images

    def test_suit_and_rank_are_whole_numbers(self):
        for value in range(52):
            card = PlayingCardBase(value)
            self.assertEqual(card.getSuit(), value // 13)
            self.assertEqual(card.getRank(), value % 13)
            self.assertIsInstance(card.getSuit(), int)

        # the card that crashed the poker table, 41 / 13 came out as 3.1538...
        card = PlayingCardBase(41)
        self.assertEqual((card.getSuit(), card.getRank()), (3, 2))

    def test_unknown_card_has_no_suit(self):
        card = PlayingCardBase.__new__(PlayingCardBase)
        card.faceUp = 1
        card.turnDown = lambda: None
        card.setValue(PlayingCardGlobals.Unknown)
        self.assertIsNone(card.getSuit())


class BlackjackBidTests(unittest.TestCase):

    def test_bids_are_whole_multiples_of_five(self):
        from pirates.minigame.BlackjackTableGUI import BlackjackTableGUI
        gui = BlackjackTableGUI.__new__(BlackjackTableGUI)
        gui.table = SimpleNamespace(betMultiplier=1)
        self.assertEqual(gui.sliderValueToBid(0.5), 25)
        self.assertEqual(gui.sliderValueToBid(0.33), 15)
        self.assertEqual(gui.sliderValueToBid(0.0), 2)
        self.assertIsInstance(gui.sliderValueToBid(0.33), int)


if __name__ == '__main__':
    unittest.main()
