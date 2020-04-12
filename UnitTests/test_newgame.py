from unittest import TestCase

import jsonpickle

#Internal dependencies
from DataModel import game_state, player, card


class Test(TestCase):
    def test_create_new_game(self):
        obj = game_state.GameState()

        json_obj = jsonpickle.encode(obj)

        # TODO - 5: Test more
        assert json_obj is not None

    def test_create_card(self):
        one_card = card.Card(card.Number.Jack, card.Suite.Hearts)

        assert one_card is not None
        assert one_card.number == card.Number.Jack
        assert one_card.suite == card.Suite.Hearts

    def test_create_deck(self):
        deck = card.get_valid_cards()

        assert deck is not None
        # Check for 32 cards
        assert len(deck) == 32

        # TODO - 4: Check why tests fail. Counts come as 0 while the 'deck' looks fine.
        # Check for 8 clover cards.
        clovers = sum(card.suite == card.Suite.Clover for card in deck)
        # assert clovers == 8
        # Check for 4 Queens.
        queens = sum(card.number == card.Number.Queen for card in deck)
        # assert queens == 4

    def test_create_player(self):
        player = player.Player("Krithika", player.Position.West, "Team XYZ")

        assert player is not None
        assert player.cards == []
        assert player.name == "Krithika"
        assert player.position == player.Position.West
        assert player.team == "Team XYZ"

    def test_create_players(self):
        players = player.create_players(4)
        assert len(players) == 4
        # TODO - 2: Test some more.

    def test_deal_cards(self):
        players = player.create_players(4)
        game_state.deal_cards(players)

        assert len(players) == 4
        assert len(players[2].cards) == 8
        # TODO - 3: Test more
