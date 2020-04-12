import enum


class GamePhase(enum.Enum):
    Bidding = 1
    TrumpSelection = 2
    Playing = 3
    Over = 4


class Metadata:
    def __init__(self):
        self.game_phase = GamePhase.Bidding.value
        self.playerCount = 4
        self.winner = -1
