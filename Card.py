# importing enum for enumerations
import enum


# creating enumerations using class
class Number(enum.IntEnum):
    Two = 8
    Three = 7
    Jack = 6
    Nine = 5
    Ace = 4
    Ten = 3
    King = 2
    Queen = 1


class Suite(enum.Enum):
    Spade = 1
    Hearts = 2
    Dice = 3
    Clover = 4


class Card():
    def __init__(self, number, suite):
        self.number = number
        self.suite = suite
        # TODO: REMOVE MAGIC NUMBERS
        self.id = suite.value * 9 + number.value

def get_valid_cards():
    valid_cards = []
    for suit in Suite:
        for number in Number:
            card = Card(suit, number)
            valid_cards.append(card)
    return valid_cards
