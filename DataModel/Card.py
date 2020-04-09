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
    # Eight = 0


class Suite(enum.Enum):
    Spade = 1
    Hearts = 2
    Dice = 3
    Clover = 4


class Card():
    def __init__(self, number, suite):
        self.number = number
        self.suite = suite
        # TODO - 1 : REMOVE MAGIC NUMBERS. ACCOMMODATE FOR 9 IN 6-PLAYER GAME IN FRONT-END RESOURCES.
        self.id = (suite.value - 1) * 8 + number.value


def get_deck():
    valid_cards = []
    for suit in Suite:
        for number in Number:
            card = Card(number, suit)
            valid_cards.append(card)
    return valid_cards
