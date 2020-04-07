
import enum

class Position(enum.Enum):
    North = 1,  # Top
    East = 2,   # Right
    South = 3,  # Bottom
    West = 4    # Left

class Player():
    def __init__(self, name, position, team):
        self.name = name
        self.position = position
        self.team = team

        # More private variables like

        # Set of 8 cards.

        # Beliefs about Trump suit.

        # Beliefs about distribution of cards of other hands.
