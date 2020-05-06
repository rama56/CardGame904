import enum
import random
import weakref

from DataModel import card
from DataModel.game_state import *
from DataModel.metadata import GamePhase
from Intelligence import belief
from Intelligence.belief import Belief


class Position(enum.Enum):
    North = 0
    East = 1
    South = 2
    West = 3
    Five = 4
    Six = 5


def create_players(player_count):
    _players = []
    for i in range(player_count):
        _player = Player("Player-" + str(i), Position(i), str((i % 2) + 1))
        _players.append(_player)
    return _players


class Player:
    def __init__(self, name, position, team):
        self.name = name
        self.position = position
        self.team = team

        # Set of 8 cards.
        self.cards = []

        self.can_ask_for_trump = False

        self.earning_capacity = 0
        self.trump_choice_card = None

        # Beliefs about Trump suit.
        # Beliefs about distribution of cards of other hands.
        self.belief = Belief(position.value)

    def suggest_move(self, game_state):
        _game_state = GameState()    # weakref.ref(game_state)
        _valid_cards = _game_state.valid_cards
        _bid = _game_state.bid
        _metadata = _game_state.metadata
        _phase = _metadata.game_phase

        if _phase == GamePhase.Bidding:
            self.earning_capacity, self.trump_choice_card = belief.get_strength(self.cards)
            if self.earning_capacity >= _bid.minimumNextBid:
                return self.earning_capacity
            else:
                return -1

        elif _phase == GamePhase.TrumpSelection:
            _trump_card_id = self.trump_choice_card.id
            assert _trump_card_id in _valid_cards
            return _trump_card_id

        elif _phase == GamePhase.Playing:
            # TODO: Think and do something.
            suggested_move = random.choice(_valid_cards)
            return suggested_move

        elif _phase == GamePhase.Over:
            a = 5
            # Throw exception??
        # end if else clauses
    # end suggest_move()

    def rethink_belief(self, game_state, scenario, move, move_by):
        _game_state = game_state  # weakref.ref(game_state) # GameState() #
        _common_knowledge = _game_state.common_knowledge

        if scenario == "CardsDealt":
            self.belief.my_hand_cards(self.cards, _common_knowledge)
        elif scenario == "CardPlayed":
            # TODO : Looks like only truth is used to update beliefs. Try some rationality assumptions.
            _current_player = move_by
            _card_played_id = move.id   # _card_played_eng = move.eng ENG_TO_ID
            self.belief.has_card(_card_played_id, _current_player)

            # Check if there was a colour cut-off.
            _carpet = _game_state.carpet
            if move.suite != _carpet.suite:
                self.belief.not_has_suite(_current_player, _carpet.suite)

        elif scenario == "BidPlaced":
            if move_by == self.position.value:
                # If I'm the bidder, there's nothing to alter my belief with.
                return
            if move == -1:
                min_bid = _game_state.bid.minimumNextBid
                if self.belief.bid_strength[move_by] is None:
                    self.belief.bid_strength[move_by] = (0, min_bid - 10)

                else:
                    return
                    # Already range is set. The player passing this time doesn't reveal anything.
            else:
                # Some proper bid has come in.
                self.belief.bid_strength[move_by] = (move - 20, move + 20)

        elif scenario == "BiddingOver":
            # Bidding is over. With the known player ranges, alter nature_hands
            self.belief.bidding_over()

        elif scenario == "TrumpRevealed":
            # TODO : subsequently about
            #  nature_cards ?
            _trump_setter = move_by
            _card_played_id = move.id
            if _trump_setter == self.position.value:
                # If I'm the trump setter, there's nothing to alter my belief about with revelation of
                # my trump.
                return
            else:
                self.belief.trump_revealed(_trump_setter, _card_played_id)
                # self.belief.has_card(_card_played_id, _trump_setter)
                # TODO: re-enable this. throws an exception, when
                #  card is actually played.

            return

    # end rethink_belief()
