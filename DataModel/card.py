# importing enum for enumerations
import enum
import math

value_points_mapping = {1: 2, 2: 3, 3: 10, 4: 11, 5: 20, 6: 30, 7: 50, 8: 100}


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
    Spade = 0
    Hearts = 1
    Dice = 2
    Clover = 3


class Card:
    def __init__(self, number, suite):
        self.number = number
        self.suite = suite
        # TODO - 1 : REMOVE MAGIC NUMBERS. ACCOMMODATE FOR 9 IN 6-PLAYER GAME IN FRONT-END RESOURCES.
        self.id = suite.value * 8 + number.value
        self.closed = False

        self.eng = self.number.name + self.suite.name

    def get_points(self):
        return value_points_mapping[self.number]

    def is_significant_card(self):
        # return self.number >= Number.Three
        return self.number >= Number.Nine


# TODO: Make this an overloaded constructor.
def get_card_from_id(card_id):
    number = card_id % 8
    suite = math.floor(card_id/8)
    card = Card(number, suite)
    return card


def get_deck():
    valid_cards = []
    for suit in Suite:
        for number in Number:
            card = Card(number, suit)
            valid_cards.append(card)
    return valid_cards


def get_significant_cards():
    full_deck = get_deck()
    high_value_cards = [card for card in full_deck if card.is_significant_card()]
    return high_value_cards


# Dealing in terms of eng here.
def get_remaining_significant_cards(cards_engs):
    sig_cards = get_significant_cards()
    remaining_sig_cards = [card.eng for card in sig_cards if card.eng not in cards_engs]

    return remaining_sig_cards


def get_remaining_cards(cards):
    cards_ids = [x.id for x in cards]
    full_deck = get_deck()
    remaining_cards = [card for card in full_deck if card.id not in cards_ids]

    return remaining_cards
