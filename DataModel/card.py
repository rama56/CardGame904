# importing enum for enumerations
import enum
import math

value_points_mapping = {1: 2, 2: 3, 3: 10, 4: 11, 5: 20, 6: 30, 7: 50, 8: 100}

eng_id_mapping = {'QueenSpade': 1, 'KingSpade': 2, 'TenSpade': 3, 'AceSpade': 4, 'NineSpade': 5, 'JackSpade': 6, 'ThreeSpade': 7,  'TwoSpade': 8,
                  'QueenHearts': 9, 'KingHearts': 10, 'TenHearts': 11, 'AceHearts': 12, 'NineHearts': 13, 'JackHearts': 14, 'ThreeHearts': 15,  'TwoHearts': 16,
                  'QueenDice': 17, 'KingDice': 18, 'TenDice': 19, 'AceDice': 20, 'NineDice': 21, 'JackDice': 22, 'ThreeDice': 23,  'TwoDice': 24,
                  'QueenClover': 25, 'KingClover': 26, 'TenClover': 27, 'AceClover': 28, 'NineClover': 29, 'JackClover': 30, 'ThreeClover': 31,  'TwoClover': 32}


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


def get_card_from_eng(eng):
    _id = eng_id_mapping[eng]
    return get_card_from_id(_id)


def is_sig_card_eng(c_str):
    c = get_card_from_eng(c_str)
    return c.is_significant_card()


# TODO: Make this an overloaded constructor.
def get_card_from_id(card_id):
    card_id = card_id - 1
    number = (card_id % 8) + 1
    suite = math.floor(card_id/8)
    card = Card(Number(number), Suite(suite))
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


def get_remaining_cards_engs(cards_engs):
    full_deck = get_deck()
    remaining_cards = [card.eng for card in full_deck if card.eng not in cards_engs]

    return remaining_cards


def get_remaining_cards(cards):
    cards_ids = [x.id for x in cards]
    full_deck = get_deck()
    remaining_cards = [card for card in full_deck if card.id not in cards_ids]

    return remaining_cards
