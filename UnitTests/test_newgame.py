from unittest import TestCase

import jsonpickle

#Internal dependencies
from DataModel import game_state, player, card
from DataModel.player import Player


class Test(TestCase):
    def test_create_new_game(self):
        obj = game_state.GameState()

        json_obj = jsonpickle.encode(obj)

        # TODO - 5: Test more
        assert json_obj is not None

    def test_create_player(self):
        player = Player("Krithika", Player.Position.West, "Team XYZ")

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
