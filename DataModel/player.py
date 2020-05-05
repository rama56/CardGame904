import enum
import random

from DataModel import card
from DataModel.game_state import *
from DataModel.metadata import GamePhase
from Intelligence.belief import Belief


class Position(enum.Enum):
    North = 0
    East = 1
    South = 2
    West = 3
    Five = 4
    Six = 5


def create_players(player_count):
    players = []
    for i in range(player_count):
        player = Player("Player-" + str(i), Position(i), str((i % 2) + 1))
        players.append(player)
    return players


class Player:
    def __init__(self, name, position, team):
        self.name = name
        self.position = position
        self.team = team

        # Set of 8 cards.
        self.cards = []

        self.can_ask_for_trump = False

        # Beliefs about Trump suit.
        # Beliefs about distribution of cards of other hands.
        self.belief = Belief(position.value)

    # def suggest_move(self):
    #     _valid_cards = self.game_state.valid_cards
    #     _bid = self.game_state.bid
    #     _metadata = self.game_state.metadata
    #     _phase = _metadata.game_phase
    #
    #     if _phase == GamePhase.Bidding:
    #         earning_capacity = self.belief.get_capacity(self.cards)
    #         min_bid = _bid.minimumNextBid
    #         if earning_capacity >= min_bid:
    #             return earning_capacity
    #
    #     suggested_move = random.choice(_valid_cards)
    #     return suggested_move

    def rethink_belief(self, scenario, common_knowledge):
        if scenario == "CardsDealt":
            self.belief.my_hand_cards(self.cards, common_knowledge)
        elif scenario == "CardPlayed":
            a = 5
            # something
