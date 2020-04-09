import enum


class GamePhase(enum.Enum):
    Bidding = 1
    Playing = 2
    Over = 3


class Metadata:
    def __init__(self):
        self.game_phase = GamePhase.Bidding
        self.playerCount = 4
        self.winner = -1
