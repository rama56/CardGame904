# importing enum for enumerations
import enum

# creating enumerations using class
class Number(enum.IntEnum):
    Two = 100,
    Three = 11,
    Jack = 30,
    Nine = 20,
    Ace = 11,
    Ten = 10,

class Suite(enum.Enum):
    Spade = 1,
    Hearts = 2,
    Dice = 3,
    Clover = 4,

class Card():
    def __init__(self, num, suite):
        self.num = num
        self.suite = suite
