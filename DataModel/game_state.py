import random
import copy
# Modules
from DataModel import player, metadata, score, carpet, trump
from DataModel import card as card_module

# Classes
from DataModel.trump import Trump
from DataModel.bid import Bid
from DataModel.metadata import Metadata
from DataModel.score import Score
from DataModel.carpet import Carpet


def deal_cards(players):
    deck = card_module.get_deck()

    random.shuffle(deck)

    card_count = len(deck)
    player_count = len(players)
    for i in range(card_count):
        player_number = i % player_count
        players[player_number].cards.append(deck[i])

    return players  # Not needed. But, helps in placing debug point.


class GameState:
    def __init__(self):
        # META DATA
        self.winning_team = -1
        self.metadata = Metadata()

        self.players = []
        self.can_ask_for_trump = False  # TODO : Okay to have it at GameState level instead of inside every player?
        self.next_player = 0

        # BID, SCORE, AND TRUMP
        self.bid = Bid()
        self.score = Score()
        self.TrumpCard = Trump()

        self.players = player.create_players(self.metadata.playerCount)

        deal_cards(self.players)
        self.valid_cards = [card.id for card in self.players[self.next_player].cards]

        self.carpet = Carpet()
        self.rounds_history = []
        self.move = -1  # Flimsy.

    def populate_test_values(self):
        self.carpet.North = self.players[0].cards[2]
        self.carpet.East = self.players[1].cards[3]
        self.carpet.South = self.players[2].cards[5]

        trump = self.players[0].cards[4]
        self.TrumpCard = trump()

        self.TrumpCard.suite = trump.suite
        self.TrumpCard.number = trump.number
        self.TrumpCard.id = trump.id

        self.TrumpCard.is_trump_revealed = False
        self.TrumpCard.is_trump_set = True
        self.TrumpCard.trump_setter = 2
        self.TrumpCard.closed = True

        self.score.chasingTeam = "N&S"
        self.score.TargetPoints = 600
        self.score.HorizontalPoints = 360
        self.score.VerticalTeamPoints = 93

    def alter_state(self):
        move = self.move
        state = self.metadata.game_phase  # Metadata.GamePhase(self.metadata.game_phase)
        current_player = self.next_player  # TODO : Are we doing a -1 to the index ?

        # BIDDING PHASE
        if state == metadata.GamePhase.Bidding.value:
            self.bid.add_bid(move, current_player)
            target, setter = self.bid.get_trump_setter_and_target()

            # Bidding closes
            if setter != -1:
                # Assign the score values.
                self.score = Score.initial_score(target, setter % 2)  # str(setter) + " and " + str((setter + 2) % 4)

                # Change to Trump Selection Step
                self.metadata.game_phase = metadata.GamePhase.TrumpSelection.value
                self.next_player = setter
                self.valid_cards = [card.id for card in self.players[setter].cards]

            else:
                self.next_player = (current_player+1) % 4

        # TRUMP SELECTION STEP
        elif state == metadata.GamePhase.TrumpSelection.value:

            # Assign trump card and remove from the player's hand.
            card_for_trump = [card for card in self.players[current_player].cards if card.id == move][0]
            self.players[current_player].cards.remove(card_for_trump)
            self.TrumpCard = Trump.trump_from_card(card_for_trump, current_player)

            # Change to Playing Phase
            self.metadata.game_phase = metadata.GamePhase.Playing.value

            # Create the ambience for Round 1.
            self.next_player = (current_player - 1) % 4
            self.carpet = Carpet.carpet_starter(self.next_player)
            self.can_ask_for_trump = False
            self.valid_cards = [card.id for card in self.players[self.next_player].cards]

        # CARD PLAYING PHASE
        elif state == metadata.GamePhase.Playing.value:

            if move == "askForTrump":
                # ASK FOR TRUMP - Reveal trump, return trump to setter's hand, set can_ask_for_trump flag to false.

                self.TrumpCard.closed = False
                self.TrumpCard.is_trump_revealed = True
                # TODO: This is a duplicate, but not sure which flag UX consumes.

                trump_copy = copy.deepcopy(self.TrumpCard)
                trump_copy.__class__ = card_module.Card
                trump_setter = self.TrumpCard.trump_setter
                self.players[trump_setter].cards.append(trump_copy)

                self.can_ask_for_trump = False
                # Nothing changes with respect to the cards the player can play.
                # WRONG ! Make the trump a valid card if the setter asked for it to be revealed.

            else:
                # PLAY CARD
                # 1. Add card to the carpet and remove from player's hand.
                card_to_play = [card for card in self.players[current_player].cards if card.id == move][0]
                self.carpet.add_card(current_player, card_to_play)
                self.players[current_player].cards.remove(card_to_play)

                # 2. Check for round completion
                if self.carpet.is_round_over():
                    winner, win_value = self.carpet.compute_winner(self.TrumpCard.is_trump_revealed,
                                                                   self.TrumpCard.suite)

                    # Update Score
                    points = self.carpet.get_points()
                    winning_team = winner % 2

                    self.score.add_points(winning_team, self.carpet)
                    self.score.set_winning_team()

                    # Update history
                    carpet_copy = copy.deepcopy(self.carpet)
                    self.rounds_history.append(carpet_copy)

                    # 2a. Check for game completion and create new round if not.
                    if len(self.rounds_history) == 8:
                        self.metadata.game_phase = metadata.GamePhase.Over.value
                    else:
                        self.next_player = winner
                        self.carpet = Carpet.carpet_starter(winner)
                        self.can_ask_for_trump = False
                        self.valid_cards = [card.id for card in self.players[winner].cards]

                else:

                    self.next_player = (current_player + 1) % 4
                    self.valid_cards = [card.id for card in self.players[self.next_player].cards
                                        if card.suite == self.carpet.suite]

                    # Colour cut-off
                    if len(self.valid_cards) == 0:
                        # Can ask for trump if it's not revealed.
                        self.can_ask_for_trump = not self.TrumpCard.is_trump_revealed
                        # Can play any card
                        self.valid_cards = [card.id for card in self.players[self.next_player].cards]

        self.move = -1
