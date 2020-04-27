from unittest import TestCase

#Internal dependencies
from DataModel import game_state, player, card


class Test(TestCase):

    def test_create_card(self):
        one_card = card.Card(card.Number.Jack, card.Suite.Hearts)

        assert one_card is not None
        assert one_card.number == card.Number.Jack
        assert one_card.suite == card.Suite.Hearts

    def test_create_deck(self):
        deck = card.get_deck()

        assert deck is not None
        # Check for 32 cards
        assert len(deck) == 32

        # Check for 8 clover cards.
        clovers = sum(x.suite == card.Suite.Clover for x in deck)
        assert clovers == 8
        # Check for 4 Queens.
        queens = sum(x.number == card.Number.Queen for x in deck)
        assert queens == 4

    def test_get_significant_cards(self):
        cards = card.get_significant_cards()

        assert cards is not None

        assert len(cards) == 16

        # Check for 4 cards in spade.
        spades = sum(x.suite == card.Suite.Clover for x in cards)
        assert spades == 4

        # Check for 4 Jacks
        jacks = sum(x.number == card.Number.Jack for x in cards)
        assert jacks == 4

        # Check for no Kings
        kings = sum(x.suite == card.Number.King for x in cards)
        assert kings == 0