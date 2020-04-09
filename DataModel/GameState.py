import random

# Modules
from DataModel import Player, Card

# Classes
from DataModel.Trump import Trump
from DataModel.Bid import Bid
from DataModel.Metadata import Metadata
from DataModel.Score import Score
from DataModel.Carpet import Carpet

def deal_cards(players):

    deck = Card.get_deck()

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
        self.metadata = Metadata()

        self.players = []
        self.next_player = 1

        # BID, SCORE, AND TRUMP
        self.bid = Bid()
        self.score = Score()
        self.TrumpCard = Trump()

        self.players = Player.create_players(self.metadata.playerCount)

        deal_cards(self.players)
        self.valid_cards = [card.id for card in self.players[self.next_player-1].cards]

        self.carpet = Carpet()
        self.move = -1  # Flimsy.

    def alter_state(self):
        move = self.move
        # Using move, alter the state and return
