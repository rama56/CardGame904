import enum


class Position(enum.Enum):
    North = 1
    East = 2
    South = 3
    West = 4
    Five = 5
    Six = 6


class Player():
    def __init__(self, name, position, team):
        self.name = name
        self.position = position
        self.team = team

        # More private variables like

        # Set of 8 cards.
        self.cards = []
        # Beliefs about Trump suit.

        # Beliefs about distribution of cards of other hands.


def create_players(player_count):
    players = []
    for i in range(player_count):
        player = Player("Player-" + str(i), Position(i + 1), str((i % 2) + 1))
        players.append(player)
    return players
