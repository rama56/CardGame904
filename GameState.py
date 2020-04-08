import random

import Card
import Player


def deal_cards(players):

    valid_cards = Card.get_valid_cards()

    random.shuffle(valid_cards)

    card_count = len(valid_cards)
    player_count = len(players)
    for i in range(card_count):
        player_number = i % player_count
        players[player_number].cards.append(valid_cards[i])

    return players  # Not needed. But, helps in placing debug point.


class GameState:
    def __init__(self):
        # CREATE A NEW GAME STATE.

        # META DATA
        self.isGameRunning = True
        self.playerCount = 4
        self.players = []
        self.winner = -1

        # BID DATA
        self.bidProgression = []
        self.maxBid = -1
        self.minimumNextBid = -1
        self.TrumpCard = -1

        # Add other variables for cards dealt, points earned etc.
        self.players = Player.create_players(self.playerCount)
        self.bidStarter = self.players[0].position

        deal_cards(self.players)
